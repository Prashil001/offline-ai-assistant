from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.chat import ChatRequest, ChatResponse
from database.session import get_db
from database.models import Conversation, Message
from llm.ollama_client import generate_chat_response, generate_chat_stream
from core.config import settings

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Chat endpoint.
    If stream=True, returns a StreamingResponse.
    Otherwise, returns a ChatResponse with full text and latency.
    """
    try:
        model_name = request.model or settings.DEFAULT_MODEL
        
        # Handle Conversation
        conv_id = request.conversation_id
        if not conv_id:
            new_conv = Conversation(title=request.message[:50])
            db.add(new_conv)
            await db.commit()
            await db.refresh(new_conv)
            conv_id = new_conv.id
        
        # Save user message
        user_msg = Message(
            conversation_id=conv_id,
            role="user",
            content=request.message
        )
        db.add(user_msg)
        await db.commit()

        if request.stream:
            # We would typically save streamed response to DB after completion.
            # For simplicity in this streaming wrapper, we will create a generator
            # that intercepts the chunks and saves to DB when done.
            async def streaming_wrapper():
                full_text = ""
                async for chunk in generate_chat_stream(request.message, model_name):
                    full_text += chunk
                    yield chunk
                
                # Save assistant message
                assistant_msg = Message(
                    conversation_id=conv_id,
                    role="assistant",
                    content=full_text,
                    model=model_name
                )
                db.add(assistant_msg)
                await db.commit()

            return StreamingResponse(
                streaming_wrapper(),
                media_type="text/plain",
                headers={"X-Conversation-ID": conv_id}
            )
        
        result = await generate_chat_response(request.message, model_name)
        
        # Save assistant message
        assistant_msg = Message(
            conversation_id=conv_id,
            role="assistant",
            content=result["response"],
            model=model_name,
            latency_ms=result["latency_ms"]
        )
        db.add(assistant_msg)
        await db.commit()

        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_history(db: AsyncSession = Depends(get_db)):
    """Fetch all conversations."""
    result = await db.execute(select(Conversation).order_by(Conversation.created_at.desc()))
    conversations = result.scalars().all()
    return conversations

@router.get("/history/{conversation_id}")
async def get_conversation(conversation_id: str, db: AsyncSession = Depends(get_db)):
    """Fetch messages for a specific conversation."""
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()
    return messages
