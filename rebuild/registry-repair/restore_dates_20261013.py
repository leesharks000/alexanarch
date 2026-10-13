#!/usr/bin/env python3
"""restore_dates_20261013.py — the 2026-07-03 restoration wave gets its works' own dates back.

MANUS ruling 2026-10-13 ("adopted. lets fix."), under the restoration dating schema ruled 2026-08-25:
date = the work's own date; date_restored = the restore event; original_doi = the wounded identifier.

Cohort: the 84 records minted 2026-07-03 whose `date` equals their mint day and whose own dead DOI
(restoration.dead_doi) carries an Issued date in the DataCite backup of 2026-06-22
(data/datacite-full-backup.json) that differs. Registry-wide, no other record shows the pattern.
Applied: 82 — 74 whose dead DOI maps back to the record in data/api/doi-axn-map.json, plus 8 already
SUPERSEDED duplicates/versions whose DOI maps to their head (#1014–#1020, #1000); the Issued date of a
record's own DOI is that record's date either way. HELD for MANUS: #964 (dead DOI maps to #1024; Issued
2026-06-15 later than registration 2026-04-06 — possibly a concept-level date) and #1032 (dead DOI not in
the map; body reseated 2026-10-07).
Metadata only: no canonical text carries the date, so no hash or AXN moves (axn/v2.2 Tier 1).
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
REG = ROOT / "data/registry.json"
HELD = {964, 1032}
TODAY = "2026-10-13"
raw = REG.read_text(encoding="utf-8"); reg = json.loads(raw)
B = {r["id"].lower(): r["attributes"] for r in json.loads((ROOT / "data/datacite-full-backup.json").read_text())["records"] if isinstance(r, dict)}
done, held = [], []
for x in reg["deposits"]:
    md = str(x.get("minted_at", ""))[:10]
    z = (x.get("restoration") or {}).get("dead_doi")
    if md != "2026-07-03" or x.get("date") != md or not z or z.lower() not in B:
        continue
    iss = [q["date"][:10] for q in B[z.lower()].get("dates", []) if q.get("dateType") == "Issued"]
    if not iss or iss[0] == x["date"]:
        continue
    if x["deposit_number"] in HELD:
        held.append(x["deposit_number"]); continue
    prior = x["date"]
    x["date"] = iss[0]; x["date_restored"] = prior; x["original_doi"] = z
    x["date_basis"] = (f"Work date from the DataCite Issued date of the record's own DOI {z} "
                       f"(data/datacite-full-backup.json, captured 2026-06-22); {prior} is the restoration date, now date_restored. "
                       f"Restoration dating schema (MANUS 2026-08-25), applied 2026-10-13.")
    x["date_modified"] = TODAY
    x.setdefault("record_modifications", []).append({"date": TODAY, "field": "date",
        "note": f"date {prior} → {iss[0]} (DataCite Issued, {z}); {prior} kept as date_restored. Metadata only; canonical bytes, hash and AXN unchanged."})
    done.append(x["deposit_number"])
REG.write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")) if "\n" not in raw.strip()
               else json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(done), "dated;", "held:", held)
print(" ".join(map(str, done)))
