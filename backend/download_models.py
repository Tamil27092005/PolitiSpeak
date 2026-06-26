"""
download_models.py — Pulls checkpoints from the politispeak-models
dataset repo on Hugging Face Hub at container build time.
"""
from huggingface_hub import snapshot_download
import os

print("Starting model download...")
print("Target dir: /app")

# The dataset repo's root already contains a `knnvc/` folder
# (knnvc/WavLM-Large.pt, knnvc/prematch_g_02500000.pt, knnvc/ref_wavs/...)
# Downloading into /app lets that structure land naturally at /app/knnvc/
snapshot_download(
    repo_id="TamilSelvan0709/politispeak-models",
    repo_type="dataset",
    local_dir="/app",
    local_dir_use_symlinks=False,
    ignore_patterns=["*.gitattributes", "README.md"],
)

# Verify the files inference.py actually needs (pure kNN pipeline —
# projection_layer.pt / projection_pairs.pt are no longer required)
expected = [
    "/app/knnvc/WavLM-Large.pt",
    "/app/knnvc/prematch_g_02500000.pt",
    "/app/knnvc/ref_wavs/stalin",
    "/app/knnvc/ref_wavs/vijay",
]
print("\n── Verification ──")
for f in expected:
    exists = os.path.exists(f)
    print(f"{'✅' if exists else '❌'} {f}")

print("\nDone!")