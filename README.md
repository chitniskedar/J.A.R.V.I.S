# J.A.R.V.I.S

A simple full-stack AI assistant demonstrating communication between a FastAPI backend and a browser-based frontend.

---

## What this project demonstrates

- FastAPI backend exposing REST APIs
- Frontend consuming backend APIs using `fetch`
- AI chat using an external LLM API
- Basic task management
- Persistent storage using JSON
- Local development setup

---

## Features

- AI chat endpoint
- Add, list, and complete tasks
- User-based task separation
- Backend and frontend run independently and communicate over HTTP

---

## How it works

1. The frontend sends HTTP requests to the FastAPI backend
2. The backend processes requests and returns JSON responses
3. The frontend updates the UI based on backend responses
4. Tasks are stored persistently in a local JSON file

---
