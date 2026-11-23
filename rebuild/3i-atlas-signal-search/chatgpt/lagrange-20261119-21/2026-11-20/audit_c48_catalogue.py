#!/usr/bin/env python3
"""Reproduce catalogue-only cc48 audit. No raw-voltage claims.
Original 2026-11-19 frozen M4b event JSON, user-selected follow-up 2026-11-20.
"""
import json, urllib.request, statistics
BASE=("https://raw.githubusercontent.com/leesharks000/alexanarch/main/"
      "rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/")
def load(p):
    with urllib.request.urlopen(BASE+p,timeout=30) as f: return json.load(f)
d=load("M4b/events/cc48.json")
events=d["events"]; control=d["control_top"]
lo,hi=1547.65,1547.80  # exploratory, selected after viewing original catalogue
band=lambda rows:[e for e in rows if lo<=e["mhz_topo"]<=hi]
on_band,off_band=band(events),band(control)
selA=[e for e in events if e["cls"]=="A"]
threshold={}
for h in [5,4.5,4,3.5,3,2.5,2]:
    threshold[str(h)]=sum(max(e["off_along"].values())<h
                          and min(e["on_along"].values())>=5 for e in selA)
freq_offsets=[]
for e in on_band:
    q=min(off_band,key=lambda x:abs(x["mhz_topo"]-e["mhz_topo"]))
    freq_offsets.append((q["mhz_topo"]-e["mhz_topo"])*1e6)
res=dict(
    warning="Bounded catalogue diagnostic, not comet-drift localization; "
            "40 strongest ON events and 15 strongest OFF events only",
    channel=48,frequency_center_mhz=d["fc_mhz"],
    full_counts={"A":d["n"]["A"],"reverse_A":d["control_n"]["A"]},
    saved={"ON":len(events),"reverse_OFF":len(control)},
    drift_zero_saved=sum(e["hz_per_s"]==0 for e in events),
    selected_interval_mhz=[lo,hi],
    ON_saved_in_interval=len(on_band),reverse_OFF_saved_in_interval=len(off_band),
    ON_interval_scan_counts={s:sum(e["scan"]==s for e in on_band)
                             for s in ("0013","0015","0017")},
    OFF_interval_scan_counts={s:sum(e["scan"]==s for e in off_band)
                              for s in ("0014","0016","0018")},
    ON_z_mean=statistics.mean(e["z_local"] for e in on_band),
    OFF_z_mean=statistics.mean(e["z_local"] for e in off_band),
    nearest_OFF_separation_Hz=freq_offsets,
    nearest_OFF_count_within_Hz={str(h):sum(abs(v)<=h for v in freq_offsets)
                                 for h in (100,500,1000,2000,5000,10000)},
    retained_A_survive_off_veto=threshold,
    n_retained_A=len(selA),
)
print(json.dumps(res,indent=2))
