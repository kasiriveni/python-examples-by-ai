"""
FastAPI web application example.
"""
from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

app = FastAPI(title="Todo API", version="1.0.0")

# Pydantic models
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=5)

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    priority: int

class SortBy(str, Enum):
    title = "title"
    priority = "priority"
    id = "id"

# In-memory store
todos_db: dict[int, dict] = {
    1: {"id": 1, "title": "Learn FastAPI", "description": "Read the docs", "done": False, "priority": 3},
    2: {"id": 2, "title": "Build an API", "description": None, "done": False, "priority": 2},
}
next_id = 3

@app.get("/")
def root():
    return {"message": "Todo API - visit /docs for Swagger UI"}

@app.get("/todos", response_model=list[TodoResponse])
def list_todos(
    done: Optional[bool] = None,
    sort_by: SortBy = SortBy.id,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    items = list(todos_db.values())
    if done is not None:
        items = [t for t in items if t["done"] == done]
    items.sort(key=lambda t: t[sort_by.value])
    return items[skip:skip + limit]

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int = Path(..., ge=1)):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]

@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = {
        "id": next_id,
        "title": todo.title,
        "description": todo.description,
        "done": False,
        "priority": todo.priority,
    }
    todos_db[next_id] = new_todo
    next_id += 1
    return new_todo

@app.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updates: TodoUpdate):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo = todos_db[todo_id]
    update_data = updates.model_dump(exclude_unset=True)
    todo.update(update_data)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "total_todos": len(todos_db)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
