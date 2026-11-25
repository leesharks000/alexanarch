"""POST HOC (written after R2 and R6 were read; not part of the frozen plan). Two checks on the three targets that cleared 95%:
(a) the ON/OFF contrast at fixed topocentric frequency in 10 kHz steps across the hydrogen line (blc24), to see whether S3's excess
    follows the Galactic H I profile; (b) the contrast at the same distance from the coarse-channel edge as OH1665_v10.51 (67 kHz below
    the top edge) and OH1612_v67.54 (199 kHz below), in the target's channel and its two neighbours, top and bottom edges.
    python3 posthoc_edges_hi.py"""
import json, os, numpy as np
import r2_r6_lines_a1 as m
HERE = os.path.dirname(os.path.abspath(__file__)); out = {}
ZERO = lambda t: 0.0
# (a)
data = {sc: m.load("blc24", sc, 1420.6) for sc in m.SCANS}
prof = []
for f in np.arange(1419.9, 1421.3, 0.01):
    P = {sc: m.tracked(x, fq, t, f, ZERO, 5e-3)[0] for sc, (_, x, fq, t) in data.items()}
    prof.append([round(float(f), 3)] + [P[on] / P[off] - 1 for on, off in m.PAIRS] + [P["0013"]])
out["hi_profile"] = {"columns": ["f_topo_MHz", "c_0013_0014", "c_0015_0016", "c_0017_0018", "power_0013"], "rows": prof}
json.dump(out, open(os.path.join(HERE, "posthoc.json"), "w"), indent=1); del data
# (b)
edges = {}
for name, f_t, d in (("OH1665_v10.51", 1665.46019, None), ("OH1612_v67.54", 1612.59422, None)):
    k0 = int((f_t - 1501.46484375) // 2.9296875); res = {}
    for k in (k0 - 1, k0, k0 + 1):
        lo, hi = 1501.46484375 + k * 2.9296875, 1501.46484375 + (k + 1) * 2.9296875
        dist = (1501.46484375 + (k0 + 1) * 2.9296875) - f_t
        data = {sc: m.load("blc23", sc, lo + 1.0) for sc in m.SCANS}
        for tag, f in (("top", hi - dist), ("bottom", lo + dist)):
            P = {sc: m.tracked(x, fq, t, f, m.VCOM, 5e-3 * f / m.H)[0] for sc, (_, x, fq, t) in data.items()}
            res[f"ch{k}_{tag}"] = {"f_MHz": f, "contrast": [P[on] / P[off] - 1 for on, off in m.PAIRS]}
            res[f"ch{k}_{tag}"]["mean"] = float(np.mean(res[f"ch{k}_{tag}"]["contrast"]))
            print(name, k, tag, "%.5f" % f, "%.4f" % res[f"ch{k}_{tag}"]["mean"], flush=True)
        del data
    edges[name] = {"edge_distance_MHz": dist, "bands": res}
    out["edges"] = edges; json.dump(out, open(os.path.join(HERE, "posthoc.json"), "w"), indent=1)
print("DONE")
