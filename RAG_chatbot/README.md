# Document-based RAG Chatbot

This project is a **full-stack AI chatbot** that allows users to upload documents (PDF and DOCX) and ask context-aware questions.  
It is built with:
- **FastAPI** (backend)
- **LangChain** for text chunking
- **Hugging Face Embeddings**
- **FAISS** for semantic search
- **HTML/CSS/JS** frontend

---

## Features
- Upload and index PDF/DOCX files (non-scanned text-based)
- Ask natural language questions about the uploaded documents
- Retrieves relevant chunks using FAISS semantic search
- Embeddings powered by Hugging Face (`sentence-transformers/all-MiniLM-L6-v2`)
- Local RAG pipeline (no external API calls)
- Full-stack implementation: FastAPI backend + custom frontend

---

## Folder Structure
```
Doc_RAG_chatbot/
│
├── backend/
│   └── app/
│       ├── main.py            # FastAPI backend with upload + query endpoints
│
├── frontend/
│   ├── index.html             # UI layout
│   ├── style.css              # Styling
│   └── app.js                 # Handles upload/query requests
│
├── test_client.py             # Script to test upload + query endpoints
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## Requirements

### Python environment
- Python 3.9 or later
- Virtual environment recommended

### Install dependencies
```bash
pip install -r requirements.txt
```

#### requirements.txt includes:
```
fastapi
uvicorn
langchain
langchain-community
langchain-huggingface
pypdf
python-docx
faiss-cpu
transformers
torch
tf-keras
```

---

## Running the Project

### 1. Backend (FastAPI)
Navigate to the project root and start the backend:

```powershell
cd backend
uvicorn app.main:app --reload
```

This runs the backend at:  
`http://localhost:8000`

### 2. Frontend
In another terminal, start a simple HTTP server:

```powershell
cd frontend
python -m http.server 3000
```

Now open in browser:  
`http://localhost:3000/index.html`

---


## Notes
- This works with **text-based PDFs** (not scanned images).  
- Ensure you use the same Python environment for backend and dependencies.  
- Add CORS middleware in `main.py` to allow frontend requests.  

---

## Future Improvements
- Add support for scanned PDFs via OCR (Tesseract)
- Add authentication for users
- Store uploaded documents persistently
- Deploy on Hugging Face Spaces or Render
