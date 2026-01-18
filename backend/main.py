from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import os

from openai import OpenAI
from tasks import create_task, get_user_tasks, mark_task_done

# ---------- SETUP ----------

load_dotenv(Path(__file__).parent / ".env")

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "mistralai/mistral-7b-instruct"

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- REQUEST MODELS ----------

class ChatRequest(BaseModel):
    user_id: str
    message: str

class TaskRequest(BaseModel):
    user_id: str
    title: str

class DoneRequest(BaseModel):
    user_id: str
    task_id: int

# ---------- ROUTES ----------

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": req.message}]
    )
    return {"reply": response.choices[0].message.content}


@app.get("/tasks/{user_id}")
def list_tasks(user_id: str):
    return get_user_tasks(user_id)


@app.post("/tasks")
def add_task(req: TaskRequest):
    return create_task(req.user_id, req.title)


@app.post("/tasks/done")
def done_task(req: DoneRequest):
    task = mark_task_done(req.user_id, req.task_id)
    return {"success": task is not None}
