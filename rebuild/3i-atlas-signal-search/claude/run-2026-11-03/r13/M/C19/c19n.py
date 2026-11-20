"""PLAN-C19 analysis 7: catalogue null.  python3 c19n.py -> null.json
Two interleaved sequences, shared step 60-75 kHz, 25 Hz tolerance, on every channel's M4b ON events and
role-reversed control list; plus a uniform-frequency Monte Carlo at each list's size."""
import json, os, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TOL = 25.0; DMIN, DMAX = 60e3, 75e3

def uniq(fs, merge=100.0):
    fs = np.sort(np.asarray(fs)); out = []
    for x in fs:
        if not out or x - out[-1] > merge: out.append(x)
    return np.array(out)

def members(f, ph, d):
    r = (f - ph) / d; return np.abs(r - np.rint(r)) * d <= TOL

def best(f):
    f = uniq(f); n = len(f); top = (0, 0, None)
    if n < 2: return dict(n=n, one=min(n, 1), two=min(n, 1), step=None)
    one = 1
    for i in range(n):
        for j in range(i + 1, n):
            g0 = int(np.ceil((f[j] - f[i]) / DMAX)); g1 = int(np.floor((f[j] - f[i]) / DMIN))
            for g in range(max(g0, 1), g1 + 1):
                d = (f[j] - f[i]) / g; mA = members(f, f[i], d); a = int(mA.sum()); one = max(one, a)
                rest = np.where(~mA)[0]; b = 0
                for k in rest:
                    b = max(b, int(members(f[rest], f[k], d).sum()))
                if b < 2: b = 0
                if a + b > top[0]: top = (a + b, a, d)
    return dict(n=n, one=one, two=top[0], step=top[2])

R = {}
for p in sorted(glob.glob(os.path.join(HERE, "..", "M4b", "events", "cc*.json"))):
    d = json.load(open(p)); cc = d["cc"]
    on = [e["mhz_topo"] * 1e6 for e in d["events"]]; ct = [e["mhz_topo"] * 1e6 for e in d["control_top"]]
    R[cc] = dict(fc=d["fc_mhz"], A=d["n"]["A"], cA=d["control_n"]["A"], on=best(on), ctrl=best(ct))
    print(cc, R[cc]["on"], R[cc]["ctrl"], flush=True)
rng = np.random.default_rng(19); MC = {}
for n in sorted({r["on"]["n"] for r in R.values()} | {r["ctrl"]["n"] for r in R.values()}):
    if n < 3: continue
    MC[n] = [best(rng.uniform(0, 2.9296875e6, n))["two"] for _ in range(200)]
    print("mc", n, np.percentile(MC[n], [50, 95, 99]), max(MC[n]), flush=True)
json.dump(dict(tol=TOL, step=[DMIN, DMAX], channels=R, mc={str(k): v for k, v in MC.items()}), open(os.path.join(HERE, "null.json"), "w"), indent=1)
