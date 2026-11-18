"""PLAN-M2: stream one scan of one coarse channel, stack P1 (V2) in the comet frame and 100 false frames.  python3 mv.py CC SCAN"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
cc, scan = int(sys.argv[1]), sys.argv[2]
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
    FX = dm.fft(X); FY = dm.fft(Y); P[k] += FX.real ** 2 + FX.imag ** 2 + FY.real ** 2 + FY.imag ** 2
t = t0s + (np.arange(nint) * INT + INT / 2) * N * TBIN / 86400.0
kk = ~np.isin(np.arange(nint), OFFROWS[scan])
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
np.savez_compressed(os.path.join(HERE, "out2", f"cc{cc:02d}_{scan}.npz"), **res)
print(cc, scan, "done", f"{time.time() - ts:.0f}s", flush=True)
