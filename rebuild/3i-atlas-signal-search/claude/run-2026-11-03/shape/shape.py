"""Arecibo-message shape search (shape/PLAN-shape.md, sha256 776fa6aa...).
  python3 shape/shape.py pks 2380 [--inject] | pks 1420 | gbt 2380 | gbt 1420   -> shape/shape_<inst>_<carrier>[_inject].json"""
import sys, os, re, json, time, urllib.request, urllib.parse, concurrent.futures as cf
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pks"))
_a = sys.argv; sys.argv = [_a[0]]
from fullband import get, header, R as PKS_R
sys.argv = _a
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.time import Time
import astropy.units as u
SHA = "776fa6aa01b21302e1e3f4b03e48defe3080f2abed5d06cac962bfec0895766e"
C = 299792.458; KS = [-10, -8, -6, -4, -2, 2, 4, 6, 8, 10]; TOLHZ = 15000.0; W0, W1 = 1282 / 1679, 397 / 1679
INST, CAR = sys.argv[1], sys.argv[2]; INJ = "--inject" in sys.argv; F0 = {"2380": 2380.0, "1420": 1420.405752}[CAR]
OUT = f"shape/shape_{INST}_{CAR}{'_inject' if INJ else ''}_v2.json"
SITE = {"pks": ("148.2635,-32.9984,0.415", EarthLocation(lon=148.2635 * u.deg, lat=-32.9984 * u.deg, height=415 * u.m)),
        "gbt": ("-79.8398,38.4331,0.807", EarthLocation(lon=-79.8398 * u.deg, lat=38.4331 * u.deg, height=807 * u.m))}[INST]
SP = {"pks": {"target": [4, 5, 6], "ctl7": [7], "ctl9": [9]}, "gbt": {"target": [3, 4], "ctl6": [6], "ctl7": [7]}}[INST]
L = {"pks": 11, "gbt": 28}[INST]

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
        rows.append((float(v[0]) - 2400000.5, nums[0], nums[1], nums[-1]))
    return np.array(rows)
def rz(a):
    m = np.median(a, -1, keepdims=True); s = 1.4826 * np.median(np.abs(a - m), -1, keepdims=True); s[s == 0] = 1; return (a - m) / s
def near(mask, w=2):
    c = np.cumsum(np.pad(mask.astype(int), (w + 1, w))); return (c[2 * w + 1:] - c[:-2 * w - 1]) > 0

def scans_meta():
    if INST == "pks":
        nd = {"2380": "blc15", "1420": "blc05"}[CAR]; idx = urllib.request.urlopen(PKS_R + nd + "/", timeout=60).read().decode()
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
            out.append({"name": fn, "on": "_S_" in fn, "t": h['tstart'] + (np.arange(20) + 0.5) * h['tsamp'] / 86400, "fch1": h['fch1'], "foff": h['foff'], "read": rd})
        return out
    import fsspec, h5py, hdf5plugin
    U = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; idx = urllib.request.urlopen(U, timeout=60).read().decode()
    cad = {"2380": r"(?:29|3[0-4])", "1420": r"1[3-8]"}[CAR]
    files = sorted(set(re.findall(r'(blc24_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_00' + cad + r'\.rawspec\.0000\.h5)', idx)), key=lambda x: x[-20:-16]); assert len(files) == 6, files
    fs = fsspec.filesystem("https", block_size=8 << 20); out = []
    for fn in files:
        d = h5py.File(fs.open(U + fn))["data"]; a = d.attrs
        out.append({"name": fn, "on": "_OFF_" not in fn, "t": float(a["tstart"]) + (np.arange(d.shape[0]) + 0.5) * float(a["tsamp"]) / 86400, "fch1": float(a["fch1"]),
                    "foff": float(a["foff"]), "read": (lambda c0, n, d=d: d[:, 0, c0:c0 + n].astype(np.float32))})
    return out

S = scans_meta()
E = horizons(min(s["t"][0] for s in S), max(s["t"][-1] for s in S) + 0.002)
coord = SkyCoord(ra=float(np.interp(S[0]["t"][0], E[:, 0], E[:, 1])) * u.deg, dec=float(np.interp(S[0]["t"][0], E[:, 0], E[:, 2])) * u.deg)
def positions(s, f0):
    v = np.interp(s["t"], E[:, 0], E[:, 3])
    corr = coord.radial_velocity_correction(kind="barycentric", obstime=Time(s["t"], format="mjd"), location=SITE[1]).to(u.km / u.s).value
    return {"topo": np.full(len(s["t"]), f0), "comet": f0 * (1 - v / C), "bary": f0 * (1 + corr / C)}
DF = abs(S[0]["foff"]) * 1e6; NU = int(TOLHZ / DF) + 12
CENTERS = {"target": F0} if INJ else {"target": F0, **{f"k{k:+d}": F0 + k for k in KS}}
state = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": SHA, "inst": INST, "carrier": F0, "df_Hz": DF, "L": L, "centers": {}}

def mapped(s, f0):
    P = positions(s, f0); allp = np.concatenate(list(P.values())); ch = lambda f: (f - s["fch1"]) / s["foff"]
    lo, hi = sorted((ch(allp.min()), ch(allp.max()))); c0 = int(np.floor(lo)) - NU - 50; n = int(np.ceil(hi)) - c0 + NU + 50
    X = s["read"](c0, n).astype(np.float64); med = np.median(X, 0); med[med == 0] = 1; r = X / med - 1.0
    if INJ and s is S[0]:
        pc = ch(P["comet"]) - c0; ks = range(4, 15)
        sd1 = 1.4826 * np.median(np.abs(r[4] - np.median(r[4])))
        for k in ks:
            j = int(round(pc[k] + 3000.0 / (s["foff"] * 1e6))); jo = int(round(pc[k] + 5000.0 / (s["foff"] * 1e6))); sp = int(round(10.0 / DF)) * int(np.sign(s["foff"]))
            a = 8 * sd1 / np.sqrt(L); r[k, j] += a; r[k, j + sp] += 0.309 * a; r[k, jo] += 6 * sd1 / np.sqrt(L)
    M = {}
    for fr, p in P.items():
        cc = np.rint(ch(p) - c0).astype(int); M[fr] = np.stack([r[k, cc[k] - NU:cc[k] + NU + 1] for k in range(r.shape[0])])
    return M

def boxt(x):
    c = np.cumsum(np.concatenate([np.zeros((1, x.shape[1])), x]), 0); return (c[L:] - c[:-L]) / np.sqrt(L)
def dstat(z, sp):
    out = np.full(z.shape, -np.inf); nrm = np.hypot(W0, W1)
    for s in sp:
        for a, b in ((W0, W1), (W1, W0)): out[..., :-s] = np.maximum(out[..., :-s], (a * z[..., :-s] + b * z[..., s:]) / nrm)
    return out

for cname, f0 in CENTERS.items():
    if cname in state["centers"]: continue
    t0 = time.time(); Ms = [mapped(s, f0) for s in S]; ons = [s["on"] for s in S]
    win = np.abs(np.arange(-NU, NU + 1)) * DF <= TOLHZ; res = {"f0": f0, "frames": {}}
    for fr in ("topo", "comet", "bary"):
        Z = [rz(boxt(M[fr])) for M in Ms]; R2 = {}
        tmpl = {"O": {"target": None}, "D": {k: v for k, v in SP.items()} if cname == "target" else {"target": SP["target"]}}
        for tn, sets in tmpl.items():
            R2[tn] = {}
            for spn, sp in sets.items():
                St = [z if tn == "O" else dstat(z, sp) for z in Z]; rr = {}
                for tgt_on, key in ((True, "true"), (False, "swap")):
                    T = [i for i in range(6) if ons[i] == tgt_on]; V = [i for i in range(6) if ons[i] != tgt_on]
                    veto = np.zeros(len(win), bool)
                    for i in V: veto |= near(St[i].max(0) >= 3)
                    sing = []
                    for i in T:
                        mx = St[i].max(0); ix = np.where((mx >= 5) & ~veto & win)[0]
                        for g in (np.split(ix, np.where(np.diff(ix) > 2)[0] + 1) if len(ix) else []):
                            c = int(g[np.argmax(mx[g])]); sing.append({"scan": i, "win": int(np.argmax(St[i][:, c])), "off_Hz": round((c - NU) * DF, 1), "stat": round(float(mx[c]), 2)})
                    hit = [near(St[i].max(0) >= 4) for i in T]; per = (np.sum(hit, 0) >= 2) & ~veto & win
                    ix = np.where(per)[0]
                    pers = []   # deviation, recorded 2026-11-04: a group counts only if two on-source scans reach >= 4 at an unvetoed in-window channel within the group +-2 (first run counted dilation edges whose >= 4 channels were vetoed)
                    for g in (np.split(ix, np.where(np.diff(ix) > 2)[0] + 1) if len(ix) else []):
                        ext = np.arange(max(g[0] - 2, 0), min(g[-1] + 3, len(win))); ok = ext[~veto[ext] & win[ext]]
                        mxs = [float(St[i].max(0)[ok].max()) if len(ok) else -9 for i in T]
                        if sum(m >= 4 for m in mxs) >= 2: pers.append({"off_Hz": round((int(g[0]) - NU) * DF, 1), "stat_on": [round(m, 2) for m in mxs]})
                    rr[key] = {"single": sing, "persistent": pers, "count": len(sing) + len(pers)}
                R2[tn][spn] = rr
        res["frames"][fr] = R2
    state["centers"][cname] = res
    json.dump(state, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(cname, f0, {fr: {tn: (v[tn]["target"]["true"]["count"], v[tn]["target"]["swap"]["count"]) for tn in ("O", "D")} for fr, v in res["frames"].items()}, "%.0fs" % (time.time() - t0), flush=True)
    del Ms
if not INJ and len(state["centers"]) == 11:
    summ = {}
    for fr in ("topo", "comet", "bary"):
        for tn in ("O", "D"):
            tg = state["centers"]["target"]["frames"][fr][tn]; t = tg["target"]["true"]["count"]; sw = tg["target"]["swap"]["count"]
            ctl = [state["centers"][f"k{k:+d}"]["frames"][fr][tn]["target"]["true"]["count"] for k in KS]
            spc = [tg[k]["true"]["count"] for k in tg if k != "target"]
            summ[f"{fr}/{tn}"] = {"target": t, "swap": sw, "freq_controls": ctl, "spacing_controls": spc,
                                  "lead": bool(t >= 1 and t > max(ctl) and t > sw and (not spc or t > max(spc)))}
    state["summary"] = summ; json.dump(state, open(OUT, "w"), indent=1); print("SUMMARY", json.dumps(summ), flush=True)
