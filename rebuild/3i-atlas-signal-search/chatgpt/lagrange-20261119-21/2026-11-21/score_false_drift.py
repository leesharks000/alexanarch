#!/usr/bin/env python3
"""OH13 final false-drift D3 cohort scorer.
This consumes measured complex-voltage derived Q2 values; it does NOT fetch telescope data.
Input: {"cohorts":[{"drift_hz_s":0.0,"candidates":[{"id":"C03","scans":{
 "0013":{"X":{"q":0.2,"sidebands":[0.1,...]}},"0014":...,"0015":...,
 "0016":...,"0017":...,"0018":...}}]}]}.
Require 41 cohorts (real 0 plus exactly 40 historical false-drift values).
"""
import argparse, json
from pathlib import Path
import numpy as np

ON=("0013","0015","0017")
OFF=("0014","0016","0018")
ALL=ON+OFF
DRIFTS=np.round(np.arange(-0.2,0.2001,0.01),3)
DRIFTS=DRIFTS[np.abs(DRIFTS)>1e-9]

def phase_curvature(x,d=2):
    u=x/np.maximum(abs(x),1e-30)
    return abs(np.mean(u[:-2*d]*u[2*d:]*np.conj(u[d:-d])**2))

def rank(record):
    controls=np.asarray(record["sidebands"],float)
    if controls.size<8 or not np.all(np.isfinite(controls)):
        raise ValueError("Need >=8 finite matched sidebands")
    q=float(record["q"])
    if not np.isfinite(q): raise ValueError("NaN source statistic")
    return float((np.count_nonzero(controls<q)+.5*np.count_nonzero(controls==q)+.5)/(len(controls)+1))

def cohort_score(c):
    rows=[]
    for candidate in c["candidates"]:
        scans=candidate["scans"]
        if any(s not in scans or "X" not in scans[s] for s in ALL):
            raise ValueError("Missing X data for candidate "+candidate["id"])
        r={s:rank(scans[s]["X"]) for s in ALL}
        contrast=np.mean([r[s] for s in ON])-np.mean([r[s] for s in OFF])
        rows.append({"id":candidate["id"],"contrast":float(contrast),
          "on_ranks":[r[s] for s in ON],"off_ranks":[r[s] for s in OFF],
          "strict":all(r[s]>.5 for s in ON) and all(r[s]<.5 for s in OFF)})
    a=np.array([r["contrast"] for r in rows])
    return {"drift_hz_s":float(c["drift_hz_s"]),"n":len(rows),
       "mean_ONminusOFF_X_D3":float(np.mean(a)) if len(a) else None,
       "size_scaled_contrast":float(np.mean(a)*np.sqrt(len(a))) if len(a) else None,
       "candidate_diagnostics":rows}

def analyse(cohorts):
    if len(cohorts)!=41: raise ValueError("Require 41 real/false cohorts")
    labels=np.round([c["drift_hz_s"] for c in cohorts],3)
    if len(set(labels))!=41 or set(labels)!=set(np.r_[0,DRIFTS]):
        raise ValueError("Mismatch with original OH13 false-drift grid")
    rows=[cohort_score(c) for c in cohorts]
    true=next(r for r in rows if abs(r["drift_hz_s"])<1e-9)
    initial=next(c for c in cohorts if abs(c["drift_hz_s"])<1e-9)
    expected={"C%02d"%i for i in range(3,14)}
    if {r["id"] for r in initial["candidates"]}!=expected:
        raise ValueError("True cohort must be exactly C03-C13, not C01/C02")
    controls=[r for r in rows if abs(r["drift_hz_s"])>=1e-9 and r["n"]>0]
    count=sum(c["size_scaled_contrast"]>=true["size_scaled_contrast"] for c in controls)
    null=np.array([c["size_scaled_contrast"] for c in controls])
    return {"primary":"sqrt(n)*mean(ON-minus-OFF local Q2 percentile), X, lag2",
     "true":true,"nonempty_false_cohorts":len(controls),
     "empty_false_cohorts":40-len(controls),
     "null_median":float(np.median(null)) if len(null) else None,
     "null_max":float(np.max(null)) if len(null) else None,
     "empirical_tail_p":(1+count)/(1+len(controls)) if controls else None,
     "p_floor":1/(1+len(controls)) if controls else None,
     "qualification":"Shared telescope recordings; drift-cohort ranks are not independent physical detections. sqrt(n) is a rough variance scale and fails when selected candidates are dependent. Must separately inspect receiver and sideband correlations.",
     "cohort_summary":[{k:v for k,v in r.items() if k!="candidate_diagnostics"} for r in rows]}

def fixture(rng,signal=False):
    groups=[]
    for d in np.r_[0,DRIFTS]:
        n=11 if d==0 else int(rng.integers(1,9))
        candidates=[]
        for j in range(n):
            scans={}
            for s in ALL:
                side=rng.beta(3,10,16)
                q=float(rng.beta(3,10))
                if signal and d==0 and s in ON:q=min(.999,q+.2)
                scans[s]={"X":{"q":q,"sidebands":side.tolist()}}
            candidates.append({"id":"C%02d"%(j+3) if d==0 else "F_%s_%s"%(d,j),
                "scans":scans})
        groups.append({"drift_hz_s":float(d),"candidates":candidates})
    return groups

def selftest():
    rng=np.random.default_rng(20261121)
    k=np.arange(4096)
    x=np.exp(1j*(.0008*k*k+.031*k))
    y=x*np.exp(1j*(1.45+.3*k))
    assert abs(phase_curvature(x)-phase_curvature(y))<1e-12
    null=[analyse(fixture(rng))["empirical_tail_p"] for _ in range(200)]
    signal=[analyse(fixture(rng,True))["empirical_tail_p"] for _ in range(60)]
    print(json.dumps({"status":"synthetic validation only",
       "phase_ramp_invariance":True,"H0_n":200,"H0_p_le_0.05":sum(p<=.05 for p in null),
       "H1_n":60,"H1_p_le_0.05":sum(p<=.05 for p in signal),
       "note":"Scorer validation only; not a calibrated GBT receiver model."},indent=2))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--input");p.add_argument("--output")
    a=p.parse_args()
    if a.self_test:selftest()
    elif a.input:
        out=json.dumps(analyse(json.loads(Path(a.input).read_text())["cohorts"]),indent=2)
        if a.output:Path(a.output).write_text(out)
        else:print(out)
    else:p.error("Supply --self-test or --input")
