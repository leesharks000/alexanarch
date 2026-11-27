import collections,json,unicodedata,re
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
MEAL={nf(x) for x in ['δειπνέω','δεῖπνον','ἀριστάω','ἄριστον','κατακλίνω','ἀνακλίνω','ἀνάκειμαι','κατάκειμαι','συνανάκειμαι','ἀναπίπτω','ἐσθίω','φάγω','συνεσθίω','τράπεζα','δοχή']}
COMMON={nf(x) for x in ['ἄνθρωπος','ἀρχιερεύς','κύριος','διδάσκαλος','βασιλεύς','ἑκατοντάρχης','ἑκατόνταρχος','ἄγγελος','δοῦλος','οἰκοδεσπότης','πατήρ','υἱός','ἀνήρ','χιλίαρχος','ἡγεμών','νεανίσκος','μαθητής']}
def track(b):
    V=load(b); keys=list(V); subj=None; sv=-99; rows=[]
    for n,key in enumerate(keys):
        for i,(l,t,w) in enumerate(V[key]):
            if t.startswith('N-NSM') and (l[0].isupper() or l in COMMON): subj=l; sv=n
            if t.startswith('V-') and (re.search(r'-3S$',t) or re.search(r'P-NSM$',t)):
                rows.append((key,n,l,t,subj if n-sv<=6 else None))
    return V,keys,rows
def enters(b):
    V,keys,rows=track(b); out=[]
    for key,n,l,t,s in rows:
        if l==nf('εἰσέρχομαι') and s:
            near=[keys[k] for k in range(max(0,n-2),min(len(keys),n+3))]
            meal=sorted({x for kk in near for x,_,_ in V[kk] if x in MEAL})
            out.append((key,s,meal))
    return out,len(keys)
res={}
for b in ['MT','MR','LU','JOH','AC']:
    e,nv=enters(b); who=collections.Counter(s for _,s,m in e if m)
    J=[(k,m) for k,s,m in e if s==nf('Ἰησοῦς') or (b=='LU' and s==nf('κύριος'))]
    Jm=[(k,m) for k,m in J if m]
    res[b]=dict(nv=nv,all=len(e),J=len(J),Jm=[f'{k[0]}:{k[1]}' for k,m in Jm])
    print(f"{b}: εἰσέρχομαι with a tracked singular subject {len(e)}; Jesus {len(J)}; Jesus with a meal word within two verses {len(Jm)} = {1000*len(Jm)/nv:.2f} per 1,000 verses: "+', '.join(f'{k[0]}:{k[1]} ({"/".join(m)})' for k,m in Jm))
    print(f"    other subjects with a meal word: "+', '.join(f'{s} {c}' for s,c in who.most_common(8) if s!=nf('Ἰησοῦς')))
json.dump(res,open('laod.json','w'),ensure_ascii=False)
# the verbs of Rev 3:19-21, every occurrence in the four Gospels, with tag and tracked subject
print()
for v in ['φιλέω','ἐλέγχω','παιδεύω','κρούω','δειπνέω','καθίζω','νικάω']:
    for b in ['MT','MR','LU','JOH']:
        V=load(b); 
        for key,toks in V.items():
            for l,t,w in toks:
                if l==nf(v): print(f"  {v:9} {b} {key[0]}:{key[1]:<3} {t:12} {w}")
