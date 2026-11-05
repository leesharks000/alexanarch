#!/usr/bin/env python3
"""Writes the EA-CORPORA-34 specs (spec34-<corpus>.json). Session tool. The sources of Secondary Source, the reception study of
how the Apocalypse came to be received as derivative, secondary and marginal (design v0.3 §5), seated before drafting."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
F1K = "ed91552c52530c8f5a3ddf2dd767e899372a804c"   # OpenGreekAndLatin/First1KGreek, HEAD on 2026-11-05 (git ls-remote)
RULING = ("Lee Sharks, 2026-11-05 09:03 EST: \"also - lets gather up and seat the sources we'll need for this one prior to writing. still under rebekah "
          "cranes for the ea-corpora, and with reference to the research occasion\".")
SEATING = "EA-CORPORA-34, the thirty-fourth seating: Secondary Source — the reception of the Apocalypse, from the fathers to the critics, 2026-11-05"
REC = "CC-BY-4.0 applies to this seat record only."
NORM_TEI = ("Originals as fetched under original/, pinned to a commit of the repository named in origin.items. text/<slug>.txt is the TEI reduced to plain "
            "text by seat.py (rebuild/corpora/ea-corpora-27), notes and apparatus dropped, divisions kept. No text was corrected by hand.")
NORM_IA = ("The Internet Archive's own text layer (_djvu.txt) as served, under original/<identifier>/, copied to text/<slug>.ocr.txt with line endings "
           "normalized. The PDF of each item is held by reference at its Archive URL and not copied. No text was corrected by hand; the loci keep the "
           "OCR's readings.")
RESEARCH = lambda section: {"study": "Secondary Source: the reception of the Apocalypse as derivative, secondary and marginal",
    "design": "drafts/SECONDARY-SOURCE-design-2026-11-05.md (v0.3, sha256 638a5e3c…)", "draft": "not yet drafted",
    "locus_table": "the locus table of design v0.3 §4.1", "owed_at": "the debts of design v0.3 §5, seated before drafting at the operator's word of 2026-11-05", "for": section}
def tei(f, slug, work):
    return {"kind": "tei", "slug": slug, "url": f"https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/{F1K}/{f}", "path": "first1k/" + f.split("/")[-1],
            "source": "Open Greek and Latin, First1KGreek", "repository": "https://github.com/OpenGreekAndLatin/First1KGreek", "commit": F1K, "file": f, "work": work}
def ia(ident, djvu, slug, work, cls=None):
    d = {"kind": "ia", "slug": slug, "work": work, "identifier": ident, "files": [djvu]}
    if cls: d["class"] = cls
    return d
def lo(label, text, find, note=None):
    d = {"label": label, "text": text, "find": find}
    if note: d["note"] = note
    return d
LIC_TEI = "The TEI is Open Greek and Latin's (First1KGreek), CC BY-SA 4.0, redistributed under the same licence and attributed."
COMMON = lambda: {"language": None, "fetched": "2026-11-05", "spine": "EA-CORPORA-34", "ruling": RULING, "seating": SEATING}
specs = []
def add(corpus, n, title, lang, lic, norm, items, loci, scope, why, section, xref=None):
    s = {"corpus": corpus, "seat": f"EA-CORPORA-34/{n:02d}", "title": title} | COMMON()
    s.update({"language": lang, "license": {"payload": lic, "record": REC}, "normalization": norm, "items": items, "loci": loci,
              "scope": scope, "why_seated": why, "research": RESEARCH(section)})
    if xref: s["cross_references"] = xref
    specs.append(s)

add("eusebius-historia-ecclesiastica", 1, "Eusebius, Historia ecclesiastica, in Greek, ed. W. Dindorf (Leipzig: Teubner, 1871)", "grc",
    "Eusebius is public domain; Dindorf's edition (1871; Dindorf died 1883) is public domain everywhere. " + LIC_TEI, NORM_TEI,
    [tei("data/tlg2018/tlg002/tlg2018.tlg002.1st1K-grc2.xml", "historia-ecclesiastica", "Eusebius, Historia ecclesiastica I–X, ed. Dindorf (1871) — First1KGreek tlg2018.tlg002.1st1K-grc2")],
    [lo("HE 5.8.6 (Irenaeus, Adv. haer. 5.30.3, in Greek): seen not long ago, near the end of Domitian's reign", "text/historia-ecclesiastica.txt", "οὐδὲ γὰρ πρὸ πολλοῦ χρόνου ἑωράθη"),
     lo("HE 3.25.4: the Apocalypse of John, 'if it seem right', which some reject and others count among the acknowledged", "text/historia-ecclesiastica.txt", "ἡ Ἰωάννου Ἀποκάλυψις, εἰ φανείη"),
     lo("HE 3.28.2: Gaius on Cerinthus and revelations 'as if written by a great apostle'", "text/historia-ecclesiastica.txt", "ὁ δι᾿ ἀποκαλύψεων ὡς ὑπὸ ἀποστόλου μεγάλου"),
     lo("HE 7.24.1: Dionysius against Nepos, bishop in Egypt", "text/historia-ecclesiastica.txt", "Νέπως ἦν, ἐπίσκοπος τῶν κατ")],
    "The ten books entire. Held for the ledger of the books (3.25), Gaius (3.28), Papias's two Johns (3.39), the Irenaeus sentence in Greek (3.18; 5.8), and Dionysius of Alexandria on Nepos and the Apocalypse (7.24–25).",
    "The record through which the date (Irenaeus), the second John (Papias), the dispute over author and standing (Gaius, Dionysius) and the book's double entry in the ledger (3.25) reach every later stratum: strata 3.2–3.4 of Secondary Source.",
    "design v0.3 §3.2–3.4; the Irenaeus sentence read in #1735 §II.1", ["gnt-nestle1904 (01/04, Revelation)"])

add("irenaeus-adversus-haereses", 2, "Irenaeus, Adversus haereses, ed. W. W. Harvey (Cambridge, 1857): the Greek of the First1KGreek TEI and both volumes of the Latin", "grc+lat",
    "Irenaeus is public domain; Harvey's edition (1857; Harvey died 1883) is public domain everywhere. " + LIC_TEI + " The Archive's scans of the two volumes are public domain.", NORM_TEI + " " + NORM_IA,
    [tei("data/tlg1447/tlg001/tlg1447.tlg001.1st1K-grc1.xml", "adversus-haereses-graece", "Irenaeus, Adversus haereses, the Greek, ed. Harvey (1857) — First1KGreek tlg1447.tlg001.1st1K-grc1"),
     ia("sanctiirenaeiep01harvgoog", "sanctiirenaeiep01harvgoog_djvu.txt", "harvey-i", "Harvey, Sancti Irenaei libros quinque adversus haereses, vol. I (1857), the Archive's text layer"),
     ia("sanctiirenaeiep00harvgoog", "sanctiirenaeiep00harvgoog_djvu.txt", "harvey-ii", "Harvey, Sancti Irenaei libros quinque adversus haereses, vol. II (1857), the Archive's text layer: books III–V")],
    [lo("Adv. haer. 5.30.3, the Latin: seen near the end of Domitian's reign", "text/harvey-ii.ocr.txt", "ad finem Domitiani imperii")],
    "The five books, Greek where it survives and the Latin of both volumes, held for 4.20.11 and 5.30.3.",
    "The single external anchor of the Domitianic date (5.30.3), read in its Latin and in the Greek Eusebius transmits: stratum 3.2.",
    "design v0.3 §3.2; #1735 §II.1", ["eusebius-historia-ecclesiastica (34/01, HE 5.8)"])

add("justin-dialogus", 3, "Justin Martyr, Dialogus cum Tryphone, in Greek, ed. G. Archambault (Paris, 1909)", "grc",
    "Justin is public domain; Archambault's edition (Paris: Picard, 1909) is public domain in the United States. " + LIC_TEI, NORM_TEI,
    [tei("data/tlg0645/tlg003/tlg0645.tlg003.perseus-grc2.xml", "dialogus", "Justin, Dialogus cum Tryphone, ed. Archambault (1909) — First1KGreek tlg0645.tlg003.perseus-grc2")],
    [lo("Dial. 81.4: John, one of the apostles of Christ, prophesied in a revelation made to him", "text/dialogus.txt", "ἐν ἀποκαλύψει γενομένῃ αὐτῷ χίλια ἔτη ποιήσειν")],
    "The Dialogue entire, held for 81.4.", "The earliest named witness to the book's author and its reading of the thousand years: stratum 3.2.", "design v0.3 §3.2")

add("muratorian-fragment-tregelles", 4, "Canon Muratorianus: the earliest catalogue of the books of the New Testament, ed. S. P. Tregelles (Oxford, 1867)", "lat+eng",
    "The fragment is public domain; Tregelles's edition (1867; Tregelles died 1875) is public domain everywhere.", NORM_IA,
    [ia("canonmuratorianu00treg", "canonmuratorianu00treg_djvu.txt", "tregelles-1867", "Tregelles, Canon Muratorianus (1867), with the facsimile, the Archive's text layer")],
    [lo("lines 47–50: Paul, following the order of his predecessor John, writes by name to seven churches", "text/tregelles-1867.ocr.txt", "sequens prodecessoris sui Iohannis ordine", "the OCR reads 'ordine' where Tregelles prints 'ordinē'; read in the scan before quotation")],
    "Tregelles's edition whole: the transcription, the facsimile and his commentary.",
    "The fragment's construal of Paul's seven churches through John's (#1735 §IV.3), seated in a public edition so that Secondary Source can read it in seat and trace what later strata did with it: strata 3.2 and 3.4.",
    "design v0.3 §1.3, §3.2; #1735 §IV.3")

add("epiphanius-panarion", 5, "Epiphanius, Panarion, in Greek, ed. K. Holl (GCS, Leipzig, 1915–1933)", "grc",
    "Epiphanius is public domain; Holl's edition (1915–1933; Holl died 1926) is public domain everywhere. " + LIC_TEI, NORM_TEI,
    [tei("data/tlg2021/tlg002/tlg2021.tlg002.1st1K-grc1.xml", "panarion", "Epiphanius, Panarion, ed. Holl — First1KGreek tlg2021.tlg002.1st1K-grc1")],
    [lo("Panarion, the table of heresies: the Alogi, who receive neither the Gospel nor the Apocalypse of John", "text/panarion.txt", "οἱ τὸ εὐαγγέλιον καὶ τὴν ἀποκάλυψιν Ἰωάννου μὴ δεχόμενοι"),
     lo("Panarion 51.3: the heresy that rejects the books of John", "text/panarion.txt", "ἀποβάλλουσαν Ἰωάννου τὰς βίβλους")],
    "The Panarion entire, held for heresy 51, the Alogi.", "The dispute in which rejecting the book's reading meant rejecting its author: stratum 3.3.", "design v0.3 §3.3")

add("westcott-canon-1896", 6, "B. F. Westcott, A General Survey of the History of the Canon of the New Testament, 7th ed. (London: Macmillan, 1896)", "eng+grc+lat",
    "Westcott (died 1901) is public domain everywhere.", NORM_IA,
    [ia("cu31924029301582", "cu31924029301582_djvu.txt", "general-survey", "Westcott, General Survey of the History of the Canon (1896), Cornell copy, the Archive's text layer")],
    [lo("the Laodicene canon 60: how many books must be read", "text/general-survey.ocr.txt", "How many books must be read"),
     lo("Appendix D: the chief catalogues of the books of the Bible during the first eight centuries", "text/general-survey.ocr.txt", "THE CHIEF CATALOGUES OF THE BOOKS OF THE BIBLE DURING THE FIRST EIGHT CENTURIES")],
    "The whole survey, with its appendix of the catalogues in their original languages, held for the canon lists of stratum 3.4: Laodicea 60, the Apostolic Canons 85, Cyril of Jerusalem, Gregory of Nazianzus, Amphilochius, Athanasius's Festal Letter 39, Hippo and Carthage.",
    "One public, pre-1929 edition that sets the fourth-century catalogues side by side in their languages; each list is read there and cited with its own reference. The Greek of Cyril's Catecheses and of the poems of Gregory and Amphilochius is not otherwise held in a public TEI this session could reach.",
    "design v0.3 §3.4")

add("collectio-hispana-1808", 7, "Collectio canonum Ecclesiae Hispanae (Madrid, 1808), with the Fourth Council of Toledo (633)", "lat",
    "The councils are public domain; the Madrid edition of 1808 is public domain everywhere.", NORM_IA,
    [ia("A28009301", "A28009301_djvu.txt", "collectio-hispana", "Collectio canonum Ecclesiae Hispanae (Matriti, 1808), the Archive's text layer")],
    [lo("the index: on receiving the book of the Apocalypse in all churches, Toledo IV, canon 17", "text/collectio-hispana.ocr.txt", "De Apocalypsis libro in omnibus recipiendo"),
     lo("Toledo IV, canon 17: the authority of many councils and the decrees of the Roman bishops ascribe the Apocalypse to John the evangelist", "text/collectio-hispana.ocr.txt", "Apocalypsis librum multorum conciliorum auctoritas et synodica sanctorum praesulum Romanorum decreta Joannis evangelistae esse praescribunt")],
    "The collection whole, held for the Fourth Council of Toledo, canon 17 (the Apocalypse to be read from Easter to Pentecost).",
    "The Western counter-witness to the Byzantine lectionary's silence: stratum 3.5 and the lectionary paragraph of design v0.3.", "design v0.3 §3.5")

add("september-testament-1522", 8, "Das Newe Testament Deutzsch (Wittenberg: Melchior Lotter, September 1522), Luther's September Testament, in the facsimile of 1883", "deu",
    "Luther's text is public domain; the facsimile (1883) is public domain everywhere.",
    NORM_IA + " The Archive's text layer of this black-letter facsimile is largely unreadable; the scan is the witness, and the preface to the Apocalypse and the table of books are read from the pages.",
    [ia("DasNeweTestamentDeutzsch1522", "DasNeweTestamentDeutzsch1522SeptemberbibelErstenAusgabeNachbildung1883Small_djvu.txt", "september-testament", "Das Newe Testament Deutzsch, 1522, facsimile of 1883, the Archive's text layer (the scan is the witness)")],
    [], "The facsimile whole, held for the table of books (Hebrews, James, Jude and the Apocalypse set apart and unnumbered) and the 1522 preface to the Apocalypse.",
    "Standing made into typography: stratum 3.6. The preface's wording enters the study only when read from the pages of this scan.", "design v0.3 §3.6")

add("erasmus-annotationes-1535", 9, "Erasmus, In Novum Testamentum Annotationes (Basel: Froben, 1535)", "lat",
    "Erasmus is public domain; the Basel printing of 1535 is public domain everywhere.", NORM_IA,
    [ia("ARes162052", "ARes162052_djvu.txt", "annotationes-1535", "Erasmus, In Novum Testamentum Annotationes (Basel, 1535), the Archive's text layer")],
    [lo("the annotations on the Apocalypse", "text/annotationes-1535.ocr.txt", "IN APOCALYPSIN")],
    "The Annotationes whole, held for the notes on the Apocalypse and on its authorship.", "The printed Bible's first critical doubt of the author: stratum 3.6.", "design v0.3 §3.6")

C10 = "the critics of the Apocalypse, 1886–1920"
add("revelation-criticism-1886-1920", 10, "The critics of the Apocalypse, 1886–1920: Vischer, Spitta, Gunkel, Bousset (1896 and 1913) and Charles", "deu+eng",
    "All public domain everywhere: Vischer (1886), Spitta (1889; died 1924), Gunkel (1895; died 1932), Bousset (1896, 1913; died 1920), Charles (1920; died 1931).", NORM_IA,
    [ia("dieoffenbarungj00viscgoog", "dieoffenbarungj00viscgoog_djvu.txt", "vischer-1886", "E. Vischer, Die Offenbarung Johannis: eine jüdische Apokalypse in christlicher Bearbeitung, with an afterword by A. Harnack (TU 2.3, Leipzig, 1886)", C10),
     ia("11604718bsb", "11604718bsb_djvu.txt", "spitta-1889", "F. Spitta, Die Offenbarung des Johannes untersucht (Halle, 1889)", C10),
     ia("schpfungundcha00gunk", "schpfungundcha00gunk_djvu.txt", "gunkel-1895", "H. Gunkel, Schöpfung und Chaos in Urzeit und Endzeit (Göttingen, 1895)", C10),
     ia("dieoffenbarungjo0000wilh_n4d2", "dieoffenbarungjo0000wilh_n4d2_djvu.txt", "bousset-1896", "W. Bousset, Die Offenbarung Johannis, Meyer's Kommentar XVI, 5th ed. (Göttingen, 1896)", C10),
     ia("kyrioschristosge00bous", "kyrioschristosge00bous_djvu.txt", "bousset-kyrios-1913", "W. Bousset, Kyrios Christos: Geschichte des Christusglaubens von den Anfängen des Christentums bis Irenaeus (Göttingen, 1913)", C10),
     ia("criticalexegetic661char", "criticalexegetic661char_djvu.txt", "charles-1920-i", "R. H. Charles, A Critical and Exegetical Commentary on the Revelation of St. John, ICC, vol. I (Edinburgh, 1920)", C10),
     ia("criticalexegetic02char", "criticalexegetic02char_djvu.txt", "charles-1920-ii", "R. H. Charles, A Critical and Exegetical Commentary on the Revelation of St. John, ICC, vol. II (Edinburgh, 1920)", C10)],
    [lo("Vischer's title: a Jewish apocalypse in Christian revision", "text/vischer-1886.ocr.txt", "EINE JÜDISCHE APOKALYPSE IN CHRISTLICHER BEARBEITUNG"),
     lo("Spitta's title page", "text/spitta-1889.ocr.txt", "UNTERSUCHT VON FRIEDRICH SPITTA"),
     lo("Bousset 1896, the title page of the fifth edition", "text/bousset-1896.ocr.txt", "Neu bearbeitet von Lic. theol. Wilhelm Bousset"),
     lo("Charles I, the contents: the Domitianic date", "text/charles-1920-i.ocr.txt", "The Domitianic date"),
     lo("Charles II on 19:13: the name the Word of God 'cannot be explained away'", "text/charles-1920-ii.ocr.txt", "cannot be explained away")],
    "Seven volumes whole: the source-critical (Vischer, Spitta), the history-of-religions (Gunkel, Bousset 1896), the developmental Christology (Kyrios Christos, 1913) and the critical commentary (Charles).",
    "Derivation made a method, for the text and for the figure: stratum 3.7, and the count of the figure's derivation (design v0.3 §2.4).", "design v0.3 §2.4, §3.7")

add("gregory-textkritik-1900", 11, "C. R. Gregory, Textkritik des Neuen Testamentes, vol. I (Leipzig: Hinrichs, 1900)", "deu",
    "Gregory (died 1917) is public domain everywhere.", NORM_IA,
    [ia("textkritikdesneu0001greg", "textkritikdesneu0001greg_djvu.txt", "textkritik-i", "Gregory, Textkritik des Neuen Testamentes I (1900), the Archive's text layer: the Greek manuscripts and the lectionaries")],
    [lo("on the prefaces to the Apocalypse in the manuscripts", "text/textkritik-i.ocr.txt", "Zu der Apokalypse begegnet selten ein anderes Vorwort")],
    "The first volume whole, held for the manuscripts that carry the Apocalypse and for the lectionaries.", "The material order: the book's transmission and its absence from the lectionary: stratum 3.5.", "design v0.3 §3.5")

for s in specs:
    (H / f"spec34-{s['corpus']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", s["seat"], s["corpus"])
