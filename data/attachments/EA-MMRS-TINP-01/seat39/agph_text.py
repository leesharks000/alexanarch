"""Analysis from the seat (2026-11-16): the vocabulary of a work's standing in the full text of the Archiv für
Geschichte der Philosophie I–XXXVI (EA-CORPORA-39/01), read from the seated files at data/corpora/agph-archiv-1888-1923/text/.
Per volume: tokens; standing terms per 100,000 tokens; the same terms within 40 tokens of a Plato/Aristotle name
(the near-name rate, per 1,000 Plato/Aristotle mentions); Plato/Aristotle mentions per 100,000 tokens. Index volumes excluded.
The Archive dates every volume 1888 (the run's start), so a volume is dated 1887+n. Running heads dropped (heads.py). OCR text as served: long-s and hyphenation errors depress counts alike in every volume; 1-10 is the index."""
import json,re,sys,pathlib,collections
sys.path.insert(0,str(pathlib.Path(__file__).parent)); from heads import body
SEAT=pathlib.Path(sys.argv[1])
src=json.load(open(SEAT/"source.json"))
dates={}
LOG=json.load(open(sys.argv[2])) if len(sys.argv)>2 else []
for x in LOG: dates[x["id"]]=x.get("date")
STAND=re.compile(r"^(echtheit\w*|unecht\w*|echtheitsfrage\w*|athetes\w*|athetier\w*|abfassungszeit\w*|abfassung\w*|chronolog\w*|zeitfolge\w*|reihenfolge\w*|untergeschoben\w*|interpol\w*|authenti\w*|inauthenti\w*|spurious\w*|genuineness|apokryph\w*|apocryph\w*|unterschieb\w*|pseudo\w*)$")
PA=re.compile(r"^(plat[oa]n?\w*|aristot\w*|aristoteles\w*|sokrat\w*|socrat\w*)$")
tok=re.compile(r"[A-Za-zÄÖÜäöüßſéèàâêîôûç]+")
rows=[]
for it in src["origin"]["items"]:
    i=it["identifier"]; v=it.get("volume") or ""
    if "index" in i or "-" in v and v!="33-36": continue
    T=[w.lower().replace("ſ","s") for w in tok.findall(body((SEAT/"text"/f"{i}.txt").read_text(errors="replace")))]
    n=len(T); st=[k for k,w in enumerate(T) if STAND.match(w)]; pa=[k for k,w in enumerate(T) if PA.match(w)]
    import bisect
    near=sum(1 for k in st if (lambda j: (j<len(pa) and pa[j]-k<=40) or (j>0 and k-pa[j-1]<=40))(bisect.bisect_left(pa,k)))
    y=1887+int(v) if v.isdigit() else 1920   # vol n = 1887+n (I 1888 … XXXI 1918); XXXIII–XXXVI bound together, 1920–1924, dated 1920 here
    rows.append((v,str(y),n,len(st),near,len(pa)))
print(f"{'vol':6}{'year':6}{'tokens':>10}{'stand/100k':>12}{'near-PA':>9}{'near/1k PA':>12}{'PA/100k':>9}")
for v,y,n,s,nr,p in rows:
    print(f"{v:6}{y or '':6}{n:>10,}{1e5*s/n:>12.1f}{nr:>9}{(1e3*nr/p if p else 0):>12.1f}{1e5*p/n:>9.1f}")
def agg(lo,hi):
    R=[r for r in rows if r[1] and lo<=int(r[1])<=hi]; n=sum(r[2] for r in R); s=sum(r[3] for r in R); nr=sum(r[4] for r in R); p=sum(r[5] for r in R)
    return f"{lo}–{hi}: {n:,} tokens; standing {1e5*s/n:.1f}/100k; near Plato/Aristotle {nr} ({1e3*nr/p:.1f} per 1,000 mentions); Plato/Aristotle {1e5*p/n:.0f}/100k"
for a,b in [(1888,1899),(1900,1909),(1910,1918),(1920,1924)]: print(agg(a,b))
