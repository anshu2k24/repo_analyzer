# Repo Analyzer / RAG Interviewer

A local RAG (Retrieval-Augmented Generation) application to ask questions against GitHub repositories. It clones a repository, chunks the code, stores embeddings locally in ChromaDB, and uses Ollama to answer questions about the codebase.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally
- The required LLM pulled in Ollama (defaults to `qwen2.5-coder` or `llama3.1`, depending on configuration in `query.py`). E.g., `ollama pull qwen2.5-coder`

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anshu2k24/repo_analyzer.git
   cd repo_analyzer
   ```

2. **Set up a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

You can use the application via the terminal or the web UI.

### Option A: Web UI (Recommended)

1. Start the backend API server:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Open `frontend/index.html` in your browser.
3. Paste a GitHub repository URL into the sidebar and click "Ingest Codebase".
4. Once indexing is complete, start asking questions in the chat interface.

### Option B: Terminal Flow

Run the pipeline script and follow the prompts:
```bash
python run_pipeline.py
```

## Structure

- `app/`: FastAPI application endpoints
- `frontend/`: Vanilla HTML/CSS/JS user interface
- `ingestion/`: Logic for cloning, chunking, and creating embeddings
- `retrieval/`: Handles queries to ChromaDB and Ollama
- `data/`: Local storage for the cloned repos and ChromaDB database
