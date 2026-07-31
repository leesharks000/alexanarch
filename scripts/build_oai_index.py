#!/usr/bin/env python3
"""build_oai_index.py — compile a lean index for the OAI-PMH endpoint.

WHY A SEPARATE INDEX
--------------------
data/registry.json is ~12 MB. A serverless function that loads it on every
harvest request pays that cost on every cold start, and a harvester walking
1,400 records in 100-record pages makes many such requests. This compiles only
the fields OAI-PMH disseminates, producing a file small enough to load per
invocation without penalty.

DELETED-RECORD POLICY
---------------------
The endpoint declares `persistent`, which under OAI-PMH means the repository
maintains information about deletions permanently and will disseminate a
`status="deleted"` header rather than dropping the record silently.

For this archive that is not a formality. Its subject is the difference between
a record that was removed and a record that never existed, and the protocol has
a field for exactly that distinction. Declaring `persistent` and honouring it is
the obelus, expressed in a harvesting protocol.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# OAI-PMH requires a bare address here — no mailto: prefix (validator WARN,
# 2026-07-31). It must also be an address that actually receives mail: the
# adminEmail is the repository's answerable contact, and an unreachable one
# is a false assertion on a machine-readable surface.
ADMIN_EMAIL = "leesharks00@gmail.com"
REG = ROOT / "data" / "registry.json"
OUT = ROOT / "data" / "oai-index.json"

FAMILY = re.compile(r"AXN:[0-9A-Fa-f]+\.([A-Z]+)\.")


def dc_type(d):
    ct = str(d.get("content_type") or "").strip()
    return ct or "Text"


DISP = ROOT / "data" / "audit" / "registration_dispositions.json"


def main():
    reg = json.loads(REG.read_text())
    disp = {}
    if DISP.exists():
        disp = json.loads(DISP.read_text()).get("dispositions", {})
    recs = []
    families = set()
    for d in reg["deposits"]:
        n = d.get("deposit_number")
        if not n:
            continue
        a = disp.get(str(n))
        if a and a.get("d") == "WITHHOLD":
            continue  # audit-withheld: excluded from the harvesting surface until repaired
        axn = d.get("axn") or ""
        m = FAMILY.search(axn)
        fam = m.group(1).lower() if m else "unclassified"
        families.add(fam)
        bs = d.get("body_status") or {}
        kws = d.get("keywords") or []
        if isinstance(kws, str):
            kws = [k.strip() for k in kws.split(",") if k.strip()]
        recs.append({
            "id": n,
            "datestamp": (d.get("date_modified") or d.get("date") or "")[:10],
            "date": (d.get("date") or "")[:10],
            "title": d.get("title") or "",
            "creator": d.get("creator") or "",
            "orcid": d.get("orcid") or "",
            "description": ((d.get("description") or "")[:2000]
                            + ((" — " + a["capsule"]) if (a and a.get("capsule")) else "")),
            "type": dc_type(d),
            "rights": d.get("license") or "CC-BY-4.0",
            "axn": axn,
            "subjects": [str(k) for k in kws][:24],
            "sets": [f"family:{fam}",
                     ("audit:cleared" if (a and a.get("d") == "HARVEST")
                      else "audit:cleared-with-warning" if (a and a.get("d") == "HARVEST_WITH_WARNING")
                      else "audit:pending")] + (
                ["completeness:metadata-capture"] if bs.get("class") == "metadata_capture"
                else ["completeness:full"]),
            "deleted": bool(d.get("status") == "WITHDRAWN"),
        })
    recs.sort(key=lambda r: r["id"])
    stamps = [r["datestamp"] for r in recs if r["datestamp"]]
    idx = {
        "repositoryName": "Alexanarch — the Crimson Hexagonal Archive",
        "baseURL": "https://www.alexanarch.org/oai",
        "protocolVersion": "2.0",
        "adminEmail": ADMIN_EMAIL,
        "earliestDatestamp": min(stamps) if stamps else "2026-06-19",
        "deletedRecord": "persistent",
        "granularity": "YYYY-MM-DD",
        "identifierScheme": "oai:alexanarch.org:{deposit_number}",
        "sets": sorted({s for r in recs for s in r["sets"]}),
        "count": len(recs),
        "records": recs,
    }
    OUT.write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    mb = OUT.stat().st_size / 1e6
    print(f"oai-index: {len(recs)} records, {mb:.2f} MB, "
          f"earliest {idx['earliestDatestamp']}, {len(idx['sets'])} sets")


if __name__ == "__main__":
    main()
