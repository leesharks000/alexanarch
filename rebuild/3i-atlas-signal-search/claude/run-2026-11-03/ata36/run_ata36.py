"""Discovery half of ata36/PLAN-ata36.md (sha256 df74d8d5030f4c517d4c51b3190d95292fa548313c9dfeabe0e071d299979a7a).
    python3 run_ata36.py  -> disc.json (resumable per block), nominees.json at the end
ATA 2025-07-03, tuning LoD.C1504, the first eight of the 16 scans, both beams; the strip 3648.0-3687.75 MHz in blocks of 524,288 channels
overlapped by 4,096 on each side. The held-out eight scans are not read here."""
import os, json, time, urllib.request, urllib.parse, concurrent.futures as CF
import numpy as np, fsspec, h5py, hdf5plugin
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = "df74d8d5030f4c517d4c51b3190d95292fa548313c9dfeabe0e071d299979a7a"
C = 299792.458; ATA = "'-121.4733,40.8178,1.019'"
M = json.load(open("../ata/ata_map.json"))["files"]
U0 = sorted([k for k, v in M.items() if v.get("fch1") and abs(v["fch1"] - 3591.75) < 1 and k.endswith("beam0000.fbh5")], key=lambda k: M[k]["tstart"])
assert len(U0) == 16
SC = [(u, u.replace("beam0000", "beam0001")) for u in U0]
DISC = SC[:8]
h = M[U0[0]]; FCH1, FOFF, NT, NCH = h["fch1"], h["foff"], h["shape"][0], h["nchans"]
FOFF_HZ = FOFF * 1e6
ch = lambda f: int(round((f - FCH1) / FOFF))
S0, S1 = ch(3648.0), NCH                       # the strip
NB, OV = 524288, 4096
BLOCKS = [(a, min(a + NB, S1)) for a in range(S0, S1, NB)]
SCAT = [ch(f) for f in (3605.0, 3615.0, 3625.0, 3635.0)]    # scatter reference blocks (deviation: sampled, RESULTS-ata36.md)
OUT = "disc.json"
st = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": PLAN, "blocks": {}, "scatter": {}}

def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
         "SITE_COORD": ATA, "START_TIME": f"'JD {t0 + 2400000.5 - 0.003:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5 + 0.003:.6f}'", "STEP_SIZE": "'1 m'", "QUANTITIES": "'20'",
         "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])
TS = {u: M[u]["tstart"] + (np.arange(NT) + 0.5) * M[u]["tsamp"] / 86400.0 for u, _ in SC}
E = horizons(min(M[u]["tstart"] for u in U0), max(TS[u][-1] for u in U0))
json.dump(E.tolist(), open("horizons.json", "w"))
deldot = lambda t: np.interp(t, E[:, 0], E[:, 1]); T0 = TS[DISC[0][0]][0]
r11 = np.random.default_rng(11); OFFS = [0.0] + list(r11.uniform(0.03, 1.0, 40) * r11.choice([-1, 1], 40) * C / 1.42e9)

def read(u, a, b):
    for k in range(5):
        try:
            f = fsspec.open(u, "rb", block_size=4 << 20).open()
            return h5py.File(f, "r")["data"][:, 0, a:b].astype(np.float32)
        except Exception as e:
            print("retry", u[-60:], a, e, flush=True); time.sleep(5 + 10 * k)
    raise RuntimeError("read failed")
def prep(x):
    y = x / np.where(np.median(x, 0) == 0, 1, np.median(x, 0)) - 1.0
    return y + np.roll(y, 1, 1) + np.roll(y, -1, 1)
def rz(a):
    m = np.median(a); s = 1.4826 * np.median(np.abs(a - m)); return (a - m) / (s if s > 0 else 1)

tol = int(10 / abs(FOFF_HZ)) + 1
def block(a, b):
    lo, hi = max(a - OV, 0), min(b + OV, NCH); core = slice(a - lo, a - lo + (b - a))
    with CF.ThreadPoolExecutor(4) as ex:
        fu = {(i, bm): ex.submit(read, uu, lo, hi) for i, (u0, u1) in enumerate(DISC) for bm, uu in ((0, u0), (1, u1))}
        Y, SCB = {}, {}
        for k, f in fu.items():
            x = f.result(); r = x[:, (a - lo):(a - lo) + (b - a)] / np.median(x[:, (a - lo):(a - lo) + (b - a)], 0) - 1.0
            SCB[f"{k[0]}_{k[1]}"] = float(1.4826 * np.median(np.abs(r - np.median(r)))); del r
            Y[k] = prep(x); del x
    f0 = (FCH1 + FOFF * (lo + hi) / 2) * 1e6
    out = []
    for dv in OFFS:
        vref = deldot(T0)
        Z = {}
        for (i, bm), y in Y.items():
            t = TS[DISC[i][0]]; v = deldot(t) + dv * (t - T0) * 86400.0
            sh = np.rint(f0 * (vref - v) / C / FOFF_HZ).astype(int)
            acc = np.zeros(y.shape[1], np.float64)
            for k in range(NT): acc += np.roll(y[k], -sh[k])
            z = rz(acc[core]); Z[(i, bm)] = np.maximum(np.maximum(z, np.roll(z, 1)), np.roll(z, -1))
        res = {}
        for lab, tb, rb in (("on", 0, 1), ("swap", 1, 0)):
            T = np.stack([Z[(i, tb)] for i in range(8)]); R = np.stack([Z[(i, rb)] for i in range(8)])
            ok = ((T >= 2.5).sum(0) >= 6) & (T.mean(0) >= 3.0) & (R < 2.0).all(0)
            ix = np.where(ok)[0]
            res[lab] = [[int(a + j), round(float(T[:, j].mean()), 3)] for j in ix]
        out.append(res)
    return out, SCB
def scatter(a):
    with CF.ThreadPoolExecutor(4) as ex:
        fu = {(i, bm): ex.submit(read, uu, a, a + 524288) for i, (u0, u1) in enumerate(DISC) for bm, uu in ((0, u0), (1, u1))}
        return {f"{i}_{bm}": float(1.4826 * np.median(np.abs((lambda y: y - np.median(y))(f.result() / np.median(f.result(), 0) - 1.0)))) for (i, bm), f in fu.items()}

for a in SCAT:
    if str(a) not in st["scatter"]:
        t0 = time.time(); st["scatter"][str(a)] = scatter(a); json.dump(st, open(OUT, "w"))
        print("scatter ref", a, f"{time.time() - t0:.0f}s", flush=True)
for a, b in BLOCKS:
    if str(a) in st["blocks"]: continue
    t0 = time.time(); r, scb = block(a, b)
    st["blocks"][str(a)] = {"b": b, "scatter": scb, "frames": r}
    json.dump(st, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(f"block {a} {FCH1 + FOFF * a:.3f} MHz on {len(r[0]['on'])} swap {len(r[0]['swap'])} {time.time() - t0:.0f}s", flush=True)

# discovery summary and nominees (written and hashed before any held-out power is read)
def clusters(ixv):
    if not ixv: return []
    ixv = sorted(ixv); out = [[ixv[0]]]
    for p in ixv[1:]:
        (out[-1].append(p) if p[0] - out[-1][-1][0] <= tol else out.append([p]))
    return out
cnt = {"on": [], "swap": []}; true_cl = None
for k in range(len(OFFS)):
    for lab in ("on", "swap"):
        allh = [tuple(x) for blk in st["blocks"].values() for x in blk["frames"][k][lab]]
        cl = clusters(allh); cnt[lab].append(len(cl))
        if k == 0 and lab == "on": true_cl = cl
on = np.array(cnt["on"][1:]); d = np.array(cnt["on"][1:]) - np.array(cnt["swap"][1:])
T, sw = cnt["on"][0], cnt["swap"][0]; mu, sd = float(on.mean()), float(on.std())
refsc = np.array([v for blk in st["scatter"].values() for v in blk.values()]); stsc = np.array([v for blk in st["blocks"].values() for v in blk["scatter"].values()])
noms = sorted([{"rest_MHz_at_ref": round(FCH1 + FOFF * max(c, key=lambda p: p[1])[0], 7), "channel": max(c, key=lambda p: p[1])[0], "mean_z": max(p[1] for p in c), "n_channels": len(c)} for c in true_cl], key=lambda x: -x["mean_z"])[:10]
summ = {"T": T, "swap": sw, "false_on": cnt["on"][1:], "false_swap": cnt["swap"][1:], "mu": mu, "sd": sd, "max": int(on.max()), "d_max": int(d.max()),
        "E": (T - mu) / max(sd, 0.5), "FLAG": bool(T > on.max() and (T - sw) > d.max()), "blocks": len(st["blocks"]),
        "scatter_ratio_strip_over_ref_median": float(np.median(stsc) / np.median(refsc)), "nominees": noms,
        "note": "rest_MHz_at_ref is the frequency in the rest frame of the first discovery scan's first sample (received there); the held-out runner converts with the saved Horizons rows"}
st["summary"] = summ; json.dump(st, open(OUT, "w"))
json.dump({"plan_sha256": PLAN, "summary": summ}, open("nominees.json", "w"), indent=1)
print("SUMMARY", json.dumps({k: v for k, v in summ.items() if k not in ("false_on", "false_swap")})[:3000], flush=True)
