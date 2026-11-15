#!/usr/bin/env python3
"""The bibliography of Classical Receptions Journal as #1769 and #1770 cite it (2026-11-14, the author's word "yup", 21:54 EST, to: the works read cited in full,
and the register of all 405 works as an appendix in the body of #1769). Built from the audit's census.json (Crossref, read 14 November 2026) and its coding tables;
nothing is typed by hand. The civil byline of the archive author's article (doi:10.1093/crj/clu016) is withheld, as everywhere in the archive.
    python3 rebuild/hk-frameworks/biblio_crj.py <audit data dir> <out dir>"""
import csv, json, pathlib, sys
D = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
W = {w["n"]: w for w in json.loads((D / "census.json").read_text(encoding="utf-8"))["works"]}
tsv = lambda f: {int(r["n"]): r for r in csv.DictReader(open(D / f, encoding="utf-8"), delimiter="\t")}
OBJ = tsv("codes-object.tsv"); DEEP = tsv("codes-deep.tsv"); READ = tsv("cc-reading.tsv"); AV = tsv("availability.tsv")
WITHHELD = {"10.1093/crj/clu016"}
OBJN = {"F": "object held fixed", "R": "object reread", "A": "ancient reception", "Q": "object unsettled"}
DIRN = {"source→later": "source → later work", "later→source": "later work → source", "field": "the field's own terms", "ancient reception": "ancient reception",
        "source-evidence": "ancient evidence unsettled", "source": "the source reread"}
EDITOR = "10.1093/crj/clv002"
def names(w):
    if w["doi"] in WITHHELD: return "[byline withheld]"
    a = [x["name"] for x in w["authors"]]
    return "[no author in the register]" if not a else a[0] if len(a) == 1 else ", ".join(a[:-1]) + " and " + a[-1]
def lic(w):
    l = (w.get("license") or "")
    if AV.get(w["n"], {}).get("cc_in_crossref") == "True": return "licence " + l
    return ("free to read" if (AV.get(w["n"], {}).get("s2_oa_status") == "BRONZE") else "")
def entry(n, coding=True):
    w = W[n]; t = (w["title"] or "").strip().rstrip(".")
    vi = f"{w['vol']}({w['issue']})" if w.get("vol") and w.get("issue") else (w.get("vol") or "")
    s = f"{names(w)} ({w['year']}). {t}. *Classical Receptions Journal* {vi}. https://doi.org/{w['doi']}".replace(" .", ".")
    if not coding: return s
    bits = []
    if n in OBJ: bits += [OBJN.get(OBJ[n]["object"], OBJ[n]["object"]), DIRN.get(DEEP[n]["direction"], DEEP[n]["direction"]) + (f", {DEEP[n]['scale']}" if DEEP[n]["scale"] not in ("—", "") else "")]
    else: bits.append("title only")
    if n in READ or w["doi"] == EDITOR: bits.append("read in full")
    if lic(w): bits.append(lic(w))
    bits.append(f"Crossref citations {w['cited_by']}")
    return s + " · " + " · ".join(bits)
# A: the works read in full (the 37 under CC licences, and the editor's article from its repository copy)
ed = next(n for n, w in W.items() if w["doi"] == EDITOR)
A = sorted(set(READ) | {ed}, key=lambda n: (W[n]["year"], n))
# the fifteen of #1770 §3.4.1 / #1769 §4.2, chosen by title
import unicodedata as U
K = ["Duy Khi", "Basílio", "Machado", "Hilst", "Black Medea", "Antígona", "Baartman", "Du Bois", "Wheatley", "McKay", "Beloved", "Walcott", "Brazilian colonial", "Fuentes Mares"]
nf = lambda s: U.normalize("NFC", s)
F15 = sorted([n for n, w in W.items() if any(nf(k) in nf(w["title"]) for k in K)], key=lambda n: (W[n]["year"], n)); assert len(F15) == 15, len(F15)
# the works #1770 names in its prose
NAMED = [58, 212, 224, 262, 299, 243, 390, 293, 17, 32, 8, 217, 277, 275, 360, 227, ed, 110]
for n in NAMED: assert n in W, n
reg = "\n".join(f"- {entry(n)}" for n in sorted(W, key=lambda n: (W[n]["year"], n)))
(OUT / "appendix-read.md").write_text("\n".join(f"- {entry(n)}" for n in A) + "\n", encoding="utf-8")
(OUT / "appendix-register.md").write_text(reg + "\n", encoding="utf-8")
(OUT / "cited-1770.md").write_text("\n".join(f"- {entry(n, coding=False)}" for n in sorted(set(NAMED) | set(F15), key=lambda n: (W[n]["year"], n))) + "\n", encoding="utf-8")
print("read", len(A), "| register", len(W), "| 1770 cites", len(set(NAMED) | set(F15)), "| withheld", sum(1 for w in W.values() if w["doi"] in WITHHELD))
