"""Context for one column of look2_parkes (PKS 2025-07-31, 2,852 Hz below the revised vessel frequency in the comet frame, S-scan
stack 5.56): the same stack over 40 neighbouring windows of the same six scans (centres at the revised frequency +- 25 kHz x k,
k = 1..20, comet frame), to see how high the largest column of an ordinary window stands, in the S scans and in the R scans.
Written after the column was seen; post hoc.   python3 look2_parkes_ctrl.py"""
import json, os, re, urllib.request, numpy as np, concurrent.futures as cf
from scipy.ndimage import median_filter
import look2_parkes_lib as L
HERE = os.path.dirname(os.path.abspath(__file__))
B = "https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/blc05/"
names = sorted(set(re.findall(r'href="([^"]*\.0000\.fil)"', urllib.request.urlopen(B, timeout=60).read().decode())))
H = [L.filhdr(B + n) for n in names]; vel = L.horizons(min(h["tstart"] for h in H), max(h["tstart"] for h in H))
def window(i, f0):
    h = H[i]; t = h["tstart"] + (np.arange(20) + 0.5) * h["tsamp"] / 86400.0; v = vel(t)
    ch = np.rint((f0 * (1 - v / L.C) - h["fch1"]) / h["foff"]).astype(int); W = np.empty((20, 2 * L.HALF + 1), np.float32)
    for k in range(20):
        a0 = h['hdr_len'] + (k * h['nchans'] + ch[k] - L.HALF) * 4; W[k] = np.frombuffer(L.get(B + names[i], a0, a0 + (2 * L.HALF + 1) * 4 - 1), '<f4')
    z = L.zmap(W); return z.mean(0) * np.sqrt(20)
def unit(k):
    f0 = L.F0["revised"] + 0.025 * k; ln = [window(i, f0) for i in range(6)]
    st = lambda idx: sum(np.clip(ln[i], -5, 5) for i in idx) / np.sqrt(3)
    S = st([i for i in range(6) if "_S_" in names[i]]); R = st([i for i in range(6) if "_R_" in names[i]])
    return {"k": k, "S_max": float(S.max()), "R_max": float(R.max()), "S_n_ge4.5": int((S >= 4.5).sum()), "R_n_ge4.5": int((R >= 4.5).sum())}
ks = [k for k in range(-20, 21) if k != 0]
with cf.ThreadPoolExecutor(6) as ex: res = list(ex.map(unit, ks))
for r in res: print(r, flush=True)
a = np.array([r["S_max"] for r in res] + [r["R_max"] for r in res])
out = {"windows": res, "max_of_80_stacks": float(a.max()), "median": float(np.median(a)), "n_ge_5.56": int((a >= 5.56).sum())}
print({k: v for k, v in out.items() if k != "windows"}); json.dump(out, open(os.path.join(HERE, "look2_parkes_ctrl.json"), "w"), indent=1)
