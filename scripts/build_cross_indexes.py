#!/usr/bin/env python3
"""build_cross_indexes.py — the archive's catalogue indexes: rooms of the Crimson Hexagon, and the captures by facet.

WHY (2026-10-16). Lee Sharks: "what i need at this point is many nesting indexing pages that point elsewhere -
indexing pages of all captures, of rooms in the hexagon, etc". The 670 capture pages are listed in
sitemap-captures.xml but linked only from /captures/, one 12.8 MB page; no alexanarch page listed the rooms of the
Crimson Hexagon or which records each room seats. Google's own guidance allows a browsable hierarchy of categories;
its doorway and link-spam policies name near-identical pages aimed at query variants and link lists that add nothing.
So every row here carries what the destination is — the capture's date, surface, exact issued query, headline and
first finding; the record's date, type and identifier — and every index is a different cut of the same holdings.

Writes (all self-canonical, server-rendered, plain links):
  /s/rooms/                          every room with its physics, description and prompt, and the records it seats
  /captures/by/                      the three facets with counts
  /captures/by/section/<slug>/       captures in one registry section
  /captures/by/surface/<slug>/       captures on one surface family (the recorded surface string shown per row)
  /captures/by/month/<YYYY-MM>/      captures dated in one month
and data/cross-index-urls.json, which regenerate_surfaces.py adds to sitemap.xml.

    python3 scripts/build_cross_indexes.py            (after build_hexagon_seats.py and any capture seat)
"""
import collections, html, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.render_navbar import render_navbar
A = 'https://www.alexanarch.org'
esc = lambda s: html.escape(str(s if s is not None else ''), quote=True)

CSS = ('@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");'
       ':root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--teal:#0a7c6a;--border:#e0e0e0;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}'
       'body{font-family:var(--sans);background:var(--bg);color:var(--fg);margin:0}.wrap{max-width:860px;margin:0 auto;padding:24px 16px}'
       'h1{font-size:1.35em;color:var(--accent);margin:12px 0 4px}h2{font-size:1.08em;color:var(--accent);margin:26px 0 4px}'
       '.sub{color:#555;font-size:.88em;margin-bottom:18px;line-height:1.55}.rec{padding:9px 0;border-bottom:1px solid #eee;overflow-wrap:anywhere}'
       '.rec a.t{font-weight:500;color:var(--accent);text-decoration:none;font-size:.95em}.rec .m{font-family:var(--mono);font-size:.72em;color:var(--teal)}'
       '.rec .d{font-size:.84em;color:#444;margin-top:3px}.room{font-size:.86em;color:#444;line-height:1.55}.room b{color:var(--fg)}'
       '.idx a{color:var(--accent)}.idx{font-size:.88em;line-height:1.9}.crumbs{font-size:.8em;color:#777;margin-bottom:8px}.crumbs a{color:var(--teal)}'
       '.q{font-family:var(--mono);font-size:.84em}')


def page(path, title, desc, crumbs, body, n):
    url = f'{A}{path}'
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": url, "description": desc,
          "isPartOf": {"@type": "WebSite", "name": "Alexanarch", "url": f"{A}/"}, "numberOfItems": n}
    cr = ' / '.join(f'<a href="{h}">{esc(t)}</a>' if h else esc(t) for t, h in crumbs)
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">'
            f'<title>{esc(title)} — Alexanarch</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script><style>{CSS}</style></head><body><div class="wrap">'
            f'{render_navbar(path)}<div class="crumbs">{cr}</div>{body}</div></body></html>\n')


def write(path, s):
    p = ROOT / path.strip('/') / 'index.html'; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding='utf-8')


def rooms_index(reg):
    S = json.load(open(ROOT / 'data/hexagon-seats.json')); D = {d['deposit_number']: d for d in reg['deposits']}
    by = collections.defaultdict(list)
    for n, e in S['seats'].items():
        for r in e['rooms']:
            by[r].append((int(n), e))
    key = lambda r: (r['locus'][0] != 'R', [int(x) if x.isdigit() else x for x in re.findall(r'\d+|\D+', r['locus'])])
    rooms = sorted((S['rooms'][r] for r in by), key=key)
    asg = collections.Counter(e.get('assignment') or 'unrecorded' for e in S['seats'].values())
    toc = ' · '.join(f'<a href="#{esc(r["id"])}">{esc(r["locus"])} {esc(r["name"])}</a> ({len(by[r["id"]])})' for r in rooms)
    parts = [f'<h1>Rooms of the Crimson Hexagon — and the records each room seats</h1>'
             f'<div class="sub">The Crimson Hexagon (Lee Sharks) is organised as rooms at <a href="https://www.crimsonhexagonal.org/rooms">crimsonhexagonal.org</a>; '
             f'the works it seats are records of this archive. {len(S["seats"])} records are seated in {len(rooms)} rooms '
             f'(a record may sit in more than one). Seats as recorded in the interface\'s hexagon_canonical.json — assignment: '
             + ', '.join(f'{v} {k}' for k, v in asg.most_common()) + '. A record with its own page on crimsonhexagonal.org links to it as "work page".</div>'
             f'<div class="idx">{toc}</div>']
    for r in rooms:
        rows = sorted(by[r['id']], key=lambda t: (D[t[0]].get('date') or '', t[0]), reverse=True)
        parts.append(f'<h2 id="{esc(r["id"])}">{esc(r["locus"])} {esc(r["name"])} — {len(rows)} records</h2>'
                     f'<div class="room">' + (f'<b>Physics</b> {esc(r["physics"])}. ' if r.get('physics') else '')
                     + (f'{esc(r["desc"])} ' if r.get('desc') else '') + (f'<b>Prompt</b> <i>{esc(r["prompt"])}</i> ' if r.get('prompt') else '')
                     + f'· <a href="{esc(r["url"])}">the room at crimsonhexagonal.org</a></div>')
        for n, e in rows:
            d = D[n]; others = [S['rooms'][x] for x in e['rooms'] if x != r['id']]
            parts.append(f'<div class="rec"><a class="t" href="/s/records/{n}/">{esc(d["title"])}</a>'
                         f'<div class="m">#{n} · {esc(d.get("date"))} · {esc(d.get("content_type") or "")} · {esc(d["axn"])}</div>'
                         + (f'<div class="d">' + (f'<a href="{esc(e["works_url"])}">work page</a>' if e.get('works_url') else '')
                            + ((' · ' if e.get('works_url') else '') + 'also in ' + ', '.join(f'<a href="{esc(o["url"])}">{esc(o["locus"])} {esc(o["name"])}</a>' for o in others) if others else '')
                            + '</div>' if (e.get('works_url') or others) else '') + '</div>')
    desc = (f'The rooms of the Crimson Hexagon, the distributed epic by Lee Sharks, and the {len(S["seats"])} archive records seated in them: '
            'each room\'s physics and prompt, each record\'s date, type and identifier.')
    write('/s/rooms/', page('/s/rooms/', 'Rooms of the Crimson Hexagon — records by room', desc,
                            [('Alexanarch', '/'), ('Browse', '/s/browse/'), ('Rooms of the Crimson Hexagon', None)], ''.join(parts), len(S['seats'])))
    return ['/s/rooms/']


def slug(s):
    s = s.replace('&', 'and').replace('∮ = 1', 'oint-equals-1')
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


SURF = [('google-ai-overview', 'Google AI Overview', r'^Google AI Overview'), ('google-ai-mode', 'Google AI Mode', r'^Google AI Mode'),
        ('google-other', 'Google (Knowledge panel, Gemini)', r'^Google'), ('chatgpt', 'ChatGPT', r'ChatGPT'),
        ('grok', 'Grok', r'^Grok'), ('bing-copilot', 'Bing Copilot', r'^Bing'), ('perplexity', 'Perplexity', r'^Perplexity'),
        ('claude', 'Claude', r'^Claude'), ('qwen', 'Qwen', r'^Qwen'), ('surface-not-recorded', 'Surface not recorded', r'^(UNDETERMINED|UNRESOLVED)$')]


def surface_family(s):
    for k, name, pat in SURF:
        if re.search(pat, s or ''):
            return k, name
    return 'other', 'Other surfaces'


def capture_indexes():
    j = json.load(open(ROOT / 'data/EA-WG-CAPTURES-01.json')); E = j['entries']
    def row(e):
        f = (e.get('findings') or [''])[0]
        n = e.get('n_observations') or 1
        return (f'<div class="rec"><a class="t" href="/captures/{esc(e["slug"])}/">{esc(e.get("mt") or e["slug"])}</a>'
                f'<div class="m">{esc(e.get("date"))} · {esc(e.get("surface"))} · {esc(e.get("s"))}' + (f' · {n} observations' if n > 1 else '') + '</div>'
                f'<div class="d"><span class="q">«{esc(e.get("q"))}»</span>' + (f' — {esc(f)}' if f else '') + '</div></div>')
    facets = {'section': collections.defaultdict(list), 'surface': collections.defaultdict(list), 'month': collections.defaultdict(list)}
    names = {'section': {}, 'surface': {}, 'month': {}}
    for e in E:
        s = e.get('s') or 'Unsectioned'; k = slug(s); facets['section'][k].append(e); names['section'][k] = s
        k, nm = surface_family(e.get('surface')); facets['surface'][k].append(e); names['surface'][k] = nm
        m = (e.get('date') or '')[:7] or 'undated'; facets['month'][m].append(e); names['month'][m] = m
    label = {'section': 'section', 'surface': 'surface', 'month': 'month'}
    urls = ['/captures/by/']
    root = [f'<h1>Captures by section, surface and month</h1><div class="sub">{len(E)} captures of machine composition — AI search '
            'overviews and chat answers composing from the Crimson Hexagonal Archive — each with its issued query, surface, date and '
            'findings. The full registry is the <a href="/captures/">Capture Registry</a> (EA-WG-CAPTURES-01); these pages are three cuts of it.</div>']
    for f, groups in facets.items():
        order = sorted(groups, reverse=(f == 'month')) if f == 'month' else sorted(groups, key=lambda k: -len(groups[k]))
        root.append(f'<h2>By {label[f]}</h2><div class="idx">' + ' · '.join(
            f'<a href="/captures/by/{f}/{k}/">{esc(names[f][k])}</a> ({len(groups[k])})' for k in order) + '</div>')
        for k in order:
            es = sorted(groups[k], key=lambda e: (e.get('date') or '', e['slug']), reverse=True)
            dates = [e.get('date') for e in es if e.get('date')]
            span = f'{min(dates)} to {max(dates)}' if dates else 'undated'
            surf = collections.Counter(surface_family(e.get('surface'))[1] for e in es).most_common(3)
            sec = collections.Counter(e.get('s') for e in es).most_common(3)
            sub = (f'{len(es)} captures, {span}. ' + ('Surfaces: ' + ', '.join(f'{a} {b}' for a, b in surf) + '. ' if f != 'surface' else '')
                   + ('Sections: ' + ', '.join(f'{a} {b}' for a, b in sec) + '.' if f != 'section' else ''))
            title = f'Captures — {names[f][k]} ({label[f]})'
            body = (f'<h1>{esc(title)}</h1><div class="sub">{esc(sub)} Each row: the capture\'s headline, its date, surface and section, the '
                    'issued query exactly as typed, and its first finding.</div>' + ''.join(row(e) for e in es))
            path = f'/captures/by/{f}/{k}/'
            write(path, page(path, title, f'{len(es)} AI search captures composing from the Crimson Hexagonal Archive — {names[f][k]}: '
                             f'issued queries, surfaces, dates and findings, {span}.',
                             [('Alexanarch', '/'), ('Captures', '/captures/'), ('By section, surface, month', '/captures/by/'), (names[f][k], None)],
                             body, len(es)))
            urls.append(path)
    write('/captures/by/', page('/captures/by/', 'Captures by section, surface and month',
                                f'{len(E)} captures of AI search compositions from the Crimson Hexagonal Archive, indexed by section, surface and month.',
                                [('Alexanarch', '/'), ('Captures', '/captures/'), ('By section, surface, month', None)], ''.join(root), len(E)))
    return urls


def main():
    reg = json.load(open(ROOT / 'data/registry.json'))
    urls = rooms_index(reg) + capture_indexes()
    (ROOT / 'data/cross-index-urls.json').write_text(json.dumps({'urls': urls}, indent=1) + '\n', encoding='utf-8')
    print(f'{len(urls)} index pages written')


if __name__ == '__main__':
    main()
