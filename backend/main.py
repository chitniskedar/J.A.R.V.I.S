from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from openai import OpenAI
from prompt import SYSTEM_PROMPT
from tasks import create_task, get_user_tasks, mark_task_done

# ---------- APP ----------

app = FastAPI()

# ---------- CORS ----------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://jarvis17.vercel.app",
        "https://jarvis-production-0594.up.railway.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- MEMORY ----------

conversation_memory = {}
MAX_HISTORY = 5

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

# ---------- TASK INTENT HANDLER ----------

def handle_task_intent(user_id: str, message: str):
    msg = message.lower().strip()

    if msg.startswith("add task"):
        title = msg.replace("add task", "").strip()
        if title:
            create_task(user_id, title)
            return f"Task added: {title}"

    if msg == "list tasks":
        tasks = get_user_tasks(user_id)
        if not tasks:
            return "You have no active tasks."

        active = [t for t in tasks if not t["done"]]
        if not active:
            return "You have no active tasks."

        return "Your tasks:\n" + "\n".join(
            f"{t['id']}. {t['title']}" for t in active
        )

    if msg.startswith("done"):
        try:
            task_id = int(msg.split()[-1])
            mark_task_done(user_id, task_id)
            return f"Task {task_id} marked as done."
        except:
            return "Please specify a valid task number."

    return None

# ---------- ROUTES ----------

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):

    # STEP 2 — task intent (INSIDE route)
    task_reply = handle_task_intent(req.user_id, req.message)
    if task_reply:
        return {"reply": task_reply}

    # STEP 1 — memory
    history = conversation_memory.get(req.user_id, [])

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": req.message}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    reply = response.choices[0].message.content

    # update memory
    history.append({"role": "user", "content": req.message})
    history.append({"role": "assistant", "content": reply})
    conversation_memory[req.user_id] = history[-MAX_HISTORY:]

    return {"reply": reply}

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
