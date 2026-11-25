"""PLAN-WOW3 amendment 1. PLAN-WOW3 R2 (the Wow's velocities applied to the OH lines, comet frame) and R6 (the hydrogen targets at rest in the Sun's frame
along the line of sight). Public rawspec .0000, streamed; ON/OFF contrast in a band around each tracked target, peak-bin z, against
200 random targets per coarse channel. Writes r2.json, r6.json.
    python3 r2_r6_lines.py"""
import json, os, sys, time, urllib.request, urllib.parse
import fsspec, h5py, hdf5plugin, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../voltages/delaymod")); import dm
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
SCANS = {"0013": ("17226", ""), "0014": ("17543", "_OFF"), "0015": ("17861", ""), "0016": ("18179", "_OFF"),
         "0017": ("18497", ""), "0018": ("18814", "_OFF")}
PAIRS = [("0013", "0014"), ("0015", "0016"), ("0017", "0018")]
C = 299792.458; H = 1420.40575177
V = {"67.54": C * 0.320 / H, "10.51": C * 0.0498 / H}
OH = {"1612": 1612.2310, "1665": 1665.4018, "1667": 1667.3590, "1720": 1720.5300}
E = dm.ephem(); VCOM = lambda t: np.interp(t, E[:, 0], E[:, 1])


def sun_frame():
    """Radial velocity (km/s, positive receding) of a source at rest in the Sun's frame in the comet's direction, from the GBT site."""
    def vec(cmd):
        p = {"format": "json", "COMMAND": cmd, "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "VECTORS", "CENTER": "'coord@399'",
             "COORD_TYPE": "GEODETIC", "SITE_COORD": "'-79.8398,38.4331,0.807'", "START_TIME": "'JD 2461027.685'", "STOP_TIME": "'JD 2461027.735'",
             "STEP_SIZE": "'1 m'", "VEC_TABLE": "'2'", "CSV_FORMAT": "YES", "OUT_UNITS": "'KM-S'"}
        txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(p), timeout=180))["result"]
        open(os.path.join(HERE, "r6_horizons_%s.txt" % cmd.strip("'").replace("/", "").replace(" ", "")), "w").write(txt)
        rows = [[x.strip() for x in l.split(",")] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
        return np.array([[float(r[0])] + [float(x) for x in r[2:8]] for r in rows])
    com, sun = vec("'C/2025 N1'"), vec("'10'")
    n = com[:, 1:4] / np.linalg.norm(com[:, 1:4], axis=1, keepdims=True)
    v_site = -sun[:, 4:7]                                  # site relative to the Sun
    vr = -(v_site * n).sum(1)                              # approaching the direction n lowers the range: negative
    return com[:, 0] - 2400000.5, vr


TS, VS = sun_frame(); VSUN = lambda t: np.interp(t, TS, VS)


def load(node, scan, f_in):
    mjd, off = SCANS[scan]
    name = f"{node}_guppi_61027_{mjd}_DIAG_3I_ATLAS{off}_{scan}.rawspec.0000.h5"
    f = fsspec.open(B + name, "rb", block_size=8 << 20).open()
    d = h5py.File(f, "r")["data"]; a = d.attrs
    fch1, foff, nfpc, ts, tst = float(a["fch1"]), float(a["foff"]), int(a["nfpc"]), float(a["tsamp"]), float(a["tstart"])
    lo = int((f_in - fch1) / foff) // nfpc * nfpc
    x = d[:, 0, lo:lo + nfpc].astype(np.float32)
    return name, x, fch1 + foff * (lo + np.arange(nfpc)), tst + (np.arange(x.shape[0]) + 0.5) * ts / 86400.0


def tracked(x, freqs, t, f_rest, vel, half, win=60e-3):
    foff = freqs[1] - freqs[0]; nb, nw = int(round(half / abs(foff))), int(round(win / abs(foff)))
    cs = [int(round((f_rest * (1 - vel(tk) / C) - freqs[0]) / foff)) for tk in t]
    nw = max(nb + 1, min(nw, min(cs) - 1, x.shape[1] - 2 - max(cs)))     # amendment 1: clip the window to the coarse channel
    acc = np.zeros(2 * nw + 1)
    for k in range(x.shape[0]):
        c = cs[k]; acc += x[k, c - nw:c + nw + 1]
    acc /= x.shape[0]
    return float(acc[nw - nb:nw + nb + 1].mean()), acc, nb


def run(node, f_in, targets, vel, avoid, seed, half_of):
    data = {}
    for sc in SCANS:
        t0 = time.time(); data[sc] = load(node, sc, f_in); print(node, "%.3f" % f_in, sc, data[sc][1].shape, "%.0fs" % (time.time() - t0), flush=True)
    freqs = data["0013"][2]; fmin, fmax = min(freqs[0], freqs[-1]) + 0.15, max(freqs[0], freqs[-1]) - 0.15
    rng = np.random.default_rng(seed); ctrl = []
    while len(ctrl) < 200:
        f = rng.uniform(fmin, fmax)
        if all(abs(f - a) > 0.05 for a in avoid): ctrl.append(f)
    res = {}
    def one(f, keep):
        half = half_of(f); P = {}; A = {}
        for sc, (_, x, fq, t) in data.items(): P[sc], A[sc], nb = tracked(x, fq, t, f, vel, half)
        c = [P[on] / P[off] - 1 for on, off in PAIRS]
        r = {"f_MHz": f, "half_kHz": half * 1e3, "on_off_contrast": c, "mean_contrast": float(np.mean(c)),
             "in_channel": bool(fmin - 0.1 < f < fmax + 0.1)}
        if keep:
            pk = {}
            for sc in SCANS:
                a = A[sc]; base = np.concatenate([a[:len(a) // 3], a[-len(a) // 3:]]); med = np.median(base); mad = np.median(np.abs(base - med)) * 1.4826
                mid = len(a) // 2; seg = (a[mid - nb:mid + nb + 1] - med) / mad
                pk[sc] = {"peak_z": float(seg.max()), "trough_z": float(seg.min())}
            r["peak_in_band"] = pk
        return r
    for k, f in targets.items(): res[k] = one(f, True)
    cm = np.array([one(f, False)["mean_contrast"] for f in ctrl])
    for k in targets:
        res[k]["rank_vs_controls"] = float((cm < res[k]["mean_contrast"]).mean())
        print(k, "%.5f" % targets[k], "contrast %.4f" % res[k]["mean_contrast"], "rank %.3f" % res[k]["rank_vs_controls"],
              {sc: round(v["peak_z"], 1) for sc, v in res[k]["peak_in_band"].items()}, flush=True)
    return {"node": node, "files": {sc: data[sc][0] for sc in data}, "coarse_channel_MHz": [float(freqs.min()), float(freqs.max())],
            "controls": {"median": float(np.median(cm)), "p05": float(np.percentile(cm, 5)), "p95": float(np.percentile(cm, 95)),
                         "min": float(cm.min()), "max": float(cm.max())}, "targets": res}


def main():
    # R2: group targets by the coarse channel that holds them
    T = {f"OH{l}_v{v}": OH[l] * (1 + V[v] / C) for l in OH for v in V}
    groups = {}
    for k, f in T.items():
        node = "blc22" if f > 1689.0 else "blc23"
        groups.setdefault((node, round((f - 1501.46484375) // 2.9296875)), {})[k] = f
    R2 = json.load(open(os.path.join(HERE, "r2.json")))["groups"]; done = {k for g in R2 for k in g["targets"]}
    for i, ((node, _), tg) in enumerate(sorted(groups.items())):
        if set(tg) <= done: continue
        f0 = list(tg.values())[0]
        R2.append(run(node, f0, tg, VCOM, list(T.values()) + list(OH.values()), 16122310 + i, lambda f: 5e-3 * f / H))
        json.dump({"velocities_kms": V, "targets_MHz": T, "groups": R2}, open(os.path.join(HERE, "r2.json"), "w"), indent=1)
    # R6: hydrogen targets at rest in the Sun's frame along the line of sight
    S = {"S1_H_sun": H, "S2_H+320k_sun": H + 0.320, "S3_H+49.8k_sun": H + 0.0498}
    r6 = run("blc24", 1420.6, S, VSUN, list(S.values()) + [1420.726], 14204060, lambda f: 5e-3)
    r6["sun_frame_radial_velocity_kms"] = {"start": float(VS[0]), "end": float(VS[-1])}
    r6["comet_frame_radial_velocity_kms"] = {"start": float(E[0, 1]), "end": float(E[-1, 1])}
    json.dump(r6, open(os.path.join(HERE, "r6.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
