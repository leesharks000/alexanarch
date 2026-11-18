"""PLAN-r13 part H (sha256 in PLAN.sha256): strength (B1), beyond-steady (I1-I3) and injection outside L band, on twelve S/C/X channels.
    python3 run_h.py -> H.json (resumable per channel). Detector copied from run_r13.py unchanged; data and frame as ocad/run_ocad.py."""
import os, json, time
import numpy as np, fsspec, h5py, hdf5plugin
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = open("PLAN.sha256").read().split()[0]
C = 299792.458; NF = 1048576; DC = slice(NF // 2 - 4, NF // 2 + 5)
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
CAD = {"S": (["0029", "0031", "0033"], ["0030", "0032", "0034"]), "C": (["0045", "0047", "0049"], ["0046", "0048", "0050"]),
       "X": (["0061", "0063", "0065"], ["0062", "0064", "0066"])}
HD = json.load(open("../ocad/headers.json")); FILES = {(v["node"], v["scan"]): k for k, v in HD.items()}; HH = {(v["node"], v["scan"]): v for v in HD.values()}
E_ = np.array(json.load(open("../ocad/horizons.json"))["E"]); deldot = lambda t: np.interp(t, E_[:, 0], E_[:, 1])
OC = json.load(open("../ocad/ocad.json"))["channels"]; ORD = json.load(open("../ocad/order.json"))
OUT = "H.json"; R = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": PLAN}
def save(): json.dump(R, open(OUT + ".tmp", "w"), indent=0, default=float); os.replace(OUT + ".tmp", OUT)
# channel choice, fixed by the plan: the four named-line channels with highest T, eight random by default_rng(17) with at least two per band
if "choice" not in R:
    key = lambda c: f"{c[0]}_{c[1]}_cc{c[2]:02d}"
    named = [key(c) for c in ORD["order"][:ORD["n_named"]]]; rand = [key(c) for c in ORD["order"][ORD["n_named"]:] if key(c) in OC]
    top4 = sorted(named, key=lambda k: (-OC[k]["T"], named.index(k)))[:4]
    rng = np.random.default_rng(17)
    while True:
        pick = [rand[i] for i in rng.choice(len(rand), 8, replace=False)]
        if all(sum(p[0] == b for p in pick) >= 2 for b in "SCX"): break
    inj = ["C_blc33_cc28"] + [next(p for p in pick if p[0] == b) for b in "SCX"]
    R["choice"] = {"named_top4": top4, "random8": pick, "inject4": inj}; save()
CH = R["choice"]["named_top4"] + R["choice"]["random8"]
def prep(Xs, keep, w=3):
    Y = {}
    for s in S6:
        x = Xs[s][keep[s]]; med = np.median(x, axis=0); y = x.astype(np.float64) / med - 1.0
        acc = y.copy()
        for j in range(1, w // 2 + 1): acc += np.roll(y, j, axis=1) + np.roll(y, -j, axis=1)
        Y[s] = acc
    return Y
def run(Y, keep, frame, coords=True, w=3, extra=False):
    V = VFR
    def tracked(s, dv):
        t = TT[s][keep[s]]; y = Y[s]
        v = V[s][keep[s]] + dv * (t - T0) * 86400.0
        sh = np.rint(F0[s] * (v[0] - v) / C / foff).astype(int)
        acc = np.zeros(NF); rmax = np.full(NF, -99.0) if extra else None
        for k in range(y.shape[0]):
            r = np.roll(y[k], -sh[k]); acc += r
            if extra:
                m_ = np.median(r); zr = (r - m_) / (1.4826 * np.median(np.abs(r - m_))); np.maximum(rmax, zr, out=rmax)
        m = np.median(acc); z = (acc - m) / (1.4826 * np.median(np.abs(acc - m))); z[DC] = 0.0
        if extra: rmax[DC] = 0.0
        return z, (F0[s] + foff * np.arange(NF)) / (1.0 - v[0] / C), rmax
    rows = []; cl_true = []; S1 = []; B2 = {k: [] for k in COORD}
    IX = {"I1": [], "I2": [], "I3": []}
    tol = max(int(10 / abs(foff)) + 1, w); ncl = lambda i: 0 if not len(i) else 1 + int(np.sum(np.diff(np.sort(i)) > tol))
    for k, dv in enumerate(OFFS):
        zs = {s: tracked(s, dv) for s in S6}; ref = zs[ON[0]][1]; A = {}; RM = {}
        mf = lambda a: np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
        for s in S6:
            ix = np.rint((zs[s][1] - ref[0]) / foff).astype(int); a = np.full(NF + 2000, -99.0)
            ok = (ix + 1000 >= 0) & (ix + 1000 < len(a)); a[ix[ok] + 1000] = zs[s][0][ok]
            A[s] = mf(a)
            if extra:
                b_ = np.full(NF + 2000, -99.0); b_[ix[ok] + 1000] = zs[s][2][ok]; RM[s] = mf(b_)
        offok = np.all([A[s] < 2.0 for s in OFF], axis=0); onok = np.all([A[s] < 2.0 for s in ON], axis=0)
        mon = np.min([A[s] for s in ON], axis=0); moff = np.min([A[s] for s in OFF], axis=0)
        p = np.where((mon >= 2.5) & offok)[0]; q = np.where((moff >= 2.5) & onok)[0]
        rows.append({"on": ncl(p), "swap": ncl(q)})
        if extra:
            zon = np.array([A[s] for s in ON]); zoff = np.array([A[s] for s in OFF])
            IX["I1"].append((ncl(np.where((zon.max(0) >= 5) & offok)[0]), ncl(np.where((zoff.max(0) >= 5) & onok)[0])))
            IX["I2"].append((ncl(np.where((np.sort(zon, 0)[1] >= 3) & offok)[0]), ncl(np.where((np.sort(zoff, 0)[1] >= 3) & onok)[0])))
            ron = np.max([RM[s] for s in ON], 0); roff = np.max([RM[s] for s in OFF], 0)
            IX["I3"].append((ncl(np.where((ron >= 6) & (roff < 4))[0]), ncl(np.where((roff >= 6) & (ron < 4))[0])))
        S1.append(float(np.max(np.where(offok, mon, -99.0))))
        if coords:
            for c, f in COORD.items():
                i = int(np.rint((f - ref[0]) / foff)) + 1000; B2[c].append(float(mon[i]) if 0 <= i < len(mon) else None)
        if k == 0: cl_true = sorted({round((ref[0] + (i - 1000) * foff) / 1e6, 6) for i in p})
    on = np.array([r["on"] for r in rows[1:]]); d = np.array([r["on"] - r["swap"] for r in rows[1:]])
    T = rows[0]["on"]; sw = rows[0]["swap"]
    res = {"T": T, "swap": sw, "mu": float(on.mean()), "sd": float(on.std()), "max": int(on.max()), "d_max": int(d.max()),
           "exceeds": bool(T > on.max() and T - sw > d.max()), "S": S1[0], "S_false_max": max(S1[1:]),
           "S_rank_of_41": int(1 + sum(x >= S1[0] for x in S1[1:])), "clusters_rest_MHz": cl_true[:300], "rows": rows, "S_all": S1}
    if extra:
        for k_, L in IX.items():
            t_, sw_ = L[0]; o = np.array([x[0] for x in L[1:]]); dd = np.array([x[0] - x[1] for x in L[1:]])
            res[k_] = {"T": t_, "swap": sw_, "mu": float(o.mean()), "sd": float(o.std()), "max": int(o.max()), "d_max": int(dd.max()),
                       "exceeds": bool(t_ > o.max() and t_ - sw_ > dd.max()), "all": L}
    if coords:
        res["B2"] = {c: {"minON_true": v[0], "rank_of_41": (int(1 + sum((x is not None and v[0] is not None and x >= v[0]) for x in v[1:])) if v[0] is not None else None)} for c, v in B2.items()}
    return res


r11 = np.random.default_rng(11); OFFS = [0.0] + list(r11.uniform(0.03, 1.0, 40) * r11.choice([-1, 1], 40) * C / 1.42e9)
COORD = {}
def fetch(nd, s, cc):
    for a_ in range(5):
        try:
            d = h5py.File(fsspec.open(B + FILES[(nd, s)], "rb", block_size=8 << 20).open(), "r")["data"]; n = int(d.attrs["nfpc"])
            return d[:, 0, cc * n:(cc + 1) * n].astype(np.float32)
        except Exception as e: print("retry", nd, s, cc, e, flush=True); time.sleep(10 * (a_ + 1))
    raise RuntimeError
for ch in CH:
    if ch in R and (ch not in R["choice"]["inject4"] or all(f"{ch}_inject_{A_}" in R for A_ in (0.5, 1.0, 2.0))): continue
    cad, nd, cc = ch.split("_"); cc = int(cc[2:]); ON, OFF = CAD[cad]; S6 = ON + OFF
    globals().update(ON=ON, OFF=OFF, S6=S6)
    t0 = time.time(); X = {s: fetch(nd, s, cc) for s in S6}
    H = {s: HH[(nd, s)] for s in S6}; foff = H[ON[0]]["foff"] * 1e6; T0 = min(H[s]["tstart"] for s in ON)
    F0 = {s: (H[s]["fch1"] + H[s]["foff"] * cc * H[s]["nfpc"]) * 1e6 for s in S6}
    TT = {s: H[s]["tstart"] + (np.arange(X[s].shape[0]) + 0.5) * H[s]["tsamp"] / 86400.0 for s in S6}
    VFR = {s: deldot(TT[s]) for s in S6}
    globals().update(foff=foff, T0=T0, F0=F0, TT=TT, VFR=VFR)
    KEEP = {s: np.ones(X[s].shape[0], bool) for s in S6}
    if ch not in R:
        R[ch] = run(prep(X, KEEP), KEEP, "comet", coords=False, extra=True); R[ch]["check_T_vs_ocad"] = [R[ch]["T"], OC[ch]["T"]]; save()
        r = R[ch]; print(ch, "T", r["T"], "(ocad", OC[ch]["T"], ") exceeds", r["exceeds"], "S", round(r["S"], 2), "rank", r["S_rank_of_41"],
              {k: (r[k]["T"], r[k]["max"], r[k]["exceeds"]) for k in ("I1", "I2", "I3")}, f"{time.time() - t0:.0f}s", flush=True)
    if ch in R["choice"]["inject4"]:
        rng = np.random.default_rng(13); v0 = deldot(TT[ON[0]][0]); INJ = []
        lo, hi = sorted([F0[ON[0]] / (1 - v0 / C), (F0[ON[0]] + foff * NF) / (1 - v0 / C)])
        while len(INJ) < 20:
            f = rng.uniform(lo, hi); j = (f * (1 - v0 / C) - F0[ON[0]]) / foff
            if abs(j - NF / 2) > 200 and all(abs(f - a) > 200 * abs(foff) for a in INJ): INJ.append(f)
        for A_ in (0.5, 1.0, 2.0):
            k_ = f"{ch}_inject_{A_}"
            if k_ in R: continue
            t1 = time.time(); Xi = {s: X[s].copy() for s in S6}
            for s in ON:
                x = Xi[s]; med = np.median(x, axis=0); r_ = x / med - 1.0; sig = 1.4826 * np.median(np.abs(r_ - np.median(r_))); v = deldot(TT[s])
                for f in INJ:
                    jj = np.rint((f * (1 - v / C) - F0[s]) / foff).astype(int)
                    for k in range(x.shape[0]):
                        if 0 <= jj[k] < NF: x[k, jj[k]] += A_ * med[jj[k]] * sig
            res = run(prep(Xi, KEEP), KEEP, "comet", coords=False); del Xi
            res["recovered"] = int(sum(any(abs(c * 1e6 - f) <= 10 for c in res["clusters_rest_MHz"]) for f in INJ)); res["inj_MHz"] = [f / 1e6 for f in INJ]
            R[k_] = res; save(); print(k_, "T", res["T"], "exceeds", res["exceeds"], "S", round(res["S"], 2), "rank", res["S_rank_of_41"], "recovered", res["recovered"], f"{time.time() - t1:.0f}s", flush=True)
    del X
print("ALLDONE", flush=True)
