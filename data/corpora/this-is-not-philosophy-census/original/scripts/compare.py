import json,collections,math,re
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values() if v) if n else 0
LOCUS=json.load(open("reach.json")) and None
src=open("reach.py").read(); LOC=re.search(r'LOCUS=r"(.*?)"\n',src).group(1)
FIELD={"phronesis","apeiron","ancient philosophy","oxford studies in ancient philosophy","classical quarterly","the classical quarterly","archiv für geschichte der philosophie","elenchos","rhizomata","journal of the history of philosophy","proceedings of the boston area colloquium in ancient philosophy","proceedings of the aristotelian society","philosophical review","mind","journal of hellenic studies","the journal of hellenic studies","classical philology","the philosophical review"}
SELF={"ap":"ancient philosophy","phronesis":"phronesis","apeiron":"apeiron","elenchos":"elenchos","rhizomata":"rhizomata","agph":"archiv für geschichte der philosophie"}
def dec(y): return f"{y//10*10}s"
out={}
for name in ["ap","phronesis","apeiron","elenchos","rhizomata","agph"]:
    C={w["n"]:w for w in json.load(open(f"census-{name}.json"))["works"]}; R=json.load(open(f"codes-{name}.json"))
    print(f"\n== {name}"); print(f"{'decade':7} {'named':>5} {'P+A%':>5} {'H':>5} {'passage%':>8} {'reopen%':>7} {'refs/w':>6} {'self%':>5} {'field%':>6} {'pre1950%':>8}")
    by=collections.defaultdict(list)
    for r in R:
        if r["year"]: by[dec(r["year"])].append(r)
    for d in sorted(by):
        rs=by[d]; named=[r for r in rs if r["group"]!="none named"]
        if len(named)<8: continue
        g=collections.Counter(r["group"] for r in named)
        refs=[x for r in rs for x in C[r["n"]]["refs"]]; wr=[r for r in rs if C[r["n"]]["n_refs"]]
        jt=[(x.get("jt") or "").strip().lower() for x in refs]; known=[j for j in jt if j]
        selfname=SELF[name]
        yrs=[int(str(x["y"])[:4]) for x in refs if str(x.get("y") or "")[:4].isdigit()]
        print(f"{d:7} {len(named):5} {100*(g['Plato']+g['Aristotle'])/len(named):5.0f} {H(g):5.2f} {100*sum(bool(re.search(LOC,r['title'])) for r in named)/len(named):8.0f} {100*sum(r['reopen'] for r in named)/len(named):7.1f} "
              f"{(len(refs)/len(wr) if wr else 0):6.1f} {(100*sum(j==selfname for j in known)/len(known) if known else 0):5.0f} {(100*sum(j in FIELD for j in known)/len(known) if known else 0):6.0f} {(100*sum(y<1950 for y in yrs)/len(yrs) if yrs else 0):8.0f}")
