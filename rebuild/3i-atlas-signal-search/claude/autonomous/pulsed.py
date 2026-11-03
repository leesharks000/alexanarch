"""Time structure an autonomous beacon would plausibly carry, in the GBT 1.07-s products (blc23 .0002.h5, 65,536 channels of 2.861 kHz,
1501.5-1689.0 MHz; cadence 0013-0018, ON 0013/0015/0017 on 3I/ATLAS, OFF 0014/0016/0018). Over one ~5-minute scan the comet's Doppler
change is far below one channel, so each channel holds a comet-fixed tone throughout.

  periodic   per channel, the time series divided by its median, minus one, Hann-windowed; power at each period from 2.15 s to 150 s,
             normalised by that channel's median power. Kept: power >= P_ON at the same channel and period in all three ON scans, and < P_OFF
             in all three OFF scans. Control: the beam swap (OFF as target).
  broadband  the channel-normalised spectrum summed over channels each second (a dispersion-free pulse train), its periodogram in each
             scan; the same rule.
  events     single 1.07-s samples >= Z_EV (robust z per channel) in an ON scan at a channel quiet (< 4) in every OFF scan; and the reverse.
    python3 pulsed.py"""
import glob, json, h5py, hdf5plugin, numpy as np
F = sorted(glob.glob("p2/*.h5")); ON = [f for f in F if "_OFF_" not in f]; OFF = [f for f in F if "_OFF_" in f]
P_ON, P_OFF, Z_EV = 12.0, 4.0, 8.0
def load(f):
    d = h5py.File(f)["data"]; x = d[:, 0, :].astype(np.float64); a = d.attrs
    return x, float(a["fch1"]), float(a["foff"]), float(a["tsamp"])
NT = min(h5py.File(f)["data"].shape[0] for f in F)
X = {}; FREQ = None
for f in F:
    x, f1, fo, ts = load(f); x = x[:NT]
    med = np.median(x, axis=0); med[med == 0] = 1; X[f] = x / med - 1.0
    FREQ = f1 + fo * np.arange(x.shape[1]); TS = ts
nc = X[F[0]].shape[1]
dc = (np.arange(nc) % 1024 >= 1020) | (np.arange(nc) % 1024 <= 3) | (np.abs((np.arange(nc) % 1024) - 512) <= 2)   # coarse-channel edges and DC
w = np.hanning(NT)[:, None]
per = NT * TS / np.arange(1, NT // 2 + 1)
keep_k = (per >= 2.15) & (per <= 150)
def pspec(x):
    P = np.abs(np.fft.rfft((x - x.mean(0)) * w, axis=0))[1:NT // 2 + 1] ** 2
    return P / np.median(P, axis=0)
PS = {f: pspec(X[f]) for f in F}
def periodic(T, R):
    ok = np.ones_like(PS[F[0]], bool)
    for f in T: ok &= PS[f] >= P_ON
    for f in R: ok &= PS[f] < P_OFF
    ok[~keep_k, :] = False; ok[:, dc] = False
    k, c = np.where(ok); return [{"f_MHz": round(FREQ[j], 4), "period_s": round(per[i], 2), **{f.split("_")[-1].split(".")[0]: round(float(PS[f][i, j]), 1) for f in F}} for i, j in zip(k, c)]
def broadband(T, R):
    def bp(f):
        s = np.where(dc, 0, X[f]).sum(1); P = np.abs(np.fft.rfft((s - s.mean()) * np.hanning(NT)))[1:NT // 2 + 1] ** 2; return P / np.median(P)
    B = {f: bp(f) for f in F}
    ok = keep_k.copy()
    for f in T: ok &= B[f] >= P_ON
    for f in R: ok &= B[f] < P_OFF
    return [round(per[i], 2) for i in np.where(ok)[0]], {f.split("_")[-1].split(".")[0] + ("off" if "_OFF_" in f else "on"): [round(per[i], 2) for i in np.argsort(B[f])[-3:]] for f in F}
def events(T, R):
    def z(x):
        m = np.median(x, 0); s = 1.4826 * np.median(np.abs(x - m), 0); s[s == 0] = np.inf; return (x - m) / s
    Z = {f: z(X[f]) for f in F}
    quiet = np.all([np.abs(Z[f]).max(0) < 4 for f in R], axis=0) & ~dc
    out = []
    for f in T:
        t, c = np.where((Z[f] >= Z_EV) & quiet[None, :]); out += [(f[-25:-17], int(ti), round(FREQ[ci], 4), round(float(Z[f][ti, ci]), 1)) for ti, ci in zip(t, c)]
    return out
res = {"nt": NT, "tsamp": TS, "P_on": P_ON, "P_off": P_OFF, "z_event": Z_EV}
for name, T, R in (("on_target", ON, OFF), ("beam_swap", OFF, ON)):
    p = periodic(T, R); b, top = broadband(T, R); e = events(T, R)
    res[name] = {"periodic_n": len(p), "periodic": p, "broadband_periods": b, "broadband_top3": top, "events_n": len(e),
                 "event_channels": len({x[2] for x in e}), "events": e}
    print(name, len(p), "periodic;", b, "broadband;", len(e), "events in", len({x[2] for x in e}), "channels", flush=True)
json.dump(res, open("p2/pulsed.json", "w"), indent=1)
