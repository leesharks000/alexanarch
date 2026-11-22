"""PLAN-HM11: the conditions as characters.   python3 hm11.py check | score
Re-reads the kept cohort products (HM6 for 0013/0014, HM8 for 0015-0018; all 380 cohorts, 11 coordinates, sidebands) and
projects each cohort's ranks onto the eight characters of the three binary conditions: scan (ON +1 / OFF -1), feed (X +1 /
Y -1), track (comet drift c +1 / mirrored f -1). Each account of the excess predicts its own character."""
import itertools, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {"0013": "../HM6", "0014": "../HM6", "0015": "../HM8", "0016": "../HM8", "0017": "../HM8", "0018": "../HM8"}
PAIRS = [("0013", "0014"), ("0015", "0016"), ("0017", "0018")]; MINSB = 6; VI = {"c": 0, "d": 1, "f": 2}
CHARS = ["", "s", "p", "t", "sp", "st", "pt", "spt"]


def load():
    R, WIN = {}, None
    for s, d in SRC.items():
        R[s] = np.load(os.path.join(HERE, d, f"hm6_{s}.npz")); w = json.load(open(os.path.join(HERE, d, f"hm6_{s}.json")))["windows"]
        WIN = WIN or w; assert w == WIN, s
    return R, WIN


def setup(WIN):
    idx = {w[0]: i for i, w in enumerate(WIN)}; sb = {}
    for nme, k, f, dv, co in WIN:
        if k.startswith("sb:"): sb.setdefault(k[3:], []).append(nme)
    sel = [(nme, co) for nme, k, f, dv, co in WIN if k == "sel" and len(sb.get(nme, [])) >= MINSB]
    sbi = {nme: np.array([idx[m] for m in sb[nme]]) for nme, co in sel}; ii = {nme: idx[nme] for nme, co in sel}
    return sel, sbi, ii


def ranks(v, sel, sbi, ii):
    return np.array([(np.sum(v[sbi[n]] < v[ii[n]]) + 0.5 * np.sum(v[sbi[n]] == v[ii[n]])) / len(sbi[n]) for n, co in sel])


def chi(c, s, p, t): return (s if "s" in c else 1) * (p if "p" in c else 1) * (t if "t" in c else 1)


def cohort_scores(per_coord, cohorts):
    """per_coord: (n_sel,) values -> {cohort: mean * sqrt(n)} as HM6/HM8."""
    out = {}
    for co in set(cohorts):
        v = per_coord[np.array([c == co for c in cohorts])]; out[co] = float(v.mean() * np.sqrt(len(v)))
    return out


def read(R, WIN, st):
    sel, sbi, ii = setup(WIN); cohorts = [co for n, co in sel]
    Q = {(s, fe, tr): ranks(R[s][st][VI[tr], fi], sel, sbi, ii) - 0.5 for s in SRC for fi, fe in enumerate("XY") for tr in "cdf"}
    per_pair = {}
    for on, off in PAIRS:
        coef = {}
        for c in CHARS:
            acc = 0
            for (sc, sg), (fe, pg), (tr, tg) in itertools.product(((on, 1), (off, -1)), (("X", 1), ("Y", -1)), (("c", 1), ("f", -1))):
                acc = acc + chi(c, sg, pg, tg) * Q[(sc, fe, tr)]
            coef[c or "mean"] = acc / 8
        # the dish-fixed contrast, outside the cube: (ON - OFF) of d minus the mean of c and f, feeds averaged
        dd = sum((Q[(on, fe, "d")] - Q[(off, fe, "d")]) - 0.5 * ((Q[(on, fe, "c")] - Q[(off, fe, "c")]) + (Q[(on, fe, "f")] - Q[(off, fe, "f")])) for fe in "XY") / 2
        coef["dish_minus_drift"] = dd
        per_pair[f"{on}/{off}"] = {k: cohort_scores(v, cohorts) for k, v in coef.items()}
    return per_pair, sel


def summarise(per_pair, sel):
    tn = [n for n, co in sel if co == "true"]; out = {}
    keys = list(next(iter(per_pair.values())).keys())
    for k in keys:
        row = {}
        pooled = None
        for p, d in per_pair.items():
            T = d[k]["true"]; Fs = np.array([v for co, v in d[k].items() if co != "true"])
            row[p] = {"true": round(T, 4), "rank": int(1 + np.sum(Fs > T)), "rank_low": int(1 + np.sum(Fs < T)), "false_mean": round(float(Fs.mean()), 4), "n": 1 + len(Fs)}
            cohs = sorted(d[k]); vec = np.array([d[k][c] for c in cohs]); pooled = vec if pooled is None else pooled + vec
        pooled = pooled / np.sqrt(len(per_pair)); cohs = sorted(next(iter(per_pair.values()))[k]); T = pooled[cohs.index("true")]; Fs = np.delete(pooled, cohs.index("true"))
        row["pooled"] = {"true": round(float(T), 4), "rank": int(1 + np.sum(Fs > T)), "rank_low": int(1 + np.sum(Fs < T)), "false_mean": round(float(Fs.mean()), 4), "n": len(pooled)}
        out[k] = row
    return out


def main(mode):
    R, WIN = load(); res = {"plan": "PLAN-HM11.md"}
    # reproduction: HM8's cohort score for 0013/0014, power, X, track c = the ON - OFF of q on that cell (an existing number)
    sel, sbi, ii = setup(WIN); cohorts = [co for n, co in sel]
    q = ranks(R["0013"]["P"][0, 0], sel, sbi, ii) - ranks(R["0014"]["P"][0, 0], sel, sbi, ii)
    rep = cohort_scores(q, cohorts)["true"]; ref = json.load(open(os.path.join(HERE, "../HM8/hm8_score.json")))["A"]["0013/0014"]["P_X"]["c"]["true"]
    res["reproduction"] = {"hm11": round(rep, 4), "hm8": ref, "ok": abs(rep - ref) < 1e-3}; print("reproduction", res["reproduction"], flush=True)
    if mode == "check": return
    assert res["reproduction"]["ok"]
    for st in ("P", "D3"):
        pp, sel = read(R, WIN, st); res[st] = summarise(pp, sel)
        print(st, {k: (v["pooled"]["true"], v["pooled"]["rank"], v["pooled"]["rank_low"]) for k, v in res[st].items()}, flush=True)
    json.dump(res, open(os.path.join(HERE, "hm11_score.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
