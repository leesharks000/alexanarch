"""PLAN-C19 amendments after the freeze (2026-11-20 15:08 onward): drift decomposition of the strong teeth
(ChatGPT, 2026-11-20 15:08), the location ratios through 0018, and analysis 2 at 16-bin resolution.  python3 c19b.py -> b.json"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(M, "../../../voltages/delaymod")); import dm
exec(open(os.path.join(HERE, "c19n.py")).read().split("R = {}")[0].replace("HERE = os.path.dirname(os.path.abspath(__file__)); ", ""))
FC = 1631.8359375e6; N, INT, DF, TBIN = dm.N, dm.INT, dm.DF, dm.TBIN; SC = ["0013", "0014", "0015", "0016", "0017", "0018"]
T = json.load(open(os.path.join(HERE, "targets.json")))["targets"]
G = {(t["seq"], t["n"]): i for i, t in enumerate(T) if t["kind"] == "G"}; Ei = [i for i, t in enumerate(T) if t["kind"] == "E"]
D = {s: np.load(os.path.join(HERE, f"v_{s}.npz")) for s in SC}
t0 = {s: int(dm.SCANS[s][0]) for s in SC}
out = {}
def excess(S, b, w=128, h=10):
    seg = S[:, b - w:b + w].sum(0); m = np.median(seg); return float((seg[w - h:w + h + 1] - m).clip(0).sum() / m)
out["location"] = {nm: {s: round(excess(D[s]["S"], D[s]["B0"][i]), 2) for s in SC} for nm, i in (("A2", G[("A", 2)]), ("B1", G[("B", 1)]))}
out["location"]["E_sum"] = {s: round(sum(excess(D[s]["S"], D[s]["B0"][i]) for i in Ei), 2) for s in SC}
# per-row tracks: power-weighted centroid within ±12 bins of the row's peak (peak sought within ±40 of the scan-mean peak)
def tracks(i):
    res = {}
    for s in SC:
        R = D[s]["R"][:, i].astype(np.float32).sum(1); w = R.shape[1] // 2; b0 = D[s]["B0"][i]
        m = R.mean(0); k0 = int(np.argmax(m[w - 40:w + 41])) + w - 40
        ts, fs, pw = [], [], []
        for r in range(R.shape[0]):
            x = R[r]; lo = max(k0 - 40, 0); k = int(np.argmax(x[lo:k0 + 41])) + lo
            seg = (x[k - 12:k + 13] - np.median(x)).clip(0); 
            if seg.sum() <= 0: continue
            c = (np.arange(k - 12, k + 13) * seg).sum() / seg.sum()
            ts.append(t0[s] + (r + 0.5) * INT * N * TBIN); fs.append(FC - (b0 - w + c + 0.5 - N // 2) * DF); pw.append(float(x[k] / np.median(x)))
        ts, fs, pw = map(np.array, (ts, fs, pw)); good = pw > 3
        fit = np.polyfit(ts[good] - ts[good].mean(), fs[good], 1) if good.sum() > 5 else [np.nan, np.nan]
        res[s] = dict(n=int(good.sum()), drift_hz_s=round(float(fit[0]), 4), f_mean=float(fit[1]), t=ts.tolist(), f=fs.tolist(), p=pw.tolist())
    return res
TR = {nm: tracks(G[k]) for nm, k in (("A2", ("A", 2)), ("B1", ("B", 1)))}
out["tracks_summary"] = {nm: {s: dict(n=v["n"], drift_hz_s=v["drift_hz_s"], f_mhz=round(v["f_mean"] / 1e6, 7)) for s, v in tr.items()} for nm, tr in TR.items()}
# whole-observation fits across scans (rows with power > 3)
def allfit(tr, deg):
    t = np.concatenate([np.array(v["t"])[np.array(v["p"]) > 3] for v in tr.values()]); f = np.concatenate([np.array(v["f"])[np.array(v["p"]) > 3] for v in tr.values()])
    if len(t) < 10: return None
    c = np.polyfit(t - t.mean(), f, deg); r = f - np.polyval(c, t - t.mean()); return dict(coef=[float(x) for x in c], rms_hz=round(float(np.sqrt(np.mean(r ** 2))), 2), n=len(t))
out["across_scans"] = {nm: {"linear": allfit(tr, 1), "quadratic": allfit(tr, 2)} for nm, tr in TR.items()}
# spacing A2 - B1 per scan (scan means) and its drift
out["spacing_A2_B1_hz"] = {s: round(TR["A2"][s]["f_mean"] - TR["B1"][s]["f_mean"], 2) for s in SC}
out["fractional_drift"] = {s: dict(A2=TR["A2"][s]["drift_hz_s"] / (TR["A2"][s]["f_mean"]) * 1e9, B1=TR["B1"][s]["drift_hz_s"] / (TR["B1"][s]["f_mean"]) * 1e9) for s in SC}
# comet drift for reference
E_ = dm.ephem(); vel = lambda t: np.interp(t, E_[:, 0], E_[:, 1])
out["comet_drift_hz_s"] = {s: round(float(-FC * (vel(61027 + (t0[s] + 300) / 86400) - vel(61027 + t0[s] / 86400)) / dm.C / 300), 4) for s in SC}
# analysis 2 at 16-bin resolution
A2 = {}
for s in SC:
    S = D[s]["S"].sum(0); sm = np.convolve(S, np.ones(16) / 16, "same"); blk = 4096
    med = np.repeat([np.median(sm[i:i + blk]) for i in range(0, N, blk)], blk)[:N]; mad = np.repeat([1.4826 * np.median(np.abs(sm[i:i + blk] - np.median(sm[i:i + blk]))) for i in range(0, N, blk)], blk)[:N]
    Z = (sm - med) / mad; lo, hi = int(N * .04), int(N * .96)
    pk = [i for i in range(lo + 8, hi - 8, 1) if Z[i] > 8 and Z[i] == Z[i - 8:i + 9].max()]
    pk = sorted(pk, key=lambda i: -Z[i])[:60]; fr = [FC - (i + 0.5 - N // 2) * DF for i in pk]
    r = best(fr); A2[s] = dict(npeaks=len(pk), two=r["two"], one=r["one"], step=r["step"], peaks_mhz=[round(f / 1e6, 6) for f in fr[:20]])
out["raw_comb_L16"] = A2
json.dump(dict(out, tracks=TR), open(os.path.join(HERE, "b.json"), "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k != "raw_comb_L16"}, indent=1, default=float)[:4000])
for s, v in A2.items(): print(s, {k: v[k] for k in ("npeaks", "two", "one", "step")})
