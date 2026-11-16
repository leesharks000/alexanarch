#!/usr/bin/env python3
"""EA-CORPORA-40, step 2: build the seats of "Philology Constituted" (the census of Classical Philology, the discipline's
constitution and method, the standing question's canon, the doxography, and the field's history of itself).

    python3 -I build_seats40.py <stage-dir> <census-dir> <seats-dir>

<stage-dir> holds books/ (one served _djvu.txt per work, named by slug), books-log.json, cp/ (one served _djvu.txt per
Classical Philology item, named by its Archive identifier), cp-log.json and cp-jstor-items.json. <census-dir> holds the
census files. Loci are verified against the text with all whitespace collapsed; the text files keep the scan's lines.
"""
import hashlib, json, pathlib, re, shutil, sys

ST = pathlib.Path(sys.argv[1]); CEN = pathlib.Path(sys.argv[2]); SEATS = pathlib.Path(sys.argv[3])
TODAY = "2026-11-16"
TRANSPORT = "in-session fetch (Transport D); No-Double-Draw"
RULING = ("Lee Sharks, 2026-11-16: \"oh - and we need an ea-corpora. what can and should be gathered up? philology is a rich historical "
          "field\"; \"first we check what we have\"; \"lets begin gathering for the ea corpora\"; \"certainly we can locate wilamowitz "
          "elsewhere... and Nietzsche - there must be copies\"; 14:48 EST: \"and then yes lets build the ea-corpora deposit\".")
RESEARCH = {"study": "The Philology Census: Classical Philology first (working notebook v0.1, not deposited), the combined audit's next station after #1770 and #1773",
            "for": "the census of Classical Philology read on the page and not only in its titles (notebook §4, limits; §5.3), and the constitution of "
                   "philology, its method, its boundary and its standing question, against which the census's codes are read"}
SPINE = "EA-CORPORA-40 (seated 2026-11-16, not deposited)"
SEAT_REC = "CC-BY-4.0 applies to this seat record only."
PD_US = "public domain in the United States (published before 1931)"
BL = json.loads((ST / "books-log.json").read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def ia(ident, files, **kw):
    return {"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}", "files": files, **kw}


DJVU_NORM = ("The Internet Archive's own text layer (_djvu.txt), held under text/ exactly as served, byte for byte: the file's SHA-256 in "
             "MANIFEST.sha256 is the hash of the served file, checked against the fetch log. It is held once (the form of EA-CORPORA-39). "
             "No text was corrected by hand; the loci keep the scan's readings. The scans are held by reference at their Archive URLs.")


def seat(n, name, meta, texts, loci, originals=()):
    d = SEATS / name
    if d.exists():   # never overwrite a seat of another seating
        prior = json.loads((d / "source.json").read_text(encoding="utf-8")).get("seat", "") if (d / "source.json").exists() else ""
        assert prior.startswith("EA-CORPORA-40/"), f"{name} is already seated as {prior}; not overwritten"
        shutil.rmtree(d)
    (d / "text").mkdir(parents=True)
    rows = []
    for src, rel in list(originals) + list(texts):
        (d / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, d / rel); rows.append(rel)
    (d / "MANIFEST.sha256").write_text("".join(f"{sha(d / r)}  {r}\n" for r in sorted(rows)))
    found, missing = [], []
    for label, rel, needle in loci:
        flat = re.sub(r"\s+", " ", (d / rel).read_text(encoding="utf-8", errors="replace"))
        (found if re.sub(r"\s+", " ", needle) in flat else missing).append(f"{label} — '{needle}' ({rel})")
    for w in meta["works"]["list"]:
        w["lines"] = (d / w["text"]).read_text(encoding="utf-8", errors="replace").count("\n")
    meta = {"corpus": name, "seat": f"EA-CORPORA-40/{n:02d}", **meta, "fetched": TODAY,
            "verified_loci": found, "loci_not_found": missing,
            "lines_total": sum((d / r).read_text(encoding="utf-8", errors="replace").count("\n") for _, r in texts),
            "ruling": RULING, "research": RESEARCH, "spine": SPINE, "axn": None,
            "axn_note": "assigned at deposit, derived from MANIFEST.sha256 as for every seat"}
    (d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    print(f"{meta['seat']} {name:48} lines {meta['lines_total']:>8}  loci {len(found)}  missing {len(missing)}")
    for m in missing:
        print("   MISSING", m)


def works(lst, units="one text file per volume or work"):
    return {"count": len(lst), "units": units, "list": lst}


def lic(author_dates, extra=""):
    return {"payload": f"{author_dates}; the scan and its text layer are {PD_US}. {extra}The archive asserts no licence over the payload.".replace("  ", " "),
            "record": SEAT_REC}


def book(n, name, title, slugs, lang, author_dates, scope, why, loci, edition=None, **kw):
    """slugs: [(slug, work label)]; loci: [(label, slug, needle)]."""
    for s, _ in slugs:
        assert sha(ST / "books" / f"{s}.txt") == BL[s]["sha256"], f"{s}: hash does not match the fetch log"
    seat(n, name, {"title": title, "edition": edition or "; ".join(f"the Internet Archive scan {BL[s]['identifier']}" for s, _ in slugs),
                   "language": lang, "license": lic(author_dates),
                   "origin": {"items": [ia(BL[s]["identifier"], [BL[s]["file"]], date=BL[s].get("date")) for s, _ in slugs], "transport": TRANSPORT},
                   "works": works([{"slug": s, "work": w, "text": f"text/{s}.txt", "served_as": BL[s]["file"]} for s, w in slugs]),
                   "normalization": DJVU_NORM, "scope": scope, "why_seated": why, **kw},
         [(ST / "books" / f"{s}.txt", f"text/{s}.txt") for s, _ in slugs],
         [(lab, f"text/{s}.txt", nd) for lab, s, nd in loci])


# 40/01 — Classical Philology, 1906–1922, whole, as JSTOR's Early Journal Content at the Internet Archive
CL = json.loads((ST / "cp-log.json").read_text(encoding="utf-8"))
ids = sorted(CL, key=lambda i: (CL[i].get("date") or "", int(i.split("-")[1])))
for i in ids:
    assert sha(ST / "cp" / f"{i}.txt") == CL[i]["sha256"], f"{i}: hash does not match the fetch log"
seat(1, "classical-philology-1906-1922",
     {"title": "Classical Philology I–XVII (Chicago: University of Chicago Press, 1906–1922), article by article, as JSTOR's Early Journal Content",
      "edition": "JSTOR Early Journal Content at the Internet Archive (identifiers jstor-NNNNNN), one item per article, note or review",
      "language": "en (with grc, la, de, fr)",
      "license": lic("Classical Philology I–XVII were published 1906–1922",
                     "JSTOR released its Early Journal Content (pre-1923 US, pre-1870 elsewhere) free to the public in 2011; "),
      "origin": {"items": [ia(i, [CL[i]["url"].rsplit("/", 1)[1]], date=CL[i].get("date")) for i in ids], "transport": TRANSPORT},
      "works": works([{"slug": i, "work": f"{CL[i].get('title')} ({(CL[i].get('date') or '')[:10]})", "text": f"text/{i}.txt",
                       "served_as": CL[i]["url"].rsplit("/", 1)[1]} for i in ids], "one text file per item, article, note or review"),
      "normalization": DJVU_NORM,
      "scope": f"Every Classical Philology item the Archive holds as Early Journal Content dated 1906–1922: {len(ids)} items "
               "(the advanced-search listing returned 922 rows, with duplicates; every distinct identifier is seated). "
               "1923–1928, public domain in the United States since 2024, is not in the Early Journal Content and is pointed to.",
      "why_seated": "The census of Classical Philology (40/16; notebook §1) is coded from titles, because Crossref holds no abstracts for the journal. "
                    "Seated whole, the early volumes let the census read the text question on the page at each grain, locus, work and corpus, "
                    "as #1773 §4.12g read the Archiv.",
      "held_out": "Classical Philology 1923–1928: in the United States public domain, not in JSTOR's Early Journal Content at the Archive; to be sought in another scan."},
     [(ST / "cp" / f"{i}.txt", f"text/{i}.txt") for i in ids],
     [("1907 (jstor-261668), a note on the authenticity of the Twelve Tables", "text/jstor-261668.txt", "the authenticity of the Twelve Tables"),
      ("jstor-262296, the authenticity of the Eighth Idyll of Theocritus defended", "text/jstor-262296.txt", "It defends the authenticity of the Eighth Idyll")])

# 40/02–40/06 — the discipline defined
book(2, "wolf-prolegomena-1795", "F. A. Wolf, Prolegomena ad Homerum, sive de operum Homericorum prisca et genuina forma variisque mutationibus et probabili ratione emendandi, I (Halle: Libraria Orphanotrophei, 1795)",
     [("wolf-prolegomena-1795", "Prolegomena ad Homerum I (1795), the first printing")], "la (with grc)", "Wolf (d. 1824)",
     "Volume I, the Prolegomena, in the printing of 1795 (Google Books scan, the Archive's bub_gb_3yoUAAAAQAAJ).",
     "One name into many: the demonstration that the Homeric poems were composed and fixed by many hands, the operation the census measures at the grain of the corpus.",
     [("the title: the prisca et genuina forma and its variae mutationes", "wolf-prolegomena-1795", "VARIISQUE MUTATIONIBUS"),
      ("the dedication to Ruhnken, princeps criticorum", "wolf-prolegomena-1795", "DAVIDI RUHNKENIO")])
book(3, "wolf-darstellung-altertumswissenschaft-1807", "F. A. Wolf, Darstellung der Alterthums-Wissenschaft (1807), in Fr. Aug. Wolf's Darstellung der Alterthums-Wissenschaft, nebst einer Auswahl seiner kleinen Schriften, ed. S. F. W. Hoffmann (Leipzig: Lehnhold, 1833)",
     [("wolf-darstellung-1807-ed1833", "Darstellung der Alterthums-Wissenschaft (1807), in the edition of 1833")], "de (with la, grc)", "Wolf (d. 1824); the edition of 1833",
     "The Darstellung with the selection of shorter writings, as the 1833 edition prints them (Bayerische Staatsbibliothek scan 10254672bsb).",
     "The discipline defined: Altertumswissenschaft as the knowledge of Greek and Roman antiquity, with the Egyptians, Hebrews, Persians and the other nations of the East set apart by definition.",
     [("the exclusion: the Hebrews not to be set on one line with the Greeks and Romans", "wolf-darstellung-1807-ed1833", "Perser und andere Nationen des Orients auf Einer Linie mit den Griechen und Römern")])
book(4, "boeckh-encyklopaedie-1877", "August Boeckh, Encyklopädie und Methodologie der philologischen Wissenschaften, ed. E. Bratuscheck (Leipzig: Teubner, 1877)",
     [("boeckh-encyklopaedie-1877", "Encyklopädie und Methodologie der philologischen Wissenschaften (1877)")], "de (with la, grc)", "Boeckh (d. 1867); Bratuscheck (d. 1883)",
     "The whole book, the lectures as Bratuscheck edited them (University of Toronto scan).",
     "Philology defined as the knowledge of what has been known, the definition every later account of the discipline answers.",
     [("philology as Erkenntniss des Erkannten", "boeckh-encyklopaedie-1877", "Erkenntniss des Erkannten")])
book(5, "usener-philologie-geschichtswissenschaft-1882", "Hermann Usener, Philologie und Geschichtswissenschaft (Bonn: Cohen, 1882)",
     [("usener-philologie-geschichtswissenschaft-1882", "Philologie und Geschichtswissenschaft (1882)")], "de", "Usener (d. 1905)",
     "The whole address.",
     "Philology placed among the historical sciences, with its own history as the unfolding of its concept.",
     [("the title page", "usener-philologie-geschichtswissenschaft-1882", "HERMANN USENER BONN VERLAG VON MAX COHEN")])

# 40/06–40/08 — the method
book(6, "lachmann-lucretius-1850", "Karl Lachmann, In T. Lucretii Cari De rerum natura libros commentarius (Berlin: Reimer, 1850)",
     [("lachmann-lucretius-commentarius-1850", "In T. Lucretii Cari De rerum natura libros commentarius (1850)")], "la", "Lachmann (d. 1851)",
     "The commentary, as scanned.", "The method named for him, run on a Latin poet: recension, the archetype, and the editor's account of the manuscripts.",
     [("the codices reported to Lachmann by his helpers", "lachmann-lucretius-commentarius-1850", "in Lucretii ingenio cognoscendo versati")])
book(7, "madvig-adversaria-critica-1871-1873", "J. N. Madvig, Adversaria critica ad scriptores Graecos et Latinos I–II (Copenhagen: Gyldendal, 1871–1873)",
     [("madvig-adversaria-i-1871", "Adversaria critica I (1871)"), ("madvig-adversaria-ii-1873", "Adversaria critica II (1873)")], "la (with grc)", "Madvig (d. 1886)",
     "Volumes I and II; volume III (1884) is pointed to.", "Conjectural criticism as a body of work: the locus grain, the one the census finds holding.",
     [("vol. I, the title", "madvig-adversaria-i-1871", "ADVERSARIA CRITICA"), ("vol. II, the title", "madvig-adversaria-ii-1873", "ADVERSARIA CRITICA")],
     held_out="Adversaria critica III (1884): not yet located.")
book(8, "housman-manilius-ii-1912", "A. E. Housman, M. Manilii Astronomicon liber secundus (London: Grant Richards, 1912)",
     [("housman-manilius-ii-1912", "Astronomicon II, recensuit et enarravit A. E. Housman (1912)")], "la", "Housman (d. 1936); published 1912",
     "Book II (University of Toronto scan, catalogued by the Archive as 1903, the date of Book I; the title page reads MDCCCCXII).",
     "The method at its most exacting, in Housman's own edition. Book I (1903), whose preface is the manifesto, is not at the Archive and is pointed to.",
     [("the title page, 1912", "housman-manilius-ii-1912", "RECENSVIT ET ENARRAVIT Α. E. HOVSMAN LONDINII APVD GRANT RICHARDS MDCCCCXII")],
     held_out="Manilius I (1903), with the preface; 'The Application of Thought to Textual Criticism' (1921): not yet located in an open scan.")

# 40/09–40/10 — the boundary drawn: the quarrel over the Geburt der Tragödie
book(9, "nietzsche-philologica-1869-1910", "Friedrich Nietzsche, the philological writings: Homer und die classische Philologie (1869), in Werke IX (Leipzig: Naumann, 1896); Beiträge zur Quellenkunde und Kritik des Laertius Diogenes (Basel, 1870); Philologica I, ed. E. Holzer, Werke XVII (Leipzig: Kröner, 1910)",
     [("nietzsche-werke-ix-1896-homer-und-die-classische-philologie-1869", "Werke IX (1896): Homer und die classische Philologie (1869), with the drafts for the Geburt"),
      ("nietzsche-beitraege-laertius-1870", "Beiträge zur Quellenkunde und Kritik des Laertius Diogenes (1870)"),
      ("nietzsche-philologica-i", "Philologica I (Werke XVII, 1910): the printed philological papers 1867–1872 and the Basel lectures, with the Einleitung in das Studium der classischen Philologie")],
     "de (with la, grc)", "Nietzsche (d. 1900); the editions of 1870, 1896 and 1910",
     "Three volumes, whole. The Geburt der Tragödie itself is seated in its new edition of 1886 (EA-CORPORA-27/03) and is not reseated.",
     "The philologist the field refused: his inaugural lecture on Homer and the discipline, his source criticism of Diogenes Laertius, and his Basel introduction to the study of classical philology.",
     [("Werke IX, the inaugural lecture", "nietzsche-werke-ix-1896-homer-und-die-classische-philologie-1869", "Homer und die classische Philologie"),
      ("Philologica I, the Basel introduction to the study", "nietzsche-philologica-i", "Einleitung in das .Studium der classischen Philologie"),
      ("the Laertius studies, the title", "nietzsche-beitraege-laertius-1870", "Laertius Diogenes")])
book(10, "rohde-afterphilologie-1872", "Erwin Rohde, Afterphilologie: Zur Beleuchtung des von dem Dr. phil. Ulrich von Wilamowitz-Möllendorff herausgegebenen Pamphlets: \"Zukunftsphilologie!\" (Leipzig: Fritzsch, 1872)",
     [("rohde-afterphilologie-1872", "Afterphilologie (1872)")], "de (with grc)", "Rohde (d. 1898)", "The whole pamphlet.",
     "The answer to Wilamowitz's Zukunftsphilologie!: the field drawing its boundary against a book, and the book's defender answering.",
     [("the title", "rohde-afterphilologie-1872", "AFTERPHILOLOGIE"), ("the pamphlet answered", "rohde-afterphilologie-1872", "Zukunftsphilologie")],
     held_out="Wilamowitz, Zukunftsphilologie! (1872) and its second part (1873): located at Google Books (PtVXAAAAcAAJ, i1NbAAAAcAAJ), not fetchable from the session; awaiting the author's copies.")

# 40/11–40/13 — the standing question's canon
book(11, "valla-donatio-schwahn-1928", "Lorenzo Valla, De falso credita et ementita Constantini donatione declamatio, ed. W. Schwahn (Leipzig: Teubner, 1928)",
     [("valla-donatio-schwahn-1928", "De falso credita et ementita Constantini donatione (1440), Schwahn's edition (1928)")], "la", "Valla (d. 1457); the edition of 1928",
     "The declamation in Schwahn's Teubner text with its apparatus.", "The first demonstration that a received document was not what it was received as.",
     [("the title", "valla-donatio-schwahn-1928", "Constantini donatione")])
book(12, "casaubon-exercitationes-1614", "Isaac Casaubon, De rebus sacris et ecclesiasticis exercitationes XVI ad Cardinalis Baronii Prolegomena in Annales (London: Norton, 1614)",
     [("casaubon-exercitationes-1614", "De rebus sacris et ecclesiasticis exercitationes XVI (1614)")], "la (with grc)", "Casaubon (d. 1614)",
     "The whole book as scanned.", "The Hermetica dated after Christ: an ancient author dissolved by a philologist's reading of the books under his name.",
     [("the books falsely ascribed to Hermes", "casaubon-exercitationes-1614", "de libris iam olim falfo Hermeti adferiptis")])
book(13, "bentley-phalaris-1699", "Richard Bentley, A Dissertation upon the Epistles of Phalaris, with an Answer to the Objections of the Honourable Charles Boyle (London: Mortlock and Hartley, 1699)",
     [("bentley-phalaris-1699", "A Dissertation upon the Epistles of Phalaris (1699)")], "en (with grc, la)", "Bentley (d. 1742)", "The whole book.",
     "The Epistles of Phalaris shown to be a later forgery: the standing question settled by language, chronology and the record.",
     [("the dissertation's head", "bentley-phalaris-1699", "DISSERTATION UPON THE EPISTLES")])

# 40/14 — the doxography; 40/15 — the field's history of itself
book(14, "diels-doxographi-graeci-1879", "Hermann Diels, Doxographi Graeci (Berlin: Reimer, 1879)",
     [("diels-doxographi-graeci-1879", "Doxographi Graeci (1879)")], "la, grc", "Diels (d. 1922)", "The whole book (Google Books scan).",
     "The construction behind every report of the Presocratics 'from Theophrastus': the source the Theophrastus line (#1580–#1605) reads against.",
     [("the title", "diels-doxographi-graeci-1879", "DOXOGRAPHI GRAECI"), ("Theophrastus named", "diels-doxographi-graeci-1879", "Theophrasti")])
book(15, "sandys-history-classical-scholarship-1903-1908", "J. E. Sandys, A History of Classical Scholarship I–III (Cambridge: University Press, 1903–1908)",
     [("sandys-history-classical-scholarship-i-1903", "I, from the sixth century B.C. to the end of the Middle Ages (1903)"),
      ("sandys-history-classical-scholarship-ii-1908", "II, from the revival of learning to the end of the eighteenth century (1908)"),
      ("sandys-history-classical-scholarship-iii-1908", "III, the eighteenth century in Germany, and the nineteenth century (1908)")],
     "en (with la, grc)", "Sandys (d. 1922)", "All three volumes.",
     "The field's history of itself, in English, at the moment the discipline was settled: Wolf's matriculation as Studiosus Philologiae told as an epoch.",
     [("III, Wolf's matriculation at Göttingen, 8 April 1777", "sandys-history-classical-scholarship-iii-1908", "matriculation-book as Studiosus Philologiae"),
      ("III, the pro-rector's objection", "sandys-history-classical-scholarship-iii-1908", "Philology was not one of")],
     held_out="Wilamowitz, Geschichte der Philologie (1921): public domain in the United States; not yet located.")

# 40/16 — the census of Classical Philology
files = ["census-cp.json", "cp-items.json", "cp-titles-all.csv", "cp-titles-sample390.csv", "sample390-ids.json", "d3-candidates.json",
         "census_cp.py", "PHILOLOGY-CENSUS-notebook-v0.1.md", "EA-CORPORA-philology-inventory.md"]
cj = json.loads((CEN / "census-cp.json").read_text(encoding="utf-8"))
assert all(not (w.get("abstract") or "").strip() for w in cj["works"]), "an abstract with text in the census"
seat(16, "philology-census-classical-philology",
     {"title": "The census of Classical Philology, 1906–2026: the Crossref records, the items kept, the samples for the blind run, the corpus-grain candidates read by hand, the script and the working notebook",
      "edition": "Built in session, 16 November 2026, from Crossref metadata", "language": "en (data); titles in their languages",
      "license": {"payload": "Crossref metadata as served (Crossref states its metadata open, CC0). Crossref holds no abstracts for this journal (0 of 11,206); none is seated. The items, samples, codes, script and notebook are the archive's, CC-BY-4.0.", "record": SEAT_REC},
      "origin": {"items": [{"source": "Crossref REST API", "url": cj["source"], "read": cj["read"], "raw_sha256": cj["raw_sha256"]}], "transport": TRANSPORT},
      "works": works([{"slug": "census", "work": "the census and its working files", "text": "text/README.md", "originals": [f"original/{f}" for f in files]}]),
      "normalization": "As built by census_cp.py (held under original/): the raw Crossref response is recorded by its SHA-256 and not reseated; the works list keeps DOI, year, type, title, subtitle, authors, volume, issue, page and citation count.",
      "scope": "Every file the notebook's tables and samples are built from.",
      "why_seated": "So that every figure in the notebook (§§1, 4) can be rebuilt from what is seated, and the blind parallel run joined to the sample by its ids."},
     [(CEN / "census-README.md", "text/README.md")], [], originals=[(CEN / f, f"original/{f}") for f in files])
