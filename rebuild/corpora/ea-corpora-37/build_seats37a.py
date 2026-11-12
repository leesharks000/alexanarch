#!/usr/bin/env python3
"""Seat EA-CORPORA-37 (seated, not deposited): the Slavonic Josephus text layer."""
import hashlib, json, pathlib, shutil, sys, datetime

DL = pathlib.Path(sys.argv[1])
ROOT = pathlib.Path("/home/claude/alexanarch")
SEATS = ROOT / "data/corpora"
TODAY = "2026-11-12"
TRANSPORT = "in-session fetch (Transport D); No-Double-Draw"
RULING = ("Lee Sharks, 2026-11-12 12:48 EST: \"also, we need to seat as much of slavonic josephus as possible, "
          "source language translation or both - we werent previously able to locate a full copy\"; "
          "the standing rule for originals-library seatings, 2026-10-18: \"original language where available always\".")
RESEARCH = {
    "study": "The Josephus Thesis (#1759) and the mine of the Ethiopian canon for the Josephus Thesis and Revelation First (2026-11-12)",
    "for": "the Testimonium's hedge (AJ 18.63 εἴγε ἄνδρα αὐτὸν λέγειν χρή) beside the Slavonic 'if it is fitting to call him a man', Catullus 51.2 si fas est and Philo's εἰ θέμις εἰπεῖν; the custody of Josephus's name in transmission (Yosippon, Zena Ayhud)",
    "supersedes_negative_search": "slavonic-josephus/NEGATIVE-SEARCH.md (2026-08-19), which found no openly served text of the recension; EA-CORPORA-01/12 stays as the index of the eight passages",
}
SPINE = "EA-CORPORA-37 (seated 2026-11-12, not deposited)"

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def norm(b):
    return b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

def write_seat(name, meta, files):
    """files: list of (src_path_or_bytes, rel_original, rel_text_or_None)."""
    d = SEATS / name
    if d.exists():
        sys.exit(f"{d} exists")
    (d / "original").mkdir(parents=True)
    (d / "text").mkdir()
    rows = []
    for src, orig_rel, text_rel, text_bytes in files:
        o = d / orig_rel
        o.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(src, (bytes, bytearray)):
            o.write_bytes(src)
        else:
            shutil.copyfile(src, o)
        rows.append(orig_rel)
        if text_rel:
            t = d / text_rel
            t.write_bytes(norm(text_bytes))
            rows.append(text_rel)
    man = "".join(f"{sha(d / r)}  {r}\n" for r in sorted(rows))
    (d / "MANIFEST.sha256").write_text(man)
    # verify loci
    found, missing = [], []
    texts = [(d / r).read_text(encoding="utf-8", errors="replace") for r in rows if r.startswith("text/")]
    for label, needle in meta.pop("_loci"):
        (found if any(needle in t for t in texts) else missing).append(f"{label} — '{needle}'" if label else needle)
    meta["verified_loci"] = found
    meta["loci_not_found"] = missing
    meta["lines_total"] = sum(t.count("\n") for t in texts)
    for w in meta["works"]["list"]:
        w["lines"] = (d / w["text"]).read_text(encoding="utf-8", errors="replace").count("\n")
    meta["ruling"] = RULING
    meta["research"] = RESEARCH
    meta["spine"] = SPINE
    meta["axn"] = None
    meta["axn_note"] = "assigned at deposit, derived from MANIFEST.sha256 as for every seat"
    (d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    if missing:
        print("LOCI NOT FOUND", name, missing)
    return meta, man

seats = []

# 37/01 — Meshcherskii 1958, the Old Russian text (seven books)
djvu = (DL / "mesch_djvu.txt").read_bytes()
lines = djvu.split(b"\n")
assert lines[9333].strip() == "ТЕКСТЫ".encode(), lines[9333]
assert lines[31517].strip() == "КОММЕНТАРИИ".encode(), lines[31517]
texts_section = b"\n".join(lines[9333:31517]) + b"\n"
full_sha = hashlib.sha256(djvu).hexdigest()
ID1 = "1958_20250223"
FN1 = "Мещерский Н.А. - История иудейской войны Иосифа Флавия в древнерусском переводе (1958)"
seats.append(("slavonic-josephus-meshcherskii-1958", {
    "corpus": "slavonic-josephus-meshcherskii-1958",
    "seat": "EA-CORPORA-37/01",
    "title": "История Иудейской войны Иосифа Флавия в древнерусском переводе, ed. N. A. Meshcherskii (Moscow–Leningrad: Akademiia Nauk SSSR, 1958): the Old Russian text of the seven books",
    "edition": "Meshcherskii 1958, the TEXTS section (books I–VII), printed from the Vilna Chronograph (16th c.) with variants from eight manuscripts of the 15th–16th c.; the Internet Archive's text layer",
    "language": "orv",
    "license": {
        "payload": "The text is the Old Russian translation of the Jewish War (Kievan period, not later than the 12th c.), a medieval work in the public domain. The 1958 edition is N. A. Meshcherskii's (1906–1987); its introduction and commentary are his prose and are held by reference, not copied. The seat copies the edition's TEXTS section only (the seven books with their variant notes), as the Internet Archive serves it publicly with no licence stated. The archive asserts no licence over the payload.",
        "record": "CC-BY-4.0 applies to this seat record only.",
    },
    "fetched": TODAY,
    "origin": {"items": [{
        "source": "Internet Archive", "identifier": ID1,
        "url": f"https://archive.org/details/{ID1}",
        "files": [FN1 + "_djvu.txt", FN1 + ".pdf (by reference, 75,066,705 bytes)"],
        "full_text_layer_sha256": full_sha,
        "excerpt": "lines 9334–31517 of the _djvu.txt as served: from the heading ТЕКСТЫ to the line before КОММЕНТАРИИ",
    }], "fetched": TODAY, "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{
        "slug": "istoriia-iudeiskoi-voiny",
        "work": "История Иудейской войны (the Old Russian Jewish War), books I–VII, Meshcherskii 1958",
        "text": "text/istoriia-iudeiskoi-voiny.orv.ocr.txt",
        "originals": [f"original/{ID1}/texts-section_djvu.txt"],
    }]},
    "normalization": "The Internet Archive's own text layer (tesseract 5.3.0, Russian model) as served, cut to the TEXTS section by line number; copied to text/ with line endings normalized. No text was corrected by hand. The OCR does not hold the old letters reliably: ѣ comes through as $, Ъ, З or Ф, superscript note numbers as ?, “ or digits, and the edition's leaf markers (л. 500, с. 9) and running heads (Книга первая 169) stand in the line. The loci keep the OCR's readings.",
    "scope": "All seven books in the language of the translation: the eight Jesus-and-John passages in their places and every other divergence from the Greek.",
    "why_seated": "The Slavonic text layer the 2026-08-19 search could not find; held in the original language.",
    "_loci": [
        ("War II after 174, the wonder-worker: 'At that time there appeared a certain man, if it is fitting to call him a man'", "явися мужь нзкыи, и аще мужем достоино есть его"),
        ("the same passage: 'therefore it is impossible for me to call him a man'", "немощно ми есть нарещи его челов$ком"),
        ("the rubric before it in the manuscript and in A: 'Josephus writes of Christ'", "Иосиф о ХристБ пишет"),
        ("Book I begins", "КНИГА ПЕРВАЯ"),
        ("Book VII", "КНИГА СЕДЬМАЯ"),
    ],
}, [(texts_section, f"original/{ID1}/texts-section_djvu.txt", "text/istoriia-iudeiskoi-voiny.orv.ocr.txt", texts_section)]))

# 37/02 — Berendts & Grass, German, books I–IV
BG = [("29178", "22537", "46086", "1", "1924", "1–160"), ("29182", "22541", "46090", "2", "1926", "161–288"),
      ("29169", "22528", "46077", "3", "1926/1927", "289–416"), ("29164", "22523", "46072", "4", "1927", "417–512")]
bg_files, bg_works, bg_items = [], [], []
for art, gal, fid, n, yr, pp in BG:
    pdf = DL / f"bg-{art}.pdf"
    txt = (DL / f"bg-{art}.plain.txt").read_bytes()
    bg_files.append((pdf, f"original/ojs-utlib-ee/{art}.pdf", f"text/lieferung-{n}.txt", txt))
    bg_works.append({"slug": f"lieferung-{n}", "work": f"Lieferung {n} (pp. {pp})", "text": f"text/lieferung-{n}.txt",
                     "originals": [f"original/ojs-utlib-ee/{art}.pdf"]})
    bg_items.append({"source": "University of Tartu, Tartu Ülikooli toimetised (OJS)", "article": art,
                     "url": f"https://ojs.utlib.ee/index.php/tyt/article/view/{art}",
                     "download": f"https://ojs.utlib.ee/index.php/tyt/article/download/{art}/{gal}/{fid}",
                     "pages": pp, "printed": f"Dorpat {yr}" if "/" not in yr else "Dorpat (the third Lieferung carries no imprint year in its text layer)"})
seats.append(("berendts-grass-slavonic-josephus-1924", {
    "corpus": "berendts-grass-slavonic-josephus-1924",
    "seat": "EA-CORPORA-37/02",
    "title": "A. Berendts and K. Grass, Flavius Josephus vom Jüdischen Kriege, Buch I–IV, nach der slavischen Übersetzung deutsch herausgegeben und mit dem griechischen Text verglichen (Dorpat, 1924–1927), four Lieferungen",
    "edition": "Berendts–Grass, the German rendering of the Slavonic War I–IV with the Greek compared in the notes, and the list of the Überschüsse (the additions over the Greek), as published in the Acta of the University of Tartu",
    "language": "deu+grc",
    "license": {
        "payload": "Published at Dorpat 1924–1927; Alexander Berendts died in 1912. Public domain in the United States (published before 1931). Served openly by the University of Tartu Library's OJS; no licence is stated on the items. The archive asserts no licence over the payload.",
        "record": "CC-BY-4.0 applies to this seat record only.",
    },
    "fetched": TODAY,
    "origin": {"items": bg_items, "fetched": TODAY, "transport": TRANSPORT},
    "works": {"count": 4, "units": "one text file per Lieferung", "list": bg_works},
    "normalization": "Each Lieferung's PDF as served is held under original/ojs-utlib-ee/. Its embedded text layer was extracted with pdftotext (poppler, reading order, no layout) to text/lieferung-N.txt, line endings normalized. No text was corrected by hand; the Greek in the notes keeps the scan's readings, which are often damaged.",
    "scope": "Books I–IV whole, in German, with the Greek compared: the thirty-odd Überschüsse among them the wonder-worker (XII), his followers (XIII), John the Forerunner (IX, XI) and Josephus's ruse at Jotapata (XV).",
    "why_seated": "The only complete rendering of Slavonic War I–IV in a western language that is out of copyright; Thackeray's appendix translates from it.",
    "_loci": [
        ("II after 174, the wonder-worker", "Damals 16 ) erschien ein Mann, wenn es auch erlaubt ist,"),
        ("the same: 'therefore it is impossible for me to call him a human being'", "Deswegen ist es mir unmöglich, ihn"),
        ("Überschuss XII in the list", "Auftreten und Kreuzestod des Wunder"),
        ("Überschuss XV: Josephus's ruse at Jotapata", "Die List des Josephus bei Errettung seines"),
    ],
}, bg_files))

# 37/03 — Thackeray, Loeb Josephus III (1928): War IV–VII and the appendix of Slavonic additions
ID3 = "josephuswithengl03joseuoft"
t3 = (DL / "loeb3.txt").read_bytes()
seats.append(("thackeray-loeb-josephus-iii-1928", {
    "corpus": "thackeray-loeb-josephus-iii-1928",
    "seat": "EA-CORPORA-37/03",
    "title": "Josephus, with an English translation by H. St. J. Thackeray, vol. III: The Jewish War, Books IV–VII (Loeb Classical Library; London: Heinemann, 1928), with the appendix 'The Principal Additional Passages in the Slavonic Version'",
    "edition": "Thackeray, Loeb Josephus III, the Internet Archive's text layer",
    "language": "eng+grc",
    "license": {
        "payload": "Thackeray died in 1930; the volume is public domain in the United States (published before 1931) and where the term is life plus seventy years. The archive asserts no licence over the payload.",
        "record": "CC-BY-4.0 applies to this seat record only.",
    },
    "fetched": TODAY,
    "origin": {"items": [{"source": "Internet Archive", "identifier": ID3, "url": f"https://archive.org/details/{ID3}",
                          "files": [f"{ID3}_djvu.txt"]}], "fetched": TODAY, "transport": TRANSPORT},
    "works": {"count": 1, "units": "one text file per work", "list": [{
        "slug": "jewish-war-iv-vii", "work": "The Jewish War IV–VII, Greek and English, with the Slavonic appendix",
        "text": "text/jewish-war-iv-vii.ocr.txt", "originals": [f"original/{ID3}/{ID3}_djvu.txt"]}]},
    "normalization": "The Internet Archive's own text layer (_djvu.txt) as served, under original/<identifier>/, copied to text/<slug>.ocr.txt with line endings normalized. The PDF is held by reference at its Archive URL and not copied. No text was corrected by hand; the loci keep the OCR's readings.",
    "scope": "The volume whole. The appendix gives twenty-two Slavonic passages in English: the first nineteen from Berendts–Grass (Books I–IV), the last three from Berendts 1906, which carry the additions of Books V–VI that Berendts–Grass does not reach.",
    "why_seated": "The English of the Slavonic additions across all seven books, out of copyright.",
    "_loci": [
        ("the appendix heading", "THE SLAVONIC VERSION"),
        ("the wonder-worker, between ii. 174 and 175", "At that time there appeared a man, if it is permissible"),
        ("its source stated", "the German rendering of the Slavonic version produced by"),
    ],
}, [(DL / "loeb3.txt", f"original/{ID3}/{ID3}_djvu.txt", "text/jewish-war-iv-vii.ocr.txt", t3)]))

# 37/04 — Eisler, IHΣOYΣ BAΣIΛEYΣ OY BAΣIΛEYΣAΣ (Heidelberg, 1929–1930), two volumes
e_files, e_works, e_items = [], [], []
for i in (1, 2):
    ident = f"iesousbasileusou000{i}eisl"
    b = (DL / f"eisler{i}.txt").read_bytes()
    e_files.append((DL / f"eisler{i}.txt", f"original/{ident}/{ident}_djvu.txt", f"text/iesous-basileus-{i}.ocr.txt", b))
    e_works.append({"slug": f"iesous-basileus-{i}", "work": f"Eisler, IHΣOYΣ BAΣIΛEYΣ, vol. {i}",
                    "text": f"text/iesous-basileus-{i}.ocr.txt", "originals": [f"original/{ident}/{ident}_djvu.txt"]})
    e_items.append({"source": "Internet Archive", "identifier": ident, "url": f"https://archive.org/details/{ident}",
                    "files": [f"{ident}_djvu.txt"], "provenance_note": "from the library of Walter Bauer (1877–1960), Claremont School of Theology"})
seats.append(("eisler-iesous-basileus-1929", {
    "corpus": "eisler-iesous-basileus-1929",
    "seat": "EA-CORPORA-37/04",
    "title": "Robert Eisler, ΙΗΣΟΥΣ ΒΑΣΙΛΕΥΣ ΟΥ ΒΑΣΙΛΕΥΣΑΣ: Die messianische Unabhängigkeitsbewegung vom Auftreten Johannes des Täufers bis zum Untergang Jakobs des Gerechten nach der neuerschlossenen Eroberung von Jerusalem des Flavius Josephus und den christlichen Quellen (Religionswissenschaftliche Bibliothek 9; Heidelberg: Winter, 1929–1930), two volumes",
    "edition": "Eisler, IHΣOYΣ BAΣIΛEYΣ, vols. I–II, the Internet Archive's text layer",
    "language": "deu+grc+lat+orv",
    "license": {
        "payload": "Eisler died in 1949; the volumes are public domain where the term is life plus seventy years, and in the United States (published 1929–1930). The archive asserts no licence over the payload.",
        "record": "CC-BY-4.0 applies to this seat record only.",
    },
    "fetched": TODAY,
    "origin": {"items": e_items, "fetched": TODAY, "transport": TRANSPORT},
    "works": {"count": 2, "units": "one text file per volume", "list": e_works},
    "normalization": "The Internet Archive's own text layer (_djvu.txt) as served, under original/<identifier>/, copied to text/<slug>.ocr.txt with line endings normalized. The PDFs are held by reference at their Archive URLs and not copied. No text was corrected by hand; the loci keep the OCR's readings.",
    "scope": "Both volumes whole: the case that the Slavonic preserves Josephus's Aramaic first draft, with the Slavonic passages rendered and argued, the Testimonium, and the Halōsis (the Capture of Jerusalem). Held as the thesis's strongest statement, not as its proof; the consensus answer (Zeitlin, Creed, Meshcherskii) is named in EA-CORPORA-01/12.",
    "why_seated": "The book Thackeray's appendix was written beside, and the source of the English Messiah Jesus (1931), which is still in copyright.",
    "_loci": [
        ("the wonder-worker rendered, §174a", "Damals? erschien® ein Mann?, wenn es auch erlaubt ist°,"),
        ("the table of contents", "Das Josephuszeugnis und die Juden"),
    ],
}, e_files))

out = []
for name, meta, files in seats:
    m, man = write_seat(name, meta, files)
    out.append((name, m, man))
    print(name, m["seat"], m["lines_total"], "loci", len(m["verified_loci"]), "missing", len(m["loci_not_found"]))
json.dump([[n, m] for n, m, _ in out], open(DL.parent / "seats.json", "w"), ensure_ascii=False, indent=1)
