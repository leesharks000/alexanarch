"""Stylometry of abstracts along three dimensions of convergence (2026-11-15).
LANGUAGE: function-word profile (form, independent of topic).  OPERATION: the move lexicon (what the abstract says it does).
CONCEPT: content vocabulary (TF-IDF, names and stopwords removed).  Convergence = mean pairwise cosine within a period,
bootstrapped at a fixed n (60, 200 draws) so that periods of different size are comparable. Plus formula rates and a template score."""
import json,re,random,collections,math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, ENGLISH_STOP_WORDS
R=json.load(open("corpus.json"))
def P(y): return "2000–09" if y<2010 else "2010–15" if y<2016 else "2016–20" if y<2021 else "2021–26"
for r in R: r["p"]=P(r["year"])
R=[r for r in R if r["year"]>=2000]
FW="the of and to in that is a this as for be by with which it on are not or from his but an has its have can what at their also both he we only such these one more than how was there into other even does whether thus rather itself them this our so i my me".split()
MOVES={"argue":r"\bargu(e|es|ed|ing)\b|\bcontend","show":r"\bshow(s|n|ing)?\b|\bdemonstrat","reconstruct":r"\breconstruct","defend":r"\bdefen(d|se)","resolve":r"\bresolv|\breconcil|\bdissolv|\bconsisten|\bcoheren","propose":r"\bpropos|\bsuggest|\boffer","examine":r"\bexamin|\banaly[sz]|\binvestigat|\bconsider","explore":r"\bexplor|\breflect","challenge":r"\bchalleng|\bagainst\b|\bcontrary to|\breject|\bdispute|\bcritiqu|\bcriticiz","reread":r"\breread|\breinterpret|\bnew (reading|interpretation)|\bread(ing)? of","trace":r"\btrac(e|es|ing)\b|\bgenealog","clarify":r"\bclarif|\billuminat|\bshed(s)? light|\bmake sense","distinguish":r"\bdistinguish|\bdistinction","develop":r"\bdevelop|\belaborat","apply":r"\bappl(y|ies|ied|ying)\b|\bdrawing on|\bin light of"}
RECEIVED=r"\b(scholars|commentators|interpreters|scholarship|literature|standard (view|reading|interpretation)|traditional(ly)?|commonly|widely|often (read|taken|thought|assumed)|it has been|has been (read|taken|argued|understood)|orthodox|prevailing|received view|consensus)\b"
CLAIM=r"\b(i|we) (argue|contend|show|suggest|propose|defend|claim)\b|\b(this|the present) (paper|article|essay|study|chapter) (argues|shows|contends|suggests|proposes|defends|claims|offers|aims)"
PAYOFF=r"\b(sheds? light|illuminat|allows us|enables us|makes sense|better understand|helps (us )?(to )?(understand|explain)|new light|account for|consequences for|implications for)\b"
def boot(X,idx,n=60,B=200,seed=0):
    rng=random.Random(seed); idx=list(idx)
    if len(idx)<n: n=len(idx)
    out=[]
    for _ in range(B):
        s=rng.sample(idx,n); M=X[s]; S=(M@M.T); k=len(s); out.append((S.sum()-np.trace(S))/(k*(k-1)))
    return float(np.mean(out))
texts=[r["text"] for r in R]
# LANGUAGE: relative function-word frequencies, L2-normalized
cv=CountVectorizer(vocabulary=sorted(set(FW)),token_pattern=r"(?u)\b\w+\b",lowercase=True); F=cv.fit_transform(texts).toarray().astype(float)
F=F/np.maximum(F.sum(1,keepdims=True),1); F=F-F.mean(0); F=F/np.maximum(np.linalg.norm(F,axis=1,keepdims=True),1e-9)
# OPERATION: move-vector counts
O=np.array([[len(re.findall(p,t,re.I)) for p in MOVES.values()] for t in texts],float); O=O/np.maximum(np.linalg.norm(O,axis=1,keepdims=True),1e-9)
# CONCEPT: content TF-IDF, proper names removed (capitalized tokens not at sentence start are dropped)
def content(t):
    t=re.sub(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-zà-ÿ’']+\b"," ",t); return t
tv=TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS|set(FW)),min_df=3,token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z\-]{2,}\b",sublinear_tf=True)
C=tv.fit_transform([content(t) for t in texts]).toarray()
groups=collections.defaultdict(list)
for i,r in enumerate(R): groups[(r["field"],r["p"])].append(i); groups[(r["j"],r["p"])].append(i)
lines=[]
def row(key,ix):
    rs=[R[i] for i in ix]; n=len(ix)
    rec=sum(bool(re.search(RECEIVED,r["text"],re.I)) for r in rs)/n; cl=sum(bool(re.search(CLAIM,r["text"],re.I)) for r in rs)/n
    pay=sum(bool(re.search(PAYOFF,r["text"],re.I)) for r in rs)/n
    tmpl=sum(bool(re.search(RECEIVED,r["text"],re.I)) and bool(re.search(CLAIM,r["text"],re.I)) for r in rs)/n
    fp=sum(bool(re.search(r"\b(I|my)\b",r["text"])) for r in rs)/n
    mv=collections.Counter(); [mv.update(k for k,p in MOVES.items() if re.search(p,r["text"],re.I)) for r in rs]
    tot=sum(mv.values()); Hm=-sum(v/tot*math.log2(v/tot) for v in mv.values()) if tot else 0
    words=sum(len(r["text"].split()) for r in rs)/n
    return f"{key[0]:12} {key[1]:8} {n:4} {boot(F,ix):6.3f} {boot(O,ix):6.3f} {boot(C,ix):6.3f}   {100*cl:4.0f} {100*rec:4.0f} {100*tmpl:4.0f} {100*pay:4.0f} {100*fp:4.0f}  {Hm:4.2f} {words:4.0f}"
hdr="group        period      n   LANG    OPER   CONC   claim% recv% tmpl% payoff% 1st%  Hmove words"
print("Mean pairwise cosine (bootstrapped, n=60); higher = more alike.\n"+hdr)
for f in ["ancient","continental","analytic"]:
    for p in ["2000–09","2010–15","2016–20","2021–26"]:
        if len(groups[(f,p)])>=30: print(row((f,p),groups[(f,p)]))
print("\nby journal\n"+hdr)
for j in ["ap","phronesis","apeiron","elenchos","rhizomata","agph","rip","phiToday","cpr","ppr","nous","mind"]:
    for p in ["2000–09","2010–15","2016–20","2021–26"]:
        if len(groups[(j,p)])>=30: print(row((j,p),groups[(j,p)]))
# cross-field convergence: mean cosine between ancient and continental abstracts in the same period
print("\ncross-field mean cosine, same period")
rng=random.Random(1)
for p in ["2000–09","2010–15","2016–20","2021–26"]:
  for f1,f2 in [("ancient","continental"),("ancient","analytic"),("continental","analytic")]:
    a=groups[(f1,p)]; c=groups[(f2,p)]
    if len(a)<30 or len(c)<30: continue
    vals=[]
    for M in (F,O,C):
        v=[]
        for _ in range(200):
            sa=rng.sample(a,min(60,len(a))); sc=rng.sample(c,min(60,len(c))); v.append(float((M[sa]@M[sc].T).mean()))
        vals.append(np.mean(v))
    print(f"  {p} {f1[:4]}x{f2[:4]}  LANG {vals[0]:.3f}  OPER {vals[1]:.3f}  CONC {vals[2]:.3f}")
# concept novelty: share of a period's content vocabulary (df>=3 in period) absent from all earlier periods, per field
print("\nconcept novelty and concentration")
vocab=tv.get_feature_names_out()
for f in ["ancient","continental","analytic"]:
    seen=set()
    for p in ["2000–09","2010–15","2016–20","2021–26"]:
        ix=groups[(f,p)]
        if not ix: continue
        df=(C[ix]>0).sum(0); terms=set(vocab[df>=3]); new=terms-seen if seen else set()
        tok=C[ix].sum(0); top=np.sort(tok)[::-1]; conc=top[:100].sum()/tok.sum()
        print(f"  {f:12} {p}  terms={len(terms):5}  new={100*len(new)/len(terms) if seen else float('nan'):5.1f}%  top100-share={100*conc:4.1f}%")
        seen|=terms
