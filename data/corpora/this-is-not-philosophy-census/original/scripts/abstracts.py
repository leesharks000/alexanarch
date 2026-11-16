import json,re,collections
R={r["n"]:r for r in json.load(open("codes.json"))}; W=json.load(open("census.json"))["works"]
exec(open("reach.py").read().split("def works_named")[0].split("R=json.load")[0])  # imports
src=open("reach.py").read(); PL=re.search(r'PL=r"(.*?)"\n',src).group(1); AR=re.search(r'AR=r"(.*?)"\n',src).group(1)
LOCUS=re.search(r'LOCUS=r"(.*?)"\n',src).group(1); CORPUS=re.search(r'CORPUS=r"(.*?)"\n',src).group(1); MODERN=re.search(r'MODERN=r"(.*?)"\n',src).group(1)
PUZZLE=r"puzzl|tension|inconsisten|reconcil|consistent|coheren|contradict|apparent(ly)? conflict|dilemma|problem for|difficult(y|ies) for|seems to|prima facie|objection"
RECEIVED=r"standard (view|reading|interpretation)|received (view|reading)|traditional (view|reading|interpretation)|orthodox|prevailing|commonly (held|assumed|thought|read)|scholars (have|often|generally|typically)|commentators|most interpreters|recent (scholarship|interpreters|literature)|consensus|it is often"
DEFEND=r"defend|rehabilitat|vindicat|plausib|philosophically (interesting|significant|attractive)|compelling|attractive (view|position)|we should|remains relevant"
OTHERAUTH=r"Presocratic|Heracl|Parmenides|Empedocles|Democritus|Stoic|Epicur|Plotinus|Proclus|Galen|Sextus|Xenophon|Theophrastus|Alexander of|Simplicius|Philoponus|Cicero|Seneca|Plutarch|Porphyry"
rows=[]
for w in W:
    r=R[w["n"]]
    if not w["has_abstract"] or r["group"] not in ("Plato","Aristotle"): continue
    a=re.sub(r"<[^>]+>"," ",w["abstract"]); a=re.sub(r"\s+"," ",a).strip()
    works=set(m.group(0) for m in re.finditer(PL+"|"+AR,a)); both=bool(re.search(r"Plato",a)) and bool(re.search(r"Aristot",a))
    rows.append({"year":w["year"],"title":w["title"],"words":len(a.split()),"works":len(works),"both":both,
      "other":bool(re.search(OTHERAUTH,a)),"locus":bool(re.search(LOCUS,a)),"corpus":bool(re.search(CORPUS,a,re.I)),"modern":bool(re.search(MODERN,a)),
      "puzzle":bool(re.search(PUZZLE,a,re.I)),"received":bool(re.search(RECEIVED,a,re.I)),"defend":bool(re.search(DEFEND,a,re.I)),"abstract":a})
json.dump(rows,open("abstract-codes.json","w"),ensure_ascii=False)
def show(lbl,rs):
    n=len(rs); f=lambda k:100*sum(bool(x[k]) for x in rs)/n
    print(f"{lbl:10} {n:4} one-work%={100*sum(x['works']<=1 and not x['both'] for x in rs)/n:3.0f} P&A%={f('both'):3.0f} other-author%={f('other'):3.0f} locus%={f('locus'):3.0f} about-text%={f('corpus'):3.0f} bridge%={f('modern'):3.0f} puzzle%={f('puzzle'):3.0f} vs-received%={f('received'):3.0f} defends%={f('defend'):3.0f} words={sum(x['words'] for x in rs)/n:4.0f}")
print("Plato/Aristotle articles with abstracts:",len(rows))
show("2019–22",[x for x in rows if x["year"]<=2022]); show("2023–26",[x for x in rows if x["year"]>=2023])
for y in range(2019,2027): show(str(y),[x for x in rows if x["year"]==y])
