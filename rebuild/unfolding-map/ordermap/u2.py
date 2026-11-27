exec(open('u1.py').read().split("P.sort(key=lambda p:(p['m'],p['r']))")[0])
by=collections.defaultdict(list)
for p in P: by[p['row']].append(p)
Q=sorted(((v[0]['m'],int(statistics.median(x['r'] for x in v)),k) for k,v in by.items()))
name=lambda V,i: f'{V[i][0]}:{V[i][1]}'
def runs(pts,gm=12,gr=25):
    out=[]; cur=[pts[0]]; d=0
    for a,b in zip(pts,pts[1:]):
        dm=b[0]-a[0]; dr=b[1]-a[1]; s=(dr>0)-(dr<0)
        if dm<=gm and 0<abs(dr)<=gr and (d==0 or s==d): cur.append(b); d=s
        else:
            if len(cur)>=3: out.append((cur,d))
            cur=[a] if (dm<=gm and 0<abs(dr)<=gr) else []
            cur=(cur+[b]) if cur else [b]; d=s if len(cur)==2 else 0
    if len(cur)>=3: out.append((cur,d))
    return out
random.seed(5); N=4000
for gm,gr in [(12,25),(20,40)]:
    R=runs(Q,gm,gr); ms=[q[0] for q in Q]; rs=[q[1] for q in Q]; ge=0; up=0
    for _ in range(N):
        random.shuffle(rs); ge+= len(runs(sorted(zip(ms,rs,range(len(ms)))),gm,gr))>=len(R)
    print(f'one point per row; gaps Mt<={gm}, Rev<={gr}: runs of 3+ = {len(R)}, p = {round((ge+1)/(N+1),3)}; rising {sum(d>0 for _,d in R)}, falling {sum(d<0 for _,d in R)}')
    for cur,d in R: print('    ','rising ' if d>0 else 'falling','Mt',' , '.join(name(mk_,x[0]) for x in cur),'| Rev',' → '.join(name(rk_,x[1]) for x in cur))
# pairs: adjacent in Matthew (<=12 verses) and near in Revelation (<=25): direction
pr=[(a,b) for a,b in itertools.combinations(Q,2) if 0<b[0]-a[0]<=12 and 0<abs(b[1]-a[1])<=25]
up=sum(b[1]>a[1] for a,b in pr); print('near pairs',len(pr),'rising',up,'falling',len(pr)-up)
rs=[q[1] for q in Q]; ms=[q[0] for q in Q]; cnt=0; obs=len(pr)
for _ in range(N):
    random.shuffle(rs); Z=sorted(zip(ms,rs)); c=sum(1 for a,b in itertools.combinations(Z,2) if 0<b[0]-a[0]<=12 and 0<abs(b[1]-a[1])<=25); cnt+= c>=obs
print('near pairs against shuffling: p =',round((cnt+1)/(N+1),3))
from math import comb
k=max(up,len(pr)-up); n=len(pr); print('sign test two-sided p =',round(min(1,2*sum(comb(n,i) for i in range(k,n+1))/2**n),3))
