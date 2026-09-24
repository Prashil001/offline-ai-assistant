import pytest
from benchmark.dataset import get_benchmark_dataset

def test_dataset_format():
    """Verify the dataset is formatted correctly for the engine."""
    dataset = get_benchmark_dataset()
    assert isinstance(dataset, list)
    assert len(dataset) > 0
    
    for item in dataset:
        assert "id" in item
        assert "question" in item
        assert "expected_answer_keywords" in item
        assert isinstance(item["expected_answer_keywords"], list)

def test_benchmark_api_validation():
    """Test that the benchmark API requires models."""
    from fastapi.testclient import TestClient
    from main import app
    
    test_client = TestClient(app)
    response = test_client.post("/api/v1/benchmarks/run", json={"models": []})
    
    assert response.status_code == 400
    assert "No models specified" in response.json()["detail"]
