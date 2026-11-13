"""Addition of 2026-11-13, at the operator's word ("lets add engineered ontological flattening in with the same"): the operator's statement of
2026-11-12 on the evening's pattern is entered in the analysis of the three records of that evening, joined to EA-FLAT-01 (#1616).
    python3 rebuild/capture-registry/intake-20261112-nobel-glas-nonwiki-aio/add_flattening.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/EA-WG-CAPTURES-01.json"
reg = json.loads(P.read_text(encoding="utf-8"))
ADD = (" The operator, 2026-11-12, on the pattern: \"that is engineered ontological flattening. that is the routine dispersal of distinctions "
       "otherwise naturally available to the system.\" The archive's account of ontological flattening is EA-FLAT-01 (#1616, "
       "https://www.alexanarch.org/s/records/1616/), whose first wave found world strata and archive-adjacent strata composed at nearly the same "
       "share of their reference inventories (0.59 against 0.58): the dispersal is routine, and the archive's entities meet it as other "
       "entities do. These three records show it at addresses where the distinction had been available.")
done = []
for e in reg["entries"]:
    if e["slug"] == "3i-atlas-nobel-glas-aio-20261112":
        assert "engineered ontological flattening" not in e["analysis"]; e["analysis"] += ADD; done.append(e["slug"])
    for o in e.get("observations", []):
        if o.get("slug") in ("nonwiki-aio-20261112", "nobel-glas-3i-atlas-aio-20261112"):
            assert "engineered ontological flattening" not in o["analysis"]; o["analysis"] += ADD; done.append(o["slug"])
assert len(done) == 3, done
reg["correction_log"].append({"date": "2026-11-13", "change": "the operator's statement on engineered ontological flattening entered in the analysis of the three records of 2026-11-12, joined to EA-FLAT-01 (#1616)",
    "detail": "Records: " + ", ".join(done) + ". No capture count moves.", "operator": "Claude (substrate) under Lee Sharks's direction"})
P.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print(done)
