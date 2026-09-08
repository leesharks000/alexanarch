#!/usr/bin/env python3
"""check_settles.py — a deposit minted after 2026-09-08 must record what it does not settle.

The protocol has always required Methodology and Falsification Conditions. Until
2026-09-08 the pipeline extracted them and dropped them, so the archive's own
statement of its limits existed only in the issue body and, for some records, in a
prose section of the text. This gate holds the line forward: any record minted on or
after 2026-09-08 must carry `falsification_conditions` in the registry.

Records minted before that date are exempt — the field cannot be recovered for most
of them, and pretending otherwise would be worse than the gap.
"""
import json, sys

CUTOFF = "2026-09-08"
reg = json.load(open("data/registry.json"))
fails = []
for d in reg["deposits"]:
    minted = (d.get("minted_at") or "")[:10]
    if not minted or minted < CUTOFF:
        continue
    if (d.get("status") or "ACTIVE") != "ACTIVE":
        continue
    if not (d.get("falsification_conditions") or "").strip():
        fails.append(d.get("deposit_number"))
for n in fails[:10]:
    print(f"  FAIL  #{n}: minted on or after {CUTOFF} with no falsification_conditions — "
          f"the deposit does not say what it does not settle")
have = sum(1 for d in reg["deposits"] if (d.get("falsification_conditions") or "").strip())
print(f"check_settles: {have} records state their falsification conditions · {len(fails)} failure(s)")
sys.exit(1 if fails else 0)
