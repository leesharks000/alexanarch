#!/usr/bin/env python3
"""per_d_write.py — write the dimensional PER under rubric v1.1 (obs-pass-d/scored.json) into the Capture Registry.

Operator rulings 2026-10-19 23:57, 2026-10-20 00:01, 00:03, 00:13 (quoted in templates.json v1_1). For every observation re-read,
per_dim is replaced by the v1.1 reading (PER-M and PER-C presence as at v12.305, PER-D re-read; inversions, standing substitutions);
the v1.0 per_dim is kept beside it as per_dim_v1_0, and per, per_v and per_corrected are untouched. The observations held at v12.305
are written for the first time against their true targets (retarget pass). Held observations that could not be read (misfiled
transcripts; addresses with no record) are written with the no_atom_set gate and the reason. Observations not re-read (ABN, no PER-D
atom) keep their v1.0 per_dim unchanged.
  python3 scripts/per_d_write.py [--check]
"""
import json, pathlib, sys, collections, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "data/EA-WG-CAPTURES-01.json"
OD = ROOT / "rebuild/capture-registry/per-atoms/obs-pass-d"
SC = json.loads((OD / "scored.json").read_text(encoding="utf-8"))
HI = json.loads((OD / "held-index.json").read_text(encoding="utf-8"))
SPEC = "PER-dim rubric v1.1"


def pd_of(r):
    basis = "; ".join(x for x in [
        ("reached: " + str(r.get("reached_basis"))[:300]) if r.get("reached_basis") else "",
        ("beneath the gate: PER " + str((r.get("beneath") or {}).get("PER"))) if r.get("beneath") else "",
        "tombstone pointer: a severed record presented as live" if r.get("tombstone_pointer") else "",
        ("retargeted: " + str(r.get("retarget_basis"))[:300]) if r.get("retargeted") else ""] if x)
    return {"spec": SPEC, "entity_type": r["target"].get("template"), "target": {"ent": r["target"]["id"], "name": r["target"]["name"]},
            "qualifier": r.get("qualifier"), "reached": r["reached"], "gate": r["gate"],
            "atoms": [{k: a.get(k) for k in ("atom", "dim", "weight", "kind", "present", "evidence")} for a in r["atoms"]],
            "inversions": r.get("inversions") or [], "standing_substitutions": r.get("standing_substitutions") or [],
            "scores": r["scores"], "src": r.get("src"), "tombstone_pointer": bool(r.get("tombstone_pointer")),
            "after_challenge": r.get("after_challenge"), "basis": basis,
            "read": {"by": ("held-observation reader, " + str(r["batch_d"])) if r.get("retargeted") else "deep-dimension reader, batch %s" % r["batch_d"],
                     "on": "2026-10-20", "brief": "rebuild/capture-registry/per-atoms/obs-pass-d/" + ("HELD-BRIEF.md" if r.get("retargeted") else "BRIEF.md"),
                     "m_c_from": None if r.get("retargeted") else "v12.305 (PER-dim rubric v1.0 reading)"}}


def main():
    reg = json.loads(P.read_text(encoding="utf-8"))
    by = collections.defaultdict(list)
    for r in SC["rows"]:
        by[(r["entry"], str(r["obs_index"]))].append(r)
    unread = {(k, s): why for k, s, why in HI["not_read"]}
    stats = collections.Counter()
    for e in reg["entries"]:
        obs = e["observations"] if e.get("observations") else [e]
        for i, o in enumerate(obs, 1):
            rows = by.get((e["slug"], str(i)))
            if rows:
                r = rows.pop(0)
                if o.get("per_dim"):
                    o["per_dim_v1_0"] = o["per_dim"]
                o["per_dim"] = pd_of(r)
                stats["held_written" if r.get("retargeted") else "rewritten"] += 1
                continue
            key = o.get("obs_id") or e.get("obs_id")
            hit = next((why for (k, s), why in unread.items() if s in (o.get("slug"), e["slug"]) and k in (key, e.get("obs_id"), None)), None)
            if not o.get("per_dim") and hit:
                o["per_dim"] = {"spec": SPEC, "entity_type": None, "target": None, "reached": "unread", "gate": "no_atom_set", "atoms": [],
                                "scores": {"PER": None, "M": None, "C": None, "D": None}, "src": None,
                                "basis": "held at v12.305; " + ("the seated transcript belongs to another address (misfiled): the observation is gated until its own frame is found"
                                                                if hit == "misfiled" else "the address has no archive referent (no defining record): no atom set")}
                stats["held_unread"] += 1
            else:
                stats["kept_v1_0" if o.get("per_dim") else "no_per_dim"] += 1
        if e.get("observations"):
            root = next((x for x in e["observations"] if x.get("obs_id") and x.get("obs_id") == e.get("obs_id")), e["observations"][0])
            if root.get("per_dim"):
                e["per_dim"] = root["per_dim"]
    left = sum(len(v) for v in by.values())
    print(dict(stats), "rows unplaced", left)
    if "--check" in sys.argv or left:
        return
    old = reg["version"]; mj, mn = old.split(".")
    reg["version"] = f"{mj}.{int(mn) + 1}"; reg["date"] = "2026-10-20"
    rows = SC["rows"]
    reg.setdefault("correction_log", []).append({
        "date": "2026-10-20", "change": f"version {old} → {reg['version']}; dimensional PER re-read under PER-dim rubric v1.1 (deep dimension: purpose and commitments; inversion; standing substitution)",
        "detail": ("Operator, 2026-10-19 23:57: 'deep provenance describes an entity's purpose and commitments. deposit chain, identifier, and licence are poor proxies for that. mostly irrelevant.' "
                   "2026-10-20 00:01: 'identifier and deposit chain matter when they advance the purpose of the entity … and yes - inversion is a core mechanism of per-d'. "
                   "00:03: 'erasure skew happens regularly when standing is substituted as an evaluative proxy for evidence, argument, and/or beauty'. "
                   "00:13: 'standing substitutions can go into 1.1, and well leave beauty recorded only for now … it can still be erasure even if uptake fulfills its purpose with or without attribution'. "
                   "Entity pass (deep dimension): 299 entities, 8 readers; retargeting of the 84 held observations: 2 readers, 26 new target sets; calibration: two blind readers on ten observations "
                   "(48/50 atom readings agreed; the two divisions ruled into calibration_rules_d); observation pass: 24 readers over 824 observations (PER-D only; PER-M and PER-C as at v12.305) and "
                   f"3 readers over 80 held observations (in full). Every reader span checked verbatim by scripts/per_d_verify.py (1,800 spans, 0 misses). Scores by scripts/per_d_score.py. "
                   f"Written: {dict(stats)}. Inversions recorded {sum(len(r['inversions']) for r in rows)}; standing substitutions {sum(len(r['standing_substitutions']) for r in rows)}; "
                   f"tombstone pointers {sum(1 for r in rows if r['tombstone_pointer'])}. The v1.0 reading is kept on each observation as per_dim_v1_0; per, per_v and per_corrected unchanged.")})
    P.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
