"""PLAN-M stage 1.  python3 mnominate.py > M1.json"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); JO = os.path.join(HERE, "../J/out")
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
N = dm.N; SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; NF = 401; V = "V2"; ZC, MARG, DIST = 4.0, 1.0, 6.0
D = {s: np.load(os.path.join(JO, f"{s}.npz")) for s in SC}
offs = D["0013"]["offs"]; SPAN = 292.1
drift_bins = offs * SPAN * dm.FC / dm.C / dm.DF          # each frame's extra drift over the scan, in bins
pseudo = np.random.default_rng(29).choice(np.arange(1, NF), 40, replace=False)

def frame(s, fi):
    d = D[s]; return d[f"m1_{V}_f{fi}_idx"].astype(np.int64), d[f"m1_{V}_f{fi}_z"].astype(np.float32), float(d[f"m1_{V}_f{fi}_v0"])

def nominate(s, target):
    ti, tz, tv0 = frame(s, target)
    keep = (tz >= ZC) & (np.abs(ti - N // 2) > 8); P, Pz = ti[keep], tz[keep]
    if len(P) == 0: return []
    best = np.full(len(P), -np.inf)
    for fi in range(NF):
        if fi == target or abs(drift_bins[fi] - drift_bins[target]) < DIST: continue
        idx, z, v0 = frame(s, fi)
        sh = int(np.rint(dm.FC * (v0 - tv0) / dm.C / dm.DF)); j = idx - sh   # registered to the target frame
        o = np.argsort(j); j, z = j[o], z[o]
        lo = np.searchsorted(j, P - 2); hi = np.searchsorted(j, P + 3)
        for k in range(len(P)):
            if hi[k] > lo[k]: best[k] = max(best[k], float(z[lo[k]:hi[k]].max()))
    ok = Pz - np.maximum(best, 0.0) >= MARG
    leads = []; last = -99
    for p, zc, b in sorted(zip(P[ok], Pz[ok], best[ok])):
        if p - last > 4: leads.append({"bin": int(p), "hz_from_cc_centre": float((p - N // 2) * dm.DF), "z": float(zc), "best_distinct": (None if b == -np.inf else float(b))})
        last = p
    return leads

R = {"plan": open(os.path.join(HERE, "PLAN-M.sha256")).read().split(), "pseudo_targets": [int(x) for x in pseudo], "per_scan": {}}
for s in SC:
    comet = nominate(s, 0); ps = [len(nominate(s, int(t))) for t in pseudo]
    R["per_scan"][s] = {"role": dm.SCANS[s][2], "comet_leads": len(comet), "pseudo_mean": float(np.mean(ps)), "pseudo_max": int(max(ps)),
                        "pseudo_p": float((1 + sum(x >= len(comet) for x in ps)) / 41), "leads": comet}
    print(s, dm.SCANS[s][2], len(comet), "pseudo", np.mean(ps), max(ps), file=sys.stderr, flush=True)
print(json.dumps(R, indent=1))
