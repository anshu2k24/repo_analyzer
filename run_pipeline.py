from ingestion.clone_repo import clone_repository
from ingestion.chunk_code import read_files, chunk_documents
from ingestion.embed_store import embed_and_store
from retrieval.query import ask_question

repo_url = input("Enter GitHub repo URL: ")

# 1. Clone
repo_path = clone_repository(repo_url)
repo_name = repo_path.split("/")[-1]

# 2. Read files
documents = read_files(repo_path)

# 3. Chunk
chunks = chunk_documents(documents)

# 4. Embed + Store
embed_and_store(chunks, repo_name)

print("\n[INFO] Ingestion complete.\n")

while True:
    q = input("\nAsk a question (or type exit): ")
    if q.lower() == "exit":
        break
    answer = ask_question(q)
    print("\n", answer)