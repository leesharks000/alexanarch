"""The 1546.977840 MHz line read from C4850's saved spectra (READING-C4850-line-1546977840.md).  python3 c4850_line_reading.py"""
import os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S = ["0013", "0014", "0015", "0016", "0017", "0018"]; OFFB = [0, 1, 2, 3, 13, 14, 15]
def load(s):
    d = np.load(os.path.join(H, f"v_cc48_{s}.npz")); V = d["V"][:, 0]; P = np.abs(V) ** 2
    Q = P / np.median(P[:, :, OFFB], axis=(0, 2))[None, :, None]; return d, V, Q
prof = {s: load(s)[2].mean(1).mean(0) for s in S}; ref = np.mean([prof[s] for s in S[:4]], 0)
for s in S: print(s, "excess bins 6-11:", round(float((prof[s] - ref)[6:12].sum()), 2))
d, V, Q = load("0017"); t = d["t"]; off = np.median(Q[:, :, OFFB])
sm = np.convolve((Q[:, :, 6:12].sum(2) - 6 * off).sum(1), np.ones(5) / 5, "same")
pk = [j for j in range(2, 831) if sm[j] == sm[max(0, j - 30):j + 31].max() and sm[j] > 3 * np.median(sm)]
for j in pk:
    P = np.abs(V[j - 6:j + 6]) ** 2; pr = P.sum((0, 1)); c = (np.arange(4, 14) * pr[4:14]).sum() / pr[4:14].sum()
    print(f"burst t={t[j]:.1f}s height {sm[j]:.1f} centroid bin {c:.2f} comet shift {d['SH'][j]}")
for s in S:
    _, _, Qs = load(s); o = np.median(Qs[:, :, OFFB]); m = np.convolve((Qs[:, :, 6:12].sum(2) - 6 * o).sum(1), np.ones(5) / 5, "same")
    print(s, "5-frame excess max", round(float(m.max()), 1))
