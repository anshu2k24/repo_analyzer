import requests
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "data/chroma_db"
COLLECTION_NAME = "codebase"

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(COLLECTION_NAME)


def retrieve(query, top_k=4):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0]


def ask_llama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            # "model": "llama3.1:8b",
            "model": "llama3.1:latest",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


def ask_question(user_query):
    retrieved_chunks = retrieve(user_query)

    context = "\n\n---\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI technical interviewer.

Below is relevant code from a candidate's repository:

{context}

User Question:
{user_query}

Answer based strictly on the code context above.
"""

    return ask_llama(prompt)