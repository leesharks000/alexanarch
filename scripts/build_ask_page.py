#!/usr/bin/env python3
"""build_ask_page.py — the Ask tab (/ask/): general archival queries, and what the act of querying has accrued.

Operator, 2026-11-19 10:04–10:08: "somewhere there needs to be a page for general archival queries - this could be its own tab,
and extensive"; "its basically disciplines and subdisciplines, can have programme theme of practice grouped queries as well";
"that page should have some infographics or capture registry visual and data analysis, just something to show the relationship
between the act of querying and the representations that accrue".

Queries: data/ask-queries.json. Figures: computed from data/EA-WG-CAPTURES-01.json at build time. ChatGPT only (the
2026-11-19 10:04 ruling for the record-page battery). Run after seating captures or editing the query file:
    python3 scripts/build_ask_page.py
"""
import json, re, sys, datetime, collections, html
from pathlib import Path
from urllib.parse import quote_plus
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.render_navbar import render_navbar

E = html.escape
Q = json.loads((ROOT / 'data/ask-queries.json').read_text())
REG = json.loads((ROOT / 'data/EA-WG-CAPTURES-01.json').read_text())
TODAY = datetime.date.today()
DATE_TXT = f'{TODAY.day} {TODAY.strftime("%b %Y")}'
S1, S2 = '#2a78d6', '#eb6834'          # dataviz reference palette, categorical slots 1 and 2 (validated on #fcfcfb)


def entries():
    out = []
    def walk(o):
        if isinstance(o, dict):
            if 'slug' in o and 'q' in o:
                out.append(o); return
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(REG)
    return out


def num(v):
    try: return int(v)
    except (TypeError, ValueError): return 0


def _dedup(es):
    seen = {}
    for e in es:
        seen.setdefault(e['slug'], e)
    return list(seen.values())
ENTS = _dedup([e for e in entries() if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(e.get("date") or ""))])
def obs_dates(e):
    ob = [str(o.get('date'))[:10] for o in (e.get('observations') or []) if isinstance(o, dict) and o.get('date')]
    if len(ob) < (num(e.get('n_observations')) or 1): ob = [str(d)[:10] for d in (e.get('dates') or [e['date']])]
    return ob
ARCH = re.compile(r'alexanarch|lee sharks|crimson hexagon|sharks\'|the archive', re.I)
RECORD = re.compile(r'deposit #\d+|/s/records/\d+', re.I)


def is_archive_level(e):
    q = str(e['q'])
    return bool(ARCH.search(q)) and not RECORD.search(q) and len(q.split()) >= 5


def ask_link(q, text=None, cls='q b'):
    """A query as a ChatGPT link, shown as a short button label; the full query is in the href and the tooltip.
    {date} is filled in the browser; the static href and tooltip carry the build date."""
    qs = q.replace('{date}', DATE_TXT)
    t = E(text or q).replace('{date}', f'<span class="d">{E(DATE_TXT)}</span>')
    return f'<a class="{cls}" data-q="{E(q)}" title="{E(qs)}" href="https://chatgpt.com/?q={E(quote_plus(qs))}" target="_blank" rel="noopener">{t}</a>'


L = Q['labels']


def row(label, buttons, sub=False):
    return f'<div class="row{" sub" if sub else ""}"><span class="rl">{E(label)}</span><span class="bs">{"".join(buttons)}</span></div>'


def cap(x):
    return x[0].upper() + x[1:]


def short(q, n=88):
    q = re.sub(r'\s+', ' ', q).strip()
    return q if len(q) <= n else q[:n].rsplit(' ', 1)[0] + '…'


def fill(t, **kw):
    for k, v in kw.items(): t = t.replace('{' + k + '}', v)
    return t.replace('{ground}', Q['ground'])


# ---------- figures ----------
def svg_frame(w, h, body, label):
    return f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{E(label)}" style="max-width:{w}px;font-family:var(--sans);font-size:11px">{body}</svg>'


def fig_accrual():
    """Cumulative addresses (queries asked) and cumulative observations (compositions seated), by week."""
    wk = lambda d: (datetime.date.fromisoformat(d) - datetime.timedelta(days=datetime.date.fromisoformat(d).weekday()))
    addr = collections.Counter(wk(e['date']) for e in ENTS)
    obs = collections.Counter()
    for e in ENTS:
        for d in obs_dates(e):
            try: obs[wk(str(d)[:10])] += 1
            except ValueError: pass
    weeks = sorted(set(addr) | set(obs)); ca = co = 0; rows = []
    for w in weeks:
        ca += addr[w]; co += obs[w]; rows.append((w, ca, co))
    W, H, L, B, T, R = 680, 260, 48, 30, 14, 130
    ymax = max(r[2] for r in rows) * 1.05; n = len(rows)
    x = lambda i: L + i * (W - L - R) / max(n - 1, 1); y = lambda v: H - B - v * (H - B - T) / ymax
    g = ''.join(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#e6e6e3"/><text x="{L-6}" y="{y(v)+4:.1f}" text-anchor="end" fill="#52514e">{v:,}</text>'
                for v in range(0, int(ymax) + 1, 250))
    def line(k, col):
        pts = ' '.join(f'{x(i):.1f},{y(r[k]):.1f}' for i, r in enumerate(rows))
        dots = ''.join(f'<circle cx="{x(i):.1f}" cy="{y(r[k]):.1f}" r="7" fill="transparent"><title>week of {r[0]}: {r[1]:,} addresses, {r[2]:,} observations</title></circle>' for i, r in enumerate(rows))
        return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>{dots}'
    ticks = ''.join(f'<text x="{x(i):.1f}" y="{H-10}" text-anchor="middle" fill="#52514e">{r[0].strftime("%d %b")}</text>' for i, r in enumerate(rows) if i % max(n // 7, 1) == 0)
    lab = (f'<text x="{x(n-1)+6:.1f}" y="{y(rows[-1][2])+4:.1f}" fill="#0b0b0b">observations {rows[-1][2]:,}</text>'
           f'<text x="{x(n-1)+6:.1f}" y="{y(rows[-1][1])+4:.1f}" fill="#0b0b0b">addresses {rows[-1][1]:,}</text>')
    body = g + line(2, S2) + line(1, S1) + ticks + lab
    table = ''.join(f'<tr><td>{r[0]}</td><td>{r[1]:,}</td><td>{r[2]:,}</td></tr>' for r in rows)
    return svg_frame(W, H, body, 'Cumulative addresses and observations by week'), f'<table><tr><th>week of</th><th>addresses</th><th>observations</th></tr>{table}</table>', rows


def fig_series():
    """The 'living body of thought' series: each composition, by date, with the citations it carried."""
    pts = sorted([(e['date'], num(e.get('cites')), e['slug'], e.get('surface') or '') for e in ENTS
                  if re.search(r'living body|body of (evolving )?thought|evolving (literary|system|body)', str(e['q']), re.I)])
    W, H, L, B, T, R = 680, 220, 40, 30, 14, 20
    d0 = datetime.date.fromisoformat(pts[0][0]); d1 = datetime.date.fromisoformat(pts[-1][0]); span = max((d1 - d0).days, 1)
    ymax = max(p[1] for p in pts) * 1.1 or 1
    x = lambda d: L + (datetime.date.fromisoformat(d) - d0).days * (W - L - R) / span; y = lambda v: H - B - v * (H - B - T) / ymax
    step = 10 if ymax > 40 else 5
    g = ''.join(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#e6e6e3"/><text x="{L-6}" y="{y(v)+4:.1f}" text-anchor="end" fill="#52514e">{v}</text>' for v in range(0, int(ymax) + 1, step))
    dots = ''.join(f'<a href="/captures/{E(s)}/"><circle cx="{x(d):.1f}" cy="{y(c):.1f}" r="5" fill="{S1}" stroke="#fcfcfb" stroke-width="2"><title>{d} · {E(su)} · {c} citations · {E(s)}</title></circle></a>' for d, c, s, su in pts)
    ticks = ''.join(f'<text x="{x(str(d0 + datetime.timedelta(days=k)))}" y="{H-10}" text-anchor="middle" fill="#52514e">{(d0 + datetime.timedelta(days=k)).strftime("%d %b")}</text>' for k in range(0, span + 1, max(span // 6, 1)))
    table = ''.join(f'<tr><td>{d}</td><td>{E(su)}</td><td>{c}</td><td><a href="/captures/{E(s)}/">{E(s)}</a></td></tr>' for d, c, s, su in pts)
    return svg_frame(W, H, g + dots + ticks, 'Living-body series: citations per composition'), f'<table><tr><th>date</th><th>surface</th><th>citations</th><th>capture</th></tr>{table}</table>', pts


def fig_bars(counter, label, top=8):
    items = counter.most_common(top); rest = sum(counter.values()) - sum(v for _, v in items)
    if rest: items.append(('other', rest))
    W, rowh, L = 680, 24, 210; H = rowh * len(items) + 8; vmax = max(v for _, v in items)
    body = ''
    for i, (k, v) in enumerate(items):
        yy = 4 + i * rowh; w = max((W - L - 60) * v / vmax, 2)
        body += (f'<text x="{L-8}" y="{yy+15}" text-anchor="end" fill="#0b0b0b">{E(str(k))}</text>'
                 f'<rect x="{L}" y="{yy+4}" width="{w:.1f}" height="{rowh-8}" rx="4" fill="{S1}"><title>{E(str(k))}: {v:,}</title></rect>'
                 f'<text x="{L+w+6:.1f}" y="{yy+15}" fill="#52514e">{v:,}</text>')
    table = ''.join(f'<tr><td>{E(str(k))}</td><td>{v:,}</td></tr>' for k, v in items)
    return svg_frame(W, H, body, label), f'<table>{table}</table>'


def figure(title, caption, svg, table):
    return (f'<figure><h3>{E(title)}</h3>{svg}<figcaption>{caption}</figcaption>'
            f'<details><summary>Table</summary>{table}</details></figure>')


# ---------- page ----------
def build():
    arch = [e for e in ENTS if is_archive_level(e)]
    n_addr, n_obs = len(ENTS), sum(len(obs_dates(e)) for e in ENTS)
    cited = [e for e in arch if num(e.get('cites')) > 0]
    f1, t1, rows = fig_accrual()
    f2, t2, pts = fig_series()
    f3, t3 = fig_bars(collections.Counter(e.get('surface') or 'unrecorded' for e in arch), 'Archive-level addresses by surface')
    dc = collections.Counter()
    for e in arch:
        try: ds = e.get('defects') if isinstance(e.get('defects'), list) else json.loads(str(e.get('defects') or '[]').replace("'", '"'))
        except ValueError: ds = []
        dc.update(ds)
    f4, t4 = fig_bars(dc, 'Defects recorded on archive-level compositions')

    sec = []
    ts = Q['timescales']
    tq = ''.join(row(lt, [ask_link(fill(t, window=w, date='{date}'), lw) for w, lw in zip(ts['windows'], L['windows'])]) for t, lt in zip(ts['templates'], L['timescale_templates']))
    sec.append(f'<section id="time"><h2>The archive over time</h2><p class="n">Read a window of work ending today as one body of thought.</p>{tq}</section>')
    sec.append('<section id="whole"><h2>The archive as a whole</h2><div class="bs wrapb">' + ''.join(ask_link(q, lq) for q, lq in zip(Q['whole'], L['whole'])) + '</div></section>')
    def hfill(t, h):
        q = fill(t, name=h['name'], focus=h['focus'])
        return q.replace(h['name'] + "'s", h['name'] + "'") if h['name'].endswith('s') else q
    cast = row('the cast', [ask_link(fill(q), lq) for q, lq in zip(Q['cast'], L['cast'])])
    cast += ''.join(row(h['name'], [ask_link(hfill(t, h), lt.replace('{focus}', h['focus'])) for t, lt in zip(Q['heteronym_templates'], L['heteronym_templates'])], sub=True) for h in Q['heteronyms'])
    sec.append(f'<section id="heteronyms"><h2>The heteronyms</h2><p class="n">The cast of characters: the twelve of the Dodecad, each from several angles.</p>{cast}</section>')
    disc = ''
    for dsc in Q['disciplines']:
        top = row('the field', [ask_link(fill(t, field=dsc['name']), lt) for t, lt in zip(Q['discipline_templates'], L['discipline_templates'])])
        subs = ''.join(row(s_, [ask_link(fill(t, field=s_), lt) for t, lt in zip(Q['subdiscipline_templates'], L['subdiscipline_templates'])], sub=True) for s_ in dsc['subs'])
        disc += f'<details><summary>{E(cap(dsc["name"]))} <span class="c">{len(dsc["subs"])} subfield{"s" if len(dsc["subs"]) != 1 else ""}</span></summary>{top}{subs}</details>'
    sec.append(f'<section id="disciplines"><h2>By discipline and subdiscipline</h2>{disc}</section>')
    for key, title in (('programmes', 'By programme'), ('themes', 'By theme'), ('practices', 'By practice')):
        tk = key[:-1] + '_templates'
        body = ''.join(row(cap(n), [ask_link(fill(t, name=n), lt) for t, lt in zip(Q[tk], L[tk])]) for n in Q[key])
        sec.append(f'<section id="{key}"><h2>{title}</h2>{body}</section>')
    asked = sorted(arch, key=lambda e: e['date'], reverse=True)
    def arow(e):
        q = str(e['q']).strip()
        return (f'<li><span class="m">{E(e["date"])} · {E(e.get("surface") or "")} · {num(e.get("cites"))} cites</span>'
                f'{ask_link(q, short(q), "q t")} <a class="cap" href="/captures/{E(e["slug"])}/">capture</a></li>')
    ab = ''.join(arow(e) for e in asked[:15])
    more = f'<details><summary>All {len(asked)} <span class="c">newest first</span></summary><ul class="asked">{"".join(arow(e) for e in asked[15:])}</ul></details>' if len(asked) > 15 else ''
    sec_asked = (f'<section id="asked"><h2>Asked before <span class="c">{len(asked)} archive-level addresses</span></h2>'
                 f'<p class="n">Each was asked as written and its composition is seated. The link reopens the query; "capture" opens what came back.</p><ul class="asked">{ab}</ul>{more}</section>')

    n_q = sum(len(Q['timescales']['templates']) * len(Q['timescales']['windows']) for _ in [0]) + len(Q['whole']) + len(Q['cast']) + len(Q['heteronyms']) * len(Q['heteronym_templates']) + sum(len(Q['discipline_templates']) + len(d['subs']) * len(Q['subdiscipline_templates']) for d in Q['disciplines']) + sum(len(Q[k]) * len(Q[k[:-1] + '_templates']) for k in ('programmes', 'themes', 'practices'))
    first = min(e['date'] for e in ENTS)
    stats = (f'<div class="stats"><div><b>{n_q:,}</b>queries on this page</div><div><b>{n_addr:,}</b>addresses seated since {first}</div>'
             f'<div><b>{n_obs:,}</b>observations</div><div><b>{len(arch):,}</b>archive-level addresses</div>'
             f'<div><b>{round(100 * len(cited) / max(len(arch), 1))}%</b>of those compositions cite a source</div></div>')
    figs = (figure('Querying and what accrues', f'Each address is a query asked once and seated; each observation is a composition recorded at an address, the first and every later return. The gap between the lines is the re-asking: an address asked again accrues at the same record. Weekly, from the Capture Registry (v{E(str(REG.get("version")))}).', f1, t1)
            + figure('The living-body series', f'Each dot is one composition forced by a query that asks the archive to be read as a living or evolving body of thought over a window of time ({len(pts)} compositions), placed by date and by the number of citations it carried. Each dot opens its capture.', f2, t2)
            + figure('Where the archive-level queries were asked', 'Archive-level addresses (queries that name the archive, its author or the Crimson Hexagon, and no single deposit) by the surface they were asked on.', f3, t3)
            + figure('What went wrong in the compositions', 'Defects recorded at intake on the archive-level compositions, as coded in the registry (a composition can carry several). The representation that accrues includes its failures.', f4, t4))

    nav = render_navbar(active='/ask/')
    desc = f'General archival queries for alexanarch.org: {n_q:,} queries by time scale, heteronym, discipline and subdiscipline, programme, theme and practice, each opening on ChatGPT; with figures from the Capture Registry on what the act of querying has accrued.'
    page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ask — Alexanarch</title><link rel="canonical" href="https://www.alexanarch.org/ask/"><meta name="description" content="{E(desc)}">
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--dim:#777;--border:#e0e0e0;--surface:#fff;--sans:'IBM Plex Sans',sans-serif;--mono:'IBM Plex Mono',monospace}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.6;font-size:15px}}
.wrap{{max-width:900px;margin:0 auto;padding:60px 16px}}
.nav{{display:flex;gap:20px;margin-bottom:30px;font-size:0.85em;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}}
.nav a{{color:var(--accent);text-decoration:none}}
h1{{font-weight:500;font-size:1.7em;margin-bottom:.3em}} h2{{font-weight:500;font-size:1.15em;margin:2em 0 .6em;border-bottom:1px solid var(--border);padding-bottom:.2em}} h3{{font-weight:500;font-size:1em;margin-bottom:.4em}}
p{{margin:.5em 0}} .n{{color:#52514e;font-size:.9em}}
ul{{list-style:none}} li{{margin:.35em 0}} li.sub{{margin:.8em 0 .4em}} .sl{{font-size:.82em;text-transform:uppercase;letter-spacing:.05em;color:#52514e}}
li.sub ul{{margin-left:1em}}
a.q{{color:var(--accent);text-decoration:none}}
a.b{{display:inline-block;padding:3px 11px;margin:3px 6px 3px 0;border:1px solid #c9d3de;border-radius:14px;background:var(--surface);font-size:.84em;line-height:1.5;white-space:nowrap}}
a.b:hover,a.b:focus-visible{{background:var(--accent);border-color:var(--accent);color:#fff}}
a.t{{border-bottom:1px dotted #b8c4d0}} a.t:hover{{border-bottom-style:solid}}
.row{{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 10px;padding:5px 0;border-bottom:1px solid #f0f0ee}} .row:last-child{{border-bottom:none}}
.rl{{flex:0 0 230px;font-size:.9em;color:#2b2b2a}} .row.sub .rl{{padding-left:1em;color:#52514e;font-size:.85em}} .bs{{flex:1 1 300px}}
.lede{{color:#3a3a38;margin:.2em 0 .6em}} details.about{{font-size:.92em}} details.about summary,details.figs summary{{font-weight:400;color:var(--accent)}}
@media (max-width:600px){{.rl{{flex-basis:100%}} .row.sub .rl{{padding-left:0}}}}
details{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:.5em .9em;margin:.4em 0}} summary{{cursor:pointer;font-weight:500}} details ul{{margin:.5em 0 .3em}}
.c{{font-family:var(--mono);font-size:.78em;color:var(--dim);margin-left:.4em}}
.stats{{display:flex;flex-wrap:wrap;gap:12px;margin:1.2em 0}} .stats div{{flex:1 1 140px;background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:.7em .9em;font-size:.85em;color:#52514e}} .stats b{{display:block;font-size:1.6em;font-weight:500;color:#0b0b0b}}
figure{{background:#fcfcfb;border:1px solid var(--border);border-radius:6px;padding:1em;margin:1em 0}} figcaption{{font-size:.85em;color:#52514e;margin-top:.5em}}
figure details{{border:none;padding:0;background:none;margin-top:.5em}} table{{border-collapse:collapse;font-size:.8em;margin-top:.4em}} td,th{{border-bottom:1px solid var(--border);padding:2px 8px;text-align:left}}
ul.asked li{{font-size:.92em}} .m{{font-family:var(--mono);font-size:.75em;color:var(--dim);margin-right:.4em}} a.cap{{font-size:.8em;color:var(--dim)}}
.toc a{{display:inline-block;white-space:nowrap;margin-right:1em;color:var(--accent);font-size:.9em}}
</style></head><body><div class="wrap">
<!-- NAV-START -->{nav}<!-- NAV-END -->
<h1>Ask</h1>
<p class="lede">Queries to the archive as a whole. Each button opens ChatGPT with the full query; hover to read it first.</p>
<details class="about"><summary>About this page</summary>
<p>Queries addressed to the archive as a whole: over time, by heteronym, by discipline and subdiscipline, by programme, theme and practice. Each opens on ChatGPT, signed out, with the query as written. A composition any of them forces can be seated in the <a href="/captures/" style="color:var(--accent)">Capture Registry</a>, where each query string is its own address. Single works are asked from their record pages, which carry their own battery.</p>
</details>
<p class="toc"><a href="#time">Over time</a><a href="#whole">As a whole</a><a href="#heteronyms">Heteronyms</a><a href="#disciplines">Disciplines</a><a href="#programmes">Programmes</a><a href="#themes">Themes</a><a href="#practices">Practices</a><a href="#accrue">What accrues</a><a href="#asked">Asked before</a></p>
{''.join(sec)}
<section id="accrue"><h2>What accrues</h2>{stats}{figs}</section>
{sec_asked}
<p class="n" style="margin-top:2em">Built {TODAY.isoformat()} by scripts/build_ask_page.py from data/ask-queries.json and the Capture Registry. Dates in the queries are filled with today's date in your browser.</p>
</div>
<script>
(function(){{try{{var d=new Date(),m=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],t=d.getDate()+" "+m[d.getMonth()]+" "+d.getFullYear();
document.querySelectorAll("a.q").forEach(function(a){{var q=a.getAttribute("data-q");if(q.indexOf("{{date}}")<0)return;
var f=q.split("{{date}}").join(t);a.href="https://chatgpt.com/?q="+encodeURIComponent(f).replace(/%20/g,"+");a.title=f;
a.querySelectorAll(".d").forEach(function(s){{s.textContent=t}})}})}}catch(e){{}}}})();
</script></body></html>'''
    out = ROOT / 'ask' / 'index.html'; out.parent.mkdir(exist_ok=True); out.write_text(page)
    print(f'ask: {n_q} queries; {len(arch)} archive-level addresses; {len(pts)} living-body compositions; written {out.relative_to(ROOT)}')


if __name__ == '__main__':
    build()
