#!/usr/bin/env python3
"""EA-CORPORA-42, step 2: build the ten seats of the Contra Geocentrism gathering (the form of build_seats41.py).

    python3 -I build_seats42.py <stage-dir> <seats-dir>

<stage-dir> holds the originals as fetched (one folder per seat) and _text/ from prepare_texts42.py.
<seats-dir> is where the seat folders are written: a staging folder while the seating is assembled, data/corpora/
when the operator says seat. Must print `missing 0` for every seat.
"""
import hashlib, json, pathlib, re, shutil, sys

ST = pathlib.Path(sys.argv[1]); TX = ST / "_text"; SEATS = pathlib.Path(sys.argv[2])
TODAY = "2026-11-22"
RULING = ("Lee Sharks, 2026-11-22 00:33 EST: \"rebekah cranes gets ea corpora deposits. lets expand the scope there, deposit, and "
          "close debts on the contea geocentrism so that were ready to deposit when the ea corpora lands\"; earlier (00:04): \"yup\" "
          "to seating the Academica and the Plutarch; the standing rule for originals-library seatings, 2026-10-18: \"original "
          "language where available always\".")
RESEARCH = {
    "study": "Contra Geocentrism: The Socratic–Peripatetic Corpus Against Its Own Conversion (draft, 2026-11-22, not deposited)",
    "for": "the reports that carried the case against the resting central earth out of the school (Theophrastus in Plutarch and "
           "Cicero, the Placita), the road to Copernicus, the school commentary on De caelo, and the history of blaming the name",
}
SPINE = "EA-CORPORA-42 (assembled 2026-11-22, not deposited)"
PERSEUS = {"repo": "PerseusDL/canonical-greekLit", "commit": "dacb04909e43dc47738828d33cc3d2b0635bc54c"}
PERSEUS_LAT = {"repo": "PerseusDL/canonical-latinLit", "commit": "8cef51623130f2412da410858e32c322eb796c0a"}
F1K = {"repo": "OpenGreekAndLatin/First1KGreek", "commit": "ed91552c52530c8f5a3ddf2dd767e899372a804c"}
CC_SA = "CC BY-SA 4.0 (the TEI packaging, as stated in the file's teiHeader); the underlying editions are public domain"
TEI_NORM = ("The TEI as fetched under original/. text/ is the <text> reduced by code (rebuild/corpora/ea-corpora-42/"
            "prepare_texts42.py, the reducer of EA-CORPORA-41): teiHeader, note, app and bibl dropped; one line per <p>, <l>, "
            "<head> or <ab>; each numbered <div> marked [<subtype> <n>]; the edition's page breaks stand as [p. N] and its "
            "numbered lines as |N. No text was corrected by hand.")
WEB_NORM = ("The page as served under original/. text/ is the page reduced by code (prepare_texts42.py, webpage()): script, style "
            "and edit links dropped, one line per block element, entities decoded; the page's own markers stand as text. No text "
            "was corrected by hand.")


def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def norm(s): return re.sub(r"\s+", " ", s)


def seat(n, name, meta, originals, texts, loci):
    if isinstance(meta.get("license"), str):
        meta["license"] = {"payload": meta["license"], "record": "CC-BY-4.0 applies to this seat record only."}
    d = SEATS / name
    if d.exists(): shutil.rmtree(d)
    (d / "original").mkdir(parents=True); (d / "text").mkdir()
    rows = []
    for src, rel in originals:
        (d / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, d / rel); rows.append(rel)
    for slug, rel in texts:
        shutil.copyfile(TX / f"{slug}.txt", d / rel); rows.append(rel)
    (d / "MANIFEST.sha256").write_text("".join(f"{sha(d / r)}  {r}\n" for r in sorted(rows)))
    found, missing = [], []
    for label, needle in loci:
        hit = [r for _, r in texts if norm(needle) in norm((d / r).read_text(encoding="utf-8"))]
        (found if hit else missing).append(f"{label} — '{needle}' ({hit[0] if hit else 'not found'})")
    for w in meta["works"]["list"]:
        w["lines"] = (d / w["text"]).read_text(encoding="utf-8").count("\n")
    meta = {"corpus": name, "seat": f"EA-CORPORA-42/{n:02d}", **meta, "fetched": TODAY,
            "verified_loci": found, "loci_not_found": missing,
            "lines_total": sum((d / r).read_text(encoding="utf-8").count("\n") for _, r in texts),
            "ruling": RULING, "research": RESEARCH, "spine": SPINE, "axn": None,
            "axn_note": "assigned at deposit, derived from MANIFEST.sha256 as for every seat"}
    (d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    print(f"{meta['seat']} {name:44} works {len(meta['works']['list']):>3}  lines {meta['lines_total']:>7}  loci {len(found)}  missing {len(missing)}")
    if missing: print("   MISSING", missing)


def cts_title(path):
    t = pathlib.Path(path).read_text(encoding="utf-8"); m = re.search(r"<ti:title[^>]*>([^<]*)", t)
    return m.group(1).strip() if m else ""


def tei_seat(n, name, folder, author, edition, why, loci, repo, paths, language="grc"):
    files = sorted(p for p in (ST / folder).glob("*.xml") if "__cts__" not in p.name)
    originals, texts, works = [], [], []
    for f in files:
        stem = f.name.rsplit(".", 1)[0]; wid = ".".join(stem.split(".")[:2]); cts = ST / folder / f"{wid}.__cts__.xml"
        originals.append((f, f"original/{f.name}"))
        if cts.exists(): originals.append((cts, f"original/{wid}.__cts__.xml"))
        rel = f"text/{stem}.txt"; texts.append((f"{folder}--{stem}", rel))
        works.append({"id": stem, "title": f"{author}, {cts_title(cts) if cts.exists() else ''}".strip(", "), "text": rel})
    meta = {"title": f"{author}, {edition}", "edition": edition, "language": language, "license": CC_SA,
            "origin": {**repo, "paths": paths, "transport": "raw.githubusercontent.com at the pinned commit (the repository's HEAD on the day)"},
            "works": {"count": len(works), "units": "one file per work", "per-work": "text/<edition-stem>.txt", "list": works},
            "normalization": TEI_NORM, "scope": "whole, as the repository holds it", "why_seated": why}
    seat(n, name, meta, originals, texts, loci)


def web_seat(n, name, folder, title, edition, language, license, origin, pages, why, loci, scope):
    originals, texts, works = [], [], []
    for stem, wtitle in pages:
        f = ST / folder / f"{stem}.html"
        originals.append((f, f"original/{f.name}")); rel = f"text/{stem}.txt"; texts.append((f"{folder}--{stem}", rel))
        works.append({"id": stem, "title": wtitle, "text": rel})
    meta = {"title": title, "edition": edition, "language": language, "license": license, "origin": origin,
            "works": {"count": len(works), "units": "one file per served page", "per-work": "text/<page>.txt", "list": works},
            "normalization": WEB_NORM, "scope": scope, "why_seated": why}
    seat(n, name, meta, originals, texts, loci)


tei_seat(1, "plutarch-platonic-questions-de-facie-numa", "plutarch42", "Plutarch",
         "Platonicae quaestiones, De facie in orbe lunae, Numa (Perseus canonical-greekLit, perseus-grc2)",
         "THE REPORTS. Platonic Questions 8.1 (1006C): Theophrastus reports that Plato, grown older, repented of giving the earth "
         "the middle place, which did not befit it; the same Question reads the Timaeus's winding earth as the earth Aristarchus and "
         "Seleucus later showed turning. Numa 11: the Pythagorean central fire called Hestia, the earth not of the most honoured parts, "
         "and Plato grown old said to think the same. De facie 6 (923A): Cleanthes held that the Greeks should indict Aristarchus for "
         "impiety, as moving the hearth (Hestia) of the cosmos.",
         [("Plat. Q. 8.1, 1006C, Plato's repentance on Theophrastus's word", "Θεόφραστος δὲ καὶ προσιστορεῖ τῷ Πλάτωνι πρεσβυτέρῳ γενομένῳ μεταμέλειν"),
          ("Plat. Q. 8.1, Aristarchus and Seleucus", "Ἀρίσταρχος καὶ Σέλευκος ἀπεδείκνυσαν"),
          ("Numa 11, the earth not of the most honoured parts", "οὐ τῶν τιμιωτάτων οὐδὲ τῶν πρώτων τοῦ κόσμου μορίων"),
          ("De facie 923A, Cleanthes against Aristarchus", "ὥσπερ Ἀρίσταρχον ᾤετο δεῖν Κλεάνθης τὸν Σάμιον ἀσεβείας προσκαλεῖσθαι τοὺς Ἕλληνας")],
         PERSEUS, ["data/tlg0007/tlg133", "data/tlg0007/tlg126", "data/tlg0007/tlg005"])
tei_seat(2, "pseudo-plutarch-placita", "placita", "Pseudo-Plutarch", "Placita philosophorum (Perseus canonical-greekLit, perseus-grc2)",
         "THE DOXOGRAPHY COPERNICUS QUOTED. Placita III 13: Philolaus's earth carried about the fire, Heraclides and Ecphantus's earth "
         "turning in place like a wheel, the passage Copernicus copies into his dedication; II 24: Aristarchus sets the sun with the "
         "fixed stars and moves the earth about the solar circle.",
         [("III 13, Philolaus", "Φιλόλαος δʼ ὁ Πυθαγόρειος κύκλῳ περιφέρεσθαι περὶ τὸ πῦρ"),
          ("III 13, Heraclides and Ecphantus", "Ἡρακλείδης ὁ Ποντικὸς καὶ Ἔκφαντος ὁ Πυθαγόρειος κινοῦσι μὲν τὴν γῆν"),
          ("II 24, Aristarchus", "Ἀρίσταρχος τὸν ἥλιον ἵστησι μετὰ τῶν ἀπλανῶν")],
         PERSEUS, ["data/tlg0094/tlg003"])
tei_seat(3, "cicero-lucullus", "cicero42", "Cicero", "Lucullus (Academica priora II) (Perseus canonical-latinLit, perseus-lat2)",
         "HICETAS, UT AIT THEOPHRASTUS. Lucullus 123: Hicetas of Syracuse, as Theophrastus says, holds that the heaven and all above "
         "stand and the earth alone turns about its axis, and that all comes out the same as if the earth stood; the first source "
         "Copernicus names. Beside the seated Academica posteriora (EA-CORPORA-13/03).",
         [("Lucullus 123, Hicetas", "Hicetas Syracosius, ut ait Theophrastus"),
          ("Lucullus 123, the appearances alike", "eadem effici omnia quasi stante terra caelum moveretur")],
         PERSEUS_LAT, ["data/phi0474/phi046"], language="lat")
tei_seat(4, "archimedes-arenarius", "archimedes", "Archimedes", "Arenarius (First1KGreek, 1st1K-grc1; Heiberg)",
         "ARISTARCHUS'S HYPOTHESES. The Sand-Reckoner reports that Aristarchus of Samos published writings on certain hypotheses, in "
         "which the fixed stars and the sun stay unmoved and the earth is carried about the sun.",
         [("Aristarchus's hypotheses", "Ἀρίσταρχος δὲ ὁ Σάμιος ὑποθέσιών τινων ἐξέδωκεν γραφάς")],
         F1K, ["data/tlg0552/tlg006"])
tei_seat(5, "simplicius-in-de-caelo", "simplicius42", "Simplicius", "In Aristotelis De caelo commentaria (First1KGreek, 1st1K-grc1; Heiberg, CAG VII)",
         "THE COMMENTARY IN GREEK. Simplicius on De caelo II: Heraclides of Pontus, supposing the earth at the centre moving in a "
         "circle and the heaven at rest, thought he saved the phenomena (p. 519); and again, the earth turning about the centre as "
         "Heraclides supposed (p. 541). Beside the seated In Physica (EA-CORPORA-41/11).",
         [("p. 519, Heraclides saves the phenomena", "Ἡρακλείδης ὁ Ποντικὸς ὑποθέμενος σώζειν ᾤετο"),
          ("p. 541, as Heraclides supposed", "ὡς Ἡρακλείδης ὁ Ποντικὸς ὑπετίθετο")],
         F1K, ["data/tlg4013/tlg001"])

# 42/06: Diels, the OCR layer as served by the Internet Archive
d6 = ST / "diels"
seat(6, "diels-doxographi-graeci",
     {"title": "Diels, Doxographi Graeci (Berlin: Reimer, 1879)", "edition": "Hermann Diels, Doxographi Graeci (Berolini: G. Reimer, 1879) — Internet Archive bub_gb_aaMNAAAAIAAJ (Google Books scan), the OCR layer",
      "language": "mul", "license": "Diels's Doxographi Graeci (1879) is public domain; the OCR layer is the Internet Archive's, as served.",
      "origin": {"source": "Internet Archive", "identifier": "bub_gb_aaMNAAAAIAAJ", "url": "https://archive.org/details/bub_gb_aaMNAAAAIAAJ",
                 "files": ["bub_gb_aaMNAAAAIAAJ_djvu.txt", "bub_gb_aaMNAAAAIAAJ_meta.xml"]},
      "works": {"count": 1, "units": "the volume", "per-work": "text/<id>.txt",
                "list": [{"id": "bub_gb_aaMNAAAAIAAJ_djvu", "title": "Diels, Doxographi Graeci", "text": "text/bub_gb_aaMNAAAAIAAJ_djvu.txt"}]},
      "normalization": "The Archive's _djvu.txt as served, line endings normalized. OCR errors stand; loci are quoted as the OCR reads them.",
      "scope": "whole", "why_seated": "AËTIUS. The reconstructed Placita in parallel with Stobaeus, with Theophrastus's Physical Opinions; "
      "Aëtius I 15 (On colours), in Stobaeus's column, gives Aristarchus of Samos as the hearer of Strato, Theophrastus's successor."},
     [(d6 / "bub_gb_aaMNAAAAIAAJ_djvu.txt", "original/bub_gb_aaMNAAAAIAAJ_djvu.txt"), (d6 / "bub_gb_aaMNAAAAIAAJ_meta.xml", "original/bub_gb_aaMNAAAAIAAJ_meta.xml")],
     [("diels--bub_gb_aaMNAAAAIAAJ_djvu", "text/bub_gb_aaMNAAAAIAAJ_djvu.txt")],
     [("Aëtius I 15, Aristarchus hearer of Strato (OCR: ἀχηυστὴς)", "Αρίσταρχος Σάμιος μαϑηματιχὸς \nἀχηυστὴς Στράτωνος")])

web_seat(7, "aquinas-in-de-caelo", "aquinas", "Thomas Aquinas, In libros Aristotelis De caelo et mundo expositio",
         "The Leonine text (Rome, 1886), as recognized by Enrique Alarcón from Roberto Busa's Index Thomisticus, Corpus Thomisticum (corpusthomisticum.org), books I–III",
         "lat", "The Leonine text (1886) is public domain; the digital text is the Corpus Thomisticum's (Fundación Tomás de Aquino), as served, under its terms.",
         {"source": "Corpus Thomisticum", "urls": [f"https://www.corpusthomisticum.org/ccm{b}.html" for b in (1, 2, 3)]},
         [("aquinas-ccm1", "In De caelo, book I"), ("aquinas-ccm2", "In De caelo, book II"), ("aquinas-ccm3", "In De caelo, book III (to lect. 8)")],
         "THE SCHOOL COMMENTARY. On De caelo II: Aristotle 'supposes for the present that the earth rests, which he will prove later', "
         "with Heraclides and Aristarchus reported as moving it daily (lect. 11 n. 2); the astronomers' suppositions need not be true, "
         "since the appearances might be saved some other way (lect. 17 n. 2); the indecisive phenomena answered with the lunar eclipse, "
         "and the Timaeus's ἰλλομένην read as binding, not motion (lect. 21 nn. 4–5).",
         [("lect. 11 n. 2", "Supponit autem Aristoteles ad praesens quod terra quiescat, quod postmodum probabit"),
          ("lect. 17 n. 2", "Illorum tamen suppositiones quas adinvenerunt, non est necessarium esse veras"),
          ("lect. 21 n. 4", "Sed hoc intelligi posset si terra per modicum spatium distaret a medio"),
          ("lect. 21 n. 5", "si vero scribatur per diphthongum, significat prohibitionem")], "books I–III, as the site holds them")
web_seat(8, "copernicus-de-revolutionibus", "copernicus", "Copernicus, De revolutionibus orbium coelestium (1543): the prefaces and Book I",
         "Wikisource (la.wikisource.org), transcribed from the Nuremberg print of 1543", "lat",
         "The 1543 text is public domain; the Wikisource transcription is CC BY-SA 4.0.",
         {"source": "Latin Wikisource", "urls": [f"https://la.wikisource.org/wiki/De_revolutionibus_orbium_coelestium/{p}" for p in ("01", "02", "05")]},
         [("copernicus-01", "Ad lectorem de hypothesibus huius operis (Osiander)"), ("copernicus-02", "Praefatio authoris (the dedication to Paul III)"),
          ("copernicus-05", "Liber primus")],
         "THE ROAD'S END. The dedication: 'I found first in Cicero that Nicetas held that the earth moved; afterwards in Plutarch', with "
         "Placita III 13 copied in Greek, and from that occasion the turn to the earth's mobility.",
         [("the dedication, Cicero first", "Ac reperi quidem apud Ciceronem primum, Nicetum sensisse terram moveri"),
          ("the dedication, Plutarch after", "Postea & apud Plutarchum inveni quosdam alios in ea fuisse opinione"),
          ("the dedication, the occasion", "Inde igitur occasionem nactus")],
         "the two prefaces and Book I, the pages the transcription holds at the quality it marks")
web_seat(9, "bacon-novum-organum", "bacon", "Bacon, Novum Organum (1620)", "Wikisource (la.wikisource.org)", "lat",
         "The 1620 text is public domain; the Wikisource transcription is CC BY-SA 4.0.",
         {"source": "Latin Wikisource", "urls": [f"https://la.wikisource.org/wiki/Novum_Organum/{p}" for p in ("Praefatio_II", "Liber_Primus", "Liber_Secundus")]},
         [("bacon-Praefatio_II", "Praefatio"), ("bacon-Liber_Primus", "Liber primus"), ("bacon-Liber_Secundus", "Liber secundus")],
         "BLAMING THE NAME. I.63: Aristotle the conspicuous case, 'who corrupted natural philosophy by his dialectic', among the charges "
         "the single proper motion of each body, the premise of De caelo II 14.",
         [("I.63", "Primi generis exemplum in Aristotele maxime conspicuum est, qui philosophiam naturalem dialectica sua corrupit"),
          ("I.63, one motion to each body", "motum singulis corporibus unicum et proprium")], "the Novum Organum proper (the Instauratio front matter not seated)")
web_seat(10, "galileo-dialogo", "galileo", "Galileo, Dialogo sopra i due massimi sistemi del mondo tolemaico e copernicano (1632)",
         "Wikisource (it.wikisource.org), from Le opere di Galileo Galilei, Edizione Nazionale, vol. VII, ed. Antonio Favaro", "ita",
         "The text is public domain; the Wikisource transcription is CC BY-SA 4.0.",
         {"source": "Italian Wikisource", "urls": [f"https://it.wikisource.org/wiki/Dialogo_sopra_i_due_massimi_sistemi_del_mondo_tolemaico_e_copernicano/{p}" for p in ("Al_discreto_lettore", "Giornata_prima", "Giornata_seconda", "Giornata_terza", "Giornata_quarta")]},
         [("galileo-Al_discreto_lettore", "Al discreto lettore"), ("galileo-Giornata_prima", "Giornata prima"), ("galileo-Giornata_seconda", "Giornata seconda"),
          ("galileo-Giornata_terza", "Giornata terza"), ("galileo-Giornata_quarta", "Giornata quarta")],
         "ARISTOTLE AGAINST THE PERIPATETICS. Day 1: Salviati, 'if Aristotle were in our age he would change his opinion', and the "
         "heaven made inalterable by the followers; Simplicio the Peripatetic holding the conclusion as authority.",
         [("Day 1, Salviati", "non dubito punto che se Aristotile fusse all’età nostra"),
          ("Day 1, sense before discourse", "le sensate esperienze si dovessero anteporre a qualsivoglia discorso fabbricato da ingegno umano")],
         "the dialogue whole, the four days with the address to the reader")
