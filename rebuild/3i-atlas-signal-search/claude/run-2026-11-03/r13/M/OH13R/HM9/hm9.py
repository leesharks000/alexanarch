"""PLAN-HM9: reading for coherence.   python3 hm9.py selftest | stage1 | stage2
Reads HMR2's kept products (hashed in HMR2/RESULTS-HMR2.sha256): per frame and window, the de-Dopplered complex
spectrum's central 33 bins (SP) and the X/Y power ratio (P), for the comet cohort's 95 windows (11 coordinates, 84
sidebands), 833 frames, scans 0013-0018. Stage 1 reads ON 0013 and OFF 0014 only. Stage 2 reads the hold-out
(0015-0018), after any amendment is frozen."""
import hashlib, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "../HMR2")
SEED = 20261123; PTH = 1e-4; NS_SHIFT = 2000; NS_PHASE = 2000; NS_SETS = 10000; NS_H4 = 200
CB = list(range(14, 19))   # centre bin 16 and +-2 bins (+-5.6 Hz)
TAUS = list(range(1, 9))   # frame lags 1..8 (0.36-2.9 s)
G = ["C08", "C09", "C10", "C11"]


def coh(a, b):
    return np.abs(np.sum(a * np.conj(b), axis=0)) / np.sqrt(np.sum(np.abs(a) ** 2, axis=0) * np.sum(np.abs(b) ** 2, axis=0))


def h1(X, Y):  # cross-feed coherence, centre bins; X, Y: (N, 33)
    g = coh(X[:, CB], Y[:, CB]); i = int(np.argmax(g)); N = X.shape[0]
    cross = np.sum(X[:, CB[i]] * np.conj(Y[:, CB[i]]))
    return float(g[i]), CB[i] - 16, float(np.angle(cross)), float(1 - (1 - np.exp(-N * g[i] ** 2)) ** len(CB))


def h2(S):  # carrier coherence across frames, one feed; S: (N, 33)
    N = S.shape[0]; best = (0.0, 0, 0)
    for t in TAUS:
        a, b = S[:-t][:, CB], S[t:][:, CB]; r = coh(a, b); i = int(np.argmax(r))
        if r[i] > best[0]: best = (float(r[i]), CB[i] - 16, t)
    p1 = np.exp(-(N - best[2]) * best[0] ** 2)
    pg = np.abs(np.fft.fft(S[:, CB], axis=0)) ** 2; pg = pg / pg.mean(axis=0); j = np.unravel_index(np.argmax(pg), pg.shape)
    r = float(pg[j])
    return {"rho": best[0], "bin": best[1], "tau": best[2], "p": float(1 - (1 - p1) ** (len(CB) * len(TAUS))),
            "pgram_peak": r, "pgram_bin": CB[j[1]] - 16, "pgram_cycles": int(j[0]) if j[0] <= N // 2 else int(j[0]) - N,
            "pgram_p": float(1 - (1 - np.exp(-r)) ** (len(CB) * N))}


def h4mat(V):  # V: (N, 66) normalized; leading eigenvalue at lag 0, leading singular value at lags 1..8
    N = V.shape[0]; G0 = V.conj().T @ V / N; w, U = np.linalg.eigh(G0)
    lag = [(np.linalg.svd(V[:-t].conj().T @ V[t:] / (N - t), compute_uv=False)[0], t) for t in TAUS]
    s, t = max(lag)
    return float(w[-1]), U[:, -1], float(s), int(t)


def vec(SPs, fi_both=True):
    V = np.concatenate([SPs[0], SPs[1]], axis=1)  # (N, 66): X bins then Y bins
    return V / np.sqrt(np.mean(np.abs(V) ** 2, axis=0))


def form(u):
    e = np.abs(u) ** 2
    return {"X_share": round(float(e[:33].sum()), 3), "Y_share": round(float(e[33:].sum()), 3),
            "top_elements": [("X" if k < 33 else "Y") + f"{(k % 33) - 16:+d}" for k in np.argsort(e)[::-1][:6]],
            "top_weights": [round(float(x), 3) for x in np.sort(e)[::-1][:6]]}


def read_scan(SP, P, names, kinds, rng, coord_idx, fixed=None):
    """All readings for one scan. SP (2, N, 95, 33); P (2, N, 95). Surrogates only at the comet coordinates."""
    out = {}; N = SP.shape[1]
    for i, nm in enumerate(names):
        X, Y = SP[0, :, i, :], SP[1, :, i, :]
        r = {}
        g, b, ph, p = h1(X, Y); r["H1"] = {"gamma": g, "bin": b, "phase": ph, "p": p}
        r["H2X"] = h2(X); r["H2Y"] = h2(Y)
        V = vec((X, Y)); l0, u, sl, t = h4mat(V); r["H4"] = {"lam0": l0, "form0": form(u), "sv_lag": sl, "tau": t}
        if fixed and nm in fixed:  # stage 2: the stage-1 form, held fixed
            uf = np.array(fixed[nm]["re"]) + 1j * np.array(fixed[nm]["im"]); G0 = V.conj().T @ V / N
            r["H4"]["fixed_form_q"] = float(np.real(uf.conj() @ G0 @ uf))
        if i in coord_idx:
            # H1 empirical: circular shifts of Y by 20..N-20 frames
            sh = rng.integers(20, N - 20, NS_SHIFT)
            r["H1"]["emp_ge"] = int(sum(h1(X, np.roll(Y, k, axis=0))[0] >= g for k in sh))
            # H2 empirical: an independent random phase per frame (keeps each frame's spectrum, breaks the carrier across frames)
            for fe, S in (("H2X", X), ("H2Y", Y)):
                ge = gp = 0
                for _ in range(NS_PHASE):
                    q = h2(S * np.exp(2j * np.pi * rng.random(N))[:, None]); ge += q["rho"] >= r[fe]["rho"]; gp += q["pgram_peak"] >= r[fe]["pgram_peak"]
                r[fe]["emp_ge"] = int(ge); r[fe]["pgram_emp_ge"] = int(gp)
            # H4 empirical: each of the 66 element series circularly shifted independently (zero lag);
            # an independent random phase per frame and element (lags)
            ge0 = gel = 0; geq = 0
            for _ in range(NS_H4):
                Vs = np.stack([np.roll(V[:, k], rng.integers(20, N - 20)) for k in range(66)], axis=1)
                ge0 += h4mat(Vs)[0] >= l0
                Vp = V * np.exp(2j * np.pi * rng.random(V.shape))
                gel += h4mat(Vp)[2] >= sl
                if fixed and nm in fixed:
                    G0s = Vs.conj().T @ Vs / N; geq += float(np.real(uf.conj() @ G0s @ uf)) >= r["H4"]["fixed_form_q"]
            r["H4"]["emp0_ge"] = int(ge0); r["H4"]["emplag_ge"] = int(gel)
            if fixed and nm in fixed: r["H4"]["fixed_emp_ge"] = int(geq)
            r["H4"]["u0"] = {"re": u.real.tolist(), "im": u.imag.tolist()}
        out[nm] = r
    # H3: common mode of the X power ratio among C08-C11, against random four-sets of sidebands
    sbi = [i for i, k in enumerate(kinds) if k.startswith("sb:")]; gi = [names.index(c) for c in G]
    h3 = {}
    for fi, fe in enumerate("XY"):
        for form_, A in (("raw", P[fi]), ("diff", np.diff(P[fi], axis=0))):
            Cm = np.corrcoef(A.T); mr = lambda ix: float(np.mean([Cm[a, b] for k, a in enumerate(ix) for b in ix[k + 1:]]))
            obs = mr(gi); null = np.array([mr(list(rng.choice(sbi, 4, replace=False))) for _ in range(NS_SETS)])
            own = {c: float(np.mean([Cm[names.index(c), j] for j in sbi if kinds[j] == "sb:" + c])) for c in G}
            h3[f"{fe}|{form_}"] = {"mean_r_G": obs, "null_ge": int((null >= obs).sum()), "null_mean": float(null.mean()),
                                   "null_q9999": float(np.quantile(null, 0.9999)), "own_sideband_mean_r": own,
                                   "coord_matrix": [[round(float(Cm[names.index(a), names.index(b)]), 4) for b in names if b[0] == "C" and "k" not in b]
                                                    for a in names if a[0] == "C" and "k" not in a]}
    out["_H3"] = h3
    return out


def rules(R, names, kinds, coords):
    """Per coordinate: does each reading pass (PLAN §3)?"""
    sb = {c: [n for n, k in zip(names, kinds) if k == "sb:" + c] for c in coords}; res = {}
    for c in coords:
        r = R[c]; above = lambda f: all(f(r) > f(R[s]) for s in sb[c])
        res[c] = {
            "H1_cross_feed": bool(r["H1"]["p"] < PTH and r["H1"]["emp_ge"] == 0 and above(lambda q: q["H1"]["gamma"])),
            "H2X_carrier": bool((r["H2X"]["p"] < PTH and r["H2X"]["emp_ge"] == 0 and above(lambda q: q["H2X"]["rho"])) or
                                (r["H2X"]["pgram_p"] < PTH and r["H2X"]["pgram_emp_ge"] == 0 and above(lambda q: q["H2X"]["pgram_peak"]))),
            "H2Y_carrier": bool((r["H2Y"]["p"] < PTH and r["H2Y"]["emp_ge"] == 0 and above(lambda q: q["H2Y"]["rho"])) or
                                (r["H2Y"]["pgram_p"] < PTH and r["H2Y"]["pgram_emp_ge"] == 0 and above(lambda q: q["H2Y"]["pgram_peak"]))),
            "H4_open_zero_lag": bool(r["H4"]["emp0_ge"] == 0 and above(lambda q: q["H4"]["lam0"])),
            "H4_open_lag": bool(r["H4"]["emplag_ge"] == 0 and above(lambda q: q["H4"]["sv_lag"]))}
    h3 = {k: bool(v["null_ge"] == 0) for k, v in R["_H3"].items()}
    return res, h3


def base_rate(R, names, kinds):
    sbn = [n for n, k in zip(names, kinds) if k.startswith("sb:")]
    return {"sidebands": len(sbn), "H1_p_lt": sum(R[n]["H1"]["p"] < PTH for n in sbn),
            "H2X_p_lt": sum(R[n]["H2X"]["p"] < PTH or R[n]["H2X"]["pgram_p"] < PTH for n in sbn),
            "H2Y_p_lt": sum(R[n]["H2Y"]["p"] < PTH or R[n]["H2Y"]["pgram_p"] < PTH for n in sbn)}


def verify_sources(scans):
    want = {}
    for line in open(os.path.join(SRC, "RESULTS-HMR2.sha256")):
        h, f = line.split(); want[f] = h
    for s in scans:
        f = f"hmr2_{s}.npz"; h = hashlib.sha256(open(os.path.join(SRC, f), "rb").read()).hexdigest()
        assert want.get(f) == h, f"hash mismatch {f}"
    return True


def load(s):
    z = np.load(os.path.join(SRC, f"hmr2_{s}.npz")); W = json.load(open(os.path.join(SRC, f"hmr2_{s}.json")))["windows"]
    return z["SP"], z["P"], [w[0] for w in W], [w[1] for w in W]


def stage(scans, tag, fixed=None):
    verify_sources(scans); rng = np.random.default_rng(SEED + (0 if tag == "stage1" else 1)); out = {"plan": "PLAN-HM9.md", "stage": tag, "seed": SEED}
    for s in scans:
        SP, P, names, kinds = load(s); coords = [n for n, k in zip(names, kinds) if k == "sel"]; ci = [names.index(c) for c in coords]
        R = read_scan(SP, P, names, kinds, rng, ci, fixed); ru, h3 = rules(R, names, kinds, coords)
        out[s] = {"readings": R, "rules": ru, "H3_rules": h3, "base_rate": base_rate(R, names, kinds)}
        print(s, "done", {c: [k for k, v in ru[c].items() if v] for c in coords}, h3, flush=True)
    json.dump(out, open(os.path.join(HERE, f"hm9_{tag}.json"), "w"))


def selftest():
    """Synthetic only: complex Gaussian noise, and the same with a coherent tone in both feeds at one coordinate."""
    rng = np.random.default_rng(1); N, nw = 833, 95
    names = ["C%02d" % i for i in range(3, 14)]; kinds = ["sel"] * 11
    for c in list(names):
        for k in range(8 if c in ("C03", "C04", "C05", "C06", "C07", "C08", "C09") else 7): names.append(f"{c}+{k}k"); kinds.append("sb:" + c)
    assert len(names) == nw
    SP = (rng.standard_normal((2, N, nw, 33)) + 1j * rng.standard_normal((2, N, nw, 33))) / np.sqrt(2)
    P = rng.random((2, N, nw)); ci = list(range(11))
    global NS_SHIFT, NS_PHASE, NS_SETS, NS_H4
    NS_SHIFT = NS_PHASE = 200; NS_SETS = 1000; NS_H4 = 20
    R = read_scan(SP, P, names, kinds, rng, ci); ru, h3 = rules(R, names, kinds, names[:11])
    print("noise: passes", sum(v for c in ru.values() for v in c.values()), "H3", h3)
    tone = 0.25 * np.exp(2j * np.pi * (0.3 * np.arange(N) + 0.1))  # a carrier 0.3 bin off centre, both feeds, 0.25 of noise rms
    SP[0, :, 5, 16] += tone; SP[1, :, 5, 16] += tone * np.exp(0.7j)
    P[0, :, 5:9] += 0.5 * np.sin(np.arange(N) / 30)[:, None]  # a common mode at C08-C11
    R = read_scan(SP, P, names, kinds, rng, ci); ru, h3 = rules(R, names, kinds, names[:11])
    print("tone at C08:", ru["C08"], "form", R["C08"]["H4"]["form0"]["top_elements"][:3], "H3", h3)
    s = (rng.standard_normal(N) + 1j * rng.standard_normal(N)) / np.sqrt(2)  # a noise-like source common to both feeds
    SP[0, :, 6, 16] += 0.4 * s; SP[1, :, 6, 16] += 0.4 * s * np.exp(1.1j)
    env = (rng.standard_normal(N) + 1j * rng.standard_normal(N)) / np.sqrt(2)  # one series across nine X bins: a shaped form
    SP[0, :, 7, 12:21] += 0.4 * env[:, None] * np.exp(1j * np.linspace(0, 2, 9))[None, :]
    R = read_scan(SP, P, names, kinds, rng, ci); ru, h3 = rules(R, names, kinds, names[:11])
    print("common noise at C09:", ru["C09"], "gamma", round(R["C09"]["H1"]["gamma"], 3))
    print("nine-bin form at C10:", ru["C10"], "lam0", round(R["C10"]["H4"]["lam0"], 2), "form", R["C10"]["H4"]["form0"]["top_elements"])


if __name__ == "__main__":
    a = sys.argv[1]
    if a == "selftest": selftest()
    elif a == "stage1": stage(["0013", "0014"], "stage1")
    elif a == "stage2":
        s1 = json.load(open(os.path.join(HERE, "hm9_stage1.json")))
        fixed = {c: s1["0013"]["readings"][c]["H4"]["u0"] for c in s1["0013"]["rules"]}
        stage(["0015", "0016", "0017", "0018"], "stage2", fixed)
