from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

# Load env
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

print("Jarvis is ready. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": user_input}]
    )

    print("Jarvis:", response.choices[0].message.content, "\n")
