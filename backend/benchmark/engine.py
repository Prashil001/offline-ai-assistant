import time
import psutil
import asyncio
import os
import json
from datetime import datetime
from graph.workflow import app_workflow
from benchmark.dataset import get_benchmark_dataset
import logging

logger = logging.getLogger(__name__)

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "benchmarks", "results")

async def run_single_eval(model_name: str, item: dict):
    """Runs a single evaluation against the LangGraph workflow."""
    start_time = time.time()
    
    # Measure initial resources
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss
    cpu_before = process.cpu_times().user
    
    initial_state = {
        "question": item["question"],
        "model_name": model_name,
        "retry_count": 0,
        "error": None
    }
    
    # First token latency tracking is tricky without streaming, 
    # but we will track full graph latency here for the structured workflow.
    
    try:
        result = await app_workflow.ainvoke(initial_state)
        parsed_json = result.get("parsed_json")
        raw_response = result.get("raw_response", "")
        
        valid_json = parsed_json is not None
        actual_answer = parsed_json.answer if parsed_json else raw_response
        
        # Simple accuracy check (keyword matching)
        accuracy = 0.0
        if any(keyword.lower() in actual_answer.lower() for keyword in item["expected_answer_keywords"]):
            accuracy = 1.0
            
    except Exception as e:
        logger.error(f"Error during eval: {e}")
        valid_json = False
        accuracy = 0.0
        
    end_time = time.time()
    latency = end_time - start_time
    
    mem_after = process.memory_info().rss
    cpu_after = process.cpu_times().user
    
    mem_used_mb = max(0, (mem_after - mem_before) / (1024 * 1024))
    cpu_used = max(0, cpu_after - cpu_before)
    
    return {
        "question_id": item["id"],
        "latency_s": latency,
        "mem_used_mb": mem_used_mb,
        "cpu_used_s": cpu_used,
        "valid_json": valid_json,
        "accuracy": accuracy
    }

async def run_benchmark(models: list[str]):
    """Runs the benchmark suite across specified models."""
    dataset = get_benchmark_dataset()
    results = {}
    
    for model in models:
        logger.info(f"Benchmarking model: {model}")
        model_results = []
        
        for item in dataset:
            logger.info(f"  Evaluating: {item['id']}")
            res = await run_single_eval(model, item)
            model_results.append(res)
            
        # Aggregate results
        avg_latency = sum(r["latency_s"] for r in model_results) / len(model_results)
        avg_mem = sum(r["mem_used_mb"] for r in model_results) / len(model_results)
        avg_cpu = sum(r["cpu_used_s"] for r in model_results) / len(model_results)
        json_success_rate = sum(1 for r in model_results if r["valid_json"]) / len(model_results)
        accuracy_rate = sum(r["accuracy"] for r in model_results) / len(model_results)
        
        results[model] = {
            "avg_latency_s": round(avg_latency, 2),
            "avg_mem_mb": round(avg_mem, 2),
            "avg_cpu_s": round(avg_cpu, 2),
            "json_success_rate": round(json_success_rate, 2),
            "accuracy_rate": round(accuracy_rate, 2),
            "details": model_results
        }
        
    # Save results to disk
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    file_path = os.path.join(RESULTS_DIR, f"benchmark_{timestamp}.json")
    
    with open(file_path, "w") as f:
        json.dump(results, f, indent=2)
        
    return {
        "timestamp": timestamp,
        "results": results
    }
