"""PLAN-M4b events: drift-search hits associated across the six scans along their drift tracks.
python3 mdhits.py CC [TAG]  -> JSON on stdout"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
sys.path.insert(0, os.path.join(HERE, "M4b")); import mdrift
Z_HIT, Z_VETO, K = 10.0, 5.0, 0.5
SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
TROW = dm.INT * dm.N * dm.TBIN; SPAN = (mdrift.NR - 1) * TROW
cc = int(sys.argv[1]); TAG = sys.argv[2] if len(sys.argv) > 2 else ""
D = {s: np.load(os.path.join(HERE, "out3", f"cc{cc:02d}_{s}{TAG}.npz")) for s in SC}
fc = float(D["0013"]["fc"]); T0 = {s: float(D[s]["t"][0]) * 86400.0 for s in SC}
MZ = {(s, L): D[s][f"L{L}_maxz"].astype(np.float32) for s in SC for L in mdrift.LEVELS}


def peaks(s, L):
    idx, z, d = D[s][f"L{L}_idx"], D[s][f"L{L}_z"], D[s][f"L{L}_d"]; k = z >= Z_HIT; idx, z, d = idx[k], z[k], d[k]
    out = []; o = np.argsort(-z); used = set()
    for i in o:
        if any(abs(int(idx[i]) - u) <= 2 for u in used): continue
        used.add(int(idx[i])); out.append((int(idx[i]), float(z[i]), int(d[i])))
    return out


def along(c, d, s, s2, L):
    rate = d / SPAN; dt = T0[s2] - T0[s]; cp = c + rate * dt
    W = 3 + int(np.ceil(abs(dt) / SPAN)) + int(np.ceil(K * abs(rate * dt)))
    m = MZ[(s2, L)]; a, b = max(int(np.floor(cp)) - W, 0), min(int(np.ceil(cp)) + W + 1, len(m))
    return float(m[a:b].max()) if b > a else 0.0


def events(on, off):
    ev = []
    for s in on:
        for L in mdrift.LEVELS:
            for c, z, d in peaks(s, L):
                o = {v: along(c, d, s, v, L) for v in off}
                if max(o.values()) >= Z_VETO: continue
                n = {v: along(c, d, s, v, L) for v in on if v != s}
                ev.append({"scan": s, "level": L, "cell": c, "z": round(z, 2),
                           "mhz_topo": (fc - ((c + 0.5) * L - dm.N // 2) * dm.DF) / 1e6,
                           "hz_per_s": -d * L * dm.DF / SPAN, "off_along": {k: round(v, 2) for k, v in o.items()},
                           "on_along": {k: round(v, 2) for k, v in n.items()},
                           "cls": "A" if min(n.values()) >= Z_VETO else "B"})
    ev.sort(key=lambda e: -e["z"]); merged = []
    for e in ev:   # one event per signal: the same scan within 134 Hz at any level is the same event
        if any(m["scan"] == e["scan"] and abs(m["mhz_topo"] - e["mhz_topo"]) < 134e-6 for m in merged): continue
        merged.append(e)
    return merged


real = events(ON, OFF); ctrl = events(OFF, ON)
print(json.dumps({"plan": open(os.path.join(HERE, "PLAN-M4b.sha256")).read().split() if os.path.exists(os.path.join(HERE, "PLAN-M4b.sha256")) else None,
                  "cc": cc, "tag": TAG, "fc_mhz": fc / 1e6, "thresholds": {"Z_HIT": Z_HIT, "Z_VETO": Z_VETO, "K": K},
                  "n": {"A": sum(e["cls"] == "A" for e in real), "B": sum(e["cls"] == "B" for e in real)},
                  "control_n": {"A": sum(e["cls"] == "A" for e in ctrl), "B": sum(e["cls"] == "B" for e in ctrl)},
                  "events": real[:30], "control_top": ctrl[:10]}, indent=1))
