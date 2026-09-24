# System Architecture

## Overview
This offline AI Assistant is built using a modern, scalable microservice architecture. All inference runs locally.

```mermaid
graph TD
    UI[React + Vite UI] -->|HTTP/REST| API[FastAPI Backend]
    
    subgraph Backend
        API --> DB[(SQLite)]
        API --> LG[LangGraph State Machine]
        LG --> LLM[Ollama Local Engine]
        
        API --> RAG[RAG Pipeline]
        RAG --> Chroma[(ChromaDB Vector Store)]
        RAG --> LG
        
        API --> BM[Benchmark Engine]
        BM --> psutil[OS Metrics Tracker]
        BM --> LG
    end
```

## LangGraph Workflow
Our robust state machine ensures JSON integrity via cyclic retries.

```mermaid
stateDiagram-v2
    [*] --> Retrieve
    Retrieve --> Generate: Inject Context
    Generate --> Validate: Raw String
    Validate --> Generate: Schema Mismatch (Count < 3)
    Validate --> [*]: Valid JSON
    Validate --> Fallback: Retry Limit Exceeded
    Fallback --> [*]
```
