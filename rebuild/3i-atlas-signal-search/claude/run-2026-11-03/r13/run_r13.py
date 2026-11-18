"""PLAN-r13 (sha256 in PLAN.sha256): the thirteen again: gate, row cuts (A), strength (B), injection (C), frames (D), ephemeris (E).
    python3 run_r13.py   -> r13.json (resumable by part). Arithmetic as lheld/run_lheld.py and ocad/run_ocad.py."""
import os, json, time, csv, urllib.request, urllib.parse
import numpy as np, fsspec, h5py, hdf5plugin
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PLAN = open("PLAN.sha256").read().split()[0]
C = 299792.458; NF = 1048576; DC = slice(NF // 2 - 4, NF // 2 + 5); CC = 7
ON, OFF = ["0013", "0015", "0017"], ["0014", "0016", "0018"]; S6 = ON + OFF
SM = {"0013": "17226", "0014": "17543", "0015": "17861", "0016": "18179", "0017": "18497", "0018": "18814"}
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
FN = lambda s: f"blc23_guppi_61027_{SM[s]}_DIAG_3I_ATLAS{'_OFF' if s in OFF else ''}_{s}.rawspec.0000.h5"
OUT = "r13.json"; R = json.load(open(OUT)) if os.path.exists(OUT) else {"plan_sha256": PLAN}
def save(): json.dump(R, open(OUT + ".tmp", "w"), indent=0, default=float); os.replace(OUT + ".tmp", OUT)

# ---------- data ----------
def fetch(s):
    for a in range(5):
        try:
            d = h5py.File(fsspec.open(B + FN(s), "rb", block_size=8 << 20).open(), "r")["data"]; t = d.attrs
            n = int(t["nfpc"]); h = {"fch1": float(t["fch1"]), "foff": float(t["foff"]), "nfpc": n, "tsamp": float(t["tsamp"]), "tstart": float(t["tstart"])}
            return d[:, 0, CC * n:(CC + 1) * n].astype(np.float32), h
        except Exception as e:
            print("retry", s, e, flush=True); time.sleep(10 * (a + 1))
    raise RuntimeError(s)
X, H = {}, {}
for s in S6:
    X[s], H[s] = fetch(s); print("fetched", s, X[s].shape, flush=True)
foff = H["0013"]["foff"] * 1e6; T0 = min(H[s]["tstart"] for s in ON)
F0 = {s: (H[s]["fch1"] + H[s]["foff"] * CC * H[s]["nfpc"]) * 1e6 for s in S6}
TT = {s: H[s]["tstart"] + (np.arange(X[s].shape[0]) + 0.5) * H[s]["tsamp"] / 86400.0 for s in S6}

# ---------- ephemeris (range-rate, RA, DEC) ----------
if not os.path.exists("horizons.json"):
    t0 = min(H[s]["tstart"] for s in S6) - 0.005; t1 = max(H[s]["tstart"] for s in S6) + 0.02
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "YES", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER",
         "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC", "SITE_COORD": "'-79.8398,38.4331,0.807'",
         "START_TIME": f"'JD {t0 + 2400000.5:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'",
         "QUANTITIES": "'1,20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD", "ANG_FORMAT": "DEG"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",")] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    E = [(float(r[0]) - 2400000.5, float(r[3]), float(r[4]), float(r[-2] if r[-1] == "" else r[-1])) for r in rows]
    json.dump({"raw": txt, "E": E}, open("horizons.json", "w"))
HJ = json.load(open("horizons.json")); E = np.array(HJ["E"])
deldot = lambda t: np.interp(t, E[:, 0], E[:, 3]); ra = lambda t: np.interp(t, E[:, 0], E[:, 1]); de = lambda t: np.interp(t, E[:, 0], E[:, 2])
if "E" not in R:
    sol = [l.strip() for l in HJ["raw"].splitlines() if "JPL#" in l or "Soln.date" in l or "soln ref" in l.lower()][:4]
    span = (max(TT[s][-1] for s in S6) - T0) * 86400.0; fmid = F0["0013"] + foff * NF / 2
    # acceleration error a moving a tone one channel across the cadence: f * a * span / c = foff
    R["E"] = {"solution_lines": sol, "cadence_span_s": span, "a_one_channel_km_s2": abs(foff) * C / (fmid * span),
              "false_min_km_s2": 0.03 * C / 1.42e9}
    save()

# ---------- frames ----------
from astropy.time import Time
from astropy.coordinates import EarthLocation, SkyCoord
import astropy.units as u
GBT = EarthLocation.from_geodetic(-79.8398 * u.deg, 38.4331 * u.deg, 807 * u.m)
def frame_v(name, t):
    if name == "comet": return deldot(t)
    if name == "flip": return -deldot(t)
    if name == "topo": return np.zeros_like(t)
    tm = Time(t, format="mjd", scale="utc"); n = SkyCoord(ra(t) * u.deg, de(t) * u.deg, frame="icrs")
    if name == "bary":
        return -n.radial_velocity_correction(kind="barycentric", obstime=tm, location=GBT).to(u.km / u.s).value
    if name == "geo":
        _, v = GBT.get_gcrs_posvel(tm); vx = v.xyz.to(u.km / u.s).value
        nx = np.vstack([np.cos(np.radians(de(t))) * np.cos(np.radians(ra(t))), np.cos(np.radians(de(t))) * np.sin(np.radians(ra(t))), np.sin(np.radians(de(t)))])
        return -(vx * nx).sum(0)
VF = {}
def vframe(name):
    if name not in VF: VF[name] = {s: frame_v(name, TT[s]) for s in S6}
    return VF[name]

# ---------- rows (part A) ----------
TEL = json.load(open("telemetry.json")); BT = 524288 * float(TEL["0013"]["0"]["TBIN"])
def offtarget_rows():
    out = {}
    for s in S6:
        d = TEL[s]; g = sorted(d, key=int)
        tr = [k for k in g if d[k]["TRK_MODE"] == "TRACK"]
        b = np.array([int(k) for k in tr], float); r_ = np.array([float(d[k]["RA"]) for k in tr]); e_ = np.array([float(d[k]["DEC"]) for k in tr])
        fr = np.polyfit(b, r_, 1); fd = np.polyfit(b, e_, 1)
        dev = np.hypot((r_ - np.polyval(fr, b)) * np.cos(np.radians(e_)), e_ - np.polyval(fd, b)) * 60
        bad = [int(k) for k in g if d[k]["TRK_MODE"] != "TRACK"] + [int(x) for x, y in zip(b, dev) if y > 0.2]
        rows = sorted({int(x * BT // H[s]["tsamp"]) for x in bad})
        info = {"nontrack_blocks": [int(k) for k in g if d[k]["TRK_MODE"] != "TRACK"], "max_dev_arcmin": float(dev.max()), "rows_off": rows}
        if s in ON:  # offset of the tracked line from the comet at the scan middle
            bm = b.mean(); tm = H[s]["tstart"] + bm * BT / 86400.0
            info["offset_from_comet_arcmin"] = float(np.hypot((np.polyval(fr, bm) - ra(tm)) * np.cos(np.radians(de(tm))), np.polyval(fd, bm) - de(tm)) * 60)
        out[s] = info
    return out
if "A" not in R: R["A"] = offtarget_rows(); save()
KEEP = {"V0": {s: np.ones(X[s].shape[0], bool) for s in S6},
        "V1": {s: np.arange(X[s].shape[0]) > 0 for s in S6},
        "V2": {s: ~np.isin(np.arange(X[s].shape[0]), R["A"][s]["rows_off"]) for s in S6}}

# ---------- detector ----------
r11 = np.random.default_rng(11); OFFS = [0.0] + list(r11.uniform(0.03, 1.0, 40) * r11.choice([-1, 1], 40) * C / 1.42e9)
COORD = {}
for r in csv.DictReader(open("../../voltages/delaymod/oh13_candidates.csv")): COORD[r["id"]] = float(r["f_rest_MHz"]) * 1e6
def prep(Xs, keep, w=3, inj=None):
    Y = {}
    for s in S6:
        x = Xs[s][keep[s]]
        if inj is not None and s in ON: x = inj(s, x.copy())
        med = np.median(x, axis=0); y = x.astype(np.float64) / med - 1.0
        acc = y.copy()
        for j in range(1, w // 2 + 1): acc += np.roll(y, j, axis=1) + np.roll(y, -j, axis=1)
        Y[s] = acc
    return Y
def run(Y, keep, frame, coords=True, w=3, extra=False):
    V = vframe(frame)
    def tracked(s, dv):
        t = TT[s][keep[s]]; y = Y[s]
        v = V[s][keep[s]] + dv * (t - T0) * 86400.0
        sh = np.rint(F0[s] * (v[0] - v) / C / foff).astype(int)
        acc = np.zeros(NF); rmax = np.full(NF, -99.0) if extra else None
        for k in range(y.shape[0]):
            r = np.roll(y[k], -sh[k]); acc += r
            if extra:
                m_ = np.median(r); zr = (r - m_) / (1.4826 * np.median(np.abs(r - m_))); np.maximum(rmax, zr, out=rmax)
        m = np.median(acc); z = (acc - m) / (1.4826 * np.median(np.abs(acc - m))); z[DC] = 0.0
        if extra: rmax[DC] = 0.0
        return z, (F0[s] + foff * np.arange(NF)) / (1.0 - v[0] / C), rmax
    rows = []; cl_true = []; S1 = []; B2 = {k: [] for k in COORD}
    IX = {"I1": [], "I2": [], "I3": []}
    tol = max(int(10 / abs(foff)) + 1, w); ncl = lambda i: 0 if not len(i) else 1 + int(np.sum(np.diff(np.sort(i)) > tol))
    for k, dv in enumerate(OFFS):
        zs = {s: tracked(s, dv) for s in S6}; ref = zs[ON[0]][1]; A = {}; RM = {}
        mf = lambda a: np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
        for s in S6:
            ix = np.rint((zs[s][1] - ref[0]) / foff).astype(int); a = np.full(NF + 2000, -99.0)
            ok = (ix + 1000 >= 0) & (ix + 1000 < len(a)); a[ix[ok] + 1000] = zs[s][0][ok]
            A[s] = mf(a)
            if extra:
                b_ = np.full(NF + 2000, -99.0); b_[ix[ok] + 1000] = zs[s][2][ok]; RM[s] = mf(b_)
        offok = np.all([A[s] < 2.0 for s in OFF], axis=0); onok = np.all([A[s] < 2.0 for s in ON], axis=0)
        mon = np.min([A[s] for s in ON], axis=0); moff = np.min([A[s] for s in OFF], axis=0)
        p = np.where((mon >= 2.5) & offok)[0]; q = np.where((moff >= 2.5) & onok)[0]
        rows.append({"on": ncl(p), "swap": ncl(q)})
        if extra:
            zon = np.array([A[s] for s in ON]); zoff = np.array([A[s] for s in OFF])
            IX["I1"].append((ncl(np.where((zon.max(0) >= 5) & offok)[0]), ncl(np.where((zoff.max(0) >= 5) & onok)[0])))
            IX["I2"].append((ncl(np.where((np.sort(zon, 0)[1] >= 3) & offok)[0]), ncl(np.where((np.sort(zoff, 0)[1] >= 3) & onok)[0])))
            ron = np.max([RM[s] for s in ON], 0); roff = np.max([RM[s] for s in OFF], 0)
            IX["I3"].append((ncl(np.where((ron >= 6) & (roff < 4))[0]), ncl(np.where((roff >= 6) & (ron < 4))[0])))
        S1.append(float(np.max(np.where(offok, mon, -99.0))))
        if coords:
            for c, f in COORD.items():
                i = int(np.rint((f - ref[0]) / foff)) + 1000; B2[c].append(float(mon[i]) if 0 <= i < len(mon) else None)
        if k == 0: cl_true = sorted({round((ref[0] + (i - 1000) * foff) / 1e6, 6) for i in p})
    on = np.array([r["on"] for r in rows[1:]]); d = np.array([r["on"] - r["swap"] for r in rows[1:]])
    T = rows[0]["on"]; sw = rows[0]["swap"]
    res = {"T": T, "swap": sw, "mu": float(on.mean()), "sd": float(on.std()), "max": int(on.max()), "d_max": int(d.max()),
           "exceeds": bool(T > on.max() and T - sw > d.max()), "S": S1[0], "S_false_max": max(S1[1:]),
           "S_rank_of_41": int(1 + sum(x >= S1[0] for x in S1[1:])), "clusters_rest_MHz": cl_true[:300], "rows": rows, "S_all": S1}
    if extra:
        for k_, L in IX.items():
            t_, sw_ = L[0]; o = np.array([x[0] for x in L[1:]]); dd = np.array([x[0] - x[1] for x in L[1:]])
            res[k_] = {"T": t_, "swap": sw_, "mu": float(o.mean()), "sd": float(o.std()), "max": int(o.max()), "d_max": int(dd.max()),
                       "exceeds": bool(t_ > o.max() and t_ - sw_ > dd.max()), "all": L}
    if coords:
        res["B2"] = {c: {"minON_true": v[0], "rank_of_41": (int(1 + sum((x is not None and v[0] is not None and x >= v[0]) for x in v[1:])) if v[0] is not None else None)} for c, v in B2.items()}
    return res

# ---------- gate and part A/B ----------
for V in ("V0", "V1", "V2"):
    key = f"comet_{V}"
    if key in R: continue
    t0 = time.time(); R[key] = run(prep(X, KEEP[V]), KEEP[V], "comet", extra=(V != "V1")); save()
    print(key, R[key]["T"], "null", round(R[key]["mu"], 2), R[key]["max"], "exceeds", R[key]["exceeds"], "S", round(R[key]["S"], 2), "rank", R[key]["S_rank_of_41"],
          {k_: (R[key][k_]["T"], R[key][k_]["max"], R[key][k_]["exceeds"]) for k_ in ("I1", "I2", "I3") if k_ in R[key]}, f"{time.time() - t0:.0f}s", flush=True)
    if V == "V0" and R[key]["T"] != 13:
        R["gate"] = {"passed": False, "T": R[key]["T"]}; save(); print("GATE FAILED", flush=True); raise SystemExit
R["gate"] = {"passed": True, "T": 13}; save()

# ---------- part K: wider kernels ----------
for w in (9, 33):
    for V in ("V0", "V2"):
        key = f"comet_{V}_w{w}"
        if key in R: continue
        t0 = time.time(); R[key] = run(prep(X, KEEP[V], w), KEEP[V], "comet", coords=False, w=w); save()
        print(key, R[key]["T"], "null", round(R[key]["mu"], 2), R[key]["max"], "exceeds", R[key]["exceeds"], f"{time.time() - t0:.0f}s", flush=True)

# ---------- part C: injection ----------
rng = np.random.default_rng(13); lo, hi = sorted([F0["0013"] / (1 - deldot(TT["0013"][0]) / C), (F0["0013"] + foff * NF) / (1 - deldot(TT["0013"][0]) / C)])
avoid = list(COORD.values()) + [1665.615127e6]; INJ = []
while len(INJ) < 20:
    f = rng.uniform(lo, hi); j = (f * (1 - deldot(TT["0013"][0]) / C) - F0["0013"]) / foff
    if abs(j - NF / 2) > 200 and all(abs(f - a) > 200 * abs(foff) for a in avoid + INJ): INJ.append(f)
R["C_freqs_MHz"] = [f / 1e6 for f in INJ]
for A_ in (0.25, 0.5, 1.0, 2.0, 4.0):
    key = f"inject_{A_}"
    if key in R: continue
    t0 = time.time()
    def inj(s, x, A_=A_):
        med = np.median(x, axis=0); r_ = x / med - 1.0; sig = 1.4826 * np.median(np.abs(r_ - np.median(r_))); del r_
        v = deldot(TT[s])
        for f in INJ:
            jj = np.rint((f * (1 - v / C) - F0[s]) / foff).astype(int)
            for k in range(x.shape[0]):
                if 0 <= jj[k] < NF: x[k, jj[k]] += A_ * med[jj[k]] * sig
        return x
    res = run(prep(X, KEEP["V0"], inj=inj), KEEP["V0"], "comet", coords=False)
    rec = []
    for f in INJ:
        hit = any(abs(c * 1e6 - f) <= 10 for c in res["clusters_rest_MHz"]); rec.append(hit)
    res["recovered"] = int(sum(rec)); res["recovered_each"] = rec
    R[key] = res; save()
    print(key, "T", res["T"], "exceeds", res["exceeds"], "S", round(res["S"], 2), "rank", res["S_rank_of_41"], "recovered", res["recovered"], f"{time.time() - t0:.0f}s", flush=True)
# per-tone smallest ON z at each A is recomputed cheaply from the aligned arrays in a second pass (analysis script), from the same inputs

# ---------- part D: frames ----------
for fr in ("flip", "geo", "bary", "topo"):
    for V in ("V0", "V2"):
        key = f"{fr}_{V}"
        if key in R: continue
        t0 = time.time(); R[key] = run(prep(X, KEEP[V]), KEEP[V], fr, coords=False); save()
        print(key, R[key]["T"], "null", round(R[key]["mu"], 2), R[key]["max"], "exceeds", R[key]["exceeds"], "S", round(R[key]["S"], 2), "rank", R[key]["S_rank_of_41"], f"{time.time() - t0:.0f}s", flush=True)
R["frames_v_range_km_s"] = {fr: [float(min(vframe(fr)[s].min() for s in S6)), float(max(vframe(fr)[s].max() for s in S6))] for fr in ("comet", "flip", "geo", "bary", "topo")}
save(); print("ALLDONE", flush=True)
