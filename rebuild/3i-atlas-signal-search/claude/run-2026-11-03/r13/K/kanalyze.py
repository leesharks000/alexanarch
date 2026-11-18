"""PLAN-K statistics over out/<scan>.npz.  python3 kanalyze.py > K.json.  Gate first: the 0013 V0 comet-frame stack must equal J's m1_V0_f0 list."""
import os, sys, json
import numpy as np
from scipy.ndimage import maximum_filter1d
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
sys.path.insert(0, HERE); from kcore import DSET
N = dm.N; SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
PAIR = {"0013": "0014", "0015": "0016", "0017": "0018"}
OUT = os.environ.get("K_OUT", os.path.join(HERE, "out"))   # env only for the synthetic smoke test
D = {s: np.load(os.path.join(OUT, f"{s}.npz")) for s in SC}
offs = D["0013"]["offs"]; NF = len(offs); FR = [f"f{i}" for i in range(NF)]
near = np.argsort(np.abs(offs[1:]))[:40]
R = {"plan": open(os.path.join(HERE, "PLAN-K.sha256")).read().split() if os.path.exists(os.path.join(HERE, "PLAN-K.sha256")) else None}
J = np.load(os.path.join(HERE, "../J/out/0013.npz"))["m1_V0_f0_idx"]
g = D["0013"]["gate_idx"]; R["gate"] = {"k_len": int(len(g)), "j_len": int(len(J)), "passed": bool(len(g) == len(J) and np.array_equal(g, J))}
if not R["gate"]["passed"] and not os.environ.get("K_SMOKE"):
    print(json.dumps(R, indent=1)); sys.exit()

def clusters(idx, gap=4): return 0 if len(idx) == 0 else 1 + int(np.sum(np.diff(idx) > gap))

def reg(V, fr, d):
    v0r = float(D["0013"][f"{V}_{fr}_v0"]); A = {}
    for s in SC:
        x = D[s]; idx = x[f"{V}_{fr}_d{d}_idx"].astype(np.int64); z = x[f"{V}_{fr}_d{d}_z"].astype(np.float32)
        sh = int(np.rint(dm.FC * (float(x[f"{V}_{fr}_v0"]) - v0r) / dm.C / dm.DF))
        a = np.full(N + 4000, -99.0, np.float32); j = idx - sh + 2000; ok = (j >= 0) & (j < len(a))
        np.maximum.at(a, j[ok], z[ok]); A[s] = maximum_filter1d(a, 3, mode="nearest")
    return A

def k1(V, fr):
    tot = 0; per = {s: 0 for s in ON}
    for d in DSET:
        A = reg(V, fr, d); ok = np.ones(N + 4000, bool)
        for s in SC: ok &= (A[s] >= 3.0) if s in ON else (A[s] < 2.0)
        tot += clusters(np.where(ok)[0])
        for s in ON: per[s] += clusters(np.where((A[s] >= 3.0) & (A[PAIR[s]] < 2.0))[0])
    return tot, per

def k2(s, V, fr): return max(float(D[s][f"{V}_{fr}_d{d}_k2_h2"].astype(np.float32).mean()) for d in DSET)
def k3(s, V, fr): return max(float(D[s][f"{V}_{fr}_d{d}_k3_s"].max()) for d in DSET)

def rank(true, null, stat):
    null = np.asarray(null, float)
    return {"true": float(true), "stationary": float(stat), "null_mean": float(null.mean()), "null_sd": float(null.std()),
            "null_max": float(null.max()), "null_p99": float(np.percentile(null, 99)),
            "p": float((1 + np.sum(null >= true)) / (len(null) + 1)), "exceeds_p99": bool(true > np.percentile(null, 99)),
            "exceeds_stationary": bool(true > stat), "near40_p": float((1 + np.sum(null[near] >= true)) / 41)}

for V in ("V0", "V2"):
    R[V] = {}
    allf = FR + ["S"]
    r1 = {fr: k1(V, fr) for fr in allf}
    e = {"combined": rank(r1["f0"][0], [r1[f][0] for f in FR[1:]], r1["S"][0])}
    for s in ON: e[f"single_{s}"] = rank(r1["f0"][1][s], [r1[f][1][s] for f in FR[1:]], r1["S"][1][s])
    e["counts"] = all(e[k]["exceeds_p99"] and e[k]["exceeds_stationary"] for k in e)
    R[V]["K1"] = e
    for name, fn in (("K2", k2), ("K3", k3)):
        vals = {s: {fr: fn(s, V, fr) for fr in allf} for s in SC}
        comb = {fr: min(vals[s][fr] for s in ON) for fr in allf}
        e = {"combined": rank(comb["f0"], [comb[f] for f in FR[1:]], comb["S"])}
        for s in SC: e[f"single_{s}"] = rank(vals[s]["f0"], [vals[s][f] for f in FR[1:]], vals[s]["S"])
        e["counts"] = (e["combined"]["exceeds_p99"] and e["combined"]["exceeds_stationary"]
                       and all(e[f"single_{s}"]["exceeds_p99"] and e[f"single_{s}"]["exceeds_stationary"]
                               and vals[s]["f0"] > vals[PAIR[s]]["f0"] for s in ON))
        if name == "K3":
            best = []
            for s in ON:
                d = max(DSET, key=lambda d: float(D[s][f"{V}_f0_d{d}_k3_s"].max())); i = int(np.argmax(D[s][f"{V}_f0_d{d}_k3_s"]))
                best.append({"scan": s, "d": d, "f": int(D[s][f"{V}_f0_d{d}_k3_f"][i]), "score": float(D[s][f"{V}_f0_d{d}_k3_s"][i]),
                             "period": int(D[s][f"{V}_f0_d{d}_k3_p"][i]), "phase": int(D[s][f"{V}_f0_d{d}_k3_ph"][i])})
            e["comet_frame_best"] = best
        R[V][name] = e
print(json.dumps(R, indent=1))
