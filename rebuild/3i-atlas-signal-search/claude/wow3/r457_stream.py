"""PLAN-WOW3 R4 (the Wow! profile along frequency), R5 (a 12 s, 10-on/2-off cadence in time) and R7 (Big Ear rebuilt on blc24),
from one pass over each public rawspec .0002 product (streamed, nothing kept). Writes r4_<node>.json, r5_<node>.json, r7.json.
    python3 r457_stream.py blc21 [blc22 ...]"""
import json, os, sys, time
import fsspec, h5py, hdf5plugin, numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv
from scipy.ndimage import median_filter
HERE = os.path.dirname(os.path.abspath(__file__))
B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
SCANS = {"0013": ("17226", ""), "0014": ("17543", "_OFF"), "0015": ("17861", ""), "0016": ("18179", "_OFF"),
         "0017": ("18497", ""), "0018": ("18814", "_OFF")}
PAIRS = [("0013", "0014"), ("0015", "0016"), ("0017", "0018")]
H = 1420.40575177
WOW = np.array([6, 14, 26, 30, 19, 5], float)
rng = np.random.default_rng(19770816)
def smooth():
    c, w, sk = rng.uniform(1.5, 3.5), rng.uniform(0.6, 2.5), rng.uniform(0.6, 1.6)
    i = np.arange(6.0); s = np.where(i > c, w * sk, w)
    return np.exp(-0.5 * ((i - c) / s) ** 2)
CTRL_SMOOTH = [smooth() for _ in range(200)]
CTRL_RAND = [rng.integers(1, 36, 6).astype(float) for _ in range(200)]
def norm(T):
    T = np.array(T, float); T = T - T.mean(1, keepdims=True); return T / np.linalg.norm(T, axis=1, keepdims=True)
T4 = {"asc": norm([WOW] + CTRL_SMOOTH + CTRL_RAND), "desc": norm([WOW[::-1]] + CTRL_SMOOTH + CTRL_RAND)}
DET_ON, DET_OFF = 6.0, 3.0
rng5 = np.random.default_rng(1977081612)
PERIODS = [12.0]
while len(PERIODS) < 201:
    p = rng5.uniform(7, 20)
    if not 11 <= p <= 13: PERIODS.append(p)
CHARS = " 123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rsig(a, axis=None):
    med = np.median(a, axis=axis, keepdims=True); mad = np.median(np.abs(a - med), axis=axis, keepdims=True) * 1.4826
    return (a - med) / np.where(mad > 0, mad, np.inf)


def read(node, scan):
    mjd, off = SCANS[scan]
    name = f"{node}_guppi_61027_{mjd}_DIAG_3I_ATLAS{off}_{scan}.rawspec.0002.h5"
    f = fsspec.open(B + name, "rb", block_size=16 << 20).open()
    d = h5py.File(f, "r")["data"]; a = d.attrs
    return name, d[:, 0, :].astype(np.float64), float(a["fch1"]), float(a["foff"]), float(a["tsamp"])


def r4_scores(x, w):
    """Time-mean spectrum at channel width w (1 or 3 fine channels), flattened by a running median, robust sigma per 1024/w block;
    sliding correlation along frequency with every template. Returns {order: (401, n-5)}."""
    s = x.mean(0); n = len(s) // w * w; s = s[:n].reshape(-1, w).sum(1)
    r = s / median_filter(s, 101, mode="nearest") - 1
    blk = 1024 // w if w == 1 else 341
    z = np.concatenate([rsig(r[i:i + blk]) for i in range(0, len(r), blk)])
    W = swv(z, 6)
    return {o: (W @ T.T).T.astype(np.float32) for o, T in T4.items()}


def r5_scores(x, ts):
    n = x.shape[1] // 3 * 3; y = x[:, :n].reshape(x.shape[0], n // 3, 3).sum(2)
    z = rsig(y, axis=0).astype(np.float32); z = z - z.mean(0, keepdims=True)
    t = np.arange(x.shape[0]) * ts; out = np.empty((len(PERIODS), z.shape[1]), np.float32)
    for i, P in enumerate(PERIODS):
        T = np.array([(((t - ph * P / 12) % P) < P * 5 / 6).astype(np.float32) for ph in range(12)])
        T -= T.mean(1, keepdims=True); T /= np.linalg.norm(T, axis=1, keepdims=True)
        out[i] = (T @ z).max(0)
    return out, y


def bigear(y, ts, freqs3):
    t = np.arange(y.shape[0]) * ts
    rows = [y[(t >= 12 * k) & (t < 12 * k + 10)].mean(0) for k in range(int((t[-1] - 10) // 12) + 1)]
    snr = rsig(np.array(rows), axis=0)                                # (25, nch)
    c = int(np.argmin(np.abs(freqs3 - H)))
    def stat(c0):
        b = np.floor(snr[:, c0 - 25:c0 + 25]).astype(int); b = np.clip(b, 0, 35)
        hi = b >= 5; run = 0
        for j in range(hi.shape[1]):
            k = 0
            for v in hi[:, j]:
                k = k + 1 if v else 0; run = max(run, k)
        return int(hi.sum()), int(run), b
    n5, run, b = stat(c)
    rc = np.random.default_rng(14204061); ctrl = []
    while len(ctrl) < 200:
        c0 = int(rc.integers(60, snr.shape[1] - 60))
        if abs(c0 - c) > 60: ctrl.append(stat(c0)[:2])
    ctrl = np.array(ctrl)
    return {"centre_MHz": float(freqs3[c]), "chars_ge5": n5, "longest_run": run,
            "rank_chars": float((ctrl[:, 0] < n5).mean()), "rank_run": float((ctrl[:, 1] < run).mean()),
            "control_chars_median": float(np.median(ctrl[:, 0])), "control_run_max": int(ctrl[:, 1].max()),
            "printout": ["".join(CHARS[v] for v in row) for row in b]}


def detect(S, freqs):
    """S: {scan: (templates, channels)} -> counts per template and the detections of template 0."""
    counts = np.zeros(next(iter(S.values())).shape[0], int); dets = []
    lit = {sc: S[sc][0] >= DET_ON for sc in S}
    for on, off in PAIRS:
        hit = (S[on] >= DET_ON) & (S[off] < DET_OFF); counts += hit.sum(1)
        for c in np.where(hit[0])[0]:
            dets.append({"pair": f"{on}/{off}", "freq_MHz": round(float(freqs[c]), 6), "score_on": round(float(S[on][0, c]), 2),
                         "score_off": round(float(S[off][0, c]), 2), "also_lit_in": [sc for sc in S if sc != on and lit[sc][c]]})
    return counts, dets


def main():
    for node in sys.argv[1:]:
        t0 = time.time(); S4 = {(w, o): {} for w in (1, 3) for o in T4}; S5 = {}; names = {}; R7 = {}
        for sc in SCANS:
            names[sc], x, fch1, foff, ts = read(node, sc)
            for w in (1, 3):
                r = r4_scores(x, w)
                for o in T4: S4[(w, o)][sc] = r[o]
            S5[sc], y = r5_scores(x, ts)
            freqs3 = fch1 + foff * (np.arange(y.shape[1]) * 3 + 1)
            if node == "blc24": R7[sc] = bigear(y, ts, freqs3)
            print(node, sc, "%.0fs" % (time.time() - t0), flush=True)
        f1 = fch1 + foff * np.arange(x.shape[1])
        out4 = {"node": node, "files": names}
        for (w, o), S in S4.items():
            fr = f1 if w == 1 else freqs3
            counts, dets = detect(S, fr[:next(iter(S.values())).shape[1]] + (2.5 * foff * w))
            out4[f"w{w}_{o}"] = {"channel_kHz": abs(foff) * w * 1e3, "detections_n": int(counts[0]), "smooth_counts": counts[1:201].tolist(),
                                 "rand_counts": counts[201:].tolist(), "rank_vs_smooth": float((counts[1:201] < counts[0]).mean()),
                                 "rank_vs_rand": float((counts[201:] < counts[0]).mean()), "detections": dets[:2000]}
            print(node, "R4", w, o, counts[0], "smooth median", np.median(counts[1:201]), "rank", out4[f"w{w}_{o}"]["rank_vs_smooth"], flush=True)
        json.dump(out4, open(os.path.join(HERE, f"r4_{node}.json"), "w"), indent=1)
        counts, dets = detect(S5, freqs3)
        json.dump({"node": node, "files": names, "periods_s": PERIODS, "detections_12s": int(counts[0]), "control_counts": counts[1:].tolist(),
                   "rank_vs_periods": float((counts[1:] < counts[0]).mean()), "control_median": float(np.median(counts[1:])),
                   "detections": dets[:2000]}, open(os.path.join(HERE, f"r5_{node}.json"), "w"), indent=1)
        print(node, "R5", counts[0], "control median", np.median(counts[1:]), "rank", float((counts[1:] < counts[0]).mean()), flush=True)
        if R7:
            json.dump({"node": node, "files": names, "scans": R7}, open(os.path.join(HERE, "r7.json"), "w"), indent=1)
            for sc, r in R7.items(): print("R7", sc, r["chars_ge5"], r["longest_run"], r["rank_chars"], r["rank_run"], flush=True)


if __name__ == "__main__":
    main()
