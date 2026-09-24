from fastapi import APIRouter
from api.endpoints import chat, structured_chat, documents, benchmarks

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(structured_chat.router, prefix="/structured", tags=["structured"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(benchmarks.router, prefix="/benchmarks", tags=["benchmarks"])
