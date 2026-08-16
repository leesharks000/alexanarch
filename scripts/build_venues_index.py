#!/usr/bin/env python3
"""build_venues_index.py — project venues/records/ into venues.json.

ONE CANONICAL STORE, ONE PROJECTION — the same architecture as the heteronym
substrate, adopted for the same reason.

  datasets/venues/records/*.json  CANONICAL. Eight venue records: seven
                                  chartered journals and the CHA province.
  datasets/venues/venues.json     PROJECTION. Generated. Its v1.2 shape is
                                  PRESERVED because it is a published contract:
                                  datasets/index.html, the registry-audit
                                  workplan, INDEX.md, repair_ledger.json and
                                  several data/records/*.json read it.

SCHEMA PRINCIPLE (operator, 2026-08-15): a field can be null, but a datum
without a field ends up not existing. The records declare every field they might
ever need — identifiers, deposits, editorial offices, rulings, open questions —
even where empty. An empty field is a place to put something; an absent field is
a thing that cannot be said.

Usage: build_venues_index.py [--check]
"""
import json, sys, pathlib, argparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
RECORDS = ROOT / "datasets/venues/records"
INDEX = ROOT / "datasets/venues/venues.json"


def build():
    prior = json.loads(INDEX.read_text()) if INDEX.exists() else {}
    recs = [json.loads(p.read_text()) for p in sorted(RECORDS.glob("*.json"))]
    journals = []
    for r in recs:
        j = {"canonical": r["canonical"], "abbrev": r.get("abbrev"),
             "press": r.get("press"), "class": r.get("class")}
        if r.get("known_typos"):
            j["known_typos"] = r["known_typos"]
        # fields added by the records layer; harmless to prior consumers
        j["venue_id"] = r.get("venue_id")
        j["venue_string"] = r.get("venue_string")
        j["status"] = r.get("status")
        j["record"] = f"records/{r['venue_id']}.json"
        j["editorial_structure"] = (r.get("editorial") or {}).get("structure")
        j["duoviri"] = (r.get("editorial") or {}).get("duoviri") or []
        j["offices"] = [o.get("title") + ": " + str(o.get("holder"))
                        for o in ((r.get("editorial") or {}).get("offices") or [])]
        journals.append(j)
    # keep the v1.2 ordering: creative first, then academic, province last
    order = {"creative": 0, "academic": 1, "province": 2}
    journals.sort(key=lambda j: (order.get(j.get("class"), 9), j["canonical"]))

    out = dict(prior)
    out["version"] = "2.0"
    out["generated"] = "2026-08-15"
    out["canonical_store"] = ("records/*.json — THE DATA. This file is a generated projection; "
                              "edit a record and run scripts/build_venues_index.py.")
    out["regenerate_with"] = "scripts/build_venues_index.py"
    out["schema_principle"] = ("A field can be null, but a datum without a field ends up not existing. "
                               "Records declare fields they may never fill.")
    out["journals"] = journals
    return json.dumps(out, ensure_ascii=False, indent=1) + "\n"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    new = build()
    if a.check:
        cur = INDEX.read_text() if INDEX.exists() else ""
        if cur != new:
            print("FAIL: venues.json has drifted from records/."); return 1
        print("OK: venues.json matches records/"); return 0
    INDEX.write_text(new)
    print(f"wrote {INDEX.relative_to(ROOT)} from {len(list(RECORDS.glob('*.json')))} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
