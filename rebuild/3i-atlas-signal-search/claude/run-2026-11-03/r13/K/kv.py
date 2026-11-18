"""PLAN-K (PLAN-K.sha256): one scan's coarse-channel-7 voltages streamed again (decoding as voltages/delaymod/dm.py); P1 per integration;
for V0 and V2, in the comet frame, the stationary frame and J's first 200 false frames, the complementarity relation of kcore.relate.
python3 kv.py SCAN  -> out/SCAN.npz, out/SCAN.json"""
import sys, os, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../voltages/delaymod")); import dm
sys.path.insert(0, HERE); from kcore import shift, relate, DSET
N, INT, C, FC, DF, TBIN = dm.N, dm.INT, dm.C, dm.FC, dm.DF, dm.TBIN
OFFROWS = {"0013": [0], "0014": [0, 1], "0015": [0, 1], "0016": [0, 1, 2], "0017": [0, 1], "0018": [0]}
ONS = ("0013", "0015", "0017"); NFALSE = int(os.environ.get("K_NFALSE", 200))   # env only for the synthetic smoke test
T0 = 61027 + 17226 / 86400.0

def offsets():   # as J: the same draw, first 200 of the 400
    rng = np.random.default_rng(23)
    o = rng.uniform(0.03, 1.0, 400) * rng.choice([-1, 1], 400) * C / 1.42e9
    return np.concatenate([[0.0], o[:NFALSE]])

def main(scan):
    nfr = int(os.environ.get("K_NFR", 833)); nint = nfr // INT; thr = 3.0 if scan in ONS else 2.0
    t0s = 61027 + int(dm.SCANS[scan][0]) / 86400.0
    E = dm.ephem(); vel = lambda t: np.interp(t, E[:, 0], E[:, 1])
    P = np.zeros((nint, N), np.float32); ts = time.time()
    for j, X, Y in dm.frames(scan, nfr):
        k = j // INT
        if k >= nint: continue
        FX = dm.fft(X); FY = dm.fft(Y); P[k] += FX.real ** 2 + FX.imag ** 2 + FY.real ** 2 + FY.imag ** 2
        if j % 100 == 0: print(scan, "frame", j, f"{time.time() - ts:.0f}s", flush=True)
    t = t0s + (np.arange(nint) * INT + INT / 2) * N * TBIN / 86400.0
    med = np.median(P, axis=0); med[med <= 0] = 1
    R = P / med - 1.0; del P
    R = (R + np.roll(R, 1, axis=1) + np.roll(R, -1, axis=1)).astype(np.float32)
    offs = offsets(); res = {"offs": offs, "thr": np.float32(thr)}
    keep = {"V0": np.ones(nint, bool), "V2": ~np.isin(np.arange(nint), OFFROWS[scan])}
    # gate product: J's M1 stack for V0, comet frame
    v = vel(t); sh = np.rint(FC * (v - v[0]) / C / DF).astype(int)
    acc = shift(R.astype(np.float64), sh).sum(0); mm = np.median(acc); s = 1.4826 * np.median(np.abs(acc - mm)); z = (acc - mm) / s
    z[N // 2 - 4:N // 2 + 5] = 0; res["gate_idx"] = np.where(z >= 2.0)[0].astype(np.int32); del acc, z
    frames = [("f%d" % i, dv) for i, dv in enumerate(offs)] + [("S", None)]
    for V, kk in keep.items():
        for name, dv in frames:
            if dv is None: shv = np.zeros(nint, int)
            else:
                vv = vel(t) + dv * (t - T0) * 86400.0; shv = np.rint(FC * (vv - vv[0]) / C / DF).astype(int)
            o = relate(shift(R[kk], shv[kk]))
            key = f"{V}_{name}"; res[key + "_v0"] = np.float64((vel(t) + (0 if dv is None else dv * (t - T0) * 86400.0))[kk][0])
            for d, r in o.items():
                zz = r["z"]; ii = np.where(zz >= thr)[0]
                res[f"{key}_d{d}_idx"] = ii.astype(np.int32); res[f"{key}_d{d}_z"] = zz[ii].astype(np.float16)
                for a in ("k2_f", "k2_h1", "k2_h2", "k3_f", "k3_s", "k3_p", "k3_ph"): res[f"{key}_d{d}_{a}"] = r[a]
            if name.endswith("0") and name[1:].isdigit() and int(name[1:]) % 50 == 0 or name == "S":
                print(scan, V, name, f"{time.time() - ts:.0f}s", flush=True)
    OUT = os.environ.get("K_OUT", os.path.join(HERE, "out")); os.makedirs(OUT, exist_ok=True)
    np.savez_compressed(os.path.join(OUT, f"{scan}.npz"), **res)
    json.dump({"scan": scan, "nframes": nfr, "nint": nint, "offrows": OFFROWS[scan], "thr": thr, "elapsed_s": time.time() - ts},
              open(os.path.join(OUT, f"{scan}.json"), "w"))
    print(scan, "done", f"{time.time() - ts:.0f}s", flush=True)

if __name__ == "__main__":
    main(sys.argv[1])
