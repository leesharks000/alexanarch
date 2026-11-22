"""PLAN-HM13 B4: persistence of scan-average features along each path at C08-C13, ATA July 3.  python3 hm13b4.py -> hm13b4.json"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "look_hm13.json")))["runs"]
T = json.load(open(os.path.join(HERE, "targets_hm13.json")))
LAB = ["comet", "comet_swap", "flipped", "flipped_swap", "topo", "topo_swap"]
def persist(pts):   # pts: (off_Hz, scan); single linkage at 4 Hz; persistence = distinct scans in a cluster
    pts = sorted(pts); best, cl = (0, None), []
    for p in pts + [(float("inf"), None)]:
        if cl and p[0] - cl[-1][0] > 4:
            n = len({s for _, s in cl})
            if n > best[0]: best = (n, [round(cl[0][0], 1), round(cl[-1][0], 1)])
            cl = []
        cl.append(p)
    return best
out = {"plan": "PLAN-HM13.md", "targets": {}}
for tn in T:
    runs = {k: v for k, v in L.items() if k.endswith("|" + tn) and "paths" in v}
    errs = [k for k, v in L.items() if k.endswith("|" + tn) and "paths" not in v]
    r = {"n_scans": len({k.split("|")[1] for k in runs}), "errors": errs, "labels": {}}
    for lab in LAB:
        pts = [(f["off_Hz"], k.split("|")[1]) for k, v in runs.items() for f in v["paths"].get(lab, []) if f["kind"] == "avg"]
        n, span = persist(pts); r["labels"][lab] = {"n_avg_features": len(pts), "max_persistence": n, "cluster_Hz": span}
    others = max(r["labels"][l]["max_persistence"] for l in LAB if l != "comet")
    r["lead"] = bool(r["labels"]["comet"]["max_persistence"] >= 3 and others <= 2)
    out["targets"][tn] = r
json.dump(out, open(os.path.join(HERE, "hm13b4.json"), "w"), indent=1)
for tn, r in out["targets"].items(): print(tn, r["n_scans"], {l: r["labels"][l]["max_persistence"] for l in LAB}, "LEAD" if r["lead"] else "")
