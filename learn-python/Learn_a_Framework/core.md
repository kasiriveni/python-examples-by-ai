# Core Python Concepts

## Core Themes
- Framework-specific app bootstrapping and routing.
- Sync and async web-server patterns.
- Hands-on examples across Flask, FastAPI, Django, Sanic, Tornado, and Aiohttp.

## Core Theme Examples
- Example 1: Initialize app and map decorators to handler functions.
- Example 2: Write async handlers with await and event loops.
- Example 3: Run FastAPI with uvicorn and Flask with development servers.

## Files and Concepts
- Aiohttp.py: async I O, aiohttp Application setup, async route handlers
- Django.py: Django project setup, CLI commands, app scaffolding
- FastAPI.py: FastAPI app creation, route decorators, uvicorn startup
- fastapi_tutorial.py: FastAPI filtering, query parameters, pagination
- Flask.py: Flask app instance, route registration, development server
- flask_tutorial.py: Flask templates, dynamic routing, HTTP methods
- Sanic.py: Sanic async framework, async handlers, JSON responses
- Tornado.py: Tornado IOLoop, RequestHandler classes, async server setup

## Core Example
This example shows a tiny router object that registers handlers by path.

```python
class Router:
	def __init__(self):
		self.routes = {}

	def add(self, path, handler):
		self.routes[path] = handler

router = Router()
router.add("/hello", lambda: "hello")
print(router.routes["/hello"]())
```
