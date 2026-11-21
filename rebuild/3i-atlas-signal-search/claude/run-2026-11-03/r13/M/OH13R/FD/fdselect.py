"""PLAN-OH13R-FD step 1: the original detector, unchanged, at oh_cluster.py's 40 false-drift offsets (and dv = 0 as a check).
Public products fetched with oh13/code/fetch_cc.py into a scratch directory.  python3 fdselect.py SCRATCHDIR"""
import json, os, subprocess, sys, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CODE = os.path.join(HERE, "../../../../../oh13/code")
CAT = json.load(open(os.path.join(CODE, "../oh13_candidates.json")))["candidates"]
SCR = sys.argv[1]; os.makedirs(os.path.join(SCR, "raw"), exist_ok=True)
files = {s["scan"]: s["file"] for s in CAT[0]["scans"]}
for scan, fn in files.items():
    stem = os.path.join(SCR, "raw", f"OH_{scan}")
    if not os.path.exists(stem + ".npy"):
        subprocess.run([sys.executable, os.path.join(CODE, "fetch_cc.py"), fn, "1666.99", stem], check=True)
os.chdir(SCR)
sys.argv = ["x", "raw/OH", "2.5", "2.0"]
spec = importlib.util.spec_from_file_location("cf", os.path.join(CODE, "cometframe_raw.py")); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)


def merge(rows, tol_hz=10.0):
    cl = []
    for r in sorted(rows, key=lambda r: r["f_rest_MHz"]):
        if cl and (r["f_rest_MHz"] - cl[-1][-1]["f_rest_MHz"]) * 1e6 <= tol_hz: cl[-1].append(r)
        else: cl.append([r])
    return [{"f_rest_Hz": float(np.mean([r["f_rest_MHz"] for r in c])) * 1e6, "rows": len(c),
             "z_on": [max(r[f"z_{s}"] for r in c) for s in cf.ON], "z_off": [max(r[f"z_{s}"] for r in c) for s in cf.OFF]} for c in cl]


true = merge(cf.coincidences(0.0, keep=True))
rng = np.random.default_rng(11); offs = rng.uniform(0.03, 1.0, 40) * rng.choice([-1, 1], 40) * cf.C / 1.42e9   # oh_cluster.py, unchanged
frames = [{"k": k, "dv": float(dv), "selections": merge(cf.coincidences(dv, keep=True))} for k, dv in enumerate(offs)]
out = {"T0_mjd": float(cf.T0), "true_frame": true, "false_frames": frames,
       "counts": {"true": len(true), "false": [len(f["selections"]) for f in frames]},
       "check_true_matches_catalogue": sorted(round(c["f_rest_Hz"]) for c in true) == sorted(round(c["f_rest_Hz"]) for c in CAT)}
json.dump(out, open(os.path.join(HERE, "fd_selections.json"), "w"), indent=1)
print("true-frame clusters:", len(true), "matches catalogue:", out["check_true_matches_catalogue"])
print("false-frame clusters: total", sum(out["counts"]["false"]), "mean", np.mean(out["counts"]["false"]), "max", max(out["counts"]["false"]))
