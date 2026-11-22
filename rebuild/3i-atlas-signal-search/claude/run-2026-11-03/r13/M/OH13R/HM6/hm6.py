"""PLAN-HM6: python3 hm6.py SCAN [NFRAMES] | score
The first pair, 0013 against 0014, in X and Y: (A) the comet's coordinates on three tracks (the comet's drift, held fixed at
the dish, the drift mirrored), D3 and power; (B) the OH 1667.359 MHz line, signed, comet and dish frames, X and Y apart."""
import json, os, sys, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(HERE, "../FD")); sys.path.insert(0, os.path.join(HERE, "../HM"))
MINSB = 6; D = 2; FEEDS = ["X", "Y"]; ON_S, OFF_S = "0013", "0014"; VAR = ["c", "d", "f"]  # comet drift, dish-fixed, mirrored
OH = 1667.359e6; OHW = 0.07e6; BIN = 0.0028e6; EXCL = 0.008e6; CORE = 0.004e6
OUT = os.environ.get("HM6_OUT", HERE)


def windows():
    import hm
    real = hm.HERE; hm.HERE = HERE
    src = os.path.join(HERE, "hm_selections.json")
    if not os.path.exists(src): os.symlink("hm6_selections.json", src)
    W = hm.hm_windows(); hm.HERE = real
    return W


def scan(s, nf=None):
    import fdstream as F
    from common import N, DF, NF, TF, W as WW, dm, vel_fn, t0
    NF = nf or NF
    WIN = [w for w in windows() if w[1] != "ref"]  # as HM2 Amendment 1
    T0 = json.load(open(os.path.join(HERE, "hm6_selections.json")))["T0_mjd"]; c = WW // 2; SR = WW * DF
    ifl = np.array([F.track_f(s, f, dv, T0)[:NF] for _, _, f, dv, _ in WIN]); mid = np.rint(np.median(np.rint(ifl), axis=1)).astype(int)
    off_c = (ifl - mid[:, None]) * DF; nw = len(WIN); assert mid.min() > WW and mid.max() < N - WW
    jm = NF // 2; OFFV = {"c": off_c, "d": np.zeros_like(off_c), "f": 2 * off_c[:, [jm]] - off_c}
    span = (ifl.max(1) - ifl.min(1))  # drift across the scan, native bins
    tc = (np.arange(NF) + 0.5) * TF; carry = {v: np.zeros(nw) for v in VAR}
    accD = np.zeros((len(VAR), 2, nw)); accP = np.zeros((len(VAR), 2, nw)); n = 0
    # (B) OH: comet-frame and dish-frame spectra, +-70 kHz, native bins, summed over frames
    v = vel_fn(); tt = t0(s) + (np.arange(NF) + 0.5) * TF / 86400.0
    ic = N // 2 - (OH * (1 - v(tt) / dm.C) - dm.FC) / DF; kc = np.rint(ic).astype(int); kd = int(np.rint(np.median(ic))); H = int(OHW / DF)
    ohC = np.zeros((2, 2 * H + 1)); ohD = np.zeros((2, 2 * H + 1)); T00 = time.time()
    for j, X, Y in dm.frames(s, NF):
        ts = (j * WW + np.arange(WW)) / SR
        a = np.clip(np.searchsorted(tc, ts) - 1, 0, NF - 2); w = np.clip((ts - tc[a]) / TF, 0.0, 1.0)
        Es = {}
        for vv in VAR:
            o = OFFV[vv]; off = o[:, a] * (1 - w)[None, :] + o[:, a + 1] * w[None, :]
            Phi = carry[vv][:, None] + 2 * np.pi * np.cumsum(off, axis=1) / SR; carry[vv] = Phi[:, -1].copy(); Es[vv] = np.exp(-1j * Phi)
        for fi, Fc in enumerate((dm.fft(X), dm.fft(Y))):
            Pw = np.abs(Fc) ** 2; ohC[fi] += Pw[kc[j] - H:kc[j] + H + 1]; ohD[fi] += Pw[kd - H:kd + H + 1]
            B = np.stack([Fc[m - c:m + c] for m in mid]); z0 = sf.ifft(sf.ifftshift(B, axes=1), axis=1)
            for vi, vv in enumerate(VAR):
                S2 = sf.fftshift(sf.fft(z0 * Es[vv], axis=1), axes=1)[:, c - 64:c + 65]
                u = S2 / np.maximum(np.abs(S2), 1e-30); nn = u.shape[1] - 2 * D
                accD[vi, fi] += np.abs(np.mean(u[:, :nn] * u[:, 2 * D:2 * D + nn] * np.conj(u[:, D:D + nn]) ** 2, axis=1))
                P = np.abs(S2) ** 2; accP[vi, fi] += P[:, 64] / np.maximum(P.mean(axis=1), 1e-30)
        n += 1
        if j % 100 == 0: print(s, j, round(time.time() - T00), flush=True)
    assert n == NF
    np.savez_compressed(os.path.join(OUT, f"hm6_{s}.npz"), D3=accD / n, P=accP / n, span=span, ohC=ohC / n, ohD=ohD / n, n=n)
    json.dump({"scan": s, "frames": n, "windows": [list(x) for x in WIN], "variants": VAR, "oh_bins": 2 * H + 1, "oh_df": DF,
               "seconds": round(time.time() - T00)}, open(os.path.join(OUT, f"hm6_{s}.json"), "w"))
    print(s, "done", nw, round(time.time() - T00), flush=True)


def score():
    from common import DF
    R = {s: np.load(os.path.join(HERE, f"hm6_{s}.npz")) for s in (ON_S, OFF_S)}; WIN = json.load(open(os.path.join(HERE, f"hm6_{ON_S}.json")))["windows"]
    idx = {w[0]: i for i, w in enumerate(WIN)}; sb = {}
    for nme, k, f, dv, co in WIN:
        if k.startswith("sb:"): sb.setdefault(k[3:], []).append(nme)
    excl = [nme for nme, k, f, dv, co in WIN if k == "sel" and len(sb.get(nme, [])) < MINSB]
    sel = [(nme, co, f) for nme, k, f, dv, co in WIN if k == "sel" and nme not in excl]
    sbi = {nme: np.array([idx[m] for m in sb[nme]]) for nme, co, f in sel}; ii = {nme: idx[nme] for nme, co, f in sel}
    def ranks(v, s):
        return {nme: (np.sum(v[sbi[nme]] < v[ii[nme]]) + 0.5 * np.sum(v[sbi[nme]] == v[ii[nme]])) / len(sbi[nme]) for nme, co, f in sel}
    def cohort(st, vi, fi):
        ron, roff = ranks(R[ON_S][st][vi, fi], ON_S), ranks(R[OFF_S][st][vi, fi], OFF_S); coh = {}
        for nme, co, f in sel: coh.setdefault(co, []).append(ron[nme] - roff[nme])
        sc = {co: float(np.mean(v) * np.sqrt(len(v))) for co, v in coh.items()}; T = sc["true"]; Fs = np.array([v for co, v in sc.items() if co != "true"])
        tn = [nme for nme, co, f in sel if co == "true"]
        return {"true": T, "rank": int(1 + np.sum(Fs > T)), "n_false": len(Fs), "false_p95": float(np.percentile(Fs, 95)), "false_mean": float(Fs.mean()),
                "on_mean_rank": float(np.mean([ron[x] for x in tn])), "off_mean_rank": float(np.mean([roff[x] for x in tn])),
                "per_coordinate": {x: round(float(ron[x] - roff[x]), 4) for x in tn},
                "G1667_P_mean": float(np.mean([ron[x] - roff[x] for x in ("C08", "C09", "C10", "C11")]))}
    out = {"min_sidebands": MINSB, "excluded": excl}
    H5 = json.load(open(os.path.join(HERE, "../HM5/hm5_score.json")))["full"]
    rep = {}
    for st, k5 in (("D3", "D3"), ("P", "P")):
        for fi, fd in enumerate(FEEDS):
            a = cohort(st, 0, fi); b = H5[f"{k5}_{fd}"]
            rep[f"{st}_{fd}"] = {"hm6": a["true"], "hm5": b["true"], "per_coord_equal": all(abs(a["per_coordinate"][x] - b["per_coordinate"][x]) < 1e-9 for x in b["per_coordinate"])}
    out["reproduction"] = rep; out["reproduction_ok"] = bool(all(abs(r["hm6"] - r["hm5"]) < 1e-9 and r["per_coord_equal"] for r in rep.values()))
    print("reproduction", out["reproduction_ok"], rep, flush=True)
    tn = [nme for nme, co, f in sel if co == "true"]
    out["drift_span_bins"] = {x: round(float(R[ON_S]["span"][idx[x]]), 2) for x in tn}
    out["tracks"] = {f"{st}_{fd}": {VAR[vi]: cohort(st, vi, fi) for vi in range(len(VAR))} for st in ("D3", "P") for fi, fd in enumerate(FEEDS)}
    # (B) OH 1667.359: ON/OFF - 1, cubic baseline over +-70 kHz excluding +-8 kHz, centre +-4 kHz over robust scatter; 40 controls
    def analyse(spec):
        nbn = int(round(BIN / DF)); m = len(spec) // nbn; s = spec[:m * nbn].reshape(m, nbn).mean(1)
        o = ((np.arange(m) + 0.5) * nbn - len(spec) / 2) * DF * -1.0   # bin index rises as frequency falls (common.idx): positive = higher frequency
        if o[0] > o[-1]: s, o = s[::-1], o[::-1]
        base = np.abs(o) > EXCL; p = np.polyfit(o[base] / 1e3, s[base], 3); r = s - np.polyval(p, o / 1e3)
        sig = 1.4826 * np.median(np.abs(r[base] - np.median(r[base])))
        dep = lambda cc: float(r[np.abs(o - cc) <= CORE].mean() / sig)
        ctl = [dep(cc) for cc in np.r_[np.linspace(-0.055e6, -0.015e6, 20), np.linspace(0.015e6, 0.055e6, 20)]]
        return {"centre_sigma": round(dep(0.0), 2), "controls_rank_at_or_below": int(sum(x <= dep(0.0) for x in ctl)), "controls_min": round(min(ctl), 2),
                "controls_max": round(max(ctl), 2), "sigma_frac": float(sig), "spectrum_khz_frac": [[round(float(a) / 1e3, 2), round(float(b), 7)] for a, b in zip(o, r)]}
    out["oh1667"] = {}
    for fr, key in (("comet", "ohC"), ("dish", "ohD")):
        for fi, fd in enumerate(FEEDS):
            out["oh1667"][f"{fr}_{fd}"] = analyse(R[ON_S][key][fi] / R[OFF_S][key][fi] - 1)
        out["oh1667"][f"{fr}_I"] = analyse((R[ON_S][key][0] + R[ON_S][key][1]) / (R[OFF_S][key][0] + R[OFF_S][key][1]) - 1)
    json.dump(out, open(os.path.join(HERE, "hm6_score.json"), "w"), indent=1)
    print("drift span (bins)", out["drift_span_bins"])
    for k, v in out["tracks"].items():
        print(k, {vv: (round(v[vv]["true"], 3), v[vv]["rank"], round(v[vv]["G1667_P_mean"], 3)) for vv in VAR})
    for k, v in out["tracks"].items():
        if k in ("P_X", "D3_X", "P_Y"): print(k, {vv: v[vv]["per_coordinate"] for vv in VAR})
    for k, v in out["oh1667"].items(): print("OH1667", k, v["centre_sigma"], "rank", v["controls_rank_at_or_below"], "/40", "controls", v["controls_min"], v["controls_max"])


if __name__ == "__main__":
    a = sys.argv[1]
    score() if a == "score" else scan(a, int(sys.argv[2]) if len(sys.argv) > 2 else None)
