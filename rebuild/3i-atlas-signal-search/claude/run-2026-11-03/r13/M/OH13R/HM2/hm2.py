"""PLAN-HM2: python3 hm2.py select SCRATCHDIR | SCAN | score"""
import json, os, sys, time, importlib.util
import numpy as np, scipy.fft as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..")); sys.path.insert(0, os.path.join(HERE, "../FD")); sys.path.insert(0, os.path.join(HERE, "../HM"))
MINSB = 6; D = 2; HALF = 417


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
        return [{"f_rest_Hz": float(np.mean([r["f_rest_MHz"] for r in c])) * 1e6, "rows": len(c)} for c in cl]
    true = merge(cf.coincidences(0.0, keep=True))
    grid = [float(d) for d in np.round(np.arange(-1.0, 1.00001, 0.005), 3) if abs(d) >= 0.005 - 1e-9]
    assert len(grid) == 400
    frames = []; T00 = time.time()
    for k, d in enumerate(grid):
        frames.append({"k": k, "d_Hz_per_s": d, "dv": d * cf.C / 1.667e9, "selections": merge(cf.coincidences(d * cf.C / 1.667e9, keep=True))})
        if k % 50 == 0: print(k, round(time.time() - T00), flush=True)
    out = {"T0_mjd": float(cf.T0), "true_frame": true, "false_frames": frames, "counts": [len(f["selections"]) for f in frames],
           "check_true_matches_catalogue": sorted(round(c["f_rest_Hz"]) for c in true) == sorted(round(c["f_rest_Hz"]) for c in CAT)}
    json.dump(out, open(os.path.join(HERE, "hm2_selections.json"), "w"))
    print("true", len(true), "catalogue", out["check_true_matches_catalogue"], "| false total", sum(out["counts"]), "empty", sum(1 for c in out["counts"] if c == 0))


def windows():
    import hm
    real = hm.HERE; hm.HERE = HERE
    src = os.path.join(HERE, "hm_selections.json")
    if not os.path.exists(src): os.symlink("hm2_selections.json", src)
    W = hm.hm_windows(); hm.HERE = real
    return W


def scan(s):
    import fdstream as F
    from common import N, DF, FC, NF, TF, W as WW, dm
    WIN = windows(); T0 = json.load(open(os.path.join(HERE, "hm2_selections.json")))["T0_mjd"]; c = WW // 2; SR = WW * DF
    ifl = np.array([F.track_f(s, f, dv, T0) for _, _, f, dv, _ in WIN]); mid = np.rint(np.median(np.rint(ifl), axis=1)).astype(int)
    off_f = (ifl - mid[:, None]) * DF; nw = len(WIN); assert mid.min() > WW and mid.max() < N - WW
    tc = (np.arange(NF) + 0.5) * TF; carry = np.zeros(nw); acc = np.zeros((2, nw)); T00 = time.time()
    for j, X, Y in dm.frames(s, NF):
        ts = (j * WW + np.arange(WW)) / SR
        a = np.clip(np.searchsorted(tc, ts) - 1, 0, NF - 2); w = np.clip((ts - tc[a]) / TF, 0.0, 1.0)
        off = off_f[:, a] * (1 - w)[None, :] + off_f[:, a + 1] * w[None, :]
        Phi = carry[:, None] + 2 * np.pi * np.cumsum(off, axis=1) / SR; carry = Phi[:, -1].copy()
        Fx = dm.fft(X); B = np.stack([Fx[m - c:m + c] for m in mid])
        z = sf.ifft(sf.ifftshift(B, axes=1), axis=1) * np.exp(-1j * Phi); S2 = sf.fftshift(sf.fft(z, axis=1), axes=1)[:, c - 64:c + 65]
        u = S2 / np.maximum(np.abs(S2), 1e-30); n = u.shape[1] - 2 * D
        acc[0 if j < HALF else 1] += np.abs(np.mean(u[:, :n] * u[:, 2 * D:2 * D + n] * np.conj(u[:, D:D + n]) ** 2, axis=1))
        if j % 200 == 0: print(s, j, round(time.time() - T00), flush=True)
    h1, h2 = acc[0] / HALF, acc[1] / (NF - HALF)
    json.dump({"scan": s, "windows": [list(x) for x in WIN], "h1": h1.tolist(), "h2": h2.tolist(), "full": ((acc[0] + acc[1]) / NF).tolist(), "seconds": round(time.time() - T00)},
              open(os.path.join(HERE, f"hm2_{s}.json"), "w"))
    print(s, "done", nw, round(time.time() - T00), flush=True)


def score():
    from common import SCANS, ON
    R = {s: json.load(open(os.path.join(HERE, f"hm2_{s}.json"))) for s in SCANS}; WIN = R["0013"]["windows"]
    idx = {w[0]: i for i, w in enumerate(WIN)}; sb = {}
    for n, k, f, dv, c in WIN:
        if k.startswith("sb:"): sb.setdefault(k[3:], []).append(n)
    excl = [n for n, k, f, dv, c in WIN if k == "sel" and len(sb.get(n, [])) < MINSB]
    out = {"min_sidebands": MINSB, "excluded": excl}
    for part in ("full", "h1", "h2"):
        coh = {}
        for n, k, f, dv, c in WIN:
            if k != "sel" or n in excl: continue
            rk = []
            for s in SCANS:
                x = R[s][part][idx[n]]; v = np.array([R[s][part][idx[m]] for m in sb[n]])
                rk.append((s, (np.sum(v < x) + 0.5 * np.sum(v == x)) / len(v)))
            con = np.mean([r for s, r in rk if s in ON]) - np.mean([r for s, r in rk if s not in ON])
            coh.setdefault(c, []).append(con)
        sc = {c: float(np.mean(v) * np.sqrt(len(v))) for c, v in coh.items()}
        T = sc.get("true"); Fs = np.array([v for c, v in sc.items() if c != "true"])
        out[part] = {"true": T, "n_true": len(coh.get("true", [])), "n_false_nonempty": len(Fs), "n_false_at_or_above": int(np.sum(Fs >= T)),
                     "p": float((1 + np.sum(Fs >= T)) / (1 + len(Fs))), "false_p95": float(np.percentile(Fs, 95)), "false_mean": float(Fs.mean()), "false_sd": float(Fs.std()),
                     "top": sorted(sc.items(), key=lambda x: -x[1])[:8]}
        print(part, {k: v for k, v in out[part].items() if k != "top"}, out[part]["top"][:4])
    out["survives"] = bool(out["full"]["p"] <= 0.01 and out["h1"]["true"] >= out["h1"]["false_p95"] and out["h2"]["true"] >= out["h2"]["false_p95"])
    json.dump(out, open(os.path.join(HERE, "hm2_score.json"), "w"), indent=1)
    print("excluded (fewer than", MINSB, "sidebands):", len(excl), excl[:12]); print("SURVIVES" if out["survives"] else "RETIRES")


if __name__ == "__main__":
    a = sys.argv[1]
    select(sys.argv[2]) if a == "select" else score() if a == "score" else scan(a)
