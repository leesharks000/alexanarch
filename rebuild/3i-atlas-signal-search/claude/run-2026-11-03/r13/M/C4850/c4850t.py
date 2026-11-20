"""PLAN-C4850 targets.  python3 c4850t.py CC -> targets_ccCC.json"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.dirname(HERE)
cc = int(sys.argv[1]); FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6
d = json.load(open(os.path.join(M, "M4b", "events", f"cc{cc:02d}.json"))); assert abs(d["fc_mhz"] * 1e6 - FC) < 1
T = [dict(kind="E", f=e["mhz_topo"] * 1e6, scan=e["scan"], cls=e["cls"], z=e["z_local"], hz_per_s=e["hz_per_s"], level=e["level"]) for e in d["events"]]
T += [dict(kind="Q", f=e["mhz_topo"] * 1e6, scan=e["scan"], cls=e["cls"], z=e["z_local"], hz_per_s=e["hz_per_s"], level=e["level"]) for e in d["control_top"]]
rng = np.random.default_rng(4850); lo, hi = FC - 1.35e6, FC + 1.35e6; F = np.array([t["f"] for t in T]); n = 0
while n < 60:
    f = rng.uniform(lo, hi)
    if np.min(np.abs(F - f)) > 500: T.append(dict(kind="X", f=f)); n += 1
json.dump(dict(cc=cc, fc=FC, targets=T), open(os.path.join(HERE, f"targets_cc{cc}.json"), "w"), indent=1)
print(cc, {k: sum(t["kind"] == k for t in T) for k in "EQX"})
