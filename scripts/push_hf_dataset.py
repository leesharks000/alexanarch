#!/usr/bin/env python3
"""push_hf_dataset.py — upload hf-dataset/ to the Hub. Needs HF_TOKEN (write) and HF_REPO (e.g. leesharks/crimson-hexagonal-archive)."""
import os, sys, pathlib
from huggingface_hub import HfApi
repo = os.environ.get('HF_REPO'); tok = os.environ.get('HF_TOKEN')
if not (repo and tok): sys.exit("HF_REPO and HF_TOKEN required")
api = HfApi(token=tok)
api.create_repo(repo, repo_type='dataset', exist_ok=True)
folder = pathlib.Path(__file__).resolve().parent.parent/'hf-dataset'
api.upload_folder(folder_path=str(folder), repo_id=repo, repo_type='dataset',
                  commit_message=f"rebuild from alexanarch {os.environ.get('GITHUB_SHA','local')[:8]}")
print(f"pushed {sorted(p.name for p in folder.iterdir())} to https://huggingface.co/datasets/{repo}")
