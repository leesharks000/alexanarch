#!/usr/bin/env python3
"""build_non.py — project the Negative of the Negative v2 into alexanarch.org/non (one surface, not mirrored).

Reads, never writes back:
  datasets/negative-of-the-negative/v2/panel/panel.json          the working panel (not frozen, §7.0)
  datasets/negative-of-the-negative/v2/rows/*.json               rows with composed objects
  datasets/negative-of-the-negative/v2/traversal/*/summary.json  D/R/O string passes
  datasets/negative-of-the-negative/v2/traversal/*/reading.json  admission by reading, where done
Writes:
  non/index.html, non/index.json
  index.html for each data folder the spec links as a folder (worked-example/selection/, worked-example/audit/,
  v2/traversal/<row>/), so that those links resolve to a listing with hashes.
Deterministic apart from the build date line.
"""
import json, html, re, pathlib, hashlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DS = ROOT / "datasets/negative-of-the-negative"
V2 = DS / "v2"
OUT = ROOT / "non"
BASE = "https://www.alexanarch.org"
esc = html.escape

import sys
sys.path.insert(0, str(ROOT))
from scripts.render_navbar import render_navbar

def nav():
    """The canonical nav (data/navigation.json), with /non marked as the page in view."""
    return render_navbar(active="/non/")

def md_inline(t):
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r'<code class="cid">\1</code>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<em>\1</em>", t)
    return t

def md_block(text):
    out, inlist = [], False
    for line in text.split("\n"):
        if line.startswith("- "):
            if not inlist:
                out.append("<ul>"); inlist = True
            out.append(f"<li>{md_inline(line[2:])}</li>")
            continue
        if inlist:
            out.append("</ul>"); inlist = False
        if not line.strip():
            continue
        out.append(f"<p>{md_inline(line)}</p>")
    if inlist:
        out.append("</ul>")
    return "\n".join(out)

CSS = """
:root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.65;font-size:15px}
.wrap{max-width:980px;margin:0 auto;padding:36px 20px}
a{color:var(--accent);text-decoration:none} a:hover{color:var(--accent2)}
h1{font-size:1.5em;font-weight:600;color:var(--accent);margin-bottom:6px}
h2{font-size:1.05em;font-weight:600;color:var(--accent);margin:30px 0 10px;padding-bottom:4px;border-bottom:1px solid var(--border)}
h3{font-size:.95em;font-weight:600;margin:16px 0 6px}
p{margin-bottom:9px;color:#333}
ul{margin:0 0 10px 20px} li{margin-bottom:4px;color:#333}
code,.mono{font-family:var(--mono);font-size:.84em}
code.cid{color:var(--teal);font-size:.76em;white-space:nowrap}
.nav{display:flex;gap:12px;margin-bottom:22px;font-size:.85em;overflow-x:auto;white-space:nowrap}
.nav a{color:#777;font-weight:500}
.sub{color:var(--dim);font-size:.92em;margin-bottom:16px}
.status{background:#fef3c7;border-left:4px solid #d97706;padding:10px 14px;border-radius:6px;margin:12px 0 18px;font-size:.9em;color:#78350f}
.objs{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:10px 0 16px}
.obj{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:10px 12px;font-size:.86em}
.obj b{display:block;color:var(--accent2);font-family:var(--mono);font-size:.95em;margin-bottom:2px}
details{background:var(--surface);border:1px solid var(--border);border-radius:6px;margin:8px 0;padding:8px 14px}
details>summary{cursor:pointer;font-weight:600;color:var(--accent);font-size:.93em}
details[open]>summary{margin-bottom:8px}
table{border-collapse:collapse;width:100%;font-size:.84em;margin:8px 0 14px;background:var(--surface)}
th,td{border:1px solid var(--border);padding:5px 8px;text-align:left;vertical-align:top}
th{background:#f3f4f6;font-weight:600;color:#333}
.tw{overflow-x:auto}
.pill{display:inline-block;font-family:var(--mono);font-size:.74em;padding:1px 6px;border-radius:9px;background:#e0f2fe;color:#075985;margin-right:3px}
.foot{color:var(--dim);font-size:.82em;margin-top:30px;border-top:1px solid var(--border);padding-top:12px}
"""

def page(title, desc, body, canonical, jsonld=None):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return (f'<!DOCTYPE html>\n<html lang="en"><head>\n<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
            f'<title>{esc(title)}</title>\n<link rel="canonical" href="{canonical}">\n<meta name="description" content="{esc(desc)}">\n'
            f'<meta name="citation_author" content="Lee Sharks">\n{ld}\n<style>{CSS}</style>\n</head><body><div class="wrap">\n{nav()}\n{body}\n</div></body></html>\n')

def table(rows, cols, render=None):
    h = "".join(f"<th>{esc(c)}</th>" for c in cols)
    trs = []
    for r in rows:
        tds = "".join(f"<td>{(render or {}).get(c, lambda v: md_inline(str(v)))(r.get(c, ''))}</td>" for c in cols)
        trs.append(f"<tr>{tds}</tr>")
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'

def folder_index(folder, title, note):
    files = sorted(p for p in folder.iterdir() if p.is_file() and p.name != "index.html")
    rows = []
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        rows.append({"file": f'<a href="/{rel}">{esc(p.name)}</a>', "bytes": f"{p.stat().st_size:,}",
                     "sha256": f'<code>{hashlib.sha256(p.read_bytes()).hexdigest()}</code>'})
    body = (f'<p style="font-size:.85em"><a href="/non/">/non</a> › <code>{esc(folder.relative_to(ROOT).as_posix())}/</code></p>'
            f"<h1>{esc(title)}</h1><p class='sub'>{esc(note)}</p>"
            + table(rows, ["file", "bytes", "sha256"], {"file": str, "bytes": str, "sha256": str}))
    canon = f"{BASE}/{folder.relative_to(ROOT).as_posix()}/"
    (folder / "index.html").write_text(page(title + " — Alexanarch", note, body, canon), encoding="utf-8")

def main():
    panel = json.loads((V2 / "panel/panel.json").read_text(encoding="utf-8"))
    rows = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((V2 / "rows").glob("*.json"))}
    trav = {}
    for d in sorted((V2 / "traversal").iterdir()):
        if (d / "summary.json").exists():
            trav[d.name] = {"summary": json.loads((d / "summary.json").read_text(encoding="utf-8")),
                            "reading": json.loads((d / "reading.json").read_text(encoding="utf-8")) if (d / "reading.json").exists() else None}
    built = datetime.date.today().isoformat()

    b = []
    b.append('<h1>The Negative of the Negative</h1>')
    b.append('<p class="sub">Public knowledge, composed three ways at one address: as the composition layer gave it, as its own disclosed sources give it, and with the Crimson Hexagonal Archive admitted on equal terms. Each row is adjudicated later against what the world does.</p>')
    b.append('<div class="status"><strong>Under construction, by design.</strong> The generation procedure (EA-NEGONT-02 v0.7, <a href="/s/records/1665/">#1665</a>, which supersedes <a href="/s/records/1664/">#1664</a>) is being tested, iterated and revised; the panel below is a working list and is frozen only after the procedure is (§7.0, ruled 2026-10-05). Nothing on this page is a frozen measurement.</div>')
    b.append('<h2>How a row reads</h2><div class="objs">'
             '<div class="obj"><b>T</b>the transcript: what the composition layer gave, verbatim, with its source cards</div>'
             '<div class="obj"><b>L(B)</b>the address recomposed from the full texts of the sources the layer itself surfaced</div>'
             '<div class="obj"><b>L(B ∪ A)</b>the same algorithm with the archive\'s subset admitted on equal terms</div>'
             '<div class="obj"><b>Δ</b>T against L(B): what the disclosed field held and was not composed. L(B) against L(B ∪ A): what admission adds</div>'
             '<div class="obj"><b>K</b>the prospective kernel: what admission adds, derived from the plan, adjudicated later in both directions</div></div>')
    b.append('<p>The archive\'s subset is selected by its <strong>bearing</strong> on the address, in three strata: <strong>D</strong>, direct (the archive names the entity and says something about it); <strong>R</strong>, relational (the archive relates the entity to one of its own objects); <strong>O</strong>, ontological (the archive applies one of its own categories to the entity, or to a class the field says it belongs to). A citation hop from what reading admits finds the term-absent tail. Volume never removes a source.</p>')

    # rows with compositions
    for key, r in rows.items():
        o = r["objects"]
        b.append(f'<h2>Row: <code>{esc(r["address"])}</code> · {esc(r["surface"])} · epoch {esc(r["epoch"])}</h2>')
        b.append(f'<p class="sub">{esc(r["status"]["procedure"])}. Ledger: {esc(r["status"]["ledger"])}. Not frozen.</p>')
        tclaims = "".join(f"<li>{esc(c)}</li>" for c in o["T"]["claims"])
        b.append(f'<details><summary>T — the transcript ({o["T"]["words"]} words, {o["T"]["cards"]} cards)</summary>'
                 f'<p><a href="/{o["T"]["path"]}">verbatim text</a> · sha256 <code>{o["T"]["sha256"][:16]}…</code></p><ul>{tclaims}</ul></details>')
        fld = "".join(f"<li><strong>{esc(f['id'])}</strong> {esc(f['card'])}: {esc(f['fetched'])}</li>" for f in r["field"])
        b.append(f'<details><summary>B — the disclosed field</summary><ul>{fld}</ul></details>')
        b.append(f'<details><summary>L(B) — recomposed from the disclosed field (body {o["L_B"]["words"]} words)</summary>{md_block(o["L_B"]["text"])}</details>')
        rail = table(o["L_BA"].get("rail", []), ["Card", "Snippet"]) if o["L_BA"].get("rail") else ""
        b.append(f'<details open><summary>L(B ∪ A) — with the archive on equal terms (body {o["L_BA"]["words"]} words)</summary>{md_block(o["L_BA"]["text"])}<h3>Card rail</h3>{rail}</details>')
        b.append(f'<details><summary>Δ — the delta</summary><p><strong>T against L(B)</strong> (representational): {esc(r["delta"]["T_vs_LB"])}</p><p><strong>L(B) against L(B ∪ A)</strong> (the intervention): {esc(r["delta"]["LB_vs_LBA"])}</p></details>')
        kcols = list(r["kernel"][0].keys()) if r["kernel"] else []
        b.append(f'<details><summary>K — the prospective kernel ({len(r["kernel"])} entries; sealed only at freeze)</summary>{table(r["kernel"], kcols)}</details>')
        b.append(f'<p style="font-size:.85em">Data: <a href="/datasets/negative-of-the-negative/v2/rows/{key}.json">row</a> · '
                 f'<a href="/{r["ledger"]["archive"]}">archive ledger</a> · <a href="/{r["ledger"]["selection"]}">selection readings</a> · '
                 f'<a href="/{r["ledger"]["audit"]}">extraction audit</a></p>')

    # traversals
    b.append('<h2>D/R/O traversals</h2>')
    trows = []
    for key, t in trav.items():
        c = t["summary"]["counts"]
        rd = t["reading"]
        trows.append({"row": f'<a href="/datasets/negative-of-the-negative/v2/traversal/{key}/">{esc(t["summary"]["address"])}</a>',
                      "D": f'{c["D_deposits"]} deposits ({c["D_sentences"]})', "R": f'{c["R_deposits"]} ({c["R_sentences"]})',
                      "O": f'{c["O_deposits"]} ({c["O_direct"]} direct, {c["O_class"]} class)',
                      "hop": str(c.get("H_candidates") or "—"),
                      "reading": (f'{len(rd["verdicts"])} admitted, {len(rd["not_admitted"])} not' if rd else "unread")})
    b.append(table(trows, ["row", "D", "R", "O", "hop", "reading"], {k: str for k in ["row", "D", "R", "O", "hop", "reading"]}))
    for key, t in trav.items():
        rd = t["reading"]
        if not rd or not rd.get("lineages"):
            continue
        lrows = [{"lineage": l["lineage"], "instances": ", ".join(f"#{n}" for n in l["instances"]), "earliest": f'#{l["earliest"]}'} for l in rd["lineages"]]
        b.append(f'<details open><summary>{esc(t["summary"]["address"])} — admitted by lineage ({esc(rd["pass"])})</summary>{table(lrows, ["lineage", "instances", "earliest"])}'
                 + "".join(f"<p>{esc(x)}</p>" for x in rd.get("observations", [])) + "</details>")

    # panel
    b.append(f'<h2>The panel — {esc(panel["status"])}</h2><p class="sub">{esc(panel["rule"])} {len(panel["rows"])} rows.</p>')
    b.append(f'<details><summary>All rows</summary>{table(panel["rows"], ["address", "type", "source", "stage"])}</details>')
    b.append('<h2>Procedure and data</h2><ul>'
             '<li>Specification: <a href="/s/records/1665/">#1665</a> (EA-NEGONT-02 v0.7, 2026-10-05), superseding <a href="/s/records/1664/">#1664</a> (v0.6, 2026-10-04)</li>'
             '<li>Traversal tool: <a href="/scripts/non_traverse.py">scripts/non_traverse.py</a> · configurations: <a href="/datasets/negative-of-the-negative/v2/panel/configs/">v2/panel/configs/</a></li>'
             '<li>Panel: <a href="/datasets/negative-of-the-negative/v2/panel/panel.json">panel.json</a> · v1 rows: <a href="/datasets/negative-of-the-negative/rows.json">rows.json</a></li>'
             '<li>This page is built by <a href="/scripts/build_non.py">scripts/build_non.py</a> from those files; it writes nothing back.</li></ul>')
    b.append(f'<p class="foot">Lee Sharks · Crimson Hexagonal Archive · built {built}. The surface is single: /non is not mirrored.</p>')

    jsonld = {"@context": "https://schema.org", "@type": "Dataset", "name": "The Negative of the Negative (v2, compositional)",
              "url": f"{BASE}/non/", "creator": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
              "license": "https://creativecommons.org/licenses/by/4.0/", "creativeWorkStatus": "working; procedure not frozen",
              "isBasedOn": f"{BASE}/s/records/1665/"}
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(page("The Negative of the Negative — /non — Alexanarch",
                                         "Public knowledge composed three ways at one address, with the archive admitted on equal terms; working, not frozen.",
                                         "\n".join(b), f"{BASE}/non/", jsonld), encoding="utf-8")
    (OUT / "index.json").write_text(json.dumps({"built": built, "panel": "datasets/negative-of-the-negative/v2/panel/panel.json",
        "rows": sorted(rows), "traversals": {k: v["summary"]["counts"] for k, v in trav.items()}}, ensure_ascii=False, indent=1), encoding="utf-8")

    W = DS / "worked-example"
    folder_index(W / "selection", "Selection readings — model collapse", "The S1–S3 readings of Appendix A (§A.3): each candidate, its verdict and its quoted reason.")
    folder_index(W / "audit", "Extraction audit — model collapse", "The second extraction (§3.8, §A.9) and the control arm A′.")
    folder_index(V2 / "panel/configs", "Traversal configurations", "One configuration per address for scripts/non_traverse.py.")
    for d in sorted((V2 / "traversal").iterdir()):
        if d.is_dir():
            folder_index(d, f"D/R/O traversal — {d.name}", "Candidate files by stratum, the summary, and the reading where done. Candidates are found by string; admission is by reading.")
    print("non/index.html", (OUT / "index.html").stat().st_size, "bytes; rows", len(rows), "; traversals", len(trav))

if __name__ == "__main__":
    main()
