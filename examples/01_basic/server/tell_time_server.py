# Import FastAPI and utility classes
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create FastAPI app instance
app = FastAPI()


# ---------------------------------------
# Pydantic Models for Request Validation
# ---------------------------------------
class Part(BaseModel):
    text: str


class Message(BaseModel):
    parts: List[Part]
    role: str = "user"  # "user" is the default role for incoming messages


class Task(BaseModel):
    id: str
    message: Message


# ---------------------------------------
# Endpoint: Agent Card (Discovery Phase)
# ---------------------------------------
@app.get("/.well-known/agent.json")
def agent_card():
    return {
        "name": "TellTimeAgent",
        "description": "Tells the current time when asked",
        "url": "http://localhost:8000",
        "version": "1.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
    }


# ---------------------------------------
# Endpoint: Task Handling (tasks/send)
# ---------------------------------------
@app.post("/tasks/send")
def handle_task(task: Task):
    try:
        # extract the task ID from the request
        task_id = task.id

        # extract the user message text from the request
        user_message = task.message.parts[0].text

    # if the request doesn't match the expected structure, return a 400 error.
    except IndexError, AttributeError:
        raise HTTPException(status_code=400, detail="Invalid task format")

    # generate response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reply_text = f"The current time is: {current_time}"

    return {
        "id": task_id,  # reuse the same task ID in the response
        "status": {"state": "completed"},  # mark the task as completed
        "messages": [
            task.message,  # include the original user message in the response (for context)
            {
                "role": "agent",  # this message is from the agent
                "parts": [{"text": reply_text}],  # reply content in text format
            },
        ],
    }


# ---------------------------------------
# Run with: uvicorn filename:app --port 8000
# ---------------------------------------
