"""Wow!-guided intermittent search, Parkes 2025-07-31 blc05 (wow/PLAN-wow.md, sha256 10ecba29...). Detectors P (single-sample) and P2 (single-scan
persistence) per the plan, over the target window and the ten control windows of the protected band. Resumable per window.
  python3 wow/wow_pks.py            -> wow/wow_pks.json
  python3 wow/wow_pks.py --inject   -> wow/wow_pks_inject2.json (target window only; injection check)"""
import sys, os, json, re, time, urllib.request, concurrent.futures as cf
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pks"))
_a = sys.argv; sys.argv = [_a[0]]
from fullband import get, header, horizons, R, C   # same reader and ephemeris as the full-band run
sys.argv = _a
NODE = "blc05"; SHA = "10ecba29335d295e5b48dfae59557a71bf99f3b7b3b69460baffb831790877c1"
WS = [1, 5, 50, 500, 5000]; ZEV, ZVETO, Z2, Z2VETO = 7.0, 4.0, 6.0, 3.0
WIN = [(1400.2 + 2.4 * k, 1400.2 + 2.4 * (k + 1)) for k in range(11)]; TARGET = 8
ANCH = {"A1_HI": 1420.405752, "A2_Ehman": 1420.4556, "A3_Mendez": 1420.726}; TOL = 0.015
INJ = "--inject" in sys.argv
OUT = "wow/wow_pks_inject2.json" if INJ else "wow/wow_pks.json"

idx = urllib.request.urlopen(R + NODE + "/", timeout=60).read().decode()
FILES = sorted(set(re.findall(r'href="([^"]+_[SR]_0001\.0000\.fil)"', idx))); assert len(FILES) == 6
ROLES = ["S" if "_S_" in f else "R" for f in FILES]
H = [header(R + NODE + "/" + f) for f in FILES]
NCH, FOFF, FCH1 = H[0]['nchans'], H[0]['foff'], H[0]['fch1']          # MHz
E = horizons(min(h['tstart'] for h in H), max(h['tstart'] for h in H) + 0.01)
T = [h['tstart'] + (np.arange(20) + 0.5) * h['tsamp'] / 86400.0 for h in H]
EX = cf.ThreadPoolExecutor(24)

def chan(f): return int(round((f - FCH1) / FOFF))
def boxcar(x, w):
    if w == 1: return x
    c = np.cumsum(np.pad(x, [(0, 0), (w // 2 + 1, w - w // 2)] if x.ndim == 2 else (w // 2 + 1, w - w // 2)), axis=-1)
    return (c[..., w:-1] - c[..., :-w - 1]) / np.sqrt(w)
def rz(a):
    m = np.median(a, -1, keepdims=True); s = 1.4826 * np.median(np.abs(a - m), -1, keepdims=True); s[s == 0] = 1; return (a - m) / s

def load(i, c0, n):
    h = H[i]
    def one(k):
        a = h['hdr_len'] + (k * NCH + c0) * 4; return k, np.frombuffer(get(R + NODE + "/" + FILES[i], a, a + n * 4 - 1), '<f4')
    X = np.zeros((20, n), np.float32)
    for k, row in EX.map(one, range(20)): X[k] = row
    return X

def anchors_topo(i, j):
    v = float(np.interp(T[i][j], E[:, 0], E[:, 1]))
    return {**{k + "_c": a * (1 - v / C) for k, a in ANCH.items()}, **{k + "_t": a for k, a in ANCH.items()}}

def run_window(wi):
    lo, hi = WIN[wi]; c0 = min(chan(lo), chan(hi)); n = abs(chan(hi) - chan(lo))
    per = []   # per scan: dict W -> (event list, veto map)
    for i in range(6):
        X = load(i, c0, n).astype(np.float64)
        med = np.median(X, 0); med[med == 0] = 1; r = X / med - 1.0
        if INJ and i == 0:
            print("dc check", [float(r[:, chan(1420.0) - c0 + d].std()) for d in (-2, -1, 0, 1, 2)], flush=True)   # in the normalised data: a 1-channel tone at 1420.0 MHz in sample 7, a 10 kHz burst at 1421.0 MHz in sample 13, each z ~ 10
            sd = 1.4826 * np.median(np.abs(r[7] - np.median(r[7]))); r[7, chan(1420.1234) - c0] += 10 * sd
            b = chan(1421.0) - c0; r[13, b - 2500:b + 2500] += 10 * sd / np.sqrt(5000)
        v = np.interp(T[i], E[:, 0], E[:, 1]); sh = np.rint(FCH1 * 1e6 * (v[0] - v) / C / (FOFF * 1e6)).astype(int)
        acc = np.zeros(n)
        for k in range(20): acc += np.roll(r[k], -sh[k])
        d = {}
        for W in WS:
            z = rz(boxcar(r, W)); z2 = rz(boxcar(acc[None], W))[0]
            ev = np.argwhere(z >= ZEV)
            d[W] = {"ev": ev, "zev": z[ev[:, 0], ev[:, 1]] if len(ev) else np.array([]), "vmax": z.max(0), "z2": z2}
        per.append(d); del X, r
    res = {"f_lo": lo, "f_hi": hi, "P": {}, "P2": {}, "P_events": [], "P2_events": []}
    for W in WS:
        pad = W + 2
        def dil(a, thr):   # channels within +-pad of any value >= thr
            m = (a >= thr).astype(np.int32); c = np.cumsum(np.pad(m, (pad + 1, pad))); return (c[2 * pad + 1:] - c[:-2 * pad - 1]) > 0
        for tgt, vet, key in (("S", "R", "true"), ("R", "S", "swap")):
            vP = np.zeros(n, bool); v2 = np.zeros(n, bool)
            for i in range(6):
                if ROLES[i] == vet: vP |= dil(per[i][W]["vmax"], ZVETO); v2 |= dil(per[i][W]["z2"], Z2VETO)
            cP = c2 = 0
            for i in range(6):
                if ROLES[i] != tgt: continue
                ev = per[i][W]["ev"]; zz = per[i][W]["zev"]
                keep = [(int(c), int(s), float(z)) for (s, c), z in zip(ev, zz) if not vP[c]]
                keep.sort(); cl = []
                for c, s, z in keep:
                    if cl and c - cl[-1][0][-1] <= pad: cl[-1][0].append(c); cl[-1][1].append((z, s, c))
                    else: cl.append(([c], [(z, s, c)]))
                cP += len(cl)
                if key == "true":
                    for _, members in cl:
                        z, s, c = max(members); f = FCH1 + FOFF * (c0 + c); A = anchors_topo(i, s)
                        res["P_events"].append({"W": W, "scan": i, "sample": s, "f_MHz": round(f, 6), "z": round(z, 2),
                                                "off_kHz": {k: round((f - a) * 1e3, 2) for k, a in A.items()}, "in_tol": any(abs(f - a) <= TOL for a in A.values())})
                ix = np.where((per[i][W]["z2"] >= Z2) & ~v2)[0]
                g = np.split(ix, np.where(np.diff(ix) > pad)[0] + 1) if len(ix) else []
                c2 += len(g)
                if key == "true":
                    for gg in g:
                        c = int(gg[np.argmax(per[i][W]["z2"][gg])]); f = FCH1 + FOFF * (c0 + c); A = anchors_topo(i, 0)
                        res["P2_events"].append({"W": W, "scan": i, "f_MHz": round(f, 6), "z": round(float(per[i][W]["z2"][c]), 2),
                                                 "off_kHz": {k: round((f - a) * 1e3, 2) for k, a in A.items()}, "in_tol": any(abs(f - a) <= TOL for a in A.values())})
            res["P"].setdefault(key, {})[str(W)] = cP; res["P2"].setdefault(key, {})[str(W)] = c2
    return res

state = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": SHA, "node": NODE, "files": FILES, "windows": {}}
for wi in ([TARGET] if INJ else [TARGET] + [k for k in range(11) if k != TARGET]):
    if str(wi) in state["windows"]: continue
    t0 = time.time(); r = run_window(wi); state["windows"][str(wi)] = r
    json.dump(state, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(wi, r["f_lo"], "P", r["P"], "P2", r["P2"], "%.0fs" % (time.time() - t0), flush=True)
Wd = state["windows"]
if not INJ and len(Wd) == 11:
    tot = lambda w, det, key: sum(w[det][key].values())
    tgt = {d: tot(Wd[str(TARGET)], d, "true") for d in ("P", "P2")}
    ctl = {d: [tot(Wd[str(k)], d, "true") for k in range(11) if k != TARGET] for d in ("P", "P2")}
    sw = {d: tot(Wd[str(TARGET)], d, "swap") for d in ("P", "P2")}
    intol = any(e["in_tol"] for e in Wd[str(TARGET)]["P_events"] + Wd[str(TARGET)]["P2_events"])
    state["summary"] = {"target": tgt, "controls": ctl, "swap": sw, "any_in_tol": intol,
                        "lead": bool(intol and any(tgt[d] > max(ctl[d]) and tgt[d] > sw[d] for d in ("P", "P2")))}
    json.dump(state, open(OUT, "w"), indent=1); print("SUMMARY", state["summary"], flush=True)
