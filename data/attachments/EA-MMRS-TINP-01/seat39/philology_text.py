"""Analysis from the seat (2026-11-16): the measure of agph_text.py applied to the philology seats, Philologus (39/10) and the
Classical Quarterly (39/11). These are the volumes the study cites, chosen because they hold an article on a work's standing,
so their rates are an upper bound for their journals and are read beside AGPh only as the same measure, not as a sample."""
import json,re,sys,pathlib,bisect
sys.path.insert(0,str(pathlib.Path(__file__).parent)); from heads import body
C=pathlib.Path("/home/claude/alexanarch/data/corpora")
STAND=re.compile(r"^(echtheit\w*|unecht\w*|echtheitsfrage\w*|athetes\w*|athetier\w*|abfassungszeit\w*|abfassung\w*|chronolog\w*|zeitfolge\w*|reihenfolge\w*|untergeschoben\w*|interpol\w*|authenti\w*|inauthenti\w*|spurious\w*|genuineness|apokryph\w*|apocryph\w*|unterschieb\w*|pseudo\w*)$")
PA=re.compile(r"^(plat[oa]n?\w*|aristot\w*|aristoteles\w*|sokrat\w*|socrat\w*)$")
tok=re.compile(r"[A-Za-zÄÖÜäöüßſéèàâêîôûç]+")
for seat in ["philologus-cited-1858-1916","classical-quarterly-1914-1929"]:
    s=json.load(open(C/seat/"source.json")); print(seat)
    for it in s["origin"]["items"]:
        i=it["identifier"]; T=[w.lower().replace("ſ","s") for w in tok.findall(body((C/seat/"text"/f"{i}.txt").read_text(errors="replace")))]
        n=len(T); st=[k for k,w in enumerate(T) if STAND.match(w)]; pa=[k for k,w in enumerate(T) if PA.match(w)]
        near=sum(1 for k in st if (lambda j:(j<len(pa) and pa[j]-k<=40) or (j>0 and k-pa[j-1]<=40))(bisect.bisect_left(pa,k)))
        print(f"  {i:42}{str(it.get('date')):12}{n:>9,}  standing {1e5*len(st)/n:5.1f}/100k  near-PA {near:3} ({1e3*near/max(1,len(pa)):5.1f}/1k)  PA {1e5*len(pa)/n:5.0f}/100k")

# aggregates: Philologus (all cited volumes); CQ 1914; CQ 1926–1929
def agg(seat,keep,label):
    s=json.load(open(C/seat/"source.json")); N=S=NR=P=0
    for it in s["origin"]["items"]:
        i=it["identifier"]
        if not keep(i): continue
        T=[w.lower().replace("ſ","s") for w in tok.findall(body((C/seat/"text"/f"{i}.txt").read_text(errors="replace")))]
        st=[k for k,w in enumerate(T) if STAND.match(w)]; pa=[k for k,w in enumerate(T) if PA.match(w)]
        NR+=sum(1 for k in st if (lambda j:(j<len(pa) and pa[j]-k<=40) or (j>0 and k-pa[j-1]<=40))(bisect.bisect_left(pa,k)))
        N+=len(T); S+=len(st); P+=len(pa)
    print(f"{label}: {N:,} tokens; standing {1e5*S/N:.1f}/100k; near Plato/Aristotle {NR} ({1e3*NR/P:.1f} per 1,000 mentions); Plato/Aristotle {1e5*P/N:.0f}/100k")
agg("philologus-cited-1858-1916",lambda i:True,"Philologus, the eight cited volumes (V 1850 – LXXIII 1914–16)")
agg("classical-quarterly-1914-1929",lambda i:"1914" in i,"Classical Quarterly 1914 (three issues)")
agg("classical-quarterly-1914-1929",lambda i:"1914" not in i,"Classical Quarterly 1926–1929 (twelve issues)")
