// Config
const BACKEND_URL = "http://127.0.0.1:8000"; // change if different host/port

// Elements
const fileInput = document.getElementById("fileInput");
const dropzone = document.getElementById("dropzone");
const uploadForm = document.getElementById("uploadForm");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");
const indexedDocs = document.getElementById("indexedDocs");
const docTitle = document.getElementById("docTitle");

const askForm = document.getElementById("askForm");
const queryInput = document.getElementById("queryInput");
const chatWindow = document.getElementById("chatWindow");
const lastContext = document.getElementById("lastContext");

// drag & drop UX
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.style.borderColor = "#cfdcff";
});
dropzone.addEventListener("dragleave", () => {
  dropzone.style.borderColor = "";
});
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.style.borderColor = "";
  const files = e.dataTransfer.files;
  if (files.length) fileInput.files = files;
});

// show selected file name
fileInput.addEventListener("change", () => {
  if (fileInput.files.length) {
    const name = fileInput.files[0].name;
    uploadStatus.classList.remove("hidden");
    uploadStatus.textContent = `Selected: ${name}`;
  }
});

// Upload handler
uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!fileInput.files.length) {
    uploadStatus.classList.remove("hidden");
    uploadStatus.textContent = "Please choose a PDF or DOCX file first.";
    return;
  }

  uploadBtn.disabled = true;
  uploadBtn.textContent = "Uploading...";

  const file = fileInput.files[0];
  const form = new FormData();
  form.append("file", file, file.name);

  try {
    const res = await fetch(`${BACKEND_URL}/upload`, {
      method: "POST",
      body: form
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || data.message || "Upload failed");

    uploadStatus.classList.remove("hidden");
    uploadStatus.textContent = `${data.message} — ${data.chunks} chunks indexed.`;

    // update indexed docs list
    addIndexedDoc(file.name);

    fileInput.value = "";
    docTitle.value = "";
  } catch (err) {
    uploadStatus.classList.remove("hidden");
    uploadStatus.textContent = `Error: ${err.message}`;
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload & Index";
  }
});

function addIndexedDoc(name) {
  // remove placeholder if present
  const first = indexedDocs.querySelector("li");
  if (first && first.classList.contains("muted")) first.remove();

  const li = document.createElement("li");
  li.textContent = name;
  indexedDocs.prepend(li);
}

// ask handler
askForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = queryInput.value.trim();
  if (!q) return;

  appendMessage("user", q);
  queryInput.value = "";
  appendMessage("assistant", "Searching...");

  try {
    const res = await fetch(`${BACKEND_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q }) // ensure correct key
    });

    let data;
    try {
      data = await res.json();
    } catch {
      removeLastAssistantPlaceholder();
      appendMessage("assistant", "Error: Server returned invalid JSON.");
      return;
    }

    removeLastAssistantPlaceholder();

    if (!res.ok) {
      const errorMsg = typeof data.detail === "object"
        ? JSON.stringify(data.detail)
        : data.detail || data.error || "No answer";
      appendMessage("assistant", `Error: ${errorMsg}`);
      return;
    }

    appendMessage("assistant", data.answer || "No answer found.");
    lastContext.textContent = data.context_used || "";
  } catch (err) {
    removeLastAssistantPlaceholder();
    appendMessage("assistant", `Error: ${err.message}`);
  }
});

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.classList.add("msg", role === "user" ? "user" : "assistant");
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeLastAssistantPlaceholder() {
  const msgs = chatWindow.querySelectorAll(".msg.assistant");
  if (msgs.length) {
    const last = msgs[msgs.length - 1];
    if (last.textContent === "Searching...") last.remove();
  }
}

// simple initialization: try to fetch indexed docs count (optional)
(async function init() {
  // optional endpoint could be added to backend to list indexed docs
})();