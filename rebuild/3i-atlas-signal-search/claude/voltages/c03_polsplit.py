"""c03_polsplit.py — the one split the public products cannot make: C03 in the X and Y polarizations separately
(independent noise realizations, same sky). Comet track, 0.70 Hz, 7-bin aperture; z per scan against parallel tracks
(|offset| >= 20 Hz), and the ON-minus-OFF contrast per polarization. A signal present in the sky is in both; a noise
fluctuation selected in the summed power need not be."""
import numpy as np, json, pathlib
H = pathlib.Path(__file__).resolve().parent
TR = {s["scan"]: s for s in {c["id"]: c for c in json.load(open(H.parent / "oh13/oh13_candidates.json"))["candidates"]}["C03"]["scans"]}
ON, OFF = ["0013", "0015", "0017"], ["0014", "0016", "0018"]; per = {"XX": {}, "YY": {}}
for s in ON + OFF:
    z = np.load(H / f"out/zoom_C03hr_scan{s}.npz"); fs = z["fsky"]; dt = float(z["dt"]); df = float(z["df"])
    nT = z["XX"].shape[0]; t = (np.arange(nT) + 0.5) * dt; tr = TR[s]; ts, ns = tr["tsamp_s"], tr["n_steps"]
    fpath = tr["f_topo_first_Hz"] + (tr["f_topo_last_Hz"] - tr["f_topo_first_Hz"]) * (t - ts / 2) / (ts * (ns - 1))
    j0 = np.array([int(np.argmin(np.abs(fs - f))) for f in fpath])
    offs = [o for o in range(-int(150 / df), int(150 / df) + 1) if abs(o) >= int(20 / df) or o == 0]
    for p in ("XX", "YY"):
        P = z[p].astype(float); Pn = P / np.median(P, axis=1, keepdims=True) - 1; nF = Pn.shape[1]
        vals = {o: sum(Pn[k, j0[k] + o - 3:j0[k] + o + 4].mean() for k in range(nT) if 3 <= j0[k] + o < nF - 3) for o in offs}
        nul = np.array([vals[o] for o in offs if o != 0])
        per[p][s] = {o: (vals[o] - nul.mean()) / nul.std() for o in offs}
out = {}
for p in ("XX", "YY"):
    offs = list(per[p][ON[0]]); c = {o: sum(per[p][s][o] for s in ON) - sum(per[p][s][o] for s in OFF) for o in offs}
    nul = np.array([c[o] for o in offs if o != 0])
    out[p] = {"per_scan_z": {s: round(float(per[p][s][0]), 2) for s in ON + OFF}, "contrast_z": round(float((c[0] - nul.mean()) / nul.std()), 2), "frac_null_ge": round(float((nul >= c[0]).mean()), 3)}
    print(p, out[p])
json.dump(out, open(H / "out/c03_polsplit.json", "w"), indent=1)
