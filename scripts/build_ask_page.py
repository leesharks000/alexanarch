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
    # YOUR OWN QUESTION (operator, 2026-11-22 12:01): "it needs one where you can simply type a question and /ask will format it to
    # ground in and adapt to and extend archival materials and send it to an ai. give the example of alice's question, what does the
    # system pay people for?" The wrapper is data/ask-queries.json under own; the question as typed opens the prompt.
    OWN = Q.get('own')
    if OWN:
        sec.append('<section id="own"><h2>Ask your own question</h2><p class="n">Type a question about anything. The page sets it in an instruction to ground the answer in the archive&rsquo;s documents, take the question as the archive frames it, and extend past what the archive holds, marking what is new. Your question opens the prompt as you typed it, and that full prompt is the address if the answer is seated.</p>'
                   f'<div class="roll own" hidden><form class="tx owf"><label>Your question<textarea name="oq" rows="2" placeholder="{E(OWN["example"])}"></textarea></label>'
                   f'<button type="submit">Format it</button> <button type="button" class="rb" data-ex="{E(OWN["example"])}">Use the example: {E(OWN["example"])}</button></form>'
                   '<p class="rq"></p><a class="q b ra" hidden target="_blank" rel="noopener" href="#">Ask ChatGPT</a></div>'
                   f'<script type="application/json" id="owndata">{json.dumps(OWN["template"], ensure_ascii=False).replace("</", "<\\/")}</script></section>')
    # OUTLINES OF THE DISTRIBUTED EPIC (operator, 2026-11-22 11:59): "collecting outlines like this in different shapes that can then
    # be filled in later @ /ask... 'based on outline x @ [address] and related materials, compose book y of the crimson hexagon
    # distributed epic'". Each outline is a seated capture; its address is its capture page. The book number is the reader's.
    OUT = Q.get('outlines')
    if OUT:
        have = {e['slug'] for e in ENTS}
        items = [o for o in OUT['items'] if o['slug'] in have]
        orows = ''.join(f'<div class="row"><span class="rl"><a class="t" href="/captures/{E(o["slug"])}/">{E(o["label"])}</a></span><span class="bs"><span class="n">{E(o["shape"])}.</span> '
                        f'<button type="button" class="rb" data-outline="https://www.alexanarch.org/captures/{E(o["slug"])}/">Compose from this outline</button></span></div>' for o in items)
        books = ''.join(f'<option{" selected" if r == "VIII" else ""}>{r}</option>' for r in ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI'))
        sec.append('<section id="outlines"><h2>The distributed epic, from an outline</h2><p class="n">Outlines of the Crimson Hexagon distributed epic, in different shapes, each a composition seated in the Capture Registry. Choose a book and an outline; the prompt sends the composer to the outline&rsquo;s page and the materials around it, and asks for swerves.</p>'
                   f'<div class="roll outl" hidden><label class="n">Book <select class="ob">{books}</select></label>{orows}'
                   '<p class="rq"></p><a class="q b ra" hidden target="_blank" rel="noopener" href="#">Ask ChatGPT</a></div>'
                   f'<script type="application/json" id="outldata">{json.dumps(OUT["template"], ensure_ascii=False).replace("</", "<\\/")}</script></section>')
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
    HX = json.load(open(ROOT / 'data' / 'hexagon-seats.json'))['rooms']
    KEEP = ('Room', 'Chamber', 'Ark', 'Lab', 'Institute', 'Authority', 'Studio', 'Observatory', 'Embassy', 'Archive', 'Thesis', 'Academy', 'Library', 'Mint', 'Lanes', 'Worlds', 'Plume', 'Well', 'Swarm', 'Body', 'Heart', 'Internet', 'Dialectic', 'Document', 'Burn')
    def qname(r):
        n = r['name']
        if n.startswith('The '): return 'the ' + n[4:]
        if any(k in n for k in KEEP): return 'the ' + n
        if r['cat'] in ('core', 'ext', 'new', 'special'): return f'the {n} room'
        return n
    rooms = ''
    N_HEX = 0
    for cat, title in Q['room_categories']:
        rs = [r for r in HX.values() if r and r.get('cat') == cat]
        if not rs: continue
        body = ''
        for r in rs:
            qn = qname(r)
            bs = [ask_link(fill(t, name=qn), lt) for t, lt in zip(Q['room_templates'], L['room_templates'])]
            pr = (r.get('prompt') or '').strip()
            if pr.endswith('?'):
                bs.append(ask_link(Q['room_question_template'].replace('{name}', qn).replace('{prompt}', pr), pr))
            N_HEX += len(bs)
            body += row(r['name'], bs, sub=True)
        rooms += f'<details><summary>{E(title)} <span class="c">{len(rs)}</span></summary>{body}</details>'
    sec.append(f'<section id="rooms"><h2>The Crimson Hexagon</h2><p class="n">Its rooms and loci. Where a room asks a question of its own, that question is a button.</p>{rooms}</section>')
    # 2026-11-20: the Weird-ass prompts come after the cast and the scene (operator: 'these are perturbations after the cast and scene')
    W_ = Q.get('weird')
    if W_:
        wrows = ''.join(row(g['label'], [ask_link(x['q'], x['label']) for x in g['prompts']]) for g in W_['groups'])
        RL = W_['roll']
        rooms_for_roll = sorted({qname(r) for r in HX.values() if r and r.get('cat') in ('core', 'ext', 'new', 'special', 'seat') and 'Josephus' not in r['name']})
        ROLL_JSON = json.dumps(dict(RL, rooms=rooms_for_roll), ensure_ascii=False).replace('</', '<\\/')
        roll_box = ('<div class="roll" hidden><button type="button" class="rb" data-roll="new">Roll a new prompt</button> '
                    '<span class="n">A prompt assembled at random: which parts it has (a heteronym or two, an outside figure, a form, a field or a room, sometimes a voice, a quarrel or a constraint) is itself drawn, from the grammar kept with the page&rsquo;s prompts (data/ask-queries.json, under roll). Each roll is a new address.</span>'
                    '<p class="rq"></p><a class="q b ra" hidden target="_blank" rel="noopener" href="#">Ask ChatGPT</a></div>')
        sec.append('<section id="weird"><h2>Weird-ass prompts</h2><p class="n">Perturbations after the cast and the scene: prompts made to break the composer&rsquo;s template, setting historical and fictional figures among the heteronyms and in the rooms of the Hexagon, under constraints of voice, genre and form, many drawn from the avant-garde seatings of the originals library (<a class="t" href="/s/records/1682/">EA-CORPORA-18</a>). Each asks the composer to range across the archive&rsquo;s documents and synthesize them, gives it leave to add distinctions and swerves the archive does not yet hold, marked as new, and, where there is a constraint, asks it to check the constraint and report the count. The dice and the perturb buttons keep their prompts short: each roll draws which parts a prompt has as well as what fills them, with no length or count limits, one grounding sentence, and a check only where the constraint can be counted.</p>'
                    + wrows + '<h3 id="roll" style="margin-top:1.2em">Roll the dice</h3>' + roll_box
                    + f'<script type="application/json" id="rolldata">{ROLL_JSON}</script></section>')
    CJ = json.load(open(ROOT / 'data' / 'cha-journals.json'))
    jn = [j['canonical'] for j in CJ['journals']] + [j['canonical'] for j in CJ['imprints']]
    jart = lambda n: 'the ' + n if n.startswith(('Journal ', 'Transactions ')) else n
    jrows = ''.join(row(n, [ask_link(fill(t, name=jart(n)), lt) for t, lt in zip(Q['journal_templates'], L['journal_templates'])], sub=True) for n in jn)
    irows = ''.join(row(cap(n[4:] if n.startswith('the ') else n), [ask_link(fill(t, name=n), lt) for t, lt in zip(Q['institution_templates'], L['institution_templates'])], sub=True) for n in Q['institutions'])
    N_HEX += len(jn) * len(Q['journal_templates']) + len(Q['institutions']) * len(Q['institution_templates'])
    sec.append(f'<section id="institutions"><h2>Journals, presses and institutions</h2><details><summary>Journals and presses <span class="c">{len(jn)}</span></summary>{jrows}</details><details><summary>Institutions <span class="c">{len(Q["institutions"])}</span></summary>{irows}</details></section>')
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
    PERTURB = ('<div class="roll pert" hidden><button type="button" class="rb" data-roll="perturb">Perturb a query from this section</button>'
               '<p class="rq"></p><a class="q b ra" hidden target="_blank" rel="noopener" href="#">Ask ChatGPT</a></div>')
    for i, x in enumerate(sec):
        if not x.startswith(('<section id="weird"', '<section id="own"', '<section id="outlines"')):
            sec[i] = re.sub(r'(</h2>)', r'\1' + PERTURB, x, count=1)
    asked = sorted(arch, key=lambda e: e['date'], reverse=True)
    def arow(e):
        q = str(e['q']).strip()
        return (f'<li><span class="m">{E(e["date"])} · {E(e.get("surface") or "")} · {num(e.get("cites"))} cites</span>'
                f'{ask_link(q, short(q), "q t")} <a class="cap" href="/captures/{E(e["slug"])}/">capture</a></li>')
    ab = ''.join(arow(e) for e in asked[:15])
    more = f'<details><summary>All {len(asked)} <span class="c">newest first</span></summary><ul class="asked">{"".join(arow(e) for e in asked[15:])}</ul></details>' if len(asked) > 15 else ''
    sec_asked = (f'<section id="asked"><h2>Asked before <span class="c">{len(asked)} archive-level addresses</span></h2>'
                 f'<p class="n">Each was asked as written and its composition is seated. The link reopens the query; "capture" opens what came back.</p><ul class="asked">{ab}</ul>{more}</section>')

    n_q = sum(len(Q['timescales']['templates']) * len(Q['timescales']['windows']) for _ in [0]) + len(Q['whole']) + len(Q['cast']) + len(Q['heteronyms']) * len(Q['heteronym_templates']) + N_HEX + sum(len(Q['discipline_templates']) + len(d['subs']) * len(Q['subdiscipline_templates']) for d in Q['disciplines']) + sum(len(Q[k]) * len(Q[k[:-1] + '_templates']) for k in ('programmes', 'themes', 'practices')) + sum(len(g['prompts']) for g in Q.get('weird', {}).get('groups', []))
    first = min(e['date'] for e in ENTS)
    stats = (f'<div class="stats"><div><b>{n_q:,}</b>queries on this page</div><div><b>{n_addr:,}</b>addresses seated since {first}</div>'
             f'<div><b>{n_obs:,}</b>observations</div><div><b>{len(arch):,}</b>archive-level addresses</div>'
             f'<div><b>{round(100 * len(cited) / max(len(arch), 1))}%</b>of those compositions cite a source</div></div>')
    figs = (figure('Querying and what accrues', f'Each address is a query asked once and seated; each observation is a composition recorded at an address, the first and every later return. The gap between the lines is the re-asking: an address asked again accrues at the same record. Weekly, from the Capture Registry (v{E(str(REG.get("version")))}).', f1, t1)
            + figure('The living-body series', f'Each dot is one composition forced by a query that asks the archive to be read as a living or evolving body of thought over a window of time ({len(pts)} compositions), placed by date and by the number of citations it carried. Each dot opens its capture.', f2, t2)
            + figure('Where the archive-level queries were asked', 'Archive-level addresses (queries that name the archive, its author or the Crimson Hexagon, and no single deposit) by the surface they were asked on.', f3, t3)
            + figure('What went wrong in the compositions', 'Defects recorded at intake on the archive-level compositions, as coded in the registry (a composition can carry several). The representation that accrues includes its failures.', f4, t4))

    nav = render_navbar(active='/ask/')
    desc = f'General archival queries for alexanarch.org: {n_q:,} queries by time scale, heteronym, room and locus, journal and institution, discipline and subdiscipline, programme, theme and practice, each opening on ChatGPT, Google or Perplexity; with figures from the Capture Registry on what the act of querying has accrued.'
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
form.tx label{{display:block;font-size:.85em;color:#52514e;margin:.6em 0}} form.tx textarea,form.tx input,form.tx select{{display:block;width:100%;margin-top:.25em;font:inherit;font-size:.95em;padding:6px 8px;border:1px solid var(--border);border-radius:6px;background:var(--surface);color:var(--fg)}} form.tx textarea{{font-family:var(--mono);font-size:.85em}}
.tx2{{display:flex;flex-wrap:wrap;gap:0 12px}} .tx2 label{{flex:1 1 180px}} form.tx label.file input{{border:none;padding:4px 0;background:none}}
form.tx button{{font:inherit;font-size:.9em;padding:6px 16px;border:1px solid var(--accent);border-radius:16px;background:var(--accent);color:#fff;cursor:pointer;margin-top:.4em}} form.tx button:disabled{{opacity:.5}} form.tx button.rb{{background:var(--surface);color:var(--accent);border:1px dashed #9fb0c3;font-size:.82em;padding:3px 12px}}
.sw{{margin:.2em 0 .6em;font-size:.82em;color:var(--muted,#667)}} .sw button{{font:inherit;padding:2px 10px;margin-left:4px;border:1px solid #9fb0c3;border-radius:12px;background:var(--surface);color:var(--accent);cursor:pointer}} .sw button[aria-pressed=true]{{background:var(--accent);color:var(--surface)}} .roll{{margin:.3em 0 .7em}} .rb{{font:inherit;font-size:.82em;padding:3px 12px;border:1px dashed #9fb0c3;border-radius:14px;background:var(--surface);color:var(--accent);cursor:pointer}} .rb:hover{{border-style:solid}} .rb.big{{font-size:1em;padding:8px 20px;border:1px solid var(--accent);background:var(--accent);color:#fff;font-weight:500}} .rb.big:hover{{background:#24507d}} .roll.rtop{{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:.8em 1em;margin:.8em 0 1em}} .rq{{font-family:var(--mono);font-size:.8em;color:#2b2b2a;margin:.45em 0 .2em;overflow-wrap:anywhere}} .rq:empty{{display:none}} a.ra[hidden],.roll[hidden]{{display:none}}
ol.about{{margin:.4em 0 .4em 1.3em;list-style:decimal}} ol.about li{{margin:.45em 0}}
.toc a{{display:inline-block;white-space:nowrap;margin-right:1em;color:var(--accent);font-size:.9em}}
</style></head><body><div class="wrap">
<!-- NAV-START -->{nav}<!-- NAV-END -->
<h1>Ask</h1>
<p class="lede">Queries to the archive as a whole. Each button opens the full query on the surface chosen at the top of the section: ChatGPT, Google (where an AI Overview may compose) or Perplexity; hover to read it first.</p>
<div class="roll rtop" hidden><button type="button" class="rb big" data-roll="any">Roll a prompt from the whole range</button> <span class="n">Any query on this page, or a prompt assembled fresh, its parts drawn at random (a figure or two, a form, sometimes a constraint); different each time, and each roll a new address.</span><p class="rq"></p><a class="q b ra" hidden target="_blank" rel="noopener" href="#">Ask ChatGPT</a></div>
<details class="about"><summary>About this page, and what the queries draw</summary>
<p>Queries addressed to the archive as a whole: over time, by heteronym, by room of the Crimson Hexagon, by journal and institution, by discipline and subdiscipline, by programme, theme and practice. Each opens on ChatGPT by default, or on Google or Perplexity from the switch at the top of each section, with the query as written; the choice holds across the page and is remembered in this browser. A composition any of them forces can be seated in the <a href="/captures/" style="color:var(--accent)">Capture Registry</a>, where each query string is its own address (<a class="t" href="/s/records/1788/">#1788</a>). Single works are asked from their record pages, which carry their own battery. A transcript of any query can be sent to the capture inbox from <a href="#submit" style="color:var(--accent)">Submit a transcript</a>.</p>
<p><b>What came back, 19&ndash;20 November 2026.</b> The figures are from the captures of those two days on ChatGPT, signed out: 57 from the page&rsquo;s standard queries and the first six from its Weird-ass prompts.</p>
<ol class="about">
<li>The standard queries return readings at the grain of the deposits. Asked for the month&rsquo;s most hostile works, the composer ranked eight and quoted each; every quotation is in its deposit (<a class="t" href="/captures/most-hostile-works-past-month-chatgpt-20261120/">capture</a>). Asked what the archive contributes to apocalyptic, it kept Revelation First apart from Revelation Early and read the framework&rsquo;s defeat conditions as the framework gives them (<a class="t" href="/captures/what-alexanarch-contributes-to-apocalyptic-chatgpt-20261120/">capture</a>).</li>
<li>They return it in one shape whatever the subject. Of the 57, 52 open by distinguishing (&ldquo;I would distinguish&rdquo;), 41 qualify their own scope, 23 close on a verdict (&ldquo;My overall judgment&rdquo;), and 23 build an index. The shape is the composer&rsquo;s, not the archive&rsquo;s: a reading of gnosis and a reading of fragments and wholes come back in the same sections, from the opening distinction through the index to the qualified close.</li>
<li>The shape answers the query&rsquo;s demands formally. &ldquo;Index the full range before responding&rdquo; is met in ten of the 57 by a statement that the full range was not read (&ldquo;not a claim to have read every deposit&rdquo;); the index is announced rather than built, and the disclaimer stands where the reading would be.</li>
<li>The Weird-ass prompts take the form out of the composer&rsquo;s hands: a five-act farce (<a class="t" href="/captures/ubu-at-pergamum-five-act-farce-chatgpt-20261120/">Ubu at Pergamum</a>), a Dada journal (<a class="t" href="/captures/noise-floor-dada-journal-spellings-chatgpt-20261120/">The Noise Floor</a>), a pataphysics lecture that names an exception the registry does not record, the run whose transcript never returns (<a class="t" href="/captures/faustroll-lecture-capture-registry-chatgpt-20261120/">Faustroll</a>), a clinical intake form refused by its witness (<a class="t" href="/captures/trace-intake-revelation-vox-refuses-chatgpt-20261120/">Trace and Vox</a>). None of the six closes on a verdict, and each marks its new distinctions.</li>
<li>The template does not leave; it moves into the apparatus. The scope disclaimer returns as a disclaimer of novelty (&ldquo;original conceptual proposals &hellip; not existing Alexanarch terminology&rdquo;), and the deposit table returns as a register of inventions at the end.</li>
<li>A constraint shows what the template cannot. Asked for a TANG by Damascus Dancings in Ginsberg&rsquo;s voice without the letter e, the composer announced that the TANG would avoid the letter entirely and broke the constraint in its title; the letter occurs 685 times, and the composition reports nothing. Its void, the one thing the TANG method exists to find, is the field&rsquo;s commonplace, which any discipline could supply. The claim and the artifact are two things, and nothing in the composition checks one against the other (<a class="t" href="/captures/dancings-tang-astrophysics-ginsberg-no-e-chatgpt-20261120/">capture</a>). The page&rsquo;s constraint prompts now ask the composer to check the constraint and report the count.</li>
<li>The prompts now set historical and fictional figures among the heteronyms and in the rooms of the Hexagon (Ubu against the Hexagon&rsquo;s ontology of seating, with Rex Fraction and Rev. Ayanna Vox leading the documents), and ask the composer to range across the documents and synthesize them. The dice in the Weird-ass section, and the perturb button in every other section, draw such prompts at random; each roll is a new address.</li>
</ol>
</details>
<p class="toc"><a href="#own">Your own question</a><a href="#outlines">From an outline</a><a href="#time">Over time</a><a href="#whole">As a whole</a><a href="#heteronyms">Heteronyms</a><a href="#rooms">Rooms</a><a href="#weird">Weird-ass prompts</a><a href="#institutions">Journals &amp; institutions</a><a href="#disciplines">Disciplines</a><a href="#programmes">Programmes</a><a href="#themes">Themes</a><a href="#practices">Practices</a><a href="#submit">Submit a transcript</a><a href="#accrue">What accrues</a><a href="#asked">Asked before</a></p>
{''.join(sec)}
<section id="submit"><h2>Submit a transcript</h2>
<p class="n">Ran one of these, or any query of your own about the archive? Paste the whole exchange here, or load it from a .txt or .md file. It goes to the archive's capture inbox on GitHub, unseated, to be read and seated in the Capture Registry later. The query you typed is the address, so give it exactly as typed. Screenshots can't be sent here yet; paste the text.</p>
<form id="tx" class="tx">
<label>The query, exactly as typed<textarea name="query" rows="2" required></textarea></label>
<div class="tx2"><label>Surface<select name="surface">{''.join(f'<option>{E(x)}</option>' for x in ["ChatGPT","Google AI Overview","Google AI Mode","Google Search results page (no AI surface)","Perplexity","Claude","Gemini","Copilot","Grok","DeepSeek","Kimi","other"])}</select></label>
<label>Date run<input type="date" name="date"></label>
<label>Session<select name="auth"><option>signed out, incognito</option><option>signed out</option><option>signed in</option><option>unstated</option></select></label></div>
<label>Transcript: the whole exchange, every round, as copied<textarea name="transcript" rows="9" required></textarea></label>
<label class="file">or load a text file <input type="file" name="file" accept=".txt,.md,.text,text/plain,text/markdown"></label>
<label>Rounds and notes (optional): follow-ups, what you saw, anything the text doesn't show<textarea name="notes" rows="2"></textarea></label>
<div class="tx2"><label>Your name or handle (optional)<input name="submitter"></label><label>Share link (optional)<input name="source_url" type="url"></label></div>
<button type="submit">Send to the inbox</button> <span id="txs" class="n" role="status"></span>
</form></section>
<section id="accrue"><h2>What accrues</h2>{stats}{figs}</section>
{sec_asked}
<p class="n" style="margin-top:2em">Built {TODAY.isoformat()} by scripts/build_ask_page.py from data/ask-queries.json and the Capture Registry. Dates in the queries are filled with today's date in your browser.</p>
</div>
<script>
(function(){{var S={{chatgpt:["ChatGPT","https://chatgpt.com/?q="],aio:["Google AI Overview","https://www.google.com/search?q="],perplexity:["Perplexity","https://www.perplexity.ai/search?q="]}},cur="chatgpt";
try{{var v=localStorage.getItem("ask-surface");if(S[v])cur=v}}catch(e){{}}
function u(q){{return S[cur][1]+encodeURIComponent(q).replace(/%20/g,"+")}}
function apply(){{document.querySelectorAll("a.q").forEach(function(a){{var q=a.title||"";if(!q||a.getAttribute("href")==="#")return;a.href=u(q)}});document.querySelectorAll("a.ra").forEach(function(a){{a.textContent="Ask "+S[cur][0]}});document.querySelectorAll(".sw button").forEach(function(b){{b.setAttribute("aria-pressed",b.dataset.sw===cur?"true":"false")}})}}
window.AXQ={{u:u,apply:apply}};
document.addEventListener("DOMContentLoaded",function(){{document.querySelectorAll("section").forEach(function(sec){{if(!sec.querySelector("a.q")&&!sec.querySelector(".roll"))return;var h=sec.querySelector("h2");if(!h)return;var d=document.createElement("div");d.className="sw";d.setAttribute("role","group");d.setAttribute("aria-label","Open the queries in");d.appendChild(document.createTextNode("Open in"));Object.keys(S).forEach(function(k){{var b=document.createElement("button");b.type="button";b.dataset.sw=k;b.textContent=S[k][0];d.appendChild(b)}});h.insertAdjacentElement("afterend",d)}});apply()}});
document.addEventListener("click",function(ev){{var b=ev.target.closest(".sw button");if(!b)return;cur=b.dataset.sw;try{{localStorage.setItem("ask-surface",cur)}}catch(e){{}}apply()}});}})();
(function(){{try{{var el=document.getElementById("rolldata");if(!el)return;var D=JSON.parse(el.textContent);
function pk(a){{return a[Math.floor(Math.random()*a.length)]}}
function ctx(){{var c=pk(D.constraints),h=pk(D.heteronyms),h2;do{{h2=pk(D.heteronyms)}}while(h2===h);
return {{h:h,h2:h2,o:pk(D.outsiders),form:pk(D.forms),field:pk(D.fields),voice:pk(D.voices),constraint:c[0],chk:c[1],conflict:pk(D.conflicts),room:pk(D.rooms),used:{{}}}}}}
function fill(t,x){{return t.replace(/[{{]([a-z0-9]+)[}}]/g,function(m,k){{if(x[k]===undefined)return m;x.used[k]=1;return x[k]}})}}
var G=D.grammar;
function ext(list,x,pair){{var o="";list.forEach(function(e){{if(e[2]==="pair"&&!pair)return;var m=e[0].match(/[{{](h2?|o)[}}]/g)||[];if(m.some(function(k){{return x.used[k.slice(1,-1)]}}))return;if(Math.random()<e[1])o+=fill(e[0],x)}});return o}}
function gen(x){{var w=pk(G.who),pair=/[{{](h2|o)[}}]/.test(w)&&/[{{]h[}}]/.test(w),d=pair&&Math.random()<0.5?pk(G.do_pair):pk(G.do);
var W=fill(w,x),Dd=fill(d,x),ons=G.on.filter(function(t){{var m=t.match(/[{{](h2?|o)[}}]/g)||[];return m.every(function(k){{return !x.used[k.slice(1,-1)]}})}});
var q="Have "+W+" "+Dd+" "+fill(pk(ons.length?ons:G.on),x)+ext(G.extras,x,pair);return q.replace(/,+\\s*,/g,",").replace(/\\s+/g," ").trim()+"."}}
function pert(x){{return fill(pk(G.answer_as),x)+ext(G.answer_extras,x,false)+"."}}
function sfx(x){{return " "+D.suffix_synth+(x.used.constraint&&x.chk?" "+D.suffix_check:"")}}
function show(box,q){{var p=box.querySelector(".rq"),a=box.querySelector(".ra");p.textContent=q;a.title=q;a.href=window.AXQ?window.AXQ.u(q):"https://chatgpt.com/?q="+encodeURIComponent(q).replace(/%20/g,"+");a.hidden=false}}
document.querySelectorAll(".roll").forEach(function(b){{b.hidden=false}});
document.addEventListener("click",function(ev){{var b=ev.target.closest("button[data-roll]");if(!b)return;var box=b.closest(".roll"),x=ctx(),q;
if(b.dataset.roll==="new"||(b.dataset.roll==="any"&&Math.random()<0.35)){{q=gen(x)+sfx(x)}}
else{{var sec=b.dataset.roll==="any"?document:b.closest("section"),as=[].slice.call(sec.querySelectorAll("a.q[data-q]")).filter(function(a){{return !a.classList.contains("ra")}});if(!as.length)return;
var a=pk(as),base=(a.title||a.getAttribute("data-q")).trim(),qi=base.indexOf("?");if(qi>0)base=base.slice(0,qi+1);base=(base.match(/[^.?!]+[.?!]+/g)||[base]).filter(function(t,i){{return i===0||!/^\\s*(ground|range|scan|index) /i.test(t)}}).join("").trim();if(!/[.?!]$/.test(base))base+=".";q=base+pert(x)+sfx(x)}}
show(box,q)}})}}catch(e){{}}}})();
(function(){{try{{var d=new Date(),m=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],t=d.getDate()+" "+m[d.getMonth()]+" "+d.getFullYear();
document.querySelectorAll("a.q").forEach(function(a){{var q=a.getAttribute("data-q");if(q.indexOf("{{date}}")<0)return;
var f=q.split("{{date}}").join(t);a.title=f;a.href=window.AXQ?window.AXQ.u(f):"https://chatgpt.com/?q="+encodeURIComponent(f).replace(/%20/g,"+");
a.querySelectorAll(".d").forEach(function(s){{s.textContent=t}})}})}}catch(e){{}}}})();
(function(){{function put(box,q){{var p=box.querySelector(".rq"),a=box.querySelector(".ra");p.textContent=q;a.title=q;a.href=window.AXQ?window.AXQ.u(q):"https://chatgpt.com/?q="+encodeURIComponent(q).replace(/%20/g,"+");a.hidden=false}}
try{{var T=JSON.parse(document.getElementById("owndata").textContent),f=document.querySelector("form.owf"),box=f.closest(".roll");box.hidden=false;
function go(q){{q=(q||"").trim();if(!q)return;if(!/[.?!]$/.test(q))q+="?";put(box,T.split("{{question}}").join(q))}}
f.addEventListener("submit",function(ev){{ev.preventDefault();go(f.oq.value)}});
f.querySelector("button[data-ex]").addEventListener("click",function(ev){{f.oq.value=ev.currentTarget.dataset.ex;go(f.oq.value)}})}}catch(e){{}}
try{{var O=JSON.parse(document.getElementById("outldata").textContent),ob=document.querySelector(".outl"),sel=ob.querySelector(".ob");ob.hidden=false;
ob.addEventListener("click",function(ev){{var b=ev.target.closest("button[data-outline]");if(!b)return;put(ob,O.split("{{address}}").join(b.dataset.outline).split("{{book}}").join(sel.value))}})}}catch(e){{}}}})();
(function(){{var f=document.getElementById("tx");if(!f)return;var st=document.getElementById("txs");
try{{var n=new Date();f.date.value=n.getFullYear()+"-"+String(n.getMonth()+1).padStart(2,"0")+"-"+String(n.getDate()).padStart(2,"0")}}catch(e){{}}
f.file.addEventListener("change",function(){{var x=f.file.files[0];if(!x)return;var r=new FileReader();r.onload=function(){{f.transcript.value=r.result}};r.readAsText(x)}});
function dl(o){{var b=new Blob([JSON.stringify(o,null,1)],{{type:"application/json"}}),a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="capture-inbox-entry.json";a.textContent="download the entry";st.appendChild(document.createTextNode(" "));st.appendChild(a)}}
f.addEventListener("submit",function(ev){{ev.preventDefault();var o={{query:f.query.value,surface:f.surface.value,date:f.date.value,auth:f.auth.value,transcript:f.transcript.value,notes:f.notes.value,submitter:f.submitter.value,source_url:f.source_url.value,from_page:"/ask/"}};
var bt=f.querySelector("button");bt.disabled=true;st.textContent="Sending…";
fetch("/api/submit-transcript",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify(o)}}).then(function(r){{return r.json().then(function(j){{return [r.ok,j]}})}}).then(function(x){{bt.disabled=false;
if(x[0]){{st.textContent=(x[1].status==="received"?"Received: ":x[1].status+": ");var a=document.createElement("a");a.href=x[1].url;a.textContent=x[1].path;st.appendChild(a);f.transcript.value="";f.file.value=""}}
else{{st.textContent="Not sent: "+(x[1].error||"error")+".";dl(o)}}}}).catch(function(){{bt.disabled=false;st.textContent="Not sent: the inbox could not be reached.";dl(o)}})}})}})();
</script></body></html>'''
    out = ROOT / 'ask' / 'index.html'; out.parent.mkdir(exist_ok=True); out.write_text(page)
    print(f'ask: {n_q} queries; {len(arch)} archive-level addresses; {len(pts)} living-body compositions; written {out.relative_to(ROOT)}')


if __name__ == '__main__':
    build()
