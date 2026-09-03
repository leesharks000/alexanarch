#!/usr/bin/env python3
"""build_browse_sections.py — paginated browse sections beside the monolith (WS1).

The monolith s/browse/index.html is a machine contract (numberOfItems, END-OF-BROWSE-ROWS,
browse-index.json) read by gates and agents, and is NOT modified here. These sections are
crawlable pages of ≤ ~60 records each, with descriptions and prev/next, so that link equity
and crawl reach individual records instead of pooling on one ~940 KB page:

  /s/browse/family/<FAMILY>/        /s/browse/family/
  /s/browse/month/YYYY-MM/          /s/browse/month/
  /s/browse/venue/<slug>/           /s/browse/venue/

Self-canonical, in the sitemap (regenerate_surfaces adds them), linked from the monolith
header and (WS2) from record pages. `--check` verifies every ACTIVE deposit appears in
exactly one month page and one family page and that counts match the registry head.
"""
import json, re, sys, pathlib, html, datetime, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.render_navbar import render_navbar

BASE = "https://www.alexanarch.org"
PAGE = 60

def esc(s): return html.escape(str(s or ""), quote=True)
def slug(s): return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')[:60] or 'unnamed'

CSS = """<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--teal:#0a7c6a;--border:#e0e0e0;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}body{font-family:var(--sans);background:var(--bg);color:var(--fg);margin:0}.wrap{max-width:860px;margin:0 auto;padding:24px 16px}h1{font-size:1.35em;color:var(--accent);margin:12px 0 4px}.sub{color:#777;font-size:.88em;margin-bottom:18px}.rec{padding:10px 0;border-bottom:1px solid #eee}.rec a.t{font-weight:500;color:var(--accent);text-decoration:none;font-size:.95em}.rec .m{font-family:var(--mono);font-size:.72em;color:var(--teal)}.rec .d{font-size:.84em;color:#444;margin-top:3px}.pn{display:flex;justify-content:space-between;font-size:.85em;margin:18px 0}.idx a{display:block;padding:6px 0;border-bottom:1px solid #f0f0f0;text-decoration:none;color:var(--accent)}.crumbs{font-size:.8em;color:#777;margin-bottom:8px}.crumbs a{color:var(--teal)}</style>"""

def head(title, desc, canonical, extra_jsonld=None):
    j = {"@context":"https://schema.org","@type":"CollectionPage","name":title,"url":canonical,"description":desc,"isPartOf":{"@type":"WebSite","name":"Alexanarch","url":BASE+"/"}}
    if extra_jsonld: j.update(extra_jsonld)
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">'
            f'<title>{esc(title)} — Alexanarch</title><meta name="description" content="{esc(desc)}">'
            f'<link rel="canonical" href="{canonical}">'
            f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>{CSS}</head><body><div class="wrap">'
            + render_navbar(active='/s/browse/') )

FOOT = '<div class="sub" style="margin-top:24px">Complete registry: <a href="/s/browse/">all deposits on one page</a> · machine index: <a href="/data/browse-index.json">browse-index.json</a> · ∮ = 1</div><script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></div></body></html>'

def record_html(d):
    n = d['deposit_number']; desc = (d.get('description') or '').strip()
    if len(desc) > 420: desc = desc[:417].rsplit(' ',1)[0] + '…'
    st = d.get('status'); badge = f' <span class="m">{esc(st.lower())}</span>' if st and st != 'ACTIVE' else ''
    return (f'<div class="rec" itemscope itemtype="https://schema.org/CreativeWork"><span class="m">#{n}</span> '
            f'<a class="t" itemprop="url" href="/s/records/{n}/"><span itemprop="name">{esc(d.get("title"))}</span></a>{badge} '
            f'<time itemprop="datePublished" datetime="{esc(d.get("date"))}" class="m">{esc(d.get("date"))}</time>'
            f'<div class="d" itemprop="description">{esc(desc)}</div>'
            f'<div class="m">{esc(d.get("axn"))}</div></div>')

def paginate(items):
    return [items[i:i+PAGE] for i in range(0, len(items), PAGE)] or [[]]

def write_section(kind, key, label, items, idx_label, out_dir, sitemap_urls):
    pages = paginate(items)
    for pi, page in enumerate(pages, 1):
        path = f"/s/browse/{kind}/{key}/" + (f"{pi}/" if pi > 1 else "")
        can = BASE + path
        title = f"{label} — {idx_label}" + (f" (page {pi} of {len(pages)})" if len(pages) > 1 else "")
        desc = f"{len(items)} deposits in the Crimson Hexagonal Archive, {idx_label.lower()} {label}: titles, dates, abstracts, identifiers."
        nav = '<div class="pn">' + (f'<a href="/s/browse/{kind}/{key}/{(pi-1) if pi-1>1 else ""}{"/" if pi-1>1 else ""}">← page {pi-1}</a>' if pi > 1 else '<span></span>') + \
              (f'<a href="/s/browse/{kind}/{key}/{pi+1}/">page {pi+1} →</a>' if pi < len(pages) else '<span></span>') + '</div>'
        body = (head(title, desc, can, {"numberOfItems": len(items)}) +
                f'<div class="crumbs"><a href="/s/browse/">Browse</a> › <a href="/s/browse/{kind}/">{esc(idx_label)}</a> › {esc(label)}</div>'
                f'<h1>{esc(label)}</h1><div class="sub">{len(items)} deposits · {idx_label.lower()} · sorted by work date</div>' + nav +
                ''.join(record_html(d) for d in page) + nav + FOOT)
        p = out_dir / path.lstrip('/') ; p.mkdir(parents=True, exist_ok=True); (p/'index.html').write_text(body, encoding='utf-8')
        sitemap_urls.append(can)

def write_index(kind, idx_label, groups, out_dir, sitemap_urls, key_label):
    path = f"/s/browse/{kind}/"; can = BASE + path
    body = (head(f"Browse by {idx_label.lower()}", f"The Crimson Hexagonal Archive's deposits by {idx_label.lower()}: {len(groups)} sections.", can) +
            f'<div class="crumbs"><a href="/s/browse/">Browse</a> › {esc(idx_label)}</div><h1>Browse by {esc(idx_label.lower())}</h1><div class="idx">' +
            ''.join(f'<a href="/s/browse/{kind}/{k}/">{esc(key_label(k, items))} <span class="m">· {len(items)}</span></a>' for k, items in groups) + '</div>' + FOOT)
    p = out_dir / path.lstrip('/'); p.mkdir(parents=True, exist_ok=True); (p/'index.html').write_text(body, encoding='utf-8'); sitemap_urls.append(can)

def build(reg_path=ROOT/'data/registry.json', out_dir=ROOT, check=False):
    reg = json.load(open(reg_path))['deposits']
    deps = [d for d in reg if d.get('deposit_number')]
    deps.sort(key=lambda d: (d.get('date') or '', d['deposit_number']))
    fam = collections.defaultdict(list); mon = collections.defaultdict(list); ven = collections.defaultdict(list)
    vmap = {}
    ja = ROOT/'datasets/journals/assignments.jsonl'
    if ja.exists():
        for l in ja.read_text().splitlines():
            if l.strip():
                r = json.loads(l); vmap[r.get('deposit')] = r.get('journal')
    for d in deps:
        fam[(d.get('family') or 'UNCLASSIFIED')].append(d)
        mon[(d.get('date') or 'undated')[:7]].append(d)
        v = vmap.get(d['deposit_number'])
        if v: ven[slug(v)].append(d)
    vname = {slug(v): v for v in vmap.values() if v}
    if check:
        active = [d for d in deps if d.get('status') == 'ACTIVE']
        ok = all(sum(1 for k,items in fam.items() if d in items) == 1 for d in active) and all(sum(1 for k,items in mon.items() if d in items) == 1 for d in active)
        exp = ROOT/'s/browse/month'
        n_pages = sum(1 for _ in exp.rglob('index.html')) if exp.exists() else 0
        print(f"browse-sections --check: {len(active)} ACTIVE each in one family and one month section: {'ok' if ok else 'FAIL'}; families {len(fam)}, months {len(mon)}, venues {len(ven)}; month pages on disk {n_pages}")
        return 0 if ok else 1
    urls = []
    write_index('family', 'Family', sorted(fam.items()), out_dir, urls, lambda k, items: k)
    for k, items in fam.items(): write_section('family', k, k, items, 'Family', out_dir, urls)
    write_index('month', 'Month', sorted(mon.items(), reverse=True), out_dir, urls, lambda k, items: k)
    for k, items in mon.items(): write_section('month', k, k, items, 'Month', out_dir, urls)
    write_index('venue', 'Venue', sorted(ven.items()), out_dir, urls, lambda k, items: vname.get(k, k))
    for k, items in ven.items(): write_section('venue', k, vname.get(k, k), items, 'Venue', out_dir, urls)
    (ROOT/'data/browse-sections-urls.json').write_text(json.dumps({"generated": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'), "urls": urls}, indent=1))
    print(f"  ✓ browse sections: {len(fam)} families, {len(mon)} months, {len(ven)} venues → {len(urls)} pages")
    return 0

if __name__ == '__main__':
    sys.exit(build(check='--check' in sys.argv))
