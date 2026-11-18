"""Comet frame in the S, C and X cadences of 2025-12-18 (ocad/PLAN-ocad.md; sha256 in PLAN.sha256).
    python3 run_ocad.py  -> order.json (written once, before any spectrum), ocad.json (resumable; each channel written before the next is read)
Procedure and arithmetic copied from lee/run_lee.py; changes: cadence scan lists, T0 = the cadence's first ON start, pool and order."""
import os, re, json, time, urllib.request, urllib.parse, concurrent.futures as CF
import numpy as np, fsspec, h5py, hdf5plugin
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = open("PLAN.sha256").read().split()[0]
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"; C = 299792.458; NF = 1048576; DC = slice(NF // 2 - 4, NF // 2 + 5)
CAD = {"S": (["0029", "0031", "0033"], ["0030", "0032", "0034"]), "C": (["0045", "0047", "0049"], ["0046", "0048", "0050"]),
       "X": (["0061", "0063", "0065"], ["0062", "0064", "0066"])}
HD = json.load(open("headers.json")); idx = urllib.request.urlopen(B, timeout=60).read().decode()
FILES = {(v["node"], v["scan"]): k for k, v in HD.items()}
H = {(v["node"], v["scan"]): v for v in HD.values()}
def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER",
         "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC", "SITE_COORD": "'-79.8398,38.4331,0.807'",
         "START_TIME": f"'JD {t0 + 2400000.5:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'",
         "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return txt, np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])
tall = [v["tstart"] for v in HD.values()]
if not os.path.exists("horizons.json"):
    txt, E = horizons(min(tall) - 0.005, max(tall) + 0.02); json.dump({"raw": txt, "E": E.tolist()}, open("horizons.json", "w"))
E = np.array(json.load(open("horizons.json"))["E"]); deldot = lambda t: np.interp(t, E[:, 0], E[:, 1])
# pool
pool, twin = [], {}
for cad, (on, off) in CAD.items():
    nodes = [v for v in HD.values() if v["scan"] == on[0]]
    seen = {}
    for v in sorted(nodes, key=lambda v: v["node"]):
        k = round(v["fch1"], 6)
        if k in seen: twin[(cad, seen[k])] = v["node"]
        else: seen[k] = v["node"]
    for nd in sorted(seen.values(), key=lambda n: -H[(n, on[0])]["fch1"]):
        for cc in range(64): pool.append((cad, nd, cc))
DONE = {("S", "blc23", 30)} | {("X", "blc72", c) for c in range(60, 64)} | {("X", "blc73", c) for c in range(14)}
pool = [p for p in pool if p not in DONE]
def ch_of(cad, f_mhz):
    on, off = CAD[cad]; ts = [H[(n, s)]["tstart"] for (n, s) in H if s in on + off]; tm = (min(ts) + max(ts) + 300 / 86400) / 2
    ft = f_mhz * (1 - deldot(tm) / C)
    for (c, nd, cc) in pool:
        if c != cad: continue
        h = H[(nd, on[0])]; a = h["fch1"] + h["foff"] * h["nfpc"] * cc; b = a + h["foff"] * h["nfpc"]
        if min(a, b) <= ft < max(a, b): return (c, nd, cc), ft
    return None, ft
LINES = [("CH3OH 6668.5192", "C", 6668.5192), ("OH 6035.0932", "C", 6035.0932), ("OH 6030.7485", "C", 6030.7485), ("H2CO 4829.6594", "C", 4829.6594),
         ("OH 4765.562", "C", 4765.562), ("OH 4750.656", "C", 4750.656), ("OH 4660.242", "C", 4660.242), ("CH3OH 12178.597", "X", 12178.597)]
if not os.path.exists("order.json"):
    named = []
    for name, cad, f in LINES:
        p, ft = ch_of(cad, f)
        named.append({"line": name, "f_topo_MHz": ft, "ch": list(p) if p else None})
    nset = []
    for n in named:
        if n["ch"] and tuple(n["ch"]) not in nset: nset.append(tuple(n["ch"]))
    perm = np.random.default_rng(41).permutation(len(pool))
    rand = [pool[i] for i in perm if pool[i] not in nset][:64 - len(nset)]
    json.dump({"plan_sha256": PLAN, "named": named, "order": [list(x) for x in nset] + [list(x) for x in rand], "n_named": len(nset),
               "pool_size": len(pool), "twins": {f"{k[0]}_{k[1]}": v for k, v in twin.items()}}, open("order.json", "w"), indent=0)
O = json.load(open("order.json")); ORDER = [tuple(x) for x in O["order"]]
OUT = "ocad.json"; st = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": PLAN, "channels": {}}
key = lambda c, nd, cc: f"{c}_{nd}_cc{cc:02d}"
def fetch(nd, s, cc):
    for attempt in range(5):
        try:
            f = fsspec.open(B + FILES[(nd, s)], "rb", block_size=8 << 20).open(); d = h5py.File(f, "r")["data"]
            nfpc = int(d.attrs["nfpc"]); lo = cc * nfpc
            return d[:, 0, lo:lo + nfpc].astype(np.float32)
        except Exception as e:
            print("retry", nd, s, cc, e, flush=True); time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"fetch failed {nd} {s} {cc}")
def fetch_channel(cad, nd, cc):
    on, off = CAD[cad]
    with CF.ThreadPoolExecutor(2) as ex:
        fu = {s: ex.submit(fetch, nd, s, cc) for s in on + off}
        return {s: fu[s].result() for s in on + off}
r11 = np.random.default_rng(11); OFFS = [0.0] + list(r11.uniform(0.03, 1.0, 40) * r11.choice([-1, 1], 40) * C / 1.42e9)
def survey_channel(cad, nd, cc, X):
    ON, OFF = CAD[cad]; S6 = ON + OFF; T0 = min(H[(nd, s)]["tstart"] for s in ON)
    foff = H[(nd, ON[0])]["foff"] * 1e6
    Y, f0 = {}, {}
    for s in S6:
        x = X.pop(s); med = np.median(x, axis=0); y = x.astype(np.float64); del x
        y /= med; y -= 1.0
        yb = y.copy(); yb += np.roll(y, 1, axis=1); yb += np.roll(y, -1, axis=1); del y
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
    fmid = (f0[ON[0]] + foff * (NF // 2)) / 1e6
    return {"f_mid_MHz": round(fmid, 4), "T": rows[0]["on"], "swap": rows[0]["swap"], "mu": float(on.mean()), "sd": float(on.std()), "max": int(on.max()),
            "d_max": int(d.max()), "freqs_rest_MHz": freqs[:200], "rows": rows}
jobs = [j for j in ORDER if key(*j) not in st["channels"]]
print("jobs", len(jobs), flush=True)
ex = CF.ThreadPoolExecutor(1); nxt = ex.submit(fetch_channel, *jobs[0]) if jobs else None
for i, j in enumerate(jobs):
    t0 = time.time(); X = nxt.result()
    nxt = ex.submit(fetch_channel, *jobs[i + 1]) if i + 1 < len(jobs) else None
    tf = time.time() - t0
    r = survey_channel(*j, X); del X
    r["named"] = ORDER.index(j) < O["n_named"]
    st["channels"][key(*j)] = r
    json.dump(st, open(OUT + ".tmp", "w")); os.replace(OUT + ".tmp", OUT)
    print(f"{key(*j)} {r['f_mid_MHz']:.3f} T {r['T']} swap {r['swap']} null {r['mu']:.2f}+-{r['sd']:.2f} max {r['max']} dmax {r['d_max']} wait {tf:.0f}s total {time.time() - t0:.0f}s", flush=True)
print("ALLDONE", flush=True)
