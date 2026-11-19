"""PLAN-M4b drift search: incoherent sums along straight drift lines (Taylor tree), at three frequency resolutions.
Imported by mvb.py; its test is test_mdrift.py."""
import numpy as np

NR = 64                 # rows after padding (an M4 scan has 46-49 on-target integrations of 6.08 s)
LEVELS = (1, 4, 16)     # frequency bins summed per cell: 2.79 Hz, 11.2 Hz, 44.7 Hz


def tree(A):
    """A: (NR, M). Returns D: (NR, M), D[d, b] = sum over rows r of A[r, b + round(d*r/(NR-1))] (Taylor's tree),
    for drifts d = 0..NR-1 cells over the NR rows, with circular wrap at the band edges."""
    D = A.copy(); b = 1
    while b < NR:
        h = b; b *= 2
        D = D.reshape(NR // b, 2, h, -1); out = np.empty((NR // b, b, D.shape[-1]), D.dtype)
        for d in range(b):
            dl = d // 2; sh = d - dl
            out[:, d] = D[:, 0, dl] + np.roll(D[:, 1, dl], -sh, axis=-1)
        D = out.reshape(NR, -1)
    return D


def zscore(row):
    s = row[::7]; m = np.median(s); sd = 1.4826 * np.median(np.abs(s - m))
    return (row - m) / (sd if sd > 0 else 1.0)


def search(R, zkeep=6.0):
    """R: (n, N) normalised power, rows in time order. For each level: per cell, the largest z over drifts -NR+1..NR-1
    and the drift attaining it; plus sparse cells with z >= zkeep. Drift d is in cells per (NR-1) rows."""
    n, N = R.shape; out = {}
    A = np.zeros((NR, N), np.float32); A[:n] = R[:NR]
    for L in LEVELS:
        Ak = A.reshape(NR, N // L, L).sum(-1)
        best = np.full(N // L, -np.inf, np.float32); bd = np.zeros(N // L, np.int16)
        for sgn in (1, -1):
            D = tree(Ak if sgn > 0 else Ak[:, ::-1])
            if sgn < 0: D = D[:, ::-1]
            for d in range(NR):
                if sgn < 0 and d == 0: continue
                z = zscore(D[d]).astype(np.float32)
                m = z > best; best[m] = z[m]; bd[m] = sgn * d
        out[L] = {"maxz": best.astype(np.float16), "drift": bd}
        k = np.where(best >= zkeep)[0]; out[L]["idx"] = k.astype(np.int32); out[L]["z"] = best[k]; out[L]["d"] = bd[k]
    return out
