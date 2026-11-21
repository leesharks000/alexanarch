"""EA-3I-HAILMARY-01 executed: python3 hm.py select SCRATCHDIR | SCAN | score"""
import json, os, sys, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(HERE, "../FD"))


def select(scr):
    CODE = os.path.join(HERE, "../../../../../oh13/code")
    CAT = json.load(open(os.path.join(CODE, "../oh13_candidates.json")))["candidates"]
    os.chdir(scr); sys.argv = ["x", "raw/OH", "2.5", "2.0"]
    spec = importlib.util.spec_from_file_location("cf", os.path.join(CODE, "cometframe_raw.py")); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
    def merge(rows, tol=10.0):
        cl = []
        for r in sorted(rows, key=lambda r: r["f_rest_MHz"]):
            if cl and (r["f_rest_MHz"] - cl[-1][-1]["f_rest_MHz"]) * 1e6 <= tol: cl[-1].append(r)
            else: cl.append([r])
        return [{"f_rest_Hz": float(np.mean([r["f_rest_MHz"] for r in c])) * 1e6, "rows": len(c),
                 "z_on": [max(r[f"z_{s}"] for r in c) for s in cf.ON], "z_off": [max(r[f"z_{s}"] for r in c) for s in cf.OFF]} for c in cl]
    true = merge(cf.coincidences(0.0, keep=True))
    grid = [float(d) for d in np.round(np.arange(-0.2, 0.2001, 0.01), 3) if abs(d) > 1e-9]
    frames = [{"k": k, "d_Hz_per_s": d, "dv": d * cf.C / 1.667e9, "selections": merge(cf.coincidences(d * cf.C / 1.667e9, keep=True))} for k, d in enumerate(grid)]
    out = {"T0_mjd": float(cf.T0), "true_frame": true, "false_frames": frames, "counts": [len(f["selections"]) for f in frames],
           "check_true_matches_catalogue": sorted(round(c["f_rest_Hz"]) for c in true) == sorted(round(c["f_rest_Hz"]) for c in CAT)}
    json.dump(out, open(os.path.join(HERE, "hm_selections.json"), "w"), indent=1)
    print("true", len(true), "catalogue", out["check_true_matches_catalogue"], "| false cohorts", out["counts"], "total", sum(out["counts"]))


def hm_windows():
    from common import windows, vel_fn, t0, LINES, EDGE, OFFS, W, DF, C
    S = json.load(open(os.path.join(HERE, "hm_selections.json")))
    r = 1 - vel_fn()(t0("0015") + 150 / 86400.0) / C; LR = [L / r for L in LINES]; ER = (EDGE[0] / r, EDGE[1] / r); half = W / 2 * DF
    near = lambda g: any(abs(L - g) < half + 1.5e3 for L in LR) or g - half < ER[0] or g + half > ER[1]
    cohorts = [("true", 0.0, [f for n, k, f, p in windows() if k == "cand"], [n for n, k, f, p in windows() if k == "cand"])]
    for fr in S["false_frames"]:
        sels = [x["f_rest_Hz"] for x in fr["selections"]]
        cohorts.append((f"F{fr['k']:02d}", fr["dv"], sels, [f"F{fr['k']:02d}s{i}" for i in range(len(sels))]))
    out = []
    for cname, dv, fs, names in cohorts:
        taken = [(f - half, f + half) for f in fs]
        for f, nm in zip(fs, names):
            if cname != "true" and near(f):
                out.append((nm, "ref", f, dv, cname)); continue
            out.append((nm, "sel", f, dv, cname)); n = 0
            for o in OFFS:
                if n == 8: break
                g = f + o; lo, hi = g - half, g + half
                if near(g) or any(not (hi < a or lo > b) for a, b in taken): continue
                out.append((f"{nm}{'+' if o > 0 else '-'}{abs(o) / 1e3:.1f}k", "sb:" + nm, g, dv, cname)); taken.append((lo, hi)); n += 1
    return out


def scan(s):
    import fdstream as F
    F.fd_windows = lambda: [(n, k, f, dv, c) for n, k, f, dv, c in hm_windows()]
    F.HERE = HERE
    T0 = json.load(open(os.path.join(HERE, "hm_selections.json")))["T0_mjd"]
    json.dump({"T0_mjd": T0, "false_frames": []}, open(os.path.join(HERE, "fd_selections.json"), "w"))   # fdstream.scan reads T0 from here
    F.scan(s); os.replace(os.path.join(HERE, f"fd_{s}.json"), os.path.join(HERE, f"hm_{s}.json"))


def score():
    from common import SCANS, ON
    R = {s: json.load(open(os.path.join(HERE, f"hm_{s}.json")))["D3"] for s in SCANS}; WIN = hm_windows(); st = "d2|X"
    sb = {}
    for n, k, f, dv, c in WIN:
        if k.startswith("sb:"): sb.setdefault(k[3:], []).append(n)
    coh = {}
    for n, k, f, dv, c in WIN:
        if k != "sel": continue
        rk = {}
        for s in SCANS:
            x = R[s][n][st]; v = np.array([R[s][m][st] for m in sb.get(n, [])])
            rk[s] = (np.sum(v < x) + 0.5 * np.sum(v == x)) / len(v) if len(v) else np.nan
        con = np.mean([rk[s] for s in ON]) - np.mean([rk[s] for s in SCANS if s not in ON])
        coh.setdefault(c, []).append({"name": n, "n_sidebands": len(sb.get(n, [])), "rank": rk, "contrast": float(con)})
    res = {c: {"n": len(v), "mean_contrast": float(np.mean([x["contrast"] for x in v])), "score": float(np.mean([x["contrast"] for x in v]) * np.sqrt(len(v))), "members": v}
           for c, v in coh.items()}
    T = res["true"]["score"]; F_ = [v["score"] for c, v in res.items() if c != "true"]
    p = (1 + sum(1 for x in F_ if x >= T)) / (1 + len(F_))
    out = {"statistic": st, "true": {k: res["true"][k] for k in ("n", "mean_contrast", "score")}, "n_false_nonempty": len(F_),
           "false_at_or_above_true": sorted([(c, round(v["score"], 3)) for c, v in res.items() if c != "true" and v["score"] >= T], key=lambda x: -x[1]),
           "p": p, "floor": 1 / (1 + len(F_)), "cohorts": res}
    json.dump(out, open(os.path.join(HERE, "hm_score.json"), "w"), indent=1)
    print("true cohort: n", res["true"]["n"], "mean contrast", round(res["true"]["mean_contrast"], 4), "score", round(T, 3))
    print("false cohorts non-empty:", len(F_), "| at or above true:", out["false_at_or_above_true"])
    print("p =", round(p, 4), "(floor", round(out["floor"], 4), ")")
    for m in res["true"]["members"]: print("  ", m["name"], m["n_sidebands"], round(m["contrast"], 3), {s: round(v, 2) for s, v in m["rank"].items()})


if __name__ == "__main__":
    a = sys.argv[1]
    select(sys.argv[2]) if a == "select" else score() if a == "score" else scan(a)
