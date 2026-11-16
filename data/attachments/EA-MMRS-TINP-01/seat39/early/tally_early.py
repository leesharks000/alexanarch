"""Tally of the lead coder's reach codes for the AGPh Plato/Aristotle articles 1888–1924 located in the seated text
(extract_openings.py), coded on title and opening (≈190 words) by the census codebook (../../reach5/codebook.md),
beside the census's own figures for the abstracts of 2010–2026 (notebook 4.7)."""
import json,collections
K={r['id']:r for r in json.load(open('to-code.json'))}
C=[json.loads(l) for l in open('codes-lead.jsonl')]
for c in C:
    r=K[c['id']]; q=" ".join(c['quote'].split()); assert q in r['title']+" "+" ".join(r['opening'].split()) and 6<=len(q.split())<=30, c['id']
def P(y): return "1888–1899" if y<1900 else "1900–1909" if y<1910 else "1910–1924"
T=collections.defaultdict(collections.Counter)
for c in C:
    if c['code']=='X': continue
    T[P(K[c['id']]['year'])][c['code']]+=1
    if c['code']=='D': T[P(K[c['id']]['year'])]['D-'+c['dir']]+=1
print(f"{'period':10}{'n':>4}"+"".join(f"{x:>5}" for x in "ABCDEF")+"  D open/confirm/neutral")
for p in sorted(T):
    n=sum(T[p][x] for x in "ABCDEF")
    print(f"{p:10}{n:>4}"+"".join(f"{T[p][x]:>5}" for x in "ABCDEF")+f"  {T[p]['D-open']}/{T[p]['D-confirm']}/{T[p]['D-neutral']}")
n=sum(sum(T[p][x] for x in "ABCDEF") for p in T)
print(f"{'all':10}{n:>4}"+"".join(f"{sum(T[p][x] for p in T):>5}" for x in "ABCDEF"))
print("census, AP and sister journals 2010–15/2016–20/2021–26 (%): A 31/23/25, B 17/13/16, C 28/35/34, D 7/7/6, E 14/17/17, F 2/4/2")
