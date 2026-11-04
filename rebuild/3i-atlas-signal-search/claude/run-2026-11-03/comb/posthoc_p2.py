"""Post hoc (not in PLAN-comb.md): P2 recomputed without C01 and C02, from comb.json. python3 posthoc_p2.py"""
import json, numpy as np
from scipy.stats import spearmanr
o = json.load(open("comb.json")); R = [r for r in o["P2"]["rows"] if r["id"] not in ("C01", "C02")]
z = np.array([r["z"] for r in R]); W = np.array([r["W"] for r in R]); sc = np.array([r["scan"] for r in R])
rho = spearmanr(z, W).correlation; rng = np.random.default_rng(41); nul = []
for _ in range(10000):
    Wp = W.copy()
    for s in set(sc): ix = np.where(sc == s)[0]; Wp[ix] = Wp[rng.permutation(ix)]
    nul.append(spearmanr(z, Wp).correlation)
print("rho", round(float(rho), 4), "p_one_sided", float(np.mean(np.array(nul) >= rho)), "rows with O>0", sum(r["O"] > 0 for r in R))
