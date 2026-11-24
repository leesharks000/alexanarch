"""PLAN-WOW stage 2 (W1): the hydrogen line, and the Wow's offsets from it, in 3I/ATLAS's frame; blc24 .0000, the coarse channel
holding 1420.4-1420.8 MHz, scans 0013-0018, streamed. Targets T1-T4 against 200 random control targets. Writes s2.json and the
±60 kHz scan-integrated windows of the targets (s2_windows.npz).
    python3 wow_s2.py"""
import json, os, sys, time
import fsspec, h5py, hdf5plugin, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../voltages/delaymod")); import dm
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
SCANS = {"0013": ("17226", ""), "0014": ("17543", "_OFF"), "0015": ("17861", ""), "0016": ("18179", "_OFF"),
         "0017": ("18497", ""), "0018": ("18814", "_OFF")}
PAIRS = [("0013", "0014"), ("0015", "0016"), ("0017", "0018")]
C = 299792.458
H = 1420.40575177
E = dm.ephem(); VEL = lambda t: np.interp(t, E[:, 0], E[:, 1])      # km/s, range rate to GBT
HALF = 5e-3                                                         # MHz: ±5 kHz, the Wow's stated uncertainty
WIN = 60e-3


def load(scan):
    mjd, off = SCANS[scan]
    name = f"blc24_guppi_61027_{mjd}_DIAG_3I_ATLAS{off}_{scan}.rawspec.0000.h5"
    f = fsspec.open(B + name, "rb", block_size=8 << 20).open()
    d = h5py.File(f, "r")["data"]; a = d.attrs
    fch1, foff, nfpc, ts, tst = float(a["fch1"]), float(a["foff"]), int(a["nfpc"]), float(a["tsamp"]), float(a["tstart"])
    i = int((1420.6 - fch1) / foff); lo = i // nfpc * nfpc
    x = d[:, 0, lo:lo + nfpc].astype(np.float32)
    freqs = fch1 + foff * (lo + np.arange(nfpc))
    t = tst + (np.arange(x.shape[0]) + 0.5) * ts / 86400.0
    return name, x, freqs, t


def tracked_band(x, freqs, t, f_rest, frame):
    """Mean power over the scan in ±HALF around the target, following the comet frame if asked; and the scan-integrated
    tracked spectrum in ±WIN for the peak-bin reading."""
    foff = freqs[1] - freqs[0]
    nb, nw = int(round(HALF / abs(foff))), int(round(WIN / abs(foff)))
    acc = np.zeros(2 * nw + 1)
    for k in range(x.shape[0]):
        f_topo = f_rest * (1 - VEL(t[k]) / C) if frame == "comet" else f_rest
        c = int(round((f_topo - freqs[0]) / foff))
        acc += x[k, c - nw:c + nw + 1]
    acc /= x.shape[0]
    band = acc[nw - nb:nw + nb + 1]
    return float(band.mean()), acc


def main():
    rng = np.random.default_rng(14204058)
    T = {"T1_1420.726_topo": (1420.726, "topo"), "T2_H_comet": (H, "comet"), "T3_H+320k_comet": (H + 0.320, "comet"),
         "T4_H+49.8k_comet": (H + 0.0498, "comet")}
    data = {}
    for sc in SCANS:
        t0 = time.time(); data[sc] = load(sc); print(sc, data[sc][1].shape, "%.0fs" % (time.time() - t0), flush=True)
    freqs = data["0013"][2]; fmin, fmax = min(freqs[0], freqs[-1]) + 0.1, max(freqs[0], freqs[-1]) - 0.1
    ctrl = []
    while len(ctrl) < 200:
        f = rng.uniform(fmin, fmax)
        if abs(f - H) > 0.05 and all(abs(f - v[0]) > 0.05 for v in T.values()):
            ctrl.append(f)
    targets = dict(T); targets.update({f"ctrl_{i:03d}": (f, "comet") for i, f in enumerate(ctrl)})
    res = {}; wins = {}
    for k, (f, fr) in targets.items():
        P = {}; A = {}
        for sc, (_, x, fq, t) in data.items():
            P[sc], A[sc] = tracked_band(x, fq, t, f, fr)
        contrast = [P[on] / P[off] - 1 for on, off in PAIRS]
        r = {"f_MHz": f, "frame": fr, "band_power": P, "on_off_contrast": contrast, "mean_contrast": float(np.mean(contrast))}
        if not k.startswith("ctrl"):
            pk = {}
            for sc in SCANS:
                a = A[sc]; base = np.concatenate([a[:len(a) // 3], a[-len(a) // 3:]])
                med = np.median(base); mad = np.median(np.abs(base - med)) * 1.4826
                mid = len(a) // 2; nb = int(round(HALF / abs(fq[1] - fq[0])))
                seg = (a[mid - nb:mid + nb + 1] - med) / mad
                pk[sc] = {"peak_z": float(seg.max()), "offset_Hz": float((seg.argmax() - nb) * abs(fq[1] - fq[0]) * 1e6)}
            r["peak_in_band"] = pk
            wins.update({f"{k}_{sc}": A[sc].astype(np.float32) for sc in SCANS})
        res[k] = r
    cm = np.array([res[k]["mean_contrast"] for k in res if k.startswith("ctrl")])
    for k in T:
        res[k]["rank_vs_controls"] = float((cm < res[k]["mean_contrast"]).mean())
        res[k]["control_contrast_sd"] = float(cm.std())
    json.dump({"files": {sc: data[sc][0] for sc in data}, "coarse_channel_MHz": [float(freqs.min()), float(freqs.max())],
               "targets": res}, open(os.path.join(HERE, "s2.json"), "w"), indent=1)
    np.savez_compressed(os.path.join(HERE, "s2_windows.npz"), **wins)
    for k in T:
        print(k, "mean ON/OFF-1 %.4f" % res[k]["mean_contrast"], "rank %.3f" % res[k]["rank_vs_controls"],
              {sc: round(v["peak_z"], 1) for sc, v in res[k]["peak_in_band"].items()}, flush=True)


if __name__ == "__main__":
    main()
