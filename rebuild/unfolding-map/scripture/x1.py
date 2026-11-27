exec(open('../residue/r1.py').read().split("print('P1")[0])
import json,glob,unicodedata,statistics,random,collections,os
SEAT='/home/claude/repos/alexanarch/data/corpora/lxx-swete/text/'
BK={'Gen':'tlg001','Exod':'tlg002','Lev':'tlg003','Num':'tlg004','Deut':'tlg005','3Kgdms':'tlg013','4Kgdms':'tlg014','Ps':'tlg027','Prov':'tlg029','Sir':'tlg034','Hos':'tlg036','Mic':'tlg038','Jonah':'tlg041','Zech':'tlg046','Mal':'tlg047','Isa':'tlg048','Jer':'tlg049','Ezek':'tlg053','Dan':'tlg057'}
LX={}; ORDER={}
for b,t in BK.items():
    f=glob.glob(SEAT+t+'-*.txt')[0]; LX[b]={}; ORDER[b]=[]
    for line in open(f,encoding='utf-8'):
        m=re.match(r'.*? (\d+):(\d+)\t(.*)',unicodedata.normalize('NFC',line.rstrip('\n')))
        if m: k=(int(m.group(1)),int(m.group(2))); LX[b][k]=m.group(3); ORDER[b].append(k)
STOP=set('αυτοσ αυτου αυτον αυτω αυτοισ αυτων αυτη αυτησ αυτην ουτοσ τουτο ταυτα εστιν εισιν εσται λεγει λεγων ειπεν παντα παντεσ υμων υμιν υμασ ημων ημιν ημασ οταν οπου ουδε μηδε αλλα εαν'.split())
def stems(txt):
    t=''.join(c for c in unicodedata.normalize('NFD',txt.lower()) if not unicodedata.combining(c)).replace('ς','σ')
    out=set()
    for w in re.findall(r'[α-ω]+',t):
        if len(w)<=3 or w in STOP: continue
        out.add(w[:5])
    return out
MT=NT['MT']; RE=NT['RE']
def mtxt(ks): return ' '.join(text('MT',k) for k in ks if k in MT)
def mv(s):
    out=[]
    for part in re.split(r'\s*;\s*',s):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip()); c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1)]
    return out
# kind, matt, [(book,c,v)...], class
EXPL=[('1:23','Isa',7,14),('2:6','Mic',5,2),('2:15','Hos',11,1),('2:18','Jer',38,15),('3:3','Isa',40,3),('4:4','Deut',8,3),('4:6','Ps',90,11),('4:7','Deut',6,16),('4:10','Deut',6,13),('4:15-16','Isa',9,1),('5:21','Exod',20,15),('5:27','Exod',20,13),('5:31','Deut',24,1),('5:33','Lev',19,12),('5:38','Exod',21,24),('5:43','Lev',19,18),('8:17','Isa',53,4),('9:13','Hos',6,6),('11:10','Mal',3,1),('12:7','Hos',6,6),('12:18-21','Isa',42,1),('13:14-15','Isa',6,9),('13:35','Ps',77,2),('15:4','Exod',20,12),('15:8-9','Isa',29,13),('19:4','Gen',1,27),('19:5','Gen',2,24),('19:18-19','Exod',20,12),('21:5','Zech',9,9),('21:9','Ps',117,26),('21:13','Isa',56,7),('21:16','Ps',8,3),('21:42','Ps',117,22),('22:24','Deut',25,5),('22:32','Exod',3,6),('22:37','Deut',6,5),('22:39','Lev',19,18),('22:44','Ps',109,1),('23:39','Ps',117,26),('26:31','Zech',13,7),('27:9-10','Zech',11,13),('27:46','Ps',21,2)]
TAC=[('2:2','Num',24,17,'E'),('2:11','Isa',60,6,'E'),('2:13-16','Exod',2,15,'X'),('2:16','Exod',1,22,'X'),('2:20','Exod',4,19,'X'),('3:4','4Kgdms',1,8,'X'),('3:17','Isa',42,1,'K'),('4:2','Exod',34,28,'X'),('5:5','Ps',36,11,'K'),('5:8','Ps',23,4,'K'),('5:34-35','Isa',66,1,'K'),('5:48','Deut',18,13,'K'),('6:6','Isa',26,20,'K'),('7:23','Ps',6,9,'K'),('8:11','Ps',106,3,'K'),('9:36','Num',27,17,'E'),('10:35-36','Mic',7,6,'K'),('11:5','Isa',35,5,'E'),('11:23','Isa',14,13,'X'),('11:28-29','Sir',51,27,'K'),('13:32','Dan',4,12,'K'),('13:43','Dan',12,3,'K'),('14:16-20','4Kgdms',4,43,'X'),('16:27','Ps',61,13,'K'),('17:2','Exod',34,29,'X'),('17:5','Deut',18,15,'E'),('18:16','Deut',19,15,'K'),('18:22','Gen',4,24,'O'),('21:33','Isa',5,2,'K'),('23:38','Jer',22,5,'K'),('24:29','Isa',13,10,'K'),('24:30','Dan',7,13,'K'),('24:31','Isa',27,13,'K'),('26:15','Zech',11,12,'E'),('26:28','Exod',24,8,'K'),('26:38','Ps',41,6,'K'),('26:64','Dan',7,13,'K'),('27:34','Ps',68,22,'E'),('27:35','Ps',21,19,'E'),('27:39','Ps',21,8,'E'),('27:43','Ps',21,9,'E'),('27:48','Ps',68,22,'E'),('28:18','Dan',7,14,'K')]
def check(m,b,c,v):
    ms=stems(mtxt(mv(m))); best=(-1,None)
    i=ORDER[b].index((c,v)) if (c,v) in LX[b] else None
    if i is None: return 0,None,[]
    for j in range(max(0,i-1),min(len(ORDER[b]),i+2)):
        k=ORDER[b][j]; sh=ms&stems(LX[b][k])
        if len(sh)>best[0]: best=(len(sh),k,sorted(sh))
    return best
res={'explicit':[],'tacit':[]}; dropped=[]
for m,b,c,v in EXPL:
    n,k,sh=check(m,b,c,v); (res['explicit'] if n>=2 else dropped).append((m,b,k,n,None))
for m,b,c,v,cl in TAC:
    n,k,sh=check(m,b,c,v); (res['tacit'] if n>=2 else dropped).append((m,b,k,n,cl))
print('checked: explicit',len(res['explicit']),'of',len(EXPL),'| tacit',len(res['tacit']),'of',len(TAC)); print('dropped:',[(d[0],d[1],d[2],d[3]) for d in dropped])
Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']
def segs(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
rev=[]; 
for r in Lr:
    mk=segs(MT,r['matt']); rk=segs(RE,r['rev'])
    if mk and rk: rev.append((len(stems(mtxt(mk))&stems(' '.join(text('RE',k) for k in rk))),len(mk),len(rk),r))
def desc(name,xs):
    xs=sorted(xs); print(f'  {name:34s} n={len(xs):3d} median {statistics.median(xs):4.1f} mean {statistics.mean(xs):4.1f} quartiles {xs[len(xs)//4]}-{xs[3*len(xs)//4]}  share with 0-1: {round(100*sum(x<=1 for x in xs)/len(xs))}%')
print('X1 shared stems per row')
E_=[x[3] for x in res['explicit']]; T_=[x[3] for x in res['tacit']]; Tall=[check(m,b,c,v)[0] for m,b,c,v,cl in TAC]
R_=[x[0] for x in rev]; Rs=[x[0] for x in rev if x[1]<=2 and x[2]<=2]; Rh=[x[0] for x in rev if x[3].get('source')!='engine']
desc('scripture, explicit',E_); desc('scripture, tacit (checked)',T_); desc('scripture, tacit (all listed)',Tall); desc('Revelation, all rows',R_); desc('Revelation, rows of 1-2 verses a side',Rs)
def mw(a,b,n=5000):
    obs=statistics.mean(a)-statistics.mean(b); z=a+b; ge=0
    for _ in range(n):
        random.shuffle(z); ge+= abs(statistics.mean(z[:len(a)])-statistics.mean(z[len(a):]))>=abs(obs)
    return round(obs,2),round((ge+1)/(n+1),4)
random.seed(1); print('  tacit(all) minus Revelation(1-2 verses): diff of means, p =',mw(list(Tall),list(Rs)))
print('X2 classes')
def cls(mvs):
    s=mvs.upper()
    if any(w in s for w in ('ENACT','EVENT','HAPPEN','STAGE')): return 'E'
    if any(w in s for w in ('OPPOSE','TURN')): return 'O'
    if any(w in s for w in ('EXCHANGE','BEARER','M2')): return 'X'
    if any(w in s for w in ('KEEP','LIKEN','FORETELL','M1')): return 'K'
    return 'other'
ct=collections.Counter(cl for m,b,c,v,cl in TAC); cr=collections.Counter(cls(str(x[3].get('move',''))) for x in rev)
for k in 'KEXO': print(f'  {k}: tacit scripture {ct[k]:2d} ({round(100*ct[k]/len(TAC))}%) | Revelation {cr[k]:3d} ({round(100*cr[k]/len(rev))}%; of classed {round(100*cr[k]/(len(rev)-cr["other"]))}%)')
print('  Revelation unclassed:',cr['other'])
print('X3 order')
mi={k:i for i,k in enumerate(MT)}
def rho(pts):
    def rk(xs):
        s=sorted(range(len(xs)),key=lambda i:xs[i]); r=[0]*len(xs)
        for a,i in enumerate(s): r[i]=a
        return r
    a=rk([p[0] for p in pts]); b=rk([p[1] for p in pts]); n=len(pts); ma=sum(a)/n; mb=sum(b)/n
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/((sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))**.5 or 1)
for bk in ('Isa','Ps','Exod','Deut','Dan','Zech'):
    pts=[(mi[mv(m)[0]],ORDER[b].index(k)) for m,b,k,n,cl in res['explicit']+res['tacit'] if b==bk]
    if len(pts)<5: print('  ',bk,len(pts),'too few'); continue
    o=rho(pts); ge=0
    for _ in range(5000):
        ys=[p[1] for p in pts]; random.shuffle(ys); ge+= abs(rho([(p[0],y) for p,y in zip(pts,ys)]))>=abs(o)
    print(f'   {bk}: {len(pts)} uses, rank correlation {o:+.2f}, p = {(ge+1)/5001:.3f}')
print('X4 conflation')
allv=set()
for r in Lr: allv|=set(segs(MT,r['matt']))
for name,rows in (('explicit',res['explicit']),('tacit',res['tacit']),('both',res['explicit']+res['tacit'])):
    S=set(k for m,*_ in rows for k in mv(m) if k in MT); hit=len(S&allv); keys=list(MT); ge=0
    for _ in range(5000): ge+= len(set(random.sample(keys,len(S)))&allv)>=hit
    print(f'   {name}: {len(S)} verses, {hit} also reached from Revelation ({round(100*hit/len(S))}%); base {round(100*len(allv)/len(MT),1)}%; p = {(ge+1)/5001:.3f}')
S=set(k for m,*_ in res['tacit'] for k in mv(m) if k in MT)
print('   tacit verses also reached:',sorted(S&allv))
json.dump(dict(explicit=res['explicit'],tacit=res['tacit'],dropped=dropped),open('x1.json','w'),ensure_ascii=False,default=str)
print('X4 by row')
for name,rows in (('explicit',[(m,) for m,b,c,v in EXPL]),('tacit',[(m,) for m,b,c,v,cl in TAC])):
    h=sum(1 for (m,) in rows if set(k for k in mv(m) if k in MT)&allv); print(f'   {name}: {h} of {len(rows)} places have a verse reached from Revelation ({round(100*h/len(rows))}%)')
