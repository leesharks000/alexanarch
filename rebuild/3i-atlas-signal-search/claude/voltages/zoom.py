"""zoom.py — full-Stokes waterfalls of chosen frequency ranges from the raw voltages of one scan, one coarse channel.
    python3 zoom.py SCAN CH LABEL F_LO_MHz F_HI_MHz [NAVG=4] [NFFT_LOG2=19]
Each spectrum is 2^NFFT_LOG2 points (0.179 s, 5.59 Hz at 19); NAVG consecutive spectra are averaged (0.716 s at 4).
Writes out/zoom_LABEL_scanSCAN.npz with XX, YY, ReXY, ImXY (time x freq), the sky frequency axis and the time step."""
import sys, re, time, urllib.request, concurrent.futures as cf, numpy as np, pathlib, json, hashlib
BASE = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/"; OUT = pathlib.Path(__file__).resolve().parent / "out"
SCAN, CH, LAB, FLO, FHI = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4]) * 1e6, float(sys.argv[5]) * 1e6
NAVG = int(sys.argv[6]) if len(sys.argv) > 6 else 4; N = 1 << (int(sys.argv[7]) if len(sys.argv) > 7 else 19)
idx = urllib.request.urlopen(BASE, timeout=60).read().decode()
files = sorted(set(re.findall(r'href="(blc23_guppi_\d+_\d+_DIAG_3I_ATLAS_(?:OFF_)?%s\.\d{4}\.raw)"' % SCAN, idx)))
def get(url, a, b):
    for k in range(6):
        try:
            d = urllib.request.urlopen(urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"}), timeout=120).read()
            if len(d) == b - a + 1: return d
        except Exception: pass
        time.sleep(2 + 3 * k)
    raise RuntimeError(url)
def hdr(url):
    b = get(url, 0, 16383); h = {}; i = 0
    while True:
        c = b[i:i + 80].decode("ascii", "replace"); i += 80
        if c.startswith("END"): break
        h[c[:8].strip()] = c[10:].strip().strip("'").strip()
    return h, ((i + 511) // 512 * 512 if int(h.get("DIRECTIO", "0")) else i)
h0, _ = hdr(BASE + files[0]); BLOC = int(h0["BLOCSIZE"]); NCH = int(h0["OBSNCHAN"]); TBIN = float(h0["TBIN"]); CBW = float(h0["CHAN_BW"]) * 1e6
fc = float(h0["OBSFREQ"]) * 1e6 + (CH + 0.5 - NCH / 2) * CBW; CHB = BLOC // NCH; NT = CHB // 4
fsky = fc + np.sign(CBW) * np.fft.fftshift(np.fft.fftfreq(N, TBIN)); sel = np.where((fsky >= FLO) & (fsky <= FHI))[0]
o = np.argsort(fsky[sel]); sel = sel[o]
blocks = []
for f in files:
    url = BASE + f; size = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=60).headers["Content-Length"])
    h, hl = hdr(url); st = hl + BLOC
    blocks += [(url, b * st + hl) for b in range(size // st)]
rows = []; acc = np.zeros((4, len(sel))); na = 0; carry = None; sha = hashlib.sha256()
def fetch(k): url, off = blocks[k]; return get(url, off + CH * CHB, off + (CH + 1) * CHB - 1)
with cf.ThreadPoolExecutor(12) as ex:
    for d in ex.map(fetch, range(len(blocks))):
        sha.update(d); a = np.frombuffer(d, np.int8).reshape(NT, 4).astype(np.float32)
        x = a[:, 0] + 1j * a[:, 1]; y = a[:, 2] + 1j * a[:, 3]
        if carry is not None: x = np.concatenate([carry[0], x]); y = np.concatenate([carry[1], y]); carry = None
        ns = len(x) // N
        for s in range(ns):
            X = np.fft.fftshift(np.fft.fft(x[s * N:(s + 1) * N]))[sel]; Y = np.fft.fftshift(np.fft.fft(y[s * N:(s + 1) * N]))[sel]
            xy = X * Y.conj(); acc += np.array([(X * X.conj()).real, (Y * Y.conj()).real, xy.real, xy.imag]); na += 1
            if na == NAVG: rows.append(acc / NAVG); acc = np.zeros_like(acc); na = 0
        if len(x) > ns * N: carry = (x[ns * N:], y[ns * N:])
R = np.array(rows, np.float32)
np.savez_compressed(OUT / f"zoom_{LAB}_scan{SCAN}.npz", XX=R[:, 0], YY=R[:, 1], ReXY=R[:, 2], ImXY=R[:, 3], fsky=fsky[sel], dt=N * TBIN * NAVG, df=1 / (N * TBIN))
json.dump({"scan": SCAN, "ch": CH, "label": LAB, "f_lo": FLO, "f_hi": FHI, "navg": NAVG, "nfft": N, "rows": len(rows), "sha256_of_channel_bytes": sha.hexdigest()}, open(OUT / f"zoom_{LAB}_scan{SCAN}.json", "w"), indent=1)
print("done", LAB, SCAN, R.shape)
