# Offline AI Assistant with Model Benchmarking 🚀

A production-grade, 100% offline, privacy-first AI assistant. This project demonstrates advanced engineering practices including LangGraph state machines, Retrieval-Augmented Generation (RAG), and a custom model benchmarking engine.

## 🌟 Key Features
- **Zero Cloud Reliance**: Runs entirely on your local machine using Ollama. No API keys, no data harvesting.
- **RAG Pipeline**: Upload PDFs and chat with your documents via ChromaDB and local HuggingFace embeddings.
- **Self-Healing JSON**: Utilizes a LangGraph cyclic workflow to enforce Pydantic structured schemas, retrying autonomously if the local model hallucinates.
- **Benchmarking Engine**: Compare `Qwen`, `Gemma`, and `Llama` across latency, RAM (RSS), CPU usage, and accuracy.
- **Interactive Dashboard**: Real-time rendering of performance metrics via Chart.js.

## 🛠️ Tech Stack
- **Backend**: FastAPI, LangChain, LangGraph, Ollama, SQLite (SQLAlchemy), PyMuPDF, ChromaDB
- **Frontend**: React, Vite, TypeScript, Tailwind CSS, Chart.js
- **DevOps**: Docker, Docker Compose, GitHub Actions, Pytest

## 🚀 Quick Start (Docker)

```bash
# Start the Ollama engine locally on your host first!
ollama run qwen3:4b

# Build and start the cluster
docker-compose up --build
```
- UI available at: `http://localhost:5173`
- API Docs at: `http://localhost:8000/api/v1/openapi.json`

## 🏗️ Architecture
See [Architecture Overview](docs/architecture.md) and [ADRs](docs/adr/) for detailed diagrams and engineering decisions.

## 🧪 Testing
```bash
cd backend
pytest tests/
```
