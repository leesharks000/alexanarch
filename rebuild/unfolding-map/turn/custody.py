import unicodedata,glob,os,json
from tisch import load
nf=lambda s:unicodedata.normalize('NFC',s)
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'
books=[os.path.basename(f)[:-4] for f in sorted(glob.glob(D+'*.txt'))]
M=[nf(x) for x in ['ἄγγελος','καταβαίνω','κλείς','ἄβυσσος','ἅλυσις','κρατέω','πιάζω','δέω','βάλλω','κλείω','σφραγίζω','λύω','φυλακή','ἀνοίγω','χίλιοι','πλανάω']]
RE=load('RE'); src={l for k in [(20,1),(20,2),(20,3),(20,7),(19,20)] for l,_,_ in RE[k] if l in M}
print('members present in Rev 19:20, 20:1-3, 20:7:',sorted(src))
rows=[]
for b in books:
    if b=='RE': continue
    V=load(b); keys=list(V)
    for i in range(len(keys)):
        win=keys[i:i+8]; got=sorted({l for k in win for l,_,_ in V[k] if l in src})
        rows.append((len(got),b,win[0],win[-1],got))
rows.sort(key=lambda r:-r[0]); seen=[]; out=[]
for n,b,a,z,got in rows:
    if any(b==b2 and abs(a[0]-a2[0])<=1 and abs((a[0]*200+a[1])-(a2[0]*200+a2[1]))<40 for b2,a2 in seen): continue
    seen.append((b,a)); out.append((n,b,a,z,got))
    if len(out)>=12: break
for n,b,a,z,got in out: print(f'  {n} of {len(src)}  {b} {a[0]}:{a[1]}-{z[0]}:{z[1]}  '+', '.join(got))
json.dump([(n,b,list(a),list(z),got) for n,b,a,z,got in out],open('custody.json','w'),ensure_ascii=False)
A=load('AC')
for v in (4,6,7,10,11): print('AC 12:%d'%v,' '.join(w for _,_,w in A[(12,v)]))
for k in [(20,1),(20,2),(20,3),(20,7)]: print('RE %d:%d'%k,' '.join(w for _,_,w in RE[k]))
