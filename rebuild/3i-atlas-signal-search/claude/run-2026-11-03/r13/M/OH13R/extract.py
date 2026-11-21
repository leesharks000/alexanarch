"""PLAN-OH13R: stream channel 7 for one scan, all 833 frames; keep every window (both feeds) as float16 complex.  python3 extract.py SCAN"""
import json, os, sys, time
import numpy as np
from common import *

s = sys.argv[1]; WIN = windows(); NW = len(WIN)
starts = np.array([track(s, f)[1] - WS // 2 for _, _, f, _ in WIN])
assert starts.min() > 0 and starts.max() + WS < N
out = np.lib.format.open_memmap(os.path.join(HERE, f"win_{s}.npy.part"), mode="w+", dtype=np.float16, shape=(NF, NW, 2, WS, 2))
T0 = time.time(); n = 0
for j, X, Y in dm.frames(s, NF):
    for q, Z in enumerate((X, Y)):
        F = dm.fft(Z) * SCALE
        B = np.stack([F[a:a + WS] for a in starts])
        out[j, :, q, :, 0] = B.real; out[j, :, q, :, 1] = B.imag
    n += 1
    if n % 100 == 0: print(s, n, round(time.time() - T0), flush=True)
assert n == NF, n
out.flush(); del out
os.replace(os.path.join(HERE, f"win_{s}.npy.part"), os.path.join(HERE, f"win_{s}.npy"))
json.dump({"scan": s, "windows": [w[0] for w in WIN], "starts": starts.tolist(), "seconds": round(time.time() - T0)}, open(os.path.join(HERE, f"win_{s}.json"), "w"))
print(s, "done", round(time.time() - T0), flush=True)
