#!/usr/bin/env python3
"""EA-CORPORA-41, step 2: build the twelve seats of the Lyceum-and-Judaea gathering, with the tragedians.

    python3 -I build_seats41.py <stage-dir> <seats-dir>

<stage-dir> holds the originals as fetched (one folder per seat, plan.json) and _text/ from prepare_texts41.py.
<seats-dir> is where the seat folders are written: a staging folder while the seating is assembled, data/corpora/
when the operator says seat.
"""
import hashlib, json, pathlib, shutil, sys

ST = pathlib.Path(sys.argv[1])
TX = ST / "_text"
SEATS = pathlib.Path(sys.argv[2])
TODAY = "2026-11-20"
RULING = ("Lee Sharks, 2026-11-20 18:31 EST: \"lets bather all the texts weve touched on or even referred to between then and "
          "here for a ea-corpora seating\"; and: \"put the tragedians in there too while were at it\"; the standing rule for "
          "originals-library seatings, 2026-10-18: \"original language where available always\".")
RESEARCH = {
    "study": "the evening of 2026-11-20: the Cicero and Sulla paste, the wills, Alexander, Antipater and Judaea, Theophrastus's "
             "On Kingship, the Clouds against the treatises, and The Thinkery and the Lyceum (groundwork note, draft v0.1)",
    "for": "the one-corpus premise (Plato, Aristotle and Theophrastus as one corpus in two transmission streams) and the "
           "relations it was read against: the impiety charges, the Macedonian patronage of the school, the Alexander "
           "traditions of Judaea, and the comic and tragic stage the King Archon administered",
}
SPINE = "EA-CORPORA-41 (assembled 2026-11-20, not seated, not deposited)"
PERSEUS = {"repo": "PerseusDL/canonical-greekLit", "commit": "dacb04909e43dc47738828d33cc3d2b0635bc54c"}
PERSEUS_LAT = {"repo": "PerseusDL/canonical-latinLit", "commit": "8cef51623130f2412da410858e32c322eb796c0a"}
F1K = {"repo": "OpenGreekAndLatin/First1KGreek", "commit": "ed91552c52530c8f5a3ddf2dd767e899372a804c"}
CC_SA = "CC BY-SA 4.0 (the TEI packaging, as stated in the file's teiHeader); the underlying editions are public domain"
TEI_NORM = ("The TEI as fetched under original/. text/ is the <text> reduced by code (rebuild/corpora/ea-corpora-41/"
            "prepare_texts41.py): teiHeader, note, app and bibl dropped; one line per <p>, <l>, <head> or <ab>; each numbered "
            "<div> marked [<subtype> <n>]; a numbered verse line carries its edition number as |N, so a play is cited by "
            "line straight from the text layer; a speaker stands as [speaker] <name>; the edition's page breaks stand as "
            "[p. N]. No text was corrected by hand.")


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def seat(n, name, meta, originals, texts, loci):
    """originals: [(src, rel)]; texts: [(slug, rel)] from _text/<slug>.txt; loci: [(label, needle)] searched in the seat's texts."""
    if isinstance(meta.get("license"), str):
        meta["license"] = {"payload": meta["license"], "record": "CC-BY-4.0 applies to this seat record only."}
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
    for label, needle in loci:
        hit = [r for _, r in texts if needle in (d / r).read_text(encoding="utf-8")]
        (found if hit else missing).append(f"{label} — '{needle}' ({hit[0] if hit else 'not found'})")
    for w in meta["works"]["list"]:
        w["lines"] = (d / w["text"]).read_text(encoding="utf-8").count("\n")
    meta = {"corpus": name, "seat": f"EA-CORPORA-41/{n:02d}", **meta, "fetched": TODAY,
            "verified_loci": found, "loci_not_found": missing,
            "lines_total": sum((d / r).read_text(encoding="utf-8").count("\n") for _, r in texts),
            "ruling": RULING, "research": RESEARCH, "spine": SPINE, "axn": None,
            "axn_note": "assigned at deposit, derived from MANIFEST.sha256 as for every seat"}
    (d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    print(f"{meta['seat']} {name:40} works {len(meta['works']['list']):>3}  lines {meta['lines_total']:>7}  loci {len(found)}  missing {len(missing)}")
    if missing:
        print("   MISSING", missing)


def cts_title(path):
    import re
    t = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.search(r"<ti:title[^>]*>([^<]*)", t)
    return m.group(1).strip() if m else ""


def tei_seat(n, name, folder, author, edition, why, loci, repo, paths, language="grc", authors=None):
    files = sorted(p for p in (ST / folder).glob("*.xml") if "__cts__" not in p.name)
    originals, texts, works = [], [], []
    for f in files:
        stem = f.name.rsplit(".", 1)[0]
        wid = ".".join(stem.split(".")[:2])
        cts = ST / folder / f"{wid}.__cts__.xml"
        title = cts_title(cts) if cts.exists() else ""
        originals.append((f, f"original/{f.name}"))
        if cts.exists():
            originals.append((cts, f"original/{wid}.__cts__.xml"))
        rel = f"text/{stem}.txt"
        texts.append((f"{folder}--{stem}", rel))
        wa = next((v for k, v in (authors or {}).items() if stem.startswith(k)), author)
        works.append({"id": stem, "title": f"{wa}, {title}".strip(", "), "text": rel})
    meta = {"title": f"{author}, {edition}" if not authors else edition, "edition": edition, "language": language, "license": CC_SA,
            "origin": {**repo, "paths": paths, "transport": "git sparse checkout of the repository at the pinned commit"},
            "works": {"count": len(works), "units": "one file per work (per volume where the edition is in volumes)",
                      "per-work": "text/<edition-stem>.txt", "list": works},
            "normalization": TEI_NORM, "scope": "whole, as the repository holds it", "why_seated": why}
    seat(n, name, meta, originals, texts, loci)


tei_seat(1, "aeschylus-tragoediae", "aeschylus", "Aeschylus", "Tragoediae (Perseus canonical-greekLit, perseus-grc2)",
         "THE TRAGEDIANS, at the author's word (\"put the tragedians in there too\"). The tragic stage stands beside the comic one "
         "in the relations of the Clouds and the King Archon (Ath. Pol. 57: the King arranges the Lenaia, procession and contest); "
         "the seven plays seated whole so that any locus resolves to bytes.",
         [("Agamemnon 1", "|1 θεοὺς μὲν αἰτῶ τῶνδʼ ἀπαλλαγὴν πόνων"), ("Eumenides 685, the court founded", "πάγον δʼ Ἄρειον")],
         PERSEUS, ["data/tlg0085 — 7 plays"])
tei_seat(2, "sophocles-tragoediae", "sophocles", "Sophocles", "Tragoediae (Perseus canonical-greekLit, perseus-grc2)",
         "THE TRAGEDIANS, at the author's word. The seven plays and the Ichneutae (the satyr play, from the papyrus) seated whole.",
         [("Oedipus Tyrannus 1", "ὦ τέκνα, Κάδμου τοῦ πάλαι νέα τροφή"), ("Oedipus at Colonus, the grove", "Κολωνόν")],
         PERSEUS, ["data/tlg0011 — 8 works"])
tei_seat(3, "euripides-tragoediae", "euripides", "Euripides", "Tragoediae (Perseus canonical-greekLit, perseus-grc2)",
         "THE TRAGEDIANS, at the author's word. The nineteen plays seated whole, the Cyclops and the Rhesus among them.",
         [("Bacchae 1", "|1 ἥκω Διὸς παῖς"), ("Medea 1", "|1 Εἴθ’ ὤφελ’ Ἀργοῦς")],
         PERSEUS, ["data/tlg0006 — 19 plays"])
tei_seat(4, "diodorus-bibliotheca", "diodorus", "Diodorus Siculus", "Bibliotheca historica, books 1–5 and 11–20 (Perseus canonical-greekLit, perseus-grc4–6)",
         "ALEXANDER AND ANTIPATER. Book 17 for Alexander's march by Tyre, Gaza and Egypt, the account in which Jerusalem does not "
         "appear; book 18 for the Lamian War, Crannon and the terms imposed on Athens (the garrison on Munychia, the franchise "
         "limited by property), the settlement at Triparadeisos and Antipater's death; book 19 for Cassander. The edition holds "
         "books 1–5 and 11–20; books 6–10 and 21–40 (the fragments, Hecataeus's account of the Jews at 40.3 among them) are not in it.",
         [("Munychia", "Μουνυχ"), ("Antipater", "Ἀντίπατρος"), ("Andromachus", "Ἀνδρόμαχ")],
         PERSEUS, ["data/tlg0060/tlg001 — perseus-grc4 (11–17), grc5 (1–5), grc6 (18–20)"])
tei_seat(5, "plutarch-phocion-eumenes-demosthenes", "plutarch41", "Plutarch",
         "Phocion, Eumenes, Demosthenes, and On the Fortune or Virtue of Alexander (Perseus canonical-greekLit)",
         "ANTIPATER'S ATHENS. Phocion for the terms after Crannon and the garrison on Munychia; Demosthenes for the flight to "
         "Calauria and the poison; Eumenes for the war of the successors; On the Fortune of Alexander for the philosopher-king "
         "Alexander. Companion to the seated Alexander and Sulla (EA-CORPORA-13/01).",
         [("Phocion, Munychia", "Μουνυχ"), ("Demosthenes, Calauria", "Καλαυρ"), ("Antipater", "Ἀντίπατρ")],
         PERSEUS, ["data/tlg0007/tlg049", "data/tlg0007/tlg041", "data/tlg0007/tlg054", "data/tlg0007/tlg087 (perseus-grc3 of two)"])
tei_seat(6, "aelian-varia-historia", "aelian", "Aelian", "Varia historia (Perseus canonical-greekLit, perseus-grc2)",
         "THE TWO SINS. Varia historia 3.36: asked why he left Athens, Aristotle answered that he would not have the Athenians sin "
         "twice against philosophy, with the death of Socrates the first. The saying the evening's reading turned on, and which the "
         "seated Diogenes does not carry.",
         [("VH 3.36, the two sins", "οὐ βούλεται Ἀθηναίους δὶς ἐξαμαρτεῖν ἐς φιλοσοφίαν"), ("Antipater", "Ἀντίπατρ")],
         PERSEUS, ["data/tlg0545/tlg002"])
tei_seat(7, "lucian-quomodo-historia", "lucian", "Lucian", "Quomodo historia conscribenda sit (Perseus canonical-greekLit, perseus-grc2 of two)",
         "HOW THE HISTORIANS WROTE. Lucian's treatise against flattery and invention in history, cited in the reading of the "
         "ancient historians as composers with incentives.",
         [("flattery", "κολακ")],
         PERSEUS, ["data/tlg0062/tlg053"])
tei_seat(8, "curtius-rufus-historiae", "curtius", "Q. Curtius Rufus", "Historiae Alexandri Magni (Perseus canonical-latinLit, perseus-lat2)",
         "ALEXANDER IN SYRIA. Curtius 4.8: Andromachus, given Coele Syria, burned alive by the Samaritans, the event the "
         "historians record where Josephus records the visit to Jerusalem.",
         [("4.8, Andromachus", "Andromacho")],
         PERSEUS_LAT, ["data/phi0860/phi001"], language="lat")

# 41/09: De oratore from Perseus; De legibus from The Latin Library (not in Perseus at the pinned commit)
f = ST / "cicero41" / "phi0474.phi037.perseus-lat2.xml"
leg = [ST / "cicero41" / "latinlib" / f"leg{b}.shtml" for b in (1, 2, 3)]
seat(9, "cicero-de-oratore-de-legibus",
     {"title": "Cicero, De oratore and De legibus", "edition": "De oratore (Perseus canonical-latinLit, perseus-lat2); De legibus (The Latin Library)",
      "language": "lat",
      "license": "De oratore: " + CC_SA + ". De legibus: the Latin text is public domain; The Latin Library's pages as served.",
      "origin": {"de_oratore": {**PERSEUS_LAT, "paths": ["data/phi0474/phi037"]},
                 "de_legibus": {"source": "The Latin Library", "urls": [f"https://www.thelatinlibrary.com/cicero/leg{b}.shtml" for b in (1, 2, 3)]}},
      "works": {"count": 4, "units": "one file per work or book", "per-work": "text/<id>.txt",
                "list": [{"id": "phi0474.phi037.perseus-lat2", "title": "Cicero, De oratore", "text": "text/phi0474.phi037.perseus-lat2.txt"}] +
                        [{"id": f"de-legibus-{b}", "title": f"Cicero, De legibus {b}", "text": f"text/de-legibus-{b}.txt"} for b in (1, 2, 3)]},
      "normalization": TEI_NORM + " The Latin Library HTML: tags dropped, entities decoded, one line per paragraph.",
      "scope": "whole", "why_seated": "HISTORY AS ORATORY. De legibus 1.5, history as opus … unum hoc oratorium maxime, the evening's "
      "sentence on the genre; De oratore, the dialogue Cicero set in the manner of Aristotle, beside the seated De finibus and Academica (EA-CORPORA-13/03)."},
     [(f, f"original/{f.name}"), (ST / "cicero41" / "phi0474.phi037.__cts__.xml", "original/phi0474.phi037.__cts__.xml")] + [(p, f"original/latinlib/{p.name}") for p in leg],
     [("cicero41--phi0474.phi037.perseus-lat2", "text/phi0474.phi037.perseus-lat2.txt")] + [(f"cicero41--de-legibus-{b}", f"text/de-legibus-{b}.txt") for b in (1, 2, 3)],
     [("De legibus 1.5", "unum hoc oratorium maxime")])

tei_seat(10, "porphyry-de-abstinentia", "porphyry41", "Porphyry", "De abstinentia (First1KGreek, 1st1K-grc1)",
         "THEOPHRASTUS ON THE JEWS. De abstinentia 2.26 carries Theophrastus's On Piety on the Jews as the Syrians who still "
         "sacrifice, philosophers by race; with Clearchus's Aristotle (Josephus, Against Apion 1.176–182, seated) and Hecataeus, "
         "the earliest Greek reports of the Jews, all from the school.",
         [("2.26, Theophrastus on the Jews", "Σύρων μὲν Ἰουδαῖοι"), ("Theophrastus named", "φησὶν ὁ Θεόφραστος")],
         F1K, ["data/tlg2034/tlg003"])
tei_seat(11, "simplicius-in-physica", "simplicius", "Simplicius", "In Aristotelis Physicorum libros commentaria (First1KGreek, 1st1K-grc1; Diels, CAG IX–X)",
         "THE MOISTURE OF THOUGHT. Simplicius preserves Diogenes of Apollonia's own words on air and thought, the doctrine the "
         "Clouds gives Socrates (227–233) and Theophrastus's De sensibus 39–44 reports: the witness outside the Peripatos that "
         "the dispersal reading has to account for.",
         [("Diogenes of Apollonia", "Ἀπολλωνιάτης")],
         F1K, ["data/tlg4013/tlg004"])

# 41/12: the rabbinic Alexander-at-Jerusalem tradition, from Sefaria's API
sef = ST / "sefaria"
months = ("Nisan", "Iyar", "Sivan", "Tammuz", "Av", "Elul", "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shevat", "Adar")
seat(12, "alexander-jerusalem-rabbinic",
     {"title": "The rabbinic Alexander at Jerusalem: Bavli Yoma 69a and Megillat Ta'anit with its scholion",
      "edition": "Bavli Yoma 69a, Wikisource Talmud Bavli (via Sefaria); Megillat Ta'anit with the scholion, Warsaw 1874 (via Sefaria)",
      "language": "heb, arc",
      "license": "Yoma 69a: CC-BY-SA (Wikisource Talmud Bavli, as Sefaria states the version). Megillat Ta'anit, Warsaw 1874: "
                 "Public Domain, as Sefaria states the version (source: National Library of Israel, NNL_ALEPH001239373).",
      "origin": {"source": "Sefaria API v3", "requests": ["https://www.sefaria.org/api/v3/texts/Yoma.69a?version=hebrew|Wikisource Talmud Bavli"] +
                 [f"https://www.sefaria.org/api/v3/texts/Megillat_Ta'anit,_{m}?version=hebrew|Warsaw, 1874" for m in months]},
      "works": {"count": 13, "units": "one file per daf or month", "per-work": "text/<id>.txt",
                "list": [{"id": "yoma-69a", "title": "Bavli Yoma 69a", "text": "text/yoma-69a.txt"}] +
                        [{"id": f"megillat-taanit-{m.lower()}", "title": f"Megillat Ta'anit, {m}", "text": f"text/megillat-taanit-{m.lower()}.txt"} for m in months]},
      "normalization": "The API's JSON as fetched under original/; text/ holds the one version's segments, one per line as [segment N], "
                       "markup stripped, with a header line naming the reference, version and licence. No text corrected by hand.",
      "scope": "Yoma 69a whole; Megillat Ta'anit whole, by month",
      "why_seated": "ALEXANDER IN JUDAEA. Yoma 69a: the Samaritans ask Alexander of Macedon for the Temple, and Simeon the "
                    "Righteous goes out to meet him in the priestly garments, the rabbinic telling of Josephus, AJ 11.317–347 "
                    "(seated) with Jaddua. Megillat Ta'anit 21 Kislev, \"the day of Mount Gerizim\", carries the same story in its "
                    "scholion; its Tevet entry names King Yannai and Queen Shalminon, the Alexander and his wife of AJ 14.10."},
     [(sef / "yoma69a.json", "original/yoma69a.json")] + [(sef / f"mt_{m}.json", f"original/megillat_taanit_{m.lower()}.json") for m in months],
     [("sefaria--yoma-69a", "text/yoma-69a.txt")] + [(f"sefaria--megillat-taanit-{m.lower()}", f"text/megillat-taanit-{m.lower()}.txt") for m in months],
     [("Yoma 69a, Alexander of Macedon", "מאלכסנדרוס מוקדון"), ("Yoma 69a, Simeon the Righteous", "שמעון הצדיק"),
      ("Megillat Ta'anit 21 Kislev", "יום הר גריזין"), ("Megillat Ta'anit, Tevet, Yannai", "ינאי המלך")])

tei_seat(13, "catiline-conspiracy", "catiline", "The Catilinarian conspiracy",
         "Sallust, Catilinae coniuratio; Cicero, In Catilinam I–IV, Pro Murena, Pro Sulla; Plutarch, Cicero, Cato the Younger, Caesar "
         "(Perseus canonical-latinLit and canonical-greekLit)",
         "THE CATILINE CONSPIRACY, at the author's word (\"and the catiline conspiracy\", 2026-11-20 18:40). The conspiracy of 63 BCE "
         "in its own witnesses: Sallust's monograph; Cicero's four speeches against Catiline, the Pro Murena delivered in the same "
         "weeks, and the Pro Sulla for P. Sulla, the dictator's nephew, accused of complicity; Plutarch's Cicero, Cato the Younger "
         "and Caesar for the debate on the conspirators. Companion to Plutarch's Sulla (EA-CORPORA-13/01).",
         [("Sallust, Cat. 5", "L. Catilina, nobili genere natus"), ("Cicero, Cat. 1.1", "quo usque tandem abutere, Catilina"),
          ("Pro Sulla", "Sulla et antea dignitatis suae splendorem"), ("Plutarch, Cicero, Catiline introduced", "Λεύκιον Κατιλίναν")],
         {"repos": [PERSEUS_LAT, PERSEUS]},
         ["canonical-latinLit data/phi0631/phi001 (perseus-lat3 of two)", "data/phi0474/phi013, phi014, phi015",
          "canonical-greekLit data/tlg0007/tlg055, tlg050, tlg048"], language="lat, grc", authors={"phi0631": "Sallust", "phi0474": "Cicero", "tlg0007": "Plutarch"})
tei_seat(14, "appian-dio-sulla-catiline", "appiandio", "Appian and Cassius Dio",
         "Appian, Mithridatica and Bella civilia; Cassius Dio, Historia Romana 36–55 (Perseus canonical-greekLit, perseus-grc2)",
         "SULLA AT ATHENS AND THE CONSPIRACY IN GREEK. Appian's Mithridatic Wars for the war that made Athens a battleground, "
         "Aristion's tyranny and Sulla's siege and sack (86 BCE), the setting of the seizure of Apellicon's library; Appian's Civil "
         "Wars 2 and Cassius Dio 37 for the Catilinarian conspiracy; Dio for the late Republic around both.",
         [("Mithridatica, Aristion of Athens", "διʼ Ἀριστίωνος ἀνδρὸς Ἀθηναίου"), ("Cassius Dio 37, Catiline", "Λούκιος Κατιλίνας ἀνὴρ θρασύτατος")],
         PERSEUS, ["data/tlg0551/tlg014", "data/tlg0551/tlg017", "data/tlg0385/tlg001 (books 36–55, as Perseus holds them)"], authors={"tlg0551": "Appian", "tlg0385": "Cassius Dio"})
