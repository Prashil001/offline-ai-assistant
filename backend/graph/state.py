from typing import TypedDict, Optional, Any
from models.structured import StructuredAnswer

class GraphState(TypedDict):
    """
    State for the LangGraph workflow.
    """
    question: str
    model_name: str
    raw_response: Optional[str]
    parsed_json: Optional[StructuredAnswer]
    error: Optional[str]
    retry_count: int
