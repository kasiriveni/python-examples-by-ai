# Core Python Concepts

## Core Themes
- HTTP client patterns for external API consumption.
- Authentication, pagination, and rate-limit handling.
- REST request building and service-integration structure.

## Core Theme Examples
- Example 1: Fetch and parse JSON from external REST endpoints.
- Example 2: Add API keys and manage pagination cursors.
- Example 3: Build HTTP request objects with headers and status codes.

## Files and Concepts
- api_authentication.py: API key generation, basic auth, HMAC signing
- api_client_example.py: requests library, JSON parsing, status-code handling
- fastapi_example.py: FastAPI endpoints, query parameters, response models
- post_request_example.py: POST payloads, requests.post, JSON request bodies
- rate_limiting_and_pagination.py: token-bucket limiting, pagination cursors
- rest_api_client.py: GET requests, response parsing, HTTP error handling

## Core Example
This example models an authenticated request with urllib and JSON parsing.

```python
import json
from urllib.request import Request

token = "demo-token"
request = Request("https://example.com/items")
request.add_header("Authorization", f"Bearer {token}")

sample_response = '{"page": 1, "items": ["a", "b"]}'
payload = json.loads(sample_response)
print(payload["items"])
```
