"""PLAN-C08 step 2: uncapped z at the comet and fixed predictions.  python3 c08z.py > z.json"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(M, "../../../voltages/delaymod")); import dm
SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; P0 = 787546; HW = 5
D = {s: np.load(os.path.join(M, "out2", f"cc08_{s}.npz")) for s in SC}
fc = float(D["0013"]["fc"]); v00 = float(D["0013"]["f0_v0"])
def win(d, fi, c):
    idx = d[f"f{fi}_idx"].astype(np.int64); z = d[f"f{fi}_z"].astype(np.float32)
    m = (idx >= c - HW) & (idx <= c + HW)
    return {int(i - c): round(float(v), 3) for i, v in zip(idx[m], z[m])}
out = {"plan": open(os.path.join(HERE, "PLAN-C08.sha256")).read().split(), "p0": P0, "scans": {}}
for s in SC:
    d = D[s]; cb = P0 + int(np.rint(fc * (float(d["f0_v0"]) - v00) / dm.C / dm.DF)); e = {"role": dm.SCANS[s][2]}
    for name, c in (("comet", cb), ("fixed", P0)):
        w = win(d, 0, c); mx = max(w.values()) if w else None
        ref = [max(win(d, fi, c).values() or [0]) for fi in range(1, len(d["offs"]))]
        e[name] = {"bin": c, "mhz": (fc - (c - dm.N // 2) * dm.DF) / 1e6, "z_by_offset": w, "max_z": mx,
                   "false_frames_reaching": None if mx is None else int(sum(r >= mx for r in ref)), "false_frames": len(ref)}
    out["scans"][s] = e
print(json.dumps(out, indent=1))
