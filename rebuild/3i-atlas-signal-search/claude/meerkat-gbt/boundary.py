"""Boundary search over the MeerKAT 3I/ATLAS hit lists, under the operator's five conditions (artificial; aware of
our blind spots and capacities; precise control of signal as meaning; operating at the boundary of determinability;
meant to be visible as signal to those who know how to look). The search looks inside the classes the pipeline
discards, and every test is run on the target beam and, as a null, on the 63 control beams of the same pointings.

Tests (each a property RFI has no reason to carry and a designed signal could):
  T1 drift-exact   : non-zero drift equal, within one drift step, to the drift a transmitter on 3I/ATLAS shows
                     from MeerKAT (JPL Horizons range-rate, differentiated), whatever band or beam count.
  T2 comet-frame   : the same frequency recurring on two or more days once each hit is corrected to the comet's
                     rest frame (topocentric RFI does not stay fixed in that frame as the comet's velocity changes).
  T3 inside-OH     : narrowband hits inside the comet's own OH lines (1612.231, 1665.402, 1667.359 MHz rest),
                     Doppler-shifted to the comet: a signal hidden in the line MeerKAT detected.
  T4 hydrogen      : hits within 1 kHz of the hydrogen line, and of H/sqrt2 and H/phi, in the comet frame.
    python3 boundary.py"""
import gzip, json, math, os, urllib.parse, urllib.request
import numpy as np, pandas as pd, ijson

HERE = os.path.dirname(os.path.abspath(__file__))
C = 299792.458  # km/s
FILES = ["atlas_hits_2025_11.json.gz", "atlas_hits_2025_12.json.gz"]
KEEP = ["frequency", "driftRate", "snr", "beam", "sourceName", "tstart", "tsamp", "numTimesteps", "filename"]

def load(path):
    cols = {k: [] for k in KEEP}
    for it in ijson.items(gzip.open(path, "rb"), "item", use_float=True):
        for k in KEEP:
            cols[k].append(it.get(k))
    df = pd.DataFrame(cols)
    cats = df["filename"].astype("category")
    names = pd.Series(cats.cat.categories).str.extract(r"(guppi_\d+_\d+_\d+_[^/]+?)_\d{4}\.hits")[0]
    df["pointing"] = cats.map(dict(zip(cats.cat.categories, names))).astype(str)
    return df.drop(columns=["filename"])

cache = os.path.join(HERE, "hits_all.parquet")
if os.path.exists(cache):
    df = pd.read_parquet(cache)
else:
    df = pd.concat([load(os.path.join(HERE, f)) for f in FILES], ignore_index=True)
    df = df.drop_duplicates(subset=["frequency", "driftRate", "beam", "tstart", "pointing"])
    df.to_parquet(cache)
df["tmid"] = df["tstart"] + (df["numTimesteps"].fillna(0) * df["tsamp"].fillna(0) / 2.0) / 86400.0
df["target"] = df["sourceName"].str.contains("atlas", case=False)
df["day"] = df["tstart"].astype(int)
df["pointing_beams"] = df.groupby("pointing")["beam"].transform("nunique")

# --- Horizons: range-rate of 3I/ATLAS from MeerKAT, 1-minute steps over each day's span
def horizons(t0, t1):
    q = {"format": "json", "COMMAND": "'C/2025 N1'", "OBJ_DATA": "NO", "MAKE_EPHEM": "YES", "EPHEM_TYPE": "OBSERVER",
         "CENTER": "'coord@399'", "COORD_TYPE": "GEODETIC", "SITE_COORD": "'21.4430,-30.7110,1.038'",
         "START_TIME": f"'JD {t0 + 2400000.5:.6f}'", "STOP_TIME": f"'JD {t1 + 2400000.5:.6f}'", "STEP_SIZE": "'1 m'",
         "QUANTITIES": "'20'", "CSV_FORMAT": "YES", "TIME_TYPE": "UT", "CAL_FORMAT": "JD"}
    url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q)
    txt = json.load(urllib.request.urlopen(url, timeout=120))["result"]
    body = txt.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines()
    rows = []
    for line in body:
        p = [x.strip() for x in line.split(",") if x.strip()]
        rows.append((float(p[0]) - 2400000.5, float(p[-1])))  # JD -> MJD, deldot km/s
    return np.array(rows)

eph = []
for d, g in df.groupby("day"):
    e = horizons(g["tmid"].min() - 0.01, g["tmid"].max() + 0.01)
    eph.append(e)
E = np.vstack(eph); E = E[np.argsort(E[:, 0])]
t, v = E[:, 0], E[:, 1]
acc = np.gradient(v, t * 86400.0)  # km/s^2
df["deldot"] = np.interp(df["tmid"], t, v)
df["drift_exp"] = -df["frequency"] * 1e6 * np.interp(df["tmid"], t, acc) / C
df["resid"] = df["driftRate"] - df["drift_exp"]
df["f_rest"] = df["frequency"] / (1.0 - df["deldot"] / C)

STEP = 0.0050440  # drift step, Hz/s (from the hit lists)
out = {"hits": int(len(df)), "target_hits": int(df.target.sum()), "days": sorted(int(x) for x in df.day.unique()),
       "deldot_km_s_range": [float(v.min()), float(v.max())]}

def rate(mask):
    tg = df.target & mask; ct = (~df.target) & mask
    nt, nc = int(tg.sum()), int(ct.sum())
    ntot_t, ntot_c = int(df.target.sum()), int((~df.target).sum())
    return {"target": nt, "control": nc, "target_rate": nt / max(ntot_t, 1), "control_rate": nc / max(ntot_c, 1),
            "ratio": (nt / max(ntot_t, 1)) / max(nc / max(ntot_c, 1), 1e-12)}

# T1
t1 = (df.driftRate != 0) & (df.resid.abs() <= STEP)
out["T1_drift_exact"] = rate(t1)
df[df.target & t1].sort_values("snr", ascending=False).to_csv(os.path.join(HERE, "T1_target.csv"), index=False)

# T2: comet-frame recurrence across days, 50 Hz bins (both neighbouring bins)
def recurring(sub):
    b = np.rint(sub["f_rest"] * 1e6 / 50.0).astype("int64")
    s = pd.DataFrame({"b": b, "day": sub["day"].values})
    days = pd.concat([s, s.assign(b=s.b + 1)]).groupby("b").day.nunique()
    keep = set(days[days >= 2].index)
    return sub[b.isin(keep) | (b + 1).isin(keep)]
rt = recurring(df[df.target & (df.driftRate != 0)])
# null: recurrence in the comet frame within control beams, by beam index (each control beam its own series)
nulls = [len(recurring(df[(df.beam == k) & (~df.target) & (df.driftRate != 0)])) for k in range(1, 64)]
out["T2_comet_frame_recurrence"] = {"target_hits_recurring": int(len(rt)), "control_beam_median": float(np.median(nulls)),
                                    "control_beam_max": int(max(nulls)), "control_beams_ge_target": int(sum(n >= len(rt) for n in nulls))}
rt.sort_values("f_rest").to_csv(os.path.join(HERE, "T2_target.csv"), index=False)

# T3: inside the comet's OH lines (rest frequencies, MHz), +-5 kHz in the comet frame
OH = [1612.2310, 1665.4018, 1667.3590]
t3 = np.zeros(len(df), bool)
for f0 in OH:
    t3 |= (df.f_rest - f0).abs().values <= 0.005
out["T3_inside_OH"] = rate(pd.Series(t3, index=df.index))
df[df.target & t3].to_csv(os.path.join(HERE, "T3_target.csv"), index=False)

# T4: hydrogen and two ratios of it, +-1 kHz in the comet frame
H = 1420.405751768
t4 = np.zeros(len(df), bool)
for f0 in [H, H / math.sqrt(2), H / ((1 + math.sqrt(5)) / 2)]:
    t4 |= (df.f_rest - f0).abs().values <= 0.001
out["T4_hydrogen_family"] = rate(pd.Series(t4, index=df.index))
df[df.target & t4].to_csv(os.path.join(HERE, "T4_target.csv"), index=False)

print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "boundary_summary.json"), "w"), indent=1)
