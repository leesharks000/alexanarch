import sys,json,re,collections,unicodedata
exec(open('../residue/r1.py').read().split("print('P1")[0])
N=nf
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c)).lower().replace('ς','σ')
PRE=['συν','συμ','συγ','συλ','απο','αφ','επι','εφ','επ','κατα','καθ','κατ','ανα','αν','δια','δι','εκ','εξ','εισ','εν','εμ','εγ','περι','προσ','προ','υπο','υφ','υπερ','παρα','παρ','μετα','μεθ','μετ','αντι','ανθ']
def root(l):
    s=strip(l)
    return s[:5] if len(s)>=5 else s
def keys(V,s):
    out=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); out+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return out
Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']
def cont(b,ks): return {(l,t[0]) for k in ks for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}
df=collections.Counter()
for b in books:
    for k in NT[b]:
        for l in {l for l,t,_ in NT[b][k]}: df[l]+=1
pairs=collections.Counter(); ex=[]; verbier=0; n=0; dirs=collections.Counter()
for r in Lr:
    rk=keys(NT['RE'],r['rev']); mk=keys(NT['MT'],r['matt'])
    if not rk or not mk: continue
    R=cont('RE',rk); M=cont('MT',mk); n+=1
    rv=sum(1 for l,p in R if p=='V')/max(1,len(R)); mv=sum(1 for l,p in M if p=='V')/max(1,len(M)); verbier+= mv>rv
    Rl={l for l,p in R}; Ml={l for l,p in M}
    for l,p in R:
        if l in Ml or df[l]>120: continue
        for m,q in M:
            if m in Rl or m==l or df[m]>120: continue
            if root(l)==root(m) and len(strip(l))>=5:
                pairs[(l,p,m,q)]+=1; dirs[(p,q)]+=1
print('rows',n,'| Matthew side more verbal in',verbier, round(100*verbier/n))
print('same-root reformed pairs:',sum(pairs.values()),'distinct',len(pairs),'| by direction (Rev POS, Matt POS):',dict(dirs))
for (l,p,m,q),c in sorted(pairs.items(),key=lambda x:(x[0][1]+x[0][3],x[0][0])): print(f'  {l}({p}) → {m}({q})')
# declared rev_only / matt_only substitutions in the ledger
print('\nDeclared one-side lemmas (rows where the hand marked a change):')
for r in Lr:
    if r.get('rev_only') or r.get('matt_only'): print(f"  {r['rev']} → {r['matt']}: {', '.join(r.get('rev_only',[]))}  ⇒  {', '.join(r.get('matt_only',[]))}")
