"""PLAN-SYMBOLON K3 (the Wow's offsets from the hydrogen line, mirrored below it, in 3I/ATLAS's frame; and its number mirrored
about the line, topocentric) and K4 (the halves joined: the smaller of the ON/OFF contrasts at H+d and H-d). blc24 .0000, the coarse
channel holding 1420.4-1420.8 MHz, scans 0013-0018, streamed, as wow_s2.py. Controls: the same 200 random targets as wow_s2.py
(same seed, same exclusions); for K4, 200 symmetric pairs c +/- d around random centres. Writes k34.json, k34_windows.npz.
    python3 symb_k34.py"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../wow")); import wow_s2 as w   # load(), tracked_band(), SCANS, PAIRS, H, HALF
H = w.H


def main():
    data = {}
    for sc in w.SCANS:
        t0 = time.time(); data[sc] = w.load(sc); print(sc, data[sc][1].shape, "%.0fs" % (time.time() - t0), flush=True)
    freqs = data["0013"][2]; fmin, fmax = min(freqs[0], freqs[-1]) + 0.1, max(freqs[0], freqs[-1]) - 0.1
    # the wow_s2 controls, regenerated exactly
    rng = np.random.default_rng(14204058)
    T_old = {"T1": 1420.726, "T2": H, "T3": H + 0.320, "T4": H + 0.0498}
    ctrl = []
    while len(ctrl) < 200:
        f = rng.uniform(fmin, fmax)
        if abs(f - H) > 0.05 and all(abs(f - v) > 0.05 for v in T_old.values()):
            ctrl.append(f)
    T = {"T5_H-320k_comet": (H - 0.320, "comet"), "T6_H-49.8k_comet": (H - 0.0498, "comet"),
         "T7_1420.0855_topo": (2 * H - 1420.726, "topo"),
         "T3_H+320k_comet": (H + 0.320, "comet"), "T4_H+49.8k_comet": (H + 0.0498, "comet")}   # the first halves, re-read for K4
    targets = dict(T); targets.update({f"ctrl_{i:03d}": (f, "comet") for i, f in enumerate(ctrl)})

    def read(f, fr, keep=False):
        P = {}; A = {}
        for sc, (_, x, fq, t) in data.items():
            P[sc], A[sc] = w.tracked_band(x, fq, t, f, fr)
        c = [P[on] / P[off] - 1 for on, off in w.PAIRS]
        r = {"f_MHz": f, "frame": fr, "band_power": P, "on_off_contrast": c, "mean_contrast": float(np.mean(c))}
        if keep:
            pk = {}
            fq = data["0013"][2]; nb = int(round(w.HALF / abs(fq[1] - fq[0])))
            for sc in w.SCANS:
                a = A[sc]; base = np.concatenate([a[:len(a) // 3], a[-len(a) // 3:]])
                med = np.median(base); mad = np.median(np.abs(base - med)) * 1.4826
                mid = len(a) // 2; seg = (a[mid - nb:mid + nb + 1] - med) / mad
                pk[sc] = {"peak_z": float(seg.max()), "trough_z": float(seg.min()),
                          "offset_Hz": float((seg.argmax() - nb) * abs(fq[1] - fq[0]) * 1e6)}
            r["peak_in_band"] = pk
        return r, A

    res = {}; wins = {}
    for k, (f, fr) in targets.items():
        r, A = read(f, fr, keep=not k.startswith("ctrl"))
        res[k] = r
        if not k.startswith("ctrl"):
            wins.update({f"{k}_{sc}": A[sc].astype(np.float32) for sc in w.SCANS})
    cm = np.array([res[k]["mean_contrast"] for k in res if k.startswith("ctrl")])
    for k in T:
        res[k]["rank_vs_controls"] = float((cm < res[k]["mean_contrast"]).mean())
    # K4: the halves joined
    rng4 = np.random.default_rng(14204059); K4 = {}
    for name, d in (("320k", 0.320), ("49.8k", 0.0498)):
        up, dn = res[f"T3_H+320k_comet" if name == "320k" else "T4_H+49.8k_comet"], res[f"T5_H-320k_comet" if name == "320k" else "T6_H-49.8k_comet"]
        joint = min(up["mean_contrast"], dn["mean_contrast"])
        cj = []
        while len(cj) < 200:
            c = rng4.uniform(fmin + d, fmax - d)
            if abs(c - H) > 0.05 and all(abs(c - v[0]) > 0.05 for v in T.values()):
                a, _ = read(c + d, "comet"); b, _ = read(c - d, "comet")
                cj.append(min(a["mean_contrast"], b["mean_contrast"]))
        cj = np.array(cj)
        K4[name] = {"joint_min_contrast": joint, "up": up["mean_contrast"], "down": dn["mean_contrast"],
                    "per_pair_min": [min(a, b) for a, b in zip(up["on_off_contrast"], dn["on_off_contrast"])],
                    "rank_vs_symmetric_controls": float((cj < joint).mean()), "control_median": float(np.median(cj)),
                    "control_range": [float(cj.min()), float(cj.max())]}
        print("K4", name, K4[name], flush=True)
    json.dump({"files": {sc: data[sc][0] for sc in data}, "coarse_channel_MHz": [float(freqs.min()), float(freqs.max())],
               "control_contrast": {"mean": float(cm.mean()), "min": float(cm.min()), "max": float(cm.max())},
               "targets": res, "K4": K4}, open(os.path.join(HERE, "k34.json"), "w"), indent=1)
    np.savez_compressed(os.path.join(HERE, "k34_windows.npz"), **wins)
    for k in T:
        print(k, "mean ON/OFF-1 %.4f" % res[k]["mean_contrast"], "rank %.3f" % res[k]["rank_vs_controls"],
              {sc: (round(v["peak_z"], 1), round(v["trough_z"], 1)) for sc, v in res[k]["peak_in_band"].items()}, flush=True)


if __name__ == "__main__":
    main()
