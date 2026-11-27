import collections,itertools,json,unicodedata,re,glob,os,math
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'
books=[os.path.basename(f)[:-4] for f in sorted(glob.glob(D+'*.txt'))]
NT={b:load(b) for b in books}; GOS=['MT','MR','LU','JOH']
NEG={nf(x) for x in ['οὐ','μή','οὐδείς','μηδείς','οὐδέ','μηδέ','οὔτε','μήτε','οὐχί','οὐκέτι','μηκέτι','οὔπω','οὐδέποτε','μήποτε']}
df=collections.Counter()
for b in books:
    for k,t in NT[b].items():
        for l in {l for l,tg,_ in t if tg[:2] in('N-','A-','V-')}: df[l]+=1
STOPL={nf(x) for x in ['εἰμί','λέγω','ἔχω','γίνομαι','ποιέω']}
def content(t): return sorted({(l,tg[0]) for l,tg,_ in t if tg[:2] in('N-','A-','V-') and df[l]<=150 and l not in STOPL})
IDX=collections.defaultdict(list)   # pair -> [(book,key)]
for b in books:
    for k,t in NT[b].items():
        c=content(t)
        for (a,pa),(bb,pb) in itertools.combinations(c,2):
            if pa=='V' or pb=='V': IDX[(a,bb)].append((b,k))
def marks(b,k,pair):
    t=NT[b][k]; neg=False; pas=set(); per=set()
    for i,(l,tg,_) in enumerate(t):
        if l in pair:
            if any(t[j][0] in NEG for j in range(max(0,i-4),i)): neg=True
            if tg.startswith('V-'):
                m=re.match(r'V-2?[A-Z]([A-Z])',tg); 
                if m: pas.add(l+(':P' if m.group(1)=='P' else ':A'))
                p=re.search(r'-([123])[SP]$',tg)
                if p: per.add(l+':'+p.group(1))
    return neg,pas,per
def links(src,targets,part=None):
    out=[]
    for pair,occ in IDX.items():
        bs={b for b,_ in occ}
        if src not in bs or not (bs&set(targets)) or (bs-{src}-set(GOS)): continue
        if src in GOS and (bs-{src}-set(targets)-set(GOS)): continue
        so=[(b,k) for b,k in occ if b==src and (part is None or part(k))]; to=[(b,k) for b,k in occ if b in targets and b!=src]
        if not so or not to: continue
        s=so[0]; t=to[0]; ns,ps,es=marks(*s,pair); nt,pt,et=marks(*t,pair)
        vs={x.split(':')[0]:x.split(':')[1] for x in ps}; vt={x.split(':')[0]:x.split(':')[1] for x in pt}
        voice=any(v in vt and vs[v]!=vt[v] for v in vs)
        ps_={x.split(':')[0]:x.split(':')[1] for x in es}; pt_={x.split(':')[0]:x.split(':')[1] for x in et}
        person=any(v in pt_ and ps_[v]!=pt_[v] for v in ps_)
        out.append(dict(pair=pair,src=f'{s[0]} {s[1][0]}:{s[1][1]}',tgt=f'{t[0]} {t[1][0]}:{t[1][1]}',nsrc=len(so),ntgt=len(to),pol=(ns!=nt),voice=voice,person=person,turned=(ns!=nt) or voice))
    return out
def rate(L): 
    n=len(L); k=sum(1 for x in L if x['turned']); return k,n,(k/n if n else 0)
def fisher(a,b,c,d):
    # one-sided: P(X>=a) hypergeometric
    from math import comb
    n=a+b+c+d; r1=a+b; c1=a+c; p=0
    for x in range(a,min(r1,c1)+1): p+=comb(c1,x)*comb(n-c1,r1-x)/comb(n,r1)
    return p
R=links('RE',GOS); A=links('AC',GOS); M=links('MR',['MT']); H=links('HEB',GOS); J=links('JAS',GOS); P=links('1PE',GOS); RO=links('RO',GOS); C1=links('1CO',GOS); L2=links('LU',['MT']); JN=links('1JO',GOS)
res={}
for nm,L in [('Revelation',R),('Acts',A),('Mark with Matthew',M),('Luke with Matthew',L2),('Hebrews',H),('James',J),('1 Peter',P),('Romans',RO),('1 Corinthians',C1),('1 John',JN)]:
    k,n,r=rate(L); pol=sum(1 for x in L if x['pol']); vo=sum(1 for x in L if x['voice']); pe=sum(1 for x in L if x['person'])
    res[nm]=dict(n=n,turned=k,rate=r,pol=pol,voice=vo,person=pe); print(f"{nm:20} constructions {n:5}  turned {k:4} = {100*r:5.1f}%   polarity {100*pol/max(n,1):5.1f}%  voice {100*vo/max(n,1):5.1f}%  person {100*pe/max(n,1):5.1f}%")
kR,nR,_=rate(R); kA,nA,_=rate(A); kM,nM,_=rate(M)
print(f"T1: Revelation against Acts, Fisher one-sided p = {fisher(kR,nR-kR,kA,nA-kA):.4f}; against Mark with Matthew p = {fisher(kR,nR-kR,kM,nM-kM):.4f}")
Rl=[x for x in R if x['src'].split()[1].split(':')[0] in('2','3')]; Rr=[x for x in R if x not in Rl]
print('T2: letters',rate(Rl),'rest of Revelation',rate(Rr))
print('\nThe seven letters, every exclusive verb construction with a Gospel (P polarity, V voice, p person):')
for x in sorted(Rl,key=lambda x:(int(x['src'].split()[1].split(':')[0]),int(x['src'].split(':')[1]))):
    print(f"  {x['src']:9} {x['tgt']:10} {x['pair'][0]}+{x['pair'][1]:14} {'P' if x['pol'] else '-'}{'V' if x['voice'] else '-'}{'p' if x['person'] else '-'}  (Gospel verses {x['ntgt']})")
json.dump(dict(res=res,letters=[dict(x,pair=list(x['pair'])) for x in Rl]),open('turn.json','w'),ensure_ascii=False)
