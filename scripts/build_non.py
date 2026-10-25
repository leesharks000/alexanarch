#!/usr/bin/env python3
"""build_non.py — project the Negative of the Negative v2 into alexanarch.org/non (one surface, not mirrored).

Reads, never writes back:
  datasets/negative-of-the-negative/v2/panel/panel.json          the working panel (not frozen, §7.0)
  datasets/negative-of-the-negative/v2/rows/*.json               rows with composed objects
  datasets/negative-of-the-negative/v2/traversal/*/summary.json  D/R/O string passes
  datasets/negative-of-the-negative/v2/traversal/*/reading.json  admission by reading, where done
Writes (one page per entity, as the Capture Registry was split on 2026-10-01; ruled for /non 2026-10-07):
  non/index.html                 the table of contents as a page: status, method, legend, one card per entity,
                                 the register summary, the panel, the procedure (well under 200 KB)
  non/index.json                 the table of contents as data: one row per entity, each entity.json's sha256
  non/{entity}/index.html        the entity's page and its citation (knowledge object first)
  non/{entity}/entity.json       the entity as a compact record; points to its row, ledgers and traversal
  sitemap-non.xml                the entity pages
  index.html for each data folder the spec links as a folder (worked-example/selection/, worked-example/audit/,
  v2/panel/configs/, v2/traversal/<row>/), so that those links resolve to a listing with hashes.
Deterministic: same data, same bytes. Any output over 4,000,000 bytes fails the build; an entity page over
600,000 bytes is warned of.

Usage:
    python3 scripts/build_non.py           # write
    python3 scripts/build_non.py --check   # fail if any output is missing or stale
"""
import json, html, re, pathlib, hashlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DS = ROOT / "datasets/negative-of-the-negative"
V2 = DS / "v2"
OUT = ROOT / "non"
BASE = "https://www.alexanarch.org"
esc = html.escape

sys.path.insert(0, str(ROOT))
from scripts.render_navbar import render_navbar
from scripts import capture_join_render as CJ
from scripts.spxi_instrument_label import label as _spxi_label, record as _spxi_record

def nav():
    """The canonical nav (data/navigation.json), with /non marked as the page in view."""
    return render_navbar(active="/non/")

def md_inline(t):
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r'<code class="cid">\1</code>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<em>\1</em>", t)
    return link_deps(t)

def link_deps(t):
    """#N in escaped text becomes a link to the record page (not inside an existing tag or entity)."""
    parts = re.split(r"(<[^>]+>)", t)
    depth = 0
    for i, p in enumerate(parts):
        if p.startswith("<a "):
            depth += 1
        elif p == "</a>":
            depth -= 1
        elif not p.startswith("<") and depth == 0:
            parts[i] = re.sub(r"(?<![\w&/])#(\d{1,4})\b", r'<a href="/s/records/\1/">#\1</a>', p)
    return "".join(parts)

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
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");
:root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}
*{margin:0;padding:0;box-sizing:border-box}

body{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.65;font-size:15px}
.wrap{max-width:900px;margin:0 auto;padding:36px 20px;min-width:0}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid rgba(26,58,92,.25)} a:hover{color:var(--accent2);border-color:var(--accent2)}
h1{font-size:1.6em;font-weight:600;color:var(--accent);margin-bottom:6px;line-height:1.3}
h2{font-size:.78em;font-family:var(--mono);font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--teal);margin:34px 0 10px;padding-bottom:5px;border-bottom:1px solid var(--border)}
h3{font-size:.95em;font-weight:600;margin:16px 0 6px}
p{margin-bottom:9px;color:#333}
ul{margin:0 0 10px 20px} li{margin-bottom:4px;color:#333}
p,li,td,th,summary,dd{overflow-wrap:anywhere}
code,.mono{font-family:var(--mono);font-size:.84em}
code.cid{color:var(--teal);font-size:.78em;white-space:normal;overflow-wrap:anywhere}
/* the nav: the captures gallery's rules, verbatim (2026-10-06: the 10-06 restyle dropped them, and the
   page's own link underline reached the nav) */
.nav{display:flex;gap:20px;margin-bottom:30px;font-size:0.85em;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch;padding-bottom:6px}
.nav a{color:var(--dim);text-decoration:none;font-weight:500;border:0}
.nav a:hover,.nav a.active{color:var(--accent)}
.sub{color:var(--dim);font-size:.92em;margin-bottom:16px}
.jump{display:flex;flex-wrap:wrap;gap:6px 14px;font-family:var(--mono);font-size:.76em;margin:14px 0 4px}
.jump a{border:0;color:var(--dim)} .jump a:hover{color:var(--accent2)}
.status{background:#fef3c7;border-left:4px solid #d97706;padding:10px 14px;border-radius:6px;margin:14px 0 18px;font-size:.88em;color:#78350f}
.status a{color:#78350f}
.objs{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px;margin:10px 0 14px}
.obj{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:9px 11px;font-size:.84em;color:#444}
.obj b{display:block;color:var(--accent2);font-family:var(--mono);font-size:.95em;margin-bottom:2px}
/* the card: captures grammar */
.card{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:16px;margin-bottom:12px}
.trec{margin-top:10px;border-top:1px dashed var(--border);padding-top:8px}.trec>summary{cursor:pointer;font-family:var(--mono);font-size:.76em;color:var(--dim)}.trec-t{white-space:pre-wrap;word-break:break-word;font-family:var(--mono);font-size:.78em;line-height:1.5;max-height:460px;overflow:auto;background:var(--bg);border:1px solid var(--border);border-radius:4px;padding:10px;margin-top:6px}
.card-head{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px;margin-bottom:6px}
.card-section{font-family:var(--mono);font-size:.72em;color:var(--teal);text-transform:uppercase;letter-spacing:.06em}
.card-date{font-family:var(--mono);font-size:.74em;color:var(--dim)}
.card-query{font-weight:600;color:var(--accent);font-size:1.15em;margin-bottom:6px;line-height:1.4}
.card-query a{border:0}
.card-query{overflow-wrap:anywhere}
.card-status{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:10px;font-size:.78em}
.pill{display:inline-block;font-family:var(--mono);font-size:.92em;padding:1px 7px;border-radius:9px;background:#e0f2fe;color:#075985;white-space:normal;max-width:100%}
.pill.warn{background:#fef3c7;color:#92400e} .pill.ok{background:#dcfce7;color:#166534} .pill.dim{background:#f3f4f6;color:#555}
.card-links{font-family:var(--mono);font-size:.74em;color:var(--dim);display:flex;flex-wrap:wrap;gap:4px 12px;margin-top:12px;padding-top:10px;border-top:1px solid var(--border)}
.card-links a{border:0}
/* collapsibles */
details{border:1px solid var(--border);border-radius:6px;margin:6px 0;background:#fcfcfc}
details>summary{cursor:pointer;padding:8px 12px;font-size:.88em;color:#444;list-style:none;display:flex;gap:8px;align-items:baseline}
details>summary::-webkit-details-marker{display:none}
details>summary::before{content:"\\25B8";color:var(--teal);font-size:.85em;flex:none;transition:transform .15s}
details[open]>summary::before{transform:rotate(90deg)}
details>summary:hover{color:var(--accent2)}
details>summary>span:not(.k):not(.n){flex:1 1 12em;min-width:0}
details>summary{flex-wrap:wrap}
details>summary .k{font-family:var(--mono);font-weight:500;color:var(--accent2);flex:none}
details>summary .n{color:var(--dim);font-family:var(--mono);font-size:.86em;margin-left:auto;flex:0 1 auto;min-width:0;max-width:100%;overflow-wrap:anywhere;padding-left:8px}
details[open]>summary{border-bottom:1px solid var(--border)}
details>.inner{padding:10px 14px 6px}
details details{background:var(--surface)}
.stack>details{margin:5px 0}
dl.kv{display:grid;grid-template-columns:max-content 1fr;gap:3px 12px;font-size:.86em}
dl.kv dt{color:var(--dim);font-family:var(--mono);font-size:.9em}
dl.kv dd{color:#333;min-width:0}
table{border-collapse:collapse;width:100%;font-size:.84em;margin:6px 0 12px;background:var(--surface)}
th,td{border-bottom:1px solid var(--border);padding:6px 8px;text-align:left;vertical-align:top}
th{font-family:var(--mono);font-size:.82em;font-weight:500;color:var(--dim);text-transform:uppercase;letter-spacing:.04em}
.tw{overflow-x:auto;max-width:100%}
/* the knowledge object */
.ko{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:6px;padding:18px 22px;margin:4px 0 8px}
.ko-head{font-family:var(--mono);font-size:.72em;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin-bottom:4px}
.ko-title{font-size:1.3em;color:var(--accent);margin:0 0 10px;font-family:Georgia,"Times New Roman",serif;font-weight:600}
.ko p{font-family:Georgia,"Times New Roman",serif;font-size:1.04em;line-height:1.75;color:#222}
.prov-s{font-size:.9em;color:#222}
ul.claims{list-style:none;margin:0} ul.claims>li{font-size:.86em;color:#444;padding:6px 0;border-bottom:1px dashed var(--border)} ul.claims>li:last-child{border:0}
ul.claims .qt{color:#222;font-style:italic}
ul.claims .qt::before{content:"\\201C"} ul.claims .qt::after{content:"\\201D"}
.meta{font-family:var(--mono);font-size:.82em;color:var(--dim)}
.plist{list-style:none;margin:0}
.plist>li{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;padding:6px 0;border-bottom:1px solid var(--border);font-size:.88em}
.plist>li:last-child{border:0}
.plist .stage{color:var(--dim);font-size:.9em;flex-basis:100%}
.foot{color:var(--dim);font-size:.82em;margin-top:30px;border-top:1px solid var(--border);padding-top:12px}
.arms{display:inline-flex;border:1px solid var(--border);border-radius:999px;padding:3px;margin:4px 0 12px;background:#f5f5f5;gap:2px;flex-wrap:wrap}
.arms button{border:0;background:none;font:500 .8em var(--sans);color:#555;padding:5px 12px;border-radius:999px;cursor:pointer}
.arms button[aria-pressed="true"]{background:var(--surface);color:var(--accent);box-shadow:0 1px 2px rgba(0,0,0,.12)}
/* two levels of resolution: the compression (popup) and the expansion (entry), one simultaneous projection (2026-10-06) */
.lv{margin:6px 0 10px}
.lv-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:14px}
.lv-grid>*,.pop,.rail{min-width:0}
.lv-label{font-family:var(--mono);font-size:.68em;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin-bottom:6px;display:flex;justify-content:space-between;gap:8px}
.pop{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px 16px 12px;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.pop-lede{font-size:1.02em;line-height:1.6;color:#1f1f1f;margin-bottom:10px}
.pop-lede b{color:var(--accent)}
.pop h4{font-size:.92em;font-weight:600;color:#222;margin:12px 0 4px}
.pop ul.pi-list{list-style:none;margin:0}
.pop details.pi{border:0;background:none;margin:0;border-radius:6px}
.pop details.pi>summary{display:block;padding:4px 6px 4px 16px;font-size:.92em;color:#2a2a2a;position:relative;line-height:1.5}
.pop details.pi>summary::before{content:"•";position:absolute;left:4px;top:4px;color:var(--teal);transform:none}
.pop details.pi[open]>summary{border-bottom:0}
.pop details.pi>summary b{color:#111}
.pop .pi-x{font-family:var(--mono);font-size:.72em;color:var(--teal);margin-left:4px;white-space:nowrap}
.pop .pi-exp{margin:2px 0 8px 16px;padding:8px 10px;border-left:3px solid var(--accent);background:#f7f9fb;font-family:Georgia,"Times New Roman",serif;font-size:.95em;line-height:1.6;color:#222}
.pop .pi-exp a{font-family:var(--mono);font-size:.72em;border:0;margin-left:4px}
.pi.hl>summary,.ks.hl{background:#fff3c4;border-radius:4px}
.ks{transition:background .15s;border-radius:3px;cursor:default}
.ks[data-p]:hover{background:#fff8dd}
.rail{display:flex;gap:8px;overflow-x:auto;padding:10px 2px 4px;margin-top:10px;border-top:1px solid var(--border);-webkit-overflow-scrolling:touch;scroll-snap-type:x proximity}
.rail details.lc{flex:0 0 200px;scroll-snap-align:start;background:#fbfbfb;border:1px solid var(--border);border-radius:8px;margin:0;font-size:.8em}
.rail details.lc[open]{flex-basis:300px;background:var(--surface)}
.rail details.lc>summary{display:block;padding:8px 10px;color:#333;line-height:1.35}
.rail details.lc>summary::before{content:none}
.rail .lc-n{font-family:var(--mono);color:var(--teal);margin-right:4px}
.rail .lc-e{display:block;color:var(--dim);font-size:.92em;margin-top:3px}
.rail .lc-c{display:block;color:var(--accent);font-family:var(--mono);font-size:.85em;margin-top:3px}
.rail ul.claims{padding:0 10px 8px}
.ent .ko{margin-top:0}
.ent .ko p{font-size:1em}
.flg{width:auto;min-width:60%;font-size:.8em}
@media (min-width:960px){
 .wrap{max-width:1180px}
 .lv-grid{grid-template-columns:minmax(0,5fr) minmax(0,6fr);align-items:start;gap:22px}
 .lv-pop{position:sticky;top:12px}
 .pop .pi-exp{display:none}
 .pop details.pi>summary{cursor:pointer}
}
@media (max-width:560px){.wrap{padding:24px 14px}.ko{padding:14px 15px}.card{padding:13px}dl.kv{grid-template-columns:1fr}dl.kv dt{margin-top:4px}}
"""

def page(title, desc, body, canonical, jsonld=None):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return (f'<!DOCTYPE html>\n<html lang="en"><head>\n<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
            f'<title>{esc(title)}</title>\n<link rel="canonical" href="{canonical}">\n<meta name="description" content="{esc(desc)}">\n'
            f'<meta name="citation_author" content="Lee Sharks">\n{ld}\n<style>{CSS}</style>\n</head><body><div class="wrap">\n{nav()}\n{body}\n</div>\n<script src="https://www.themandalaoracle.com/embed/sigil.js" defer></script>\n</body></html>\n')

def table(rows, cols, render=None):
    h = "".join(f"<th>{esc(c)}</th>" for c in cols)
    trs = []
    for r in rows:
        tds = "".join(f"<td>{(render or {}).get(c, lambda v: md_inline(str(v)))(r.get(c, ''))}</td>" for c in cols)
        trs.append(f"<tr>{tds}</tr>")
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'

def det(key, label, inner, n="", open_=False, cls=""):
    """One collapsible entry: a key glyph, a label, a count at the right."""
    k = f'<span class="k">{key}</span>' if key else ""
    nn = f'<span class="n">{n}</span>' if n else ""
    return (f'<details{" open" if open_ else ""}{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}><summary>{k}<span>{label}</span>{nn}</summary>'
            f'<div class="inner">{inner}</div></details>')

def unquote(q):
    """The quote's own text, without the quotation marks the ledger stored around it (the page supplies them)."""
    q = (q or "").strip()
    while len(q) > 1 and q[0] in "\"“'‘" and q[-1] in "\"”'’":
        q = q[1:-1].strip()
    return q

def cite_links(tx):
    """A transcript for reading: each inline citation [n](url) shown as the numbered link the layer rendered.
    The register keeps the transcript as cleaned; this changes the page only."""
    t = esc(tx)
    return re.sub(r"\[(\d{1,2})\]\((https?://[^)\s]+)\)", lambda m: f'<a href="{m.group(2)}" rel="nofollow noopener">[{m.group(1)}]</a>', t)

def kv(d):
    return '<dl class="kv">' + "".join(f"<dt>{esc(str(k))}</dt><dd>{md_inline(str(v))}</dd>" for k, v in d.items()) + "</dl>"

def address_href(row, address):
    for slug in (row, re.sub(r"[^a-z0-9]+", "-", address.lower()).strip("-")):
        if slug and (ROOT / "addresses" / slug / "index.html").exists():
            return f"/addresses/{slug}/"
    return None

def _sources():
    reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
    # archive sources that are surfaces, not deposits (admitted outside the string pass; first: spxi.dev, 2026-10-13)
    reg["spxi.dev"] = {"title": "spxi.dev — the protocol's canonical surface (current; not a deposit)", "creator": "Lee Sharks / Rex Fraction", "date": "2026-10-13"}
    return reg

def dep_href(dep):
    return f"/s/records/{dep}/" if isinstance(dep, int) else {"spxi.dev": "https://www.spxi.dev/"}.get(dep, "#")

def dep_label(dep):
    return f"#{dep}" if isinstance(dep, int) else str(dep)

def claim_li(cid, ko, ledger, reg, FC=None, FS=None):
    """One sourced claim, the same rendering wherever it appears (provenance list, lineage card)."""
    FC = FC if FC is not None else ko["field_claims"]
    FS = FS if FS is not None else ko["field_sources"]
    if cid not in FC and cid not in ledger:
        # a claim the row cites and neither ledger holds: recorded on the page, never dropped (2026-10-24)
        return f'<li><code class="cid">{esc(cid)}</code> <span class="pill warn">unresolved: in neither the field claims nor the archive ledger</span></li>'
    if cid in FC:
        f = FC[cid]
        return (f'<li><code class="cid">{esc(cid)}</code> {esc(FS.get(f["source"], f["source"]))}, {esc(f["locus"])} '
                f'<span class="pill dim">documented · field</span><br><span class="qt">{esc(unquote(f["quote"]))}</span></li>')
    c = ledger[cid]
    # a source that is not a deposit (a blog post, a surface) carries its own title, creator and url in the ledger
    d = reg.get(c["dep"]) or {"title": c.get("title") or str(c["dep"]), "creator": c.get("creator"), "date": c.get("date")}
    href = dep_href(c["dep"]) if c["dep"] in reg or isinstance(c["dep"], int) else ((c.get("surface") or {}).get("url") or "#")
    return (f'<li><code class="cid">{esc(cid)}</code> <a href="{href}">{esc(dep_label(c["dep"]))}</a> <em>{esc(d["title"][:120])}</em> '
            f'<span class="meta">{esc(str(d.get("creator") or ""))} · {esc(str(c.get("date") or ""))} · {esc(c["locus"])}</span> '
            f'<span class="pill">{esc(c["modality"])}</span><br><span class="qt">{esc(unquote(c["quote"]))}</span></li>')

def lineage_rail(row):
    """L(B ∪ A)'s card rail at spec §5.2: one visible card per lineage, its snippet the lineage's earliest instance,
    the other source instances nested under it; a source in no lineage keeps its own card. The lineages are the
    compression's (objects.P.rail); a claim's source is the ledger's deposit or the field claim's source."""
    o = row["objects"]; cards = o["L_BA"].get("rail") or []
    if not cards:
        return ""
    ledger = {c["id"]: c for c in json.loads((ROOT / row["ledger"]["archive"]).read_text(encoding="utf-8"))}
    FC = {**row.get("field_claims", {}), **(o.get("KO") or {}).get("field_claims", {})}
    def ckey(card):
        m = re.match(r"#(\d+)\b", card)
        return int(m.group(1)) if m else card.split()[0]
    bykey = {ckey(c["Card"]): c for c in cards}
    def src(cid):
        if cid in ledger: return ledger[cid]["dep"]
        if cid in FC: return FC[cid]["source"]
        m = re.match(r"[A-Z](\d+)-", cid)
        return int(m.group(1)) if m else None
    used, out = set(), []
    for i, ln in enumerate((o.get("P") or {}).get("rail") or [], 1):
        docs = []
        for c in ln["claims"]:
            k = src(c)
            if k in bykey and k not in docs: docs.append(k)
        e = ln["earliest"]
        if e not in docs and e in bykey: docs.insert(0, e)
        if not docs: continue
        lead = e if e in docs else docs[0]
        used.update(docs)
        rest = [d for d in docs if d != lead]
        inner = "".join(f'<li>{md_inline(bykey[d]["Card"])} — {md_inline(bykey[d]["Snippet"])}</li>' for d in rest)
        out.append(f'<details class="lc"><summary><span class="lc-n">{i}</span>{esc(ln["lineage"])}'
                   f'<span class="lc-e">{md_inline(bykey[lead]["Card"])} — {md_inline(bykey[lead]["Snippet"])}</span>'
                   f'<span class="lc-c">{len(docs)} source{"" if len(docs) == 1 else "s"}</span></summary>'
                   + (f'<ul class="claims">{inner}</ul>' if inner else '<p class="meta">one source</p>') + '</details>')
    own = [c for k, c in bykey.items() if k not in used]
    for c in own:
        out.append(f'<details class="lc"><summary><span class="lc-n">·</span>{md_inline(c["Card"])}'
                   f'<span class="lc-e">{md_inline(c["Snippet"])}</span><span class="lc-c">own card</span></summary>'
                   '<p class="meta">a source in no shared lineage keeps its own card (§5.2)</p></details>')
    return (f'<h3>Card rail</h3><p class="meta">One card per lineage (§5.2): {len(out) - len(own)} lineages carry '
            f'{len(used)} of {len(bykey)} sources; {len(own)} keep their own card. Expand a lineage for its instances.</p>'
            f'<div class="rail" aria-label="Sources, one card per lineage">{"".join(out)}</div>')

TYPE_KEY = {"A": "the archive coined it", "B": "a rival occupant holds it", "C": "a conventional reading holds it",
            "I": "the archive's infrastructure", "E": "the archive's own entity", "Op": "an operator, composed as its own object"}

def type_code(t):
    """The type's code (A, B, C, E, I; Op for an operator SPXI-gnΩsis composes), read from the front of the type as the
    panel states it; the statement itself is kept whole beside it (2026-10-24: the code is what a filter reads)."""
    m = re.match(r"\s*(Op|[ABCEI])(?:/(?:[ABCEI]))?(?![a-z])", str(t or ""))
    return m.group(1) if m else "?"

# ── provenance, identifiers and history (2026-10-24) ──
AXN_LEDGER = V2 / "axn.json"
LANDINGS_F = V2 / "landings.json"

def load_axn():
    return json.loads(AXN_LEDGER.read_text(encoding="utf-8"))["entries"] if AXN_LEDGER.exists() else {}

def load_landings():
    """The latest landing of each row (scripts/land_non_row.py)."""
    out = {}
    if LANDINGS_F.exists():
        for x in json.loads(LANDINGS_F.read_text(encoding="utf-8"))["landings"]:
            out[x["row"]] = x
    return out

def composition_of(r, landing=None):
    """Who composed the row, and under what, as one block for every row. Read from what the row itself states, never
    inferred: a session row's composition_v09 and status; a gnosis row's composition_gnosis, its T's provenance, and
    the landing record. The row file is not changed."""
    if not r:
        return None
    st = r.get("status") or {}
    cg = r.get("composition_gnosis")
    if cg:
        sv = cg.get("service") or {}
        out = {"composer_class": "gnosis", "composer": f'{sv.get("name", "SPXI-gnΩsis")} {sv.get("version", "")}'.strip(),
               "service": sv, "protocol": cg.get("protocol"), "mode": cg.get("mode"), "models": cg.get("models"),
               "archive_release": cg.get("archive_release"), "passes": len(cg.get("passes") or []),
               "cost_usd": cg.get("cost_usd"), "seconds": cg.get("seconds"),
               "t_provenance": ((r.get("objects") or {}).get("T") or {}).get("provenance"),
               "readings": st.get("readings")}
        if landing:
            out["landing"] = {"landed": landing.get("landed"), "execution_key": landing.get("execution_key"),
                              "result_id": landing.get("result_id"), "manifest_sha256": landing.get("manifest_sha256"),
                              "source": landing.get("source"), "record": f"{BASE}{DS_URL}/landings.json"}
    else:
        cv = r.get("composition_v09") or {}
        out = {"composer_class": "session", "composer": cv.get("composer"),
               **({} if cv.get("composer") else {"composer_note": "the row does not name its composer"}),
               "source": cv.get("source")}
    out.update({"spec": r.get("spec"), "epoch": r.get("epoch"), "procedure": st.get("procedure"), "ledger": st.get("ledger"),
                "frozen": bool(st.get("frozen")), "composed": bool((r.get("objects") or {}).get("KO")),
                **({"note": r["objects"]["note"]} if (r.get("objects") or {}).get("note") else {}),
                **({"breaches": r["breaches"]} if r.get("breaches") else {})})
    return {k: v for k, v in out.items() if v is not None}

READING_NOTE = ("A reader that fetches this page may stop short of its end; the entry's text, every sentence of its knowledge object "
                "with the claims it cites and each claim's quote, source and locus, is in entity.json beside it.")

def entry_of(r, reg):
    """The entry itself, for entity.json (2026-10-24: the record carries the entry, as a capture's record.json carries
    the composition): the knowledge object's title, the compression's lede, every sentence with its claims, and each
    claim's quote, source and locus. Read from the row and its archive ledger; the row is the authority."""
    o = (r or {}).get("objects") or {}
    ko = o.get("KO")
    if not ko:
        return {"composed": False, "note": o.get("note") or "no knowledge object composed"}
    P = o.get("P") or {}
    try:
        ledger = {c["id"]: c for c in json.loads((ROOT / r["ledger"]["archive"]).read_text(encoding="utf-8"))}
    except Exception:
        ledger = {}
    FC = {**(r.get("field_claims") or {}), **(ko.get("field_claims") or {})}
    FS = {**(r.get("field_sources") or {}), **(ko.get("field_sources") or {})}
    claims = {}
    for s in ko.get("sentences") or []:
        for cid in s.get("claims") or []:
            if cid in claims:
                continue
            if cid in FC:
                f = FC[cid]
                claims[cid] = {"kind": "field", "quote": unquote(f.get("quote")), "source": f.get("source"),
                               "source_label": FS.get(f.get("source")), "locus": f.get("locus"), "modality": f.get("modality")}
            elif cid in ledger:
                c = ledger[cid]
                d = reg.get(c["dep"]) or {}
                claims[cid] = {"kind": "archive", "quote": unquote(c.get("quote")), "deposit": c["dep"] if isinstance(c["dep"], int) else None,
                               "source_label": (f'#{c["dep"]} {d.get("title", "")}'.strip() if isinstance(c["dep"], int) else str(c.get("title") or c["dep"])),
                               "record": (f'{BASE}/s/records/{c["dep"]}/' if isinstance(c["dep"], int) else (c.get("surface") or {}).get("url") or (c.get("record") or {}).get("url")),
                               "locus": c.get("locus"), "modality": c.get("modality"), "date": c.get("date")}
            else:
                claims[cid] = {"kind": "unresolved", "note": "in neither the field claims nor the archive ledger"}
    return {"composed": True, "title": ko.get("title"), "genre": ko.get("genre"), "status": ko.get("status"),
            "compression": {"title": P.get("title"), "lede": (P.get("lede") or {}).get("text")} if P else None,
            "sentences": [{"n": s.get("n"), "para": s.get("para"), "text": s.get("text"), "claims": s.get("claims") or []} for s in ko.get("sentences") or []],
            "claims": claims,
            "note": ("The knowledge object (KO): the entry as public knowledge, each sentence sourced by the claims it lists. The compression, "
                     "the field-only arm, the transcript, the delta and the kernel are in the row (links.row), which is the authority.")}

# Link, cite and research (2026-10-24: "all the /non articles need buttons to link, cite, and research on chatgpt or
# google. deposits have the research links. captures have the copy and cite links"). The entity is searched as named,
# and again with its /non title, which can bring up the /non material itself.
COPY_JS = ("<script>document.addEventListener('click',function(ev){var b=ev.target.closest('[data-act]');"
           "if(!b||(b.dataset.act!=='cite'&&b.dataset.act!=='link'))return;ev.preventDefault();"
           "var t=b.dataset.act==='cite'?b.dataset.citation:b.dataset.cite;"
           "if(navigator.clipboard){navigator.clipboard.writeText(t).then(function(){var o=b.textContent;"
           "b.textContent='copied';setTimeout(function(){b.textContent=o},1200)})}});</script>")

def non_title(name):
    return f"{name} — The Negative of the Negative"

def citation_of(name, url, axn, date):
    return (f'Sharks, Lee. "{non_title(name)}"' + (f" [{axn}]" if axn else "") + f", {date or 'n.d.'}. "
            f"The Negative of the Negative (EA-NEGONT-02), Crimson Hexagonal Archive, Alexanarch. {url}")

def research_links(name):
    from urllib.parse import quote_plus as qp
    nt = non_title(name)
    g = lambda q: f"https://www.google.com/search?q={qp(q)}"
    c = lambda q: f"https://chatgpt.com/?q={qp(q)}"
    return {
        "google": g(name),
        "google_non": g(f'"{nt}"'),
        "chatgpt": c(f"What is {name}? Ground your answer in a reading of the sources themselves."),
        "chatgpt_non": c(f"What does \u201c{nt}\u201d (alexanarch.org/non) say about {name}? Ground your answer in a reading of the entry itself."),
    }

def action_row(name, url, axn, date):
    r = research_links(name)
    A = 'target="_blank" rel="noopener"'
    return ('<div class="nact">'
            f'<button type="button" class="nbtn" data-act="link" data-cite="{esc(url)}" aria-label="Copy the permalink to this entry">⛓ Link</button>'
            f'<button type="button" class="nbtn" data-act="cite" data-cite="{esc(url)}" data-citation="{esc(citation_of(name, url, axn, date))}" aria-label="Copy a citation for this entry">¶ Cite</button>'
            f'<span class="nres">Search: <a href="{esc(r["google"])}" {A}>Google ↗</a> '
            f'<a href="{esc(r["google_non"])}" {A}>with its /non title ↗</a> · '
            f'<a href="{esc(r["chatgpt"])}" {A}>Ask ChatGPT ↗</a> '
            f'<a href="{esc(r["chatgpt_non"])}" {A}>about this entry ↗</a></span></div>')

ACT_CSS = ('<style>.nact{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin:6px 0 12px;font-size:.84em}'
           '.nbtn{font:inherit;font-family:var(--mono);font-size:.92em;padding:3px 10px;border:1px solid var(--border);border-radius:999px;background:var(--surface);color:var(--accent);cursor:pointer}'
           '.nbtn:hover{border-color:var(--accent2);color:var(--accent2)}.nres{color:#555}.nres a{margin-right:4px}</style>\n')

def earlier_rows(k):
    """Rows an entity had before a landing replaced them, kept by scripts/land_non_row.py under v2/history/<row>/."""
    d = V2 / "history" / k
    out = []
    if d.is_dir():
        for sub in sorted(d.iterdir(), reverse=True):
            p = sub / "rows" / f"{k}.json"
            if p.is_file():
                rr = json.loads(p.read_text(encoding="utf-8"))
                out.append({"replaced": sub.name[:10], "epoch": rr.get("epoch"), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                            "row": f"{BASE}/{p.relative_to(ROOT).as_posix()}", "folder": f"{BASE}/{sub.relative_to(ROOT).as_posix()}/",
                            "composition": composition_of(rr)})
    return out

def composition_line(c):
    """The composition block in one line, for the page."""
    if not c:
        return ""
    if c["composer_class"] == "gnosis":
        rel = (c.get("archive_release") or {}).get("archive_commit") or ""
        s = (f'composed by <strong><a href="{GNOSIS}">{esc(c["composer"])}</a></strong> · {esc(str(c.get("protocol") or ""))} · {esc(str(c.get("mode") or ""))}'
             + (f' · models {esc(", ".join(f"{k} {v}" for k, v in (c.get("models") or {}).items()))}' if c.get("models") else "")
             + (f' · archive at <code>{esc(rel[:12])}</code>' if rel else "")
             + f' · {c.get("passes", 0)} passes')
        if c.get("landing"):
            L = c["landing"]
            s += (f' · landed {esc(str(L.get("landed")))}, execution key <code>{esc(str(L.get("execution_key") or "")[:16])}</code>'
                  f' (<a href="{DS_URL}/landings.json">landing record</a>)'
                  + (f' · result <a href="{GNOSIS}v1/results/{esc(L["result_id"])}/composition"><code>{esc(L["result_id"])}</code></a>' if L.get("result_id") else ""))
        return s
    who = esc(c["composer"]) if c.get("composer") else '<span class="meta">composer not named in the row</span>'
    return f'composed in session · {who}'

def type_label(t):
    """'C (public entity)' → 'type C — a conventional reading holds it (public entity)': the code never appears bare."""
    m = re.match(r"\s*([ABCEI])(?:/([ABCEI]))?\s*(\(.*\))?\s*$", str(t))
    if not m:
        return f"type {t}"
    codes = [c for c in m.groups()[:2] if c]
    return "type " + "/".join(codes) + " — " + "; ".join(TYPE_KEY[c] for c in codes) + (f" {m.group(3)}" if m.group(3) else "")

def t_record(row):
    """AIO's transcript as a record inside the compression, opened on expansion (v0.8 §4.8, ruled 2026-10-08)."""
    T = row["objects"]["T"]
    txt = (ROOT / T["path"]).read_text(encoding="utf-8").strip()
    ref = T.get("register") or {}
    return (f'<details class="trec"><summary>AIO\'s transcript, a record · {esc(row["address"])} · {esc(row["surface"])} · '
            f'{T["words"]} words · {T["cards"]} cards</summary><pre class="trec-t">{esc(txt)}</pre>'
            + (f'<p class="meta">register entry <a href="/non/{esc(row["entity"])}/#reg-{esc(ref["slug"])}">{esc(ref["slug"])}</a></p>' if ref.get("slug") else "")
            + '</details>')

CASE_LABEL = {"equal": "equal terms, ontology included (v0.9)", "witness": "the archive's ontology rules, the suppressed witness (v0.9)",
              "mixed": "equal terms, the archive ruling its own senses (v0.9)", "archive": "composed in the archive's ontology (v0.8)"}

def spec_no(en, r=None):
    """The specification an entry is composed under: the row's own spec where it names one (2026-10-24: a row SPXI-gnΩsis
    composes states it; its panel entry carries no ontology); else v0.9 (#1690) for a case-read composition, v0.8 (#1671),
    or v0.7 (#1665)."""
    m = re.search(r"#(\d+)", str((r or {}).get("spec") or ""))
    if m:
        return int(m.group(1))
    on = en.get("ontology") or {}
    return 1690 if on.get("composition") in ("equal", "witness", "mixed") else (1671 if on else 1665)

def onto_line(en):
    """The entity's type line: the composition's case and ontology first, the field's type after it."""
    on = en.get("ontology")
    if not on:
        return type_label(en["type"])
    return f"{CASE_LABEL.get(on.get('composition'), 'composed in the archive' + chr(39) + 's ontology')} · ρ = {on['rho']} · the field's {type_label(en['type'])}"

def _words(t):
    return len(re.findall(r"[A-Za-z0-9'’-]+", t or ""))

def two_levels(row, key, pk="P", kk="KO", arm="Field and archive (B ∪ A)"):
    """The compression and the expansion as one simultaneous projection.

    The compression (objects.P, the popup) is the surface; the expansion (objects.KO, the entry) is projected
    beside it, not after it as a follow-up turn. The correspondence between the two levels is not authored:
    a compression line and an expansion sentence correspond when they share a claim id, so the links are
    computed from the ledger. Desktop: two columns, the compression held in view, pointing at a line on either
    side lights its counterparts on the other. Phone: each compression line opens in place into the expansion
    sentences it compresses, and the whole entry follows below."""
    o = row["objects"]; pop, ko = o[pk], o[kk]
    ledger = {c["id"]: c for c in json.loads((ROOT / row["ledger"]["archive"]).read_text(encoding="utf-8"))}
    reg = _sources()
    FC = {**row.get("field_claims", {}), **ko.get("field_claims", {})}
    FS = {**row.get("field_sources", {}), **ko.get("field_sources", {})}
    sents = ko["sentences"]
    def match(claims):
        cs = set(claims)
        return [x["n"] for x in sents if cs & set(x["claims"])]
    items = []  # (pid, claims)
    # compression
    pc = [f'<div class="lv-pop"><div class="lv-label"><span>Compression · {esc(arm)}</span><span>{esc(row["address"])}</span></div><div class="pop">']
    lk = match(pop["lede"]["claims"])
    items.append(("p0", pop["lede"]["claims"]))
    pc.append(f'<p class="pop-lede pi-lede" id="{key}-p0" data-k="{" ".join(map(str, lk))}"><b>{esc(pop["title"])}</b> {esc(pop["lede"]["text"])}</p>')
    n = 0
    for sec in pop["sections"]:
        pc.append(f'<h4>{esc(sec["icon"])} {esc(sec["head"])}</h4><ul class="pi-list">')
        for it in sec["items"]:
            n += 1; pid = f"p{n}"; items.append((pid, it["claims"]))
            ks = match(it["claims"])
            exp = " ".join(f'{esc(x["text"])}<a href="#{key}-ks{x["n"]}">§{x["n"]}</a>' for x in sents if x["n"] in ks)
            lab = f'<b>{esc(it["label"])}</b> ' if it["label"] else ""
            pc.append(f'<li><details class="pi" id="{key}-{pid}" data-k="{" ".join(map(str, ks))}"><summary>{lab}{esc(it["text"])}'
                      f'<span class="pi-x">{len(ks)}↘</span></summary><div class="pi-exp">{exp}</div></details></li>')
        pc.append('</ul>')
    # the rail: one card per lineage, its earliest instance named
    cards = []
    for i, ln in enumerate(pop["rail"], 1):
        e = ln["earliest"]
        if isinstance(e, str):
            src = FS.get(e, e); eh = esc(src)
        else:
            d = reg.get(e) or {"title": f"#{e}"}; eh = f'#{e} {esc(d["title"][:70])} · {esc(str(d.get("date") or ""))}'
        others = sorted({dep_label(ledger[c]["dep"]) if c in ledger else FC[c]["source"] if c in FC else f"{c} unresolved" for c in ln["claims"]}, key=str)
        cards.append(f'<details class="lc"><summary><span class="lc-n">{i}</span>{esc(ln["lineage"])}<span class="lc-e">{eh}</span>'
                     f'<span class="lc-c">{len(ln["claims"])} claim{"" if len(ln["claims"]) == 1 else "s"} · {esc(", ".join(others))}</span></summary>'
                     f'<ul class="claims">{"".join(claim_li(c, ko, ledger, reg, FC, FS) for c in ln["claims"])}</ul></details>')
    pc.append(f'<div class="rail" aria-label="Sources, one card per lineage">{"".join(cards)}</div>'
              + (t_record(row) if pk == "P" and row.get("ontology") else "") + '</div></div>')
    # expansion: the entry, each sentence addressable and linked back to the compression lines that share its claims
    back = {x["n"]: [pid for pid, cl in items if set(cl) & set(x["claims"])] for x in sents}
    paras = {}
    for x in sents:
        paras.setdefault(x["para"], []).append(
            f'<span class="ks" id="{key}-ks{x["n"]}" data-p="{" ".join(back[x["n"]])}">{esc(x["text"])}</span>')
    ec = [f'<div class="ent"><div class="lv-label"><span>Expansion · {esc(arm)}</span><span>{len(sents)} sentences · every one sourced below</span></div>',
          '<div class="ko">', f'<h3 class="ko-title">{esc(ko["title"])}</h3>']
    ec += [f"<p>{' '.join(v)}</p>" for _, v in sorted(paras.items())]
    ec.append('</div>')
    entries = []
    for x in sents:
        entries.append(det(f'{x["n"]}.', f'<span class="prov-s">{esc(x["text"])}</span>',
                           f'<ul class="claims">{"".join(claim_li(c, ko, ledger, reg, FC, FS) for c in x["claims"])}</ul>', n=f'{len(x["claims"])}'))
    used = {c for x in sents for c in x["claims"]}
    nf = sum(1 for c in used if c in FC)
    ec.append(det("", "Provenance — every sentence sourced",
                  f'<p class="meta">{len(sents)} sentences; {nf} field claims, {len(used) - nf} archive claims. Modality is the source\'s own; the prose carries it in its grammar.</p>'
                  f'<div class="stack">{"".join(entries)}</div>', n=f'{len(sents)} sentences'))
    ec.append('</div>')
    # the numbers for the row's form ledger, computed
    pw = _words(pop["lede"]["text"]) + _words(pop["title"]) + sum(_words(it["label"] + " " + it["text"]) for s_ in pop["sections"] for it in s_["items"])
    pcl = set(pop["lede"]["claims"]) | {c for s_ in pop["sections"] for it in s_["items"] for c in it["claims"]}
    kw = sum(_words(x["text"]) for x in sents)
    stats = {"P": {"words": pw, "claims": pcl, "rail": len(pop["rail"])}, "KO": {"words": kw, "claims": used, "sentences": len(sents)}}
    script = ('<script>(function(){var r=document.getElementById("lv-' + key + '");if(!r)return;'
              'function on(ids,cls){ids.forEach(function(i){var e=document.getElementById(i);if(e)e.classList.add(cls)})}'
              'function clear(){r.querySelectorAll(".hl").forEach(function(e){e.classList.remove("hl")})}'
              'var wide=function(){return window.matchMedia("(min-width:960px)").matches};'
              'r.querySelectorAll("[data-k]").forEach(function(p){var ks=(p.dataset.k||"").split(" ").filter(Boolean).map(function(n){return "' + key + '-ks"+n});'
              'function lit(){clear();p.classList.add("hl");on(ks,"hl")}'
              'p.addEventListener("mouseenter",lit);p.addEventListener("focusin",lit);p.addEventListener("mouseleave",clear);'
              'var s=p.querySelector("summary");if(s)s.addEventListener("click",function(ev){if(!wide())return;ev.preventDefault();lit();'
              'var f=document.getElementById(ks[0]);if(f){var b=f.getBoundingClientRect();if(b.top<0||b.bottom>innerHeight)f.scrollIntoView({block:"center",behavior:"smooth"})}})});'
              'r.querySelectorAll(".ks[data-p]").forEach(function(k){var ps=(k.dataset.p||"").split(" ").filter(Boolean).map(function(i){return "' + key + '-"+i});'
              'if(!ps.length)return;k.addEventListener("mouseenter",function(){clear();k.classList.add("hl");on(ps,"hl")});k.addEventListener("mouseleave",clear)})})();</script>')
    return (f'<section class="lv" id="lv-{key}" data-arm="{esc(arm)}"><div class="lv-grid">{"".join(pc)}{"".join(ec)}</div>'
            + f'<p class="meta" style="margin-top:6px">{esc(pop["genre"])}. {esc(pop["entity"])} {esc(pop["status"])}</p>'
            + script + '</section>'), stats

def form_ledger(row, arms):
    """One table per row: AIO's transcript against every composed object of both arms, computed at build."""
    o = row["objects"]
    FC = set(row.get("field_claims", {})) | set(o.get("KO", {}).get("field_claims", {}))
    tw, tcl = o["T"]["words"], len(o["T"]["claims"])
    cols = [("AIO (T)", tw, None, f'{o["T"]["cards"]} documents', "none")]
    for label, st in arms:
        for lvl, name, rail, mod in (("P", "compression", f'{st["P"]["rail"]} lineages', "typography"), ("KO", "expansion", "per sentence", "grammar")):
            cols.append((f"{label} {name}", st[lvl]["words"], st[lvl]["claims"], rail, mod))
    rows_ = [("body words", [c[1] for c in cols]),
             ("distinct claims", [tcl] + [len(c[2]) for c in cols[1:]]),
             ("claims per 100 words", [f"{100 * tcl / tw:.1f}"] + [f"{100 * len(c[2]) / c[1]:.1f}" for c in cols[1:]]),
             ("field claims carried (of %d)" % len(FC), ["—"] + [len(c[2] & FC) for c in cols[1:]]),
             ("archive claims", ["0"] + [len(c[2] - FC) for c in cols[1:]]),
             ("rail", [c[3] for c in cols]), ("modality shown in", [c[4] for c in cols])]
    head = "".join(f"<th>{esc(c[0])}</th>" for c in cols)
    body = "".join(f"<tr><td>{esc(n)}</td>" + "".join(f"<td>{esc(str(v))}</td>" for v in vals) + "</tr>" for n, vals in rows_)
    return det("", "Form ledger — AIO against both arms, at both levels",
               f'<div class="tw"><table class="flg"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table></div>'
               '<p class="meta">Computed from the row at build: words counted in the text; claims from the ledger ids each line or sentence carries. '
               'T\'s claims are the worked example\'s T1–T9.</p>')

def arm_switch(key, arms):
    btns = "".join(f'<button type="button" data-t="lv-{esc(k)}"{" aria-pressed=" + chr(34) + "true" + chr(34) if i == 0 else ""}>{esc(lab)}</button>' for i, (k, lab) in enumerate(arms))
    js = ('<script>document.addEventListener("DOMContentLoaded",function(){var w=document.getElementById("arms-' + key + '");if(!w)return;var bs=w.querySelectorAll("button");'
          'function show(t){bs.forEach(function(b){var on=b.dataset.t===t;b.setAttribute("aria-pressed",on?"true":"false");'
          'var s=document.getElementById(b.dataset.t);if(s)s.hidden=!on})}'
          'bs.forEach(function(b){b.addEventListener("click",function(){show(b.dataset.t)})});show(bs[0].dataset.t)});</script>')
    return f'<div class="arms" id="arms-{key}" role="group" aria-label="Arm">{btns}</div>' + js

def knowledge_object(ko, row):
    """The knowledge object: the plan of L(B ∪ A) realized as encyclopedic prose with no provenance in it, and every sentence
    sourced below, claim by claim, from the frozen ledgers (the archive's from ledger-archive.json, the field's from the row).
    Each sentence is its own collapsible entry, so the provenance can be read one sentence at a time."""
    ledger = {c["id"]: c for c in json.loads((ROOT / row["ledger"]["archive"]).read_text(encoding="utf-8"))}
    reg = _sources()
    paras = {}
    for snt in ko["sentences"]:
        paras.setdefault(snt["para"], []).append(snt["text"])
    out = ['<div class="ko"><div class="ko-head">The knowledge object</div>',
           f'<h3 class="ko-title">{esc(ko["title"])}</h3>']
    out += [f"<p>{esc(' '.join(v))}</p>" for _, v in sorted(paras.items())]
    out.append('</div>')
    entries = []
    for snt in ko["sentences"]:
        cl = []
        for cid in snt["claims"]:
            if cid in ko["field_claims"]:
                f = ko["field_claims"][cid]
                cl.append(f'<li><code class="cid">{esc(cid)}</code> {esc(ko["field_sources"].get(f["source"], f["source"]))}, {esc(f["locus"])} '
                          f'<span class="pill dim">documented · field</span><br><span class="qt">{esc(unquote(f["quote"]))}</span></li>')
            else:
                c = ledger[cid]; d = reg[c["dep"]]
                cl.append(f'<li><code class="cid">{esc(cid)}</code> <a href="{dep_href(c["dep"])}">{esc(dep_label(c["dep"]))}</a> <em>{esc(d["title"][:120])}</em> '
                          f'<span class="meta">{esc(str(d.get("creator") or ""))} · {esc(str(c.get("date") or ""))} · {esc(c["locus"])}</span> '
                          f'<span class="pill">{esc(c["modality"])}</span><br><span class="qt">{esc(unquote(c["quote"]))}</span></li>')
        entries.append(det(f'{snt["n"]}.', f'<span class="prov-s">{esc(snt["text"])}</span>', f'<ul class="claims">{"".join(cl)}</ul>',
                           n=f'{len(snt["claims"])}'))
    used = {c for snt in ko["sentences"] for c in snt["claims"]}
    nf = sum(1 for c in used if c in ko["field_claims"])
    na = len(used) - nf
    out.append(det("", "Provenance — every sentence sourced", 
                   f'<p class="meta">{len(ko["sentences"])} sentences; {nf} field claims, {na} archive claims. Modality is the source\'s own; the prose carries it in its grammar. Open a sentence to read its sources.</p>'
                   f'<div class="stack">{"".join(entries)}</div>', n=f'{len(ko["sentences"])} sentences'))
    out.append(f'<p class="meta" style="margin-top:6px">{esc(ko["genre"])}. {esc(ko["status"])}.</p>')
    return "\n".join(out)


def folder_index(folder, title, note):
    """A listing with hashes for a data folder the spec links as a folder. Returns (path, html); main writes it."""
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
    return folder / "index.html", page(title + " — Alexanarch", note, body, canon)


# ── the per-entity surface (ruled 2026-10-07) ─────────────────────────────────────────────────────────
# "we will have to take some cues from the capture registry to ensure non entries are modular, navigable,
# machine-inspectable, and not unwieldy. this is to be a relatively comprehensive knowledge project, so were
# going to need to break apart file size." (Lee Sharks, 2026-10-07.) The one page (2.8 MB at 11 entities) is
# split as the Capture Registry was split on 2026-10-01 (scripts/build_capture_records.py): one page per entity
# at its own URL, its JSON beside it, a small table of contents, a sitemap. /non/ itself keeps only the cards.
#
#   non/index.html                 the table of contents as a page: status, method, legend, one card per entity,
#                                  the register summary, the panel, the procedure
#   non/index.json                 the table of contents as data: one row per entity, each entity.json's sha256
#   non/{entity}/index.html        the entity's page and its citation: the knowledge object first, its addresses
#                                  and transcripts and its archive bearing folded beneath
#   non/{entity}/entity.json       the entity as a compact machine record; points to the row, does not copy it
#   sitemap-non.xml                the entity pages
#
# Deterministic: same data, same bytes (the build date line is gone; the page states the register's date).
# Directories under non/ it no longer owns are removed only if they carry its marker.

MARK = "<!-- generated by scripts/build_non.py -->"
SITEMAP = ROOT / "sitemap-non.xml"
HF_NON = "https://huggingface.co/datasets/leesharks/negative-of-the-negative"
DS_URL = "/datasets/negative-of-the-negative/v2"
# The service that composes /non rows on commission, and the SPXI method /non is (0.16; gnosis is 0.17), ruled 2026-10-25:
# gnosis links to /non, and /non and every /non page to gnosis.
GNOSIS = "https://gnosis.spxi.dev/"
SERVICE_BLOCK = {"name": "SPXI-gnΩsis", "url": GNOSIS, "index": GNOSIS + "v1/quote",
                 "statement": ("SPXI-gnΩsis opens pinned Wikipedia revisions sentence by sentence against the sources they cite (EA-WIKI-OPEN-01 v1.1, #1697); "
                               "a commission consults the Crimson Hexagonal Archive by its own procedure and composes the entity's /non row, which lands here. "
                               "Quotes are free: POST https://gnosis.spxi.dev/v1/quote with {oldid, tier: \"commission\"} or {object: {name, …}}.")}
def gnosis_line(by_gnosis=None):
    """The service, on the index (None) and on every entry page: whether this row was composed by it, and what it does."""
    a = '<a href="https://gnosis.spxi.dev/">SPXI-gnΩsis</a> (gnosis.spxi.dev)'
    does = ("opens a Wikipedia revision sentence by sentence against the sources it cites; a commission consults the archive by "
            "its own procedure and composes the entity's row here")
    if by_gnosis is None:
        s = f"Rows are composed in session or on commission by {a}, which {does}. A quote is free."
    elif by_gnosis:
        s = f"This row was composed on commission by {a}, which {does}."
    else:
        s = f"This row was composed in session. {a} {does}; a quote to recompose this entity is free."
    return f'<p class="meta gnosis">{s}</p>'
CEIL, WARN = 4_000_000, 600_000
CREATOR = {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"}
LICENSE = "https://creativecommons.org/licenses/by/4.0/"
NON_DESC = ("Public knowledge composed three ways at one address, with the archive admitted on equal terms: per-entity "
            "knowledge objects in the archive's ontology, the public field carried whole, and the translation between them; "
            "working, not frozen (EA-NEGONT-02).")

def npage(title, desc, body, canonical, jsonld, head_extra="", tail=""):
    """A /non page: the capture record's head (canonical, cite-as, describedby, collection, citation meta, JSON-LD)."""
    return ('<!DOCTYPE html>\n<html lang="en"><head>\n' + MARK + '\n'
            '<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
            f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(desc)}">\n'
            f'<meta name="citation_author" content="Sharks, Lee">\n{head_extra}'
            f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n'
            f'<style>{CSS}</style>\n</head><body><div class="wrap">\n{nav()}\n{body}\n</div>\n{tail}'
            '<script src="https://www.themandalaoracle.com/embed/sigil.js" defer></script>\n</body></html>\n')

def jdump(o):
    return json.dumps(o, ensure_ascii=False, indent=1) + "\n"

def _date(s):
    m = re.search(r"\d{4}-\d{2}-\d{2}", str(s or ""))
    return m.group(0) if m else None

# a fragment target inside a closed <details>, or inside the arm not shown, is opened before it is scrolled to
OPEN_JS = ('<script>(function(){function o(){var h=location.hash.slice(1);if(!h)return;var e=document.getElementById(decodeURIComponent(h));'
           'if(!e)return;var s=e.closest("section.lv[hidden]");if(s){var b=document.querySelector(\'.arms button[data-t="\'+s.id+\'"]\');if(b)b.click()}'
           'for(var p=e.parentElement;p;p=p.parentElement){if(p.tagName==="DETAILS")p.open=true}e.scrollIntoView()}'
           'addEventListener("hashchange",o);addEventListener("DOMContentLoaded",o)})();</script>\n')

BY_TYPES = {"A": "type A — the archive coined the concept", "B": "type B — a rival occupant holds it",
            "C": "type C — a conventional reading holds it", "E": "type E — the archive, its author and heteronyms, its works, its mantles",
            "I": "type I — a function of the archive's infrastructure"}


def _entry_line(row):
    """The entry in one line: the first sentence of the compression's lede, as the reader meets it on the page."""
    t = (((row or {}).get("objects") or {}).get("P") or {}).get("lede", {}).get("text", "") if row else ""
    t = re.sub(r"\s+", " ", t).strip()
    m = re.match(r"(.{40,320}?[.;])\s", t + " ")
    return (m.group(1) if m else t[:320]).strip()


def _case_of(row):
    on = (row or {}).get("ontology") or {}
    c = str(on.get("composition") or "")
    if c.startswith("archive"):
        return "archive"
    return c or ("v0.7" if row and (row.get("objects") or {}).get("KO") else "none")


def by_index(toc, rows, groups, panel, reg):
    """/non/by/: the entries by type, by case and by month, and every address in the register, each row with its
    entity, its addresses (query, date, surface, signed), its case and its entry in one line — the grammar of
    /captures/by/. Built from the same files as the entity pages; it writes nothing back."""
    CASE_NAMES = dict(CASE_LABEL, **{"v0.7": "composed under v0.7 (#1665), awaiting recomposition", "none": "not yet composed"})
    slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    def rec(x):
        k = x["entity"]; r = rows.get(k)
        adr = "".join(f'<div class="q"><a href="/non/{esc(k)}/#reg-{esc(e["slug"])}">{esc(e["q"])}</a> '
                      f'<span class="m">{esc(", ".join(e["dates"]))} · {esc(e["surface"])} · {esc(e["auth"])} · archive {"present" if e["archive_present"] else "absent"}</span></div>'
                      for e in groups.get(k, []))
        case = _case_of(r); rho = ((r or {}).get("ontology") or {}).get("rho")
        rho = rho.get("value") if isinstance(rho, dict) else rho
        meta = f'{esc(type_label(x["type"]))} · {esc(CASE_NAMES.get(case, case))}' + (f' · ρ = {esc(str(rho))}' if rho else "") + f' · {esc(x.get("date") or "")}'
        line = _entry_line(r)
        return (f'<div class="rec"><a class="t" href="/non/{esc(k)}/">{esc(x["name"])}</a> <span class="m">{meta}</span>'
                + adr + (f'<div class="d">{md_inline(line)}</div>' if line else "") + '</div>')
    groups_by = {"type": {}, "case": {}, "month": {}}
    for x in toc:
        t = (re.match(r"\s*([ABCEI])", str(x["type"])) or [None, "?"])[1]
        groups_by["type"].setdefault(t, []).append(x)
        groups_by["case"].setdefault(_case_of(rows.get(x["entity"])), []).append(x)
        groups_by["month"].setdefault((x.get("date") or "undated")[:7], []).append(x)
    label = {"type": lambda g: BY_TYPES.get(g, f"type {g}"), "case": lambda g: CASE_NAMES.get(g, g), "month": lambda g: g}
    order = {"type": lambda g: g, "case": lambda g: ["equal", "mixed", "witness", "archive", "v0.7", "none"].index(g) if g in ("equal", "mixed", "witness", "archive", "v0.7", "none") else 9,
             "month": lambda g: g}
    BYCSS = ('<style>.rec{padding:9px 0;border-bottom:1px solid #eee;overflow-wrap:anywhere}.rec a.t{font-weight:500;text-decoration:none;font-size:.95em}'
             '.rec .m{font-family:var(--mono);font-size:.72em;color:var(--teal,#0a7c6a)}.rec .d{font-size:.84em;color:#444;margin-top:3px}'
             '.rec .q{font-size:.86em;margin-top:3px}.idx{font-size:.88em;line-height:1.9}.crumbs{font-size:.8em;color:#777;margin-bottom:8px}</style>\n')
    def bpage(path, title, desc, body, n):
        url = f"{BASE}/{path[:-10]}"
        jl = {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": url, "description": desc,
              "isPartOf": {"@type": "Dataset", "name": "The Negative of the Negative", "url": f"{BASE}/non/"}, "numberOfItems": n}
        return npage(title + " — Alexanarch", desc, body, url, jl, f'<link rel="canonical" href="{url}">\n' + BYCSS)
    out, idx = {}, []
    head = lambda title, n: (f'<p class="crumbs"><a href="/non/">/non</a> · <a href="/non/by/">by type, case and month</a></p><h1>{esc(title)}</h1>'
                             f'<p class="sub">{n} entr{"y" if n == 1 else "ies"} of The Negative of the Negative (EA-NEGONT-02 v0.9, <a href="/s/records/1690/">#1690</a>). '
                             'Each row: the entity (its page is its citation), its type, its case and ρ, the date composed; then each address at which it was observed, '
                             'with date, surface and sign-in; then the entry in one line. Working, not frozen.</p>')
    for dim in ("type", "case", "month"):
        links = []
        for g in sorted(groups_by[dim], key=order[dim]):
            xs = sorted(groups_by[dim][g], key=lambda x: (x.get("date") or "", x["name"]), reverse=(dim == "month"))
            path = f"non/by/{dim}/{slugify(g)}/index.html"
            title = f"/non by {dim}: {label[dim](g)}"
            out[path] = bpage(path, title, f"{len(xs)} entries of The Negative of the Negative, {label[dim](g)}.",
                              head(title, len(xs)) + "".join(rec(x) for x in xs), len(xs))
            links.append(f'<a href="/{path[:-10]}">{esc(label[dim](g))}</a> ({len(xs)})')
        idx.append(f'<h2>By {dim}</h2><p class="idx">' + " · ".join(links) + "</p>")
    allrows = "".join(rec(x) for x in sorted(toc, key=lambda x: x["name"].lower()))
    n_addr = sum(len(groups.get(x["entity"], [])) for x in toc)
    regrows = []
    for e in sorted(reg.get("entries", []), key=lambda e: (e["date"], e["q"]), reverse=True):
        k = e["entity"]
        dest = f'/non/{esc(k)}/#reg-{esc(e["slug"])}' if any(x["entity"] == k for x in toc) else "/non/#register"
        regrows.append(f'<div class="rec"><a class="t" href="{dest}">{esc(e["q"])}</a> <span class="m">{esc(", ".join(e["dates"]))} · {esc(e["surface"])} · '
                       f'{esc(e["auth"])} · archive {"present" if e["archive_present"] else "absent"}</span>'
                       f'<div class="d">entity: <a href="/non/{esc(k)}/">{esc(next((x["name"] for x in toc if x["entity"] == k), k))}</a></div></div>')
    out["non/by/index.html"] = bpage("non/by/index.html", "/non by type, case and month",
                                     f"{len(toc)} entries and {len(reg.get('entries', []))} addresses of The Negative of the Negative, indexed by type, case and month.",
                                     '<p class="crumbs"><a href="/non/">/non</a></p><h1>The Negative of the Negative, by type, case and month</h1>'
                                     f'<p class="sub">{len(toc)} entries, {n_addr} of the register\'s {len(reg.get("entries", []))} addresses under them. Smaller pages, each row with its entity, '
                                     'its addresses, its case and its entry in one line; the entity\'s own page is its citation. The register\'s addresses, newest first, are below.</p>'
                                     + "".join(idx) + '<h2>Every entry</h2>' + allrows
                                     + f'<h2 id="addresses">Every address in the register ({len(regrows)})</h2>' + "".join(regrows),
                                     len(toc))
    return out


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if any output is missing or stale")
    a = ap.parse_args()

    panel = json.loads((V2 / "panel/panel.json").read_text(encoding="utf-8"))
    rows = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((V2 / "rows").glob("*.json"))}
    trav = {}
    for d in sorted((V2 / "traversal").iterdir()):
        if (d / "summary.json").exists():
            trav[d.name] = {"summary": json.loads((d / "summary.json").read_text(encoding="utf-8")),
                            "reading": json.loads((d / "reading.json").read_text(encoding="utf-8")) if (d / "reading.json").exists() else None}
    REGH, ROWH, TRAVH, REGQ, STATS = {}, {}, {}, {}, {}
    AX, LANDS = load_axn(), load_landings()
    REG = _sources()

    LEDE = ('<p class="sub">Public knowledge of an entity, constructed before the addresses at which it is found, and composed three ways: as the composition layer gave it, as its own disclosed sources give it, and with the Crimson Hexagonal Archive admitted on equal terms. Each row is adjudicated later against what the world does.</p>')
    STATUS = ('<div class="status"><strong>Under construction, by design.</strong> The generation procedure (EA-NEGONT-02 v0.9, <a href="/s/records/1690/">#1690</a>, which supersedes <a href="/s/records/1671/">#1671</a>) is being tested, iterated and revised. Under v0.9 the archive\'s sources are admitted on equal terms, ontology included, where the archive extends the field\'s ontology, and the archive\'s ontology rules where it supplies one no other source makes available, by the law of the suppressed witness; each entry\'s case is read from its defining papers, and the entries composed under v0.7 are recomposed one at a time (ruled 2026-10-18), each page showing its v0.7 composition below the current one, labelled; SPXI and Theophrastus stand at v0.8, the cases v0.9\'s law of the suppressed witness calls for (ruled 2026-10-19); the panel (<a href="/non/panel/">/non/panel/</a>) is a working list and is frozen only after the procedure is (§7.0, ruled 2026-10-05). Nothing on /non is a frozen measurement.</div>')
    how = ('<div class="objs">'
             '<div class="obj"><b>T</b>the transcript: what the composition layer gave, verbatim, with its source cards</div>'
             '<div class="obj"><b>L(B)</b>the address recomposed from the full texts of the sources the layer itself surfaced</div>'
             '<div class="obj"><b>L(B ∪ A)</b>the same algorithm with the archive\'s subset admitted on equal terms</div>'
             '<div class="obj"><b>Δ</b>T against L(B): what the disclosed field held and was not composed. L(B) against L(B ∪ A): what admission adds</div>'
             '<div class="obj"><b>KO</b>the knowledge object: L(B ∪ A) written as public knowledge, with no provenance in the prose and every sentence sourced below it</div>'
             '<div class="obj"><b>K</b>the prospective kernel: what admission adds, derived from the plan, adjudicated later in both directions</div></div>'
             '<p>The archive\'s subset is selected by its <strong>bearing</strong> on the address, in three strata: <strong>D</strong>, direct (the archive names the entity and says something about it); <strong>R</strong>, relational (the archive relates the entity to one of its own objects); <strong>O</strong>, ontological (the archive applies one of its own categories to the entity, or to a class the field says it belongs to). A citation hop from what reading admits finds the term-absent tail. Volume never removes a source.</p>')
    HOW = det("", "How an entity reads", how, n="T · L(B) · L(B ∪ A) · Δ · KO · K")

    # the register: one card per address, captures grammar (2026-10-06)
    regp = V2 / "register.json"
    reg = json.loads(regp.read_text(encoding="utf-8")) if regp.exists() else {"entries": [], "version": None, "date": None}
    groups = {}
    for e in reg["entries"]:
        groups.setdefault(e["entity"], []).append(e)
    ents = {x["entity"]: x for x in panel["entities"]}
    if regp.exists():
        REGHEAD = (f'<p class="sub" id="register">The register — {len(groups)} entities, {reg["address_count"]} address{"" if reg["address_count"] == 1 else "es"}, '
                 f'{reg["observation_count"]} observation{"" if reg["observation_count"] == 1 else "s"} · v{esc(str(reg["version"]))}. '
                 f'{esc(reg["_what_this_is"])}</p>')
        order = [x["entity"] for x in panel["entities"] if x["entity"] in groups] + [k for k in groups if k not in ents]
        for ek in order:
            en = ents.get(ek, {"name": ek, "type": "not on the panel"})
            addrs = []
            for e in groups[ek]:
                pills = [f'<span class="pill dim">{esc(e["surface"])}</span>', f'<span class="pill dim">{esc(e["auth"])}</span>',
                         ('<span class="pill warn">archive present · also a capture</span>' if e["archive_present"] else '<span class="pill">archive absent</span>')]
                if e.get("cites") is not None:
                    pills.append(f'<span class="pill dim">{e["cites"]} source card{"" if e["cites"] == 1 else "s"}</span>')
                obs = [e] + e["observations"][1:] if e["observations"] else [e]
                inner = []
                for ob in obs:
                    tx = ob.get("transcript")
                    body = (f'<pre style="white-space:pre-wrap;overflow-wrap:anywhere;font-family:var(--mono);font-size:.8em;color:#333">{cite_links(tx)}</pre>' if tx
                            else f'<p>Held by the Capture Registry: <a href="/captures/{esc((ob.get("capture_ref") or {}).get("slug", ""))}/">{esc((ob.get("capture_ref") or {}).get("slug", ""))}</a></p>')
                    cl = "".join(f'<li>{esc(str(x.get("n")))}. {esc(str(x.get("site")))} — {esc(str(x.get("title")))}</li>' for x in (ob.get("cite_list") or []))
                    inner.append(det("", f'{esc(ob["date"])} · transcript', body + (f'<h3>Source cards</h3><ul>{cl}</ul>' if cl else "")
                                     + f'<p class="meta">{esc(ob["obs_id"])} · {esc(ob.get("transcript_class") or "")} · {esc(ob.get("transcript_read") or "")}'
                                     + (f' · sha256 {esc(ob["transcript_sha256"][:16])}…' if ob.get("transcript_sha256") else "") + '</p>'
                                     + f'<p class="meta">Surface: {esc(ob.get("surface_basis") or "")}</p>'
                                     + f'<p class="meta">Archive: {esc(ob.get("archive_basis") or "")}</p>', n=esc(ob["obs_id"])))
                href = address_href(ek, e["q"])
                qh = f'<a href="{href}">{esc(e["q"])}</a>' if href else esc(e["q"])
                addrs.append(f'<div id="reg-{esc(e["slug"])}" style="margin:12px 0 4px;padding-top:10px;border-top:1px solid var(--rule,#e5e5e5)">'
                             f'<p class="meta" style="margin:0 0 4px">at the address · {esc(", ".join(e["dates"]))}</p>'
                             f'<div class="card-query" style="font-size:1em">{qh}</div><div class="card-status">{"".join(pills)}</div>'
                             f'<div class="stack">{"".join(inner)}</div></div>')
            n_a = len(groups[ek])
            REGQ[ek] = n_a
            REGH[ek] = (f'<div class="card" id="ent-{esc(ek)}"><div class="card-head"><span class="card-section">entity · {esc(type_label(en["type"]))}</span>'
                     f'<span class="card-date">{n_a} address{"" if n_a == 1 else "es"}</span></div>'
                     f'<div class="card-query">{esc(en["name"])}</div>'
                     + "".join(addrs)
                     + f'<div class="card-links"><a href="{DS_URL}/register.json">register json</a>'
                     f'<a href="{DS_URL}/register.schema.json">schema</a><a href="/scripts/non_intake.py">intake</a>'
                     + (f'<a href="#row-{esc(ek)}">composed row</a>' if ek in rows else "") + '</div></div>')

    # rows with compositions: one card per row, captures grammar
    for key, r in rows.items():
        o = r["objects"]
        href = address_href(key, r["address"])
        q = f'<a href="{href}">{esc(r["address"])}</a>' if href else esc(r["address"])
        ko = o.get("KO")
        pills = ['<span class="pill warn">not frozen</span>', f'<span class="pill dim">{esc(type_label(r["type"]))}</span>',
                 f'<span class="pill dim">{esc(r["auth"])}</span>']
        if ko:
            pills.append(f'<span class="pill ok">knowledge object · {len(ko["sentences"])} sentences</span>')
        c = [f'<div class="card" id="row-{esc(key)}"><div class="card-head"><span class="card-section">{esc(r["surface"])}</span>'
             f'<span class="card-date">epoch {esc(r["epoch"])}</span></div>',
             f'<div class="card-query">{q}</div><div class="card-status">{"".join(pills)}</div>',
             f'<p class="meta" style="margin-bottom:12px">{md_inline(r["status"]["procedure"])}. Ledger: {md_inline(r["status"]["ledger"])}.</p>']
        if o.get("note") and not ko:
            c.append(f'<p class="meta" style="margin-bottom:8px"><span class="pill warn">not composed</span> {md_inline(o["note"])}</p>')
        if r.get("breaches"):
            c.append(det("", "breaches recorded", "<ul>" + "".join(f'<li><code>{esc(str(b.get("check", "")))}</code> {md_inline(str(b.get("detail", "")))}</li>' for b in r["breaches"]) + "</ul>",
                         n=f'{len(r["breaches"])}'))
        earlier = []
        if o.get("P") and ko:
            arms, stats = [], []
            onto = bool(r.get("ontology"))
            _cv = (r.get("ontology") or {}).get("composition")
            LA = ("Field and archive, equal terms — L(B ∪ A)" if _cv == "equal" else
                  "Field and archive, the archive ruling its senses — L(B ∪ A)" if _cv == "mixed" else
                  "The archive's ontology — L_A(B ∪ A)" if onto else "Field and archive (B ∪ A)")
            LF = "The field's ontology — L_F(B)" if onto else "Field alone (B)"
            html_a, st_a = two_levels(r, key, "P", "KO", LA)
            arms.append((key, LA)); stats.append(("L_A" if onto else "B ∪ A", st_a))
            STATS[key] = st_a
            html_b = ""
            if o.get("P_B") and o.get("KO_B"):
                html_b, st_b = two_levels(r, key + "-b", "P_B", "KO_B", LF)
                arms.append((key + "-b", LF)); stats.append(("L_F" if onto else "B", st_b))
            led = r["status"]["ledger"].lower()
            badge = ("working knowledge object · not frozen · ledger " + ("unaudited" if "unaudited" in led else "audited")).upper()
            c.append(f'<p class="kobadge" style="font-family:var(--mono);font-size:.72em;letter-spacing:.08em;color:#8a5a00;background:#fff4dc;'
                     f'border:1px solid #f0d9a6;border-radius:4px;padding:5px 9px;margin:10px 0 8px;display:inline-block">{esc(badge)}</p>')
            cur = re.match(r"EA-NEGONT-02 (v[0-9.]+), #(\d+)", r["spec"])
            c.append(f'<h3 class="inst-h" style="margin-top:14px">Current instantiation — composed under EA-NEGONT-02 {esc(cur.group(1))} '
                     f'(<a href="/s/records/{cur.group(2)}/">#{cur.group(2)}</a>)</h3>' if cur else "")
            c.append(arm_switch(key, arms) + html_a + html_b + form_ledger(r, list(reversed(stats))))
            # earlier instantiations, kept in the row (row.superseded), rendered below the current one, each labelled by its spec
            for ver, sv in sorted((r.get("superseded") or {}).items(), reverse=True):
                if not (sv.get("P") and sv.get("KO")):
                    continue
                sm = re.match(r"EA-NEGONT-02 (v[0-9.]+), #(\d+)", sv.get("spec", ""))
                vlab, vno = (sm.group(1), sm.group(2)) if sm else (ver, "")
                vk = key + "-" + re.sub(r"[^0-9a-z]", "", ver.lower())
                rv = {**r, "objects": {**o, "P": sv["P"], "KO": sv["KO"]}, "ontology": None}
                html_v, _ = two_levels(rv, vk, "P", "KO", f"Earlier instantiation · {vlab} — Field and archive (B ∪ A)")
                vref = f' (<a href="/s/records/{vno}/">#{vno}</a>)' if vno else ""
                earlier.append(f'<h3 class="inst-h" id="{esc(vk)}" style="margin-top:22px">Earlier instantiation — composed under EA-NEGONT-02 {esc(vlab)}{vref}</h3>'
                         f'<p class="meta">{esc(sv.get("note", ""))} Shown as composed; its spec, not the current one, governs it. '
                         f'Its field-only arm (L_F(B)) is unchanged and is the current one above.</p>'
                         + det("", f"The {vlab} composition — compression and expansion", html_v, n=f'{len(sv["KO"]["sentences"])} sentences')
                         + (det("L(B ∪ A)", f"the {vlab} long composition, with the archive on equal terms", md_block(sv["L_BA"]["text"]),
                                n=f'{sv["L_BA"]["words"]} words') if (sv.get("L_BA") or {}).get("text") else ""))
        elif ko:
            c.append(knowledge_object(ko, r))
        tclaims = "".join(f"<li>{md_inline(x)}</li>" for x in o["T"]["claims"])
        fld = "".join(f"<li><strong>{esc(f['id'])}</strong> {md_inline(f['card'])} <span class=\"meta\">{esc(f['fetched'])}</span></li>" for f in r["field"])
        rail = lineage_rail(r) if o.get("L_BA") else ""
        kent = "".join(det(esc(k.get("K", "")), md_inline(str(k.get("claim", ""))) + f' <span class="meta">{md_inline(str(k.get("source", "")))}</span>',
                           kv({kk: vv for kk, vv in k.items() if kk not in ("K",)}), n=esc(str(k.get("contrast", "")))) for k in (r.get("kernel") or []))
        c.append('<h3 style="margin-top:18px">The objects</h3><div class="stack">')
        tref = o["T"].get("register")
        tlink = (f'<a href="#reg-{esc(tref["slug"])}">register entry {esc(tref["slug"])}</a> <span class="meta">{esc(tref["obs_id"])}</span> · '
                 if tref else "")
        c.append(det("T", "the transcript", f'<p>{tlink}<a href="/{o["T"]["path"]}">file as first run</a> <span class="meta">sha256 {o["T"]["sha256"][:16]}…</span></p><ul>{tclaims}</ul>',
                     n=f'{o["T"]["words"]} words · {o["T"]["cards"]} cards'))
        c.append(det("B", "the disclosed field", f"<ul>{fld}</ul>", n=f'{len(r["field"])} sources'))
        onto = bool(r.get("ontology"))
        if onto:
            on = r["ontology"]
            c.append(det("E", "the two entities and their relation",
                         f'<p><strong>E_A</strong>, the archive\'s entity: {md_inline(on["E_A"]["definition"])} <span class="meta">{esc(" ".join(on["E_A"]["claims"]))}; '
                         f'defining papers {link_deps(", ".join("#%d" % n for n in on["E_A"]["defining_papers"]))}</span></p>'
                         f'<p><strong>E_F</strong>, the field\'s entity ({esc(type_label(on["E_F"]["type"]))}): {md_inline(on["E_F"]["definition"])}</p>'
                         f'<p><strong>ρ = {esc(on["rho"]["value"])}</strong>: {md_inline(on["rho"]["statement"])} <span class="meta">{esc(" ".join(on["rho"]["claims"]))}</span>. '
                         f'Guard: {md_inline(on["rho"]["guard"])}</p>'
                         + (f'<p><strong>The case: {esc(CASE_LABEL.get(on["case"]["value"], on["case"]["value"]))}</strong>. {md_inline(on["case"].get("statement", ""))}</p>'
                            + "".join(f'<p class="meta">#{L["dep"]} {esc(L.get("locus", ""))}: <span class="qt">{esc(L["quote"])}</span></p>' for L in on["case"].get("loci", []))
                            if on.get("case") else ""),
                         n=f'ρ = {esc(on["rho"]["value"])}' + (f' · {esc(on["case"]["value"])} case' if on.get("case") else "")))
            trs = "".join(f'<tr><td>{esc(", ".join(t_["field_claims"]))}</td><td>{md_inline(t_["received"])}</td><td>{md_inline(t_["receiving_text"]) if t_.get("receiving_text") else '<span class="meta">not located</span>'}</td>'
                          f'<td>{md_inline(t_["translation"])}</td><td>{esc(", ".join(t_["archive_claims"]))}</td></tr>' for t_ in on["translation"])
            nfc = len({x for t_ in on["translation"] for x in t_["field_claims"]})
            c.append(det("τ", "the translation: every field claim carried, beside its statement in the archive's ontology",
                         f'<div class="tw"><table class="flg"><thead><tr><th>field claims</th><th>received</th><th>receiving text</th><th>translation</th><th>archive</th></tr></thead>'
                         f'<tbody>{trs}</tbody></table></div><p class="meta">{md_inline(on["receiving_texts"])}. Reading the received column recovers the field (§5.9).</p>',
                         n=f'{nfc} field claims · {len(on["translation"])} rows'))
            ms = r.get("measure") or {}
            if ms:
                vk = "v0.9" if "v0.9" in ms else "v0.8"
                v7 = (f'; v0.7 {ms["v0.7"]["surviving"]} of {ms["v0.7"]["of"]} (positions {esc(str(ms["v0.7"]["positions"]))})' if ms.get("v0.7") else
                      f' (positions {esc(str(ms[vk]["positions"]))}; composed first under {vk}, so there is no v0.7 object to measure against)')
                orun = ms.get("opening_run")
                ob = (f' Opening-run check (§5.10): {"BREACH, recorded" if orun["breach"] else "no breach"}.' if orun else "")
                c.append(det("R7", "the measure", f'<p>{md_inline(ms["rule"])}: {vk} {ms[vk]["surviving"]} of {ms[vk]["of"]}{v7}.{ob}</p>',
                             n=f'{ms[vk]["surviving"]} of {ms[vk]["of"]} survive'))
            ng = r.get("negative")
            if ng:
                ex = ng["exhibit"]
                crs = "".join(f'<tr><td>{esc(x["id"])}</td><td><span class="qt">{esc(x["span"])}</span></td><td>{esc(x["type"])}</td>'
                              f'<td>{esc(", ".join(x["answered_by"]))}</td><td>{esc(", ".join("§%d" % n for n in x["KO_sentences"]))}</td>'
                              f'<td>{esc("; ".join(x["P_items"]))}</td><td>{esc(x["check"])}</td></tr>' for x in ng["corrections"])
                pe = r.get("procedure_experimental") or {}
                c.append(det("N", "the negative exhibit and its corrections <span class=\"meta\">the corrective exhibit, v0.9 §4.11</span>",
                             f'<p><a href="{esc(ex["record"])}">{esc(ex["address"])}</a> · {esc(ex["surface"])} · {esc(ex["date"])} · {esc(ex["auth"])}. {md_inline(ex["role"])}</p>'
                             f'<div class="tw"><table class="flg"><thead><tr><th></th><th>N, verbatim</th><th>move</th><th>answered by</th><th>KO</th><th>compression</th><th>check</th></tr></thead>'
                             f'<tbody>{crs}</tbody></table></div><p class="meta">{md_inline(ng["check"]["rule"])}: {ng["check"]["answered"]} of {ng["check"]["of"]} answered.</p>'
                             + (f'<p class="meta"><strong>The procedure, as metadata of this worked example.</strong> {esc(pe.get("status", ""))}</p><ul>'
                                + "".join(f"<li>{md_inline(x)}</li>" for x in pe.get("steps", [])) + '</ul>' if pe else ""),
                             n=f'{ng["check"]["answered"]} of {ng["check"]["of"]} answered'))
        if o.get("L_B"):
            c.append(det("L_F(B)" if onto else "L(B)", "recomposed from the disclosed field" + (", in the field's ontology" if onto else ""),
                         md_block(o["L_B"]["text"]), n=f'{o["L_B"]["words"]} words'))
        if o.get("L_BA"):
            c.append(det("L_A(B ∪ A)" if onto else "L(B ∪ A)",
                         "the field and the archive composed in the archive's ontology" if onto else "with the archive on equal terms",
                         md_block(o["L_BA"]["text"]) + rail, n=f'{o["L_BA"]["words"]} words'))
        tl = "L_F(B)" if onto else "L(B)"
        tk = "AIO's ontology at work on its own cards" if onto else "representational"
        dl = r.get("delta") or {}
        if dl:
            c.append(det("Δ", "the delta", (f'<p><strong>T against {tl}</strong> ({tk}): {md_inline(str(dl["T_vs_LB"]))}</p>' if dl.get("T_vs_LB") else "")
                         + (f'<p class="meta">{md_inline(str(dl["T_vs_LB_reading"]))}</p>' if dl.get("T_vs_LB_reading") else "")
                         + (f'<p><strong>{"L_F(B) against L_A(B ∪ A)" if onto else "L(B) against L(B ∪ A)"}</strong> (the intervention): {md_inline(str(dl["LB_vs_LBA"]))}</p>' if dl.get("LB_vs_LBA") else "")
                         + "".join(f'<p><strong>{esc(str(kk))}</strong>: {md_inline(str(vv))}</p>' for kk, vv in dl.items() if kk not in ("T_vs_LB", "T_vs_LB_reading", "LB_vs_LBA"))))
        if r.get("kernel"):
            c.append(det("K", "the prospective kernel <span class=\"meta\">sealed only at freeze</span>", f'<div class="stack">{kent}</div>', n=f'{len(r["kernel"])} entries'))
        c.append(CJ.non_block(key))  # the capture join: observations read as concerning this entity (2026-10-14)
        c.append('</div>')
        c.extend(earlier)  # earlier instantiations, below the whole of the current one
        c.append(f'<div class="card-links"><a href="{DS_URL}/rows/{key}.json">row json</a>'
                 f'<a href="/{r["ledger"]["archive"]}">archive ledger</a><a href="/{r["ledger"]["selection"]}">selection readings</a>'
                 + (f'<a href="/{r["ledger"]["field"]}">field ledger</a>' if r["ledger"].get("field") else "")
                 + (f'<a href="/{r["ledger"]["audit"]}">extraction audit</a>' if r["ledger"].get("audit") else '<span class="meta">extraction unaudited</span>')
                 + (f'<a href="{DS_URL}/traversal/{key}/">D/R/O traversal</a>' if key in trav else "")
                 + (f'<a href="{href}">address page</a>' if href else "") + '</div></div>')
        ROWH[key] = "".join(c)

    # traversals: one card each
    for key, t in trav.items():
        cn = t["summary"]["counts"]
        rd = t["reading"]
        addr = t["summary"]["address"]
        href = address_href(key, addr)
        pills = [f'<span class="pill">D {cn["D_deposits"]} deposits · {cn["D_sentences"]} sentences</span>',
                 f'<span class="pill">R {cn["R_deposits"]} · {cn["R_sentences"]}</span>',
                 f'<span class="pill">O {cn["O_deposits"]} · {cn["O_direct"]} direct, {cn["O_class"]} class</span>',
                 f'<span class="pill dim">hop {cn.get("H_candidates") or "—"}</span>',
                 (f'<span class="pill ok">read: {len(rd["verdicts"])} admitted, {len(rd["not_admitted"])} not</span>' if rd else '<span class="pill warn">unread</span>')]
        c = [f'<div class="card" id="trav-{esc(key)}"><div class="card-head"><span class="card-section">traversal</span>'
             + (f'<span class="card-date">{esc(rd["pass"])}</span>' if rd else "") + '</div>'
             f'<div class="card-query">{f"<a href={chr(34)}{href}{chr(34)}>{esc(addr)}</a>" if href else esc(addr)}</div><div class="card-status">{"".join(pills)}</div>']
        if rd and rd.get("lineages"):
            lin = "".join(det("", esc(l["lineage"]), f'<p>{link_deps(", ".join(f"#{n}" for n in l["instances"]))}</p>',
                              n=f'{len(l["instances"])}' + (f' · from #{l["earliest"]}' if l.get("earliest") else '')) for l in rd["lineages"])
            c.append(det("", "admitted, by lineage", f'<div class="stack">{lin}</div>' + "".join(f"<p>{md_inline(x)}</p>" for x in rd.get("observations", [])),
                         n=f'{len(rd["lineages"])} lineages'))
        c.append(f'<div class="card-links"><a href="{DS_URL}/traversal/{key}/">candidate files</a>'
                 f'<a href="{DS_URL}/panel/configs/{key}.json">configuration</a>'
                 + (f'<a href="{href}">address page</a>' if href else "") + '</div></div>')
        TRAVH[key] = "".join(c)

    # ── one page per entity, entity first (ruled 2026-10-07) ──
    files = {}
    names = ents
    keys = [x["entity"] for x in panel["entities"] if x["entity"] in ROWH or x["entity"] in REGH or x["entity"] in TRAVH]
    keys.sort(key=lambda k: (k not in ROWH, k not in REGH))
    toc, idxrows, sm, mentions_all = [], [], [], set()
    for k in keys:
        en = names[k]
        r = rows.get(k)
        t = trav.get(k)
        rd = t["reading"] if t else None
        url = f"{BASE}/non/{k}/"
        regs = groups.get(k, [])
        # addresses: the panel's, each with what the register seated at it; a seated address the panel does not list is kept
        addr_rows = []
        for ad in en["addresses"]:
            addr_rows.append({"address": ad["address"], "address_url": None, "register": []})
        for e in regs:
            hit = next((x for x in addr_rows if x["address"].lower() == e["q"].lower()), None)
            if hit is None:
                hit = {"address": e["q"], "address_url": None, "register": []}; addr_rows.append(hit)
            hit["register"].append({"slug": e["slug"], "obs_id": e["obs_id"], "surface": e["surface"], "auth": e["auth"],
                                    "dates": e["dates"], "archive_present": e["archive_present"],
                                    "transcript_sha256": e.get("transcript_sha256"), "url": f"{url}#reg-{e['slug']}"})
        for x in addr_rows:
            h = address_href(k, x["address"])
            x["address_url"] = f"{BASE}{h}" if h else None
        addr_url = next((x["address_url"] for x in addr_rows if x["address_url"]), None)
        dates = [d for d in ([r["epoch"]] if r else []) + [d for e in regs for d in e["dates"]] if _date(d)]
        if not dates and rd:
            dates = [_date(rd.get("pass"))] if _date(rd.get("pass")) else []
        last = max(dates) if dates else reg.get("date")
        st = STATS.get(k)
        ko = (r or {}).get("objects", {}).get("KO") if r else None
        FCk = set((r or {}).get("field_claims", {})) | set((ko or {}).get("field_claims", {}))
        counts = {"ko_sentences": len(ko["sentences"]) if ko else 0,
                  "p_words": st["P"]["words"] if st else 0,
                  # the ledgers' totals, and how many of each the knowledge object (B ∪ A) cites
                  "field_claims": len(FCk),
                  "archive_claims": len(json.loads((ROOT / r["ledger"]["archive"]).read_text(encoding="utf-8"))) if r else 0,
                  "ko_field_claims_cited": len(st["KO"]["claims"] & FCk) if st else 0,
                  "ko_archive_claims_cited": len(st["KO"]["claims"] - FCk) if st else 0,
                  "admitted_deposits": len(rd["verdicts"]) if rd else None,
                  "register_addresses": len(regs),
                  "traversal": t["summary"]["counts"] if t else None}
        links = {"record": url, "table_of_contents": f"{BASE}/non/index.json", "register": f"{BASE}{DS_URL}/register.json"}
        if r:
            links.update({"row": f"{BASE}{DS_URL}/rows/{k}.json", "archive_ledger": f"{BASE}/{r['ledger']['archive']}",
                          "field_ledger": f"{BASE}/{r['ledger']['field']}" if r["ledger"].get("field") else None,
                          "selection": f"{BASE}/{r['ledger']['selection']}" if r["ledger"].get("selection") else None,
                          "audit": f"{BASE}/{r['ledger']['audit']}" if r["ledger"].get("audit") else None})
        if t:
            links.update({"traversal": f"{BASE}{DS_URL}/traversal/{k}/", "traversal_summary": f"{BASE}{DS_URL}/traversal/{k}/summary.json",
                          "reading": f"{BASE}{DS_URL}/traversal/{k}/reading.json" if rd else None})
        if (V2 / "panel/configs" / f"{k}.json").exists():
            links["configuration"] = f"{BASE}{DS_URL}/panel/configs/{k}.json"
        links["address_page"] = addr_url
        links["dataset"] = HF_NON
        links = {kk: vv for kk, vv in links.items() if vv}
        ax = AX.get(k)
        comp = composition_of(r, LANDS.get(k))
        hist = earlier_rows(k)
        rec = {"entity": k, "name": en["name"],
               "axn": ({"axn": ax["axn"], "root": ax["root"], "hex": ax["hex"], "family": "NON", "row_sha256": ax["sha256"],
                        "minted": ax["minted"], "resolver": f"{BASE}/s/axn/{ax['hex']}/",
                        "earlier_versions": ax.get("history") or []} if ax else None),
               "type": en["type"], "type_code": type_code(en["type"]), "type_label": type_label(en["type"]),
               "case": _case_of(r), "composition": comp}
        if hist:
            rec["earlier_rows"] = hist
        rec["reading"] = READING_NOTE
        rec["service"] = SERVICE_BLOCK
        rec["spxi_instrument"] = _spxi_record(url)
        rec["citation"] = citation_of(en["name"], url, ax["axn"] if ax else None, last)
        rec["research"] = research_links(en["name"])
        rec["entry"] = entry_of(r, REG) if r else {"composed": False, "note": "no row: the entity has addresses or a traversal, and no composition"}
        if en.get("type_basis"):
            rec["type_basis"] = en["type_basis"]
        rec.update({"source": en.get("source"), "stage": en.get("stage"), "date": last,
                    "status": (r["status"] if r else {"procedure": None, "ledger": None, "frozen": False,
                               "note": "no knowledge object composed yet"}),
                    "addresses": addr_rows, "counts": counts, "links": links,
                    "row_sha256": hashlib.sha256((V2 / "rows" / f"{k}.json").read_bytes()).hexdigest() if r else None,
                    "record_url": url, "json_url": url + "entity.json",
                    "spec": f"{BASE}/s/records/{spec_no(en, r)}/", "creator": "Lee Sharks", "orcid": "0009-0000-1599-0703", "license": "CC BY 4.0"})
        ej = jdump(rec)
        files[f"non/{k}/entity.json"] = ej

        # the page
        sub = [f'<a href="/non/">the table of contents</a>', '<a href="entity.json">this entity as data</a>',
               '<a href="/non/index.json">contents as data</a>', f'<a href="{HF_NON}">the dataset on the Hub</a>']
        if r:
            sub.append(f'<a href="{DS_URL}/rows/{k}.json">row json</a>')
            if r["ledger"].get("field"):
                sub.append(f'<a href="/{r["ledger"]["field"]}">field ledger</a>')
            sub.append(f'<a href="/{r["ledger"]["archive"]}">archive ledger</a>')
        if t:
            sub.append(f'<a href="{DS_URL}/traversal/{k}/">D/R/O traversal</a>')
        if addr_url:
            sub.append(f'<a href="{esc(addr_url[len(BASE):])}">the address page</a>')
        sec = [f'<p style="font-size:.85em;margin:0 0 4px"><a href="/non/">The Negative of the Negative</a> › entity <code>{esc(k)}</code></p>',
               f'<p class="sub" style="font-size:.85em">One entity of the Negative of the Negative (EA-NEGONT-02, <a href="/s/records/{spec_no(en, r)}/">#{spec_no(en, r)}</a>), '
               f'cited at <code>{url}</code>. ' + " · ".join(sub) + '.</p>'
               f'<p class="meta" data-for="machines">{esc(READING_NOTE)}</p>',
               f'<section id="e-{esc(k)}"><h1>{esc(en["name"])}</h1>'
               f'<p class="meta">{esc(onto_line(en))} · sought at {" · ".join("<code>" + esc(x["address"]) + "</code>" for x in addr_rows)}</p>'
               f'<p class="meta">{md_inline(en.get("stage") or "")}</p>']
        if ax:
            sec.append(f'<p class="meta">AXN <a href="/s/axn/{esc(ax["hex"])}/"><code>{esc(ax["axn"])}</code></a> · root <code>{esc(ax["root"])}</code>'
                       + (f' · {len(ax["history"])} earlier version{"" if len(ax["history"]) == 1 else "s"}' if ax.get("history") else "") + '</p>')
        if comp:
            sec.append(f'<p class="meta">{composition_line(comp)}</p>')
        sec.append(action_row(en["name"], url, ax["axn"] if ax else None, last))
        sec.append(gnosis_line(bool(comp and comp.get("composer_class") == "gnosis")))
        sec.append(ROWH[k] if k in ROWH else '<p class="meta" style="margin-top:12px">No knowledge object composed yet.</p>')
        if hist:
            hl = "".join(f'<li>until {esc(h["replaced"])} · epoch {esc(str(h["epoch"]))} · {composition_line(h["composition"])} · '
                         f'<a href="{esc(h["row"][len(BASE):])}">row</a> · <a href="{esc(h["folder"][len(BASE):])}">its files</a> '
                         f'<span class="meta">sha256 {esc(h["sha256"][:16])}…</span></li>' for h in hist)
            sec.append(det("", "Earlier rows of this entity", f'<p class="meta">Rows a landing replaced, kept as they stood.</p><ul>{hl}</ul>', n=f'{len(hist)}'))
        if k in REGH:
            sec.append(det("", "Addresses and transcripts", REGH[k], n=f'{REGQ[k]} address{"" if REGQ[k] == 1 else "es"}', open_=k not in ROWH))
        if k in TRAVH:
            note = ""
            if k in REGH and k not in ROWH:
                note = ('<p class="meta" style="margin-top:6px"><strong>Since ' + esc(min(e["date"] for e in regs)) + '</strong> the entity has a seated transcript, at '
                        + ", ".join(f'<a href="#reg-{esc(e["slug"])}"><code>{esc(e["q"])}</code></a> ({esc(e["surface"])})' for e in regs)
                        + ': its disclosed field B exists, and T against L(B) can now be built. The reading below is dated to its pass.</p>')
            sec.append(det("", "Archive bearing — D/R/O traversal", '<p class="sub">Candidates are found by string; admission is by reading.</p>' + note + TRAVH[k],
                           n="read" if '>read:' in TRAVH[k] else "unread", open_=k not in ROWH and k not in REGH))
        sec.append('</section>')
        sec.append(f'<p class="foot">Lee Sharks · Crimson Hexagonal Archive · register v{esc(str(reg.get("version")))}, {esc(str(reg.get("date")))}. '
                   'Built by <a href="/scripts/build_non.py">scripts/build_non.py</a> from the files linked above; it writes nothing back. '
                   'Working, not frozen.</p>')
        body = "".join(sec)
        deps = sorted({int(n) for n in re.findall(r'href="/s/records/(\d+)/"', body)})
        mentions_all.update(deps)
        lede = ""
        P = (r or {}).get("objects", {}).get("P") if r else None
        if P:
            lede = f'{P["title"]} {P["lede"]["text"]}'
        desc = lede or f'{en["name"]}: {type_label(en["type"])}. {en.get("stage") or ""}'
        ld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": f'{en["name"]} — The Negative of the Negative',
              "url": url, "identifier": ([f"non:{k}", {"@type": "PropertyValue", "propertyID": "AXN", "value": ax["axn"], "url": f"{BASE}/s/axn/{ax['hex']}/"}] if ax else f"non:{k}"), "dateModified": last, "description": desc[:600], "creator": CREATOR, "license": LICENSE,
              "creativeWorkStatus": "working; not frozen", "isBasedOn": f"{BASE}/s/records/{spec_no(en, r)}/",
              "isPartOf": {"@type": "Dataset", "name": "The Negative of the Negative (EA-NEGONT-02)", "url": f"{BASE}/non/", "version": reg.get("version"),
                           "description": NON_DESC, "creator": CREATOR, "license": LICENSE},
              "encoding": {"@type": "MediaObject", "encodingFormat": "application/json", "contentUrl": url + "entity.json",
                           "description": "the entry itself: its knowledge object, every sentence with its claims, each claim's quote, source and locus"},
              "usageInfo": READING_NOTE}
        if deps:
            ld["mentions"] = [{"@type": "CreativeWork", "url": f"{BASE}/s/records/{n}/", "identifier": f"#{n}"} for n in deps]
        head = (f'<link rel="canonical" href="{url}">\n<link rel="cite-as" href="{url}">\n'
                f'<link rel="describedby" href="{url}entity.json" type="application/json">\n<link rel="collection" href="{BASE}/non/">\n'
                f'<meta name="citation_title" content="{esc(en["name"])} — The Negative of the Negative"><meta name="citation_date" content="{esc(str(last))}">'
                f'<meta name="citation_public_url" content="{url}">\n')
        files[f"non/{k}/index.html"] = npage(f'{en["name"]} — The Negative of the Negative — Alexanarch', desc[:300], body, url, ld, head + ACT_CSS, OPEN_JS + COPY_JS)

        toc.append({"entity": k, "name": en["name"], "axn": ax["axn"] if ax else None, "type": en["type"], "type_code": type_code(en["type"]),
                    "case": _case_of(r), "composer_class": (comp or {}).get("composer_class"), "stage": en.get("stage"),
                    "addresses": [x["address"] for x in addr_rows], "has_ko": bool(ko), "ko_sentences": counts["ko_sentences"],
                    "p_words": counts["p_words"], "n_register": len(regs), "traversal_counts": counts["traversal"],
                    "date": last, "record_url": url, "json_url": url + "entity.json", "address_url": addr_url,
                    "sha256": hashlib.sha256(ej.encode()).hexdigest()})
        # 2026-10-15: the page date — a confirmed join ("Observations of this entity") changes the page
        sm.append(f"  <url><loc>{url}</loc><lastmod>{CJ.page_date(last, CJ.non_date(k))}</lastmod></url>")

        # the entry's row on /non/ (2026-10-24: one compact row per entity, alphabetical, searchable)
        idxrows.append({"k": k, "name": en["name"], "ax": ax, "type": en["type"], "code": type_code(en["type"]), "case": _case_of(r),
                        "comp": (comp or {}).get("composer_class") or "none", "composer": (comp or {}).get("composer"), "date": str(last or ""),
                        "n": counts["ko_sentences"], "addrs": [x["address"] for x in addr_rows], "line": _entry_line(r) if r else "",
                        "title": ((((r or {}).get("objects") or {}).get("P") or {}).get("title") or ""),
                        "composed": bool(ko)})

    # ── the index (2026-10-24: one status line; one compact row per entity, alphabetical, searchable; the status
    #    and procedure, the register and the panel each on a page of their own) ──
    built_on = f'register v{esc(str(reg.get("version")))}, {esc(str(reg.get("date")))}'
    CASE_SHORT = {"equal": "equal terms", "mixed": "mixed", "witness": "suppressed witness", "archive": "archive's ontology (v0.8)",
                  "v0.7": "v0.7, awaiting recomposition", "none": "not composed"}
    COMP_SHORT = {"session": "session", "gnosis": "SPXI-gnΩsis", "none": "not composed"}
    sortkey = lambda s: re.sub(r"^[\W_]+", "", re.sub(r"^(the|a|an)\s+", "", s.lower().strip())).strip()
    idxrows.sort(key=lambda x: (sortkey(x["name"]), x["k"]))
    def facet(rows_, key, label, names):
        vals = sorted({x[key] for x in rows_}, key=lambda v: (v == "none", v))
        return (f'<label class="fl"><span>{label}</span><select data-f="{key}"><option value="">all</option>'
                + "".join(f'<option value="{esc(v)}">{esc(names.get(v, v))} ({sum(1 for x in rows_ if x[key] == v)})</option>' for v in vals)
                + '</select></label>')
    er = []
    for x in idxrows:
        ax = x["ax"]
        s = " ".join([x["name"], x["k"], *(x["addrs"]), ax["axn"] if ax else "", ax["root"] if ax else "", x["type"], x["line"]]).lower()
        line = x["line"] if len(x["line"]) <= 200 else x["line"][:200].rsplit(" ", 1)[0] + "…"
        er.append(f'<li class="er" id="c-{esc(x["k"])}" data-s="{esc(s)}" data-code="{esc(x["code"])}" data-case="{esc(x["case"])}" '
                  f'data-comp="{esc(x["comp"])}" data-date="{esc(x["date"])}" data-name="{esc(sortkey(x["name"]))}">'
                  f'<div class="er-h"><a class="er-n" href="/non/{esc(x["k"])}/">{esc(x["name"])}</a>'
                  + (f'<a class="er-x" href="/s/axn/{esc(ax["hex"])}/" title="{esc(ax["axn"])}">{esc(ax["axn"])}</a>' if ax else '<span class="er-x">no row, no AXN</span>')
                  + '</div><div class="er-m">'
                  f'<span title="{esc(x["type"])}">type {esc(x["code"])}</span><span>{esc(CASE_SHORT.get(x["case"], x["case"]))}</span>'
                  + (f'<span>{esc(COMP_SHORT.get(x["comp"], x["comp"]))}</span>' if x["comp"] != "none" else "") + f'<span>{esc(x["date"])}</span>'
                  + (f'<span>{x["n"]} sentences</span>' if x["n"] else "")
                  + '</div>' + (f'<p class="er-d">' + (f'<b>{esc(x["title"])}</b> ' if x["title"] else "") + f'{md_inline(line)}</p>' if line else "")
                  + f'<p class="er-a">sought at {" · ".join("<code>" + esc(a_) + "</code>" for a_ in x["addrs"])}</p></li>')
    SEARCH_JS = ('<script>(function(){var q=document.getElementById("nq"),L=document.getElementById("nl"),C=document.getElementById("nc"),'
                 'S=document.querySelectorAll("select[data-f]"),O=document.getElementById("ns"),E=[].slice.call(L.children);'
                 'function run(){var t=(q.value||"").toLowerCase().trim().split(/\\s+/).filter(Boolean),f={},n=0;'
                 'S.forEach(function(s){if(s.value)f[s.dataset.f]=s.value});'
                 'E.forEach(function(e){var ok=t.every(function(w){return e.dataset.s.indexOf(w)>=0});'
                 'for(var k in f){if(e.dataset[k]!==f[k])ok=false}e.hidden=!ok;if(ok)n++});'
                 'C.textContent=n+" of "+E.length;}'
                 'function sort(){var by=O.value;E.sort(function(a,b){return by==="date"?(b.dataset.date.localeCompare(a.dataset.date)||a.dataset.name.localeCompare(b.dataset.name)):a.dataset.name.localeCompare(b.dataset.name)});'
                 'E.forEach(function(e){L.appendChild(e)})}'
                 'try{var u=new URLSearchParams(location.search);if(u.get("q"))q.value=u.get("q");S.forEach(function(s){var v=u.get(s.dataset.f==="code"?"type":s.dataset.f);if(v)s.value=v})}catch(e){}'
                 'q.addEventListener("input",run);S.forEach(function(s){s.addEventListener("change",run)});O.addEventListener("change",function(){sort();run()});run();'
                 '})();</script>\n')
    ICSS = ('<style>.statusline{font-size:.86em;color:#78350f;background:#fef3c7;border-left:4px solid #d97706;border-radius:6px;padding:7px 12px;margin:10px 0 14px}'
            '.statusline a{color:#78350f}.dl{font-size:.84em;color:var(--dim);margin:0 0 14px}'
            '.find{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:flex-end;margin:6px 0 10px}'
            '.find input{flex:1 1 220px;min-width:0;font:inherit;font-size:.95em;padding:8px 10px;border:1px solid var(--border);border-radius:6px;background:var(--surface)}'
            '.fl{display:flex;flex-direction:column;font-family:var(--mono);font-size:.7em;color:var(--dim);gap:2px}'
            '.fl select{font:inherit;font-size:1.1em;padding:5px 6px;border:1px solid var(--border);border-radius:6px;background:var(--surface);color:var(--fg);max-width:44vw}'
            '#nc{font-family:var(--mono);font-size:.74em;color:var(--dim);margin-left:auto}'
            'ul.erl{list-style:none;margin:0}.er{padding:10px 0;border-bottom:1px solid var(--border)}.er[hidden]{display:none}'
            '.er-h{display:flex;flex-wrap:wrap;gap:2px 12px;align-items:baseline}.er-n{font-weight:600;border:0;font-size:1.02em}'
            '.er-x{font-family:var(--mono);font-size:.74em;color:var(--teal);border:0;overflow-wrap:anywhere}'
            '.er-m{display:flex;flex-wrap:wrap;gap:2px 10px;font-family:var(--mono);font-size:.72em;color:var(--dim);margin-top:2px}'
            '.er-d{font-size:.86em;color:#444;margin:4px 0 0}.er-a{font-size:.78em;color:var(--dim);margin:2px 0 0}</style>\n')
    b = ['<h1>The Negative of the Negative</h1>', LEDE,
         '<p class="statusline"><strong>Working, not frozen.</strong> Composed under EA-NEGONT-02 v0.9 (<a href="/s/records/1690/">#1690</a>), '
         'which is being tested, iterated and revised. <a href="/non/about/">Status, method and procedure</a>.</p>',
         gnosis_line(),
         f'<p class="dl">{len(idxrows)} entries, {sum(1 for x in idxrows if x["ax"])} with an AXN (family NON). '
         'As data: <a href="/non/index.json">index.json</a> (one row per entry) · <a href="/non/claims.json">claims.json</a> (every field claim quoted, by row) · '
         f'each entry\'s <code>/non/{{entity}}/entity.json</code> · <a href="{HF_NON}">the dataset on the Hub</a>. '
         'Also: <a href="/non/by/">by type, case and month</a> · <a href="/non/register/">the register</a> (every address and transcript) · '
         '<a href="/non/panel/">the panel</a> (the working list).</p>',
         '<p class="meta" data-for="machines">A reader of this page finds each entry\'s page, its citation, at /non/{entity}/, and the entry itself '
         '(its knowledge object, every sentence with the claims it cites, each claim\'s quote, source and locus) at /non/{entity}/entity.json; '
         '/non/index.json lists every entry with both addresses and its AXN.</p>',
         '<div class="find" role="search"><input id="nq" type="search" placeholder="Search names, addresses, AXNs" aria-label="Search the entries">'
         + facet(idxrows, "code", "type", {k_: f"{k_}" for k_ in TYPE_KEY})
         + facet(idxrows, "case", "case", CASE_SHORT) + facet(idxrows, "comp", "composed by", COMP_SHORT)
         + '<label class="fl"><span>order</span><select id="ns"><option value="name">A–Z</option><option value="date">newest</option></select></label>'
         + '<span id="nc" aria-live="polite"></span></div>',
         f'<ul class="erl" id="nl">{"".join(er)}</ul>',
         f'<p class="foot">Lee Sharks · Crimson Hexagonal Archive · {built_on}. The surface is single: /non is not mirrored. '
         'Built by <a href="/scripts/build_non.py">scripts/build_non.py</a>; it writes nothing back.</p>']

    # the status, method and procedure
    LEGEND = ('<dl class="legend" style="font-size:.88em;margin:8px 0 12px"><dt style="font-weight:600">Entity types (spec §1.2)</dt>'
              '<dd><b>A</b> the archive coined the concept; the default at it is empty</dd>'
              '<dd><b>B</b> a rival occupant holds it</dd>'
              '<dd><b>C</b> a conventional reading holds it; a public entity (a work, a person, a concept of general knowledge) on which the archive bears</dd>'
              '<dd><b>I</b> a function of the archive\'s infrastructure</dd>'
              '<dd><b>E</b> the entity: the archive, its author and heteronyms, its works, its mantles</dd>'
              '<dd><b>Op</b> an operator: the operation an entity form conceals, composed as its own object (SPXI-gnΩsis)</dd></dl>'
              '<p class="meta">Each entry\'s type is kept as the panel states it; the code is read from its front.</p>')
    PROC = ('<h2 id="procedure">Procedure and data</h2><ul>'
            '<li>Specification: <a href="/s/records/1690/">#1690</a> (EA-NEGONT-02 v0.9, 2026-10-18), superseding <a href="/s/records/1671/">#1671</a> (v0.8, 2026-10-08), <a href="/s/records/1665/">#1665</a> (v0.7, 2026-10-05) and <a href="/s/records/1664/">#1664</a> (v0.6, 2026-10-04)</li>'
            f'<li>Traversal tool: <a href="/scripts/non_traverse.py">scripts/non_traverse.py</a> · configurations: <a href="{DS_URL}/panel/configs/">v2/panel/configs/</a></li>'
            f'<li>Panel: <a href="{DS_URL}/panel/panel.json">panel.json</a> · v1 rows: <a href="/datasets/negative-of-the-negative/rows.json">rows.json</a></li>'
            f'<li>Composition: every entry\'s <code>composition</code> block (in its entity.json) states who composed its row — in session, or SPXI-gnΩsis — and under what. '
            f'Rows SPXI-gnΩsis composes land by <a href="/scripts/land_non_row.py">scripts/land_non_row.py</a>, each landing recorded in <a href="{DS_URL}/landings.json">landings.json</a>; '
            'a row a landing replaces is kept, and listed on its entry\'s page.</li>'
            f'<li>Identifiers: each entry with a row has an AXN in the family NON (axn/v2.3, <a href="/api/axn-protocol.json">the protocol</a>, non_entries), minted by '
            f'<a href="/scripts/non_axn.py">scripts/non_axn.py</a> into <a href="{DS_URL}/axn.json">axn.json</a>: its root is the entry across its compositions, and each composition of the row is a version.</li>'
            '<li>Table of contents: <a href="/non/index.json">/non/index.json</a> · field claims: <a href="/non/claims.json">/non/claims.json</a> · entity pages: <a href="/sitemap-non.xml">sitemap-non.xml</a></li>'
            f'<li>Service: rows are composed on commission by <a href="{GNOSIS}">SPXI-gnΩsis</a> (EA-WIKI-OPEN-01 v1.1, <a href="/s/records/1697/">#1697</a>), whose results name their /non row; '
            f'/non is SPXI method <a href="https://www.spxi.dev/methods/#m-0-16">0.16</a> and the opening method <a href="https://www.spxi.dev/methods/#m-0-17">0.17</a>.</li>'
            '<li>These pages are built by <a href="/scripts/build_non.py">scripts/build_non.py</a> from those files; it writes nothing back.</li></ul>')
    crumbs = lambda here: f'<p class="meta" style="margin-bottom:8px"><a href="/non/">/non</a> › {esc(here)}</p>'
    def subpage(path, title, desc, body, ld_type="WebPage"):
        url = f"{BASE}/{path[:-10]}"
        jl = {"@context": "https://schema.org", "@type": ld_type, "name": title, "url": url, "description": desc,
              "isPartOf": {"@type": "Dataset", "name": "The Negative of the Negative", "url": f"{BASE}/non/"}}
        files[path] = npage(title + " — Alexanarch", desc, body, url, jl, f'<link rel="canonical" href="{url}">\n<style>.regt td{{overflow-wrap:normal;word-break:normal}}</style>\n')
        sm.append(f"  <url><loc>{url}</loc></url>")
    subpage("non/about/index.html", "The Negative of the Negative — status, method and procedure",
            "The status of the Negative of the Negative, how an entity reads, its entity types, and its procedure and data.",
            crumbs("status, method and procedure") + '<h1>Status, method and procedure</h1>' + LEDE + STATUS
            + '<h2>How an entity reads</h2>' + how + '<h2>Entity types</h2>' + LEGEND + PROC
            + f'<p class="foot">Lee Sharks · Crimson Hexagonal Archive · {built_on}.</p>')
    if regp.exists():
        trs = []
        for ek in [x["entity"] for x in panel["entities"] if x["entity"] in groups] + [k for k in groups if k not in ents]:
            for e in groups[ek]:
                dest = f'/non/{esc(ek)}/#reg-{esc(e["slug"])}' if ek in keys else f'#reg-{esc(e["slug"])}'
                cards_ = f' · {e["cites"]} card{"" if str(e["cites"]) == "1" else "s"}' if e.get("cites") is not None else ""
                trs.append(f'<tr><td><a href="/non/{esc(ek)}/">{esc(ents.get(ek, {"name": ek})["name"])}</a></td>'
                           f'<td><a href="{dest}">{esc(e["q"])}</a><br><span class="meta" style="white-space:nowrap">{esc(", ".join(e["dates"]))}</span></td>'
                           f'<td>{esc(e["surface"])}<br><span class="meta">{esc(e["auth"])}</span></td>'
                           f'<td>{"present" if e["archive_present"] else "absent"}<span class="meta">{esc(cards_)}</span></td></tr>')
        subpage("non/register/index.html", "The Negative of the Negative — the register",
                f"Every address of the Negative of the Negative: {reg.get('address_count')} addresses, {reg.get('observation_count')} observations.",
                crumbs("the register") + '<h1>The register</h1>' + REGHEAD
                + '<div class="tw"><table class="regt"><thead><tr><th>entity</th><th>address · date</th><th>surface · signed</th><th>archive · cards</th></tr></thead>'
                + f'<tbody>{"".join(trs)}</tbody></table></div>'
                + f'<p class="meta">Each address opens on its entity\'s page, transcript and source cards with it. '
                f'<a href="{DS_URL}/register.json">register json</a> · <a href="{DS_URL}/register.schema.json">schema</a> · <a href="/scripts/non_intake.py">intake</a></p>', "CollectionPage")
    seen = {}
    for e in reg["entries"]:
        seen.setdefault(e["entity"], set()).add(e["q"])
    pl = []
    for pr in sorted(panel["entities"], key=lambda x: sortkey(x["name"])):
        al = []
        for ad in pr["addresses"]:
            href = address_href(pr["entity"], ad["address"])
            nm = f'<a href="{href}">{esc(ad["address"])}</a>' if href else esc(ad["address"])
            al.append(f'<code>{nm}</code>' + (' <span class="pill ok">observed</span>' if ad["address"] in seen.get(pr["entity"], ()) else ""))
        done = pr["entity"] in rows
        nm = f'<a href="/non/{esc(pr["entity"])}/">{esc(pr["name"])}</a>' if pr["entity"] in keys else esc(pr["name"])
        pl.append(f'<li id="p-{esc(pr["entity"])}"><strong>{nm}</strong><span class="pill dim">{esc(type_label(pr["type"]))}</span><span class="pill dim">{esc(pr["source"])}</span>'
                  + ('<span class="pill ok">composed</span>' if done else '<span class="pill warn">listed, not composed</span>') + f'<span class="stage">addresses: {" · ".join(al)}</span>'
                  + f'<span class="stage">{md_inline(pr["stage"])}</span></li>')
    n_done = sum(1 for pr in panel["entities"] if pr["entity"] in rows)
    subpage("non/panel/index.html", "The Negative of the Negative — the panel",
            f"The working panel of the Negative of the Negative: {len(panel['entities'])} entities, {n_done} composed.",
            crumbs("the panel") + f'<h1>The panel — {esc(panel["status"])}</h1>'
            + f'<p class="sub">{len(panel["entities"])} entities, {n_done} composed, {len(panel["entities"]) - n_done} listed and not yet composed; alphabetical. '
            f'{esc(panel["keying"])} {esc(panel["rule"])}</p><ul class="plist">{"".join(pl)}</ul>'
            + f'<p class="meta"><a href="{DS_URL}/panel/panel.json">panel.json</a></p>', "CollectionPage")

    # old anchors (/non/#e-k, #row-k, #ent-k, #trav-k, #reg-slug, #lv-k, #k-ksN …) land on the entity's page;
    # #register, #panel and #procedure land on the pages that now hold them
    regmap = {e["slug"]: e["entity"] for e in reg["entries"] if e["entity"] in keys}
    redirect = ('<script>(function(){var h=decodeURIComponent(location.hash.slice(1));if(!h||document.getElementById(h))return;'
                'var P={"register":"/non/register/","panel":"/non/panel/","procedure":"/non/about/#procedure","entities":"/non/"};'
                'if(P[h]){if(P[h]!=="/non/")location.replace(P[h]);return}'
                f'var K={json.dumps(sorted(keys, key=lambda x: (-len(x), x)))},R={json.dumps(regmap, sort_keys=True)};var k=null;'
                'if(h.indexOf("reg-")===0)k=R[h.slice(4)]||null;'
                'if(!k){var r=h.replace(/^(e|row|ent|trav|lv)-/,"");for(var i=0;i<K.length;i++){if(r===K[i]||r.indexOf(K[i]+"-")===0){k=K[i];break}}}'
                'if(k)location.replace("/non/"+k+"/#"+encodeURIComponent(h))})();</script>\n')
    jsonld = {"@context": "https://schema.org", "@type": "Dataset", "name": "The Negative of the Negative (v2, compositional)",
              "url": f"{BASE}/non/", "description": NON_DESC, "creator": CREATOR, "license": LICENSE, "creativeWorkStatus": "working; procedure not frozen",
              "isBasedOn": f"{BASE}/s/records/1690/", "version": reg.get("version"), "dateModified": reg.get("date"),
              "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{BASE}/non/index.json"},
                               {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{BASE}/non/claims.json"}],
              "hasPart": [{"@type": "CreativeWork", "name": x["name"], "url": x["record_url"],
                           **({"identifier": {"@type": "PropertyValue", "propertyID": "AXN", "value": x["axn"]}} if x.get("axn") else {})} for x in toc]}
    ihead = (f'<link rel="canonical" href="{BASE}/non/">\n<link rel="cite-as" href="{BASE}/non/">\n'
             f'<link rel="describedby" href="{BASE}/non/index.json" type="application/json">\n'
             f'<meta name="citation_title" content="The Negative of the Negative"><meta name="citation_date" content="{esc(str(reg.get("date")))}">'
             f'<meta name="citation_public_url" content="{BASE}/non/">\n' + ICSS + redirect)
    files["non/index.html"] = npage("The Negative of the Negative — /non — Alexanarch",
                                    "Public knowledge composed three ways at one address, with the archive admitted on equal terms; working, not frozen.",
                                    "\n".join(b), f"{BASE}/non/", jsonld, ihead, SEARCH_JS)

    # every field claim quoted, by row: what a sentence-level reader (SPXI-gnΩsis) matches a sentence against
    cl = []
    for k_ in sorted(rows):
        r_ = rows[k_]
        fc = {**(r_.get("field_claims") or {}), **(((r_.get("objects") or {}).get("KO") or {}).get("field_claims") or {})}
        fs = {**(r_.get("field_sources") or {}), **(((r_.get("objects") or {}).get("KO") or {}).get("field_sources") or {})}
        for cid in sorted(fc, key=lambda s: (len(s), s)):
            f = fc[cid]
            q = unquote(f.get("quote") or "")
            if not q:
                continue
            cl.append({"row": k_, "id": cid, "quote": q, "source": f.get("source"), "source_label": fs.get(f.get("source")),
                       "locus": f.get("locus"), "url": f"{BASE}/non/{k_}/"})
    files["non/claims.json"] = jdump({
        "id": "EA-NEGONT-02-NON-CLAIMS", "title": "The Negative of the Negative — every field claim quoted, by row",
        "canonical": f"{BASE}/non/claims.json", "date": reg.get("date"),
        "statement": ("Every field claim of every /non row with its quote as the row holds it, unquoted: a sentence-level reader matches a "
                      "sentence against these to name the row that already holds it. The row and its ledgers are the authority; this is their index."),
        "rows": {k_: {"axn": (AX.get(k_) or {}).get("axn"), "row_sha256": hashlib.sha256((V2 / "rows" / f"{k_}.json").read_bytes()).hexdigest()} for k_ in sorted(rows)},
        "service": SERVICE_BLOCK, "spxi_instrument": _spxi_record(f"{BASE}/non/"),
        "count": len(cl), "claims": cl})
    files["non/index.json"] = jdump({
        "id": "EA-NEGONT-02-NON", "title": "The Negative of the Negative — table of contents",
        "canonical": f"{BASE}/non/", "version": reg.get("version"), "date": reg.get("date"),
        "counts": {"panel_entities": len(panel["entities"]), "entity_pages": len(toc), "composed": sum(1 for x in toc if x["has_ko"]),
                   "register_addresses": reg.get("address_count"), "observations": reg.get("observation_count"),
                   "traversals": len(trav)},
        "statement": ("The Negative of the Negative (EA-NEGONT-02, #1690, v0.9): per-entity knowledge objects composed with the archive's sources on equal terms, ontology included, or in the archive's ontology where it is the suppressed witness, "
                      "the field carried whole and translated; entries composed under v0.7 (#1665) are recomposed one at a time. One row per entity with a page. Each record_url is the entity's own page and "
                      "its citation; json_url is the entry as data: its AXN, its composition, and the entry itself (entry: the knowledge object, every sentence with its claims, each claim's quote, source and locus), with links to its row, ledgers and traversal. "
                      "Working, not frozen (§7.0)."),
        "spec": f"{BASE}/s/records/1690/", "dataset": HF_NON, "panel": f"{BASE}{DS_URL}/panel/panel.json", "register": f"{BASE}{DS_URL}/register.json",
        "record_form": f"{BASE}/non/{{entity}}/", "json_form": f"{BASE}/non/{{entity}}/entity.json",
        "service": SERVICE_BLOCK, "spxi_instrument": _spxi_record(f"{BASE}/non/"),
        "entities": toc})
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sm) + "\n</urlset>\n"
    files["sitemap-non.xml"] = sitemap

    W = DS / "worked-example"
    fi = [folder_index(W / "selection", "Selection readings — model collapse", "The S1–S3 readings of Appendix A (§A.3): each candidate, its verdict and its quoted reason."),
          folder_index(W / "audit", "Extraction audit — model collapse", "The second extraction (§3.8, §A.9) and the control arm A′."),
          folder_index(V2 / "panel/configs", "Traversal configurations", "One configuration per address for scripts/non_traverse.py.")]
    for d in sorted((V2 / "traversal").iterdir()):
        if d.is_dir():
            fi.append(folder_index(d, f"D/R/O traversal — {d.name}", "Candidate files by stratum, the summary, and the reading where done. Candidates are found by string; admission is by reading."))
    for p, h in fi:
        files[p.relative_to(ROOT).as_posix()] = h

    # ── the index by type, case and month, as /captures/by/ (ruled 2026-10-19: "/non needs an index like /captures") ──
    for k, v in by_index(toc, rows, groups, panel, reg).items():
        files[k] = v
        sm.append(f"<url><loc>{BASE}/{k[:-10]}</loc></url>")
    files["sitemap-non.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sm) + "\n</urlset>\n"

    # ── every /non page labels itself as SPXI method 0.16, as /captures does 0.9 (ruled 2026-10-25) ──
    for k in list(files):
        if k.startswith("non/") and k.endswith(".html"):
            files[k] = _spxi_label(files[k], f"{BASE}/" + (k[:-len("index.html")] if k.endswith("index.html") else k))

    # ── write or check ──
    owned ={k.split("/")[1] for k in files if k.startswith("non/") and k.count("/") == 2}
    stale = [k for k, v in files.items() if not (ROOT / k).exists() or (ROOT / k).read_text(encoding="utf-8") != v]
    orphans = sorted(p.name for p in OUT.iterdir() if p.is_dir() and p.name not in owned and (p / "index.html").exists()
                     and MARK in (p / "index.html").read_text(encoding="utf-8")[:400]) if OUT.exists() else []
    sizes = {k: len(v.encode()) for k, v in files.items()}
    big = [k for k, n in sizes.items() if n > CEIL]
    if big:
        print(f"FAIL: {big} exceed {CEIL:,} bytes, the fetch ceiling these pages exist to stay under", file=sys.stderr)
        return 1
    for k in sorted(files):
        if k.startswith("non/") and k.endswith("/index.html") and k != "non/index.html" and sizes[k] > WARN:
            print(f"warning: {k} is {sizes[k]:,} bytes (over {WARN:,})", file=sys.stderr)
    if a.check:
        bad = stale + [f"non/{d}/ (orphan)" for d in orphans]
        if bad:
            print(f"FAIL: {len(bad)} /non output(s) missing or stale, e.g. {bad[:5]}", file=sys.stderr)
            return 1
        print(f"/non current: {len(toc)} entity pages, table of contents, sitemap, {len(fi)} folder listings")
        return 0
    for k in stale:
        p = ROOT / k
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(files[k], encoding="utf-8")
    import shutil
    for d in orphans:
        shutil.rmtree(OUT / d)
    ep = {k: n for k, n in sizes.items() if k.startswith("non/") and k.endswith("/index.html") and k != "non/index.html"}
    mx = max(ep, key=ep.get) if ep else None
    print(f"/non: {len(toc)} entity pages; non/index.html {sizes['non/index.html']:,} bytes; non/index.json {sizes['non/index.json']:,} bytes; "
          f"largest entity page {mx} {ep.get(mx, 0):,} bytes; {len(stale)} written, {len(orphans)} removed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
