"""Topical spread by object (2026-11-16): which ancient author or school each abstract is about, read from its text by a name list
(the first group named; a dialogue or treatise counts for its author). Per journal: Plato+Aristotle share; the number of distinct
groups in 20 abstracts; Shannon entropy over groups (bits). Real: 2016–26, 20 drawn, 500 draws. For the continental journals: the
number of distinct named modern philosophers in 20 abstracts, from a list of the 40 names most frequent in the real set."""
import json,re,random,collections,math
G=json.load(open("gen.json")); R=[r for r in json.load(open("../stylo/corpus.json")) if r["year"]>=2016]
GR=[("Plato",r"\bPlat(o|onic)\b|\bSocrat|\b(Republic|Phaedo|Phaedrus|Meno|Gorgias|Theaetetus|Sophist|Statesman|Timaeus|Philebus|Symposium|Laws|Protagoras|Apology|Euthyphro|Charmides|Laches|Lysis|Cratylus)\b"),
    ("Aristotle",r"\bAristot|\b(Nicomachean|Eudemian|De Anima|Metaphysics|Posterior Analytics|Prior Analytics|Topics|Physics II|Physics IV|Categories|Politics|Poetics|Rhetoric|De Caelo)\b"),
    ("Presocratics",r"\b(Heraclit|Parmenid|Zeno\b(?! of Citium)|Empedocl|Anaxagor|Democrit|Leucipp|Pythagor|Presocratic|Xenophan|Thales|Anaximand|Anaximen|Eleatic|Philolaus|atomis)"),
    ("Stoics",r"\b(Stoic|Chrysipp|Seneca|Epictet|Marcus Aurel|Hierocles|Cleanthes|Posidon|Panaet)"),
    ("Epicureans",r"\b(Epicur|Lucreti|Philodem)"),
    ("Sceptics",r"\b(Sextus|Pyrrh|Sceptic|Skeptic|Arcesila|Carneade)"),
    ("Platonists late",r"\b(Plotin|Porphyr|Procl|Iamblich|Damasc|Neoplaton|late antiqu|Middle Platon|Plutarch|Numenius|Alcinous)"),
    ("Commentators",r"\b(Alexander of Aphrodisias|Simplici|Philopon|Themisti|Ammonius|commentator)"),
    ("Science and medicine",r"\b(Euclid|Ptolem|Galen|Hippocrat|medical writer|Archimed|Hero of)"),
    ("Other ancient",r"\b(Cicero|Philo\b|Theophrast|Xenophon|Sophists?\b|Protagoras'|Gorgias'|Thucydid|Herodot|Homer|Hesiod|Augustin|Diogenes|Cynic|Cyrena|Megari)")]
def grp(t):
    best=None
    for g,p in GR:
        m=re.search(p,t)
        if m and (best is None or m.start()<best[1]): best=(g,m.start())
    return best[0] if best else "none"
def stats(texts):
    gs=[grp(t) for t in texts]; c=collections.Counter(gs); n=len(gs)
    pa=100*(c["Plato"]+c["Aristotle"])/n; H=-sum(v/n*math.log2(v/n) for v in c.values())
    return pa,len(c),H,c
rng=random.Random(0)
print(f"{'journal':10} {'P+A% real':>10} {'gen':>5} | {'groups real':>11} {'gen':>4} | {'H real':>7} {'gen':>5}")
for j in ["ap","phronesis","apeiron"]:
    rt=[r["text"] for r in R if r["j"]==j]; gt=[g["title"]+". "+g["text"] for g in G if g["j"]==j]
    rv=[stats(rng.sample(rt,20)) for _ in range(500)]
    pa,ng,H,c=stats(gt)
    import numpy as np
    print(f"{j:10} {np.mean([x[0] for x in rv]):10.0f} {pa:5.0f} | {np.mean([x[1] for x in rv]):11.1f} {ng:4} | {np.mean([x[2] for x in rv]):7.2f} {H:5.2f}   gen: {dict(c)}")
# continental names
NAMES="Husserl Heidegger Merleau-Ponty Levinas Sartre Derrida Foucault Deleuze Arendt Nietzsche Hegel Kant Beauvoir Ricoeur Gadamer Adorno Benjamin Agamben Butler Marion Henry Patočka Fink Scheler Stein Kierkegaard Schelling Fichte Marx Freud Lacan Badiou Nancy Blanchot Bataille Irigaray Fanon Wittgenstein Spinoza Descartes Plato Aristotle Ahmed Honneth Weil Murdoch Ihde Habermas Rancière Malabou Stiegler Simondon Bergson Jaspers".split()
print("\ncontinental: distinct named philosophers in 20 abstracts (list of", len(NAMES), "names)")
for j in ["rip","phiToday"]:
    rt=[r["text"] for r in R if r["j"]==j]; gt=[g["title"]+". "+g["text"] for g in G if g["j"]==j]
    f=lambda ts: len({n for t in ts for n in NAMES if re.search(r"\b"+re.escape(n)+r"\b",t)})
    print(f"  {j:9} real {np.mean([f(rng.sample(rt,20)) for _ in range(300)]):5.1f}   gen {f(gt)}")
