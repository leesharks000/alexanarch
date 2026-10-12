#!/usr/bin/env python3
"""Bring data/lexical-minting-registry.csv up to the canonical JSON (2026-10-12, on the operator's ruling of 16:25:
"yes, lets do that"). The six lexicon passes of 2026-10-12 wrote the JSON only; the CSV had none of pass 6's 348 terms and
was 820 JSON entries behind in all. Projection only: every JSON entry absent from the CSV, keyed (term, defining deposit), is
appended in JSON order, the way the mint pipeline appends (scripts/apply_internal_deposit_packet.py: DictWriter, "\n").
Nothing is removed or rewritten. Left as found and reported: 81 CSV rows with no JSON entry (never in the JSON since at least
2026-10-08), 46 rows whose JSON title is empty, 3 rows whose definitions differ (pass 2 repaired the JSON's)."""
import csv, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
J = ROOT / "data/lexical-minting-registry.json"; C = ROOT / "data/lexical-minting-registry.csv"
terms = json.loads(J.read_text(encoding="utf-8"))["terms"]
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
with C.open(encoding="utf-8", newline="") as fh:
    rd = csv.DictReader(fh); fields = rd.fieldnames; have = {(r["term"], r["deposit_number"]) for r in rd}
assert fields == ["term", "definition", "deposit_number", "deposit_title", "type"], fields
add = []
for t in terms:
    n = t.get("defined_in_deposit"); k = (t["term"], str(n))
    if k in have: continue
    title = t.get("defined_in_title") or (reg.get(n, {}).get("title", "") if isinstance(n, int) else "")
    add.append({"term": t["term"], "definition": t.get("definition") or "", "deposit_number": "" if n is None else n,
                "deposit_title": title, "type": t.get("type") or ""}); have.add(k)
raw = C.read_bytes()
with C.open("a", encoding="utf-8", newline="") as fh:
    if not raw.endswith(b"\n"): fh.write("\n")
    w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
    for r in add: w.writerow(r)
print("appended", len(add))
