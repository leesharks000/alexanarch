"""Frozen Parkes test of the oh13 frequencies (pks/PLAN.md, sha256 336fcb1a...). Reads only +-16 kHz around each target from each scan by HTTP range,
then applies the plan's detector. python3 pks/pks13.py"""
import json, struct, urllib.request, urllib.parse, csv, numpy as np
B = "https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/blc07/"
SC = [("S", "guppi_60887_50760_6690867462_3IATLAS_S_0001.0000.fil"), ("R", "guppi_60887_51102_6690868766_3IATLAS_R_0001.0000.fil"),
      ("S", "guppi_60887_51442_6690870063_3IATLAS_S_0001.0000.fil"), ("R", "guppi_60887_51782_6690871360_3IATLAS_R_0001.0000.fil"),
      ("S", "guppi_60887_52123_6690872661_3IATLAS_S_0001.0000.fil"), ("R", "guppi_60887_52472_6690873992_3IATLAS_R_0001.0000.fil")]
C = 299792.458
T = {r["id"]: float(r["f_rest_MHz"]) * 1e6 for r in csv.DictReader(open("oh13/oh13_candidates.csv"))}
HALF = 8000  # channels each side (+-16 kHz)

def get(url, a, b):
    r = urllib.request.Request(url, headers={"Range": f"bytes={a}-{b}"}); return urllib.request.urlopen(r, timeout=120).read()

def header(url):
    b = get(url, 0, 2047); i = 0
    def rs(i):
        n = struct.unpack('<i', b[i:i + 4])[0]; return b[i + 4:i + 4 + n].decode('latin1'), i + 4 + n
    _, i = rs(0); h = {}
    while True:
        k, i = rs(i)
        if k == 'HEADER_END': h['hdr_len'] = i; return h
        if k in ('source_name', 'rawdatafile'): v, i = rs(i)
        elif k in ('telescope_id', 'machine_id', 'data_type', 'nchans', 'nbits', 'nifs', 'nbeams', 'ibeam', 'barycentric', 'pulsarcentric'):
            v = struct.unpack('<i', b[i:i + 4])[0]; i += 4
        else: v = struct.unpack('<d', b[i:i + 8])[0]; i += 8
        h[k] = v

H = [header(B + f) for _, f in SC]
nt = [20] * 6
t0 = min(h['tstart'] for h in H); t1 = max(h['tstart'] for h in H) + 0.01
q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
     "SITE_COORD": "'148.2635,-32.9984,0.415'", "START_TIME": f"'JD {t0 + 2400000.5 - 0.003:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'",
     "STEP_SIZE": "'1 m'", "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
rows = [[x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
E = np.array([(float(r[0]) - 2400000.5, float(r[-1])) for r in rows])
dd = lambda t: np.interp(t, E[:, 0], E[:, 1])
print("deldot at Parkes %.3f .. %.3f km/s" % (E[:, 1].min(), E[:, 1].max()), "nbits", H[0]['nbits'], "tsamp", H[0]['tsamp'], flush=True)

res = {"plan_sha256": "336fcb1a601ea6dd91805ecf996b99ab306d71b9199992b98c9a12889df6dbaf", "deldot_km_s": [float(E[:, 1].min()), float(E[:, 1].max())], "targets": {}}
for cid, F in sorted(T.items()):
    zs = []  # per scan: z spectrum on a common rest grid (offsets in channels from F)
    for (role, f), h in zip(SC, H):
        foff = h['foff'] * 1e6; fch1 = h['fch1'] * 1e6; n = h['nchans']; ts = h['tsamp']
        t = h['tstart'] + (np.arange(20) + 0.5) * ts / 86400.0; v = dd(t)
        ftop = F * (1 - v / C); ch = np.rint((ftop - fch1) / foff).astype(int)
        lo = int(ch.min()) - HALF; hi = int(ch.max()) + HALF
        X = np.zeros((20, hi - lo), np.float32)
        for k in range(20):
            a = h['hdr_len'] + (k * n + lo) * 4
            X[k] = np.frombuffer(get(B + f, a, a + (hi - lo) * 4 - 1), '<f4')
        med = np.median(X, 0); med[med == 0] = 1
        r = X / med - 1.0; r = r + np.roll(r, 1, 1) + np.roll(r, -1, 1)
        acc = np.zeros(2 * HALF)
        for k in range(20):
            s0 = ch[k] - lo - HALF; acc += r[k, s0:s0 + 2 * HALF]
        m = np.median(acc); sd = 1.4826 * np.median(np.abs(acc - m)); z = (acc - m) / sd
        zs.append((role, z))
    S = np.array([z for ro, z in zs if ro == "S"]); R = np.array([z for ro, z in zs if ro == "R"])
    mf = lambda a: np.maximum(np.maximum(a, np.roll(a, 1, -1)), np.roll(a, -1, -1))
    Sm, Rm = mf(S), mf(R)
    chw = abs(H[0]['foff'] * 1e6)
    def window(center_hz, half_hz):
        c = HALF + int(round(center_hz / chw)); w = int(round(half_hz / chw))
        sl = slice(c - w, c + w + 1)
        smin = Sm[:, sl].min(0); rmax = Rm[:, sl].max(0)
        flag = bool(np.any((smin >= 2.5) & (rmax < 2.0)))
        j = int(np.argmax(smin)); return flag, float(smin[j]), float(rmax[j]), [round(float(x), 2) for x in Sm[:, sl][:, j]], [round(float(x), 2) for x in Rm[:, sl][:, j]]
    out = {}
    for name, half in (("strict_5Hz", 5.0), ("wide_100Hz", 100.0)):
        fl, smin, rmax, sv, rv = window(0.0, half)
        ctrl = [window(k * 250.0 * sg, half) for k in range(1, 51) for sg in (1, -1)]
        out[name] = {"flag": fl, "best_min_S": round(smin, 3), "R_at_best": round(rmax, 3), "S_scores": sv, "R_scores": rv,
                     "controls_flagged": sum(c[0] for c in ctrl), "controls_min_S_ge_target": sum(c[1] >= smin for c in ctrl)}
    res["targets"][cid] = {"f_rest_MHz": F / 1e6, **out}
    print(cid, F / 1e6, {k: {kk: out[k][kk] for kk in ("flag", "best_min_S", "R_at_best", "controls_flagged", "controls_min_S_ge_target")} for k in out}, flush=True)
json.dump(res, open("pks/pks13.json", "w"), indent=1)
