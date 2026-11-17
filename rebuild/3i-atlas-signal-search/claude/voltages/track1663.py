"""track1663.py — the 1663.3–1663.5 MHz feature in the 179 Hz x 0.72 s full-Stokes waterfalls (zoom_D1663_*):
per scan, each row normalized by the scan's per-frequency median; band power smoothed over 9 bins (1.6 kHz);
the peak frequency, its z, and V/I, Q/I, U/I there, reported per 30 s; and the drift rate fitted where the peak holds."""
import numpy as np, json, pathlib, sys
from scipy.ndimage import uniform_filter1d
H = pathlib.Path(__file__).resolve().parent / "out"; out = {}
for s in ["0013", "0014", "0015", "0016", "0017", "0018"]:
    f = H / f"zoom_D1663_scan{s}.npz"
    if not f.exists(): continue
    z = np.load(f); XX, YY, RE, IM, fs = (z[k].astype(float) for k in ("XX", "YY", "ReXY", "ImXY", "fsky")); dt = float(z["dt"])
    I = XX + YY; V = -2 * IM; Q = XX - YY; U = 2 * RE
    In = I / np.median(I, axis=0, keepdims=True) - 1
    Is = uniform_filter1d(In, 9, axis=1)
    sd = 1.4826 * np.median(np.abs(Is - np.median(Is)))
    rows = []
    step = int(round(30 / dt))
    for a in range(0, len(Is), step):
        blk = Is[a:a + step].mean(0); j = int(np.argmax(blk)); zz = blk[j] / (sd / np.sqrt(min(step, len(Is) - a)))
        sl = slice(max(0, j - 4), j + 5); Ib = I[a:a + step, sl].sum()
        rows.append({"t_s": round(a * dt, 1), "f_MHz": round(fs[j] / 1e6, 5), "z": round(float(zz), 1),
                     "V/I": round(float(V[a:a + step, sl].sum() / Ib), 3), "Q/I": round(float(Q[a:a + step, sl].sum() / Ib), 3), "U/I": round(float(U[a:a + step, sl].sum() / Ib), 3)})
    good = [r for r in rows if r["z"] > 6]
    drift = None
    if len(good) >= 3:
        drift = float(np.polyfit([r["t_s"] for r in good], [r["f_MHz"] * 1e6 for r in good], 1)[0])
    out[s] = {"rows": rows, "drift_Hz_per_s": None if drift is None else round(drift, 2)}
    print(s, "drift", out[s]["drift_Hz_per_s"])
    for r in rows: print("   ", r)
json.dump(out, open(H / "track1663.json", "w"), indent=1)
