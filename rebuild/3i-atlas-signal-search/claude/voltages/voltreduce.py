"""voltreduce.py — read one coarse channel of the Breakthrough Listen GBT raw voltages (GUPPI RAW, blc23, 3I/ATLAS,
2025-12-18, scans 0013–0018) by HTTP range reads, channelize it, and keep (1) the scan-integrated full-Stokes spectrum
and (2) full-time-resolution full-Stokes windows around each of the 13 comet-frame candidates (../oh13).
Data: https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/ (made available by M. Lebofsky, 2026-11-17).
Nothing is downloaded whole; each 128 MiB block contributes only its 2 MiB slice for the channel.
    python3 voltreduce.py SCAN COARSE_CHANNEL [NFFT_LOG2=19]
GUPPI layout per block: header (80-byte cards to END, padded to 512 when DIRECTIO=1), then OBSNCHAN channels, each
ntime x (Xre, Xim, Yre, Yim) int8. Sky frequency of FFT bin: fc + sign(CHAN_BW)*f_bb (CHAN_BW < 0 here)."""
import sys, json, time, hashlib, urllib.request, concurrent.futures as cf, numpy as np, pathlib, re
BASE = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/"
H = pathlib.Path(__file__).resolve().parent; OUT = H / "out"
SCAN, CH = sys.argv[1], int(sys.argv[2]); LN = int(sys.argv[3]) if len(sys.argv) > 3 else 19; N = 1 << LN
idx = urllib.request.urlopen(BASE, timeout=60).read().decode()
files = sorted(set(re.findall(r'href="(blc23_guppi_\d+_\d+_DIAG_3I_ATLAS_(?:OFF_)?%s\.\d{4}\.raw)"' % SCAN, idx)))
assert files, SCAN
def get(url, a, b, tries=6):
    for k in range(tries):
        try:
            r = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"})
            d = urllib.request.urlopen(r, timeout=120).read()
            if len(d) == b - a + 1: return d
        except Exception as e:
            err = e
        time.sleep(2 + 3 * k)
    raise RuntimeError(f"range {url} {a}-{b}")
def hdr(url, off):
    b = get(url, off, off + 16383); h = {}; i = 0
    while True:
        c = b[i:i + 80].decode("ascii", "replace"); i += 80
        if c.startswith("END"): break
        h[c[:8].strip()] = c[10:].strip().strip("'").strip()
    if int(h.get("DIRECTIO", "0")): i = (i + 511) // 512 * 512
    return h, i
h0, hl0 = hdr(BASE + files[0], 0)
BLOC = int(h0["BLOCSIZE"]); NCH = int(h0["OBSNCHAN"]); TBIN = float(h0["TBIN"]); CBW = float(h0["CHAN_BW"]) * 1e6
FC_TOP = float(h0["OBSFREQ"]) * 1e6 - float(h0["OBSBW"]) * 1e6 / 2 * (1 if CBW < 0 else -1)
fc = float(h0["OBSFREQ"]) * 1e6 + (CH + 0.5 - NCH / 2) * CBW          # centre of coarse channel CH
CHB = BLOC // NCH; NT = CHB // 4
assert NT % N == 0 or N % NT == 0
fbb = np.fft.fftshift(np.fft.fftfreq(N, TBIN)); fsky = fc + np.sign(CBW) * fbb   # per bin
order = np.argsort(fsky); fsky_sorted = fsky[order]
# candidates
cands = []
if CH == 7:
    J = json.load(open(H.parent / "oh13/oh13_candidates.json"))
    for c in J["candidates"]:
        s = [x for x in c["scans"] if x["scan"] == SCAN][0]
        cands.append((c["id"], s["f_topo_first_Hz"], s["f_topo_last_Hz"], s["tsamp_s"], s["n_steps"]))
W = 32
# block list
blocks = []
for f in files:
    url = BASE + f
    size = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=60).headers["Content-Length"])
    h, hl = hdr(url, 0); stride = hl + BLOC
    nb = size // stride
    for b in range(nb): blocks.append((url, b * stride, hl))
nblk = len(blocks); tblk = NT * TBIN
print(SCAN, CH, "files", len(files), "blocks", nblk, "tblk", tblk, "fc", fc, flush=True)
I = np.zeros(N); Q = np.zeros(N); U = np.zeros(N); V = np.zeros(N)
win = np.zeros((len(cands), nblk * max(1, NT // N), 2 * W + 1, 4), np.float32); wf = np.zeros((len(cands), win.shape[1]))
def fetch(k):
    url, off, hl = blocks[k]
    # verify header length on the first block of each file
    if off == 0:
        _, hl2 = hdr(url, 0); assert hl2 == hl
    return k, get(url, off + hl + CH * CHB, off + hl + (CH + 1) * CHB - 1)
t0 = time.time(); done = 0; sha = hashlib.sha256(); row = 0; carry = None
with cf.ThreadPoolExecutor(14) as ex:
    futs = {}
    nxt = 0
    for nxt in range(min(28, nblk)): futs[nxt] = ex.submit(fetch, nxt)
    nxt = min(28, nblk)
    for k in range(nblk):
        _, d = futs.pop(k).result()
        if nxt < nblk: futs[nxt] = ex.submit(fetch, nxt); nxt += 1
        sha.update(d)
        a = np.frombuffer(d, np.int8).reshape(NT, 4).astype(np.float32)
        x = a[:, 0] + 1j * a[:, 1]; y = a[:, 2] + 1j * a[:, 3]
        if carry is not None: x = np.concatenate([carry[0], x]); y = np.concatenate([carry[1], y]); carry = None
        nseg = len(x) // N
        if nseg == 0: carry = (x, y); continue
        for s in range(nseg):
            X = np.fft.fftshift(np.fft.fft(x[s * N:(s + 1) * N])); Y = np.fft.fftshift(np.fft.fft(y[s * N:(s + 1) * N]))
            xx = (X * X.conj()).real; yy = (Y * Y.conj()).real; xy = X * Y.conj()
            I += xx + yy; Q += xx - yy; U += 2 * xy.real; V += -2 * xy.imag
            tmid = (row + 0.5) * N * TBIN
            for ci, (cid, ff, fl, ts, ns) in enumerate(cands):
                f = ff + (fl - ff) * (tmid - ts / 2) / (ts * (ns - 1))
                j = int(np.argmin(np.abs(fsky - f)))
                sl = slice(j - W, j + W + 1)
                if row < win.shape[1]:
                    win[ci, row, :, 0] = xx[sl]; win[ci, row, :, 1] = yy[sl]; win[ci, row, :, 2] = xy.real[sl]; win[ci, row, :, 3] = xy.imag[sl]
                    wf[ci, row] = fsky[j]
            row += 1
        if len(x) > nseg * N: carry = (x[nseg * N:], y[nseg * N:])
        done += 1
        if done % 100 == 0: print(f"{done}/{nblk} {time.time()-t0:.0f}s {done*CHB/1e6/(time.time()-t0):.1f} MB/s", flush=True)
nr = row
stem = f"scan{SCAN}_ch{CH}_n{LN}"
np.savez_compressed(OUT / f"integ_{stem}.npz", I=I.astype(np.float32), Q=Q.astype(np.float32), U=U.astype(np.float32), V=V.astype(np.float32), fsky=fsky, nspec=nr, tbin=TBIN, N=N)
if cands:
    np.savez_compressed(OUT / f"cand_{stem}.npz", win=win[:, :nr], fcen=wf[:, :nr], ids=np.array([c[0] for c in cands]), W=W, df=1 / (N * TBIN), dt=N * TBIN)
meta = {"scan": SCAN, "coarse_channel": CH, "fc_Hz": fc, "nfft": N, "df_Hz": 1 / (N * TBIN), "dt_s": N * TBIN, "nspec": nr, "files": files,
        "blocks": nblk, "sha256_of_channel_bytes": sha.hexdigest(), "header0": {k: h0[k] for k in ("BLOCSIZE","OBSNCHAN","NBITS","NPOL","TBIN","OBSFREQ","OBSBW","CHAN_BW","STT_IMJD","STT_SMJD","SRC_NAME","RA_STR","DEC_STR") if k in h0},
        "seconds": time.time() - t0}
json.dump(meta, open(OUT / f"meta_{stem}.json", "w"), indent=1)
print("done", stem, nr, meta["seconds"], flush=True)
