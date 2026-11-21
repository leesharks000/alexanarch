"""PLAN-P3W-D2: stream cc21 for one scan, all 833 frames; keep the target slice's time series (both feeds) as float16.  python3 p3wd2s.py SCAN"""
import os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../../../voltages/delaymod")); import dm
dm.CH = 21; dm.FC = 1595.21484375e6 + 93.75e6 - 21.5 * 2.9296875e6
N, DF, FC = dm.N, dm.DF, dm.FC; WD = 65536; F0 = 1625.2936106175184e6
b = lambda f: int(np.rint(N // 2 + (FC - f) / DF - 0.5)); c0 = b(F0)
s = sys.argv[1]; NF = 833
out = np.lib.format.open_memmap(os.path.join(HERE, f"ser_{s}.npy.part"), mode="w+", dtype=np.float16, shape=(2, NF * WD, 2))
T0 = time.time(); n = 0
for j, X, Y in dm.frames(s, NF):
    for q, Z in enumerate((X, Y)):
        F = dm.fft(Z); z = np.fft.ifft(np.fft.ifftshift(F[c0 - WD // 2:c0 + WD // 2].astype(np.complex128)))
        out[q, j * WD:(j + 1) * WD, 0] = z.real; out[q, j * WD:(j + 1) * WD, 1] = z.imag
    n += 1
    if n % 100 == 0: print(s, n, round(time.time() - T0), flush=True)
assert n == NF, n
out.flush(); del out; os.replace(os.path.join(HERE, f"ser_{s}.npy.part"), os.path.join(HERE, f"ser_{s}.npy")); print(s, "done", round(time.time() - T0), flush=True)
