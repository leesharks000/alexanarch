#!/usr/bin/env python3
"""EA-CORPORA-39, step 2: build the seats of "This Is Not Philosophy" (the construction of the object, the field before the
flattening, and the evidence of the census).

    python3 -I build_seats39.py <stage-dir> <seats-dir>

<stage-dir> is the session's staging folder (agph/, construction/, philologus/, cq/, ocr/, census-seat/, gates-seat/).
<seats-dir> is where the seat folders are written: a staging folder while the seating is assembled, data/corpora/ when
the operator says seat. Loci are verified against the text with all whitespace collapsed, so that a passage broken
across the scan's lines is still found; the text files themselves keep the scan's lines.
"""
import hashlib, json, pathlib, re, shutil, sys

ST = pathlib.Path(sys.argv[1]); SEATS = pathlib.Path(sys.argv[2])
TODAY = "2026-11-15"
TRANSPORT = "in-session fetch (Transport D); No-Double-Draw"
RULING = ("Lee Sharks, 2026-11-15 22:43 EST: \"i suppose we need to gather up materials for an ea-corpora seating for this one, "
          "and that that will help the case substantially, especially as we increase holdings beyond the recent, where the "
          "flattening is already largely accomplished\"; 22:56 EST, on the three rulings (cited volumes; the census without the "
          "publishers' abstracts; the gate documents as dated excerpts): \"adopted on all. lets build the seating\"; 23:51 EST, on holding the Archive's text layers once, as served, and on the order: "
          "\"adopted. and the seating goes first - we have more analysis to run from it\".")
RESEARCH = {"study": "This Is Not Philosophy: How Disciplinarity Murdered Philosophy — The Shape of the Field (working notebook v0.16)",
            "for": "the field before the flattening (§4.12), the construction of the object (§§1.5, 3.1), and the census, the reach "
                   "coding and the gates (§§0A, 4, 4.16), held so that the measurements can be read against the texts"}
SPINE = "EA-CORPORA-39 (seated 2026-11-16, not deposited)"
SEAT_REC = "CC-BY-4.0 applies to this seat record only."
PD_US = "public domain in the United States (published before 1931)"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def norm(src, dst):
    """The Archive's text layer with runs of spaces and tabs inside a line reduced to one space; line breaks kept."""
    t = pathlib.Path(src).read_text(encoding="utf-8", errors="replace")
    t = "\n".join(re.sub(r"[ \t]+", " ", l).rstrip() for l in t.replace("\r\n", "\n").split("\n"))
    pathlib.Path(dst).write_text(t, encoding="utf-8")


def ia(ident, files, **kw):
    return {"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}", "files": files, **kw}


DJVU_NORM = ("The Internet Archive's own text layer (_djvu.txt), held under text/ exactly as served, byte for byte: the file's SHA-256 in "
             "MANIFEST.sha256 is the hash of the served file. It is not held a second time under original/ (operator, 2026-11-15 23:51, on the "
             "size of the seating: a second, whitespace-normalized copy added nothing the loci need, since they are verified with all "
             "whitespace collapsed). No text was corrected by hand; the loci keep the scan's readings. The scans are held by reference at "
             "their Archive URLs.")
OCR_NORM = ("This seat's OCR: each page image fetched from the Archive (page/n<k>.jpg), read by tesseract 5 with the tessdata_fast "
            "<lang> model, single thread, and deleted; the pages joined in order, each headed [page nNNNN] (the Archive's leaf "
            "number). The Archive's own text layer, which reads this scan poorly, is held under original/ for comparison. No text "
            "was corrected by hand.")


def seat(n, name, meta, originals, texts, loci):
    """originals: [(src, rel)]; texts: [(src, rel, normalize)]; loci: [(label, rel, needle)]."""
    d = SEATS / name
    if d.exists():   # never overwrite a seat of another seating
        prior = json.loads((d / "source.json").read_text(encoding="utf-8")).get("seat", "") if (d / "source.json").exists() else ""
        assert prior.startswith("EA-CORPORA-39/"), f"{name} is already seated as {prior}; not overwritten"
        shutil.rmtree(d)
    (d / "text").mkdir(parents=True)
    rows = []
    for src, rel in originals:
        (d / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, d / rel); rows.append(rel)
    for src, rel, nm in texts:
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (norm if nm else shutil.copyfile)(src, d / rel); rows.append(rel)
    (d / "MANIFEST.sha256").write_text("".join(f"{sha(d / r)}  {r}\n" for r in sorted(rows)))
    found, missing = [], []
    for label, rel, needle in loci:
        flat = re.sub(r"\s+", " ", (d / rel).read_text(encoding="utf-8", errors="replace"))
        (found if re.sub(r"\s+", " ", needle) in flat else missing).append(f"{label} — '{needle}' ({rel})")
    for w in meta["works"]["list"]:
        w["lines"] = (d / w["text"]).read_text(encoding="utf-8", errors="replace").count("\n")
    meta = {"corpus": name, "seat": f"EA-CORPORA-39/{n:02d}", **meta, "fetched": TODAY,
            "verified_loci": found, "loci_not_found": missing,
            "lines_total": sum((d / r).read_text(encoding="utf-8", errors="replace").count("\n") for _, r, _ in texts),
            "ruling": RULING, "research": RESEARCH, "spine": SPINE, "axn": None,
            "axn_note": "assigned at deposit, derived from MANIFEST.sha256 as for every seat"}
    (d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    print(f"{meta['seat']} {name:44} lines {meta['lines_total']:>8}  loci {len(found)}  missing {len(missing)}")
    for m in missing:
        print("   MISSING", m)


def works(lst):
    return {"count": len(lst), "units": "one text file per volume or work", "list": lst}


def lic(author_dates, extra=""):
    return {"payload": f"{author_dates}; the scan and its text layer are {PD_US}. {extra}The archive asserts no licence over the payload.".replace("  ", " "),
            "record": SEAT_REC}


def simple(n, name, title, ident, slug, lang, author_dates, scope, why, loci, edition=None, **kw):
    src = ST / "construction" / f"{slug}.txt"
    seat(n, name, {"title": title, "edition": edition or f"The Internet Archive scan {ident}", "language": lang,
                   "license": lic(author_dates), "origin": {"items": [ia(ident, [f"{ident}_djvu.txt"])], "transport": TRANSPORT},
                   "works": works([{"slug": slug, "work": title, "text": f"text/{slug}.txt", "served_as": f"{ident}_djvu.txt"}]),
                   "normalization": DJVU_NORM, "scope": scope, "why_seated": why, **kw},
         [], [(src, f"text/{slug}.txt", False)],
         [(lab, f"text/{slug}.txt", nd) for lab, nd in loci])


# 39/01 — the Archiv für Geschichte der Philosophie, I–XXXVI (1888–1923)
AG = ST / "agph"; log = {x["id"]: x for x in json.load(open(AG / "fetch-log.json"))} if (AG / "fetch-log.json").exists() else {}
ag_ids = sorted(p.stem for p in AG.glob("archivfr*.txt"))
seat(1, "agph-archiv-1888-1923",
     {"title": "Archiv für Geschichte der Philosophie, ed. L. Stein et al., I–XXXVI (Berlin: Reimer, 1888–1923)",
      "edition": "The University of Toronto scans at the Internet Archive (archivfrgeschiNNsteiuoft), with the index volumes",
      "language": "de (with fr, en, it, grc)",
      "license": lic("The Archiv's volumes I–XXXVI were printed 1888–1923"),
      "origin": {"items": [ia(i, [f"{i}_djvu.txt"], volume=(log.get(i) or {}).get("volume")) for i in ag_ids], "transport": TRANSPORT},
      "works": works([{"slug": i, "work": f"AGPh {i.replace('archivfrgeschi','').replace('steiuoft','')}", "text": f"text/{i}.txt",
                       "served_as": f"{i}_djvu.txt"} for i in ag_ids]),
      "normalization": DJVU_NORM,
      "scope": "Volumes I–XXXVI as the Toronto run holds them: I–XIII, XV–XXVIII, XXX, XXXI, XXXIII–XXXVI (one volume) and the indexes. "
               "XIV (1901), XXIX (1916) and XXXII (1919) are not in the run and are pointed to.",
      "why_seated": "The field before the flattening (§4.12): in the 1890s one ancient title in five puts a work's standing in question, "
                    "as an ordinary article in a philosophy journal — the authenticity of the Sophistes (1892) and of the De interpretatione "
                    "(1900), the latest athetesis of the Philebus (1896), the order of the Metaphysics (1908).",
      "held_out": "AGPh XIV (1901), XXIX (1916), XXXII (1919): not in the Toronto run at the Archive; to be sought in another scan."},
     [],
     [(AG / f"{i}.txt", f"text/{i}.txt", False) for i in ag_ids],
     [("V (1892) 55–60, Appel, Zur Echtheitsfrage des Dialogs Sophistes: the Sophist mocks Plato's own doctrine of Ideas",
       "text/archivfrgeschi05steiuoft.txt", "Die platonische Lehre von der Erhabenheit und Heiligkeit der Ideenwelt wird im Sophisten offenbar verspottet"),
      ("V (1892), the article's title", "text/archivfrgeschi05steiuoft.txt", "Zur Echtheitsfrage des Dialogs Sophistes"),
      ("IX (1896), the latest athetesis of the Philebus", "text/archivfrgeschi09steiuoft.txt", "Athetese des Philebos"),
      ("XIII (1900), the authenticity of the De interpretatione", "text/archivfrgeschi13steiuoft.txt", "Echtheit der Aristotelischen Hermeneutik"),
      ("XX (1907/08), the order of the Metaphysics", "text/archivfrgeschi20steiuoft.txt", "Anordnung der Aristotelischen Metaphysik")])

# 39/02–39/09 — the construction of the object, 1742–1923
simple(2, "brucker-historia-critica-1742", "Jacob Brucker, Historia critica philosophiae, I (Leipzig: Breitkopf, 1742)",
       "iacobibruckerire06bruc", "brucker-hcp-1742-i", "la", "Brucker (d. 1770)",
       "Volume I as scanned: the preface and the history from the beginnings.",
       "The historiographical concept 'system of philosophy' applied to the ancients (§1.5, Catana): the history told as the narration of the ancients' systems.",
       [("Praefatio: the history as the narration of the systems of the ancients", "enarratione fyftematum veterum")])
simple(3, "brucker-historia-critica-iv-1743", "Jacob Brucker, Historia critica philosophiae, IV.1 (Leipzig: Breitkopf, 1743)",
       "JacobiBruckeriHistoriaCritica4p1", "brucker-hcp-4-1", "la", "Brucker (d. 1770)",
       "The part as scanned (the Archive's text layer covers part of the volume).",
       "The same concept carried to the later Platonists: 'in fyftematis ordinem' (§1.5).",
       [("the Platonists brought it into the order of a system under Ammonius", "in fyftematis ordinem duce Ammonio redegerunt")])
simple(4, "hermann-geschichte-system-1839", "Karl Friedrich Hermann, Geschichte und System der platonischen Philosophie I (Heidelberg: Winter, 1839)",
       "bub_gb_peC8m7Z_6p4C", "hermann-1839", "de", "Hermann (d. 1855)",
       "The first part, the historical-critical foundation.",
       "The genetic reading: Plato's dialogues as stages of a development, the frame later scholarship's chronology inherits (§3.1).",
       [("the classification of the scientific development up to Plato", "Allgemeine Classification der wissenschaftlichen Entwickelung")])
simple(5, "zeller-philosophie-griechen-1865", "Eduard Zeller, Die Philosophie der Griechen in ihrer geschichtlichen Entwicklung I (2nd ed., Tübingen: Fues, 1856/1865)",
       "diephilosophiede01zell", "zeller-pdg-1865", "de", "Zeller (d. 1908)",
       "Volume I as scanned.",
       "The handbook that fixed the received order of Greek philosophy; it records Schaarschmidt's athetesis of the Philolaus fragments as live scholarship.",
       [("the authenticity of the Philolaus fragments contested by Schaarschmidt", "SCHAARSCHMIDT (Die angebl. Schriftstellerei des Philolaus 1864)")])
simple(6, "ueberweg-echtheit-zeitfolge-1861", "Friedrich Ueberweg, Untersuchungen über die Echtheit und Zeitfolge platonischer Schriften (Wien: Gerold, 1861)",
       "bub_gb_IdlBK7eBgeMC", "ueberweg-1861", "de", "Ueberweg (d. 1871)", "The whole book.",
       "The question of genuineness and order as the subject of a book: the Aristotelian testimonies weighed dialogue by dialogue.",
       [("the testimonies for the genuineness of the writings under Plato's name", "Echtheit der unter Plato’s Namen auf uns gekommenen Schriften")])
simple(8, "grote-plato-1865", "George Grote, Plato, and the Other Companions of Sokrates I (London: Murray, 1865)",
       "bub_gb_j9D7DspOx9kC", "grote-plato-1865", "en", "Grote (d. 1871)", "Volume I.",
       "The defence of the Thrasyllan canon against the athetizers: the high-water mark of the question, answered by a canon.",
       [("chapter IV: the canon established by Thrasyllus", "Canon established by Thrasyllus")])
simple(9, "lutoslawski-plato-logic-1897", "Wincenty Lutosławski, The Origin and Growth of Plato's Logic (London: Longmans, 1897)",
       "in.ernet.dli.2015.6224", "lutoslawski-1897", "en", "Lutosławski (d. 1954); the 1897 printing", "The whole book.",
       "Stylometry named and turned on the order of the dialogues: the method that fixed early, middle and late.",
       [("the method of stylometry, running head", "METHOD OF STYLOMETRY")])
# 39/07 — the OCR seat (Schaarschmidt), built when the OCR is complete
OC = ST / "ocr"
for n, name, ident, lang, title, author, scope, why, loci in [
    (7, "schaarschmidt-sammlung-1866", "bub_gb_6jrTSVHrpBQC", "deu",
     "Carl Schaarschmidt, Die Sammlung der platonischen Schriften zur Scheidung der echten von den unechten untersucht (Bonn: Marcus, 1866)",
     "Schaarschmidt (d. 1909)", "The whole book.",
     "The athetesis at its height: the collection examined to divide the genuine from the spurious, with the Sophistes and Politicus among the doubted.",
     [("p. 54: Ueberweg's chronology, 'sofern sie echt sind'", "die kleineren ethischen Dialoge, sofern sie echt sind"),
      ("contents: the spuriousness of the Sophist and Statesman demonstrated", "Unechtheit des Sophista und Politikus nachgewiesen")])]:
    o = OC / f"{ident}.ocr.txt"
    if not o.exists():
        print(f"EA-CORPORA-39/{n:02d} {name}: OCR not complete, not built"); continue
    orig = ST / "construction" / "schaarschmidt-1866.txt"
    originals = [(orig, f"original/{ident}_djvu.txt")] if orig.is_file() else []
    seat(n, name, {"title": title, "edition": f"The Internet Archive scan {ident}", "language": "de", "license": lic(author),
                   "origin": {"items": [ia(ident, ["page images"] + ([f"{ident}_djvu.txt"] if originals else []))], "transport": TRANSPORT},
                   "works": works([{"slug": name, "work": title, "text": f"text/{name}.ocr.txt", "originals": [r for _, r in originals]}]),
                   "normalization": OCR_NORM.replace("<lang>", lang), "scope": scope, "why_seated": why},
         originals, [(o, f"text/{name}.ocr.txt", False)], [(l, f"text/{name}.ocr.txt", nd) for l, nd in loci])

# 39/10 — Philologus, the volumes the baseline cites; 39/11 — the Classical Quarterly, 1914–1929
for n, name, d, title, lang, why, loci in [
    (10, "philologus-cited-1858-1916", "philologus", "Philologus: Zeitschrift für das klassische Altertum, the volumes cited in §4.12c",
     "de (with la, grc)", "The philology journal where the question of a work's standing persisted (§4.12c): the date of the Theaetetus (1890–92), the Metaphysics as the unified work of one author (1896), the date of the Phaedrus (1916).",
     [("LV (1896): the Metaphysics the unified work of one author", "philologus55deutuoft", "einheitliche Werk"),
      ("LXXIII (1914–16): the date of the Phaedrus", "philologus73deutuoft", "Abfassungszeit des Phaidros"),
      ("XLIX (1890): the date of the Theaetetus", "philologus49deutuoft", "Abfassungszeit des Platonischen Theaetet"),
      ("XIII (1858): the authentica of the Berlin Aristotle", "philologus13deutuoft", "authentica der Berliner")]),
    (11, "classical-quarterly-1914-1929", "cq", "The Classical Quarterly, the issues of 1914 and 1926–1929",
     "en (with grc, la)", "The interim question in English (§4.12c): the authenticity and the authorship of the Hippias Major (1926, 1927), the composition of the Politics (1927), the Problems (1928), the text of the Ethics (1929).",
     [("XX (1926): the authenticity of the Hippias Major", "sim_classical-quarterly_1926-01_20_1", "Authenticity of the Hippias"),
      ("XXI (1927) 82 ff., Tarrant, The Authorship of the Hippias Maior (the scan reads the title 'A/PPIAS MATOR'; the opening line)",
       "sim_classical-quarterly_1927-04_21_2", "Continued and detailed study of the Hippias Maior"),
      ("XXII (1928): the pseudo-Aristotelian Problems", "sim_classical-quarterly_1928-01_22_1", "Pseudo-Aristotelian Problems"),
      ("XXIII (1929): the text of the Nicomachean Ethics", "sim_classical-quarterly_1929-01_23_1", "Text of the Nicomachean")])]:
    D = ST / d; logx = {x["id"]: x for x in json.load(open(D / "fetch-log.json"))}
    ids = sorted(p.stem for p in D.glob("*.txt"))
    seat(n, name, {"title": title, "edition": "Internet Archive scans", "language": lang,
                   "license": lic("The volumes seated were printed 1858–1929"),
                   "origin": {"items": [ia(i, [logx[i]["file"]], volume=logx[i].get("volume"), date=logx[i].get("date")) for i in ids], "transport": TRANSPORT},
                   "works": works([{"slug": i, "work": f"{i} ({logx[i].get('date')})", "text": f"text/{i}.txt", "served_as": logx[i]["file"]} for i in ids]),
                   "normalization": DJVU_NORM, "scope": "The volumes or issues that hold the articles §4.12c cites; the rest of the run is pointed to.",
                   "why_seated": why},
         [], [(D / f"{i}.txt", f"text/{i}.txt", False) for i in ids],
         [(lab, f"text/{f}.txt", nd) for lab, f, nd in loci])

# 39/12 — the census; 39/13 — the gates
CS = ST / "census-seat"
rows = sorted(str(p.relative_to(CS)) for p in CS.rglob("*") if p.is_file())
seat(12, "this-is-not-philosophy-census",
     {"title": "The census of This Is Not Philosophy: twenty journals in Crossref and two series in Persée, the object codes, the reach coding with its spans, the adjudication logs, the stylometry and the scripts",
      "edition": "Built in session, 15 November 2026, from Crossref and Persée metadata", "language": "en (data); titles in their languages",
      "license": {"payload": "Crossref metadata as served (Crossref states its metadata open, CC0); Persée's OAI-PMH metadata as served, under the terms Persée states at persee.fr; the codes, spans, logs and scripts are the archive's, CC-BY-4.0. The publishers' abstracts are not reseated; each is reached by its DOI.", "record": SEAT_REC},
      "origin": {"items": [{"source": "Crossref REST API", "url": "https://api.crossref.org/journals/{ISSN}/works"},
                           {"source": "Persée OAI-PMH", "url": "https://oai.persee.fr/oai"}], "transport": TRANSPORT},
      "works": works([{"slug": "census", "work": "the census, the codes and the evidence", "text": "text/README.md", "originals": []}]),
      "normalization": "As built by the scripts held under original/scripts/; the abstracts and reference lists dropped by stage_census39.py; a guard refuses any data file in which a key 'abstract' holds running text.",
      "scope": "All the files the notebook's tables are built from, except the abstracts.",
      "why_seated": "So that every figure in §§4.2–4.16 can be rebuilt from what is seated, and every reach code checked against its span and its DOI."},
     [(CS / r, f"original/{r}") for r in rows], [(ST / "census-README.md", "text/README.md", False)], [])
GS = ST / "gates-seat" / "text" / "gates.md"
seat(13, "this-is-not-philosophy-gates",
     {"title": "The gates of This Is Not Philosophy: the editor's responses to the submissions, and the journal and publisher policies on AI, as dated excerpts",
      "edition": "Excerpted in session, 15 November 2026", "language": "en",
      "license": {"payload": "Excerpts quoted for the record, each with its source and date; the full texts remain at their sources.", "record": SEAT_REC},
      "origin": {"items": [{"source": "the author's correspondence with the editor of Ancient Philosophy (institutional, by the author's ruling of 2026-11-15)"},
                           {"source": "Daily Nous; De Gruyter Brill; the journals' pages, as cited per excerpt"}], "transport": TRANSPORT},
      "works": works([{"slug": "gates", "work": "the gates", "text": "text/gates.md", "originals": []}]),
      "normalization": "Written in session; quotations exact as fetched.",
      "scope": "§0A and §4.16 of the notebook, as excerpts.",
      "why_seated": "The gate read against the census: the specification of the unit in the editor's words, and the policies of the template's home."},
     [], [(GS, "text/gates.md", False)],
     [("the editor, 9 September 2026: the claim refused, the topic admitted", "text/gates.md", "If the paper is not about Aristotle and Theophrastus being one person"),
      ("P&PA, August 2026: the prohibition", "text/gates.md", "Our policy is therefore to prohibit the submission of AI-authored content")])
