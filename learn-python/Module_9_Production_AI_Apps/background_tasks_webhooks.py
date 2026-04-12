"""
This script demonstrates background tasks and webhooks in FastAPI.
Topics covered:
1. Using background tasks.
2. Implementing webhooks.
"""

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

# Background task function
def write_log(message: str):
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

@app.post("/webhook/", tags=["Webhooks"])
async def webhook(data: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Received data: {data}")
    return {"message": "Webhook received, processing in background."}

# Run the app with: uvicorn script_name:app --reload