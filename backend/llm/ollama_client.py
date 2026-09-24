import time
import logging
from typing import AsyncGenerator
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from core.config import settings

logger = logging.getLogger(__name__)

def get_llm(model: str = settings.DEFAULT_MODEL) -> ChatOllama:
    """Returns a ChatOllama instance configured with the specified model."""
    return ChatOllama(
        model=model,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.7,
    )

async def generate_chat_response(message: str, model: str) -> dict:
    """Generates a full response from the LLM."""
    llm = get_llm(model)
    start_time = time.time()
    
    try:
        response = await llm.ainvoke([HumanMessage(content=message)])
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        return {
            "response": response.content,
            "model": model,
            "latency_ms": latency_ms
        }
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise

async def generate_chat_stream(message: str, model: str) -> AsyncGenerator[str, None]:
    """Generates a streaming response from the LLM."""
    llm = get_llm(model)
    try:
        async for chunk in llm.astream([HumanMessage(content=message)]):
            yield chunk.content
    except Exception as e:
        logger.error(f"Error streaming response: {e}")
        yield f"Error: {str(e)}"
