from pydantic import BaseModel, Field
from typing import List, Optional

class StructuredAnswer(BaseModel):
    answer: str = Field(description="The detailed answer to the user's question.")
    confidence: float = Field(description="A confidence score between 0.0 and 1.0", ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list, description="List of sources or reasoning steps.")

class StructuredRequest(BaseModel):
    message: str = Field(..., description="The user's message")
    model: Optional[str] = Field(None, description="The model to use")
