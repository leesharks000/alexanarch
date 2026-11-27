exec(open('u3.py').read().split("ms=[q[0] for q in Q]; rs=[q[1] for q in Q]; nR=len(RE)")[0])
random.seed(9); N=4000
def test(label,sub):
    a=[x for x,_ in sub]; b=[y for _,y in sub]; o=sp(a,b); s2=b[:]; le=0
    for _ in range(N): random.shuffle(s2); le+= sp(a,s2)<=o
    print(label,len(sub),'correlation',round(o,3),'p',round((le+1)/(N+1),4))
test('engine rows only',[(m,r) for m,r,k in Q if cls(L[k]['standing'])=='engine'])
test('sealed only',[(m,r) for m,r,k in Q if cls(L[k]['standing']) in('sealed','blind')])
test('machine-found this session (counted, rows 86+)',[(m,r) for m,r,k in Q if cls(L[k]['standing'])=='counted' and k>=86])
test('engine + machine-found',[(m,r) for m,r,k in Q if cls(L[k]['standing'])=='engine' or (cls(L[k]['standing'])=='counted' and k>=86)])
# U5 interpolation
sys.path.insert(0,'../residue')
import glob,os,unicodedata
D='/tmp/fetch/tischendorf-data/word-per-line/2.8/Unicode/'; books=[os.path.basename(f)[:-4] for f in sorted(glob.glob(D+'*.txt'))]
NT={b:load(b) for b in books}; df=collections.Counter()
for b in books:
    for k in NT[b]:
        for l in {l for l,t,_ in NT[b][k] if t[:2] in('N-','A-','V-')}: df[l]+=1
rare=lambda V,k:{l for l,t,_ in V[k] if t[:2] in('N-','A-','V-') and df[l]<=40}
held={mi[k] for k in MT if k[0] in (11,12)}
pairs=[(a,b) for a,b in itertools.combinations(Q,2) if 2<=b[0]-a[0]<=20 and 2<=abs(b[1]-a[1])<=25]
obs=0; exp=0; found=[]
for a,b in pairs:
    Mb=[i for i in range(a[0]+1,b[0]) if i not in held and mk_[i] not in covM]; lo,hi=sorted((a[1],b[1])); Rb=[j for j in range(lo+1,hi) if rk_[j] not in covR]
    if not Mb or not Rb: continue
    ML={}; 
    for i in Mb:
        for l in rare(MT,mk_[i]): ML.setdefault(l,i)
    RL={}
    for j in Rb:
        for l in rare(RE,rk_[j]): RL.setdefault(l,j)
    sh=set(ML)&set(RL); obs+=len(sh)
    for l in sh: found.append((l,mk_[ML[l]],rk_[RL[l]],df[l]))
    tot=0; T=60
    for _ in range(T):
        s=random.randrange(0,len(rk_)-len(Rb)); RL2=set()
        for j in range(s,s+len(Rb)): RL2|=rare(RE,rk_[j])
        tot+=len(set(ML)&RL2)
    exp+=tot/T
print('U5 pairs',len(pairs),'| rare lemmas shared between the between-stretches:',obs,'| expected from random stretches of Revelation:',round(exp,1),'| ratio',round(obs/max(exp,1e-9),2))
seen=set()
for l,m,r,d in sorted(found,key=lambda x:x[3]):
    if (l,m,r) in seen: continue
    seen.add((l,m,r)); print(f'   {l} (in {d} verses of the NT): Mt {m[0]}:{m[1]} ~ Rev {r[0]}:{r[1]}')
