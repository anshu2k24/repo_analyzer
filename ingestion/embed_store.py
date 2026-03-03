import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "data/chroma_db"
COLLECTION_NAME = "codebase"

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(COLLECTION_NAME)

def embed_and_store(chunks, repo_name):
    texts = [c["text"] for c in chunks]
    metadatas = [{
        "file_path": c["file_path"],
        "repo": repo_name
    } for c in chunks]

    print("[INFO] Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    ids = [f"{repo_name}_{i}" for i in range(len(texts))]

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

    print("[INFO] Stored in Chroma.")