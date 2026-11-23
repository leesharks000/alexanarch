#!/usr/bin/env python3
"""Reproduce the two interleaved cc19 comb fits from the original M4b event catalogue.
Usage: python reproduce_cc19_comb.py path/to/cc19.json
Exploratory post-hoc analysis; not a physical-source or false-alarm-rate determination.
"""
import json, math, sys

# Original Class A/Class B records, assigned after inspecting the catalogue.
# Index numbering is anchored at the Class A line near 1631.7475 MHz.
GROUPS = {
    "A": [(-2, 1631.6126212477684), (-1, 1631.680078804493),
          (0, 1631.7475084215403), (1, 1631.8149492144585),
          (3, 1631.949809845537), (4, 1632.017232477665),
          (5, 1632.0846900343895), (6, 1632.1521028876305)],
    "B": [(-3, 1631.5653710626066), (-1, 1631.7002344876528),
          (0, 1631.7676529288292), (2, 1631.9025233387947),
          (4, 1632.0373895578086), (5, 1632.1048219688237)],
}

def fit_line(rows):
    n = len(rows)
    sx = sum(i for i, _ in rows)
    sy = sum(f * 1e6 for _, f in rows)
    sxx = sum(i*i for i, _ in rows)
    sxy = sum(i*f*1e6 for i, f in rows)
    slope = (n*sxy-sx*sy)/(n*sxx-sx*sx)
    intercept = (sy-slope*sx)/n
    residual = [f*1e6 - (intercept+slope*i) for i,f in rows]
    return slope, intercept, residual

def main(path):
    d=json.load(open(path))
    assert d["cc"] == 19 and d["n"]["A"] == 6
    assert d["control_n"]["A"] == 0
    obs=d["events"]
    for name,rows in GROUPS.items():
        for i,f in rows:
            matches=[e for e in obs if abs(e["mhz_topo"]-f)<0.0000002]
            if len(matches)!=1: raise RuntimeError(f"{name} index {i}: expected one exact catalogue record")
        slope,intercept,residual=fit_line(rows)
        rms=math.sqrt(sum(r*r for r in residual)/len(residual))
        print(name,"n=",len(rows),"step Hz=",round(slope,4),
              "intercept MHz=",round(intercept/1e6,9),
              "rms residual Hz=",round(rms,4),"max_abs Hz=",round(max(map(abs,residual)),4))
        print("  index,residualHz", [(i,round(r,3)) for (i,_),r in zip(rows,residual)])
    # Common step with two separate offsets.
    allrows=[(i,0,f*1e6) for i,f in GROUPS["A"]]+[(i,1,f*1e6) for i,f in GROUPS["B"]]
    mx=sum(i for i,g,y in allrows)/len(allrows)
    # Center within each intercept group, not across them:
    groups=[[r for r in allrows if r[1]==g] for g in (0,1)]
    means=[(sum(r[0] for r in gg)/len(gg),sum(r[2] for r in gg)/len(gg)) for gg in groups]
    num=sum((i-means[g][0])*(y-means[g][1]) for i,g,y in allrows)
    den=sum((i-means[g][0])**2 for i,g,y in allrows)
    shared=num/den
    offsets=[means[g][1]-shared*means[g][0] for g in (0,1)]
    resid=[y-(offsets[g]+shared*i) for i,g,y in allrows]
    print("SHARED", "step Hz", round(shared,4),"offset difference Hz",round(offsets[1]-offsets[0],4),
          "rms residual Hz",round(math.sqrt(sum(r*r for r in resid)/len(resid)),4),
          "max abs Hz",round(max(map(abs,resid)),4))
    print("CAUTION: group membership was chosen after viewing this same catalogue.")

if __name__ == "__main__":
    if len(sys.argv)!=2: raise SystemExit(__doc__)
    main(sys.argv[1])
