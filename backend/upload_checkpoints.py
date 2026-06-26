"""
upload_checkpoints.py — Upload WavLM-Large.pt + prematch_g_02500000.pt
to the politispeak-models dataset repo on Hugging Face.

Run from: C:\\Users\\hp\\OneDrive\\SRM\\Soc_doc_reader\\backend
Usage:
    py -3.11 upload_checkpoints.py
"""

from pathlib import Path
from huggingface_hub import HfApi, login

REPO_ID   = "TamilSelvan0709/politispeak-models"
REPO_TYPE = "dataset"

# Files to upload: (local_path, path_in_repo)
FILES_TO_UPLOAD = [
    ("knnvc/WavLM-Large.pt",          "knnvc/WavLM-Large.pt"),
    ("knnvc/prematch_g_02500000.pt",  "knnvc/prematch_g_02500000.pt"),
]

def main():
    # If you haven't logged in via `huggingface-cli login`, uncomment and paste your token:
    # login(token="hf_xxxxxxxxxxxxxxxxxxxx")

    api = HfApi()

    for local_path, repo_path in FILES_TO_UPLOAD:
        local_path = Path(local_path)
        if not local_path.exists():
            print(f"❌ Missing locally: {local_path} — skipping")
            continue

        size_mb = local_path.stat().st_size / 1024 / 1024
        print(f"⬆️  Uploading {local_path.name} ({size_mb:.1f} MB) → {repo_path} ...")

        api.upload_file(
            path_or_fileobj=str(local_path),
            path_in_repo=repo_path,
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
        )
        print(f"✅ Done: {repo_path}")

    print("\n🎉 All uploads complete. Check: https://huggingface.co/datasets/" + REPO_ID)


if __name__ == "__main__":
    main()