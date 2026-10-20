#!/usr/bin/env python3
"""per_d_batches.py — build the reader inputs for the deep-dimension observation pass (PER-dim rubric v1.1).

Each item is an observation the v1.0 pass read (the batch inputs under PER_BATCHES, joined by position with obs-pass/scored.json),
with its v1.0 reached and gate, and its target's PER-D atoms under v1.1 from data/per-atom-sets.json. Observations held from the
v1.0 write (obs-pass/held.json) are excluded here: they are read in full against their new targets.
  python3 scripts/per_d_batches.py calib KEY... -> obs-pass-d/calibration/set.json
  python3 scripts/per_d_batches.py batches N    -> PER_D_OUT/batch-1..N.json  (default the scratchpad given by PER_D_OUT)
"""
import json, pathlib, os, sys, hashlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
PA = ROOT / "rebuild/capture-registry/per-atoms"
BD = pathlib.Path(os.environ.get("PER_BATCHES", PA / "obs-pass"))
SETS = {s["id"]: s for s in json.loads((ROOT / "data/per-atom-sets.json").read_text(encoding="utf-8"))["entities"]}
SC = json.loads((PA / "obs-pass/scored.json").read_text(encoding="utf-8"))["rows"]
HELD = {h["key"] for h in json.loads((PA / "obs-pass/held.json").read_text(encoding="utf-8"))}


def d_atoms(s):
    out = []
    for a in s.get("atoms", []):
        if a["dim"] != "D":
            continue
        out.append({k: a.get(k) for k in ("atom", "weight", "kind", "applicability", "tokens", "reference", "why")}
                   | {"record_quotes": [e["record_quote"][:400] for e in (a.get("evidence") or [])][:6]})
    return out


def items():
    out, i = [], 0
    for b in range(1, 25):
        for it in json.loads((BD / f"batch-{b}.json").read_text(encoding="utf-8")):
            r = SC[i]; i += 1
            assert r["key"] == it["key"] and r["entry"] == it["entry"]
            s = SETS[it["target"]["id"]]
            out.append({"key": it["key"], "entry": it["entry"], "obs_index": it["obs_index"], "slug": it["slug"], "q": it["q"],
                        "surface": it["surface"], "date": it["date"], "transcript_class": it.get("transcript_class"),
                        "transcript": it["transcript"], "cards": it.get("cards"),
                        "target": {"id": s["id"], "name": s["name"], "template": s.get("template")},
                        "v1_0": {"reached": r["reached"], "abn": r["abn"], "gate": r["gate"], "basis": (r.get("reached_basis") or "")[:300]},
                        "d_atoms": d_atoms(s), "inversion_guidance": s.get("inversion_guidance")})
    return out


def main():
    allit = items()
    if sys.argv[1] == "calib":
        keys = sys.argv[2:]
        sel = [next(x for x in allit if x["key"] == k) for k in keys]
        p = PA / "obs-pass-d/calibration/set.json"; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(sel, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(len(sel), "calibration items")
        return
    if sys.argv[1] == "held":  # the retargeted observations, read in full (reached, M, C, D) against their new targets
        n = int(sys.argv[2])
        TG = json.loads((PA / "retarget/targets.json").read_text(encoding="utf-8"))["observations"]
        todo, skip = [], []
        for x in allit:
            if x["key"] not in HELD:
                continue
            t = TG.get(x["key"] + "|" + x["slug"])
            if t is None:
                t = next((v for k, v in TG.items() if k.startswith(x["key"] + "|") and v[0]["entry"] == x["entry"]), None)
            t = t[0] if t else None
            s = SETS.get((t or {}).get("target_id") or "")
            if not t or t.get("misfiled") or not s or not s.get("atoms"):
                skip.append([x["key"], x["slug"], "misfiled" if t and t.get("misfiled") else "no atom set"]); continue
            x = x | {"target": {"id": s["id"], "name": s["name"], "template": s.get("template")}, "qualifier": t.get("qualifier"),
                     "retarget_basis": t.get("basis"), "inversion_guidance": s.get("inversion_guidance"), "atom_set": {"atoms": [{k: a.get(k) for k in ("atom", "dim", "weight", "kind", "applicability", "tokens", "reference", "why")}
                                                                         | {"record_quotes": [e["record_quote"][:400] for e in (a.get("evidence") or [])][:6]} for a in s["atoms"]]}}
            x.pop("d_atoms"); x.pop("v1_0")
            todo.append(x)
        od = pathlib.Path(os.environ["PER_D_OUT"]); od.mkdir(parents=True, exist_ok=True)
        idx = []
        for b in range(n):
            part = todo[b::n]; t = json.dumps(part, ensure_ascii=False, indent=1) + "\n"
            (od / f"held-{b+1}.json").write_text(t, encoding="utf-8")
            idx.append({"batch": "held-%d" % (b + 1), "n": len(part), "keys": [[x["key"], x["entry"], x["obs_index"]] for x in part], "sha256": hashlib.sha256(t.encode()).hexdigest()})
        (PA / "obs-pass-d/held-index.json").write_text(json.dumps({"batches": idx, "not_read": skip}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(len(todo), "held items in", n, "batches; not read", skip)
        return
    n = int(sys.argv[2])
    todo = [x for x in allit if x["key"] not in HELD and x["v1_0"]["gate"] != "abn" and any(a["applicability"] == "required" for a in x["d_atoms"])]
    od = pathlib.Path(os.environ["PER_D_OUT"]); od.mkdir(parents=True, exist_ok=True)
    idx = []
    for b in range(n):
        part = todo[b::n]
        t = json.dumps(part, ensure_ascii=False, indent=1) + "\n"
        (od / f"batch-{b+1}.json").write_text(t, encoding="utf-8")
        idx.append({"batch": b + 1, "n": len(part), "keys": [[x["key"], x["entry"], x["obs_index"]] for x in part], "sha256": hashlib.sha256(t.encode()).hexdigest()})
    (PA / "obs-pass-d/batches-index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(todo), "items in", n, "batches; excluded held", sum(1 for x in allit if x["key"] in HELD), "abn", sum(1 for x in allit if x["v1_0"]["gate"] == "abn"))


if __name__ == "__main__":
    main()
