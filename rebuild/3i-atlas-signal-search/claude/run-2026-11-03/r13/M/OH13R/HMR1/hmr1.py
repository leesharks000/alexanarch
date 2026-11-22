"""PLAN-HMR1: python3 hmr1.py [check]
Reading before attribution, first step: is there sequential structure in the per-frame series at the comet's coordinates,
beyond the series' own surrogates and beyond the same measures on their sidebands? Data: HM5's kept series (hm5_0013.npz,
hm5_0014.npz: frP, frD for the 95 comet windows, X and Y). No voltages are read."""
import json, os, sys, zlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); H5 = os.path.join(HERE, "../HM5")
NSUR_SH = 1000; NSUR_IA = 1000; LAGS = 50; XLAG = 20; NSYM = 4; SEED = 20261122
OUT = os.environ.get("HMR1_OUT", HERE)


def iaaft(x, rng, it=20):
    """Iterative amplitude-adjusted Fourier surrogate: keeps the power spectrum and the value distribution."""
    s = np.sort(x); A = np.abs(np.fft.rfft(x)); y = rng.permutation(x)
    for _ in range(it):
        Y = np.fft.rfft(y); y = np.fft.irfft(A * np.exp(1j * np.angle(Y)), n=len(x))
        y = s[np.argsort(np.argsort(y))]
    return y


def symb(x):  # four quantile symbols
    q = np.quantile(x, [0.25, 0.5, 0.75]); return bytes((np.searchsorted(q, x) + 65).astype(np.uint8))


def m1(x):  # Ljung-Box Q over lags 1..50
    x = x - x.mean(); n = len(x); d = np.dot(x, x)
    r = np.array([np.dot(x[:-k], x[k:]) / d for k in range(1, LAGS + 1)])
    return float(n * (n + 2) * np.sum(r ** 2 / (n - np.arange(1, LAGS + 1))))


def m2(x):  # compressed length of the symbol string (smaller = more structure)
    return len(zlib.compress(symb(x), 9))


def xmax(a, b):  # largest |cross-correlation| over lags -20..20, lag 0 included
    a = (a - a.mean()) / a.std(); b = (b - b.mean()) / b.std(); n = len(a)
    return float(max(abs(np.dot(a[max(0, -k):n - max(0, k)], b[max(0, k):n - max(0, -k)]) / (n - abs(k))) for k in range(-XLAG, XLAG + 1)))


def main(check=False):
    rng = np.random.default_rng(SEED)
    W = json.load(open(os.path.join(H5, "hm5_0013.json")))["windows"]
    Z = {s: np.load(os.path.join(H5, f"hm5_{s}.npz")) for s in ("0013", "0014")}
    ci = [int(i) for i in Z["0013"]["comet"]]; pos = {W[i][0]: j for j, i in enumerate(ci)}
    coords = [W[i][0] for i in ci if W[i][1] == "sel"]
    sbs = {c: [W[i][0] for i in ci if W[i][1] == "sb:" + c] for c in coords}
    names = [W[i][0] for i in ci]
    if check: names = names[:2]; coords = [c for c in coords if c in names]
    res = {}
    for s in ("0013", "0014"):
        for st, key in (("P", "frP"), ("D3", "frD")):
            for fi, fe in enumerate("XY"):
                for nm in names:
                    x = Z[s][key][fi][:, pos[nm]].astype(float)
                    sh1 = np.array([m1(rng.permutation(x)) for _ in range(NSUR_SH if not check else 10)])
                    ia2 = np.array([m2(iaaft(x, rng)) for _ in range(NSUR_IA if not check else 5)])
                    v1, v2 = m1(x), m2(x)
                    res[f"{s}|{st}|{fe}|{nm}"] = {"m1": v1, "m1_z": float((v1 - sh1.mean()) / sh1.std()), "m1_p": float((1 + np.sum(sh1 >= v1)) / (1 + len(sh1))),
                                                   "m2": v2, "m2_z": float((ia2.mean() - v2) / max(ia2.std(), 1e-9)), "m2_p": float((1 + np.sum(ia2 <= v2)) / (1 + len(ia2)))}
    # M4: lagged co-structure among C08-C11, against the same measure on sideband pairs (one sideband of each)
    G = ["C08", "C09", "C10", "C11"]; m4 = {}
    if not check:
        for s in ("0013", "0014"):
            for st, key in (("P", "frP"), ("D3", "frD")):
                for fi, fe in enumerate("XY"):
                    S = lambda nm: Z[s][key][fi][:, pos[nm]].astype(float)
                    gv = [xmax(S(a), S(b)) for i, a in enumerate(G) for b in G[i + 1:]]
                    sv = [xmax(S(sbs[a][k]), S(sbs[b][k])) for i, a in enumerate(G) for b in G[i + 1:] for k in range(min(len(sbs[a]), len(sbs[b])))]
                    m4[f"{s}|{st}|{fe}"] = {"G_pairs_max_xcorr": [round(v, 4) for v in gv], "G_mean": float(np.mean(gv)),
                                            "sideband_pairs_mean": float(np.mean(sv)), "sideband_pairs_p95": float(np.percentile(sv, 95)), "n_sideband_pairs": len(sv)}
    # scoring as frozen (PLAN-HMR1 §3)
    T = 3.3; out = {"seed": SEED, "per_series": res, "m4": m4, "coords": {}, "base_rate": {}}
    for s in ("0013", "0014"):
        for st in ("P", "D3"):
            for fe in "XY":
                hits_sb = {"m1": 0, "m2": 0}; nsb = 0
                for c in coords:
                    me = res[f"{s}|{st}|{fe}|{c}"]; sbv = [res[f"{s}|{st}|{fe}|{b}"] for b in sbs[c] if f"{s}|{st}|{fe}|{b}" in res]
                    rec = {}
                    for m in ("m1", "m2"):
                        z = me[m + "_z"]; above_all = all(z > b[m + "_z"] for b in sbv) if sbv else None
                        rec[m] = {"z": round(z, 3), "p": me[m + "_p"], "above_every_sideband": above_all, "passes": bool(z >= T and above_all)}
                    out["coords"][f"{s}|{st}|{fe}|{c}"] = rec
                    for b in sbv:
                        nsb += 1
                        for m in ("m1", "m2"): hits_sb[m] += int(b[m + "_z"] >= T)
                out["base_rate"][f"{s}|{st}|{fe}"] = {"sidebands": nsb, "m1_at_or_over_T": hits_sb["m1"], "m2_at_or_over_T": hits_sb["m2"]}
    json.dump(out, open(os.path.join(OUT, "hmr1_score.json"), "w"), indent=1)
    if check: print("check ok", len(res)); return
    for k, v in out["coords"].items():
        if v["m1"]["passes"] or v["m2"]["passes"]: print("PASS", k, v)
    print("base rates", json.dumps(out["base_rate"]))
    for k, v in m4.items(): print("M4", k, round(v["G_mean"], 4), "sb mean", round(v["sideband_pairs_mean"], 4), "sb p95", round(v["sideband_pairs_p95"], 4))
    for s in ("0013",):
        for st in ("P", "D3"):
            print(s, st, "X", {c: (out["coords"][f"{s}|{st}|X|{c}"]["m1"]["z"], out["coords"][f"{s}|{st}|X|{c}"]["m2"]["z"]) for c in coords})


if __name__ == "__main__":
    main(check=len(sys.argv) > 1 and sys.argv[1] == "check")
