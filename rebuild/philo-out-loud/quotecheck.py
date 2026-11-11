#!/usr/bin/env python3
"""Assert every Greek quotation in the Philo draft against the seated texts (Philo, Cohn-Wendland; LXX Zechariah, Swete; Justin, Archambault;
Eusebius, HE). Apostrophe forms and whitespace normalized; an ellipsis splits a quotation into parts, each asserted.
    python3 rebuild/philo-out-loud/quotecheck.py [draft.md]"""
import re, sys, pathlib, unicodedata
import xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parents[2]; C = ROOT / "data/corpora"
def n(x):
    x = unicodedata.normalize("NFC", x)
    for a in ["᾿", "’", "'", "ʼ", "‘"]: x = x.replace(a, "'")
    return re.sub(r"\s+", " ", x)
draft = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "DRAFT-v0.1.md"
seat = n("".join(f.read_text(encoding="utf-8") for f in [*C.glob("philo/text/*.txt"), *C.glob("lxx-swete/text/tlg046*"), *C.glob("lxx-swete/text/tlg004*"), C / "gnt-nestle1904/text/Rev.txt",
       C / "justin-dialogus/text/dialogus.txt", C / "eusebius-historia-ecclesiastica/text/historia-ecclesiastica.txt"]))
def tei(path):
    """The Philo TEI with <note> elements (the editors' apparatus) dropped, sections joined by a space: the text layer interleaves
    apparatus into some lines, which the TEI keeps apart."""
    def txt(e):
        out = e.text or ""
        for c in e:
            out += ("" if c.tag.endswith("}note") else txt(c)) + (c.tail or "")
        return out
    root = ET.parse(path).getroot().find(".//{http://www.tei-c.org/ns/1.0}text")
    return " ".join(txt(d) for d in root.iter("{http://www.tei-c.org/ns/1.0}div") if d.get("subtype") == "section")
seat += " " + n(" ".join(tei(f) for f in sorted(C.glob("philo/original/*.xml"))))
t = m = 0
for q in re.findall(r'"([^"\n]+)"', draft.read_text(encoding="utf-8")):
    if sum(1 for c in q if "Ͱ" <= c <= "Ͽ" or "ἀ" <= c <= "῿") < 0.6 * len(q.replace(" ", "")): continue
    t += 1
    for x in [n(x).strip(" ·,.;") for x in q.split("…")]:
        if len(x) > 3 and x not in seat: m += 1; print("MISS", x[:100])
print(f"{t} Greek quotations; {m} misses"); sys.exit(1 if m else 0)
