"""PLAN-r13 parts F (aggregate rank across channels, stored rows only) and G (twin independence).
    python3 fg.py F   -> F.json      python3 fg.py G -> G.json"""
import os, sys, json
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def ranks(rows, rng):
    T = rows[0]["on"]; o = np.array([r["on"] for r in rows[1:]])
    gt = int((o > T).sum()); eq = int((o == T).sum())
    return 1 + gt + int(rng.integers(0, eq + 1))  # 1 = top of 41; ties broken at random
def ks_u(r):  # discrete ranks to uniform u in (0,1]: u = rank/41
    from scipy.stats import kstest
    u = (np.array(r) - np.random.default_rng(6).uniform(0, 1, len(r))) / 41.0
    return float(kstest(u, "uniform").pvalue)
if sys.argv[1] == "F":
    from scipy.stats import binom
    rng = np.random.default_rng(5)
    L = json.load(open("../lee/lee.json"))["channels"]; LH = json.load(open("../lheld/lheld.json"))["channels"]
    O = json.load(open("../ocad/ocad.json"))["channels"]
    rowsL = {k: (v["rows"] if v.get("rows") else LH[k]["rows"]) for k, v in L.items()}
    out = {}
    for name, R in (("L_all64", rowsL), ("L_without_thirteen", {k: v for k, v in rowsL.items() if k != "blc23_cc07"}),
                    ("SCX", {k: v["rows"] for k, v in O.items()}),
                    ("S", {k: v["rows"] for k, v in O.items() if k[0] == "S"}), ("C", {k: v["rows"] for k, v in O.items() if k[0] == "C"}),
                    ("X", {k: v["rows"] for k, v in O.items() if k[0] == "X"})):
        r = [ranks(v, rng) for v in R.values()]; n = len(r); top = sum(x <= 4 for x in r)
        out[name] = {"n": n, "mean_rank": float(np.mean(r)), "expected_mean": 21.0, "top4_of_41": top, "expected_top4": n * 4 / 41,
                     "p_top4_ge": float(binom.sf(top - 1, n, 4 / 41)), "ks_p_uniform": ks_u(r), "ranks": dict(zip(R, r))}
    allr = list(out["L_without_thirteen"]["ranks"].values()) + list(out["SCX"]["ranks"].values())
    out["combined_without_thirteen"] = {"n": len(allr), "mean_rank": float(np.mean(allr)), "top4_of_41": sum(x <= 4 for x in allr),
                                        "expected_top4": len(allr) * 4 / 41, "p_top4_ge": float(binom.sf(sum(x <= 4 for x in allr) - 1, len(allr), 4 / 41)), "ks_p_uniform": ks_u(allr)}
    out["thirteen_channel_rank"] = out["L_all64"]["ranks"].get("blc23_cc07")
    json.dump(out, open("F.json", "w"), indent=0)
    for k, v in out.items():
        if isinstance(v, dict): print(k, {a: b for a, b in v.items() if a != "ranks"})
        else: print(k, v)
if sys.argv[1] == "G":
    import fsspec, h5py, hdf5plugin
    B = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
    HD = json.load(open("../ocad/headers.json")); TW = json.load(open("../ocad/order.json"))["twins"]
    FILES = {(v["node"], v["scan"]): k for k, v in HD.items()}
    FIRST = {"C": "0045", "X": "0061"}
    def sl(nd, s, cc=10, lo=300000, n=65536):
        d = h5py.File(fsspec.open(B + FILES[(nd, s)], "rb", block_size=4 << 20).open(), "r")["data"]
        a = d.attrs; nf = int(a["nfpc"]); return d[:, 0, cc * nf + lo: cc * nf + lo + n].astype(np.float64), {k: (a[k].decode() if isinstance(a[k], bytes) else (a[k].tolist() if hasattr(a[k], "tolist") else a[k])) for k in a}
    out = {}
    for k, tw in TW.items():
        cad, nd = k.split("_"); s = FIRST[cad]
        x, ax = sl(nd, s); y, ay = sl(tw, s)
        rx = x / np.median(x, 0) - 1; ry = y / np.median(y, 0) - 1
        diff_attrs = {a: (ax.get(a), ay.get(a)) for a in sorted(set(ax) | set(ay)) if ax.get(a) != ay.get(a)}
        out[k] = {"twin": tw, "scan": s, "identical": bool(np.array_equal(x, y)), "corr_rel_noise": float(np.corrcoef(rx.ravel(), ry.ravel())[0, 1]),
                  "corr_row_means": float(np.corrcoef(x.mean(1), y.mean(1))[0, 1]), "ratio_median": float(np.median(x) / np.median(y)), "attrs_differing": diff_attrs}
        print(k, tw, out[k]["identical"], round(out[k]["corr_rel_noise"], 4), round(out[k]["ratio_median"], 3), list(diff_attrs)[:8], flush=True)
    json.dump(out, open("G.json", "w"), indent=0, default=str)
