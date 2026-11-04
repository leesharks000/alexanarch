import pathlib,re,difflib,unicodedata,json
D=pathlib.Path("/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/ea33/ocr")
NAMES=["TERPANDER","ALCMAN","ARION","SAPPHO","ERINNA","ALCAEUS","STESICHORUS","IBYCUS","ANACREON","ANACREONTEA","APPENDIX ANACREONTEORUM","LASUS","TELESILLA","SIMONIDES","TIMOCREON","CORINNA","LAMPROCLES","PRATINAS","DIAGORAS","CYDIAS","PRAXILLA","BACCHYLIDES","MELANIPPIDES","LICYMNIUS","PHILOXENUS","TIMOTHEUS","TELESTES","CASTORIO","HERMODOTUS","SCOLIA","CARMINA POPULARIA","FRAGMENTA ADESPOTA","INDEX POETARUM"]
G=str.maketrans("ΑΒΓΔΕΖΗΙΚΛΜΝΟΡΤΥΧΩΘΣΠ","ASGAEZHIKAMNOPTYXOOSP")
def norm(h):
    h=unicodedata.normalize("NFD",h); h="".join(c for c in h if not unicodedata.combining(c)).upper().translate(G)
    return re.sub(r"[^A-Z ]"," ",h)
def match(h):
    words=" ".join(w for w in norm(h).split() if len(w)>=3)
    if not words: return None
    best=None;bs=0
    for n in NAMES:
        for cand in (words, " ".join(words.split()[:len(n.split())])):
            s=difflib.SequenceMatcher(None,cand,n).ratio()
            if s>bs: bs,best=s,n
    return best if bs>=0.72 else None
odd={}
for p in range(1,765,2):
    t=(D/f"bergk3-p{p}.txt").read_text(errors="ignore").strip().split("\n")
    odd[p]=match(t[0][:45]) if t else None
names=[odd[p] for p in sorted(odd)]
# fill unmatched: take the next matched
seq=sorted(odd); lab={}
for i,p in enumerate(seq):
    if odd[p]: lab[p]=odd[p]; continue
    nxt=next((odd[q] for q in seq[i+1:] if odd[q]),None); prv=next((odd[q] for q in reversed(seq[:i]) if odd[q]),None)
    lab[p]=nxt if nxt else prv
page={}
for p in range(1,765):
    q=p if p%2 else p+1
    page[p]=lab.get(min(q,763))
# forward-only monotone: a name seen and left does not return
runs=[];cur=None
for p in range(1,765):
    n=page[p]
    if n!=cur: runs.append([n,p,p]); cur=n
    else: runs[-1][2]=p
print(len(runs))
for r in runs: print(r)
json.dump(runs,open(str(D.parent/"bergk_runs.json"),"w"))
