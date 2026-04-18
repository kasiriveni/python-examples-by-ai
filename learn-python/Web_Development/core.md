# Core Python Concepts

## Core Themes
- Web routes, handlers, and CRUD-style application logic.
- Flask and FastAPI application structure.
- Templates, JSON APIs, and input validation.

## Core Theme Examples
- Example 1: Map URLs to handler functions returning HTML or JSON.
- Example 2: Create app instances and register route decorators.
- Example 3: Validate form inputs with schema models.

## Files and Concepts
- fastapi_todo_app.py: Pydantic models, field validation, enums, todo endpoints
- flask_example.py: basic Flask routes and request handlers
- flask_todo_app.py: Flask routes, JSON endpoints, Jinja templates
- web_flask_example.py: Flask jsonify responses, simple JSON handlers

## Core Example
This example maps paths to view functions in plain Python.

```python
routes = {
	"/": lambda: "home page",
	"/about": lambda: "about page",
}

path = "/about"
handler = routes.get(path, lambda: "not found")
print(handler())
```
