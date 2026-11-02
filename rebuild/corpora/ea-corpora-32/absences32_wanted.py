#!/usr/bin/env python3
"""EA-CORPORA-32 (session tool): legitimately-many-wanted (32/11), a declared absence in the form of absences31_wanted.py — the
editions and studies the remaining debts of Legitimately Many name and the thirty-second seating could not hold: the modern
editions and studies still in their United States term, and the public-domain witnesses no usable copy was found for.
    python3 absences32_wanted.py <stage>      (the stage is data/corpora)"""
import json, hashlib, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gen_spec32 import research
ST = pathlib.Path(sys.argv[1])
def fo(y):
    return f"{y + 96}-01-01 in the United States (ninety-five years from publication)"
PD = "open now (public domain in the United States); wanted: no usable copy found this session"

W = [
 ("Public domain, no copy found", "C. A. Brandis", "Aristotelis et Theophrasti Metaphysica ad veterum codicum manuscriptorum fidem recensita", "Reimer, Berlin", 1823,
  PD + "; Wimmer's preface (32/03) names it as the edition that collated four codices for Theophrastus's Metaphysics"),
 ("Public domain, no copy found", "H. Usener and the Bonn philological seminar", "Theophrasti de prima philosophia libellus", "Bonn", 1890, PD),
 ("Public domain, found, not seated", "Hegel, Michelet (ed.)", "Vorlesungen über die Geschichte der Philosophie II (Werke XIV, 1833), the rest of the lecture on Plato from p. 242 and the lectures after it, beyond the pages seated at 32/10", "Duncker und Humblot, Berlin", 1833,
  "open now (public domain); the scan is on the Archive (bub_gb_4ZpBzREnAIMC) and only pp. 169–241 were OCR'd this session"),
 ("Public domain in the United States, no open copy", "W. D. Ross and F. H. Fobes", "Theophrastus, Metaphysics, with translation, commentary and introduction", "Clarendon Press, Oxford", 1929,
  "open now in the United States (published 1929, public domain from 2025-01-01); the Archive holds only the 1967 Olms reprint (theophrastusmeta0000fhfo), lending-restricted; wanted"),
 ("Opening", "André Laks and Glenn W. Most", "Théophraste, Métaphysique", "Les Belles Lettres, Paris", 1993, fo(1993)),
 ("Opening", "Dimitri Gutas", "Theophrastus On First Principles (known as his Metaphysics)", "Brill, Leiden", 2010, fo(2010)),
 ("Opening", "Holger Thesleff", "The Pythagorean Texts of the Hellenistic Period", "Åbo Akademi, Åbo", 1965, fo(1965)),
 ("Opening", "Thomas Alexander Szlezák", "Pseudo-Archytas über die Kategorien", "de Gruyter, Berlin", 1972, fo(1972)),
 ("Opening", "Tiziano Dorandi", "Filodemo, Storia dei filosofi: Platone e l'Academia (PHerc. 1021 e 164)", "Bibliopolis, Naples", 1991, fo(1991)),
 ("Opening", "Gertjan Verhasselt", "the anonymous On Critical Signs in the Manuscripts of Plato (PSI XV 1488), edition and commentary", "", 2019, fo(2019)),
 ("Opening", "Francesca Schironi", "\"Plato at Alexandria: Aristophanes, Aristarchus, and the 'Philological Tradition' of a Philosopher\", Classical Quarterly 55", "Cambridge University Press", 2005, fo(2005)),
 ("Opening", "Marwan Rashed", "Ptolemy, Epistle to Gallus (the life, will and catalogue of Aristotle), edition", "", 2021, fo(2021)),
 ("Opening", "Matthias Perkams", "\"Die Datierung der Aristotelesedition des Andronikos von Rhodos\"", "", 2019, fo(2019)),
 ("Opening", "H. J. Drossaart Lulofs", "Nicolaus Damascenus on the Philosophy of Aristotle (Philosophia Antiqua 13), the fragments of the Syriac compendium (Cambridge University Library, Gg. 2.14) translated with introduction and commentary", "E. J. Brill, Leiden", 1965, fo(1965) + "; the Archive holds three copies for lending only (nicolausdamascen0000hjdr, trent_0116302122704, bwb_T3-BOE-620); to be read for the ground of Nicolaus's ascription of the Metaphysics (draft §3.13)"),
 ("Opening", "Josef Zürcher", "Aristoteles' Werk und Geist", "Schöningh, Paderborn", 1952, fo(1952)),
 ("Opening", "Anton-Hermann Chroust", "Aristotle: New Light on His Life and on Some of His Lost Works", "Routledge & Kegan Paul, London", 1973, fo(1973)),
 ("Opening", "Roger D. Masters; Christopher McKnight; Anton-Hermann Chroust", "the exchange on the authorship of the Aristotelian corpus: Masters, \"The Case of Aristotle's Missing Dialogues: Who Wrote the Sophist, the Statesman, and the Politics?\", Political Theory 5 (1977), p. 31; McKnight, \"On Masters, 'The Case of Aristotle's Missing Dialogues'\", 6 (1978), p. 247; Chroust, \"On Masters's 'The Case of Aristotle's Missing Dialogues'\", 7 (1979), p. 537; Masters, \"On Chroust: A Reply\", 7 (1979), p. 545", "", 1977, fo(1977) + " for the first; each piece opens ninety-five years from its own year"),
]
title = "Legitimately Many, wanted — a declared absence: the Theophrastus Metaphysics editions, Drossaart Lulofs's Nicolaus, Thesleff and Szlezák on pseudo-Archytas, Dorandi's Philodemus, PSI XV 1488, Rashed's Ptolemy, Zürcher, Chroust and the Masters exchange"
why = ("The editions and studies the remaining debts of the study Legitimately Many name and the thirty-second seating could not hold, declared beside the texts it holds "
       "(32/01–32/10, 32/12), at the author's direction of 2026-11-02. Thirteen are still in their United States term. Four are open now and wanted: Brandis and Usener, for which no copy was found; Ross and Fobes, "
       "public domain in the United States since 2025, with no open copy found; and the rest of Hegel's lectures, whose scan is referenced and was OCR'd only for pp. 169–241. The modern editions are where the twentieth century numbered and dated what the seated texts carry, so "
       "each entry names what the study cites from it.")
wanted = ("Wanted first: Brandis 1823 and Usener 1890, then Ross and Fobes 1929 from an open copy; the rest of Hegel's lectures can be OCR'd from the scan already referenced. "
          "The in-copyright studies are to be read and cited, not seated.")
shelf = ("Beside pseudo-archytas (32/01), aldine-aristotle-1497 (32/02), theophrastus-metaphysics-wimmer-1866 (32/03), philodemus-index-academicorum (32/04), "
         "dionysius-ad-ammaeum (32/05), cicero-ad-atticum (32/06), schleiermacher-platons-werke-1804 (32/07), campbell-sophistes-politicus (32/08), "
         "tennemann-platonische-philosophie (32/09), hegel (32/10) and nicolaus-damascenus (32/12); the debts of v0.1 are seated at EA-CORPORA-31.")
seat = ST / "legitimately-many-wanted"; (seat / "declared").mkdir(parents=True, exist_ok=True)
L = [dict(**{"class": c}, author=a, title=t, first_publisher=p, first_published=y, opens=o) for c, a, t, p, y, o in W]
doc = {"declared_absence": title, "kind": "copyright, and copies not found", "rights": "The authors, their estates and first publishers, as named.", "works": L,
       "wanted": wanted, "on_the_shelf": shelf, "note": "This seat holds no text of the works it names. The dates follow the terms stated; they are not legal advice."}
(seat / "declared/absence.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
md = [f"# {title}", "", why, "", "| Class | Author | Work | First publisher | Year | Opens |", "|---|---|---|---|---|---|"]
md += [f"| {w['class']} | {w['author']} | {w['title']} | {w['first_publisher'] or '—'} | {w['first_published'] or '—'} | {w['opens']} |" for w in L]
md += ["", wanted, "", shelf, "", doc["note"]]
(seat / "declared/absence.md").write_text("\n".join(md) + "\n", encoding="utf-8")
src = {"corpus": "legitimately-many-wanted", "seat": "EA-CORPORA-32/11", "title": title,
       "edition": "No edition held. The seat holds the declaration of what it would hold: declared/absence.json and declared/absence.md.",
       "language": "mul", "license": {"payload": "The declaration is the archive's own, CC-BY-4.0. The works it names are not held.", "record": "CC-BY-4.0 applies to this seat record only."},
       "fetched": "2026-11-02",
       "origin": {"items": [{"source": "Alexanarch deposit", "file": "declared/absence.json"}, {"source": "Alexanarch deposit", "file": "declared/absence.md"}],
                  "fetched": "2026-11-02", "transport": "written in session (Transport D); No-Double-Draw"},
       "works": {"count": 0, "units": f"no works held; {len(L)} declared", "list": []},
       "normalization": "None: the declaration is held as written.",
       "scope": "Declared without text: " + "; ".join(f"{w['author']}, {w['title']}" + (f" ({w['first_publisher'] + ', ' if w['first_publisher'] else ''}{w['first_published']})" if w['first_published'] else "") + f", opens: {w['opens']}" for w in L) + ". " + wanted,
       "classes": sorted({w["class"] for w in L}, key=[x[0] for x in W].index),
       "declared_absences": L, "verified_loci": [], "loci_not_found": [], "lines_total": 0,
       "why_seated": why, "research": research("design §5, 'Still owed' (the works in copyright, to be read and cited) and §7.2"), "spine": "EA-CORPORA-32",
       "ruling": 'Lee Sharks, 2026-11-02, of the texts still owed in §5 of the design Legitimately Many: "lets prepare that seating, its ea corpora deposit, and its tll spine and card".',
       "seating": "EA-CORPORA-32, the thirty-second seating: the remaining debts of Legitimately Many, 2026-11-02"}
(seat / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
m = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(seat).as_posix()}" for p in sorted(seat.rglob('*')) if p.is_file() and p.name not in ('MANIFEST.sha256', 'source.json')]
(seat / "MANIFEST.sha256").write_text("\n".join(m) + "\n")
print("legitimately-many-wanted", len(L), "declared")
