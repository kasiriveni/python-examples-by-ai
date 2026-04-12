"""
This script demonstrates building REST APIs with FastAPI.
Topics covered:
1. Creating REST endpoints.
2. Async endpoints.
3. Dependency injection.
"""

from fastapi import FastAPI, Depends

app = FastAPI()

# Dependency injection example
def common_dependency():
    return {"message": "This is a common dependency."}

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}", tags=["Items"])
async def read_item(item_id: int, dependency=Depends(common_dependency)):
    return {"item_id": item_id, "dependency": dependency}

# Run the app with: uvicorn script_name:app --reload