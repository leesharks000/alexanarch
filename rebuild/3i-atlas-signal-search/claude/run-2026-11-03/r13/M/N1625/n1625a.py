"""PLAN-N1625-run, part 1: the translated-shape recurrence score, its null, and the self-test.
python3 n1625a.py selftest [nproc] | scan SCAN | read"""
import json, os, sys, time
import numpy as np
from scipy.ndimage import uniform_filter1d
HERE = os.path.dirname(os.path.abspath(__file__))
LAGS = [4, 16, 64, 256, 1024]; SHIFTS = list(range(-8, 9)); BL = 512; TILE = 32; TOPK = 10
HANN = np.hanning(BL)


def vectors(z):
    """z: complex series -> (B, 512) baseline-subtracted unit-scaled log-power vectors, and mean power per bin."""
    B = len(z) // BL; X = z[:B * BL].reshape(B, BL) * HANN
    P = np.abs(np.fft.fftshift(np.fft.fft(X, axis=1), axes=1)) ** 2
    P = np.minimum(P / np.maximum(np.median(P, 1, keepdims=True), 1e-30), 100.0); Lg = np.log(np.maximum(P, 1e-6))
    V = Lg - uniform_filter1d(Lg, 33, axis=1, mode="wrap")
    return V, P.mean(0)


def scale(V):
    n = np.linalg.norm(V, axis=1); fl = np.quantile(n, 0.2); return V / np.maximum(n, fl)[:, None]


def score(U, lags=LAGS):
    """Family max of S(L,s,t) over candidates with participation ratio >= 4; also the best with s != 0."""
    best = (-9, None); best_nz = (-9, None); B = len(U)
    for L in lags:
        if B - 3 * L < 1: continue
        A = U[:-L]
        for s in SHIFTS:
            Bs = np.roll(U[L:], -s, axis=1); c = np.einsum("ij,ij->i", A, Bs); n = len(c)
            S = np.minimum(np.minimum(c[:n - 2 * L], c[L:n - L]), c[2 * L:])
            for t in np.argsort(S)[::-1][:TOPK]:
                w = sum(np.maximum(A[t + k * L] * Bs[t + k * L], 0) for k in range(3))
                if w.sum() <= 0 or w.sum() ** 2 / (w ** 2).sum() < 4: continue
                val = float(S[t])
                if val > best[0]: best = (val, (L, s, int(t)))
                if s != 0 and val > best_nz[0]: best_nz = (val, (L, s, int(t)))
                break
    return best, best_nz


def score_at(U, L, s):
    B = len(U)
    if B - 3 * L < 1: return None
    A = U[:-L]; Bs = np.roll(U[L:], -s, axis=1); c = np.einsum("ij,ij->i", A, Bs); n = len(c)
    S = np.minimum(np.minimum(c[:n - 2 * L], c[L:n - L]), c[2 * L:]); return float(S.max())


def perms(B, n, seed):
    rng = np.random.default_rng(seed); out = []
    for _ in range(n):
        idx = np.arange(B).reshape(-1, TILE).copy()
        for row in idx: rng.shuffle(row)
        out.append(idx.ravel())
    return out


def test(z, nperm, seed, lags=LAGS, fixed=None, lobo=False):
    V, mp = vectors(z)
    if lobo: V = V.copy(); V[:, int(np.argmax(mp))] = 0
    U = scale(V)
    P = perms(len(U), nperm, seed)
    if fixed is not None:
        real = score_at(U, *fixed); sur = [score_at(U[p], *fixed) for p in P]
        return dict(score=real, p=(1 + sum(x >= real for x in sur)) / (nperm + 1), sur_median=float(np.median(sur)))
    (r, arg), (rnz, argnz) = score(U, lags); sur = [score(U[p], lags)[0][0] for p in P]
    return dict(score=r, arg=arg, score_nonzero_shift=rnz, arg_nonzero_shift=argnz,
                p=(1 + sum(x >= r for x in sur)) / (nperm + 1), sur_median=float(np.median(sur)))


# ---- self-test -------------------------------------------------------------
NS = 32 * 65536


def motif(rng, amp):
    ntone = int(rng.integers(4, 9)); bins = rng.choice(np.arange(40, 470), ntone, replace=False); s = int(rng.choice([-2, -1, 1, 2]))
    x = np.zeros(NS, complex); t = np.arange(BL); k = 0
    for b0 in range(0, NS // BL, 16):
        ph = rng.random() * 2 * np.pi; env = 0.5 + rng.random()
        pk = sum(np.exp(1j * (2 * np.pi * ((bb + k * s) % BL - BL // 2) * t / BL + ph + 0.3 * j)) for j, bb in enumerate(bins))
        x[b0 * BL:(b0 + 1) * BL] = env * pk; k += 1
    x *= amp / np.sqrt(np.mean(np.abs(x) ** 2)); return x, s


def noise(rng): return (rng.normal(size=NS) + 1j * rng.normal(size=NS)) / np.sqrt(2)


def trial(args):
    kind, amp, seed = args; rng = np.random.default_rng(seed); n = noise(rng); s = None
    if kind == "motif": m, s = motif(rng, amp); z = n + m
    elif kind == "tone": z = n + amp * np.exp(2j * np.pi * 0.1234 * np.arange(NS))
    elif kind == "hop":
        b = rng.integers(0, BL, NS // BL); t = np.arange(BL)
        h = np.concatenate([np.exp(2j * np.pi * (bb - BL // 2) * t / BL) for bb in b]); z = n + amp * h
    else: z = n
    r = test(z, 19, seed + 7); r.update(kind=kind, amp=amp, seed=seed, injected_shift=s); return r


def selftest(nproc):
    from multiprocessing import Pool
    jobs = [("motif", a, 1000 + 100 * i + k) for i, a in enumerate((0.25, 0.5, 1.0)) for k in range(20)]
    jobs += [("noise", 0.0, 5000 + k) for k in range(100)] + [("tone", 1.0, 9001), ("hop", 1.0, 9002)]
    T0 = time.time()
    with Pool(nproc) as p: res = p.map(trial, jobs)
    json.dump(res, open(os.path.join(HERE, "selftest.json"), "w"))
    for a in (0.25, 0.5, 1.0):
        rr = [r for r in res if r["kind"] == "motif" and r["amp"] == a]
        print(f"motif rms {a}: recovered {sum(r['p'] <= 0.05 for r in rr)}/20; args", [r["arg"] for r in rr[:6]], "injected s", [r["injected_shift"] for r in rr[:6]])
    nn = [r for r in res if r["kind"] == "noise"]; print("noise: false", sum(r["p"] <= 0.05 for r in nn), "/100")
    for k in ("tone", "hop"): r = next(r for r in res if r["kind"] == k); print(k, "p", r["p"], "score", round(r["score"], 3), r["arg"])
    print("seconds", round(time.time() - T0))


# ---- real data ---------------------------------------------------------------
def real(s):
    d = np.load(os.path.join(HERE, f"crops_{s}.npz")); out = {"scan": s}
    for sl in ("target", "ctrl25k", "hidrift"):
        for q in "XY":
            z = np.concatenate([np.fft.ifft(np.fft.ifftshift(F)) for F in d[f"{sl}_{q}"]])
            seed = 16250 + 1000 * ["0013", "0014", "0015", "0016", "0017", "0018"].index(s) + 10 * "XY".index(q) + ["target", "ctrl25k", "hidrift"].index(sl)
            r = {"full": test(z, 199, seed)}
            if sl == "target": r["lobo"] = test(z, 199, seed + 3, lobo=True)
            if s == "0013" and sl == "target":
                h = len(z) // 2; r["half1"] = test(z[:h], 199, seed + 5, lags=[4, 16, 64, 256])
            out[f"{sl}_{q}"] = r
            print(s, sl, q, "score", round(r["full"]["score"], 4), r["full"]["arg"], "p", r["full"]["p"], flush=True)
    json.dump(out, open(os.path.join(HERE, f"n_{s}.json"), "w"))


def holdout_and_controls():
    """Given ON0013 first-half candidates, test the same (L, s) in the second half and elsewhere."""
    R = json.load(open(os.path.join(HERE, "n_0013.json"))); out = {}
    for q in "XY":
        h1 = R[f"target_{q}"]["half1"]
        if h1["p"] > 0.05 or h1["arg"] is None: out[q] = {"candidate": None, "half1_p": h1["p"]}; continue
        L, s, _ = h1["arg"]; o = {"candidate": [L, s], "half1_p": h1["p"]}
        for sc in ("0013", "0014", "0015", "0016", "0017", "0018"):
            d = np.load(os.path.join(HERE, f"crops_{sc}.npz"))
            for sl in ("target", "ctrl25k", "hidrift"):
                z = np.concatenate([np.fft.ifft(np.fft.ifftshift(F)) for F in d[f"{sl}_{q}"]])
                if sc == "0013" and sl == "target":
                    o["half2"] = test(z[len(z) // 2:], 199, 777, fixed=(L, s))
                o[f"{sc}_{sl}"] = test(z, 199, 778, fixed=(L, s))
        out[q] = o
    json.dump(out, open(os.path.join(HERE, "n_gates.json"), "w")); print(json.dumps(out, indent=1)[:4000])


if __name__ == "__main__":
    a = sys.argv[1]
    if a == "selftest": selftest(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif a == "scan": real(sys.argv[2])
    elif a == "gates": holdout_and_controls()
