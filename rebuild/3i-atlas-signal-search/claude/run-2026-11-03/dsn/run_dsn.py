"""Deep-space downlink band, comet frame (dsn/PLAN-dsn.md, sha256 9f2d646d...). python3 run_dsn.py -> dsn.json (resumable per channel).
lheld/run_lheld.py's procedure, unchanged; channels and cadence per the plan."""
import sys, os, re, json, hashlib, subprocess, importlib.util, urllib.request, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = hashlib.sha256(open("PLAN-dsn.md", "rb").read()).hexdigest(); assert PLAN.startswith("9f2d646d"), PLAN
U = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; idx = urllib.request.urlopen(U, timeout=60).read().decode()
SC = ("0061", "0062", "0063", "0064", "0065", "0066")
FILES = {}
for nd in ("blc72", "blc73"):
    for f in sorted(set(re.findall(r'(' + nd + r'_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_006[1-6]\.rawspec\.0000\.h5)', idx))): FILES[(nd, f[-20:-16])] = f
BAND = {"blc72": (8626.46484375, -2.7939677238464355e-06), "blc73": (8438.96484375, -2.7939677238464355e-06)}
NF = 1048576; OUT = "dsn.json"
st = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": PLAN, "channels": {}}
os.makedirs("raw", exist_ok=True)
jobs = [("blc73", c) for c in range(0, 14)] + [("blc72", c) for c in range(60, 64)]
for nd, c in jobs:
    key = f"{nd}_cc{c:02d}"
    if key in st["channels"]: continue
    f1, fo = BAND[nd]; fmid = f1 + fo * (c * NF + NF // 2); stem = f"raw/{key}"
    for sc in SC:
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
    rows = []; listing = []
    for k, dv in enumerate(offs):
        A, ref = align(dv); p = hits(A, ON, OFF); q = hits(A, OFF, ON); r = {"on": cl(p), "swap": cl(q)}
        if k == 0:
            v0 = cf.deldot(cf.H[ON[0]]["tstart"] + 0.5 * cf.H[ON[0]]["tsamp"] / 86400.0)
            for i in sorted(set(p)):
                fr = ref[0] + (i - 1000) * foff
                listing.append({"f_rest_MHz": round(fr / 1e6, 6), "f_topo_first_ON_MHz": round(fr * (1 - v0 / C) / 1e6, 6), "z": {s: round(float(A[s][i]), 2) for s in ON + OFF}})
        rows.append(r)
    t, N = rows[0], rows[1:]; on = np.array([r["on"] for r in N]); d = np.array([r["on"] - r["swap"] for r in N])
    verdict = "EXCEEDS" if (t["on"] > on.max() and t["on"] - t["swap"] > d.max()) else ("BOUNDS" if on.min() <= t["on"] <= on.max() else "BETWEEN")
    st["channels"][key] = {"f_mid_MHz": round(fmid, 4), "true_on": t["on"], "true_swap": t["swap"], "false_on_mean": round(float(on.mean()), 2), "false_on_sd": round(float(on.std()), 2),
                           "false_on_max": int(on.max()), "false_d_max": int(d.max()), "frac_false_ge_true": round(float(np.mean(on >= t["on"])), 3), "verdict": verdict,
                           "true_on_channels": listing[:400], "rows": rows}
    json.dump(st, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(key, round(fmid, 3), "true", t["on"], "swap", t["swap"], "false %.2f+-%.2f max %d dmax %d" % (on.mean(), on.std(), on.max(), d.max()), verdict, flush=True)
    for sc in SC: os.remove(f"{stem}_{sc}.npy")
R = st["channels"]
if len(R) == len(jobs):
    n = sum(v["verdict"] == "EXCEEDS" for v in R.values())
    st["summary"] = {"channels": len(R), "exceeds": n, "overall": "LEAD" if n >= 3 else ("held out for replication" if n >= 1 else "BOUNDED")}
    json.dump(st, open(OUT, "w"), indent=0); print("SUMMARY", st["summary"], flush=True)
