"""fixedlines.py — for chosen fixed topocentric bands, the scan-integrated excess (zI), fractional circular (zV) and
linear (zQ) polarization, and centroid, in each of the six scans, against 3000 same-width reference windows within
±50 kHz. Used to compare the 1666.0045/1666.0091 pair with the known interference tones (1665.6151, 1665.7501)."""
import numpy as np, json, sys, pathlib
from scipy.ndimage import median_filter
H = pathlib.Path(__file__).resolve().parent / "out"
BANDS = [(1665.61500, 1665.61525, "tone 1665.615 (C01/C02 interference)"), (1665.75000, 1665.75025, "tone 1665.750"),
         (1666.00444, 1666.00460, "pair A 1666.0045"), (1666.00908, 1666.00916, "pair B 1666.0091"),
         (1665.99985, 1666.00000, "A - 4.6 kHz"), (1666.01362, 1666.01378, "B + 4.6 kHz")]
res = {}
for s in ["0013", "0014", "0015", "0016", "0017", "0018"]:
    z = np.load(H / f"integ_scan{s}_ch7_n19.npz"); I, V, Q, f = (z[k].astype(float) for k in ("I", "V", "Q", "fsky"))
    o = np.argsort(f); I, V, Q, f = I[o], V[o], Q[o], f[o]
    In = I / median_filter(I, 1025, mode="nearest") - 1
    for lo, hi, lab in BANDS:
        b = (f >= lo * 1e6) & (f <= hi * 1e6); w = int(b.sum()); c = int(np.where(b)[0][0])
        ks = [k for k in range(c - 9000, c + 9000, w) if abs(k - c) >= 3 * w]
        ri = np.array([In[k:k + w].sum() for k in ks]); rv = np.array([V[k:k + w].sum() / I[k:k + w].sum() for k in ks]); rq = np.array([Q[k:k + w].sum() / I[k:k + w].sum() for k in ks])
        rz = lambda x, r: float((x - np.median(r)) / (1.4826 * np.median(np.abs(r - np.median(r)))))
        pos = np.clip(In[b], 0, None)
        res.setdefault(lab, {})[s] = {"zI": round(rz(In[b].sum(), ri), 1), "zV": round(rz(V[b].sum() / I[b].sum(), rv), 1), "zQ": round(rz(Q[b].sum() / I[b].sum(), rq), 1),
                                     "V_over_I": round(float(V[b].sum() / I[b].sum()), 4), "centroid_MHz": round(float((f[b] * pos).sum() / max(pos.sum(), 1e-12) / 1e6), 6)}
json.dump(res, open(H / "fixedlines.json", "w"), indent=1)
for lab in res:
    print(lab); print("   ", " ".join(f"{s}:{v['zI']:+.1f}/V{v['zV']:+.1f}/Q{v['zQ']:+.1f}" for s, v in res[lab].items()))
