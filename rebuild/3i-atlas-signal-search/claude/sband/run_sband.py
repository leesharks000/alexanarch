"""Frozen S-band property test (sband/PLAN.md, sha256 ca251bf3...). Same procedure as swapnull.py on blc23 coarse channel 30 (contains 2500 MHz),
scans 0029-0034. python3 sband/run_sband.py"""
import sys, json, importlib.util, numpy as np
sys.argv = ["x", "sband/S", "2.5", "2.0"]
spec = importlib.util.spec_from_file_location("cf", "sband/cf_s.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
ON, OFF, C, foff = cf.ON, cf.OFF, cf.C, cf.foff_hz
def align(dv):
    zs = {s: cf.tracked(s, dv) for s in ON + OFF}; ref = zs[ON[0]][1]; A = {}
    for s in ON + OFF:
        idx = np.rint((zs[s][1] - ref[0]) / foff).astype(int); z = zs[s][0]
        a = np.full(len(z) + 2000, -99.0); ok = (idx + 1000 >= 0) & (idx + 1000 < len(a)); a[idx[ok] + 1000] = z[ok]
        A[s] = np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
    return A, ref
def hits(A, T, R):
    ok = np.ones_like(A[ON[0]], bool)
    for s in T: ok &= A[s] >= 2.5
    for s in R: ok &= A[s] < 2.0
    return np.where(ok)[0]
tol = int(10 / abs(foff)) + 1
cl = lambda i: 0 if not len(i) else 1 + int(np.sum(np.diff(np.sort(i)) > tol))
rng = np.random.default_rng(11)
offs = [0.0] + list(rng.uniform(0.03, 1.0, 40) * rng.choice([-1, 1], 40) * C / 1.42e9)
rows = []
for k, dv in enumerate(offs):
    A, ref = align(dv); p = hits(A, ON, OFF); q = hits(A, OFF, ON)
    r = {"dv": float(dv), "on": cl(p), "swap": cl(q)}
    if k == 0: r["on_freqs_MHz"] = sorted({round((ref[0] + (i - 1000) * foff) / 1e6, 6) for i in p})
    rows.append(r); print(k, {a: b for a, b in r.items() if a != "on_freqs_MHz"}, flush=True)
json.dump(rows, open("sband/S_swapnull.json", "w"), indent=1)
t, N = rows[0], rows[1:]
on = np.array([r["on"] for r in N]); d = np.array([r["on"] - r["swap"] for r in N])
print("TRUE on", t["on"], "swap", t["swap"], "| false on mean %.2f sd %.2f max %d | on-swap mean %.2f max %d | frac on>=true %.3f frac d>=true %.3f" %
      (on.mean(), on.std(), on.max(), d.mean(), d.max(), np.mean(on >= t["on"]), np.mean(d >= t["on"] - t["swap"])))
