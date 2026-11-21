"""PLAN-N1625-run, part 2: the event's track through the six scans.  python3 n1625t.py"""
import json, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S = ["0013", "0014", "0015", "0016", "0017", "0018"]; OFF = [0, 317, 635, 953, 1271, 1588]
N = 1 << 20; TBIN = 3.41333333333333e-07; TROW = 17 * N * TBIN; RATE = 1.690990951372353
out = {}
d0 = np.load(os.path.join(H, "track_0013.npz")); LO, HI, FC, DF, F0 = int(d0["lo"]), int(d0["hi"]), float(d0["fc"]), float(d0["df"]), float(d0["f0"])
freq = FC - (np.arange(LO, HI) - N // 2 + 0.5) * DF
def norm(rows): return rows / np.median(rows, axis=-1, keepdims=True)
# 1. the line in ON0013: per row, the peak within +-40 bins of the predicted track
R = norm(np.load(os.path.join(H, "track_0013.npz"))["rows"].sum(1)); tr = []
for r in range(R.shape[0]):
    t = (r + 0.5) * TROW; fp = F0 + RATE * t; i = int(np.argmin(np.abs(freq - fp))); a, b = max(0, i - 40), min(len(freq), i + 41)
    k = a + int(np.argmax(R[r, a:b])); tr.append((t, float(freq[k]), float(R[r, k])))
tr = np.array(tr); good = tr[:, 2] > 3
fit = np.polyfit(tr[good, 0], tr[good, 1], 1) if good.sum() > 3 else [np.nan, np.nan]
out["on0013_rows_with_peak_gt3"] = int(good.sum()); out["on0013_fit_hz_per_s"] = float(fit[0]); out["on0013_fit_f_at_start_mhz"] = float(fit[1] / 1e6)
out["on0013_peak_median"] = float(np.median(tr[:, 2]))
print("ON0013: rows with a peak >3x the row median near the track:", int(good.sum()), "of", len(tr), "| fit drift", round(fit[0], 3), "Hz/s, start", round(fit[1] / 1e6, 7), "MHz | median peak", round(np.median(tr[:, 2]), 2))
print("  per-row peak (x median):", np.round(tr[:, 2], 1).tolist())
# 2. along the extended track (the fitted one, and M4b's), +-3 bins, in each scan
for name, (r0, f00) in {"fit": (fit[0], fit[1]), "m4b": (RATE, F0)}.items():
    for s, o in zip(S, OFF):
        Rs = norm(np.load(os.path.join(H, f"track_{s}.npz"))["rows"].sum(1)); v = []; inband = 0
        for r in range(Rs.shape[0]):
            fp = f00 + r0 * (o + (r + 0.5) * TROW)
            if not (freq.min() <= fp <= freq.max()): continue
            inband += 1; i = int(np.argmin(np.abs(freq - fp))); v.append(Rs[r, max(0, i - 3):i + 4].max())
        out[f"{name}_{s}"] = dict(rows_in_band=inband, median_peak=float(np.median(v)) if v else None, frac_gt3=float(np.mean(np.array(v) > 3)) if v else None)
        print(name, s, "rows in band", inband, "| median peak along track", round(np.median(v), 2) if v else None, "| fraction of rows >3x", round(float(np.mean(np.array(v) > 3)), 2) if v else None)
# 3. control: the same statistic along a parallel track 600 Hz away
for s, o in zip(S, OFF):
    Rs = norm(np.load(os.path.join(H, f"track_{s}.npz"))["rows"].sum(1)); v = []
    for r in range(Rs.shape[0]):
        fp = fit[1] + 600 + fit[0] * (o + (r + 0.5) * TROW)
        if not (freq.min() <= fp <= freq.max()): continue
        i = int(np.argmin(np.abs(freq - fp))); v.append(Rs[r, max(0, i - 3):i + 4].max())
    out[f"ctrl600_{s}"] = float(np.median(v)) if v else None
print("control track +600 Hz, median peak:", {s: out[f"ctrl600_{s}"] and round(out[f"ctrl600_{s}"], 2) for s in S})
json.dump(out, open(os.path.join(H, "track.json"), "w"), indent=1)
