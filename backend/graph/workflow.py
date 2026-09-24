from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import generate_node, validate_node

MAX_RETRIES = 3

def route_validation(state: GraphState):
    """Route based on validation success or retry limit."""
    if state.get("error") is None:
        return END
    
    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "fallback"
    
    return "generate"

async def fallback_node(state: GraphState) -> GraphState:
    """Provides a safe fallback if generation fails."""
    from models.structured import StructuredAnswer
    return {
        "parsed_json": StructuredAnswer(
            answer="Sorry, I couldn't generate a valid structured response after multiple attempts.",
            confidence=0.0,
            sources=[]
        ),
        "error": None
    }

def create_workflow() -> StateGraph:
    workflow = StateGraph(GraphState)
    
    workflow.add_node("generate", generate_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("fallback", fallback_node)
    
    workflow.set_entry_point("generate")
    
    workflow.add_edge("generate", "validate")
    workflow.add_conditional_edges(
        "validate",
        route_validation,
        {
            "generate": "generate",
            "fallback": "fallback",
            END: END
        }
    )
    
    workflow.add_edge("fallback", END)
    
    return workflow.compile()

app_workflow = create_workflow()
