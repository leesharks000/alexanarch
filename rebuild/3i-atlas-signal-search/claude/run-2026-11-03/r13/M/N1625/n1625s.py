"""PLAN-N1625-run: stream cc21, one pass per scan.  python3 n1625s.py SCAN
-> crops_SCAN.npz (first 32 frames, three 65,536-bin slices, both feeds) and track_SCAN.npz (per-row band power, all frames)."""
import os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../../voltages/delaymod")); import dm
dm.CH = 21; dm.FC = 1595.21484375e6 + 93.75e6 - 21.5 * 2.9296875e6
N, DF, FC = dm.N, dm.DF, dm.FC; W = 65536; F0 = 1625.2936106175184e6
SL = {"target": F0, "ctrl25k": F0 + 25e3, "hidrift": 1625.120423734188e6}
b = lambda f: int(np.rint(N // 2 + (FC - f) / DF - 0.5))
LO, HI = b(F0 + 3300.0), b(F0 - 1000.0) + 1        # band f0-1 kHz .. f0+3.3 kHz (bins run downward in frequency)
s = sys.argv[1]; NF = 833; INT = dm.INT; NR = NF // INT
crop = {f"{k}_{q}": [] for k in SL for q in "XY"}; acc = np.zeros((2, HI - LO)); rows = np.zeros((NR, 2, HI - LO), np.float32)
T0 = time.time(); n = 0
for j, X, Y in dm.frames(s, NF):
    for q, Z in enumerate((X, Y)):
        F = dm.fft(Z)
        if j < 32:
            for k, f in SL.items(): c = b(f); crop[f"{k}_{'XY'[q]}"].append(F[c - W // 2:c + W // 2].astype(np.complex64))
        acc[q] += np.abs(F[LO:HI]) ** 2
    n += 1
    if n % INT == 0 and n // INT <= NR: rows[n // INT - 1] = acc; acc[:] = 0
    if n % 100 == 0: print(s, n, round(time.time() - T0), flush=True)
assert n == NF, n
np.savez(os.path.join(HERE, f"crops_{s}.npz"), **{k: np.array(v) for k, v in crop.items()})
np.savez_compressed(os.path.join(HERE, f"track_{s}.npz"), rows=rows, lo=LO, hi=HI, fc=FC, df=DF, f0=F0)
print(s, "done", round(time.time() - T0), flush=True)
