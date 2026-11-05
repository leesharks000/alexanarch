#!/usr/bin/env python3
"""Writes the four carriage specs of EA-CORPORA-34 v1.1 (34/12–34/15). Session tool; written as EA-CORPORA-35 and folded into 34 at the operator's word of 2026-11-05 11:11 ("lets bundle the 35 sources with 34 and version in place - theyre of a piece"). Secondary Source, the count of carriage and the stratum of material transmission and succession
(design v0.4 §2.5, §3.5a), seated at the operator's word of 2026-11-05 11:02."""
import json, pathlib, sys
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "ea-corpora-34")); import importlib.util
RULING = ("Lee Sharks, 2026-11-05 11:02 EST: \"we should also be tracking material manuscript transmission and succession, that seems particularly important "
          "with revelation and less-often and -critically studied than pure reception\"; on the seating, 11:11 EST: \"lets bundle the 35 sources with 34 and version in place - theyre of a piece\"; the standing rule for the seating of 09:03 EST: \"lets gather up and seat "
          "the sources we'll need for this one prior to writing. still under rebekah cranes for the ea-corpora, and with reference to the research occasion\".")
SEATING = "EA-CORPORA-34 v1.1, the thirty-fourth seating: Secondary Source — the reception and the carriage of the Apocalypse, 2026-11-05"
REC = "CC-BY-4.0 applies to this seat record only."
NORM = ("The Internet Archive's own text layer (_djvu.txt) as served, under original/<identifier>/, copied to text/<slug>.ocr.txt with line endings normalized. "
        "The PDF of each item is held by reference at its Archive URL and not copied. No text was corrected by hand; the loci keep the OCR's readings.")
RES = lambda f: {"study": "Secondary Source: the reception of the Apocalypse as derivative, secondary and marginal",
                 "design": "drafts/SECONDARY-SOURCE-design-2026-11-05.md (v0.4, sha256 c645d2e3…)", "draft": "not yet drafted; the locus table is rebuild/secondary-source/LOCI.md",
                 "locus_table": "design v0.4 §4.1 and LOCI.md", "owed_at": "the debts of design v0.4 §5 for carriage and succession (§2.5, §3.5a)", "for": f}
ia = lambda ident, djvu, slug, work: {"kind": "ia", "slug": slug, "work": work, "identifier": ident, "files": [djvu]}
lo = lambda label, text, find: {"label": label, "text": text, "find": find}
specs = []
def add(corpus, n, title, lang, lic, items, loci, scope, why, f):
    specs.append({"corpus": corpus, "seat": f"EA-CORPORA-34/{n + 11:02d}", "title": title, "language": lang, "fetched": "2026-11-05",
                  "license": {"payload": lic, "record": REC}, "normalization": NORM, "items": items, "loci": loci, "scope": scope, "why_seated": why,
                  "research": RES(f), "spine": "EA-CORPORA-34", "ruling": RULING, "seating": SEATING})
add("scrivener-plain-introduction-1894", 1, "F. H. A. Scrivener, A Plain Introduction to the Criticism of the New Testament, 4th ed., ed. E. Miller (London: Bell, 1894), two volumes", "eng+grc",
    "Scrivener (died 1891) and Miller (died 1898) are public domain everywhere.",
    [ia("gtu_32400001627490", "gtu_32400001627490_djvu.txt", "plain-introduction-i", "Scrivener, A Plain Introduction, 4th ed., vol. I (1894): the manuscripts"),
     ia("gtu_32400001627060", "gtu_32400001627060_djvu.txt", "plain-introduction-ii", "Scrivener, A Plain Introduction, 4th ed., vol. II (1894): the versions and the printed editions")],
    [], "Both volumes whole, held for the manuscripts of the Apocalypse (the uncials and the minuscules), the lectionaries, and the printed editions from Erasmus to the received text.",
    "The standard public account of the carriers and of the succession into print: §3.5a.", "design v0.4 §2.5, §3.5a")
add("delitzsch-handschriftliche-funde-1861", 2, "Franz Delitzsch, Handschriftliche Funde, Heft 1: Die Erasmischen Entstellungen des Textes der Apokalypse (Leipzig, 1861)", "deu+grc",
    "Delitzsch (died 1890) is public domain everywhere.",
    [ia("handschriftlich00deligoog", "handschriftlich00deligoog_djvu.txt", "handschriftliche-funde", "Delitzsch, Handschriftliche Funde (1861), the Archive's text layer")],
    [], "The volume whole, held for Reuchlin's codex of the Apocalypse with Andreas's commentary, rediscovered by Delitzsch, and Erasmus's use of it in 1516.",
    "The one exemplar of the first printed Apocalypse, and what Erasmus did where it failed: §3.5a.", "design v0.4 §3.5a")
add("tregelles-printed-text-1854", 3, "S. P. Tregelles, An Account of the Printed Text of the Greek New Testament (London: Bagster, 1854)", "eng+grc",
    "Tregelles (died 1875) is public domain everywhere.",
    [ia("accountofprinted00treg", "accountofprinted00treg_djvu.txt", "account-printed-text", "Tregelles, An Account of the Printed Text (1854), the Archive's text layer")],
    [], "The account whole, held for Erasmus's editions and their passage into Stephanus, Beza and the received text.", "The succession from the 1516 Apocalypse to the received text: §3.5a.", "design v0.4 §3.5a")
add("erasmus-novum-instrumentum-1516", 4, "Erasmus, Novum Instrumentum omne (Basel: Froben, 1516)", "grc+lat",
    "Erasmus is public domain; the Basel printing of 1516 is public domain everywhere.",
    [ia("bub_gb_wd8jyWdVYRYC", "bub_gb_wd8jyWdVYRYC_djvu.txt", "novum-instrumentum", "Erasmus, Novum Instrumentum omne (Basel, 1516), the Archive's text layer (the scan is the witness)")],
    [], "The first printed Greek New Testament whole, held for its Apocalypse and the book's last page.", "The printed Apocalypse as first made: §3.5a and §3.6.", "design v0.4 §3.5a, §3.6")
LOCI = {"delitzsch-handschriftliche-funde-1861": [{"label": "the title: the Erasmian distortions of the text of the Apocalypse, shown from Reuchlin's codex thought lost", "text": "text/handschriftliche-funde.ocr.txt", "find": "DIE ERASMISCHEN ENTSTELLUNGEN DES TEXTES DER APOKALYPSE, NACHGEWIESEN AUS DEM VERLOREN GEGLAUBTEN CODEX REUCHLINS"}], "tregelles-printed-text-1854": [{"label": "Erasmus had one mutilated manuscript of the Apocalypse, borrowed from Reuchlin; the last six verses retranslated from the Latin", "text": "text/account-printed-text.ocr.txt", "find": "For the Apocalypse he had but one mutilated MS., borrowed from Reuchlin, in which the text and commentary were intermixed almost unintelligibly"}, {"label": "the last six verses wholly wanting", "text": "text/account-printed-text.ocr.txt", "find": "This was the case with regard to the last six verses, which from the mutilated condition of his MS. were wholly wanting"}], "scrivener-plain-introduction-1894": [{"label": "Erasmus's own note, as Scrivener quotes it: words at the end of the book wanting in the Greek, added from the Latin", "text": "text/plain-introduction-ii.ocr.txt", "find": "nonnulla verba reperi apud nostros, quae aberant in Graecis exem- plaribus, ea tamen ex latinis adjecimus"}]}
for s in specs:
    s["loci"] = LOCI.get(s["corpus"], [])
    (H / f"spec34-{s['corpus']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"); print("wrote", s["seat"], s["corpus"])
