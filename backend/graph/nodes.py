import json
import logging
from langchain_core.messages import HumanMessage
from graph.state import GraphState
from models.structured import StructuredAnswer
from llm.ollama_client import get_llm
from rag.vector_store import retrieve_context
from pydantic import ValidationError

logger = logging.getLogger(__name__)

async def retrieve_node(state: GraphState) -> GraphState:
    """Retrieves context from ChromaDB based on the question."""
    logger.info("Node: retrieve")
    try:
        docs = retrieve_context(state["question"])
        context = "\n\n".join([f"Source ({doc.metadata.get('source_file', 'unknown')}):\n{doc.page_content}" for doc in docs])
        return {"context": context}
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        return {"context": "No context available."}

async def generate_node(state: GraphState) -> GraphState:
    """Generates the response from the LLM."""
    logger.info("Node: generate")
    llm = get_llm(state["model_name"]).bind(format="json")
    
    prompt = f"""
    You are an AI assistant. Answer the user's question using the provided context.
    If the context doesn't contain the answer, say so, but still output valid JSON.
    
    You MUST output VALID JSON matching exactly this schema:
    {{
        "answer": "your answer here",
        "confidence": 0.95,
        "sources": ["source file 1", "source file 2"]
    }}
    
    Do not output any markdown formatting, only the JSON object.
    
    Context:
    {state.get('context', 'No context provided.')}
    
    Question: {state['question']}
    """
    
    if state.get("error"):
        prompt += f"\n\nPREVIOUS ERROR (fix this): {state['error']}\nPREVIOUS OUTPUT: {state['raw_response']}"
        
    messages = [HumanMessage(content=prompt)]
    
    response = await llm.ainvoke(messages)
    
    return {
        "raw_response": response.content,
        "retry_count": state.get("retry_count", 0)
    }

async def validate_node(state: GraphState) -> GraphState:
    """Validates the JSON output against the Pydantic schema."""
    logger.info("Node: validate")
    raw_response = state.get("raw_response", "")
    
    try:
        # Simple extraction in case LLM wraps it in markdown blocks
        if "```json" in raw_response:
            json_str = raw_response.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_response:
            json_str = raw_response.split("```")[1].split("```")[0].strip()
        else:
            json_str = raw_response.strip()
            
        parsed = json.loads(json_str)
        validated = StructuredAnswer(**parsed)
        
        return {
            "parsed_json": validated,
            "error": None
        }
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format: {str(e)}"
        logger.warning(error_msg)
        return {
            "error": error_msg,
            "retry_count": state.get("retry_count", 0) + 1
        }
    except ValidationError as e:
        error_msg = f"JSON does not match schema: {str(e)}"
        logger.warning(error_msg)
        return {
            "error": error_msg,
            "retry_count": state.get("retry_count", 0) + 1
        }
