#!/usr/bin/env python3
"""push_hf_dataset.py — upload hf-dataset/ to the Hub, SELECTIVELY.

Why selective (2026-09-08). `upload_folder` re-uploads every file, so a change to
one config re-committed all fourteen parquet files, and the datasets-server treats
each new file as a reason to rebuild that config's full-text index. Measured that
day: /search returned HTTP 500 "the dataset index is loading" for over an hour
after a push, while /rows and /filter answered in under two seconds throughout —
so a day with eleven deposits left the search index cold nearly all of it, for
configs that had not changed at all.

This compares each local file's sha256 against the Hub's recorded hash and uploads
only what differs. A deposits-only change now leaves the indexes of `citations`,
`lexicon`, `captures`, `tombstones` and the rest intact.

Needs HF_TOKEN (write) and HF_REPO (e.g. leesharks/crimson-hexagonal-archive).
"""
import os, sys, pathlib, hashlib
from huggingface_hub import HfApi

repo = os.environ.get('HF_REPO'); tok = os.environ.get('HF_TOKEN')
if not (repo and tok): sys.exit("HF_REPO and HF_TOKEN required")
api = HfApi(token=tok)
api.create_repo(repo, repo_type='dataset', exist_ok=True)
folder = pathlib.Path(__file__).resolve().parent.parent / 'hf-dataset'
local = sorted(p for p in folder.iterdir() if p.is_file())

def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(buf), b''):
            h.update(chunk)
    return h.hexdigest()

# The Hub records an LFS sha256 for large files and a git blob sha for small ones.
# Compare on the LFS hash where it exists; fall back to always-upload for the rest
# (README.md and anything under the LFS threshold — small, and cheap to re-push).
remote = {}
try:
    for info in api.get_paths_info(repo, [p.name for p in local], repo_type='dataset'):
        lfs = getattr(info, 'lfs', None)
        if lfs is not None:
            remote[info.path] = getattr(lfs, 'sha256', None) or (lfs.get('sha256') if isinstance(lfs, dict) else None)
except Exception as e:
    print(f"  could not read remote hashes ({e}); uploading everything")

changed, same = [], []
for f in local:
    r = remote.get(f.name)
    (same if (r and r == sha256(f)) else changed).append(f.name)

if not changed:
    print(f"nothing changed — {len(same)} files already current on the Hub; no commit, no index rebuild")
    sys.exit(0)

print(f"  unchanged, left alone: {sorted(same)}")
print(f"  uploading:             {sorted(changed)}")
api.upload_folder(folder_path=str(folder), repo_id=repo, repo_type='dataset',
                  allow_patterns=changed,
                  commit_message=f"rebuild from alexanarch {os.environ.get('GITHUB_SHA','local')[:8]} ({len(changed)} of {len(local)} files)")
print(f"pushed {sorted(changed)} to https://huggingface.co/datasets/{repo}")
