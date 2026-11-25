"""Context for look2_meerkat: the scan of MJD 61006.2608 (2025-11-27 06:15 UT), whose target-beam hits fall near the vessel's
frequencies. Pulls every hit of 2025-11-27 from atlas_hits_2025_11 and describes each scan: hits, beams, drift rates,
spacing, and the drift a transmitter fixed in the comet's frame would show (Horizons).   python3 mk_scan61006.py"""
import json, os, re, zlib, urllib.request, urllib.parse, numpy as np, collections
HERE = os.path.dirname(os.path.abspath(__file__)); C = 299792.458
pat = re.compile(rb'\{"frequency":[^{}]*\}'); key = re.compile(rb'"tstart":61006\.')
r = urllib.request.urlopen("https://bldata.berkeley.edu/ATLAS/MeerKAT/atlas_hits_2025_11.json.gz", timeout=300); dz = zlib.decompressobj(31); buf = b""; H = []
while True:
    c = r.read(1 << 22)
    if not c: break
    buf += dz.decompress(c); last = 0
    for m in pat.finditer(buf):
        last = m.end()
        if key.search(m.group(0)):
            h = json.loads(m.group(0)); H.append((h["tstart"], h["beam"], h["frequency"], h["driftRate"], h["snr"], h["numTimesteps"], h["tsamp"], h["sourceName"]))
    buf = buf[last:]
q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC",
     "SITE_COORD": "'21.4430,-30.7110,1.038'", "START_TIME": "'JD 2461006.70'", "STOP_TIME": "'JD 2461006.85'", "STEP_SIZE": "'1 m'", "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
E = np.array([(float(p[0]) - 2400000.5, float(p[-1])) for p in ([x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines())])
acc = np.gradient(E[:, 1], E[:, 0] * 86400)
out = {"hits_on_61006": len(H), "scans": []}
for ts in sorted({h[0] for h in H}):
    S = [h for h in H if h[0] == ts]; f = np.array(sorted(h[2] for h in S)); dr = np.array([h[3] for h in S]); tm = ts + S[0][5] * S[0][6] / 2 / 86400
    a = float(np.interp(tm, E[:, 0], acc)); v = float(np.interp(tm, E[:, 0], E[:, 1]))
    d = collections.Counter(np.round(dr, 4).tolist()).most_common(6); band = np.histogram(f, np.arange(540, 1760, 50))[0].tolist()
    out["scans"].append({"tstart": ts, "hits": len(S), "beams": len({h[1] for h in S}), "sources": sorted({h[7] for h in S})[:4], "f_range": [float(f[0]), float(f[-1])],
                         "drift_top6": d, "median_spacing_kHz": float(np.median(np.diff(f)) * 1e3), "deldot": v, "expected_drift_Hz_s_at_1420": -1420.5e6 * a / C,
                         "hits_per_50MHz_from_540": band, "snr_median": float(np.median([h[4] for h in S])), "duration_s": S[0][5] * S[0][6]})
    print(json.dumps(out["scans"][-1])[:900], flush=True)
json.dump(out, open(os.path.join(HERE, "mk_scan61006.json"), "w"), indent=1)
