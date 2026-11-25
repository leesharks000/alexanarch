"""PLAN-WOW3 R3: polarization at the Wow's velocities on the OH lines. Reads the scan-integrated full-Stokes spectra that
../voltages/voltreduce.py writes for blc23 coarse channels 7, 8 and 26 (5.59 Hz). At each target (comet frame at scan mid-time):
the largest |z| of V/I, Q/I, U/I and the largest z of I inside the band, per scan, ranked against 200 random windows of the same
width in the same coarse channel. Normalisation as ../voltages/blind_pol.py, with the channel trimmed to its inner 98%.
    python3 r3_pol.py"""
import json, os, sys, numpy as np
from scipy.ndimage import median_filter
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "../voltages/out")
sys.path.insert(0, os.path.join(HERE, "../voltages/delaymod")); import dm
C = 299792.458; H = 1420.40575177
V = {"67.54": C * 0.320 / H, "10.51": C * 0.0498 / H}
OH = {"1612": 1612.2310, "1665": 1665.4018, "1667": 1667.3590}
TARG = {7: ["OH1665_v67.54", "OH1667_v67.54", "OH1667_v10.51"], 8: ["OH1665_v10.51"], 26: ["OH1612_v67.54", "OH1612_v10.51"]}
F = {f"OH{l}_v{v}": OH[l] * (1 + V[v] / C) for l in OH for v in V}
ROLE = {"0013": "ON", "0015": "ON", "0017": "ON", "0014": "OFF", "0016": "OFF", "0018": "OFF"}
E = dm.ephem()
def rz(a): m = np.median(a); return (a - m) / (1.4826 * np.median(np.abs(a - m)) + 1e-30)
res = {}
for ch, names in TARG.items():
    for s in ROLE:
        z = np.load(os.path.join(OUT, f"integ_scan{s}_ch{ch}_n19.npz")); I, Q, U, Vv, fs = z["I"], z["Q"], z["U"], z["V"], z["fsky"]
        o = np.argsort(fs); I, Q, U, Vv, fs = I[o], Q[o], U[o], Vv[o], fs[o]; n = len(I)
        dc = n // 2; I[dc - 2:dc + 3] = np.median(I)
        e = slice(int(0.01 * n), int(0.99 * n))
        zI = rz((I / median_filter(I, 1025, mode="nearest") - 1)[e]); zp = [np.abs(rz((P / I)[e])) for P in (Vv, Q, U)]; ff = fs[e] / 1e6
        tmid = 61027 + (int(dm.SCANS[s][0]) + 150) / 86400.0; vel = float(np.interp(tmid, E[:, 0], E[:, 1]))
        df = ff[1] - ff[0]; rng = np.random.default_rng(1000 * ch + int(s))
        for k in names:
            f = F[k] * (1 - vel / C); half = 5e-3 * F[k] / H; nb = int(round(half / df)); c = int(np.searchsorted(ff, f))
            def stat(c0): 
                sl = slice(c0 - nb, c0 + nb + 1)
                return [float(zI[sl].max())] + [float(p[sl].max()) for p in zp]
            t = stat(c); ctrl = np.array([stat(int(rng.integers(nb + 1, len(ff) - nb - 1))) for _ in range(200)])
            res.setdefault(k, {"f_rest_MHz": F[k], "coarse_channel": ch, "scans": {}})["scans"][s] = {
                "role": ROLE[s], "f_topo_MHz": f, "in_trimmed_channel": bool(nb < c < len(ff) - nb),
                "max_zI": t[0], "max_absz_V": t[1], "max_absz_Q": t[2], "max_absz_U": t[3],
                "rank": {n_: float((ctrl[:, i] < t[i]).mean()) for i, n_ in enumerate(["I", "V", "Q", "U"])}}
for k, r in res.items():
    r["counts"] = {q: bool(all(r["scans"][s]["rank"][q] > 0.95 for s in ROLE if ROLE[s] == "ON") and
                           not any(r["scans"][s]["rank"][q] > 0.95 for s in ROLE if ROLE[s] == "OFF")) for q in "IVQU"}
    print(k, r["counts"], {s: {q: round(v, 2) for q, v in r["scans"][s]["rank"].items()} for s in ROLE}, flush=True)
json.dump(res, open(os.path.join(HERE, "r3.json"), "w"), indent=1)
