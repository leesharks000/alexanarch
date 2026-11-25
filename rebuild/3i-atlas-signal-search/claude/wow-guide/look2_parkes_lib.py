"""Readers shared by look2_parkes_ctrl.py (the same header parser, Horizons call and normalisation as look2_parkes.py)."""
import json, struct, urllib.request, urllib.parse, numpy as np
from scipy.ndimage import median_filter
C = 299792.458; V77 = -43.0112691; HALF = 3000
F0 = {"revised": 1420.726 / (1 - V77 / C), "ehman": 1420.4556 / (1 - V77 / C)}
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


def zmap(W):
    W = W / np.median(W, 1, keepdims=True); shape = median_filter(np.median(W, 0), 201, mode="nearest"); R = W / shape - 1
    return R / (1.4826 * np.median(np.abs(R - np.median(R))))
