#!/usr/bin/env python3
"""MANIFEST.sha256 for seat EA-CORPORA-17/01: every file the seat holds, the payload included.
Files present in the seat are hashed from the bytes; payload files not yet carried in (scripts/seat_openai_math.py
brings them) take their SHA-256 from original/SOURCE-TREE.sha256, which was computed from the commit in session.
Rerun after any change to source.json or text/."""
import hashlib, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts"))
from seat_openai_math import SEAT, seated
def sha(p):
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
tree = dict(reversed(l.split("  ", 1)) for l in (SEAT / "original/SOURCE-TREE.sha256").read_text(encoding="utf-8").splitlines())
lines = {}
for p in sorted(tree):
    if seated(p):
        lines["./original/" + p] = tree[p]
for f in sorted(SEAT.rglob("*")):
    if f.is_file() and f.name != "MANIFEST.sha256":
        rel = "./" + f.relative_to(SEAT).as_posix()
        h = sha(f)
        if rel in lines and lines[rel] != h:
            sys.exit(f"{rel}: the seated bytes differ from SOURCE-TREE.sha256")
        lines[rel] = h
(SEAT / "MANIFEST.sha256").write_text("".join(f"{h}  {r}\n" for r, h in sorted(lines.items())), encoding="utf-8")
print(len(lines), "entries")
