#!/usr/bin/env python3
"""Writes the EA-CORPORA-32 specs (spec32-<corpus>.json). Session tool. The leaves of the session-OCR seats are filled in
from the OCR files present under ocr/ when this runs (the ranges are stated in each spec)."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
SCR = "/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/ea32"
P = "341e309c821d5eca8c976bebca77c28b10bad58f"   # PerseusDL/canonical-greekLit, the commit 31/01 pins
PL = "8b536bdf3ed1f43494055efe112433b4a58eab67"  # PerseusDL/canonical-latinLit, HEAD on 2026-11-02 (git ls-remote)
RULING = ("Lee Sharks, 2026-11-02, of the texts still owed in §5 of the design Legitimately Many (drafts/LEGITIMATELY-MANY-design-2026-11-01.md): "
          "\"lets prepare that seating, its ea corpora deposit, and its tll spine and card\".")
SEATING = "EA-CORPORA-32, the thirty-second seating: the remaining debts of Legitimately Many, 2026-11-02"
REC = "CC-BY-4.0 applies to this seat record only."
NORM_TEI = "Originals as fetched under original/, pinned to a commit of the repository named in origin.items. text/<slug>.txt is the TEI reduced to plain text by seat.py (rebuild/corpora/ea-corpora-27), notes and apparatus dropped, divisions kept. No text was corrected by hand."
NORM_OCR = "The OCR is kept as made, with line endings normalized. No text was corrected by hand; the loci keep the OCR's readings and say where those differ from the printed page."
NORM_IA = "The Archive's OCR text layer (_djvu.txt) of the whole volume, line endings normalized; the scan is held by reference with the Archive's md5. "
TD = "raw.githubusercontent.com/tesseract-ocr/tessdata_best, main"
ENGINE_GRC = {"engine": "Tesseract 5.3.4", "models": f"tessdata_best grc+lat ({TD})",
              "sha256": {"grc.traineddata": "dfc9bda286cd9d8755b1832e5731a5425d1cf0803393a5fa6dee078466178cf1",
                         "lat.traineddata": "60054dd32ac03ebd9b4f87d0665bd491a7ffe0d3ee99ceb91aefaf348b65e94f"},
              "command": "tesseract nNN.jpg nNN -l grc+lat", "run": "2026-11-02, in session"}
ENGINE_FRAK = {"engine": "Tesseract 5.3.4", "models": f"tessdata_best deu_latf, the Fraktur model ({TD})",
               "sha256": {"deu_latf.traineddata": "429b8c33d37e1a4823a2bb082a644ff13e252f735b7945e08a518d22ddcc459e"},
               "command": "tesseract nNN.jpg nNN -l deu_latf", "run": "2026-11-02, in session"}


def research(section):
    """The research in connection with which the seat was made (the operator's rule of 2026-11-02: a seating conducted in the
    course of active research names that research)."""
    return {"study": "Legitimately Many: how the many-author reading of the Socratic–Peripatetic corpus embrittled",
            "design": "drafts/LEGITIMATELY-MANY-design-2026-11-01.md", "draft": "drafts/LEGITIMATELY-MANY-draft-2026-11-02.md",
            "locus_table": "rebuild/legitimately-many/loci-table.md", "owed_at": "design §5, 'Still owed'", "for": section}


def tei(base, commit, cat, g, w, ed, slug, work):
    f = f"data/{g}/{w}/{g}.{w}.{ed}.xml"
    return {"kind": "tei", "slug": slug, "url": f"https://raw.githubusercontent.com/{base}/{commit}/{f}", "path": f"perseus/{g}.{w}.{ed}.xml",
            "source": f"Perseus Digital Library, {cat}", "repository": f"https://github.com/{base}", "commit": commit, "file": f, "work": work}


def leaves(prefix):
    d = H / "ocr"
    return sorted(int(p.stem.split("-n")[-1]) for p in d.glob(f"{prefix}-n*.txt"))


specs = []

specs.append({
 "corpus": "pseudo-archytas", "seat": "EA-CORPORA-32/01",
 "title": "The pseudo-Archytan writings, with the book on the ten categories, in Mullach's Fragmenta philosophorum Graecorum I (Didot, 1860)",
 "language": "mul", "fetched": "2026-11-02",
 "license": {"payload": "The pseudo-Archytan writings (Hellenistic or early imperial) are public domain. Mullach's Fragmenta philosophorum Graecorum I (Paris: Didot, 1860) is public domain everywhere; Mullach died in 1882. The OCR layer is the Archive's.", "record": REC},
 "normalization": NORM_IA + NORM_OCR,
 "items": [{"kind": "ia_ref", "slug": "mullach-fphg-1860-vol1", "identifier": "fragmentaphilo01mull", "scan": "fragmentaphilo01mull.pdf",
            "work": "F. W. A. Mullach, Fragmenta philosophorum Graecorum I (Paris: Didot, 1860), Greek with Mullach's Latin, the Archytan fragments under ARCHYTAE TARENTINI FRAGMENTA — Internet Archive fragmentaphilo01mull (Toronto), the OCR layer"}],
 "loci": [
  {"label": "Mullach's heading for the Archytan fragments", "text": "text/mullach-fphg-1860-vol1.ocr.txt", "find": "ARCHYT/E TARENTINI", "note": "the page reads ARCHYTAE; the OCR reads ARCHYT/E"},
  {"label": "C. Logica: the book on the ten categories, in Mullach's Latin", "text": "text/mullach-fphg-1860-vol1.ocr.txt", "find": "De decem Categoriis liber."},
  {"label": "the categories book opens: five things belong to every art, matter, instrument, part, definition and end", "text": "text/mullach-fphg-1860-vol1.ocr.txt", "find": "materia , instrumentum, pars, definilio et finis.", "note": "the page reads definitio; the OCR reads definilio"},
  {"label": "Mullach on fifteen passages from the pseudo-Archytan book called the καθολικοὶ λόγοι δέκα, passed off as Ocellus", "text": "text/mullach-fphg-1860-vol1.ocr.txt", "find": "quindecim loca, e Pseudarchytz libro qui in- scribitur", "note": "the page reads Pseudarchytae; the OCR reads Pseudarchytz"},
  {"label": "Mullach: the letter of Plato to Archytas is spurious", "text": "text/mullach-fphg-1860-vol1.ocr.txt", "find": "nem. Nam spuria est Platonis ad Archytam"}],
 "scope": "The volume's OCR layer entire: the Presocratics, Ocellus, Timaeus Locrus and the Pythagorean fragments in Mullach's Greek and Latin. The seat is held for the writings under Archytas's name, above all the book on the ten categories (Περὶ τῶν καθόλου λόγων, the καθολικοὶ λόγοι δέκα), which Simplicius (seated in aristotle-commentators, 31/04) takes as Archytas's and as the source Aristotle followed. Thesleff's The Pythagorean Texts of the Hellenistic Period (1965) and Szlezák's Pseudo-Archytas über die Kategorien (1972) are in copyright and go to 32/11.",
 "why_seated": "The pseudo-Archytan Categories is the case where the slot of the one name runs the other way: a book in Doric under an older name, read by the Neoplatonist commentators as Aristotle's source. The study reads it beside Simplicius's proof of the Categories' genuineness.",
 "research": research("draft §2 (Simplicius and the Categories: the Archytas transition, In Cat. 2.15–25, 382.7–8, 407.17–19) and design §3.9a"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING, "cross_references": ["aristotle-commentators (31/04, Simplicius In Cat.)"]})

specs.append({
 "corpus": "aldine-aristotle-1497", "seat": "EA-CORPORA-32/02",
 "title": "The Aldine Aristotle, volume IV (Venice: Aldus Manutius, 1 June 1497): the end of Aristotle's Metaphysics and Theophrastus's Metaphysics, with the scholion, the register and the colophons",
 "language": "mul", "fetched": "2026-11-02",
 "license": {"payload": "Printed in 1497, the volume is public domain everywhere. The scan is the Boston Public Library's (copy Q.403.89 FOLIO), served by the Internet Archive; the page images are held by URL and sha256. The transcription was made in session and is released with this seat record.", "record": REC},
 "normalization": "The Archive's OCR of an incunable Greek fount is unusable, and an OCR made for it in session read no better, so none is kept. text/aldine-1497-vol4-transcription.txt is a transcription of named passages made by eye in session from the page images listed in origin.items: abbreviations and ligatures are resolved, accents and breathings follow the print where legible; it is a reading of the page, to be checked against the image. The rest of the leaves are held as images only.",
 "items": [{"kind": "page_images", "slug": "aldine-1497-vol4", "identifier": "opera05aris", "pages": list(range(576, 589)), "images_dir": f"{SCR}/ald",
            "transcription": "aldine-1497-vol4-transcription.txt",
            "work": "Aristotle and others, [Opera], ed. Aldus Manutius, vol. IV (Venice: Aldus Manutius, 1 June 1497), the second part of the volume as the Boston Public Library binds it: leaves 116–121 of the last foliation, the end of Aristotle's Metaphysics, Theophrastus's Metaphysics (ΘΕΟΦΡΑΣΤΟΥ ΤΩΝ ΜΕΤΑ ΤΑ ΦΥΣΙΚΑ), the scholion on it, the register and the Greek and Latin colophons — Internet Archive opera05aris, leaves n576–n588"}],
 "loci": [
  {"label": "f. 117r, the title of Theophrastus's Metaphysics", "text": "text/aldine-1497-vol4-transcription.txt", "find": "ΘΕΟΦΡΑΣΤΟΥ ΤΩΝ ΜΕΤΑ ΤΑ ΦΥΣΙΚΑ"},
  {"label": "the scholion: Andronicus and Hermippus do not know this book", "text": "text/aldine-1497-vol4-transcription.txt", "find": "Τοῦτο τὸ βιβλίον, Ἀνδρόνικος μὲν καὶ Ἕρμιππος ἀγνοοῦσιν"},
  {"label": "the scholion: Nicolaus mentions it in his study of Aristotle's Metaphysics, saying it is Theophrastus's", "text": "text/aldine-1497-vol4-transcription.txt", "find": "Νικόλαος δὲ ἐν τῇ θεωρίᾳ τῶν Ἀριστοτέλους μετὰ τὰ φυσικὰ μνημονεύει αὐτοῦ, λέγων εἶναι Θεοφράστου"},
  {"label": "the register: one heading for the two Metaphysics", "text": "text/aldine-1497-vol4-transcription.txt", "find": "Ἀριστοτέλους καὶ Θεοφράστου τῶν μετὰ τὰ φυσικά."},
  {"label": "the Latin colophon", "text": "text/aldine-1497-vol4-transcription.txt", "find": "Excriptum Venetiis in domo Aldi Manutii"}],
 "scope": "Thirteen leaves held as images (n576–n588): the last leaves of Aristotle's Metaphysics, all of Theophrastus's, the scholion printed after it, and the register and colophons that close the volume. Aldus printed the two Metaphysics consecutively, the running heads pairing the author's name on the verso with τῶν μετὰ τὰ φυσικά on the recto, and the register gathers both under one heading, Ἀριστοτέλους καὶ Θεοφράστου τῶν μετὰ τὰ φυσικά. The scholion, printed in the same fount after the text, records that Andronicus and Hermippus did not know the book, that neither mentions it in the list of Theophrastus's books, and that Nicolaus (of Damascus) mentions it in his study of Aristotle's Metaphysics as Theophrastus's. The volume's other works (Theophrastus's botany, the Problems, Alexander's Problems, the Mechanics, and the first books of the Metaphysics) are in the same scan and are not transcribed.",
 "why_seated": "The first printed edition puts the two Metaphysics together and keeps the ancient note that the shorter one was missing from the catalogues of Andronicus and Hermippus and was assigned to Theophrastus by Nicolaus. The study reads the seam at the place the print first fixed it.",
 "research": research("design §3.10 and §7.2 (the Aldine contents reported by the research pass, read here from the scan), and the Λ seam through its editions (the next item of the study)"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING,
 "cross_references": ["theophrastus (EA-CORPORA-09/01, the Metaphysics in Wimmer's Teubner, tlg0093.tlg006, which does not carry the scholion)", "hermippus (31/06)", "theophrastus-metaphysics-wimmer-1866 (32/03)"]})

specs.append({
 "corpus": "theophrastus-metaphysics-wimmer-1866", "seat": "EA-CORPORA-32/03",
 "title": "Theophrastus, Opera, in Wimmer's Greek and Latin (Paris: Didot, 1866), with the Metaphysics and Wimmer's account of its editions",
 "language": "mul", "fetched": "2026-11-02",
 "license": {"payload": "Theophrastus is public domain. Wimmer's Theophrasti Eresii opera quae supersunt omnia (Paris: Didot, 1866) is public domain everywhere; the Archive marks the item NOT_IN_COPYRIGHT. The OCR layer is the Archive's.", "record": REC},
 "normalization": NORM_IA + NORM_OCR,
 "items": [{"kind": "ia_ref", "slug": "wimmer-didot-1866", "identifier": "theophrastioper00theogoog", "scan": "theophrastioper00theogoog.pdf",
            "work": "Theophrasti Eresii opera, quae supersunt, omnia, Graeca recensuit, Latine interpretatus est F. Wimmer (Paris: Didot, 1866) — Internet Archive theophrastioper00theogoog (Oxford, digitized by Google), the OCR layer"}],
 "loci": [
  {"label": "Wimmer's heading for the Metaphysics, in the Latin", "text": "text/wimmer-didot-1866.ocr.txt", "find": "THEOPHRASTI METAPHYSICA."},
  {"label": "Wimmer's preface: Brandis collated four codices for the twelfth piece, ἐκ τῶν μετὰ τὰ φυσικά", "text": "text/wimmer-didot-1866.ocr.txt", "find": "comparavit Brandis"},
  {"label": "Wimmer's preface: Brandis gave their readings in his edition of the Metaphysics of Aristotle and Theophrastus", "text": "text/wimmer-didot-1866.ocr.txt", "find": "in editione sua Metaphysicorum Aristo- telis et Theophrasti exposuit"}],
 "scope": "The volume entire in the Archive's OCR, the Greek in a lower layer than the Latin. Wimmer prints the Metaphysics as the twelfth of the fragments under the title ἐκ τῶν μετὰ τὰ φυσικά and says in the preface that Brandis collated four codices for it and printed their readings in his edition of the Metaphysics of Aristotle and Theophrastus (Berlin, 1823), with Usener's emendations of 1858. A search of the OCR layer on 2026-11-02 found no copy of the scholion that the Aldine prints after the text (32/02), and the Teubner Wimmer already seated (theophrastus, tlg0093.tlg006) ends without it; whether the Didot prints it in a note the OCR missed is to be checked against the page. Brandis 1823 and Usener 1890, both public domain, were not found as scans and are queued; Ross and Fobes (1929), Laks and Most (1993) and Gutas (2010) go to 32/11.",
 "why_seated": "The nineteenth-century editions are where the note on the book's attribution passed from the print into the apparatus or out of the text. The study reads the Λ seam as the editions handled it.",
 "research": research("the Λ seam through its editions (the next item of the study), from design §3.10"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING,
 "queued": ["C. A. Brandis, Aristotelis et Theophrasti Metaphysica (Berlin, 1823), public domain: not found as a scan this session", "H. Usener and the Bonn philological seminar, Theophrasti de prima philosophia libellus (Bonn, 1890), public domain: not found as a scan this session"],
 "cross_references": ["theophrastus (EA-CORPORA-09/01)", "aldine-aristotle-1497 (32/02)"]})

MEK = leaves("mekler-1902")
specs.append({
 "corpus": "philodemus-index-academicorum", "seat": "EA-CORPORA-32/04",
 "title": "Philodemus, Index Academicorum (PHerc. 1021 and 164), in Mekler's edition (Berlin: Weidmann, 1902)",
 "language": "mul", "fetched": "2026-11-02",
 "license": {"payload": "Philodemus (d. c. 40 BCE) is public domain. Mekler's Academicorum philosophorum index Herculanensis (Berlin: Weidmann, 1902) is public domain in the United States (published before 1931); Mekler died in 1912, so it is public domain everywhere. The Archive marks the item NOT_IN_COPYRIGHT. The OCR was made in session from the Archive's page images and is released with this seat record.", "record": REC},
 "normalization": "The Archive's own OCR of this volume reads the Greek as Latin and is not used. The leaves named in origin.items were OCR'd in session; Mekler prints each column twice, the papyrus in majuscule as the apographs give it and his restored text beneath, and the OCR of the majuscule is poor. The OCR of each leaf is kept under original/, and the page images are held by URL and sha256. " + NORM_OCR,
 "items": [{"kind": "ocr_pages", "slug": "mekler-1902", "identifier": "academicorumphil00mekluoft", "pages": MEK, "ocr_prefix": "mekler-1902",
            "images_dir": f"{SCR}/mek", "ocr_engine": ENGINE_GRC,
            "work": f"S. Mekler, Academicorum philosophorum index Herculanensis (Berlin: Weidmann, 1902), the end of the preface, the sigla, the text of the columns and Mekler's chronological table — Internet Archive academicorumphil00mekluoft (Toronto), leaves n{MEK[0] if MEK else '?'}–n{MEK[-1] if MEK else '?'} (n39, which the OCR found blank, is not held), OCR in session"}],
 "loci": [
  {"label": "Col. I, the first column of the text", "text": "text/mekler-1902.ocr.txt", "find": "Col. I. (13. 730 O. 162 N.)"},
  {"label": "the schools of Plato and Eudoxus", "text": "text/mekler-1902.ocr.txt", "find": "Πλάτωνος χαὶ Εὐδόξου διατριβαί", "note": "the page reads καὶ; the OCR reads χαὶ"},
  {"label": "Col. VI, Plato's pupils: Mekler's restored text", "text": "text/mekler-1902.ocr.txt", "find": "Col. VI. (18. 735 0. 167 N)", "note": "the page reads 735 O.; the OCR reads 735 0."},
  {"label": "Col. VI, apparatus: the names of Speusippus and Xenocrates supplied by Spengel from Diogenes", "text": "text/mekler-1902.ocr.txt", "find": "Speusippi et Xenocratis nomina Diogene conl. suppl. Sp."},
  {"label": "Col. VI, testimonia: Diogenes III.46, the list of Plato's pupils the supplement is drawn from", "text": "text/mekler-1902.ocr.txt", "find": "μαϑηταὶ δ᾽ αὐτοῦ Σπεύσιππος ᾿Αϑηναῖος", "note": "the OCR writes ϑ for θ"}],
 "scope": "Mekler's edition from the end of its preface through the text and his chronological table, up to the indices (pp. XXXIII–120): the columns of PHerc. 1021 and 164, each printed in the apographs' majuscule with Mekler's restoration beneath, an apparatus naming who supplied each supplement, and the parallel testimonia. At Col. VI, the list of Plato's pupils, the apparatus says the names of Speusippus and Xenocrates are supplied by Spengel by comparison with Diogenes (Speusippi et Xenocratis nomina Diogene conl. suppl. Sp.), and the testimonia print Diogenes III.46. Dorandi's edition (1991) is in copyright and goes to 32/11.",
 "why_seated": "The Index Academicorum is a history of the Academy written as a succession of named heads and pupils, with the lives and the books attached to each name. The study reads it beside Diogenes Laertius and the Peripatetic wills as the Academy's own form of the slot.",
 "research": research("design §5 and §7.2 (Philodemus, reported by the research pass and not yet read)"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING,
 "queued": ["F. Buecheler, Academicorum philosophorum index Herculanensis (Greifswald, 1869), public domain: the Archive's copy (bub_gb_U6qyAAAAMAAJ) is a 28-leaf program whose OCR reads the Greek as Latin; not seated"],
 "cross_references": ["diogenes-laertius (IV, the Academics)"]})

specs.append({
 "corpus": "dionysius-ad-ammaeum", "seat": "EA-CORPORA-32/05",
 "title": "Dionysius of Halicarnassus, First Letter to Ammaeus, in Usener and Radermacher's Greek (Teubner, 1899)",
 "language": "grc", "fetched": "2026-11-02",
 "license": {"payload": "Dionysius (fl. late first century BCE) is public domain. Usener and Radermacher's Dionysii Halicarnasei opuscula I (Leipzig: Teubner, 1899) is public domain everywhere. The TEI is the Perseus Digital Library's, CC BY-SA 4.0, redistributed under the same licence and attributed to Perseus.", "record": REC},
 "normalization": NORM_TEI,
 "items": [tei("PerseusDL/canonical-greekLit", P, "canonical-greekLit", "tlg0081", "tlg008", "perseus-grc2", "ad-ammaeum-1",
               "Dionysius of Halicarnassus, Ἐπιστολὴ πρὸς Ἀμμαῖον (First Letter to Ammaeus), ed. H. Usener and L. Radermacher, Dionysii Halicarnasei opuscula I (Leipzig: Teubner, 1899) — Perseus TEI tlg0081.tlg008.perseus-grc2")],
 "loci": [
  {"label": "1, a Peripatetic undertook to show that Demosthenes learned his art from Aristotle's Rhetoric", "text": "text/ad-ammaeum-1.txt", "find": "ὅτι Δημοσθένης τὰς ῥητορικὰς τέχνας παρʼ ἐκείνου μαθὼν εἰς τοὺς ἰδίους μετήνεγκε λόγους"},
  {"label": "the Rhetoric dated after the Olynthian war by Aristotle's own words", "text": "text/ad-ammaeum-1.txt", "find": "οὑτωσὶ μὲν δὴ σαφῶς αὐτὸς ὁ φιλόσοφος ἀποδεικνύει μετὰ τὸν Ὀλυνθιακὸν πόλεμον γεγραμμένας ὑπʼ αὐτοῦ τὰς τέχνας"},
  {"label": "the archon year taken from Philochorus's Atthis, verbatim", "text": "text/ad-ammaeum-1.txt", "find": "ὡς δηλοῖ Φιλόχορος ἐν ἕκτῃ βύβλῳ τῆς Ἀτθίδος κατὰ λέξιν οὕτω γράφων"}],
 "scope": "The First Letter to Ammaeus entire. A Peripatetic had claimed that Demosthenes formed his speeches on Aristotle's Rhetoric; Dionysius answers by dating, setting the speeches by archon years from Philochorus and the Rhetoric by the events it mentions, and declaring each step of evidence as he takes it.",
 "why_seated": "An ancient chronology of a corpus that names its evidence, quotes its sources verbatim and builds the order from them is the control for the study's question of how the order of the works was fixed. The Peripatetic claim it refutes is itself a case of the school's founder made the source of what came after him.",
 "research": research("design §3.7 (the control: an ancient chronology with declared evidentiary moves) and §5"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING})

specs.append({
 "corpus": "cicero-ad-atticum", "seat": "EA-CORPORA-32/06",
 "title": "Cicero, Letters to Atticus, in Purser's Latin (Oxford Classical Texts, 1903)",
 "language": "lat", "fetched": "2026-11-02",
 "license": {"payload": "Cicero is public domain. Purser's Epistulae II (Oxford: Clarendon Press, 1903) is public domain in the United States (published before 1931); Purser died in 1932, and the edition is public domain in the European Union. The TEI is the Perseus Digital Library's, CC BY-SA 4.0, redistributed under the same licence and attributed to Perseus.", "record": REC},
 "normalization": NORM_TEI,
 "items": [tei("PerseusDL/canonical-latinLit", PL, "canonical-latinLit", "phi0474", "phi057", "perseus-lat2", "ad-atticum",
               "Cicero, Epistulae ad Atticum, ed. L. C. Purser, M. Tulli Ciceronis Epistulae II (Oxford: Clarendon Press, 1903) — Perseus TEI phi0474.phi057.perseus-lat2")],
 "loci": [
  {"label": "Att. IV.16.2, prefaces in each book, as Aristotle in the books he calls exoteric", "text": "text/ad-atticum.txt", "find": "quoniam in singulis libris utor prohoemiis ut Aristoteles in iis quos ἐξωτερικοὺς vocat"},
  {"label": "Att. IV.16.2, the speakers of the De re publica", "text": "text/ad-atticum.txt", "find": "in Africani personam et Phili et Laeli et Manili contuli"}],
 "scope": "The sixteen books of letters to Atticus entire. At IV.16.2 (54 BCE) Cicero describes the dialogue he is writing, the De re publica, and says he uses a preface in each book as Aristotle does in the works he calls exoteric. The cicero seat (EA-CORPORA-13/03) holds De finibus, the Academica and the Topica, and not the letters; it was checked first, as the design asked.",
 "why_seated": "Cicero is the first Roman reader and knows Aristotle as the author of dialogues with prefaces in his own voice. The letter shows a reader in 54 BCE taking the exoteric works as Aristotle's form, before the treatises circulated under the name.",
 "research": research("design §5 (Cicero, Ad Atticum IV.16.2, the Cicero seat to be checked first)"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING, "cross_references": ["cicero (EA-CORPORA-13/03)"]})

specs.append({
 "corpus": "schleiermacher-platons-werke-1804", "seat": "EA-CORPORA-32/07",
 "title": "Schleiermacher, Platons Werke I.1 (Berlin, 1804), with the general Einleitung",
 "language": "deu", "fetched": "2026-11-02",
 "license": {"payload": "Platons Werke von F. Schleiermacher, Ersten Theiles erster Band (Berlin: Realschulbuchhandlung, 1804) is public domain everywhere; Schleiermacher died in 1834. The OCR layer is the Archive's, made from the Bayerische Staatsbibliothek's scan.", "record": REC},
 "normalization": NORM_IA + NORM_OCR,
 "items": [{"kind": "ia_ref", "slug": "schleiermacher-1804-i1", "identifier": "10237328bsb", "scan": "10237328bsb.pdf",
            "work": "Platons Werke von F. Schleiermacher, Ersten Theiles erster Band (Berlin: Realschulbuchhandlung, 1804): the Einleitung, then Phaedrus, Lysis, Protagoras, Laches with their introductions — Internet Archive 10237328bsb (Bayerische Staatsbibliothek), the OCR layer"}],
 "loci": [
  {"label": "the Einleitung opens on Diogenes's life, set before the Greek editions", "text": "text/schleiermacher-1804-i1.ocr.txt", "find": "ein so rohes, ohne alles Urtheil zusammenge-"},
  {"label": "a natural order and a necessary relation of the dialogues to one another", "text": "text/schleiermacher-1804-i1.ocr.txt", "find": "eine natürliche Folge und eine nothwendige Be-"},
  {"label": "to restore this natural order, against all previous attempts to arrange the works", "text": "text/schleiermacher-1804-i1.ocr.txt", "find": "gen Versuchen zur Anordnung der Platonischen"}],
 "scope": "The first volume of the first edition entire in the Archive's OCR. The general Einleitung sets aside the biography from Diogenes that the Greek editions printed first, and proposes to restore the natural order (natürliche Folge) of the dialogues, in which each presupposes the effect of the one before. The second edition (1817) is on the Archive as well and is not seated.",
 "why_seated": "Schleiermacher made the order of the dialogues a question of one mind's development and put the received life aside to do it. The study reads the Einleitung as the modern founding of the order that later chronologies inherit.",
 "research": research("design §5 (Schleiermacher's Einleitung, in German) and §6"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING, "cross_references": ["plato", "diogenes-laertius (III)"]})

specs.append({
 "corpus": "campbell-sophistes-politicus", "seat": "EA-CORPORA-32/08",
 "title": "Lewis Campbell, The Sophistes and Politicus of Plato (Oxford, 1867)",
 "language": "mul", "fetched": "2026-11-02",
 "license": {"payload": "Published in Oxford by the Clarendon Press in 1867, the book is public domain everywhere; Campbell died in 1908. The Library of Congress, whose copy the Archive serves, is unaware of any copyright restriction. The OCR layer is the Archive's.", "record": REC},
 "normalization": NORM_IA + NORM_OCR,
 "items": [{"kind": "ia_ref", "slug": "campbell-1867", "identifier": "sophistespolitic00plat", "scan": "sophistespolitic00plat.pdf",
            "work": "L. Campbell, The Sophistes and Politicus of Plato, with a revised text and English notes (Oxford: Clarendon Press, 1867) — Internet Archive sophistespolitic00plat (Library of Congress), the OCR layer"}],
 "loci": [
  {"label": "General Introduction §6: structure, style and diction, illustrated from the Philebus, Timaeus and Laws", "text": "text/campbell-1867.ocr.txt", "find": "is their structure, style, and diction, which, however, receive considerable illustration from the Philebus, Timeeus, and Laws.", "note": "the page reads Timaeus; the OCR reads Timeeus"},
  {"label": "the Laws as the point of comparison", "text": "text/campbell-1867.ocr.txt", "find": "Plato afterwards embodied in the Laws."}],
 "scope": "The book entire in the Archive's OCR: the General Introduction, the introductions to each dialogue, the Greek text and the notes. In the General Introduction Campbell groups the Sophist and Statesman with the Philebus, Timaeus and Laws by their vocabulary and diction, an early argument from style for a late group of dialogues.",
 "why_seated": "Campbell's test made the order of the dialogues a count of words, and the count assumes one writer whose style moves in one direction. The study reads it as the method that fixed the late group the later chronologies keep.",
 "research": research("design §5 (Campbell, The Sophistes and Politicus of Plato, 1867)"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING, "cross_references": ["plato"]})

specs.append({
 "corpus": "tennemann-platonische-philosophie", "seat": "EA-CORPORA-32/09",
 "title": "Wilhelm Gottlieb Tennemann, System der Platonischen Philosophie I (Leipzig, 1792) and Geschichte der Philosophie II (Leipzig, 1799)",
 "language": "deu", "fetched": "2026-11-02",
 "license": {"payload": "Both books were published in Leipzig by Barth (1792; 1799) and are public domain everywhere; Tennemann died in 1819. The OCR layers are the Archive's.", "record": REC},
 "normalization": "The Archive's OCR text layers (_djvu.txt), line endings normalized; the scans are held by reference with the Archive's md5. " + NORM_OCR,
 "items": [
  {"kind": "ia_ref", "slug": "tennemann-system-1792-i", "identifier": "systemderplaton00tenngoog", "scan": "systemderplaton00tenngoog.pdf",
   "work": "W. G. Tennemann, System der Platonischen Philosophie, vol. I (Leipzig: Barth, 1792), with the life of Plato and the part on the order of the writings — Internet Archive systemderplaton00tenngoog (Oxford, digitized by Google), the OCR layer"},
  {"kind": "ia_ref", "slug": "tennemann-geschichte-1799-ii", "identifier": "bub_gb_NPMGAAAAcAAJ", "scan": "bub_gb_NPMGAAAAcAAJ.pdf",
   "work": "W. G. Tennemann, Geschichte der Philosophie, vol. II (Leipzig: Barth, 1799), with Plato's writings and philosophy — Internet Archive bub_gb_NPMGAAAAcAAJ (digitized by Google), the OCR layer"}],
 "loci": [
  {"label": "System I, part two: on the chronological order of the Platonic writings", "text": "text/tennemann-system-1792-i.ocr.txt", "find": "Ueber die Zeitfolge der Platonifchen Schriften.", "note": "the page reads Platonischen with a long s; the OCR reads Platonifchen"},
  {"label": "System I: it matters for no writer when he made a given writing, least of all for Plato", "text": "text/tennemann-system-1792-i.ocr.txt", "find": "Schrift verfertiger hat, am allerwenigſten aber beim", "note": "the page reads verfertiget; the OCR reads verfertiger"},
  {"label": "Geschichte II: the running head over the account of Plato's writings and philosophy", "text": "text/tennemann-geschichte-1799-ii.ocr.txt", "find": "Platons Schriften und Philoſophie."}],
 "scope": "Two books entire in the Archive's OCR (Fraktur, read with errors). The System sets out Plato's life, then the chronological order of the writings, then the system extracted from them; the second volume of the Geschichte gives Plato's writings and philosophy again in the history's frame, and is the volume Hegel's notes to the lectures on Plato cite as Tennemann B. II (32/10).",
 "why_seated": "Tennemann is the reader Hegel faults for extracting the determinations of the dialogues as a finished system and losing their movement. The study reads the books Hegel read.",
 "research": research("design §6 (Hegel's reading of Tennemann's Plato)"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING, "cross_references": ["hegel (32/10)", "plato"]})

HEG, DIF = leaves("hegel-gdp2-1833"), leaves("hegel-differenz-1801")
specs.append({
 "corpus": "hegel", "seat": "EA-CORPORA-32/10",
 "title": "Hegel, Differenz des Fichte'schen und Schelling'schen Systems der Philosophie (Jena, 1801), and the lectures on Plato in the Vorlesungen über die Geschichte der Philosophie II (Werke XIV, Berlin, 1833)",
 "language": "deu", "fetched": "2026-11-02",
 "license": {"payload": "Hegel (d. 1831) is public domain, as are the Differenzschrift (Jena: Seidler, 1801) and Michelet's edition of the lectures in the Werke (Berlin: Duncker und Humblot, 1833); Michelet died in 1893. The OCR was made in session from the Archive's page images (the Bayerische Staatsbibliothek's scan of 1801 and Google's of 1833) and is released with this seat record.", "record": REC},
 "normalization": "The Archive's own OCR of both books reads the Fraktur with many errors and is not used. The leaves named in origin.items were OCR'd in session with the Fraktur model; the OCR of each leaf is kept under original/, and the page images are held by URL and sha256. " + NORM_OCR,
 "units": "one text file per book",
 "items": [
  {"kind": "ocr_pages", "slug": "differenz-1801", "identifier": "10045974", "pages": DIF, "ocr_prefix": "hegel-differenz-1801", "images_dir": f"{SCR}/dif", "ocr_engine": ENGINE_FRAK,
   "why": "the Archive's own OCR layer reads the Fraktur with many errors; the leaves were OCR'd in session with the Fraktur model and the images are held by reference",
   "work": f"G. W. F. Hegel, Differenz des Fichte'schen und Schelling'schen Systems der Philosophie in Beziehung auf Reinhold's Beyträge zur leichtern Uebersicht des Zustands der Philosophie zu Anfang des neunzehnten Jahrhunderts, 1stes Heft (Jena: Seidler, 1801) — Internet Archive 10045974 (Bayerische Staatsbibliothek), leaves n{DIF[0] if DIF else '?'}–n{DIF[-1] if DIF else '?'}, OCR in session"},
  {"kind": "ocr_pages", "slug": "gdp2-plato-1833", "identifier": "bub_gb_4ZpBzREnAIMC", "pages": HEG, "ocr_prefix": "hegel-gdp2-1833", "images_dir": f"{SCR}/heg", "ocr_engine": ENGINE_FRAK,
   "why": "the Archive's own OCR layer reads the Fraktur with many errors; the leaves were OCR'd in session with the Fraktur model and the images are held by reference",
   "work": f"G. W. F. Hegel, Vorlesungen über die Geschichte der Philosophie II, ed. K. L. Michelet, Werke XIV (Berlin: Duncker und Humblot, 1833), the first part of the lecture on Plato, pp. 169–241 (the life, the writings and the dialectic) — Internet Archive bub_gb_4ZpBzREnAIMC (digitized by Google), leaves n{HEG[0] if HEG else '?'}–n{HEG[-1] if HEG else '?'}, OCR in session"}],
 "loci": [{"label": "Differenz, the Vorerinnerung", "text": "text/differenz-1801.ocr.txt", "find": "Vorerinnerung"}, {"label": "Differenz: the living spirit that dwells in a philosophy asks to be born of a kindred spirit", "text": "text/differenz-1801.ocr.txt", "find": "Der lebendige Geiſt, der", "note": "the OCR keeps the long s"}, {"label": "Differenz: division is the source of the need of philosophy", "text": "text/differenz-1801.ocr.txt", "find": "Quell des Bedürfniſſes der Philoſophie", "note": "the line before reads 'Entzweiung ist der'; the OCR reads Entzweigung"}, {"label": "Differenz: when the power of union vanishes from the life of people and the oppositions lose their living relation", "text": "text/differenz-1801.ocr.txt", "find": "Macht der Vereinigung: aus dem: Le-", "note": "the page reads 'die Macht der Vereinigung aus dem Leben der Menschen verschwindet, und die Gegensätze ihre lebendige Beziehung und Wechselwirkung verloren'; the OCR of this leaf is damaged at the gutter"}, {"label": "Lectures, the heading of the period: Plato and Aristotle", "text": "text/gdp2-plato-1833.ocr.txt", "find": "Erſter Periode dritte Abtheilung: Plato und Ariſtoteles."}, {"label": "Lectures: exoteric and esoteric philosophy, with Tennemann cited", "text": "text/gdp2-plato-1833.ocr.txt", "find": "det exoteriſche und eſoteriſche Philoſophie. Tennemann *) ſagt:", "note": "the line begins Man unterschei-; the note cites Tennemann Band II, S. 220"}, {"label": "Lectures: the most important thing in Plato's philosophy is not grasped at all in Tennemann", "text": "text/gdp2-plato-1833.ocr.txt", "find": "in der platoniſchen Philoſophie iſt bei Tennemann gerade gar nicht aufgefaßt", "note": "the page reads Wichtigste; the OCR reads Widhtigſte"}, {"label": "Lectures: the higher sense of the Philebus and Parmenides, of which Tennemann does not speak", "text": "text/gdp2-plato-1833.ocr.txt", "find": "Tennemann gar nicht davon die Rede)"}, {"label": "Lectures: the esoteric is the speculative, written and printed, and still hidden", "text": "text/gdp2-plato-1833.ocr.txt", "find": "Das Eſoteriſche iſt das Spekulative, das geſchrieben und gedru>t iſt", "note": "the page reads gedruckt; the OCR reads gedru>t"}],
 "scope": "Two books in part, OCR'd in session from the Fraktur. The Differenzschrift from its Vorerinnerung through the opening sections (leaves n7–n60; the title leaves, which the OCR found blank, are held as images by reference only): the passage on the living spirit of a philosophy, which the historical treatment turns into dead opinion, and the one locating the need of philosophy in division, where the power of union vanishes from life and the oppositions lose their living relation. The lectures on the history of philosophy, volume II, pp. 169–241 (leaves n178–n250): the opening of the period of Plato and Aristotle and the first part of the lecture on Plato, where Hegel cites Tennemann on the exoteric and esoteric, says the most important thing in Plato's philosophy is not grasped at all in Tennemann, a few determinations being gathered as dry ontological ones, and holds that the esoteric is the speculative, written and printed and still hidden from those without the interest to exert themselves. The remainder of both books is in the referenced scans; the rest of the lectures is declared at 32/11.",
 "why_seated": "Hegel is a dated witness that the received presentations of Plato kept the writings and lost their operation: the Differenzschrift locates philosophy's need where oppositions are fixed apart, and the lectures fault Tennemann for extracting Plato's determinations as a system. The study reads him at the edge of the closing it describes.",
 "research": research("design §6 (Hegel as a reader of the closing) and §5"),
 "spine": "EA-CORPORA-32", "ruling": RULING, "seating": SEATING, "cross_references": ["tennemann-platonische-philosophie (32/09)", "plato"]})

specs.append({
 "corpus": "nicolaus-damascenus", "seat": "EA-CORPORA-32/12",
 "title": "Nicolaus of Damascus: the fragments (Müller, FHG III, from the DFHG), the De plantis restored to his name (Meyer, 1841), and the Basel Theophrastus of 1541 with the scholion that cites him",
 "language": "mul", "fetched": "2026-11-02",
 "license": {"payload": "Nicolaus of Damascus (b. c. 64 BCE) is public domain, as are the witnesses quoted. Müller's FHG III (Paris: Didot, 1849) is public domain everywhere; the DFHG states that its contents are licensed CC BY-SA 4.0, redistributed under the same licence and attributed to the Digital Fragmenta Historicorum Graecorum (Leipzig). Meyer's Nicolai Damasceni De plantis (Leipzig: Voss, 1841) is public domain; the scan is the Bibliothèque interuniversitaire de santé's, under the Licence ouverte (Etalab), and its OCR layer is the Archive's. The Basel Theophrastus (Oporinus, 1541) is public domain; the Archive marks the item Public Domain Mark 1.0; its leaves are held by URL and sha256 and the transcription was made in session.", "record": REC},
 "normalization": "Three items. The DFHG response as served (JSON) is the original, reduced to one block per fragment by build31.py. Meyer 1841: the Archive's OCR layer, line endings normalized, the scan held by reference. Basel 1541: the Archive's OCR reads the Greek fount as Latin and is held only for the volume's Latin contents; leaves n290–n294 are held as images, with the title, running heads, the hinge and the scholion transcribed by eye in session (transcriptions/), a reading to be checked against the image. " + NORM_OCR,
 "units": "one text file per item",
 "items": [
  {"kind": "dfhg", "slug": "nicolaus-damascenus-fhg", "url": "http://www.dfhg-project.org/DFHG/api.php?author=NICOLAUS%20DAMASCENUS", "path": "dfhg/NICOLAUS-DAMASCENUS.json",
   "work": "Nicolaus Damascenus, fragmenta (Histories, Collection of Remarkable Customs, Life of Augustus, On His Own Life), in C. Müller, Fragmenta Historicorum Graecorum III (Paris: Didot, 1849), pp. 348–464 — DFHG, author NICOLAUS DAMASCENUS"},
  {"kind": "ia_ref", "slug": "meyer-1841-de-plantis", "identifier": "BIUSante_90960x127x01", "scan": "BIUSante_90960x127x01.pdf",
   "work": "Nicolai Damasceni De plantis libri duo Aristoteli vulgo adscripti, ex Isaaci ben Honain versione arabica Latine vertit Alfredus, ed. E. H. F. Meyer (Leipzig: Voss, 1841) — Internet Archive BIUSante_90960x127x01 (Bibliothèque interuniversitaire de santé), the OCR layer"},
  {"kind": "ia_ref", "slug": "basel-1541-contents", "identifier": "b3355142x", "scan": "b3355142x.pdf",
   "work": "Theophrastus, Opera (Basel: Oporinus, 1541), the Archive's OCR layer, held for the Latin contents — Internet Archive b3355142x"},
  {"kind": "page_images", "slug": "basel-1541-metaphysics", "identifier": "b3355142x", "pages": [290, 291, 292, 293, 294], "images_dir": f"{SCR}/bas",
   "transcription": "basel-1541-theophrastus-transcription.txt",
   "work": "Theophrastus, Opera (Basel: Oporinus, 1541), pp. 267–271: ΘΕΟΦΡΑΣΤΟΥ ΤΩΝ ΜΕΤΑ ΤΑ ΦΥΣΙΚΑ, its running heads, and the scholion after it — Internet Archive b3355142x, leaves n290–n294, transcribed in session"}],
 "loci": [
  {"label": "On His Own Life, fr. 2: Nicolaus a zealot of Aristotle", "text": "text/nicolaus-damascenus-fhg.txt", "find": "ζηλωτὴς γὰρ Ἀριστοτέλους γενόμενος"},
  {"label": "Meyer 1841, the title: the two books of the De plantis, commonly ascribed to Aristotle, as Nicolaus's", "text": "text/meyer-1841-de-plantis.ocr.txt", "find": "NICOLAI DAMASCENI DE PLANTIS LIBRI DUO ARISTOTELI VULGO ADSCRIPTI."},
  {"label": "Meyer 1841, Praefatio: the book is Nicolaus's and not Aristotle's", "text": "text/meyer-1841-de-plantis.ocr.txt", "find": "Nicolai est, nec Aristotelis."},
  {"label": "Basel 1541, the contents: Aristotle's De plantis inside the Theophrastus volume", "text": "text/basel-1541-contents.ocr.txt", "find": "Aviftotelis De plantis, lib. 11. 198", "note": "the page reads Aristotelis … lib. II.; the OCR reads Aviftotelis … lib. 11."},
  {"label": "Basel 1541, p. 267: the title", "text": "text/basel-1541-metaphysics-transcription.txt", "find": "ΘΕΟΦΡΑΣΤΟΥ ΤΩΝ ΜΕΤΑ ΤΑ ΦΥΣΙΚΑ."},
  {"label": "Basel 1541, p. 271: the scholion, Nicolaus's ascription", "text": "text/basel-1541-metaphysics-transcription.txt", "find": "Νικόλαος δὲ ἐν τῇ θεωρίᾳ τῶν Ἀριστοτέλους μετὰ τὰ φυσικὰ μνημονεύει αὐτοῦ, λέγων εἶναι Θεοφράστου"},
  {"label": "Basel 1541, p. 271: the end of the volume's Theophrastus", "text": "text/basel-1541-metaphysics-transcription.txt", "find": "ΤΕΛΟΣ ΤΩΝ ΘΕΟΦΡΑΣΤΟΥ."}],
 "scope": "Three witnesses to Nicolaus of Damascus as the scholion of Theophrastus's Metaphysics names him. (1) His fragments as Müller collected them, 165 in the DFHG, among them On His Own Life, where he is called a zealot of Aristotle (fr. 2). (2) Meyer's edition of the Latin De plantis, from Isaac ben Honain's Arabic through Alfred of Sareshel, which restores to Nicolaus the two books on plants transmitted as Aristotle's (the Greek is in Bekker's Aristotle and in the aristotle seat, tlg039). (3) The Basel Theophrastus of 1541, which the bookseller's description bound with the Archive's scan calls, after Schweiger, the first separate edition of the complete works (\"Erste besondere Ausgabe der sämtlichen Werke\"): it prints Aristotle's De plantis inside the Theophrastus volume (p. 198), and prints the Metaphysics as Theophrastus's (pp. 267–271) under the running heads ΘΕΟΦΡΑΣΤΟΥ and ΤΩΝ ΜΕΤΑ ΤΑ ΦΥΣΙΚΑ, the scholion after it, and ΤΕΛΟΣ ΤΩΝ ΘΕΟΦΡΑΣΤΟΥ. Nicolaus's On the Philosophy of Aristotle, which the scholion cites, survives in a Syriac compendium (Cambridge University Library, Gg. 2.14) and is edited by Drossaart Lulofs (Leiden: Brill, 1965), in copyright and declared at 32/11.",
 "why_seated": "Nicolaus is where the second name enters for Theophrastus's Metaphysics (draft §3.4), and a work of his own, the De plantis, travelled under Aristotle's name until Meyer restored it. The 1541 Basel volume prints the Metaphysics among Theophrastus's works, apart from Aristotle's, with the scholion still after it.",
 "research": research("draft §3.4–§3.5 and §3.13 (Nicolaus's ascription and its ground), added to the seating at the operator's word of 2026-11-02 ('yes, lets grab them, but fold into 32 and version')"),
 "spine": "EA-CORPORA-32", "ruling": RULING + " Extended 2026-11-02 at the operator's word ('lets grab nicolaus'; 'yes, lets grab them, but fold into 32 and version').", "seating": SEATING,
 "cross_references": ["aristotle (tlg039, De plantis)", "aldine-aristotle-1497 (32/02)", "theophrastus (EA-CORPORA-09/01)", "hermippus (31/06)"]})

if __name__ == "__main__":
  for s in specs:
    (H / f"spec32-{s['corpus']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(s["corpus"], len(s["loci"]))
