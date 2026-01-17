from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

# configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# create app
app = FastAPI()

# allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# request body
class Message(BaseModel):
    text: str

# chat endpoint
@app.post("/chat")
def chat(msg: Message):
    response = model.generate_content(msg.text)
    return {"reply": response.text}
