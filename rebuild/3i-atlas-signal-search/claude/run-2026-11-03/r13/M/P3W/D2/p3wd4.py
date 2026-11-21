"""PLAN-P3W-D4: the pair (422, 440) in all six families in all six scans, full length.  python3 p3wd4.py"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lean
P = lean.P; out = {}
for s in P.SCANS:
    PX, _, PY, _ = lean.load_full(s); out[s] = {}
    for f in P.FAMS:
        r = lean.at_pair_lean(PX, PY, f, 422, 440, 557)
        rng = np.random.default_rng(557); n = len(PX) - lean.W; Pq = {"X": PX, "Y": PY}; a, b, cj = lean.FMAP[f]; sa = []
        for _ in range(P.NSUR):
            LX = rng.integers(0, lean.W + 1, size=lean.SEG); LY = rng.integers(0, lean.W + 1, size=lean.SEG); L = {"X": LX, "Y": LY}
            sa.append(lean.pair_val(Pq[a][L[a][422]:L[a][422] + n, 422], Pq[b][L[b][440]:L[b][440] + n, 440], f, cj))
        r["rank_above"] = int(sum(x < r["A"] for x in sa)); out[s][f] = r
    del PX, PY
    print(s, {f: (round(out[s][f]["A"], 4), round(out[s][f]["sur_median"], 4), round(out[s][f]["sur_max"], 4), out[s][f]["rank_above"]) for f in P.FAMS}, flush=True)
json.dump(out, open(os.path.join(HERE, "p3wd4_pair.json"), "w"), indent=1)
