import sys,json,re,collections,random,itertools,statistics,bisect
sys.path.insert(0,'../map'); from tisch import load
MT=load('MT'); RE=load('RE'); L=json.load(open('../map/rev-matthew-ledger.json'))['rows']
mi={k:i for i,k in enumerate(MT)}; ri={k:i for i,k in enumerate(RE)}; mk_=list(MT); rk_=list(RE)
def segs(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); ks=[(c,v) for v in range(a,b+1) if (c,v) in V]
            if ks: out.append(ks)
    return out
def cls(s):
    s=str(s)
    return 'blind' if 'held under seal' in s else 'sealed' if re.search(r'\b[JKNPQRT]\d+[a-z]? held|sealed N\d|S\d held',s) and 'failed as written' not in s else 'engine' if s.startswith('engine') else 'counted' if (s.startswith('counted') or 'counted:' in s) else 'read'
P=[]; covM=set(); covR=set()
for i,r in enumerate(L):
    ms=segs(MT,r['matt']); rs=segs(RE,r['rev'])
    if not ms or not rs: continue
    for x in ms: covM|=set(x)
    for x in rs: covR|=set(x)
    for x in rs: P.append(dict(m=mi[ms[0][0]],r=ri[x[0]],row=i,cls=cls(r['standing']),rel='relational' in str(r['standing'])))
P.sort(key=lambda p:(p['m'],p['r']))
json.dump(dict(points=P,nM=len(MT),nR=len(RE),mch=[mi[(c,1)] for c in range(1,29)],rch=[ri[(c,1)] for c in range(1,23)]),open('points.json','w'))
print('points',len(P),'rows',len({p['row'] for p in P}))
def lis(seq):
    t=[]
    for x in seq:
        j=bisect.bisect_left(t,x)
        if j==len(t): t.append(x)
        else: t[j]=x
    return len(t)
rs_=[p['r'] for p in P]; inc=lis(rs_); dec=lis([-x for x in rs_])
random.seed(11); N=3000; gi=gd=0; sh=rs_[:]
for _ in range(N):
    random.shuffle(sh); gi+= lis(sh)>=inc; gd+= lis([-x for x in sh])>=dec
print('U1 longest rising chain',inc,'p',round((gi+1)/(N+1),3),'| longest falling',dec,'p',round((gd+1)/(N+1),3))
def runs(pts):
    out=[]; cur=[pts[0]]; d=0
    for a,b in zip(pts,pts[1:]):
        dm=b[0]-a[0]; dr=b[1]-a[1]; s=(dr>0)-(dr<0)
        if dm<=12 and 0<abs(dr)<=25 and (d==0 or s==d): cur.append(b); d=s
        else:
            if len(cur)>=3: out.append((cur,d))
            cur=[b]; d=0
    if len(cur)>=3: out.append((cur,d))
    return out
pts=[(p['m'],p['r']) for p in P]; R=runs(pts)
ge=0; ms=[p[0] for p in pts]
for _ in range(N):
    random.shuffle(sh); ge+= len(runs(sorted(zip(ms,sh))))>=len(R)
print('U2 runs of 3+:',len(R),'p',round((ge+1)/(N+1),3))
name=lambda V,i: f'{V[i][0]}:{V[i][1]}'
for cur,d in R: print('   ','rising ' if d>0 else 'falling','Mt',name(mk_,cur[0][0]),'–',name(mk_,cur[-1][0]),'| Rev',' → '.join(name(rk_,x[1]) for x in cur))
print('U3 rising',sum(d>0 for _,d in R),'falling',sum(d<0 for _,d in R))
PT=[('1',1,1),('2–3',2,3),('4–5',4,5),('6–7',6,7),('8–11',8,11),('12',12,12),('13',13,13),('14',14,14),('15–16',15,16),('17–18',17,18),('19–20',19,20),('21–22',21,22)]
print('U4 part: n, median Matthew chapter, interquartile span as share of the book')
for n,a,b in PT:
    xs=sorted(p['m'] for p in P if a<=rk_[p['r']][0]<=b)
    if len(xs)>=4:
        q=statistics.quantiles(xs,n=4); print(f'   {n:>6} {len(xs):>3}  ch {mk_[int(statistics.median(xs))][0]:>2}  IQR {round((q[2]-q[0])/len(MT),2)}')
json.dump(dict(runs=[[list(x) for x in cur] for cur,d in R]),open('runs.json','w'))
