#!/usr/bin/env python3
"""push_hf_space.py — upload hf-space/ to a Docker Space. Needs HF_TOKEN and HF_SPACE (e.g. leesharsks/crimson-hexagonal-archive-api)."""
import os, sys, pathlib
from huggingface_hub import HfApi
repo = os.environ.get('HF_SPACE'); tok = os.environ.get('HF_TOKEN')
if not (repo and tok): sys.exit("HF_SPACE and HF_TOKEN required")
api = HfApi(token=tok)
api.create_repo(repo, repo_type='space', space_sdk='gradio', exist_ok=True)
folder = pathlib.Path(__file__).resolve().parent.parent/'hf-space'
api.upload_folder(folder_path=str(folder), repo_id=repo, repo_type='space', commit_message=f"deploy from alexanarch {os.environ.get('GITHUB_SHA','local')[:8]}")
print(f"pushed to https://huggingface.co/spaces/{repo}")
