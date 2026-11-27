import math,random,collections,json,unicodedata,re
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
GOS={'CHRIST':['Ἰησοῦς'],'ADVERSARY':['Σατανᾶς','διάβολος','δαιμόνιον','Φαρισαῖος','ἀρχιερεύς','γραμματεύς','Ἰουδαῖος','Πιλᾶτος','Ἡρῴδης','Ἰούδας'],'FAITHFUL':['μαθητής','Πέτρος','Σίμων','δώδεκα','ἀδελφός','δοῦλος'],'ALL':['ὄχλος','λαός','ἔθνος','ἄνθρωπος']}
L={nf(l):r for r,ls in GOS.items() for l in ls}
SPEECH={nf(x) for x in ['λέγω','εἶπον','φημί','ἀποκρίνομαι','λαλέω']}
STOP={nf(x) for x in ['εἰμί','λέγω','ἔχω','γίνομαι','ἔρχομαι','ποιέω','ὁράω','εἶπον','δίδωμι','ἀποκρίνομαι']}
STOP_P={nf(x) for x in ['εἰμί','λέγω','εἶπον','ἀποκρίνομαι']}  # for first-person and imperative profiles keep give, do, come, have: they are the promises
def is1s(t): return t.startswith('V-') and t.endswith('-1S')
def isimp2(t): return t.startswith('V-') and re.search(r'M-2[SP]$',t) is not None
# ---------- Revelation by rule
RE=load('RE'); S_agent=[]; R_agent=[]; C_imp=[]
def in_speaker(c,v,i,toks):
    if (c==1 and v>=18) or c in(2,3): return True
    if c==1 and v==17:
        j=[k for k,(l,t,_) in enumerate(toks) if l==nf('λέγω')]; return bool(j) and i>j[0]
    return (c,v) in {(16,15),(22,7),(22,12),(22,13),(22,16),(22,20)}
EXC={(1,8),(11,3),(17,7),(18,7),(19,10),(21,5),(21,6),(21,7),(22,9),(22,18)}
for (c,v),toks in RE.items():
    for i,(l,t,w) in enumerate(toks):
        if is1s(t):
            if in_speaker(c,v,i,toks): S_agent.append((l,(c,v)))
            elif (c,v) not in EXC and l!=nf('δείκνυμι'): R_agent.append((l,(c,v)))
        if isimp2(t) and c in(2,3) and not w.lower().startswith(('ἰδο','ἴδ','ἰδ')): C_imp.append((l,(c,v)))
print('Revelation: SPEAKER first-person verbs',len(S_agent),'| SEER first-person verbs',len(R_agent),'| ASSEMBLY imperatives',len(C_imp))
# ---------- Gospels: narrated agents (v2 rule), tracked speaker/addressee
def gospel(b):
    V=load(b); last={}; n=0; nar=[]; first=[]; cmd=[]; spk=None; adr=None
    for key,toks in V.items():
        n+=1; roles=[None]*len(toks)
        for i,(l,t,_) in enumerate(toks):
            if l in L and t[:2] in('N-','A-') and len(t)>=5: roles[i]=L[l]; last[(t[3],t[4])]=(L[l],n)
            elif l==nf('αὐτός') and t[:2]=='P-' and len(t)>=5 and (t[3],t[4]) in last and n-last[(t[3],t[4])][1]<=2: roles[i]=last[(t[3],t[4])][0]
        vi=[i for i,(l,t,_) in enumerate(toks) if t.startswith('V-')]
        for i,(l,t,w) in enumerate(toks):
            # speech verb in third person or nominative participle: update speaker/addressee
            if l in SPEECH and t.startswith('V-') and (re.search(r'-3[SP]$',t) or re.search(r'P-N[SP][MF]$',t)):
                s=a=None
                for k in range(max(0,i-5),min(len(toks),i+6)):
                    if roles[k] and len(toks[k][1])>=3:
                        if toks[k][1][2]=='N' and s is None: s=roles[k]
                        if toks[k][1][2]=='D' and a is None: a=roles[k]
                spk,adr=s,a
            if roles[i] and vi and toks[i][1][2]=='N':
                j=min(vi,key=lambda k:abs(k-i))
                if abs(j-i)<=4 and not (len(toks[j][1])>3 and toks[j][1][3]=='P') and toks[j][0] not in SPEECH: nar.append((roles[i],toks[j][0],(b,)+key))
            if is1s(t) and spk: first.append((spk,l,(b,)+key))
            if isimp2(t) and spk and adr and not w.lower().startswith(('ἰδο','ἴδ','ἰδ')): cmd.append((adr,spk,l,(b,)+key))
    return nar,first,cmd
NAR=[];FIRST=[];CMD=[]
for b in ['MT','MR','LU','JOH']:
    a,f,c=gospel(b); NAR+=a; FIRST+=f; CMD+=c
print('Gospels: narrated agent events',len(NAR),dict(collections.Counter(r for r,_,_ in NAR)),'| first-person by tracked speaker',dict(collections.Counter(r for r,_,_ in FIRST)),'| commands by addressee',dict(collections.Counter(a for a,_,_,_ in CMD)))
allv=collections.Counter(l for l,_ in S_agent+R_agent+C_imp)+collections.Counter(v for _,v,_ in NAR)+collections.Counter(v for _,v,_ in FIRST)+collections.Counter(v for _,_,v,_ in CMD); tot=sum(allv.values())
def prof(vs,stop): 
    c=collections.Counter(v for v in vs if v not in stop); return {v:n*math.log(tot/allv[v]) for v,n in c.items()}
def cos(a,b):
    num=sum(a[k]*b[k] for k in a if k in b); da=math.sqrt(sum(x*x for x in a.values())); db=math.sqrt(sum(x*x for x in b.values())); return num/(da*db) if da and db else 0.0
def shared(a,b,k=16): return sorted((v for v in a if v in b),key=lambda v:-a[v]*b[v])[:k]
def test(name,src,ev,target,stop,N=2000):
    # ev: list of (label, verb); statistic cos(src,target) - max cos(src, other)
    labs=sorted({l for l,_ in ev}); P={l:prof([v for x,v in ev if x==l],stop) for l in labs}
    row={l:cos(src,P[l]) for l in labs}; obs=row[target]-max(row[l] for l in labs if l!=target)
    random.seed(11); lab=[l for l,_ in ev]; n=0
    for _ in range(N):
        random.shuffle(lab); Q={l:prof([v for x,(_,v) in zip(lab,ev) if x==l],stop) for l in labs}; r={l:cos(src,Q[l]) for l in labs}
        if r[target]-max(r[l] for l in labs if l!=target)>=obs: n+=1
    sh=shared(src,P[target])
    print(f"\n{name}\n   "+'  '.join(f'{l} {row[l]:.3f}' for l in labs)+f"\n   predicted {target}: margin {obs:+.3f}, shuffle p {n/N:.4f}; shared verbs with {target} ({len([v for v in src if v in P[target]])}): "+', '.join(sh))
    return dict(row=row,margin=obs,p=n/N,shared=len([v for v in src if v in P[target]]))
out={}
pS=prof([l for l,_ in S_agent],STOP_P); pR=prof([l for l,_ in R_agent],STOP); pC=prof([l for l,_ in C_imp],STOP_P)
out['P1']=test("P1 Revelation's SPEAKER (first person) against the Gospels' first person, by tracked speaker",pS,[(r,v) for r,v,_ in FIRST],'CHRIST',STOP_P)
out['P2']=test("P2 Revelation's SPEAKER (first person) against the Gospels' narrated agents",pS,[(r,v) for r,v,_ in NAR],'CHRIST',STOP_P)
out['P3']=test("P3 Revelation's SEER (first person) against the Gospels' narrated agents",pR,[(r,v) for r,v,_ in NAR],'FAITHFUL',STOP)
out['P4']=test("P4 Revelation's ASSEMBLY imperatives against the Gospels' commands, by addressee",pC,[(a,v) for a,_,v,_ in CMD],'FAITHFUL',STOP_P)
print("\nRevelation's lists: SPEAKER",collections.Counter(l for l,_ in S_agent).most_common(40)); print("SEER",collections.Counter(l for l,_ in R_agent).most_common(30)); print("ASSEMBLY imperatives",collections.Counter(l for l,_ in C_imp).most_common(30))
json.dump(dict(out=out,S=S_agent,R=R_agent,C=C_imp,NAR=len(NAR),FIRST=FIRST[:0],CMD=[(a,s,v,k) for a,s,v,k in CMD]),open('persons.json','w'),ensure_ascii=False)
