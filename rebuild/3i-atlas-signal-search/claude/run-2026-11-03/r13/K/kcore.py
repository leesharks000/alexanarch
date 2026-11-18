"""PLAN-K core: the relation and its statistics on one scan's integrations (shared by kv.py and kinject.py)."""
import numpy as np
DSET = (8, 32, 128, 512, 2048); PSET = (2, 4, 8, 16); NTOP2, NTOP3 = 20, 50

def shift(R, sh):
    """Row k moved by -sh[k] bins (as np.roll(R[k], -sh[k]))."""
    out = np.empty_like(R)
    for k in range(R.shape[0]): out[k] = np.roll(R[k], -int(sh[k]))
    return out

def stdz(A):
    A = A - A.mean(0, keepdims=True); s = A.std(0, keepdims=True); s[s == 0] = np.inf
    return (A / s).astype(np.float32)

def robz(x):
    m = np.median(x); s = 1.4826 * np.median(np.abs(x - m)); s = s if s > 0 else np.inf
    return ((x - m) / s).astype(np.float32)

def rho(A, d):
    """-mean_t a_f a_{f+d}, defined for f < N-d; padded with 0."""
    r = np.zeros(A.shape[1], np.float32); r[:-d] = -(A[:, :-d] * A[:, d:]).mean(0); return r

def sqscore(D):
    """Largest |normalised projection| of D(t) on a square wave of period p, over p in PSET and phase."""
    T = len(D); t = np.arange(T); best = (0.0, 0, 0)
    nd = np.sqrt((D * D).sum()) or np.inf
    for p in PSET:
        for ph in range(p):
            w = np.where(((t + ph) % p) < p / 2, 1.0, -1.0)
            s = abs((D * w).sum()) / (nd * np.sqrt(T))
            if s > best[0]: best = (float(s), p, ph)
    return best

def relate(Rs, mask_dc=True):
    """Rs: (T, N) shifted, normalised integrations (kept rows only). Returns per-d rho z (full), and the K2/K3 records."""
    T, N = Rs.shape
    if mask_dc: Rs = Rs.copy(); Rs[:, N // 2 - 4:N // 2 + 5] = 0
    h = T // 2
    A, A1, A2 = stdz(Rs), stdz(Rs[:h]), stdz(Rs[h:])
    out = {}
    for d in DSET:
        lim = slice(0, N - d)
        z = robz(rho(A, d)[lim]); z1 = robz(rho(A1, d)[lim]); z2 = robz(rho(A2, d)[lim])
        if mask_dc: z[N // 2 - 4 - d:N // 2 + 5] = 0; z1[N // 2 - 4 - d:N // 2 + 5] = 0; z2[N // 2 - 4 - d:N // 2 + 5] = 0
        top2 = np.argsort(z1)[-NTOP2:]
        top3 = np.argsort(z)[-NTOP3:]
        k3 = [sqscore(A[:, f] - A[:, f + d]) for f in top3]
        out[d] = {"z": z, "k2_f": top2.astype(np.int32), "k2_h1": z1[top2], "k2_h2": z2[top2],
                  "k3_f": top3.astype(np.int32), "k3_s": np.array([x[0] for x in k3], np.float32),
                  "k3_p": np.array([x[1] for x in k3], np.int8), "k3_ph": np.array([x[2] for x in k3], np.int8)}
    return out
