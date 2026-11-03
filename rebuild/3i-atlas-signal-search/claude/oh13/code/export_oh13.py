"""Export the 13 comet-frame candidates of the GBT 1667 MHz OH coarse channel (scans 0013–0018, MJD 61027) with their
coordinates: rest frequency in the comet frame; for each of the six scans the file, time, pointing, the comet's JPL Horizons
position and range-rate, the topocentric frequency and fine-channel index at the first and last time step (the tracked path),
and the tracked z in that scan. Selection (cometframe_raw.py): z >= 2.5 in all three ON scans and < 2.0 in all three OFF scans,
±1 channel tolerance, in the comet frame (offset 0); candidates within 10 Hz merged into one (oh_scan.py's clusters()).
    python3 export_oh13.py   ->  oh13/oh13_candidates.csv, oh13/oh13_candidates.json"""
import sys, json, csv, urllib.parse, urllib.request, importlib.util
import numpy as np
sys.argv = ['x', 'raw/OH', '2.5', '2.0']
spec = importlib.util.spec_from_file_location('cf', 'cometframe_raw.py'); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
rows = cf.coincidences(0.0, keep=True)
cl = []
for r in sorted(rows, key=lambda r: r['f_rest_MHz']):
    if cl and (r['f_rest_MHz'] - cl[-1][-1]['f_rest_MHz']) * 1e6 <= 10: cl[-1].append(r)
    else: cl.append([r])

def radec(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER",
         "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC", "SITE_COORD": "'-79.8398,38.4331,0.807'",
         "START_TIME": f"'JD {t0 + 2400000.5:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'",
         "QUANTITIES": "'1'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD", "ANG_FORMAT": "DEG"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), timeout=120))["result"]
    out = []
    for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines():
        p = [x.strip() for x in l.split(",") if x.strip()]
        nums = [x for x in p[1:] if x.replace('.', '', 1).replace('-', '', 1).isdigit()]
        out.append((float(p[0]) - 2400000.5, float(nums[0]), float(nums[1])))
    return np.array(out)
P = radec(min(cf.H[s]['tstart'] for s in cf.ON + cf.OFF) - 0.005, max(cf.H[s]['tstart'] for s in cf.ON + cf.OFF) + 0.02)
fixed_tone = 1665.615127e6  # topocentric ground tone found in all six scans (spike.py)
out = []
for i, c in enumerate(cl, 1):
    best = max(c, key=lambda r: sum(r[f'z_{s}'] for s in cf.ON))
    F = float(np.mean([r['f_rest_MHz'] for r in c])) * 1e6
    rec = {"id": f"C{i:02d}", "f_rest_Hz": round(F, 3), "f_rest_MHz": round(F / 1e6, 6), "merged_rows": len(c), "scans": []}
    for s in cf.ON + cf.OFF:
        h = cf.H[s]; nt = h['shape'][0]
        t = h['tstart'] + (np.arange(nt) + 0.5) * h['tsamp'] / 86400.0
        v = cf.deldot(t); f0 = h['fch1_cc'] * 1e6
        ftopo = F * (1 - v / cf.C)
        ch = np.rint((ftopo - f0) / cf.foff_hz).astype(int)
        tm = t[nt // 2]
        rec["scans"].append({"scan": s, "role": "ON" if s in cf.ON else "OFF", "file": h['file'],
            "url": "https://bldata.berkeley.edu/ATLAS/GB_ATLAS/" + h['file'], "coarse_channel": h['coarse_channel'],
            "mjd_start": h['tstart'], "mjd_mid": round(float(tm), 7), "tsamp_s": h['tsamp'], "n_steps": nt,
            "pointing_ra_h": h['src_raj'], "pointing_dec_deg": h['src_dej'],
            "comet_ra_deg": round(float(np.interp(tm, P[:, 0], P[:, 1])), 6), "comet_dec_deg": round(float(np.interp(tm, P[:, 0], P[:, 2])), 6),
            "deldot_km_s": round(float(cf.deldot(tm)), 6),
            "f_topo_first_Hz": round(float(ftopo[0]), 3), "f_topo_last_Hz": round(float(ftopo[-1]), 3),
            "chan_in_cc_first": int(ch[0]), "chan_in_cc_last": int(ch[-1]),
            "chan_in_file_first": int(h['coarse_channel'] * h['nchan'] + ch[0]), "chan_in_file_last": int(h['coarse_channel'] * h['nchan'] + ch[-1]),
            "z_tracked": round(float(best[f'z_{s}']), 2)})
    rec["note"] = ("crosses the fixed topocentric tone at 1665.615127 MHz, present in all six scans (ON and OFF): interference"
                   if any(abs(sc['f_topo_first_Hz'] - fixed_tone) < 60 or abs(sc['f_topo_last_Hz'] - fixed_tone) < 60 for sc in rec['scans']) else "")
    out.append(rec)
meta = {"source": "Breakthrough Listen GBT 3I/ATLAS, blc23 rawspec .0000.h5, L-band, scans 0013–0018, MJD 61027 (2025-12-18 UT)",
        "channel": "coarse channel 7 of blc23, 1665.53–1668.46 MHz, 1,048,576 fine channels of 2.794 Hz, 49 steps of 6.08 s per scan",
        "frame": "comet rest frame: f_rest = f_topo / (1 - deldot/c); deldot from JPL Horizons for C/2025 N1 at the GBT site (-79.8398, 38.4331, 0.807 km)",
        "selection": "per scan: each channel divided by its time-median minus 1; 3-channel boxcar; rows rolled along the Horizons path and summed; robust z (MAD) of the tracked spectrum; DC bin of the coarse channel zeroed; ON scans 0013/0015/0017 must each give z >= 2.5 and OFF scans 0014/0016/0018 each z < 2.0 at the same rest frequency, with ±1 channel tolerance; rows within 10 Hz merged",
        "result_context": "13 clusters at the comet frame against 3.75 ± 2.05 for 40 false-drift frames at this cut; no excess at 2.0σ/1.5σ (118 vs 120.9 ± 12.5); 1 at 3σ; the 1665 MHz OH channel shows none at the comet frame (5 vs 5.7 ± 2.2); C01/C02 are the fixed ground tone",
        "candidates": out}
json.dump(meta, open('oh13/oh13_candidates.json', 'w'), indent=1)
with open('oh13/oh13_candidates.csv', 'w', newline='') as f:
    w = csv.writer(f); keys = list(out[0]['scans'][0].keys())
    w.writerow(["id", "f_rest_MHz", "note"] + keys)
    for r in out:
        for sc in r['scans']: w.writerow([r['id'], r['f_rest_MHz'], r['note']] + [sc[k] for k in keys])
for r in out: print(r['id'], r['f_rest_MHz'], [sc['z_tracked'] for sc in r['scans']], r['note'][:30])
