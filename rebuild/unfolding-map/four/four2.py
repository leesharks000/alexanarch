import io,contextlib,sys
src=open('four.py').read().split("NAMES={1:")[0]
exec(src)
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

NAMES={1:'lion, white',2:'calf, red',3:'human face, black',4:'eagle, pale'}
NUM={nf(x) for x in ['δεύτερος','τρίτος','τέταρτος','τρεῖς','ἑπτά','ἄλλος','μέσος','εἷς','πρῶτος']}
def lexat(cap): return {k:{l for l in LEX[k] if l not in NUM and df[l]<=cap} for k in LEX}
print('AFTER THE FACT (rule declared after the first table was seen): numerals, ἄλλος and μέσος removed; rarity ceiling varied.\n')
for cap in (20,40,60,100,150):
    L=lexat(cap); M=matrix(L); O=oe(M); sc=best(O)
    allw=[l for k in L for l in L[k]]; sizes=[len(L[k]) for k in sorted(L)]
    random.seed(9); n=0; N=2000
    for _ in range(N):
        random.shuffle(allw); S={}; i=0
        for k,s in zip(sorted(L),sizes): S[k]=set(allw[i:i+s]); i+=s
        if best(oe(matrix(S)))[0][0]>=sc[0][0]: n+=1
    print(f"ceiling {cap}: sizes {sizes}; best "+', '.join(f"{NAMES[k].split(',')[0]}>{g}" for k,g in zip(sorted(L),sc[0][1]))+f"; score {sc[0][0]:.2f} (second {sc[1][0]:.2f}: {'/'.join(sc[1][1])}); shuffled share {n/N:.3f}")
    print('   '+' | '.join(f"{NAMES[k].split(',')[0]}: "+' '.join(f'{g} {M[k][g]}({O[k][g]:.2f})' for g in GOS) for k in sorted(L)))
# the four relations, by their verbs and tokens, through Revelation: windows holding all four
REL={1:['νικάω','στέφανος'],2:['σφάζω','μάχαιρα'],3:['ἀγοράζω','πωλέω','ἔμπορος','δηνάριον','ζυγός'],4:['θάνατος','ᾅδης','ἀποκτείνω']}
REL={k:{nf(x) for x in v} for k,v in REL.items()}
keys=list(RE); print('\nThe four relations (conquer; slay; buy and sell; death), every verse of Revelation holding each:')
for k in REL: print(' ',k,sorted(REL[k]),':',' '.join(f'{c}:{v}' for (c,v),t in RE.items() if any(l in REL[k] for l,_,_ in t)))
print('\nWindows of twelve verses holding all four relations:')
got=[]
for i in range(len(keys)):
    win=keys[i:i+12]; have={k for k in REL for kk in win if any(l in REL[k] for l,_,_ in RE[kk])}
    if len(have)==4: got.append((win[0],win[-1]))
# merge
merged=[]
for a,z in got:
    if merged and keys.index(a)<=keys.index(merged[-1][1]): merged[-1]=(merged[-1][0],z)
    else: merged.append((a,z))
print('  '+'; '.join(f'{a[0]}:{a[1]}-{z[0]}:{z[1]}' for a,z in merged))
tot=len(keys); cov=sum(keys.index(z)-keys.index(a)+1 for a,z in merged); print(f'  these cover {cov} of {tot} verses')
