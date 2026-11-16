"""Interim baseline (2026-11-15): Plato/Aristotle article titles in the Revue philosophique de Louvain (Persée OAI, 1894–),
reviews (identifiers with _t1_/_t2_) excluded, serial parts ('(suite)', '(suite et fin)', '(à suivre)') counted once,
hand-ruled S (a work's standing: authenticity, attribution, genesis or development of the corpus, composition, the
ancient lists of works) and T (the Greek text, a fragment or lost work), as in ../standing.py. L marks the medieval Latin
transmission, counted apart. Rulings by title, listed below."""
import json,re,collections,sys
S=["La genèse de l'œuvre d'Aristote","Autour des Ethiques attribuées à Aristote","Sur la composition du de Anima",
   "L'évolution de la psychologie d'Aristote","Deux écrits de jeunesse d'Aristote","Les listes anciennes des ouvrages d'Aristote",
   "Contribution à l'histoire des œuvres morales d'Aristote","Une interprétation génétiste de l'éthique aristotélicienne"]
# not ruled S, noted: 1993 "Platon, l'École de Tubingen et Giovanni Reale" (the unwritten doctrines: the dialogues' standing as the doctrine, not a work's authenticity)
T=["ΠΕΡΙ ΙΔΕΩΝ d'Aristote","«Protreptique» d'Aristote","« Protreptique » d'Aristote"]
L=["versions latines","version latine","traductions arabo-latines","traductions latines","traduction médiévale","Aristoteles latinus","Aristoteles Latinus","Manuscrits de philosophie aristotélicienne"]
PA=re.compile(r"\b(Plat[oó]\w*|Aristot\w*|Socrat\w*)",re.I)
f=sys.argv[1] if len(sys.argv)>1 else "phlou.jsonl"
R={};[R.setdefault(r['id'],r) for r in map(json.loads,open(f))]
seen=set(); rows=[]
for r in sorted(R.values(),key=lambda r:r['id']):
    if '_t1_' in r['id'] or '_t2_' in r['id'] or not PA.search(r.get('title') or ''): continue
    base=re.sub(r"\s*\((suite.*|à suivre)\)\s*$","",r['title']).strip()
    if base in seen: continue
    seen.add(base); rows.append((int(r['date'][:4]),base))
def P(y): return "1894–1919" if y<1920 else "1920–39" if y<1940 else "1940–59" if y<1960 else "1960–79" if y<1980 else "1980–99" if y<2000 else "2000–19"
tot,s,t,l=(collections.Counter() for _ in range(4))
for y,b in rows:
    p=P(y); tot[p]+=1; s[p]+=any(k in b for k in S); t[p]+=any(k in b for k in T); l[p]+=any(k in b for k in L)
print("phlou: Plato/Aristotle/Socrates article titles (distinct, reviews excluded)")
for p in sorted(tot): print(f"  {p:10} {tot[p]:4}  S {s[p]:2} ({100*s[p]/tot[p]:4.1f}%)  T {t[p]:2} ({100*t[p]/tot[p]:4.1f}%)  L {l[p]:2}")
print("S:",[b for y,b in rows if any(k in b for k in S)])
