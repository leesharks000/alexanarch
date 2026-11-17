"""blind_pol.py — the whole coarse channel, scan-integrated, full Stokes: bins whose polarization departs from the
channel's own distribution. For each scan: I normalized by a running median (1025 bins); fractional V, Q, U per bin;
robust z of each against the channel. Reported: bins with I excess z>=6 or |pol z|>=6, flagged as ON-only, OFF-only or both
(topocentric, matched within ±3 bins = ±17 Hz; the comet drifts ~30 Hz across a scan, so persistence is checked loosely).
    python3 blind_pol.py CH"""
import numpy as np, sys, json, pathlib
from scipy.ndimage import median_filter
H = pathlib.Path(__file__).resolve().parent / "out"; CH = sys.argv[1]
ROLE = {"0013": "ON", "0015": "ON", "0017": "ON", "0014": "OFF", "0016": "OFF", "0018": "OFF"}
def rz(a): m = np.median(a); return (a - m) / (1.4826 * np.median(np.abs(a - m)) + 1e-30)
hits = {}
for s in ROLE:
    f = H / f"integ_scan{s}_ch{CH}_n19.npz"
    if not f.exists(): continue
    z = np.load(f); I, Q, U, V, fs = z["I"], z["Q"], z["U"], z["V"], z["fsky"]
    o = np.argsort(fs); I, Q, U, V, fs = I[o], Q[o], U[o], V[o], fs[o]
    n = len(I); dc = np.argmin(np.abs(fs - fs[n // 2])); I[dc - 2:dc + 3] = np.median(I)
    edge = slice(int(0.05 * n), int(0.95 * n))
    base = median_filter(I, 1025, mode="nearest"); In = I / base - 1
    zI = rz(In[edge]); zV = rz((V / I)[edge]); zQ = rz((Q / I)[edge]); zU = rz((U / I)[edge]); ff = fs[edge]
    sel = (zI >= 6) | (np.abs(zV) >= 6) | (np.abs(zQ) >= 6) | (np.abs(zU) >= 6)
    hits[s] = [(float(ff[i]), float(zI[i]), float(zV[i]), float(zQ[i]), float(zU[i])) for i in np.where(sel)[0]]
df = 5.587935447692876
out = []
allf = {s: np.array([h[0] for h in hits[s]]) for s in hits}
for s in hits:
    for h in hits[s]:
        pres = {t: bool(len(allf[t]) and np.min(np.abs(allf[t] - h[0])) <= 3 * df) for t in hits}
        on = sum(pres[t] for t in pres if ROLE[t] == "ON"); off = sum(pres[t] for t in pres if ROLE[t] == "OFF")
        out.append({"scan": s, "role": ROLE[s], "f_MHz": round(h[0] / 1e6, 6), "zI": round(h[1], 1), "zV": round(h[2], 1), "zQ": round(h[3], 1), "zU": round(h[4], 1), "on_scans": on, "off_scans": off})
json.dump(out, open(H / f"blind_pol_ch{CH}.json", "w"), indent=0)
cls = {}
for r in out:
    k = "ON-only" if r["off_scans"] == 0 else ("OFF-only" if r["on_scans"] == 0 else "both")
    cls[k] = cls.get(k, 0) + 1
print("rows", len(out), cls)
for r in sorted(out, key=lambda r: -max(abs(r["zV"]), abs(r["zQ"]), abs(r["zU"]), r["zI"])):
    if r["off_scans"] == 0 and r["on_scans"] >= 2: print("ON-persistent", r)
