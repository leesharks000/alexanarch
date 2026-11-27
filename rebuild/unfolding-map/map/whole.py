import json,re,unicodedata,collections,itertools,glob,os
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'
books=[os.path.basename(f)[:-4] for f in sorted(glob.glob(D+'*.txt'))]
NT={b:load(b) for b in books}; GOS={'MT','MR','LU','JOH'}
df=collections.Counter()
for b in books:
    for k,t in NT[b].items():
        for l in {l for l,tg,_ in t if tg[:2] in('N-','A-','V-')}: df[l]+=1
STOPL={nf(x) for x in ['εἰμί','λέγω','ἔχω','γίνομαι','ποιέω']}
IDX=collections.defaultdict(list)
for b in books:
    for k,t in NT[b].items():
        c=sorted({(l,tg[0]) for l,tg,_ in t if tg[:2] in('N-','A-','V-') and df[l]<=150 and l not in STOPL})
        for (a,pa),(bb,pb) in itertools.combinations(c,2):
            if pa=='V' or pb=='V': IDX[(a,bb)].append((b,k))
mach=[]
for pair,occ in IDX.items():
    bs={b for b,_ in occ}
    if 'RE' in bs and 'MT' in bs and not (bs-{'RE'}-GOS):
        for (b1,k1) in occ:
            if b1!='RE': continue
            for (b2,k2) in occ:
                if b2=='MT': mach.append((k1,k2,pair,sorted(bs-{'RE','MT'})))
print('machine constructions, Revelation with Matthew (in no book outside Revelation and the Gospels):',len(mach),'| Matthew alone among the Gospels:',sum(1 for m in mach if not m[3]))
L=json.load(open('rev-matthew-ledger.json'))['rows']
def first(s):
    m=re.match(r'(\d+):(\d+)',s.strip()); return (int(m.group(1)),int(m.group(2)))
def keys(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',s):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if not m: continue
        c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
CL=[('1',1,1),('2–3',2,3),('4–5',4,5),('6',6,6),('7',7,7),('8–11',8,11),('12',12,12),('13',13,13),('14',14,14),('15–16',15,16),('17–18',17,18),('19',19,19),('20',20,20),('21–22',21,22)]
def cl(c): return next(n for n,a,b in CL if a<=c<=b)
MT=NT['MT']; nmt=len(MT)
cov_h=set(); cov_m=set(); M=collections.defaultdict(collections.Counter); Mh=collections.defaultdict(collections.Counter)
for r in L:
    mk=keys(MT,r['matt']); cov_h|=set(mk)
    for rk in {cl(k[0]) for k in keys(NT['RE'],r['rev'])}:
        for ch in {k[0] for k in mk}: Mh[ch][rk]+=1
for k1,k2,pair,oth in mach:
    cov_m.add(k2); M[k2[0]][cl(k1[0])]+=1
print(f'Matthew has {nmt} verses. In a ledger row (hand or engine): {len(cov_h)} ({100*len(cov_h)/nmt:.0f}%). Touched by a machine construction: {len(cov_m)} ({100*len(cov_m)/nmt:.0f}%). Either: {len(cov_h|cov_m)} ({100*len(cov_h|cov_m)/nmt:.0f}%).')
print('\nLedger rows by chapter of Matthew (columns: part of Revelation):')
print('Mt  '+''.join(f'{n:>6}' for n,_,_ in CL)+'   rows')
for ch in range(1,29): print(f'{ch:<4}'+''.join(f'{Mh[ch][n] or ".":>6}' for n,_,_ in CL)+f'   {sum(Mh[ch].values())}')
print('\nMachine constructions by chapter of Matthew (columns: part of Revelation):')
print('Mt  '+''.join(f'{n:>6}' for n,_,_ in CL)+'   total')
for ch in range(1,29): print(f'{ch:<4}'+''.join(f'{M[ch][n] or ".":>6}' for n,_,_ in CL)+f'   {sum(M[ch].values())}')
rs=collections.Counter(); 
for ch in M:
    for n in M[ch]: rs[n]+=M[ch][n]
vr=collections.Counter(cl(k[0]) for k in NT['RE'])
print('per part of Revelation: constructions, verses, per verse:',{n:(rs[n],vr[n],round(rs[n]/vr[n],2)) for n,_,_ in CL})
chv=collections.Counter(k[0] for k in MT); 
print('per chapter of Matthew, constructions per verse:',{ch:round(sum(M[ch].values())/chv[ch],2) for ch in range(1,29)})
json.dump(dict(machine=[(f'{a[0]}:{a[1]}',f'{b[0]}:{b[1]}',list(p),o) for a,b,p,o in mach],ledger_by_chapter={ch:dict(Mh[ch]) for ch in Mh},machine_by_chapter={ch:dict(M[ch]) for ch in M}),open('rev-matthew-whole.json','w'),ensure_ascii=False)
# render ledger in Matthew's order
rows=sorted(L,key=lambda r:first(r['matt']))
with open('ledger.md','w') as f:
    f.write('| Matthew | Revelation | In Revelation | In Matthew | Move | Standing |\n|---|---|---|---|---|---|\n')
    for r in rows:
        f.write(f"| {r['matt']} | {r['rev']} | {r['rev_relation']} | {r['matt_relation'] or '(engine entry: '+r['source'].replace('engine ','')+')'} | {r['move']} | {r['standing']} |\n")
print('ledger rows rendered:',len(rows))
