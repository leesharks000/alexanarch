#!/usr/bin/env python3
"""ontrack.py — sub-threshold, ON-beam, comet-tracking search of the ATA 3I/ATLAS session of 2025-07-03 (16 scans).

For a 0.5 MHz unit (one HDF5 chunk column = one coarse channel, 262144 native bins of 1.9073 Hz):
  1. ON beam (beam0000) of all 16 scans read by byte range; every decoded array hashed (sha256 of data and mask bytes).
  2. Each row: baseline = median of 1024-bin blocks, linearly interpolated; r = P/base - 1; z = r / (1.4826 MAD).
     Edge 3% of the coarse channel and the centre +-2 bins are masked (z = 0).
  3. Tracks: rv_k(t) = rv0 + k (rv(t) - rv0), rv from JPL Horizons at the ATA site; k = 1 is the comet; controls
     k in {-3,-2,-1,-0.5,0,0.5,1.5,2,3} (k = 0 fixed in receiver frequency; k = -1 reversed).
     Reference-frame frequency g: f_obs(t) = g (1 - rv_k(t)/c) / (1 - rv0/c), rv0 at the first integration of scan 0.
  4. Per integration, a boxcar of width w_k = 1 + round(|k| * smear) bins (smear = drift per integration) sampled at the
     track; per scan S_s(g) = sum_i B_i / sqrt(19), robust-standardized over the unit.
  5. Stack: T(g) = sum_s clip(S_s, -5, 5) / sqrt(16) (primary: a scan contributes at most 5, so only recurrence
     counts); Traw unclipped. Peaks of T >= 4 kept per track (top 12), with per-scan S_s at the peak.
Scores are empirical units (robust z), not bliss SNR; no Gaussian significance is claimed.
"""
import numpy as np, h5py, fsspec, hashlib, json, time, sys, os, concurrent.futures as cf

C = 299792458.0
# v3 (2026-11-17): the session is chosen by ATA_SESSION (default 20250703); the search is unchanged
SESSIONS = {"20250703": ("2025-07-03-05%3A10%3A38", 60859, 3), "20250708": ("2025-07-08-04%3A52%3A40", 60864, 8),
            "20250709": ("2025-07-09-05%3A20%3A16", 60865, 9), "20250710": ("2025-07-10-05%3A16%3A28", 60866, 10)}
SESS = os.environ.get("ATA_SESSION", "20250703")
_SDIR, _MJD0, _DAY = SESSIONS[SESS]
SESSION = f"https://bldata.berkeley.edu/ATLAS/ATA_ATLAS/{_SDIR}/"
HERE = os.path.dirname(os.path.abspath(__file__))
SCANS = json.load(open(os.path.join(HERE, f"scans-{SESS}.json")))
SCAN_IDS = sorted({x["scan"] for x in SCANS})
HDR = {(x["scan"], x["beam"]): x for x in SCANS}
KS = [1.0, -3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.5, 2.0, 3.0]
NCH = 262144
FOFF = 1.9073486328125e-06 * 1e6   # Hz
TSAMP = 16.777216
SUBS = [f"Lo{t}.C{c:04d}" for t in "ABCD" for c in (352, 544, 736, 928, 1120, 1312, 1504)]
FCH1 = {s: 999.75e6 + i * 96e6 for i, s in enumerate(SUBS)}   # verified from the inventory


def load_rv():
    import re
    from scipy.interpolate import CubicSpline
    t, v = [], []
    txt = open(os.path.join(HERE, f"horizons-{SESS}-ata.txt")).read()
    body = txt.split("$$SOE")[1].split("$$EOE")[0]
    mon = {"Jul": 7}
    for line in body.strip().splitlines():
        p = [x.strip() for x in line.split(",")]
        d, hm = p[0].split()
        y, m, dd = d.split("-"); hh, mm = hm.split(":")
        mjd = _MJD0 + (int(dd) - _DAY) + (int(hh) + int(mm) / 60) / 24
        t.append(mjd); v.append(float(p[-2]) * 1000.0)
    return CubicSpline(np.array(t), np.array(v))


RV = load_rv()
TMID = {sc: HDR[(sc, 0)]["tstart"] + (np.arange(19) + 0.5) * TSAMP / 86400 for sc in SCAN_IDS}
RV0 = float(RV(TMID[SCAN_IDS[0]][0]))
FS = fsspec.filesystem("https")


def url(sc, sub, beam):
    return f"{SESSION}{sc}/{sub}/{sc}-beam000{beam}.fbh5"


def read(sc, sub, beam, c, tries=4):
    u = url(sc, sub, beam)
    for a in range(tries):
        try:
            with FS.open(u, block_size=2 ** 25, cache_type="none") as f:
                h = h5py.File(f, "r")
                x = h["data"][:, 0, c * NCH:(c + 1) * NCH]
                m = h["mask"][:, 0, c * NCH:(c + 1) * NCH]
            rec = {"url": u, "chunk": c, "shape": list(x.shape), "sha256_data": hashlib.sha256(x.tobytes()).hexdigest(),
                   "sha256_mask": hashlib.sha256(m.tobytes()).hexdigest(), "mask_nonzero": int(np.count_nonzero(m)),
                   "finite": bool(np.isfinite(x).all()), "min": float(x.min())}
            return x, rec
        except Exception as e:
            err = repr(e); time.sleep(3 * (a + 1))
    raise RuntimeError(f"read failed {u} c{c}: {err}")


def normalize(P):
    n = P.shape[1]
    blk = np.median(P.reshape(P.shape[0], n // 1024, 1024), axis=2)
    xc = (np.arange(n // 1024) + 0.5) * 1024
    base = np.stack([np.interp(np.arange(n), xc, b) for b in blk])
    r = P / base - 1.0
    e = int(0.03 * n)
    msk = np.zeros(n, bool); msk[:e] = msk[-e:] = True; msk[n // 2 - 2:n // 2 + 3] = True
    med = np.median(r[:, ~msk], axis=1, keepdims=True)
    mad = 1.4826 * np.median(np.abs(r[:, ~msk] - med), axis=1, keepdims=True)
    z = (r - med) / mad
    z[:, msk] = 0.0
    return z.astype(np.float32), msk


def boxcar(z, w):
    if w <= 1:
        return z
    cs = np.cumsum(np.pad(z, ((0, 0), (w // 2 + 1, w - w // 2)), constant_values=0), axis=1, dtype=np.float64)
    out = (cs[:, w:w + z.shape[1]] - cs[:, :z.shape[1]]) / np.sqrt(w)
    return out.astype(np.float32)


def robust(s, valid):
    v = s[valid]; med = np.median(v); mad = 1.4826 * np.median(np.abs(v - med))
    return (s - med) / (mad if mad > 0 else 1.0)


def search(Z, f0, inject=None):
    """Z: dict scan -> z (19 x NCH). Returns per-track stacks and per-scan S."""
    j = np.arange(NCH, dtype=np.float64)
    g = f0 + j * FOFF
    out = {}
    for k in KS:
        S = []
        valid_all = np.ones(NCH, bool)
        for sc in SCAN_IDS:
            rvk = RV0 + k * (RV(TMID[sc]) - RV0)
            ratio = (1 - rvk / C) / (1 - RV0 / C)
            drift = np.abs(np.gradient(f0 * ratio)) if len(ratio) > 1 else 0
            smear = float(np.max(drift)) / FOFF
            w = 1 + int(round(smear))
            B = boxcar(Z[sc], w)
            kk = np.rint(((g[None, :] * ratio[:, None]) - f0) / FOFF).astype(np.int64)
            ok = (kk >= 0) & (kk < NCH)
            valid_all &= ok.all(axis=0)
            kc = np.clip(kk, 0, NCH - 1)
            s = np.take_along_axis(B, kc, axis=1).sum(axis=0) / np.sqrt(19)
            S.append(s)
        S = np.array(S)
        e = int(0.03 * NCH)
        valid = valid_all.copy(); valid[:e] = valid[-e:] = False
        S = np.array([robust(s, valid) for s in S])
        S[:, ~valid] = 0.0
        T = np.clip(S, -5, 5).sum(axis=0) / np.sqrt(len(SCAN_IDS))
        Traw = S.sum(axis=0) / np.sqrt(len(SCAN_IDS))
        T[~valid] = 0; Traw[~valid] = 0
        # v2 (2026-11-17, after 8 units of v1): residual emitted-frequency drift d across the session, and intermittency
        Sc = np.clip(S, -5, 5)
        Tres = T.copy(); dbest = np.zeros(NCH, np.float32)
        for d in DGRID:
            if d == 0:
                continue
            Td = np.zeros(NCH, np.float32)
            for si, sc in enumerate(SCAN_IDS):
                Td += np.roll(Sc[si], -int(round(d * TS[sc] / FOFF)))
            Td /= np.sqrt(len(SCAN_IDS)); Td[~valid] = 0
            better = Td > Tres
            Tres[better] = Td[better]; dbest[better] = d
        half = len(SCAN_IDS) // 2
        Thalf = np.sort(Sc, axis=0)[-half:].sum(axis=0) / np.sqrt(half)
        Thalf[~valid] = 0
        out[k] = (T, Traw, S, valid, Tres, dbest, Thalf)
    return out


# residual drift grid: one native bin over the session span; +-0.01 Hz/s
TS = {sc: float((TMID[sc].mean() - TMID[SCAN_IDS[0]][0]) * 86400) for sc in SCAN_IDS}
_SPAN = max(TS.values())
_DSTEP = FOFF / _SPAN
DGRID = np.arange(-int(0.01 / _DSTEP), int(0.01 / _DSTEP) + 1) * _DSTEP


def peaks(T, thr=4.0, sep=4, top=12):
    idx = np.where(T >= thr)[0]
    if len(idx) == 0:
        return []
    order = idx[np.argsort(-T[idx])]
    sel = []
    for i in order:
        if all(abs(i - s) > sep for s in sel):
            sel.append(int(i))
        if len(sel) >= top:
            break
    return sel


def run_unit(sub, c, beam=0, workers=4, save_dir=None, inject=None):
    f0 = FCH1[sub] + c * 0.5e6
    t0 = time.time()
    with cf.ThreadPoolExecutor(workers) as ex:
        fut = {sc: ex.submit(read, sc, sub, beam, c) for sc in SCAN_IDS}
        raw = {sc: fut[sc].result() for sc in SCAN_IDS}
    tread = time.time() - t0
    ledger = [dict(r[1], scan=sc, sub=sub, beam=beam) for sc, r in raw.items()]
    Z = {}
    for sc, (x, _) in raw.items():
        P = x.astype(np.float64)
        if inject is not None:
            P = inject(P, sc, f0)
        Z[sc], _m = normalize(P)
    del raw
    res = search(Z, f0)
    summ = {"sub": sub, "chunk": c, "beam": beam, "f0_hz": f0, "read_s": round(tread, 1), "proc_s": round(time.time() - t0 - tread, 1),
            "rv0_mps": RV0, "tracks": {}}
    for k, (T, Traw, S, valid) in res.items():
        pk = peaks(T)
        summ["tracks"][str(k)] = {"max_T": float(T.max()), "max_Traw": float(Traw.max()), "n_valid": int(valid.sum()),
                                  "peaks": [{"j": p, "g_hz": f0 + p * FOFF, "T": float(T[p]), "Traw": float(Traw[p]),
                                             "S": [round(float(v), 3) for v in S[:, max(0, p - 1):p + 2].max(axis=1)],
                                             "n_scans_ge3": int((S[:, max(0, p - 1):p + 2].max(axis=1) >= 3).sum()),
                                             "n_pos": int((S[:, p] > 0).sum())} for p in pk]}
    return summ, ledger, res


if __name__ == "__main__":
    sub, c = sys.argv[1], int(sys.argv[2])
    s, l, _ = run_unit(sub, c)
    print(json.dumps({k: v for k, v in s.items() if k != "tracks"}))
    for k, v in s["tracks"].items():
        print(k, round(v["max_T"], 2), round(v["max_Traw"], 2), [(round(p["T"], 2), p["n_scans_ge3"]) for p in v["peaks"][:3]])
