"""contrast_null.py — ON minus OFF, along the comet-frame path, for each candidate (offset 0, bins -1..+1) against the
same statistic on parallel paths at offsets |k| = 8..30 bins inside the same windows (same drift, same scans).
Statistic per scan: sum over spectra of the 3-bin path mean of I/baseline - 1, scaled by the scan's std of that sum
across offsets. Contrast = sum(ON) - sum(OFF)."""
import numpy as np, json, pathlib
H = pathlib.Path(__file__).resolve().parent / "out"
ON, OFF = ["0013", "0015", "0017"], ["0014", "0016", "0018"]
per = {}
for s in ON + OFF:
    z = np.load(H / f"cand_scan{s}_ch7_n19.npz"); win = z["win"].astype(np.float64); W = int(z["W"]); ids = list(z["ids"])
    I = win[..., 0] + win[..., 1]; k = np.arange(-W, W + 1); outer = (np.abs(k) >= 8) & (np.abs(k) <= W - 2)
    base = np.median(I[:, :, np.abs(k) >= 8], axis=2, keepdims=True); In = I / base - 1
    offs = [o for o in range(-W + 1, W) if abs(o) >= 8 or o == 0]
    st = {}
    for o in offs:
        st[o] = In[:, :, W + o - 1:W + o + 2].mean(axis=2).sum(axis=1)   # per candidate
    nullv = np.array([st[o] for o in offs if o != 0])                     # (noffs, ncand)
    sd = nullv.std(axis=0)
    per[s] = {o: st[o] / sd for o in offs}
    ids_ = ids
offs = sorted(per[ON[0]])
res = {}
for ci, cid in enumerate(ids_):
    c = {o: sum(per[s][o][ci] for s in ON) - sum(per[s][o][ci] for s in OFF) for o in offs}
    null = np.array([c[o] for o in offs if o != 0])
    rank = (null >= c[0]).mean()
    res[cid] = {"contrast": round(float(c[0]), 2), "null_mean": round(float(null.mean()), 2), "null_sd": round(float(null.std()), 2),
                "z": round(float((c[0] - null.mean()) / null.std()), 2), "frac_null_ge": round(float(rank), 3), "n_null": len(null)}
json.dump(res, open(H / "contrast_null.json", "w"), indent=1)
for cid, v in res.items(): print(cid, v)
zs = [v["z"] for c, v in res.items() if c not in ("C01", "C02")]
print("C03-C13: mean z", round(float(np.mean(zs)), 2), "n z>2:", sum(z > 2 for z in zs), "combined (sum/sqrt n):", round(float(np.sum(zs) / np.sqrt(len(zs))), 2))
