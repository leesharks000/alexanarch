"""Comb search across the Parkes band (wow/PLAN-comb.md). python3 wow/comb_band.py blc05 [blc04 ...] -> wow/comb_<node>.json (resumable)"""
import sys, os, re, json, urllib.request, concurrent.futures as cf, numpy as np
_a = sys.argv; sys.argv = [_a[0]]; sys.path.insert(0, "pks"); from fullband import get, header, R; sys.argv = _a
F0 = 1420.402360e6; PER = {"31.360": 31360.0, "31.250": 31250.0, "30.000": 30000.0, "33.333": 100000.0 / 3}
EP, BASE = (10, 11), (3, 4, 15, 16); EX = cf.ThreadPoolExecutor(24)
def fold(r, fr, Phz):
    ph = np.mod(fr - F0, Phz); nb = int(round(Phz / 2.0)); b = np.minimum((ph / Phz * nb).astype(int), nb - 1)
    s = np.bincount(b, r, nb); c = np.bincount(b, None, nb); p = s / np.maximum(c, 1)
    p = np.convolve(np.concatenate([p[-3:], p, p[:3]]), np.ones(7) / 7, "valid")
    m = np.median(p); sd = 1.4826 * np.median(np.abs(p - m)); j = int(np.argmax(p))
    off = (j + 0.5) / nb * Phz; off = off - Phz if off > Phz / 2 else off
    return float((p[j] - m) / sd), float(off)
for node in sys.argv[1:]:
    out = f"wow/comb_{node}.json"; st = json.load(open(out)) if os.path.exists(out) else {"plan": "PLAN-comb.md", "chunks": {}}
    idx = urllib.request.urlopen(R + node + "/", timeout=60).read().decode()
    files = sorted(set(re.findall(r'href="([^"]+_[SR]_0001\.0000\.fil)"', idx)))
    if len(files) != 6: print(node, "files", len(files)); continue
    fS = files[0]; h = header(R + node + "/" + fS); n, f1, fo = h['nchans'], h['fch1'] * 1e6, h['foff'] * 1e6
    lo_all = min(f1, f1 + fo * n); m = int(4e6 / abs(fo))
    for k in range(n // m):
        if str(k) in st["chunks"]: continue
        c0 = k * m
        def one(s):
            a = h['hdr_len'] + (s * n + c0) * 4; return s, np.frombuffer(get(R + node + "/" + fS, a, a + m * 4 - 1), '<f4').astype(np.float64)
        D = dict(EX.map(one, EP + BASE)); med = np.median([D[s] for s in BASE], 0); med[med == 0] = 1
        r = np.mean([D[s] for s in EP], 0) / med - 1; fr = f1 + fo * (c0 + np.arange(m))
        res = {p: fold(r, fr, P) for p, P in PER.items()}
        zt = res["31.360"][0]; zc = max(res[p][0] for p in PER if p != "31.360")
        st["chunks"][str(k)] = {"f_lo_MHz": round(float(fr.min()) / 1e6, 3), "fold": res, "comb": bool(zt >= 6 and zt - zc >= 2)}
        json.dump(st, open(out, "w"))
        print(node, st["chunks"][str(k)]["f_lo_MHz"], "z31.36 %.1f off %.0f Hz | ctrl max %.1f" % (zt, res["31.360"][1], zc), "COMB" if st["chunks"][str(k)]["comb"] else "", flush=True)
