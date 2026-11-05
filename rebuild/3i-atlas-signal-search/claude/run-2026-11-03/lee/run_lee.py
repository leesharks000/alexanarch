"""Global look-elsewhere survey (lee/PLAN-lee.md, sha256 3e8e00cccd00137248521a425320ad6c86961470af17d3251250c6493bbbd439).
    python3 run_lee.py   -> lee.json (resumable per channel; each channel written before the next is read)
Reads are those of lheld/fetch_cc.py (HTTP range reads of one coarse channel, all time steps), held in memory; the six scans of a
channel are fetched in parallel threads and the next channel is prefetched while the current one is computed. The count procedure is
lheld/run_lheld.py's, with cf.tracked's arithmetic (x/median - 1, boxcar, roll, robust z, DC zeroed) computed once per scan per channel."""
import sys, os, re, json, time, urllib.request, urllib.parse, concurrent.futures as CF
import numpy as np, fsspec, h5py, hdf5plugin
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = "3e8e00cccd00137248521a425320ad6c86961470af17d3251250c6493bbbd439"
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; C = 299792.458
ON, OFF = ["0013", "0015", "0017"], ["0014", "0016", "0018"]; S6 = ON + OFF
NODES = ["blc22", "blc23", "blc24", "blc25"]; NF = 1048576; DC = slice(NF // 2 - 4, NF // 2 + 5)
idx = urllib.request.urlopen(B, timeout=60).read().decode()
FILES = {}
for nd in NODES:
    for f in sorted(set(re.findall(r'(' + nd + r'_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_001[3-8]\.rawspec\.0000\.h5)', idx))): FILES[(nd, f[-20:-16])] = f
OUT = "lee.json"
st = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": PLAN, "channels": {}}
# reuse (plan): lheld's fifteen
LH = json.load(open("../lheld/lheld.json"))["channels"]
for k, v in LH.items():
    if k not in st["channels"]:
        on = np.array([r["on"] for r in v["rows"][1:]]); d = np.array([r["on"] - r["swap"] for r in v["rows"][1:]])
        st["channels"][k] = {"f_mid_MHz": v["f_mid_MHz"], "T": v["true_on"], "swap": v["true_swap"], "mu": float(on.mean()), "sd": float(on.std()), "max": int(on.max()),
                             "d_max": int(d.max()), "source": "lheld/lheld.json", "freqs": v.get("true_on_freqs_MHz", [])}
H = {}
def header(nd, s):
    f = fsspec.open(B + FILES[(nd, s)], "rb", block_size=8 << 20).open(); d = h5py.File(f, "r")["data"]; a = d.attrs
    return {"fch1": float(a["fch1"]), "foff": float(a["foff"]), "nfpc": int(a["nfpc"]), "tsamp": float(a["tsamp"]), "tstart": float(a["tstart"])}
def fetch(nd, s, cc):
    for attempt in range(4):
        try:
            f = fsspec.open(B + FILES[(nd, s)], "rb", block_size=8 << 20).open(); d = h5py.File(f, "r")["data"]
            nfpc = int(d.attrs["nfpc"]); lo = cc * nfpc
            return d[:, 0, lo:lo + nfpc].astype(np.float32)
        except Exception as e:
            print("retry", nd, s, cc, e, flush=True); time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"fetch failed {nd} {s} {cc}")
def fetch_channel(nd, cc):
    with CF.ThreadPoolExecutor(int(os.environ.get("LEE_THREADS", "2"))) as ex:   # 6 threads ran slower than sequential (run.log, first channel)
        fu = {s: ex.submit(fetch, nd, s, cc) for s in S6}
        return {s: fu[s].result() for s in S6}
for nd in NODES:
    for s in S6: H[(nd, s)] = header(nd, s)
t_all = [H[("blc23", s)]["tstart"] for s in S6]
def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER",
         "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC", "SITE_COORD": "'-79.8398,38.4331,0.807'",
         "START_TIME": f"'JD {t0 + 2400000.5:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'",
         "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])
E = horizons(min(t_all) - 0.005, max(t_all) + 0.02); T0 = min(t_all)
deldot = lambda t: np.interp(t, E[:, 0], E[:, 1])
r11 = np.random.default_rng(11); OFFS = [0.0] + list(r11.uniform(0.03, 1.0, 40) * r11.choice([-1, 1], 40) * C / 1.42e9)
def survey_channel(nd, cc, X):
    foff = H[(nd, "0013")]["foff"] * 1e6
    Y, f0 = {}, {}
    for s in S6:
        x = X.pop(s); med = np.median(x, axis=0); y = x.astype(np.float64); del x
        y /= med; y -= 1.0                                   # = x / med - 1, as in cf.tracked
        yb = y.copy(); yb += np.roll(y, 1, axis=1); yb += np.roll(y, -1, axis=1); del y   # (y + roll1) + roll-1, same order
        Y[s] = yb
        f0[s] = (H[(nd, s)]["fch1"] + H[(nd, s)]["foff"] * cc * H[(nd, s)]["nfpc"]) * 1e6
    def tracked(s, dv):
        h = H[(nd, s)]; y = Y[s]; nt = y.shape[0]
        t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0
        v = deldot(t) + dv * (t - T0) * 86400.0
        shift = np.rint(f0[s] * (v[0] - v) / C / foff).astype(int)
        acc = np.zeros(NF)
        for k in range(nt): acc += np.roll(y[k], -shift[k])
        m = np.median(acc); z = (acc - m) / (1.4826 * np.median(np.abs(acc - m))); z[DC] = 0.0
        return z, (f0[s] + foff * np.arange(NF)) / (1.0 - v[0] / C)
    def align(dv):
        zs = {s: tracked(s, dv) for s in S6}; ref = zs[ON[0]][1]; A = {}
        for s in S6:
            ix = np.rint((zs[s][1] - ref[0]) / foff).astype(int); z = zs[s][0]
            a = np.full(NF + 2000, -99.0); ok = (ix + 1000 >= 0) & (ix + 1000 < len(a)); a[ix[ok] + 1000] = z[ok]
            A[s] = np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
        return A, ref
    def hits(A, Tg, R):
        ok = np.ones_like(A[ON[0]], bool)
        for s in Tg: ok &= A[s] >= 2.5
        for s in R: ok &= A[s] < 2.0
        return np.where(ok)[0]
    tol = int(10 / abs(foff)) + 1; cl = lambda i: 0 if not len(i) else 1 + int(np.sum(np.diff(np.sort(i)) > tol))
    rows = []; freqs = []
    for k, dv in enumerate(OFFS):
        A, ref = align(dv); p = hits(A, ON, OFF); q = hits(A, OFF, ON); rows.append({"on": cl(p), "swap": cl(q)})
        if k == 0: freqs = sorted({round((ref[0] + (i - 1000) * foff) / 1e6, 6) for i in p})
    on = np.array([r["on"] for r in rows[1:]]); d = np.array([r["on"] - r["swap"] for r in rows[1:]])
    fmid = (f0["0013"] + foff * (NF // 2)) / 1e6
    return {"f_mid_MHz": round(fmid, 4), "T": rows[0]["on"], "swap": rows[0]["swap"], "mu": float(on.mean()), "sd": float(on.std()), "max": int(on.max()),
            "d_max": int(d.max()), "source": "lee/run_lee.py", "freqs": freqs[:200], "rows": rows}
# deviation (RESULTS-lee.md): channels run in a fixed random order (seed 29), so that a survey stopped early is a random sample of the band
ALL = [(nd, cc) for nd in NODES for cc in range(64)]; ORDER = np.random.default_rng(29).permutation(len(ALL))
jobs = [ALL[i] for i in ORDER if f"{ALL[i][0]}_cc{ALL[i][1]:02d}" not in st["channels"]]
if "blc23_cc07" not in st["channels"]: jobs = [("blc23", 7)] + [j for j in jobs if j != ("blc23", 7)]   # cc07 first: E_cc07 is the reference
print("jobs", len(jobs), flush=True)
ex = CF.ThreadPoolExecutor(1); nxt = ex.submit(fetch_channel, *jobs[0]) if jobs else None
for i, (nd, cc) in enumerate(jobs):
    t0 = time.time(); X = nxt.result()
    nxt = ex.submit(fetch_channel, *jobs[i + 1]) if i + 1 < len(jobs) else None
    tf = time.time() - t0
    r = survey_channel(nd, cc, X); del X
    st["channels"][f"{nd}_cc{cc:02d}"] = r
    json.dump(st, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(f"{nd}_cc{cc:02d} {r['f_mid_MHz']:.3f} T {r['T']} swap {r['swap']} null {r['mu']:.2f}+-{r['sd']:.2f} max {r['max']} wait {tf:.0f}s total {time.time() - t0:.0f}s", flush=True)
# summary
R = st["channels"]
def Ev(v): return (v["T"] - v["mu"]) / max(v["sd"], 0.5)
def flag(v): return v["T"] > v["max"] and (v["T"] - v["swap"]) > v["d_max"]
e7 = Ev(R["blc23_cc07"]) if "blc23_cc07" in R else None
st["summary"] = {"channels": len(R), "E_cc07": e7, "p_LEE": (sum(Ev(v) >= e7 for v in R.values()) / len(R)) if e7 is not None else None,
                 "N_FLAG": sum(flag(v) for v in R.values()), "chance_N_FLAG": round(len(R) / 41, 2),
                 "flagged": sorted([{"ch": k, "f_mid_MHz": v["f_mid_MHz"], "T": v["T"], "swap": v["swap"], "mu": round(v["mu"], 2), "sd": round(v["sd"], 2), "max": v["max"], "E": round(Ev(v), 2)} for k, v in R.items() if flag(v)], key=lambda x: -x["E"]),
                 "top_E": sorted([{"ch": k, "f_mid_MHz": v["f_mid_MHz"], "T": v["T"], "E": round(Ev(v), 2), "flag": flag(v)} for k, v in R.items()], key=lambda x: -x["E"])[:15]}
json.dump(st, open(OUT, "w"), indent=0)
print("SUMMARY", json.dumps(st["summary"])[:3000], flush=True)
