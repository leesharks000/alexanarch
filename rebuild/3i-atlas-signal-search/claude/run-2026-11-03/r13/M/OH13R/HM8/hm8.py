"""PLAN-HM8: python3 hm8.py SCAN [NFRAMES] | score
(A) HM6's path A (three tracks: comet drift c, dish-fixed d, mirrored f) on the other two pairs, 0015/0016 and 0017/0018,
with hm6.py unchanged; (B) the Green Bank X excess at C03-C13 put on HM7's Parkes scale under stated factors."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); HM6D = os.path.join(HERE, "../HM6"); HMR2D = os.path.join(HERE, "../HMR2")
PAIRS = [("0013", "0014"), ("0015", "0016"), ("0017", "0018")]
VAR = ["c", "d", "f"]; FEEDS = ["X", "Y"]; MINSB = 6; G1667 = ["C08", "C09", "C10", "C11"]
# (B) stated factors, frozen: SEFD (Jy) GBT L-band and Parkes UWL near 1.6 GHz, from memory, as a range; comet distances (au)
SEFD_G = 10.0; SEFD_P = (25.0, 40.0); D_G = 1.798; D_P = {"20250731": 2.817, "20250912": 2.548, "20251005": 2.483}
BINW_G = 2.7939677238464355; BINW_P = 2.0; STOKES_I = 0.5; SIGMA_P = {"20250731": 0.13, "20250912": 0.1298, "20251005": 0.1296}


def scan(s, nf=None):
    os.environ["HM6_OUT"] = os.environ.get("HM8_OUT", HERE)
    sys.path.insert(0, HM6D); import hm6
    hm6.scan(s, nf)


def load(s):
    d = HM6D if s in ("0013", "0014") else os.environ.get("HM8_OUT", HERE)
    return np.load(os.path.join(d, f"hm6_{s}.npz")), json.load(open(os.path.join(d, f"hm6_{s}.json")))["windows"]


def score():
    out = {"plan": "PLAN-HM8.md"}
    R = {}; WIN = None
    for on, off in PAIRS:
        for s in (on, off):
            R[s], w = load(s); WIN = WIN or w; assert w == WIN
    idx = {w[0]: i for i, w in enumerate(WIN)}; sb = {}
    for nme, k, f, dv, co in WIN:
        if k.startswith("sb:"): sb.setdefault(k[3:], []).append(nme)
    excl = [nme for nme, k, f, dv, co in WIN if k == "sel" and len(sb.get(nme, [])) < MINSB]
    sel = [(nme, co) for nme, k, f, dv, co in WIN if k == "sel" and nme not in excl]
    sbi = {nme: np.array([idx[m] for m in sb[nme]]) for nme, co in sel}; ii = {nme: idx[nme] for nme, co in sel}
    tn = [nme for nme, co in sel if co == "true"]
    def ranks(v): return {nme: (np.sum(v[sbi[nme]] < v[ii[nme]]) + 0.5 * np.sum(v[sbi[nme]] == v[ii[nme]])) / len(sbi[nme]) for nme, co in sel}
    def cohort(on, off, st, vi, fi):
        ron, roff = ranks(R[on][st][vi, fi]), ranks(R[off][st][vi, fi]); coh = {}
        for nme, co in sel: coh.setdefault(co, []).append(ron[nme] - roff[nme])
        sc = {co: float(np.mean(v) * np.sqrt(len(v))) for co, v in coh.items()}; T = sc["true"]; Fs = np.array([v for co, v in sc.items() if co != "true"])
        return {"true": round(T, 4), "rank": int(1 + np.sum(Fs > T)), "n_false": len(Fs), "false_mean": round(float(Fs.mean()), 4),
                "per_coordinate": {x: round(float(ron[x] - roff[x]), 4) for x in tn},
                "G1667_P_mean": round(float(np.mean([ron[x] - roff[x] for x in G1667])), 4)}
    # reproduction: track c power, comet windows, against HMR2's per-frame P (frame mean), new scans only
    rep = {}
    for s in ("0015", "0016", "0017", "0018"):
        h = np.load(os.path.join(HMR2D, f"hmr2_{s}.npz"))["P"]; hw = json.load(open(os.path.join(HMR2D, f"hmr2_{s}.json")))["windows"]
        worst = 0.0
        for k, w in enumerate(hw):
            for fi in range(2):
                a = float(R[s]["P"][0, fi, idx[w[0]]]); b = float(h[fi, :, k].mean()); worst = max(worst, abs(a - b) / abs(b))
        rep[s] = worst
    out["reproduction_max_rel"] = rep; out["reproduction_ok"] = bool(all(v < 1e-4 for v in rep.values()))
    print("reproduction", out["reproduction_ok"], rep, flush=True)
    out["drift_span_bins"] = {s: {x: round(float(R[s]["span"][idx[x]]), 2) for x in tn} for s in ("0013", "0015", "0017")}
    A = {}
    for on, off in PAIRS:
        A[f"{on}/{off}"] = {f"{st}_{fd}": {VAR[vi]: cohort(on, off, st, vi, fi) for vi in range(3)} for st in ("P", "D3") for fi, fd in enumerate(FEEDS)}
        px = A[f"{on}/{off}"]["P_X"]; g = {v: px[v]["G1667_P_mean"] for v in VAR}
        A[f"{on}/{off}"]["verdict_P_X_G1667"] = ("follows the comet" if g["c"] > g["d"] and g["c"] > g["f"] else "fixed at the dish" if g["d"] >= g["c"] else "not decided")
        A[f"{on}/{off}"]["C09_P_X"] = {v: px[v]["per_coordinate"]["C09"] for v in VAR}
    out["A"] = A
    newp = [A[p]["verdict_P_X_G1667"] for p in ("0015/0016", "0017/0018")]
    out["A_holds_beyond_first_pair"] = "follows the comet" in newp
    out["A_pooled_G1667_P_X"] = {v: round(float(np.mean([A[p]["P_X"][v]["G1667_P_mean"] for p in A if p.count("/")])), 4) for v in VAR}
    # (B) scale: e = (ON - OFF frame-mean P) of the coordinate minus the median of the same over its sidebands, X, track c, HMR2 per-frame P
    B = {}
    for on, off in PAIRS:
        Pon = np.load(os.path.join(HMR2D, f"hmr2_{on}.npz"))["P"]; Poff = np.load(os.path.join(HMR2D, f"hmr2_{off}.npz"))["P"]
        hw = json.load(open(os.path.join(HMR2D, f"hmr2_{on}.json")))["windows"]; hi = {w[0]: k for k, w in enumerate(hw)}
        dlt = {fd: Pon[fi].mean(0) - Poff[fi].mean(0) for fi, fd in enumerate(FEEDS)}
        for x in tn:
            sbk = [hi[w[0]] for w in hw if w[1] == f"sb:{x}"]
            for fd in FEEDS:
                e = float(dlt[fd][hi[x]] - np.median(dlt[fd][sbk]))
                B.setdefault(x, {}).setdefault(fd, {})[f"{on}/{off}"] = e
    pred = {}
    for x in tn:
        eX = float(np.mean(list(B[x]["X"].values())))
        for sess, dP in D_P.items():
            lo, hi_ = [eX * (SEFD_G / sp) * (D_G / dP) ** 2 * (BINW_G / BINW_P) * STOKES_I / SIGMA_P[sess] for sp in SEFD_P[::-1]]
            pred.setdefault(x, {})[sess] = [round(min(lo, hi_), 3), round(max(lo, hi_), 3)]
    out["B"] = {"excess_frac_per_native_bin": {x: {fd: {p: round(v, 6) for p, v in B[x][fd].items()} for fd in FEEDS} for x in tn},
                "predicted_parkes_a_range": pred, "hm7_floor_a": {"every_scan": 1.5, "about_half": 1.0}}
    json.dump(out, open(os.path.join(HERE, "hm8_score.json"), "w"), indent=1)
    for p in A: print(p, A[p]["verdict_P_X_G1667"], {v: A[p]["P_X"][v]["G1667_P_mean"] for v in VAR}, "C09", A[p]["C09_P_X"])
    print("pooled", out["A_pooled_G1667_P_X"], "holds beyond first pair", out["A_holds_beyond_first_pair"])
    for x in tn: print(x, "eX", {p: round(v, 5) for p, v in B[x]["X"].items()}, "pred a", pred[x])


if __name__ == "__main__":
    a = sys.argv[1]
    score() if a == "score" else scan(a, int(sys.argv[2]) if len(sys.argv) > 2 else None)
