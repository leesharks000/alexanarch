"""Sweep a MeerKAT seticore hit list for 3I/ATLAS: keep every hit in the target beam, test each against
the other beams of the same pointing (a hit seen in no other beam is "localized"), tag known satellite
allocations, and compare the drift with the drift a transmitter riding on 3I/ATLAS would show from
MeerKAT (Earth-rotation term; the comet's own acceleration is negligible).
    python3 sweep.py <hits.json.gz> <out_prefix>"""
import gzip, json, sys, math
import numpy as np, pandas as pd

src, out = sys.argv[1], sys.argv[2]
FOFF = 1.5944242477416992e-6  # MHz per fine channel
LAT, LON = math.radians(-30.7110), 21.4430  # MeerKAT
R_E, OMEGA, C = 6.371e6, 7.2921159e-5, 299792458.0
BANDS = [("GPS L5/Galileo E5a", 1164.0, 1189.0), ("Galileo E5b/BeiDou B2", 1189.0, 1214.0),
         ("GPS L2", 1215.0, 1240.0), ("GLONASS L2", 1240.0, 1260.0), ("BeiDou B3/Galileo E6", 1260.0, 1300.0),
         ("GPS L3", 1376.0, 1386.0), ("Inmarsat/MSS down", 1525.0, 1559.0), ("GPS L1/Galileo E1", 1563.0, 1587.0),
         ("GLONASS L1", 1593.0, 1610.0), ("Globalstar", 1610.0, 1618.725), ("Iridium", 1616.0, 1626.5),
         ("MSS up", 1626.5, 1660.5), ("DME/ADS-B/aero", 960.0, 1164.0)]

def band(f):
    for n, lo, hi in BANDS:
        if lo <= f <= hi:
            return n
    return ""

def lst_deg(mjd):
    d = mjd - 51544.5
    return (280.46061837 + 360.98564736629 * d + LON) % 360.0

def expected_drift(f_mhz, mjd, ra_h, dec_d):
    ha = math.radians((lst_deg(mjd) - ra_h * 15.0 + 540.0) % 360.0 - 180.0)
    dec = math.radians(dec_d)
    a = OMEGA ** 2 * R_E * math.cos(LAT) * math.cos(dec) * math.cos(ha)  # m/s^2 toward observer term
    return f_mhz * 1e6 * a / C, math.degrees(ha) / 15.0

import ijson
KEEP = ["frequency", "driftRate", "snr", "beam", "sourceName", "tstart", "ra", "dec", "filename"]
cols = {k: [] for k in KEEP}
for it in ijson.items(gzip.open(src, "rb"), "item", use_float=True):
    for k in KEEP:
        cols[k].append(it.get(k))
df = pd.DataFrame(cols); del cols
df["filename"] = df["filename"].astype("category")
pt = df["filename"].cat.categories.str.extract(r"(guppi_\d+_\d+_\d+_[^/]+?)_\d{4}\.hits")[0]
df["pointing"] = pd.Categorical.from_codes(df["filename"].cat.codes, categories=pd.Index(pt.fillna(pd.Series(df["filename"].cat.categories))).unique()) if False else df["filename"].map(dict(zip(df["filename"].cat.categories, pt.fillna(pd.Series(df["filename"].cat.categories))))).astype(str)
df["pointing_beams"] = df.groupby("pointing")["beam"].transform("nunique")
df["ch"] = np.rint(df["frequency"] / FOFF).astype("int64")
tgt_mask = df["sourceName"].str.contains("atlas", case=False)
a, o = df[tgt_mask].copy(), df[~tgt_mask]
nb, mx = [], []
for p, ga in a.groupby("pointing"):
    go = o[o.pointing == p].sort_values("ch")
    chs, beams, snrs = go["ch"].values, go["beam"].values, go["snr"].values
    for r in ga.itertuples():
        lo = np.searchsorted(chs, r.ch - 20); hi = np.searchsorted(chs, r.ch + 20, side="right")
        nb.append((r.Index, len(set(beams[lo:hi])), float(snrs[lo:hi].max()) if hi > lo else 0.0))
a = a.join(pd.DataFrame(nb, columns=["i", "nbeams_other", "maxsnr_other"]).set_index("i"))
a["band"] = a["frequency"].map(band)
ed = [expected_drift(f, t, ra, de) for f, t, ra, de in zip(a.frequency, a.tstart, a.ra, a.dec)]
a["drift_expected"] = [x[0] for x in ed]; a["hour_angle_h"] = [x[1] for x in ed]
a["drift_resid"] = a["driftRate"] - a["drift_expected"]
a.drop(columns=["filename"]).to_parquet(out + "_target.parquet")
summary = {"file": src, "hits_total": len(df), "target_hits": int(len(a)),
           "beams": int(df["beam"].nunique()), "pointings": int(df["pointing"].nunique()),
           "mjd_range": [float(df.tstart.min()), float(df.tstart.max())],
           "target_names": sorted(a["sourceName"].unique().tolist()),
           "pointings_testable(>=32 beams)": int(a.loc[a.pointing_beams >= 32, "pointing"].nunique()),
           "target_hits_testable": int((a.pointing_beams >= 32).sum()),
           "target_hits_untestable(single-beam pointings)": int((a.pointing_beams < 32).sum()),
           "localized": int(((a.nbeams_other == 0) & (a.pointing_beams >= 32)).sum()),
           "localized_nonzero_drift": int(((a.nbeams_other == 0) & (a.pointing_beams >= 32) & (a.driftRate != 0)).sum()),
           "localized_outside_bands": int(((a.nbeams_other == 0) & (a.pointing_beams >= 32) & (a.band == "")).sum()),
           "localized_drift_matches_expected": int(((a.nbeams_other == 0) & (a.pointing_beams >= 32) & (a.driftRate != 0) & (a.drift_resid.abs() <= 0.02)).sum())}
print(json.dumps(summary, indent=1))
json.dump(summary, open(out + "_summary.json", "w"), indent=1)
