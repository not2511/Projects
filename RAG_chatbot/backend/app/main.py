import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline
import shutil
from fastapi.middleware.cors import CORSMiddleware


# Initialize app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (good for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
FAISS_INDEX_PATH = BASE_DIR / "vectorstore"

UPLOAD_DIR.mkdir(exist_ok=True)
FAISS_INDEX_PATH.mkdir(exist_ok=True)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Improved QA model
qa_pipeline = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2",
    tokenizer="deepset/roberta-base-squad2"
)

# Request model for /query
class QueryRequest(BaseModel):
    query: str

# Upload & index documents
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Load document
    if file.filename.endswith(".pdf"):
        loader = PyPDFLoader(str(file_path))
    else:
        loader = Docx2txtLoader(str(file_path))

    documents = loader.load()

    # Chunk text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Create or update FAISS index
    if FAISS_INDEX_PATH.exists() and any(FAISS_INDEX_PATH.iterdir()):
        db = FAISS.load_local(str(FAISS_INDEX_PATH), embeddings, allow_dangerous_deserialization=True)
        db.add_documents(docs)
    else:
        db = FAISS.from_documents(docs, embeddings)

    db.save_local(str(FAISS_INDEX_PATH))

    return {"message": "File uploaded and indexed successfully", "chunks": len(docs)}

# Ask questions (renamed to /query for consistency)
@app.post("/query")
async def query_documents(req: QueryRequest):
    query = req.query

    if not FAISS_INDEX_PATH.exists() or not any(FAISS_INDEX_PATH.iterdir()):
        raise HTTPException(status_code=400, detail="No documents indexed yet. Please upload a document first.")

    db = FAISS.load_local(str(FAISS_INDEX_PATH), embeddings, allow_dangerous_deserialization=True)

    # Retrieve top-k chunks
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(query)

    if not docs:
        return {"answer": "No relevant information found."}

    # Deduplicate context
    context = "\n".join(list(dict.fromkeys([doc.page_content for doc in docs])))

    # Run QA
    result = qa_pipeline(question=query, context=context)
    clean_answer = result["answer"].strip().replace("\n", " ")

    return {
        "query": query,
        "answer": clean_answer,
        "score": result["score"],
        "context_used": context
    }
# Run the app with: uvicorn app.main:app --reload