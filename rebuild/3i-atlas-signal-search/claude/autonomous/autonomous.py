"""Signal classes an autonomous sender familiar with Earth's receivers would plausibly use, tested on the cached GBT OH coarse channel
(raw/OH_0013..0018, 1665.53-1668.46 MHz, 2.79 Hz x 6.08 s; ON 0013/0015/0017, OFF 0014/0016/0018).

Frames. A transmitter on 3I/ATLAS that pre-compensates its own Doppler so that a receiver at point X sees a constant frequency arrives at
the GBT on the path f(t) = F (1 - (v_topo(t) - v_X(t))/c), with v_topo and v_X the comet's range-rate from the GBT site and from X (JPL
Horizons). X = none gives the uncompensated comet frame (the earlier search); X = GBT gives zero drift at the telescope (the class
turboSETI-style pipelines drop as terrestrial); X = geocentre removes Earth's rotation; X = solar-system barycentre is the frame published
results are reported in.

Tests per frame:
  persistent  z >= Z_ON in all three ON scans, z < Z_OFF in all three OFF scans, same frame frequency (+-1 channel), clustered at 10 Hz;
              null 1: 24 false range-accelerations around that frame's path; null 2: beam swap (OFF scans as target, ON as reference).
  singles     z >= Z_SINGLE in exactly one scan of one beam and z < Z_OFF in all three scans of the other beam; count ON-singles against
              OFF-singles (an intermittent source on the comet gives ON > OFF; local interference is symmetric).
    python3 autonomous.py"""
import json, sys, importlib.util, urllib.parse, urllib.request
import numpy as np
sys.argv = ["x", "raw/OH", "2.5", "2.0"]
spec = importlib.util.spec_from_file_location("cf", "cometframe_raw.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
C = cf.C; ON, OFF = cf.ON, cf.OFF; H = cf.H; foff_hz = cf.foff_hz; T0 = cf.T0
Z_ON, Z_OFF, Z_SINGLE = 2.5, 2.0, 6.0

def horizons(center):
    t = [H[s]["tstart"] for s in ON + OFF]
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": center,
         "START_TIME": f"'JD {min(t) - 0.005 + 2400000.5:.6f}'", "STOP_TIME": f"'JD {max(t) + 0.02 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'",
         "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])

GEO, BARY = horizons("'500@399'"), horizons("'500@0'")
vt = lambda t: cf.deldot(t)
FRAMES = {"comet (uncompensated)": lambda t: vt(t),
          "GBT topocentric (zero drift)": lambda t: 0.0 * t,
          "geocentric": lambda t: vt(t) - np.interp(t, GEO[:, 0], GEO[:, 1]),
          "barycentric": lambda t: vt(t) - np.interp(t, BARY[:, 0], BARY[:, 1])}

def tracked(s, vf, dv=0.0):
    x = np.load(f"raw/OH_{s}.npy", mmap_mode="r"); h = H[s]; nt, nc = x.shape
    t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0
    v = vf(t) + dv * (t - T0) * 86400.0
    f0 = h["fch1_cc"] * 1e6
    shift = np.rint(f0 * (v[0] - v) / C / foff_hz).astype(int)
    med = np.median(x, axis=0); acc = np.zeros(nc)
    for k in range(nt):
        row = np.asarray(x[k], np.float64) / med - 1.0
        row = row + np.roll(row, 1) + np.roll(row, -1)
        acc += np.roll(row, -shift[k])
    m = np.median(acc); sd = 1.4826 * np.median(np.abs(acc - m)); z = (acc - m) / sd
    z[nc // 2 - 4: nc // 2 + 5] = 0.0
    return z, (f0 + foff_hz * np.arange(nc)) / (1.0 - v[0] / C)

def align(zs):
    ref = zs["0013"][1]; out = {}
    for s in ON + OFF:
        idx = np.rint((zs[s][1] - ref[0]) / foff_hz).astype(int); z = zs[s][0]
        a = np.full(len(z) + 2000, -99.0); ok = (idx + 1000 >= 0) & (idx + 1000 < len(a)); a[idx[ok] + 1000] = z[ok]
        out[s] = np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
    return out, ref

def clusters(idx, tol=int(10 / abs(foff_hz)) + 1):
    idx = np.sort(idx); return 0 if not len(idx) else 1 + int(np.sum(np.diff(idx) > tol))

def persistent(A, tgt, refb):
    ok = np.ones_like(A["0013"], bool)
    for s in tgt: ok &= A[s] >= Z_ON
    for s in refb: ok &= A[s] < Z_OFF
    return np.where(ok)[0]

def singles(A, tgt, refb):
    hi = np.sum([A[s] >= Z_SINGLE for s in tgt], axis=0) == 1
    quiet = np.all([A[s] < Z_OFF for s in refb], axis=0) & np.all([A[s] > -50 for s in tgt + refb], axis=0)
    return np.where(hi & quiet)[0]

rng = np.random.default_rng(7)
offs = rng.uniform(0.03, 1.0, 24) * rng.choice([-1, 1], 24) * C / 1.42e9
res = {}
for name, vf in FRAMES.items():
    A, ref = align({s: tracked(s, vf) for s in ON + OFF})
    p = persistent(A, ON, OFF); pswap = persistent(A, OFF, ON)
    son, soff = singles(A, ON, OFF), singles(A, OFF, ON)
    null = []
    for dv in offs:
        An, _ = align({s: tracked(s, vf, dv) for s in ON + OFF}); null.append(clusters(persistent(An, ON, OFF)))
    fr = lambda i: round((ref[0] + (i - 1000) * foff_hz) / 1e6, 6)
    rows = lambda I: [{"f_frame_MHz": fr(i), **{f"z_{s}": round(float(A[s][i]), 2) for s in ON + OFF}} for i in I]
    res[name] = {"persistent_clusters": clusters(p), "beam_swap_clusters": clusters(pswap),
                 "null_mean": float(np.mean(null)), "null_sd": float(np.std(null)), "null_max": int(max(null)),
                 "null_frac_ge": float(np.mean([n >= clusters(p) for n in null])),
                 "on_singles": clusters(son), "off_singles": clusters(soff),
                 "persistent": rows(p[:40]), "on_single_rows": rows(son[:40])}
    print(name, {k: v for k, v in res[name].items() if not isinstance(v, list)}, flush=True)
json.dump({"z_on": Z_ON, "z_off": Z_OFF, "z_single": Z_SINGLE, "frames": res}, open("raw/OH_autonomous.json", "w"), indent=1)
