#!/usr/bin/env python3
"""Independent regression audit of reported C19 raw-voltage six-scan summaries.
No new voltage bytes. Uses C19 report's excess-power numbers and scan index
as an ordinal time proxy, not exact timestamps. Python stdlib only.
"""
from math import log, exp
DATA = {
    "A n=2": [67.99,16.48,19.38,10.09,3.11,2.22],
    "B n=1": [15.35,4.99,4.34,3.21,2.75,3.11],
    "15 catalogue lines": [18.12,6.49,6.45,4.58,4.64,4.24],
}
# Alternating ON/OFF and ordinal chronological positions.
i=list(range(6))
on=[1,0,1,0,1,0]
def solve(M,b):
    A=[list(map(float,row))+[float(v)] for row,v in zip(M,b)]
    n=len(b)
    for k in range(n):
        p=max(range(k,n),key=lambda j:abs(A[j][k]))
        A[k],A[p]=A[p],A[k]
        if abs(A[k][k])<1e-12:raise ValueError("singular")
        s=A[k][k]
        A[k]=[v/s for v in A[k]]
        for j in range(n):
            if j!=k:
                q=A[j][k]
                A[j]=[v-q*w for v,w in zip(A[j],A[k])]
    return [r[-1] for r in A]
def regression(y,X):
    n=len(y);p=len(X[0])
    xx=[[sum(X[t][k]*X[t][l] for t in range(n)) for l in range(p)] for k in range(p)]
    xy=[sum(X[t][k]*y[t] for t in range(n)) for k in range(p)]
    b=solve(xx,xy)
    rss=sum((y[t]-sum(b[k]*X[t][k] for k in range(p)))**2 for t in range(n))
    return dict(coefficients=[round(v,6) for v in b],rss=round(rss,6),
                bic=round(n*log(rss/n)+p*log(n),6))
MODELS={
    "intercept": lambda t:[1],
    "pointing_only": lambda t:[1,on[t]],
    "time_only": lambda t:[1,t],
    "time_plus_pointing": lambda t:[1,t,on[t]],
}
for label,powers in DATA.items():
    print("\n"+label)
    y=[log(v) for v in powers]
    for name,gen in MODELS.items():
        print(name,regression(y,[gen(t) for t in i]))
