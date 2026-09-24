import time
from fastapi import APIRouter, HTTPException
from models.structured import StructuredRequest, StructuredAnswer
from graph.workflow import app_workflow
from core.config import settings

router = APIRouter()

@router.post("/", response_model=StructuredAnswer)
async def structured_chat(request: StructuredRequest):
    """
    Structured chat endpoint using LangGraph.
    Validates output, retries automatically, and returns valid JSON.
    """
    try:
        model_name = request.model or settings.DEFAULT_MODEL
        
        initial_state = {
            "question": request.message,
            "model_name": model_name,
            "retry_count": 0,
            "error": None
        }
        
        # Run the workflow
        result = await app_workflow.ainvoke(initial_state)
        
        # Extract the parsed answer
        parsed_json = result.get("parsed_json")
        if not parsed_json:
            raise HTTPException(status_code=500, detail="Workflow failed to produce a structured answer.")
            
        return parsed_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
