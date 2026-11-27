exec(open('../residue/r1.py').read().split("print('P1")[0])
import json,itertools,collections,random,statistics
MT=NT['MT']; RE=NT['RE']; mi={k:i for i,k in enumerate(MT)}; ri={k:i for i,k in enumerate(RE)}
Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']
def segs(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
LET=[('Ephesus',2,1,7),('Smyrna',2,8,11),('Pergamum',2,12,17),('Thyatira',2,18,29),('Sardis',3,1,6),('Philadelphia',3,7,13),('Laodicea',3,14,22)]
def unit(k):
    for n,c,a,b in LET:
        if k[0]==c and a<=k[1]<=b: return n
    return 'ch%02d'%k[0]
U=collections.defaultdict(list)
for i,r in enumerate(Lr):
    mk=segs(MT,r['matt']); rk=segs(RE,r['rev'])
    if not(mk and rk): continue
    g=collections.defaultdict(list)
    for k in rk: g[unit(k)].append(ri[k])
    for u,v in g.items(): U[u].append((mi[mk[0]],statistics.median(v),r['rev'],r['matt']))
def conc(v):
    c=d=0
    for a,b in itertools.combinations(v,2):
        s=(a[0]-b[0])*(a[1]-b[1]); c+=s>0; d+=s<0
    return c,d
def perm(groups,n=4000):
    c=sum(conc(v)[0] for v in groups); d=sum(conc(v)[1] for v in groups); obs=c/max(1,c+d); hi=lo=0
    for _ in range(n):
        cc=dd=0
        for v in groups:
            rs=[x[1] for x in v]; random.shuffle(rs); a,b=conc([(x[0],y) for x,y in zip(v,rs)]); cc+=a; dd+=b
        s=cc/max(1,cc+dd); hi+=s>=obs; lo+=s<=obs
    return c,d,(hi+1)/(n+1),(lo+1)/(n+1)
random.seed(6)
c,d,ph,pl=perm(list(U.values())); print('ALL units',len(U),'same',c,'opp',d,round(100*c/(c+d)),'% p_fwd',round(ph,3),'p_back',round(pl,3))
for u in [l[0] for l in LET]+sorted(k for k in U if k.startswith('ch')):
    v=U.get(u,[])
    if len(v)<3: print(u,len(v)); continue
    c,d,ph,pl=perm([v],2000); print(u,len(v),'same',c,'opp',d,'p_fwd',round(ph,3),'p_back',round(pl,3))
print('Laodicea rows:',sorted((x[1],x[0],x[2],x[3]) for x in U['Laodicea']))
json.dump({u:[(a,b) for a,b,_,_ in v] for u,v in U.items()},open('units.json','w'))
