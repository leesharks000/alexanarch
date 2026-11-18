"""Check on part F, written after F's result (2026-11-18): is the false-frame null exchangeable with the true frame?
For each frame j (0 = true), its mean rank among the 41 frames within each channel (ties averaged) and its top-4 count, over the
63 L-band channels other than the thirteen's and the 64 S/C/X channels; correlation of false-frame mean rank with |false offset|;
and the thirteen's channel by false-frame distance. Stored rows only.   python3 f_check.py > F_check.txt"""
import json, numpy as np
from scipy.stats import rankdata, spearmanr
C = 299792.458
r11 = np.random.default_rng(11); offs = np.array([0.0] + list(r11.uniform(0.03, 1.0, 40) * r11.choice([-1, 1], 40) * C / 1.42e9))
hz = offs * 1.42e9 / C
L = json.load(open("../lee/lee.json"))["channels"]; LH = json.load(open("../lheld/lheld.json"))["channels"]; O = json.load(open("../ocad/ocad.json"))["channels"]
rowsL = {k: (v["rows"] if v.get("rows") else LH[k]["rows"]) for k, v in L.items() if k != "blc23_cc07"}
rowsO = {k: v["rows"] for k, v in O.items()}
for name, R in (("L63 (without the thirteen's channel)", rowsL), ("SCX64", rowsO)):
    M = np.array([[r["on"] for r in v] for v in R.values()], float); rk = np.array([rankdata(-m, method="average") for m in M])
    mr = rk.mean(0); top = (rk <= 4).sum(0); near = np.argsort(np.abs(hz))[1:7]
    print(name); print("  true frame: mean rank %.2f, top-4 count %d" % (mr[0], top[0]))
    print("  false frames: mean rank %.2f +- %.2f (min %.2f); top-4 count %.2f (max %d)" % (mr[1:].mean(), mr[1:].std(), mr[1:].min(), top[1:].mean(), top[1:].max()))
    rho = spearmanr(np.abs(hz[1:]), mr[1:]); print("  Spearman |offset| vs mean rank, false frames: rho %.3f, p %.2g" % (rho.correlation, rho.pvalue))
    print("  the six false frames nearest the true frame (Hz/s at 1.42 GHz, mean rank, top-4):", [(round(float(hz[j]), 3), round(float(mr[j]), 2), int(top[j])) for j in near])
    print("  true frame's place among the 41 by mean rank: %d; by top-4 count: %d" % (1 + np.sum(mr[1:] < mr[0]), 1 + np.sum(top[1:] > top[0])))
rows = L["blc23_cc07"]["rows"]; print("the thirteen's channel (blc23 cc07), frames by distance: (Hz/s, on, swap)")
print("  ", [(round(float(hz[j]), 3), rows[j]["on"], rows[j]["swap"]) for j in np.argsort(np.abs(hz))[:12]])
