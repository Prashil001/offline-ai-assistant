import os
import tempfile
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File
from rag.document_processor import process_file
from rag.vector_store import add_documents_to_store

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a document, extracts text, chunks it, and stores embeddings in ChromaDB.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
        
    try:
        # Create a temporary file to save the uploaded content
        suffix = f".{file.filename.split('.')[-1]}"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Process the file
        splits = process_file(tmp_path, file.filename)
        
        # Add to vector store
        add_documents_to_store(splits)
        
        # Cleanup
        os.remove(tmp_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_added": len(splits)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
