import math,random,collections,json,unicodedata
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
REV={'CHRIST':['ἀρνίον','Ἰησοῦς','Χριστός'],'ADVERSARY':['δράκων','θηρίον','διάβολος','Σατανᾶς','ὄφις','πόρνη','Βαβυλών','ψευδοπροφήτης'],'FAITHFUL':['ἅγιος','δοῦλος','μάρτυς','ἀδελφός','ἐκκλησία'],'ALL':['ἔθνος','βασιλεύς','ἄνθρωπος','λαός','φυλή']}
GOS={'CHRIST':['Ἰησοῦς'],'ADVERSARY':['Σατανᾶς','διάβολος','δαιμόνιον','Φαρισαῖος','ἀρχιερεύς','γραμματεύς','Ἰουδαῖος','Πιλᾶτος','Ἡρῴδης','Ἰούδας'],'FAITHFUL':['μαθητής','Πέτρος','Σίμων','δώδεκα','ἀδελφός','δοῦλος'],'ALL':['ὄχλος','λαός','ἔθνος','ἄνθρωπος']}
def lex(d): return {nf(l):r for r,ls in d.items() for l in ls}
def events(V,L):
    ev=[]  # (role, side, verb lemma, ref)
    last={}; n=0
    for key,toks in V.items():
        n+=1
        vi=[i for i,(l,t,_) in enumerate(toks) if t.startswith('V-')]
        for i,(l,t,_) in enumerate(toks):
            role=None
            if l in L and t[:2] in('N-','A-') and len(t)>=5:
                if l==nf('ἅγιος') and (t[3]!='P'): continue
                role=L[l]; last[(t[3],t[4])]=(role,n)
            elif l==nf('αὐτός') and t[:2]=='P-' and len(t)>=5 and (t[3],t[4]) in last and n-last[(t[3],t[4])][1]<=2:
                role=last[(t[3],t[4])][0]
            if role:
                case=t[2]
                if case not in 'NA' or not vi: continue
                j=min(vi,key=lambda k:abs(k-i))
                if abs(j-i)>4: continue
                vl,vt,_=toks[j]; voice=vt[3] if len(vt)>3 else 'A'
                side='pat' if case=='A' or (case=='N' and voice=='P') else 'agt'
                ev.append((role,side,vl,key))
    return ev
RE=load('RE'); G={b:load(b) for b in ['MT','MR','LU','JOH']}
evR=events(RE,lex(REV)); evG=[]; 
for b,V in G.items(): evG+= [(r,s,v,(b,)+k) for r,s,v,k in events(V,lex(GOS))]
print('events: Rev',len(evR),collections.Counter((r,s) for r,s,_,_ in evR)); print('events: Gospels',len(evG),collections.Counter((r,s) for r,s,_,_ in evG))
# verb rarity across both
dfv=collections.Counter(v for _,_,v,_ in evR)+collections.Counter(v for _,_,v,_ in evG); tot=sum(dfv.values())
STOP={nf(x) for x in ['εἰμί','λέγω','ἔχω','γίνομαι','ἔρχομαι','ποιέω','ὁράω','εἶπον','δίδωμι','ἀποκρίνομαι']}
def prof(ev,role,side):
    c=collections.Counter(v for r,s,v,_ in ev if r==role and s==side and v not in STOP)
    return {v:n*math.log(tot/dfv[v]) for v,n in c.items()}
def cos(a,b):
    num=sum(a[k]*b[k] for k in a if k in b); da=math.sqrt(sum(x*x for x in a.values())); db=math.sqrt(sum(x*x for x in b.values()))
    return num/(da*db) if da and db else 0.0
roles=['CHRIST','ADVERSARY','FAITHFUL','ALL']
out={}
for side in('pat','agt'):
    print(f"\n{side}: rows Revelation's seat, columns the Gospels' role (cosine of rarity-weighted verb profiles)")
    print(' '*12+''.join(f'{g:>11}' for g in roles))
    M={}
    for r in roles:
        pr=prof(evR,r,side); row=[cos(pr,prof(evG,g,side)) for g in roles]; M[r]=row
        print(f'{r:12}'+''.join(f'{x:11.3f}' for x in row)+f'   n={sum(1 for a,s,_,_ in evR if a==r and s==side)}')
    out[side]=M
# S1 permutation: shuffle Gospel role labels among patient events
pa=prof(evR,'ADVERSARY','pat'); obs=cos(pa,prof(evG,'CHRIST','pat'))-cos(pa,prof(evG,'ADVERSARY','pat'))
random.seed(3); pe=[e for e in evG if e[1]=='pat']; labs=[e[0] for e in pe]; n=0; N=2000
for _ in range(N):
    random.shuffle(labs); sh=[(l,)+e[1:] for l,e in zip(labs,pe)]
    if cos(pa,prof(sh,'CHRIST','pat'))-cos(pa,prof(sh,'ADVERSARY','pat'))>=obs: n+=1
print(f"\nS1: cos(Rev ADVERSARY as patient, Gospel CHRIST as patient) - cos(..., Gospel ADVERSARY as patient) = {obs:+.3f}; shuffle p = {n/N:.4f}")
def shared(rr,gr,side,k=22):
    a=prof(evR,rr,side); b=prof(evG,gr,side); sh=sorted((v for v in a if v in b),key=lambda v:-a[v]*b[v])[:k]
    cR=collections.Counter(v for r,s,v,_ in evR if r==rr and s==side); cG=collections.Counter(v for r,s,v,_ in evG if r==gr and s==side)
    return [(v,cR[v],cG[v]) for v in sh]
print('\nshared verbs, Rev ADVERSARY as patient / Gospel CHRIST as patient (verb, n Rev, n Gospels):'); print('  '+', '.join(f'{v} {a}/{b}' for v,a,b in shared('ADVERSARY','CHRIST','pat')))
print('shared verbs, Rev ADVERSARY as patient / Gospel ADVERSARY as patient:'); print('  '+', '.join(f'{v} {a}/{b}' for v,a,b in shared('ADVERSARY','ADVERSARY','pat')))
print('shared verbs, Rev CHRIST as patient / Gospel CHRIST as patient:'); print('  '+', '.join(f'{v} {a}/{b}' for v,a,b in shared('CHRIST','CHRIST','pat')))
print('shared verbs, Rev ADVERSARY as agent / Gospel ADVERSARY as agent:'); print('  '+', '.join(f'{v} {a}/{b}' for v,a,b in shared('ADVERSARY','ADVERSARY','agt')))
print('shared verbs, Rev ADVERSARY as agent / Gospel CHRIST as agent:'); print('  '+', '.join(f'{v} {a}/{b}' for v,a,b in shared('ADVERSARY','CHRIST','agt')))
json.dump(out,open('seats2.json','w'))
