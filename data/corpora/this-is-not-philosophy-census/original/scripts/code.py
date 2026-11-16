import json,re,collections,math,csv
W=json.load(open("census.json"))["works"]
PL=r"Republic|Laws|Timaeus|Phaedo|Symposium|Phaedrus|Theaetetus|Sophist\b|Statesman|Politicus|Philebus|Meno|Euthyphro|Apology|Crito\b|Charmides|Laches|Lysis|Euthydemus|Cratylus|\bIon\b|Hippias|Menexenus|Alcibiades|Critias|Clitophon|Epinomis|Seventh Letter|Letters? of Plato"
PLAMB=r"Parmenides|Gorgias|Protagoras"
AR=r"Metaphysics|Nicomachean|Eudemian|\bEthics\b|De Anima|Categories|Analytics|Topics|Sophistical Refutations|Rhetoric|Poetics|De Interpretatione|Generation and Corruption|De Caelo|Meteorolog|Parts of Animals|Generation of Animals|History of Animals|Historia Animalium|Magna Moralia|Protrepticus|Physics [A-Z]|Physics \d|Politics [IVX\d]|\bEN\b|\bEE\b|Organon"
GROUPS=[("Aristotle",r"Aristot|Peripatetic|"+AR),("Plato",r"Plato|Platon|Socratic dialogue|"+PL),
 ("Presocratic",r"Presocratic|Pre-Socratic|Thales|Anaximander|Anaximenes|Heracl(?:e)?itus|Xenophanes|Zeno of Elea|Eleatic|Melissus|Empedocles|Empedokl|Anaxagora|Herakleit|Democritus|Leucippus|Atomis|Pythagor|Philolaus|Archytas|Alcmaeon|Diogenes of Apollonia|Derveni|"+PLAMB),
 ("Socrates/Xenophon/Sophists",r"Socrates|Xenophon|Sophist|Prodicus|Antiphon|Thrasymachus|Isocrates|Antisthenes"),
 ("Hellenistic",r"Stoic|Chrysippus|Cleanthes|Zeno of Citium|Posidonius|Panaetius|Epicur|Lucretius|Philodemus|Sceptic|Skeptic|Pyrrh|Sextus|Arcesilaus|Carneades|Academic|Cynic|Diogenes of Sinope|Cyrenaic|Hellenistic|Theophrastus|Strato"),
 ("Imperial",r"Plutarch|Seneca|Epictetus|Marcus Aurelius|Cicero|Galen|Philo\b|Philo of|Alexander of Aphrodisias|Middle Platon|Alcinous|Numenius|Aspasius|Ptolemy|Diogenes Laertius|Musonius|Hierocles"),
 ("Late antique",r"Maximus|Hiérocl|Plotinus|Porphyry|Proclus|Iamblichus|Simplicius|Philoponus|Damascius|Syrianus|Neoplaton|Augustine|Boethius|Ammonius|Olympiodorus|Themistius|Dexippus|Hermias|Gnostic|Origen|Christian")]
GROUPS.append(("Other ancient",r"Homer|Hesiod|Thucydides|Herodotus|tragedy|Tragedy|Sophocles|Aeschylus|Euripides|Aristophanes|Hippocrat|Pindar|Sappho|Ajax|Odysseus|Agathon|Greek medicine|Galen"))
def group(t):
    for g,rx in GROUPS:
        if re.search(rx,t): 
            if g=="Presocratic" and re.search(PLAMB,t) and re.search(r"Plato|dialogue",t): return "Plato"
            return g
    return "none named"
WORK=[(re.compile(r"Plato"+r".{0,30}\b("+PL+r"|"+PLAMB+r")\b|\b("+PL+r")\b"),"P:"),(re.compile(r"\b("+AR+r")"),"A:")]
def obj(t):
    for rx,pfx in WORK:
        m=rx.search(t)
        if m: return pfx+[x for x in m.groups() if x][0].strip()
    return None
REOPEN=r"authentic|spurious|authorship|attribut|dating|date of|chronolog|interpolat|manuscript|\bMSS?\b|\bms\b|text of|emendation|textual|the text|transmission|recension|lacuna|papyr|stemma|corrupt|athetes|athetize|doxograph|reconstruct|fragment"
FORM=r"^(?:[A-Z][\w’']+(?: of [A-Z]\w+)?)(?: on | and the |’s |'s )"
def span(p):
    m=re.match(r"(\d+)\s*-\s*(\d+)",p or ""); return int(m.group(2))-int(m.group(1))+1 if m else 0
rows=[]
for w in W:
    t=w["title"]; ab=re.sub("<[^>]+>"," ",w.get("abstract") or "")
    g=group(t); src="title"
    if g=="none named" and ab: g=group(ab); src="abstract" if g!="none named" else "title"
    rows.append({"n":w["n"],"doi":w["doi"],"year":w["year"],"pages":span(w["page"]),"kind":"article" if span(w["page"])>=10 else "short",
        "group":g,"group_src":src,"object":obj(t) or "","reopen":bool(re.search(REOPEN,t,re.I)),"formula":bool(re.search(FORM,t)),"cited_by":w["cited_by"],"title":t,"authors":"; ".join(w["authors"])})
with open("codes-titles.tsv","w") as f:
    c=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter="\t"); c.writeheader(); c.writerows(rows)
json.dump(rows,open("codes.json","w"),ensure_ascii=False)
print(collections.Counter(r["group"] for r in rows))
