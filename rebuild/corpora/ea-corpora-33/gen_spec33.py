#!/usr/bin/env python3
"""Writes the EA-CORPORA-33 specs (spec33-<corpus>.json). Session tool. Song and silence: Tacitus, and all of Sappho with the
melic poets. The page ranges of the session-OCR seats are found from the running heads of the OCR present under the
scratch ocr/ folder when this runs (heads() below), and stated in each spec."""
import json, pathlib, re
H = pathlib.Path(__file__).resolve().parent
OCR = pathlib.Path("/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/ea33/ocr")
PL = "bfdcd062840c67dc85993eb942fcc75e68457f6d"   # PerseusDL/canonical-latinLit, HEAD on 2026-11-04 (git ls-remote)
PG = "282e6f5a3ec12e6ca67e44cd4fa3487526e3b421"   # PerseusDL/canonical-greekLit, HEAD on 2026-11-04 (git ls-remote)
RULING = ("Lee Sharks, 2026-11-04: \"and I suppose we should seat tacitus\" (11:28 EST); \"we currently have only sappho 31 i believe. we need all sappho and all "
          "the melic poets. what an oversight. they can go together with tacitus, song and silence at one seat\" (11:29 EST); \"corinna definitely... im not familiar "
          "with telesilla or the carmina popularia but yet lets seat the\" (11:46 EST); on Edmonds, \"yes, lets seat it with the statement\" (11:54 EST).")
AUTH = ("Lee Sharks, 2026-11-04 11:46 EST: \"i feel that probably rebekah cranes should be the standing authority on the ea-corpora deposits\".")
SEATING = "EA-CORPORA-33, the thirty-third seating: song and silence — Tacitus, and Sappho whole with the melic poets, 2026-11-04"
REC = "CC-BY-4.0 applies to this seat record only."
NORM_TEI = ("Originals as fetched under original/, pinned to a commit of the repository named in origin.items. text/<slug>.txt is the TEI reduced to plain "
            "text by seat.py (rebuild/corpora/ea-corpora-27), notes and apparatus dropped, divisions kept. No text was corrected by hand.")
NORM_PDF = ("The Archive's own OCR layer of this volume reads the Greek as Latin and is not used. The PDF named in origin.items was rasterized page by page at "
            "300 dpi (pdftoppm -r 300 -gray) and each page OCR'd in session; the OCR is kept as made, line endings normalized, one '=== p<N> ===' line before "
            "each PDF page. No text was corrected by hand; the loci keep the OCR's readings and say where those differ from the printed page.")
TD = "raw.githubusercontent.com/tesseract-ocr/tessdata_best, main"
SHA = {"grc": "dfc9bda286cd9d8755b1832e5731a5425d1cf0803393a5fa6dee078466178cf1", "lat": "60054dd32ac03ebd9b4f87d0665bd491a7ffe0d3ee99ceb91aefaf348b65e94f",
       "eng": "7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2"}
ENG = lambda langs: {"engine": "Tesseract 5.3.4", "models": f"tessdata_best {langs} ({TD})",
                     "sha256": {f"{l}.traineddata": SHA[l] for l in langs.split("+")},
                     "command": f"pdftoppm -r 300 -gray -f N -l N; tesseract pN.png pN -l {langs}", "run": "2026-11-04, in session"}
BERGK = {"identifier": "poetaelyricigrae03berguoft", "pdf": "poetaelyricigrae03berguoft.pdf", "pdf_md5": "2c6ebcb7fc54793b4769bc8f4e1e36dc",
         "pdf_sha256": "2dcf282a79db5359feed6fa1934d81a0addd8103ec683f51af4e41b5cb7a4265", "pdf_pages": 764, "ocr_prefix": "bergk3", "ocr_engine": ENG("grc+lat")}
EDM = {"identifier": "lyragraecabeingr01edmouoft", "pdf": "lyragraecabeingr01edmouoft.pdf", "pdf_md5": "1784860d7abc47b281e1233d191569dd",
       "pdf_sha256": "0cc83c7ff7c8dab26f114500f9f54800a091c54f2e733d14fcffb7990f0bfccf", "pdf_pages": 490, "ocr_prefix": "edmonds1", "ocr_engine": ENG("grc+eng")}
LIC_BERGK = ("The melic poets are public domain. Bergk's Poetae Lyrici Graeci, 4th edition, vol. III (Leipzig: Teubner, 1882) is public domain everywhere; "
             "Bergk died in 1881. The Archive marks the scan's source (Toronto) as public domain. The OCR was made in session and is released with this seat record.")
LIC_EDM = ("Sappho and Alcaeus are public domain. J. M. Edmonds, Lyra Graeca I (London: Heinemann; New York: Putnam, Loeb Classical Library, 1922) is public "
           "domain in the United States (published before 1929); Edmonds died in 1958, so in jurisdictions with a term of the author's life plus seventy years "
           "the edition's own text, translation and notes remain protected until the end of 2028. The seat holds it with that statement, at the operator's word "
           "of 2026-11-04, for the papyri published after 1882 that Bergk cannot carry. The Archive marks the item NOT_IN_COPYRIGHT. The OCR was made in session.")


def research(section):
    return {"study": "The Portents Before the Fall: Josephus, Tacitus and the Apocalypse (#1737) and the Sappho line (Sappho 31, the reception operator of #1494–#1495)",
            "design": "rebuild/corpora/ea-corpora-33/NOTE.md", "draft": "drafts/THREE-WITNESSES-PORTENTS-draft-2026-11-04.md",
            "locus_table": "the correspondence table of #1737 §4", "owed_at": "the operator's requests of 2026-11-04", "for": section}


def tei(base, commit, cat, g, w, ed, slug, work):
    f = f"data/{g}/{w}/{g}.{w}.{ed}.xml"
    return {"kind": "tei", "slug": slug, "url": f"https://raw.githubusercontent.com/{base}/{commit}/{f}", "path": f"perseus/{g}.{w}.{ed}.xml",
            "source": f"Perseus Digital Library, {cat}", "repository": f"https://github.com/{base}", "commit": commit, "file": f, "work": work}


def heads(prefix, names, last):
    """first PDF page whose first three OCR lines carry each running-head name, in page order"""
    runs, prev = [], None
    for p in range(1, last + 1):
        f = OCR / f"{prefix}-p{p}.txt"
        if not f.exists():
            continue
        hd = "\n".join(f.read_text(errors="ignore").strip().split("\n")[:3]).upper()
        hit = next((n for n in names if n in hd), None)
        if hit and hit != prev:
            runs.append((p, hit)); prev = hit
    return runs


def span(runs, name, last):
    for i, (p, n) in enumerate(runs):
        if n == name:
            nxt = next((q for q, m in runs[i + 1:] if m != name), last + 1)
            return list(range(p, nxt))
    return []


def pdf_item(base, slug, pages, work):
    return dict(base, kind="pdf_ocr", slug=slug, pages=pages, work=work)


specs = []
LAT = lambda w, s, t: tei("PerseusDL/canonical-latinLit", PL, "canonical-latinLit", "phi1351", w, "perseus-lat2", s, t)
specs.append({
 "corpus": "tacitus", "seat": "EA-CORPORA-33/01",
 "title": "Tacitus, the five works in Latin: Agricola, Germania and Dialogus (Furneaux, 1899–1900), the Histories (Fisher, 1911) and the Annals (Fisher, 1906)",
 "language": "lat", "fetched": "2026-11-04",
 "license": {"payload": "Tacitus is public domain. Furneaux's Opera minora (Oxford: Clarendon Press, 1899–1900; Furneaux died 1908) and Fisher's Historiae (1911) and Annales (1906) (Oxford Classical Texts; Fisher died 1916) are public domain everywhere. The TEI is the Perseus Digital Library's, CC BY-SA 4.0, redistributed under the same licence and attributed to Perseus.", "record": REC},
 "normalization": NORM_TEI,
 "items": [LAT("phi001", "agricola", "Tacitus, De vita Iulii Agricolae, ed. H. Furneaux, Cornelii Taciti Opera minora (Oxford, 1899–1900) — Perseus TEI phi1351.phi001.perseus-lat2"),
           LAT("phi002", "germania", "Tacitus, Germania, ed. H. Furneaux (Oxford, 1899–1900) — Perseus TEI phi1351.phi002.perseus-lat2"),
           LAT("phi003", "dialogus", "Tacitus, Dialogus de oratoribus, ed. H. Furneaux (Oxford, 1899–1900) — Perseus TEI phi1351.phi003.perseus-lat2"),
           LAT("phi004", "historiae", "Tacitus, Historiae, ed. C. D. Fisher (Oxford: Clarendon Press, 1911) — Perseus TEI phi1351.phi004.perseus-lat2"),
           LAT("phi005", "annales", "Tacitus, Annales, ed. C. D. Fisher (Oxford: Clarendon Press, 1906) — Perseus TEI phi1351.phi005.perseus-lat2")],
 "loci": [
  {"label": "Hist. 5.1, the year that opens Book 5: Titus chosen to finish Judaea", "text": "text/historiae.txt", "find": "Eiusdem anni principio Caesar Titus, perdomandae Iudaeae delectus a patre"},
  {"label": "Hist. 5.13, the prodigies: armies in the sky, the temple lit by fire from the clouds", "text": "text/historiae.txt", "find": "visae per caelum concurrere acies, rutilantia arma et subito nubium igne conlucere templum"},
  {"label": "Hist. 5.13, the doors of the shrine opened, and the voice: the gods are departing", "text": "text/historiae.txt", "find": "apertae repente delubri fores et audita maior humana vox excedere deos; simul ingens motus excedentium"},
  {"label": "Hist. 5.13, the oracle in the ancient writings of the priests", "text": "text/historiae.txt", "find": "antiquis sacerdotum litteris contineri eo ipso tempore fore ut valesceret Oriens profectique Iudaea rerum potirentur"},
  {"label": "Ann. 15.44, the Christians under Nero", "text": "text/annales.txt", "find": "Christianos appellabat"}],
 "scope": "The five works entire in the Perseus TEI: the Agricola, Germania and Dialogus, the surviving books of the Histories (I–V.26) and of the Annals (I–VI, XI–XVI). Held above all for Histories 5.13, the undated account of the portents before the siege of Jerusalem, set against Josephus BJ 6.288–315 (seat josephus) and the Apocalypse in #1737.",
 "why_seated": "Tacitus gives the signs that preceded the fall of the Temple without a date, inside his narrative of the year 70: the undated witness of the three set side by side in The Portents Before the Fall (#1737). Seated whole, in Latin, so that the passage is read in its book.",
 "research": research("#1737 §2–§4 (Hist. 5.1 and 5.13, read there from the pinned Perseus file)"),
 "spine": "EA-CORPORA-33", "ruling": RULING, "seating": SEATING,
 "cross_references": ["josephus (EA-CORPORA-01/01, BJ 6.288–315)", "gnt-nestle1904 (01/04, Revelation)", "lxx-swete (01/05, 2 Maccabees 5)"]})

GRK = lambda g, w, s, t: tei("PerseusDL/canonical-greekLit", PG, "canonical-greekLit", g, w, "perseus-grc2", s, t)
specs.append({
 "corpus": "pindar", "seat": "EA-CORPORA-33/02",
 "title": "Pindar, the four books of victory odes (Olympian, Pythian, Nemean, Isthmian), in Sandys's Greek (Loeb Classical Library)",
 "language": "grc", "fetched": "2026-11-04",
 "license": {"payload": "Pindar is public domain. Sandys's Greek text (The Odes of Pindar, Loeb Classical Library, 1915; the Perseus file follows the 1937 printing) is public domain in the European Union (Sandys died 1922). The TEI is the Perseus Digital Library's, CC BY-SA 4.0, redistributed under the same licence and attributed to Perseus.", "record": REC},
 "normalization": NORM_TEI,
 "items": [GRK("tlg0033", "tlg001", "olympian", "Pindar, Olympian Odes, ed. J. Sandys (Loeb) — Perseus TEI tlg0033.tlg001.perseus-grc2"),
           GRK("tlg0033", "tlg002", "pythian", "Pindar, Pythian Odes, ed. J. Sandys (Loeb) — Perseus TEI tlg0033.tlg002.perseus-grc2"),
           GRK("tlg0033", "tlg003", "nemean", "Pindar, Nemean Odes, ed. J. Sandys (Loeb) — Perseus TEI tlg0033.tlg003.perseus-grc2"),
           GRK("tlg0033", "tlg004", "isthmian", "Pindar, Isthmian Odes, ed. J. Sandys (Loeb) — Perseus TEI tlg0033.tlg004.perseus-grc2")],
 "loci": [{"label": "Ol. 1.1, the opening of the first ode", "text": "text/olympian.txt", "find": "ἄριστον μὲν ὕδωρ, ὁ δὲ χρυσὸς αἰθόμενον πῦρ"},
          {"label": "Pyth. 8.95–96, the dream of a shadow", "text": "text/pythian.txt", "find": "σκιᾶς ὄναρ"}],
 "scope": "The four books of epinicians entire. The fragments (paeans, dithyrambs, partheneia, threnoi) are not in the Perseus files; they are queued to Bergk's Poetae Lyrici Graeci, 4th edition, vol. I (1878).",
 "why_seated": "Pindar is the ninth of the nine lyric poets and the only one whose books survive; the seat carries the canon whose other members survive in fragments.",
 "research": research("the melic canon, requested whole"),
 "spine": "EA-CORPORA-33", "ruling": RULING, "seating": SEATING,
 "queued": ["Pindar's fragments in Bergk, PLG⁴ I (1878), public domain: not OCR'd this session"]})

specs.append({
 "corpus": "bacchylides", "seat": "EA-CORPORA-33/03",
 "title": "Bacchylides, the epinicians and dithyrambs, in Jebb's Greek (Cambridge, 1905)",
 "language": "grc", "fetched": "2026-11-04",
 "license": {"payload": "Bacchylides is public domain. Jebb's Bacchylides: The Poems and Fragments (Cambridge: Cambridge University Press, 1905) is public domain everywhere; Jebb died in 1905. The TEI is the Perseus Digital Library's, CC BY-SA 4.0, redistributed under the same licence and attributed to Perseus.", "record": REC},
 "normalization": NORM_TEI,
 "items": [GRK("tlg0199", "tlg001", "epinicians", "Bacchylides, Epinicians, ed. R. C. Jebb (Cambridge, 1905) — Perseus TEI tlg0199.tlg001.perseus-grc2"),
           GRK("tlg0199", "tlg002", "dithyrambs", "Bacchylides, Dithyrambs, ed. R. C. Jebb (Cambridge, 1905) — Perseus TEI tlg0199.tlg002.perseus-grc2")],
 "loci": [{"label": "Ode 3, Croesus on the pyre", "text": "text/epinicians.txt", "find": "Κροῖσον ὁ χρυσά[ορος"},
          {"label": "Dithyramb 17 (Theseus), the ship carrying Theseus and the twice seven", "text": "text/dithyrambs.txt", "find": "Θησέα δὶς ἑπτά τʼ ἀγλαοὺς ἄγουσα"}],
 "scope": "The fourteen epinicians and six dithyrambs of the London papyrus (published 1897), in Jebb's text.",
 "why_seated": "Bacchylides came back from the sand in 1897; his seat stands beside the fragments of the others as the melic canon's second recovered book.",
 "research": research("the melic canon, requested whole"),
 "spine": "EA-CORPORA-33", "ruling": RULING, "seating": SEATING})

# Bergk III divided at its running heads (split_bergk33.py prints the runs; the corrections below are made by reading the pages):
# p1-15 front matter and the note on Olympus; p16 Eumelus; p49 is an Alcman page whose head the OCR reads as ARION; p208-214 hold
# the short sections IX-XVI (Pittacus, Bias, Thales, Cleobulus, Echembrotus, Sacadas, and section XVI) before Stesichorus at p215.
B_RUNS = [("front matter, the preface and the note on Olympus", 1, 15), ("Eumelus", 16, 16), ("Terpander", 17, 21), ("Alcman", 22, 87), ("Arion", 88, 91),
          ("Sappho", 92, 149), ("Erinna", 150, 155), ("Alcaeus", 156, 207), ("Pittacus, Bias, Thales, Cleobulus, Echembrotus, Sacadas (sections IX–XVI)", 208, 214),
          ("Stesichorus", 215, 243), ("Ibycus", 244, 261), ("Anacreon", 262, 305), ("Anacreontea", 306, 347), ("Appendix Anacreonteorum", 348, 385),
          ("Lasus", 386, 387), ("Apollodorus, Tynnichus and Telesilla", 388, 391), ("Simonides", 392, 545), ("Timocreon", 546, 551), ("Corinna", 552, 563),
          ("Lamprocles", 564, 565), ("Pratinas", 566, 569), ("Phrynichus and Diagoras", 570, 573), ("Cydias and Praxilla", 574, 577), ("Bacchylides (the fragments, before the London papyrus)", 578, 597),
          ("Melanippides and Cinesias", 598, 603), ("Ariphron and Licymnius", 604, 609), ("Philoxenus", 610, 627), ("Timotheus", 628, 635), ("Telestes", 636, 641),
          ("Lycophronides and Castorio", 642, 645), ("Hermodotus", 646, 649), ("Scolia", 650, 663), ("Carmina popularia", 664, 695), ("Fragmenta adespota", 696, 755),
          ("Index poetarum", 756, 764)]
slug = lambda n: re.sub(r"[^a-z]+", "-", n.lower().split(" (")[0]).strip("-")[:40]
B_ITEMS = [pdf_item(BERGK, "bergk-" + slug(n), list(range(a, b + 1)),
                    f"Th. Bergk, Poetae Lyrici Graeci, 4th ed., vol. III, Poetae melici (Leipzig: Teubner, 1882): {n} — PDF pages {a}–{b}") for n, a, b in B_RUNS]
specs.append({
 "corpus": "poetae-melici-bergk", "seat": "EA-CORPORA-33/04",
 "title": "Bergk, Poetae Lyrici Graeci, 4th edition, vol. III: Poetae melici (Leipzig: Teubner, 1882) — the melic poets whole, from Terpander and Alcman to the Carmina popularia and the adespota",
 "language": "mul", "fetched": "2026-11-04",
 "license": {"payload": LIC_BERGK, "record": REC},
 "normalization": NORM_PDF + " The volume is divided into works at its running heads (rebuild/corpora/ea-corpora-33/split_bergk33.py), corrected by reading the boundary pages; a page carrying the end of one section and the start of the next goes with the later. Bergk's Greek is printed with his Latin apparatus beneath; the OCR keeps both.",
 "items": B_ITEMS,
 "loci": [
  {"label": "Sappho 1 (Bergk), the hymn to Aphrodite: its first word", "text": "text/bergk-sappho.ocr.txt", "find": "Ποικιλόϑρον᾽, ἀϑάνατ᾽", "note": "the page reads Ἀφρόδιτα after it; the OCR reads Aqpódua"},
  {"label": "Sappho 2 (Bergk; 31 in later numbering), the opening line", "text": "text/bergk-sappho.ocr.txt", "find": "Φαίνεταί μοι κῆνος ἴσος ϑέοισιν"},
  {"label": "Alcman, the Louvre Partheneion: there is a vengeance of the gods", "text": "text/bergk-alcman.ocr.txt", "find": "ἔστι τις σιῶν τίσις"},
  {"label": "Corinna, the rebuke of Myrtis", "text": "text/bergk-corinna.ocr.txt", "find": "Μέμφομη δὲ κὴ λιγουρὰν Μουρτίδ᾽ ἰώνγα"},
  {"label": "Telesilla, the section's running head", "text": "text/bergk-apollodorus-tynnichus-and-telesilla.ocr.txt", "find": "TELESILLA. 381"},
  {"label": "Carmina popularia, the Rhodian swallow song", "text": "text/bergk-carmina-popularia.ocr.txt", "find": "ἦλϑε χελιδών"}],
 "scope": "The volume entire in session OCR, 764 PDF pages, divided at its running heads into 35 sections: Eumelus, Terpander, Alcman, Arion, Sappho, Erinna, Alcaeus, the sages' songs, Stesichorus, Ibycus, Anacreon with the Anacreontea, Lasus, Telesilla, Simonides, Timocreon, Corinna, Lamprocles, Pratinas, Diagoras, Praxilla, the Bacchylides fragments, Melanippides, Licymnius, Philoxenus, Timotheus, Telestes, Castorio, Hermodotus, the scolia, the carmina popularia and the fragmenta adespota, with the index. Pindar is in Bergk's vol. I and seated from Perseus (33/02); the papyri published after 1882 are in Edmonds (33/05) and the papyri panel (01/11).",
 "why_seated": "The operator asked for all of Sappho and all the melic poets, seated with Tacitus: song and silence. Bergk's fourth edition is the last complete nineteenth-century collection of the melic fragments, public domain everywhere, in Greek with its Latin apparatus.",
 "research": research("the melic canon, requested whole, with Corinna, Telesilla and the Carmina popularia named"),
 "spine": "EA-CORPORA-33", "ruling": RULING, "seating": SEATING,
 "cross_references": ["sappho (EA-CORPORA-01/10)", "papyri (01/11)", "lyra-graeca-edmonds-i (33/05)", "pindar (33/02)", "bacchylides (33/03)", "theocritus (01/03)"]})

E_NAMES = ["EUMELUS", "TERPANDER", "ALCMAN", "ARION", "SAPPHO", "ALCAEUS", "INDEX"]
ER = heads("edmonds1", E_NAMES, 490)
# the first SAPPHO head (p18) falls in the volume's introduction; the poet's section opens at the second
ER = [(p, n) for p, n in ER if not (n == "SAPPHO" and p < 100)]
E_START = ER[0][0] if ER else 33
E_ITEMS = [pdf_item(EDM, "edmonds-lyra-graeca-i-front", list(range(1, E_START)), "J. M. Edmonds, Lyra Graeca I (Loeb Classical Library, 1922): title, preface, introduction and the general testimonia — Internet Archive lyragraecabeingr01edmouoft (Toronto), PDF pages 1–%d" % (E_START - 1))]
for n in E_NAMES:
    pg = span(ER, n, 490)
    if pg:
        lab = "the index" if n == "INDEX" else n.title()
        E_ITEMS.append(pdf_item(EDM, "edmonds-" + n.lower(), pg, f"J. M. Edmonds, Lyra Graeca I (1922), {lab}: Greek and facing English, with the testimonia — PDF pages {pg[0]}–{pg[-1]}"))
specs.append({
 "corpus": "lyra-graeca-edmonds-i", "seat": "EA-CORPORA-33/05",
 "title": "Edmonds, Lyra Graeca I (Loeb Classical Library, 1922): Eumelus, Terpander, Alcman, Arion, Sappho and Alcaeus, with the papyri of Oxyrhynchus",
 "language": "mul", "fetched": "2026-11-04",
 "license": {"payload": LIC_EDM, "record": REC},
 "normalization": NORM_PDF,
 "items": E_ITEMS,
 "loci": [
  {"label": "the Life of Sappho, the section's opening", "text": "text/edmonds-sappho.ocr.txt", "find": "LIFE OF SAPPHO"},
  {"label": "Sappho 31 (Edmonds's numbering differs): the opening line", "text": "text/edmonds-sappho.ocr.txt", "find": "Φαίνεταί μοι κῆνος ἴσος θέοισιν"},
  {"label": "a Sappho papyrus from Oxyrhynchus, P.Oxy. 1231, cited for the text", "text": "text/edmonds-sappho.ocr.txt", "find": "with Ox. Pap. 1231. 16 (see 15 below)", "note": "the page abbreviates Ox. Pap."},
  {"label": "Alcman, the Louvre Partheneion: there is a vengeance of the gods", "text": "text/edmonds-alcman.ocr.txt", "find": "ἔστι τις σιῶν τίσις"},
  {"label": "Alcaeus, the ship of state: the bilge", "text": "text/edmonds-alcaeus.ocr.txt", "find": "ἄντλην, ἐπεί κε νᾶος ἔββᾳ"}],
 "scope": "The volume entire in session OCR, divided by its sections. Edmonds prints the Greek with facing English, and he prints the papyri of Sappho and Alcaeus from Oxyrhynchus published after Bergk's last edition (1882); the seat is held for those, for the operator's \"all sappho\".",
 "why_seated": "Sappho is seated at one fragment (EA-CORPORA-01/10) and in the papyri panel (01/11); the operator asked for all of her. Bergk's Poetae Lyrici Graeci III (33/04) gives the fragments as known in 1882; Edmonds gives the twentieth-century papyri beside them.",
 "research": research("the Sappho line (31 and the reception operator, #1494–#1495) and Sappho requested whole"),
 "spine": "EA-CORPORA-33", "ruling": RULING, "seating": SEATING,
 "cross_references": ["sappho (EA-CORPORA-01/10, fragment 31, the diplomatic layer)", "papyri (01/11, the Sappho circle in DCLP)", "poetae-melici-bergk (33/04)"]})

if __name__ == "__main__":
    for s in specs:
        (H / f"spec33-{s['corpus']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(s["corpus"], len(s["loci"]))
