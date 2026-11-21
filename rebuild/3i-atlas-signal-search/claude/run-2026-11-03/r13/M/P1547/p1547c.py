"""PLAN-P1547C: cross-feed coupling (shared-rotation null).  python3 p1547c.py synth | SCAN | read"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p1547 as P, p1547b as PB
dm, W, NFR, NSUR, QT, SCANS, SL, SEG = P.dm, P.W, P.NFR, P.NSUR, P.QT, P.SCANS, P.SL, P.SEG
LAGS = [-512, -256, -128, -64, -32, -16, -8, -4, -2, 0, 2, 4, 8, 16, 32, 64, 128, 256, 512]


def inc(z):
    d = z[1:] * np.conj(z[:-1]); return d / np.maximum(np.abs(d), 1e-30)


class Acc:
    def __init__(s): s.c = np.zeros(len(LAGS), complex); s.nc = np.zeros(len(LAGS)); s.k = np.zeros(len(QT), complex); s.nk = 0
    def add(s, zx, zy):
        ux, uy = inc(zx), inc(zy); n = len(ux)
        for i, L in enumerate(LAGS):
            if L >= 0: s.c[i] += np.sum(ux[L:] * np.conj(uy[:n - L])); s.nc[i] += n - L
            else: s.c[i] += np.sum(ux[:n + L] * np.conj(uy[-L:])); s.nc[i] += n + L
        PX = np.fft.fft(zx.reshape(-1, SEG), axis=1); PX /= np.maximum(np.abs(PX), 1e-30)
        PY = np.fft.fft(zy.reshape(-1, SEG), axis=1); PY /= np.maximum(np.abs(PY), 1e-30)
        k, l, m, nn = QT.T
        s.k += np.sum(PX[:, k] * PY[:, l] * np.conj(PX[:, m]) * np.conj(PY[:, nn]), axis=0); s.nk += PX.shape[0]
    def out(s): return np.abs(s.c) / s.nc, np.abs(s.k) / s.nk


def run(XS, YS, seed0):
    R = Acc(); S = [Acc() for _ in range(NSUR)]; rngs = [np.random.default_rng(seed0 + k) for k in range(NSUR)]
    for FX, FY in zip(XS, YS):
        GX, GY = PB.norm(FX), PB.norm(FY); R.add(PB.series(GX), PB.series(GY))
        for k in range(NSUR):
            e = np.exp(2j * np.pi * rngs[k].random(W)); S[k].add(PB.series(GX * e), PB.series(GY * e))
    rc, rk = R.out(); sc = np.array([x.out()[0] for x in S]); sk = np.array([x.out()[1] for x in S])
    r = dict(C=rc.tolist(), K=rk.tolist(), sC=sc.tolist(), sK=sk.tolist())
    r["family"] = {f: dict(score=float(np.max(r[f])), arg=int(np.argmax(r[f])),
                           p=(1 + int((np.array(r["s" + f]).max(1) >= np.max(r[f])).sum())) / (NSUR + 1),
                           sur_max_median=float(np.median(np.array(r["s" + f]).max(1)))) for f in ("C", "K")}
    return r


def synth():
    rng = np.random.default_rng(11); out = {}; ts = np.arange(SEG); k, l, m, n = QT[0]; nseg = W // SEG
    def noise(): return (rng.normal(size=W) + 1j * rng.normal(size=W)) / np.sqrt(2)
    def coupled():
        a, b, c = (rng.random((3, nseg)) * 2 * np.pi)
        sx = np.concatenate([(np.exp(1j * (2 * np.pi * k * ts / SEG + a[s])) + np.exp(1j * (2 * np.pi * m * ts / SEG + b[s]))) / 2 for s in range(nseg)])
        sy = np.concatenate([(np.exp(1j * (2 * np.pi * l * ts / SEG + c[s])) + np.exp(1j * (2 * np.pi * n * ts / SEG + a[s] + c[s] - b[s]))) / 2 for s in range(nseg)])
        return sx, sy
    for amp in (0.0, 0.1, 0.25, 0.5, 1.0):
        XS, YS = [], []
        for _ in range(NFR):
            sx, sy = coupled(); XS.append(np.fft.fftshift(np.fft.fft(noise() + amp * sx))); YS.append(np.fft.fftshift(np.fft.fft(noise() + amp * sy)))
        r = run(XS, YS, 990000 + len(out) * 100)
        bx = PB.run(XS, 880000 + len(out) * 100); by = PB.run(YS, 870000 + len(out) * 100)
        r["within"] = {"X": P.fam(bx), "Y": P.fam(by)}; out[f"coupled-{amp}"] = r
        fc, fk = r["family"]["C"], r["family"]["K"]
        print(f"amp {amp:4.2f} | cross memory p {fc['p']:.2f} {fc['score'] / fc['sur_max_median']:5.2f}x lag {LAGS[fc['arg']]:5d} | cross closure p {fk['p']:.2f} {fk['score'] / fk['sur_max_median']:6.2f}x q {fk['arg']}"
              f" | within-feed (P1547B) closure p X {r['within']['X']['Q']['p']:.2f} Y {r['within']['Y']['Q']['p']:.2f}, memory p X {r['within']['X']['A']['p']:.2f} Y {r['within']['Y']['A']['p']:.2f}", flush=True)
    json.dump(out, open(os.path.join(HERE, "synthC.json"), "w"))


def scan(s):
    i = SCANS.index(s); T0 = time.time(); X, Y = [], []
    for j, x, y in dm.frames(s, NFR):
        X.append(dm.fft(x)[SL].astype(np.complex128)); Y.append(dm.fft(y)[SL].astype(np.complex128))
    print(s, "fetched", len(X), round(time.time() - T0), flush=True)
    r = run(X, Y, 1547500 + 100 * i); r.update(scan=s, role=dm.SCANS[s][2], frames=len(X))
    print(s, json.dumps(r["family"]), flush=True)
    json.dump(r, open(os.path.join(HERE, f"pc_{s}.json"), "w"))


def read():
    R = {s: json.load(open(os.path.join(HERE, f"pc_{s}.json"))) for s in SCANS}
    print("scan role | cross memory: p lag score/surmax | cross closure: p quartet score/surmax")
    for s in SCANS:
        c, k = R[s]["family"]["C"], R[s]["family"]["K"]
        print(s, R[s]["role"], "|", c["p"], LAGS[c["arg"]], round(c["score"] / c["sur_max_median"], 2), "|", k["p"], k["arg"], round(k["score"] / k["sur_max_median"], 2))
    def above(s, f, a): return float(np.array(R[s][f])[a]) > float(np.array(R[s]["s" + f])[:, a].max())
    def ratio(s, f, a): return round(float(np.array(R[s][f])[a]) / float(np.median(np.array(R[s]["s" + f])[:, a])), 2)
    print("\nGates:")
    for f in ("C", "K"):
        fm = R["0015"]["family"][f]
        if fm["p"] > 0.05: print(f, "no candidate in ON0015 (p", fm["p"], ")"); continue
        a = fm["arg"]; conf = above("0017", f, a); offs = {o: above(o, f, a) for o in ("0014", "0016", "0018")}
        print(f, "candidate at", LAGS[a] if f == "C" else QT[a].tolist(), "| ON0017 above:", conf, "| OFF above:", offs,
              "| real/surrogate median:", {o: ratio(o, f, a) for o in SCANS}, "| LEAD" if conf and not any(offs.values()) else "| not a lead")


if __name__ == "__main__":
    a = sys.argv[1]
    synth() if a == "synth" else read() if a == "read" else scan(a)
