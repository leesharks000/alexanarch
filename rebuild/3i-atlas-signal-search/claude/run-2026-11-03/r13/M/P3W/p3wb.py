"""PLAN-P3W-B: p3w with steady-phase bins excluded.  python3 p3wb.py validate | SCAN | read"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p3w as P

def steady(Ph):
    S = len(Ph); c = np.abs(np.mean(Ph[1:] * np.conj(Ph[:-1]), 0)); return np.exp(-(S - 1) * c * c) <= 1e-3

_phasors = P.phasors
def phasors(z):
    Ph, pw = _phasors(z); pw = pw.copy(); pw[steady(Ph)] = np.inf   # marks the bin tonal for masks()
    return Ph, pw
P.phasors = phasors
_masks = P.masks
def masks(px, py):
    fx, fy = np.isfinite(px), np.isfinite(py)
    mx, my = np.where(fx, px, np.median(px[fx])), np.where(fy, py, np.median(py[fy]))
    m = _masks(mx, my)
    for f in P.FAMS:
        a = ~fx if f[0] == "X" else ~fy; b = ~fy if (f.startswith("XY") or f[0] == "Y") else ~fx
        m[f] &= ~(a[:, None] | b[None, :])
    return m
P.masks = masks

def validate():
    rng = np.random.default_rng(3626); res = {}; T0 = time.time()
    for form in ("X+", "X-", "XY+", "XY-"):
        for amp in (0.25, 0.5):
            zx, zy = P.noise(rng), P.noise(rng); s1, s2 = P.tones(rng, amp, form)
            zx = zx + s1
            if form.startswith("XY"): zy = zy + s2
            else: zx = zx + s2
            out, _, _ = P.run(zx, zy, 17000 + len(res)); r = out[form]; ok = r["p"] <= 0.05 and sorted(r["pair"]) == [P.F1, P.F2]
            res[f"{form}-{amp}"] = dict(family=r, recovered=bool(ok)); print(form, amp, "p", r["p"], "pair", r["pair"], "x", round(r["score"] / r["sur_max_median"], 2), "recovered", ok, flush=True)
    hits = 0
    for k in range(20):
        out, _, _ = P.run(P.noise(rng), P.noise(rng), 18000 + k); h = sum(out[f]["p"] <= 0.05 for f in P.FAMS); hits += h
        res[f"noise-{k}"] = {f: out[f]["p"] for f in P.FAMS}
    print("noise: family tests at p<=0.05:", hits, "/120", flush=True); res["noise_hits"] = hits
    t = np.arange(P.NS)
    zx = P.noise(rng) + 0.5 * np.exp(2j * np.pi * 0.2 * t); out, _, _ = P.run(zx, P.noise(rng), 18100); res["stationary"] = {f: out[f]["p"] for f in P.FAMS}
    zx = P.noise(rng) + sum(0.3 * np.exp(2j * np.pi * (f / 512 + 0.37 / 512) * t) for f in (60, 140, 230, 330, 420)); out, _, _ = P.run(zx, P.noise(rng), 18200)
    res["five_tones"] = {f: out[f]["p"] for f in P.FAMS}
    zx, zy = P.noise(rng), P.noise(rng); s1, s2 = P.tones(rng, 0.5, "none"); out, _, _ = P.run(zx + s1 + s2, zy, 18300); res["uncoupled"] = {f: out[f]["p"] for f in P.FAMS}
    for k in ("stationary", "five_tones", "uncoupled"): print(k, res[k], flush=True)
    rec = all(res[f"{f}-0.5"]["recovered"] for f in ("X+", "X-", "XY+", "XY-"))
    ctl = all(p > 0.05 for k in ("stationary", "five_tones", "uncoupled") for p in res[k].values())
    res["accepted"] = bool(rec and hits <= 12 and ctl); res["seconds"] = round(time.time() - T0)
    print("ACCEPTED" if res["accepted"] else "NOT ACCEPTED", res["seconds"], "s", flush=True)
    json.dump(res, open(os.path.join(HERE, "validationB.json"), "w"), indent=1)

def scan(s):
    d = np.load(os.path.join(P.N1625, f"crops_{s}.npz")); out = {"scan": s}; i = P.SCANS.index(s)
    for j, sl in enumerate(P.SLICES):
        r, _, _ = P.run(P.series(d, f"{sl}_X"), P.series(d, f"{sl}_Y"), 31625 + 100 * i + 10 * j); out[sl] = r
        print(s, sl, {f: (r[f]["p"], r[f]["pair"], round(r[f]["score"] / r[f]["sur_max_median"], 2)) for f in P.FAMS}, flush=True)
    json.dump(out, open(os.path.join(HERE, f"p3wb_{s}.json"), "w"), indent=1)

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "validate": validate()
    elif a == "read":
        import builtins; P.HERE_OUT = HERE
        _load = json.load
        orig = P.read.__code__
        # read p3wb_* files through p3w.read by aliasing names
        for s in P.SCANS:
            src = os.path.join(HERE, f"p3wb_{s}.json"); dst = os.path.join(HERE, f"p3w_{s}.json")
            if os.path.exists(dst): os.remove(dst)
            os.symlink(os.path.basename(src), dst)
        P.read()
        for s in P.SCANS: os.remove(os.path.join(HERE, f"p3w_{s}.json"))
    else: scan(a)
