"""PLAN-C4850 analyses.  python3 c4850a.py CC -> a_ccCC.json"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(M, "../../../voltages/delaymod")); import dm
exec(open(os.path.join(M, "C19", "c19n.py")).read().split("R = {}")[0].replace("HERE = os.path.dirname(os.path.abspath(__file__)); ", ""))
cc = int(sys.argv[1]); FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6; N, INT, C, DF, TBIN = dm.N, dm.INT, dm.C, dm.DF, dm.TBIN
SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
T = json.load(open(os.path.join(HERE, f"targets_cc{cc}.json")))["targets"]; kind = np.array([t["kind"] for t in T])
D = {s: {k: v for k, v in np.load(os.path.join(HERE, f"v_cc{cc}_{s}.npz")).items() if k in ("S", "Sc", "B0", "v0")} for s in SC}
E_ = dm.ephem(); vel = lambda t: np.interp(t, E_[:, 0], E_[:, 1]); t0 = {s: 61027 + int(dm.SCANS[s][0]) / 86400.0 for s in SC}
v0 = {s: float(D[s]["v0"]) for s in SC}
dshift = lambda a, b: int(np.rint(FC * (v0[b] - v0[a]) / C / DF))   # comet-frame bin offset from scan a's frame to scan b's
def excess(S, b, w=128, h=10):
    if b - w < 0 or b + w > S.shape[-1]: return np.nan
    seg = S[:, b - w:b + w].sum(0); m = np.median(seg); return float((seg[w - h:w + h + 1] - m).clip(0).sum() / m)
def tobin(f): return int(np.rint(N // 2 + (FC - f) / DF - 0.5))
rng = np.random.default_rng(1); RB = rng.integers(int(N * .05), int(N * .95), 400)
noise = {s: dict(S=float(np.percentile([excess(D[s]["S"], b) for b in RB], 95)), Sc=float(np.percentile([excess(D[s]["Sc"], b) for b in RB], 95))) for s in SC}
out = dict(cc=cc, fc=FC, noise_p95=noise)
def judge(b, s0):
    """Excess at bin b of scan s0 in every scan: fixed (S, same bin) and comet track (Sc, shifted)."""
    fx = {s: excess(D[s]["S"], b) for s in SC}; cm = {s: excess(D[s]["Sc"], b + dshift(s0, s)) for s in SC}
    on = max(fx[s0], cm[s0])
    def quiet(tr, key): return all(tr[s] <= max(0.01 * on, noise[s][key]) for s in OFF)
    return dict(fixed={s: round(v, 2) for s, v in fx.items()}, comet={s: round(v, 2) for s, v in cm.items()},
                off_over_on_fixed=round(max(fx[s] for s in OFF) / fx[s0], 3) if fx[s0] > 0 else None,
                off_over_on_comet=round(max(cm[s] for s in OFF) / cm[s0], 3) if cm[s0] > 0 else None,
                lead=bool(quiet(fx, "S") and quiet(cm, "Sc") and on > 2 * noise[s0]["S"]))
# 1 location per saved event
L1 = []
for i, t in enumerate(T):
    if t["kind"] not in "EQ": continue
    j = judge(int(D[t["scan"]]["B0"][i]), t["scan"]); L1.append(dict(kind=t["kind"], cls=t["cls"], scan=t["scan"], mhz=round(t["f"] / 1e6, 6), z=t["z"], hz_per_s=round(t["hz_per_s"], 4), **j))
out["events"] = L1
# 2 catalogue-free lines in each ON scan, both frames, 1 and 16 bins
def peaks(S, L):
    sm = np.convolve(S, np.ones(L) / L, "same") if L > 1 else S; blk = 4096; nb = N // blk
    Bk = sm[:nb * blk].reshape(nb, blk); md = np.median(Bk, 1); mad = 1.4826 * np.median(np.abs(Bk - md[:, None]), 1)
    Z = (Bk - md[:, None]) / mad[:, None]; Z = Z.ravel(); lo, hi = int(N * .04), int(N * .96)
    cand = np.where(Z[lo:hi] > 8)[0] + lo
    return [int(i) for i in cand if Z[i] == Z[max(i - 8, 0):i + 9].max()], Z
L2 = []; fam = {}
for s0 in ON:
    for frame in ("S", "Sc"):
        for Lr in (1, 16):
            pk, Z = peaks(D[s0][frame].sum(0), Lr)
            fam[f"{s0}_{frame}_L{Lr}"] = dict(npeaks=len(pk), **{k: (float(v) if v is not None else None) for k, v in best([FC - (b + 0.5 - N // 2) * DF for b in sorted(pk, key=lambda b: -Z[b])[:60]]).items()})
            for b in pk:
                j = judge(b, s0); L2.append(dict(scan=s0, frame=frame, L=Lr, bin=b, mhz=round((FC - (b + 0.5 - N // 2) * DF) / 1e6, 6), z=round(float(Z[b]), 1), **j))
out["lines"] = L2; out["families"] = fam
out["summary"] = dict(
    events=dict(n=len(L1), leads=sum(x["lead"] for x in L1), median_off_over_on_fixed=float(np.nanmedian([x["off_over_on_fixed"] for x in L1 if x["off_over_on_fixed"] is not None]))),
    lines=dict(n=len(L2), leads=sum(x["lead"] for x in L2), by=dict((k, sum(1 for x in L2 if f'{x["scan"]}_{x["frame"]}_L{x["L"]}' == k)) for k in fam)))
json.dump(out, open(os.path.join(HERE, f"a_cc{cc}.json"), "w"), indent=1, default=float)
print(json.dumps(out["summary"], indent=1)); print(json.dumps(fam, indent=0)[:1500])
for x in [x for x in L1 + L2 if x["lead"]][:40]: print("LEAD", {k: x[k] for k in x if k not in ("fixed", "comet")}, x["fixed"], x["comet"])
