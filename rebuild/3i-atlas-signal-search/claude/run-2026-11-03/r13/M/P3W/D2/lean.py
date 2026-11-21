"""PLAN-P3W-D2 amendment 1: P3W-D's run, at_pair and half_p, computed block-wise in single precision so a full-length scan fits in memory.
Same segments, phasors, masks, families, window W, offsets drawn in the same order from the same seeds, same p. Checked against p3wd's
32-frame results (check_lean.json) before any full-length result was computed.  python3 lean.py check | SCAN | read"""
import json, os, sys, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import p3w as P, p3wd as D
SEG, W, BLK = P.SEG, D.W, 8192


def phasors_c64(z_iter):
    """z_iter yields complex chunks whose lengths are multiples of SEG -> (unit phasors complex64 (S, SEG), mean power per bin)."""
    out = []; pw = np.zeros(SEG); S = 0
    for z in z_iter:
        X = sf.fft(np.asarray(z, np.complex64).reshape(-1, SEG), axis=1); A = np.abs(X).astype(np.float64)
        pw += (A ** 2).sum(0); S += len(X); out.append((X / np.maximum(A, 1e-30)).astype(np.complex64))
    return np.concatenate(out), pw / S


def fam_products(A, B):
    """Accumulators for P.stats' six families from blocks A (X) and B (Y)."""
    return {"X+": A.T @ A, "X-": A.T @ A.conj(), "Y+": B.T @ B, "Y-": B.T @ B.conj(), "XY+": A.T @ B, "XY-": A.T @ B.conj()}


def stats_lean(PX, PY, LX=None, LY=None):
    """|mean over the S - W windowed segments| for the six families; offsets LX, LY per bin (None = real, offset 0)."""
    n = len(PX) - W; acc = {f: np.zeros((SEG, SEG), np.complex128) for f in P.FAMS}; cols = np.arange(SEG)
    for a in range(0, n, BLK):
        b = min(n, a + BLK); rows = np.arange(a, b)[:, None]
        A = PX[a:b] if LX is None else PX[rows + LX[None, :], cols[None, :]]
        B = PY[a:b] if LY is None else PY[rows + LY[None, :], cols[None, :]]
        for f, M in fam_products(A, B).items(): acc[f] += M
    return {f: np.abs(acc[f]) / n for f in P.FAMS}


def run_lean(PX, px, PY, py, seed):
    M = P.masks(px, py); R = stats_lean(PX, PY); rng = np.random.default_rng(seed)
    sur = {f: [] for f in P.FAMS}; surA = {f: [] for f in P.FAMS}
    best = {f: (float(R[f][M[f]].max()), np.unravel_index(np.argmax(np.where(M[f], R[f], -1)), R[f].shape)) for f in P.FAMS}
    for _ in range(P.NSUR):
        LX = rng.integers(0, W + 1, size=SEG); LY = rng.integers(0, W + 1, size=SEG)
        Q = stats_lean(PX, PY, LX, LY)
        for f in P.FAMS: sur[f].append(float(Q[f][M[f]].max())); surA[f].append(float(Q[f][best[f][1]]))
    out = {}
    for f in P.FAMS:
        v, (k, l) = best[f]
        out[f] = dict(score=v, pair=[int(k), int(l)], p=(1 + sum(x >= v for x in sur[f])) / (P.NSUR + 1),
                      sur_max_median=float(np.median(sur[f])), sur_at_pair_max=float(max(surA[f])), sur_at_pair_median=float(np.median(surA[f])))
    return out


def pair_val(a, b, f, conj):
    return float(np.abs(np.mean(a * (np.conj(b) if conj else b))))


FMAP = {"X+": ("X", "X", 0), "X-": ("X", "X", 1), "Y+": ("Y", "Y", 0), "Y-": ("Y", "Y", 1), "XY+": ("X", "Y", 0), "XY-": ("X", "Y", 1)}


def at_pair_lean(PX, PY, f, k, l, seed):
    """D.at_pair at one pair: only columns k and l are needed."""
    Pq = {"X": PX, "Y": PY}; a, b, cj = FMAP[f]; n = len(PX) - W
    A = pair_val(Pq[a][:n, k], Pq[b][:n, l], f, cj); rng = np.random.default_rng(seed); sa = []
    for _ in range(P.NSUR):
        LX = rng.integers(0, W + 1, size=SEG); LY = rng.integers(0, W + 1, size=SEG); L = {"X": LX, "Y": LY}
        sa.append(pair_val(Pq[a][L[a][k]:L[a][k] + n, k], Pq[b][L[b][l]:L[b][l] + n, l], f, cj))
    return dict(A=A, sur_max=float(max(sa)), sur_median=float(np.median(sa)))


def half_p_lean(zx_chunks, zy_chunks, f, k, l, nseg_total):
    """P.half_p: each half of the series, phasors recomputed on the half, analytic p = exp(-S A^2)."""
    PX, _ = phasors_c64(zx_chunks()); PY, _ = phasors_c64(zy_chunks()); h = len(PX) // 2; out = []
    Pq = {"X": PX, "Y": PY}; a, b, cj = FMAP[f]
    for s0, s1 in ((0, h), (h, 2 * h)):
        A = pair_val(Pq[a][s0:s1, k], Pq[b][s0:s1, l], f, cj); out.append(dict(A=A, p=float(np.exp(-(s1 - s0) * A * A))))
    return out


# ---- data -------------------------------------------------------------------------------------------
def chunks_full(s, q, nchunk=64):
    a = np.load(os.path.join(HERE, f"ser_{s}.npy"), mmap_mode="r")[q]; n = (len(a) // SEG) * SEG; step = (n // nchunk // SEG) * SEG
    for i in range(0, n, step):
        x = a[i:min(n, i + step)]; yield x[:, 0].astype(np.float32) + 1j * x[:, 1].astype(np.float32)


def load_full(s):
    PX, px = phasors_c64(chunks_full(s, 0)); PY, py = phasors_c64(chunks_full(s, 1)); return PX, px, PY, py


def check():
    """Lean against p3wd on the 32-frame crops of scan 0013 (P3W-D's own result, p3wd_0013.json)."""
    d = np.load(os.path.join(P.N1625, "crops_0013.npz")); zx, zy = P.series(d, "target_X"), P.series(d, "target_Y")
    PX, px = phasors_c64([zx[:len(zx) // SEG * SEG]]); PY, py = phasors_c64([zy[:len(zy) // SEG * SEG]])
    r = run_lean(PX, px, PY, py, 31625 + 100 * 0 + 10 * 0); ref = json.load(open(os.path.join(HERE, "..", "p3wd_0013.json")))["target"]
    rep = {f: {"lean": r[f], "p3wd": ref[f]} for f in P.FAMS}
    ok = all(r[f]["pair"] == ref[f]["pair"] and abs(r[f]["score"] - ref[f]["score"]) < 1e-4 and r[f]["p"] == ref[f]["p"] for f in P.FAMS)
    rep["equivalent"] = bool(ok); json.dump(rep, open(os.path.join(HERE, "check_lean.json"), "w"), indent=1)
    for f in P.FAMS: print(f, r[f]["pair"], ref[f]["pair"], round(r[f]["score"], 6), round(ref[f]["score"], 6), r[f]["p"], ref[f]["p"])
    print("EQUIVALENT" if ok else "NOT EQUIVALENT")


def scan(s):
    T0 = time.time(); i = P.SCANS.index(s); PX, px, PY, py = load_full(s)
    r = run_lean(PX, px, PY, py, 31625 + 100 * i)
    n = len(PX) - W; A = pair_val(PY[:n, 217], PY[:n, 293], "Y+", 0)
    out = {"scan": s, "segments": len(PX), "target": r, "followup_Yplus_217_293": A, "seconds": round(time.time() - T0)}
    print(s, {f: (r[f]["p"], r[f]["pair"], round(r[f]["score"] / r[f]["sur_max_median"], 2)) for f in P.FAMS}, "Y+[217,293]", round(A, 5), round(time.time() - T0), flush=True)
    json.dump(out, open(os.path.join(HERE, f"p3wd2_{s}.json"), "w"), indent=1)


def read():
    R = {s: json.load(open(os.path.join(HERE, f"p3wd2_{s}.json"))) for s in P.SCANS}; gates = {}
    for s in ("0013", "0015", "0017"):
        for f in P.FAMS:
            r = R[s]["target"][f]
            if r["p"] > 0.05: continue
            k, l = r["pair"]
            g = {"scan": s, "family": f, "pair": [k, l], "p": r["p"], "halves": half_p_lean(lambda: chunks_full(s, 0), lambda: chunks_full(s, 1), f, k, l, None)}
            i = P.SCANS.index(s); offs = [P.SCANS[i - 1]] + ([P.SCANS[i + 1]] if i + 1 < 6 else []); g["off"] = {}
            for o in offs:
                PX, _, PY, _ = load_full(o); g["off"][o] = at_pair_lean(PX, PY, f, k, l, 555); del PX, PY
            d = np.load(os.path.join(P.N1625, f"crops_{s}.npz"))
            g["ctrl"] = {sl: D.at_pair(P.series(d, f"{sl}_X"), P.series(d, f"{sl}_Y"), f, k, l, 556) for sl in ("ctrl25k", "hidrift")}
            exc = r["score"] - r["sur_at_pair_median"]; oexc = max(v["A"] - v["sur_median"] for v in g["off"].values())
            g["verdict"] = dict(halves=all(h["p"] <= 0.01 for h in g["halves"]), off_not_above=all(v["A"] <= v["sur_max"] for v in g["off"].values()),
                                excess_ratio=(exc / oexc) if oexc > 0 else None, controls_quiet=all(v["A"] <= v["sur_max"] for v in g["ctrl"].values()))
            v = g["verdict"]; g["lead"] = bool(v["halves"] and v["off_not_above"] and (v["excess_ratio"] is None or v["excess_ratio"] >= 4) and v["controls_quiet"])
            gates[f"{s}{f}"] = g; print(json.dumps(g)[:900], flush=True)
    n = sum(1 for s in P.SCANS for f in P.FAMS if R[s]["target"][f]["p"] <= 0.05)
    print("families at p<=0.05 across 36 (6 scans x 6):", n, "| expected about 1.8")
    print("follow-up Y+[217,293]:", {s: round(R[s]["followup_Yplus_217_293"], 5) for s in P.SCANS})
    json.dump(gates, open(os.path.join(HERE, "p3wd2_gates.json"), "w"), indent=1)


if __name__ == "__main__":
    a = sys.argv[1]
    check() if a == "check" else read() if a == "read" else scan(a)
