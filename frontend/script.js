const API = "/api";
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

    if (!res.ok) {
  const text = await res.text()
  addMessage("Jarvis", "Backend error: " + text)
  return
}

const data = await res.json()
addMessage("Jarvis", data.reply)

  } catch (err) {
    console.error(err)
    addMessage("Jarvis", "Error: " + err.message)
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

  try {
    const res = await fetch(API + "/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: USER_ID,
        title: title
      })
    })

    if (!res.ok) {
      console.error("Task add failed", await res.text())
      return
    }

    input.value = ""
    loadTasks()
  } catch (err) {
    console.error("Task add error:", err)
  }
}


async function loadTasks() {
  if (!USER_ID) return

  try {
    const res = await fetch(API + "/tasks/" + USER_ID)

    if (!res.ok) {
      console.error("Failed to load tasks", await res.text())
      return
    }

    const tasks = await res.json()

    const list = document.getElementById("taskList")
    list.innerHTML = ""

    tasks.forEach(task => {
      if (task.done) return

      const li = document.createElement("li")

      const checkbox = document.createElement("input")
      checkbox.type = "checkbox"
      checkbox.onchange = () => doneTask(task.id)

      const span = document.createElement("span")
      span.innerText = task.title

      li.appendChild(checkbox)
      li.appendChild(span)

      list.appendChild(li)
    })
  } catch (err) {
    console.error("Task load error:", err)
  }
}

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
