"""PLAN-P1547B: P1547 with the lines kept (smoothed-magnitude normalization, magnitude-preserving surrogates).
python3 p1547b.py synth | SCAN | read   -> synthB.json, pb_SCAN.json"""
import json, os, sys, time
import numpy as np
from scipy.ndimage import median_filter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p1547 as P
dm, W, NFR, NSUR, LAGS, QT, SCANS, SL = P.dm, P.W, P.NFR, P.NSUR, P.LAGS, P.QT, P.SCANS, P.SL
MED = 1025


def norm(Fs):
    m = median_filter(np.abs(Fs), size=MED, mode="reflect"); m[m == 0] = 1
    return Fs / m


def series(G): return np.fft.ifft(np.fft.ifftshift(G))


def run(slices, seed0):
    R = P.Acc(); S = [P.Acc() for _ in range(NSUR)]; rngs = [np.random.default_rng(seed0 + k) for k in range(NSUR)]
    for Fs in slices:
        G = norm(Fs); a = np.abs(G); R.add(series(G))
        for k in range(NSUR):
            S[k].add(series(a * np.exp(2j * np.pi * rngs[k].random(W))))
    ra, rq = R.out(); sa = np.array([x.out()[0] for x in S]); sq = np.array([x.out()[1] for x in S])
    return dict(A=ra.tolist(), Q=rq.tolist(), sA=sa.tolist(), sQ=sq.tolist())


def synth():
    rng = np.random.default_rng(7); out = {}; t = np.arange(W)
    code = np.exp(1j * np.pi / 2 * rng.integers(0, 4, 64)); qpsk = np.tile(np.repeat(code, 2), W // 128)
    k, l, m, n = QT[0]; ph = rng.random(3) * 2 * np.pi; ph = list(ph) + [ph[0] + ph[1] - ph[2]]
    tones = sum(np.exp(1j * (2 * np.pi * f_ * t / P.SEG + p_)) for f_, p_ in zip((k, l, m, n), ph)) / 2
    sig = {"qpsk": qpsk, "closure": tones}
    def noise(): return (rng.normal(size=W) + 1j * rng.normal(size=W)) / np.sqrt(2)
    cases = [("noise", None, 0)] + [(c, c, a) for c in sig for a in (0.1, 0.25, 0.5, 1.0)]
    for name, c, a in cases:
        sl = [np.fft.fftshift(np.fft.fft(noise() + (a * sig[c] if c else 0))) for _ in range(NFR)]
        r = run(sl, 990000 + len(out) * 100); r["family"] = P.fam(r); key = f"{name}-{a}"; out[key] = r
        fa, fq = r["family"]["A"], r["family"]["Q"]
        print(f"{key:14s} A p {fa['p']:.2f} score/surmax {fa['score'] / fa['sur_max_median']:7.2f} lag {LAGS[fa['arg']]:4d} | Q p {fq['p']:.2f} score/surmax {fq['score'] / fq['sur_max_median']:7.2f} q {fq['arg']}", flush=True)
    json.dump(out, open(os.path.join(HERE, "synthB.json"), "w"))


def scan(s):
    i = SCANS.index(s); T0 = time.time(); X, Y = [], []
    for j, x, y in dm.frames(s, NFR):
        X.append(dm.fft(x)[SL].astype(np.complex128)); Y.append(dm.fft(y)[SL].astype(np.complex128))
    print(s, "fetched", len(X), round(time.time() - T0), flush=True)
    out = {"scan": s, "role": dm.SCANS[s][2], "bin_centre": P.B, "frames": len(X)}
    for q, sl in enumerate((X, Y)):
        r = run(sl, 1547000 + 100 * i + 10 * q); r["family"] = P.fam(r); out["XY"[q]] = r
        print(s, "XY"[q], json.dumps(r["family"]), flush=True)
    json.dump(out, open(os.path.join(HERE, f"pb_{s}.json"), "w"))


def read():
    Pq = {s: json.load(open(os.path.join(HERE, f"pb_{s}.json"))) for s in SCANS}
    print("scan role feed | A: p lag score/surmax | Q: p quartet score/surmax")
    for s in SCANS:
        for q in "XY":
            fm = Pq[s][q]["family"]; a, b = fm["A"], fm["Q"]
            print(s, Pq[s]["role"], q, "|", a["p"], LAGS[a["arg"]], round(a["score"] / a["sur_max_median"], 2), "|", b["p"], b["arg"], round(b["score"] / b["sur_max_median"], 2))
    def above(s, q, f, a): return float(np.array(Pq[s][q][f])[a]) > float(np.array(Pq[s][q]["s" + f])[:, a].max())
    def ratio(s, q, f, a): return float(np.array(Pq[s][q][f])[a]) / float(np.median(np.array(Pq[s][q]["s" + f])[:, a]))
    print("\nGates:")
    for q in "XY":
        for f in ("A", "Q"):
            fm = Pq["0015"][q]["family"][f]
            if fm["p"] > 0.05: print(f, q, "no candidate in ON0015 (p", fm["p"], ")"); continue
            a = fm["arg"]; conf = above("0017", q, f, a); offs = {o: above(o, q, f, a) for o in ("0014", "0016", "0018")}
            rs = {o: round(ratio(o, q, f, a), 2) for o in SCANS}
            print(f, q, "candidate at", LAGS[a] if f == "A" else QT[a].tolist(), "| ON0017 above:", conf, "| OFF above:", offs, "| real/surrogate median by scan:", rs,
                  "| LEAD" if conf and not any(offs.values()) else "| not a lead")


if __name__ == "__main__":
    a = sys.argv[1]
    synth() if a == "synth" else read() if a == "read" else scan(a)
