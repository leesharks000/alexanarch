"""EXPLORATORY open look (not a frozen test): ATA 3I/ATLAS public spectra, narrow windows at physically motivated frequencies, along the comet's
true Doppler path (the drift class the published positive-only filter removed), the sign-flipped path (the class it kept), and dish-fixed.
Two simultaneous beams per scan: beam0000 on-source, beam0001 reference (ChatGPT 2026-11-02: beam 0 header matches pointing; beam 1 offset 0.262 deg).
  python3 ata/look.py  -> ata/look.json (resumable per scan x target), ata/look.log"""
import json, os, re, sys, time, urllib.request, urllib.parse, multiprocessing as mp
import numpy as np
C = 299792.458; OUT = sys.argv[1] if len(sys.argv) > 1 else "ata/look.json"; HALF = 0.03   # MHz window half-width around each path
T = {"HI": 1420.405752, "WowE": 1420.4556, "WowM": 1420.726, "OH1612": 1612.231, "OH1665": 1665.4018, "C03": 1665.633777, "OH1667": 1667.359,
     "OH1720": 1720.53, "A2380": 2380.0, "2HI": 2840.811504}
if len(sys.argv) > 2: T = json.loads(open(sys.argv[2]).read())
ATA = "'-121.4733,40.8178,1.019'"
M = json.load(open("ata/ata_map.json"))["files"]

def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
         "SITE_COORD": ATA, "START_TIME": f"'JD {t0 + 2400000.5 - 0.003:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'", "QUANTITIES": "'20'",
         "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])
def rz(a):
    m = np.median(a, -1, keepdims=True); s = 1.4826 * np.median(np.abs(a - m), -1, keepdims=True); s[s == 0] = 1; return (a - m) / s

def read(u, c0, n):
    import fsspec, h5py, hdf5plugin
    fs = fsspec.filesystem("https", block_size=1 << 20)
    for k in range(4):
        try: return h5py.File(fs.open(u))["data"][:, 0, c0:c0 + n].astype(np.float64)
        except Exception as e:
            if k == 3: raise
            time.sleep(3 + 5 * k)

def job(args):
    key, u0, u1, tname, f0, E = args
    h = M[u0]; f1, fo, nt = h["fch1"], h["foff"], h["shape"][0]
    t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400; v = np.interp(t, E[:, 0], E[:, 1])
    paths = {"comet": f0 * (1 - v / C), "flipped": f0 * (1 - (2 * v[0] - v) / C), "topo": np.full(nt, f0)}   # flipped: same start, drift of opposite sign
    ch = lambda f: (f - f1) / fo
    allp = np.concatenate(list(paths.values())); lo, hi = sorted((ch(allp.min() - HALF), ch(allp.max() + HALF)))
    c0 = int(lo); n = int(hi) - c0 + 1
    if c0 < 0 or c0 + n > h["nchans"]: return key, {"error": "window off file edge"}
    X = {b: read(uu, c0, n) for b, uu in (("on", u0), ("ref", u1))}
    df = abs(fo) * 1e6; NU = int(HALF * 1e6 / df) - 5; res = {"f0": f0, "df_Hz": df, "nt": nt, "v_kms": [round(v[0], 4), round(v[-1], 4)],
            "drift_Hz_s": round(float((paths["comet"][-1] - paths["comet"][0]) * 1e6 / ((t[-1] - t[0]) * 86400)), 4), "paths": {}}
    R = {b: (x / np.where(np.median(x, 0) == 0, 1, np.median(x, 0)) - 1.0) for b, x in X.items()}
    for pn, p in paths.items():
        cc = np.rint(ch(p) - c0).astype(int)
        G = {b: np.stack([r[k, cc[k] - NU:cc[k] + NU + 1] for k in range(nt)]) for b, r in R.items()}
        za = {b: rz(g.mean(0)[None])[0] for b, g in G.items()}; zs = {b: rz(g) for b, g in G.items()}
        for tb, rb, lab in (("on", "ref", pn), ("ref", "on", pn + "_swap")):
            rv = np.convolve((np.abs(za[rb]) >= 2) | (np.abs(zs[rb]).max(0) >= 4), np.ones(5), "same") > 0
            feats = []
            for kind, z, thr in (("avg", za[tb], 4.0), ("sample", zs[tb].max(0), 5.0)):
                ix = np.where((z >= thr) & ~rv)[0]
                for g in (np.split(ix, np.where(np.diff(ix) > 2)[0] + 1) if len(ix) else []):
                    c = int(g[np.argmax(z[g])]); ser = G[tb][:, c]; srz = (ser - np.median(ser)) / (1.4826 * np.median(np.abs(ser - np.median(ser))) + 1e-12)
                    pos = np.clip(ser, 0, None); top2 = float(np.sort(pos)[-2:].sum() / (pos.sum() + 1e-12))
                    ac1 = float(np.corrcoef(ser[:-1], ser[1:])[0, 1]) if nt > 2 else 0.0
                    feats.append({"kind": kind, "u": c - NU, "off_Hz": round(float((c - NU) * df * np.sign(fo)), 1), "z": round(float(z[c]), 2), "z_avg": round(float(za[tb][c]), 2),
                                  "z_other": round(float(za[rb][c]), 2), "peak_sample": int(np.argmax(ser)), "top2_frac": round(top2, 3), "ac1": round(ac1, 3),
                                  "bits": "".join("1" if x > 1.0 else "0" for x in srz)})
            res["paths"][lab] = feats
    return key, res

if __name__ == "__main__":
    st = json.load(open(OUT)) if os.path.exists(OUT) else {"note": "exploratory; not a frozen test", "runs": {}}
    scans = {}
    for u, h in M.items():
        if "JPLH_ATLAS" not in u or "error" in h: continue
        m = re.search(r"ATA_ATLAS/([^/]+)/([^/]+)/([^/]+)/.+-beam000([01])\.fbh5$", u)
        if not m: continue
        scans.setdefault((m.group(1), m.group(2), m.group(3)), {})[m.group(4)] = u
    jobs = []; Ecache = {}
    for (sess, sc, tun), b in sorted(scans.items()):
        if "0" not in b or "1" not in b: continue
        h = M[b["0"]]; lo, hi = sorted((h["fch1"], h["fch1"] + h["foff"] * h["nchans"]))
        for tn, f0 in T.items():
            if not (lo + 0.5 < f0 < hi - 0.5): continue
            key = f"{sess}|{sc}|{tun}|{tn}"
            if key in st["runs"]: continue
            if sess not in Ecache:
                ts = [M[x["0"]]["tstart"] for (s2, _, _), x in scans.items() if s2 == sess and "0" in x]; Ecache[sess] = horizons(min(ts), max(ts) + 0.02)
            jobs.append((key, b["0"], b["1"], tn, f0, Ecache[sess]))
    print("jobs", len(jobs), flush=True)
    with mp.Pool(10) as pool:
        for i, (key, r) in enumerate(pool.imap_unordered(job, jobs)):
            st["runs"][key] = r
            if i % 5 == 0 or i == len(jobs) - 1: json.dump(st, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
            nf = {p: len(v) for p, v in r.get("paths", {}).items()}
            print(i, key, r.get("drift_Hz_s"), nf, r.get("error", ""), flush=True)
    json.dump(st, open(OUT, "w"), indent=0)
