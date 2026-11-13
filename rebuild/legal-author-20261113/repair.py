"""Metadata correction of 2026-11-13: seven substrate lines named Lee Sharks "legal author". Lee Sharks, 2026-11-12: "you will not find me
claiming or instructing the claim of lee sharks as a legal name anywhere"; the wording spread by template copying from 2026-11-03.
The phrase is removed from the registry field and the record JSON, and an erratum records the old wording. The deposited text's
header line keeps its bytes (records are not reversioned for metadata defects, ruling of 2026-11-10); the erratum says so.
    python3 rebuild/legal-author-20261113/repair.py
"""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[2]
NUMS = [1735, 1736, 1741, 1742, 1758, 1759, 1761]
def fix(t):
    t2 = t.replace(" (legal author Lee Sharks)", "").replace("; the legal author is Lee Sharks.", ".")
    assert "legal author" not in t2 and t2 != t, t[:120]
    return t2
reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
for d in reg["deposits"]:
    n = d.get("deposit_number")
    if n not in NUMS: continue
    old = d["substrate"]; new = fix(old); d["substrate"] = new
    d.setdefault("errata", []).append({"date": "2026-11-13", "kind": "metadata correction", "locus": "registry field substrate",
        "was": old, "now": new,
        "reason": "Lee Sharks is not a legal name and is not to be described as one. Lee Sharks, 2026-11-12: \"you will not find me claiming or instructing the claim of lee sharks as a legal name anywhere.\" The wording entered substrate lines by template copying from 2026-11-03. The header of the deposited text keeps the old line in its bytes; this record's metadata carries the correction.",
        "raised_by": "Lee Sharks (2026-11-12)", "status": "corrected in the metadata"})
    rp = ROOT / f"data/records/{n}.json"; rt = rp.read_text(encoding="utf-8"); r = json.loads(rt)
    r["substrate"] = new
    ind = 2 if rt.startswith('{\n  "') else (1 if rt.startswith('{\n "') else None)
    rp.write_text(json.dumps(r, ensure_ascii=False, indent=ind) + ("\n" if rt.endswith("\n") else ""), encoding="utf-8")
    print(n, "fixed")
(ROOT / "data/registry.json").write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
