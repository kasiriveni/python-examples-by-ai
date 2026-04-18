# Core Python Concepts

## Core Themes
- REST API construction across common Python frameworks.
- GraphQL schemas and resolver patterns.
- JWT-based authentication and serialization concerns.

## Core Theme Examples
- Example 1: Build REST endpoints with GET, POST, and DELETE routes.
- Example 2: Define GraphQL types and write query resolvers.
- Example 3: Validate JWT tokens and handle authorization headers.

## Files and Concepts
- Django_REST.py: Django REST framework serializers, APIView classes, endpoint structure
- FastAPI_REST.py: FastAPI routing, path parameters, query parameters
- Flask_REST.py: Flask route decorators, blueprints, jsonify responses
- GraphQL_Graphene.py: Graphene schemas, ObjectType, query resolvers
- GraphQL_Strawberry.py: Strawberry decorators, async schema types, FastAPI integration
- JWT_Authentication.py: JWT decoding, OAuth2 scheme flow, token validation

## Core Example
This example builds a tiny JSON response with the standard library.

```python
import json
from http.server import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		body = json.dumps({"status": "ok", "items": [1, 2, 3]}).encode()
		self.send_response(200)
		self.send_header("Content-Type", "application/json")
		self.end_headers()
		self.wfile.write(body)
```
