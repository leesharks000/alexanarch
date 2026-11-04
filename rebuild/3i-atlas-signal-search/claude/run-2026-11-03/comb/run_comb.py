"""Cadence/comb test (comb/PLAN-comb.md, sha256 75a991d4cc60fdbd45aa7e9c718b6902f9c1cb5269fa01f1c2d4961aedd1e08e).
    python3 run_comb.py   (inputs raw/cc07_00NN.npy|.json from fetch_cc.py; writes comb.json)
The tracked sum is cf.tracked's arithmetic (x/median - 1, 3-channel boxcar, path roll, robust z, DC zeroed), with the
normalized rows computed once per scan and an optional mask of receiver-frame structure channels set to 0 before the boxcar."""
import sys, os, json, csv, importlib.util, numpy as np
from scipy.ndimage import median_filter
from scipy.stats import spearmanr
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = "75a991d4cc60fdbd45aa7e9c718b6902f9c1cb5269fa01f1c2d4961aedd1e08e"
sys.argv = ["x", "raw/cc07", "2.5", "2.0"]
spec = importlib.util.spec_from_file_location("cf", "cf.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
ON, OFF, C, foff, H = cf.ON, cf.OFF, cf.C, cf.foff_hz, cf.H
NC = 1048576; DC = slice(NC // 2 - 4, NC // 2 + 5)
rz = lambda a: (a - np.median(a)) / (1.4826 * np.median(np.abs(a - np.median(a))))
out = {"plan_sha256": PLAN}

# ---- Step A: structure from the OFF scans
S_k, V_k = [], []
for s in OFF:
    x = np.load(f"raw/cc07_{s}.npy").astype(np.float64)
    med = np.median(x, axis=0)
    base = median_filter(med, size=1025, mode="nearest")
    S_k.append(med / base - 1.0)
    y = x / med - 1.0; del x
    V_k.append(1.4826 * np.median(np.abs(y - np.median(y, axis=0)), axis=0)); del y
S = np.median(np.array(S_k), axis=0); V = np.mean(np.array(V_k), axis=0)
keep = np.ones(NC, bool); keep[DC] = False
def rzk(a):
    m = np.median(a[keep]); sc = 1.4826 * np.median(np.abs(a[keep] - m)); z = (a - m) / sc; z[DC] = 0.0; return z
zS, zV = rzk(S), rzk(V)
def mk(th):
    core = (zS >= th) | (zV >= th)
    return core, core | np.roll(core, 1) | np.roll(core, -1)
TH = 5.0; core, mask = mk(TH)
if mask.mean() > 0.25: TH = 8.0; core, mask = mk(TH)
f0 = H["0013"]["fch1_cc"] * 1e6
ftopo = lambda j: (f0 + foff * np.asarray(j)) / 1e6
out["A"] = {"threshold": TH, "mask_fraction": float(mask.mean()), "core_channels": int(core.sum()), "masked_channels": int(mask.sum()),
            "n_S_ge": int((zS >= TH).sum()), "n_V_ge": int((zV >= TH).sum())}
# radiosonde edge 1668.40-1668.46 (topocentric)
jr = np.where((ftopo(np.arange(NC)) >= 1668.40))[0]
out["A"]["radiosonde_edge"] = {"channels": int(len(jr)), "core_in_edge": int(core[jr].sum()), "fraction_core": float(core[jr].mean()),
                               "zS_max": float(zS[jr].max()), "zV_max": float(zV[jr].max())}
# local comb at C01/C02
jc = int(round((1665.61512e6 - f0) / foff)); w = int(500 / abs(foff))
loc = [(round(float(ftopo(j)), 6), round(float(zS[j]), 1), round(float(zV[j]), 1)) for j in range(jc - w, jc + w + 1) if zS[j] >= TH or zV[j] >= TH]
out["A"]["local_1665_61512"] = loc
# Fourier power of zS
P = np.abs(np.fft.rfft(zS)) ** 2; k = np.arange(len(P)); sp = np.where(k > 0, NC / np.maximum(k, 1) * abs(foff), np.inf)
rng_ = (sp >= 8) & (sp <= 3000); medP = float(np.median(P[rng_]))
idx = np.where(rng_)[0]; top = idx[np.argsort(P[idx])[::-1]]
peaks = []
for i in top:
    if any(abs(i - p) <= 2 for p, _, _ in peaks): continue
    peaks.append((int(i), float(sp[i]), float(P[i] / medP)))
    if len(peaks) == 10: break
out["A"]["fourier_peaks"] = [{"k": p, "spacing_Hz": round(s_, 4), "power_over_median": round(r, 2)} for p, s_, r in peaks]
print("A", json.dumps(out["A"])[:1500], flush=True)

# ---- Step B: masked and unmasked counts
def prep(m):
    Y = {}
    for s in ON + OFF:
        x = np.load(f"raw/cc07_{s}.npy", mmap_mode="r"); med = np.median(x, axis=0)
        y = np.asarray(x, np.float64) / med - 1.0
        if m is not None: y[:, m] = 0.0
        Y[s] = y + np.roll(y, 1, axis=1) + np.roll(y, -1, axis=1)
    return Y
def tracked(Y, s, dv):
    h = H[s]; y = Y[s]; nt = y.shape[0]
    t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0
    v = cf.deldot(t) + dv * (t - cf.T0) * 86400.0
    fz = h["fch1_cc"] * 1e6
    shift = np.rint(fz * (v[0] - v) / C / foff).astype(int)
    acc = np.zeros(NC)
    for k_ in range(nt): acc += np.roll(y[k_], -shift[k_])
    m_ = np.median(acc); z = (acc - m_) / (1.4826 * np.median(np.abs(acc - m_))); z[DC] = 0.0
    return z, (fz + foff * np.arange(NC)) / (1.0 - v[0] / C)
def align(Y, dv):
    zs = {s: tracked(Y, s, dv) for s in ON + OFF}; ref = zs[ON[0]][1]; A = {}
    for s in ON + OFF:
        ix = np.rint((zs[s][1] - ref[0]) / foff).astype(int); z = zs[s][0]
        a = np.full(NC + 2000, -99.0); ok = (ix + 1000 >= 0) & (ix + 1000 < len(a)); a[ix[ok] + 1000] = z[ok]
        A[s] = np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
    return A, ref
def hits(A, T, R):
    ok = np.ones_like(A[ON[0]], bool)
    for s in T: ok &= A[s] >= 2.5
    for s in R: ok &= A[s] < 2.0
    return np.where(ok)[0]
tol = int(10 / abs(foff)) + 1
cl = lambda i: 0 if not len(i) else 1 + int(np.sum(np.diff(np.sort(i)) > tol))
r11 = np.random.default_rng(11); offs = [0.0] + list(r11.uniform(0.03, 1.0, 40) * r11.choice([-1, 1], 40) * C / 1.42e9)
def run(m, frames):
    Y = prep(m); rows = []
    for kk, dv in enumerate(frames):
        A, ref = align(Y, dv); p = hits(A, ON, OFF); q = hits(A, OFF, ON); r = {"on": cl(p), "swap": cl(q)}
        if kk == 0: r["on_freqs_MHz"] = sorted({round((ref[0] + (i - 1000) * foff) / 1e6, 6) for i in p})
        rows.append(r)
    del Y; return rows
def summ(rows):
    t, N = rows[0], rows[1:]; on = np.array([r["on"] for r in N])
    return {"true_on": t["on"], "true_swap": t["swap"], "true_on_freqs_MHz": t.get("on_freqs_MHz", []), "null_mean": round(float(on.mean()), 3),
            "null_sd": round(float(on.std()), 3), "null_max": int(on.max()), "frac_null_ge_true": round(float(np.mean(on >= t["on"])), 3), "null": [r["on"] for r in N]}
out["B0"] = summ(run(None, offs)); print("B0", {k_: v for k_, v in out["B0"].items() if k_ != "null"}, flush=True)
out["B1"] = summ(run(mask, offs)); print("B1", {k_: v for k_, v in out["B1"].items() if k_ != "null"}, flush=True)
r23 = np.random.default_rng(23); sh = r23.integers(10000, NC - 10000 + 1, 10)
out["B2"] = []
for o in sh:
    r = run(np.roll(mask, int(o)), [0.0])[0]; out["B2"].append({"offset": int(o), "true_on": r["on"], "true_swap": r["swap"]}); print("B2", out["B2"][-1], flush=True)
json.dump(out, open("comb.json.tmp", "w"), indent=1); os.replace("comb.json.tmp", "comb.json")

# ---- Step C
rows = list(csv.DictReader(open("../../oh13/oh13_candidates.csv")))
F13 = sorted({float(r["f_rest_MHz"]) for r in rows})
def path(F_hz, s):
    h = H[s]; t = h["tstart"] + (np.arange(49) + 0.5) * h["tsamp"] / 86400.0
    return np.rint((F_hz * (1 - cf.deldot(t) / C) - f0) / foff).astype(int)
def O_W(F_hz, s):
    c = path(F_hz, s); win = np.clip(np.stack([c - 1, c, c + 1]), 0, NC - 1)
    return float(mask[win].any(axis=0).mean()), float(zV[win].max(axis=0).sum()), c
def dO(F_hz): return np.mean([O_W(F_hz, s)[0] for s in ON]) - np.mean([O_W(F_hz, s)[0] for s in OFF])
d13 = np.array([dO(F * 1e6) for F in F13])
rest_lo, rest_hi = sorted([ftopo(0) * 1e6 / (1 - cf.deldot(H["0013"]["tstart"]) / C), ftopo(NC - 1) * 1e6 / (1 - cf.deldot(H["0013"]["tstart"]) / C)])
rc = np.random.default_rng(31); ctrl = []
while len(ctrl) < 13000:
    F = rc.uniform(rest_lo + 2000, rest_hi - 2000)
    if min(abs(F - g * 1e6) for g in F13) <= 10: continue
    if any(np.any(np.abs(path(F, s) - NC // 2) <= 10) for s in ON + OFF): continue
    ctrl.append(F)
dc = np.array([dO(F) for F in ctrl])
sub = np.array([dc[rc.choice(len(dc), 13, replace=False)].mean() for _ in range(10000)])
out["P1"] = {"thirteen_dO": [round(float(x), 4) for x in d13], "thirteen_mean_dO": round(float(d13.mean()), 4),
             "control_dO_mean": round(float(dc.mean()), 4), "control_dO_sd": round(float(dc.std()), 4),
             "percentile_of_thirteen_mean_among_13_subsets": round(float(np.mean(sub < d13.mean()) * 100), 2),
             "control_frac_O_on_any": round(float(np.mean([O_W(F, ON[0])[0] > 0 for F in ctrl[:2000]])), 4)}
zt = np.array([float(r["z_tracked"]) for r in rows]); sc_ = np.array([r["scan"] for r in rows])
Wv = np.array([O_W(float(r["f_rest_MHz"]) * 1e6, r["scan"])[1] for r in rows]); Ov = np.array([O_W(float(r["f_rest_MHz"]) * 1e6, r["scan"])[0] for r in rows])
rho = spearmanr(zt, Wv).correlation; rp = np.random.default_rng(37); nul = []
for _ in range(10000):
    Wp = Wv.copy()
    for s in ON + OFF: ix = np.where(sc_ == s)[0]; Wp[ix] = Wp[rp.permutation(ix)]
    nul.append(spearmanr(zt, Wp).correlation)
out["P2"] = {"rho": round(float(rho), 4), "p_one_sided": round(float(np.mean(np.array(nul) >= rho)), 4),
             "rows": [{"id": r["id"], "scan": r["scan"], "z": float(r["z_tracked"]), "O": round(float(o), 3), "W": round(float(w_), 2)} for r, o, w_ in zip(rows, Ov, Wv)]}
# P3
p3 = []
for kk, spc, ratio in peaks:
    if ratio < 10: continue
    ph0 = np.angle(np.fft.rfft(zS)[kk])  # tooth where 2*pi*kk*j/NC + ph0 = 0 mod 2*pi
    ent = {"spacing_Hz": round(spc, 4), "power_over_median": round(ratio, 2), "candidates": {}}
    for F in F13:
        d = {}
        for s in ON + OFF:
            c = path(F * 1e6, s); jm = c[24]; ph = ((kk * jm / NC) + ph0 / (2 * np.pi)) % 1.0; d[s] = round(float(min(ph, 1 - ph)), 3)
        ent["candidates"][f"{F:.6f}"] = d
    p3.append(ent)
cidx = np.where(core)[0]
def mind(c): return int(np.min(np.abs(cidx[np.searchsorted(cidx, c).clip(0, len(cidx) - 1)] - c)))
c03 = {}
for s in ON + OFF:
    c = path(1665.633777e6, s); dd = [min(abs(cidx[np.clip(np.searchsorted(cidx, x) + o, 0, len(cidx) - 1)] - x) for o in (-1, 0)) for x in c]
    c03[s] = {"path_first_last": [int(c[0]), int(c[-1])], "min_dist_channels": int(min(dd)), "steps_within_1": int(sum(x <= 1 for x in dd))}
out["P3"] = {"combs": p3, "C03_distance_to_structure": c03}
json.dump(out, open("comb.json.tmp", "w"), indent=1); os.replace("comb.json.tmp", "comb.json")
print("P1", out["P1"]); print("P2", out["P2"]["rho"], out["P2"]["p_one_sided"]); print("P3 combs", [(e["spacing_Hz"], e["power_over_median"]) for e in p3]); print("C03", c03, flush=True)
