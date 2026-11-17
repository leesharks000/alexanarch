"""c03hr_aperture.py — C03 along the comet track at 0.70 Hz, with apertures of 3, 7 and 11 bins (2.1, 4.9, 7.7 Hz),
scored against parallel tracks offset by >= 20 Hz; ON sum minus OFF sum against the same contrast on the parallel tracks."""
import numpy as np, json, pathlib
H = pathlib.Path(__file__).resolve().parent
TR = {s["scan"]: s for s in {c["id"]: c for c in json.load(open(H.parent / "oh13/oh13_candidates.json"))["candidates"]}["C03"]["scans"]}
ON, OFF = ["0013", "0015", "0017"], ["0014", "0016", "0018"]; out = {}
per = {}
for s in ON + OFF:
    z = np.load(H / f"out/zoom_C03hr_scan{s}.npz"); I = (z["XX"] + z["YY"]).astype(float); fs = z["fsky"]; dt = float(z["dt"]); df = float(z["df"])
    In = I / np.median(I, axis=1, keepdims=True) - 1; nT, nF = In.shape; t = (np.arange(nT) + 0.5) * dt
    tr = TR[s]; ts, ns = tr["tsamp_s"], tr["n_steps"]
    fpath = tr["f_topo_first_Hz"] + (tr["f_topo_last_Hz"] - tr["f_topo_first_Hz"]) * (t - ts / 2) / (ts * (ns - 1))
    j0 = np.array([int(np.argmin(np.abs(fs - f))) for f in fpath])
    offs = [o for o in range(-int(150 / df), int(150 / df) + 1) if abs(o) >= int(20 / df) or o == 0]
    per[s] = {}
    for ap in (3, 7, 11):
        h = ap // 2; vals = {}
        for o in offs:
            acc = 0.0
            for k in range(nT):
                j = j0[k] + o
                if h <= j < nF - h: acc += In[k, j - h:j + h + 1].mean()
            vals[o] = acc
        nul = np.array([vals[o] for o in offs if o != 0]); sd = nul.std()
        per[s][ap] = {o: vals[o] / sd for o in offs}
for ap in (3, 7, 11):
    offs = list(per[ON[0]][ap]); c = {o: sum(per[s][ap][o] for s in ON) - sum(per[s][ap][o] for s in OFF) for o in offs}
    nul = np.array([c[o] for o in offs if o != 0])
    out[ap] = {"per_scan_z": {s: round(float((per[s][ap][0] - np.mean([per[s][ap][o] for o in offs if o != 0])) ), 2) for s in ON + OFF},
               "contrast_z": round(float((c[0] - nul.mean()) / nul.std()), 2), "frac_null_ge": round(float((nul >= c[0]).mean()), 3), "n_null": len(nul)}
    print("aperture", ap, out[ap])
json.dump(out, open(H / "out/c03hr_aperture.json", "w"), indent=1)
