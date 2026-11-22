"""PLAN-HMR2: python3 hmr2.py SCAN [NFRAMES] | score
Reading D3: the comet cohort's 95 windows (11 coordinates and their sidebands), every frame, both feeds, scans 0013-0018.
Kept per frame and window: the complex D3 at lags d = 1..16 (d = 2 is HM5's), power as HM4 §D, and the de-Dopplered
spectrum's central 33 bins (+-16 bins, +-44.7 Hz) for demodulation."""
import json, os, sys, time
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(HERE, "../FD")); sys.path.insert(0, os.path.join(HERE, "../HM"))
DS = np.arange(1, 17); HB = 16
OUT = os.environ.get("HMR2_OUT", HERE)


def windows():
    import hm
    real = hm.HERE; hm.HERE = HERE
    src = os.path.join(HERE, "hm_selections.json")
    if not os.path.exists(src): os.symlink("hmr2_selections.json", src)
    W = hm.hm_windows(); hm.HERE = real
    return [w for w in W if w[1] != "ref" and w[4] == "true"]  # the comet cohort: coordinates and their sidebands


def d3c(u, d):
    n = u.shape[1] - 2 * d
    return np.mean(u[:, :n] * u[:, 2 * d:2 * d + n] * np.conj(u[:, d:d + n]) ** 2, axis=1)


def scan(s, nf=None):
    import fdstream as F
    from common import N, DF, NF, TF, W as WW, dm
    NF = nf or NF
    WIN = windows()
    T0 = json.load(open(os.path.join(HERE, "hmr2_selections.json")))["T0_mjd"]; c = WW // 2; SR = WW * DF
    ifl = np.array([F.track_f(s, f, dv, T0)[:NF] for _, _, f, dv, _ in WIN]); mid = np.rint(np.median(np.rint(ifl), axis=1)).astype(int)
    off_f = (ifl - mid[:, None]) * DF; nw = len(WIN); assert mid.min() > WW and mid.max() < N - WW
    tc = (np.arange(NF) + 0.5) * TF; carry = np.zeros(nw)
    D3 = np.zeros((2, NF, nw, len(DS)), np.complex64); P = np.zeros((2, NF, nw), np.float32); SP = np.zeros((2, NF, nw, 2 * HB + 1), np.complex64)
    T00 = time.time(); n = 0
    for j, X, Y in dm.frames(s, NF):
        ts = (j * WW + np.arange(WW)) / SR
        a = np.clip(np.searchsorted(tc, ts) - 1, 0, NF - 2); w = np.clip((ts - tc[a]) / TF, 0.0, 1.0)
        off = off_f[:, a] * (1 - w)[None, :] + off_f[:, a + 1] * w[None, :]
        Phi = carry[:, None] + 2 * np.pi * np.cumsum(off, axis=1) / SR; carry = Phi[:, -1].copy(); E = np.exp(-1j * Phi)
        for fi, Fc in enumerate((dm.fft(X), dm.fft(Y))):
            B = np.stack([Fc[m - c:m + c] for m in mid])
            z = sf.ifft(sf.ifftshift(B, axes=1), axis=1) * E; S2 = sf.fftshift(sf.fft(z, axis=1), axes=1)[:, c - 64:c + 65]
            u = S2 / np.maximum(np.abs(S2), 1e-30)
            for k, d in enumerate(DS): D3[fi, j, :, k] = d3c(u, d)
            Pw = np.abs(S2) ** 2; P[fi, j] = Pw[:, 64] / np.maximum(Pw.mean(axis=1), 1e-30)
            SP[fi, j] = S2[:, 64 - HB:64 + HB + 1]
        n += 1
        if j % 100 == 0: print(s, j, round(time.time() - T00), flush=True)
    assert n == NF
    np.savez_compressed(os.path.join(OUT, f"hmr2_{s}.npz"), D3=D3, P=P, SP=SP)
    json.dump({"scan": s, "frames": n, "windows": [list(x) for x in WIN], "lags": DS.tolist(), "half_bins": HB, "seconds": round(time.time() - T00)},
              open(os.path.join(OUT, f"hmr2_{s}.json"), "w"))
    print(s, "done", nw, round(time.time() - T00), flush=True)


# ------------------------------------------------------------------------------------------------------------- scoring
RAYP = 1e-4; SEED = 20261122; NSUR = int(os.environ.get('HMR2_NSUR', 1000)); G = ["C08", "C09", "C10", "C11"]


def rayleigh(ph):
    n = len(ph); R = np.abs(np.mean(np.exp(1j * ph))); z = n * R * R
    p = np.exp(np.sqrt(1 + 4 * n + 4 * (n * n - (n * R) ** 2)) - (1 + 2 * n))  # Zar's approximation
    return float(R), float(z), float(min(1.0, p))


def iaaft(x, rng, it=20):
    s = np.sort(x); A = np.abs(np.fft.rfft(x)); y = rng.permutation(x)
    for _ in range(it):
        Yf = np.fft.rfft(y); y = np.fft.irfft(A * np.exp(1j * np.angle(Yf)), n=len(x)); y = s[np.argsort(np.argsort(y))]
    return y


def score():
    import zlib
    rng = np.random.default_rng(SEED)
    Z = {s: np.load(os.path.join(HERE, f"hmr2_{s}.npz")) for s in ("0013", "0014", "0015", "0016", "0017", "0018")}
    WIN = json.load(open(os.path.join(HERE, "hmr2_0013.json")))["windows"]; names = [w[0] for w in WIN]
    coords = [w[0] for w in WIN if w[1] == "sel"]; sbs = {cn: [i for i, w in enumerate(WIN) if w[1] == "sb:" + cn] for cn in coords}
    ix = {nm: i for i, nm in enumerate(names)}
    out = {"plan": "PLAN-HMR2.md", "seed": SEED}
    # reproduction: |D3 at d=2| and power against HM5's kept per-frame series (0013, 0014)
    H5 = {s: np.load(os.path.join(HERE, f"../HM5/hm5_{s}.npz")) for s in ("0013", "0014")}
    rep = {}
    for s in ("0013", "0014"):
        a = np.abs(Z[s]["D3"][:, :, :, 1]); nn = a.shape[1]; b = H5[s]["frD"][:, :nn]; pa = Z[s]["P"]; pb = H5[s]["frP"][:, :nn]
        rep[s] = {"d3_max_abs_diff": float(np.max(np.abs(a - b))), "p_max_rel_diff": float(np.max(np.abs(pa - pb) / np.maximum(np.abs(pb), 1e-12)))}
    out["reproduction"] = rep; out["reproduction_ok"] = bool(all(r["d3_max_abs_diff"] < 1e-5 and r["p_max_rel_diff"] < 1e-4 for r in rep.values()))
    print("reproduction", out["reproduction_ok"], rep, flush=True)
    # R1: phase locking of D3 (d = 2) across frames, per window, scan and feed
    R1 = {}
    for s in Z:
        for fi, fe in enumerate("XY"):
            for i, nm in enumerate(names):
                R, zz, p = rayleigh(np.angle(Z[s]["D3"][fi, :, i, 1])); R1[f"{s}|{fe}|{nm}"] = {"R": R, "z": zz, "p": p}
    # R2: the lag profile of phase-locked D3, |mean over frames of D3(d)|, d = 1..16, per window
    R2 = {}
    for s in Z:
        for fi, fe in enumerate("XY"):
            M = np.abs(Z[s]["D3"][fi].mean(axis=0))  # (nw, 16)
            for i, nm in enumerate(names): R2[f"{s}|{fe}|{nm}"] = [round(float(v), 5) for v in M[i]]
    # R3: sequence in the D3 phase (cos and sin of arg D3, d = 2): lag dependence against shuffles, compression against IAAFT
    def q(x, L=50):
        x = x - x.mean(); d = np.dot(x, x); nn = len(x); r = np.array([np.dot(x[:-k], x[k:]) / d for k in range(1, L + 1)])
        return float(nn * (nn + 2) * np.sum(r ** 2 / (nn - np.arange(1, L + 1))))
    def cz(x):
        qq = np.quantile(x, [0.25, 0.5, 0.75]); return len(zlib.compress(bytes((np.searchsorted(qq, x) + 65).astype(np.uint8)), 9))
    R3 = {}
    for s in ("0013", "0014", "0015", "0016", "0017", "0018"):
        for fi, fe in enumerate("XY"):
            for i, nm in enumerate(names):
                ph = np.angle(Z[s]["D3"][fi, :, i, 1]); rec = {}
                for part, x in (("cos", np.cos(ph)), ("sin", np.sin(ph))):
                    v1 = q(x); sh = np.array([q(rng.permutation(x)) for _ in range(NSUR)]); v2 = cz(x); ia = np.array([cz(iaaft(x, rng)) for _ in range(NSUR)])
                    rec[part] = {"q_p": float((1 + np.sum(sh >= v1)) / (1 + NSUR)), "c_p": float((1 + np.sum(ia <= v2)) / (1 + NSUR))}
                R3[f"{s}|{fe}|{nm}"] = rec
    # R4: demodulation. Per frame, the central 33 bins inverse-transformed give a 33-sample complex series (about 10.9 ms apart);
    # concatenated over frames, its envelope spectrum (|z| mean-removed) shows any amplitude modulation, read at each coordinate.
    R4 = {}
    for s in Z:
        for fi, fe in enumerate("XY"):
            sp = Z[s]["SP"][fi]  # (NF, nw, 33)
            z = np.fft.ifft(np.fft.ifftshift(sp, axes=2), axis=2)  # (NF, nw, 33)
            env = np.abs(z).transpose(1, 0, 2).reshape(len(names), -1); env = env - env.mean(axis=1, keepdims=True)
            ps = np.abs(np.fft.rfft(env, axis=1)) ** 2; fr = np.fft.rfftfreq(env.shape[1], d=0.358 / 33)
            for i, nm in enumerate(names):
                k = int(np.argmax(ps[i, 1:]) + 1); R4[f"{s}|{fe}|{nm}"] = {"peak_hz": round(float(fr[k]), 4), "peak_over_median": round(float(ps[i, k] / np.median(ps[i, 1:])), 2)}
    out["R1"] = R1; out["R2"] = R2; out["R3"] = R3; out["R4"] = R4
    # the reading rule (PLAN §3)
    reads = {}
    def above_all(key, val, s, fe, cn, f):
        return all(val > f(f"{s}|{fe}|{names[j]}") for j in sbs[cn])
    for s in Z:
        for fe in "XY":
            for cn in coords:
                k = f"{s}|{fe}|{cn}"
                r1 = R1[k]["p"] < RAYP and above_all(k, R1[k]["R"], s, fe, cn, lambda kk: R1[kk]["R"])
                r3 = any(R3[k][pt][m] <= 0.001 for pt in ("cos", "sin") for m in ("q_p", "c_p"))
                r4 = R4[k]["peak_over_median"] >= 20 and above_all(k, R4[k]["peak_over_median"], s, fe, cn, lambda kk: R4[kk]["peak_over_median"])
                reads[k] = {"R1_locked": bool(r1), "R3_sequence": bool(r3), "R4_modulation": bool(r4)}
    out["reads"] = reads
    base = {}
    for s in Z:
        for fe in "XY":
            sbk = [f"{s}|{fe}|{names[j]}" for cn in coords for j in sbs[cn]]
            base[f"{s}|{fe}"] = {"sidebands": len(sbk), "R1_p_lt": sum(R1[k]["p"] < RAYP for k in sbk),
                                 "R3_p_le_0.001": sum(any(R3[k][pt][m] <= 0.001 for pt in ("cos", "sin") for m in ("q_p", "c_p")) for k in sbk),
                                 "R4_ge_20": sum(R4[k]["peak_over_median"] >= 20 for k in sbk)}
    out["base_rate"] = base
    # hold-out: C12 power lag dependence (HMR1) in ON 0015 and 0017, X
    hold = {}
    for s in ("0015", "0017"):
        x = Z[s]["P"][0][:, ix["C12"]].astype(float); v = q(x); sh = np.array([q(rng.permutation(x)) for _ in range(NSUR)])
        sbv = [q(Z[s]["P"][0][:, j].astype(float)) for j in sbs["C12"]]
        hold[s] = {"q_p": float((1 + np.sum(sh >= v)) / (1 + NSUR)), "above_every_sideband": bool(all(v > b for b in sbv))}
    out["C12_holdout"] = hold
    json.dump(out, open(os.path.join(HERE, "hmr2_score.json"), "w"), indent=1)
    for k, v in reads.items():
        if any(v.values()): print("READ", k, v, R1[k], R4[k])
    print("base", json.dumps(base)); print("C12 hold-out", hold)
    for cn in coords: print(cn, "0013 X", "R", round(R1[f"0013|X|{cn}"]["R"], 4), "p", "%.2g" % R1[f"0013|X|{cn}"]["p"], "R4", R4[f"0013|X|{cn}"])


if __name__ == "__main__":
    a = sys.argv[1]
    score() if a == "score" else scan(a, int(sys.argv[2]) if len(sys.argv) > 2 else None)
