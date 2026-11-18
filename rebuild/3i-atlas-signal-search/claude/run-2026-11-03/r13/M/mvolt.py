"""PLAN-M3: weird-as-voltage battery for one channel's ON hits.  python3 mvolt.py CC  -> volt/ccNN.json"""
import sys, os, json, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
cc = int(sys.argv[1]); dm.CH = cc; dm.FC = 1595.21484375e6 + 93.75e6 - (cc + 0.5) * 2.9296875e6
N, INT, C, DF, TBIN, FC = dm.N, dm.INT, dm.C, dm.DF, dm.TBIN, dm.FC
W = 64; COMPS = [-7200, -3600, -1800, 1800, 3600, 7200]
OFFROWS = {"0013": [0], "0014": [0, 1], "0015": [0, 1], "0016": [0, 1, 2], "0017": [0, 1], "0018": [0]}
N = dm.N; SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
HERE2 = HERE
# hit rule copied verbatim from mhits.py (PLAN-M2)
def load(cc): return {s: np.load(os.path.join(HERE2, "out2", f"cc{cc:02d}_{s}.npz")) for s in SC}
def fr(d, fi): return d[f"f{fi}_idx"].astype(np.int64), d[f"f{fi}_z"].astype(np.float32), float(d[f"f{fi}_v0"])
def hits(D, s, vetoes, fc):
    d = D[s]; offs = d["offs"]; nf = len(offs); drift = offs * 292.1 * fc / dm.C / dm.DF
    ti, tz, tv0 = fr(d, 0); keep = tz >= 4.0; P, Pz = ti[keep], tz[keep]
    if len(P) == 0: return []
    best = np.full(len(P), 0.0)
    for fi in range(1, nf):
        if abs(drift[fi]) < 6: continue
        idx, z, v0 = fr(d, fi); j = idx - int(np.rint(fc * (v0 - tv0) / dm.C / dm.DF)); o = np.argsort(j); j, z = j[o], z[o]
        lo = np.searchsorted(j, P - 2); hi = np.searchsorted(j, P + 3)
        for k in range(len(P)):
            if hi[k] > lo[k]: best[k] = max(best[k], float(z[lo[k]:hi[k]].max()))
    ok = Pz - best >= 1.0
    for v in vetoes:
        idx, z, v0 = fr(D[v], 0); j = np.sort(idx - int(np.rint(fc * (v0 - tv0) / dm.C / dm.DF)))
        lo = np.searchsorted(j, P - 3); hi = np.searchsorted(j, P + 4); ok &= (hi == lo)
    out = []; last = -99
    for p, z, b in sorted(zip(P[ok], Pz[ok], best[ok])):
        if p - last > 4: out.append({"bin": int(p), "mhz_topo": float((fc - (p - N // 2) * dm.DF) / 1e6), "z": float(z), "weirdness": float(z - b)})
        last = p
    return out
D = load(cc)
E = dm.ephem(); vel = lambda t: np.interp(t, E[:, 0], E[:, 1])
def v0_of(s): return float(D[s]["f0_v0"])
targets = {s: [] for s in SC}            # (label, start bin in that scan's comet frame)
hitlist = []
for s in ON:
    h = sorted(hits(D, s, OFF, FC), key=lambda x: -x["z"])[:10]
    for k, x in enumerate(h):
        hid = f"{s}#{k}"; p = x["bin"]; hitlist.append(dict(x, scan=s, id=hid))
        targets[s].append((hid + "|hit", p))
        for c in COMPS: targets[s].append((hid + f"|cmp{c:+d}", p + c))
        for o in OFF: targets[o].append((hid + f"|off{o}", p + int(np.rint(FC * (v0_of(o) - v0_of(s)) / C / DF))))
def battery(x):
    p = np.abs(x) ** 2; mu2 = p.mean(); k4 = float((p ** 2).mean() / mu2 ** 2)
    rate = 2 * W / (N * TBIN); env = p - mu2; S = np.abs(sf.rfft(env)) ** 2; f = np.arange(len(S)) * rate / len(x)
    fr = 1 / (N * TBIN); band = (f >= 0.1) & (f <= 50) & (np.abs(((f + fr / 2) % fr) - fr / 2) > 0.05)
    w1 = float(S[band].max() / np.median(S[band])); f1 = float(f[band][np.argmax(S[band])])
    S1 = np.abs(sf.fft(x)) ** 2; S2 = np.abs(sf.fft(x * x)) ** 2
    return {"k4": k4, "W1": w1, "W1_hz": f1, "pr1": float(S1.max() / np.median(S1)), "pr2": float(S2.max() / np.median(S2))}
res = {"cc": cc, "fc": FC, "hits": hitlist, "series": {}}; ts = time.time()
for s in SC:
    if not targets[s]: continue
    t0s = 61027 + int(dm.SCANS[s][0]) / 86400.0; nint = 833 // INT
    keepf = lambda j: (j // INT) < nint and (j // INT) not in OFFROWS[s]
    tk0 = t0s + ((OFFROWS[s][-1] + 1) * INT + INT / 2) * N * TBIN / 86400.0; v0 = vel(tk0)
    bufs = {lab: ([], []) for lab, _ in targets[s]}
    for j, X, Y in dm.frames(s, 833):
        if not keepf(j): continue
        tc = t0s + (j + 0.5) * N * TBIN / 86400.0; sh = int(np.rint(FC * (vel(tc) - v0) / C / DF))
        FX = dm.fft(X); FY = dm.fft(Y)
        for lab, p in targets[s]:
            b = p + sh
            if b - W < 0 or b + W > N: continue
            for q, F in ((0, FX), (1, FY)): bufs[lab][q].append(sf.ifft(sf.ifftshift(F[b - W:b + W])).astype(np.complex64))
    for lab, (bx, by) in bufs.items():
        if not bx: continue
        res["series"][lab] = {"X": battery(np.concatenate(bx)), "Y": battery(np.concatenate(by))}
    print(cc, s, "done", f"{time.time() - ts:.0f}s", flush=True)
nom = []
for h in hitlist:
    hid = h["id"]; ref = [k for k in res["series"] if k.startswith(hid + "|") and not k.endswith("|hit")]
    if hid + "|hit" not in res["series"] or not ref: continue
    for q in ("X", "Y"):
        me = res["series"][hid + "|hit"][q]; R = [res["series"][k][q] for k in ref]
        why = []
        if me["W1"] > 1.5 * max(r["W1"] for r in R): why.append(f"W1 {me['W1']:.1f} at {me['W1_hz']:.3f} Hz")
        if me["pr2"] > 1.5 * max(r["pr2"] for r in R) and me["pr2"] / me["pr1"] > 1.5 * max(r["pr2"] / r["pr1"] for r in R): why.append(f"suppressed carrier pr2 {me['pr2']:.1f}, pr2/pr1 {me['pr2'] / me['pr1']:.2f}")
        if why: nom.append({"hit": hid, "feed": q, "why": why, "bin": h["bin"], "mhz_topo": h["mhz_topo"], "z": h["z"], "k4": me["k4"]})
res["nominations"] = nom
os.makedirs(os.path.join(HERE, "volt"), exist_ok=True)
json.dump(res, open(os.path.join(HERE, "volt", f"cc{cc:02d}.json"), "w"), indent=1)
print(cc, "nominations", len(nom), flush=True)
