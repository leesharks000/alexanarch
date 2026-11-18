"""PLAN-L over r13 part J's products.  python3 lanalyze.py > L.json"""
import os, sys, json
import numpy as np
from scipy.ndimage import maximum_filter1d
HERE = os.path.dirname(os.path.abspath(__file__)); JO = os.path.join(HERE, "../J/out")
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
N = dm.N; SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; OFF = ["0014", "0016", "0018"]; NF = 401
D = {s: np.load(os.path.join(JO, f"{s}.npz")) for s in SC}
offs = D["0013"]["offs"]; near = np.argsort(np.abs(offs[1:]))[:40]

def reg(V, fi, m=1):
    v0r = float(D["0013"][f"m{m}_{V}_f{fi}_v0"]); A = {}
    for s in SC:
        d = D[s]; idx = d[f"m{m}_{V}_f{fi}_idx"].astype(np.int64); z = d[f"m{m}_{V}_f{fi}_z"].astype(np.float32)
        sh = int(np.rint(m * dm.FC * (float(d[f"m{m}_{V}_f{fi}_v0"]) - v0r) / dm.C / dm.DF))
        a = np.full(N + 4000, -99.0, np.float32); j = idx - sh + 2000; ok = (j >= 0) & (j < len(a))
        np.maximum.at(a, j[ok], z[ok]); A[s] = maximum_filter1d(a, 3, mode="nearest")
    return A

def clusters(idx, gap=4): return 0 if len(idx) == 0 else 1 + int(np.sum(np.diff(idx) > gap))

def stats(V, fi):
    A = reg(V, fi); veto = np.all([A[s] < 2.0 for s in OFF], axis=0)
    l1 = (A["0013"] >= 3) & (A["0017"] >= 3) & (A["0015"] < 2) & veto
    p = np.where(l1)[0]; h = np.where((A["0015"] >= 3) & veto)[0]
    keep = []
    for f in p:
        lo = np.searchsorted(h, f - 2000); hi = np.searchsorted(h, f + 2001); w = h[lo:hi]
        if np.any(np.abs(w - f) >= 5): keep.append(f)
    return clusters(p), clusters(np.array(keep, dtype=np.int64)), [int(x) for x in p[:50]]

def j1_gate():
    A = reg("V0", 0); ok = np.ones(N + 4000, bool)
    for s in SC: ok &= (A[s] >= 2.5) if s in ("0013", "0015", "0017") else (A[s] < 2.0)
    return clusters(np.where(ok)[0])

def rank(true, null):
    null = np.asarray(null, float)
    return {"true": float(true), "null_mean": float(null.mean()), "null_sd": float(null.std()), "null_max": float(null.max()),
            "null_p99": float(np.percentile(null, 99)), "p": float((1 + np.sum(null >= true)) / (len(null) + 1)),
            "exceeds_p99": bool(true > np.percentile(null, 99)), "near40_p": float((1 + np.sum(null[near] >= true)) / 41)}

R = {"plan": open(os.path.join(HERE, "PLAN-L.sha256")).read().split()}
g = j1_gate(); R["gate"] = {"j1_m1_V0_frame0": g, "expected": 11, "passed": g == 11}
if not R["gate"]["passed"]:
    print(json.dumps(R, indent=1)); sys.exit()
for V in ("V0", "V2"):
    rows = [stats(V, fi) for fi in range(NF)]
    R[V] = {"L1": rank(rows[0][0], [r[0] for r in rows[1:]]), "L2": rank(rows[0][1], [r[1] for r in rows[1:]]),
            "comet_frame_L1_positions_registered": rows[0][2]}
    for k in ("L1", "L2"): R[V][k]["counts"] = R[V][k]["exceeds_p99"]
print(json.dumps(R, indent=1))
