#!/usr/bin/env python3
"""Finish the two seats of EA-CORPORA-44 in data/corpora/: give each source.json the fields the indexes and the shelf read
(seat, lines_total, verified_loci, why_seated, scope, normalization, research, ruling, files), verify every locus in the
text it names, and rewrite MANIFEST.sha256 over the payload (source.json outside it, as in the earlier seatings).
    python3 rebuild/corpora/ea-corpora-44/finish44.py"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
RULING = ('Lee Sharks, 2026-11-27 23:10 EST: "i think we legitimate havent seated the frankfurt school - if so thats a large whoops"; 23:13: "agreed. lets seat"; '
          '23:59: "ok. so lets seat all volumes without notes"; 2026-11-28 00:54: "yup lets cut the non-commons bits"; 02:34: "go".')
RESEARCH = {"study": "none named: the Frankfurt School was found absent from the originals library on 2026-11-27 and seated on that finding",
            "for": "the library itself; first gathering, the others to follow as public copies are found"}
SPEC = {
 "benjamin": dict(seat="EA-CORPORA-44/01",
   why="WALTER BENJAMIN IN THE LANGUAGE HE WROTE IN. The theses on history, the Trauerspiel book, the Baudelaire studies, the Kunstwerk essay, the Passagen-Werk and the rest of the seven volumes, as his words without the editors' apparatus, beside the first printings that are open.",
   scope="Benjamin's own text. The editors' reports and notes, and eight pieces co-signed with or written or translated by authors not seventy years dead, are left out and marked in place; the whole volumes are pinned by address and hash.",
   norm="Wikisource layers are the rendered page with header, images and edit links removed, checked against the page by character count. OCR layers are the Internet Archive text as fetched, cut by character offset, runs of spaces and blank lines collapsed. No text was corrected by hand.",
   loci=[("the angel: 'Engel der Geschichte'", "text/gs1-ueber-den-begriff-der-geschichte-ocr.txt", "Engel der Geschichte"),
         ("thesis VII: 'gegen den Strich zu b…'", "text/gs1-ueber-den-begriff-der-geschichte-ocr.txt", "gegen den Strich zu b"),
         ("thesis XIV: 'Tigersprung'", "text/gs1-ueber-den-begriff-der-geschichte-ocr.txt", "Tigersprung"),
         ("the aura: 'einmalige Erscheinung einer Ferne'", "text/kunstwerk-dritte-fassung.txt", "einmalige Erscheinung einer Ferne"),
         ("the first piece of Einbahnstraße: 'Tankstelle'", "text/einbahnstrasse-1928.txt", "Tankstelle"),
         ("'Dialektik im Stillstand'", "text/gs5-das-passagen-werk-ocr.txt", "Dialektik im Stillstand")]),
 "zeitschrift-fuer-sozialforschung": dict(seat="EA-CORPORA-44/02",
   why="THE INSTITUTE'S JOURNAL, FIXED. Nine yearly volumes held by address and hash, with who wrote what in each year, and the articles of its contributors more than seventy years dead as text. Horkheimer, Adorno, Marcuse, Fromm, Pollock and Löwenthal are in copyright and are pinned, not copied.",
   scope="Thirteen articles by authors more than seventy years dead, and the essay list of each volume. The volumes themselves, and every article by an author still in copyright, are pinned by address, size and SHA-256 and not carried.",
   norm="The Internet Archive text layers as fetched, cut by character offset, runs of spaces and blank lines collapsed. Uncorrected OCR; no text was corrected by hand.",
   loci=[("Benjamin on Fuchs, the title: 'Sammler und der Historiker'", "text/benjamin-eduard-fuchs-1937-ocr.txt", "Sammler und der Historiker"),
         ("Benjamin on Baudelaire: 'Chockerlebnis'", "text/benjamin-ueber-einige-motive-bei-baudelaire-1939-ocr.txt", "Chockerlebnis"),
         ("Grossmann's title: 'Krisenproblem'", "text/grossmann-wert-preis-transformation-1932-ocr.txt", "Krisenproblem"),
         ("the 1932 essay list names its first article: 'Bemerkungen uber Wissenschaft und Krise' (OCR spelling)", "text/inhalt-aufsaetze-jg1-ocr.txt", "Bemerkungen uber Wissenschaft und Krise")]),
}
for name, sp in SPEC.items():
    d = ROOT / "data/corpora" / name; s = json.loads((d / "source.json").read_text(encoding="utf-8"))
    found, missing = [], []
    for lab, f, needle in sp["loci"]:
        (found if needle in (d / f).read_text(encoding="utf-8") else missing).append(f"{lab} ({f})")
    pay = sorted(p for p in d.rglob("*") if p.is_file() and p.name not in ("MANIFEST.sha256", "source.json"))
    if name == "benjamin":
        s["edition"] = ("German Wikisource transcriptions at pinned revisions (thirteen pieces); Internet Archive scans of Deutsche Menschen (1936), the Tableaux Parisiens (1923) and Archiv für Sozialwissenschaft und Sozialpolitik 47 (1920/21); "
                        "Gesammelte Schriften I–VII, ed. Rolf Tiedemann and Hermann Schweppenhäuser with others (Frankfurt am Main: Suhrkamp), Internet Archive text layers cut to Benjamin's text. Each work's source is named in works.list.")
    s.update({"seat": sp["seat"], "scope": sp["scope"], "why_seated": sp["why"], "normalization": sp["norm"],
              "lines_total": sum(p.read_bytes().count(b"\n") for p in pay if p.parts[-2] == "text" or "/text/" in p.as_posix()),
              "verified_loci": found, "loci_not_found": missing, "research": RESEARCH, "ruling": RULING, "seated": "2026-11-28",
              "seating": "pending the EA-CORPORA-44 deposit",
              "files": {p.relative_to(d).as_posix(): ("text layer" if "/text/" in p.as_posix() else "as fetched, byte-exact") for p in pay}})
    (d / "source.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (d / "MANIFEST.sha256").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(d).as_posix()}\n" for p in pay))
    print(name, sp["seat"], "files", len(pay), "lines", s["lines_total"], "loci", len(found), "missing", len(missing), missing)
