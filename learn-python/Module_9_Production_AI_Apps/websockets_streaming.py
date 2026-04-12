"""
This script demonstrates using WebSockets for real-time streaming in FastAPI.
Topics covered:
1. Setting up WebSocket endpoints.
2. Sending and receiving real-time messages.
"""

from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")

# Run the app with: uvicorn script_name:app --reload
# Test with a WebSocket client.