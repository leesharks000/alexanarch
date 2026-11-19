"""PLAN-M4b events: drift-search hits associated across the six scans along their drift tracks.
python3 mdhits.py CC [TAG]  -> JSON on stdout

Calibration (cc30, 2026-11-19) found the drift-search z, scaled by one MAD across the whole coarse channel, unusable where
a broadband emitter occupies part of the band (GLONASS L1 in cc30: ~10^5 cells with z >= 10, concentrated in the occupied
part). The hit statistic is therefore LOCAL: each level's per-cell maximum over drifts is rescaled by the median and MAD of
that maximum in blocks of BLK cells. Hits and vetoes are read on the local statistic; the work is vectorised."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
sys.path.insert(0, os.path.join(HERE, "M4b")); import mdrift
from scipy.ndimage import maximum_filter1d
Z_HIT, Z_VETO, K, BLK = 10.0, 5.0, 0.5, 1024
SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
TROW = dm.INT * dm.N * dm.TBIN; SPAN = (mdrift.NR - 1) * TROW
cc = int(sys.argv[1]); TAG = sys.argv[2] if len(sys.argv) > 2 else ""
D = {s: np.load(os.path.join(HERE, "out3", f"cc{cc:02d}_{s}{TAG}.npz")) for s in SC}
fc = float(D["0013"]["fc"]); T0 = {s: float(D[s]["t"][0]) * 86400.0 for s in SC}


def local(m):
    n = len(m); b = m[: n - n % BLK].reshape(-1, BLK)
    med = np.median(b, axis=1); mad = 1.4826 * np.median(np.abs(b - med[:, None]), axis=1); mad[mad <= 0] = 1
    c = np.arange(BLK // 2, n - n % BLK, BLK)
    return (m - np.interp(np.arange(n), c, med)) / np.interp(np.arange(n), c, mad)


LZ = {(s, L): local(D[s][f"L{L}_maxz"].astype(np.float32)) for s in SC for L in mdrift.LEVELS}
DR = {(s, L): D[s][f"L{L}_drift"].astype(np.int32) for s in SC for L in mdrift.LEVELS}


class RMQ:   # range maximum by sparse table
    def __init__(self, a):
        self.t = [a]; k = 1
        while 2 * k <= len(a):
            p = self.t[-1]; self.t.append(np.maximum(p[:-k], p[k:])); k *= 2
    def q(self, a, b):   # max over [a, b), b > a
        L = b - a; j = np.floor(np.log2(L)).astype(int); out = np.empty(len(a), np.float32)
        for jj in np.unique(j):
            m = j == jj; t = self.t[jj]; out[m] = np.maximum(t[a[m]], t[b[m] - (1 << jj)])
        return out


Q = {k: RMQ(v) for k, v in LZ.items()}


def peaks(s, L):
    z = LZ[(s, L)]; c = np.where((z >= Z_HIT) & (z == maximum_filter1d(z, 5)))[0]
    return c, z[c], DR[(s, L)][c]


def along(c, d, s, s2, L):
    rate = d / SPAN; dt = T0[s2] - T0[s]; cp = c + rate * dt; n = len(LZ[(s2, L)])
    W = 3 + int(np.ceil(abs(dt) / SPAN)) + np.ceil(K * np.abs(rate * dt)).astype(int)
    a = np.clip(np.floor(cp).astype(int) - W, 0, n - 1); b = np.clip(np.ceil(cp).astype(int) + W + 1, 1, n)
    b = np.maximum(b, a + 1)
    return Q[(s2, L)].q(a, b)


def events(on, off):
    ev = []
    for s in on:
        for L in mdrift.LEVELS:
            c, z, d = peaks(s, L)
            if len(c) == 0: continue
            o = np.stack([along(c, d, s, v, L) for v in off]); keep = o.max(axis=0) < Z_VETO
            if not keep.any(): continue
            c, z, d, o = c[keep], z[keep], d[keep], o[:, keep]
            others = [v for v in on if v != s]; n_ = np.stack([along(c, d, s, v, L) for v in others])
            for i in range(len(c)):
                ev.append({"scan": s, "level": L, "cell": int(c[i]), "z_local": round(float(z[i]), 2),
                           "mhz_topo": (fc - ((c[i] + 0.5) * L - dm.N // 2) * dm.DF) / 1e6,
                           "hz_per_s": float(-d[i] * L * dm.DF / SPAN),
                           "off_along": {v: round(float(o[k, i]), 2) for k, v in enumerate(off)},
                           "on_along": {v: round(float(n_[k, i]), 2) for k, v in enumerate(others)},
                           "cls": "A" if n_[:, i].min() >= Z_VETO else "B"})
    ev.sort(key=lambda e: -e["z_local"]); merged = []
    # One event per signal. Calibration round 2 (cc08): a strong drifting line also raises weaker off-track peaks at the coarse
    # resolutions, within the band its own track sweeps during the scan. A weaker event in the same scan whose start lies inside
    # a stronger event's swept band (widened by 134 Hz and by one cell of the stronger event's resolution) is that event's ghost.
    for e in ev:
        lo_hi = lambda m: sorted((m["mhz_topo"], m["mhz_topo"] + m["hz_per_s"] * SPAN / 1e6))
        def ghost(m):
            a, b = lo_hi(m); pad = 134e-6 + m["level"] * dm.DF / 1e6
            return m["scan"] == e["scan"] and a - pad <= e["mhz_topo"] <= b + pad
        if any(ghost(m) for m in merged): continue
        merged.append(e)
    return merged


real = events(ON, OFF); ctrl = events(OFF, ON)
pl = os.path.join(HERE, "PLAN-M4b.sha256")
print(json.dumps({"plan": open(pl).read().split() if os.path.exists(pl) else None,
                  "cc": cc, "tag": TAG, "fc_mhz": fc / 1e6, "thresholds": {"Z_HIT": Z_HIT, "Z_VETO": Z_VETO, "K": K, "BLK": BLK},
                  "n_hits_on": {s: {L: int(len(peaks(s, L)[0])) for L in mdrift.LEVELS} for s in SC},
                  "n": {"A": sum(e["cls"] == "A" for e in real), "B": sum(e["cls"] == "B" for e in real)},
                  "control_n": {"A": sum(e["cls"] == "A" for e in ctrl), "B": sum(e["cls"] == "B" for e in ctrl)},
                  "events": real[:40], "control_top": ctrl[:15]}, indent=1))
