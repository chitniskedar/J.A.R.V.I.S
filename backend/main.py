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

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "mistralai/mistral-7b-instruct"

app = FastAPI()

# ---------- CORS (FIXED FOR VERCEL) ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://jarvis17.vercel.app",
        "https://jarvis-orpin-rho.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
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

@app.get("/")
def root():
    return {"status": "Jarvis backend running"}

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
