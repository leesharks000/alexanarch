"""Hydrogen-line ratio search, Parkes 2025-07-31 (ratio/PLAN-ratio.md, sha256 1cd2fef8...). Resumable per frequency.
  python3 ratio/ratio_pks.py            -> ratio/ratio_pks.json
  python3 ratio/ratio_pks.py --inject   -> ratio/ratio_pks_inject.json (5/3 only; injection check)"""
import sys, os, re, json, time, math, urllib.request, concurrent.futures as cf
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pks"))
_a = sys.argv; sys.argv = [_a[0]]
from fullband import get, header, horizons, R, C
sys.argv = _a
SHA = "1cd2fef8e4e77372059dab25b0547ec2c6e72232d468943eaee09b01684c395d"
HI = 1420.405752
ALPHA = {"5/3": 5 / 3, "15/8": 15 / 8, "7/4": 7 / 4, "3/2": 3 / 2, "7/5": 7 / 5, "sqrt2": math.sqrt(2), "2": 2.0, "4/3": 4 / 3, "8/7": 8 / 7,
         "7/6": 7 / 6, "7/8": 7 / 8, "1/2": 0.5, "4/7": 4 / 7}
CTRL = {f"{p}/{q}": p / q for p, q in [(11, 4), (11, 5), (6, 11), (11, 6), (7, 11), (11, 7), (13, 5), (8, 11), (11, 8), (13, 6), (7, 13), (9, 11), (11, 9)]}
WS = [1, 5, 50, 500, 5000]; ZEV, ZVETO, Z2, Z2VETO = 5.0, 4.0, 5.0, 3.0; TOL = 0.015; PAD_LOAD = 0.2; EDGE = 0.2
INJ = "--inject" in sys.argv; OUT = "ratio/ratio_pks_inject.json" if INJ else "ratio/ratio_pks.json"
EX = cf.ThreadPoolExecutor(24); DIAG = {}

def rz(a):
    m = np.median(a, -1, keepdims=True); s = 1.4826 * np.median(np.abs(a - m), -1, keepdims=True); s[s == 0] = 1; return (a - m) / s
def boxcar(x, w):
    if w == 1: return x
    c = np.cumsum(np.pad(x, [(0, 0), (w // 2 + 1, w - w // 2)] if x.ndim == 2 else (w // 2 + 1, w - w // 2)), axis=-1)
    return (c[..., w:-1] - c[..., :-w - 1]) / np.sqrt(w)

# node map
root = urllib.request.urlopen(R, timeout=60).read().decode()
NODES = sorted(set(re.findall(r'href="(blc\d\d)/"', root)))
NM = {}
for nd in NODES:
    idx = urllib.request.urlopen(R + nd + "/", timeout=60).read().decode()
    fl = sorted(set(re.findall(r'href="([^"]+_[SR]_0001\.0000\.fil)"', idx)))
    if len(fl) != 6: continue
    h = header(R + nd + "/" + fl[0]); lo, hi = sorted((h['fch1'], h['fch1'] + h['foff'] * h['nchans'])); NM[nd] = (lo, hi, fl)
_E = {}

def run(name, r):
    f = r * HI
    nd = next((n for n, (lo, hi, _) in NM.items() if lo + EDGE <= f <= hi - EDGE), None)
    if nd is None: return {"f_MHz": f, "covered": False}
    files = NM[nd][2]; roles = ["S" if "_S_" in x else "R" for x in files]
    H = [header(R + nd + "/" + x) for x in files]; NCH, FOFF, FCH1 = H[0]['nchans'], H[0]['foff'], H[0]['fch1']
    if nd not in _E: _E[nd] = horizons(min(h['tstart'] for h in H), max(h['tstart'] for h in H) + 0.01)
    E = _E[nd]; T = [h['tstart'] + (np.arange(20) + 0.5) * h['tsamp'] / 86400.0 for h in H]
    vv = [np.interp(T[i], E[:, 0], E[:, 1]) for i in range(6)]
    fc = [f * (1 - v / C) for v in vv]   # comet-frame position per sample
    allpos = [f] + [x for a in fc for x in a]; flo, fhi = min(allpos) - PAD_LOAD, max(allpos) + PAD_LOAD
    chan = lambda x: int(round((x - FCH1) / FOFF))
    c0 = min(chan(flo), chan(fhi)); n = abs(chan(fhi) - chan(flo)); fr = FCH1 + FOFF * (c0 + np.arange(n))
    per = []
    for i in range(6):
        h = H[i]
        def one(k):
            a = h['hdr_len'] + (k * NCH + c0) * 4; return k, np.frombuffer(get(R + nd + "/" + files[i], a, a + n * 4 - 1), '<f4')
        X = np.zeros((20, n))
        for k, row in EX.map(one, range(20)): X[k] = row
        med = np.median(X, 0); med[med == 0] = 1; rr = X / med - 1.0
        if INJ and i == 0:
            j = chan(f) - c0; sd = 1.4826 * np.median(np.abs(rr[7] - np.median(rr[7]))); rr[7, j] += 7 * sd
            j2 = chan(f + 0.003) - c0; b50 = boxcar(rr[12], 50); sd = 1.4826 * np.median(np.abs(b50 - np.median(b50))); rr[12, j2 - 25:j2 + 25] += 7 * sd / np.sqrt(50)   # z ~ 7 in the W=50 statistic (deviation, recorded: first calibration used single-channel sd)
        sh = np.rint(FCH1 * 1e6 * (vv[i][0] - vv[i]) / C / (FOFF * 1e6)).astype(int)
        acc = np.zeros(n)
        for k in range(20): acc += np.roll(rr[k], -sh[k])
        d = {}
        for W in WS:
            z = rz(boxcar(rr, W)); z2 = rz(boxcar(acc[None], W))[0]; ev = np.argwhere(z >= ZEV)
            d[W] = {"ev": ev, "zev": z[ev[:, 0], ev[:, 1]] if len(ev) else np.array([]), "vmax": z.max(0), "z2": z2}
        if INJ and i == 0:
            DIAG.update({f"W{W}": {"tone_s7": round(float(d[W]["z"][7, j]) if False else 0, 2)} for W in WS})
            for W in WS:
                zz = rz(boxcar(rr, W)); DIAG[f"W{W}"] = {"tone_s7": round(float(zz[7, j]), 2), "burst_s12": round(float(zz[12, j2 - 2:j2 + 3].max()), 2)}
        per.append(d); del X, rr
    def intol(i, s, fx):
        pos = [f, fc[i][s]]; off = [(fx - p) * 1e3 for p in pos]
        return min(off, key=abs), ("topo" if abs(off[0]) <= abs(off[1]) else "comet"), any(abs(o) <= TOL * 1e3 for o in off)
    if INJ:
        for W in WS:
            pad = W + 2; m = np.zeros(n, bool)
            for i in range(6):
                if roles[i] == "R": m |= np.convolve((per[i][W]["vmax"] >= ZVETO).astype(int), np.ones(2 * pad + 1), "same") > 0
            jt = chan(f) - c0; jb = chan(f + 0.003) - c0
            DIAG[f"W{W}"].update({"veto_tone": bool(m[jt]), "veto_burst": bool(m[jb - 2:jb + 3].any()), "veto_frac_window": round(float(m.mean()), 3)})
        print("DIAG", DIAG, flush=True)
    res = {"f_MHz": f, "covered": True, "node": nd, "true": [], "swap": []}
    for W in WS:
        pad = W + 2
        def dil(a, thr):
            m = (a >= thr).astype(np.int32); c = np.cumsum(np.pad(m, (pad + 1, pad))); return (c[2 * pad + 1:] - c[:-2 * pad - 1]) > 0
        for tgt, vet, key in (("S", "R", "true"), ("R", "S", "swap")):
            vP = np.zeros(n, bool); v2 = np.zeros(n, bool)
            for i in range(6):
                if roles[i] == vet: vP |= dil(per[i][W]["vmax"], ZVETO); v2 |= dil(per[i][W]["z2"], Z2VETO)
            for i in range(6):
                if roles[i] != tgt: continue
                keep = sorted((int(c), int(s), float(z)) for (s, c), z in zip(per[i][W]["ev"], per[i][W]["zev"]) if not vP[c])
                cl = []
                for c, s, z in keep:
                    if cl and c - cl[-1][-1][0] <= pad: cl[-1].append((c, s, z))
                    else: cl.append([(c, s, z)])
                for g in cl:
                    c, s, z = max(g, key=lambda q: q[2]); off, fr_, ok = intol(i, s, fr[c])
                    if ok: res[key].append({"det": "P", "W": W, "scan": i, "sample": s, "f_MHz": round(float(fr[c]), 6), "off_kHz": round(off, 2), "frame": fr_, "z": round(z, 2)})
                ix = np.where((per[i][W]["z2"] >= Z2) & ~v2)[0]
                for gg in (np.split(ix, np.where(np.diff(ix) > pad)[0] + 1) if len(ix) else []):
                    c = int(gg[np.argmax(per[i][W]["z2"][gg])]); off, fr_, ok = intol(i, 0, fr[c])
                    if ok: res[key].append({"det": "P2", "W": W, "scan": i, "f_MHz": round(float(fr[c]), 6), "off_kHz": round(off, 2), "frame": fr_, "z": round(float(per[i][W]["z2"][c]), 2)})
    return res

state = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": SHA, "nodes": {k: v[:2] for k, v in NM.items()}, "alpha": {}, "ctrl": {}}
jobs = [("alpha", "5/3", ALPHA["5/3"])] if INJ else [("alpha", k, v) for k, v in ALPHA.items()] + [("ctrl", k, v) for k, v in CTRL.items()]
for lst, k, v in jobs:
    if k in state[lst]: continue
    t0 = time.time(); r = run(k, v); state[lst][k] = r
    json.dump(state, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(lst, k, round(r["f_MHz"], 4), r.get("node"), "true", len(r.get("true", [])), "swap", len(r.get("swap", [])), "%.0fs" % (time.time() - t0), flush=True)
if not INJ:
    rate = lambda lst, key: (lambda cov: sum(len(x[key]) for x in cov) / max(len(cov), 1))([x for x in state[lst].values() if x["covered"]])
    multi = False
    for x in state["alpha"].values():
        if not x["covered"]: continue
        sc = {}
        for e in x["true"]: sc.setdefault(e["frame"], set()).add(e["scan"])
        multi |= any(len(s) >= 2 for s in sc.values())
    a, c, sw = rate("alpha", "true"), rate("ctrl", "true"), rate("alpha", "swap")
    state["summary"] = {"alpha_rate": a, "ctrl_rate": c, "alpha_swap_rate": sw, "ctrl_swap_rate": rate("ctrl", "swap"),
                        "covered": {l: sum(x["covered"] for x in state[l].values()) for l in ("alpha", "ctrl")}, "multi_scan": multi,
                        "lead": bool(a > c and a > sw and multi)}
    json.dump(state, open(OUT, "w"), indent=1); print("SUMMARY", state["summary"], flush=True)
