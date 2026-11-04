"""Held-out L-band property test (lheld/PLAN-lheld.md, sha256 e059db4e...). python3 lheld/run_lheld.py -> lheld/lheld.json (resumable per channel)"""
import sys, os, re, json, subprocess, importlib.util, urllib.request, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
U = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; idx = urllib.request.urlopen(U, timeout=60).read().decode()
FILES = {}
for nd in ("blc23", "blc24"):
    for f in sorted(set(re.findall(r'(' + nd + r'_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_001[3-8]\.rawspec\.0000\.h5)', idx))): FILES[(nd, f[-20:-16])] = f
BAND = {"blc23": (1688.96484375, -2.7939677238464355e-06), "blc24": (1501.46484375, -2.7939677238464355e-06)}
NF = 1048576; OUT = "lheld.json"
st = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": "e059db4e0b74828bde525debadf5567dd1b82772c58663f861ef4fbe5b267a98", "channels": {}}
os.makedirs("raw", exist_ok=True)
jobs = [(nd, c) for nd in ("blc24", "blc23") for c in range(7, 64, 8) if not (nd == "blc23" and c == 7)]
for nd, c in jobs:
    key = f"{nd}_cc{c:02d}"
    if key in st["channels"]: continue
    f1, fo = BAND[nd]; fmid = f1 + fo * (c * NF + NF // 2); stem = f"raw/{key}"
    for sc in ("0013", "0014", "0015", "0016", "0017", "0018"):
        if not os.path.exists(f"{stem}_{sc}.npy"): subprocess.run([sys.executable, "fetch_cc.py", FILES[(nd, sc)], str(fmid), f"{stem}_{sc}"], check=True)
    sys.argv = ["x", stem, "2.5", "2.0"]
    spec = importlib.util.spec_from_file_location("cf_" + key, "cf.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
    ON, OFF, C, foff = cf.ON, cf.OFF, cf.C, cf.foff_hz
    def align(dv):
        zs = {s: cf.tracked(s, dv) for s in ON + OFF}; ref = zs[ON[0]][1]; A = {}
        for s in ON + OFF:
            ix = np.rint((zs[s][1] - ref[0]) / foff).astype(int); z = zs[s][0]
            a = np.full(len(z) + 2000, -99.0); ok = (ix + 1000 >= 0) & (ix + 1000 < len(a)); a[ix[ok] + 1000] = z[ok]
            A[s] = np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
        return A, ref
    def hits(A, T, R):
        ok = np.ones_like(A[ON[0]], bool)
        for s in T: ok &= A[s] >= 2.5
        for s in R: ok &= A[s] < 2.0
        return np.where(ok)[0]
    tol = int(10 / abs(foff)) + 1; cl = lambda i: 0 if not len(i) else 1 + int(np.sum(np.diff(np.sort(i)) > tol))
    rng = np.random.default_rng(11); offs = [0.0] + list(rng.uniform(0.03, 1.0, 40) * rng.choice([-1, 1], 40) * C / 1.42e9)
    rows = []
    for k, dv in enumerate(offs):
        A, ref = align(dv); p = hits(A, ON, OFF); q = hits(A, OFF, ON); r = {"on": cl(p), "swap": cl(q)}
        if k == 0: r["on_freqs_MHz"] = sorted({round((ref[0] + (i - 1000) * foff) / 1e6, 6) for i in p})
        rows.append(r)
    t, N = rows[0], rows[1:]; on = np.array([r["on"] for r in N]); d = np.array([r["on"] - r["swap"] for r in N])
    verdict = "REPLICATES" if (t["on"] > on.max() and t["on"] - t["swap"] > d.max()) else ("BOUNDS" if on.min() <= t["on"] <= on.max() else "BETWEEN")
    st["channels"][key] = {"f_mid_MHz": round(fmid, 4), "true_on": t["on"], "true_swap": t["swap"], "false_on_mean": round(float(on.mean()), 2), "false_on_sd": round(float(on.std()), 2),
                           "false_on_max": int(on.max()), "false_d_max": int(d.max()), "frac_false_ge_true": round(float(np.mean(on >= t["on"])), 3), "verdict": verdict,
                           "true_on_freqs_MHz": t.get("on_freqs_MHz", []), "rows": rows}
    json.dump(st, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(key, round(fmid, 3), "true", t["on"], "swap", t["swap"], "false %.2f+-%.2f max %d" % (on.mean(), on.std(), on.max()), verdict, flush=True)
    for sc in ("0013", "0014", "0015", "0016", "0017", "0018"): os.remove(f"{stem}_{sc}.npy")
R = st["channels"]
if len(R) == len(jobs):
    n = sum(v["verdict"] == "REPLICATES" for v in R.values())
    st["summary"] = {"channels": len(R), "replicate": n, "overall": "REPLICATES" if n >= 3 else ("consistent with chance" if n >= 1 else "BOUNDS")}
    json.dump(st, open(OUT, "w"), indent=0); print("SUMMARY", st["summary"], flush=True)
