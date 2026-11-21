"""PLAN-L1546.  python3 l1546.py selftest | SCAN | read"""
import json, os, sys, time
import numpy as np
from scipy.ndimage import gaussian_filter1d
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../../voltages/delaymod")); import dm
dm.CH = 48; dm.FC = 1595.21484375e6 + 93.75e6 - 48.5 * 2.9296875e6
N, DF, FC, CHB = dm.N, dm.DF, dm.FC, dm.CHB
F0 = 1546.9778403639793e6; W = 8192; LAGS = [32, 64, 128, 256, 512]; NSUR = 39; SIG = 32
SCANS = ["0013", "0014", "0015", "0016", "0017", "0018"]
SETS = {"A": 0, "B": 401}


def centre(f): return int(np.rint(N // 2 + (FC - f) / DF - 0.5))


def frames_at(scan, j0, n):
    """n frames from frame j0 (2 blocks a frame), via dm.fetch; blocks must lie in one file."""
    b0 = 2 * j0; assert b0 // 128 == (b0 + 2 * n - 1) // 128
    raw = dm.fetch(scan, b0, 2 * n)
    for k in range(n):
        r = np.frombuffer(raw[2 * k * CHB:2 * (k + 1) * CHB], np.int8).reshape(N, 4)
        v = np.maximum(r.astype(np.float32) / 127.0, -1.0)
        yield (v[:, 0] + 1j * v[:, 1]).astype(np.complex64), (v[:, 2] + 1j * v[:, 3]).astype(np.complex64)


def flat(F):
    env = gaussian_filter1d(np.abs(F) ** 2, SIG, mode="reflect"); env[env <= 0] = 1
    return np.fft.ifft(np.fft.ifftshift(F / np.sqrt(env)))


def A(zs):
    s = np.zeros(len(LAGS), complex); n = np.zeros(len(LAGS))
    for z in zs:
        u = z[1:] * np.conj(z[:-1]); u /= np.maximum(np.abs(u), 1e-30)
        for i, L in enumerate(LAGS): s[i] += np.sum(u[L:] * np.conj(u[:-L])); n[i] += len(u) - L
    return np.abs(s) / n


def test(crops, seed):
    real = A([flat(F) for F in crops]); rng = np.random.default_rng(seed)
    sur = np.array([A([flat(np.abs(F) * np.exp(2j * np.pi * rng.random(W))) for F in crops]) for _ in range(NSUR)])
    med = np.median(sur, 0); rs = real / med; ss = (sur / med).max(1)
    a = int(np.argmax(rs)); p = (1 + int((ss >= rs.max()).sum())) / (NSUR + 1)
    plag = [(1 + int((sur[:, i] >= real[i]).sum())) / (NSUR + 1) for i in range(len(LAGS))]
    return dict(A=real.tolist(), sur_median=med.tolist(), ratio=rs.tolist(), lag=LAGS[a], score=float(rs.max()), p=p, p_lag=plag)


def selftest():
    rng = np.random.default_rng(15469); out = {}
    code = np.exp(1j * np.pi / 2 * rng.integers(0, 4, 256)); sig = np.tile(code, W // 256)
    for name, amp in (("qpsk-0.65", 0.65), ("noise", 0.0)):
        crops = [np.fft.fftshift(np.fft.fft((rng.normal(size=W) + 1j * rng.normal(size=W)) / np.sqrt(2) + amp * sig)) for _ in range(16)]
        r = test(crops, 9900 + len(out)); out[name] = r
        print(name, "lag", r["lag"], "score", round(r["score"], 3), "p", r["p"], flush=True)
    json.dump(out, open(os.path.join(HERE, "selftest.json"), "w"))


def scan(s):
    i = SCANS.index(s); out = {"scan": s, "role": dm.SCANS[s][2]}
    b0, b8 = centre(F0), centre(F0 + 8000.0); out["bins"] = [b0, b8]
    for sk, j0 in SETS.items():
        T0 = time.time(); X, Y = [], []
        for x, y in frames_at(s, j0, 16):
            fx, fy = dm.fft(x), dm.fft(y)
            X.append((fx[b0 - W // 2:b0 + W // 2].astype(np.complex128), fx[b8 - W // 2:b8 + W // 2].astype(np.complex128)))
            Y.append((fy[b0 - W // 2:b0 + W // 2].astype(np.complex128), fy[b8 - W // 2:b8 + W // 2].astype(np.complex128)))
        print(s, sk, "fetched", round(time.time() - T0), flush=True)
        for q, fr in enumerate((X, Y)):
            base = 15469 + 1000 * i + 100 * q + 10 * list(SETS).index(sk)
            r = {"line": test([a for a, _ in fr], base), "ctrl8k": test([b for _, b in fr], base + 1)}
            if s == "0017":
                r["half1"] = test([a for a, _ in fr[:8]], base + 2); r["half2"] = test([a for a, _ in fr[8:]], base + 3)
            out[f"{sk}{'XY'[q]}"] = r
            print(s, sk, "XY"[q], "line p", r["line"]["p"], "lag", r["line"]["lag"], round(r["line"]["score"], 3), "| ctrl p", r["ctrl8k"]["p"], flush=True)
    json.dump(out, open(os.path.join(HERE, f"l_{s}.json"), "w"))


def read():
    R = {s: json.load(open(os.path.join(HERE, f"l_{s}.json"))) for s in SCANS}
    for sk in SETS:
        print(f"\nSet {sk}: scan role feed | line p lag score | +8 kHz p lag score")
        for s in SCANS:
            for q in "XY":
                r = R[s][f"{sk}{q}"]; l, c = r["line"], r["ctrl8k"]
                h = f" | halves p@lag {r['half1']['p_lag'][LAGS.index(l['lag'])]:.3f} {r['half2']['p_lag'][LAGS.index(l['lag'])]:.3f}" if "half1" in r else ""
                print(s, R[s]["role"], q, "|", l["p"], l["lag"], round(l["score"], 3), "|", c["p"], c["lag"], round(c["score"], 3), h)
        for q in "XY":
            r = R["0017"][f"{sk}{q}"]; l = r["line"]
            if l["p"] > 0.05: print(f"  {sk}{q}: no candidate in ON0017 (p {l['p']})"); continue
            k = LAGS.index(l["lag"]); ctrl = r["ctrl8k"]["p"] <= 0.05
            halves = r["half1"]["p_lag"][k] <= 0.05 and r["half2"]["p_lag"][k] <= 0.05
            offs = {o: (round(R[o][f"{sk}{q}"]["line"]["ratio"][k], 3), R[o][f"{sk}{q}"]["line"]["p_lag"][k]) for o in ("0014", "0016", "0018")}
            print(f"  {sk}{q}: candidate lag {l['lag']} | control fires: {ctrl} | both halves at lag: {halves} | OFF (ratio, p at lag): {offs}",
                  "| LEAD" if (not ctrl and halves and all(v[1] > 0.05 for v in offs.values())) else "| not a lead")


if __name__ == "__main__":
    a = sys.argv[1]
    selftest() if a == "selftest" else read() if a == "read" else scan(a)
