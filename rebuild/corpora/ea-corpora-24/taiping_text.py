#!/usr/bin/env python3
"""Derive the Taiping seat's text layer from the harvested Wikisource renders (session tool).
Each page's rendered HTML (action=render at a recorded oldid) is reduced by code: the header table, the
licence banner and noprint elements are dropped; the text keeps its line breaks. A work's pages are
joined in the order given, each under a heading '=== <page title> (oldid N) ==='.
    python3 taiping_text.py <seat-dir>"""
import json, sys, pathlib
from bs4 import BeautifulSoup
seat = pathlib.Path(sys.argv[1]); ws = seat / "original/wikisource"
idx = json.loads((ws / "index.json").read_text(encoding="utf-8"))
WORKS = json.loads((pathlib.Path(__file__).with_name("taiping_works.json")).read_text(encoding="utf-8"))
def text_of(f):
    s = BeautifulSoup(f.read_text(encoding="utf-8"), "html.parser")
    for sel in ["#headerContainer", ".licenseContainer", ".noprint", "style", ".mw-editsection", ".ws-noexport"]:
        for el in s.select(sel): el.decompose()
    t = s.get_text("\n")
    return "\n".join(l.rstrip() for l in t.split("\n") if l.strip()) + "\n"
(seat / "text").mkdir(exist_ok=True)
for w in WORKS:
    out = []
    for t in w["pages"]:
        v = idx[t]
        out.append(f"=== {t} (oldid {v['revid']}) ===")
        out.append(text_of(ws / "html" / f"{v['file']}.html"))
    (seat / "text" / f"{w['slug']}.txt").write_text("\n".join(out), encoding="utf-8")
    print(w["slug"], sum(len(x) for x in out))
