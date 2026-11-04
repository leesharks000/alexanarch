"""Background models (bg/PLAN-bg.md, sha256 b8fd193abad6f20c3a6c8e552da6eecfa4d063ba34859c3f54987b615d186b0a).
    python3 run_bg.py   (inputs raw/cc07_00NN.npy|.json from fetch_cc.py; writes bg.json after each null)
Tracked-sum arithmetic of comb/run_comb.py B0, copied; the true comet frame throughout."""
import sys, os, json, itertools, importlib.util, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = "b8fd193abad6f20c3a6c8e552da6eecfa4d063ba34859c3f54987b615d186b0a"
sys.argv = ["x", "raw/cc07", "2.5", "2.0"]
spec = importlib.util.spec_from_file_location("cf", "cf.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
ON, OFF, C, foff, H = cf.ON, cf.OFF, cf.C, cf.foff_hz, cf.H
S6 = ON + OFF
NC = 1048576; DC = slice(NC // 2 - 4, NC // 2 + 5)
box = lambda y: y + np.roll(y, 1, axis=-1) + np.roll(y, -1, axis=-1)
Y, MAG, END = {}, {}, {}
for s in S6:
    x = np.load(f"raw/cc07_{s}.npy", mmap_mode="r"); med = np.median(x, axis=0)
    y = np.asarray(x, np.float64) / med - 1.0
    F = np.fft.rfft(y, axis=1); MAG[s] = np.abs(F).astype(np.float32); END[s] = (F[:, 0].copy(), F[:, -1].copy()); del F
    Y[s] = box(y); del y
def shifts(s):
    h = H[s]; nt = Y[s].shape[0]
    t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0
    v = cf.deldot(t); fz = h["fch1_cc"] * 1e6
    return np.rint(fz * (v[0] - v) / C / foff).astype(int), (fz + foff * np.arange(NC)) / (1.0 - v[0] / C)
SH = {s: shifts(s) for s in S6}
def zfrom(acc):
    m = np.median(acc); z = (acc - m) / (1.4826 * np.median(np.abs(acc - m))); z[DC] = 0.0; return z
def tracked(s, rowfn):
    sh, fr = SH[s]; acc = np.zeros(NC)
    for k in range(len(sh)): acc += np.roll(rowfn(s, k), -sh[k])
    return zfrom(acc), fr
def align(rowfn):
    zs = {s: tracked(s, rowfn) for s in S6}; ref = zs[ON[0]][1]; A = {}
    for s in S6:
        ix = np.rint((zs[s][1] - ref[0]) / foff).astype(int); z = zs[s][0]
        a = np.full(NC + 2000, -99.0); ok = (ix + 1000 >= 0) & (ix + 1000 < len(a)); a[ix[ok] + 1000] = z[ok]
        A[s] = np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
    return A
tol = int(10 / abs(foff)) + 1
cl = lambda i: 0 if not len(i) else 1 + int(np.sum(np.diff(np.sort(i)) > tol))
def count(A, T, R):
    ok = np.ones_like(A[S6[0]], bool)
    for s in T: ok &= A[s] >= 2.5
    for s in R: ok &= A[s] < 2.0
    return cl(np.where(ok)[0])
out = {"plan_sha256": PLAN}
def save(): json.dump(out, open("bg.json.tmp", "w"), indent=1); os.replace("bg.json.tmp", "bg.json")
def summ(v, true=13):
    v = np.array(v); return {"mean": round(float(v.mean()), 3), "sd": round(float(v.std()), 3), "max": int(v.max()), "frac_ge_true": round(float(np.mean(v >= true)), 3),
                             "verdict": "EXCEEDS" if true > v.max() else "WITHIN", "values": v.tolist()}
# N2 role partitions (true frame, unmodified rows)
A0 = align(lambda s, k: Y[s][k])
parts = []
for T in itertools.combinations(S6, 3):
    R = [s for s in S6 if s not in T]; parts.append({"on": list(T), "count": count(A0, list(T), R)})
true_n = [p["count"] for p in parts if p["on"] == ON][0]
others = [p["count"] for p in parts if p["on"] != ON]
out["true_count"] = true_n
out["N2"] = {"partitions": parts, "rank_of_true_desc": int(1 + sum(c > true_n for c in others)), "ties": int(sum(c == true_n for c in others)), **summ(others, true_n)}
print("N2", true_n, out["N2"]["rank_of_true_desc"], sorted(others, reverse=True), flush=True); save()
# N1 time-shuffled rows
rng = np.random.default_rng(101); v1 = []
for d in range(40):
    P = {s: rng.permutation(Y[s].shape[0]) for s in S6}
    A = align(lambda s, k, P=P: Y[s][P[s][k]]); c = count(A, ON, OFF); v1.append(c); print("N1", d, c, flush=True)
out["N1"] = summ(v1, true_n); save()
# N3 phase-randomized rows
rng = np.random.default_rng(103); v3 = []
NF = NC // 2 + 1
for d in range(40):
    def row(s, k):
        ph = rng.uniform(0, 2 * np.pi, NF); Z = MAG[s][k].astype(np.float64) * np.exp(1j * ph)
        Z[0] = END[s][0][k]; Z[-1] = END[s][1][k]
        return box(np.fft.irfft(Z, n=NC))
    A = align(row); c = count(A, ON, OFF); v3.append(c); print("N3", d, c, flush=True)
out["N3"] = summ(v3, true_n); save()
print("SUMMARY", {k: (out[k]["mean"], out[k]["sd"], out[k]["max"], out[k]["verdict"]) for k in ("N1", "N2", "N3")}, flush=True)
