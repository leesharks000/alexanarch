"""Counts for the v12.559 snapshot deposit, computed from data/EA-WG-CAPTURES-01.json.  python3 stats.py -> stats.json"""
import json, pathlib, collections, statistics
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]
R = json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8")); E = R["entries"]
def obs(e):
    o = e.get("observations") or []
    if not o: return [e]
    return o
O = [(e, o) for e in E for o in obs(e)]
g = lambda e, o, k: o.get(k) if o.get(k) not in (None, "", []) else e.get(k)
sec = collections.Counter(e["s"] for e in E)
surf = collections.Counter((g(e, o, "surface") or "not recorded") for e, o in O)
def authk(a):
    a = (a or "").lower().strip()
    if not a: return "unrecorded"
    si = "signed in" in a or "logged in" in a; so = "signed out" in a or "logged out" in a; inc = "incognito" in a
    if si and not so: return "signed in"
    if so and inc: return "signed out and incognito"
    if inc: return "incognito"
    if so: return "signed out"
    return "other recorded states"
auth = collections.Counter(authk(g(e, o, "auth")) for e, o in O)
tr = sum(1 for e, o in O if (g(e, o, "transcript") or "").strip())
fr = sum(1 for e, o in O if g(e, o, "imgs"))
per = [g(e, o, "per") for e, o in O]; per = [p for p in per if isinstance(p, (int, float))]
pdim = sum(1 for e, o in O if o.get("per_dim") or (o is e and e.get("per_dim")))
pend = sum(1 for e, o in O if (o.get("per_dim_pending") if o is not e else e.get("per_dim_pending")))
dates = sorted({str(g(e, o, "date")) for e, o in O if g(e, o, "date")})
declared = sum(e.get("n_observations") or 1 for e in E)
defects = collections.Counter()
for e in E:
    for d in e.get("defects") or []:
        defects[d if isinstance(d, str) else (d.get("type") or d.get("kind") or json.dumps(d)[:40])] += 1
mismatch = [(e["slug"], e.get("n_observations"), len(e.get("observations") or [])) for e in E if (e.get("n_observations") or 1) != max(1, len(e.get("observations") or []))]
since = [c for c in R.get("correction_log", []) if str(c.get("date", "")) > "2026-10-12"]
out = {"version": R["version"], "date": R["date"], "addresses": len(E), "captures_held": len(O), "captures_declared": declared, "mismatch": mismatch,
       "sections": sec.most_common(), "surfaces": surf.most_common(), "auth": auth.most_common(), "transcript": tr, "frame": fr,
       "per_scored": len(per), "per_mean": round(statistics.mean(per), 3) if per else None, "per_dim_scored": pdim, "per_dim_pending": pend,
       "n_dates": len(dates), "first": dates[0], "last": dates[-1], "defects": defects.most_common(), "corrections_since_v12167": len(since),
       "correction_dates": sorted({c.get("date") for c in since})}
json.dump(out, open(H / "stats.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("surfaces",)}, ensure_ascii=False)[:3000]); print(out["surfaces"][:25])
