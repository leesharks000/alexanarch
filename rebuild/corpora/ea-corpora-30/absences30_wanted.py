#!/usr/bin/env python3
"""EA-CORPORA-30 (session tool): exact-wanted (30/12), a declared absence in the form of absences29_wanted.py — the works of
the exact sciences the thirtieth seating could not hold: the papers still in their United States term (Gödel 1931,
the Königsberg discussion, Turing, EPR, the Tetrabiblos editions) and the public-domain witnesses no copy could be
fetched for this session.
    python3 absences30_wanted.py <stage>      (the stage is data/corpora)"""
import json, hashlib, pathlib, sys
ST = pathlib.Path(sys.argv[1])
REN = " if its copyright was renewed (a United States work published before 1964 needed renewal; the renewal is to be checked)"
def us(y, renew=False):
    return f"{y + 96}-01-01" + (REN if renew else "")
def fo(y):
    return f"{y + 96}-01-01 in the United States (ninety-five years from first publication abroad)"
PD = "open now (public domain in the United States); wanted: no fetchable copy found this session"

W = [
 ("Public domain, no copy found", "Kurt Gödel", "Die Vollständigkeit der Axiome des logischen Funktionenkalküls, Monatshefte für Mathematik und Physik 37, 349–360", "Akademische Verlagsgesellschaft, Leipzig", 1930,
  PD + " (HathiTrust's Cornell volume, coo.31924000966790, full view, refused the seating's requests on 2026-10-30; the Internet Archive holds volume 36 only); in copyright in Europe until 2049-01-01"),
 ("Public domain, no copy found", "Kurt Gödel", "Einige metamathematische Resultate über Entscheidungsdefinitheit und Widerspruchsfreiheit, Anzeiger der Akademie der Wissenschaften in Wien, math.-naturw. Klasse 67, 214–215", "Akademie der Wissenschaften, Wien", 1930, PD),
 ("Public domain, no copy found", "Albert Einstein", "Eine neue Bestimmung der Moleküldimensionen, the Bern dissertation print", "Buchdruckerei K. J. Wyss, Bern", 1905, PD + "; the Annalen printing of 1906 is seated in 30/01"),
 ("Public domain, no copy found", "Albert Einstein", "Über die spezielle und die allgemeine Relativitätstheorie (Gemeinverständlich), the first printing", "Vieweg, Braunschweig", 1917, PD + "; the fifth printing of 1920 is seated in 30/01"),
 ("Public domain, no copy found", "Nicolaus Copernicus", "Commentariolus, Curtze's first printing, Mittheilungen des Coppernicus-Vereins für Wissenschaft und Kunst zu Thorn 1, 1–17", "Thorn", 1878,
  PD + " (the Archive item mittheilungende00curtgoog carries an OCR layer in which the text does not appear)"),
 ("Public domain, no copy found", "Archimedes, ed. J. L. Heiberg", "Ἔφοδος (the Method), first edited in Hermes 42", "Weidmann, Berlin", 1907, PD),
 ("Public domain, no copy found", "Archimedes, ed. J. L. Heiberg", "Ἔφοδος (the Method), in Archimedis opera omnia II, editio altera", "Teubner, Leipzig", 1913, PD),
 ("Public domain, no copy found", "Werner Heisenberg", "Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik, Zeitschrift für Physik 43, 172–198", "Springer, Berlin", 1927,
  PD + " (the Archive item zeitschrift-fur-physik-vol-43 is to be opened); in copyright in Europe until 2047-01-01"),
 ("Opening", "Kurt Gödel", "Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I, Monatshefte für Mathematik und Physik 38, 173–198", "Akademische Verlagsgesellschaft, Leipzig", 1931,
  fo(1931) + "; in Europe 2049-01-01, seventy years after the author's death"),
 ("Opening", "Kurt Gödel, Rudolf Carnap, Arend Heyting, John von Neumann and others", "Diskussion zur Grundlegung der Mathematik (the Königsberg discussion of 7 September 1930), Erkenntnis 2, 135–151", "Felix Meiner, Leipzig", 1931, fo(1931)),
 ("Opening", "Alan M. Turing", "On Computable Numbers, with an Application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42, 230–265", "London Mathematical Society", 1936,
  fo(1936) + "; open in the United Kingdom since 2025-01-01, seventy years after the author's death"),
 ("Opening", "Albert Einstein, Boris Podolsky, Nathan Rosen", "Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?, Physical Review 47, 777–780", "American Physical Society, New York", 1935, us(1935, True)),
 ("Opening", "Ptolemy, ed. and tr. F. E. Robbins", "Tetrabiblos (Ἀποτελεσματικά), Greek text with English translation, Loeb Classical Library 435", "Harvard University Press; Heinemann", 1940, us(1940, True)),
 ("Opening", "Ptolemy, ed. F. Boll and Ae. Boer", "Ἀποτελεσματικά, Claudii Ptolemaei opera quae exstant omnia III.1 (the First1KGreek file gives 1954; the date of the first Teubner printing is to be checked)", "Teubner, Leipzig", 1954,
  fo(1954) + " for the printing named; an earlier printing opens earlier"),
]
title = "The Exact Sciences, wanted — a declared absence: Gödel's incompleteness paper, the Königsberg discussion, Turing, EPR and the Tetrabiblos as they open, with the public-domain witnesses no copy could be found for"
why = ("The works of the exact sciences the thirtieth seating could not hold, declared beside the ones it holds (30/01–30/11), at the author's direction to seat "
       "'what is in the public domain, and what else' (2026-10-30). Six are still in their United States term and open on the dates given, the first of them Gödel's "
       "incompleteness paper on 2027-01-01; eight are open now and wanted because no copy could be fetched this session. Each entry names what would be seated, and the "
       "shelf grows as the works open or the copies are found.")
wanted = ("Wanted: the public-domain entries first, as scans of their first printings; then Gödel 1931 and the Königsberg discussion on 2027-01-01, which would join "
          "30/02 goedel; Turing in 2032; EPR in 2031 or now, as its renewal is found; the Tetrabiblos as its editions open.")
shelf = ("Beside einstein (30/01), goedel (30/02), tesla (30/03), copernicus (30/04), galileo (30/05), kepler (30/06), newton (30/07), arabic-mathematics (30/08), "
         "paul-klee (30/09), quantum-founders (30/10) and archimedes-ptolemy (30/11); Euclid is seated at 20/04.")
seat = ST / "exact-wanted"; (seat / "declared").mkdir(parents=True, exist_ok=True)
L = [dict(**{"class": c}, author=a, title=t, first_publisher=p, first_published=y, opens=o) for c, a, t, p, y, o in W]
doc = {"declared_absence": title, "kind": "copyright, and copies not found", "rights": "The authors, their estates and first publishers, as named.", "works": L,
       "wanted": wanted, "on_the_shelf": shelf, "note": "This seat holds no text of the works it names. The dates follow the terms stated; they are not legal advice."}
(seat / "declared/absence.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
md = [f"# {title}", "", why, "", "| Class | Author | Work | First publisher | Year | Opens |", "|---|---|---|---|---|---|"]
md += [f"| {w['class']} | {w['author']} | {w['title']} | {w['first_publisher'] or '—'} | {w['first_published'] or '—'} | {w['opens']} |" for w in L]
md += ["", wanted, "", shelf, "", doc["note"]]
(seat / "declared/absence.md").write_text("\n".join(md) + "\n", encoding="utf-8")
src = {"corpus": "exact-wanted", "seat": "EA-CORPORA-30/12", "title": title,
       "edition": "No edition held. The seat holds the declaration of what it would hold: declared/absence.json and declared/absence.md.",
       "language": "mul", "license": {"payload": "The declaration is the archive's own, CC-BY-4.0. The works it names are not held.", "record": "CC-BY-4.0 applies to this seat record only."},
       "fetched": "2026-10-30",
       "origin": {"items": [{"source": "Alexanarch deposit", "file": "declared/absence.json"}, {"source": "Alexanarch deposit", "file": "declared/absence.md"}],
                  "fetched": "2026-10-30", "transport": "written in session (Transport D); No-Double-Draw"},
       "works": {"count": 0, "units": f"no works held; {len(L)} declared", "list": []},
       "normalization": "None: the declaration is held as written.",
       "scope": "Declared without text: " + "; ".join(f"{w['author']}, {w['title']} ({w['first_publisher']}, {w['first_published']}), opens: {w['opens']}" for w in L) + ". " + wanted,
       "classes": sorted({w["class"] for w in L}, key=[x[0] for x in W].index),
       "declared_absences": L, "verified_loci": [], "loci_not_found": [], "lines_total": 0,
       "why_seated": why, "spine": "EA-CORPORA-30",
       "ruling": 'Lee Sharks, 2026-10-30: "and then an ea-corpora seating... Einstein, Gödel, Tesla, Copernicus, Galileo, classical Arabic mathematicians... what is in the public domain, and what else? and just to be perverse lets seat the promised Klee notebooks with them"; to the proposed set, "yes, thats a good set".',
       "seating": "EA-CORPORA-30, the thirtieth seating: the exact sciences and Klee's Bauhaus notebook, 2026-10-30"}
(seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
m = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')]
(seat / "MANIFEST.sha256").write_text("\n".join(m) + "\n")
print("exact-wanted", len(L), "declared")
