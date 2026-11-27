src=open('x1.py',encoding='utf-8').read()
exec(src.split("# kind, matt")[0])
BK.update({'Joel':'tlg039','Zeph':'tlg044'})
for b in ('Joel','Zeph'):
    f=glob.glob(SEAT+BK[b]+'-*.txt')[0]; LX[b]={}; ORDER[b]=[]
    for line in open(f,encoding='utf-8'):
        m=re.match(r'.*? (\d+):(\d+)\t(.*)',unicodedata.normalize('NFC',line.rstrip('\n')))
        if m: k=(int(m.group(1)),int(m.group(2))); LX[b][k]=m.group(3); ORDER[b].append(k)
RE=NT['RE']
REVS=[('1:7','Dan',7,13,'K'),('1:7','Zech',12,10,'K'),('1:13','Dan',7,13,'K'),('1:14','Dan',7,9,'X'),('1:15','Ezek',43,2,'K'),('1:17','Isa',44,6,'K'),('2:7','Gen',2,9,'K'),('2:23','Jer',17,10,'K'),('2:26-27','Ps',2,9,'X'),('3:7','Isa',22,22,'K'),('3:9','Isa',60,14,'X'),('3:19','Prov',3,12,'K'),('4:2-3','Ezek',1,26,'K'),('4:6-7','Ezek',1,10,'K'),('4:8','Isa',6,3,'K'),('5:1','Ezek',2,10,'K'),('5:6','Isa',53,7,'K'),('5:10','Exod',19,6,'K'),('6:2-5','Zech',6,2,'K'),('6:8','Ezek',14,21,'K'),('6:12-13','Joel',2,31,'K'),('6:13-14','Isa',34,4,'K'),('6:15-16','Isa',2,19,'K'),('6:16','Hos',10,8,'K'),('7:3','Ezek',9,4,'K'),('7:16','Isa',49,10,'K'),('7:17','Isa',25,8,'K'),('8:7','Exod',9,24,'X'),('8:8','Exod',7,20,'X'),('9:3','Exod',10,12,'X'),('10:9-10','Ezek',3,3,'K'),('11:4','Zech',4,14,'K'),('11:7','Dan',7,21,'K'),('12:5','Ps',2,9,'K'),('12:14','Dan',7,25,'K'),('13:1-2','Dan',7,3,'K'),('13:5','Dan',7,8,'K'),('14:5','Zeph',3,13,'K'),('14:8','Isa',21,9,'K'),('14:10','Isa',51,17,'K'),('14:15','Joel',3,13,'K'),('15:4','Ps',85,9,'K'),('16:2','Exod',9,10,'X'),('16:4','Exod',7,20,'X'),('17:1','Jer',28,13,'K'),('18:2','Isa',13,21,'K'),('18:4','Jer',28,45,'K'),('18:7','Isa',47,8,'K'),('18:21','Jer',28,63,'K'),('19:15','Isa',11,4,'K'),('19:15','Isa',63,3,'K'),('19:17-18','Ezek',39,17,'K'),('20:8','Ezek',38,2,'K'),('20:11-12','Dan',7,10,'K'),('21:1','Isa',65,17,'K'),('21:3','Ezek',37,27,'K'),('21:4','Isa',25,8,'K'),('21:12-13','Ezek',48,31,'K'),('22:1-2','Ezek',47,12,'K'),('22:12','Isa',40,10,'K')]
def rtxt(ks): return ' '.join(text('RE',k) for k in ks if k in RE)
def checkr(m,b,c,v):
    ms=stems(rtxt(mv(m)))
    if (c,v) not in LX[b]: return (0,None,[])
    i=ORDER[b].index((c,v)); best=(-1,None,[])
    for j in range(max(0,i-1),min(len(ORDER[b]),i+2)):
        k=ORDER[b][j]; sh=ms&stems(LX[b][k])
        if len(sh)>best[0]: best=(len(sh),k,sorted(sh))
    return best
out=[(m,b,)+checkr(m,b,c,v)[:2]+(cl,) for m,b,c,v,cl in REVS]
miss=[(o[0],o[1],o[3],o[2]) for o in out if o[2]<2]; print('listed',len(out),'| under two stems:',len(miss),miss)
RS=[o[2] for o in out]
Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']; MT=NT['MT']
def segs(V,s):
    o=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); o+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return o
RM=[]
for r in Lr:
    mk=segs(MT,r['matt']); rk=segs(RE,r['rev'])
    if mk and rk and len(mk)<=2 and len(rk)<=2: RM.append(len(stems(mtxt(mk))&stems(rtxt(rk))))
def desc(name,xs):
    xs=sorted(xs); print(f'  {name:42s} n={len(xs):3d} median {statistics.median(xs):4.1f} mean {statistics.mean(xs):4.2f} quartiles {xs[len(xs)//4]}-{xs[3*len(xs)//4]}  one or none: {round(100*sum(x<=1 for x in xs)/len(xs))}%')
print('Y1'); desc('Revelation using scripture (all listed)',RS); desc('Revelation-Matthew rows, 1-2 verses a side',RM)
def mw(a,b,n=10000):
    obs=statistics.mean(a)-statistics.mean(b); z=list(a)+list(b); ge=0
    for _ in range(n):
        random.shuffle(z); ge+= abs(statistics.mean(z[:len(a)])-statistics.mean(z[len(a):]))>=abs(obs)
    return round(obs,2),(ge+1)/(n+1)
random.seed(2); print('  difference of means, p:',mw(RS,RM))
print('Y2 classes:',collections.Counter(o[4] for o in out))
TM=2.2; print('Y3 means: Rev-scripture',round(statistics.mean(RS),2),'| Matthew tacit scripture 2.2 | Rev-Matthew',round(statistics.mean(RM),2))
by=collections.defaultdict(list)
for o in out: by[o[1]].append(o[2])
print('  by book:',{b:(len(v),round(statistics.mean(v),1)) for b,v in by.items() if len(v)>=4})
