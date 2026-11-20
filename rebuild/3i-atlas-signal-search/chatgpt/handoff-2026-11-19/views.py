import numpy as np
from scipy import fft, signal

OPS = [
    "BRIDE", "BEAST", "MIRROR", "SHADOW", "FLAME",
    "THUNDER", "INVERSION", "SILENCE", "TS", "ST"
]

def prefix(a):
    return np.pad(a.cumsum(0).cumsum(1), ((1, 0), (1, 0)))

def boxes(a, wf, wt):
    I = prefix(a)
    return (
        I[wf:, wt:] - I[:-wf, wt:]
        - I[wf:, :-wt] + I[:-wf, :-wt]
    ) / (wf * wt)

def boxmax(a, timewidths=(1, 4, 16)):
    best = (-np.inf, {})
    for wf in [8, 32, 128]:
        if wf > a.shape[0]:
            continue
        for wt in timewidths:
            if wt > a.shape[1]:
                continue
            b = boxes(a, wf, wt)
            ij = np.unravel_index(np.argmax(b), b.shape)
            value = float(b[ij])
            if value > best[0]:
                best = (
                    value,
                    {
                        "f_start": int(ij[0]),
                        "t_start": int(ij[1]),
                        "f_width": wf,
                        "t_width": wt,
                    },
                )
    return {"score": max(0, best[0]), **best[1]}

def voltage_power(x):
    # Two feeds; 64 nonoverlapping windows of 256 samples.
    z = fft.fftshift(
        fft.fft(
            np.asarray(x).reshape(2, 64, 256)
            * signal.windows.hann(256, sym=False)[None, None, :],
            axis=-1,
        ),
        axes=-1,
    )
    # Reverse FFT frequency order because source channel bandwidth is negative.
    return (abs(z) ** 2).sum(0).T[::-1]

def fields(P):
    L = np.log(np.maximum(P, np.finfo(float).tiny))
    out = []
    for axis in [0, 1]:
        a = L - np.median(L, axis=axis, keepdims=True)
        center = np.median(a)
        scale = 1.4826 * np.median(abs(a - center))
        out.append(a / max(scale, 1e-12))
    return out

# A = frequency-median subtraction at each time:
#     retains persistent narrow spectral peaks/deficits.
# B = time-median subtraction at each frequency:
#     retains temporal change.
# Scaling is global MAD for each field, not Gaussian sigma.

def phase_grain(x):
    seg = np.asarray(x).reshape(2, 4, 4096)
    u = seg / np.maximum(abs(seg), np.finfo(float).tiny)
    best = (-1, {})
    for q in [2, 4, 8]:
        z = abs(fft.fft(u ** q, axis=-1)) / 4096
        ij = np.unravel_index(np.argmax(z), z.shape)
        value = float(z[ij])
        if value > best[0]:
            best = (
                value,
                {
                    "order": q,
                    "feed": int(ij[0]),
                    "segment": int(ij[1]),
                    "powered_bin": int(ij[2]),
                },
            )
    return {"score": best[0], **best[1]}

def views(P, x=None):
    P = np.asarray(P, dtype=float)
    A, B = fields(P)
    F, T = A.shape
    result = {}

    # BRIDE: 16 frequency groups; exclude adjacent pairs.
    groups = B.reshape(16, F // 16, T).mean(1)
    groups -= groups.mean(1, keepdims=True)
    norm = np.sqrt((groups ** 2).sum(1))
    C = groups @ groups.T / np.maximum(
        norm[:, None] * norm[None, :], 1e-20
    )
    ii, jj = np.triu_indices(16, k=2)
    j = int(np.argmax(C[ii, jj]))
    result["BRIDE"] = {
        "score": float(max(0, C[ii[j], jj[j]])),
        "group_a": int(ii[j]),
        "group_b": int(jj[j]),
    }

    result["BEAST"] = phase_grain(x) if x is not None else None

    # MIRROR: double-median log contrast, then translated recurrence.
    M = np.log(np.maximum(P, np.finfo(float).tiny))
    M -= np.median(M, axis=1, keepdims=True)
    M -= np.median(M, axis=0, keepdims=True)
    C = signal.fftconvolve(M, M[::-1, ::-1], mode="full")
    E = prefix(M * M)
    ds = np.arange(-64, 65)[:, None]
    dt = np.arange(1, min(24, T // 2) + 1)[None, :]

    def rect(f0, f1, t0, t1):
        return E[f1, t1] - E[f0, t1] - E[f1, t0] + E[f0, t0]

    e0 = rect(np.maximum(ds, 0), np.minimum(F, F + ds), dt, T)
    e1 = rect(np.maximum(-ds, 0), np.minimum(F, F - ds), 0, T - dt)
    corr = C[F - 1 + ds, T - 1 + dt] / np.maximum(
        np.sqrt(e0 * e1), 1e-30
    )
    ij = np.unravel_index(np.argmax(corr), corr.shape)
    result["MIRROR"] = {
        "score": float(corr[ij]),
        "f_shift_bins": int(ds[ij[0], 0]),
        "t_shift_rows": int(dt[0, ij[1]]),
    }

    for name, sign in [("SHADOW", -1), ("FLAME", 1)]:
        candidates = [
            {**boxmax(sign * field), "normalization": i}
            for i, field in enumerate([A, B])
        ]
        result[name] = max(candidates, key=lambda v: v["score"])

    # THUNDER: every split with >=2 rows on each side.
    I = np.pad(np.cumsum(B, axis=1), ((0, 0), (1, 0)))
    best = (-1, {})
    for split in range(2, T - 1):
        d = (
            (I[:, -1] - I[:, split]) / (T - split)
            - I[:, split] / split
        ) * np.sqrt(split * (T - split) / T)
        for wf in [8, 32, 128]:
            v = np.convolve(d, np.ones(wf) / wf, mode="valid")
            k = int(np.argmax(abs(v)))
            score = float(abs(v[k]))
            if score > best[0]:
                best = (
                    score,
                    {
                        "split": split,
                        "f_start": k,
                        "f_width": wf,
                        "direction": int(np.sign(v[k])),
                    },
                )
    result["THUNDER"] = {"score": best[0], **best[1]}

    # INVERSION: signed increment asymmetry.
    best = (-1, {})
    for wf in [8, 32, 128]:
        g = boxes(B, wf, 1)
        d = np.diff(g, axis=1)
        ratio = (d ** 3).sum(1) / np.maximum(
            (abs(d) ** 3).sum(1), 1e-30
        )
        k = int(np.argmax(abs(ratio)))
        if abs(ratio[k]) > best[0]:
            best = (
                float(abs(ratio[k])),
                {
                    "f_start": k,
                    "f_width": wf,
                    "signed_asymmetry": float(ratio[k]),
                },
            )
    result["INVERSION"] = {"score": best[0], **best[1]}

    # SILENCE: longest run below -1 robust unit, in either baseline.
    best = (-1, {})
    for mode, field in enumerate([A, B]):
        for wf in [8, 32]:
            g = boxes(field, wf, 1)
            low = g < -1
            runs = np.zeros(g.shape[0], int)
            for t in range(T):
                runs = np.where(low[:, t], runs + 1, 0)
                k = int(np.argmax(runs))
                value = float(runs[k] / np.sqrt(T))
                if value > best[0]:
                    best = (
                        value,
                        {
                            "f_start": k,
                            "f_width": wf,
                            "end_row": t,
                            "run_rows": int(runs[k]),
                            "threshold_robust_unit": -1,
                            "normalization": mode,
                        },
                    )
    result["SILENCE"] = {"score": best[0], **best[1]}

    result["TS"] = boxmax(
        np.diff(np.maximum(-B, 0), axis=1), (1, 4)
    )
    result["ST"] = boxmax(
        np.maximum(-np.diff(B, axis=1), 0), (1, 4)
    )
    return result
