"""Does the comet-frame excess need scan 0017? Same procedure and null as swapnull.py (40 false frames, seed 11); for each frame the
ON rule z >= 2.5 is applied to each subset of the ON scans, OFF < 2.0 in all three OFF scans, 10 Hz clusters. If 0017 was off target
(header 16.1 arcmin from the comet, GBT FWHM ~7.6 arcmin at 1667 MHz, beam gain ~3e-6 there), comet-locked power is absent from it, and
subsets that include it should carry no excess beyond what the false frames give. C03's per-scan z is listed in every frame.
    python3 c03_scan17.py"""
import json, itertools, numpy as np
src = open("autonomous.py").read().split("rng = np.random.default_rng(7)")[0]
exec(compile(src, "autonomous.py", "exec"))
vf = FRAMES["comet (uncompensated)"]
rng = np.random.default_rng(11)
offs = [0.0] + list(rng.uniform(0.03, 1.0, 40) * rng.choice([-1, 1], 40) * C / 1.42e9)
subsets = [s for k in (1, 2, 3) for s in itertools.combinations(ON, k)]
F03 = 1665.633777e6
rows = []
for i, dv in enumerate(offs):
    A, ref = align({s: tracked(s, vf, dv) for s in ON + OFF})
    off_ok = np.all([A[s] < Z_OFF for s in OFF], axis=0)
    r = {"dv": float(dv)}
    for sub in subsets:
        ok = off_ok & np.all([A[s] >= Z_ON for s in sub], axis=0)
        r["+".join(sub)] = clusters(np.where(ok)[0])
    if i == 0:
        j = int(round((F03 - ref[0]) / foff_hz)) + 1000
        w = slice(j - 3, j + 4)
        r["C03_z"] = {s: round(float(A[s][w].max()), 2) for s in ON + OFF}
    rows.append(r); print(i, r, flush=True)
json.dump(rows, open("raw/OH_c03_scan17.json", "w"), indent=1)
t, N = rows[0], rows[1:]
for sub in subsets:
    k = "+".join(sub); v = np.array([x[k] for x in N])
    print(f"{k:16s} true {t[k]:4d} | false mean {v.mean():7.2f} sd {v.std():6.2f} max {v.max():4d} | frac >= true {np.mean(v >= t[k]):.3f}")
