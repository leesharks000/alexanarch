import json,re,collections,math,sys
NAMES="""Kant Hegel Fichte Schelling Hölderlin|Holderlin Schleiermacher Kierkegaard Marx Nietzsche Dilthey Husserl Heidegger Scheler Jaspers Sartre Beauvoir Merleau-Ponty Levinas|Lévinas Gadamer Ricoeur|Ricœur Arendt Adorno Horkheimer Benjamin Marcuse Habermas Derrida Foucault Deleuze Guattari Lacan Freud Lyotard Bataille Blanchot Irigaray Kristeva Badiou Žižek|Zizek Agamben Nancy Rancière|Ranciere Butler Stiegler Malabou Patočka|Patocka Fink Henry Marion Bergson Schopenhauer Spinoza Plato|Platonic Aristotle|Aristotelian Descartes|Cartesian Leibniz Hume Rousseau Wittgenstein Frege Peirce James Dewey Whitehead Schmitt Löwith Strauss Kojève|Kojeve Hyppolite Cassirer Natorp Cohen Rickert Brentano Stein Gurwitsch Schutz Ingarden Waldenfels Lingis Bachelard Canguilhem Simondon Laruelle Meillassoux Haraway Latour Fanon Glissant Wynter Spivak Said Hall Bourdieu Althusser Lukács|Lukacs Gramsci Bloch Kafka Celan Rilke Trakl Augustine Eckhart Pascal Vico Herder Hamann Jacobi Novalis Schlegel Goethe Lessing Mendelssohn Kracauer Weber Simmel Plessner Gehlen Uexküll Jonas Anders Tugendhat Henrich Sloterdijk Han Honneth Jaeggi""".split()
PAT={n.split('|')[0]:re.compile(r"\b(?:"+n+r")(?:'s|’s|ian|ean|ism)?\b") for n in NAMES}
AMBIG=set("Han James Hall Said Fink Henry Marion Stein Nancy Bloch Cohen Weber Jonas Anders Strauss Benjamin Butler Peirce Jacobi Fanon Schmitt".split())
PATI={k:re.compile(p.pattern,re.I) for k,p in PAT.items() if k not in AMBIG}
NAME=sys.argv[1]
W=json.load(open(f"census-{NAME}.json"))["works"]
out=[]
for w in W:
    t=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",w["title"] or "")).strip()
    if not t or not w["year"]: continue
    pg=w.get("page") or ""; m=re.match(r"(\d+)\D+(\d+)",pg); span=(int(m.group(2))-int(m.group(1))+1) if m else None
    rev=bool(re.search(r"\bby\b|review|book note|books received|\(eds?\.|isbn|pp\.|editorial|introduction to the|contributors|index|errat|corrigend|in memoriam|obituary",t,re.I))
    names=[k for k in PAT if (PATI[k].search(t) if k in PATI else PAT[k].search(t))]
    out.append({"n":w["n"],"year":w["year"],"title":t,"span":span,"review":rev,"names":names,
                "article":(span is None or span>=8) and not rev and w["type"]=="journal-article"})
json.dump(out,open(f"codes-{NAME}.json","w"),ensure_ascii=False)
print(NAME,len(out),sum(o["article"] for o in out))
