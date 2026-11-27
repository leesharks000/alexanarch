import sys,re,json,collections,unicodedata as U
sys.path.insert(0,'/home/claude/unfold/seats'); import tisch
n=lambda s:U.normalize('NFC',s)
B=['MT','MR','LU','JOH','AC','RO','1CO','2CO','GA','EPH','PHP','COL','1TH','2TH','1TI','2TI','TIT','PHM','HEB','JAS','1PE','2PE','1JO','2JO','3JO','JUDE','RE']
D={}
for b in B:
    try: D[b]=tisch.load(b)
    except Exception: pass
K={b:list(D[b]) for b in D}; W={b:[D[b][k] for k in K[b]] for b in D}
LS={b:[set(x[0] for x in v) for v in W[b]] for b in D}
allL=set().union(*[s for b in LS for s in LS[b]])
ref=lambda b,i:f'{b} {K[b][i][0]}:{K[b][i][1]}'
def ck(xs):
    for x in xs:
        if n(x) not in allL: print('   !! not in text:',x)
    return [n(x) for x in xs]
# K1
x=[]
for b in D:
    for i,v in enumerate(W[b]):
        if any(t[0] in (n('ὁράω'),n('ὀπτάνομαι'),n('ὄπτομαι')) and re.search(r'V-F..-3P',t[1]) for t in v) and (n('θεός') in LS[b][i] or n('πρόσωπον') in LS[b][i]): x.append(ref(b,i))
print('K1',x)
x=[ref(b,i) for b in D for i,v in enumerate(W[b]) if any(re.search(r'V-F..-3P',t[1]) and t[2].lower().startswith(('ὄψ','ὀψ')) for t in v)]
print('   all 3pl future of seeing:',x)
# K2
g1=ck(['φονεύς','φονεύω','φόνος','ἀνδροφόνος']); g2=ck(['πόρνος','πορνεία','μοιχεύω','μοιχεία','πορνεύω']); g3=ck(['ψεῦδος','ψευδής','ψεύστης','ἐπιορκέω','ἐπίορκος','ψευδομαρτυρέω','ψευδομαρτυρία'])
x=[]
for b in D:
    last=-99
    for i in range(len(K[b])):
        win=set().union(*LS[b][i:i+20])
        if all(any(a in win for a in g) for g in (g1,g2,g3)) and any(a in LS[b][i] for g in (g1,g2,g3) for a in g):
            if i-last>20: x.append(ref(b,i)); last=i
print('K2 windows (first verse of each):',x)
# K3
p=ck(['πένθος','πενθέω']); c=ck(['παρακαλέω','ἐξαλείφω','παράκλησις'])
x=[ref(b,i) for b in D for i in range(len(K[b])) if any(a in LS[b][i] for a in p) and any(a in set().union(*LS[b][max(0,i-1):i+2]) for a in c)]
print('K3',x)
# K4
freq=collections.Counter(l for b in D for s in LS[b] for l in s)
tok=collections.Counter(t[0] for b in D for v in W[b] for t in v)
stop={l for l,_ in tok.most_common(120)}
def lem(b,sel): return set().union(*[LS[b][i] for i,k in enumerate(K[b]) if sel(k)])-stop
def toks(b,sel): return sum(1 for i,k in enumerate(K[b]) if sel(k) for t in W[b][i] if t[0] not in stop)
src=lem('RE',lambda k:(k[0]==21) or (k[0]==22 and k[1]<=15))
src2=lem('RE',lambda k:k[0] in (2,3))
print('K4 source content lemmas',len(src))
for name,sel in (('5-7',lambda k:k[0] in (5,6,7)),('8-9',lambda k:k[0] in (8,9)),('10',lambda k:k[0]==10),('13',lambda k:k[0]==13),('23',lambda k:k[0]==23),('24-25',lambda k:k[0] in (24,25)),('26-27',lambda k:k[0] in (26,27))):
    L=lem('MT',sel); T=toks('MT',sel)
    sh=src&L; rare=[l for l in sh if freq[l]<=150]
    sh2=src2&L
    print(f'   Matt {name:6} content tokens {T:5} | shared with Rev 21-22: {len(sh):3} = {1000*len(sh)/T:5.1f} per 1000 tokens; rare(<=150 vv) {len(rare):3} = {1000*len(rare)/T:5.1f} | with Rev 2-3: {1000*len(sh2)/T:5.1f}')
# K8 denominators
def content(b,i): return LS[b][i]-stop
MK=[content('MR',i) for i in range(len(K['MR']))]; LK=[content('LU',i) for i in range(len(K['LU']))]
def match(c,pool):
    if len(c)<2: return False
    need=min(3,max(2,(len(c)+1)//2))
    return any(len(c&p)>=need for p in pool)
cls={}
for i,k in enumerate(K['MT']):
    c=content('MT',i)
    cls[k]='MARK' if match(c,MK) else ('DOUBLE' if match(c,LK) else 'OWN')
rows=json.load(open('/home/claude/unfold/map/rev-matthew-ledger.json'))['rows']
cov=set(); covh=set()
for r in rows:
    for part in str(r['matt']).split(';'):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c0,a,b2=int(m.group(1)),int(m.group(2)),int(m.group(3) or m.group(2))
            s={(c0,v) for v in range(a,b2+1) if (c0,v) in cls}; cov|=s
            if r['source'].startswith('hand'): covh|=s
tot=collections.Counter(cls.values()); hit=collections.Counter(cls[k] for k in cov)
print('K8 proxy classes',dict(tot))
for c in ('MARK','DOUBLE','OWN'): print(f'   {c:7} {hit[c]:4} of {tot[c]:4} = {100*hit[c]/tot[c]:.1f}%')
print('   all',len(cov),len(cls),f'{100*len(cov)/len(cls):.1f}%')
# rows shared: how many ledger rows have a Luke verse with the row's lemmas
def haslemmas(b,ls):
    ls=[n(x) for x in ls if n(x) in allL]
    return [ref(b,i) for i in range(len(K[b])) if ls and all(l in LS[b][i] for l in ls)]
sh=collections.Counter()
for r in rows:
    if not r['source'].startswith('hand'): continue
    ls=r['lemmas']
    inL=bool(haslemmas('LU',ls)); inM=bool(haslemmas('MR',ls))
    sh[('Mark' if inM else '')+('Luke' if inL else '') or 'neither']+=1
print('hand rows whose required lemmas also stand together in a verse of:',dict(sh))
json.dump({f'{k[0]}:{k[1]}':v for k,v in cls.items()},open('matt-proxy-classes.json','w'))
