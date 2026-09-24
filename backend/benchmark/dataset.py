import json
import os

# We will provide a subset of the dataset for demonstration purposes.
# In a real scenario, this would be loaded from a JSON/CSV file.

BENCHMARK_DATASET = [
    {
        "id": "f1",
        "category": "factual",
        "difficulty": "easy",
        "question": "What is the capital of France?",
        "expected_answer_keywords": ["Paris"]
    },
    {
        "id": "r1",
        "category": "reasoning",
        "difficulty": "medium",
        "question": "If I have 3 apples and eat 1, then buy 5 more, how many apples do I have?",
        "expected_answer_keywords": ["7", "seven"]
    },
    {
        "id": "r2",
        "category": "reasoning",
        "difficulty": "hard",
        "question": "Solve for x: 2x + 5 = 15",
        "expected_answer_keywords": ["5", "five"]
    }
]

def get_benchmark_dataset():
    return BENCHMARK_DATASET
