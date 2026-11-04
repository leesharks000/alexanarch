"""[ratio/ratio_gbt.py: derived from wow/wow_gbt.py for ratio/PLAN-ratio.md, sha256 1cd2fef8...; z >= 5; list frequencies in the 2214-2401 MHz cadence]
Wow!-guided intermittent search, GBT 2025-12-18 blc24 .0002.h5 (wow/PLAN-wow.md, sha256 10ecba29...). Detector G per the plan, over the
target window and the ten control windows, all four cadences. Downloads one cadence at a time (6 x ~52 MB), deletes after.
  python3 wow/wow_gbt.py            -> wow/wow_gbt.json
  python3 wow/wow_gbt.py --inject   -> wow/wow_gbt_inject.json (first cadence, target window; injection check)"""
import sys, os, re, json, urllib.request, urllib.parse, subprocess
import numpy as np, h5py, hdf5plugin
U = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; SHA = "1cd2fef8e4e77372059dab25b0547ec2c6e72232d468943eaee09b01684c395d"
C = 299792.458; WS = [1, 2, 4]; LS = [1, 10, 67]; ZEV, ZVETO = 5.0, 4.0
HI = 1420.405752; LIST = {"alpha 5/3": 5 / 3 * HI, "ctrl 11/7": 11 / 7 * HI}; TOL = 0.015
INJ = False; OUT = "ratio/ratio_gbt.json"
idx = urllib.request.urlopen(U, timeout=60).read().decode()
F = sorted(set(re.findall(r'(blc24_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_(\d{4})\.rawspec\.0002\.h5)', idx)), key=lambda x: x[1])
CAD = [F[i:i + 6] for i in range(0, len(F), 6)]; assert len(CAD) == 4 and all(len(c) == 6 for c in CAD)

def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
         "SITE_COORD": "'-79.8398,38.4331,0.807'", "START_TIME": f"'JD {t0 + 2400000.5 - 0.003:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'",
         "STEP_SIZE": "'1 m'", "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])
def rz(a):
    m = np.median(a, -1, keepdims=True); s = 1.4826 * np.median(np.abs(a - m), -1, keepdims=True); s[s == 0] = 1; return (a - m) / s
def box(x, w, ax):
    if w == 1: return x
    c = np.cumsum(x, axis=ax); c = np.concatenate([np.zeros_like(np.take(c, [0], ax)), c], ax)
    n = x.shape[ax]; return (np.take(c, range(w, n + 1), ax) - np.take(c, range(0, n - w + 1), ax)) / np.sqrt(w)

state = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": SHA, "node": "blc24", "cadences": {}}
os.makedirs("wow/dl", exist_ok=True)
for ci, cad in enumerate(CAD[:1] if INJ else CAD):
    key = cad[0][1]
    if key in state["cadences"]: continue
    S = []
    for fn, scan in cad:
        p = "wow/dl/" + fn
        if not os.path.exists(p): subprocess.run(["curl", "-sS", "-o", p, U + fn], check=True)
        h = h5py.File(p); d = h["data"]; a = d.attrs
        f1, fo, ts, t0 = float(a["fch1"]), float(a["foff"]), float(a["tsamp"]), float(a["tstart"])
        S.append({"scan": scan, "on": "_OFF_" not in fn, "f1": f1, "fo": fo, "ts": ts, "t0": t0, "p": p, "nt": d.shape[0]})
        h.close()
    bandlo, bandhi = sorted((S[0]["f1"], S[0]["f1"] + S[0]["fo"] * 65536))
    inband = {k: f for k, f in LIST.items() if bandlo + 0.5 <= f <= bandhi - 0.5}
    if not inband:
        state["cadences"][key] = {"covers": False, "band_MHz": [bandlo, bandhi]}; json.dump(state, open(OUT, "w"))
        for s in S: os.remove(s["p"])
        print(key, "no list frequency", bandlo, bandhi, flush=True); continue
    E = horizons(min(s["t0"] for s in S), max(s["t0"] for s in S) + 0.01)
    out = {"scans": [s["scan"] for s in S], "freqs": {}}
    for name, f0 in inband.items():
        vlo, vhi = E[:, 1].min(), E[:, 1].max(); pos = [f0, f0 * (1 - vlo / C), f0 * (1 - vhi / C)]
        lo, hi = min(pos) - 0.3, max(pos) + 0.3; per = []
        for s in S:
            ch = lambda f: int(round((f - s["f1"]) / s["fo"]))
            c0, c1 = sorted((ch(lo), ch(hi))); x = h5py.File(s["p"])["data"][:, 0, c0:c1].astype(np.float64)
            med = np.median(x, 0); med[med == 0] = 1; r = x / med - 1.0
            j = np.arange(c0, c1); mask = (j % 1024 >= 1020) | (j % 1024 <= 3) | (np.abs(j % 1024 - 512) <= 2); r[:, mask] = 0
            d = {}
            for L in LS:
                for W in WS:
                    z = rz(box(box(r, L, 0), W, 1)); z[:, mask[:z.shape[1]]] = 0
                    ev = np.argwhere(z >= ZEV); d[(L, W)] = {"ev": ev, "z": z[ev[:, 0], ev[:, 1]] if len(ev) else np.array([]), "vmax": z.max(0)}
            per.append((s, c0, d))
        res = {"f_MHz": f0, "true": [], "swap": []}
        for L in LS:
            for W in WS:
                pad = W + 1
                for tgt_on, keyname in ((True, "true"), (False, "swap")):
                    veto = None
                    for s, c0, d in per:
                        if s["on"] != tgt_on:
                            m = (d[(L, W)]["vmax"] >= ZVETO).astype(int); cs = np.cumsum(np.pad(m, (pad + 1, pad))); v = (cs[2 * pad + 1:] - cs[:-2 * pad - 1]) > 0
                            veto = v if veto is None else (veto | v[:len(veto)] if len(v) >= len(veto) else veto[:len(v)] | v)
                    for s, c0, d in per:
                        if s["on"] != tgt_on: continue
                        keep = sorted((int(c), int(t), float(z)) for (t, c), z in zip(d[(L, W)]["ev"], d[(L, W)]["z"]) if c < len(veto) and not veto[c])
                        cl = []
                        for c, t, z in keep:
                            if cl and c - cl[-1][-1][0] <= pad: cl[-1].append((c, t, z))
                            else: cl.append([(c, t, z)])
                        for g in cl:
                            c, t, z = max(g, key=lambda q: q[2]); f = s["f1"] + s["fo"] * (c0 + c + (W - 1) / 2)
                            tm = s["t0"] + (t + L / 2) * s["ts"] / 86400; v = float(np.interp(tm, E[:, 0], E[:, 1]))
                            offs = {"topo": (f - f0) * 1e3, "comet": (f - f0 * (1 - v / C)) * 1e3}; fr = min(offs, key=lambda k: abs(offs[k]))
                            if abs(offs[fr]) <= TOL * 1e3:
                                res[keyname].append({"L": L, "W": W, "scan": s["scan"], "t_s": round(t * s["ts"], 1), "f_MHz": round(f, 5), "z": round(z, 2), "frame": fr, "off_kHz": round(offs[fr], 2)})
        out["freqs"][name] = res
        print(key, name, round(f0, 4), "true", len(res["true"]), "swap", len(res["swap"]), flush=True)
    state["cadences"][key] = out
    json.dump(state, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    for s in S: os.remove(s["p"])
