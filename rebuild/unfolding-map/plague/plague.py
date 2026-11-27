import sys,itertools,json,collections,unicodedata as U
sys.path.insert(0,'/home/claude/unfold/seats'); import tisch
SP={'σῴζω':'σώζω','ἀποθνῄσκω':'ἀποθνήσκω'}
n=lambda s:U.normalize('NFC',SP.get(U.normalize('NFC',s),s))
B=['MT','MR','LU','JOH','AC','RO','1CO','2CO','GA','EPH','PHP','COL','1TH','2TH','1TI','2TI','TIT','PHM','HEB','JAS','1PE','2PE','1JO','2JO','3JO','JUDE','RE']
D={}
for b in B:
    try: D[b]=tisch.load(b)
    except Exception as e: print('skip',b,e)
K={b:list(D[b].keys()) for b in D}
LS={b:[set(x[0] for x in D[b][k]) for k in K[b]] for b in D}
allL=set().union(*[s for b in LS for s in LS[b]])
T={'D1':['ἕλκος','χόρτος','δένδρον'],'D2':['θάλασσα','πλοῖον'],'D3':['ὕδωρ','ποταμός','πηγή'],'D4':['ἥλιος','σελήνη','ἀστήρ']}
O={'D1':['θεραπεύω','ἰάομαι','καθαρίζω','ἐσθίω','χορτάζω'],'D2':['σῴζω','γαλήνη','ἐπιτιμάω','ὑπακούω','περιπατέω','κοπάζω'],'D3':['σῴζω','περιπατέω','ζάω','θεραπεύω','ἰάομαι'],'D4':['λάμπω','ἀνατέλλω','φῶς','ἀναβλέπω','ἀνοίγω']}
LOOSE={'D1':['λέπρα','λεπρός','πυρετός','νόσος','μαλακία'],'D4':['τυφλός','ὀφθαλμός','σκότος']}
for d in (T,O,LOOSE):
    for k in d:
        d[k]=[n(x) for x in d[k]]
        for x in d[k]:
            if x not in allL: print('LEMMA NOT IN TEXT',x)
def hits(b,terms,opps,sel=None,w=1):
    out=[]
    for i,k in enumerate(K[b]):
        if sel and not sel(k): continue
        t=[x for x in terms if x in LS[b][i]]
        if not t: continue
        o=set()
        for j in range(max(0,i-w),min(len(K[b]),i+w+1)):
            o|={x for x in opps if x in LS[b][j]}
        if o: out.append((k,t,sorted(o)))
    return out
mir=lambda k:k[0] in (8,9,14,15)
def table(T,O,label):
    print('==',label)
    tot=0;dom=0
    for d in T:
        h=hits('MT',T[d],O[d],mir); tot+=len(h); dom+=bool(h)
        print(d,len(h),[(f'{k[0]}:{k[1]}',t,o) for k,t,o in h])
    print('domains with a hit',dom,'total',tot)
    ds=list(T); res=[]
    for p in itertools.permutations(ds):
        res.append((sum(len(hits('MT',T[d],O[q],mir)) for d,q in zip(ds,p)),p))
    m=[r for r in res if r[1]==tuple(ds)][0][0]
    print('matched',m,'rank among 24:',1+sum(r[0]>m for r in res),'ties',sum(r[0]==m for r in res)-1,'max other',max(r[0] for r in res if r[1]!=tuple(ds)))
    nm=sum(1 for k in K['MT'] if mir(k))
    print('rate MT 8-9,14-15: %.1f per 1000 (%d verses)'%(1000*tot/nm,nm))
    for b in ['MT','MR','LU','JOH','AC','RE']:
        c=sum(len(hits(b,T[d],O[d])) for d in T); print('  ',b,c,'%.1f'%(1000*c/len(K[b])))
    a=[(k,d) for d in T for k,_,_ in hits('AC',T[d],O[d])]
    print('  Acts by chapter',collections.Counter(k[0] for k,_ in a))
    return tot
table(T,O,'STRICT')
T2={d:T[d]+LOOSE.get(d,[]) for d in T}
table(T2,O,'LOOSENED')
def near(a,bs,w):
    out=[]
    for b in D:
        for i,k in enumerate(K[b]):
            if a in LS[b][i] and any(x in LS[b][j] for j in range(max(0,i-w),min(len(K[b]),i+w+1)) for x in bs):
                out.append(f'{b} {k[0]}:{k[1]}')
    return out
print('S2',near(n('ἀποθνῄσκω'),[n('ὕδωρ')],1))
s3=[]
for b in D:
    for i,k in enumerate(K[b]):
        if n('βλασφημέω') in LS[b][i]:
            for j in range(max(0,i-6),min(len(K[b]),i+7)):
                if n('δοξάζω') in LS[b][j] or (n('δόξα') in LS[b][j] and n('δίδωμι') in LS[b][j]):
                    s3.append(f'{b} {k[0]}:{k[1]}~{K[b][j][0]}:{K[b][j][1]}')
print('S3',len(s3),s3)
