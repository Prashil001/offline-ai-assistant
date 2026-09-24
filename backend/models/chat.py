from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message")
    conversation_id: Optional[str] = Field(None, description="ID of the conversation to append to")
    model: Optional[str] = Field(None, description="The model to use")
    stream: bool = Field(False, description="Whether to stream the response")

class ChatResponse(BaseModel):
    response: str
    model: str
    latency_ms: Optional[float] = None
