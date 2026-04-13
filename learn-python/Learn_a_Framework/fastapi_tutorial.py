"""
Learn a Framework: FastAPI tutorial with examples.
"""

# NOTE: Requires `pip install fastapi uvicorn`

FASTAPI_BASIC = '''
from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Todo API", version="1.0.0")

# === Models ===
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=5)

class TodoResponse(TodoCreate):
    id: int
    completed: bool = False

# === In-memory store ===
todos: dict[int, dict] = {}
counter = 0

# === Routes ===
@app.get("/")
async def root():
    return {"message": "Todo API", "docs": "/docs"}

@app.get("/todos", response_model=list[TodoResponse])
async def list_todos(
    completed: Optional[bool] = None,
    priority: Optional[int] = Query(None, ge=1, le=5),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """List all todos with optional filters."""
    result = list(todos.values())
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    if priority is not None:
        result = [t for t in result if t["priority"] == priority]
    return result[skip:skip + limit]

@app.post("/todos", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate):
    """Create a new todo."""
    global counter
    counter += 1
    new_todo = {**todo.model_dump(), "id": counter, "completed": False}
    todos[counter] = new_todo
    return new_todo

@app.get("/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int = Path(..., ge=1)):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@app.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo: TodoCreate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id].update(todo.model_dump())
    return todos[todo_id]

@app.patch("/todos/{todo_id}/complete")
async def complete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id]["completed"] = True
    return todos[todo_id]

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
'''

# === FastAPI with dependency injection ===
FASTAPI_DEPENDENCIES = '''
from fastapi import Depends, Header, HTTPException

# Auth dependency
async def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization[7:]
    if token != "valid-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": 1, "role": "admin"}

# Database dependency
class Database:
    async def connect(self):
        print("Connected to DB")
    async def disconnect(self):
        print("Disconnected from DB")

async def get_db():
    db = Database()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

@app.get("/protected")
async def protected_route(user=Depends(verify_token), db=Depends(get_db)):
    return {"message": f"Hello user {user['user_id']}", "role": user["role"]}
'''

# === FastAPI middleware ===
FASTAPI_MIDDLEWARE = '''
import time
from fastapi.middleware.cors import CORSMiddleware

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_timing(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    return response
'''

if __name__ == "__main__":
    sections = [
        ("Basic FastAPI App", FASTAPI_BASIC),
        ("Dependency Injection", FASTAPI_DEPENDENCIES),
        ("Middleware", FASTAPI_MIDDLEWARE),
    ]

    for title, code in sections:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        print(code)

    print("\n=== Run with ===")
    print("uvicorn main:app --reload --port 8000")
    print("Open http://localhost:8000/docs for Swagger UI")
