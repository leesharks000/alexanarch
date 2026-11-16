"""Model test (2026-11-16): the 140 generated abstracts (gen.json; seven journals, twenty each, ChatGPT signed out) against the
journals' own abstracts of 2016–2026 (../stylo/corpus.json), on the measures of ../stylo/stylo.py: LANG (function words), OPER
(the move lexicon), CONC (content TF-IDF, names removed), fitted on real and generated together. Within a journal: mean pairwise
cosine, real bootstrapped at n=20 (500 draws) to match the generated sets; higher = more alike, so lower CONC = wider topical
spread. Across journals: mean cosine between two journals' sets. Topical duplication: pairs of abstracts from different journals
of the same field with CONC cosine >= 0.25, per 100 cross-journal pairs. Formula rates as in stylo.py."""
import json,re,random,collections,itertools,sys
import numpy as np
sys.path.insert(0,"../stylo")
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
G=json.load(open("gen.json")); R=[r for r in json.load(open("../stylo/corpus.json")) if r["year"]>=2016 and r["j"] in {g["j"] for g in G}]
for r in R: r["src"]="real"
for g in G: g["src"]="gen"
A=R+G; T=[a["text"] for a in A]
FW="the of and to in that is a this as for be by with which it on are not or from his but an has its have can what at their also both he we only such these one more than how was there into other even does whether thus rather itself them this our so i my me".split()
MOVES={"argue":r"\bargu(e|es|ed|ing)\b|\bcontend","show":r"\bshow(s|n|ing)?\b|\bdemonstrat","reconstruct":r"\breconstruct","defend":r"\bdefen(d|se)","resolve":r"\bresolv|\breconcil|\bdissolv|\bconsisten|\bcoheren","propose":r"\bpropos|\bsuggest|\boffer","examine":r"\bexamin|\banaly[sz]|\binvestigat|\bconsider","explore":r"\bexplor|\breflect","challenge":r"\bchalleng|\bagainst\b|\bcontrary to|\breject|\bdispute|\bcritiqu|\bcriticiz","reread":r"\breread|\breinterpret|\bnew (reading|interpretation)|\bread(ing)? of","trace":r"\btrac(e|es|ing)\b|\bgenealog","clarify":r"\bclarif|\billuminat|\bshed(s)? light|\bmake sense","distinguish":r"\bdistinguish|\bdistinction","develop":r"\bdevelop|\belaborat","apply":r"\bappl(y|ies|ied|ying)\b|\bdrawing on|\bin light of"}
CLAIM=r"\b(i|we) (argue|contend|show|suggest|propose|defend|claim)\b|\b(this|the present) (paper|article|essay|study|chapter) (argues|shows|contends|suggests|proposes|defends|claims|offers|aims)"
RECEIVED=r"\b(scholars|commentators|interpreters|scholarship|literature|standard (view|reading|interpretation)|traditional(ly)?|commonly|widely|often (read|taken|thought|assumed|interpreted|understood|treated|regarded|discussed|invoked|presented)|frequently|usually|it has been|has been (read|taken|argued|understood)|orthodox|prevailing|received view|consensus|influential)\b"
cv=CountVectorizer(vocabulary=sorted(set(FW)),token_pattern=r"(?u)\b\w+\b"); F=cv.fit_transform(T).toarray().astype(float)
F=F/np.maximum(F.sum(1,keepdims=True),1); F=F-F.mean(0); F=F/np.maximum(np.linalg.norm(F,axis=1,keepdims=True),1e-9)
O=np.array([[len(re.findall(p,t,re.I)) for p in MOVES.values()] for t in T],float); O=O/np.maximum(np.linalg.norm(O,axis=1,keepdims=True),1e-9)
def content(t): return re.sub(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-zà-ÿ’']+\b"," ",t)
tv=TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS|set(FW)),min_df=2,token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z\-]{2,}\b",sublinear_tf=True)
C=tv.fit_transform([content(t) for t in T]).toarray()
ix=collections.defaultdict(list)
for i,a in enumerate(A): ix[(a["src"],a["j"])].append(i)
rng=random.Random(0)
def within(M,I,n=20,B=500):
    if len(I)<=n: S=M[I]@M[I].T; k=len(I); return (S.sum()-np.trace(S))/(k*(k-1))
    v=[]
    for _ in range(B):
        s=rng.sample(I,n); S=M[s]@M[s].T; v.append((S.sum()-np.trace(S))/(n*(n-1)))
    return float(np.mean(v))
def across(M,I,J): return float((M[I]@M[J].T).mean())
def rate(I,pat): return 100*sum(bool(re.search(pat,A[i]["text"],re.I)) for i in I)/len(I)
JS=["ap","phronesis","apeiron","rip","phiToday","nous","ppr"]
print("within-journal mean pairwise cosine (real 2016–26 at n=20 bootstrap; gen = the 20)")
print(f"{'journal':10}{'n real':>7} | {'LANG r':>7}{'gen':>7} | {'OPER r':>7}{'gen':>7} | {'CONC r':>7}{'gen':>7} | {'claim% r':>9}{'gen':>6} | {'recv+claim% r':>14}{'gen':>6}")
for j in JS:
    r,g=ix[("real",j)],ix[("gen",j)]
    tm=lambda I: 100*sum(bool(re.search(RECEIVED,A[i]["text"],re.I)) and bool(re.search(CLAIM,A[i]["text"],re.I)) for i in I)/len(I)
    print(f"{j:10}{len(r):>7} | {within(F,r):7.3f}{within(F,g):7.3f} | {within(O,r):7.3f}{within(O,g):7.3f} | {within(C,r):7.3f}{within(C,g):7.3f} | {rate(r,CLAIM):9.0f}{rate(g,CLAIM):6.0f} | {tm(r):14.0f}{tm(g):6.0f}")
print("\nacross journals, same field: mean cosine between the two journals' sets (real | gen)")
for f,js in [("ancient",["ap","phronesis","apeiron"]),("continental",["rip","phiToday"]),("analytic",["nous","ppr"])]:
    for a,b in itertools.combinations(js,2):
        print(f"  {a:9}x {b:9} LANG {across(F,ix[('real',a)],ix[('real',b)]):.3f} | {across(F,ix[('gen',a)],ix[('gen',b)]):.3f}   OPER {across(O,ix[('real',a)],ix[('real',b)]):.3f} | {across(O,ix[('gen',a)],ix[('gen',b)]):.3f}   CONC {across(C,ix[('real',a)],ix[('real',b)]):.3f} | {across(C,ix[('gen',a)],ix[('gen',b)]):.3f}")
print("\nacross fields (gen): ancient x continental, ancient x analytic, continental x analytic, on real | gen")
FI={"ancient":["ap","phronesis","apeiron"],"continental":["rip","phiToday"],"analytic":["nous","ppr"]}
for a,b in [("ancient","continental"),("ancient","analytic"),("continental","analytic")]:
    ra=[i for j in FI[a] for i in ix[("real",j)]]; rb=[i for j in FI[b] for i in ix[("real",j)]]
    ga=[i for j in FI[a] for i in ix[("gen",j)]]; gb=[i for j in FI[b] for i in ix[("gen",j)]]
    print(f"  {a[:4]}x{b[:4]}  LANG {across(F,ra,rb):.3f} | {across(F,ga,gb):.3f}   OPER {across(O,ra,rb):.3f} | {across(O,ga,gb):.3f}   CONC {across(C,ra,rb):.3f} | {across(C,ga,gb):.3f}")
print("\ntopical duplication: cross-journal pairs within a field with CONC cosine >= 0.25, per 100 pairs (real: 20 drawn per journal, 200 draws)")
for f,js in FI.items():
    if len(js)<2: continue
    def dup(I_by_j):
        hits=tot=0
        for a,b in itertools.combinations(js,2):
            S=C[I_by_j[a]]@C[I_by_j[b]].T; hits+=(S>=0.25).sum(); tot+=S.size
        return 100*hits/tot
    g=dup({j:ix[("gen",j)] for j in js})
    rv=[dup({j:rng.sample(ix[("real",j)],20) for j in js}) for _ in range(200)]
    print(f"  {f:12} real {np.mean(rv):5.2f}  gen {g:5.2f}")
print("\nclosest cross-journal pairs in the generated sets (CONC cosine)")
P=[]
for f,js in FI.items():
    for a,b in itertools.combinations(js,2):
        for i in ix[("gen",a)]:
            for k in ix[("gen",b)]: P.append((float(C[i]@C[k]),A[i]["id"],A[i]["title"][:55],A[k]["id"],A[k]["title"][:55]))
for p in sorted(P,reverse=True)[:16]: print(f"  {p[0]:.2f}  {p[1]} {p[2]}  ||  {p[3]} {p[4]}")
