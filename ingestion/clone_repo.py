import os
from git import Repo

BASE_DIR = "data/repos"

def clone_repository(repo_url: str):
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(BASE_DIR, repo_name)

    if os.path.exists(repo_path):
        print(f"[INFO] Repo already exists: {repo_path}")
        return repo_path

    print(f"[INFO] Cloning {repo_url}...")
    Repo.clone_from(repo_url, repo_path)
    print("[INFO] Clone complete.")
    return repo_path