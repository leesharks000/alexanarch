#!/usr/bin/env python3
"""Writes the EA-CORPORA-31 specs (spec31-<corpus>.json). Session tool."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
SCR = "/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/ea30raw"
P = "341e309c821d5eca8c976bebca77c28b10bad58f"   # PerseusDL/canonical-greekLit, the commit the Strabo and Diogenes seats pin
F = "ed91552c52530c8f5a3ddf2dd767e899372a804c"   # OpenGreekAndLatin/First1KGreek, the commit 30/11 pins
RULING = "Lee Sharks, 2026-11-01, of the texts named in §5 of the design Legitimately Many (drafts/LEGITIMATELY-MANY-design-2026-11-01.md): \"lets gather and seat those. with an ea-corpora\"."
SEATING = "EA-CORPORA-31, the thirty-first seating: the transmission of the Peripatetic corpus, 2026-11-01"
NORM_TEI = "Originals as fetched under original/, pinned to a commit of the repository named in origin.items. text/<slug>.txt is the TEI reduced to plain text by seat.py (rebuild/corpora/ea-corpora-27), notes and apparatus dropped, divisions kept. No text was corrected by hand."
NORM_OCR = "The OCR is kept as made, with line endings normalized. No text was corrected by hand; the loci keep the OCR's readings and say where those differ from the printed page."
ENGINE = {"engine": "Tesseract 5.3.4", "models": "tessdata_best grc+lat (raw.githubusercontent.com/tesseract-ocr/tessdata_best, main)",
          "sha256": {"grc.traineddata": "dfc9bda286cd9d8755b1832e5731a5425d1cf0803393a5fa6dee078466178cf1",
                     "lat.traineddata": "60054dd32ac03ebd9b4f87d0665bd491a7ffe0d3ee99ceb91aefaf348b65e94f"},
          "command": "tesseract nNN.jpg nNN -l grc+lat", "run": "2026-11-01, in session"}
REC = "CC-BY-4.0 applies to this seat record only."
ALL = "Seated as the debts of the study Legitimately Many (design §5): the texts in which the tradition fixed one author per name and recorded how it did so."


def tei(repo, commit, g, w, ed, slug, work, cls=None):
    base = "PerseusDL/canonical-greekLit" if repo == "P" else "OpenGreekAndLatin/First1KGreek"
    f = f"data/{g}/{w}/{g}.{w}.{ed}.xml"
    d = {"kind": "tei", "slug": slug, "url": f"https://raw.githubusercontent.com/{base}/{commit}/{f}", "path": f"{'perseus' if repo == 'P' else 'first1k'}/{g}.{w}.{ed}.xml",
         "source": "Perseus Digital Library, canonical-greekLit" if repo == "P" else "Open Greek and Latin, First1KGreek",
         "repository": f"https://github.com/{base}", "commit": commit, "file": f, "work": work}
    if cls:
        d["class"] = cls
    return d


specs = []

specs.append({
 "corpus": "athenaeus", "seat": "EA-CORPORA-31/01",
 "title": "Athenaeus, Deipnosophistae, in Kaibel's Greek (Teubner, 1887–1892)",
 "language": "grc", "fetched": "2026-11-01",
 "license": {"payload": "Athenaeus (fl. c. 200 CE) is public domain. Kaibel's edition (Leipzig: Teubner, 1887–1892) is public domain in the United States (published before 1931); Kaibel died in 1901. The TEI is the Perseus Digital Library's, CC BY-SA 4.0, redistributed under the same licence and attributed to Perseus.", "record": REC},
 "normalization": NORM_TEI,
 "units": "one text file for the fifteen books",
 "items": [tei("P", P, "tlg0008", "tlg001", "perseus-grc3", "deipnosophistae-kaibel",
               "Athenaeus, Δειπνοσοφισταί, books I–XV, ed. G. Kaibel, Athenaei Naucratitae Dipnosophistarum libri XV (Leipzig: Teubner, 1887–1892) — Perseus TEI tlg0008.tlg001.perseus-grc3")],
 "loci": [
  {"label": "I.3a–b, Neleus and the sale to Ptolemy Philadelphus", "text": "text/deipnosophistae-kaibel.txt", "find": "καὶ τὸν τὰ τούτων διατηρήσαντα βιβλία Νηλέα· παρ’ οὗ πάντα, φησί, πριάμενος ὁ ἡμεδαπὸς βασιλεὺς Πτολεμαῖος"},
  {"label": "I.3b, the books taken to Alexandria with those from Athens and Rhodes", "text": "text/deipnosophistae-kaibel.txt", "find": "μετὰ τῶν Ἀθήνηθεν καὶ τῶν ἀπὸ Ῥόδου εἰς τὴν καλὴν Ἀλεξάνδρειαν μετήγαγε"},
  {"label": "V.214d, Apellicon of Teos and the library of Aristotle", "text": "text/deipnosophistae-kaibel.txt", "find": "καὶ τὴν Ἀριστοτέλους βιβλιοθήκην καὶ"}],
 "scope": "The Deipnosophistae entire in Kaibel's text. Athenaeus I.3a–b gives the second custody of the Peripatetic books: Neleus sold them to Ptolemy Philadelphus, who took them to Alexandria. Strabo XIII.1.54 and Plutarch, Sulla 26 (seated at EA-CORPORA-17 and in the Plutarch seat) give the first, through Scepsis, Apellicon and Sulla. Gulick's Loeb text (Perseus perseus-grc4) is not seated: Kaibel's is the earlier critical text.",
 "why_seated": "The two custody stories cannot both be complete. Athenaeus's sale to Ptolemy sits beside the narrative of the cellar at Scepsis, and the study reads where each one puts the books and under whose name.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING,
 "cross_references": ["strabo (XIII.1.54)", "plutarch (Sulla 26)", "diogenes-laertius (V, the will of Theophrastus)"]})

specs.append({
 "corpus": "galen", "seat": "EA-CORPORA-31/02",
 "title": "Galen, In Hippocratis De natura hominis commentaria, in Kühn's Greek (vol. XV, 1828)",
 "language": "grc", "fetched": "2026-11-01",
 "license": {"payload": "Galen (d. c. 216 CE) is public domain. Kühn's Claudii Galeni opera omnia (Leipzig: Knobloch, 1821–1833) is public domain everywhere. The TEI is First1KGreek's, CC BY-SA 4.0, redistributed under the same licence and attributed to Open Greek and Latin.", "record": REC},
 "normalization": NORM_TEI,
 "items": [tei("F", F, "tlg0057", "tlg085", "1st1K-grc1", "in-hipp-nat-hom-kuehn",
               "Galen, Εἰς τὸ Ἱπποκράτους περὶ φύσεως ἀνθρώπου ὑπόμνημα (In Hippocratis De natura hominis), ed. C. G. Kühn, Claudii Galeni opera omnia XV (Leipzig: Knobloch, 1828) — First1KGreek TEI tlg0057.tlg085.1st1K-grc1")],
 "loci": [
  {"label": "the Attalid and Ptolemaic kings competing to acquire books", "text": "text/in-hipp-nat-hom-kuehn.txt", "find": "ἐν γὰρ τῷ κατὰ τοὺς Ἀτταλικούς τε καὶ Πτολεμαϊκοὺς βασιλέας χρόνῳ πρὸς ἀλλήλους ἀντιφιλοτιμουμένους περὶ κτήσεως βιβλίων"},
  {"label": "forgery of titles and recensions for money", "text": "text/in-hipp-nat-hom-kuehn.txt", "find": "ἡ περὶ τὰς ἐπιγραφάς τε καὶ διασκευὰς αὐτῶν ἤρξατο γίγνεσθαι ῥᾳδιουργία τοῖς ἕνεκα τοῦ λαβεῖν ἀργύριον ἀναφέρουσιν ὡς τοὺς βασιλεῖς ἀνδρῶν ἐνδόξων συγγράμματα"}],
 "scope": "The commentary on De natura hominis entire. Its preface on the joining of two short books under one title (De natura hominis and Polybus's De salubri victu) states the mechanism: in the time of the competing Attalid and Ptolemaic kings, titles and recensions were falsified by those who brought books to the kings as the writings of famous men, to receive money. Galen's other statements on Hippocratic forgery (In Hipp. Epid. and elsewhere) are not seated here.",
 "why_seated": "Galen names an acquisition economy that paid by the name and the falsifying of titles it produced. The study reads it for incentive and function: when the slot carries a price, a title is filed under the name that sells.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING})

specs.append({
 "corpus": "porphyry", "seat": "EA-CORPORA-31/03",
 "title": "Porphyry, Life of Plotinus, in Volkmann's Greek (Teubner, 1883) — the Internet Archive's OCR",
 "language": "grc", "fetched": "2026-11-01",
 "license": {"payload": "Porphyry (d. c. 305 CE) is public domain. Volkmann's Plotini Enneades I (Leipzig: Teubner, 1883) is public domain; the Archive marks the item Public Domain Mark 1.0. The OCR layer is the Archive's.", "record": REC},
 "normalization": "The Archive's OCR text layer (_djvu.txt) of the whole volume, line endings normalized; the scan (138 MB) is held by reference with the Archive's md5. " + NORM_OCR,
 "items": [{"kind": "ia_ref", "slug": "volkmann-1883-vol1", "identifier": "volkmann-enneades-gr-v.-1-1883",
            "ocr": "Volkmann - Enneades, [gr], v.1, 1883_djvu.txt", "scan": "Volkmann - Enneades, [gr], v.1, 1883.pdf",
            "work": "Plotini Enneades, praemisso Porphyrii De vita Plotini deque ordine librorum eius libello, ed. R. Volkmann, vol. I (Leipzig: Teubner, 1883) — Internet Archive volkmann-enneades-gr-v.-1-1883, the OCR layer of the volume; Porphyry's Life of Plotinus opens it"}],
 "loci": [
  {"label": "Vita Plotini 1, the opening", "text": "text/volkmann-1883-vol1.ocr.txt", "find": "Πλωτῖνος ὁ x«9\" ἡμᾶς ysyovOg φιλόσοφος", "note": "the OCR reads καθ' ἡμᾶς γεγονὼς as x«9\" ἡμᾶς ysyovOg; the locus keeps the OCR's reading"},
  {"label": "Vita Plotini 24, the books left 'in confusion' by date of issue", "text": "text/volkmann-1883-vol1.ocr.txt", "find": "οὐ κατὰ χρόνους ἐᾶσαι φύρδην ἐκδεδομένα"},
  {"label": "Vita Plotini 24, Andronicus's arrangement of Aristotle and Theophrastus by subject", "text": "text/volkmann-1883-vol1.ocr.txt", "find": "ναῖον καὶ ᾿Ανδρόνικαν τὸν Περιπατητικόν, ὧν ὁ", "note": "the page reads Ἀνδρόνικον; the OCR reads ᾿Ανδρόνικαν"},
  {"label": "Vita Plotini 24, into treatises, gathering the proper subjects together", "text": "text/volkmann-1883-vol1.ocr.txt", "find": "εἰς ταὐτὸν συναγαγών"}],
 "scope": "The volume's OCR layer entire: Porphyry's Life of Plotinus and On the Order of his Books, then Enneads I–III in Volkmann's text. The Enneads are already seated from First1KGreek (plotinus, EA-CORPORA-04/02); this seat is held for the Life, which First1KGreek does not carry. At chapter 24 Porphyry takes as his model Andronicus the Peripatetic, who divided the works of Aristotle and Theophrastus into treatises, bringing the proper subjects together, ὁ δὲ τὰ Ἀριστοτέλους καὶ Θεοφράστου εἰς πραγματείας διεῖλε τὰς οἰκείας ὑποθέσεις εἰς ταὐτὸν συναγαγών (the OCR reads ᾿Δριστοτέλους and πραψματείας).",
 "why_seated": "Porphyry is the witness for Andronicus's edition as an operation: two names joined by καί, the works redivided by subject and the chronological order of issue undone. He says he did the same to his own teacher's books.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING, "cross_references": ["plotinus (EA-CORPORA-04/02)"]})

specs.append({
 "corpus": "aristotle-commentators", "seat": "EA-CORPORA-31/04",
 "title": "The Prolegomena to Aristotle in the Greek commentators: Ammonius, Simplicius, Philoponus, Olympiodorus, Elias and David (Commentaria in Aristotelem Graeca, 1887–1907)",
 "language": "grc", "fetched": "2026-11-01",
 "license": {"payload": "The commentators (fifth to sixth centuries CE) are public domain. The Commentaria in Aristotelem Graeca (Berlin: Reimer, 1882–1909) are public domain in the United States (published before 1931); the editors are named per item. The TEI is First1KGreek's, CC BY-SA 4.0, redistributed under the same licence and attributed to Open Greek and Latin.", "record": REC},
 "normalization": NORM_TEI,
 "units": "one text file per commentary; each carries its commentator as class",
 "classes": ["Ammonius", "Simplicius", "Philoponus", "Olympiodorus", "Elias", "David"],
 "items": [
  tei("F", F, "tlg4016", "tlg002", "1st1K-grc1", "ammonius-in-cat", "Ammonius, In Aristotelis Categorias commentarius, ed. A. Busse, CAG IV.4 (Berlin: Reimer, 1895) — First1KGreek TEI tlg4016.tlg002.1st1K-grc1", "Ammonius"),
  tei("F", F, "tlg4013", "tlg003", "1st1K-grc1", "simplicius-in-cat", "Simplicius, In Aristotelis Categorias commentarium, ed. K. Kalbfleisch, CAG VIII (Berlin: Reimer, 1907) — First1KGreek TEI tlg4013.tlg003.1st1K-grc1", "Simplicius"),
  tei("F", F, "tlg4015", "tlg001", "1st1K-grc1", "philoponus-in-cat", "John Philoponus, In Aristotelis Categorias commentarium, ed. A. Busse, CAG XIII.1 (Berlin: Reimer, 1898) — First1KGreek TEI tlg4015.tlg001.1st1K-grc1", "Philoponus"),
  tei("F", F, "tlg4019", "tlg001", "1st1K-grc1", "olympiodorus-prolegomena", "Olympiodorus, Prolegomena, ed. A. Busse, CAG XII.1 (Berlin: Reimer, 1902) — First1KGreek TEI tlg4019.tlg001.1st1K-grc1", "Olympiodorus"),
  tei("F", F, "tlg4019", "tlg002", "1st1K-grc1", "olympiodorus-in-cat", "Olympiodorus, In Aristotelis Categorias commentarium, ed. A. Busse, CAG XII.1 (Berlin: Reimer, 1902) — First1KGreek TEI tlg4019.tlg002.1st1K-grc1", "Olympiodorus"),
  tei("F", F, "tlg4020", "tlg002", "1st1K-grc1", "elias-in-cat", "Elias, In Aristotelis Categorias commentarium, ed. A. Busse, CAG XVIII.1 (Berlin: Reimer, 1900) — First1KGreek TEI tlg4020.tlg002.1st1K-grc1", "Elias"),
  tei("F", F, "tlg4021", "tlg001", "1st1K-grc1", "david-prolegomena", "David, Prolegomena philosophiae, ed. A. Busse, CAG XVIII.2 (Berlin: Reimer, 1904) — First1KGreek TEI tlg4021.tlg001.1st1K-grc1", "David")],
 "loci": [
  {"label": "Olympiodorus, Prolegomena: the question of the genuine", "text": "text/olympiodorus-prolegomena.txt", "find": "πρῶτον μὲν διὰ πόσους τρόπους ἐνοθεύοντο τὰ βιβλία καὶ ποῖά εἰσιν κριτήρια τὰ δυνάμενα διαχωρίζειν τὰ γνήσια ἀπὸ τῶν νόθων"},
  {"label": "Olympiodorus, Prolegomena: three ways books were made spurious, the kings' ambition, the pupils' goodwill, homonymy", "text": "text/olympiodorus-prolegomena.txt", "find": "ἢ διὰ φιλοτιμίαν τῶν βασιλέων ἢ δι’ εὔνοιαν τῶν μαθητῶν ἢ διὰ ὁμωνυμίαν"},
  {"label": "Ammonius, In Cat.: the fifth head, whether the book is spurious or genuine", "text": "text/ammonius-in-cat.txt", "find": "πέμπτον εἰ νόθον ἢ γνήσιον τοῦ φιλοσόφου τὸ βιβλίον"},
  {"label": "Ammonius, In Cat.: many composed works and inscribed them with Aristotle's name", "text": "text/ammonius-in-cat.txt", "find": "πολλοὶ γὰρ αὑτῶν συντιθέντες ἐπέγραφον τῷ Ἀριστοτέλους ὀνόματι"},
  {"label": "Simplicius, In Cat.: the heads to be set out before a treatise of Aristotle", "text": "text/simplicius-in-cat.txt", "find": "εἰ γνήσιον τοῦ φιλοσόφου τὸ βιβλίον"},
  {"label": "Philoponus, In Cat.: three occasions for the spuriousness of Aristotle's writings, the first homonymy of authors", "text": "text/philoponus-in-cat.txt", "find": "τρεῖς γὰρ αφορμαὶ γεγόνασι τοὐ νοθεύεσθαι τὰ συγγράμματά του Ἀριστοτέλους"},
  {"label": "Philoponus, In Cat.: Andronicus of Rhodes on beginning with logic", "text": "text/philoponus-in-cat.txt", "find": "ὁ δὲ τούτου διδάσκαλος Ἀνδρόνικος ὁ Ῥόδιος ἀκριβέστερον ἐξετάζων"},
  {"label": "Elias, In Cat.: Ptolemy's catalogue, a thousand works, with the life and the will", "text": "text/elias-in-cat.txt", "find": "χιλίων τὸν ἀριθμόν, ὥς φησι Πτολεμαῖος ὁ Φιλάδελφος ἀναγραφὴν αὐτῶν ποιησάμενος καὶ τὸν βίον αὐτοῦ καὶ τὴν διάθεσιν"},
  {"label": "Elias, In Cat.: royal ambition, Iobates collecting Pythagoras and Ptolemy collecting Aristotle", "text": "text/elias-in-cat.txt", "find": "ἢ διὰ φιλοτιμίαν βασιλικήν· Ἰοβάτους γὰρ τοῦ Λιβύων βασιλέως συναγαγόντος τὰ Πυθαγόρου καὶ Πτολεμαίου τὰ Ἀριστοτέλους"},
  {"label": "Elias, In Cat.: books aged artificially for the market", "text": "text/elias-in-cat.txt", "find": "τινὲς καπηλείας χάριν τὰ τυχόντα συγγράμματα λαμβάνοντες"},
  {"label": "Elias, In Cat.: works inscribed to the teachers, Socratics under Socrates and Pythagoreans under Pythagoras", "text": "text/elias-in-cat.txt", "find": "ὡς τὰ Πυθαγόρου καὶ Σωκράτους ἐπιγραφόμενα βιβλία μὴ ὄντα Σωκράτους ἢ Πυθαγόρου ἀλλὰ Σωκρατικῶν καὶ Πυθαγορικῶν"}],
 "scope": "Six commentators of the school of Ammonius and its neighbours, seven texts: the commentaries on the Categories by Ammonius, Simplicius, Philoponus, Olympiodorus and Elias, Olympiodorus's Prolegomena, and David's Prolegomena to philosophy. Each prolegomenon sets the reader's questions before a treatise; one of them is whether the book is genuine, and several give the ways books came to be spurious: the ambition of royal collectors, the goodwill of pupils who wrote under the teacher's name, and homonymy of authors, of works or of commentaries. Elias names Ptolemy's catalogue of a thousand works with the life and the will. Elias's and David's commentaries on the Isagoge, and the Prolegomena of the anonymous and of Simplicius's other prefaces, are not seated.",
 "why_seated": "The prolegomena are where the tradition wrote its rules for keeping one author per name. The study reads them for what the test of genuineness presupposes, and for the mechanisms of spuriousness they name, one of which, the pupils' goodwill, describes the many writing under one.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING})

AR = "https://raw.githubusercontent.com/OpenITI"
specs.append({
 "corpus": "arabic-biobibliography", "seat": "EA-CORPORA-31/05",
 "title": "The Arabic witnesses to Ptolemy's catalogue of Aristotle: Ibn al-Nadīm's Fihrist, Ibn al-Qifṭī and Ibn Abī Uṣaybiʿa",
 "language": "ara", "fetched": "2026-11-01",
 "license": {"payload": "The works are medieval (Ibn al-Nadīm d. c. 995; Ibn al-Qifṭī d. 1248; Ibn Abī Uṣaybiʿa d. 1270) and in the public domain. The Fihrist file transcribes Flügel's edition (Leipzig, 1871–1872), public domain everywhere. The Ibn al-Qifṭī and Ibn Abī Uṣaybiʿa files transcribe modern Beirut printings (ed. Ibrāhīm Shams al-Dīn; ed. Nizār Riḍā, 1965); edition-level status for those printings is UNVERIFIED AT SEAT TIME, and the seat claims no more for them than the OpenITI licence gives. The OpenITI files are CC BY-NC-SA 4.0 at the corpus: handled under the NC payload/record split ruled at EA-CORPORA-02, as at 29/09 and 30/08; the NonCommercial payload licence is carried forward unmodified and does not attach to this seat record.", "record": REC},
 "normalization": "The OpenITI files as served from raw.githubusercontent.com (branch master, fetched 2026-11-01; each file's sha256 is in MANIFEST.sha256), kept as text, line endings normalized. OpenITI's mARkdown markers (#, ~~, PageV..P..) are kept. No text was corrected by hand.",
 "units": "one text file per work",
 "items": [
  {"kind": "text", "slug": "ibn-al-nadim-fihrist", "class": "Ibn al-Nadīm", "url": f"{AR}/0400AH/master/data/0385IbnNadim/0385IbnNadim.Fihrist/0385IbnNadim.Fihrist.GRAR000030-ara2", "path": "openiti/0385IbnNadim.Fihrist.GRAR000030-ara2", "source": "OpenITI 0400AH (Graeco-Arabic Studies transcription of Flügel)",
   "work": "Ibn al-Nadīm, Kitāb al-Fihrist (كتاب الفهرست), ed. G. Flügel (Leipzig: Vogel, 1871–1872), vol. I pp. 2–360 — OpenITI 0385IbnNadim.Fihrist.GRAR000030-ara2"},
  {"kind": "text", "slug": "ibn-al-qifti-ikhbar", "class": "Ibn al-Qifṭī", "url": f"{AR}/0650AH/master/data/0646IbnQifti/0646IbnQifti.IkhbarCulama/0646IbnQifti.IkhbarCulama.Shamela0026336-ara1.mARkdown", "path": "openiti/0646IbnQifti.IkhbarCulama.Shamela0026336-ara1.mARkdown", "source": "OpenITI 0650AH (Shamela)",
   "work": "Ibn al-Qifṭī, Ikhbār al-ʿulamāʾ bi-akhbār al-ḥukamāʾ (إخبار العلماء بأخبار الحكماء), ed. Ibrāhīm Shams al-Dīn (Beirut: Dār al-Kutub al-ʿIlmiyya) — OpenITI 0646IbnQifti.IkhbarCulama.Shamela0026336-ara1"},
  {"kind": "text", "slug": "ibn-abi-usaybia-uyun", "class": "Ibn Abī Uṣaybiʿa", "url": f"{AR}/0675AH/master/data/0668IbnAbiUsaybica/0668IbnAbiUsaybica.CuyunAnba/0668IbnAbiUsaybica.CuyunAnba.Shamela0006687-ara1.completed", "path": "openiti/0668IbnAbiUsaybica.CuyunAnba.Shamela0006687-ara1.completed", "source": "OpenITI 0675AH (Shamela)",
   "work": "Ibn Abī Uṣaybiʿa, ʿUyūn al-anbāʾ fī ṭabaqāt al-aṭibbāʾ (عيون الأنباء في طبقات الأطباء), ed. Nizār Riḍā (Beirut: Dār Maktabat al-Ḥayāh, 1965) — OpenITI 0668IbnAbiUsaybica.CuyunAnba.Shamela0006687-ara1"}],
 "loci": [
  {"label": "Fihrist, the entry for Ptolemy al-Gharīb, partisan of Aristotle", "text": "text/ibn-al-nadim-fihrist.txt", "find": "بطليميوس الغريب وكان يتوالى ارسطاليس وينشر محاسنه"},
  {"label": "Fihrist, Aristotle's will as al-Gharīb gives it", "text": "text/ibn-al-nadim-fihrist.txt", "find": "وصية ارسطاليس قال الغريب لما حضرته الوفاة"},
  {"label": "Fihrist, the genealogy from Asclepius 'as Ptolemy al-Gharīb mentions'", "text": "text/ibn-al-nadim-fihrist.txt", "find": "كذا ذكر بطلميوس الغريب"},
  {"label": "Ibn al-Qifṭī, the list of Aristotle's books as a man called Ptolemy gives it in his book to Gallus", "text": "text/ibn-al-qifti-ikhbar.txt", "find": "ثبت كتب أرسطوطاليس على ما ذكره رجل يسمى بطليموس في كتابه إلى أغلس"},
  {"label": "Ibn Abī Uṣaybiʿa, Ptolemy's book to Gallus on Aristotle's life, his will and the list of his books", "text": "text/ibn-abi-usaybia-uyun.txt", "find": "وقال بطليموس في كتابه إلى غلس في سيرة أرسطوطاليس وخبره ووصيته وفهرست"},
  {"label": "Ibn Abī Uṣaybiʿa, the will of Aristotle, Antipater executor", "text": "text/ibn-abi-usaybia-uyun.txt", "find": "إني جعلت وصيي أبدا في جميع ما خلفت انطيبطرس"},
  {"label": "Ibn Abī Uṣaybiʿa, Theophrastus his mother's sister's son succeeds to the chair", "text": "text/ibn-abi-usaybia-uyun.txt", "find": "وجلس على كرسيه وورث مرتبته ابن"}],
 "scope": "The three Arabic works entire. Each carries the life of Aristotle from Ptolemy al-Gharīb (Ptolemy 'the stranger'; Rose's Ptolemaeus philosophus; Elias, seated at 31/04, calls him ὁ Φιλάδελφος), whose Greek book to Gallus gave the life, the will and the catalogue together and is lost in Greek; Ibn al-Qifṭī and Ibn Abī Uṣaybiʿa transmit the catalogue itself. Ibn Abī Uṣaybiʿa says Theophrastus was Aristotle's mother's sister's son (ابن خالته), the Fihrist his sister's son (ابن اخته). Rose's Latin rendering of the list, with its Greek reconstruction, is seated at 31/07. The Müller edition of Ibn Abī Uṣaybiʿa (Cairo and Königsberg, 1882–1884) and Lippert's Ibn al-Qifṭī (Leipzig, 1903), both public domain, were not found as text this session and are queued.",
 "why_seated": "The fourth catalogue survives only in Arabic, and it travels with the will: one book gave the life, the testament and the list of works as a single dossier of the person. The study reads it as the slot's most complete filling.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING,
 "queued": ["Ibn Abī Uṣaybiʿa, ʿUyūn al-anbāʾ, ed. A. Müller (1882–1884), public domain: no text layer found this session", "Ibn al-Qifṭī, Taʾrīkh al-ḥukamāʾ, ed. J. Lippert (Leipzig, 1903), public domain: OpenITI holds an uncorrected OCR (0646IbnQifti.TarikhHukama.Kraken220308195636-ara1), not seated"]})

specs.append({
 "corpus": "hermippus", "seat": "EA-CORPORA-31/06",
 "title": "Hermippus the Callimachean, fragments, in Müller's Fragmenta Historicorum Graecorum III (1849), from the DFHG",
 "language": "grc", "fetched": "2026-11-01",
 "license": {"payload": "Hermippus (fl. late third century BCE) is public domain, as are the witnesses quoted. Müller's FHG III (Paris: Didot, 1849) is public domain everywhere. The DFHG states that its contents are licensed CC BY-SA 4.0; redistributed under the same licence and attributed to the Digital Fragmenta Historicorum Graecorum (Leipzig).", "record": REC},
 "normalization": "The DFHG API response as served (JSON) is the original. text/hermippus-callimachius.txt is derived by build31.py: one block per fragment, its number, FHG volume and page, work and book, the witness, and the Greek text with whitespace collapsed. No text was corrected by hand.",
 "items": [{"kind": "dfhg", "slug": "hermippus-callimachius", "url": "http://www.dfhg-project.org/DFHG/api.php?author=HERMIPPUS%20CALLIMACHIUS", "path": "dfhg/HERMIPPUS-CALLIMACHIUS.json",
            "work": "Hermippus Callimachius, fragmenta, in C. Müller, Fragmenta Historicorum Graecorum III (Paris: Didot, 1849), pp. 36–54 — DFHG, author HERMIPPUS CALLIMACHIUS"}],
 "loci": [
  {"label": "fr. 41, the genealogy of Aristotle from the Asclepiads, 'as Hermippus says in his On Aristotle'", "text": "text/hermippus-callimachius.txt", "find": "καθά φησιν Ἕρμιππος ἐν τῷ Περὶ Ἀριστοτέλους"},
  {"label": "fr. 42, Herpyllis, and the care she received in the philosopher's will", "text": "text/hermippus-callimachius.txt", "find": "ἐπιμελείας φάσκων τῆς δεούσης τετυχηκέναι ἐν ταῖς τοῦ φιλοσόφου διαθήκαις"},
  {"label": "fr. 43, Theophrastus's performance in the Peripatos", "text": "text/hermippus-callimachius.txt", "find": "Ἕρμιππος δέ φησι Θεόφραστον παραγίνεσθαι εἰς τὸν περίπατον"},
  {"label": "fr. 45, Hermippus's On Theophrastus", "text": "text/hermippus-callimachius.txt", "find": "ἀλλὰ καὶ Ἕρμιππος ἐν τῷ Περὶ Θεοφράστου"}],
 "scope": "All ninety-three fragments the DFHG gives for Hermippus the Callimachean, from his Lives (On Aristotle, On Theophrastus, the lawgivers, the Seven Sages, the Pythagoreans) and his other works. Wehrli's edition (Die Schule des Aristoteles, Suppl. I, 1974) and Bollansée's (FGrHist IV A 3, 1999) are in copyright and go to 31/11.",
 "why_seated": "Hermippus, Callimachus's pupil, wrote separate lives of Aristotle and Theophrastus and is the earliest named source behind Diogenes Laertius's biographies and lists. The study reads him as the point where the library's catalogue became biography.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING, "cross_references": ["diogenes-laertius (V)"]})

specs.append({
 "corpus": "hesychian-catalogue", "seat": "EA-CORPORA-31/07",
 "title": "The Hesychian life and catalogue of Aristotle (the Vita Menagiana), with Rose's Ptolemy, in Rose's Aristotelis fragmenta (Teubner, 1886), pp. 9–22",
 "language": "mul", "fetched": "2026-11-01",
 "license": {"payload": "The Hesychian life (Hesychius of Miletus, sixth century) is public domain. Rose's Aristotelis qui ferebantur librorum fragmenta (Leipzig: Teubner, 1886) is public domain; the Archive marks the item NOT_IN_COPYRIGHT. The OCR was made in session from the Archive's page images and is released with this seat record.", "record": REC},
 "normalization": "The Archive's own OCR of this volume reads the Greek as Latin and is not used. Leaves n17–n30 were OCR'd in session (the engine and models are in origin.items); the OCR of each leaf is kept under original/, and the page images are held by URL and sha256. " + NORM_OCR,
 "items": [{"kind": "ocr_pages", "slug": "rose-1886-pp9-22", "identifier": "aristotelisquif00arisgoog", "pages": list(range(17, 31)), "ocr_prefix": "rose-1886",
            "images_dir": f"{SCR}/rose", "ocr_engine": ENGINE,
            "work": "V. Rose, Aristotelis qui ferebantur librorum fragmenta (Leipzig: Teubner, 1886), pp. 9–22: the end of Diogenes Laertius's list, the Hesychian life and catalogue from Ambros. L 93 sup. with Rose's apparatus, and Ptolemy's list in Rose's Latin with its Greek titles — Internet Archive aristotelisquif00arisgoog, leaves n17–n30, OCR in session"}],
 "loci": [
  {"label": "Rose's running head over all the lists", "text": "text/rose-1886-pp9-22.ocr.txt", "find": "EX ANDRONICI RHODII INDICE"},
  {"label": "the Hesychian life: the successors of the school in order", "text": "text/rose-1886-pp9-22.ocr.txt", "find": "διάδοχοι δὲ αὐτοῦ τῆς σχολῆς κατὰ τάξιν"},
  {"label": "the Hesychian life: the list introduced", "text": "text/rose-1886-pp9-22.ocr.txt", "find": "τὰ δὲ συγγράμματα αὐτοῦ ταῦτα"},
  {"label": "the Hesychian catalogue: its pseudepigrapha", "text": "text/rose-1886-pp9-22.ocr.txt", "find": "ψευδεπίγραφα δὲ"},
  {"label": "Rose on Ptolemy's list", "text": "text/rose-1886-pp9-22.ocr.txt", "find": "PTOLEMAEI PHILOSOPHI"},
  {"label": "Rose's note: Andronicus the eleventh successor, after Elias", "text": "text/rose-1886-pp9-22.ocr.txt", "find": "ὁ τούτου ἑνδέκατος γενόμενος διάδοχος"}],
 "scope": "Rose's pages 9–22 (leaves n17–n30): the close of Diogenes Laertius's catalogue, the Hesychian life and catalogue with its closing list of pseudepigrapha, and Ptolemy's catalogue in Rose's Latin with the Greek titles he restores. Rose sets every list under the running head EX ANDRONICI RHODII INDICE, his thesis that the lists descend from Andronicus's catalogue. Diogenes's list is seated whole in diogenes-laertius; the Arabic text of Ptolemy's list is at 31/05. Düring's edition of the lives (1957) is in copyright and goes to 31/11.",
 "why_seated": "The Hesychian catalogue is the third ancient list, and it alone names pseudepigrapha under Aristotle's name, filing the spurious inside the one name's list. Rose's running head is itself a reading: every list made one edition's index.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING, "cross_references": ["diogenes-laertius (V.22–27)", "arabic-biobibliography (31/05)"]})

specs.append({
 "corpus": "callimachus-pinakes", "seat": "EA-CORPORA-31/08",
 "title": "Callimachus, Pinakes, the fragments and Schneider's account of them, in Callimachea II (Teubner, 1873), pp. 296–328",
 "language": "mul", "fetched": "2026-11-01",
 "license": {"payload": "Callimachus (d. c. 240 BCE) is public domain. Schneider's Callimachea II (Leipzig: Teubner, 1873) is public domain; the Archive marks the item Public Domain Mark 1.0. The OCR was made in session from the Archive's page images and is released with this seat record.", "record": REC},
 "normalization": "The Archive's own OCR of this volume reads the Greek as Latin and is not used. Leaves n297–n329 were OCR'd in session; the OCR of each leaf is kept under original/, and the page images are held by URL and sha256. " + NORM_OCR,
 "items": [{"kind": "ocr_pages", "slug": "schneider-1873-pinakes", "identifier": "bub_gb_Gr2y6qtXZCMC", "pages": list(range(297, 330)), "ocr_prefix": "schneider-callimachea-2",
            "images_dir": f"{SCR}/call", "ocr_engine": ENGINE,
            "work": "O. Schneider, Callimachea II: Fragmenta a Bentleio collecta et explicata, ab aliis aucta (Leipzig: Teubner, 1873), pp. 296–328: fr. 100d, the Πίνακες, with the end of fr. 100c and the start of fr. 100e — Internet Archive bub_gb_Gr2y6qtXZCMC, leaves n297–n329, OCR in session"}],
 "loci": [
  {"label": "the Pinax of philosophers in chronological order", "text": "text/schneider-1873-pinakes.ocr.txt", "find": "D. Πίναξ καὶ ἀναγραφὴ τῶν κατὰ χρόνους καὶ ἀπ᾽ ἀρχῆς"},
  {"label": "the Pinakes of those distinguished in all learning", "text": "text/schneider-1873-pinakes.ocr.txt", "find": "ἐν πάσῃ παιδείᾳ διαλαμψάντων"},
  {"label": "the Pinax of orators", "text": "text/schneider-1873-pinakes.ocr.txt", "find": "γενυμένων ῥητορικῶν", "note": "the page reads γενομένων; the OCR reads γενυμένων"}],
 "scope": "The pages of Schneider's second volume that carry fr. 100d, the Pinakes: his reconstruction of the parts of the work, then the testimonia and fragments, with the edges of fr. 100c and fr. 100e. Pfeiffer's Callimachus (1949–1953), the standard numbering, is in copyright and goes to 31/11.",
 "why_seated": "The Pinakes are the filing system the later lists inherit: tables 'of those distinguished in every branch of learning', a name with its works and their opening words and line-counts. The slot of one name per list begins in this library.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING})

specs.append({
 "corpus": "bekker-aristotle-1831", "seat": "EA-CORPORA-31/09",
 "title": "The preface to Bekker's Aristotle, Aristoteles graece I (Berlin, 1831)",
 "language": "lat", "fetched": "2026-11-01",
 "license": {"payload": "Aristoteles graece ex recensione Immanuelis Bekkeri, edidit Academia Regia Borussica, vol. I (Berlin: Reimer, 1831) is public domain everywhere; the Archive marks the item NOT_IN_COPYRIGHT. The OCR was made in session and is released with this seat record.", "record": REC},
 "normalization": "The Archive's own OCR reads the preface's Latin as Greek and is not used. Leaves n8–n11 were OCR'd in session with the Latin model; the OCR of each leaf is kept under original/, and the page images, like the volume's scan (120 MB), are held by reference. " + NORM_OCR,
 "items": [{"kind": "ocr_pages", "slug": "bekker-1831-praefatio", "identifier": "aristotelisopera01arisuoft", "pages": [8, 9, 10, 11], "ocr_prefix": "bekker-1831-v1",
            "images_dir": f"{SCR}/bekker", "ocr_engine": ENGINE | {"command": "tesseract nNN.jpg nNN -l lat (n10, n11 with lat+grc)"},
            "work": "Aristoteles graece ex recensione Immanuelis Bekkeri, edidit Academia Regia Borussica, vol. I (Berlin: Reimer, 1831), the Praefatio and the list of codices — Internet Archive aristotelisopera01arisuoft (Toronto), leaves n8–n11, OCR in session"}],
 "loci": [
  {"label": "the heading", "text": "text/bekker-1831-praefatio.ocr.txt", "find": "PRAEFATIO."},
  {"label": "Schleiermacher's plan for the edition", "text": "text/bekker-1831-praefatio.ocr.txt", "find": "consilium ce- pisset Aristotelis ex diutino situ excitandi novaque editione celebrandi"},
  {"label": "the libraries searched", "text": "text/bekker-1831-praefatio.ocr.txt", "find": "in perlustrandis Italiae Galliae Britanniae copiis litterariis"},
  {"label": "the first codex of the sigla", "text": "text/bekker-1831-praefatio.ocr.txt", "find": "codex Urbinas 35"}],
 "scope": "The preface entire and the list of codices that follows it. The preface is one paragraph: the Berlin Academy's plan, on Schleiermacher's initiative, to raise Aristotle 'from long neglect', the more than three years (plus quam triennium) Bekker and Brandis spent in the libraries of Italy, France and Britain, the division of labour between text and scholia, and the sigla. It says nothing of genuineness, order or authorship. The pagination this volume set (the Bekker numbers) is the one every later citation of Aristotle uses, Theophrastus's works not among them.",
 "why_seated": "The modern edition fixed the corpus as numbered pages under one name, and its preface records the operation as a search of libraries. What the preface leaves unsaid is the finding the study reads.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING})

specs.append({
 "corpus": "jaeger-aristoteles", "seat": "EA-CORPORA-31/10",
 "title": "Werner Jaeger, Aristoteles: Grundlegung einer Geschichte seiner Entwicklung (Berlin, 1923)",
 "language": "deu", "fetched": "2026-11-01",
 "license": {"payload": "Published in Berlin by Weidmann in 1923, the book is public domain in the United States (published before 1931). Jaeger died in 1961, so the author's term runs in the European Union and in Germany until the end of 2031; the seat is made under the archive's United States rule and says so. The OCR layer is the Archive's.", "record": REC},
 "normalization": "The Archive's OCR text layer (_djvu.txt), line endings normalized; the scan (33 MB) is held by reference with the Archive's md5. " + NORM_OCR,
 "items": [{"kind": "ia_ref", "slug": "jaeger-1923", "identifier": "aristotelesgrund00jaeguoft", "scan": "aristotelesgrund00jaeguoft.pdf",
            "work": "W. Jaeger, Aristoteles: Grundlegung einer Geschichte seiner Entwicklung (Berlin: Weidmann, 1923) — Internet Archive aristotelesgrund00jaeguoft (Toronto), the OCR layer"}],
 "loci": [
  {"label": "Andronicus and the renewal of the treatises", "text": "text/jaeger-1923.ocr.txt", "find": "Die Erneuerung des Studiums der Lehrschriften durch Andronikos"},
  {"label": "Skepsis, Erastus and Coriscus", "text": "text/jaeger-1923.ocr.txt", "find": "und Koriskos aus Skepsis am Ida"}],
 "scope": "The book entire in the Archive's OCR. Jaeger reads the treatises as the strata of a development, from a Platonic beginning to an empirical end, and orders the texts by the life the order produces. Düring's critique (Aristoteles, 1966) and Moraux's Les listes anciennes des ouvrages d'Aristote (1951) are in copyright and go to 31/11.",
 "why_seated": "Jaeger builds a biography out of the texts and then reads the texts by the biography, the dependency the archive's Locating the Dependencies protocol (#1602) names run forward into the modern apparatus. The study reads him as the last stratum before the encyclopedia.",
 "spine": "EA-CORPORA-31", "ruling": RULING, "seating": SEATING})

for s in specs:
    (H / f"spec31-{s['corpus']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(s["corpus"])
