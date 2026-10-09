#!/usr/bin/env python3
"""mirror_openai_math_hf.py — the whole of openai/math at fd4aeeb2, mirrored to a Hugging Face dataset.

Seat EA-CORPORA-17/01 holds the manuscripts and records in the archive and pins the 122,000 Lean proof files by hash.
This mirror carries the entire commit: one git-archive tarball (zstd), the commit's tree files from the seat, and a card.
The tarball's member list is checked against the seat's GIT-TREE.txt before upload.

USAGE (HF_TOKEN in the environment)
  python3 scripts/mirror_openai_math_hf.py --src <openai/math checkout at fd4aeeb2> [--repo leesharks/openai-math-fd4aeeb2]
"""
import argparse, hashlib, os, pathlib, subprocess, sys, tarfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEAT = ROOT / "data/corpora/openai-math"
COMMIT = "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb"

CARD = """---
license: apache-2.0
pretty_name: "openai/math at fd4aeeb2 (2026-10-07), mirrored whole"
tags: [mathematics, lean4, formal-verification, provenance, mirror]
size_categories: [100K<n<1M]
---

# openai/math at fd4aeeb2, mirrored whole

A byte-exact mirror of [github.com/openai/math](https://github.com/openai/math) at commit
`{commit}` (2026-10-07 22:20 -0700): the 719 current manuscripts in 372 result families, 27 previous versions,
3 withdrawal notices, the reasoning summaries, and the full Lean library.

- `openai-math-{short}.tar.zst` — `git archive` of the commit ({files:,} files); sha256 `{tar_sha}`
- `GIT-TREE.txt` — the publisher's object id for every file (`git ls-tree -r`)
- `SOURCE-TREE.sha256` — SHA-256 of every file

Licence: Apache-2.0, the publisher's (LICENSE in the archive). The publisher's files are unchanged.

The manuscripts, top-level files, reasoning summaries and Lean records are also seated in the Crimson Hexagonal
Archive as EA-CORPORA-17/01, with a finding aid and the release's record of authorship:
[alexanarch.org/data/corpora/openai-math/](https://www.alexanarch.org/data/corpora/openai-math/).
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True)
    ap.add_argument("--repo", default="leesharks/openai-math-fd4aeeb2")
    ap.add_argument("--out", default="hf-mirror")
    ap.add_argument("--no-upload", action="store_true")
    a = ap.parse_args()
    src = pathlib.Path(a.src); out = pathlib.Path(a.out); out.mkdir(exist_ok=True)
    head = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != COMMIT:
        print(f"source is at {head}, the mirror is of {COMMIT}"); return 2
    short = COMMIT[:8]
    tar = out / f"openai-math-{short}.tar"
    subprocess.run(["git", "-C", str(src), "archive", "--format=tar", "-o", str(tar.resolve()), COMMIT], check=True)
    want = {l.split("\t", 1)[1] for l in (SEAT / "original/GIT-TREE.txt").read_text(encoding="utf-8").splitlines()}
    with tarfile.open(tar) as t:
        got = {m.name for m in t.getmembers() if m.isfile()}
    if got != want:
        print(f"tarball and GIT-TREE.txt disagree: {len(got ^ want)} paths"); return 1
    subprocess.run(["zstd", "-q", "-19", "-T0", "--rm", str(tar)], check=True)
    zst = tar.with_suffix(".tar.zst")
    h = hashlib.sha256()
    with open(zst, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    for n in ("GIT-TREE.txt", "SOURCE-TREE.sha256"):
        (out / n).write_bytes((SEAT / "original" / n).read_bytes())
    (out / "README.md").write_text(CARD.format(commit=COMMIT, short=short, files=len(want), tar_sha=h.hexdigest()), encoding="utf-8")
    print(f"{zst.name}: {zst.stat().st_size / 1e6:.1f} MB, sha256 {h.hexdigest()}, {len(want):,} files")
    if a.no_upload:
        return 0
    from huggingface_hub import HfApi
    api = HfApi(token=os.environ["HF_TOKEN"])
    api.create_repo(a.repo, repo_type="dataset", exist_ok=True)
    api.upload_folder(repo_id=a.repo, repo_type="dataset", folder_path=str(out),
                      commit_message=f"openai/math at {COMMIT}, mirrored whole")
    print(f"https://huggingface.co/datasets/{a.repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
