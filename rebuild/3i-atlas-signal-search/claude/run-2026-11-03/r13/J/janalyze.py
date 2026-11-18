"""PLAN-J statistics over out/<scan>.npz and out/<scan>-Q.npy.  python3 janalyze.py > J.json
Gate first: J1 m=1 V0 frame 0 must give delaymod's 11; if not, only the gate is written."""
import os, sys, json
import numpy as np
from scipy.ndimage import maximum_filter1d
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
N = dm.N; SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
PAIR = {"0013": "0014", "0015": "0016", "0017": "0018"}; NF = 401
D = {s: np.load(os.path.join(HERE, "out", f"{s}.npz")) for s in SC}
Qa = {s: np.load(os.path.join(HERE, "out", f"{s}-Q.npy")) for s in SC}
offs = D["0013"]["offs"]; near = np.argsort(np.abs(offs[1:]))[:40] + 1

def reg(m, V, fi):
    v0r = float(D["0013"][f"m{m}_{V}_f{fi}_v0"]); A = {}
    for s in SC:
        d = D[s]; idx = d[f"m{m}_{V}_f{fi}_idx"].astype(np.int64); z = d[f"m{m}_{V}_f{fi}_z"].astype(np.float32)
        sh = int(np.rint(m * dm.FC * (float(d[f"m{m}_{V}_f{fi}_v0"]) - v0r) / dm.C / dm.DF))
        a = np.full(N + 4000, -99.0, np.float32); j = idx - sh + 2000; ok = (j >= 0) & (j < len(a))
        np.maximum.at(a, j[ok], z[ok]); A[s] = maximum_filter1d(a, 3, mode="nearest")
    return A

def clusters(idx, gap=4):
    if len(idx) == 0: return 0
    return 1 + int(np.sum(np.diff(idx) > gap))

def j1(m, V, fi):
    A = reg(m, V, fi)
    ok = np.ones(N + 4000, bool)
    for s in SC: ok &= (A[s] >= 2.5) if s in ON else (A[s] < 2.0)
    per = {s: clusters(np.where((A[s] >= 2.5) & (A[PAIR[s]] < 2.0))[0]) for s in ON}
    return clusters(np.where(ok)[0]), per

def rank(true, null):
    null = np.asarray(null, float)
    return {"true": float(true), "null_mean": float(null.mean()), "null_sd": float(null.std()), "null_max": float(null.max()),
            "null_p99": float(np.percentile(null, 99)), "p": float((1 + np.sum(null >= true)) / (len(null) + 1)),
            "exceeds_p99": bool(true > np.percentile(null, 99)),
            "near40_p": float((1 + np.sum(null[near - 1] >= true)) / 41)}

def rz(a):
    m = np.median(a, axis=-1, keepdims=True); s = 1.4826 * np.median(np.abs(a - m), axis=-1, keepdims=True); s[s == 0] = np.inf
    return (a - m) / s

R = {"plan": open(os.path.join(HERE, "PLAN-J.sha256")).read().split()}
g, _ = j1(1, "V0", 0); R["gate"] = {"j1_m1_V0_frame0": g, "delaymod": 11, "passed": g == 11}
if not R["gate"]["passed"]:
    print(json.dumps(R, indent=1)); sys.exit()
for V in ("V0", "V2"):
    R[V] = {}
    for m in (1, 2, 4):
        tot, per = zip(*[j1(m, V, fi) for fi in range(NF)])
        e = {"combined": rank(tot[0], tot[1:])}
        for s in ON: e[f"single_{s}"] = rank(per[0][s], [p[s] for p in per[1:]])
        e["counts"] = e["combined"]["exceeds_p99"] and all(e[f"single_{s}"]["exceeds_p99"] for s in ON)
        R[V][f"J1_m{m}"] = e
    vi = 0 if V == "V0" else 1
    q = {s: rz(Qa[s][vi]) for s in SC}                     # (401, 1996)
    onmin = np.minimum.reduce([q[s] for s in ON]); offmax = np.maximum.reduce([q[s] for s in OFF])
    T2 = np.where(offmax < 2.0, onmin, -np.inf).max(axis=1)
    e = {"combined": rank(T2[0], T2[1:]), "lag_bins_true": int(np.argmax(np.where(offmax[0] < 2.0, onmin[0], -np.inf)) + 5)}
    for s in ON:
        ms = q[s].max(axis=1); e[f"single_{s}"] = rank(ms[0], ms[1:])
    e["counts"] = e["combined"]["exceeds_p99"] and all(e[f"single_{s}"]["exceeds_p99"] for s in ON)
    R[V]["J2"] = e
print(json.dumps(R, indent=1))
