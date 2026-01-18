import json
from pathlib import Path
from datetime import datetime

# Path to storage file
TASK_FILE = Path(__file__).parent / "storage" / "tasks.json"


def _load_all():
    if not TASK_FILE.exists():
        return {}
    with open(TASK_FILE, "r") as f:
        return json.load(f)


def _save_all(data):
    with open(TASK_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_user_tasks(user_id):
    data = _load_all()
    return data.get(user_id, [])


def create_task(user_id, title):
    data = _load_all()

    if user_id not in data:
        data[user_id] = []

    tasks = data[user_id]
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat()
    }

    tasks.append(task)
    _save_all(data)
    return task


def mark_task_done(user_id, task_id):
    data = _load_all()

    if user_id not in data:
        return None

    for task in data[user_id]:
        if task["id"] == task_id:
            task["done"] = True
            _save_all(data)
            return task

    return None
