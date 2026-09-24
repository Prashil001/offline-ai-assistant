import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from benchmark.engine import run_benchmark, RESULTS_DIR

router = APIRouter()

class BenchmarkRequest(BaseModel):
    models: List[str]

@router.post("/run")
async def execute_benchmark(request: BenchmarkRequest):
    """Triggers the benchmark engine for the specified models."""
    if not request.models:
        raise HTTPException(status_code=400, detail="No models specified.")
    
    try:
        results = await run_benchmark(request.models)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results")
async def get_results():
    """Retrieves all past benchmark results."""
    if not os.path.exists(RESULTS_DIR):
        return []
        
    results_list = []
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(RESULTS_DIR, filename)
            with open(filepath, "r") as f:
                data = json.load(f)
                results_list.append({"filename": filename, "data": data})
                
    # Sort by filename descending (newest first)
    results_list.sort(key=lambda x: x["filename"], reverse=True)
    return results_list
