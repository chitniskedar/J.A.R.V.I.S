from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from openai import OpenAI
from prompt import SYSTEM_PROMPT
from tasks import create_task, get_user_tasks, mark_task_done

# ---------- APP ----------

app = FastAPI()

# ---------- CORS (MUST BE FIRST) ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://jarvis17.vercel.app",
        "https://jarvis-production-0594.up.railway.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- OPENROUTER ----------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-3.5-turbo"


# ---------- MODELS ----------

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
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": req.message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        print("AI ERROR:", e)
        return {"reply": "AI backend error. Check server logs."}


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
