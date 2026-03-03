# 🚀 RAG Interviewer

A context-aware AI technical interviewer that uses Retrieval-Augmented Generation (RAG) to analyze GitHub repositories and answer questions based on the candidate's actual code.

![Terminal UI Interface](https://img.shields.io/badge/Interface-Terminal--Style-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.100%2B-009688)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-yellow)

## ✨ Features

- **Repo Ingestion**: Clones any public GitHub repository and extracts its structure.
- **Smart Chunking**: Processes code files with overlap to maintain context between chunks.
- **Semantic Search**: Uses `BAAI/bge-small-en-v1.5` embeddings and **ChromaDB** for fast, local vector search.
- **Local LLM Integration**: Powered by **Ollama** (Llama 3.1) for secure, local code analysis.
- **Terminal UI**: A modern, minimal, dark-themed frontend that feels like a local AI terminal.
- **CORS Supported**: Fully configured FastAPI backend to handle cross-origin browser requests.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Pydantic
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence-Transformers (`BAAI/bge-small-en-v1.5`)
- **LLM**: Ollama (Llama 3.1)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (no frameworks)
- **Git Interaction**: GitPython, PyDriller

## 📦 Installation & Setup

### 1. Prerequisites
- **Python 3.10+**
- **Ollama**: [Download and install](https://ollama.com/)
- **Llama 3.1**: Pull the model using `ollama pull llama3.1`

### 2. Clone and Install
```bash
git clone https://github.com/anshu2k24/repo_analyzer.git
cd repo_analyzer
```

### 3. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 How to Use

### Step 1: Ingest a Repository
Run the pipeline to clone and index a GitHub repo:
```bash
python run_pipeline.py
```
*Enter the target repository URL when prompted.*

### Step 2: Start the Backend Server
Launch the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### Step 3: Launch the UI
Simply open `index.html` in your favorite web browser. You're ready to interview your codebase!

## 📂 Project Structure

```text
rag-interviewer/
├── app/                  # FastAPI Application
│   ├── main.py           # API Entry Point & CORS Setup
│   └── config.py         # App Configurations
├── ingestion/            # Pipeline logic
│   ├── clone_repo.py     # Repo cloning (GitPython)
│   ├── chunk_code.py     # Code chunking logic
│   └── embed_store.py    # ChromaDB indexing
├── retrieval/            # RAG Logic
│   └── query.py          # Vector search + Ollama interaction
├── data/                 # Ignored by Git (Local Only)
│   ├── repos/            # Cloned source code
│   └── chroma_db/        # Persistent vector database
├── index.html            # Minimal Terminal Frontend
└── requirements.txt      # Python Dependencies
```

## 🤝 Contributing
Feel free to fork this project and submit pull requests for any features or bug fixes.

---
*Developed for intelligent, local, and private code analysis.*
