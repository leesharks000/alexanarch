import re,collections,unicodedata,json
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
def lex(d): return {nf(l):r for r,ls in d.items() for l in ls}
LEX={
 'RE':lex({'GOD':['θεός'],'ANGEL':['ἄγγελος'],'CHRIST':['ἀρνίον','Ἰησοῦς','Χριστός'],'ADVERSARY':['δράκων','θηρίον','διάβολος','Σατανᾶς','ὄφις','πόρνη','Βαβυλών','ψευδοπροφήτης'],'FAITHFUL':['ἅγιος','δοῦλος','μάρτυς','ἀδελφός','ἐκκλησία'],'ALL':['ἔθνος','βασιλεύς','ἄνθρωπος','λαός','φυλή']}),
 'GOS':lex({'GOD':['θεός'],'ANGEL':['ἄγγελος'],'CHRIST':['Ἰησοῦς'],'ADVERSARY':['Σατανᾶς','διάβολος','δαιμόνιον','Φαρισαῖος','ἀρχιερεύς','γραμματεύς','Ἰουδαῖος','Πιλᾶτος','Ἡρῴδης','Ἰούδας'],'FAITHFUL':['μαθητής','Πέτρος','Σίμων','δώδεκα','ἀδελφός','δοῦλος'],'ALL':['ὄχλος','λαός','ἔθνος','ἄνθρωπος']}),
 'AC':lex({'GOD':['θεός'],'ANGEL':['ἄγγελος'],'CHRIST':['Ἰησοῦς','Χριστός'],'ADVERSARY':['Ἰουδαῖος','ἀρχιερεύς','Ἡρῴδης','Σαδδουκαῖος','Φαρισαῖος','Σατανᾶς','διάβολος','στρατηγός'],'FAITHFUL':['Πέτρος','Παῦλος','Σαῦλος','Στέφανος','Βαρναβᾶς','Φίλιππος','ἀπόστολος','μαθητής','ἀδελφός'],'ALL':['ὄχλος','λαός','ἔθνος','ἄνθρωπος']})}
STOP={nf(x) for x in ['εἰμί','λέγω','γίνομαι','ἔχω','ὁράω']}
SPEECH={nf(x) for x in ['λέγω','φημί','ἀποκρίνομαι','λαλέω']}
EXC={(1,8),(11,3),(17,7),(18,7),(19,10),(21,5),(21,6),(21,7),(22,9),(22,18)}
SPK={(16,15),(22,7),(22,12),(22,13),(22,16),(22,20)}
def rev_person(c,v,i,toks):
    """seat of the first person singular at token i in Revelation; and of the second person"""
    if (c==1 and v>=18) or c in(2,3) or (c,v) in SPK: return 'CHRIST'
    if c==1 and v==17:
        j=[k for k,(l,t,_) in enumerate(toks) if l==nf('λέγω')]; return 'CHRIST' if (j and i>j[0]) else 'SEER'
    if (c,v) in EXC: return None
    return 'SEER'
def voice(t):
    m=re.match(r'V-2?[A-Z]([A-Z])',t); return m.group(1) if m else 'A'
def person(t):
    m=re.search(r'-([123])([SP])$',t); return (m.group(1),m.group(2)) if m else None
def extract(book):
    V=load(book); L=LEX['RE' if book=='RE' else ('AC' if book=='AC' else 'GOS')]
    last={}; n=0; spk=adr=None; out=[]
    for key,toks in V.items():
        n+=1; c,v=key; seat=[None]*len(toks)
        for i,(l,t,w) in enumerate(toks):
            if l in L and t[:2] in('N-','A-') and len(t)>=5:
                if l==nf('ἅγιος') and t[3]!='P': continue
                seat[i]=L[l]; last[(t[3],t[4])]=(L[l],n)
            elif l==nf('αὐτός') and t[:2]=='P-' and len(t)>=5 and (t[3],t[4]) in last and n-last[(t[3],t[4])][1]<=2: seat[i]=last[(t[3],t[4])][0]
        # person pronouns as seats (accusative/dative only matter as patients)
        for i,(l,t,w) in enumerate(toks):
            if t.startswith('P-1') and t.endswith('S') and len(t)==5:
                seat[i]=rev_person(c,v,i,toks) if book=='RE' else spk
            elif t.startswith('P-2') and len(t)==5:
                seat[i]=('FAITHFUL' if c in(2,3) else None) if book=='RE' else adr
        # clauses
        bounds=[0]
        for i,(l,t,w) in enumerate(toks):
            if w and w[-1] in ',·.;': bounds.append(i+1)
        bounds.append(len(toks)); cl=[(bounds[k],bounds[k+1]) for k in range(len(bounds)-1) if bounds[k]<bounds[k+1]]
        for a,b in cl:
            for i in range(a,b):
                l,t,w=toks[i]
                if not t.startswith('V-'): continue
                if book!='RE' and l in SPEECH and (re.search(r'-3[SP]$',t) or re.search(r'P-N[SP][MF]$',t)):
                    s=d=None
                    for k in range(max(0,i-5),min(len(toks),i+6)):
                        if seat[k] and not toks[k][1].startswith('P-1') and not toks[k][1].startswith('P-2'):
                            cs=toks[k][1][2]
                            if cs=='N' and s is None: s=seat[k]
                            if cs=='D' and d is None: d=seat[k]
                    spk,adr=s,d
                if l in STOP or l in SPEECH: continue
                def near(case):
                    c2=[k for k in range(a,b) if seat[k] and len(toks[k][1])>=3 and toks[k][1][2]==case and k!=i]
                    return min(c2,key=lambda k:abs(k-i)) if c2 else None
                nom=near('N'); acc=near('A'); dat=near('D'); pr=person(t); pseat=None
                if pr:
                    if pr==('1','S'): pseat=rev_person(c,v,i,toks) if book=='RE' else spk
                    elif pr[0]=='2':
                        if book=='RE': pseat=('SEER' if (l==nf('γράφω')) else 'FAITHFUL') if c in(2,3) else None
                        else: pseat=adr
                subj=seat[nom] if nom is not None else pseat
                if voice(t)=='P':
                    ag=None
                    for k in range(a,b):
                        if toks[k][0]==nf('ὑπό'):
                            for m in range(k+1,min(b,k+4)):
                                if seat[m]: ag=seat[m]; break
                    pat=subj
                else:
                    ag=subj; pat=seat[acc] if acc is not None else (seat[dat] if dat is not None else None)
                if ag or pat: out.append((ag,l,pat,f'{c}:{v}'))
    return out
if __name__=='__main__':
    R={}
    for b in ['RE','MT','MR','LU','JOH','AC']:
        R[b]=extract(b); both=sum(1 for a,_,p,_ in R[b] if a and p)
        print(b,'relations',len(R[b]),'| with agent and patient',both,'| agents',dict(collections.Counter(a for a,_,_,_ in R[b] if a)),'| patients',dict(collections.Counter(p for _,_,p,_ in R[b] if p)))
    json.dump(R,open('relations.json','w'),ensure_ascii=False)
    print('\nRevelation, relations with both seats, first 40:'); 
    for a,v,p,k in [x for x in R['RE'] if x[0] and x[2]][:40]: print(f'   {k:6} {a} {v} {p}')
