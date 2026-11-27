import sys,math,random,collections,json
from tisch import load
def chap(V):
    C=collections.defaultdict(collections.Counter)
    for (c,v),toks in V.items():
        for lem,tag,_ in toks:
            if tag[:2] in('N-','A-','V-'): C[c][lem]+=1
    return C
NT={b:load(b) for b in ['MT','MR','LU','JOH','AC','RE','RO','1CO','HEB']}
df=collections.Counter()
nv=0
for b,V in NT.items():
    for k,toks in V.items():
        nv+=1
        for lem in {l for l,t,_ in toks if t[:2] in('N-','A-','V-')}: df[lem]+=1
def idf(l): return math.log(nv/df[l]) if df[l]<=150 else 0.0
def matrix(src,tgt):
    A,B=chap(NT[src]),chap(NT[tgt]); R=sorted(A); J=sorted(B)
    M=[[sum(idf(l) for l in A[r] if l in B[j]) for j in J] for r in R]
    rs=[sum(x) for x in M]; cs=[sum(M[i][k] for i in range(len(R))) for k in range(len(J))]; tot=sum(rs)
    OE=[[M[i][k]/(rs[i]*cs[k]/tot) if rs[i] and cs[k] else 0 for k in range(len(J))] for i in range(len(R))]
    return R,J,OE
def stat(best,tol=2): return sum(1 for a,b in zip(best,best[1:]) if abs(a-b)<=tol)
def run(src,tgt,show=False):
    R,J,OE=matrix(src,tgt); best=[max(range(len(J)),key=lambda k:OE[i][k]) for i in range(len(R))]
    s=stat(best); random.seed(7); n=0; N=5000; idx=list(range(len(J))); tot=0
    for _ in range(N):
        random.shuffle(idx); pos={k:i for i,k in enumerate(idx)}; x=stat([pos[b] for b in best]); tot+=x
        if x>=s: n+=1
    print(f"{src}x{tgt}: adjacent pairs within 2: {s} of {len(R)-1} | permutation mean {tot/N:.2f} | p {n/N:.4f}")
    if show:
        print("  best chapter of %s for each chapter of %s:"%(tgt,src)); print("  "+" ".join(f"{R[i]}>{J[best[i]]}" for i in range(len(R))))
        for i in range(len(R)):
            top=sorted(range(len(J)),key=lambda k:-OE[i][k])[:3]; print(f"   {src} {R[i]:>2}: "+", ".join(f"{J[k]} ({OE[i][k]:.2f})" for k in top))
    return dict(best=[J[b] for b in best],stat=s,p=n/N)
out={}
out['RExJOH']=run('RE','JOH',True)
for t in ['MT','MR','LU','AC']: out['REx'+t]=run('RE',t)
for s in ['AC','HEB','RO']: out[s+'xJOH']=run(s,'JOH')
json.dump(out,open('john.json','w'))
