"""The vessel's own-frame frequency (look1.py) in the public MeerKAT 3I/ATLAS hit lists (seticore, SNR >= 6; Nov and Dec 2025).
Streams the four lists, keeps every hit between 1419.5 and 1421.5 MHz in any beam, takes each to the comet frame with the
range-rate from MeerKAT (Horizons), and lists the hits within +-10 kHz of 1420.5222 (revised) and 1420.2518 (Ehman), target
beam and other beams apart. A look, not a frozen test.   python3 look2_meerkat.py"""
import json, os, re, zlib, urllib.request, urllib.parse, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); B = "https://bldata.berkeley.edu/ATLAS/MeerKAT/"
C = 299792.458; V77 = -43.0112691
F0 = {"revised": 1420.726 / (1 - V77 / C), "ehman": 1420.4556 / (1 - V77 / C)}
LISTS = ["atlas_hits", "atlas_hits_2025_11", "atlas_hits_2025_11_dups", "atlas_hits_2025_12"]
pat = re.compile(rb'\{"frequency":([0-9.eE+-]+),[^{}]*\}')
hits = []; total = {}
for L in LISTS:
    r = urllib.request.urlopen(B + L + ".json.gz", timeout=300); dz = zlib.decompressobj(31); buf = b""; n = 0
    while True:
        c = r.read(1 << 22)
        if not c: break
        buf += dz.decompress(c); last = 0
        for m in pat.finditer(buf):
            n += 1; last = m.end()
            if 1419.5 <= float(m.group(1)) <= 1421.5:
                h = json.loads(m.group(0)); h["list"] = L; h.pop("filename", None); hits.append(h)
        buf = buf[last:]
    total[L] = n; print(L, n, "hits;", len(hits), "kept so far", flush=True)
def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER", "CENTER": "'coord@399'",
         "COORD_TYPE": "GEODETIC", "SITE_COORD": "'21.4430,-30.7110,1.038'", "START_TIME": f"'JD {t0 + 2400000.5:.6f}'",
         "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'", "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    return [(float(p[0]) - 2400000.5, float(p[-1])) for p in ([x.strip() for x in l.split(",") if x.strip()] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines())]
for h in hits: h["tmid"] = h["tstart"] + h.get("numTimesteps", 0) * h.get("tsamp", 0) / 2 / 86400
E = []
for d in sorted({int(h["tmid"]) for h in hits}):
    ts = [h["tmid"] for h in hits if int(h["tmid"]) == d]; E += horizons(min(ts) - 0.01, max(ts) + 0.01)
E = np.array(sorted(E))
for h in hits:
    h["deldot"] = float(np.interp(h["tmid"], E[:, 0], E[:, 1])); h["f_comet"] = h["frequency"] / (1 - h["deldot"] / C)
    h["target"] = "atlas" in h["sourceName"].lower()
out = {"F0_MHz": F0, "lists": total, "kept_1419.5_1421.5": len(hits), "kept_target_beam": sum(h["target"] for h in hits),
       "days": sorted({int(h["tmid"]) for h in hits}), "deldot_range": [float(E[:, 1].min()), float(E[:, 1].max())], "near": {}}
for name, f0 in F0.items():
    nb = sorted([h for h in hits if abs(h["f_comet"] - f0) <= 0.010], key=lambda h: h["tmid"])
    out["near"][name] = {"target_beam": [h for h in nb if h["target"]], "other_beams_count": sum(not h["target"] for h in nb),
                         "other_beams": [h for h in nb if not h["target"]][:200]}
    print(name, "%.4f" % f0, "target-beam hits within 10 kHz:", len(out["near"][name]["target_beam"]), "other beams:", out["near"][name]["other_beams_count"])
fc = np.array([h["f_comet"] for h in hits]); tg = np.array([h["target"] for h in hits]); edges = np.arange(1419.5, 1421.5001, 0.02)
out["hist_20kHz"] = {"edges_MHz": [1419.5, 1421.5, 0.02], "target": np.histogram(fc[tg], edges)[0].tolist(), "other": np.histogram(fc[~tg], edges)[0].tolist()}
json.dump(out, open(os.path.join(HERE, "look2_meerkat.json"), "w"), indent=1)
json.dump(hits, open(os.path.join(HERE, "look2_meerkat_hits.json"), "w"))
