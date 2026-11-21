"""PLAN-OH13R: windows, tracks and representations shared by extraction and analysis."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "../../../..")
sys.path.insert(0, os.path.join(ROOT, "voltages/delaymod")); import dm
N, DF, FC, TBIN, C = dm.N, dm.DF, dm.FC, dm.TBIN, dm.C
TF = N * TBIN; NF = 833; W = 1024; M = 32; WS = W + 2 * M; SCALE = 1 / 64
SCANS = ["0013", "0014", "0015", "0016", "0017", "0018"]; ON = ["0013", "0015", "0017"]; OFF = ["0014", "0016", "0018"]
LINES = [1665.615127e6, 1665.75011e6, 1666.0045e6, 1666.0091e6]
OFFS = [3.2e3, -3.2e3, 6.4e3, -6.4e3, 9.6e3, -9.6e3, 12.8e3, -12.8e3, 16.0e3, -16.0e3, 19.2e3, -19.2e3]
EDGE = (FC - 1.46484375e6 + 15e3, FC + 1.46484375e6 - 15e3)


def cands():
    d = json.load(open(os.path.join(ROOT, "oh13/oh13_candidates.json")))
    return {c["id"]: c["f_rest_Hz"] for c in d["candidates"]}


def windows():
    """[(name, kind, f_rest_centre, parent)] — C01 is folded into C02's window. Lines and edges are topocentric and are
    taken to the comet rest frame at mid-session (scan 0015 mid) before comparison."""
    F = cands(); cs = [k for k in sorted(F) if k != "C01"]
    half = WS / 2 * DF; r = 1 - vel_fn()(t0("0015") + 150 / 86400.0) / C
    LINES_R = [L / r for L in LINES]; EDGE_R = (EDGE[0] / r, EDGE[1] / r)
    out = [(k, "cand" if k != "C02" else "ref", F[k], k) for k in cs]
    taken = [(F[k] - half, F[k] + half) for k in cs]
    for k in cs:
        n = 0
        for o in OFFS:
            if n == 6: break
            f = F[k] + o; lo, hi = f - half, f + half
            if lo < EDGE_R[0] or hi > EDGE_R[1]: continue
            if any(abs(L - f) < half + 1.5e3 for L in LINES_R): continue
            if any(not (hi < a or lo > b) for a, b in taken): continue
            out.append((f"{k}{'+' if o > 0 else '-'}{abs(o) / 1e3:.1f}k", "ctrl", f, k)); taken.append((lo, hi)); n += 1
        assert n == 6, (k, n)
    return out


def vel_fn():
    E = dm.ephem(); return lambda t: np.interp(t, E[:, 0], E[:, 1])


def t0(scan): return 61027 + int(dm.SCANS[scan][0]) / 86400.0


def idx(f): return np.rint(N // 2 - (f - FC) / DF).astype(int)


def track(scan, f_rest):
    """Native-bin index of the comet track for every frame, and the mid-scan index."""
    v = vel_fn(); t = t0(scan) + (np.arange(NF) + 0.5) * TF / 86400.0
    i = idx(np.asarray(f_rest) * (1 - v(t) / C)); return i, int(np.rint(np.median(i)))


def selection(Wd, scan=None, f_rest=None, frame="topo"):
    """Wd: (NF, WS) complex window as stored -> (NF, W) topocentric selection (amendment 1: the comet frame is made by dedop)."""
    assert frame == "topo"; return Wd[:, M:M + W]


def phase_track(scan, f_rest, nf=NF):
    """Amendment 1: the continuous phase Φ(t) = 2π∫off(t)dt of the comet track, in the window's baseband (off = track offset
    from the window centre, Hz), at every sample of the 2,861 Hz series."""
    v = vel_fn(); tf = t0(scan) + (np.arange(nf) + 0.5) * TF / 86400.0
    ifl = N // 2 - (f_rest * (1 - v(tf) / C) - FC) / DF; mid = track(scan, f_rest)[1]
    off_f = (ifl - mid) * DF; tc = (np.arange(nf) + 0.5) * TF
    ts = np.arange(nf * W) / (W * DF); off = np.interp(ts, tc, off_f)
    return 2 * np.pi * np.cumsum(off) / (W * DF)


def dedop(S, Phi):
    """Topocentric selection (nf, W) -> comet-frame spectra: the series multiplied by exp(-iΦ), re-transformed per frame."""
    nf = S.shape[0]; z = series(S) * np.exp(-1j * Phi[:nf * W])
    return np.fft.fftshift(np.fft.fft(z.reshape(nf, W), axis=1), axes=1).astype(np.complex64)


def series(S):
    """(NF, W) spectra (fftshifted, dm.fft convention) -> time series at W·DF Hz, frames concatenated."""
    return np.fft.ifft(np.fft.ifftshift(S, axes=1), axis=1).ravel()


def segspec(z, L):
    B = len(z) // L; return np.fft.fftshift(np.fft.fft(z[:B * L].reshape(B, L), axis=1), axes=1)


def load(scan):
    a = np.load(os.path.join(HERE, f"win_{scan}.npy"), mmap_mode="r"); return a   # (NF, NWIN, 2, WS, 2) float16
