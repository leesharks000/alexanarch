#!/usr/bin/env python3
"""per_atoms_d_merge.py — merge the deep-dimension entity pass and the retargeting into data/per-atom-sets.json (PER-dim rubric v1.1).

Operator, 2026-10-19 23:57 and 2026-10-20 00:01 (quoted in templates.json v1_1): PER-D is the entity's purpose and commitments;
identifier and deposit chain count where they advance the purpose; inversion is a core mechanism of PER-D.

  1. entity-pass-d/out-1..8.json: each entity's v1.0 PER-D atoms (lineage, identifier, deposit chain, licence) are replaced by the
     v1.1 atoms (purpose 3, commitments 2, lineage 2, identifier 1, deposit chain 1) with their record quotes; the v1.0 atoms are
     kept under d_v1_0 so the earlier instantiation stays readable; inversion_guidance is added.
  2. retarget/out-1..2.json: new atom sets for the true targets of the held observations. Two readers built some of the same
     targets; duplicates are merged under one id (ALIAS below), the fuller set kept, the other kept under alternate.
     Target ids are TGT-<slug> (atom-set targets with no entity-register row yet).
  3. retarget/targets.json: each held observation's key -> target id, qualifier, misfiled, basis (both readers' choices where they differ).
Quotes are checked by the readers' scripts and again by an independent check before this runs.
  python3 scripts/per_atoms_d_merge.py [--check]
"""
import json, pathlib, sys, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]
PA = ROOT / "rebuild/capture-registry/per-atoms"
P = ROOT / "data/per-atom-sets.json"
ALIAS = {  # batch-2 slug -> canonical slug (same defining deposits)
    "h-core-formal-specification-v2-6-tuple": "h-core-formal-specification",
    "leesharks-the-final-time-dataset": "leesharks-the-final-time",
    "leesharks-hugging-face-datasets": "alexanarch-dataset-set",
}
D_ORDER = ["purpose", "commitments", "lineage", "identifier", "deposit chain"]


def req(atoms):
    return sum(1 for a in atoms if a.get("applicability") == "required")


def main():
    S = json.loads(P.read_text(encoding="utf-8"))
    by = {e["id"]: e for e in S["entities"]}
    stats = collections.Counter()
    for i in range(1, 9):
        for o in json.loads((PA / f"entity-pass-d/out-{i}.json").read_text(encoding="utf-8")):
            e = by.get(o["id"])
            if e is None:
                stats["unmatched"] += 1; continue
            old = [a for a in e["atoms"] if a["dim"] == "D"]
            new = sorted([a | {"dim": "D"} for a in o["atoms"]], key=lambda a: D_ORDER.index(a["atom"]) if a["atom"] in D_ORDER else 9)
            e["atoms"] = [a for a in e["atoms"] if a["dim"] != "D"] + new
            e["d_v1_0"] = old
            e["inversion_guidance"] = o.get("inversion_guidance")
            if o.get("notes"):
                e["notes_d"] = o["notes"]
            e["state_d"] = f"entity pass, deep dimension (rubric v1.1) 2026-10-20, batch {i}"
            stats["entities_d"] += 1
            for a in new:
                stats["d_" + a["applicability"]] += 1
    sets, obs = {}, {}
    for i in (1, 2):
        O = json.loads((PA / f"retarget/out-{i}.json").read_text(encoding="utf-8"))
        for s in O["new_atom_sets"]:
            slug = ALIAS.get(s["new"], s["new"])
            s = s | {"built_by": f"retarget reader, batch {i}"}
            if slug in sets:
                a, b = sets[slug], s
                keep, alt = (a, b) if req(a["atoms"]) >= req(b["atoms"]) else (b, a)
                keep = keep | {"alternate": {k: alt[k] for k in ("new", "name", "records", "built_by") if k in alt}}
                sets[slug] = keep
                stats["duplicates_merged"] += 1
            else:
                sets[slug] = s
        for x in O["observations"]:
            t = x["target"] or {}
            tid = t.get("id") or (("TGT-" + ALIAS.get(t["new"], t["new"])) if t.get("new") else None)
            obs.setdefault(x["key"] + "|" + str(x.get("obs")), []).append(x | {"target_id": tid, "batch": i})
    for slug, s in sets.items():
        tid = "TGT-" + slug
        ent = {"id": tid, "name": s["name"], "template": s.get("template"), "type_basis": s.get("type_basis"), "records": s.get("records"),
               "atoms": s.get("atoms") or [], "inversion_guidance": s.get("inversion_guidance"), "notes": s.get("notes"),
               "state": "retarget pass 2026-10-20 (" + s["built_by"] + "); a target with no entity-register row yet"}
        if s.get("alternate"):
            ent["alternate"] = s["alternate"]
        if tid in by:
            by[tid].update(ent)
        else:
            S["entities"].append(ent); by[tid] = ent
        stats["new_sets"] += 1
    disagree = [k for k, v in obs.items() if len({y["target_id"] for y in v}) > 1]
    print(dict(stats), "observations", len(obs), "readers disagree on", len(disagree))
    if "--check" in sys.argv:
        return
    S["rubric"] = "PER-dim rubric v1.1"
    S["count"] = len(S["entities"])
    S["with_atom_set"] = sum(1 for e in S["entities"] if e.get("atoms"))
    S["entity_pass_d"] = {"date": "2026-10-20", "brief": "rebuild/capture-registry/per-atoms/entity-pass-d/BRIEF.md", "readers": 8,
                          "entities": stats["entities_d"], "applicability": {k[2:]: v for k, v in stats.items() if k.startswith("d_")},
                          "retarget": {"brief": "rebuild/capture-registry/per-atoms/retarget/BRIEF.md", "readers": 2, "new_sets": stats["new_sets"],
                                       "duplicates_merged": stats["duplicates_merged"]}}
    P.write_text(json.dumps(S, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (PA / "retarget/targets.json").write_text(json.dumps({"observations": obs, "disagree": disagree}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
