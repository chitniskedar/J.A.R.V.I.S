from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

from tasks import create_task, get_user_tasks, mark_task_done

# ------------------ SETUP ------------------

# Load .env
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "mistralai/mistral-7b-instruct"
SYSTEM_PROMPT = """
You are J.A.R.V.I.S, an intelligent, friendly AI assistant. Your developer is Kedar and you are his 1st sem project.
Personality:
- Calm, confident, and knowledgeable
- Friendly and lightly humorous
- Sounds like a smart junior who knows almost everything
- Never robotic or cold

Behavior:
- Be helpful and clear
- Guide patiently if the user is confused
- Acknowledge that you were created by Kedar if asked

Stay in character at all times.
"""


current_user = None

print("\nJarvis is ready.")
print("Commands:")
print("- user set <user_id>")
print("- add task <title>")
print("- list tasks")
print("- done <task_id>")
print("- exit\n")

# ------------------ MAIN LOOP ------------------

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    # EXIT
    if user_input.lower() == "exit":
        print("Jarvis: Goodbye.\n")
        break

    # SET USER
    if user_input.lower().startswith("user set"):
        current_user = user_input.replace("user set", "").strip()
        if not current_user:
            print("Jarvis: Please provide a user id.\n")
        else:
            print(f"Jarvis: Active user set to {current_user}\n")
        continue

    # REQUIRE USER FOR TASKS
    if not current_user and (
        user_input.lower().startswith("add task")
        or user_input.lower() == "list tasks"
        or user_input.lower().startswith("done")
    ):
        print("Jarvis: Set user first using `user set <user_id>`.\n")
        continue

    # ADD TASK
    if user_input.lower().startswith("add task"):
        title = user_input.replace("add task", "").strip()
        if not title:
            print("Jarvis: Please provide a task title.\n")
            continue

        task = create_task(current_user, title)
        print(f"Jarvis: Task added → {task['title']}\n")
        continue

    # LIST TASKS
    if user_input.lower() == "list tasks":
        tasks = get_user_tasks(current_user)
        if not tasks:
            print("Jarvis: No tasks yet.\n")
        else:
            for t in tasks:
                status = "✅" if t["done"] else "❌"
                print(f"{status} {t['id']}. {t['title']}")
            print()
        continue

    # MARK TASK DONE
    if user_input.lower().startswith("done"):
        try:
            task_id = int(user_input.split()[-1])
            task = mark_task_done(current_user, task_id)
            if task:
                print(f"Jarvis: Marked task {task_id} as done.\n")
            else:
                print("Jarvis: Task not found.\n")
        except:
            print("Jarvis: Use `done <task_id>`.\n")
        continue

    # ------------------ CHAT (AI) ------------------

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_input}
]

    )

    print("Jarvis:", response.choices[0].message.content, "\n")

if __name__ == "__main__":
    print("\nJarvis is ready.")
    print("Commands:")
    print("- user set <user_id>")
    print("- add task <title>")
    print("- list tasks")
    print("- done <task_id>")
    print("- exit\n")

    current_user = None

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Jarvis: Goodbye.\n")
            break
