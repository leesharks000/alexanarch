"""c03hr.py — C03 at 0.70 Hz x 1.43 s (2^22-point spectra) in all six scans, full Stokes.
1. Drift search: for drift rates -1.0..+1.0 Hz/s (0.005 steps) and every start bin in the 800 Hz band, sum the normalized
   power along the line; per scan, the best (f_mid, rate) and its z against all (f, rate) cells.
2. The predicted tracks: comet frame (from ../oh13, f_topo first->last) and receiver-fixed (1665644304.70 Hz, from the
   ChatGPT S-band audit): score at each, against parallel tracks offset by >= 20 Hz.
3. The line along the comet track, stacked: profile at 0.70 Hz, XX and YY separately, V/I.
Writes out/c03hr.json."""
import numpy as np, json, pathlib
H = pathlib.Path(__file__).resolve().parent
J = {c["id"]: c for c in json.load(open(H.parent / "oh13/oh13_candidates.json"))["candidates"]}["C03"]
TRACK = {s["scan"]: s for s in J["scans"]}
ROLE = {"0013": "ON", "0015": "ON", "0017": "ON", "0014": "OFF", "0016": "OFF", "0018": "OFF"}
RX = 1665644304.702512
res = {}
rates = np.arange(-1.0, 1.0001, 0.005)
for s in ["0013", "0014", "0015", "0016", "0017", "0018"]:
    f = H / f"out/zoom_C03hr_scan{s}.npz"
    if not f.exists(): continue
    z = np.load(f); XX, YY, IM, fs = (z[k].astype(float) for k in ("XX", "YY", "ImXY", "fsky")); dt = float(z["dt"]); df = float(z["df"])
    I = XX + YY; V = -2 * IM
    In = I / np.median(I, axis=1, keepdims=True) - 1
    nT, nF = In.shape; t = (np.arange(nT) + 0.5) * dt; tm = t.mean()
    # drift search
    best = None; grid = np.zeros((len(rates), nF))
    for ri, r in enumerate(rates):
        sh = np.rint(r * (t - tm) / df).astype(int)
        acc = np.zeros(nF)
        for k in range(nT):
            acc += np.roll(In[k], -sh[k])
        grid[ri] = acc
    edge = int(np.ceil(abs(rates).max() * (t[-1] - tm) / df)) + 2
    g = grid[:, edge:nF - edge]; mu = np.median(g); sd = 1.4826 * np.median(np.abs(g - mu))
    ri, fi = np.unravel_index(np.argmax(g), g.shape)
    bestz = (g[ri, fi] - mu) / sd; fbest = fs[fi + edge]
    # predicted tracks
    tr = TRACK[s]; ts, ns = tr["tsamp_s"], tr["n_steps"]
    def score(fpath):
        vals = []
        for off in range(-int(150 / df), int(150 / df) + 1):
            acc = 0.0
            for k in range(nT):
                j = int(np.argmin(np.abs(fs - fpath(t[k])))) + off
                if 1 <= j < nF - 1: acc += In[k, j - 1:j + 2].mean()
            vals.append(acc)
        vals = np.array(vals); c = len(vals) // 2
        null = np.concatenate([vals[:c - int(20 / df)], vals[c + int(20 / df) + 1:]])
        return float((vals[c] - np.median(null)) / (1.4826 * np.median(np.abs(null - np.median(null))))), vals
    comet = lambda tt: tr["f_topo_first_Hz"] + (tr["f_topo_last_Hz"] - tr["f_topo_first_Hz"]) * (tt - ts / 2) / (ts * (ns - 1))
    zc, vc = score(comet); zr, vr = score(lambda tt: RX)
    # stacked profile along the comet track
    prof = np.zeros(41); pxx = np.zeros(41); pyy = np.zeros(41); pv = np.zeros(41); pi_ = np.zeros(41)
    for k in range(nT):
        j = int(np.argmin(np.abs(fs - comet(t[k]))))
        if 20 <= j < nF - 20:
            prof += In[k, j - 20:j + 21]
            pxx += XX[k, j - 20:j + 21] / np.median(XX[k]); pyy += YY[k, j - 20:j + 21] / np.median(YY[k])
            pv += V[k, j - 20:j + 21]; pi_ += I[k, j - 20:j + 21]
    res[s] = {"role": ROLE[s], "drift_search_best": {"rate_Hz_s": round(float(rates[ri]), 3), "f_mid_Hz": round(float(fbest), 2), "z": round(float(bestz), 2)},
              "z_comet_track": round(zc, 2), "z_receiver_fixed": round(zr, 2), "comet_rate_Hz_s": round((tr["f_topo_last_Hz"] - tr["f_topo_first_Hz"]) / (ts * (ns - 1)), 4),
              "profile_I": [round(float(x / nT), 4) for x in prof], "profile_XX": [round(float(x / nT - 1), 4) for x in pxx], "profile_YY": [round(float(x / nT - 1), 4) for x in pyy],
              "V_over_I_centre3": round(float(pv[19:22].sum() / pi_[19:22].sum()), 4), "df_Hz": df, "dt_s": dt, "nT": nT}
    r = res[s]
    print(s, r["role"], "best", r["drift_search_best"], "| comet z", r["z_comet_track"], "| rx-fixed z", r["z_receiver_fixed"], "| V/I", r["V_over_I_centre3"])
    print("    I profile (centre ±5 bins):", r["profile_I"][15:26])
json.dump(res, open(H / "out/c03hr.json", "w"), indent=1)
