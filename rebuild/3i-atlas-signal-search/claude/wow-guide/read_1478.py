"""Reading the one cluster key_gate met outside GPS L3 (1375-1382 MHz): 1478.49-1478.60 MHz. blc24 .0002, the six scans, channels
1478.35-1478.75 MHz: per scan the excess over the scan's quiet channels, where it sits, and its time course. Post hoc.
    python3 read_1478.py"""
import json, os, sys, numpy as np, h5py, hdf5plugin, fsspec
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../wow3")); import r457_stream as r
ROLE = {"0013": "ON", "0014": "OFF", "0015": "ON", "0016": "OFF", "0017": "ON", "0018": "OFF"}; out = {}
for sc in r.SCANS:
    mjd, off = r.SCANS[sc]; name = f"blc24_guppi_61027_{mjd}_DIAG_3I_ATLAS{off}_{sc}.rawspec.0002.h5"
    d = h5py.File(fsspec.open(r.B + name, "rb", block_size=16 << 20).open(), "r")["data"]; a = d.attrs; fch1, foff, ts = float(a["fch1"]), float(a["foff"]), float(a["tsamp"])
    i0, i1 = sorted((int((1478.35 - fch1) / foff), int((1478.75 - fch1) / foff))); x = d[:, 0, i0:i1].astype(np.float64); f = fch1 + foff * np.arange(i0, i1)
    base = np.median(x); z = x / base - 1                      # fractional excess over the window's median power
    spec = z.mean(0); k = np.argsort(spec)[-8:]; lo, hi = f[k].min(), f[k].max(); sel = (f >= lo) & (f <= hi)
    y = z[:, sel].mean(1); thr = 3 * 1.4826 * np.median(np.abs(y - np.median(y))) + np.median(y)
    onoff = "".join("#" if v > thr else "." for v in y)
    out[sc] = {"role": ROLE[sc], "peak_MHz": float(f[np.argmax(spec)]), "band_MHz": [float(lo), float(hi)], "mean_excess_peak": float(spec.max()), "frac_time_on": float((y > thr).mean()),
               "max_excess_time": float(y.max()), "series": [round(float(v), 3) for v in y], "pattern": onoff}
    print(sc, ROLE[sc], "peak %.4f MHz, band %.4f-%.4f, mean excess %.3f, on %.0f%% of steps, max %.2f" % (f[np.argmax(spec)], lo, hi, spec.max(), 100 * (y > thr).mean(), y.max())); print("  ", onoff, flush=True)
json.dump(out, open(os.path.join(HERE, "read_1478.json"), "w"), indent=1)
