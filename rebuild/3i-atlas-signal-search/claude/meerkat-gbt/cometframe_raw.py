"""Comet-frame search in raw GBT spectra (one coarse channel, 2.79 Hz x 6.08 s), below the published threshold.

Each scan is normalised channel by channel (divided by its own time-median, minus one), then summed along the
exact path a tone fixed on 3I/ATLAS would take through the scan (JPL Horizons range-rate for the Green Bank site),
giving a comet-tracked spectrum. The three ON scans are aligned on the comet's rest frame and a candidate must
stand above z in all three; the three OFF scans, tracked the same way, must stay below z_off at that rest frequency.
The null repeats the whole procedure with the frame displaced by a false range-rate offset, many times.
    python3 cometframe_raw.py <stem> [z_on] [z_off]   (stem e.g. raw/HI ; scans 0013..0018)"""
import sys, json, urllib.parse, urllib.request
import numpy as np

stem = sys.argv[1]; Z_ON = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0; Z_OFF = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
C = 299792.458
ON, OFF = ["0013", "0015", "0017"], ["0014", "0016", "0018"]
H = {s: json.load(open(f"{stem}_{s}.json")) for s in ON + OFF}
foff_hz = H["0013"]["foff"] * 1e6
t_all = [H[s]["tstart"] for s in ON + OFF]

def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER",
         "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC", "SITE_COORD": "'-79.8398,38.4331,0.807'",
         "START_TIME": f"'JD {t0 + 2400000.5:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'",
         "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])

E = horizons(min(t_all) - 0.005, max(t_all) + 0.02)
T0 = min(t_all)
def deldot(t): return np.interp(t, E[:, 0], E[:, 1])

def tracked(s, dv=0.0):
    """Sum scan s along the comet path; dv shifts the assumed range-rate (null). Returns (z-spectrum, f_rest of channel 0 Hz offset fn)."""
    x = np.load(f"{stem}_{s}.npy", mmap_mode="r")
    h = H[s]; nt, nc = x.shape
    t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0
    v = deldot(t) + dv * (t - T0) * 86400.0  # dv: false range-acceleration offset, km/s^2 (null)
    f0 = h["fch1_cc"] * 1e6  # Hz, channel 0
    # a tone at rest frequency F appears at F*(1 - v/c); relative to the first step it moves by F*(v0 - v)/c
    shift = np.rint(f0 * (v[0] - v) / C / foff_hz).astype(int)  # channels, per time step
    med = np.median(x, axis=0)
    acc = np.zeros(nc, np.float64)
    for k in range(nt):
        row = np.asarray(x[k], np.float64) / med - 1.0
        row = row + np.roll(row, 1) + np.roll(row, -1)  # 3-channel boxcar: tolerate rounding of the path
        acc += np.roll(row, -shift[k])
    m = np.median(acc); s_ = 1.4826 * np.median(np.abs(acc - m))
    z = (acc - m) / s_
    z[nc // 2 - 4: nc // 2 + 5] = 0.0  # DC bin of the coarse channel
    # rest frequency of channel j at the first step
    frest = (f0 + foff_hz * np.arange(nc)) / (1.0 - v[0] / C)
    return z, frest

def coincidences(dv=0.0, keep=False):
    zs = {s: tracked(s, dv) for s in ON + OFF}
    ref = zs["0013"][1]
    grid = lambda s: np.rint((zs[s][1] - ref[0]) / foff_hz).astype(int)
    aligned = {}
    for s in ON + OFF:
        idx = grid(s); z = zs[s][0]
        a = np.full(len(z) + 2000, -99.0); off = 1000
        ok = (idx + off >= 0) & (idx + off < len(a)); a[idx[ok] + off] = np.maximum(a[idx[ok] + off], z[ok])
        aligned[s] = a
    # allow +-1 channel tolerance by max-filtering ON and OFF
    mf = lambda a: np.maximum(np.maximum(a, np.roll(a, 1)), np.roll(a, -1))
    on_ok = np.ones_like(aligned["0013"], bool)
    for s in ON: on_ok &= mf(aligned[s]) >= Z_ON
    off_ok = np.ones_like(on_ok)
    for s in OFF: off_ok &= mf(aligned[s]) < Z_OFF
    hit = np.where(on_ok & off_ok)[0]
    if keep:
        rows = []
        for i in hit:
            rows.append({"f_rest_MHz": (ref[0] + (i - 1000) * foff_hz) / 1e6, **{f"z_{s}": float(mf(aligned[s])[i]) for s in ON + OFF}})
        return rows
    return len(hit)

if __name__ == "__main__":
    real = coincidences(0.0, keep=True)
    rng = np.random.default_rng(7)
    # false drifts of 0.03-1.0 Hz/s at 1.42 GHz, as range-accelerations (km/s^2)
    offs = rng.uniform(0.03, 1.0, 24) * rng.choice([-1, 1], 24) * C / 1.42e9
    null = [coincidences(dv) for dv in offs]
    out = {"z_on": Z_ON, "z_off": Z_OFF, "deldot_km_s": [float(E[:, 1].min()), float(E[:, 1].max())],
           "candidates_true_frame": len(real), "null_mean": float(np.mean(null)), "null_sd": float(np.std(null)),
           "null_max": int(max(null)), "null_frac_ge_true": float(np.mean([n >= len(real) for n in null])), "candidates": real[:50]}
    print(json.dumps(out, indent=1))
    json.dump(out, open(f"{stem}_cometframe.json", "w"), indent=1)
