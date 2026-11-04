"""Reply-frequency doublet search (reply/PLAN-2380.md, sha256 e0754a9a...).
  python3 reply/r2380.py pks [--inject]   -> reply/r2380_pks[_inject].json
  python3 reply/r2380.py gbt              -> reply/r2380_gbt.json"""
import sys, os, re, json, time, urllib.request, urllib.parse, concurrent.futures as cf
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pks"))
_a = sys.argv; sys.argv = [_a[0]]
from fullband import get, header, R as PKS_R
sys.argv = _a
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.time import Time
import astropy.units as u
SHA = "e0754a9a4bb3081329bbb4f9529c258909f09984af8b1e0f0804b57d433b26c5"
C = 299792.458; F0 = 2380.0; KS = [-10, -8, -6, -4, -2, 2, 4, 6, 8, 10]; TOLHZ = 15000.0
INST = sys.argv[1]; INJ = "--inject" in sys.argv
OUT = f"reply/r2380_{INST}{'_inject' if INJ else ''}.json"
SITE = {"pks": ("148.2635,-32.9984,0.415", EarthLocation(lon=148.2635 * u.deg, lat=-32.9984 * u.deg, height=415 * u.m)),
        "gbt": ("-79.8398,38.4331,0.807", EarthLocation(lon=-79.8398 * u.deg, lat=38.4331 * u.deg, height=807 * u.m))}[INST]
SP = {"pks": {"target": [4, 5, 6], "ctl7": [7], "ctl9": [9]}, "gbt": {"target": [3, 4], "ctl6": [6], "ctl7": [7]}}[INST]

def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
         "SITE_COORD": f"'{SITE[0]}'", "START_TIME": f"'JD {t0 + 2400000.5 - 0.003:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'",
         "STEP_SIZE": "'1 m'", "QUANTITIES": "'1,20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD", "ANG_FORMAT": "DEG"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = []
    for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines():
        v = [x.strip() for x in l.split(",")]; nums = []
        for x in v[1:]:
            try: nums.append(float(x))
            except ValueError: pass
        rows.append((float(v[0]) - 2400000.5, nums[0], nums[1], nums[-1]))   # mjd, ra, dec, deldot
    return np.array(rows)

def rz(a):
    m = np.median(a, -1, keepdims=True); s = 1.4826 * np.median(np.abs(a - m), -1, keepdims=True); s[s == 0] = 1; return (a - m) / s

def scans_meta():
    """per scan: on, t (mjd per sample), fch1 MHz, foff MHz, reader(c0, n) -> (nt, n) float32"""
    if INST == "pks":
        nd = "blc15"; idx = urllib.request.urlopen(PKS_R + nd + "/", timeout=60).read().decode()
        files = sorted(set(re.findall(r'href="([^"]+_[SR]_0001\.0000\.fil)"', idx))); assert len(files) == 6
        ex = cf.ThreadPoolExecutor(24); out = []
        for fn in files:
            h = header(PKS_R + nd + "/" + fn); nch = h['nchans']
            def rd(c0, n, h=h, fn=fn, nch=nch):
                def one(k):
                    a = h['hdr_len'] + (k * nch + c0) * 4; return k, np.frombuffer(get(PKS_R + nd + "/" + fn, a, a + n * 4 - 1), '<f4')
                X = np.zeros((20, n), np.float32)
                for k, row in ex.map(one, range(20)): X[k] = row
                return X
            out.append({"name": fn, "on": "_S_" in fn, "t": h['tstart'] + (np.arange(20) + 0.5) * h['tsamp'] / 86400, "fch1": h['fch1'], "foff": h['foff'], "nch": nch, "read": rd,
                        "src": (h.get('src_raj'), h.get('src_dej'))})
        return out
    import fsspec, h5py, hdf5plugin
    U = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; idx = urllib.request.urlopen(U, timeout=60).read().decode()
    files = sorted(set(re.findall(r'(blc24_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_00(?:29|3[0-4])\.rawspec\.0000\.h5)', idx)), key=lambda x: x[-20:-16]); assert len(files) == 6, files
    fs = fsspec.filesystem("https", block_size=8 << 20); out = []
    for fn in files:
        f = fs.open(U + fn); hh = h5py.File(f); d = hh["data"]; a = d.attrs
        def rd(c0, n, d=d):
            return d[:, 0, c0:c0 + n].astype(np.float32)
        out.append({"name": fn, "on": "_OFF_" not in fn, "t": float(a["tstart"]) + (np.arange(d.shape[0]) + 0.5) * float(a["tsamp"]) / 86400, "fch1": float(a["fch1"]),
                    "foff": float(a["foff"]), "nch": int(a["nchans"]), "read": rd, "src": (float(a["src_raj"]), float(a["src_dej"]))})
    return out

S = scans_meta()
E = horizons(min(s["t"][0] for s in S), max(s["t"][-1] for s in S) + 0.002)
ra0, de0 = float(np.interp(S[0]["t"][0], E[:, 0], E[:, 1])), float(np.interp(S[0]["t"][0], E[:, 0], E[:, 2]))
print("horizons ra/dec", ra0, de0, "header src", S[0]["src"], flush=True)
coord = SkyCoord(ra=ra0 * u.deg, dec=de0 * u.deg)   # deviation, recorded: source position from Horizons, header src fields printed for comparison
def positions(s, f0):
    v = np.interp(s["t"], E[:, 0], E[:, 3])
    corr = coord.radial_velocity_correction(kind="barycentric", obstime=Time(s["t"], format="mjd"), location=SITE[1]).to(u.km / u.s).value
    return {"topo": np.full(len(s["t"]), f0), "comet": f0 * (1 - v / C), "bary": f0 * (1 + corr / C)}

DF = abs(S[0]["foff"]) * 1e6; NU = int(TOLHZ / DF) + 12
CENTERS = {"target": F0, **{f"k{k:+d}": F0 + k for k in KS}}
state = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": SHA, "inst": INST, "df_Hz": DF, "centers": {}}
if INJ: CENTERS = {"target": F0}

def mapped(s, f0):
    P = positions(s, f0); allp = np.concatenate(list(P.values()))
    ch = lambda f: (f - s["fch1"]) / s["foff"]
    lo, hi = sorted((ch(allp.min()), ch(allp.max()))); c0 = int(np.floor(lo)) - NU - 50; n = int(np.ceil(hi)) - c0 + NU + 50
    X = s["read"](c0, n).astype(np.float64); med = np.median(X, 0); med[med == 0] = 1; r = X / med - 1.0
    if INJ and s["on"]:
        pc = ch(P["comet"]) - c0
        for k in range(r.shape[0]):
            j = int(round(pc[k] + 3000.0 / (s["foff"] * 1e6)))
            sd = 1.4826 * np.median(np.abs(r[k] - np.median(r[k]))) / np.sqrt(r.shape[0])
            r[k, j] += 6 * sd; r[k, j + int(round(10.0 / DF))] += 6 * sd
    M = {}
    for fr, p in P.items():
        cc = np.rint(ch(p) - c0).astype(int); M[fr] = np.stack([r[k, cc[k] - NU:cc[k] + NU + 1] for k in range(r.shape[0])])
    return M

def doublet(z, sp):
    out = np.full(z.shape, -np.inf)
    for s in sp: out[..., :-s] = np.maximum(out[..., :-s], np.minimum(z[..., :-s], z[..., s:]))
    return out
def near(mask, w=2):
    c = np.cumsum(np.pad(mask.astype(int), (w + 1, w))); return (c[2 * w + 1:] - c[:-2 * w - 1]) > 0

for cname, f0 in CENTERS.items():
    if cname in state["centers"]: continue
    t0 = time.time(); Ms = [mapped(s, f0) for s in S]; ons = [s["on"] for s in S]
    res = {"f0": f0, "frames": {}}
    win = np.abs(np.arange(-NU, NU + 1)) * DF <= TOLHZ
    for fr in ("topo", "comet", "bary"):
        A = [rz(M[fr].mean(0)[None])[0] for M in Ms]; Z = [rz(M[fr]) for M in Ms]
        R2 = {}
        for spn, sp in (SP.items() if cname == "target" else [("target", SP["target"])]):
            Da = [doublet(a, sp) for a in A]; Dz = [doublet(z, sp) for z in Z]; rr = {}
            for tgt_on, key in ((True, "true"), (False, "swap")):
                T = [i for i in range(6) if ons[i] == tgt_on]; V = [i for i in range(6) if ons[i] != tgt_on]
                vA = np.zeros(len(win), bool); vS = np.zeros(len(win), bool)
                for i in V: vA |= near(Da[i] >= 3); vS |= near(Da[i] >= 3) | near(Dz[i].max(0) >= 4)
                hit = [near(Da[i] >= 4) for i in T]; per = (np.sum(hit, 0) >= 2) & ~vA & win
                ix = np.where(per)[0]; groups = np.split(ix, np.where(np.diff(ix) > 2)[0] + 1) if len(ix) else []
                pers = [{"u": int(g[np.argmax(sum(Da[i][g] for i in T))]) - NU, "off_Hz": round((int(g[np.argmax(sum(Da[i][g] for i in T))]) - NU) * DF, 1),
                         "D_on": [round(float(Da[i][g].max()), 2) for i in T]} for g in groups]
                sing = []
                for i in T:
                    ev = np.argwhere((Dz[i] >= 5) & ~vS[None] & win[None]); ev = ev[np.argsort(ev[:, 1])]; last = -99
                    for k, c in ev:
                        if c - last > 2: sing.append({"scan": i, "sample": int(k), "u": int(c) - NU, "off_Hz": round((int(c) - NU) * DF, 1), "D": round(float(Dz[i][k, c]), 2)})
                        last = c
                rr[key] = {"persistent": pers, "single": sing, "count": len(pers) + len(sing)}
            R2[spn] = rr
        res["frames"][fr] = R2
    state["centers"][cname] = res
    json.dump(state, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(cname, f0, {fr: (v["target"]["true"]["count"], v["target"]["swap"]["count"], len(v["target"]["true"]["persistent"])) for fr, v in res["frames"].items()}, "%.0fs" % (time.time() - t0), flush=True)
    del Ms

if not INJ and len(state["centers"]) == 11:
    summ = {}
    for fr in ("topo", "comet", "bary"):
        tg = state["centers"]["target"]["frames"][fr]
        t = tg["target"]["true"]["count"]; sw = tg["target"]["swap"]["count"]
        ctl = [state["centers"][f"k{k:+d}"]["frames"][fr]["target"]["true"]["count"] for k in KS]
        spc = [tg[k]["true"]["count"] for k in SP if k != "target"]
        summ[fr] = {"target": t, "swap": sw, "freq_controls": ctl, "spacing_controls": spc, "persistent": len(tg["target"]["true"]["persistent"]),
                    "lead": bool(t > max(ctl) and t > sw and t > max(spc) and len(tg["target"]["true"]["persistent"]) >= 1)}
    state["summary"] = summ; json.dump(state, open(OUT, "w"), indent=1); print("SUMMARY", json.dumps(summ), flush=True)
