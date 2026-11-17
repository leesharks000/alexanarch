"""baseband.py — the C03 band as a complex voltage time series, both polarizations, one scan.
Each block's 2 MiB slice of coarse channel 7 is mixed down so that the topocentric frequency F0 sits at 0 Hz,
then boxcar-averaged over 4096 samples (output rate 2.9296875 MHz / 4096 = 715.26 Hz, band about ±357 Hz,
boxcar first null at 715 Hz). The phase of the mixer runs continuously across blocks and files.
    python3 baseband.py SCAN F0_MHz LABEL
Writes out/bb_LABEL_scanSCAN.npz (x, y complex64; fs; F0; t0 = scan start)."""
import sys, re, time, urllib.request, concurrent.futures as cf, numpy as np, pathlib, json, hashlib
BASE = "https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/"; OUT = pathlib.Path(__file__).resolve().parent / "out"
SCAN, F0, LAB = sys.argv[1], float(sys.argv[2]) * 1e6, sys.argv[3]; CH = 7; DEC = 4096
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
fbb = (F0 - fc) / np.sign(CBW)          # baseband frequency of F0 (sky = fc + sign(CBW) * fbb)
blocks = []
for f in files:
    url = BASE + f; size = int(urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=60).headers["Content-Length"])
    h, hl = hdr(url); st = hl + BLOC; blocks += [(url, b * st + hl) for b in range(size // st)]
def fetch(k): url, off = blocks[k]; return get(url, off + CH * CHB, off + (CH + 1) * CHB - 1)
X = []; Y = []; n0 = 0; sha = hashlib.sha256(); assert NT % DEC == 0
w = 2 * np.pi * fbb * TBIN
with cf.ThreadPoolExecutor(12) as ex:
    for d in ex.map(fetch, range(len(blocks))):
        sha.update(d); a = np.frombuffer(d, np.int8).reshape(NT, 4).astype(np.float32)
        ph = np.exp(-1j * ((w * (n0 + np.arange(NT))) % (2 * np.pi))).astype(np.complex64)
        x = (a[:, 0] + 1j * a[:, 1]) * ph; y = (a[:, 2] + 1j * a[:, 3]) * ph
        X.append(x.reshape(-1, DEC).mean(1).astype(np.complex64)); Y.append(y.reshape(-1, DEC).mean(1).astype(np.complex64)); n0 += NT
x = np.concatenate(X); y = np.concatenate(Y)
np.savez_compressed(OUT / f"bb_{LAB}_scan{SCAN}.npz", x=x, y=y, fs=1 / (TBIN * DEC), F0=F0, fbb=fbb, tbin=TBIN)
json.dump({"scan": SCAN, "label": LAB, "F0_Hz": F0, "fs_Hz": 1 / (TBIN * DEC), "n": len(x), "sha256_of_channel_bytes": sha.hexdigest()}, open(OUT / f"bb_{LAB}_scan{SCAN}.json", "w"), indent=1)
print("done", LAB, SCAN, len(x))
