"""PLAN-J (PLAN-J.sha256): part J of PLAN-r13. Streams one scan's coarse-channel-7 voltages again (decoding as voltages/delaymod/dm.py),
computes P1, P2, P4 per integration, and for V0 and V2 stacks them in the comet frame and 400 false-drift frames (default_rng(23)).
Keeps sparse z>=2 lists (J1) and the pair product Q(Δ), Δ=5..2000 (J2).   python3 jv.py SCAN  -> out/SCAN.npz, out/SCAN-Q.npy, out/SCAN.json"""
import sys, os, json, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
N, INT, C, FC, DF, TBIN = dm.N, dm.INT, dm.C, dm.FC, dm.DF, dm.TBIN
OFFROWS = {"0013": [0], "0014": [0, 1], "0015": [0, 1], "0016": [0, 1, 2], "0017": [0, 1], "0018": [0]}
NFALSE = 400; DMIN, DMAX = 5, 2000
T0 = 61027 + 17226 / 86400.0

def offsets():
    rng = np.random.default_rng(23)
    return np.concatenate([[0.0], rng.uniform(0.03, 1.0, NFALSE) * rng.choice([-1, 1], NFALSE) * C / 1.42e9])

def stack(R, sh):
    acc = np.zeros(N)
    for k in range(R.shape[0]):
        s = sh[k]
        if s >= 0: acc[:N - s] += R[k, s:]; acc[N - s:] += R[k, :s]
        else: acc[-s:] += R[k, :N + s]; acc[:-s] += R[k, N + s:]
    return acc  # identical to sum of np.roll(R[k], -sh[k])

def main(scan):
    nfr = 833; nint = nfr // INT
    t0s = 61027 + int(dm.SCANS[scan][0]) / 86400.0
    E = dm.ephem(); vel = lambda t: np.interp(t, E[:, 0], E[:, 1])
    P = {m: np.zeros((nint, N), np.float32) for m in (1, 2, 4)}
    ts = time.time()
    for j, X, Y in dm.frames(scan, nfr):
        k = j // INT
        if k >= nint: continue
        FX = dm.fft(X); FY = dm.fft(Y)
        P[1][k] += FX.real ** 2 + FX.imag ** 2 + FY.real ** 2 + FY.imag ** 2
        x2 = X * X; y2 = Y * Y; F2x = dm.fft(x2); F2y = dm.fft(y2)
        P[2][k] += F2x.real ** 2 + F2x.imag ** 2 + F2y.real ** 2 + F2y.imag ** 2
        F4x = dm.fft(x2 * x2); F4y = dm.fft(y2 * y2)
        P[4][k] += F4x.real ** 2 + F4x.imag ** 2 + F4y.real ** 2 + F4y.imag ** 2
        if j % 100 == 0: print(scan, "frame", j, f"{time.time() - ts:.0f}s", flush=True)
    t = t0s + (np.arange(nint) * INT + INT / 2) * N * TBIN / 86400.0
    offs = offsets()
    keep = {"V0": np.ones(nint, bool), "V2": ~np.isin(np.arange(nint), OFFROWS[scan])}
    res = {"offs": offs}; Q = np.zeros((2, NFALSE + 1, DMAX - DMIN + 1), np.float32)
    for vi, V in enumerate(("V0", "V2")):
        kk = keep[V]
        for m in (1, 2, 4):
            x = P[m]
            med = np.median(x, axis=0); med[med <= 0] = 1   # as delaymod: median over all 49 integrations
            R = x / med - 1.0
            R = R + np.roll(R, 1, axis=1) + np.roll(R, -1, axis=1)
            R = R[kk].astype(np.float64); tk = t[kk]
            for fi, dv in enumerate(offs):
                v = vel(t) + dv * (t - T0) * 86400.0
                sh = np.rint(m * FC * (v[kk] - v[0]) / C / DF).astype(int)
                acc = stack(R, sh)
                mm = np.median(acc); s = 1.4826 * np.median(np.abs(acc - mm)); z = (acc - mm) / s
                z[N // 2 - 4:N // 2 + 5] = 0
                idx = np.where(z >= 2.0)[0]
                res[f"m{m}_{V}_f{fi}_idx"] = idx.astype(np.int32); res[f"m{m}_{V}_f{fi}_z"] = z[idx].astype(np.float16)
                res[f"m{m}_{V}_f{fi}_v0"] = np.float64(v[0])
                if m == 1:
                    Yc = np.clip(z, 0, None); F = sf.rfft(Yc, 2 * N, workers=4)
                    ac = sf.irfft(F.real ** 2 + F.imag ** 2, 2 * N, workers=4)
                    Q[vi, fi] = ac[DMIN:DMAX + 1]
                if fi % 50 == 0: print(scan, V, "m", m, "frame", fi, f"{time.time() - ts:.0f}s", flush=True)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    np.savez_compressed(os.path.join(HERE, "out", f"{scan}.npz"), **res)
    np.save(os.path.join(HERE, "out", f"{scan}-Q.npy"), Q)
    json.dump({"scan": scan, "nframes": nfr, "nint": nint, "offrows": OFFROWS[scan], "elapsed_s": time.time() - ts},
              open(os.path.join(HERE, "out", f"{scan}.json"), "w"))
    print(scan, "done", f"{time.time() - ts:.0f}s", flush=True)

if __name__ == "__main__":
    main(sys.argv[1])
