from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.chat import ChatRequest, ChatResponse
from llm.ollama_client import generate_chat_response, generate_chat_stream
from core.config import settings

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint.
    If stream=True, returns a StreamingResponse.
    Otherwise, returns a ChatResponse with full text and latency.
    """
    try:
        model_name = request.model or settings.DEFAULT_MODEL
        
        if request.stream:
            # We are using plain streaming for the basic version.
            # In production for a web app, Server-Sent Events (SSE) might be better.
            return StreamingResponse(
                generate_chat_stream(request.message, model_name),
                media_type="text/plain"
            )
        
        result = await generate_chat_response(request.message, model_name)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
