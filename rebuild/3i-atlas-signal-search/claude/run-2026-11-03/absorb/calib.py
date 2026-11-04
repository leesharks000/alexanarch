"""OH absorption calibration, GBT 2025-12-18 (absorb/PLAN-absorb-calib.md, sha256 62d0a126...).  python3 absorb/calib.py -> absorb/calib.json"""
import json, re, urllib.request, urllib.parse, numpy as np, fsspec, h5py, hdf5plugin, concurrent.futures as cf
SHA = "62d0a126ff28564dcff58873f27e936144d84bc8c93c38e6d5d9cd8e4e11faf2"; C = 299792.458
U = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; LINES = {"OH1665": 1665.4018, "OH1667": 1667.3590, "OH1612": 1612.2310}
W, EXCL, CORE, BIN = 0.060, 0.008, 0.004, 0.0028   # MHz
idx = urllib.request.urlopen(U, timeout=60).read().decode()
F = sorted(set(re.findall(r'(blc23_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_001[3-8]\.rawspec\.0000\.h5)', idx)), key=lambda x: x[-20:-16])
fs = fsspec.filesystem("https", block_size=8 << 20)
D = [h5py.File(fs.open(U + f))["data"] for f in F]; A = [d.attrs for d in D]
T = [float(a["tstart"]) + (np.arange(d.shape[0]) + 0.5) * float(a["tsamp"]) / 86400 for a, d in zip(A, D)]
def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
         "SITE_COORD": "'-79.8398,38.4331,0.807'", "START_TIME": f"'JD {t0 + 2400000.5 - 0.003:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'",
         "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])
E = horizons(T[0][0], T[-1][-1] + 0.002)
f1, fo = float(A[0]["fch1"]), float(A[0]["foff"]); df = abs(fo)
out = {"plan_sha256": SHA, "files": F, "v_kms": [round(float(np.interp(T[0][0], E[:, 0], E[:, 1])), 4), round(float(np.interp(T[-1][-1], E[:, 0], E[:, 1])), 4)], "lines": {}}

def scan_avg(i, f0, frame):
    v = np.interp(T[i], E[:, 0], E[:, 1]); pos = f0 * (1 - v / C) if frame == "comet" else np.full(len(v), f0)
    ch = lambda f: (f - f1) / fo; lo, hi = sorted((ch(pos.min() - W - 0.01), ch(pos.max() + W + 0.01))); c0 = int(lo); n = int(hi) - c0 + 1
    X = D[i][:, 0, c0:c0 + n].astype(np.float64); nu = int(W / df)
    cc = np.rint(ch(pos) - c0).astype(int); G = np.stack([X[k, cc[k] - nu:cc[k] + nu + 1] for k in range(X.shape[0])])
    return G.mean(0), (np.arange(-nu, nu + 1) * df * np.sign(fo))   # offset in MHz (positive = higher frequency)

def analyse(spec, off):
    nb = int(BIN / df); m = len(spec) // nb; s = spec[:m * nb].reshape(m, nb).mean(1); o = off[:m * nb].reshape(m, nb).mean(1)
    if o[0] > o[-1]: s, o = s[::-1], o[::-1]
    base = np.abs(o) > EXCL; p = np.polyfit(o[base], s[base], 3); r = s - np.polyval(p, o)
    sig = 1.4826 * np.median(np.abs(r[base] - np.median(r[base])))
    def depth(c): return float(r[np.abs(o - c) <= CORE].mean() / sig)
    ctl = [depth(c) for c in np.r_[np.linspace(-0.055, -0.015, 20), np.linspace(0.015, 0.055, 20)]]
    return {"centre": round(depth(0.0), 2), "controls_min": round(min(ctl), 2), "controls_rank": int(sum(c <= depth(0.0) for c in ctl)),
            "sigma_frac": float(sig), "centre_frac": float(r[np.abs(o) <= CORE].mean()), "spectrum": [[round(float(a) * 1e3, 2), round(float(b), 7)] for a, b in zip(o, r)]}

ON, OFFS = [0, 2, 4], {0: (1, 1), 2: (1, 3), 4: (3, 5)}
for name, f0 in LINES.items():
    out["lines"][name] = {}
    for frame in ("comet", "topo"):
        with cf.ThreadPoolExecutor(1) as ex: av = list(ex.map(lambda i: scan_avg(i, f0, frame), range(6)))
        offs = av[0][1]; pairs = {i: av[i][0] / ((av[OFFS[i][0]][0] + av[OFFS[i][1]][0]) / 2) - 1 for i in ON}
        res = {}
        for lab, use in (("all3", ON), ("no0017", [0, 2])):
            res[lab] = analyse(np.mean([pairs[i] for i in use], 0), offs)
        res["per_pair"] = {F[i][-20:-16]: analyse(pairs[i], offs)["centre"] for i in ON}
        out["lines"][name][frame] = res
        print(name, frame, {k: (v["centre"], v["controls_min"], v["controls_rank"]) for k, v in res.items() if k != "per_pair"}, res["per_pair"], flush=True)
json.dump(out, open("absorb/calib.json", "w"), indent=0)
