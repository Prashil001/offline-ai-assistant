# ADR 1: Use LangGraph for Structured Outputs

**Date**: 2026-09-24  
**Status**: Accepted  

## Context
Local LLMs (3B - 8B parameters) often struggle to strictly adhere to complex JSON schemas. When they fail, returning a 500 error to the frontend is a poor user experience. Standard LangChain pipelines are linear and difficult to cycle for retries based on custom parsing logic.

## Decision
We implemented a `StateGraph` using `langgraph`. The state tracks the `retry_count` and `error` string. If Pydantic fails to validate the JSON, the Graph routes back to the generation node, injecting the previous failure into the prompt so the LLM can self-correct.

## Trade-offs
- **Pros**: Significantly higher success rate for valid JSON; self-healing architecture; easy to add new tools (like search) later.
- **Cons**: Adds complexity to the codebase over a simple `try/except` loop.
