#!/usr/bin/env python3
"""EA-CORPORA-38/01: Kant, the Akademie-Ausgabe I–XVIII, in a Fraktur OCR made for this seat.

    python3 -I build_kant38.py <kant-ia-dir> <seats-dir>

<kant-ia-dir> holds aa<NN>.txt (the Internet Archive's own text layers, as served) and ocr/<identifier>/n<NNNN>.txt
(one page each, tesseract 5 deu_latf from tessdata_best, single thread; the page image fetched, read and deleted).
"""
import hashlib, json, pathlib, sys

K = pathlib.Path(sys.argv[1])
SEATS = pathlib.Path(sys.argv[2])
NAME = "kant-akademie-ausgabe"
TODAY = "2026-11-14"
ROMAN = {"00": "VII", "01": "I", "02": "II", "03": "III", "04": "IV", "05": "V", "06": "VI", "08": "VIII", "09": "IX",
         "10": "X", "11": "XI", "12": "XII", "13": "XIII", "14": "XIV", "151": "XV.1", "152": "XV.2", "16": "XVI",
         "17": "XVII", "18": "XVIII"}
# printing years read from each volume's title page in the scan
PRINTED = {"VII": 1917, "I": 1910, "II": 1912, "III": 1911, "IV": 1911, "V": 1913, "VI": 1914, "VIII": 1923, "IX": 1923,
           "X": 1922, "XI": 1922, "XII": 1922, "XIII": 1922, "XIV": 1925, "XV.1": 1923, "XV.2": 1923, "XVI": 1924,
           "XVII": 1926, "XVIII": 1928}
CONTENTS = {"I": "Vorkritische Schriften I (1747–1756)", "II": "Vorkritische Schriften II (1757–1777)",
            "III": "Kritik der reinen Vernunft (2. Aufl. 1787)", "IV": "Kritik der reinen Vernunft (1. Aufl. 1781), Prolegomena, Grundlegung zur Metaphysik der Sitten, Metaphysische Anfangsgründe der Naturwissenschaft",
            "V": "Kritik der praktischen Vernunft, Kritik der Urtheilskraft", "VI": "Die Religion innerhalb der Grenzen der bloßen Vernunft, Die Metaphysik der Sitten",
            "VII": "Der Streit der Facultäten, Anthropologie in pragmatischer Hinsicht", "VIII": "Abhandlungen nach 1781",
            "IX": "Logik (Jäsche), Physische Geographie, Pädagogik", "X": "Briefwechsel I (1747–1788)", "XI": "Briefwechsel II (1789–1794)",
            "XII": "Briefwechsel III (1795–1803)", "XIII": "Briefwechsel IV (Anmerkungen und Register)", "XIV": "Handschriftlicher Nachlaß I: Mathematik, Physik und Chemie, Physische Geographie",
            "XV.1": "Handschriftlicher Nachlaß II.1: Anthropologie", "XV.2": "Handschriftlicher Nachlaß II.2: Anthropologie",
            "XVI": "Handschriftlicher Nachlaß III: Logik", "XVII": "Handschriftlicher Nachlaß IV: Metaphysik I", "XVIII": "Handschriftlicher Nachlaß V: Metaphysik II"}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


d = SEATS / NAME
(d / "original").mkdir(parents=True, exist_ok=True)
(d / "text").mkdir(exist_ok=True)
rows, works, items = [], [], []
for code, vol in ROMAN.items():
    ident = f"kantsgesammeltes{code}" + ("kant" if code == "02" else "imma")
    pages = sorted((K / "ocr" / ident).glob("n*.txt"))
    slug = "aa-" + vol.lower().replace(".", "-")
    text = "".join(f"[page n{p.stem[1:]}]\n" + p.read_text(encoding="utf-8").replace("\f", "") for p in pages)
    (d / "text" / f"{slug}.ocr.txt").write_text(text, encoding="utf-8")
    orig = f"original/{ident}/{ident}_djvu.txt"
    (d / orig).parent.mkdir(parents=True, exist_ok=True)
    (d / orig).write_bytes((K / f"aa{code}.txt").read_bytes())
    rows += [orig, f"text/{slug}.ocr.txt"]
    works.append({"slug": slug, "volume": vol, "work": f"AA {vol}: {CONTENTS[vol]}", "printed": PRINTED[vol],
                  "pages": len(pages), "text": f"text/{slug}.ocr.txt", "originals": [orig],
                  "lines": text.count("\n")})
    items.append({"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}",
                  "files": [f"{ident}_djvu.txt", "page/n<i>.jpg (each fetched, read and deleted)"],
                  "copy": "University of Toronto (Kelly)" if code == "02" else "Gumberg Library, Duquesne University"})
(d / "MANIFEST.sha256").write_text("".join(f"{sha(d / r)}  {r}\n" for r in sorted(rows)))

LOCI = [
    ("AA III 7 (B viii): logic has taken no step forward since Aristotle", "text/aa-iii.ocr.txt", "daß ſie auch bis jeht keinen Schritt vorwärts hat thun können"),
    ("AA IX 3–4, Jäsche's preface: Meier's Auszug as Kant's Materialien-Magazin", "text/aa-ix.ocr.txt", "das Materialien-Magazin aus, das Kant hier für ſeine Vor-"),
    ("AA IX 20 (the editor's note): Kant's judgment not in doubt", "text/aa-ix.ocr.txt", "Kant's Urtheil über dieſen Punkt nicht zweifelhaft"),
    ("AA XVI, the Reflexionen on the history of logic: '2. Aristotelici: Theophrast,'", "text/aa-xvi.ocr.txt", "2. Aristotelici: Theophraſt,"),
]
found, missing = [], []
for label, rel, needle in LOCI:
    (found if needle in (d / rel).read_text(encoding="utf-8") else missing).append(f"{label} — '{needle}' ({rel})")

meta = {
    "corpus": NAME, "seat": "EA-CORPORA-38/01",
    "title": "Kant's gesammelte Schriften, herausgegeben von der Königlich Preußischen Akademie der Wissenschaften, Bände I–XVIII (Berlin: Reimer / de Gruyter, printings of 1910–1928)",
    "edition": "The Akademie-Ausgabe (AA), Abteilungen I–III (Werke, Briefwechsel, Handschriftlicher Nachlaß), vols. I–XVIII as scanned by the Internet Archive; a Fraktur OCR made for this seat, the Archive's own text layer held beside it",
    "language": "deu", "fetched": TODAY,
    "license": {"payload": "Kant (d. 1804) is public domain. The volumes seated were printed 1910–1928 and are public domain in the United States (published before 1931). The editors' apparatus is held as printed; the archive asserts no licence over the payload. The OCR is the archive's, made by code and not corrected.", "record": "CC-BY-4.0 applies to this seat record only."},
    "origin": {"items": items, "fetched": TODAY, "transport": "in-session fetch (Transport D); No-Double-Draw"},
    "works": {"count": len(works), "units": "one text file per volume (XV in its two halves)", "list": works},
    "normalization": "text/aa-<vol>.ocr.txt is this seat's OCR: each page image fetched from the Archive, read by tesseract 5 with the deu_latf model (tessdata_best, Fraktur), single thread, and deleted; the pages joined in order, each headed [page nNNNN] (the Archive's leaf number, not the AA page). The long s stands as ſ, as printed. No text was corrected by hand; the loci keep the OCR's readings. original/<identifier>/ holds the Archive's own text layer as served, which reads the Fraktur poorly, for comparison.",
    "scope": "AA I–XVIII whole: the Werke (I–IX), the Briefwechsel (X–XIII) and the Handschriftliche Nachlaß through Metaphysik II (XIV–XVIII), XVI the Reflexionen zur Logik.",
    "why_seated": "Kant's verdict that logic has taken no step forward since Aristotle and seems closed and complete (B viii), the Logik Jäsche made from Meier's Auszug, and the Reflexionen zur Logik, seated whole so the verdict can be read against the whole: the hinge of the reception history of inference.",
    "held_out": "AA XIX–XXIII (printed 1934–1955) are not in this seat: they were printed after 1931 (XIX 1934, XX 1942, XXI 1936, XXII 1938, XXIII 1955), and whether they are seated is the operator's ruling. The Archive's own text layers of XIX–XXIII were fetched for that ruling and are not carried here.",
    "duplicate_not_seated": "A second scan of VII (kantsgesammeltes07kant, Toronto) was OCR'd in the same run before kantsgesammeltes00imma was seen to be VII; it is not seated, so VII is held once.",
    "verified_loci": found, "loci_not_found": missing,
    "lines_total": sum(w["lines"] for w in works),
    "ruling": ("Lee Sharks, 2026-11-13, the construction and reception history of inference: Kant seated whole; "
               "2026-11-14 01:25 EST: \"lets continue to assemble and we'll deposit and seat the whole thing as a massive batch\"."),
    "research": {"study": "Critique of Pure Inference (working draft v1.1), §11.6 \"the witnesses between\"",
                 "for": "Kant's verdict that logic has taken no step since Aristotle (B viii), Jäsche's Logik and its Materialien-Magazin, and the Reflexionen zur Logik in XVI"},
    "spine": "EA-CORPORA-38 (assembled 2026-11-14, not seated, not deposited)", "axn": None,
    "axn_note": "assigned at deposit, derived from MANIFEST.sha256 as for every seat",
}
(d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
print(meta["seat"], NAME, "volumes", len(works), "lines", meta["lines_total"], "loci", len(found), "missing", len(missing))
for m in missing:
    print("  MISSING", m)
