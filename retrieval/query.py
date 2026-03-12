import requests
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "data/chroma_db"
COLLECTION_NAME = "codebase"

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(COLLECTION_NAME)


def retrieve(query, repo_name=None, top_k=4):
    query_embedding = model.encode([query]).tolist()

    kwargs = {
        "query_embeddings": query_embedding,
        "n_results": top_k
    }

    if repo_name:
        kwargs["where"] = {"repo": repo_name}

    results = collection.query(**kwargs)

    return results["documents"][0] if results["documents"] else []


import json

def ask_llama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            # "model": "llama3.1:8b",
            "model": "qwen2.5-coder",
            # "model": "llama3.1:latest",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    yield data["response"]
            except Exception as e:
                pass


def ask_question(user_query, repo_name=None):
    retrieved_chunks = retrieve(user_query, repo_name)

    if not retrieved_chunks:
        context = "No relevant context found."
    else:
        context = "\n\n---\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI assistant helping a user understand a codebase.

Below is retrieved code from the repository:

{context}

User Question:
{user_query}

Please provide a direct, concise answer to the User Question based strictly on the code context above. Do NOT critique the code or act like an interviewer unless specifically asked.
"""

    return ask_llama(prompt)