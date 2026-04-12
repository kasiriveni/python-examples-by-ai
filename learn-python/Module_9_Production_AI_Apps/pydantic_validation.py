"""
This script demonstrates using Pydantic models for request and response validation in FastAPI.
Topics covered:
1. Defining Pydantic models.
2. Validating request data.
3. Structuring response data.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define Pydantic models
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ResponseModel(BaseModel):
    item: Item
    message: str

@app.post("/items/", response_model=ResponseModel, tags=["Items"])
async def create_item(item: Item):
    return ResponseModel(item=item, message="Item created successfully!")

# Run the app with: uvicorn script_name:app --reload