import json,re,collections
R=json.load(open("codes.json")); W={w["n"]:w for w in json.load(open("census.json"))["works"]}
PL=r"Republic|Laws|Timaeus|Phaedo|Symposium|Phaedrus|Theaetetus|Sophist\b|Statesman|Politicus|Philebus|Meno|Euthyphro|Apology|Crito\b|Charmides|Laches|Lysis|Euthydemus|Cratylus|\bIon\b|Hippias|Menexenus|Alcibiades|Critias|Clitophon|Epinomis|Parmenides|Gorgias|Protagoras|Letter"
AR=r"Metaphysics|Nicomachean|Eudemian|\bEthics\b|De Anima|On the Soul|Categories|Analytics|Topics|Refutations|Rhetoric|Poetics|De Interpretatione|Generation and Corruption|generatione|De Caelo|Meteorolog|Parts of Animals|Generation of Animals|History of Animals|Historia|Magna Moralia|Protrepticus|Physics|Politics|Organon|De Motu|Parva Naturalia|De Sensu|Memoria"
LOCUS=r"\b\d{2,4}\s?[a-e]\s?\d{0,2}\b|\b(?:[IVX]{1,4}|[A-ZΑ-Ω]|α|Λ|Ζ|Θ|Γ|Δ|Η)\s?\.?\s?\d{1,2}\b|\bBook\s+[IVX\dA-ZΑ-Ω]|\bfr\.|\bB\d|\bDK\b|\bchapters?\s+\d|\bch\.\s?\d|\b[ivx]{1,4}\s\d{1,2}\b|\b\d{1,2}\.\d{1,3}\b"
CORPUS=r"authentic|spurious|authorship|chronolog|develop(ment|mental)|unity of|composition of|structure of the|the dialogue form|dramatic|literary form|order of|esoteric|unwritten|corpus|the dialogues|Socratic dialogues|interpolat|text of|transmission|lost work|exoteric|early dialogues|late dialogues|middle dialogues|reading order|prologue|frame"
MODERN=r"Kant|Hegel|Heidegger|Gadamer|Nietzsche|Descartes|Spinoza|Leibniz|Hume|Locke|Wittgenstein|Frege|Russell|Husserl|Derrida|Strauss|Rawls|contemporary|modern|Aquinas|Medieval|Renaissance|today|Maimonides|Averroes|Avicenna|Arabic|Islamic|Byzantine"
EXEG=r"^(?:Plato|Aristotle|Socrates)(?:’s|'s)? (?:on|account of|conception of|theory of|notion of|view of|argument|analysis of|definition of|treatment of|doctrine of|use of|criticism of|critique of)|^(?:Plato|Aristotle)(?:’s|'s) [A-Z]?[a-z]+$|^(?:Plato|Aristotle) on "
def works_named(t):
    return len(set(m.group(0) for m in re.finditer(PL+"|"+AR,t)))
def period(y): return "1980–89" if y<1990 else "1990–99" if y<2000 else "2000–09" if y<2010 else "2010–19" if y<2020 else "2020–26"
rows=collections.defaultdict(list)
for r in R:
    if r["kind"]!="article" or r["group"] not in ("Plato","Aristotle"): continue
    t=r["title"]; rows[period(r["year"])].append({
      "locus":bool(re.search(LOCUS,t)),"multi":works_named(t)>=2 or (bool(re.search("Plato",t)) and bool(re.search("Aristot",t))),
      "corpus":bool(re.search(CORPUS,t,re.I)),"modern":bool(re.search(MODERN,t)),"exeg":bool(re.search(EXEG,t)),
      "work_named":works_named(t)>=1,"title":t,"year":r["year"]})
print(f"{'period':8} {'n':>4} {'passage%':>8} {'work%':>6} {'author-only%':>12} {'multi-text%':>11} {'about-the-text%':>15} {'bridge%':>7} {'X-on-Y%':>7}")
for p in ["1980–89","1990–99","2000–09","2010–19","2020–26"]:
    rs=rows[p]; n=len(rs); f=lambda k: 100*sum(x[k] for x in rs)/n
    work=100*sum((x["work_named"] and not x["locus"]) for x in rs)/n; auth=100*sum((not x["work_named"] and not x["locus"]) for x in rs)/n
    print(f"{p:8} {n:4} {f('locus'):8.0f} {work:6.0f} {auth:12.0f} {f('multi'):11.0f} {f('corpus'):15.0f} {f('modern'):7.0f} {f('exeg'):7.0f}")
json.dump(rows,open("reach.json","w"),ensure_ascii=False)
for p in ["1980–89","2020–26"]:
    print("\n",p,"about-the-text:",[x["title"][:70] for x in rows[p] if x["corpus"]][:6])
    print(p,"bridges:",[x["title"][:70] for x in rows[p] if x["modern"]][:6])
