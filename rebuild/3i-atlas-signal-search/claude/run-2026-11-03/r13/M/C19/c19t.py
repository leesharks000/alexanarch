"""PLAN-C19 targets (fixed before streaming).  python3 c19t.py -> targets.json"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
FC = 1631.8359375e6
A = [1631.6126212477684, 1631.680078804493, 1631.7475084215403, 1631.8149492144585, 1631.949809845537, 1632.017232477665, 1632.0846900343895, 1632.1521028876305]
nA = [-2, -1, 0, 1, 3, 4, 5, 6]
B = [1631.5653710626066, 1631.7002344876528, 1631.7676529288292, 1631.9025233387947, 1632.0373895578086, 1632.1048219688237]
nB = [-3, -1, 0, 2, 4, 5]
OFFGRID_A = 1631.863676011562
# shared step, two intercepts: f = a + n*d (A), f = b + n*d (B)
M = np.zeros((14, 3)); y = np.array(A + B) * 1e6
M[:8, 0] = 1; M[8:, 1] = 1; M[:, 2] = nA + nB
(a, b, d), *_ = np.linalg.lstsq(M, y, rcond=None)
res = y - M @ np.array([a, b, d])
lo, hi = FC - 1.35e6, FC + 1.35e6
T = []
def add(kind, f, **kw): T.append(dict(kind=kind, f=float(f), **kw))
for f, n in zip(A, nA): add("E", f * 1e6, seq="A", n=n)
for f, n in zip(B, nB): add("E", f * 1e6, seq="B", n=n)
add("E", OFFGRID_A * 1e6, seq="offgrid", n=None)
for seq, c0, have in (("A", a, set(nA)), ("B", b, set(nB))):
    for n in range(-60, 61):
        f = c0 + n * d
        if lo <= f <= hi and n not in have: add("G", f, seq=seq, n=n)
        fs = f + d / 2
        if lo <= fs <= hi: add("X", fs, seq=seq + "+half", n=n)
c = a + (b - a) / 2
for k in range(-120, 121):
    f = c + k * d / 2
    if lo <= f <= hi: add("K", f, k=k)
rng = np.random.default_rng(19); Ef = np.array([t["f"] for t in T if t["kind"] == "E"]); n = 0
while n < 60:
    f = rng.uniform(lo, hi)
    if np.min(np.abs(Ef - f)) > 500: add("X", f, seq="random", n=None); n += 1
out = dict(fc=FC, step_hz=float(d), a_hz=float(a), b_hz=float(b), offset_hz=float(b - a), rms_hz=float(np.sqrt(np.mean(res ** 2))), max_abs_hz=float(np.max(np.abs(res))), targets=T)
json.dump(out, open(os.path.join(HERE, "targets.json"), "w"), indent=1)
print({k: sum(t["kind"] == k for t in T) for k in "EGKX"}, round(d, 3), round(b - a, 3), round(out["rms_hz"], 3))
