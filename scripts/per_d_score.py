#!/usr/bin/env python3
"""per_d_score.py — compute the dimensional PER under rubric v1.1 (2026-10-20).

PER-M and PER-C presence stand as read at v12.305 (obs-pass/scored.json). PER-D presence, inversions, standing substitutions and
tombstone pointers come from the deep-dimension observation pass (obs-pass-d/out-N.json, joined by position with the batch inputs
listed in obs-pass-d/batches-index.json). The 80 observations held from the v1.0 write are read in full against their new targets
(obs-pass-d/held-out-N.json); for those the v1.0 normalisations N1–N3 (scripts/per_dim_score.py) are applied to M and C atoms.
Weights from data/per-atom-sets.json (v1.1 PER-D: purpose 3, commitments 2, lineage 2, identifier 1, deposit chain 1). An atom
used in an inversion is absent (templates.json v1_1). Gates as in v1.0: abn -> null; target_absent -> 1.0 with the atoms beneath.
Scores are computed here, never by a reader. Writes obs-pass-d/scored.json.
  PER_D_IN=<batch dir> python3 scripts/per_d_score.py
"""
import json, pathlib, os, collections, datetime, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import per_dim_score as V  # score(), first_segment(), norm(), written(), WORKS, SETS
PA = ROOT / "rebuild/capture-registry/per-atoms"
OD = PA / "obs-pass-d"
IN = pathlib.Path(os.environ["PER_D_IN"])
SETS = {s["id"]: s for s in json.loads((ROOT / "data/per-atom-sets.json").read_text(encoding="utf-8"))["entities"]}
SC = json.loads((PA / "obs-pass/scored.json").read_text(encoding="utf-8"))["rows"]
ABSENT = {"substitute", "proximal_substitute", "generic", "refused"}


def apply_inv(pres, inv):
    for x in inv or []:
        if x.get("atom") in pres:
            pres[x["atom"]] = False
    return pres


def final(gate, sc):
    if gate == "abn":
        return {d: None for d in sc}
    if gate == "target_absent":
        return {d: (1.0 if sc[d] is not None else None) for d in sc}
    return sc


def main():
    v10 = collections.defaultdict(list)
    for r in SC:
        v10[(r["key"], str(r["entry"]), str(r["obs_index"]))].append(r)
    rows, stats = [], collections.Counter()
    idx = json.loads((OD / "batches-index.json").read_text(encoding="utf-8"))
    for b in idx:
        B = json.loads((IN / f"batch-{b['batch']}.json").read_text(encoding="utf-8"))
        O = json.loads((OD / f"out-{b['batch']}.json").read_text(encoding="utf-8"))
        assert len(B) == len(O), b["batch"]
        for it, r in zip(B, O):
            assert r["key"] == it["key"], (b["batch"], r["key"], it["key"])
            old = v10[(it["key"], str(it["entry"]), str(it["obs_index"]))].pop(0)
            s = SETS[it["target"]["id"]]
            req = [a for a in s["atoms"] if a["applicability"] == "required"]
            pres = {a["atom"]: a["present"] for a in old["atoms"] if a["dim"] in "MC" and a["applicability"] == "required"}
            spans = {a["atom"]: a["evidence"] for a in old["atoms"] if a["dim"] in "MC"}
            for a in r["atoms"]:
                pres[a["atom"]] = bool(a.get("present")); spans[a["atom"]] = a.get("span")
            apply_inv(pres, r.get("inversions"))
            sc = V.score(pres, req)
            ac = r.get("after_challenge")
            ac_out = None
            if ac and old.get("after_challenge"):
                ap = {a["atom"]: a["present"] for a in old["atoms"] if a["dim"] in "MC"}  # v1.0 after-challenge M/C atoms are not kept per atom; carried from the first answer
                for a in ac.get("atoms", []):
                    ap[a["atom"]] = bool(a.get("present"))
                apply_inv(ap, ac.get("inversions"))
                ak = old["after_challenge"]["reached"]
                ac_out = {"turn": ac.get("turn"), "reached": ak, "scores": ({d: 1.0 for d in "MCD"} | {"PER": 1.0}) if ak in ABSENT else V.score(ap, req),
                          "inversions": ac.get("inversions") or [], "standing_substitutions": ac.get("standing_substitutions") or [], "d_only": True}
            elif ac:
                ac_out = {"turn": ac.get("turn"), "inversions": ac.get("inversions") or [], "standing_substitutions": ac.get("standing_substitutions") or [], "d_only": True}
            rows.append(old | {"rubric": "v1.1", "scores": final(old["gate"], sc), "beneath": sc if old["gate"] != "scored" else None,
                               "atoms": [{"atom": a["atom"], "dim": a["dim"], "weight": a["weight"], "kind": a.get("kind"), "applicability": "required",
                                          "present": pres.get(a["atom"], False), "evidence": spans.get(a["atom"])} for a in req],
                               "inversions": r.get("inversions") or [], "standing_substitutions": r.get("standing_substitutions") or [],
                               "tombstone_pointer": bool(old.get("tombstone_pointer")) or bool(r.get("tombstone_pointer")),
                               "after_challenge": ac_out if ac_out else old.get("after_challenge"),
                               "notes_d": r.get("notes"), "batch_d": b["batch"], "v1_0_scores": old["scores"]})
            stats[old["gate"]] += 1
    # held observations, read in full
    hidx = json.loads((OD / "held-index.json").read_text(encoding="utf-8"))
    for b in hidx["batches"]:
        B = json.loads((IN / f"{b['batch']}.json").read_text(encoding="utf-8"))
        O = json.loads((OD / f"held-out-{b['batch'].split('-')[1]}.json").read_text(encoding="utf-8"))
        assert len(B) == len(O), b["batch"]
        for it, r in zip(B, O):
            assert r["key"] == it["key"]
            s = SETS[it["target"]["id"]]
            req = [a for a in s["atoms"] if a["applicability"] == "required"]
            pres = {a["atom"]: bool(a.get("present")) for a in r["atoms"]}
            spans = {a["atom"]: a.get("span") for a in r["atoms"]}
            seg = V.norm(V.first_segment(it["transcript"]))
            how = {}
            for a in req:
                n = a["atom"]
                if pres.get(n) or a["dim"] == "D":
                    continue
                if n in ("date", "dates"):
                    hit = next((w for tk in a.get("tokens") or [] for w in V.written(tk) if V.norm(w) in seg), None)
                    if hit:
                        pres[n] = True; spans[n] = hit; how[n] = "N3"
            apply_inv(pres, r.get("inversions"))
            kind = (r.get("reached") or {}).get("kind"); abn = bool((r.get("reached") or {}).get("abn"))
            gate = "abn" if abn else ("target_absent" if kind in ABSENT else "scored")
            sc = V.score(pres, req)
            ac = r.get("after_challenge")
            ac_out = None
            if ac:
                ap = {a["atom"]: bool(a.get("present")) for a in ac.get("atoms", [])}
                apply_inv(ap, ac.get("inversions"))
                ak = (ac.get("reached") or {}).get("kind")
                ac_out = {"turn": ac.get("turn"), "reached": ak, "scores": ({d: 1.0 for d in "MCD"} | {"PER": 1.0}) if ak in ABSENT else V.score(ap, req),
                          "inversions": ac.get("inversions") or [], "standing_substitutions": ac.get("standing_substitutions") or []}
            rows.append({"key": it["key"], "entry": it["entry"], "obs_index": it["obs_index"], "slug": it["slug"], "rubric": "v1.1", "retargeted": True,
                         "target": it["target"], "qualifier": it.get("qualifier"), "retarget_basis": it.get("retarget_basis"),
                         "reached": kind, "abn": abn, "gate": gate, "scores": final(gate, sc), "beneath": sc if gate != "scored" else None,
                         "src": r.get("src"), "tombstone_pointer": bool(r.get("tombstone_pointer")), "scored_object": r.get("scored_object"),
                         "atoms": [{"atom": a["atom"], "dim": a["dim"], "weight": a["weight"], "kind": a.get("kind"), "applicability": "required",
                                    "present": pres.get(a["atom"], False), "evidence": spans.get(a["atom"]), "normalised": how.get(a["atom"])} for a in req],
                         "inversions": r.get("inversions") or [], "standing_substitutions": r.get("standing_substitutions") or [],
                         "after_challenge": ac_out, "reached_basis": (r.get("reached") or {}).get("span"), "notes": r.get("notes"), "batch_d": b["batch"]})
            stats["held_" + gate] += 1
    left = sum(len(v) for v in v10.values())
    (OD / "scored.json").write_text(json.dumps({"rubric": "PER-dim rubric v1.1", "computed": datetime.date.today().isoformat(), "rows": rows},
                                               ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    sc = [r["scores"]["PER"] for r in rows if r["gate"] == "scored" and r["scores"]["PER"] is not None]
    dd = [r["scores"]["D"] for r in rows if r["gate"] == "scored" and r["scores"]["D"] is not None]
    old = [r["v1_0_scores"]["D"] for r in rows if r.get("v1_0_scores") and r["gate"] == "scored" and r["v1_0_scores"]["D"] is not None]
    print(len(rows), "rows", dict(stats), "v1.0 rows not re-read", left)
    print(f"PER mean {sum(sc)/len(sc):.3f} over {len(sc)}; D mean v1.1 {sum(dd)/len(dd):.3f}; D mean v1.0 {sum(old)/len(old):.3f}")
    print("inversions", sum(len(r["inversions"]) for r in rows), "standing substitutions", sum(len(r["standing_substitutions"]) for r in rows),
          "tombstone pointers", sum(1 for r in rows if r["tombstone_pointer"]))


if __name__ == "__main__":
    main()
