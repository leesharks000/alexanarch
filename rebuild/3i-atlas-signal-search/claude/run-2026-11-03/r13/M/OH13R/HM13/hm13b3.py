"""PLAN-HM13-B3B5 B3: P1547B's lag-2 phase memory, all 833 frames, 199 surrogates.  python3 hm13b3.py SCAN -> b3_SCAN.json"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PD = os.path.join(HERE, "../../P1547"); sys.path.insert(0, PD)
import p1547 as P, p1547b as PB
dm, W, SCANS, SL = P.dm, P.W, P.SCANS, P.SL
NSUR, NFR, BLK = 199, 833, [(0, 208), (208, 416), (416, 624), (624, 833)]
def lag2(z):
    d = z[1:] * np.conj(z[:-1]); d /= np.maximum(np.abs(d), 1e-30); return np.sum(d[2:] * np.conj(d[:-2])), len(d) - 2
s = sys.argv[1]; i = SCANS.index(s); T0 = time.time()
seeds = {q: [1547000 + 100 * i + 10 * q + k if k < 19 else 2026112200 + 1000 * i + 500 * q + k for k in range(NSUR)] for q in (0, 1)}
rng = {q: [np.random.default_rng(x) for x in seeds[q]] for q in (0, 1)}
acc = {q: np.zeros((len(BLK), NSUR + 1), complex) for q in (0, 1)}; cnt = {q: np.zeros(len(BLK)) for q in (0, 1)}; g0 = {}
nf = 0
for j, x, y in dm.frames(s, NFR):
    b = next(k for k, (a, e) in enumerate(BLK) if a <= j < e)
    for q, v in ((0, x), (1, y)):
        G = PB.norm(dm.fft(v)[SL].astype(np.complex128)); a = np.abs(G)
        z, n = lag2(PB.series(G)); acc[q][b, 0] += z; cnt[q][b] += n
        for k in range(NSUR):
            acc[q][b, k + 1] += lag2(PB.series(a * np.exp(2j * np.pi * rng[q][k].random(W))))[0]
    nf += 1
    if nf == 16:
        for q in (0, 1): g0["XY"[q]] = (np.abs(acc[q][0, :20]) / cnt[q][0]).tolist()
    if nf % 100 == 0: print(s, nf, round(time.time() - T0), flush=True)
PBr = json.load(open(os.path.join(PD, f"pb_{s}.json"))); out = {"scan": s, "role": dm.SCANS[s][2], "frames": nf, "G0": {}}
for q in (0, 1):
    f = "XY"[q]; want = [PBr[f]["A"][0]] + [r[0] for r in PBr[f]["sA"]]; got = g0[f]
    out["G0"][f] = {"pass": bool(np.max(np.abs(np.array(got) - want) / np.abs(want)) < 1e-9), "max_rel": float(np.max(np.abs(np.array(got) - want) / np.abs(want)))}
    tot = np.abs(acc[q].sum(0)) / cnt[q].sum(); blk = np.abs(acc[q]) / cnt[q][:, None]
    pv = lambda v: float((1 + np.sum(v[1:] >= v[0])) / (NSUR + 1))
    out[f] = {"real": float(tot[0]), "sur_median": float(np.median(tot[1:])), "sur_max": float(tot[1:].max()), "p": pv(tot),
              "blocks": [{"frames": list(BLK[k]), "real": float(blk[k, 0]), "sur_median": float(np.median(blk[k, 1:])), "p": pv(blk[k])} for k in range(len(BLK))]}
json.dump(out, open(os.path.join(HERE, f"b3_{s}.json"), "w"), indent=1)
print(json.dumps({k: (v if k == "G0" else {kk: vv for kk, vv in v.items() if kk != "blocks"} if isinstance(v, dict) else v) for k, v in out.items()}), flush=True)
