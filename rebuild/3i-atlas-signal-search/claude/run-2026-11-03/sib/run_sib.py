"""Below-threshold siblings (sib/PLAN-sib.md, sha256 86bc3bb30f2a088c6e156f480c7e95d88d10116e5eb64c7f45366a65625f8338).
    python3 run_sib.py   (inputs raw/cc07_00NN.npy|.json from fetch_cc.py; writes sib.json)
Tracked-sum arithmetic of comb/run_comb.py B0 (unmasked), copied; only the ON condition changes to bands of min ON z."""
import sys, os, json, importlib.util, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = "86bc3bb30f2a088c6e156f480c7e95d88d10116e5eb64c7f45366a65625f8338"
sys.argv = ["x", "raw/cc07", "2.5", "2.0"]
spec = importlib.util.spec_from_file_location("cf", "cf.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
ON, OFF, C, foff, H = cf.ON, cf.OFF, cf.C, cf.foff_hz, cf.H
NC = 1048576; DC = slice(NC // 2 - 4, NC // 2 + 5)
Y = {}
for s in ON + OFF:
    x = np.load(f"raw/cc07_{s}.npy", mmap_mode="r"); med = np.median(x, axis=0)
    y = np.asarray(x, np.float64) / med - 1.0
    Y[s] = y + np.roll(y, 1, axis=1) + np.roll(y, -1, axis=1)
def tracked(s, dv):
    h = H[s]; y = Y[s]; nt = y.shape[0]
    t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0
    v = cf.deldot(t) + dv * (t - cf.T0) * 86400.0
    fz = h["fch1_cc"] * 1e6
    shift = np.rint(fz * (v[0] - v) / C / foff).astype(int)
    acc = np.zeros(NC)
    for k in range(nt): acc += np.roll(y[k], -shift[k])
    m = np.median(acc); z = (acc - m) / (1.4826 * np.median(np.abs(acc - m))); z[DC] = 0.0
    return z, (fz + foff * np.arange(NC)) / (1.0 - v[0] / C)
def align(dv):
    zs = {s: tracked(s, dv) for s in ON + OFF}; ref = zs[ON[0]][1]; A = {}
    for s in ON + OFF:
        ix = np.rint((zs[s][1] - ref[0]) / foff).astype(int); z = zs[s][0]
        a = np.full(NC + 2000, -99.0); ok = (ix + 1000 >= 0) & (ix + 1000 < len(a)); a[ix[ok] + 1000] = z[ok]
        A[s] = np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
    return A, ref
tol = int(10 / abs(foff)) + 1
cl = lambda i: 0 if not len(i) else 1 + int(np.sum(np.diff(np.sort(i)) > tol))
def count(A, T, R, lo, hi=np.inf):
    mn = np.minimum.reduce([A[s] for s in T]); ok = (mn >= lo) & (mn < hi)
    for s in R: ok &= A[s] < 2.0
    return np.where(ok)[0]
BANDS = {"S1": (2.0, 2.5), "S2": (2.25, 2.5), "ge2.0": (2.0, np.inf), "ge2.25": (2.25, np.inf), "ge2.5": (2.5, np.inf), "ge2.75": (2.75, np.inf), "ge3.0": (3.0, np.inf)}
r11 = np.random.default_rng(11); offs = [0.0] + list(r11.uniform(0.03, 1.0, 40) * r11.choice([-1, 1], 40) * C / 1.42e9)
rows = []
for k, dv in enumerate(offs):
    A, ref = align(dv); r = {}
    for b, (lo, hi) in BANDS.items():
        p = count(A, ON, OFF, lo, hi); r[b] = cl(p)
        if k == 0:
            r[b + "_swap"] = cl(count(A, OFF, ON, lo, hi))
            if b == "S1": r["S1_freqs_MHz"] = sorted({round((ref[0] + (i - 1000) * foff) / 1e6, 6) for i in p})
    rows.append(r); print(k, {b: r[b] for b in BANDS}, flush=True)
t, N = rows[0], rows[1:]
out = {"plan_sha256": PLAN, "true": t, "null": {}}
for b in BANDS:
    v = np.array([r[b] for r in N])
    out["null"][b] = {"mean": round(float(v.mean()), 3), "sd": round(float(v.std()), 3), "min": int(v.min()), "max": int(v.max()), "frac_ge_true": round(float(np.mean(v >= t[b])), 3), "values": v.tolist()}
s1 = out["null"]["S1"]
out["verdict_S1"] = "SIBLINGS" if t["S1"] > s1["max"] else ("BELOW" if t["S1"] < s1["min"] else "NONE")
json.dump(out, open("sib.json", "w"), indent=1)
print("VERDICT", out["verdict_S1"], {b: (t[b], out["null"][b]["mean"], out["null"][b]["sd"], out["null"][b]["max"]) for b in BANDS}, flush=True)
