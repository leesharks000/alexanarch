"""PLAN-HM10: the comet's OH line, measured and calibrated.   python3 hm10.py selftest | run
(A) Public rawspec.0000 total-power spectra (2.794 Hz x 6.08 s), scans 0013-0018: OH 1665.4018 and 1667.3590 MHz jointly
(LTE 5:9), 1612.2310 reported; comet frame from the session's Horizons range-rate (voltages/delaymod). (B) Voltage spectra at
1667 (HM6/HM8 kept ohC, X and Y apart). Matched filter: cubic baseline + Gaussian of FWHM 1, 2, 3 km/s, centred on the comet's
rest velocity; null from the same fit at line-free offsets; calibration by injecting absorption lines into the ON spectra."""
import json, os, re, sys, urllib.request
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); C = 299792.458
sys.path.insert(0, os.path.join(HERE, "../../../../../voltages/delaymod")); import dm
U = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/"
L1665, L1667, L1612 = 1665.4018e6, 1667.3590e6, 1612.2310e6
WIDTHS = [1.0, 2.0, 3.0]                      # km/s FWHM
HALF = 90e3; BIN = 1.4e3                      # +-90 kHz window, 1.4 kHz bins
CTRL = np.r_[np.arange(-60e3, -24e3, 1e3), np.arange(25e3, 61e3, 1e3)]   # 72 line-free centres
INJ_A = [0.5e-3, 1.0e-3, 1.5e-3, 2.0e-3, 3.0e-3]; INJ_POS = CTRL[::6]     # fraction of system power at the 1667 peak
PAIRS = [("0013", ["0014"]), ("0015", ["0014", "0016"]), ("0017", ["0016", "0018"])]   # as absorb-calib
ORDER = ["0013", "0014", "0015", "0016", "0017", "0018"]
SEFD = 10.0                                    # Jy, approximate (absorb-calib), so mJy are approximate


def gauss(o, c, fwhm_hz): return np.exp(-4 * np.log(2) * ((o - c) / fwhm_hz) ** 2)


def fit(specs, offs, fw, c, ratios):
    """Joint least squares: per-line cubic baseline + one amplitude A on templates scaled by ratios. Returns A."""
    cols, y = [], []; nl = len(specs); nb = [len(s) for s in specs]; tot = sum(nb); row = 0
    X = np.zeros((tot, 4 * nl + 1))
    for li, (s, o) in enumerate(zip(specs, offs)):
        u = o / HALF
        for p in range(4): X[row:row + len(s), 4 * li + p] = u ** p
        X[row:row + len(s), -1] = ratios[li] * gauss(o, c, fw[li]); y.append(s); row += len(s)
    beta = np.linalg.lstsq(X, np.concatenate(y), rcond=None)[0]; return float(beta[-1])


def measure(specs, offs, freqs, ratios):
    """For each width: A at the comet's velocity, A at the 72 controls, z against the controls' robust scatter."""
    out = {}
    for w in WIDTHS:
        fw = [f * w / C for f in freqs]
        a0 = fit(specs, offs, fw, 0.0, ratios); ac = np.array([fit(specs, offs, fw, c, ratios) for c in CTRL])
        sg = 1.4826 * np.median(np.abs(ac - np.median(ac)))
        out[f"{w:g}"] = {"A": a0, "sigma": float(sg), "z": float(a0 / sg), "controls_below": int((ac <= a0).sum()), "n_controls": len(CTRL),
                         "three_sigma_frac": float(3 * sg), "three_sigma_mJy": float(3 * sg * SEFD * 1e3)}
    return out


def rebin(s, o):
    nb = int(round(BIN / abs(o[1] - o[0]))); m = len(s) // nb
    s2, o2 = s[:m * nb].reshape(m, nb).mean(1), o[:m * nb].reshape(m, nb).mean(1)
    if o2[0] > o2[-1]: s2, o2 = s2[::-1], o2[::-1]
    return s2, o2


# ---------------------------------------------------------------- (A) rawspec
def rawspec_scans(freqs):
    import fsspec, h5py, hdf5plugin  # noqa: F401
    idx = urllib.request.urlopen(U, timeout=60).read().decode()
    F = sorted(set(re.findall(r'(blc23_guppi_\d+_\d+_DIAG_3I_ATLAS(?:_OFF)?_001[3-8]\.rawspec\.0000\.h5)', idx)), key=lambda x: x[-20:-16])
    assert [f[-20:-16] for f in F] == ORDER, F
    fs = fsspec.filesystem("https", block_size=8 << 20); E = dm.ephem(); out = {}
    for f, s in zip(F, ORDER):
        d = h5py.File(fs.open(U + f))["data"]; a = d.attrs; f1, fo = float(a["fch1"]) * 1e6, float(a["foff"]) * 1e6
        T = float(a["tstart"]) + (np.arange(d.shape[0]) + 0.5) * float(a["tsamp"]) / 86400; v = np.interp(T, E[:, 0], E[:, 1])
        per = {}
        for f0 in freqs:
            pos = f0 * (1 - v / C); ch = lambda x: (x - f1) / fo
            lo, hi = sorted((ch(pos.min() - HALF - 5e3), ch(pos.max() + HALF + 5e3))); c0 = int(lo); n = int(hi) - c0 + 1
            Xd = d[:, 0, c0:c0 + n].astype(np.float64); nu = int(HALF / abs(fo)); cc = np.rint(ch(pos) - c0).astype(int)
            G = np.stack([Xd[k, cc[k] - nu:cc[k] + nu + 1] for k in range(Xd.shape[0])])
            per[f0] = (G.mean(0), np.arange(-nu, nu + 1) * abs(fo) * np.sign(fo))
        out[s] = per; print("rawspec", s, "read", flush=True)
    return out, {"files": F}


def ratio_spectra(S, f0, inj=None):
    """Pooled ON/OFF - 1 over the three pairs (equal weight), rebinned; inj = (a, centre) multiplies ON by (1 - a g)."""
    acc = None
    for on, offs in PAIRS:
        son, o = S[on][f0]; soff = np.mean([S[x][f0][0] for x in offs], axis=0)
        if inj is not None:
            a, c, fw = inj; son = son * (1 - a * gauss(o, c, fw))
        r = son / soff - 1; acc = r if acc is None else acc + r
    return rebin(acc / len(PAIRS), o)


def per_pair(S, f0):
    out = []
    for on, offs in PAIRS:
        son, o = S[on][f0]; soff = np.mean([S[x][f0][0] for x in offs], axis=0); out.append(rebin(son / soff - 1, o))
    return out


def run():
    res = {"plan": "PLAN-HM10.md", "sefd_Jy_assumed": SEFD}
    S, meta = rawspec_scans([L1665, L1667, L1612]); res["rawspec_files"] = meta["files"]
    sp = {f0: ratio_spectra(S, f0) for f0 in (L1665, L1667, L1612)}
    res["joint_1665_1667"] = measure([sp[L1665][0], sp[L1667][0]], [sp[L1665][1], sp[L1667][1]], [L1665, L1667], [5 / 9, 1.0])
    for nm, f0 in (("1665", L1665), ("1667", L1667), ("1612", L1612)):
        res[f"line_{nm}"] = measure([sp[f0][0]], [sp[f0][1]], [f0], [1.0])
        res[f"line_{nm}_per_pair"] = [measure([s], [o], [f0], [1.0])["2"] for s, o in per_pair(S, f0)]
    # calibration: absorption injected into the ON spectra at line-free offsets, both main lines at 5:9
    cal = {}
    for w in WIDTHS:
        for a in INJ_A:
            rec = []
            for c in INJ_POS:
                s65 = ratio_spectra(S, L1665, (a * 5 / 9, c, L1665 * w / C)); s67 = ratio_spectra(S, L1667, (a, c, L1667 * w / C))
                fw = [L1665 * w / C, L1667 * w / C]
                A = fit([s65[0], s67[0]], [s65[1], s67[1]], fw, c, [5 / 9, 1.0]); rec.append(A)
            sg = res["joint_1665_1667"][f"{w:g}"]["sigma"]; rec = np.array(rec)
            cal[f"{w:g}|{a:g}"] = {"injected_frac": a, "injected_mJy": a * SEFD * 1e3, "mean_recovered": float(rec.mean()),
                                   "recovered_over_injected": float(-rec.mean() / a), "detected_3sigma": int((rec / sg <= -3).sum()), "n": len(rec)}
        print("calibration width", w, {k: v["detected_3sigma"] for k, v in cal.items() if k.startswith(f"{w:g}|")}, flush=True)
    res["calibration"] = cal
    # (B) voltages, 1667 only, X and Y apart (HM6 for 0013/0014, HM8 for 0015-0018)
    V = {}
    for s in ORDER:
        p = os.path.join(HERE, "../HM6" if s in ("0013", "0014") else "../HM8", f"hm6_{s}.npz"); z = np.load(p); V[s] = z["ohC"]
    nb = V["0013"].shape[1]; o = -((np.arange(nb) - nb // 2) * dm.DF)   # bin index rises as frequency falls
    vres = {}
    for fi, fe in enumerate("XY"):
        acc = sum(V[on][fi] / np.mean([V[x][fi] for x in offs], axis=0) - 1 for on, offs in PAIRS) / len(PAIRS)
        s2, o2 = rebin(acc, o); keep = np.abs(o2) <= 70e3; vres[fe] = measure([s2[keep]], [o2[keep]], [L1667], [1.0])
    res["voltage_1667"] = vres
    json.dump(res, open(os.path.join(HERE, "hm10.json"), "w"), indent=1)
    print(json.dumps({k: res[k] for k in ("joint_1665_1667", "line_1667", "line_1665")}, indent=0)[:3000])


def selftest():
    """Synthetic only: noise spectra with a cubic bandpass; then the same with a 5:9 absorption pair at the comet's velocity."""
    rng = np.random.default_rng(3); o = np.arange(-HALF, HALF + 1, 2.794); bp = 1 + 0.02 * (o / HALF) - 0.01 * (o / HALF) ** 3
    def spec(depth):
        s65 = bp * (1 - depth * 5 / 9 * gauss(o, 0, L1665 * 2 / C)) + rng.normal(0, 0.03, len(o))
        s67 = bp * (1 - depth * gauss(o, 0, L1667 * 2 / C)) + rng.normal(0, 0.03, len(o))
        return rebin(s65 / bp - 1, o), rebin(s67 / bp - 1, o)
    for depth in (0.0, 1.5e-3):
        (a, b), (c, d) = spec(depth); m = measure([a, c], [b, d], [L1665, L1667], [5 / 9, 1.0])
        print("injected", depth, {w: (round(v["A"] * 1e3, 3), round(v["z"], 1)) for w, v in m.items()})


if __name__ == "__main__":
    {"selftest": selftest, "run": run}[sys.argv[1]]()
