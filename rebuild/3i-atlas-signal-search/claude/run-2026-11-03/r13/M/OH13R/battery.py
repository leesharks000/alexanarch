"""PLAN-OH13R: the object portraits, the battery (96 statistics), injections and the reading.
python3 battery.py portraits | stats PART NPARTS | inject PART NPARTS | read"""
import json, os, sys, time, zlib
import numpy as np
from scipy.ndimage import uniform_filter1d
from common import *
sys.path.insert(0, os.path.join(HERE, "../N1625")); import n1625a as NS

FRAMES = ["topo", "comet"]; FEEDS = ["X", "Y"]; FAM = ["X+", "X-", "Y+", "Y-", "XY+", "XY-"]
c = W // 2; SR = W * DF; HALF = NF // 2


def unit(A): return A / np.maximum(np.abs(A), 1e-30)


def STATS():
    s = []
    for fr in FRAMES:
        for q in FEEDS:
            s += [f"D1|{q}|{fr}"] + [f"D2|{L}|{q}|{fr}" for L in (512, 4096)] + [f"D3|d{d}|{q}|{fr}" for d in (1, 2, 4, 8, 16, 32)]
            s += [f"D4|{q}|{fr}", f"D7|{q}|{fr}"] + [f"D8|{L}|{q}|{fr}" for L in (64, 512)]
            s += [f"D9a|{q}|{fr}", f"D9b|{q}|{fr}", f"D10|{q}|{fr}", f"D11|{q}|{fr}"]
        s += [f"D5|{L}|{f}|{fr}" for L in (64, 512) for f in FAM] + [f"D6|{L}|{fr}" for L in (512, 4096)]
    assert len(s) == 96, len(s); return s


def cband(L): return {64: [L // 2], 512: [L // 2 - 1, L // 2, L // 2 + 1], 4096: list(range(L // 2 - 11, L // 2 + 12))}[L]


def feats(SX, SY, fr):
    """SX, SY: (nf, W) native spectra of one selection -> {stat: value} for this frame configuration."""
    out = {}; Z = {"X": series(SX), "Y": series(SY)}; NAT = {"X": SX, "Y": SY}
    R = {(q, L): segspec(Z[q], L) for q in FEEDS for L in (64, 512, 4096)}
    for q in FEEDS:
        S = NAT[q]; P = (np.abs(S) ** 2).mean(0)
        ex = np.r_[0:c - 20, c + 21:W]; out[f"D1|{q}|{fr}"] = float(P[c - 3:c + 4].mean() / np.median(P[ex]))
        for L in (512, 4096):
            U = unit(R[(q, L)]); v = 0.0
            for k in cband(L):
                for lag in (1, 2, 4, 8): v = max(v, float(np.abs(np.mean(U[lag:, k] * np.conj(U[:-lag, k])))))
            out[f"D2|{L}|{q}|{fr}"] = v
        u = unit(S[:, c - 64:c + 65])
        for d in (1, 2, 4, 8, 16, 32):
            n = u.shape[1] - 2 * d; Q = np.abs(np.mean(u[:, :n] * u[:, 2 * d:2 * d + n] * np.conj(u[:, d:d + n]) ** 2, axis=1))
            out[f"D3|d{d}|{q}|{fr}"] = float(Q.mean())
        U = unit(R[(q, 512)]); L = 512; cc = L // 2; v = 0.0
        for k in cband(L):
            l = np.arange(L); m = k + l - cc; ok = (np.abs(l - k) >= 2) & (m >= 0) & (m < L)
            A = np.abs(np.mean(U[:, k][:, None] * U[:, l[ok]] * np.conj(U[:, m[ok]]), axis=0)); v = max(v, float(A.max()))
        out[f"D4|{q}|{fr}"] = v
        V, _ = NS.vectors(Z[q]); best, _ = NS.score(NS.scale(V)); out[f"D7|{q}|{fr}"] = float(best[0])
        for L, band in ((64, (0.05, 20.0)), (512, (0.01, 2.5))):
            p = (np.abs(R[(q, L)][:, cband(L)]) ** 2).sum(1); p = p - p.mean(); dt = L / SR
            I = np.abs(np.fft.rfft(p)) ** 2; f = np.fft.rfftfreq(len(p), dt); sel = (f >= band[0]) & (f <= band[1])
            out[f"D8|{L}|{q}|{fr}"] = float(I[sel].max() / np.median(I[sel]))
        x = R[(q, 64)][:, 32]; a2 = np.abs(x) ** 2; out[f"D9a|{q}|{fr}"] = float(np.mean(a2 ** 2) / np.mean(a2) ** 2 - 2)
        U = unit(R[(q, 512)][:, 256]); dphi = np.angle(U[1:] * np.conj(U[:-1]))
        b = np.clip(((dphi + np.pi) / (2 * np.pi) * 16).astype(int), 0, 15).astype(np.uint8).tobytes()
        out[f"D9b|{q}|{fr}"] = float(-len(zlib.compress(b, 9)) / len(b))
        lg = np.log(np.maximum(P, 1e-30)); v = lg - uniform_filter1d(lg, 33, mode="nearest"); v = v - v.mean()
        ac = np.correlate(v, v, "full")[W - 1:] / (v @ v); out[f"D10|{q}|{fr}"] = float(np.abs(ac[4:401]).max())
        z = Z[q]; n = len(z); F = np.fft.fft(z, 2 * n); r = np.fft.ifft(np.abs(F) ** 2)[:1025]
        out[f"D11|{q}|{fr}"] = float(np.abs(r[4:1025]).max() / np.abs(r[0]))
    for L in (64, 512):
        UX, UY = unit(R[("X", L)]), unit(R[("Y", L)]); ks = cband(L); l = np.arange(L)
        best = {f: 0.0 for f in FAM}
        for k in ks:
            ok = np.abs(l - k) >= 2
            pairs = {"X+": (UX[:, k], UX[:, l[ok]], 1), "X-": (UX[:, k], UX[:, l[ok]], -1), "Y+": (UY[:, k], UY[:, l[ok]], 1),
                     "Y-": (UY[:, k], UY[:, l[ok]], -1)}
            for f, (a, B, sg) in pairs.items():
                A = np.abs(np.mean(a[:, None] * (B if sg > 0 else np.conj(B)), axis=0)); best[f] = max(best[f], float(A.max()))
            for f, sg in (("XY+", 1), ("XY-", -1)):
                for a, B in ((UX[:, k], UY[:, l[ok]]), (UY[:, k], UX[:, l[ok]])):
                    A = np.abs(np.mean(a[:, None] * (B if sg > 0 else np.conj(B)), axis=0)); best[f] = max(best[f], float(A.max()))
        for f in FAM: out[f"D5|{L}|{f}|{fr}"] = best[f]
    for L in (512, 4096):
        X, Y = R[("X", L)], R[("Y", L)]; v = 0.0
        for k in cband(L):
            v = max(v, float(np.abs(np.mean(X[:, k] * np.conj(Y[:, k]))) / np.sqrt(np.mean(np.abs(X[:, k]) ** 2) * np.mean(np.abs(Y[:, k]) ** 2))))
        out[f"D6|{L}|{fr}"] = v
    return out


def window_spec(A, w, q):
    a = A[:, w, q]; return (a[..., 0].astype(np.float32) + 1j * a[..., 1].astype(np.float32)).astype(np.complex64)


def configs(SX, SY, scan, f):
    """Topocentric spectra -> {frame: (SX, SY)}; the comet frame by continuous de-Doppler (amendment 1)."""
    Phi = phase_track(scan, f, SX.shape[0]); return {"topo": (SX, SY), "comet": (dedop(SX, Phi), dedop(SY, Phi))}


def all_feats(SXs, SYs, scan, f, halves):
    """Both frame configurations; full and, if asked, the two halves."""
    res = {"full": {}, "h1": {}, "h2": {}}
    C2 = configs(selection(SXs), selection(SYs), scan, f)
    for fr in FRAMES:
        SX, SY = C2[fr]
        res["full"].update(feats(SX, SY, fr))
        if halves:
            res["h1"].update(feats(SX[:HALF], SY[:HALF], fr)); res["h2"].update(feats(SX[HALF:], SY[HALF:], fr))
    return res


# ---- injection ----------------------------------------------------------------
LEVEL0 = 0.16
CLASSES = list("abcdefghijk")


def inject(SX, SY, scan, f, cls, lvl, seed):
    """Add class cls at lvl × LEVEL0 of a native bin's noise power to a topocentric selection, following the comet track with
    the continuous track phase Φ (amendment 1)."""
    rng = np.random.default_rng(seed); nf = SX.shape[0]; sig2 = float(np.median(np.abs(SX) ** 2)); Ptot = lvl * LEVEL0 * sig2
    Phi = phase_track(scan, f, nf)[:nf * W].reshape(nf, W); ts = np.arange(W) / SR
    def tone_frames(phase_fn, amp_fn=None, extra_hz=0.0):
        out = np.zeros((nf, W), np.complex64)
        for j in range(nf):
            tt = j * TF + ts; ph = Phi[j] + 2 * np.pi * extra_hz * tt + phase_fn(j, tt)
            a = 1.0 if amp_fn is None else amp_fn(tt)
            out[j] = a * np.exp(1j * ph)
        return out
    def to_spec(z): return np.fft.fftshift(np.fft.fft(z, axis=1), axes=1)
    dX = np.zeros_like(SX); dY = np.zeros_like(SY); BIN = SR / 512
    if cls == "a":
        dX = to_spec(tone_frames(lambda j, tt: 0.0))
    elif cls == "b":
        steps = np.cumsum(rng.normal(0, 0.3 / np.sqrt(512), nf * W)).reshape(nf, W); dX = to_spec(tone_frames(lambda j, tt: steps[j]))
    elif cls == "c":
        k = np.arange(-64, 65); ph = np.pi * 0.37 * k ** 2; S = np.zeros((nf, W), np.complex64); S[:, c - 64:c + 65] = np.exp(1j * ph)[None, :]; dX = S
    elif cls in "de":
        nseg = nf * W // 512 + 1; a = rng.uniform(0, 2 * np.pi, nseg); b = rng.uniform(0, 2 * np.pi, nseg)
        seg = lambda j, tt: (j * W + np.arange(W)) // 512
        if cls == "d":
            dX = to_spec(tone_frames(lambda j, tt: a[seg(j, tt)], extra_hz=1 * BIN) + tone_frames(lambda j, tt: b[seg(j, tt)], extra_hz=37 * BIN)
                         + tone_frames(lambda j, tt: a[seg(j, tt)] + b[seg(j, tt)], extra_hz=38 * BIN))
        else:
            dX = to_spec(tone_frames(lambda j, tt: a[seg(j, tt)]) + tone_frames(lambda j, tt: -a[seg(j, tt)], extra_hz=53 * BIN))
    elif cls == "f":
        nseg = nf * W // 512 + 1; ph = rng.uniform(0, 2 * np.pi, nseg); amp = rng.rayleigh(1, nseg)
        z = tone_frames(lambda j, tt: ph[(j * W + np.arange(W)) // 512], amp_fn=None)
        z = z * amp[(np.arange(nf)[:, None] * W + np.arange(W)[None, :]) // 512]; dX = to_spec(z); dY = dX.copy()
    elif cls == "g":
        z = np.zeros((nf, W), np.complex64); pos = rng.choice(np.arange(-40, 41), 8, replace=False); wts = rng.uniform(0.5, 1.5, 8); seglen = 512; nseg = nf * W // seglen
        zz = z.ravel()
        for s in range(0, nseg, 64):
            tt = np.arange(seglen) / SR; j0 = s * seglen
            for i, w8 in zip(pos, wts): zz[j0:j0 + seglen] += w8 * np.exp(1j * (Phi.ravel()[j0:j0 + seglen] + 2 * np.pi * i * BIN * tt))
        dX = to_spec(zz.reshape(nf, W))
    elif cls == "h":
        dX = to_spec(tone_frames(lambda j, tt: 0.0, amp_fn=lambda tt: (np.sin(2 * np.pi * 1.3 * tt) > 0).astype(float)))
    elif cls == "i":
        starts = rng.uniform(0, nf * TF, int(nf * TF / 0.5))
        def amp(tt):
            m = np.zeros_like(tt)
            for s0 in starts[(starts > tt[0] - 0.05) & (starts < tt[-1])]: m[(tt >= s0) & (tt < s0 + 0.05)] = 1
            return m
        dX = to_spec(tone_frames(lambda j, tt: 0.0, amp_fn=amp))
    elif cls == "j":
        S = np.zeros((nf, W), np.complex64); nb = (rng.normal(size=(nf, 5)) + 1j * rng.normal(size=(nf, 5))).astype(np.complex64)
        S[:, c - 2:c + 3] = nb; S[:, c + 198:c + 203] = nb; dX = S
    elif cls == "k":
        wn = (rng.normal(size=nf * W + 300) + 1j * rng.normal(size=nf * W + 300)).astype(np.complex64); z = wn[300:] + wn[:-300]
        dX = to_spec(z.reshape(nf, W))
    g = np.sqrt(Ptot / max(float((np.abs(dX) ** 2).sum(1).mean()), 1e-30))   # mean over frames of the injected power summed over bins = Ptot
    return (SX + g * dX).astype(np.complex64), (SY + g * dY).astype(np.complex64)


# ---- inference -------------------------------------------------------------------
def pvals(T, ctrl_idx, idx_all):
    """Empirical p of every window against the control population (controls leave themselves out)."""
    out = {}
    cv = np.array([T[i] for i in ctrl_idx])
    for i in idx_all:
        x = T[i]; n = np.sum(cv >= x); m = len(cv)
        if i in ctrl_idx: n -= 1; m -= 1
        out[i] = (1 + n) / (1 + m)
    return out


def resolves(p_on, p_off, h_on, h_ctrl90):
    return all(p <= 0.10 for p in p_on) and all(p > 0.10 for p in p_off) and all(h_on[h] > h_ctrl90[h] for h in ("h1", "h2"))


# ---- drivers ------------------------------------------------------------------
def portraits():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    WIN = windows(); od = os.path.join(HERE, "object"); os.makedirs(od, exist_ok=True); summ = {}
    A = {s: load(s) for s in SCANS}
    for w, (name, kind, f, par) in enumerate(WIN):
        if kind == "ctrl": continue
        fig, ax = plt.subplots(4, 6, figsize=(18, 11)); summ[name] = {}
        for j, s in enumerate(SCANS):
            row = {}
            for q, nm in ((0, "X"), (1, "Y")):
                Sc = dedop(selection(window_spec(A[s], w, q)), phase_track(s, f)); S = Sc[:, c - 64:c + 65]; P = np.abs(S) ** 2
                D = P[:NF // 17 * 17].reshape(-1, 17, 129).mean(1); D = D / np.median(D)
                ax[q, j].imshow(D, aspect="auto", origin="lower", cmap="magma", vmin=0.5, vmax=2.0, extent=[-64 * DF, 64 * DF, 0, NF * TF])
                ax[q, j].set_title(f"{name} {s} {'ON' if s in ON else 'OFF'} {nm}", fontsize=8)
                prof = P.mean(0) / np.median(P.mean(0)); ax[2, j].plot((np.arange(129) - 64) * DF, prof, lw=0.8, label=nm)
                row[nm] = {"centre_power_ratio": float(prof[61:68].mean()), "peak_offset_hz": float((np.argmax(prof[56:73]) - 8) * DF)}
                z = series(Sc); R4 = segspec(z, 4096)[:, 2048]
                ax[3, j].plot(np.unwrap(np.angle(R4)), lw=0.6, label=nm)
            ax[2, j].axvspan(-8, 8, color="0.9"); ax[2, j].legend(fontsize=6); ax[3, j].set_title("centre-bin phase, R(4096)", fontsize=7)
            summ[name][s] = row
        fig.suptitle(f"{name} (f_rest {f / 1e6:.6f} MHz): comet-frame dynamic spectra (rows of 17 frames, ±64 bins), profiles, centre phase")
        fig.tight_layout(); fig.savefig(os.path.join(od, f"{name}.png"), dpi=70); plt.close(fig)
        print(name, json.dumps(summ[name])[:300], flush=True)
    json.dump(summ, open(os.path.join(od, "portraits.json"), "w"), indent=1)


def stats(part, nparts):
    WIN = windows(); res = {}; A = {s: load(s) for s in SCANS}; T0 = time.time()
    for w in range(part, len(WIN), nparts):
        name, kind, f, par = WIN[w]; res[name] = {}
        for s in SCANS:
            SX = window_spec(A[s], w, 0); SY = window_spec(A[s], w, 1)
            res[name][s] = all_feats(SX, SY, s, f, halves=s in ON)
        print(name, round(time.time() - T0), flush=True)
        json.dump(res, open(os.path.join(HERE, f"stats_part{part}.json"), "w"))


INJ_WIN = ["C03", "C05", "C07", "C09", "C11", "C13"]


def injections(part, nparts):
    WIN = windows(); names = [w[0] for w in WIN]; A = {s: load(s) for s in ON}; res = {}; T0 = time.time(); jobs = []
    for cand in INJ_WIN:
        w = next(i for i, x in enumerate(WIN) if x[1] == "ctrl" and x[3] == cand)
        for cls in CLASSES:
            for lvl in (1, 3, 10): jobs.append((w, cls, lvl))
    for n, (w, cls, lvl) in enumerate(jobs):
        if n % nparts != part: continue
        name, kind, f, par = WIN[w]; key = f"{name}|{cls}|{lvl}"; res[key] = {}
        for si, s in enumerate(ON):
            SXs = window_spec(A[s], w, 0); SYs = window_spec(A[s], w, 1); r = {"full": {}, "h1": {}, "h2": {}}
            SX, SY = inject(selection(SXs), selection(SYs), s, f, cls, lvl, seed=zlib.crc32(f'{name}|{cls}|{lvl}|{s}'.encode()))
            C2 = configs(SX, SY, s, f)
            for fr in FRAMES:
                SX, SY = C2[fr]
                r["full"].update(feats(SX, SY, fr)); r["h1"].update(feats(SX[:HALF], SY[:HALF], fr)); r["h2"].update(feats(SX[HALF:], SY[HALF:], fr))
            res[key][s] = r
        print(key, round(time.time() - T0), flush=True)
        json.dump(res, open(os.path.join(HERE, f"inject_part{part}.json"), "w"))


def merge(prefix):
    d = {}
    for fn in sorted(os.listdir(HERE)):
        if fn.startswith(prefix + "_part") and fn.endswith(".json"): d.update(json.load(open(os.path.join(HERE, fn))))
    return d


def read():
    WIN = windows(); ST = STATS(); S = merge("stats"); I = merge("inject")
    names = [w[0] for w in WIN]; kind = {w[0]: w[1] for w in WIN}; ctrl = [n for n in names if kind[n] == "ctrl"]
    cands = [n for n in names if kind[n] == "cand"]; rng = np.random.default_rng(1665)
    out = {"per_stat": {}, "resolutions": [], "ctrl_resolutions": 0, "inject": {}}
    for st in ST:
        p = {}; D = {}
        for s in SCANS:
            T = {n: S[n][s]["full"][st] for n in names}; p[s] = pvals(T, ctrl, names)
        hsum = {}
        for h in ("h1", "h2"):
            ph = {}
            for s in ON:
                T = {n: S[n][s][h][st] for n in names}; ph[s] = pvals(T, ctrl, names)
            hsum[h] = {n: -sum(np.log(ph[s][n]) for s in ON) for n in names}
        h90 = {h: float(np.quantile([hsum[h][n] for n in ctrl], 0.9)) for h in hsum}
        res_names = []
        for n in names:
            D[n] = -sum(np.log(p[s][n]) for s in ON) + sum(np.log(p[s][n]) for s in OFF)
            if resolves([p[s][n] for s in ON], [p[s][n] for s in OFF], {h: hsum[h][n] for h in hsum}, h90): res_names.append(n)
        cd = np.array([D[n] for n in ctrl]); m = np.mean([D[n] for n in cands])
        draws = np.array([cd[rng.choice(len(cd), len(cands), replace=False)].mean() for _ in range(10000)])
        pagg = float((1 + np.sum(draws >= m)) / 10001)
        out["per_stat"][st] = {"p_agg": pagg, "mean_delta_cands": float(m), "resolved": res_names,
                               "ref_C02": {"p_on": [p[s]["C02"] for s in ON], "p_off": [p[s]["C02"] for s in OFF]},
                               "delta_max_ctrl": float(cd.max()), "delta": {n: float(D[n]) for n in cands + ["C02"]}}
        for n in res_names:
            if kind[n] == "cand": out["resolutions"].append({"stat": st, "cand": n, "delta": float(D[n]), "exceeds_all_ctrl": bool(D[n] > cd.max())})
            elif kind[n] == "ctrl": out["ctrl_resolutions"] += 1
        # injections: p of the injected control against the untouched control population, same rule
        for key, v in I.items():
            name = key.split("|")[0]
            pon = []
            for s in ON:
                T = {n: S[n][s]["full"][st] for n in names}; cv = np.array([T[n] for n in ctrl if n != name]); x = v[s]["full"][st]
                pon.append((1 + np.sum(cv >= x)) / (1 + len(cv)))
            hs = {}
            for h in ("h1", "h2"):
                tot = 0
                for s in ON:
                    T = {n: S[n][s][h][st] for n in names}; cv = np.array([T[n] for n in ctrl if n != name]); x = v[s][h][st]
                    tot += -np.log((1 + np.sum(cv >= x)) / (1 + len(cv)))
                hs[h] = tot
            poff = [p[s][name] for s in OFF]
            if resolves(pon, poff, hs, h90): out["inject"].setdefault(key, []).append(st)
    nst = len(ST); out["n_stats"] = nst; out["n_ctrl"] = len(ctrl); out["n_cands"] = len(cands)
    out["ctrl_rate"] = out["ctrl_resolutions"] / (nst * len(ctrl))
    out["cand_resolutions"] = len(out["resolutions"])
    from scipy.stats import binom
    out["binom_p"] = float(binom.sf(out["cand_resolutions"] - 1, nst * len(cands), max(out["ctrl_rate"], 1e-9)))
    out["n_p05"] = sum(v["p_agg"] <= 0.05 for v in out["per_stat"].values()); out["bonf"] = [k for k, v in out["per_stat"].items() if v["p_agg"] <= 0.05 / nst]
    json.dump(out, open(os.path.join(HERE, "reading.json"), "w"), indent=1)
    print("candidate resolutions:", out["cand_resolutions"], "control rate:", round(out["ctrl_rate"], 5), "binom p:", out["binom_p"])
    print("stats with aggregate p<=0.05:", out["n_p05"], "of", nst, "| Bonferroni:", out["bonf"])
    for r in out["resolutions"]: print("RES", r)


if __name__ == "__main__":
    a = sys.argv[1]
    if a == "portraits": portraits()
    elif a == "stats": stats(int(sys.argv[2]), int(sys.argv[3]))
    elif a == "inject": injections(int(sys.argv[2]), int(sys.argv[3]))
    elif a == "read": read()
