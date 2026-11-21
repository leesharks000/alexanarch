"""PLAN-OH13R-FD steps 2-3: OH13R's D3, computed as channel 7 streams, for the false-drift selections and their controls, and for
the true-frame candidates and OH13R's 72 controls.  python3 fdstream.py SCAN | check | read"""
import json, os, sys, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from common import *                                     # OH13R's common (frozen): N, DF, FC, TF, NF, W, track, idx, vel_fn, t0, windows, dm
LAGS = (1, 2, 4, 8, 16, 32); c = W // 2; SR = W * DF
LINES_T = LINES


def fd_windows():
    """[(name, kind, f_rest, dv, frame)] — kind 'sel', 'ref' (a selection by a known line), 'ctrl'; frame 'true' or the false frame k."""
    S = json.load(open(os.path.join(HERE, "fd_selections.json"))); out = []
    for name, kind, f, par in windows():
        if kind == "ref": continue
        out.append((name, "sel" if kind == "cand" else "ctrl", f, 0.0, "true"))
    r = 1 - vel_fn()(t0("0015") + 150 / 86400.0) / C; LR = [L / r for L in LINES_T]; ER = (EDGE[0] / r, EDGE[1] / r); half = W / 2 * DF
    for fr in S["false_frames"]:
        k, dv = fr["k"], fr["dv"]; sels = [x["f_rest_Hz"] for x in fr["selections"]]
        taken = [(f - half, f + half) for f in sels]
        for i, f in enumerate(sels):
            ref = any(abs(L - f) < half + 1.5e3 for L in LR) or f - half < ER[0] or f + half > ER[1]
            out.append((f"F{k:02d}s{i}", "ref" if ref else "sel", f, dv, k))
            if ref: continue
            n = 0
            for o in OFFS:
                if n == 6: break
                g = f + o; lo, hi = g - half, g + half
                if lo < ER[0] or hi > ER[1] or any(abs(L - g) < half + 1.5e3 for L in LR) or any(not (hi < a or lo > b) for a, b in taken): continue
                out.append((f"F{k:02d}s{i}{'+' if o > 0 else '-'}{abs(o) / 1e3:.1f}k", "ctrl", g, dv, k)); taken.append((lo, hi)); n += 1
    return out


def track_f(scan, f_rest, dv, T0):
    """Per-frame float bin index of the (false) track: v = deldot(t) + dv (t - T0) 86400, as cometframe_raw.py."""
    v = vel_fn(); t = t0(scan) + (np.arange(NF) + 0.5) * TF / 86400.0
    vv = v(t) + dv * (t - T0) * 86400.0
    return N // 2 - (f_rest * (1 - vv / C) - FC) / DF


def scan(s):
    WIN = fd_windows(); T0 = json.load(open(os.path.join(HERE, "fd_selections.json")))["T0_mjd"]
    ifl = np.array([track_f(s, f, dv, T0) for _, _, f, dv, _ in WIN])            # (nw, NF)
    mid = np.rint(np.median(np.rint(ifl), axis=1)).astype(int)   # as common.track; off_f = (ifl - mid[:, None]) * DF; nw = len(WIN)
    assert mid.min() > W and mid.max() < N - W
    tc = (np.arange(NF) + 0.5) * TF; carry = np.zeros(nw); acc = np.zeros((2, nw, len(LAGS))); T00 = time.time()
    for j, X, Y in dm.frames(s, NF):
        ts = (j * W + np.arange(W)) / SR
        a = np.clip(np.searchsorted(tc, ts) - 1, 0, NF - 2); w = np.clip((ts - tc[a]) / TF, 0.0, 1.0)   # np.interp, clamped at the ends
        off = off_f[:, a] * (1 - w)[None, :] + off_f[:, a + 1] * w[None, :]
        Phi = carry[:, None] + 2 * np.pi * np.cumsum(off, axis=1) / SR; carry = Phi[:, -1].copy()
        ph = np.exp(-1j * Phi)
        for q, Z in enumerate((X, Y)):
            F = dm.fft(Z); B = np.stack([F[m - c:m + c] for m in mid])
            z = sf.ifft(sf.ifftshift(B, axes=1), axis=1) * ph; S2 = sf.fftshift(sf.fft(z, axis=1), axes=1)[:, c - 64:c + 65]
            u = S2 / np.maximum(np.abs(S2), 1e-30)
            for li, d in enumerate(LAGS):
                n = u.shape[1] - 2 * d
                acc[q, :, li] += np.abs(np.mean(u[:, :n] * u[:, 2 * d:2 * d + n] * np.conj(u[:, d:d + n]) ** 2, axis=1))
        if j % 100 == 0: print(s, j, round(time.time() - T00), flush=True)
    D = acc / NF
    out = {WIN[i][0]: {f"d{d}|{q}": float(D[qi, i, li]) for qi, q in enumerate("XY") for li, d in enumerate(LAGS)} for i in range(nw)}
    json.dump({"scan": s, "windows": [list(w[:2]) + [w[2], w[3], w[4]] for w in WIN], "D3": out, "seconds": round(time.time() - T00)},
              open(os.path.join(HERE, f"fd_{s}.json"), "w"))
    print(s, "done", nw, "windows", round(time.time() - T00), flush=True)


def read():
    R = {s: json.load(open(os.path.join(HERE, f"fd_{s}.json"))) for s in SCANS}; WIN = R["0013"]["windows"]; rng = np.random.default_rng(1665)
    groups = {"true": ([w[0] for w in WIN if w[4] == "true" and w[1] == "sel"], [w[0] for w in WIN if w[4] == "true" and w[1] == "ctrl"]),
              "false": ([w[0] for w in WIN if w[4] != "true" and w[1] == "sel"], [w[0] for w in WIN if w[4] != "true" and w[1] == "ctrl"])}
    res = {}
    for st in [f"d{d}|{q}" for q in "XY" for d in LAGS]:
        res[st] = {}
        for g, (sel, ctl) in groups.items():
            D = {}
            for n in sel + ctl:
                tot = 0.0
                for s in SCANS:
                    cv = np.array([R[s]["D3"][m][st] for m in ctl if m != n]); x = R[s]["D3"][n][st]; p = (1 + np.sum(cv >= x)) / (1 + len(cv))
                    tot += (-np.log(p)) if s in ON else np.log(p)
                D[n] = tot
            cd = np.array([D[n] for n in ctl]); m = np.mean([D[n] for n in sel])
            draws = np.array([cd[rng.choice(len(cd), len(sel), replace=False)].mean() for _ in range(10000)])
            res[st][g] = {"n_sel": len(sel), "n_ctrl": len(ctl), "mean_delta_sel": float(m), "p_agg": float((1 + np.sum(draws >= m)) / 10001),
                          "per_frame_mean": ({str(k): float(np.mean([D[w[0]] for w in WIN if w[4] == k and w[1] == "sel"]))
                                              for k in sorted({w[4] for w in WIN if w[4] != "true" and w[1] == "sel"})} if g == "false" else None),
                          "delta": {n: float(D[n]) for n in sel} if g == "true" else None}
        print(st, {g: (res[st][g]["n_sel"], round(res[st][g]["mean_delta_sel"], 3), res[st][g]["p_agg"]) for g in groups})
    json.dump(res, open(os.path.join(HERE, "fd_reading.json"), "w"), indent=1)


def check():
    """Streaming D3 against OH13R's stored-window D3 (stats_part*.json), comet frame, all true-frame windows, scan by scan."""
    st = {}
    for p in (0, 1): st.update(json.load(open(os.path.join(HERE, "..", f"stats_part{p}.json"))))
    worst = 0.0; n = 0
    for s in SCANS:
        R = json.load(open(os.path.join(HERE, f"fd_{s}.json")))["D3"]
        for name in st:
            if name not in R: continue
            for d in LAGS:
                for q in "XY":
                    a = R[name][f"d{d}|{q}"]; b = st[name][s]["full"][f"D3|d{d}|{q}|comet"]; worst = max(worst, abs(a - b) / b); n += 1
    print("compared", n, "values; worst relative difference", worst)
    json.dump({"compared": n, "worst_rel_diff": worst}, open(os.path.join(HERE, "fd_check.json"), "w"))


if __name__ == "__main__":
    a = sys.argv[1]
    read() if a == "read" else check() if a == "check" else scan(a)
