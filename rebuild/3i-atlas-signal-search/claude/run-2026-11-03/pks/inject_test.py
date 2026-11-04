"""Injection check of fullband.py's tracking and alignment: one block of blc07, a tone at fixed rest frequency riding on the comet injected into the
three S scans (amplitude A x the channel's median per sample, one channel), then the fullband detector. Recovery near the injected rest channel = the
shifts and the cross-scan alignment have the right sign. python3 pks/inject_test.py"""
import numpy as np, json, re, urllib.request
src = open("pks/fullband.py").read()
exec(src.split("def run(node):")[0])
node = "blc07"
idx = urllib.request.urlopen(R + node + "/", timeout=60).read().decode()
files = sorted(set(re.findall(r'href="([^"]+_[SR]_0001\.0000\.fil)"', idx))); roles = ["S" if "_S_" in f else "R" for f in files]
H = [header(R + node + "/" + f) for f in files]; nch, foff, fch1 = H[0]['nchans'], H[0]['foff'] * 1e6, H[0]['fch1'] * 1e6
E = horizons(min(h['tstart'] for h in H), max(h['tstart'] for h in H) + 0.01)
t = [h['tstart'] + (np.arange(20) + 0.5) * h['tsamp'] / 86400.0 for h in H]; T0 = min(h['tstart'] for h in H)
b0 = 20 * (BLK - OV); n = BLK
X = np.zeros((6, 20, n), np.float32)
for i in range(6):
    for k in range(20):
        a = H[i]['hdr_len'] + (k * nch + b0) * 4; X[i, k] = np.frombuffer(get(R + node + "/" + files[i], a, a + n * 4 - 1), '<f4')
v0 = np.interp(t[0], E[:, 0], E[:, 1]); Fc = fch1 + foff * (b0 + n / 2)
inj = [200000, 500000, 800000]; A = 0.6
for i in range(6):
    if roles[i] != "S": continue
    v = np.interp(t[i], E[:, 0], E[:, 1])
    for j0 in inj:
        F = (fch1 + foff * (b0 + j0)) / (1 - v0[0] / C)      # rest freq whose topo channel at scan0's first sample is j0
        for k in range(20):
            ch = int(np.rint((F * (1 - v[k] / C) - fch1) / foff)) - b0
            X[i, k, ch] += A * np.median(X[i, :, ch])
Rn = []
for i in range(6):
    med = np.median(X[i], 0); med[med == 0] = 1; r = X[i] / med - 1.0; r = r + np.roll(r, 1, 1) + np.roll(r, -1, 1); Rn.append(r)
zs = []
for i in range(6):
    v = np.interp(t[i], E[:, 0], E[:, 1]); sh = np.rint(Fc * (v[0] - v) / C / foff).astype(int)
    acc = np.zeros(n)
    for k in range(20): acc += np.roll(Rn[i][k], -sh[k])
    m = np.median(acc); s = 1.4826 * np.median(np.abs(acc - m)); z = (acc - m) / s
    d = int(np.rint(Fc * (v0[0] - v[0]) / C / foff)) if i else 0
    zs.append(np.roll(z, -d) if d else z)
for j0 in inj:
    print("inject at", j0, {f"{roles[i]}{i}": round(float(zs[i][j0 - 2:j0 + 3].max()), 1) for i in range(6)}, "best ch S0:", int(np.argmax(zs[0][j0 - 50:j0 + 50])) - 50)
