"""EA-CORPORA-36 v1.1, Part F (36/33–36/40): the sources of the reception study, at the operator's word of 2026-11-07 14:42 EST ("lets expand
it to include all materials well need for the reception study in one bundle"), the study being how Sappho became a jealous woman (the
operator's question of 14:13 EST: "im particularly interested in how sappho became a jealous woman rather than a writer, which i believe
begins with lucretius"), with the texts Closing the Fragment v7 cites that the library did not yet hold. The ancient witnesses already seated
(Lucretius, Theocritus, Apollonius, Horace, Ovid, Herodotus, Athenaeus) enter as cross-references in xref36.py.   python3 gen_spec36_partF.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
base = json.loads((H / "spec36-cicero-tusculanae.json").read_text(encoding="utf-8"))
RULING = base["ruling"] + (" And at 14:42 EST: \"lets expand it to include all materials well need for the reception study in one bundle\"; the study "
          "is the operator's question of 14:13 EST: \"im particularly interested in how sappho became a jealous woman rather than a writer, which i "
          "believe begins with lucretius\".")
SEATING, NORM = base["seating"], base["normalization"]
RESEARCH = base["research"] + (" From v1.1, also the reception study of how Sappho became a jealous woman, from Lucretius's division of fr. 31 "
            "(DRN 3.152–58 and 4.1139–40) through Hermann's reading of 1816 and Welcker's answer to it.")
GC = "a6eb0cc3e6f6e382934a2c8b33577d2fb4371e00"; LC = "8b536bdf3ed1f43494055efe112433b4a58eab67"; FC = "ed91552c52530c8f5a3ddf2dd767e899372a804c"
F = "the jealousy reading"
PERSEUS_LIC = "Perseus Digital Library TEI under CC BY-SA 4.0 (the packaging); the edition in the public domain"


def pg(slug, work, tlg, ed, cls=F):
    a, w = tlg.split(".")
    return {"kind": "tei", "slug": slug, "work": work, "url": f"https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/{GC}/data/{a}/{w}/{tlg}.perseus-{ed}.xml",
            "path": f"perseus/{tlg}.perseus-{ed}.xml", "source": "PerseusDL/canonical-greekLit", "repository": "https://github.com/PerseusDL/canonical-greekLit",
            "commit": GC, "file": f"data/{a}/{w}/{tlg}.perseus-{ed}.xml", "class": cls}


def pl(slug, work, phi, ed, cls=F):
    a, w = phi.split(".")
    return {"kind": "tei", "slug": slug, "work": work, "url": f"https://raw.githubusercontent.com/PerseusDL/canonical-latinLit/{LC}/data/{a}/{w}/{phi}.perseus-{ed}.xml",
            "path": f"perseus/{phi}.perseus-{ed}.xml", "source": "PerseusDL/canonical-latinLit", "repository": "https://github.com/PerseusDL/canonical-latinLit",
            "commit": LC, "file": f"data/{a}/{w}/{phi}.perseus-{ed}.xml", "class": cls}


SEATS = [
 ("hermann-elementa-1816", "33", "G. Hermann, Elementa doctrinae metricae (Leipzig, 1816)", "lat, grc",
  "Public domain everywhere (1816; Hermann died 1848).",
  [{"kind": "ia", "slug": "hermann-1816", "work": "G. Hermann, Elementa doctrinae metricae (Lipsiae: apud Gerh. Fleischerum, 1816), the Library of Congress copy",
    "identifier": "godofredihermann00herm", "files": ["godofredihermann00herm_djvu.txt"], "class": F}],
  "The book whole.",
  "Hermann's conjectured close of fr. 31, and with it the jealousy reading stated as the sense of the last line: 'invidens Sappho viro illi, "
  "omnia sibi audenda dicit'. Welcker answers it the same year (36/06), naming it ('Darum hat Hermann einen andern Schluß erfunden') and "
  "denying the jealousy ('nicht, wie man irrig gewähnt hat, aus dunkler Eifersucht')."),
 ("plutarch-demetrius-amatorius", "34", "Plutarch, Demetrius and Amatorius (Perseus)", "grc",
  PERSEUS_LIC + " (Perrin's Lives, 1920, and Bernardakis's Moralia, 1892).",
  [pg("plutarch-demetrius", "Plutarch, Demetrius, ed. B. Perrin (Loeb, 1920), Perseus tlg0007.tlg057 grc2 (38: Erasistratus reads the symptoms of fr. 31 in Antiochus)", "tlg0007.tlg057", "grc2"),
   pg("plutarch-amatorius", "Plutarch, Amatorius, ed. G. N. Bernardakis (Leipzig, 1892), Perseus tlg0007.tlg113 grc2 (18, 763a: fr. 31 as love at the beloved's appearing)", "tlg0007.tlg113", "grc2")],
  "The two works whole.",
  "The two ancient readings of fr. 31's symptoms as love: the physician's diagnosis in the Life (Erasistratus finds in Antiochus 'the things of "
  "Sappho', the stepmother the cause) and the Amatorius's quotation of the poem as what love does at the beloved's appearing, the passage "
  "Smyth (36/21) cites against the jealousy reading."),
 ("erasistratus-witnesses", "35", "The Erasistratus story in its other carriers: Valerius Maximus 5.7 ext. 1 and Appian, Syriaca 59–61 (Perseus)", "lat, grc",
  PERSEUS_LIC + " (Kempf's Valerius, 1888; White's Appian, 1899).",
  [pl("valerius-maximus", "Valerius Maximus, Facta et dicta memorabilia, ed. C. Kempf (Leipzig, 1888), Perseus phi1038.phi001 lat1", "phi1038.phi001", "lat1"),
   pg("appian-syriaca", "Appian, Syriaca, ed. L. Mendelssohn and P. Viereck, via Perseus tlg0551.tlg013 grc2", "tlg0551.tlg013", "grc2")],
  "The two works whole.",
  "The story of Antiochus and Stratonice without Sappho's name: the symptoms read by a physician as love for a woman the patient may not have, "
  "the frame in which fr. 31's body becomes a case history."),
 ("gellius-noctes-atticae", "36", "Aulus Gellius, Noctes Atticae (Perseus)", "lat",
  PERSEUS_LIC + " (Hosius's edition, 1903).",
  [pl("gellius", "A. Gellius, Noctes Atticae, ed. C. Hosius (Leipzig, 1903), Perseus phi1254.phi001 lat2 (19.9: Valerius Aedituus)", "phi1254.phi001", "lat2")],
  "The twenty books whole.",
  "19.9, where Julianus has the early Latin love epigrams recited, Valerius Aedituus's among them, the Roman fr. 31 before Catullus: speech "
  "failing, sweat, the heart giving out."),
 ("maximus-tyrius", "37", "Maximus of Tyre, Dissertationes (First1KGreek)", "grc",
  "First1KGreek TEI under CC BY-SA 4.0 (the packaging); Hobein's edition (Leipzig, 1910) in the public domain in the United States.",
  [{"kind": "tei", "slug": "maximus-dissertationes", "work": "Maximus Tyrius, Philosophumena, ed. H. Hobein (Leipzig, 1910), First1KGreek tlg0563.tlg001 1st1K-grc1",
    "url": f"https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/{FC}/data/tlg0563/tlg001/tlg0563.tlg001.1st1K-grc1.xml",
    "path": "first1k/tlg0563.tlg001.1st1K-grc1.xml", "source": "OpenGreekAndLatin/First1KGreek", "repository": "https://github.com/OpenGreekAndLatin/First1KGreek",
    "commit": FC, "file": "data/tlg0563/tlg001/tlg0563.tlg001.1st1K-grc1.xml", "class": F}],
  "The forty-one discourses whole.",
  "Or. 18.9, Sappho's art of love set beside Socrates's, her rivals beside his (Gorgo and Andromeda against Prodicus and Gorgias): the writer "
  "read as the lover and the lover read through the philosopher."),
 ("racine-phedre", "38", "J. Racine, Phèdre (1677), in the Didot edition (Paris, 1854), Wikisource (fr)", "fra",
  "Public domain everywhere (1677; Racine died 1699). The Wikisource page's text under CC BY-SA 4.0 for the site's contributions.",
  [{"kind": "ws", "slug": f"phedre-acte-{i.lower()}", "work": f"Racine, Phèdre, Didot 1854, Acte {i}, fr.wikisource", "lang": "fr",
    "title": f"Phèdre (Racine), Didot, 1854/Acte {i}", "class": F} for i in ("I", "II", "III", "IV", "V")],
  "The five acts whole, in the Didot edition of 1854 as Wikisource gives it.",
  "Phèdre's avowal (I.3), the symptoms of fr. 31 given to a stepmother's forbidden love, the case of the Erasistratus story turned round, "
  "in the same years as Boileau's Traité (36/02)."),
 ("smollett-roderick-random", "39", "T. Smollett, The Adventures of Roderick Random (1748), the Project Gutenberg text", "eng",
  "Public domain everywhere (1748; Smollett died 1771); the Gutenberg file under its licence.",
  [{"kind": "text", "slug": "roderick-random", "work": "Smollett, The Adventures of Roderick Random, Project Gutenberg #4085", "url": "https://www.gutenberg.org/cache/epub/4085/pg4085.txt",
    "path": "gutenberg/pg4085.txt", "source": "Project Gutenberg #4085", "licence": "The Project Gutenberg License (header and footer kept as served)", "class": F}],
  "The novel whole.",
  "The fr. 31 Smollett gives his hero, with a final stanza of its own ('Unheard I mourn, unknown I sigh'), the added continuation Closing the "
  "Fragment v7 §6.4 cites from Wharton, here in its novel."),
 ("wikipedia-sappho-31", "40", "Wikipedia, 'Sappho 31', revision 1375954224 of 2026-09-21", "eng",
  "Wikipedia text under CC BY-SA 4.0, as the site states.",
  [{"kind": "text", "slug": "wikipedia-sappho-31", "work": "Wikipedia, 'Sappho 31', revision 1375954224 of 2026-09-21, the wikitext as served",
    "url": "https://en.wikipedia.org/w/index.php?title=Sappho_31&action=raw&oldid=1375954224", "path": "wikipedia/sappho-31-1375954224.wiki",
    "source": "Wikipedia (en)", "licence": "CC BY-SA 4.0", "class": F}],
  "The article at one revision.",
  "The encyclopedia's account of the poem, its interpretation and its reception, at the revision current when the reception study opened: the "
  "readings it reports for the speaker's state, the jealousy reading among them, as a composition layer is likely to meet them."),
]
for corpus, n, title, lang, lic, items, scope, why in SEATS:
    spec = {"corpus": corpus, "seat": f"EA-CORPORA-36/{n}", "title": title, "language": lang, "fetched": "2026-11-07", "spine": "EA-CORPORA-36",
            "ruling": RULING, "seating": SEATING, "license": {"payload": lic, "record": "CC-BY-4.0 applies to this seat record only."},
            "normalization": NORM, "items": items, "loci": [], "scope": scope, "why_seated": why, "research": RESEARCH}
    f = H / f"spec36-{corpus}.json"
    if f.exists():
        spec["loci"] = json.loads(f.read_text(encoding="utf-8")).get("loci", [])
    f.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", corpus)
