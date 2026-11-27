import collections,itertools,random,json,math,unicodedata,glob,os,re
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'
books=[os.path.basename(f)[:-4] for f in sorted(glob.glob(D+'*.txt'))]
NT={b:load(b) for b in books}; RE=NT['RE']; GOS=['MT','MR','LU','JOH']
def con(t): return [l for l,tg,_ in t if tg[:2] in('N-','A-','V-')]
df=collections.Counter()
for b in books:
    for k,t in NT[b].items():
        for l in set(con(t)): df[l]+=1
SEEDV={1:[(6,1),(6,2)],2:[(6,3),(6,4)],3:[(6,5),(6,6)],4:[(6,7),(6,8)]}
CRE={1:['λέων'],2:['μόσχος'],3:['πρόσωπον','ἄνθρωπος'],4:['ἀετός','πέτομαι']}
raw={k:set(l for v in vs for l in con(RE[v])) for k,vs in SEEDV.items()}
LEX={}
for k in raw:
    others=set().union(*[raw[j] for j in raw if j!=k])
    LEX[k]={l for l in raw[k]-others if df[l]<=150}|{nf(x) for x in CRE[k] if df[nf(x)]<=150 or x in('λέων','μόσχος','ἀετός','πέτομαι','πρόσωπον')}
NAMES={1:'lion, white',2:'calf, red',3:'human face, black',4:'eagle, pale'}
for k in LEX: print(k,NAMES[k],sorted(LEX[k]))
seedverses={v for vs in SEEDV.values() for v in vs}|{(4,7)}
VS=[(k,set(con(t))) for k,t in RE.items() if k not in seedverses]
def cohesion(L):
    w=x=0
    own={l:k for k in L for l in L[k]}
    for key,ls in VS:
        hit=[own[l] for l in ls if l in own]
        for a,b in itertools.combinations(hit,2):
            if a==b: w+=1
            else: x+=1
    return w,x
w,x=cohesion(LEX); allw=[l for k in LEX for l in LEX[k]]; sizes=[len(LEX[k]) for k in sorted(LEX)]
random.seed(4); n=0; N=3000; ratios=[]
for _ in range(N):
    random.shuffle(allw); L={}; i=0
    for k,s in zip(sorted(LEX),sizes): L[k]=set(allw[i:i+s]); i+=s
    a,b=cohesion(L); ratios.append(a/(a+b) if a+b else 0)
    if (a/(a+b) if a+b else 0)>=w/(w+x): n+=1
print(f"\nF1 cohesion outside the seed verses: pairs within a strand {w}, across strands {x}, share within {w/(w+x):.3f}; shuffled mean {sum(ratios)/N:.3f}; p {n/N:.4f}")
# where each strand stands in Revelation
print('\nEach strand through Revelation (verses outside the seeds holding two or more of its lemmas, or one of its rarest):')
for k in sorted(LEX):
    rows=[]
    for key,ls in VS:
        h=sorted(ls&LEX[k])
        if len(h)>=2 or any(df[l]<=12 for l in h): rows.append(f"{key[0]}:{key[1]} ({', '.join(h)})")
    bych=collections.Counter(key[0] for key,ls in VS for l in ls if l in LEX[k])
    print(f" {k} {NAMES[k]}: chapters {dict(sorted(bych.items()))}\n     "+'; '.join(rows))
# Gospels
W={g:sum(len(t) for t in NT[g].values()) for g in GOS}
def matrix(L):
    M={k:{g:sum(1 for t in NT[g].values() for l,_,_ in t if l in L[k]) for g in GOS} for k in L}
    return M
def oe(M):
    rs={k:sum(M[k].values()) for k in M}; cs={g:sum(M[k][g] for k in M) for g in GOS}; tot=sum(rs.values())
    return {k:{g:(M[k][g]+0.5)/((rs[k]*cs[g]/tot)+0.5) for g in GOS} for k in M}
def best(O):
    sc=[]
    for perm in itertools.permutations(GOS):
        sc.append((sum(math.log(O[k][g]) for k,g in zip(sorted(O),perm)),perm))
    sc.sort(reverse=True); return sc
M=matrix(LEX); O=oe(M); sc=best(O)
print('\nF2 counts of each strand\'s lemmas by Gospel (observed/expected):')
print(' '*22+''.join(f'{g:>16}' for g in GOS))
for k in sorted(LEX): print(f'{k} {NAMES[k]:19}'+''.join(f'{M[k][g]:>8} ({O[k][g]:.2f})' for g in GOS))
print('best assignment:',dict(zip([NAMES[k] for k in sorted(LEX)],sc[0][1])),f'score {sc[0][0]:.3f}; second {sc[1][0]:.3f} {sc[1][1]}')
random.seed(5); n=0; N=3000
for _ in range(N):
    random.shuffle(allw); L={}; i=0
    for k,s in zip(sorted(LEX),sizes): L[k]=set(allw[i:i+s]); i+=s
    if best(oe(matrix(L)))[0][0]>=sc[0][0]: n+=1
print(f'share of shuffled lexicons whose best assignment scores as high: {n/N:.4f}')
print('\nper lemma, counts in MT MR LU JOH:')
for k in sorted(LEX):
    print(' ',k,NAMES[k]+':',' | '.join(f"{l} {'/'.join(str(sum(1 for t in NT[g].values() for x,_,_ in t if x==l)) for g in GOS)}" for l in sorted(LEX[k])))
json.dump(dict(lex={k:sorted(v) for k,v in LEX.items()},cohesion=[w,x],M=M,best=[list(sc[0][1]),sc[0][0]]),open('four.json','w'),ensure_ascii=False)
