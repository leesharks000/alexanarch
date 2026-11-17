#!/usr/bin/env python3
"""EA-CORPORA-40 v1.1: seat 40/17, Classical Philology 1906–1922, the articles and notes, with the codes read from
the page (Dead Letters §§6.2–6.4, 3.2 and the conviction coding of §8.3).

    python3 -I build_seat40_17.py <philology-dir> <seats-dir>

<philology-dir> is the census working directory: gather/cp-articles/ (one served _djvu.txt per item, named by its Archive
identifier), gather/cp-articles-log.json (the fetch log, with each served file's SHA-256), gather/cp-articles-items.json
(the listing), coding/, coding-art/, conviction/, sample390-hand.jsonl, blind/ and the openings ruling. Every served
file is checked against the fetch log before it is seated. Loci are verified with whitespace collapsed."""
import hashlib, json, pathlib, re, shutil, sys
PH = pathlib.Path(sys.argv[1]); SEATS = pathlib.Path(sys.argv[2])
TODAY = "2026-11-17"; NAME = "classical-philology-1906-1922-articles"
TRANSPORT = "in-session fetch (Transport D); No-Double-Draw"
RULING = ("Lee Sharks, 2026-11-17 00:18 EST: \"yup lets version the ea corpora\", of the item in the census's next steps to seat the "
          "876 articles and notes of 1906–1922, so that the codes can be checked against an archive record.")
RESEARCH = {"study": "Dead Letters: Classical Philology and the Atom of Evidence (the philology census, first station; working notebook v0.14, not deposited)",
            "for": "the journal's own voice on the page, 1906–1922 (§6.2), read at each grain; the openings and what they open to (§6.4); the agreement of the codes (§3.2); and the judgments of conviction (§8.3)"}
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
L = json.loads((PH / "gather/cp-articles-log.json").read_text(encoding="utf-8"))
ok = {i: v for i, v in L.items() if "sha256" in v}
err = {i: v for i, v in L.items() if "error" in v}
ids = sorted(ok, key=lambda i: (ok[i].get("date") or "", int(i.split("-")[1])))
for i in ids:
    assert sha(PH / "gather/cp-articles" / f"{i}.txt") == ok[i]["sha256"], f"{i}: hash does not match the fetch log"
# the seat of 40/01 must not overlap
s01 = json.loads((SEATS / "classical-philology-1906-1922/source.json").read_text(encoding="utf-8"))
held01 = {x["identifier"] for x in s01["origin"]["items"]}
assert not (set(ids) & held01), "an item already seated in 40/01"
d = SEATS / NAME
if d.exists():
    assert json.loads((d / "source.json").read_text())["seat"] == "EA-CORPORA-40/17"; shutil.rmtree(d)
(d / "text").mkdir(parents=True); (d / "original/codes").mkdir(parents=True)
rows = []
for i in ids:
    shutil.copyfile(PH / "gather/cp-articles" / f"{i}.txt", d / f"text/{i}.txt"); rows.append(f"text/{i}.txt")
CODES = [("coding-art/cp-articles-1906-1922-coded.json", "the articles and notes coded on §2 by ten readers, every span checked against the page"),
         ("coding/cp-reviews-1906-1922-coded.json", "the book-review section (seated as 40/01) coded on §2, every span checked against the page"),
         ("openings-classed.json", "what each of the 161 openings of 1906–1922 puts in place of the received text (§6.4), one reader"),
         ("conviction/cp-items.json", "the 916 sentences of conviction found by the lexicon in 40/01 and 40/17, with the sentence before and after"),
         ("conviction/measure.py", "the conviction lexicon"),
         ("conviction/INSTRUCTIONS.md", "the instructions the conviction readers coded under"),
         ("coding-art/INSTRUCTIONS.md", "the instructions the §2 readers coded under"),
         ("sample390-hand.jsonl", "the 390-title sample (40/16) coded by hand, for agreement with the blind run (§3.2)"),
         ("blind/cp-sample390-chatgpt-coded.csv", "ChatGPT's blind run on the same 390 titles (§3.1)")]
for f, _ in CODES:
    shutil.copyfile(PH / f, d / "original/codes" / pathlib.Path(f).name); rows.append("original/codes/" + pathlib.Path(f).name)
conv = sorted((PH / "conviction").glob("cp-out-*.jsonl"))
with open(d / "original/codes/cp-conviction-coded.jsonl", "w", encoding="utf-8") as out:
    for f in conv: out.write(f.read_text(encoding="utf-8").rstrip("\n") + "\n")
rows.append("original/codes/cp-conviction-coded.jsonl")
(d / "MANIFEST.sha256").write_text("".join(f"{sha(d / r)}  {r}\n" for r in sorted(rows)))
LOCI = [("Scott, Odyssean Words Found in but One Book of the Iliad (1910)", "jstor-261886", "Odyssean Words"),
        ("Shewan, Another Chorizontic Failure (1921), the head in capitals", "jstor-262834", "CHORIZONTIC"),
        ("Kelsey on Hirtius' letter to Balbus (1907)", "jstor-261663", "Hirtius"),
        ("Scott, Non-Odyssean Words Found in the Iliad (1918)", "jstor-263749", "Non-Odyssean")]
found, missing = [], []
for lab, i, nd in LOCI:
    flat = re.sub(r"\s+", " ", (d / f"text/{i}.txt").read_text(encoding="utf-8", errors="replace"))
    (found if nd in flat else missing).append(f"{lab} — '{nd}' (text/{i}.txt)")
lines = sum((d / f"text/{i}.txt").read_text(encoding="utf-8", errors="replace").count("\n") for i in ids)
meta = {"corpus": NAME, "seat": "EA-CORPORA-40/17",
 "title": "Classical Philology I–XVII (Chicago, 1906–1922): the articles and notes, as JSTOR's Early Journal Content, with the codes read from the page",
 "edition": "JSTOR Early Journal Content at the Internet Archive (identifiers jstor-NNNNNN), one item per article, note, titled review or notice",
 "language": "en (with grc, la, de, fr)",
 "license": {"payload": "Classical Philology I–XVII were published 1906–1922; the scan and its text layer are public domain in the United States (published before 1931). JSTOR released its Early Journal Content (pre-1923 US, pre-1870 elsewhere) free to the public in 2011. The codes, samples, scripts and instructions under original/codes/ are the archive's, CC-BY-4.0; their spans quote the public-domain pages and the titles (Crossref metadata, CC0). The archive asserts no licence over the payload.",
             "record": "CC-BY-4.0 applies to this seat record only."},
 "origin": {"items": [{"source": "Internet Archive", "identifier": i, "url": f"https://archive.org/details/{i}", "files": [ok[i]["url"].rsplit("/", 1)[1]], "date": ok[i].get("date")} for i in ids],
            "transport": TRANSPORT, "listing": "the collection jstor_clasphil (1,714 items) less the items seated in 40/01"},
 "works": {"count": len(ids), "units": "one text file per item: article, note, titled review or notice",
           "list": [{"slug": i, "work": f"{ok[i].get('title')} ({(ok[i].get('date') or '')[:10]})", "text": f"text/{i}.txt", "served_as": ok[i]["url"].rsplit("/", 1)[1],
                     "lines": (d / f"text/{i}.txt").read_text(encoding="utf-8", errors="replace").count("\n")} for i in ids],
           "codes": [{"file": "original/codes/" + pathlib.Path(f).name, "what": w} for f, w in CODES] + [{"file": "original/codes/cp-conviction-coded.jsonl", "what": "the 916 sentences coded for polarity, judge, object and reason (§8.3), four readers' outputs joined"}]},
 "normalization": "The Internet Archive's own text layer (_djvu.txt), held under text/ exactly as served, byte for byte: the file's SHA-256 in MANIFEST.sha256 is the hash of the served file, checked against the fetch log. No text was corrected by hand; the loci keep the scan's readings.",
 "scope": f"The articles and notes of Classical Philology 1906–1922 that the seat of 40/01 does not hold: {len(ids)} items served of {len(L)} listed "
          f"({len(err)} returned a server error at the Archive and are pointed to: {', '.join(sorted(err))}). Counted by distinct text they are 876: 412 articles, 295 notes, 102 titled reviews and 67 notices (Dead Letters §6.2).",
 "why_seated": "The erratum on #1776 found 40/01 to hold the Book Reviews section; the journal's own articles and notes were fetched for a later seat. Seated, they let every code of the census's reading of 1906–1922 be checked against an archive record (Dead Letters §6.2, limits; §9.8).",
 "held_out": f"{', '.join(sorted(err))}: HTTP 500 at the Archive when fetched (2026-11-16); to be fetched again. Classical Philology 1923–1928 remains pointed to (40/01).",
 "fetched": "2026-11-16", "seated": TODAY, "verified_loci": found, "loci_not_found": missing, "lines_total": lines,
 "ruling": RULING, "research": RESEARCH, "spine": "EA-CORPORA-40 v1.1 (seated 2026-11-17, not deposited)", "axn": None,
 "axn_note": "assigned at deposit, derived from MANIFEST.sha256 as for every seat"}
(d / "source.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
print(meta["seat"], NAME, "items", len(ids), "lines", lines, "loci", len(found), "missing", len(missing), "files", len(rows))
