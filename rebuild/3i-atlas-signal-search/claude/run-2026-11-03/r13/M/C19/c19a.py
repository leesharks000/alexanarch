"""PLAN-C19 analyses 1-6 over v_00NN.npz.  python3 c19a.py -> a.json"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(M, "../../../voltages/delaymod")); import dm
exec(open(os.path.join(HERE, "c19n.py")).read().split("R = {}")[0].replace("HERE = os.path.dirname(os.path.abspath(__file__)); ", ""))
cc = 19; FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6; N, INT, C, DF, TBIN = dm.N, dm.INT, dm.C, dm.DF, dm.TBIN
SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ROLE = {s: dm.SCANS[s][2] for s in SC}
TG = json.load(open(os.path.join(HERE, "targets.json"))); T = TG["targets"]; kind = np.array([t["kind"] for t in T])
IE = np.where(kind == "E")[0]; IX = np.where(kind == "X")[0]; IXr = np.array([i for i in IX if T[i]["seq"] == "random"])
lab = lambda i: f'{T[i]["seq"]}{T[i]["n"] if T[i]["n"] is not None else ""} {T[i]["f"]/1e6:.6f}'
D = {s: np.load(os.path.join(HERE, f"v_{s}.npz")) for s in SC}
E_ = dm.ephem(); vel = lambda t: np.interp(t, E_[:, 0], E_[:, 1]); t0 = {s: 61027 + int(dm.SCANS[s][0]) / 86400.0 for s in SC}
out = {}
# A1 presence
def strength(S, b, w=128, h=3):
    seg = S[b - w:b + w]; m = np.median(seg); k = int(np.argmax(seg[w - h:w + h + 1])); return float(seg[w - h + k] / m), k - h
A1 = {}
for s in SC:
    S = D[s]["S"]; B0 = D[s]["B0"]; st = np.array([[strength(S[q], B0[i])[0] for q in (0, 1)] for i in range(len(T))])
    mx = st.max(1); A1[s] = dict(E={lab(i): [round(x, 2) for x in st[i]] for i in IE},
        dist={k: dict(n=int((kind == k).sum()), median=round(float(np.median(mx[kind == k])), 2), p95=round(float(np.percentile(mx[kind == k], 95)), 2), above10=int((mx[kind == k] > 10).sum())) for k in "EGKX"},
        xr_p99=round(float(np.percentile(mx[IXr], 99)), 2))
out["A1_presence"] = A1
# A2 the comb in the raw spectrum: peak list from the normalized scan-mean spectrum, then the same two-sequence search
A2 = {}
for s in SC:
    S = D[s]["S"].sum(0); lo, hi = int(N * 0.04), int(N * 0.96); blk = 4096
    med = np.array([np.median(S[i:i + blk]) for i in range(0, N, blk)]); base = np.repeat(med, blk)[:N]; Z = S / base
    pk = [i for i in range(lo + 1, hi - 1) if Z[i] > 8 and Z[i] >= Z[i - 1] and Z[i] >= Z[i + 1]]
    pk = sorted(pk, key=lambda i: -Z[i])[:60]; fr = [FC - (i + 0.5 - N // 2) * DF for i in pk]
    r = best(fr); A2[s] = dict(npeaks_gt8=int(sum(1 for i in range(lo, hi) if Z[i] > 8)), used=len(pk), result={k: (float(v) if v is not None else None) for k, v in r.items()},
        e_lines_among_top60=int(sum(1 for f in fr if np.min(np.abs(np.array([T[i]["f"] for i in IE]) - f)) < 25)))
out["A2_raw_comb"] = A2
# A3 time structure: per-frame power at the fixed bin (both feeds), log, correlations
A3 = {}
for s in SC:
    P = D[s]["Pf"].sum(2); L = np.log(P / np.median(P, 0)); Cm = np.corrcoef(L.T)
    def mc(I, J=None):
        J = I if J is None else J; v = [Cm[i, j] for i in I for j in J if i < j or J is not I]; return round(float(np.mean(v)), 3) if v else None
    iA = [i for i in IE if T[i]["seq"] == "A"]; iB = [i for i in IE if T[i]["seq"] == "B"]
    A3[s] = dict(AA=mc(iA), BB=mc(iB), AB=mc(iA, iB), XrXr=mc(list(IXr)), EXr=mc(list(IE), list(IXr)))
out["A3_time"] = A3
# A4 kinematics: fit on ON0013, predict without refit
def rowtimes(s): return t0[s] + (np.arange(D[s]["R"].shape[0]) + 0.5) * INT * N * TBIN / 86400.0
v13 = vel(t0["0013"] + 0.5 * N * TBIN / 86400.0)
A4 = {}
for i in IE:
    R13 = D["0013"]["R"][:, i].astype(np.float32).sum(1); w = R13.shape[1] // 2
    m = R13.mean(0); k13 = int(np.argmax(m[w - 20:w + 21])) - 20; b13 = D["0013"]["B0"][i] + k13
    sh13 = FC * (vel(rowtimes("0013")) - v13) / C / DF
    rec = {"fit_bin_offset_0013": k13}
    for s in SC:
        Rr = D[s]["R"][:, i].astype(np.float32).sum(1); base = D[s]["B0"][i] - w; sh = FC * (vel(rowtimes(s)) - v13) / C / DF
        sc = {}
        for name, pred in (("F", np.full(len(sh), b13, float)), ("C", b13 + sh - sh13.mean())):
            pr = np.rint(pred - base).astype(int); ok = (pr > 3) & (pr < 2 * w - 4)
            if not ok.any(): sc[name] = None; continue
            pw = [Rr[r, pr[r] - 2:pr[r] + 3].sum() / (5 * np.median(Rr[r])) for r in np.where(ok)[0]]
            obs = [int(np.argmax(Rr[r, max(pr[r] - 10, 0):pr[r] + 11])) + max(pr[r] - 10, 0) - pr[r] for r in np.where(ok)[0]]
            sc[name] = dict(track_power=round(float(np.mean(pw)), 2), resid_bins=round(float(np.median(np.abs(obs))), 1))
        rec[s] = sc
    A4[lab(i)] = rec
out["A4_kinematics"] = A4
# A5 polarization and A6 voltage, from V (per-frame complex spectra ±8 bins around each E line)
A56 = {}
for s in SC:
    V = D[s]["V"]; S = D[s]["S"]; rows = {}
    for jj, i in enumerate(IE):
        c = V[:, jj, :, 7:10]; x, y = c[:, 0], c[:, 1]
        coh = float(np.abs((x * np.conj(y)).sum()) / np.sqrt((np.abs(x) ** 2).sum() * (np.abs(y) ** 2).sum()))
        a = np.abs(c).sum((1, 2)); a2 = a ** 2
        kurt = float(np.mean((a2 - a2.mean()) ** 4) / np.var(a2) ** 2) if np.var(a2) > 0 else None
        top = float(np.sort(a2)[-len(a2) // 20:].sum() / a2.sum())
        fx = np.abs(np.fft.rfft(a2 - a2.mean())) ** 2; fq = np.fft.rfftfreq(len(a2), N * TBIN); k = int(np.argmax(fx[1:])) + 1
        b = D[s]["B0"][i]; xy = float(S[0, b - 1:b + 2].sum() / S[1, b - 1:b + 2].sum())
        rows[lab(i)] = dict(xy_power=round(xy, 3), coh=round(coh, 3), kurt=round(kurt, 2) if kurt else None, top5pct=round(top, 3), mod_hz=round(float(fq[k]), 4), mod_frac=round(float(fx[k] / fx[1:].sum()), 3))
    eb = V[:, :, :, [0, 1, 14, 15]]; ebx, eby = eb[:, :, 0], eb[:, :, 1]
    noise_coh = float(np.median([np.abs((ebx[:, j, m] * np.conj(eby[:, j, m])).sum()) / np.sqrt((np.abs(ebx[:, j, m]) ** 2).sum() * (np.abs(eby[:, j, m]) ** 2).sum()) for j in range(eb.shape[1]) for m in range(4)]))
    A56[s] = dict(lines=rows, edge_bin_coh_median=round(noise_coh, 3), edge_top5pct_expect=0.05)
out["A5_A6_pol_voltage"] = A56
json.dump(out, open(os.path.join(HERE, "a.json"), "w"), indent=1, default=float)
print("written a.json")
