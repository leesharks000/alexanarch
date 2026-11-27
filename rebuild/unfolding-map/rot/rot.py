import json,re,random,collections
R='/home/claude/repos/alexanarch/data/corpora/gnt-nestle1904/text'
import os,glob
idx=collections.defaultdict(list)
for f in sorted(glob.glob(R+'/*')):
    for l in open(f,encoding='utf8'):
        m=re.match(r'(\S+) (\d+):(\d+)\t',l)
        if m: idx[m.group(1)].append((int(m.group(2)),int(m.group(3))))
print({b:len(v) for b,v in idx.items() if b in('Rev','Matt','Mark','Luke','John')})
pos={b:{cv:i for i,cv in enumerate(v)} for b,v in idx.items()}
N=len(idx['Rev']); chstart={c:min(i for (ch,v),i in pos['Rev'].items() if ch==c) for c in range(1,23)}
def loc(s):
    m=re.search(r'(Rev|Matt|Mark|Luke|John) (\d+):(\d+)',s); 
    return (m.group(1),(int(m.group(2)),int(m.group(3)))) if m else None
def rank(x):
    o=sorted(range(len(x)),key=lambda i:x[i]); r=[0]*len(x); i=0
    while i<len(o):
        j=i
        while j+1<len(o) and x[o[j+1]]==x[o[i]]: j+=1
        for k in range(i,j+1): r[o[k]]=(i+j)/2
        i=j+1
    return r
def sp(a,b):
    ra,rb=rank(a),rank(b); n=len(a); ma=sum(ra)/n; mb=sum(rb)/n
    num=sum((x-ma)*(y-mb) for x,y in zip(ra,rb)); da=sum((x-ma)**2 for x in ra)**.5; db=sum((y-mb)**2 for y in rb)**.5
    return num/(da*db) if da and db else 0
def scan(pairs,label):
    # pairs: (revidx, gospel, gfrac)
    if len(pairs)<8: print(label,'n',len(pairs),'too few'); return
    rv=[p[0] for p in pairs]; g=[p[2] for p in pairs]
    res={c:sp([(r-chstart[c])%N for r in rv],g) for c in range(1,23)}
    top=sorted(res,key=lambda c:-res[c])
    random.seed(1); mx=[]
    for _ in range(1000):
        gs=g[:]; random.shuffle(gs); mx.append(max(sp([(r-chstart[c])%N for r in rv],gs) for c in range(1,23)))
    p=sum(1 for m in mx if m>=res[top[0]])/1000
    p12=sum(1 for m in mx if m>=res[12])/1000
    print(f"{label}: n={len(pairs)} | cut1 (unrotated) {res[1]:+.2f} | cut12 {res[12]:+.2f} (rank {top.index(12)+1} of 22; p vs max-over-cuts null {p12:.3f}) | best: "+', '.join(f'{c}:{res[c]:+.2f}' for c in top[:4])+f" | best p {p:.3f} | worst: {top[-1]}:{res[top[-1]]:+.2f}")
    return res
out={}
# A. engine derivations
d=json.load(open('engine/derivations.json'))['derivations']; P=[]
for x in d:
    a=loc(x['seed']); b=loc(x['target'])
    if a and b and a[0]=='Rev' and b[0] in('Matt','Mark','Luke','John') and a[1] in pos['Rev'] and b[1] in pos[b[0]]:
        P.append((pos['Rev'][a[1]],b[0],pos[b[0]][b[1]]/len(idx[b[0]])))
print('engine derivations with Rev seed and Gospel target:',len(P))
out['engine']=scan(P,'ENGINE all')
for gsp in('Matt','Mark','Luke','John'): scan([p for p in P if p[1]==gsp],'ENGINE '+gsp)
# B. machine links
L=[]
for l in open('blocks/links.tsv',encoding='utf8'):
    f=l.rstrip('\n').split('\t'); a=loc(f[0]); b=loc(f[1])
    if a and b and a[1] in pos['Rev'] and b[1] in pos[b[0]]: L.append((pos['Rev'][a[1]],b[0],pos[b[0]][b[1]]/len(idx[b[0]])))
out['links']=scan(L,'LINKS all')
for gsp in('Matt','Mark','Luke','John'): scan([p for p in L if p[1]==gsp],'LINKS '+gsp)
json.dump(out,open('rot/rot.json','w'))
