"""PLAN-HM13-B2 targets.  python3 hm13b2_targets.py -> targets_hm13b2.json
Every saved M4b event of cc21 (E: ON events; Q: role-reversed control_top) and N1625's target, each with the tile holding its
recorded topocentric frequency and the two neighbouring tiles (drifts up to 7.35 Hz/s move a line about 0.77 tile in a scan)."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); M = os.path.normpath(os.path.join(HERE, "../.."))
cc = 21; N = 1 << 20; TBIN = 3.41333333333333e-07; DF = 1 / TBIN / N; FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6; W = 1024
d = json.load(open(os.path.join(M, "M4b", "events", "cc21.json"))); assert abs(d["fc_mhz"] * 1e6 - FC) < 1
def tobin(f): return int(np.rint(N // 2 + (FC - f) / DF - 0.5))
def entry(kind, f, **kw):
    b = tobin(f); t = b // W; return dict(kind=kind, f=f, bin=b, tiles=[x for x in (t - 1, t, t + 1) if 0 <= x < N // W], **kw)
T = [entry("E", e["mhz_topo"] * 1e6, scan=e["scan"], cls=e["cls"], z=e["z_local"], hz_per_s=e["hz_per_s"]) for e in d["events"]]
T += [entry("Q", e["mhz_topo"] * 1e6, scan=e["scan"], cls=e["cls"], z=e["z_local"], hz_per_s=e["hz_per_s"]) for e in d["control_top"]]
T.append(entry("N", 1625.2936106e6, scan="0013", cls="N1625", z=None, hz_per_s=None))
json.dump(dict(cc=cc, fc=FC, tile_bins=W, targets=T), open(os.path.join(HERE, "targets_hm13b2.json"), "w"), indent=1)
print({k: sum(t["kind"] == k for t in T) for k in "EQN"}, "tiles", len({x for t in T for x in t["tiles"]}))
