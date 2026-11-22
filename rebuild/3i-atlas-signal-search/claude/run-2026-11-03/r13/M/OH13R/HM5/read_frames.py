"""READ-HM5-frames: the per-frame series HM5 kept (hm5_0013.npz, hm5_0014.npz), read for the shape at C08–C11.
Path 3 of 2026-11-22 (the author, 10:42: "lets begin working through tests 1-4"). Descriptive: no new computation on the
voltages, no test, no threshold. C08–C11 were named from X, so nothing here is evidence that they are special.
For each comet coordinate and feed: power per frame (centre bin over the mean of 129 bins, as HM4 §D), the coordinate's
rank among its own sidebands frame by frame, in ON 0013 and OFF 0014."""
import json, os
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(H, "hm5_0013.json")))["windows"]
Z = {s: np.load(os.path.join(H, f"hm5_{s}.npz")) for s in ("0013", "0014")}
ci = [int(i) for i in Z["0013"]["comet"]]; pos = {W[i][0]: j for j, i in enumerate(ci)}
coords = [W[i][0] for i in ci if W[i][1] == "sel"]
sbs = {c: [pos[W[i][0]] for i in ci if W[i][1] == "sb:" + c] for c in coords}
FE = ["X", "Y"]; NB = 26; BIN = 32
def binmean(a):  # 26 bins of 32 frames, the last taking frames 800–832, as HM5
    return np.array([a[b * BIN:(b + 1) * BIN if b < NB - 1 else len(a)].mean(axis=0) for b in range(NB)])
out = {"note": __doc__, "coords": {}}
for c in coords:
    j = pos[c]; sb = sbs[c]; out["coords"][c] = {"f_rest_MHz": round(W[ci[j]][2] / 1e6, 6), "n_sidebands": len(sb)}
    for fi, fe in enumerate(FE):
        r = {}
        for s in ("0013", "0014"):
            P = Z[s]["frP"][fi].astype(float)  # (833, 95)
            me, sbv = P[:, j], P[:, sb]
            rank = (np.sum(sbv < me[:, None], 1) + 0.5 * np.sum(sbv == me[:, None], 1)) / len(sb)  # per frame
            Pb = binmean(P); rb = (np.sum(Pb[:, sb] < Pb[:, [j]], 1) + 0.5 * np.sum(Pb[:, sb] == Pb[:, [j]], 1)) / len(sb)
            ex = me / sbv.mean(1)  # the coordinate's power over its sidebands' mean, per frame
            top = rank >= 1.0  # frames where it stands above every sideband
            e = np.flatnonzero(np.diff(np.r_[0, top.astype(int), 0])); runs = e[1::2] - e[0::2]
            r[s] = {"mean_power_ratio_to_sidebands": round(float(ex.mean()), 4), "median_ratio": round(float(np.median(ex)), 4),
                    "frames_above_every_sideband": int(top.sum()), "frames_below_every_sideband": int((rank <= 0).sum()),
                    "expected_each_by_chance": round(len(me) / (len(sb) + 1), 1), "longest_run_above_all": int(runs.max()) if len(runs) else 0,
                    "rank_per_bin": [round(float(x), 2) for x in rb],
                    "ratio_first_half": round(float(ex[:416].mean()), 4), "ratio_second_half": round(float(ex[416:].mean()), 4),
                    "max_frame_ratio": round(float(ex.max()), 3), "argmax_frame": int(ex.argmax())}
        out["coords"][c][fe] = r
# co-variation: do C08–C11 rise together frame by frame in X ON? (correlation of their per-frame excess over sidebands)
G = ["C08", "C09", "C10", "C11"]
for s in ("0013", "0014"):
    for fi, fe in enumerate(FE):
        P = Z[s]["frP"][fi].astype(float)
        E = np.array([P[:, pos[c]] / P[:, sbs[c]].mean(1) for c in G])
        cc = np.corrcoef(E); off = cc[np.triu_indices(4, 1)]
        # the same for four other coordinates, as a comparison
        O = np.array([P[:, pos[c]] / P[:, sbs[c]].mean(1) for c in ["C03", "C05", "C12", "C13"]])
        oo = np.corrcoef(O)[np.triu_indices(4, 1)]
        out.setdefault("covariation", {})[f"{s}_{fe}"] = {"C08-C11 pairwise r": [round(float(x), 3) for x in off], "mean": round(float(off.mean()), 3),
                                                          "C03,C05,C12,C13 pairwise r mean": round(float(oo.mean()), 3)}
json.dump(out, open(os.path.join(H, "READ-HM5-frames.json"), "w"), indent=1, ensure_ascii=False)
for c in coords:
    for fe in FE:
        a, b = out["coords"][c][fe]["0013"], out["coords"][c][fe]["0014"]
        print(c, fe, "ON ratio", a["mean_power_ratio_to_sidebands"], "top", a["frames_above_every_sideband"], "run", a["longest_run_above_all"], "| OFF ratio", b["mean_power_ratio_to_sidebands"], "top", b["frames_above_every_sideband"], "| exp", a["expected_each_by_chance"], "| ON halves", a["ratio_first_half"], a["ratio_second_half"])
print(json.dumps(out["covariation"], indent=0))
for c in G: print(c, "X ON per-bin rank", out["coords"][c]["X"]["0013"]["rank_per_bin"]); print(c, "X OFF per-bin rank", out["coords"][c]["X"]["0014"]["rank_per_bin"])
