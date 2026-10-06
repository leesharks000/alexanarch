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
.card-head{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px;margin-bottom:6px}
.card-section{font-family:var(--mono);font-size:.72em;color:var(--teal);text-transform:uppercase;letter-spacing:.06em}
.card-date{font-family:var(--mono);font-size:.74em;color:var(--dim)}
.card-query{font-weight:600;color:var(--accent);font-size:1.15em;margin-bottom:6px;line-height:1.4}
.card-query a{border:0}
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
details>summary .n{color:var(--dim);font-family:var(--mono);font-size:.86em;margin-left:auto;flex:none;padding-left:8px}
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
    return reg

def claim_li(cid, ko, ledger, reg, FC=None, FS=None):
    """One sourced claim, the same rendering wherever it appears (provenance list, lineage card)."""
    FC = FC if FC is not None else ko["field_claims"]
    FS = FS if FS is not None else ko["field_sources"]
    if cid in FC:
        f = FC[cid]
        return (f'<li><code class="cid">{esc(cid)}</code> {esc(FS.get(f["source"], f["source"]))}, {esc(f["locus"])} '
                f'<span class="pill dim">documented · field</span><br><span class="qt">{esc(unquote(f["quote"]))}</span></li>')
    c = ledger[cid]; d = reg[c["dep"]]
    return (f'<li><code class="cid">{esc(cid)}</code> <a href="/s/records/{c["dep"]}/">#{c["dep"]}</a> <em>{esc(d["title"][:120])}</em> '
            f'<span class="meta">{esc(str(d.get("creator") or ""))} · {esc(str(c.get("date") or ""))} · {esc(c["locus"])}</span> '
            f'<span class="pill">{esc(c["modality"])}</span><br><span class="qt">{esc(unquote(c["quote"]))}</span></li>')

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
            d = reg[e]; eh = f'#{e} {esc(d["title"][:70])} · {esc(str(d.get("date") or ""))}'
        others = sorted({("#%d" % ledger[c]["dep"]) if c in ledger else FC[c]["source"] for c in ln["claims"]})
        cards.append(f'<details class="lc"><summary><span class="lc-n">{i}</span>{esc(ln["lineage"])}<span class="lc-e">{eh}</span>'
                     f'<span class="lc-c">{len(ln["claims"])} claim{"" if len(ln["claims"]) == 1 else "s"} · {esc(", ".join(others))}</span></summary>'
                     f'<ul class="claims">{"".join(claim_li(c, ko, ledger, reg, FC, FS) for c in ln["claims"])}</ul></details>')
    pc.append(f'<div class="rail" aria-label="Sources, one card per lineage">{"".join(cards)}</div></div></div>')
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
    reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
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
                cl.append(f'<li><code class="cid">{esc(cid)}</code> <a href="/s/records/{c["dep"]}/">#{c["dep"]}</a> <em>{esc(d["title"][:120])}</em> '
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
    b.append('<nav class="jump"><a href="#register">register</a><a href="#rows">rows</a><a href="#traversals">traversals</a><a href="#panel">panel</a><a href="#procedure">procedure and data</a></nav>')
    b.append('<h2>How a row reads</h2><div class="objs">'
             '<div class="obj"><b>T</b>the transcript: what the composition layer gave, verbatim, with its source cards</div>'
             '<div class="obj"><b>L(B)</b>the address recomposed from the full texts of the sources the layer itself surfaced</div>'
             '<div class="obj"><b>L(B ∪ A)</b>the same algorithm with the archive\'s subset admitted on equal terms</div>'
             '<div class="obj"><b>Δ</b>T against L(B): what the disclosed field held and was not composed. L(B) against L(B ∪ A): what admission adds</div>'
             '<div class="obj"><b>KO</b>the knowledge object: L(B ∪ A) written as public knowledge, with no provenance in the prose and every sentence sourced below it</div>'
             '<div class="obj"><b>K</b>the prospective kernel: what admission adds, derived from the plan, adjudicated later in both directions</div></div>')
    b.append('<p>The archive\'s subset is selected by its <strong>bearing</strong> on the address, in three strata: <strong>D</strong>, direct (the archive names the entity and says something about it); <strong>R</strong>, relational (the archive relates the entity to one of its own objects); <strong>O</strong>, ontological (the archive applies one of its own categories to the entity, or to a class the field says it belongs to). A citation hop from what reading admits finds the term-absent tail. Volume never removes a source.</p>')

    # the register: one card per address, captures grammar (2026-10-06)
    regp = V2 / "register.json"
    if regp.exists():
        reg = json.loads(regp.read_text(encoding="utf-8"))
        b.append(f'<h2 id="register">The register — {reg["address_count"]} address{"" if reg["address_count"] == 1 else "es"}, '
                 f'{reg["observation_count"]} observation{"" if reg["observation_count"] == 1 else "s"} · v{esc(str(reg["version"]))}</h2>'
                 f'<p class="sub">{esc(reg["_what_this_is"])}</p>')
        for e in reg["entries"]:
            pills = [f'<span class="pill dim">{esc(e["auth"])}</span>', f'<span class="pill dim">panel row {esc(e["panel_row"])}</span>',
                     ('<span class="pill warn">archive present · also a capture</span>' if e["archive_present"] else '<span class="pill">archive absent</span>')]
            if e.get("cites") is not None:
                pills.append(f'<span class="pill dim">{e["cites"]} source cards</span>')
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
                                 + f'<p class="meta">Archive: {esc(ob.get("archive_basis") or "")}</p>', n=esc(ob["obs_id"])))
            href = address_href(e["panel_row"], e["q"])
            qh = f'<a href="{href}">{esc(e["q"])}</a>' if href else esc(e["q"])
            b.append(f'<div class="card" id="reg-{esc(e["slug"])}"><div class="card-head"><span class="card-section">{esc(e["surface"])}</span>'
                     f'<span class="card-date">{esc(", ".join(e["dates"]))}</span></div>'
                     f'<div class="card-query">{qh}</div>'
                     f'<div class="card-status">{"".join(pills)}</div><div class="stack">{"".join(inner)}</div>'
                     f'<div class="card-links"><a href="/datasets/negative-of-the-negative/v2/register.json">register json</a>'
                     f'<a href="/datasets/negative-of-the-negative/v2/register.schema.json">schema</a><a href="/scripts/non_intake.py">intake</a>'
                     + (f'<a href="#row-{esc(e["panel_row"])}">composed row</a>' if e["panel_row"] in rows else "") + '</div></div>')

    # rows with compositions: one card per row, captures grammar
    b.append('<h2 id="rows">Rows composed</h2>')
    for key, r in rows.items():
        o = r["objects"]
        href = address_href(key, r["address"])
        q = f'<a href="{href}">{esc(r["address"])}</a>' if href else esc(r["address"])
        ko = o.get("KO")
        pills = ['<span class="pill warn">not frozen</span>', f'<span class="pill dim">type {esc(r["type"])}</span>',
                 f'<span class="pill dim">{esc(r["auth"])}</span>']
        if ko:
            pills.append(f'<span class="pill ok">knowledge object · {len(ko["sentences"])} sentences</span>')
        c = [f'<div class="card" id="row-{esc(key)}"><div class="card-head"><span class="card-section">{esc(r["surface"])}</span>'
             f'<span class="card-date">epoch {esc(r["epoch"])}</span></div>',
             f'<div class="card-query">{q}</div><div class="card-status">{"".join(pills)}</div>',
             f'<p class="meta" style="margin-bottom:12px">{md_inline(r["status"]["procedure"])}. Ledger: {md_inline(r["status"]["ledger"])}.</p>']
        if o.get("P") and ko:
            arms, stats = [], []
            html_a, st_a = two_levels(r, key, "P", "KO", "Field and archive (B ∪ A)")
            arms.append((key, "Field and archive (B ∪ A)")); stats.append(("B ∪ A", st_a))
            html_b = ""
            if o.get("P_B") and o.get("KO_B"):
                html_b, st_b = two_levels(r, key + "-b", "P_B", "KO_B", "Field alone (B)")
                arms.append((key + "-b", "Field alone (B)")); stats.append(("B", st_b))
            c.append(arm_switch(key, arms) + html_a + html_b + form_ledger(r, list(reversed(stats))))
        elif ko:
            c.append(knowledge_object(ko, r))
        tclaims = "".join(f"<li>{md_inline(x)}</li>" for x in o["T"]["claims"])
        fld = "".join(f"<li><strong>{esc(f['id'])}</strong> {md_inline(f['card'])} <span class=\"meta\">{esc(f['fetched'])}</span></li>" for f in r["field"])
        rail = ('<h3>Card rail</h3>' + table(o["L_BA"]["rail"], ["Card", "Snippet"])) if o["L_BA"].get("rail") else ""
        kent = "".join(det(esc(k.get("K", "")), md_inline(str(k.get("claim", ""))) + f' <span class="meta">{md_inline(str(k.get("source", "")))}</span>',
                           kv({kk: vv for kk, vv in k.items() if kk not in ("K",)}), n=esc(str(k.get("contrast", "")))) for k in r["kernel"])
        c.append('<h3 style="margin-top:18px">The objects</h3><div class="stack">')
        tref = o["T"].get("register")
        tlink = (f'<a href="#reg-{esc(tref["slug"])}">register entry {esc(tref["slug"])}</a> <span class="meta">{esc(tref["obs_id"])}</span> · '
                 if tref else "")
        c.append(det("T", "the transcript", f'<p>{tlink}<a href="/{o["T"]["path"]}">file as first run</a> <span class="meta">sha256 {o["T"]["sha256"][:16]}…</span></p><ul>{tclaims}</ul>',
                     n=f'{o["T"]["words"]} words · {o["T"]["cards"]} cards'))
        c.append(det("B", "the disclosed field", f"<ul>{fld}</ul>", n=f'{len(r["field"])} sources'))
        c.append(det("L(B)", "recomposed from the disclosed field", md_block(o["L_B"]["text"]), n=f'{o["L_B"]["words"]} words'))
        c.append(det("L(B ∪ A)", "with the archive on equal terms", md_block(o["L_BA"]["text"]) + rail, n=f'{o["L_BA"]["words"]} words'))
        c.append(det("Δ", "the delta", f'<p><strong>T against L(B)</strong> (representational): {md_inline(r["delta"]["T_vs_LB"])}</p>'
                     f'<p><strong>L(B) against L(B ∪ A)</strong> (the intervention): {md_inline(r["delta"]["LB_vs_LBA"])}</p>'))
        c.append(det("K", "the prospective kernel <span class=\"meta\">sealed only at freeze</span>", f'<div class="stack">{kent}</div>', n=f'{len(r["kernel"])} entries'))
        c.append('</div>')
        c.append(f'<div class="card-links"><a href="/datasets/negative-of-the-negative/v2/rows/{key}.json">row json</a>'
                 f'<a href="/{r["ledger"]["archive"]}">archive ledger</a><a href="/{r["ledger"]["selection"]}">selection readings</a>'
                 f'<a href="/{r["ledger"]["audit"]}">extraction audit</a>'
                 + (f'<a href="/datasets/negative-of-the-negative/v2/traversal/{key}/">D/R/O traversal</a>' if key in trav else "")
                 + (f'<a href="{href}">address page</a>' if href else "") + '</div></div>')
        b.append("".join(c))

    # traversals: one card each
    b.append('<h2 id="traversals">D/R/O traversals</h2><p class="sub">Candidates are found by string; admission is by reading.</p>')
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
                              n=f'{len(l["instances"])} · from #{l["earliest"]}') for l in rd["lineages"])
            c.append(det("", "admitted, by lineage", f'<div class="stack">{lin}</div>' + "".join(f"<p>{md_inline(x)}</p>" for x in rd.get("observations", [])),
                         n=f'{len(rd["lineages"])} lineages'))
        c.append(f'<div class="card-links"><a href="/datasets/negative-of-the-negative/v2/traversal/{key}/">candidate files</a>'
                 f'<a href="/datasets/negative-of-the-negative/v2/panel/configs/{key}.json">configuration</a>'
                 + (f'<a href="{href}">address page</a>' if href else "") + '</div></div>')
        b.append("".join(c))

    # panel: one entry per row
    b.append(f'<h2 id="panel">The panel — {esc(panel["status"])}</h2><p class="sub">{esc(panel["rule"])}</p>')
    pl = []
    for pr in panel["rows"]:
        href = address_href(pr["row"], pr["address"])
        nm = f'<a href="{href}">{esc(pr["address"])}</a>' if href else esc(pr["address"])
        done = pr["row"] in rows
        pl.append(f'<li><strong>{nm}</strong><span class="pill dim">type {esc(pr["type"])}</span><span class="pill dim">{esc(pr["source"])}</span>'
                  + ('<span class="pill ok">composed</span>' if done else "") + f'<span class="stage">{md_inline(pr["stage"])}</span></li>')
    b.append(det("", "All rows", f'<ul class="plist">{"".join(pl)}</ul>', n=f'{len(panel["rows"])} rows'))
    b.append('<h2 id="procedure">Procedure and data</h2><ul>'
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
