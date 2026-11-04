"""Time profile of a 31.360 kHz tooth grid in one 4 MHz chunk: every sample of all six scans. python3 wow/comb_time.py node f_lo_MHz phase_Hz"""
import sys, re, json, urllib.request, concurrent.futures as cf, numpy as np
_a = sys.argv; sys.argv = [_a[0]]; sys.path.insert(0, "pks"); from fullband import get, header, R; sys.argv = _a
node, flo, phz = _a[1], float(_a[2]) * 1e6, float(_a[3]); F0 = 1420.402360e6 + phz; P = 31360.0; EX = cf.ThreadPoolExecutor(24)
idx = urllib.request.urlopen(R + node + "/", timeout=60).read().decode()
files = sorted(set(re.findall(r'href="([^"]+_[SR]_0001\.0000\.fil)"', idx)))
print(node, flo / 1e6, "grid phase", phz, "Hz")
for i, f in enumerate(files):
    h = header(R + node + "/" + f); n, f1, fo = h['nchans'], h['fch1'] * 1e6, h['foff'] * 1e6; m = int(4e6 / abs(fo))
    c0 = int(round((flo + 4e6 - f1) / fo)) if fo < 0 else int(round((flo - f1) / fo))
    def one(s):
        a = h['hdr_len'] + (s * n + c0) * 4; return s, np.frombuffer(get(R + node + "/" + f, a, a + m * 4 - 1), '<f4').astype(np.float32)
    X = np.zeros((20, m), np.float32)
    for s, x in EX.map(one, range(20)): X[s] = x
    med = np.median(X, 0); med[med == 0] = 1; r = X / med - 1; fr = f1 + fo * (c0 + np.arange(m))
    t = np.abs(fr - F0 - np.round((fr - F0) / P) * P) < 6
    z = []
    for s in range(20):
        mm = np.median(r[s]); sd = 1.4826 * np.median(np.abs(r[s] - mm)); z.append((r[s][t].mean() - mm) / (sd / np.sqrt(t.sum())))
    print(" ", "S" if "_S_" in f else "R", i, " ".join(f"{x:6.1f}" for x in z), flush=True)
