#!/usr/bin/env python3
"""EA-CORPORA-38, step 2: build the seats of the inference reception history.

    python3 -I build_seats38.py <stage-dir> <seats-dir>

<stage-dir> holds the originals as fetched and _text/ from prepare_texts38.py. <seats-dir> is where the seat
folders are written: a staging folder while the seating is assembled, data/corpora/ when the operator says seat.
38/01 (Kant, the Akademie-Ausgabe) is built by its own script when the OCR run is complete.
"""
import hashlib, json, pathlib, shutil, sys

ST = pathlib.Path(sys.argv[1])
TX = ST / "_text"
SEATS = pathlib.Path(sys.argv[2])
TODAY = "2026-11-14"
TRANSPORT = "in-session fetch (Transport D); No-Double-Draw"
RULING = ("Lee Sharks, 2026-11-14 01:25 EST: \"lets continue to assemble and we'll deposit and seat the whole thing as a "
          "massive batch\"; the standing rule for originals-library seatings, 2026-10-18: \"original language where available always\".")
RESEARCH = {
    "study": "Critique of Pure Inference (working draft v1.1) and The Production of Readers (#1767), §11.6 \"the witnesses between\"",
    "for": "the reception history of inference from the Peripatos to the machine: the commentators who name Aristotle's "
           "ἑταῖροι, the Latin handbooks, the early-modern refusals of the syllogism, the nineteenth-century rebuilds, and the "
           "traditions that reasoned about inference without the Organon",
}
SPINE = "EA-CORPORA-38 (assembled 2026-11-14, not seated, not deposited)"
CC_SA = "CC BY-SA 4.0 (the TEI packaging, as stated in the file's teiHeader)"
SEAT_REC = "CC-BY-4.0 applies to this seat record only."


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def seat(n, name, meta, originals, texts, loci):
    """originals: [(src, rel)]; texts: [(slug, rel)] taken from _text/<slug>.txt; loci: [(label, text-rel, needle)]."""
    d = SEATS / name
    if d.exists():
        shutil.rmtree(d)
    (d / "original").mkdir(parents=True)
    (d / "text").mkdir()
    rows = []
    for src, rel in originals:
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, d / rel)
        rows.append(rel)
    for slug, rel in texts:
        shutil.copyfile(TX / f"{slug}.txt", d / rel)
        rows.append(rel)
    (d / "MANIFEST.sha256").write_text("".join(f"{sha(d / r)}  {r}\n" for r in sorted(rows)))
    found, missing = [], []
    for label, rel, needle in loci:
        t = (d / rel).read_text(encoding="utf-8")
        (found if needle in t else missing).append(f"{label} — '{needle}' ({rel})")
    for w in meta["works"]["list"]:
        w["lines"] = (d / w["text"]).read_text(encoding="utf-8").count("\n")
    meta = {"corpus": name, "seat": f"EA-CORPORA-38/{n:02d}", **meta, "fetched": TODAY,
            "verified_loci": found, "loci_not_found": missing,
            "lines_total": sum((d / r).read_text(encoding="utf-8").count("\n") for _, r in texts),
            "ruling": RULING, "research": RESEARCH, "spine": SPINE, "axn": None,
            "axn_note": "assigned at deposit, derived from MANIFEST.sha256 as for every seat"}
    (d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    print(f"{meta['seat']} {name:40} lines {meta['lines_total']:>7}  loci {len(found)}  missing {len(missing)}")
    if missing:
        print("   MISSING", missing)


def gh(repo, path):
    return {"source": "GitHub", "repo": repo, "path": path, "branch": "master",
            "url": f"https://github.com/{repo}/blob/master/{path}"}


def ia(ident, files, **kw):
    return {"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}", "files": files, **kw}


TEI_NORM = ("The TEI as fetched under original/. text/ is the <text> reduced by code (prepare_texts38.py): teiHeader, "
            "note, app and bibl dropped; one line per <p>, <l> or <head>; each numbered <div> marked [<subtype> <n>]; the "
            "edition's page breaks stand as [p. N] and its numbered lines as |L. No text was corrected by hand.")
DJVU_NORM = ("The Internet Archive's own text layer (_djvu.txt) as served, under original/<identifier>/, copied to "
             "text/<slug>.ocr.txt with line endings normalized. The scan is held by reference at its Archive URL and not "
             "copied. No text was corrected by hand; the loci keep the OCR's readings.")
PG_NORM = ("The Project Gutenberg file as served, under original/. text/ is the same file with the Gutenberg header and "
           "licence cut at their markers. No text was corrected by hand.")

# 38/02 Alexander, In APr I
F = "tlg0732.tlg005.1st1K-grc1.xml"
seat(2, "alexander-in-apr-wallies-1883", {
    "title": "Alexander of Aphrodisias, In Aristotelis Analyticorum priorum librum I commentarium, ed. M. Wallies (CAG II.1; Berlin: Reimer, 1883)",
    "edition": "Wallies 1883, the First1KGreek TEI (from the Internet Archive scan), with Wallies's pages and line numbers",
    "language": "grc",
    "license": {"payload": f"Alexander (fl. c. 200 CE) and Wallies 1883 are public domain. {CC_SA}; the archive asserts no further licence.", "record": SEAT_REC},
    "origin": {"items": [gh("OpenGreekAndLatin/First1KGreek", f"data/tlg0732/tlg005/{F}")], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "in-apr-i", "work": "In Analytica priora I", "text": "text/in-apr-i.txt", "originals": [f"original/{F}"]}]},
    "normalization": TEI_NORM + " The file's line numbers also carry the manuscript's folio marks (|40r) and some numbers out of sequence; a locus is cited by its [p. N] and the Wallies line numbers that bracket it.",
    "scope": "Book I whole: the commentary that names the ἑταῖροι of Aristotle, Theophrastus and Eudemus, against him on the modal mixtures.",
    "why_seated": "The first surviving witness who reads the Prior Analytics with its school beside it: the ἑταῖροι dissent at 124.5–10 (cited as 124.8).",
}, [(ST / "alexander-in-apr" / F, f"original/{F}")], [("alexander-in-apr-i", "text/in-apr-i.txt")], [
    ("124.5–10, the companions dissent on the mixture of necessary and assertoric", "text/in-apr-i.txt", "οἱ δέ γε ἑταῖροι αὐτοῦ οἱ περὶ Εὔδημόν τε καὶ Θεόφραστον οὐχ οὕτως λέγουσι"),
    ("Wallies's page 124", "text/in-apr-i.txt", "[p. 124]"),
])

# 38/03 Philoponus, In APr
F = "tlg4015.tlg002.1st1K-grc1.xml"
seat(3, "philoponus-in-apr-wallies-1905", {
    "title": "John Philoponus, In Aristotelis Analytica priora commentaria, ed. M. Wallies (CAG XIII.2; Berlin: Reimer, 1905)",
    "edition": "Wallies 1905, the First1KGreek TEI (from the Internet Archive scan), with Wallies's pages and line numbers",
    "language": "grc",
    "license": {"payload": f"Philoponus (d. c. 570) and Wallies 1905 are public domain. {CC_SA}; the archive asserts no further licence.", "record": SEAT_REC},
    "origin": {"items": [gh("OpenGreekAndLatin/First1KGreek", f"data/tlg4015/tlg002/{F}")], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "in-apr", "work": "In Analytica priora", "text": "text/in-apr.txt", "originals": [f"original/{F}"]}]},
    "normalization": TEI_NORM,
    "scope": "The commentary whole.",
    "why_seated": "The witness who names the school as ὁ φιλόσοφος against οἱ ἑταῖροι αὐτοῦ οἱ περὶ Θεόφραστον καὶ Εὔδημον (123–124).",
}, [(ST / "philoponus-in-apr" / F, f"original/{F}")], [("philoponus-in-apr", "text/in-apr.txt")], [
    ("123.15, the companions about Theophrastus and Eudemus", "text/in-apr.txt", "οἱ δὲ ἑταῖροι αὐτοῦ οἱ περὶ Θεόφραστον καὶ Εὔδημο"),
    ("124, the companions object", "text/in-apr.txt", "Οἱ δὲ ἑταῖροι αὐτοῦ ἐνίστανται πρὸς τὰ εἰρημένα"),
])

# 38/04 Theophrastus, Characters
F = "tlg0093.tlg009.perseus-grc2.xml"
seat(4, "theophrastus-characteres-diels-1909", {
    "title": "Theophrastus, Characteres, ed. H. Diels (Oxford: Clarendon Press, 1909)",
    "edition": "Diels 1909, the Perseus TEI",
    "language": "grc",
    "license": {"payload": f"Theophrastus and Diels 1909 are public domain. {CC_SA}; the archive asserts no further licence.", "record": SEAT_REC},
    "origin": {"items": [gh("PerseusDL/canonical-greekLit", f"data/tlg0093/tlg009/{F}")], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "characteres", "work": "Characteres, with the proem", "text": "text/characteres.txt", "originals": [f"original/{F}"]}]},
    "normalization": TEI_NORM,
    "scope": "The thirty characters and the proem, as Diels prints them.",
    "why_seated": "The draft position (#1767): the work that moves from the Peripatetic definition toward the drawn person. It extends Theophrastus's seat (EA-CORPORA-09/01), which did not carry it.",
}, [(ST / "char/t-perseus-grc2.xml", f"original/{F}")], [("characteres", "text/characteres.txt")], [
    ("1.1, irony defined", "text/characteres.txt", "ἡ μὲν οὖν εἰρωνεία δόξειεν ἂν εἶναι, ὡς τύπῳ λαβεῖν, προσποίησις ἐπὶ χεῖρον"),
    ("the proem, to Polycles", "text/characteres.txt", "ἐγὼ γάρ, ὦ Πολύκλεις"),
])

# 38/05 Epictetus
F = "tlg0557.tlg001.perseus-grc2.xml"
seat(5, "epictetus-dissertationes-schenkl-1916", {
    "title": "Epictetus, Dissertationes ab Arriano digestae, ed. H. Schenkl, editio maior (Leipzig: Teubner, 1916)",
    "edition": "Schenkl 1916, the Perseus TEI",
    "language": "grc",
    "license": {"payload": f"Epictetus, Arrian and Schenkl 1916 are public domain. {CC_SA}; the archive asserts no further licence.", "record": SEAT_REC},
    "origin": {"items": [gh("PerseusDL/canonical-greekLit", f"data/tlg0557/tlg001/{F}")], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "dissertationes", "work": "Dissertationes I–IV, with Arrian's letter to Gellius", "text": "text/dissertationes.txt", "originals": [f"original/{F}"]}]},
    "normalization": TEI_NORM,
    "scope": "The four books whole.",
    "why_seated": "The Stoic line of inference as the Peripatos did not hold it: the Master Argument of Diodorus at 2.19.",
}, [(ST / "epictetus" / F, f"original/{F}")], [("dissertationes", "text/dissertationes.txt")], [
    ("2.19.1, the Master Argument", "text/dissertationes.txt", "ὁ κυριεύων λόγος ἀπὸ τοιούτων τινῶν ἀφορμῶν ἠρωτῆσθαι φαίνεται"),
    ("Arrian to Lucius Gellius", "text/dissertationes.txt", "Ἀρριανὸς Λουκίῳ Γελλίῳ χαίρειν"),
])

# 38/06 Cicero, Topica
F = "phi0474.phi042.perseus-lat2.xml"
seat(6, "cicero-topica-wilkins-1902", {
    "title": "M. Tullius Cicero, Topica, in Rhetorica II, ed. A. S. Wilkins (Oxford Classical Texts; Oxford: Clarendon Press, 1902)",
    "edition": "Wilkins 1902, the Perseus TEI",
    "language": "lat",
    "license": {"payload": f"Cicero and Wilkins 1902 are public domain. {CC_SA}; the archive asserts no further licence.", "record": SEAT_REC},
    "origin": {"items": [gh("PerseusDL/canonical-latinLit", f"data/phi0474/phi042/{F}")], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "topica", "work": "Topica, with Wilkins's sigla", "text": "text/topica.txt", "originals": [f"original/{F}"]}]},
    "normalization": TEI_NORM,
    "scope": "The Topica whole.",
    "why_seated": "The Latin door to the topics: Cicero's division of disserendi ratio into inveniendi and iudicandi, which Boethius commented and the handbooks carried. It extends Cicero's seat, which did not carry it.",
}, [(ST / "cicero-topica" / F, f"original/{F}")], [("topica", "text/topica.txt")], [
    ("§6, the two parts of reasoning", "text/topica.txt", "Cum omnis ratio diligens disserendi duas habeat partis, unam inveniendi alteram iudicandi"),
])

# 38/07 Bacon
seat(7, "bacon-novum-organum-1620", {
    "title": "Francis Bacon, Novum Organum (London, 1620), Books I and II",
    "edition": "The Latin text as published by the Latin Library (thelatinlibrary.com/bacon), which does not name its copy-text",
    "language": "lat",
    "license": {"payload": "Bacon (d. 1626) is public domain; the Latin Library serves the transcription openly. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [{"source": "The Latin Library", "url": "https://www.thelatinlibrary.com/bacon/bacon.liber1.shtml", "file": "liber1.shtml"},
                         {"source": "The Latin Library", "url": "https://www.thelatinlibrary.com/bacon/bacon.liber2.shtml", "file": "liber2.shtml"}], "transport": TRANSPORT},
    "works": {"count": 2, "units": "one text file per book", "list": [
        {"slug": "novum-organum-i", "work": "Novum Organum, Liber primus (Aphorisms I–CXXX)", "text": "text/novum-organum-i.txt", "originals": ["original/thelatinlibrary/liber1.shtml"]},
        {"slug": "novum-organum-ii", "work": "Novum Organum, Liber secundus", "text": "text/novum-organum-ii.txt", "originals": ["original/thelatinlibrary/liber2.shtml"]}]},
    "normalization": "The pages as served (Latin-1), under original/thelatinlibrary/. text/ is the page with its markup removed by code, entities decoded, one line per paragraph. No text was corrected by hand.",
    "scope": "Both books.",
    "why_seated": "The refusal of the syllogism as an instrument of discovery (I.13–14) and the induction set in its place.",
}, [(ST / "bacon/liber1.shtml", "original/thelatinlibrary/liber1.shtml"), (ST / "bacon/liber2.shtml", "original/thelatinlibrary/liber2.shtml")],
    [("novum-organum-i", "text/novum-organum-i.txt"), ("novum-organum-ii", "text/novum-organum-ii.txt")], [
    ("I.14, the syllogism consists of propositions", "text/novum-organum-i.txt", "Syllogismus ex propositionibus constat"),
    ("I.130, the art of interpreting nature", "text/novum-organum-i.txt", "artem ipsam Interpretandi Naturam proponamus"),
])

# 38/08 Hume
seat(8, "hume-treatise-enquiry", {
    "title": "David Hume, A Treatise of Human Nature (London, 1739–1740) and An Enquiry concerning Human Understanding (1748)",
    "edition": "The Project Gutenberg texts (#4705 and #9662), which do not name their copy-texts",
    "language": "eng",
    "license": {"payload": "Hume (d. 1776) is public domain; the Gutenberg files are served under the Project Gutenberg licence, which is cut from text/ and kept in original/. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [{"source": "Project Gutenberg", "ebook": 4705, "url": "https://www.gutenberg.org/ebooks/4705", "file": "pg4705.txt"},
                         {"source": "Project Gutenberg", "ebook": 9662, "url": "https://www.gutenberg.org/ebooks/9662", "file": "pg9662.txt"}], "transport": TRANSPORT},
    "works": {"count": 2, "units": "one text file per work", "list": [
        {"slug": "treatise", "work": "A Treatise of Human Nature, Books I–III", "text": "text/treatise.txt", "originals": ["original/gutenberg/pg4705.txt"]},
        {"slug": "enquiry", "work": "An Enquiry concerning Human Understanding", "text": "text/enquiry.txt", "originals": ["original/gutenberg/pg9662.txt"]}]},
    "normalization": PG_NORM,
    "scope": "Both works whole.",
    "why_seated": "The inference from cause to effect taken apart: Treatise I.iii (Of knowledge and probability) and Enquiry IV–VII.",
}, [(ST / "hume/pg4705.txt", "original/gutenberg/pg4705.txt"), (ST / "hume/pg9662.txt", "original/gutenberg/pg9662.txt")],
    [("treatise", "text/treatise.txt"), ("enquiry", "text/enquiry.txt")], [
    ("Treatise I.iii.14", "text/treatise.txt", "THE IDEA OF NECESSARY CONNEXION"),
    ("Treatise I.iii", "text/treatise.txt", "OF KNOWLEDGE AND PROBABILITY"),
    ("Enquiry IV.i", "text/enquiry.txt", "All reasonings concerning matter of fact"),
])

# 38/09 Carroll
seat(9, "carroll-symbolic-logic-1897", {
    "title": "Lewis Carroll, Symbolic Logic, Part I: Elementary, fourth edition (London: Macmillan, 1897)",
    "edition": "The Project Gutenberg text (#28696), from the fourth edition",
    "language": "eng",
    "license": {"payload": "C. L. Dodgson (d. 1898) is public domain; the Gutenberg licence is cut from text/ and kept in original/. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [{"source": "Project Gutenberg", "ebook": 28696, "url": "https://www.gutenberg.org/ebooks/28696", "file": "pg28696.txt"}], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "symbolic-logic", "work": "Symbolic Logic, Part I", "text": "text/symbolic-logic.txt", "originals": ["original/gutenberg/pg28696.txt"]}]},
    "normalization": PG_NORM,
    "scope": "Part I whole, with the sorites problems.",
    "why_seated": "The syllogism made a game for the machine of the diagram: the sorites as a puzzle to be solved by a method.",
}, [(ST / "carroll/pg28696.txt", "original/gutenberg/pg28696.txt")], [("symbolic-logic", "text/symbolic-logic.txt")], [
    ("the preface to the fourth edition", "text/symbolic-logic.txt", "PREFACE TO THE FOURTH EDITION"),
    ("the sorites", "text/symbolic-logic.txt", "Soriteses"),
])

# 38/10 Hegel
seat(10, "hegel-wissenschaft-der-logik", {
    "title": "G. W. F. Hegel, Wissenschaft der Logik (Nürnberg, 1812–1816; Book I revised 1831)",
    "edition": "The Project Gutenberg texts (#6729, #6834; Latin-1 files 8wsl110, 8wsl210), which do not name their copy-text; Band 1 carries the 1831 preface to the second edition, so the copy-text is a printing of the Werke (1833–34 or later)",
    "language": "deu",
    "license": {"payload": "Hegel (d. 1831) is public domain; the Gutenberg licence is cut from text/ and kept in original/. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [{"source": "Project Gutenberg via the Internet Archive", "identifier": "wissenschaftderl06729gut", "url": "https://archive.org/details/wissenschaftderl06729gut", "file": "8wsl110.txt"},
                         {"source": "Project Gutenberg via the Internet Archive", "identifier": "wissenschaftderl06834gut", "url": "https://archive.org/details/wissenschaftderl06834gut", "file": "8wsl210.txt"}], "transport": TRANSPORT},
    "works": {"count": 2, "units": "one text file per Band", "list": [
        {"slug": "wissenschaft-der-logik-1", "work": "Band 1: Die objektive Logik", "text": "text/wissenschaft-der-logik-1.txt", "originals": ["original/gutenberg/8wsl110.txt"]},
        {"slug": "wissenschaft-der-logik-2", "work": "Band 2: Die subjektive Logik, with the chapter Der Schluß", "text": "text/wissenschaft-der-logik-2.txt", "originals": ["original/gutenberg/8wsl210.txt"]}]},
    "normalization": PG_NORM + " The files are Latin-1 and are decoded to UTF-8 in text/.",
    "scope": "Both Bände whole.",
    "why_seated": "The syllogism taken into the concept: Der Schluß des Daseyns, der Reflexion, der Nothwendigkeit. It extends Hegel's seat, which held the Differenz and the Plato lectures only.",
}, [(ST / "hegel/8wsl110.txt", "original/gutenberg/8wsl110.txt"), (ST / "hegel/8wsl210.txt", "original/gutenberg/8wsl210.txt")],
    [("wissenschaft-der-logik-1", "text/wissenschaft-der-logik-1.txt"), ("wissenschaft-der-logik-2", "text/wissenschaft-der-logik-2.txt")], [
    ("the syllogism chapter", "text/wissenschaft-der-logik-2.txt", "A. Der Schluß des Daseyns."),
    ("the syllogism as the posited concept", "text/wissenschaft-der-logik-2.txt", "Der Schluß ist somit der vollständig gesetzte Begriff"),
    ("Der Schluß der Nothwendigkeit", "text/wissenschaft-der-logik-2.txt", "C. Der Schluß der Nothwendigkeit."),
])

# 38/11 Frege
I = "rcin.org.pl.WA35_20448_6464_Begriffsschrift_50430"
seat(11, "frege-begriffsschrift-1879", {
    "title": "Gottlob Frege, Begriffsschrift, eine der arithmetischen nachgebildete Formelsprache des reinen Denkens (Halle: Nebert, 1879)",
    "edition": "The first edition, the RCIN (Repozytorium Cyfrowe Instytutów Naukowych) copy on the Internet Archive; the Archive's text layer",
    "language": "deu",
    "license": {"payload": "Frege (d. 1925) is public domain; the Archive marks the item Public Domain. The text layer does not render the two-dimensional notation; the formulae are held in the scan, by reference. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [ia(I, ["WA35_20448_6464_Begriffsschrift_djvu.txt", "WA35_20448_6464_Begriffsschrift.pdf (by reference, 9,933,784 bytes)"])], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "begriffsschrift", "work": "Begriffsschrift (1879)", "text": "text/begriffsschrift.ocr.txt", "originals": [f"original/{I}/WA35_20448_6464_Begriffsschrift_djvu.txt"]}]},
    "normalization": DJVU_NORM,
    "scope": "The book whole, the prose; the notation in the scan.",
    "why_seated": "Inference rebuilt from the judgment-stroke out, with one rule of inference; the end of the syllogism as the form of inference.",
}, [(ST / "frege/rcin_djvu.txt", f"original/{I}/WA35_20448_6464_Begriffsschrift_djvu.txt")], [("begriffsschrift.ocr", "text/begriffsschrift.ocr.txt")], [
    ("the subtitle", "text/begriffsschrift.ocr.txt", "Formelsprache des reinen Denkens"),
    ("the preface, on the Bündigkeit of proof", "text/begriffsschrift.ocr.txt", "meiner Begriffsschrift, wo ein besonderer Werth auf die Bündig"),
])

# 38/12 Peirce
seat(12, "peirce-logic-papers-1867-1878", {
    "title": "Charles S. Peirce, the logic papers of 1867 (Proceedings of the American Academy of Arts and Sciences VII) and the six Illustrations of the Logic of Science (Popular Science Monthly XII–XIII, 1877–1878)",
    "edition": "The three volumes as printed; the Internet Archive's text layers, held whole, with Peirce's papers located by line",
    "language": "eng",
    "license": {"payload": "Peirce (d. 1914) and the volumes (1868, 1877–1878) are public domain. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [ia("proceedingsofame07amer", ["proceedingsofame07amer_djvu.txt"]),
                         ia("popularsciencemo12newy", ["popularsciencemo12newy_djvu.txt"]),
                         ia("popularsciencemo13newy", ["popularsciencemo13newy_djvu.txt"])], "transport": TRANSPORT},
    "works": {"count": 3, "units": "one text file per volume, held whole", "list": [
        {"slug": "paaas-vii", "work": "PAAAS VII (1865–1868): On the Natural Classification of Arguments (9 April 1867, from line 16221); On a New List of Categories (14 May 1867, from 17706); Upon the Logic of Mathematics (10 September 1867, from 23144); Upon Logical Comprehension and Extension (from 23887)", "text": "text/paaas-vii.ocr.txt", "originals": ["original/proceedingsofame07amer/proceedingsofame07amer_djvu.txt"]},
        {"slug": "psm-xii", "work": "PSM XII (1877–1878): I The Fixation of Belief (from line 57); II How to Make Our Ideas Clear (18555); III The Doctrine of Chances (39525); IV The Probability of Induction (46109)", "text": "text/psm-xii.ocr.txt", "originals": ["original/popularsciencemo12newy/popularsciencemo12newy_djvu.txt"]},
        {"slug": "psm-xiii", "work": "PSM XIII (1878): V The Order of Nature (from line 12618); VI Deduction, Induction, and Hypothesis (30343)", "text": "text/psm-xiii.ocr.txt", "originals": ["original/popularsciencemo13newy/popularsciencemo13newy_djvu.txt"]}]},
    "normalization": DJVU_NORM + " The volumes are held whole because the text layers drop the running heads and the papers' ends cannot be cut by code without guessing; each paper is located by the line of its heading.",
    "scope": "The ten papers in which Peirce reclassifies inference as deduction, induction and hypothesis.",
    "why_seated": "The third kind of inference named: the beans of the sixth paper (Rule, Case, Result) against the syllogism's one order.",
}, [(ST / "peirce/paas7_djvu.txt", "original/proceedingsofame07amer/proceedingsofame07amer_djvu.txt"),
    (ST / "peirce/psm12_djvu.txt", "original/popularsciencemo12newy/popularsciencemo12newy_djvu.txt"),
    (ST / "peirce/psm13_djvu.txt", "original/popularsciencemo13newy/popularsciencemo13newy_djvu.txt")],
    [("paaas-vii.ocr", "text/paaas-vii.ocr.txt"), ("psm-xii.ocr", "text/psm-xii.ocr.txt"), ("psm-xiii.ocr", "text/psm-xiii.ocr.txt")], [
    ("1867, the heading", "text/paaas-vii.ocr.txt", "On  the  Natural  Classification  of  Arguments.    By  C.  S.  Peirce."),
    ("1877, the first paper", "text/psm-xii.ocr.txt", "FIRST  PAPER.— THE  FIXATION  OF  BELIEF."),
    ("1878, the sixth paper", "text/psm-xiii.ocr.txt", "SIXTH    PAPER.  — DEDUCTION,    INDUCTION,    AND    HYPOTHESIS."),
    ("the beans", "text/psm-xiii.ocr.txt", "Rule. — All  the  beans  from  this  bag  are  white."),
])

# 38/13 Boethius
I = "patrologiaecursu0064mign"
seat(13, "boethius-logica-migne-pl64", {
    "title": "Boethius, the logical works, in Patrologiae cursus completus, series Latina 64, ed. J.-P. Migne (Paris, 1847)",
    "edition": "Migne PL 64 (Boethius II): the commentaries on Porphyry, the Categories, De interpretatione and Cicero's Topica; the Introductio ad syllogismos categoricos, De syllogismo categorico, De syllogismo hypothetico, De divisione, De differentiis topicis; the Archive's text layer",
    "language": "lat",
    "license": {"payload": "Boethius (d. c. 524) and Migne 1847 are public domain. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [ia(I, [f"{I}_djvu.txt"])], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per volume", "list": [{"slug": "pl64", "work": "PL 64, the volume whole", "text": "text/pl64.ocr.txt", "originals": [f"original/{I}/{I}_djvu.txt"]}]},
    "normalization": DJVU_NORM,
    "scope": "The volume whole: the Latin Organon as the Middle Ages received it.",
    "why_seated": "The Latin gap of §11.6: the handbooks through which the syllogism reached the schools.",
}, [(ST / "boethius/pl64_djvu.txt", f"original/{I}/{I}_djvu.txt")], [("pl64.ocr", "text/pl64.ocr.txt")], [
    ("Introductio ad syllogismos categoricos", "text/pl64.ocr.txt", "INTRODUCTIO AD SYLLOGISMOS CATEGORICOS"),
    ("De syllogismo categorico", "text/pl64.ocr.txt", "DE SYLLOGISMO CATEGORICO"),
    ("De syllogismo hypothetico", "text/pl64.ocr.txt", "DE SYLLOGISMO HYPOTHETICO"),
    ("De differentiis topicis", "text/pl64.ocr.txt", "DE DIFFERENTIIS TOPICIS"),
])

# 38/14 Nyāya
I = "nyayasutrabhashyaofvatsaynaextractsfromnyayavartikatatparyatikaramasastritailanganavss111896_20_427_a"
FN = "Nyaya Sutra Bhashya of Vatsayna Extracts from Nyaya Vartika & Tatparya Tika Rama Sastri Tailangana VSS 11 1896_djvu.txt"
seat(14, "nyaya-sutra-vatsyayana-1896", {
    "title": "Gautama, Nyāyasūtra, with the Bhāṣya of Vātsyāyana and extracts from the Nyāyavārttika and the Tātparyaṭīkā, ed. Gangadhara Sastri Tailanga (Vizianagram Sanskrit Series 9/11; Benares, 1896)",
    "edition": "The Vizianagram edition, the Internet Archive's text layer (Devanagari OCR)",
    "language": "san",
    "license": {"payload": "The sūtras and the Bhāṣya are ancient; the 1896 edition is public domain. The Archive marks the item CC0. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [ia(I, [FN])], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "nyaya-sutra-bhashya", "work": "Nyāyasūtra with Vātsyāyana's Bhāṣya", "text": "text/nyaya-sutra-bhashya.ocr.txt", "originals": [f"original/{I}/vss11_djvu.txt"]}]},
    "normalization": DJVU_NORM + " The OCR misreads conjuncts often (1.1.1 is read प्रमाणप्रमेयसंशयग्रयोजन for …प्रयोजन); the loci keep its readings.",
    "scope": "The five adhyāyas with the Bhāṣya.",
    "why_seated": "Inference (anumāna) reasoned about without the Organon: the five-membered argument (pañcāvayava) and the sixteen categories.",
}, [(ST / "nyaya/vss11_djvu.txt", f"original/{I}/vss11_djvu.txt")], [("nyaya-sutra-bhashya.ocr", "text/nyaya-sutra-bhashya.ocr.txt")], [
    ("1.1.1, the sixteen categories, as OCR'd", "text/nyaya-sutra-bhashya.ocr.txt", "प्रमाणप्रमेयसंशयग्रयोजनद्रष्टान्तसिद्वान्तौवयवतक"),
])

# 38/16 Buridan
I = "4OEXVSUP2_P3a"
seat(16, "buridan-sophismata-c1489", {
    "title": "John Buridan, Sophismata ([Paris, c. 1489])",
    "edition": "The incunable as scanned (Internet Archive 4OEXVSUP2_P3a, Public Domain Mark); its text layer is held as served and does not read the black letter or its abbreviations",
    "language": "lat",
    "license": {"payload": "Buridan (d. c. 1361) and the c. 1489 print are public domain; the Archive marks the item Public Domain Mark 1.0. The archive asserts no licence over the payload.", "record": SEAT_REC},
    "origin": {"items": [ia(I, ["4OEXVSUP2_P3_djvu.txt", "4OEXVSUP2_P3.pdf (by reference, 20,540,388 bytes)"])], "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "sophismata", "work": "Sophismata (c. 1489)", "text": "text/sophismata.ocr.txt", "originals": [f"original/{I}/4OEXVSUP2_P3_djvu.txt"]}]},
    "normalization": DJVU_NORM + " The layer is unreadable for the most part (black letter, abbreviations); the scan is the witness and the text layer is held so the seat says what the commons carries.",
    "scope": "The print whole.",
    "why_seated": "The only commons witness found to Buridan's logic. No commons scan of the Tractatus de consequentiis was found (searched 2026-11-14: the Internet Archive, e-rara, the MDZ; Gallica refused the session); its modern edition (Hubien 1976) is not in the commons. It is declared absent at EA-CORPORA-38.",
}, [(ST / "buridan/soph_djvu.txt", f"original/{I}/4OEXVSUP2_P3_djvu.txt")], [("sophismata.ocr", "text/sophismata.ocr.txt")], [])

# 38/15 Ibn Sīnā, al-Ishārāt wa-l-tanbīhāt, Part I (logic)
I = "kitbalishrtwaalt00avic"
OCRD = pathlib.Path("/tmp/claude-0/ara-ocr/ocr") / I
if (TX / "isharat-i.ocr.txt").exists():
    seat(15, "ibn-sina-isharat-forget-1892", {
        "title": "Ibn Sīnā, Kitāb al-ishārāt wa-l-tanbīhāt, al-juzʾ al-awwal (the logic), ed. J. Forget, Le livre des théorèmes et des avertissements (Leiden: Brill, 1892)",
        "edition": "Forget 1892, Part I; OCR made for this seat (tesseract 5, tessdata_best ara, one page at a time) from the Archive's page images, because the Archive's own layer is mostly noise in the Arabic",
        "language": "ara",
        "license": {"payload": "Ibn Sīnā (d. 1037) and Forget 1892 are public domain. The OCR is the archive's, made by code and not corrected. The archive asserts no licence over the payload.", "record": SEAT_REC},
        "origin": {"items": [ia(I, [f"{I}_djvu.txt", f"page/n0–n231.jpg (fetched one at a time, OCR'd, deleted)", f"{I}.pdf (by reference, 14,256,855 bytes)"])], "transport": TRANSPORT},
        "works": {"count": 1, "units": "one text file per work", "list": [{"slug": "isharat-i", "work": "al-Ishārāt wa-l-tanbīhāt, Part I: al-manṭiq", "text": "text/isharat-i.ocr.txt", "originals": [f"original/{I}/{I}_djvu.txt"]}]},
        "normalization": "original/ holds the Archive's own text layer as served (for comparison). text/isharat-i.ocr.txt is the seat's OCR, one block per page headed [page nNNNN]. No text was corrected by hand; the loci keep the OCR's readings (التمثتيل for التمثيل).",
        "scope": "Part I whole, with Forget's French front matter as the OCR reads it.",
        "why_seated": "Inference sorted into qiyās, istiqrāʾ and tamthīl outside the Latin line; the Qiyās of the Shifāʾ is declared absent (no commons edition: Cairo 1964 only).",
    }, [(ST / "avicenna/forget_djvu.txt", f"original/{I}/{I}_djvu.txt")], [("isharat-i.ocr", "text/isharat-i.ocr.txt")], [
        ("the classification of arguments: qiyās, istiqrāʾ, tamthīl", "text/isharat-i.ocr.txt", "اشارة الى القياس والاستقراء والتمثتيل"),
    ])
