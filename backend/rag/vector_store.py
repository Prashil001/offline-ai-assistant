import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store():
    return Chroma(
        collection_name="assistant_docs",
        embedding_function=get_embeddings(),
        persist_directory=DB_DIR
    )

def add_documents_to_store(docs):
    vector_store = get_vector_store()
    vector_store.add_documents(docs)
    return True

def retrieve_context(query: str, k: int = 3):
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query, k=k)
    return docs
