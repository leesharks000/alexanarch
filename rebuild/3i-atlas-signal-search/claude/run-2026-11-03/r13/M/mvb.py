"""PLAN-M4b: mv.py (PLAN-M2, unchanged below the marked lines) plus the drift search of M4b/mdrift.py on the same in-memory power,
from one download.  python3 mvb.py CC SCAN [INJ]   INJ: an injection file (calibration only)."""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
sys.path.insert(0, os.path.join(HERE, "M4b")); import mdrift
cc, scan = int(sys.argv[1]), sys.argv[2]
INJ = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []
TAG = os.path.splitext(os.path.basename(sys.argv[3]))[0] if INJ else ""
dm.CH = cc; dm.FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6
N, INT, C, DF, TBIN = dm.N, dm.INT, dm.C, dm.DF, dm.TBIN; FC = dm.FC
OFFROWS = {"0013": [0], "0014": [0, 1], "0015": [0, 1], "0016": [0, 1, 2], "0017": [0, 1], "0018": [0]}
T0 = 61027 + 17226 / 86400.0
rng = np.random.default_rng(23); o = rng.uniform(0.03, 1.0, 400) * rng.choice([-1, 1], 400) * C / 1.42e9
offs = np.concatenate([[0.0], o[:100]])
nfr = 833; nint = nfr // INT; t0s = 61027 + int(dm.SCANS[scan][0]) / 86400.0
E = dm.ephem(); vel = lambda t: np.interp(t, E[:, 0], E[:, 1])
P = np.zeros((nint, N), np.float32); ts = time.time()
for j, X, Y in dm.frames(scan, nfr):
    k = j // INT
    if k >= nint: continue
    if INJ:   # M4b calibration only: synthetic linear chirps added to both feeds before the FFT
        if j == 0: S2 = float(np.mean(np.abs(X) ** 2))   # amp is given as r, the tone's power over the mean noise power of its bin
        tt = (j * N + np.arange(N)) * TBIN; ta = tt + (t0s - (61027 + 17226 / 86400.0)) * 86400.0   # ta: from scan 0013's start
        for f0, rate, r, ab in INJ:
            amp = np.sqrt(r * S2 / N); u = ta if ab else tt   # ab: one source continuing across the six scans
            ph = 2 * np.pi * (f0 * u + 0.5 * rate * u * u); sig = (amp * np.exp(1j * ph)).astype(np.complex64); X = X + sig; Y = Y + sig
    FX = dm.fft(X); FY = dm.fft(Y); P[k] += FX.real ** 2 + FX.imag ** 2 + FY.real ** 2 + FY.imag ** 2
t = t0s + (np.arange(nint) * INT + INT / 2) * N * TBIN / 86400.0
kk = ~np.isin(np.arange(nint), OFFROWS[scan])
# --- M4b: the drift search, on the same power normalised across frequency (a stationary tone survives; mv.py's
# normalisation over time, below, removes it), rows on target, in time order ---
B = np.median(P[kk], axis=0); bm = np.median(B.reshape(-1, 1024), axis=1); bm[bm <= 0] = 1
bp = np.interp(np.arange(N), np.arange(512, N, 1024), bm)
Rf = P[kk] / bp; g = np.median(Rf, axis=1); g[g <= 0] = 1; Rf = (Rf / g[:, None] - 1.0).astype(np.float32)
Rf[:, N // 2 - 4:N // 2 + 5] = 0   # the channel centre, as the hit rule masks it
Dr = mdrift.search(Rf); del Rf
dres = {"cc": cc, "fc": FC, "t": t[kk], "nrows": int(kk.sum())}
for L, e in Dr.items():
    for k_, v in e.items(): dres[f"L{L}_{k_}"] = v
os.makedirs(os.path.join(HERE, "out3"), exist_ok=True)
np.savez_compressed(os.path.join(HERE, "out3", f"cc{cc:02d}_{scan}{TAG}.npz"), **dres); del Dr, dres
# --- end M4b; below unchanged from mv.py ---
med = np.median(P, axis=0); med[med <= 0] = 1; R = P / med - 1.0; del P
R = (R + np.roll(R, 1, axis=1) + np.roll(R, -1, axis=1))[kk].astype(np.float64); tk = t[kk]
res = {"offs": offs, "cc": cc, "fc": FC}
for fi, dv in enumerate(offs):
    v = vel(tk) + dv * (tk - T0) * 86400.0; sh = np.rint(FC * (v - v[0]) / C / DF).astype(int)
    acc = np.zeros(N)
    for r in range(R.shape[0]):
        s = sh[r]
        if s >= 0: acc[:N - s] += R[r, s:]; acc[N - s:] += R[r, :s]
        else: acc[-s:] += R[r, :N + s]; acc[:-s] += R[r, N + s:]
    mm = np.median(acc); sd = 1.4826 * np.median(np.abs(acc - mm)); z = (acc - mm) / sd; z[N // 2 - 4:N // 2 + 5] = 0
    idx = np.where(z >= 2.0)[0]; res[f"f{fi}_idx"] = idx.astype(np.int32); res[f"f{fi}_z"] = z[idx].astype(np.float16); res[f"f{fi}_v0"] = np.float64(v[0])
os.makedirs(os.path.join(HERE, "out2"), exist_ok=True)
np.savez_compressed(os.path.join(HERE, "out2", f"cc{cc:02d}_{scan}{TAG}.npz"), **res)
print(cc, scan, "done", f"{time.time() - ts:.0f}s", flush=True)
