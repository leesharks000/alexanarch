"""GBT 3I/ATLAS raw voltages, coarse channel 7: delayed-copy and modulation products (PLAN.md v1).
python3 dm.py SCAN [NFRAMES]   e.g. 0013 ; NFRAMES for a pilot (default 833)."""
import sys, os, re, json, time, threading, queue, urllib.request
import numpy as np, scipy.fft as sf
from scipy.ndimage import median_filter

SCANS = {"0013": ("17226", "", "ON"), "0014": ("17543", "_OFF", "OFF"), "0015": ("17861", "", "ON"),
         "0016": ("18179", "_OFF", "OFF"), "0017": ("18497", "", "ON"), "0018": ("18814", "_OFF", "OFF")}
BASE = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/"
HDR, BLK, CH, CHB = 7168, 134217728, 7, 2097152
BSTRIDE = HDR + BLK
N = 1 << 20; NS = 524288          # samples per frame, per block
TBIN = 3.41333333333333e-07; FS = 1 / TBIN; DF = FS / N
FC = 1595.21484375e6 + 93.75e6 - 7.5 * 2.9296875e6   # 1666.9921875 MHz
C = 299792.458
INT = 17
HERE = os.path.dirname(os.path.abspath(__file__))

def url(scan, filei):
    smjd, off, _ = SCANS[scan]
    return f"{BASE}blc23_guppi_61027_{smjd}_DIAG_3I_ATLAS_{scan}.{filei:04d}.raw"

def fetch(scan, b0, nb):
    """Channel-7 payload of blocks b0..b0+nb-1 (all inside one file), as one bytes object."""
    f = b0 // 128; r = []
    for g in range(b0, b0 + nb):
        a = (g % 128) * BSTRIDE + HDR + CH * CHB; r.append(f"{a}-{a + CHB - 1}")
    for attempt in range(6):
        try:
            req = urllib.request.Request(url(scan, f), headers={"Range": "bytes=" + ",".join(r)})
            body = urllib.request.urlopen(req, timeout=120).read()
            if nb == 1:
                assert len(body) == CHB; return body
            out = []; pos = 0
            for m in re.finditer(rb"Content-Range: bytes (\d+)-(\d+)/\d+\r\n\r\n", body):
                a, b = int(m.group(1)), int(m.group(2)); s = m.end(); out.append((a, body[s:s + b - a + 1]))
            out.sort(); assert len(out) == nb and all(len(x[1]) == CHB for x in out), (len(out), nb)
            return b"".join(x[1] for x in out)
        except Exception as e:
            print("retry", scan, b0, e, flush=True); time.sleep(5 * (attempt + 1))
    raise RuntimeError("fetch failed")

def frames(scan, nfr):
    """Yield (j, X, Y) complex64 frames of N samples; prefetch in 16-block groups."""
    nblk = 2 * nfr; groups = []
    b = 0
    while b < nblk:
        n = min(16, nblk - b, 128 - b % 128); groups.append((b, n)); b += n
    q = queue.Queue(maxsize=3)
    def prod():
        for g in groups: q.put((g, fetch(scan, *g)))
        q.put(None)
    threading.Thread(target=prod, daemon=True).start()
    pend = b""; j = 0
    while True:
        it = q.get()
        if it is None: break
        pend += it[1]
        while len(pend) >= 2 * CHB:
            raw = np.frombuffer(pend[:2 * CHB], np.int8).reshape(N, 4); pend = pend[2 * CHB:]
            v = np.maximum(raw.astype(np.float32) / 127.0, -1.0)
            X = (v[:, 0] + 1j * v[:, 1]).astype(np.complex64); Y = (v[:, 2] + 1j * v[:, 3]).astype(np.complex64)
            yield j, X, Y; j += 1

def ephem():
    t = open(os.path.join(HERE, "horizons-gbt-20251218.txt")).read()
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in t.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    E = np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows]); return E

def coords():
    import csv
    rows = list(csv.DictReader(open(os.path.join(HERE, "oh13_candidates.csv"))))
    F = {}
    for r in rows: F[r["id"]] = float(r["f_rest_MHz"]) * 1e6
    ids = sorted(F); fr = [F[i] for i in ids]
    c03 = F["C03"]
    for k in range(1, 51):
        for s in (+1, -1): ids.append(f"K{'+' if s > 0 else '-'}{k:02d}"); fr.append(c03 + s * k * 1e3)
    return ids, np.array(fr)

def fft(x): return sf.fftshift(sf.fft(x, workers=1))

def main(scan, nfr):
    t0s = 61027 + int(SCANS[scan][0]) / 86400.0
    E = ephem(); vel = lambda t: np.interp(t, E[:, 0], E[:, 1])
    ids, FR = coords(); NC = len(FR)
    nint = nfr // INT
    P = {m: np.zeros((nint, N), np.float32) for m in (1, 2, 4)}
    PX = np.zeros(N); PY = np.zeros(N); CXY = np.zeros(N, np.complex128)
    EX = np.zeros(N // 2 + 1); EY = np.zeros(N // 2 + 1)
    G = np.zeros((2, nfr * 16, 512), np.float32)
    M3 = np.zeros((2, NC, 2048))
    TF = N * TBIN
    t_start = time.time()
    for j, X, Y in frames(scan, nfr):
        k = j // INT
        FX = fft(X); FY = fft(Y)
        ax = (FX.real ** 2 + FX.imag ** 2); ay = (FY.real ** 2 + FY.imag ** 2)
        if k < nint: P[1][k] += ax + ay
        PX += ax; PY += ay; CXY += FX * np.conj(FY)
        for m, (x, y) in ((2, (X * X, Y * Y)),):
            F2x = fft(x); F2y = fft(y)
            if k < nint: P[2][k] += F2x.real ** 2 + F2x.imag ** 2 + F2y.real ** 2 + F2y.imag ** 2
            x4 = x * x; y4 = y * y
            F4x = fft(x4); F4y = fft(y4)
            if k < nint: P[4][k] += F4x.real ** 2 + F4x.imag ** 2 + F4y.real ** 2 + F4y.imag ** 2
        ex = sf.rfft(X.real ** 2 + X.imag ** 2, workers=1); ey = sf.rfft(Y.real ** 2 + Y.imag ** 2, workers=1)
        EX += ex.real ** 2 + ex.imag ** 2; EY += ey.real ** 2 + ey.imag ** 2
        for p, z in ((0, X), (1, Y)):
            s = sf.fftshift(sf.fft(z.reshape(1024, 1024), axis=1, workers=1), axes=1)
            pw = (s.real ** 2 + s.imag ** 2).reshape(16, 64, 1024).sum(1).reshape(16, 512, 2).sum(2)
            G[p, j * 16:(j + 1) * 16] = pw
        # M3: local streams at comet-tracked coordinates
        tc = t0s + (j + 0.5) * TF / 86400.0
        f = FR * (1 - vel(tc) / C)
        i0 = np.rint(N // 2 - (f - FC) / DF).astype(int)
        for p, S in ((0, FX), (1, FY)):
            blk = np.stack([S[i - 1024:i + 1024] for i in i0])
            zt = sf.ifft(sf.ifftshift(blk, axes=1), axis=1, workers=1)
            e = sf.fft(zt.real ** 2 + zt.imag ** 2, axis=1, workers=1)
            M3[p] += e.real ** 2 + e.imag ** 2
        if j % 50 == 0: print(scan, j, nfr, f"{time.time() - t_start:.0f}s", flush=True)
    out = os.path.join(HERE, "out", scan); os.makedirs(out, exist_ok=True)
    np.save(f"{out}/PX.npy", PX.astype(np.float32)); np.save(f"{out}/PY.npy", PY.astype(np.float32))
    np.save(f"{out}/CXY.npy", CXY.astype(np.complex64))
    np.save(f"{out}/EX.npy", EX.astype(np.float32)); np.save(f"{out}/EY.npy", EY.astype(np.float32))
    np.save(f"{out}/G.npy", G.astype(np.float16)); np.save(f"{out}/M3.npy", M3.astype(np.float32))
    for m in (1, 2, 4): np.save(f"{out}/Pmean{m}.npy", P[m].mean(0))
    json.dump({"scan": scan, "nframes": nfr, "nint": nint, "ids": ids, "f_rest": FR.tolist(), "t0_mjd": t0s,
               "elapsed_s": time.time() - t_start}, open(f"{out}/meta.json", "w"))
    track(scan, P, t0s, vel, out)

def track(scan, P, t0s, vel, out):
    """M1: comet-frame and 40 false-drift stacks of P1, P2, P4; sparse z>=2 lists."""
    nint = P[1].shape[0]
    t = t0s + (np.arange(nint) * INT + INT / 2) * N * TBIN / 86400.0
    T0 = 61027 + 17226 / 86400.0
    rng = np.random.default_rng(7)
    offs = np.concatenate([[0.0], rng.uniform(0.03, 1.0, 40) * rng.choice([-1, 1], 40) * C / 1.42e9])
    res = {}
    for m in (1, 2, 4):
        x = P[m]
        med = np.median(x, axis=0); med[med <= 0] = 1
        R = x / med - 1.0
        R = R + np.roll(R, 1, axis=1) + np.roll(R, -1, axis=1)
        for fi, dv in enumerate(offs):
            v = vel(t) + dv * (t - T0) * 86400.0
            sh = np.rint(m * FC * (v - v[0]) / C / DF).astype(int)
            acc = np.zeros(N)
            for k in range(nint): acc += np.roll(R[k], -sh[k])
            mm = np.median(acc); s = 1.4826 * np.median(np.abs(acc - mm)); z = (acc - mm) / s
            z[N // 2 - 4:N // 2 + 5] = 0
            idx = np.where(z >= 2.0)[0]
            res[f"m{m}_f{fi}_idx"] = idx.astype(np.int32); res[f"m{m}_f{fi}_z"] = z[idx].astype(np.float16)
            res[f"m{m}_f{fi}_v0"] = np.float64(v[0])
            if m == 1 and fi == 0: np.save(f"{out}/z1_comet.npy", z.astype(np.float32))
    res["offs"] = offs
    np.savez_compressed(f"{out}/M1_sparse.npz", **res)

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 833)
