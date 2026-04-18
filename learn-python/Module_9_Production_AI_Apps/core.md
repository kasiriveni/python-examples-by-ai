# Core Python Concepts

## Core Themes
- Serving AI features with FastAPI and async application structure.
- Validation, logging, tracing, caching, and background work.
- Testing production AI endpoints and streaming interfaces.

## Core Theme Examples
- Example 1: FastAPI endpoints with Pydantic request validation.
- Example 2: Async background tasks and webhook handler patterns.
- Example 3: WebSocket streaming for real-time response delivery.

## Files and Concepts
- background_tasks_webhooks.py: background tasks, webhook handlers
- environment_management.py: venv, Poetry, dependency and environment setup
- fastapi_example.py: basic FastAPI endpoints
- fastapi_rest_api.py: async endpoints, dependency injection, REST API structure
- logging_tracing.py: structlog, OpenTelemetry, distributed tracing
- production_patterns.py: TTL caches, response caching, production hardening
- pydantic_validation.py: BaseModel validation, fields, response models
- testing_ai_code.py: pytest, mocking LLM calls, parametrized contract tests
- websockets_streaming.py: WebSocket endpoints, real-time streaming responses

## Core Example
This example validates an input payload and returns a structured response.

```python
from dataclasses import dataclass

@dataclass
class Prediction:
	text: str
	score: float

def predict(text):
	cleaned = text.strip()
	return Prediction(cleaned, score=len(cleaned) / 10)

print(predict(" hello "))
```
