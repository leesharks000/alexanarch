"""Offline statistics for PLAN.md v1 over out/<scan>/ products. python3 analyze.py > results.json"""
import os, json, itertools
import numpy as np
from scipy.ndimage import median_filter, maximum_filter1d
import dm

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
N = dm.N; LABELS = list(itertools.combinations(SC, 3))
R = {}

def rz(a, axis=None):
    m = np.median(a, axis=axis, keepdims=True); s = 1.4826 * np.median(np.abs(a - m), axis=axis, keepdims=True)
    s[s == 0] = np.inf; return (a - m) / s

def onlyon(Z, on, zon, zoff, tol=1):
    """Z: dict scan -> 1-D z array (same grid). Count positions with z>=zon in all `on`, <zoff in the rest (±tol)."""
    mf = lambda a: maximum_filter1d(a, 2 * tol + 1, mode="nearest") if tol else a
    ok = np.ones(len(next(iter(Z.values()))), bool)
    for s in SC:
        ok &= (mf(Z[s]) >= zon) if s in on else (mf(Z[s]) < zoff)
    return np.where(ok)[0]

def perm(Z, zon, zoff, tol=1, keep=False):
    counts = {",".join(l): len(onlyon(Z, l, zon, zoff, tol)) for l in LABELS}
    true = counts[",".join(ON)]; others = [v for k, v in counts.items() if k != ",".join(ON)]
    d = {"true": true, "others_max": max(others), "others_mean": float(np.mean(others)),
         "rank_frac_ge": float(np.mean([o >= true for o in others]))}
    if keep: d["positions"] = onlyon(Z, ON, zon, zoff, tol)[:200].tolist()
    return d

def clusters(idx, gap=4):
    if len(idx) == 0: return []
    out = [[idx[0]]]
    for i in idx[1:]:
        (out[-1].append(i) if i - out[-1][-1] <= gap else out.append([i]))
    return out

# ---------- M1 ----------
M1 = {s: np.load(f"{OUT}/{s}/M1_sparse.npz") for s in SC}
R["M1"] = {}
for m in (1, 2, 4):
    for zon, zoff in ((2.5, 2.0), (3.0, 2.0)):
        counts = []; keep = None
        for fi in range(41):
            v0r = float(M1["0013"][f"m{m}_f{fi}_v0"]); A = {}
            for s in SC:
                d = M1[s]; idx = d[f"m{m}_f{fi}_idx"].astype(np.int64); z = d[f"m{m}_f{fi}_z"].astype(np.float32)
                sh = int(np.rint(m * dm.FC * (float(d[f"m{m}_f{fi}_v0"]) - v0r) / dm.C / dm.DF))
                a = np.full(N + 4000, -99.0, np.float32); j = idx - sh + 2000
                okk = (j >= 0) & (j < len(a)); np.maximum.at(a, j[okk], z[okk]); A[s] = a
            hit = onlyon(A, ON, zon, zoff)
            cl = clusters(hit); counts.append(len(cl))
            if fi == 0:
                keep = [{"index_ref0013": int(np.mean(c)) - 2000, "f_topo_ref_MHz_if_m1": (dm.FC - (int(np.mean(c)) - 2000 - N // 2) * dm.DF) / 1e6,
                         **{f"z_{s}": float(maximum_filter1d(A[s], 3)[c[0]]) for s in SC}} for c in cl]
        null = counts[1:]
        R["M1"][f"m{m}_{zon}/{zoff}"] = {"comet_clusters": counts[0], "null_mean": float(np.mean(null)), "null_sd": float(np.std(null)),
                                         "null_max": int(max(null)), "null_p95": float(np.percentile(null, 95)),
                                         "null_frac_ge": float(np.mean([n >= counts[0] for n in null])), "comet_list": keep[:60]}

# ---------- D1 short-lag delayed copy ----------
def white(P):
    b = median_filter(P.astype(np.float64), 1025, mode="nearest"); b[b <= 0] = 1
    w = P / b - 1.0; ed = int(0.03 * N); w[:ed] = 0; w[-ed:] = 0; w[N // 2 - 5:N // 2 + 6] = 0
    s = 1.4826 * np.median(np.abs(w[ed:-ed])); return np.clip(w, -10 * s, 10 * s), b
D1 = {k: {} for k in ("X", "Y", "XY")}
for s in SC:
    wx, bx = white(np.load(f"{OUT}/{s}/PX.npy")); wy, by = white(np.load(f"{OUT}/{s}/PY.npy"))
    cxy = np.load(f"{OUT}/{s}/CXY.npy") / np.sqrt(bx * by); ed = int(0.03 * N)
    cxy[:ed] = 0; cxy[-ed:] = 0; cxy[N // 2 - 5:N // 2 + 6] = 0
    for k, w in (("X", wx), ("Y", wy), ("XY", cxy)):
        r = np.abs(np.fft.ifft(np.fft.ifftshift(w)))
        lags = r[:N // 2].copy(); lags[:3] = np.median(lags)
        D1[k][s] = rz(lags).ravel()
R["D1"] = {k: {f"{a}/{b}": perm(D1[k], a, b, keep=True) for a, b in ((5, 3), (4, 3))} for k in D1}
R["D1_top"] = {k: {s: [[int(i), float(D1[k][s][i]), i * dm.TBIN] for i in np.argsort(D1[k][s])[-8:][::-1]] for s in SC} for k in D1}

# ---------- D2 long-lag, M2-low ----------
D2 = {}; ML = {}; RHO = {}
for s in SC:
    G = np.load(f"{OUT}/{s}/G.npy").astype(np.float64)  # (2, T, 512)
    T = G.shape[1]; t = np.arange(T)
    out_acf = []; out_ml = []
    for p in (0, 1):
        g = G[p] / G[p].mean(0) - 1.0
        A = np.vstack([t, np.ones(T)]).T; coef, *_ = np.linalg.lstsq(A, g, rcond=None); g = g - A @ coef
        F = np.fft.rfft(g, 2 * T, axis=0)
        acf = np.fft.irfft(np.abs(F) ** 2, axis=0)[:T]; acf = acf / acf[0]
        out_acf.append(acf); out_ml.append(np.abs(np.fft.rfft(g, axis=0)) ** 2)
    gx = G[0] / G[0].mean(0) - 1; gy = G[1] / G[1].mean(0) - 1
    xy = np.fft.irfft(np.fft.rfft(gx, 2 * T, axis=0) * np.conj(np.fft.rfft(gy, 2 * T, axis=0)), axis=0)
    xy = xy / np.sqrt((gx ** 2).sum(0) * (gy ** 2).sum(0))
    RHO[s] = {"X": out_acf[0][:, 8:504].mean(1), "Y": out_acf[1][:, 8:504].mean(1), "XY_pos": xy[:T, 8:504].mean(1), "XY_neg": xy[-1:-T:-1, 8:504].mean(1)}
    acf = (out_acf[0] + out_acf[1]) / 2; a = acf[2:6000, 8:504]
    D2[s] = rz(a, axis=0).ravel()           # per-bin z over lags 2..5999 (44.8 ms .. 134 s)
    ml = (out_ml[0] + out_ml[1])[2:, 8:504]  # modulation 2/T*... per bin
    ML[s] = rz(np.log(ml), axis=0).ravel()
    np.save(f"{OUT}/{s}/rho.npy", np.vstack([RHO[s][k][:6000] for k in ("X", "Y", "XY_pos", "XY_neg")]).astype(np.float32))
R["D2"] = {f"{a}/{b}": perm(D2, a, b, tol=0) for a, b in ((5, 3), (6, 3))}
R["D2_rho_summary"] = {s: {k: {"lag1_44.8ms": float(RHO[s][k][2]), "max_lag>=10s": float(RHO[s][k][447:6000].max()),
                               "argmax_lag>=10s_s": float((447 + RHO[s][k][447:6000].argmax()) * 0.0223696)} for k in RHO[s]} for s in SC}
R["M2_low"] = {f"{a}/{b}": perm(ML, a, b, tol=0) for a, b in ((5, 3), (6, 3))}

# ---------- M2 wide envelope ----------
EW = {}
for s in SC:
    e = (np.load(f"{OUT}/{s}/EX.npy").astype(np.float64) + np.load(f"{OUT}/{s}/EY.npy"))[1:]
    b = median_filter(e, 1025, mode="nearest"); w = np.log(e / b); w[:20] = 0
    EW[s] = rz(w).ravel()
R["M2_wide"] = {f"{a}/{b}": perm(EW, a, b, keep=True) for a, b in ((5, 3), (4, 3))}
R["M2_wide_top"] = {s: [[int(i) + 1, float(EW[s][i]), (i + 1) * dm.DF / 2 * 2] for i in np.argsort(EW[s])[-10:][::-1]] for s in SC}

# ---------- M3 local envelope at the 13 and 100 controls ----------
meta = json.load(open(f"{OUT}/0013/meta.json")); ids = meta["ids"]; ctrl = [i for i, x in enumerate(ids) if x.startswith("K")]
ZL = {}
for s in SC:
    M = np.load(f"{OUT}/{s}/M3.npy").sum(0)[:, 1:1024]  # positive envelope frequencies 2.79 Hz .. 2.86 kHz
    L = np.log(M); base = np.median(L[ctrl], axis=0)
    S = L - base; ZL[s] = (S - np.median(S[ctrl], 0)) / (1.4826 * np.median(np.abs(S[ctrl] - np.median(S[ctrl], 0)), 0))
res3 = {}
for c, name in enumerate(ids):
    Z = {s: ZL[s][c] for s in SC}
    res3[name] = {r: len(onlyon(Z, ON, *map(float, r.split("/")))) for r in ("2.5/2.0", "3.0/2.0")}
cc = [res3[ids[i]]["2.5/2.0"] for i in ctrl]
R["M3"] = {"per_coordinate": {k: v for k, v in res3.items() if k.startswith("C")},
           "controls_2.5/2.0": {"mean": float(np.mean(cc)), "p95": float(np.percentile(cc, 95)), "max": int(max(cc))},
           "rank_vs_controls": {k: float(np.mean([x >= v["2.5/2.0"] for x in cc])) for k, v in res3.items() if k.startswith("C")}}
print(json.dumps(R, indent=1, default=float))
