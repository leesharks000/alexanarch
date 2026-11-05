#!/usr/bin/env python3
"""Two-epoch match (frozen plan PLAN-epoch.md, sha256 1b3234fa...). Reads only stored files: ../pks/fb_blc*.json, ../lee/lee.json."""
import glob, hashlib, json, pathlib, bisect
import numpy as np
H = pathlib.Path(__file__).resolve().parent
PLAN = hashlib.sha256((H / "PLAN-epoch.md").read_bytes()).hexdigest()
assert PLAN.startswith("1b3234fa"), PLAN
# Parkes candidates and node spans
P, spans = [], []
for p in sorted(glob.glob(str(H.parent / "pks/fb_blc*.json"))):
    d = json.load(open(p)); top = d["fch1_MHz"]; spans.append((top - 128.0, top))
    for b in d["blocks"].values():
        for c in b["cands"]:
            P.append((c["f_rest_MHz"] * 1e6, d["node"], c))
P.sort(key=lambda x: x[0]); PF = np.array([x[0] for x in P])
def covered(f): return any(lo * 1e6 < f < hi * 1e6 for lo, hi in spans)
# Green Bank clusters, merged at 10 Hz per channel
L = json.load(open(H.parent / "lee/lee.json"))["channels"]
G = []  # (f_Hz, channel)
for ch, v in L.items():
    fs = sorted(f * 1e6 for f in v["freqs"]); cl = []
    for f in fs:
        if cl and f - cl[-1][-1] <= 10.0: cl[-1].append(f)
        else: cl.append([f])
    for c in cl: G.append((float(np.mean(c)), ch, len(c)))
dense = {ch for ch, v in L.items() if v["T"] > 50}
thirteen_ch = "blc23_cc07"
def nearest(f):
    i = bisect.bisect_left(PF, f); best = None
    for j in (i - 1, i):
        if 0 <= j < len(PF):
            dd = abs(PF[j] - f)
            if best is None or dd < best[0]: best = (dd, j)
    return best
def M(sel, d, shift=0.0):
    n = 0
    for f, ch, k in sel:
        g = f + shift
        if not covered(g): continue
        b = nearest(g)
        if b and b[0] <= d: n += 1
    return n
sets = {"primary": [g for g in G if g[1] not in dense], "all": G, "thirteen": [g for g in G if g[1] == thirteen_ch]}
rng = np.random.default_rng(5)
mag = rng.uniform(1e3, 50e3, 400); sgn = rng.choice([-1.0, 1.0], 400); shifts = mag * sgn
out = {"plan_sha256": PLAN, "parkes_candidates": len(P), "gbt_clusters": {k: len(v) for k, v in sets.items()},
       "gbt_clusters_in_parkes_coverage": {k: sum(covered(f) for f, _, _ in v) for k, v in sets.items()},
       "dense_channels": sorted(dense), "results": {}, "pairs": []}
for name, sel in sets.items():
    for d in (10.0, 50.0):
        t = M(sel, d); null = np.array([M(sel, d, s) for s in shifts])
        out["results"][f"{name}_d{int(d)}"] = {"M": t, "null_mean": round(float(null.mean()), 3), "null_sd": round(float(null.std()), 3),
                                               "null_max": int(null.max()), "p": float((null >= t).mean())}
for f, ch, k in G:
    if not covered(f): continue
    b = nearest(f)
    if b and b[0] <= 50.0:
        pf, node, c = P[b[1]]
        out["pairs"].append({"gbt_channel": ch, "gbt_f_rest_MHz": round(f / 1e6, 6), "gbt_cluster_channels": k, "parkes_node": node,
                             "parkes_f_rest_MHz": c["f_rest_MHz"], "parkes_f_topo_MHz": c["f_topo0_MHz"], "diff_Hz": round(pf - f, 2),
                             "parkes_z": c["z"], "dense": ch in dense})
r = out["results"]
out["verdict"] = {"primary_lead": r["primary_d10"]["p"] <= 0.01,
                  "thirteen_lead": r["thirteen_d10"]["M"] >= 1 and r["thirteen_d10"]["p"] <= 0.01}
json.dump(out, open(H / "epoch.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("parkes_candidates", "gbt_clusters", "gbt_clusters_in_parkes_coverage", "results", "verdict")}, indent=1))
print("pairs within 50 Hz:", len(out["pairs"]))
for q in out["pairs"]: print(q["gbt_channel"], q["gbt_f_rest_MHz"], q["parkes_node"], q["parkes_f_rest_MHz"], q["diff_Hz"], q["dense"])
