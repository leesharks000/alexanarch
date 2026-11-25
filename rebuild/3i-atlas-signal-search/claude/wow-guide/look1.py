"""First look under the Wow-as-guide hypothesis (2026-11-24, 22:13 EST): if the Wow! was sent by 3I/ATLAS at a frequency fixed in its
own frame, that frequency is the Wow's received frequency taken back through the object's 1977 range-rate from Big Ear (-43.011 km/s
on the present orbit): F0 = 1420.726 / (1 + 43.011/c) = 1420.5222 MHz (revised), 1420.4556 -> 1420.2519 MHz (Ehman).
Reads blc24 rawspec .0000 (2.79 Hz x 6.08 s), scans 0013-0018, de-Dopplered to the comet frame, +-6 kHz around each F0.
Not a frozen test: a look. Lists what is there: lines steady in the comet frame, single-step bursts, per scan. Writes look1.json/.npz.
    python3 look1.py"""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "../wow3"))
import r2_r6_lines_a1 as m
C = m.C; V77 = -43.0112691
F0 = {"revised": 1420.726 / (1 - V77 / C), "ehman": 1420.4556 / (1 - V77 / C)}
ROLE = {"0013": "ON", "0014": "OFF", "0015": "ON", "0016": "OFF", "0017": "ON", "0018": "OFF"}
data = {sc: m.load("blc24", sc, 1420.6) for sc in m.SCANS}
out = {"F0_MHz": F0, "v1977_kms": V77, "targets": {}}; keep = {}
for name, f0 in F0.items():
    T = {"f_topo_2025_MHz": None, "scans": {}}
    for sc, (_, x, fq, t) in data.items():
        foff = fq[1] - fq[0]; nw = int(round(6e-3 / abs(foff)))
        W = np.empty((x.shape[0], 2 * nw + 1), np.float32)
        for k in range(x.shape[0]):
            c = int(round((f0 * (1 - m.VCOM(t[k]) / C) - fq[0]) / foff)); W[k] = x[k, c - nw:c + nw + 1]
        if T["f_topo_2025_MHz"] is None: T["f_topo_2025_MHz"] = float(f0 * (1 - m.VCOM(t[0]) / C))
        W = W / np.median(W, 1, keepdims=True)                         # each time step by its own level
        base = np.median(W, 0)                                         # the band's shape in this scan
        from scipy.ndimage import median_filter
        shape = median_filter(base, 201, mode="nearest"); R = W / shape - 1
        sig = 1.4826 * np.median(np.abs(R - np.median(R)))
        Z = R / sig; line = Z.mean(0) * np.sqrt(Z.shape[0])            # steady in the comet frame
        off_hz = (np.arange(2 * nw + 1) - nw) * abs(foff) * 1e6
        top = np.argsort(line)[-5:][::-1]; pix = np.argwhere(Z >= 5)
        T["scans"][sc] = {"role": ROLE[sc], "line_max_z": float(line.max()), "line_top5": [(float(off_hz[i]), float(line[i])) for i in top],
                          "pixels_ge5": int(len(pix)), "pixels_expected_gauss": float(Z.size * 2.87e-7), "pix_max_z": float(Z.max()),
                          "pix_top5": [(int(a), float(off_hz[b]), float(Z[a, b])) for a, b in pix[np.argsort(Z[pix[:, 0], pix[:, 1]])[-5:][::-1]]] if len(pix) else [],
                          "noise_sigma_frac": float(sig)}
        keep[f"{name}_{sc}"] = Z.astype(np.float16)
        print(name, sc, ROLE[sc], "line max z %.1f" % line.max(), "pixels>=5: %d (max %.1f)" % (len(pix), Z.max()), flush=True)
    out["targets"][name] = T
json.dump(out, open(os.path.join(HERE, "look1.json"), "w"), indent=1); np.savez_compressed(os.path.join(HERE, "look1.npz"), **keep)
print(json.dumps({k: (v["f_topo_2025_MHz"]) for k, v in out["targets"].items()}), F0)
