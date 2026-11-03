"""Read C03 as far as the GBT .0000 product allows (2.794 Hz x 6.08 s, total power, 49 steps per scan). Along C03's comet-frame path in each scan
(rest 1665.633777 MHz, the oh13 path rule): (1) the per-step series of the tracked channel (3-channel boxcar) in ON and OFF scans, its run and
autocorrelation structure against 200 random paths in the same scan; (2) the tracked spectrum +-300 channels (+-840 Hz) around C03, stacked over
the three ON scans and over the three OFF scans, to look for sidebands at fixed offsets; (3) cross-scan correlation of the ON per-step series at
lags, for a repeating pattern.
    python3 c03_read.py"""
import json, numpy as np, importlib.util, sys
sys.argv = ["x", "raw/OH", "2.5", "2.0"]
spec = importlib.util.spec_from_file_location("cf", "cometframe_raw.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
C, foff = cf.C, cf.foff_hz; F = 1665.633777e6; W = 300
out = {"series": {}, "nbhd": {}}
def path(s):
    h = cf.H[s]; x = np.load(f"raw/OH_{s}.npy", mmap_mode="r"); nt = x.shape[0]
    t = h["tstart"] + (np.arange(nt) + 0.5) * h["tsamp"] / 86400.0; v = cf.deldot(t)
    f0 = h["fch1_cc"] * 1e6; ch = np.rint((F * (1 - v / C) - f0) / foff).astype(int)
    return x, ch
rng = np.random.default_rng(3)
for s in cf.ON + cf.OFF:
    x, ch = path(s); lo, hi = ch.min() - W - 3, ch.max() + W + 4
    blk = np.asarray(x[:, lo:hi], np.float64); med = np.median(np.asarray(x[:, lo - 2000:hi + 2000], np.float64), axis=0)[2000:2000 + (hi - lo)]
    r = blk / med - 1.0; r = r + np.roll(r, 1, 1) + np.roll(r, -1, 1)
    k = ch - lo
    ser = r[np.arange(len(k)), k]                           # the C03 per-step series
    nb = np.array([r[i, k[i] - W:k[i] + W + 1] for i in range(len(k))]).sum(0)   # tracked neighbourhood
    sd = 1.4826 * np.median(np.abs(nb - np.median(nb)))
    out["nbhd"][s] = ((nb - np.median(nb)) / sd).round(3).tolist()
    # random paths: same drift, offsets far from C03
    offs = rng.choice(np.r_[-W:-20, 20:W], 200, replace=False)
    rand = np.array([r[np.arange(len(k)), k + o] for o in offs])
    zs = (ser - rand.mean(0)) / rand.std(0).clip(1e-12)
    def ac1(a): a = a - a.mean(); return float((a[1:] * a[:-1]).sum() / (a * a).sum())
    pos = ser > np.median(rand)
    runs = 1 + int(np.sum(pos[1:] != pos[:-1]))
    out["series"][s] = {"z_steps": zs.round(2).tolist(), "sum_z": round(float(zs.sum() / np.sqrt(len(zs))), 2),
                        "lag1_autocorr": round(ac1(ser), 3), "lag1_autocorr_random_mean": round(float(np.mean([ac1(a) for a in rand])), 3),
                        "lag1_random_sd": round(float(np.std([ac1(a) for a in rand])), 3), "runs_above_median": runs, "n": len(zs),
                        "top2_share": round(float(np.sort(np.clip(ser, 0, None))[-2:].sum() / max(np.clip(ser, 0, None).sum(), 1e-12)), 3)}
    print(s, {k: v for k, v in out["series"][s].items() if k != "z_steps"}, flush=True)
on = np.array([out["nbhd"][s] for s in cf.ON]).sum(0) / np.sqrt(3); offn = np.array([out["nbhd"][s] for s in cf.OFF]).sum(0) / np.sqrt(3)
off_hz = (np.arange(-W, W + 1) * abs(foff)).round(2)
top = np.argsort(on)[-8:][::-1]
print("ON stack, centre z %.2f; top offsets (Hz, z):" % on[W], [(float(off_hz[i]), round(float(on[i]), 2)) for i in top])
print("OFF stack, centre z %.2f; top offsets:" % offn[W], [(float(off_hz[i]), round(float(offn[i]), 2)) for i in np.argsort(offn)[-5:][::-1]])
sym = [(float(off_hz[W + d]), round(float(on[W + d] + on[W - d]) / np.sqrt(2), 2)) for d in range(3, W + 1)]
print("strongest symmetric sideband pairs (Hz, z):", sorted(sym, key=lambda a: -a[1])[:6])
A = np.array([out["series"][s]["z_steps"] for s in cf.ON])
cc = {}
for a, b in [(0, 1), (0, 2), (1, 2)]:
    cc[f"{cf.ON[a]}x{cf.ON[b]}"] = max(((lag, round(float(np.corrcoef(A[a][max(0, lag):len(A[a]) + min(0, lag)], A[b][max(0, -lag):len(A[b]) - max(0, lag)])[0, 1]), 3)) for lag in range(-10, 11)), key=lambda t: abs(t[1]))
print("cross-scan max |corr| over lags -10..10 (lag, r):", cc)
out.update({"on_stack": on.round(3).tolist(), "off_stack": offn.round(3).tolist(), "offset_hz": off_hz.tolist(), "cross_scan": cc})
json.dump(out, open("raw/OH_c03_read.json", "w"))
