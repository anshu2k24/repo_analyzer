from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

from ingestion.clone_repo import clone_repository
from ingestion.chunk_code import read_files, chunk_documents
from ingestion.embed_store import embed_and_store
from retrieval.query import ask_question

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    repo_name: str = None

class IngestRequest(BaseModel):
    repo_url: str

@app.post("/ingest")
def ingest_repo(req: IngestRequest):
    try:
        repo_path = clone_repository(req.repo_url)
        repo_name = repo_path.split("/")[-1]
        
        documents = read_files(repo_path)
        chunks = chunk_documents(documents)
        embed_and_store(chunks, repo_name)
        
        return {"status": "success", "message": f"Successfully ingested {repo_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask(req: QueryRequest):
    try:
        return StreamingResponse(ask_question(req.question, req.repo_name), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))