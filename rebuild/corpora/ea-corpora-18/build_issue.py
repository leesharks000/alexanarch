#!/usr/bin/env python3
"""Write the EA-CORPORA-18 deposit issue body (a DRAFT until minted) from the ten seat records.
Every edition line, locus and licence statement is read from data/corpora/<seat>/source.json, so the deposit
cannot say anything about a seat that its record does not.  -> data/issue-bodies/EA-CORPORA-18-issue.md"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
spec = json.loads((pathlib.Path(__file__).with_name("seats.json")).read_text(encoding="utf-8"))
C = "https://www.alexanarch.org/data/corpora"
seats = [json.loads((ROOT / "data/corpora" / s["corpus"] / "source.json").read_text(encoding="utf-8")) for s in spec["seats"]]
works = sum(s["works"]["count"] for s in seats); lines = sum(s["lines_total"] for s in seats)
files = sum(1 for s in spec["seats"] for p in (ROOT / "data/corpora" / s["corpus"]).rglob("*") if p.is_file())

title = ("EA-CORPORA-18 — The Eighteenth Seating: The Avant-Garde and Its Sources — Pound and the Cantos as First Printed, "
         "the Italian Lyric, Futurism, Dada, Jarry, Farce, Nonsense and Constraint, Visual Poetry, Stein, and Russian Formalism")
desc = (f"Ten seats on the originals shelf, {works} works and {lines:,} lines, for the modern avant-garde and the sources it read, "
        "in the editions a reader of their time could open, every one public domain in the United States. Pound's further volumes "
        "and the Cantos as first printed (Three Cantos, Poetry, 1917) with his Cavalcanti of 1912; the Italian lyric of the "
        "thirteenth and fourteenth centuries, the Sicilian school to the stilnovisti, with Rossetti's English; Italian and Russian "
        "Futurism and the English Vortex; Dada, the journal entire; Jarry, Ubu to Faustroll; French farce; the nonsense and "
        "constraint the Oulipo named as its plagiarists by anticipation; visual poetry from Optatianus to Mallarmé and Apollinaire, "
        "the line behind concrete poetry; Stein; and Russian Formalism, OPOJAZ's Poetika of 1919 and Shklovsky to 1930. Each seat "
        "holds the files as fetched, scans where the page is the text, one text per work, a provenance record with its verified "
        "loci, and a SHA-256 manifest; each has a card on the Training Layer Literature shelf. What is still in copyright — the "
        "Oulipo itself, the concrete poets proper, the Cantos after XXX — is named and not seated.")

out = ["### Protocol Version\n\nalexanarch-deposit-protocol/v1\n",
       f"### Title\n\n{title}\n", "### Creator\n\nSharks, Lee\n", "### ORCID\n\n0009-0000-1599-0703\n",
       "### Date\n\n2026-10-15\n", f"### Description\n\n{desc}\n", "### Content Type\n\nDataset\n", "### License\n\nCC-BY-4.0\n",
       "### Substrate Disclosure\n\nHuman–machine collaborative. Sources located, fetched, verified against their front matter, "
       "assembled into seats, hashed and indexed, and every locus found in the seated text, all in session by TACHYON (Claude, "
       "Anthropic) under MANUS (Lee Sharks) direction. The selection — which movements, which authors, Pound and the Cantos, the "
       "Italian lyric, Jarry and Shklovsky — is Lee Sharks's. CC-BY-4.0 applies to this record and the seat records; each payload "
       "carries its own licence, stated per seat.\n",
       "### Keywords\n\ncorpus seating, primary sources, public domain, avant-garde, modernism, Ezra Pound, The Cantos, Three Cantos, "
       "Guido Cavalcanti, dolce stil novo, Scuola siciliana, Giacomo da Lentini, Dante Gabriel Rossetti, Futurism, F. T. Marinetti, "
       "parole in libertà, zaum, Velimir Khlebnikov, Aleksei Kruchenykh, Vladimir Mayakovsky, Vorticism, Blast, Dada, Tristan Tzara, "
       "Francis Picabia, Hugo Ball, Alfred Jarry, Ubu Roi, pataphysics, farce, Alphonse Allais, nonsense, Lewis Carroll, Edward Lear, "
       "Christian Morgenstern, Raymond Roussel, Lautréamont, Oulipo, constraint, visual poetry, concrete poetry, Optatianus Porphyrius, "
       "Stéphane Mallarmé, Un coup de dés, Guillaume Apollinaire, Calligrammes, Gertrude Stein, Russian Formalism, OPOJAZ, Viktor "
       "Shklovsky, ostranenie, Yury Tynyanov, Boris Eikhenbaum, Training Layer Literature, originals shelf, EA-CORPORA\n",
       "### Related Identifiers\n\nAXN deposit #1673 — EA-CORPORA-17: the preceding seating\n"
       "AXN deposit #1580 — EA-CORPORA-12: the rule that seatings are periodically gathered\n"
       "Seat EA-CORPORA-05/01 (browning) and 05/02 (pound) — the constructed-voice series this seating extends\n",
       "### Version\n\nv1.0\n",
       "### Methodology\n\nSources located on Project Gutenberg (catalogue searched by author), the Internet Archive (advanced search, "
       "item metadata read for access restriction and files) and Wikisource (fr, ru; rendered pages, the single-page text where one "
       "exists). Each item's front matter read against the edition claimed for it and the edition statement corrected to what the "
       "file shows; publishers not shown in a file are not asserted. Gutenberg texts stripped at the START/END markers; Internet "
       "Archive scans seated with their OCR text layers, uncorrected, the scan as witness; Wikisource texts as rendered from the "
       "proofread transcription, their page lists kept. Every file hashed into the seat's MANIFEST.sha256. Every verified locus is a "
       "string found in the seated text by rebuild/corpora/ea-corpora-18/build_seats.py; a locus not found is recorded as not found. "
       "Licences stated per seat, with the EU term carried where it differs (payload/record split, EA-CORPORA-02/01). The builders, "
       "the seat specification and this body are under rebuild/corpora/ea-corpora-18/.\n",
       "### Falsification Conditions\n\nA seat is falsified if its files do not verify against its MANIFEST.sha256 at the canonical URL; "
       "if a seated file differs from the file at the origin its source.json names; if an edition statement misstates the front "
       "matter of the file it describes; if a verified locus cannot be found in the seated text; if an item stated public domain in "
       "the United States was published in or after 1931 by an author not in the public domain in the source country on 1 January "
       "1996; or if the four surfaces (seat, index, deposit, shelf) disagree.\n",
       "### Body\n\n# EA-CORPORA-18 — The Eighteenth Seating\n\n"
       "MANUS, 15 October 2026: \"we need more seatings of avant garde literature. dada. farce. oulipo. futurist. - whatevers in the "
       "public domain. originals is good on classics, impoverished on modern. and i want the italian troubadors. and pound, more pound. "
       "need the cantos.\" — \"and the concrete poets\" — \"also need jarry, schlovsky, etc\".\n"]
for S, s in zip(spec["seats"], seats):
    n = S["corpus"]
    out.append(f"## Seat {S['card']} — {S['spine']}\n\n*{s['title']}*\n")
    out.append("- Editions:\n" + "\n".join(f"  - {w['work']}" for w in s["works"]["list"]))
    out.append(f"- Licence: {s['license']['payload']}")
    for l in s["verified_loci"]:
        out.append(f"- Verified locus: {l}")
    out.append(f"- Scope: {s['scope']}")
    out.append(f"- Why seated: {s['why_seated']}")
    out.append(f"- Files: [the seat]({C}/{n}/) — [source.json]({C}/{n}/source.json), [MANIFEST.sha256]({C}/{n}/MANIFEST.sha256). "
               f"Shelf: [traininglayerliterature.org/originals/{n}](https://traininglayerliterature.org/originals/{n}/)\n")
out.append("## Not seated, and why\n\n- The Oulipo (founded 1960) and the Collège de 'Pataphysique: in copyright. The seat is its "
           "anticipatory line (18/05, 18/07).\n- The concrete poets proper (Gomringer, the Noigandres group, Finlay, Garnier): in "
           "copyright. The seat is the line behind them (18/08, with 18/03 and 18/07).\n- The Cantos after XXX: in copyright in the "
           "United States (Eleven New Cantos, 1934, until 2030). The 1925, 1928 and 1930 Drafts are public domain in the United States, "
           "but no public-domain witness was reachable in the session.\n- The Italians who wrote in Occitan (Sordello and others): no "
           "public-domain edition located; queued.\n- Everything marked QUEUED in a seat's scope.\n")
out.append("### Terms\n\n- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json\n"
           "- [x] I confirm this work is deposited under the stated license\n- [x] I confirm the substrate disclosure is accurate\n"
           "- [x] I understand that deposited content will NOT be used to train enforcement classifiers\n")
p = ROOT / "data/issue-bodies/EA-CORPORA-18-issue.md"
p.write_text("\n".join(out), encoding="utf-8")
print(p.relative_to(ROOT), len(p.read_text()), "chars;", works, "works,", lines, "lines,", files, "files")
