const API = "https://jarvis-production-0594.up.railway.app"
let USER_ID = localStorage.getItem("jarvis_user") || ""

/* ---------------- USER ---------------- */
function setUser() {
  const input = document.getElementById("userId")
  USER_ID = input.value.trim()

  if (!USER_ID) {
    alert("Enter user id first")
    return
  }

  localStorage.setItem("jarvis_user", USER_ID)
  loadTasks()
}

/* ---------------- CHAT ---------------- */

function addMessage(sender, text) {
  const box = document.getElementById("chatBox")
  const msg = document.createElement("div")

  msg.classList.add("message")
  msg.classList.add(sender === "You" ? "user" : "jarvis")

  msg.innerText = text
  box.appendChild(msg)

  box.scrollTop = box.scrollHeight
}

async function sendMessage() {
  if (!USER_ID) {
    alert("Set user first")
    return
  }

  const input = document.getElementById("message")
  const text = input.value.trim()
  if (!text) return

  addMessage("You", text)
  input.value = ""

  try {
    const res = await fetch(API + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: USER_ID,
        message: text
      })
    })

    const data = await res.json()
    addMessage("Jarvis", data.reply)
  } catch (err) {
    addMessage("Jarvis", "Backend not reachable")
  }
}

/* ---------------- TASKS ---------------- */

async function addTask() {
  if (!USER_ID) {
    alert("Set user first")
    return
  }

  const input = document.getElementById("taskTitle")
  const title = input.value.trim()
  if (!title) return

  await fetch(API + "/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: USER_ID,
      title: title
    })
  })

  input.value = ""
  loadTasks()
}

window.onload = () => {
  if (USER_ID) {
    document.getElementById("userId").value = USER_ID
    loadTasks()
  }
}

async function loadTasks() {
  if (!USER_ID) return

  const res = await fetch(API + "/tasks/" + USER_ID)
  const tasks = await res.json()

  const list = document.getElementById("taskList")
  list.innerHTML = ""

  tasks.forEach(task => {
    if (task.done) return // hide completed tasks

    const li = document.createElement("li")

    li.innerHTML = `
      <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
        <input 
          type="checkbox"
          onchange="doneTask(${task.id})"
        />
        <span>${task.title}</span>
      </label>
    `

    list.appendChild(li)
  })
}
async

async function doneTask(taskId) {
  await fetch(API + "/tasks/done", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: USER_ID,
      task_id: taskId
    })
  })

  loadTasks() // refresh list → task disappears
}
