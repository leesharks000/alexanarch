"""PLAN-HM12: the unexamined branches, batch A (kept products only).   python3 hm12.py
A1 HM11's track effect, by scan role, feed and coordinate; A2 the size of the D3 excess against selection;
A3 C10's phase concentration on the hold-out. A4-A6 are readings of kept files, written in RESULTS-HM12.md."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../HM11"))
import hm11 as H
out = {"plan": "PLAN-HM12.md"}

# A1 -------------------------------------------------------------------------------------------------------------
R, WIN = H.load(); sel, sbi, ii = H.setup(WIN); coh = [co for n, co in sel]; names = [n for n, co in sel]
tn = [i for i, co in enumerate(coh) if co == "true"]
A1 = {}
for st in ("P", "D3"):
    for fi, fe in enumerate("XY"):
        for s in H.SRC:
            q = {tr: H.ranks(R[s][st][H.VI[tr], fi], sel, sbi, ii) - 0.5 for tr in "cdf"}
            t = q["c"] - q["f"]; sc = H.cohort_scores(t, coh); T = sc["true"]; Fs = np.array([v for c, v in sc.items() if c != "true"])
            A1[f"{st}|{fe}|{s}"] = {"role": "ON" if s in ("0013", "0015", "0017") else "OFF", "true": round(T, 4),
                                    "rank": int(1 + np.sum(Fs > T)), "false_mean": round(float(Fs.mean()), 4),
                                    "per_coordinate": {names[i]: round(float(t[i]), 4) for i in tn}}
out["A1_track_c_minus_f"] = A1
pw = A1  # rule (PLAN §A1): the effect belongs to the coordinates' frequencies if the OFF-only rank is <= 19 in at least two OFF scans
offr = {fe: [A1[f"P|{fe}|{s}"]["rank"] for s in ("0014", "0016", "0018")] for fe in "XY"}
out["A1_rule"] = {fe: {"off_ranks": offr[fe], "frequencies_not_beam": sum(r <= 19 for r in offr[fe]) >= 2} for fe in "XY"}

# A2 -------------------------------------------------------------------------------------------------------------
fd = json.load(open(os.path.join(HERE, "../FD/fd_reading.json")))["d2|X"]
T = fd["true"]["mean_delta_sel"]; per = np.array([v for v in fd["false"]["per_frame_mean"].values() if v is not None], float)
out["A2_size"] = {"true_mean_delta": T, "false_frame_means_n": int(len(per)), "false_max": float(per.max()), "false_mean": float(per.mean()),
                  "rank": int(1 + np.sum(per > T)), "p": float((1 + np.sum(per >= T)) / (1 + len(per))), "exceeds_all": bool(T > per.max())}

# A3 -------------------------------------------------------------------------------------------------------------
S = json.load(open(os.path.join(HERE, "../HMR2/hmr2_score.json")))["R1"]
A3 = {}
for s in ("0013", "0015", "0017", "0014", "0016", "0018"):
    for fe in "XY":
        k = f"{s}|{fe}|C10"; sb = [v for kk, v in S.items() if kk.startswith(f"{s}|{fe}|C10") and kk != k]
        A3[k] = {"R": S[k]["R"], "p": S[k]["p"], "sb_max_R": max(x["R"] for x in sb), "above_all_sb": bool(S[k]["R"] > max(x["R"] for x in sb))}
out["A3_C10"] = A3
out["A3_rule"] = {s: bool(A3[f"{s}|X|C10"]["p"] < 1e-4 and A3[f"{s}|X|C10"]["above_all_sb"]) for s in ("0015", "0017")}
json.dump(out, open(os.path.join(HERE, "hm12.json"), "w"), indent=1)
print(json.dumps({k: out[k] for k in ("A1_rule", "A2_size", "A3_rule")}, indent=1))
