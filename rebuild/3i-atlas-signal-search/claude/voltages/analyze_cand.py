"""analyze_cand.py — the 13 candidates in the raw voltages: tracked-bin power per 0.179 s spectrum, its scan sum,
full Stokes at the tracked bin, and periodicity, ON (0013, 0015, 0017) against OFF (0014, 0016, 0018).
Normalization: each spectrum's 65-bin window is divided by the median of its outer bins (|k|>=8), minus 1.
    python3 analyze_cand.py [scans...]"""
import numpy as np, json, sys, pathlib
H = pathlib.Path(__file__).resolve().parent / "out"
scans = sys.argv[1:] or ["0013", "0014", "0015", "0016", "0017", "0018"]
ROLE = {"0013": "ON", "0015": "ON", "0017": "ON", "0014": "OFF", "0016": "OFF", "0018": "OFF"}
res = {}
for s in scans:
    f = H / f"cand_scan{s}_ch7_n19.npz"
    if not f.exists(): continue
    z = np.load(f); win = z["win"].astype(np.float64); ids = list(z["ids"]); W = int(z["W"])
    k = np.arange(-W, W + 1); outer = np.abs(k) >= 8
    I = win[..., 0] + win[..., 1]; Q = win[..., 0] - win[..., 1]; U = 2 * win[..., 2]; V = -2 * win[..., 3]
    base = np.median(I[:, :, outer], axis=2, keepdims=True)
    In = I / base - 1                                     # per spectrum, per bin
    nT = In.shape[1]
    for ci, cid in enumerate(ids):
        tr = In[ci, :, W - 1:W + 2].mean(axis=1)          # tracked bin ±1 (the path)
        # scan sum z against the window's other bins (each offset k treated as a null path)
        sums = In[ci].sum(axis=0)                        # per offset, summed over time
        null = sums[outer]; zc = (sums[W - 1:W + 2].mean() - np.median(null)) / (1.4826 * np.median(np.abs(null - np.median(null))) + 1e-12)
        Ic = I[ci, :, W - 1:W + 2].sum(); Qc = Q[ci, :, W - 1:W + 2].sum(); Uc = U[ci, :, W - 1:W + 2].sum(); Vc = V[ci, :, W - 1:W + 2].sum()
        Ib = I[ci][:, outer].sum(axis=0); Vb = V[ci][:, outer].sum(axis=0); Qb = Q[ci][:, outer].sum(axis=0); Ub = U[ci][:, outer].sum(axis=0)
        vfrac = Vc / Ic; vnull = Vb / Ib; qfrac = Qc / Ic; qnull = Qb / Ib; ufrac = Uc / Ic; unull = Ub / Ib
        zv = (vfrac - np.median(vnull)) / (1.4826 * np.median(np.abs(vnull - np.median(vnull))) + 1e-12)
        zq = (qfrac - np.median(qnull)) / (1.4826 * np.median(np.abs(qnull - np.median(qnull))) + 1e-12)
        zu = (ufrac - np.median(unull)) / (1.4826 * np.median(np.abs(unull - np.median(unull))) + 1e-12)
        # periodicity of the tracked series
        p = np.abs(np.fft.rfft(tr - tr.mean())) ** 2; fr = np.fft.rfftfreq(nT, float(z["dt"]))
        pk = int(np.argmax(p[3:])) + 3; pz = p[pk] / np.median(p[3:])
        # peak single-spectrum excursion
        tz = (tr - np.median(tr)) / (1.4826 * np.median(np.abs(tr - np.median(tr))) + 1e-12)
        res.setdefault(cid, {})[s] = {"role": ROLE[s], "z_sum": round(float(zc), 2), "V_over_I": round(float(vfrac), 5), "z_V": round(float(zv), 2),
            "z_Q": round(float(zq), 2), "z_U": round(float(zu), 2), "max_spectrum_z": round(float(tz.max()), 2), "n_spectra_z>4": int((tz > 4).sum()),
            "period_peak_Hz": round(float(fr[pk]), 4), "period_power_ratio": round(float(pz), 1), "nspec": nT}
json.dump(res, open(H / "cand_analysis.json", "w"), indent=1)
for cid in sorted(res):
    row = res[cid]
    print(cid, " ".join(f"{s}{row[s]['role'][0:2]}:z{row[s]['z_sum']:+.1f} V{row[s]['z_V']:+.1f} Q{row[s]['z_Q']:+.1f} U{row[s]['z_U']:+.1f} mx{row[s]['max_spectrum_z']:.1f}" for s in sorted(row)))
