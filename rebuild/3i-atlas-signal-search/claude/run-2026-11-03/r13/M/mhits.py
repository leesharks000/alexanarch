"""PLAN-M2 hits.  python3 mhits.py > M2.json"""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
N = dm.N; SC = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
def load(cc): return {s: np.load(os.path.join(HERE, "out2", f"cc{cc:02d}_{s}.npz")) for s in SC}
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
R = {"plan": open(os.path.join(HERE, "PLAN-M2.sha256")).read().split(), "channels": {}}
ccs = sorted({int(os.path.basename(f)[2:4]) for f in glob.glob(os.path.join(HERE, "out2", "cc*_0013.npz"))})
for cc in ccs:
    if not all(os.path.exists(os.path.join(HERE, "out2", f"cc{cc:02d}_{s}.npz")) for s in SC): continue
    D = load(cc); fc = float(D["0013"]["fc"]); e = {"fc_mhz": fc / 1e6}
    for s in SC:
        vet = OFF if s in ON else [x for x in SC if x != s]
        h = sorted(hits(D, s, vet, fc), key=lambda x: -x["weirdness"]); e[s] = {"role": dm.SCANS[s][2], "n": len(h), "top": h[:10]}
    offmax = max([e[s]["top"][0]["weirdness"] for s in OFF if e[s]["top"]] or [0])
    e["on_hits_beyond_every_off"] = [dict(x, scan=s) for s in ON for x in e[s]["top"] if x["weirdness"] > offmax]
    R["channels"][f"cc{cc:02d}"] = e
print(json.dumps(R, indent=1))
