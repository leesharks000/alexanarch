"""PLAN-HM5: python3 hm5.py SCAN | score   (the first ON–OFF pair, 0013 against 0014, through time; X and Y, D3 and power)"""
import json, os, sys, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(HERE, "../FD")); sys.path.insert(0, os.path.join(HERE, "../HM"))
MINSB = 6; D = 2; BIN = 32; FEEDS = ["X", "Y"]; ON_S, OFF_S = "0013", "0014"


def windows():
    import hm
    real = hm.HERE; hm.HERE = HERE
    src = os.path.join(HERE, "hm_selections.json")
    if not os.path.exists(src): os.symlink("hm5_selections.json", src)
    W = hm.hm_windows(); hm.HERE = real
    return W


def nbins(nf): return nf // BIN   # 26 bins; the last takes the remainder (frames 800–832)


def binof(j, nf): return min(j // BIN, nbins(nf) - 1)


def scan(s):
    import fdstream as F
    from common import N, DF, NF, TF, W as WW, dm
    WIN = [w for w in windows() if w[1] != "ref"]  # as HM2 Amendment 1
    T0 = json.load(open(os.path.join(HERE, "hm5_selections.json")))["T0_mjd"]; c = WW // 2; SR = WW * DF
    ifl = np.array([F.track_f(s, f, dv, T0) for _, _, f, dv, _ in WIN]); mid = np.rint(np.median(np.rint(ifl), axis=1)).astype(int)
    off_f = (ifl - mid[:, None]) * DF; nw = len(WIN); assert mid.min() > WW and mid.max() < N - WW
    comet = sorted({i for i, (n, k, f, dv, co) in enumerate(WIN) if co == "true"})   # comet windows and their sidebands, kept per frame
    NB = nbins(NF); tc = (np.arange(NF) + 0.5) * TF; carry = np.zeros(nw)
    accD = np.zeros((2, NB, nw)); accP = np.zeros((2, NB, nw)); nb = np.zeros(NB)
    frD = np.zeros((2, NF, len(comet)), np.float32); frP = np.zeros((2, NF, len(comet)), np.float32); T00 = time.time()
    for j, X, Y in dm.frames(s, NF):
        b = binof(j, NF); nb[b] += 1
        ts = (j * WW + np.arange(WW)) / SR
        a = np.clip(np.searchsorted(tc, ts) - 1, 0, NF - 2); w = np.clip((ts - tc[a]) / TF, 0.0, 1.0)
        off = off_f[:, a] * (1 - w)[None, :] + off_f[:, a + 1] * w[None, :]
        Phi = carry[:, None] + 2 * np.pi * np.cumsum(off, axis=1) / SR; carry = Phi[:, -1].copy(); E = np.exp(-1j * Phi)
        for fi, Fc in enumerate((dm.fft(X), dm.fft(Y))):
            B = np.stack([Fc[m - c:m + c] for m in mid])
            z = sf.ifft(sf.ifftshift(B, axes=1), axis=1) * E; S2 = sf.fftshift(sf.fft(z, axis=1), axes=1)[:, c - 64:c + 65]
            u = S2 / np.maximum(np.abs(S2), 1e-30); n = u.shape[1] - 2 * D
            d3 = np.abs(np.mean(u[:, :n] * u[:, 2 * D:2 * D + n] * np.conj(u[:, D:D + n]) ** 2, axis=1))
            P = np.abs(S2) ** 2; pw = P[:, 64] / np.maximum(P.mean(axis=1), 1e-30)
            accD[fi, b] += d3; accP[fi, b] += pw; frD[fi, j] = d3[comet]; frP[fi, j] = pw[comet]
        if j % 200 == 0: print(s, j, round(time.time() - T00), flush=True)
    assert nb.sum() == NF
    np.savez_compressed(os.path.join(HERE, f"hm5_{s}.npz"), D3=accD.astype(np.float64), P=accP, nb=nb, frD=frD, frP=frP, comet=np.array(comet))
    json.dump({"scan": s, "windows": [list(x) for x in WIN], "nbins": NB, "bin_frames": BIN, "seconds": round(time.time() - T00)}, open(os.path.join(HERE, f"hm5_{s}.json"), "w"))
    print(s, "done", nw, round(time.time() - T00), flush=True)


def score():
    from common import TF, dm
    R = {s: np.load(os.path.join(HERE, f"hm5_{s}.npz")) for s in (ON_S, OFF_S)}; WIN = json.load(open(os.path.join(HERE, f"hm5_{ON_S}.json")))["windows"]
    idx = {w[0]: i for i, w in enumerate(WIN)}; sb = {}
    for n, k, f, dv, c in WIN:
        if k.startswith("sb:"): sb.setdefault(k[3:], []).append(n)
    excl = [n for n, k, f, dv, c in WIN if k == "sel" and len(sb.get(n, [])) < MINSB]
    sel = [(n, c, f) for n, k, f, dv, c in WIN if k == "sel" and n not in excl]
    NB = R[ON_S]["D3"].shape[1]
    def series(st, fi, s, part):
        A = R[s][st][fi]; nb = R[s]["nb"]
        return A.sum(0) / nb.sum() if part == "full" else A[part] / nb[part]
    sbi = {n: np.array([idx[m] for m in sb[n]]) for n, c, f in sel}; ii = {n: idx[n] for n, c, f in sel}
    def ranks(st, fi, s, part):
        v = series(st, fi, s, part)
        return {n: (np.sum(v[sbi[n]] < v[ii[n]]) + 0.5 * np.sum(v[sbi[n]] == v[ii[n]])) / len(sbi[n]) for n, c, f in sel}
    def cohort(st, fi, part):
        ron, roff = ranks(st, fi, ON_S, part), ranks(st, fi, OFF_S, part); coh = {}
        for n, c, f in sel: coh.setdefault(c, []).append(ron[n] - roff[n])
        sc = {c: float(np.mean(v) * np.sqrt(len(v))) for c, v in coh.items()}; T = sc["true"]; Fs = np.array([v for c, v in sc.items() if c != "true"])
        tn = [n for n, c, f in sel if c == "true"]
        return {"true": T, "rank": int(1 + np.sum(Fs > T)), "n_false": len(Fs), "false_p95": float(np.percentile(Fs, 95)), "false_mean": float(Fs.mean()),
                "on_mean_rank": float(np.mean([ron[n] for n in tn])), "off_mean_rank": float(np.mean([roff[n] for n in tn])),
                "per_coordinate": {n: round(float(ron[n] - roff[n]), 4) for n in tn}}
    out = {"min_sidebands": MINSB, "excluded": excl, "nbins": NB}
    H4 = json.load(open(os.path.join(HERE, "../HM4/hm4_score.json")))["pairs_X"]["0013-0014"]["full"]["cohort"]["true"]
    out["reproduction"] = {"hm5": cohort("D3", 0, "full")["true"], "hm4_pair_0013_0014": H4}; out["reproduction_ok"] = bool(abs(out["reproduction"]["hm5"] - H4) < 1e-9)
    print("reproduction", out["reproduction"], out["reproduction_ok"], flush=True)
    t0 = {s: 61027 + int(dm.SCANS[s][0]) / 86400.0 for s in (ON_S, OFF_S)}
    def utc(mjd):
        sec = (mjd - 61027) * 86400; return f"2025-12-18T{int(sec // 3600):02d}:{int(sec % 3600 // 60):02d}:{sec % 60:05.2f}Z"
    nbON = R[ON_S]["nb"]; edges = np.concatenate([[0], np.cumsum(nbON)]).astype(int)
    out["bins"] = [{"b": b, "frames": [int(edges[b]), int(edges[b + 1] - 1)], "on_utc": utc(t0[ON_S] + edges[b] * TF / 86400), "off_utc": utc(t0[OFF_S] + edges[b] * TF / 86400)} for b in range(NB)]
    out["full"] = {f"{st}_{fd}": cohort(st, fi, "full") for st in ("D3", "P") for fi, fd in enumerate(FEEDS)}
    out["time"] = {f"{st}_{fd}": [cohort(st, fi, b) for b in range(NB)] for st in ("D3", "P") for fi, fd in enumerate(FEEDS)}
    # the episode rule (PLAN §4): the best run of at most three contiguous bins against the positive total
    S = np.array([x["true"] for x in out["time"]["D3_X"]]); Ptot = float(np.sum(np.maximum(S, 0))); best = (-1e9, None)
    for L in (1, 2, 3):
        for b in range(NB - L + 1):
            v = float(S[b:b + L].sum());
            if v > best[0]: best = (v, (b, b + L - 1))
    ep = {"positive_total": Ptot, "best_run_sum": best[0], "best_run_bins": list(best[1]), "fraction": (best[0] / Ptot if Ptot > 0 else None)}
    ep["episode"] = bool(Ptot > 0 and best[0] >= 0.5 * Ptot); b0, b1 = best[1]
    ep["run"] = {k: [out["time"][k][b] | {"b": b} for b in range(b0, b1 + 1)] for k in out["time"]}
    ep["on_utc"] = [out["bins"][b0]["on_utc"], out["bins"][b1]["on_utc"]]; out["episode"] = ep
    tn = [n for n, c, f in sel if c == "true"]; ci = list(R[ON_S]["comet"])
    out["coords"] = {n: WIN[idx[n]][2] for n in tn}
    json.dump(out, open(os.path.join(HERE, "hm5_score.json"), "w"), indent=1)
    for k, v in out["full"].items(): print("full", k, round(v["true"], 3), v["rank"], "on", round(v["on_mean_rank"], 3), "off", round(v["off_mean_rank"], 3))
    for b in range(NB): print("bin", b, out["bins"][b]["on_utc"][11:19], " ".join(f"{k} {out['time'][k][b]['true']:+.2f}({out['time'][k][b]['rank']})" for k in out["time"]))
    print("episode", {k: v for k, v in ep.items() if k != "run"})
    print("per-coordinate D3_X", out["full"]["D3_X"]["per_coordinate"]); print("per-coordinate P_X", out["full"]["P_X"]["per_coordinate"])


if __name__ == "__main__":
    a = sys.argv[1]
    score() if a == "score" else scan(a)
