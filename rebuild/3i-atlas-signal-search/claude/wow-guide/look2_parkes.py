"""Second look under the Wow-as-guide hypothesis (2026-11-24, 22:22 EST, "yes, lets do the last one next"): the vessel's own-frame
frequency (look1.py: 1420.5222 MHz revised, 1420.2518 MHz Ehman) read in the Parkes UWL sessions of 2025-07-31, 09-12 and 10-05.
blc05 (1344-1472 MHz) product .0000 (2 Hz x 15 s), each scan de-Dopplered to the comet frame with the range-rate from Parkes
(Horizons), +-6 kHz around each frequency. S = on 3I/ATLAS, R = reference. A look, not a frozen test: lists what is there.
    python3 look2_parkes.py"""
import json, os, re, struct, urllib.request, urllib.parse, numpy as np, h5py, hdf5plugin, fsspec
from scipy.ndimage import median_filter
HERE = os.path.dirname(os.path.abspath(__file__)); B = "https://bldata.berkeley.edu/ATLAS/"
C = 299792.458; V77 = -43.0112691
F0 = {"revised": 1420.726 / (1 - V77 / C), "ehman": 1420.4556 / (1 - V77 / C)}
SESS = ["PKS_Jul_31_2025", "PKS_Sep_12_2025", "PKS_Oct_05_2025"]; HALF = 3000

def get(url, a, b):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"}), timeout=180).read()

def filhdr(url):
    b = get(url, 0, 2047); i = 0; h = {}
    def rs(i):
        n = struct.unpack('<i', b[i:i + 4])[0]; return b[i + 4:i + 4 + n].decode('latin1'), i + 4 + n
    _, i = rs(0)
    while True:
        k, i = rs(i)
        if k == 'HEADER_END': h['hdr_len'] = i; return h
        if k in ('source_name', 'rawdatafile'): v, i = rs(i)
        elif k in ('telescope_id', 'machine_id', 'data_type', 'nchans', 'nbits', 'nifs', 'nbeams', 'ibeam', 'barycentric', 'pulsarcentric'):
            v = struct.unpack('<i', b[i:i + 4])[0]; i += 4
        else: v = struct.unpack('<d', b[i:i + 8])[0]; i += 8
        h[k] = v

def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'",
         "COORD_TYPE": "GEODETIC", "SITE_COORD": "'148.2635,-32.9984,0.415'", "START_TIME": f"'JD {t0 + 2400000.5 - 0.003:.6f}'",
         "STOP_TIME": f"'JD {t1 + 2400000.5 + 0.02:.6f}'", "STEP_SIZE": "'1 m'", "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    E = np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows]); return lambda t: np.interp(t, E[:, 0], E[:, 1])

out = {"F0_MHz": F0, "sessions": {}}; keep = {}
for s in SESS:
    names = sorted(set(re.findall(r'href="([^"]*\.0000\.(?:fil|h5))"', urllib.request.urlopen(B + s + "/blc05/", timeout=60).read().decode())))
    scans = []
    for n in names:
        u = B + s + "/blc05/" + n
        if n.endswith(".fil"):
            h = filhdr(u); size = int(urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=60).headers["Content-Length"])
            nt = (size - h['hdr_len']) // (4 * h['nchans']); scans.append((n, "fil", h, nt, u))
        else:
            d = h5py.File(fsspec.open(u, "rb", block_size=4 << 20).open(), "r")["data"]; a = d.attrs
            h = {k: float(a[k]) for k in ("fch1", "foff", "tsamp", "tstart")}; h["nchans"] = d.shape[2]; scans.append((n, "h5", h, d.shape[0], d))
    scans = [x for x in scans if x[3] > 0]
    vel = horizons(min(x[2]["tstart"] for x in scans), max(x[2]["tstart"] for x in scans)); S = {"scans": []}
    for n, kind, h, nt, src in scans:
        role = "S" if "_S_" in n else "R"; fch1, foff, ts = h["fch1"], h["foff"], h["tsamp"]
        t = h["tstart"] + (np.arange(nt) + 0.5) * ts / 86400.0; v = vel(t); rec = {"file": n, "role": role, "nt": int(nt), "deldot_kms": [float(v[0]), float(v[-1])], "targets": {}}
        for name, f0 in F0.items():
            ch = np.rint((f0 * (1 - v / C) - fch1) / foff).astype(int); W = np.empty((nt, 2 * HALF + 1), np.float32)
            for k in range(nt):
                lo = ch[k] - HALF
                if kind == "fil":
                    a0 = h['hdr_len'] + (k * h['nchans'] + lo) * 4; W[k] = np.frombuffer(get(src, a0, a0 + (2 * HALF + 1) * 4 - 1), '<f4')
                else: W[k] = src[k, 0, lo:lo + 2 * HALF + 1]
            W = W / np.median(W, 1, keepdims=True); shape = median_filter(np.median(W, 0), 201, mode="nearest"); R = W / shape - 1
            sig = 1.4826 * np.median(np.abs(R - np.median(R))); Z = R / sig; line = Z.mean(0) * np.sqrt(nt)
            off = (np.arange(2 * HALF + 1) - HALF) * abs(foff) * 1e6; top = np.argsort(line)[-5:][::-1]; pix = np.argwhere(Z >= 5)
            rec["targets"][name] = {"f_topo_MHz": float(f0 * (1 - v[0] / C)), "line_max_z": float(line.max()), "line_top5": [(float(off[i]), float(line[i])) for i in top],
                                    "pixels_ge5": int(len(pix)), "pixels_expected_gauss": float(Z.size * 2.87e-7), "pix_max_z": float(Z.max()),
                                    "pix_top5": [(int(a), float(off[b]), float(Z[a, b])) for a, b in pix[np.argsort(Z[pix[:, 0], pix[:, 1]])[-5:][::-1]]] if len(pix) else []}
            keep[f"{s}|{n[6:17]}|{role}|{name}"] = Z.astype(np.float16)
            print(s, n[6:17], role, name, "nt", nt, "line max %.1f at %+.0f Hz" % (line.max(), off[top[0]]), "pix>=5: %d (max %.1f)" % (len(pix), Z.max()), flush=True)
        S["scans"].append(rec)
    out["sessions"][s] = S
json.dump(out, open(os.path.join(HERE, "look2_parkes.json"), "w"), indent=1); np.savez_compressed(os.path.join(HERE, "look2_parkes.npz"), **keep)
