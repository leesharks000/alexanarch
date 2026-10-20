#!/usr/bin/env python3
"""per_atoms_merge.py — fold the entity pass (2026-10-19) into data/per-atom-sets.json.

The entity pass (rebuild/capture-registry/per-atoms/entity-pass/BRIEF.md) had eight readers confirm, for each of the 302
entities the Capture Registry's observations target, its template, its defining records and every atom's applicability, tokens
and reference, each carrying the record's own words with locus. 7,823 record quotes were checked verbatim against their files
and registry fields before this merge. Entities the pass did not reach (no observation targets them) keep their mechanical
first state, marked as such.

Corrections applied here, each stated:
  - identifiers are exempt from own-name pruning (Rule 5 governs names filling second atoms; a registry id such as
    EA-WG-CAPTURES-01 is an identifier and stays one);
  - the entities the readers found no defining record for take the no_atom_set gate (#1530 §2.3), with the reader's basis.
  python3 scripts/per_atoms_merge.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
EP = ROOT / "rebuild/capture-registry/per-atoms/entity-pass"
OUT = ROOT / "data/per-atom-sets.json"
T = json.loads((ROOT / "rebuild/capture-registry/per-atoms/templates.json").read_text(encoding="utf-8"))
doc = json.loads(OUT.read_text(encoding="utf-8"))
mech = {s["id"]: s for s in doc["entities"]}

NO_SET = {  # reader's basis, verbatim in substance
    "ENT-cd9c7d1072": "summarizer layer: no deposit defines the term or claims its coinage (registry titles, descriptions, keywords, defines_concepts and 138 full texts read); entity pass batch 7",
    "ENT-51e73d0d18": "executable scripture: the phrase occurs only in the capture registry, which calls the address a control with no archive presence; entity pass batch 8",
    "ENT-6caf9cd798": "In the Crimson Hexagon: an extraction artefact (a heading in #499's also-by list, marked 'not kept as a term' in data/lexical-minting-registry.json); the observation targets r.29 (#743); entity pass batch 8",
}
EXTRA_ID = {"Capture Registry": [{"token": "EA-WG-CAPTURES-01", "record_quote": "\"registry_id\": \"EA-WG-CAPTURES-01\"", "locus": "data/EA-WG-CAPTURES-01.json (top-level registry_id)"}]}

merged, n = [], 0
for i in range(1, 9):
    for e in json.loads((EP / f"out-{i}.json").read_text(encoding="utf-8")):
        n += 1
        if e["id"] in NO_SET:
            merged.append({"id": e["id"], "name": e["name"], "type": e.get("template"), "gate": "no_atom_set", "basis": NO_SET[e["id"]], "state": "entity pass 2026-10-19"})
            continue
        for a in e["atoms"]:
            if a["atom"] == "identifier" and e["name"] in EXTRA_ID:
                for x in EXTRA_ID[e["name"]]:
                    if x["token"] not in a.get("tokens", []):
                        a.setdefault("tokens", []).append(x["token"]); a.setdefault("evidence", []).append({"record_quote": x["record_quote"], "locus": x["locus"]})
        req = {d: sum(a["weight"] for a in e["atoms"] if a["dim"] == d and a["applicability"] == "required") for d in "MCD"}
        merged.append({"id": e["id"], "name": e["name"], "template": e["template"], "type_basis": e.get("type_basis"), "records": e.get("records"),
                       "atoms": e["atoms"], "required": req, "notes": e.get("notes"), "state": f"entity pass 2026-10-19, batch {i}"})
seen = {m["id"] for m in merged}
rest = [dict(s, state="mechanical first state (no observation targets this entity)") for k, s in mech.items() if k not in seen]
doc.update({"rubric": T["rubric"], "templates_status": T["status"], "count": len(merged) + len(rest),
            "with_atom_set": sum(1 for s in merged + rest if s.get("atoms")),
            "entity_pass": {"date": "2026-10-19", "entities": n, "brief": "rebuild/capture-registry/per-atoms/entity-pass/BRIEF.md",
                            "record_quotes_checked": 7823, "failures": 0},
            "entities": merged + rest})
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"merged {len(merged)} (no_atom_set {sum(1 for m in merged if m.get('gate') == 'no_atom_set')}), mechanical kept {len(rest)}")
