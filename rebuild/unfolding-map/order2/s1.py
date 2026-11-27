import sys,json,re,collections,random,itertools
sys.path.insert(0,'../map'); from tisch import load
MT=load('MT'); RE=load('RE'); L=json.load(open('../map/rev-matthew-ledger.json'))['rows']
def keys(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
BL=[('1–2',1,2),('3–4',3,4),('5–7 D1',5,7),('8–9',8,9),('10 D2',10,10),('11–12',11,12),('13 D3',13,13),('14–17',14,17),('18 D4',18,18),('19–23',19,23),('24–25 D5',24,25),('26–27',26,27),('28',28,28)]
PT=[('1',1,1),('2–3',2,3),('4–5',4,5),('6–7',6,7),('8–11',8,11),('12',12,12),('13',13,13),('14',14,14),('15–16',15,16),('17–18',17,18),('19–20',19,20),('21–22',21,22)]
blk=lambda c: next(n for n,a,b in BL if a<=c<=b); prt=lambda c: next(n for n,a,b in PT if a<=c<=b)
def narr(k):
    t=[tg for _,tg,_ in MT[k] if tg.startswith('V-')]
    third=any(re.match(r'V-(AA|AM|AP|IA|IM|IP|2A.)I-3',tg) or re.match(r'V-[2]?[AI].I-3',tg) for tg in t)
    sp=any(re.search(r'-[12][SP]$',tg) or re.match(r'V-..M',tg) for tg in t)
    return third and not sp
rows=[]
for i,r in enumerate(L):
    mk=keys(MT,r['matt']); rk=keys(RE,r['rev'])
    if not mk or not rk: continue
    s=str(r['standing']); src=str(r.get('source',''))
    unchosen = src.startswith('engine') or 'machine' in s or 'root instrument' in s or (s.startswith('counted') and i>=86)
    rows.append(dict(i=i,mk=mk,rk=rk,pos=min(mk),b=blk(min(mk)[0]),parts=sorted({prt(c) for c,_ in rk}),narr=sum(narr(k) for k in mk)>len(mk)/2,move=r['move'],unch=unchosen,disc=('D' in blk(min(mk)[0]))))
print('rows',len(rows),'unchosen',sum(r['unch'] for r in rows),'narrative rows',sum(r['narr'] for r in rows))
def table(rs):
    T=collections.Counter()
    for r in rs:
        for p in r['parts']: T[(r['b'],p)]+=1
    return T
def chi(T):
    rb=collections.Counter(); cp=collections.Counter(); n=sum(T.values())
    for (b,p),v in T.items(): rb[b]+=v; cp[p]+=v
    return sum((T.get((b,p),0)-rb[b]*cp[p]/n)**2/(rb[b]*cp[p]/n) for b in rb for p in cp)
def perm(rs,N=5000):
    obs=chi(table(rs)); bs=[r['b'] for r in rs]; ge=0; random.seed(7)
    for _ in range(N):
        random.shuffle(bs); T=collections.Counter()
        for r,b in zip(rs,bs):
            for p in r['parts']: T[(b,p)]+=1
        ge+= chi(T)>=obs
    return round(obs,1),(ge+1)/(N+1)
print('S1 all rows chi, p:',perm(rows),'| unchosen:',perm([r for r in rows if r['unch']]))
T=table(rows)
print('S2 table (rows: block of Matthew; columns: part of Revelation)'); print('          '+''.join(f'{p:>6}' for p,_,_ in PT))
for b,_,_ in BL: print(f'{b:<10}'+''.join(f'{T.get((b,p),0) or ".":>6}' for p,_,_ in PT))
for p,_,_ in PT:
    col=sorted(((T.get((b,p),0),b) for b,_,_ in BL),reverse=True)[:3]; print('   part',p,'top blocks:',[(b,n) for n,b in col if n])
d=[len(r['parts']) for r in rows if r['disc']]; n=[len(r['parts']) for r in rows if not r['disc']]
print('S3 mean parts per row: discourse',round(sum(d)/len(d),2),len(d),'| narrative blocks',round(sum(n)/len(n),2),len(n))
m2=[r for r in rows if 'EXCHANGE' in r['move'] or r['move'].startswith('M2')]
print('S4 M2 rows',len(m2),'in 26–27, 14:3, 16:21:',sum(1 for r in m2 if r['b']=='26–27' or r['pos'] in [(14,3),(16,21)]),[ (r['b']) for r in m2])
def s5(rs):
    sp=[r for r in rs if not r['narr']]; na=[r for r in rs if r['narr']]
    sh=[(a,b) for a in sp for b in na if set(a['rk'])&set(b['rk'])]; ns=[(a,b) for a in sp for b in na if not set(a['rk'])&set(b['rk'])]
    f=lambda P: (sum(a['pos']<b['pos'] for a,b in P),len(P))
    return f(sh),f(ns)
(a,b),(c,dn)=s5(rows); print('S5 sharing a verse of Revelation: speech first in',a,'of',b,round(100*a/max(1,b)),'% | baseline',c,'of',dn,round(100*c/dn),'%')
(a,b),(c,dn)=s5([r for r in rows if r['unch']]); print('S5 unchosen:',a,'of',b,'| baseline',round(100*c/max(1,dn)),'%')
sp=[r for r in rows if not r['narr']]; na=[r for r in rows if r['narr']]
for x in sp:
    for y in na:
        if set(x['rk'])&set(y['rk']): print('   ',L[x['i']]['rev'],'| speech Mt',L[x['i']]['matt'],'| narrative Mt',L[y['i']]['matt'],'|','speech first' if x['pos']<y['pos'] else 'narrative first')
# S6
order=[b for b,_,_ in BL]; setb=collections.defaultdict(set)
for r in rows: setb[r['b']]|=set(r['rk'])
disc=[b for b in order if 'D' in b]; nar=[b for b in order if 'D' not in b]
for dd in disc:
    prev=order[order.index(dd)-1]; j=lambda x,y: round(len(setb[x]&setb[y])/max(1,len(setb[x]|setb[y])),3)
    others=[j(dd,x) for x in nar if x!=prev]; print('S6',dd,'with preceding',prev,j(dd,prev),'| mean with other narrative blocks',round(sum(others)/len(others),3))
