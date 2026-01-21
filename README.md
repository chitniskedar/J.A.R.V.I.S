# J.A.R.V.I.S 🤖

J.A.R.V.I.S is a full-stack AI assistant inspired by Iron Man’s J.A.R.V.I.S, built with a focus on clean UX, conversational intelligence, and real backend integration.

It combines AI chat, short-term memory, and personal task management — all usable directly from the browser.

---

## ✨ Features

### 🤖 AI Chat
- Conversational AI powered by OpenRouter
- Custom personality (friendly, calm, intelligent)
- Remembers recent conversation context (per user)
- Typing indicator (“Jarvis is thinking…”)
- Press **Enter to send** (Shift + Enter for new line)

### ✅ Task Management
- Add, list, and complete tasks
- Tasks persist per user
- Tasks can be controlled via **UI buttons or natural language chat**
  - `add task buy groceries`
  - `list tasks`
  - `done 1`

### 🌐 Fully Deployed
- Frontend and backend are live
- No local setup required to try it

---

## 🛠 Tech Stack

**Frontend**
- HTML
- CSS
- Vanilla JavaScript
- Deployed on **Vercel**

**Backend**
- Python
- FastAPI
- OpenRouter (LLM API)
- JSON-based task storage
- In-memory chat memory
- Deployed on **Railway**

---

## 📸 Screenshots

### Main Interface
AI chat with memory, natural language task control, and a Jarvis-inspired UI.

![J.A.R.V.I.S Main UI](screenshots/main-ui.png)

---

## 🌍 Live Demo

Frontend:  
https://jarvis17.vercel.app  

Backend API:  
https://jarvis-production-0594.up.railway.app  

> Note: The backend may take a few seconds to wake up after inactivity.

---

## 🧠 How It Works

- Frontend is hosted on Vercel
- Backend API runs on Railway
- Frontend communicates with backend via `/api`
- Each user has:
  - short-term conversation memory
  - their own task list
- Task-related messages are intercepted and handled before reaching the AI

---

## 📌 Author

Built by **Kedar**

Designed, implemented, debugged, and deployed end-to-end as a full-stack project.

---

⭐ If you like this project, feel free to star the repo!

---
## License
MIT

---
