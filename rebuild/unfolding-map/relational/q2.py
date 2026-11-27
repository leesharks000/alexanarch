import itertools
exec(open('q1.py').read().split("Lr=json.load")[0])
def rt(l):
    s=strip(l)
    for p in sorted(PRE,key=len,reverse=True):
        if s.startswith(p) and len(s)-len(p)>=4: s=s[len(p):]; break
    return s[:4]
Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']
cov=set()
for r in Lr: cov|=set(keys(NT['MT'],r['matt']))
W=json.load(open('../map/rev-matthew-whole.json')); cm={tuple(int(x) for x in b.split(':')) for a,b,p,o in W['machine']}
df=collections.Counter()
for b in books:
    for k in NT[b]:
        for l in {l for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}: df[l]+=1
GOS={'MT','MR','LU','JOH'}
IDX=collections.defaultdict(list); LEM=collections.defaultdict(set)
for b in books:
    for k,t in NT[b].items():
        c=sorted({(rt(l),tg[0],l) for l,tg,_ in t if tg[:2] in('N-','A-','V-') and df[l]<=150})
        rs=sorted({(a,p) for a,p,l in c})
        for a,p,l in c: LEM[(b,k,a)].add(l)
        for (a,pa),(bb,pb) in itertools.combinations(rs,2):
            if a!=bb and (pa=='V' or pb=='V'): IDX[(a,bb)].append((b,k))
hits=collections.defaultdict(list)
for pair,occ in IDX.items():
    bs={b for b,_ in occ}
    if 'RE' in bs and 'MT' in bs and not (bs-{'RE'}-GOS):
        for b1,k1 in occ:
            if b1!='RE': continue
            for b2,k2 in occ:
                if b2!='MT': continue
                la=LEM[('RE',k1,pair[0])]|LEM[('RE',k1,pair[1])]; lb=LEM[('MT',k2,pair[0])]|LEM[('MT',k2,pair[1])]
                if la!=lb: hits[k2].append((k1,sorted(la),sorted(lb),sorted(bs-{'RE','MT'})))   # at least one lemma reformed
tot={k for k in hits}
new=sorted(tot-cov-cm)
print('root pairs with a reformed lemma: Matthew verses',len(tot),'| outside ledger and lemma layer:',len(new))
for k in new:
    a=hits[k][0]; print(f'MT {k[0]}:{k[1]} ← RE {a[0][0]}:{a[0][1]}  {"+".join(a[1])} ⇒ {"+".join(a[2])} [{",".join(a[3]) or "Mt alone"}]' + (f' (+{len(hits[k])-1})' if len(hits[k])>1 else ''))
