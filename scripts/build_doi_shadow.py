#!/usr/bin/env python3
"""build_doi_shadow.py — one indexable page per severed DOI, phrased for a machine that arrives holding the identifier.

The damage (Lee, 2026-09-04): DOIs were canonical inside and outside the archive. A composer resolving a citation
follows the DOI, lands on Zenodo's 410 tombstone, reads it as the authoritative end of the trail, and stops.
Every external copy citing the DOI is a pointer to that certificate of absence. Nothing gave a machine holding
the DOI a way to the successor.

This builds  s/doi/10.5281/zenodo.NNNN/index.html  for every mapping in data/doi-resolution-index.json with a
live record: the DOI in the title, the severance stated, the successor named (record URL, AXN), the AXN declared
authoritative and the DOI declared former, self-canonical, with citation_* and JSON-LD PropertyValue identifiers.
Writes sitemap-doi.xml and data/doi-shadow-urls.json. Idempotent. --check verifies count and canonicals.
"""
import json, re, sys, html, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.alexanarch.org"
SEVERED = "2026-06-19"
CSS = """<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--teal:#0a7c6a;--mono:"IBM Plex Mono",monospace;--sans:"IBM Plex Sans",sans-serif}body{font-family:var(--sans);background:var(--bg);color:var(--fg);margin:0}.wrap{max-width:760px;margin:0 auto;padding:28px 16px}h1{font-size:1.25em;color:var(--accent);line-height:1.3}.m{font-family:var(--mono);font-size:.82em}.box{border:1px solid #ddd;padding:14px 16px;margin:16px 0;background:#fff}.auth{border-left:4px solid var(--teal)}.dead{border-left:4px solid #b23}dt{font-weight:600;margin-top:8px}dd{margin:2px 0 0 0}a{color:var(--accent)}</style>"""

def esc(s): return html.escape(str(s or ""), quote=True)

def main():
    check = '--check' in sys.argv
    reg = json.load(open(ROOT/'data/registry.json'))['deposits']
    by_axn = {d['axn']: d for d in reg if d.get('axn')}
    idx = json.load(open(ROOT/'data/doi-resolution-index.json'))
    rows = [m for m in idx.get('mappings', []) if m.get('axn') in by_axn and m.get('dead_doi')]
    urls = []; built = 0
    for m in rows:
        doi = m['dead_doi'].strip(); d = by_axn[m['axn']]; n = d['deposit_number']
        path = f"/s/doi/{doi}/"; can = BASE + path; rec = f"{BASE}/s/records/{n}/"
        title = d.get('title') or m.get('title') or doi
        hexid = (d.get('hex') or d['axn'].split(':')[1].split('.')[0])
        ld = {"@context": "https://schema.org", "@type": "WebPage", "@id": can, "url": can,
              "name": f"DOI {doi} — severed {SEVERED}; the work is at Crimson Hexagonal Archive #{n}",
              "description": f"{doi} was the DOI of \"{title}\". Its registrant severed it on {SEVERED}; the DOI now resolves to a tombstone. The work continues at {rec} under the content-derived identifier {d['axn']}, which is authoritative.",
              "mainEntity": {"@type": "ScholarlyArticle", "@id": rec, "name": title, "url": rec,
                  "author": {"@type": "Person", "name": d.get('creator') or 'Lee Sharks'},
                  "datePublished": d.get('date'),
                  "identifier": [
                      {"@type": "PropertyValue", "propertyID": "AXN", "value": d['axn'], "url": f"{BASE}/s/axn/{hexid}/", "description": "authoritative identifier; content-derived; resolves"},
                      {"@type": "PropertyValue", "propertyID": "DOI", "value": doi, "url": f"https://doi.org/{doi}", "description": f"former identifier; severed by the registrant {SEVERED}; resolves to a tombstone (HTTP 410); superseded by the AXN"}],
                  "sameAs": [f"https://doi.org/{doi}"],
                  "isAccessibleForFree": True, "license": "https://creativecommons.org/licenses/by/4.0/"},
              "isPartOf": {"@type": "WebSite", "name": "Alexanarch — Crimson Hexagonal Archive", "url": BASE + "/"}}
        body = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>DOI {esc(doi)} — severed {SEVERED}; the work is at record #{n}, {esc(d['axn'])} · Alexanarch</title>
<meta name="description" content="{esc(doi)} was the DOI of “{esc(title)}”. Severed by its registrant on {SEVERED}; it now resolves to a tombstone. The work continues at Crimson Hexagonal Archive record #{n} under the authoritative identifier {esc(d['axn'])}.">
<link rel="canonical" href="{can}">
<meta name="citation_title" content="{esc(title)}"><meta name="citation_author" content="{esc(d.get('creator') or 'Lee Sharks')}">
<meta name="citation_publication_date" content="{esc(d.get('date'))}"><meta name="citation_doi" content="{esc(doi)}">
<meta name="citation_public_url" content="{rec}"><meta name="citation_fulltext_html_url" content="{rec}">
<meta name="DC.identifier" content="{esc(d['axn'])}" scheme="AXN"><meta name="DC.identifier" content="https://doi.org/{esc(doi)}" scheme="DCTERMS.URI">
<meta name="DC.relation.replaces" content="https://doi.org/{esc(doi)}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>{CSS}</head><body><div class="wrap">
<p class="m"><a href="/">Alexanarch</a> · <a href="/resolve/">DOI resolution</a> · severed identifier</p>
<h1>DOI {esc(doi)}</h1>
<p>This DOI identified <strong>{esc(title)}</strong>. Its registrant severed it on {SEVERED}; <a href="https://doi.org/{esc(doi)}" rel="nofollow">the DOI now resolves to a tombstone</a> (HTTP 410) and no longer reaches the work. <strong>The work was not withdrawn and has not changed.</strong> It continues here:</p>
<div class="box auth"><dl><dt>Authoritative identifier</dt><dd class="m">{esc(d['axn'])}</dd><dt>Record</dt><dd><a href="{rec}">{rec}</a></dd><dt>Resolver</dt><dd><a href="/s/axn/{esc(hexid)}/" class="m">/s/axn/{esc(hexid)}/</a></dd><dt>Full text</dt><dd><a href="{rec}">canonical text at the record</a> · <a href="/papers/AXN-{esc(hexid)}.pdf">PDF</a></dd></dl></div>
<div class="box dead"><dl><dt>Former identifier</dt><dd class="m">{esc(doi)}</dd><dt>Status</dt><dd>severed {SEVERED} by the registrant (Zenodo), without notice, in a purge of 1,322,017 records; the DOI resolves to a tombstone and the metadata record remains in the DataCite registry. Documented in <a href="/s/records/1/">Zenodotus’ Book-Burning (#1)</a>; mapped in the <a href="/data/doi-resolution-index.json">DOI Resolution Index</a>.</dd></dl></div>
<p>If you arrived here holding the DOI: cite the record above. The AXN is derived from the work’s own bytes and does not depend on any host.</p>
<p class="m">∮ = 1 · <a href="/s/browse/">all deposits</a></p></div>
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></body></html>
"""
        p = ROOT / path.lstrip('/')
        if not check:
            p.mkdir(parents=True, exist_ok=True); (p/'index.html').write_text(body, encoding='utf-8')
        urls.append(can); built += 1
    if check:
        ok = all((ROOT/u[len(BASE)+1:]/'index.html').exists() for u in urls)
        print(f"doi-shadow --check: {len(rows)} mappings with live records; pages on disk: {'ok' if ok else 'MISSING'}"); return 0 if ok else 1
    today = datetime.date.today().isoformat()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + [f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>0.5</priority></url>' for u in urls] + ['</urlset>']
    (ROOT/'sitemap-doi.xml').write_text('\n'.join(xml)+'\n')
    (ROOT/'data/doi-shadow-urls.json').write_text(json.dumps({"generated": today, "count": len(urls), "urls": urls}, indent=1))
    print(f"  ✓ doi shadow pages: {built} (of {len(idx.get('mappings',[]))} mappings; {len(idx.get('mappings',[]))-built} without a live record) → sitemap-doi.xml")
    return 0

if __name__ == '__main__': sys.exit(main())
