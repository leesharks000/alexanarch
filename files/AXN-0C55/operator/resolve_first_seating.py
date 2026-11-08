#!/usr/bin/env python3
"""Recover, for each record of a framework kernel, the commit that first seated its text in the archive's repository, that first text, and the
record's description in the registry at that commit. The builder dates a claim's introduction from these: a quotation present there is attested
from the first seating; a quotation absent there is present in the current version with its introduction unresolved.
   python3 resolve_first_seating.py <alexanarch root> <out dir> <deposit number> ..."""
import sys, json, subprocess, hashlib, pathlib
ROOT, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); NS = [int(x) for x in sys.argv[3:]]
REG = {r["deposit_number"]: r for r in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
paths = {REG[n]["full_text_path"].lstrip("/"): n for n in NS}
g = lambda *a: subprocess.run(["git", "-c", "gc.auto=0", *a], cwd=ROOT, capture_output=True).stdout
log = g("log", "--diff-filter=A", "--format=COMMIT %h %ad", "--date=short", "--name-only", "--", *paths).decode()
first, cur = {}, None
for line in log.splitlines():
    line = line.strip()
    if line.startswith("COMMIT"): cur = line.split()[1:]
    elif line in paths: first[paths[line]] = (cur, line)     # newest first: the last assignment is the oldest add
(OUT / "first").mkdir(parents=True, exist_ok=True); regs, out = {}, {}
for n, ((commit, day), p) in first.items():
    t = g("show", f"{commit}:{p}"); (OUT / "first" / f"{n}.md").write_bytes(t)
    if commit not in regs:
        raw = g("show", f"{commit}:data/registry.json")
        regs[commit] = {r["deposit_number"]: r for r in json.loads(raw)["deposits"]} if raw else {}
    d = (regs[commit].get(n) or {}).get("description") or ""; (OUT / "first" / f"{n}.desc").write_text(d)
    out[n] = {"commit": commit, "date": day, "path": p, "text_sha256": hashlib.sha256(t).hexdigest(), "desc_at_commit": bool(d)}
json.dump(out, open(OUT / "first-seating.json", "w"), indent=1)
print(f"{len(out)} records resolved; unresolved: {sorted(set(NS) - set(out))}")
