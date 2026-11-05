"""Comet frame under satellite clutter (sat/PLAN-sat.md, sha256 5c817090...). python3 run_sat.py -> sat.json (resumable per channel).
lheld/run_lheld.py's procedure, unchanged, computed twice per frame: untrimmed, and with the 5 largest shifted rows dropped at every channel."""
import sys, os, re, json, hashlib, subprocess, importlib.util, urllib.request, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = hashlib.sha256(open("PLAN-sat.md", "rb").read()).hexdigest(); assert PLAN.startswith("5c817090"), PLAN
U = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; idx = urllib.request.urlopen(U, timeout=60).read().decode()
FILES = {f[-20:-16]: f for f in sorted(set(re.findall(r'(blc23_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_001[3-8]\.rawspec\.0000\.h5)', idx)))}
F1, FO = 1688.96484375, -2.7939677238464355e-06; NF = 1048576; OUT = "sat.json"; TRIM = 5
IRI0, IRIS = 1616.0208333e6, 41666.667
st = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": PLAN, "channels": {}}
os.makedirs("raw", exist_ok=True)
for c in range(20, 27):
    key = f"blc23_cc{c:02d}"
    if key in st["channels"]: continue
    fmid = F1 + FO * (c * NF + NF // 2); stem = f"raw/{key}"
    for sc in ("0013", "0014", "0015", "0016", "0017", "0018"):
        if not os.path.exists(f"{stem}_{sc}.npy"): subprocess.run([sys.executable, "fetch_cc.py", FILES[sc], str(fmid), f"{stem}_{sc}"], check=True)
    sys.argv = ["x", stem, "2.5", "2.0"]
    spec = importlib.util.spec_from_file_location("cf_" + key, "cf.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
    ON, OFF, C, foff = cf.ON, cf.OFF, cf.C, cf.foff_hz
    X = {s: np.load(f"{stem}_{s}.npy", mmap_mode="r") for s in ON + OFF}
    MED = {s: np.median(X[s], axis=0) for s in ON + OFF}
    def tracked2(s, dv):
        x = X[s]; h = cf.H[s]; nt, nc = x.shape
        t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0
        v = cf.deldot(t) + dv * (t - cf.T0) * 86400.0
        f0 = h["fch1_cc"] * 1e6
        shift = np.rint(f0 * (v[0] - v) / C / foff).astype(int)
        S = np.empty((nt, nc), np.float32)
        for k in range(nt):
            row = np.asarray(x[k], np.float64) / MED[s] - 1.0
            row = row + np.roll(row, 1) + np.roll(row, -1)
            S[k] = np.roll(row, -shift[k])
        acc = S.sum(0, dtype=np.float64)
        top = np.partition(S, nt - TRIM, axis=0)[nt - TRIM:].sum(0, dtype=np.float64)
        out = []
        for a in (acc, acc - top):
            m = np.median(a); sd = 1.4826 * np.median(np.abs(a - m)); z = (a - m) / sd; z[nc // 2 - 4: nc // 2 + 5] = 0.0; out.append(z)
        frest = (f0 + foff * np.arange(nc)) / (1.0 - v[0] / C)
        return out, frest, v[0]
    def align(dv):
        Z = {s: tracked2(s, dv) for s in ON + OFF}; ref = Z[ON[0]][1]; A = ({}, {})
        for s in ON + OFF:
            ix = np.rint((Z[s][1] - ref[0]) / foff).astype(int)
            for m in (0, 1):
                z = Z[s][0][m]; a = np.full(len(z) + 2000, -99.0); ok = (ix + 1000 >= 0) & (ix + 1000 < len(a)); a[ix[ok] + 1000] = z[ok]
                A[m][s] = np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
        return A, ref, Z[ON[0]][2]
    def hits(A, T, R):
        ok = np.ones_like(A[ON[0]], bool)
        for s in T: ok &= A[s] >= 2.5
        for s in R: ok &= A[s] < 2.0
        return np.where(ok)[0]
    tol = int(10 / abs(foff)) + 1
    def clusters(i):
        i = np.sort(i)
        if not len(i): return []
        return np.split(i, np.where(np.diff(i) > tol)[0] + 1)
    rng = np.random.default_rng(11); offs = [0.0] + list(rng.uniform(0.03, 1.0, 40) * rng.choice([-1, 1], 40) * C / 1.42e9)
    rows = []; listing = []
    for k, dv in enumerate(offs):
        A, ref, v0 = align(dv); r = {}
        for m, name in ((0, "untrimmed"), (1, "trimmed")):
            p = hits(A[m], ON, OFF); q = hits(A[m], OFF, ON); r[name] = {"on": len(clusters(p)), "swap": len(clusters(q))}
            if k == 0 and name == "trimmed":
                for g in clusters(p):
                    j = int(g[np.argmax(sum(A[1][s][g] for s in ON))]); fr = ref[0] + (j - 1000) * foff; ft = fr * (1.0 - v0 / C)
                    off = (ft - IRI0) - IRIS * round((ft - IRI0) / IRIS)
                    listing.append({"f_rest_MHz": round(fr / 1e6, 6), "f_topo_0013_MHz": round(ft / 1e6, 6), "iridium_grid_offset_Hz": round(off, 1),
                                    "channels": int(len(g)), "z_trimmed": {s: round(float(A[1][s][j]), 2) for s in ON + OFF},
                                    "z_untrimmed": {s: round(float(A[0][s][j]), 2) for s in ON + OFF}})
        rows.append(r)
    res = {"f_mid_MHz": round(fmid, 4)}
    for name in ("untrimmed", "trimmed"):
        t = rows[0][name]; on = np.array([x[name]["on"] for x in rows[1:]]); d = np.array([x[name]["on"] - x[name]["swap"] for x in rows[1:]])
        res[name] = {"true_on": t["on"], "true_swap": t["swap"], "false_on_mean": round(float(on.mean()), 2), "false_on_sd": round(float(on.std()), 2),
                     "false_on_max": int(on.max()), "false_d_max": int(d.max()), "frac_false_ge_true": round(float(np.mean(on >= t["on"])), 3),
                     "verdict": "EXCEEDS" if (t["on"] > on.max() and t["on"] - t["swap"] > d.max()) else ("BOUNDS" if on.min() <= t["on"] <= on.max() else "BETWEEN")}
    res["trimmed_true_clusters"] = listing; res["rows"] = rows
    st["channels"][key] = res
    json.dump(st, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(key, round(fmid, 3), "| untrimmed", res["untrimmed"]["true_on"], "vs %.2f max %d" % (res["untrimmed"]["false_on_mean"], res["untrimmed"]["false_on_max"]), res["untrimmed"]["verdict"],
          "| trimmed", res["trimmed"]["true_on"], "swap", res["trimmed"]["true_swap"], "vs %.2f+-%.2f max %d dmax %d" % (res["trimmed"]["false_on_mean"], res["trimmed"]["false_on_sd"], res["trimmed"]["false_on_max"], res["trimmed"]["false_d_max"]),
          res["trimmed"]["verdict"], flush=True)
    del X
    for sc in ("0013", "0014", "0015", "0016", "0017", "0018"): os.remove(f"{stem}_{sc}.npy")
R = st["channels"]
if len(R) == 7:
    n = sum(v["trimmed"]["verdict"] == "EXCEEDS" for v in R.values())
    st["summary"] = {"channels": 7, "trimmed_exceeds": n, "overall": "LEAD" if n >= 2 else ("one channel to hold out" if n == 1 else "CLEARS")}
    json.dump(st, open(OUT, "w"), indent=0); print("SUMMARY", st["summary"], flush=True)
