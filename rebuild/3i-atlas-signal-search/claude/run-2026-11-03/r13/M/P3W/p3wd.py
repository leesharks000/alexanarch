"""PLAN-P3W-D: p3w with a shift null without wraparound (each bin read from its own offset 0..W over S-W segments).  python3 p3wd.py validate | SCAN | read"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p3w as P

W = 512


def window(Ph, rng=None):
    S, K = Ph.shape; n = S - W
    if rng is None: return Ph[:n]
    L = rng.integers(0, W + 1, size=K)
    return Ph[np.arange(n)[:, None] + L[None, :], np.arange(K)[None, :]]


def run(zx, zy, seed):
    PX, px = P.phasors(zx); PY, py = P.phasors(zy); M = P.masks(px, py); R = P.stats(window(PX), window(PY)); rng = np.random.default_rng(seed)
    sur = {f: [] for f in P.FAMS}; surA = {f: [] for f in P.FAMS}
    best = {f: (float(R[f][M[f]].max()), np.unravel_index(np.argmax(np.where(M[f], R[f], -1)), R[f].shape)) for f in P.FAMS}
    for _ in range(P.NSUR):
        Q = P.stats(window(PX, rng), window(PY, rng))
        for f in P.FAMS:
            sur[f].append(float(Q[f][M[f]].max())); surA[f].append(float(Q[f][best[f][1]]))
    out = {}
    for f in P.FAMS:
        v, (k, l) = best[f]
        out[f] = dict(score=v, pair=[int(k), int(l)], p=(1 + sum(x >= v for x in sur[f])) / (P.NSUR + 1),
                      sur_max_median=float(np.median(sur[f])), sur_at_pair_max=float(max(surA[f])), sur_at_pair_median=float(np.median(surA[f])))
    return out, R, M


def at_pair(zx, zy, f, k, l, seed):
    PX, _ = P.phasors(zx); PY, _ = P.phasors(zy); R = P.stats(window(PX), window(PY)); rng = np.random.default_rng(seed); sa = []
    for _ in range(P.NSUR):
        sa.append(float(P.stats(window(PX, rng), window(PY, rng))[f][k, l]))
    return dict(A=float(R[f][k, l]), sur_max=float(max(sa)), sur_median=float(np.median(sa)))


P.run = run; P.at_pair = at_pair


def steady_tones(fr, amp):
    t = np.arange(P.NS); return sum(amp * np.exp(2j * np.pi * (b + o) / P.SEG * t) for b, o in fr)


def validate():
    rng = np.random.default_rng(3628); res = {}; T0 = time.time()
    for form in ("X+", "X-", "XY+", "XY-"):
        for amp in (0.25, 0.5):
            zx, zy = P.noise(rng), P.noise(rng); s1, s2 = P.tones(rng, amp, form)
            zx = zx + s1
            if form.startswith("XY"): zy = zy + s2
            else: zx = zx + s2
            out, _, _ = run(zx, zy, 37000 + len(res)); r = out[form]; ok = r["p"] <= 0.05 and sorted(r["pair"]) == [P.F1, P.F2]
            res[f"{form}-{amp}"] = dict(family=r, recovered=bool(ok)); print(form, amp, "p", r["p"], "pair", r["pair"], "x", round(r["score"] / r["sur_max_median"], 2), "recovered", ok, flush=True)
    hits = 0
    for k in range(20):
        out, _, _ = run(P.noise(rng), P.noise(rng), 38000 + k); h = sum(out[f]["p"] <= 0.05 for f in P.FAMS); hits += h
        res[f"noise-{k}"] = {f: out[f]["p"] for f in P.FAMS}
    print("noise: family tests at p<=0.05:", hits, "/120", flush=True); res["noise_hits"] = hits
    t = np.arange(P.NS); B = (60, 140, 230, 330, 420)
    ctl = {"stationary": lambda: 0.5 * np.exp(2j * np.pi * 0.2 * t),
           "five_same": lambda: steady_tones([(b, 0.37) for b in B], 0.3),
           "five_mixed": lambda: steady_tones(list(zip(B, (0.11, 0.37, 0.52, 0.68, 0.90))), 0.3)}
    passed = {}
    for j, (name, sig) in enumerate(ctl.items()):
        reps = []
        for r_ in range(5):
            out, _, _ = run(P.noise(rng) + sig(), P.noise(rng), 38100 + 100 * j + r_); reps.append({f: out[f]["p"] for f in P.FAMS})
        n = sum(p <= 0.05 for r in reps for p in r.values()); res[name] = dict(reps=reps, hits=n); passed[name] = n <= 3; print(name, n, "/30", reps, flush=True)
    reps = []
    for r_ in range(5):
        zx, zy = P.noise(rng), P.noise(rng); s1, s2 = P.tones(rng, 0.5, "none"); out, _, _ = run(zx + s1 + s2, zy, 38400 + r_); reps.append({f: out[f]["p"] for f in P.FAMS})
    n = sum(p <= 0.05 for r in reps for p in r.values()); res["uncoupled"] = dict(reps=reps, hits=n); passed["uncoupled"] = n <= 3; print("uncoupled", n, "/30", reps, flush=True)
    nseg = P.NS // P.SEG; on = np.repeat(rng.random(nseg // 32) < 0.5, 32 * P.SEG)
    out, _, _ = run(P.noise(rng) + on * 0.5 * np.exp(2j * np.pi * 0.2 * t), P.noise(rng), 38500); res["burst_reported"] = {f: out[f]["p"] for f in P.FAMS}; print("burst (reported)", res["burst_reported"], flush=True)
    rec = all(res[f"{f}-0.5"]["recovered"] for f in ("X+", "X-", "XY+", "XY-"))
    res["passed"] = passed; res["accepted"] = bool(rec and hits <= 12 and all(passed.values())); res["seconds"] = round(time.time() - T0)
    print("ACCEPTED" if res["accepted"] else "NOT ACCEPTED", res["seconds"], "s", flush=True)
    json.dump(res, open(os.path.join(HERE, "validationD.json"), "w"), indent=1)


def scan(s):
    d = np.load(os.path.join(P.N1625, f"crops_{s}.npz")); out = {"scan": s}; i = P.SCANS.index(s)
    for j, sl in enumerate(P.SLICES):
        r, _, _ = run(P.series(d, f"{sl}_X"), P.series(d, f"{sl}_Y"), 31625 + 100 * i + 10 * j); out[sl] = r
        print(s, sl, {f: (r[f]["p"], r[f]["pair"], round(r[f]["score"] / r[f]["sur_max_median"], 2)) for f in P.FAMS}, flush=True)
    json.dump(out, open(os.path.join(HERE, f"p3wd_{s}.json"), "w"), indent=1)


def read():
    # p3w.read() reads p3w_{s}.json and writes p3w_gates.json; alias the P3W-D files in and out
    for s in P.SCANS:
        dst = os.path.join(HERE, f"p3w_{s}.json")
        if os.path.lexists(dst): os.remove(dst)
        os.symlink(f"p3wd_{s}.json", dst)
    try: P.read()
    finally:
        for s in P.SCANS: os.remove(os.path.join(HERE, f"p3w_{s}.json"))
        g = os.path.join(HERE, "p3w_gates.json")
        if os.path.exists(g): os.replace(g, os.path.join(HERE, "p3wd_gates.json"))


if __name__ == "__main__":
    a = sys.argv[1]
    validate() if a == "validate" else read() if a == "read" else scan(a)
