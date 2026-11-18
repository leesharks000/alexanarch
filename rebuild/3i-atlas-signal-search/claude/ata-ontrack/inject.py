#!/usr/bin/env python3
"""Injection check for ontrack.py: on one unit's real ON data, add tones that follow the comet (k=1) and tones fixed in
receiver frequency (k=0), at fixed reference positions and amplitudes, then run the identical search.
Amplitude a is in units of each row's robust sigma of P/base, spread over the integration's drift (exposure smear,
32 sub-steps) with a Gaussian of 0.6 native bins. Positions are fixed before the search; zero amplitude is the identity."""
import sys, json, numpy as np, concurrent.futures as cf
import ontrack as o
sub, c = sys.argv[1], int(sys.argv[2])
f0 = o.FCH1[sub] + c * 0.5e6
with cf.ThreadPoolExecutor(2) as ex:
    fut = {sc: ex.submit(o.read, sc, sub, 0, c) for sc in o.SCAN_IDS}
    raw = {sc: fut[sc].result()[0].astype(np.float64) for sc in o.SCAN_IDS}
POS = [30000, 60000, 90000, 120000, 150000, 180000, 210000, 240000]
AMPS = [0.0, 0.25, 0.5, 1.0]          # per-integration peak, in row sigma
# layout: pos[i] gets (kind, amp) = comet for even i, fixed for odd i; amplitudes cycle
plan = [(p, "comet" if i % 2 == 0 else "fixed", AMPS[(i // 2) % 4]) for i, p in enumerate(POS)]
bins = np.arange(o.NCH)


def add(P, sc):
    P = P.copy()
    blk = np.median(P.reshape(19, o.NCH // 1024, 1024), axis=2)
    xc = (np.arange(o.NCH // 1024) + 0.5) * 1024
    base = np.stack([np.interp(bins, xc, b) for b in blk])
    r = P / base - 1
    sig = 1.4826 * np.median(np.abs(r - np.median(r, axis=1, keepdims=True)), axis=1)
    for p, kind, a in plan:
        if a == 0:
            continue
        k = 1.0 if kind == "comet" else 0.0
        g = f0 + p * o.FOFF
        for i in range(19):
            prof = np.zeros(o.NCH)
            for s in range(32):
                t = o.TMID[sc][i] + ((s + 0.5) / 32 - 0.5) * o.TSAMP / 86400
                rvk = o.RV0 + k * (float(o.RV(t)) - o.RV0)
                kk = (g * (1 - rvk / o.C) / (1 - o.RV0 / o.C) - f0) / o.FOFF
                lo, hi = int(kk) - 4, int(kk) + 5
                x = bins[lo:hi]; prof[lo:hi] += np.exp(-0.5 * ((x - kk) / 0.6) ** 2)
            prof /= prof.max() if prof.max() > 0 else 1
            P[i] += a * sig[i] * base[i] * prof
    return P


Z = {sc: o.normalize(add(raw[sc], sc))[0] for sc in o.SCAN_IDS}
res = o.search(Z, f0)
out = []
for p, kind, a in plan:
    row = {"pos": p, "kind": kind, "amp": a}
    for k in (1.0, 0.0, -1.0):
        T, Traw, S, v, Tres, dbest, Thalf = res[k]
        row[f"T_k{k:g}"] = round(float(T[p - 2:p + 3].max()), 2)
        row[f"Tres_k{k:g}"] = round(float(Tres[p - 2:p + 3].max()), 2)
        row[f"Thalf_k{k:g}"] = round(float(Thalf[p - 2:p + 3].max()), 2)
        if k == 1.0:
            row["S_comet"] = [round(float(x), 2) for x in S[:, p - 1:p + 2].max(axis=1)]
    out.append(row)
ctrl = max(float(res[k][0].max()) for k in o.KS if k not in (1.0, 0.0))
print(json.dumps({"unit": [sub, c], "control_max_T": round(ctrl, 2), "comet_max_T": round(float(res[1.0][0].max()), 2), "rows": out}, indent=1))
