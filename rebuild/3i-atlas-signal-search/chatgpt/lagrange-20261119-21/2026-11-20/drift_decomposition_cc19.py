#!/usr/bin/env python3
"""Reproduce exploratory cc19 two-comb drift decomposition from ORIGINAL frozen M4b JSON.
No raw voltages are downloaded; analysis is catalogue-only. Python stdlib only.
"""
import json, urllib.request, itertools, statistics
URL = ("https://raw.githubusercontent.com/leesharks000/alexanarch/main/"
       "rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/events/cc19.json")
# Frequency groups/teeth frozen from prior post-hoc frequency-only comb reconstruction.
GROUPS = {
    "A": [(-2,1631.6126212477684),(-1,1631.680078804493),
          (0,1631.7475084215403),(1,1631.8149492144585),
          (3,1631.949809845537),(4,1632.017232477665),
          (5,1632.0846900343895),(6,1632.1521028876305)],
    "B": [(-3,1631.5653710626066),(-1,1631.7002344876528),
          (0,1631.7676529288292),(2,1631.9025233387947),
          (4,1632.0373895578086),(5,1632.1048219688237)]
}
def mean(x): return sum(x)/len(x)
def summarize(rows):
    xs=[r["hz_per_s"] for r in rows]
    return dict(n=len(xs), mean=mean(xs), median=statistics.median(xs),
                sd=statistics.stdev(xs), min=min(xs), max=max(xs))
def perms_exact(rows, A_count):
    y=[r["hz_per_s"] for r in rows]
    obs=mean(y[:A_count])-mean(y[A_count:])
    ext=0; total=0
    for subset in itertools.combinations(range(len(y)), A_count):
        idx=set(subset)
        a=[v for i,v in enumerate(y) if i in idx]
        b=[v for i,v in enumerate(y) if i not in idx]
        total+=1
        if abs(mean(a)-mean(b))>=abs(obs)-1e-12: ext+=1
    return dict(observed_difference=obs, extreme=ext, trials=total, tail_fraction=ext/total)
def strata_perms(rows):
    levels=sorted(set(r["level"] for r in rows))
    buckets=[]
    for level in levels:
        ix=[i for i,r in enumerate(rows) if r["level"]==level]
        na=sum(rows[i]["group"]=="A" for i in ix)
        buckets.append([set(s) for s in itertools.combinations(ix,na)])
    obs=mean([r["hz_per_s"] for r in rows if r["group"]=="A"])-mean(
        [r["hz_per_s"] for r in rows if r["group"]=="B"])
    extreme=total=0
    for parts in itertools.product(*buckets):
        chosen=set().union(*parts)
        aa=[r["hz_per_s"] for i,r in enumerate(rows) if i in chosen]
        bb=[r["hz_per_s"] for i,r in enumerate(rows) if i not in chosen]
        total+=1
        if abs(mean(aa)-mean(bb)) >= abs(obs)-1e-12: extreme+=1
    return dict(observed_difference=obs, extreme=extreme, trials=total,
                tail_fraction=extreme/total)
def ols_tooth(rows):
    x=[r["tooth"] for r in rows]; y=[r["hz_per_s"] for r in rows]
    xm,ym=mean(x),mean(y); vxx=sum((q-xm)**2 for q in x)
    slope=sum((a-xm)*(b-ym) for a,b in zip(x,y))/vxx
    intercept=ym-slope*xm
    rms=(mean([(v-intercept-slope*t)**2 for v,t in zip(y,x)]))**0.5
    return dict(intercept_hz_s=intercept,slope_hz_s_per_tooth=slope,rms_hz_s=rms)
def main():
    with urllib.request.urlopen(URL,timeout=25) as resp:
        d=json.load(resp)
    rows=[]
    for group,spec in GROUPS.items():
        for tooth,mhz in spec:
            found=[e for e in d["events"] if abs(e["mhz_topo"]-mhz)<1e-9]
            if len(found)!=1: raise ValueError((group,tooth,mhz,len(found)))
            rows.append(dict(group=group,tooth=tooth,**found[0]))
    assert len(rows)==14 and all(r["scan"]=="0013" for r in rows)
    a=[r for r in rows if r["group"]=="A"];b=[r for r in rows if r["group"]=="B"]
    report=dict(source=URL,provenance="post-hoc selected frequencies; 14 of 19 records",
        all_one_scan=True,all_fourteen_scan="0013",
        A=summarize(a),B=summarize(b),
        drift_mean_difference_hz_s=mean([r["hz_per_s"] for r in a])-mean([r["hz_per_s"] for r in b]),
        exact_permutation=perms_exact(rows,8),
        resolution_stratified_permutation=strata_perms(rows),
        remove_max_positive_event=perms_exact([r for r in rows if r["hz_per_s"]!=max(x["hz_per_s"] for x in rows)],7),
        regression_A=ols_tooth(a),regression_B=ols_tooth(b),
        by_resolution={str(l): {"A":[r["hz_per_s"] for r in a if r["level"]==l],
                                "B":[r["hz_per_s"] for r in b if r["level"]==l]}
                       for l in sorted(set(r["level"] for r in rows))},
        source_drift_not_identifiable="rate_i = source_Doppler + intrinsic_oscillator_i + propagation_i + detector_bias_i")
    print(json.dumps(report,indent=2))
if __name__ == "__main__": main()
