import os

ALLOWED_EXTENSIONS = [".py", ".js", ".ts", ".java", ".go", ".cpp"]
EXCLUDED_DIRS = ["node_modules", ".git", "dist", "build", "__pycache__"]

def should_ignore(path):
    return any(excluded in path for excluded in EXCLUDED_DIRS)

def read_files(repo_path):
    documents = []

    for root, dirs, files in os.walk(repo_path):
        if should_ignore(root):
            continue

        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        documents.append({
                            "content": content,
                            "file_path": full_path
                        })
                except:
                    continue

    return documents


def chunk_text(text, chunk_size=1200, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def chunk_documents(documents):
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["content"])
        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "file_path": doc["file_path"]
            })

    return all_chunks