"""EXPLORATORY (not frozen), 2026-11-06: a closer look at two deep-space-band channels after the frozen run.
blc72 cc61 (8446.29 MHz: true ON 6, ON-swap 5 above every false frame) and blc72 cc63 (8440.43 MHz: true ON 0).
Uses the run's own cf.py unchanged (imported with its stem). Writes look.json and cutouts.png.
    python3 look.py <dsn dir> <raw dir> <out dir>"""
import sys, json, importlib.util, numpy as np
D, RAW, OUT = sys.argv[1:4]
res = {}
mods = {}
for cc in (61, 63):
    stem = f"{RAW}/blc72_cc{cc}"
    sys.argv = ["cf.py", stem, "2.5", "2.0"]
    spec = importlib.util.spec_from_file_location(f"cf{cc}", f"{D}/cf.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    mods[cc] = m
    r = {"health": {}, "single_scan_tail": {}}
    for s in m.ON + m.OFF:
        x = np.load(f"{stem}_{s}.npy", mmap_mode="r")
        a = np.asarray(x, np.float64)
        med = np.median(a, axis=0)
        rowp = a.mean(axis=1)
        r["health"][s] = {"shape": list(a.shape), "zeros_frac": float(np.mean(a == 0)), "nan_frac": float(np.mean(~np.isfinite(a))),
                          "bandpass_p01_p99": [float(np.percentile(med, 1)), float(np.percentile(med, 99))],
                          "bandpass_edge_to_centre": [float(np.median(med[:20000]) / np.median(med[500000:540000])), float(np.median(med[-20000:]) / np.median(med[500000:540000]))],
                          "row_power_cv": float(rowp.std() / rowp.mean())}
        z, fr = m.tracked(s)
        zz = z[z != 0]
        r["single_scan_tail"][s] = {"n_ge_2p5": int(np.sum(zz >= 2.5)), "frac_ge_2p5": float(np.mean(zz >= 2.5)),
                                    "frac_lt_2p0": float(np.mean(zz < 2.0)), "kurtosis_excess": float(((zz - zz.mean()) ** 4).mean() / zz.var() ** 2 - 3)}
    # the count's sensitivity to the gate (true frame only)
    sens = {}
    for zon in (2.3, 2.4, 2.5, 2.6):
        m.Z_ON = zon; sens[str(zon)] = m.coincidences(0.0)
    m.Z_ON = 2.5
    r["true_count_by_gate"] = sens
    # the pairwise ON coincidences (two of three) in the true frame, at the gate
    r["pairs"] = {}
    zs = {s: m.tracked(s) for s in m.ON}
    ref = zs[m.ON[0]][1]; foff = m.foff_hz
    al = {}
    for s in m.ON:
        idx = np.rint((zs[s][1] - ref[0]) / foff).astype(int); a = np.full(len(zs[s][0]) + 2000, -99.0)
        ok = (idx + 1000 >= 0) & (idx + 1000 < len(a)); a[idx[ok] + 1000] = np.maximum(a[idx[ok] + 1000], zs[s][0][ok]); al[s] = a
    mf = lambda a: np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
    for i, s in enumerate(m.ON):
        for t in m.ON[i + 1:]:
            r["pairs"][f"{s}&{t}"] = int(np.sum((mf(al[s]) >= 2.5) & (mf(al[t]) >= 2.5)))
    res[f"blc72_cc{cc}"] = r

# cutouts: each cc61 true-frame cluster, +-60 fine channels around its topocentric frequency, every scan, normalised rows
dj = json.load(open(f"{D}/dsn.json"))["channels"]["blc72_cc61"]["true_on_channels"]
seen, cl = [], []
for c in dj:
    if all(abs(c["f_rest_MHz"] - x) > 1e-5 for x in seen): seen.append(c["f_rest_MHz"]); cl.append(c)
m = mods[61]
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
json.dump(res, open(f"{OUT}/look.json", "w"), indent=1)
fig, ax = plt.subplots(len(cl), 6, figsize=(12, 2.0 * len(cl)))
for i, c in enumerate(cl):
    for j, s in enumerate(m.ON + m.OFF):
        x = np.load(f"{RAW}/blc72_cc61_{s}.npy", mmap_mode="r"); h = m.H[s]
        nt = x.shape[0]; tt = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0; v = m.deldot(tt)
        F = c["f_rest_MHz"]; kk = np.rint((F * (1 - v / m.C) - h["fch1_cc"]) / h["foff"]).astype(int)  # the comet path, per row
        med = np.median(np.asarray(x, np.float64), axis=0)
        sl = np.array([np.asarray(x[r, kk[r] - 60:kk[r] + 61], np.float64) / med[kk[r] - 60:kk[r] + 61] - 1 for r in range(nt)])
        ax[i, j].imshow(sl, aspect="auto", cmap="viridis", vmin=-0.2, vmax=0.4, origin="lower")
        ax[i, j].set_xticks([]); ax[i, j].set_yticks([])
        if i == 0: ax[i, j].set_title(("ON " if s in m.ON else "OFF ") + s, fontsize=8)
    ax[i, 0].set_ylabel(f"{c['f_rest_MHz']:.4f}", fontsize=7)
fig.suptitle("blc72 cc61: the six true-frame clusters, +-60 fine channels (+-168 Hz) along the comet path (centre column); rows = time (49 x 6.1 s)", fontsize=9)
fig.tight_layout(); fig.savefig(f"{OUT}/cutouts.png", dpi=110)
json.dump(res, open(f"{OUT}/look.json", "w"), indent=1)
print(json.dumps(res, indent=1)[:4000])
