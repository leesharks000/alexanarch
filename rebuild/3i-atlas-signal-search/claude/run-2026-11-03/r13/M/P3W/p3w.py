"""PLAN-P3W.  python3 p3w.py validate | SCAN | read"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); N1625 = os.path.join(HERE, "../N1625")
SEG = 512; NSUR = 39; SCANS = ["0013", "0014", "0015", "0016", "0017", "0018"]; SLICES = ["target", "ctrl25k", "hidrift"]
FAMS = ["X+", "X-", "Y+", "Y-", "XY+", "XY-"]
KK, LL = np.meshgrid(np.arange(SEG), np.arange(SEG), indexing="ij")


def phasors(z):
    X = np.fft.fft(z[:len(z) // SEG * SEG].reshape(-1, SEG), axis=1); P = np.abs(X) ** 2
    return X / np.maximum(np.abs(X), 1e-30), P.mean(0)


def masks(px, py):
    tx = px > 2 * np.median(px); ty = py > 2 * np.median(py); near = np.abs(KK - LL) < 2
    m = {}
    for f in FAMS:
        a = tx if f[0] == "X" else ty; b = ty if f.startswith("XY") or f[0] == "Y" else tx
        mm = ~(near | a[:, None] | b[None, :])
        if not f.startswith("XY"): mm &= KK < LL
        m[f] = mm
    return m


def stats(PX, PY):
    S = len(PX)
    return {"X+": np.abs(PX.T @ PX) / S, "X-": np.abs(PX.T @ PX.conj()) / S, "Y+": np.abs(PY.T @ PY) / S,
            "Y-": np.abs(PY.T @ PY.conj()) / S, "XY+": np.abs(PX.T @ PY) / S, "XY-": np.abs(PX.T @ PY.conj()) / S}


def run(zx, zy, seed):
    PX, px = phasors(zx); PY, py = phasors(zy); M = masks(px, py); R = stats(PX, PY); rng = np.random.default_rng(seed)
    sur = {f: [] for f in FAMS}; surA = {f: [] for f in FAMS}
    best = {f: (float(R[f][M[f]].max()), np.unravel_index(np.argmax(np.where(M[f], R[f], -1)), R[f].shape)) for f in FAMS}
    for _ in range(NSUR):
        e = np.exp(2j * np.pi * rng.random(PX.shape)); Q = stats(PX * e, PY * e)
        for f in FAMS:
            sur[f].append(float(Q[f][M[f]].max())); surA[f].append(float(Q[f][best[f][1]]))
    out = {}
    for f in FAMS:
        v, (k, l) = best[f]
        out[f] = dict(score=v, pair=[int(k), int(l)], p=(1 + sum(x >= v for x in sur[f])) / (NSUR + 1),
                      sur_max_median=float(np.median(sur[f])), sur_at_pair_max=float(max(surA[f])), sur_at_pair_median=float(np.median(surA[f])))
    return out, R, M


def at_pair(zx, zy, f, k, l, seed):
    PX, _ = phasors(zx); PY, _ = phasors(zy); R = stats(PX, PY); rng = np.random.default_rng(seed); sa = []
    for _ in range(NSUR):
        e = np.exp(2j * np.pi * rng.random(PX.shape)); sa.append(float(stats(PX * e, PY * e)[f][k, l]))
    return dict(A=float(R[f][k, l]), sur_max=float(max(sa)), sur_median=float(np.median(sa)))


def half_p(zx, zy, f, k, l):
    out = []
    for h in (0, 1):
        n = len(zx) // 2; a, b = zx[h * n:(h + 1) * n], zy[h * n:(h + 1) * n]
        PX, _ = phasors(a); PY, _ = phasors(b); A = stats(PX, PY)[f][k, l]; out.append(dict(A=float(A), p=float(np.exp(-len(PX) * A * A))))
    return out


# ---- validation ------------------------------------------------------------
NS = 32 * 65536; F1, F2 = 137, 301


def tones(rng, amp, form):
    """Per-segment-constant tones at F1 and F2 with fresh random phases; the coupled combination fixed at 0."""
    nseg = NS // SEG; t = np.arange(SEG); a = rng.random(nseg) * 2 * np.pi; c = rng.random(nseg) * 2 * np.pi
    if form.endswith("+"): b = -a
    elif form.endswith("-"): b = a
    else: b = c                                          # uncoupled
    s1 = np.concatenate([np.exp(1j * (2 * np.pi * F1 * t / SEG + a[s])) for s in range(nseg)])
    s2 = np.concatenate([np.exp(1j * (2 * np.pi * F2 * t / SEG + b[s])) for s in range(nseg)])
    k = amp / np.sqrt(SEG)        # unit-variance noise has per-bin rms sqrt(SEG); a tone of amplitude k gives k*SEG: ratio amp
    return k * s1, k * s2


def noise(rng): return (rng.normal(size=NS) + 1j * rng.normal(size=NS)) / np.sqrt(2)


def validate():
    rng = np.random.default_rng(3625); res = {}; T0 = time.time()
    for form in ("X+", "X-", "XY+", "XY-"):
        for amp in (0.1, 0.25, 0.5):
            zx, zy = noise(rng), noise(rng); s1, s2 = tones(rng, amp, form)
            zx = zx + s1; zy = zy + s2 if form.startswith("XY") else zy
            if not form.startswith("XY"): zx = zx + s2
            out, R, M = run(zx, zy, 7000 + len(res)); r = out[form]; ok = r["p"] <= 0.05 and sorted(r["pair"]) == [F1, F2]
            res[f"{form}-{amp}"] = dict(family=r, recovered=bool(ok)); print(form, amp, "p", r["p"], "pair", r["pair"], "score/surmax", round(r["score"] / r["sur_max_median"], 2), "recovered", ok, flush=True)
    fa = 0
    for k in range(20):
        out, _, _ = run(noise(rng), noise(rng), 8000 + k); hit = [f for f in FAMS if out[f]["p"] <= 0.05]; fa += bool(hit)
        res[f"noise-{k}"] = {f: out[f]["p"] for f in FAMS}
    print("noise trials with any family at p<=0.05:", fa, "/20", flush=True)
    zx = noise(rng) + 0.5 * np.exp(2j * np.pi * 0.2 * np.arange(NS)); out, _, _ = run(zx, noise(rng), 8100)
    res["stationary"] = {f: out[f]["p"] for f in FAMS}; print("stationary tone:", res["stationary"], flush=True)
    zx, zy = noise(rng), noise(rng); s1, s2 = tones(rng, 0.5, "none"); out, _, _ = run(zx + s1 + s2, zy, 8200)
    res["uncoupled"] = {f: out[f]["p"] for f in FAMS}; print("uncoupled pair:", res["uncoupled"], flush=True)
    res["seconds"] = round(time.time() - T0); json.dump(res, open(os.path.join(HERE, "validation.json"), "w"), indent=1)


# ---- data --------------------------------------------------------------------
def series(d, key): return np.concatenate([np.fft.ifft(np.fft.ifftshift(F.astype(np.complex128))) for F in d[key]])


def scan(s):
    d = np.load(os.path.join(N1625, f"crops_{s}.npz")); out = {"scan": s}; i = SCANS.index(s)
    for j, sl in enumerate(SLICES):
        zx, zy = series(d, f"{sl}_X"), series(d, f"{sl}_Y"); r, _, _ = run(zx, zy, 31625 + 100 * i + 10 * j); out[sl] = r
        print(s, sl, {f: (r[f]["p"], r[f]["pair"], round(r[f]["score"] / r[f]["sur_max_median"], 2)) for f in FAMS}, flush=True)
    json.dump(out, open(os.path.join(HERE, f"p3w_{s}.json"), "w"), indent=1)


def read():
    R = {s: json.load(open(os.path.join(HERE, f"p3w_{s}.json"))) for s in SCANS}; gates = {}
    for s in ("0013", "0015", "0017"):
        for f in FAMS:
            r = R[s]["target"][f]
            if r["p"] > 0.05: continue
            k, l = r["pair"]; d = np.load(os.path.join(N1625, f"crops_{s}.npz")); zx, zy = series(d, "target_X"), series(d, "target_Y")
            g = {"scan": s, "family": f, "pair": [k, l], "p": r["p"], "halves": half_p(zx, zy, f, k, l)}
            i = SCANS.index(s); offs = [SCANS[i - 1]] + ([SCANS[i + 1]] if i + 1 < 6 else [])
            g["off"] = {}
            for o in offs:
                dd = np.load(os.path.join(N1625, f"crops_{o}.npz")); g["off"][o] = at_pair(series(dd, "target_X"), series(dd, "target_Y"), f, k, l, 555)
            g["ctrl"] = {sl: at_pair(series(d, f"{sl}_X"), series(d, f"{sl}_Y"), f, k, l, 556) for sl in ("ctrl25k", "hidrift")}
            exc = r["score"] - r["sur_at_pair_median"]; oexc = max(v["A"] - v["sur_median"] for v in g["off"].values())
            g["verdict"] = dict(halves=all(h["p"] <= 0.01 for h in g["halves"]),
                                off_not_above=all(v["A"] <= v["sur_max"] for v in g["off"].values()), excess_ratio=(exc / oexc) if oexc > 0 else None,
                                controls_quiet=all(v["A"] <= v["sur_max"] for v in g["ctrl"].values()))
            v = g["verdict"]; g["lead"] = bool(v["halves"] and v["off_not_above"] and (v["excess_ratio"] is None or v["excess_ratio"] >= 4) and v["controls_quiet"])
            gates[f"{s}{f}"] = g; print(json.dumps(g)[:900])
    n = sum(1 for s in SCANS for sl in SLICES for f in FAMS if R[s][sl][f]["p"] <= 0.05)
    print("families at p<=0.05 across all 108 (6 scans x 3 slices x 6):", n, "| expected about 5.4")
    json.dump(gates, open(os.path.join(HERE, "p3w_gates.json"), "w"), indent=1)


if __name__ == "__main__":
    a = sys.argv[1]
    validate() if a == "validate" else read() if a == "read" else scan(a)
