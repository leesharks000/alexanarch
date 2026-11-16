import json,re,sys,collections
PA=re.compile(r"\b(Plat[oó]\w*|platonici\w*|Aristot\w*|Aristote|Stagirite|Socrat\w*|Sokrat\w*)",re.I)
LEX=re.compile(r"authenti|apocryph|inauthent|chronolog|\bdates?\b|\bordre\b|composition|unité|attribu|\btexte\b|fragment|Echtheit|interpol|manuscrit|genèse|évolution|développement|rédaction|édition|traduction|spurious|genuine",re.I)
for f in sys.argv[1:]:
    R=[json.loads(l) for l in open(f)]
    seen=set();R=[r for r in R if not (r['id'] in seen or seen.add(r['id']))]
    n=collections.Counter(); 
    for r in R:
        y=int((r.get('date') or '0')[:4] or 0); t=r.get('title') or ''
        if 'article' not in (r.get('type') or ['article']): pass
        if PA.search(t):
            n[y//10*10]+=1
            if LEX.search(t): print(f"{f[:5]}\t{y}\t{r['id'].rsplit('/',1)[1]}\t{t}")
    print(f, len(R), dict(sorted(n.items())), file=sys.stderr)
