"""PLAN-WOW stage 1 (W2 + W3 + W4): the Wow! profile 6-14-26-30-19-5 matched in time across blc21-26, against 400 control templates.
Streams each rawspec .0002 product (nothing kept); writes s1_<node>.json per node.
    python3 wow_s1.py blc21 [blc22 ...]"""
import json, sys, time
import fsspec, h5py, hdf5plugin, numpy as np

B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
SCANS = {"0013": ("17226", ""), "0014": ("17543", "_OFF"), "0015": ("17861", ""), "0016": ("18179", "_OFF"),
         "0017": ("18497", ""), "0018": ("18814", "_OFF")}
PAIRS = [("0013", "0014"), ("0015", "0016"), ("0017", "0018")]
WOW = np.array([6, 14, 26, 30, 19, 5], float)
rng = np.random.default_rng(19770816)
CTRL_PERM = [rng.permutation(WOW) for _ in range(200)]
CTRL_RAND = [rng.integers(1, 36, 6).astype(float) for _ in range(200)]
TEMPL = np.array([WOW] + CTRL_PERM + CTRL_RAND)
TEMPL = TEMPL - TEMPL.mean(1, keepdims=True)          # zero-mean: a baseline offset does not score
TEMPL /= np.linalg.norm(TEMPL, axis=1, keepdims=True)  # unit norm: under noise the correlation is ~N(0,1)
DET_ON, DET_OFF = 6.0, 3.0


def series(node, scan):
    mjd, off = SCANS[scan]
    name = f"{node}_guppi_61027_{mjd}_DIAG_3I_ATLAS{off}_{scan}.rawspec.0002.h5"
    f = fsspec.open(B + name, "rb", block_size=16 << 20).open()
    d = h5py.File(f, "r")["data"]; a = d.attrs
    x = d[:, 0, :].astype(np.float64)                  # (279, 65536)
    fch1, foff, ts = float(a["fch1"]), float(a["foff"]), float(a["tsamp"])
    nch = x.shape[1] // 3 * 3
    x = x[:, :nch].reshape(x.shape[0], nch // 3, 3).sum(2)          # W2: 3 fine channels -> 8.58 kHz
    freqs = fch1 + foff * (np.arange(nch // 3) * 3 + 1)
    t = np.arange(x.shape[0]) * ts
    rows = []
    for k in range(int((t[-1] - 10) // 12) + 1):                    # W3: 10 s sums every 12 s
        m = (t >= 12 * k) & (t < 12 * k + 10)
        rows.append(x[m].sum(0) / m.sum())
    s = np.array(rows)                                               # (24, nch/3)
    med = np.median(s, 0); mad = np.median(np.abs(s - med), 0) * 1.4826
    snr = (s - med) / np.where(mad > 0, mad, np.inf)
    return name, freqs, snr


def scores(snr):
    n = snr.shape[0] - 5
    W = np.stack([snr[k:k + 6] for k in range(n)])                   # (n, 6, ch)
    out = np.empty((len(TEMPL), snr.shape[1]), np.float32)
    for i in range(0, len(TEMPL), 40):
        c = np.einsum("tj,kjc->tkc", TEMPL[i:i + 40], W)
        out[i:i + 40] = c.max(1)
    return out                                                       # (401, ch)


def main():
    for node in sys.argv[1:]:
        t0 = time.time(); S = {}; names = {}
        for sc in SCANS:
            names[sc], freqs, snr = series(node, sc)
            S[sc] = scores(snr)
            print(node, sc, snr.shape, "%.0fs" % (time.time() - t0), flush=True)
        counts = np.zeros(len(TEMPL), int); dets = []
        lit = {sc: S[sc][0] >= DET_ON for sc in S}                    # where the Wow template lights, per scan
        for on, off in PAIRS:
            hit = (S[on] >= DET_ON) & (S[off] < DET_OFF)
            counts += hit.sum(1)
            for c in np.where(hit[0])[0]:
                dets.append({"pair": f"{on}/{off}", "freq_MHz": round(float(freqs[c]), 6), "score_on": round(float(S[on][0, c]), 2),
                             "score_off": round(float(S[off][0, c]), 2),
                             "also_lit_in": [sc for sc in S if sc != on and lit[sc][c]]})
        rank = float((counts[1:] < counts[0]).mean())
        json.dump({"node": node, "files": names, "f_range_MHz": [float(freqs.min()), float(freqs.max())], "n_channels": int(len(freqs)),
                   "wow_detections": int(counts[0]), "perm_counts": counts[1:201].tolist(), "rand_counts": counts[201:].tolist(),
                   "wow_rank_below": rank, "detections": dets}, open(f"s1_{node}.json", "w"), indent=1)
        print(node, "wow", counts[0], "perm median", np.median(counts[1:201]), "rand median", np.median(counts[201:]), "rank", rank, flush=True)


if __name__ == "__main__":
    main()
