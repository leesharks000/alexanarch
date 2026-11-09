"""Add first seatings for records to a first-seating folder: the first commit adding the record's text, the text there, and the registry description at that commit.
    python3 add_first.py <alexanarch root> <first dir> N [N ...]"""
import sys, json, subprocess, hashlib, pathlib
root, fd = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); ns = [int(x) for x in sys.argv[3:]]
g = lambda *a: subprocess.run(["git", "-C", str(root), *a], capture_output=True, check=True).stdout
REG = {d["deposit_number"]: d for d in json.loads((root / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
F = json.loads((fd / "first-seating.json").read_text())
for n in ns:
    if str(n) in F: continue
    p = REG[n]["full_text_path"].lstrip("/")
    c, d = g("log", "--diff-filter=A", "--format=%h %ad", "--date=short", "--", p).decode().split("\n")[-2].split()
    t = g("show", f"{c}:{p}")
    desc, ok = REG[n].get("description") or "", False
    try:
        R = json.loads(g("show", f"{c}:data/registry.json")); R = R["deposits"] if isinstance(R, dict) else R
        r = next((x for x in R if x.get("deposit_number") == n), None)
        if r is not None: desc, ok = r.get("description") or "", True
    except Exception: pass
    (fd / "first" / f"{n}.md").write_bytes(t); (fd / "first" / f"{n}.desc").write_text(desc, encoding="utf-8")
    F[str(n)] = {"commit": c, "date": d, "path": p, "text_sha256": hashlib.sha256(t).hexdigest(), "desc_at_commit": ok}
    print(n, c, d, ok, len(t))
(fd / "first-seating.json").write_text(json.dumps(F, indent=1), encoding="utf-8")
