#!/usr/bin/env python3
"""seat_openai_math.py — carry the openai/math payload into seat EA-CORPORA-17/01, verified file by file.

The seat's records were built in session from openai/math at commit fd4aeeb2 (2026-10-07):
  original/GIT-TREE.txt        the publisher's own object ids for every file in that commit (git ls-tree -r)
  original/SOURCE-TREE.sha256  SHA-256 of every file in that commit, 133,955 files
  MANIFEST.sha256              SHA-256 of every file of the seat, the payload included
The payload (11,496 files, 643 MB: the manuscripts, the top-level files, the reasoning summaries, and the Lean
scope notes, challenge statements, catalogue, build files and dependency patches) is too large to travel in a bundle,
so the workflow fetches the commit and this script copies the seated paths into original/, refusing any file whose
git object id or SHA-256 differs from the records. The 122,000 Lean proof files stay out of the archive and are
pinned by the two tree files; the whole commit is mirrored on Hugging Face.

USAGE
  python3 scripts/seat_openai_math.py --src <openai/math checkout at fd4aeeb2> [--check-only]
"""
import argparse, hashlib, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEAT = ROOT / "data/corpora/openai-math"
COMMIT = "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb"
TOP = {"README.md", "CONTENTS.md", "history.md", "LICENSE", "overview.pdf", "overview.tex",
       "lean/README.md", "lean/LICENSE", "lean/formalization.yaml", "lean/lakefile.lean",
       "lean/lake-manifest.json", "lean/lean-toolchain", "lean/OAI.lean"}
PREFIXES = ("preprints/", "reasoning_traces/", "lean/docs/", "lean/ComparatorChallenges/", "lean/patches/")


def seated(path):
    return path in TOP or path.startswith(PREFIXES)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def git_blob(p):
    data = p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True)
    ap.add_argument("--check-only", action="store_true", help="verify the source checkout and the manifest; copy nothing")
    a = ap.parse_args()
    src = pathlib.Path(a.src)
    head = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != COMMIT:
        print(f"source is at {head}, the seat is of {COMMIT}"); return 2
    blobs = {}
    for l in (SEAT / "original/GIT-TREE.txt").read_text(encoding="utf-8").splitlines():
        meta, path = l.split("\t", 1)
        blobs[path] = meta.split()[2]
    shas = {}
    for l in (SEAT / "original/SOURCE-TREE.sha256").read_text(encoding="utf-8").splitlines():
        h, path = l.split("  ", 1)
        shas[path] = h
    assert set(blobs) == set(shas), "the two tree files disagree on the file list"
    want = sorted(p for p in shas if seated(p))
    bad = []
    for i, p in enumerate(want, 1):
        f = src / p
        if not f.is_file():
            bad.append((p, "absent from source")); continue
        if git_blob(f) != blobs[p]:
            bad.append((p, "git object id differs from GIT-TREE.txt")); continue
        if sha256(f) != shas[p]:
            bad.append((p, "SHA-256 differs from SOURCE-TREE.sha256")); continue
        if not a.check_only:
            dest = SEAT / "original" / p
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
        if i % 2000 == 0:
            print(f"  {i}/{len(want)}")
    if bad:
        for p, why in bad[:20]:
            print(f"REFUSED {p}: {why}")
        print(f"{len(bad)} of {len(want)} files refused; nothing is seated until all verify"); return 1
    print(f"verified {len(want)} payload files against the publisher's object ids and SOURCE-TREE.sha256")
    if a.check_only:
        return 0
    # the seat's own manifest, over every file it now holds
    miss, n = [], 0
    for l in (SEAT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        h, rel = l.split("  ", 1)
        f = SEAT / rel[2:]
        n += 1
        if not f.is_file() or sha256(f) != h:
            miss.append(rel)
    if miss:
        print(f"MANIFEST.sha256: {len(miss)} of {n} entries fail, e.g. {miss[:5]}"); return 1
    print(f"MANIFEST.sha256: {n}/{n} verify")
    return 0


if __name__ == "__main__":
    sys.exit(main())
