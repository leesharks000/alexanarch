"""Equivalence of hkcore with the Socrates builder: recompute every deposited EA-HK-ORTHONYM-01 v1.1 claim's target and introduction."""
import json, pathlib, sys, tempfile
from hkcore import Kernel
A = pathlib.Path("/home/claude/alexanarch"); HK = pathlib.Path("/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/hk-orthonym")
K = Kernel(A, tempfile.mkdtemp(), HK, "T", "0", "2026-11-08")
dep = [json.loads(l) for l in (A / "files/AXN-0C55/kernel/03-claims.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
bad = 0
for c in dep:
    n = int(c["target"]["record"].split(":")[1]); q = c["target"]["exact"]
    K.BODY[n] = c["body"]; K.C.clear()
    K.claim(c["id"], n, q, c["claim_kind"], c["state"], body=c["body"], notes=c.get("notes"), role=c["role"], original_wording=c["target"].get("original_wording"))
    if K.C[0] != c:
        bad += 1; print("DIFF", c["id"]); print(" dep", json.dumps(c, ensure_ascii=False)[:300]); print(" new", json.dumps(K.C[0], ensure_ascii=False)[:300])
print(f"{len(dep)} claims compared, {bad} differ")
sys.exit(1 if bad else 0)
