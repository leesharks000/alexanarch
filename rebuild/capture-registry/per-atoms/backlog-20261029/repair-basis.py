"""Repair 2026-10-29: per_dim.basis written whole. scripts/per_backlog.py cut the reached span at 300 characters and the reader's
basis note at 400, leaving the basis mid-word on the 58 backlog observations and the 15 labor captures scored at intake (found by
the /non composers of berkeley-negotiating-tech and stanford-canaries). The basis is recomputed from the readers' own outputs
(backlog-20261029/scored.json; intake-20261029-labor/per/out-L1..L3.json scored again by the same functions) with the patched pd_of,
and only per_dim.basis is replaced. Scores, atoms and every other field are untouched.
  python3 repair-basis.py [--check]"""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import per_backlog as PB
P = ROOT / "data/EA-WG-CAPTURES-01.json"
rows = json.loads((H / "scored.json").read_text(encoding="utf-8"))["rows"]
PB.BD = ROOT / "rebuild/capture-registry/intake-20261029-labor/per"; PB.GROUPS = ["L1", "L2", "L3"]
sets, by, groups = PB.load()
rows += PB.score(by, {}, groups)
want = {(r["entry"], int(r["obs_index"])): PB.pd_of(r)["basis"] for r in rows}
reg = json.loads(P.read_text(encoding="utf-8"))
done = 0
for e in reg["entries"]:
    obs = e["observations"] if e.get("observations") else [e]
    for i, o in enumerate(obs, 1):
        b = want.pop((e["slug"], i), None)
        if b is None or not o.get("per_dim"): continue
        if e.get("observations") and e.get("per_dim") is not None and e["per_dim"].get("basis") == o["per_dim"].get("basis") and o.get("obs_id") == e.get("obs_id"):
            e["per_dim"]["basis"] = b
        o["per_dim"]["basis"] = b; done += 1
assert not want, ("unplaced", list(want)[:5])
print("basis rewritten on", done, "observations")
if "--check" not in sys.argv:
    P.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
