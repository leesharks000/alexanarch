#!/usr/bin/env python3
"""Build the Legitimately Many locus table: locate every phrase of loci.py in its seat (TEI citation where the seat has TEI,
else the text-layer line and the nearest page marker), refuse unlocated rows, and write loci-table.json and loci-table.md
with the count of codes by stratum. python3 build_table.py"""
import json, pathlib, collections, sys
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H))
from locate import locate_tei, locate_text, line_agreement
AGREE = {}
def _page_only(pl):
    return pl.rsplit('.', 1)[0] if pl.count('.') else pl
from loci import L
CODES = ["does_not_address", "presupposes", "argues_for", "considers_excludes", "revises", "holds_open"]
rows, missing = [], []
for r in L:
    assert r["code_attr"] in CODES and r["code_count"] in CODES, r["id"]
    where = None
    if r.get("tei"):
        where = locate_tei(str(H / r["tei"]), r["find"])
        if where and where.get("page_line"):
            ag = AGREE.setdefault(r["tei"], line_agreement(str(H / r["tei"])))
            if ag < 0.8:   # the file's physical lines do not follow the printed lines: keep the page, drop the line
                where["page_line"] = where["page_line"].split(".")[0] if "1st1K" in r["tei"] else _page_only(where["page_line"])
            where["line_basis"] = f"start-of-line <lb n> agreement {ag:.0%}" + ("" if ag >= 0.8 else "; line not derivable, page only")
    if where is None and r.get("text"):
        where = locate_text(str(H / r["text"]), r["find"])
    if where is None:
        missing.append(r["id"]); continue
    rows.append({**{k: v for k, v in r.items() if k not in ("tei", "text")}, "seat": (r.get("tei") or r.get("text")).replace("../../", ""), "located": where,
                 "coding": "provisional (session reading, 2026-11-02); the operator rules"})
if missing:
    sys.exit(f"NOT LOCATED: {missing}")
(H / "loci-table.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
def cite(w):
    if "page_line" in w:
        bits = [x for x in (w.get("textpart"), w.get("milestone")) if x]
        return " · ".join(bits + ([f"p. {w['page_line']}"] if w.get("page_line") else []))
    return f"text l. {w['text_line']}" + (f" · {w['marker']}" if w.get("marker") else "")
md = ["# Legitimately Many — the locus table", "", "Built by build_table.py from loci.py; every phrase located in its seat. Codes per design v0.5 §4.1, with *holds open* added. "
      "Coding provisional (session reading, 2026-11-02); the operator rules. Page.line for the CAG files is TEI-derived, anchored on the start-of-line <lb n> markers, to be checked against the printed page.", "",
      "| id | § | work | located | phrase | slot → filler | attribution | count |", "|---|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['id']} | {r['stratum']} | {r['work']} | {cite(r['located'])} | {r['find']} | {r['slot']} → {r['filler']} | {r['code_attr']} | {r['code_count']} |")
md += ["", "## Counts by stratum", "", "| § | n | attribution codes | count codes |", "|---|---|---|---|"]
by = collections.OrderedDict()
for r in rows:
    by.setdefault(r["stratum"], []).append(r)
for st, rs in by.items():
    ca = collections.Counter(r["code_attr"] for r in rs); cc = collections.Counter(r["code_count"] for r in rs)
    md.append(f"| {st} | {len(rs)} | " + ", ".join(f"{k} {v}" for k, v in ca.items()) + " | " + ", ".join(f"{k} {v}" for k, v in cc.items()) + " |")
ta = collections.Counter(r["code_attr"] for r in rows); tc = collections.Counter(r["code_count"] for r in rows)
md += ["", f"Total {len(rows)} loci. Attribution: " + ", ".join(f"{k} {ta[k]}" for k in CODES if ta[k]) + ". Count: " + ", ".join(f"{k} {tc[k]}" for k in CODES if tc[k]) + "."]
md += ["", "## Notes", ""] + [f"- **{r['id']}** {r['note']}" for r in rows if r.get("note")]
(H / "loci-table.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(len(rows), "located"); print(md[-len([r for r in rows if r.get('note')])-4])
