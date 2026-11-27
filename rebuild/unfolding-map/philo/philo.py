import re,json,glob,collections,itertools,unicodedata as U,sys
C='/home/claude/repos/alexanarch/data/corpora/'
def stems(t):
    t=U.normalize('NFD',t); t=''.join(c for c in t if not U.combining(c)).lower().replace('ς','σ')
    return {w[:5] for w in re.findall(r'[α-ω]+',t) if len(w)>=5}
def units(files):
    out=[]
    for f in files:
        for l in open(f,encoding='utf-8'):
            if '\t' in l:
                r,t=l.rstrip('\n').split('\t',1); out.append((r,stems(t),t))
    return out
NT={}
for f in sorted(glob.glob(C+'gnt-nestle1904/text/*.txt')):
    for r,s,t in units([f]): NT[r]=(s,t)
PH=units(sorted(glob.glob(C+'philo/text/*.txt'))); JO=units(sorted(glob.glob(C+'josephus/text/*.txt'))); LX=units(sorted(glob.glob(C+'lxx-swete/text/*.txt')))
print('units: Philo',len(PH),'Josephus',len(JO),'LXX',len(LX),'| words Philo',sum(len(u[2].split()) for u in PH),'Josephus',sum(len(u[2].split()) for u in JO))
freq=collections.Counter(s for r,(ss,_) in NT.items() for s in ss)
rare={s for s,c in freq.items() if c<=60}
def index(us):
    ix=collections.defaultdict(set)
    for i,(r,ss,_) in enumerate(us):
        for s in ss: ix[s].add(i)
    return ix
iP,iJ,iL=index(PH),index(JO),index(LX)
def pairs(ss):
    r=sorted(ss&rare); P=[];J=[]
    for a,b in itertools.combinations(r,2):
        if iL[a]&iL[b]: continue
        p=iP[a]&iP[b]; j=iJ[a]&iJ[b]
        if p: P.append((a,b,sorted(p)[:3]))
        if j: J.append((a,b,sorted(j)[:3]))
    return P,J
cls=json.load(open('/home/claude/unfold/rev3/matt-proxy-classes.json'))
rows=json.load(open('/home/claude/unfold/map/rev-matthew-ledger.json'))['rows']
cov=set()
for r in rows:
    for part in str(r['matt']).split(';'):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m: cov|={f'{m.group(1)}:{v}' for v in range(int(m.group(2)),int(m.group(3) or m.group(2))+1)}
res={}
def book(b):
    out={}
    for r,(ss,t) in NT.items():
        if r.startswith(b+' '):
            P,J=pairs(ss); ps={(a,b2) for a,b2,_ in P}; js={(a,b2) for a,b2,_ in J}
            out[r[len(b)+1:]]=(P,J,bool(ps-js),bool(js-ps))
    return out
MT=book('Matt'); MR=book('Mark'); LU=book('Luke')
def tab(name,keys,B):
    n=len(keys); p=sum(B[k][2] for k in keys); j=sum(B[k][3] for k in keys); both=sum(bool(B[k][0]) and bool(B[k][1]) for k in keys)
    print(f'{name:34} n={n:4}  Philo-not-Jos {p:4} ({100*p/max(n,1):5.1f}%)  Jos-not-Philo {j:4} ({100*j/max(n,1):5.1f}%)  ratio {p/max(j,1):.2f}')
allk=list(MT)
un=[k for k in allk if k not in cov]
print('--- L1')
for c in ('MARK','DOUBLE','OWN'): tab('Matt unreached '+c,[k for k in un if cls.get(k)==c],MT)
tab('Matt reached',[k for k in allk if k in cov],MT)
print('--- L2/L3')
tab('Matt 5-7 unreached',[k for k in un if k.split(':')[0] in ('5','6','7')],MT)
tab('Matt all',allk,MT); tab('Mark all',list(MR),MR); tab('Luke all',list(LU),LU)
tab('Luke 6:20-49 (plain sermon)',[k for k in LU if k.split(':')[0]=='6' and int(k.split(':')[1])>=20],LU)
for ch in ('1','10','13','18','23','24','25'): tab('Matt '+ch,[k for k in allk if k.split(':')[0]==ch],MT)
print('--- Sermon verses, unreached, with a pair Philo has and Josephus lacks')
for k in un:
    if k.split(':')[0] in ('5','6','7') and MT[k][2]:
        js={(a,b) for a,b,_ in MT[k][1]}
        show=[(a,b,[PH[i][0] for i in ids]) for a,b,ids in MT[k][0] if (a,b) not in js][:3]
        print(' ',k,show)
json.dump({k:[[ (a,b,[PH[i][0] for i in ids]) for a,b,ids in v[0]],[(a,b,[JO[i][0] for i in ids]) for a,b,ids in v[1]]] for k,v in MT.items()},open('matt-philo-pairs.json','w'),ensure_ascii=False)
# L4
def find(us,*alts,n=8):
    out=[r for r,ss,t in us if all(any(a in ss for a in alt) for alt in alts)]
    return len(out),out[:n]
print('--- L4')
print('a swear+heaven+earth Philo',find(PH,['ομνυ','ομνυν','ομοσα','ομωμο','ομοσα','ορκον','ορκοσ','ορκου'],['ουραν'],['γην','γησ']),'| Jos',find(JO,['ομνυ','ομνυν','ορκον','ορκοσ','ορκου'],['ουραν'],['γην','γησ'])[0])
def phrase(us,rx):
    out=[]
    for r,ss,t in us:
        x=U.normalize('NFD',t); x=''.join(c for c in x if not U.combining(c)).lower().replace('ς','σ')
        if re.search(rx,x): out.append(r)
    return len(out),out[:10]
print('  not swearing best:',phrase(PH,r'μη ομνυναι|ανωμοτ|μηδ. ομνυναι'),'| Jos',phrase(JO,r'μη ομνυναι|ανωμοτ'))
print('b seeing God:',phrase(PH,r'ορων (τον )?θεον|θεον ορων|ορωντοσ (τον )?θεον|ορατικ'),'| Jos',phrase(JO,r'ορων (τον )?θεον|θεον ορων')[0],'| LXX',phrase(LX,r'ορων (τον )?θεον|θεον ορων')[0])
print('c peacemaker:',phrase(PH,r'ειρηνοποι'),'| Jos',phrase(JO,r'ειρηνοποι'),'| LXX',phrase(LX,r'ειρηνοποι'),'| NT',phrase([(r,s,t) for r,(s,t) in NT.items()],r'ειρηνοποι'))
print('d treasure+heaven:',find(PH,['θησαυ'],['ουραν']),'| Jos',find(JO,['θησαυ'],['ουραν']),'| LXX',find(LX,['θησαυ'],['ουραν']))
print('e desire+adultery:',find(PH,['επιθυ'],['μοιχε','μοιχο','μοιχα','μοιχι']),'| Jos',find(JO,['επιθυ'],['μοιχε','μοιχο','μοιχα','μοιχι']),'| LXX',find(LX,['επιθυ'],['μοιχε','μοιχο','μοιχα','μοιχι']))
