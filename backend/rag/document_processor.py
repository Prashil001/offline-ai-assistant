import tempfile
import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_file(file_path: str, filename: str):
    """Loads a file, extracts text, and chunks it."""
    ext = filename.split(".")[-1].lower()
    
    if ext == "pdf":
        loader = PyMuPDFLoader(file_path)
    elif ext in ["txt", "md"]:
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload PDF, TXT, or MD.")
        
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    splits = text_splitter.split_documents(docs)
    
    # Add metadata
    for split in splits:
        split.metadata["source_file"] = filename
        
    return splits
