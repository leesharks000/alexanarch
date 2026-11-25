"""PLAN-WOW3 R1: 3I/ATLAS (C/2025 N1) as seen from Big Ear at the Wow!'s time, and daily 1970-1985. Writes r1.json, r1_horizons_*.txt.
    python3 r1_horizons.py"""
import json, urllib.request, urllib.parse, numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__))
C = 299792.458; H = 1420.40575177
V_REV, V_EHM, DV = C * 0.320 / H, C * 0.0498 / H, C * 0.005 / H
SITE = "'-83.0489,40.2513,0.282'"
WOW = [(291.37917, -26.95), (292.09167, -26.95)]   # J2000: 19h25m31s, 19h28m22s; -26d57'


def q(start, stop, step, tag):
    p = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER",
         "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC", "SITE_COORD": SITE, "START_TIME": f"'{start}'", "STOP_TIME": f"'{stop}'",
         "STEP_SIZE": f"'{step}'", "QUANTITIES": "'1,20'", "CSV_FORMAT": "YES", "CAL_FORMAT": "JD", "ANG_FORMAT": "DEG"}
    txt = json.load(urllib.request.urlopen("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(p), timeout=180))["result"]
    open(os.path.join(HERE, f"r1_horizons_{tag}.txt"), "w").write(txt)
    rows = [[x.strip() for x in l.split(",")] for l in txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()]
    return np.array([[float(r[0]), float(r[3]), float(r[4]), float(r[5]), float(r[6])] for r in rows])  # JD, RA, Dec, delta AU, deldot km/s


def sep(ra1, d1, ra2, d2):
    a, b, c, d = map(np.radians, (ra1, d1, ra2, d2))
    return np.degrees(np.arccos(np.clip(np.sin(b) * np.sin(d) + np.cos(b) * np.cos(d) * np.cos(a - c), -1, 1)))


e = q("1977-08-16 03:16", "1977-08-16 03:17", "1 m", "event")[0]
D = q("1970-01-01", "1985-12-31", "1 d", "daily")
out = {"v_revised_kms": V_REV, "v_ehman_kms": V_EHM, "dv_kms": DV,
       "event": {"jd": e[0], "ra_deg": e[1], "dec_deg": e[2], "delta_au": e[3], "deldot_kms": e[4],
                 "sep_from_wow_horns_deg": [float(sep(e[1], e[2], r, d)) for r, d in WOW]},
       "match_revised": bool(abs(e[4] + V_REV) <= DV), "match_ehman": bool(abs(e[4] + V_EHM) <= DV),
       "daily_1970_1985": {"n": len(D), "deldot_min": float(D[:, 4].min()), "deldot_max": float(D[:, 4].max()),
                           "frac_within_revised": float((np.abs(D[:, 4] + V_REV) <= DV).mean()),
                           "frac_within_ehman": float((np.abs(D[:, 4] + V_EHM) <= DV).mean()),
                           "sep_min_deg": float(min(sep(D[:, 1], D[:, 2], r, d).min() for r, d in WOW)),
                           "frac_sep_le_event": float(np.mean(np.minimum(sep(D[:, 1], D[:, 2], *WOW[0]), sep(D[:, 1], D[:, 2], *WOW[1]))
                                                              <= min(sep(e[1], e[2], r, d) for r, d in WOW)))},
       "deldot_1977": {"min": float(D[(D[:, 0] > 2443144.5) & (D[:, 0] < 2443509.5), 4].min()),
                       "max": float(D[(D[:, 0] > 2443144.5) & (D[:, 0] < 2443509.5), 4].max())}}
json.dump(out, open(os.path.join(HERE, "r1.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
