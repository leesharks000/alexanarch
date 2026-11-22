"""PLAN-HM4: python3 hm4.py SCAN | score   (tracking X: time map, feed basis, power; windows and selections from HM2, unchanged)"""
import json, os, sys, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(HERE, "../FD")); sys.path.insert(0, os.path.join(HERE, "../HM"))
MINSB = 6; D = 2; HALF = 417; NSEG = 8
COMBOS = ["X", "P+", "P-"]            # X; (X+Y)/sqrt2; (X-Y)/sqrt2  (linear in the voltages, so formed on the spectra)
G = ["C07", "C08", "C09", "C10", "C11"]; LO, HI = 1667.0e6, 1668.0e6
PAIRS = [("0013", "0014"), ("0015", "0016"), ("0017", "0018")]


def windows():
    import hm
    real = hm.HERE; hm.HERE = HERE
    src = os.path.join(HERE, "hm_selections.json")
    if not os.path.exists(src): os.symlink("hm4_selections.json", src)
    W = hm.hm_windows(); hm.HERE = real
    return W


def scan(s):
    import fdstream as F
    from common import N, DF, FC, NF, TF, W as WW, dm
    WIN = [w for w in windows() if w[1] != "ref"]  # as HM2 Amendment 1
    T0 = json.load(open(os.path.join(HERE, "hm4_selections.json")))["T0_mjd"]; c = WW // 2; SR = WW * DF
    ifl = np.array([F.track_f(s, f, dv, T0) for _, _, f, dv, _ in WIN]); mid = np.rint(np.median(np.rint(ifl), axis=1)).astype(int)
    off_f = (ifl - mid[:, None]) * DF; nw = len(WIN); assert mid.min() > WW and mid.max() < N - WW
    tc = (np.arange(NF) + 0.5) * TF; carry = np.zeros(nw); acc = np.zeros((len(COMBOS), NSEG, nw)); pw = np.zeros((NSEG, nw)); nseg = np.zeros(NSEG)
    r2 = 1 / np.sqrt(2); T00 = time.time()
    for j, X, Y in dm.frames(s, NF):
        g = j * NSEG // NF; nseg[g] += 1
        ts = (j * WW + np.arange(WW)) / SR
        a = np.clip(np.searchsorted(tc, ts) - 1, 0, NF - 2); w = np.clip((ts - tc[a]) / TF, 0.0, 1.0)
        off = off_f[:, a] * (1 - w)[None, :] + off_f[:, a + 1] * w[None, :]
        Phi = carry[:, None] + 2 * np.pi * np.cumsum(off, axis=1) / SR; carry = Phi[:, -1].copy(); E = np.exp(-1j * Phi)
        Fx = dm.fft(X); Fy = dm.fft(Y)
        for ci, Fc in enumerate((Fx, (Fx + Fy) * r2, (Fx - Fy) * r2)):
            B = np.stack([Fc[m - c:m + c] for m in mid])
            z = sf.ifft(sf.ifftshift(B, axes=1), axis=1) * E; S2 = sf.fftshift(sf.fft(z, axis=1), axes=1)[:, c - 64:c + 65]
            u = S2 / np.maximum(np.abs(S2), 1e-30); n = u.shape[1] - 2 * D
            acc[ci, g] += np.abs(np.mean(u[:, :n] * u[:, 2 * D:2 * D + n] * np.conj(u[:, D:D + n]) ** 2, axis=1))
            if ci == 0:
                P = np.abs(S2) ** 2; pw[g] += P[:, 64] / np.maximum(P.mean(axis=1), 1e-30)
        if j % 200 == 0: print(s, j, round(time.time() - T00), flush=True)
    assert nseg[:4].sum() == HALF and nseg.sum() == NF
    out = {"scan": s, "windows": [list(x) for x in WIN], "nseg": nseg.tolist(), "seconds": None}
    for ci, k in enumerate(COMBOS): out[k] = acc[ci].tolist()
    out["powerX"] = pw.tolist(); out["seconds"] = round(time.time() - T00)
    json.dump(out, open(os.path.join(HERE, f"hm4_{s}.json"), "w"))
    print(s, "done", nw, out["seconds"], flush=True)


def parts(seg, nseg):
    """sums per segment -> mean over frames for full, h1, h2, s0..s7"""
    seg = np.asarray(seg); ns = np.asarray(nseg)[:, None]
    P = {"full": seg.sum(0) / ns.sum(), "h1": seg[:4].sum(0) / ns[:4].sum(), "h2": seg[4:].sum(0) / ns[4:].sum()}
    for g in range(NSEG): P[f"s{g}"] = seg[g] / ns[g, 0]
    return P


def score():
    from common import SCANS, ON
    R = {s: json.load(open(os.path.join(HERE, f"hm4_{s}.json"))) for s in SCANS}; WIN = R["0013"]["windows"]
    idx = {w[0]: i for i, w in enumerate(WIN)}; sb = {}
    for n, k, f, dv, c in WIN:
        if k.startswith("sb:"): sb.setdefault(k[3:], []).append(n)
    excl = [n for n, k, f, dv, c in WIN if k == "sel" and len(sb.get(n, [])) < MINSB]
    sel = [(n, c) for n, k, f, dv, c in WIN if k == "sel" and n not in excl]
    pool = [n for n, k, f, dv, c in WIN if k == "sel" and c != "true" and n not in excl and LO <= f < HI]
    stats = list(COMBOS) + ["powerX"]
    V = {st: {s: parts(R[s][st], R[s]["nseg"]) for s in SCANS} for st in stats}
    PARTS = ["full", "h1", "h2"] + [f"s{g}" for g in range(NSEG)]

    def rank(st, s, part, n):
        x = V[st][s][part][idx[n]]; v = np.array([V[st][s][part][idx[m]] for m in sb[n]])
        return (np.sum(v < x) + 0.5 * np.sum(v == x)) / len(v)

    def con(st, part, n, pair=None):
        if pair: return rank(st, pair[0], part, n) - rank(st, pair[1], part, n)
        return np.mean([rank(st, s, part, n) for s in SCANS if s in ON]) - np.mean([rank(st, s, part, n) for s in SCANS if s not in ON])

    def cohort(st, part, pair=None):
        coh = {}
        for n, c in sel: coh.setdefault(c, []).append(con(st, part, n, pair))
        sc = {c: float(np.mean(v) * np.sqrt(len(v))) for c, v in coh.items()}
        T = sc["true"]; Fs = np.array([v for c, v in sc.items() if c != "true"])
        return {"true": T, "rank": int(1 + np.sum(Fs > T)), "n_false": len(Fs), "p": float((1 + np.sum(Fs >= T)) / (1 + len(Fs))),
                "false_p95": float(np.percentile(Fs, 95)), "false_mean": float(Fs.mean())}, sc

    def g1667(st, part, pair=None):
        rng = np.random.default_rng(20261121)
        Tg = float(np.mean([con(st, part, n, pair) for n in G]) * np.sqrt(len(G))); pc = {n: con(st, part, n, pair) for n in pool}
        dr = np.array([np.mean([pc[n] for n in rng.choice(pool, len(G), replace=False)]) * np.sqrt(len(G)) for _ in range(10000)])
        return {"G1667": Tg, "p": float((1 + np.sum(dr >= Tg)) / 10001), "null_p95": float(np.percentile(dr, 95)), "null_mean": float(dr.mean())}

    out = {"min_sidebands": MINSB, "excluded": excl, "pool": len(pool)}
    # A. reproduction of HM2 (X, full/h1/h2) — must match hm2_score.json
    H2 = json.load(open(os.path.join(HERE, "../HM2/hm2_score.json")))
    out["reproduction"] = {p: {"hm4": cohort("X", p)[0]["true"], "hm2": H2[p]["true"]} for p in ("full", "h1", "h2")}
    out["reproduction_ok"] = bool(all(abs(v["hm4"] - v["hm2"]) < 1e-9 for v in out["reproduction"].values()))
    print("reproduction", out["reproduction"], out["reproduction_ok"], flush=True)
    # B. time map in X: segments and scan pairs
    out["time_X"] = {p: {"cohort": cohort("X", p)[0], "G1667": g1667("X", p)} for p in PARTS}
    out["pairs_X"] = {f"{a}-{b}": {p: {"cohort": cohort("X", p, (a, b))[0], "G1667": g1667("X", p, (a, b))} for p in ("full", "h1", "h2")} for a, b in PAIRS}
    # C. feed basis: P+ and P-, and the asymmetry P+ minus P-
    out["basis"] = {}
    for p in ("full", "h1", "h2"):
        cp, sp = cohort("P+", p); cm, sm = cohort("P-", p)
        Af = np.array([sp[c] - sm[c] for c in sp if c != "true"]); At = sp["true"] - sm["true"]
        gp, gm = g1667("P+", p), g1667("P-", p)
        rng = np.random.default_rng(20261121); pcp = {n: con("P+", p, n) for n in pool}; pcm = {n: con("P-", p, n) for n in pool}
        dA = []
        for _ in range(10000):
            ch = rng.choice(pool, len(G), replace=False); dA.append((np.mean([pcp[n] for n in ch]) - np.mean([pcm[n] for n in ch])) * np.sqrt(len(G)))
        dA = np.abs(np.array(dA)); AG = gp["G1667"] - gm["G1667"]
        out["basis"][p] = {"cohort_P+": cp, "cohort_P-": cm, "cohort_asym": float(At), "cohort_asym_p_two_sided": float((1 + np.sum(np.abs(Af) >= abs(At))) / (1 + len(Af))),
                           "G1667_P+": gp, "G1667_P-": gm, "G1667_asym": float(AG), "G1667_asym_p_two_sided": float((1 + np.sum(dA >= abs(AG))) / 10001),
                           "G1667_asym_null_abs_p95": float(np.percentile(dA, 95))}
        print("basis", p, {k: v for k, v in out["basis"][p].items() if "asym" in k}, flush=True)
    # D. power in X at the track centre
    out["power_X"] = {p: {"cohort": cohort("powerX", p)[0], "G1667": g1667("powerX", p)} for p in ("full", "h1", "h2")}
    json.dump(out, open(os.path.join(HERE, "hm4_score.json"), "w"), indent=1)
    for p in PARTS: print("time", p, round(out["time_X"][p]["cohort"]["true"], 3), out["time_X"][p]["cohort"]["rank"], "| G1667", round(out["time_X"][p]["G1667"]["G1667"], 3), round(out["time_X"][p]["G1667"]["p"], 4))
    for k, v in out["pairs_X"].items(): print("pair", k, {p: (round(v[p]["cohort"]["true"], 3), v[p]["cohort"]["rank"], round(v[p]["G1667"]["G1667"], 3)) for p in v})
    for p, v in out["power_X"].items(): print("power", p, round(v["cohort"]["true"], 3), v["cohort"]["rank"], round(v["G1667"]["G1667"], 3), round(v["G1667"]["p"], 4))


if __name__ == "__main__":
    a = sys.argv[1]
    score() if a == "score" else scan(a)
