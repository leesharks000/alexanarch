"""PLAN-P1547.  python3 p1547.py synth      -> synth.json
             python3 p1547.py SCAN       -> p_SCAN.json  (SCAN in 0013..0018)
             python3 p1547.py read       -> the gates, from the six p_SCAN.json"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../../voltages/delaymod")); import dm
dm.CH = 48; dm.FC = 1595.21484375e6 + 93.75e6 - 48.5 * 2.9296875e6
N, DF, FC = dm.N, dm.DF, dm.FC
F0, W, NFR, NSUR, SEG = 1547.72e6, 65536, 16, 19, 512
LAGS = [2, 4, 8, 16, 32, 64, 128, 256, 512]
B = int(np.rint(N // 2 + (FC - F0) / DF - 0.5)); SL = slice(B - W // 2, B + W // 2)
SCANS = ["0013", "0014", "0015", "0016", "0017", "0018"]


def quartets():
    r = np.random.default_rng(20261120); out = []; seen = set()
    while len(out) < 128:
        k, l, m = (int(x) for x in r.integers(1, SEG, 3)); n = k + l - m
        if not (1 <= n < SEG) or sorted((k, l)) == sorted((m, n)): continue
        key = (tuple(sorted((k, l))), tuple(sorted((m, n))))
        if key in seen: continue
        seen.add(key); out.append((k, l, m, n))
    return np.array(out)
QT = quartets()


def white(Fs):
    a = np.abs(Fs); a[a == 0] = 1
    return np.fft.ifft(np.fft.ifftshift(Fs / a))


class Acc:
    """Accumulates both filters over frames for one series stream."""
    def __init__(s): s.a = np.zeros(len(LAGS), complex); s.na = np.zeros(len(LAGS)); s.q = np.zeros(len(QT), complex); s.nq = 0
    def add(s, z):
        d = z[1:] * np.conj(z[:-1]); d /= np.maximum(np.abs(d), 1e-30)
        for i, L in enumerate(LAGS):
            s.a[i] += np.sum(d[L:] * np.conj(d[:-L])); s.na[i] += len(d) - L
        P = np.fft.fft(z.reshape(-1, SEG), axis=1); P = P / np.maximum(np.abs(P), 1e-30)
        k, l, m, n = QT.T
        s.q += np.sum(P[:, k] * P[:, l] * np.conj(P[:, m]) * np.conj(P[:, n]), axis=0); s.nq += P.shape[0]
    def out(s): return np.abs(s.a) / s.na, np.abs(s.q) / s.nq


def run(slices, seed0, post=None):
    """slices: iterable of per-frame cropped spectra (W,) for one feed. Returns real and surrogate statistics.
    post (validation only): a function of z giving the series after an injection made after whitening."""
    R = Acc(); S = [Acc() for _ in range(NSUR)]; rngs = [np.random.default_rng(seed0 + k) for k in range(NSUR)]
    for Fs in slices:
        R.add(white(Fs) if post is None else post(white(Fs)))
        for k in range(NSUR):
            S[k].add(white(np.exp(2j * np.pi * rngs[k].random(W))))
    ra, rq = R.out(); sa = np.array([x.out()[0] for x in S]); sq = np.array([x.out()[1] for x in S])
    return dict(A=ra.tolist(), Q=rq.tolist(), sA=sa.tolist(), sQ=sq.tolist())


def fam(r):
    o = {}
    for f in ("A", "Q"):
        real = np.array(r[f]); sur = np.array(r["s" + f]); mx = sur.max(1)
        o[f] = dict(score=float(real.max()), arg=int(real.argmax()), p=(1 + int((mx >= real.max()).sum())) / (NSUR + 1),
                    sur_max_median=float(np.median(mx)))
    return o


def synth():
    """Validation (amended before any data, PLAN-P1547 amendment 1). Slice-rate signals, 16 frames of W samples:
    pre: injected before whitening, as a signal would arrive (amplitudes 0.25, 0.5, 1 of the noise rms);
    post: injected after whitening at the whitened series' rms (ChatGPT's capability check)."""
    rng = np.random.default_rng(7); out = {}; t = np.arange(W)
    code = np.exp(1j * np.pi / 2 * rng.integers(0, 4, 64)); qpsk = np.tile(np.repeat(code, 2), W // 128)
    k, l, m, n = QT[0]; ph = rng.random(3) * 2 * np.pi; ph = list(ph) + [ph[0] + ph[1] - ph[2]]
    tones = sum(np.exp(1j * (2 * np.pi * f_ * t / SEG + p_)) for f_, p_ in zip((k, l, m, n), ph)) / 2
    sig = {"qpsk": qpsk, "closure": tones}
    def noise(): return (rng.normal(size=W) + 1j * rng.normal(size=W)) / np.sqrt(2)
    cases = [("noise", None, 0, "pre")] + [(c, c, a, "pre") for c in sig for a in (0.25, 0.5, 1.0)] + [(c, c, 1.0, "post") for c in sig]
    for name, c, a, stage in cases:
        sl = [np.fft.fftshift(np.fft.fft(noise() + (a * sig[c] if (c and stage == "pre") else 0))) for _ in range(NFR)]
        post = (lambda z, c=c: z + sig[c] * np.sqrt(np.mean(np.abs(z) ** 2))) if stage == "post" else None
        r = run(sl, 990000 + len(out) * 100, post); r["family"] = fam(r); key = f"{name}-{stage}-{a}"; out[key] = r
        fa, fq = r["family"]["A"], r["family"]["Q"]
        print(f"{key:20s} A p {fa['p']:.2f} score/surmax {fa['score'] / fa['sur_max_median']:6.2f} lag {LAGS[fa['arg']]:4d} | Q p {fq['p']:.2f} score/surmax {fq['score'] / fq['sur_max_median']:6.2f} q {fq['arg']}", flush=True)
    json.dump(out, open(os.path.join(HERE, "synth.json"), "w"))


def scan(s):
    i = SCANS.index(s); T0 = time.time(); X, Y = [], []
    for j, x, y in dm.frames(s, NFR):
        X.append(dm.fft(x)[SL].astype(np.complex128)); Y.append(dm.fft(y)[SL].astype(np.complex128))
    print(s, "fetched", len(X), round(time.time() - T0), flush=True)
    out = {"scan": s, "role": dm.SCANS[s][2], "bin_centre": B, "frames": len(X)}
    for q, sl in enumerate((X, Y)):
        r = run(sl, 1547000 + 100 * i + 10 * q); r["family"] = fam(r); out["XY"[q]] = r
        print(s, "XY"[q], json.dumps(r["family"]), flush=True)
    json.dump(out, open(os.path.join(HERE, f"p_{s}.json"), "w"))


def read():
    P = {s: json.load(open(os.path.join(HERE, f"p_{s}.json"))) for s in SCANS}
    rows = []
    for s in SCANS:
        for q in "XY":
            fm = P[s][q]["family"]
            rows.append((s, P[s]["role"], q, fm["A"]["p"], LAGS[fm["A"]["arg"]], round(fm["A"]["score"] * 1e4, 3), round(fm["A"]["sur_max_median"] * 1e4, 3),
                         fm["Q"]["p"], fm["Q"]["arg"], round(fm["Q"]["score"], 4), round(fm["Q"]["sur_max_median"], 4)))
    print("scan role feed | A: p lag score·1e4 surmax·1e4 | Q: p quartet score surmax")
    for r in rows: print(*r)
    def above(s, q, f, a):
        return float(np.array(P[s][q][f])[a]) > float(np.array(P[s][q]["s" + f])[:, a].max())
    print("\nGates (candidate in ON0015, confirmation in ON0017, controls OFF0014/16/18):")
    for q in "XY":
        for f in ("A", "Q"):
            fm = P["0015"][q]["family"][f]
            if fm["p"] > 0.05: print(f, q, "no candidate in ON0015 (p", fm["p"], ")"); continue
            a = fm["arg"]; conf = above("0017", q, f, a); offs = {o: above(o, q, f, a) for o in ("0014", "0016", "0018")}
            print(f, q, "candidate at", LAGS[a] if f == "A" else QT[a].tolist(), "| ON0017 above surrogates:", conf, "| OFF above:", offs,
                  "| LEAD" if conf and not any(offs.values()) else "| not a lead")


if __name__ == "__main__":
    a = sys.argv[1]
    synth() if a == "synth" else read() if a == "read" else scan(a)
