"""PLAN-C08 step 3: per-frame power and band spectrum at both predictions.  python3 c08v.py SCAN"""
import os, sys
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(M, "../../../voltages/delaymod")); import dm
s = sys.argv[1]; cc = 8; dm.CH = cc; dm.FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6
N, INT, C, DF, TBIN, FC = dm.N, dm.INT, dm.C, dm.DF, dm.TBIN, dm.FC; W = 64; P0 = 787546
OFFROWS = {"0013": [0], "0014": [0, 1], "0015": [0, 1], "0016": [0, 1, 2], "0017": [0, 1], "0018": [0]}
E = dm.ephem(); vel = lambda t: np.interp(t, E[:, 0], E[:, 1])
v00 = float(np.load(os.path.join(M, "out2", "cc08_0013.npz"))["f0_v0"]); v0s = float(np.load(os.path.join(M, "out2", f"cc08_{s}.npz"))["f0_v0"])
pred = {"comet": P0 + int(np.rint(FC * (v0s - v00) / C / DF)), "fixed": P0}
t0s = 61027 + int(dm.SCANS[s][0]) / 86400.0
tk0 = t0s + ((OFFROWS[s][-1] + 1) * INT + INT / 2) * N * TBIN / 86400.0; v0 = vel(tk0)
pw = {k: [] for k in pred}; sp = {k: np.zeros((2, 2 * W)) for k in pred}; ser = []; tt = []; n = 0
for j, X, Y in dm.frames(s, 833):
    tc = t0s + (j + 0.5) * N * TBIN / 86400.0; sh = int(np.rint(FC * (vel(tc) - v0) / C / DF))
    FX = dm.fft(X); FY = dm.fft(Y); tt.append((j + 0.5) * N * TBIN); n += 1
    for k, p in pred.items():
        b = p + sh if k == "comet" else p
        row = []
        for q, F in enumerate((FX, FY)):
            seg = F[b - W:b + W]; a = np.abs(seg) ** 2; sp[k][q] += a; row.append(float(a[W - 2:W + 3].sum() / np.median(a)))
            if k == "comet" and s == "0013": ser.append(sf.ifft(sf.ifftshift(seg)).astype(np.complex64)) if q == 1 else None
        pw[k].append(row)
np.savez_compressed(os.path.join(HERE, f"v_{s}.npz"), t=np.array(tt), pred=np.array([pred["comet"], pred["fixed"]]),
    pw_comet=np.array(pw["comet"]), pw_fixed=np.array(pw["fixed"]), sp_comet=sp["comet"] / n, sp_fixed=sp["fixed"] / n,
    serY=np.concatenate(ser) if ser else np.zeros(0, np.complex64))
print(s, "done", n, flush=True)
