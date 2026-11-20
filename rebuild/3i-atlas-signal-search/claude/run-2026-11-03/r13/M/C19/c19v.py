"""PLAN-C19 products for one scan.  python3 c19v.py SCAN  ->  v_SCAN.npz"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(M, "../../../voltages/delaymod")); import dm
s = sys.argv[1]; cc = 19; dm.CH = cc; dm.FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6
N, INT, C, DF, TBIN, FC = dm.N, dm.INT, dm.C, dm.DF, dm.TBIN, dm.FC
TG = json.load(open(os.path.join(HERE, "targets.json"))); assert abs(TG["fc"] - FC) < 1
f = np.array([t["f"] for t in TG["targets"]]); kind = np.array([t["kind"] for t in TG["targets"]])
B0 = np.rint(N // 2 + (FC - f) / DF - 0.5).astype(int); NT = len(B0)
WR, WP, WV = 128, 2, 8; IE = np.where(kind == "E")[0]
E = dm.ephem(); vel = lambda t: np.interp(t, E[:, 0], E[:, 1])
t0s = 61027 + int(dm.SCANS[s][0]) / 86400.0
v0 = vel(t0s + 0.5 * N * TBIN / 86400.0)
NF = 833; NR = NF // INT
S = np.zeros((2, N)); racc = np.zeros((2, N), np.float32); R = np.zeros((NR, NT, 2, 2 * WR), np.float32); RM = np.zeros((NR, NT, 2), np.float32)
Pf = np.zeros((NF, NT, 2), np.float32); Pc = np.zeros((NF, NT, 2), np.float32); V = np.zeros((NF, len(IE), 2, 2 * WV), np.complex64)
SH = np.zeros(NF, int); tt = np.zeros(NF); off = np.arange(-WP, WP + 1); n = 0; T0 = time.time()
for j, X, Y in dm.frames(s, NF):
    tc = t0s + (j + 0.5) * N * TBIN / 86400.0; sh = int(np.rint(FC * (vel(tc) - v0) / C / DF)); SH[j] = sh; tt[j] = (j + 0.5) * N * TBIN
    for q, Z in enumerate((X, Y)):
        F = dm.fft(Z); p = (F.real ** 2 + F.imag ** 2).astype(np.float32)
        S[q] += p; racc[q] += p
        Pf[j, :, q] = p[B0[:, None] + off].sum(1); Pc[j, :, q] = p[B0[:, None] + sh + off].sum(1)
        V[j, :, q] = F[B0[IE][:, None] + np.arange(-WV, WV)]
    n += 1
    if n % INT == 0 and n // INT <= NR:
        r = n // INT - 1
        for q in range(2):
            w = racc[q][B0[:, None] + np.arange(-WR, WR)]; md = np.median(w, 1, keepdims=True); RM[r, :, q] = md[:, 0]; R[r, :, q] = w / md
        racc[:] = 0
    if n % 100 == 0: print(s, n, round(time.time() - T0), flush=True)
assert n == NF, n
np.savez_compressed(os.path.join(HERE, f"v_{s}.npz"), S=(S / n).astype(np.float32), R=R.astype(np.float16), RM=RM, Pf=Pf, Pc=Pc, V=V, SH=SH, t=tt, B0=B0, v0=v0, nframes=n)
print(s, "done", n, round(time.time() - T0), flush=True)
