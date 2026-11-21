"""Part 2, the event itself: rows 31-34 of ON0013 at full resolution, and strong peaks anywhere in the band in every scan."""
import os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S = ["0013", "0014", "0015", "0016", "0017", "0018"]; N = 1 << 20; TROW = 17 * N * 3.41333333333333e-07
d = np.load(os.path.join(H, "track_0013.npz")); LO, HI, FC, DF, F0 = int(d["lo"]), int(d["hi"]), float(d["fc"]), float(d["df"]), float(d["f0"])
freq = FC - (np.arange(LO, HI) - N // 2 + 0.5) * DF
for s in S:
    rows = np.load(os.path.join(H, f"track_{s}.npz"))["rows"]; R = rows.sum(1) / np.median(rows.sum(1), -1, keepdims=True)
    hits = [(r, int(np.argmax(R[r])), float(R[r].max())) for r in range(R.shape[0]) if R[r].max() > 8]
    print(s, "rows with any bin >8x median in the band (f0-1 kHz..f0+3.3 kHz):", [(r, round((freq[k] - F0), 1), round(v, 1)) for r, k, v in hits])
R = np.load(os.path.join(H, "track_0013.npz"))["rows"]; T = R.sum(1); T = T / np.median(T, -1, keepdims=True)
for r in (31, 32, 33, 34):
    k = int(np.argmax(T[r])); prof = T[r, k - 6:k + 7]
    xy = R[r, 0, k] / R[r, 1, k]
    above = np.where(T[r] > 3)[0]
    print(f"row {r} (t {r * TROW:.0f}-{(r + 1) * TROW:.0f} s): peak at f0{freq[k] - F0:+.1f} Hz, {T[r, k]:.1f}x; bins >3x: {len(above)} spanning {freq[above].max() - freq[above].min() if len(above) else 0:.0f} Hz; X/Y {xy:.2f}; profile", np.round(prof, 1).tolist())
