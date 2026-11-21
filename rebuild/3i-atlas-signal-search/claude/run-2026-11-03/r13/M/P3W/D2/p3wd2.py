"""PLAN-P3W-D2: P3W-D's run on the full-length target slice; read with P3W-D's gates.  python3 p3wd2.py SCAN | read"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import p3w as P, p3wd as D                                   # p3wd patches P.run and P.at_pair with the no-wrap shift null


def full(s, q):
    a = np.load(os.path.join(HERE, f"ser_{s}.npy"), mmap_mode="r")[q]; return a[:, 0].astype(np.float64) + 1j * a[:, 1].astype(np.float64)


def scan(s):
    i = P.SCANS.index(s); r, _, _ = D.run(full(s, 0), full(s, 1), 31625 + 100 * i)
    k, l = 217, 293; PX, _ = P.phasors(full(s, 0)); PY, _ = P.phasors(full(s, 1))
    A = P.stats(D.window(PX), D.window(PY))["Y+"][k, l]; del PX, PY
    out = {"scan": s, "target": r, "followup_Yplus_217_293": float(A)}
    print(s, {f: (r[f]["p"], r[f]["pair"], round(r[f]["score"] / r[f]["sur_max_median"], 2)) for f in P.FAMS}, "Y+[217,293]", round(float(A), 4), flush=True)
    json.dump(out, open(os.path.join(HERE, f"p3wd2_{s}.json"), "w"), indent=1)


def read():
    R = {s: json.load(open(os.path.join(HERE, f"p3wd2_{s}.json"))) for s in P.SCANS}; gates = {}
    for s in ("0013", "0015", "0017"):
        for f in P.FAMS:
            r = R[s]["target"][f]
            if r["p"] > 0.05: continue
            k, l = r["pair"]; zx, zy = full(s, 0), full(s, 1)
            g = {"scan": s, "family": f, "pair": [k, l], "p": r["p"], "halves": P.half_p(zx, zy, f, k, l)}
            i = P.SCANS.index(s); offs = [P.SCANS[i - 1]] + ([P.SCANS[i + 1]] if i + 1 < 6 else []); g["off"] = {}
            for o in offs: g["off"][o] = D.at_pair(full(o, 0), full(o, 1), f, k, l, 555)
            d = np.load(os.path.join(P.N1625, f"crops_{s}.npz"))
            g["ctrl"] = {sl: D.at_pair(P.series(d, f"{sl}_X"), P.series(d, f"{sl}_Y"), f, k, l, 556) for sl in ("ctrl25k", "hidrift")}
            exc = r["score"] - r["sur_at_pair_median"]; oexc = max(v["A"] - v["sur_median"] for v in g["off"].values())
            g["verdict"] = dict(halves=all(h["p"] <= 0.01 for h in g["halves"]), off_not_above=all(v["A"] <= v["sur_max"] for v in g["off"].values()),
                                excess_ratio=(exc / oexc) if oexc > 0 else None, controls_quiet=all(v["A"] <= v["sur_max"] for v in g["ctrl"].values()))
            v = g["verdict"]; g["lead"] = bool(v["halves"] and v["off_not_above"] and (v["excess_ratio"] is None or v["excess_ratio"] >= 4) and v["controls_quiet"])
            gates[f"{s}{f}"] = g; print(json.dumps(g)[:900], flush=True)
    n = sum(1 for s in P.SCANS for f in P.FAMS if R[s]["target"][f]["p"] <= 0.05)
    print("families at p<=0.05 across 36 (6 scans x 6):", n, "| expected about 1.8")
    print("follow-up Y+[217,293]:", {s: round(R[s]["followup_Yplus_217_293"], 4) for s in P.SCANS})
    json.dump(gates, open(os.path.join(HERE, "p3wd2_gates.json"), "w"), indent=1)


if __name__ == "__main__":
    read() if sys.argv[1] == "read" else scan(sys.argv[1])
