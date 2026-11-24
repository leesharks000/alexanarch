"""PLAN-SYMBOLON K1 (the Wow! profile time-reversed, 5-19-30-26-14-6) and K2 (the Wow! profile sign-inverted, a dip of its shape),
matched in time across blc21-26 as wow_s1b.py, against the same 200 smooth single-peaked controls and 200 random six-value sequences
(same generator, same seed), negated for K2. Streams each rawspec .0002 product (nothing kept); writes k12_<node>.json.
    python3 symb_k12.py blc21 [blc22 ...]"""
import json, sys, time
import fsspec, h5py, hdf5plugin, numpy as np

B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
SCANS = {"0013": ("17226", ""), "0014": ("17543", "_OFF"), "0015": ("17861", ""), "0016": ("18179", "_OFF"),
         "0017": ("18497", ""), "0018": ("18814", "_OFF")}
PAIRS = [("0013", "0014"), ("0015", "0016"), ("0017", "0018")]
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
SETS = {"K1": norm([WOW[::-1]] + CTRL_SMOOTH + CTRL_RAND),
        "K2": -norm([WOW] + CTRL_SMOOTH + CTRL_RAND)}
DET_ON, DET_OFF = 6.0, 3.0


def series(node, scan):
    mjd, off = SCANS[scan]
    name = f"{node}_guppi_61027_{mjd}_DIAG_3I_ATLAS{off}_{scan}.rawspec.0002.h5"
    f = fsspec.open(B + name, "rb", block_size=16 << 20).open()
    d = h5py.File(f, "r")["data"]; a = d.attrs
    x = d[:, 0, :].astype(np.float64)
    fch1, foff, ts = float(a["fch1"]), float(a["foff"]), float(a["tsamp"])
    nch = x.shape[1] // 3 * 3
    x = x[:, :nch].reshape(x.shape[0], nch // 3, 3).sum(2)
    freqs = fch1 + foff * (np.arange(nch // 3) * 3 + 1)
    t = np.arange(x.shape[0]) * ts
    rows = []
    for k in range(int((t[-1] - 10) // 12) + 1):
        m = (t >= 12 * k) & (t < 12 * k + 10)
        rows.append(x[m].sum(0) / m.sum())
    s = np.array(rows)
    med = np.median(s, 0); mad = np.median(np.abs(s - med), 0) * 1.4826
    return name, freqs, (s - med) / np.where(mad > 0, mad, np.inf)


def scores(snr, T):
    n = snr.shape[0] - 5
    W = np.stack([snr[k:k + 6] for k in range(n)])
    out = np.empty((len(T), snr.shape[1]), np.float32)
    for i in range(0, len(T), 40):
        out[i:i + 40] = np.einsum("tj,kjc->tkc", T[i:i + 40], W).max(1)
    return out


def main():
    for node in sys.argv[1:]:
        t0 = time.time(); S = {k: {} for k in SETS}; names = {}
        for sc in SCANS:
            names[sc], freqs, snr = series(node, sc)
            for k, T in SETS.items():
                S[k][sc] = scores(snr, T)
            print(node, sc, "%.0fs" % (time.time() - t0), flush=True)
        out = {"node": node, "files": names, "f_range_MHz": [float(freqs.min()), float(freqs.max())], "n_channels": int(len(freqs))}
        for k in SETS:
            counts = np.zeros(401, int); dets = []
            lit = {sc: S[k][sc][0] >= DET_ON for sc in SCANS}
            for on, off in PAIRS:
                hit = (S[k][on] >= DET_ON) & (S[k][off] < DET_OFF)
                counts += hit.sum(1)
                for c in np.where(hit[0])[0]:
                    dets.append({"pair": f"{on}/{off}", "freq_MHz": round(float(freqs[c]), 6), "score_on": round(float(S[k][on][0, c]), 2),
                                 "score_off": round(float(S[k][off][0, c]), 2), "also_lit_in": [sc for sc in SCANS if sc != on and lit[sc][c]]})
            out[k] = {"detections_n": int(counts[0]), "smooth_counts": counts[1:201].tolist(), "rand_counts": counts[201:].tolist(),
                      "rank_vs_smooth": float((counts[1:201] < counts[0]).mean()), "rank_vs_rand": float((counts[201:] < counts[0]).mean()),
                      "detections": dets}
            print(node, k, counts[0], "smooth median", np.median(counts[1:201]), "rank", out[k]["rank_vs_smooth"],
                  "rand median", np.median(counts[201:]), flush=True)
        json.dump(out, open(f"k12_{node}.json", "w"), indent=1)


if __name__ == "__main__":
    main()
