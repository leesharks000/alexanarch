"""Interim baseline, philology (2026-11-16): Plato/Aristotle/Socrates article titles in the Revue des Études Grecques
(Persée OAI, 1888–), reviews excluded (identifiers with _t1_/_t2_, and the numbered review entries '6. Janko (Richard), …'),
serial parts counted once, hand-ruled S and T as in ../standing.py. Rulings by title, listed below."""
import json,re,collections
S=["De l'unité de composition du Phèdre","Contributions à la chronologie des dialogues de Platon","Principes de stylométrie appliqués",
   "problèmes musicaux attribués à Aristote","La date des lettres 13 et 2 de Platon","La chronologie des œuvres de Platon"]
T=["copiste du Platon de Paris","scholies pour le Phèdre","fragment inédit d'un manuscrit d'Aristote","fragment de la Constitution de Delphes",
   "Notes sur le texte de Platon","Sur le texte de la « Poétique »","Une édition nouvelle des Petits Traités","La tradition patristique de Platon",
   "glose chrétienne fourvoyée dans le texte des Catégories","Théétète 155 B 1-2"]
# not ruled: 2015 Pisistratid chronology in the Constitution 'attribuée à Aristote' (the subject is the tyranny, not the work's standing)
PA=re.compile(r"\b(Plat[oó]\w*|Aristot\w*|Socrat\w*)",re.I)
R={};[R.setdefault(r['id'],r) for r in map(json.loads,open('reg.jsonl'))]
seen=set();rows=[]
for r in sorted(R.values(),key=lambda r:r['date']):
    t=r.get('title') or ''
    if '_t1_' in r['id'] or '_t2_' in r['id'] or re.match(r"\d+\.\s",t) or not PA.search(t): continue
    b=re.sub(r"\s*\((suite.*|à suivre|fin)\)\s*$","",t).strip()
    if b in seen: continue
    seen.add(b); rows.append((int(r['date'][:4]),b))
def P(y): return "1888–1919" if y<1920 else "1920–39" if y<1940 else "1940–59" if y<1960 else "1960–79" if y<1980 else "1980–99" if y<2000 else "2000–26"
tot,s,t=(collections.Counter() for _ in range(3))
for y,b in rows:
    p=P(y); tot[p]+=1; s[p]+=any(k in b for k in S); t[p]+=any(k in b for k in T)
print("reg: Plato/Aristotle/Socrates article titles (distinct, reviews excluded)")
for p in sorted(tot): print(f"  {p:10} {tot[p]:4}  S {s[p]:2} ({100*s[p]/tot[p]:4.1f}%)  T {t[p]:2} ({100*t[p]/tot[p]:4.1f}%)")
