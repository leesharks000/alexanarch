#!/usr/bin/env python3
"""generate_axn_resolver.py — regenerate the AXN resolution layer from data/registry.json.

Writes: s/axn/<HEX>/index.html for every hex (disambiguation page for any hex
assigned to multiple deposits — resolver policy: never silently select),
api/axn-index.json (machine map), sitemap-axn.xml. Idempotent; called by
regenerate_surfaces.py so every mint refreshes resolution automatically.
"""
import json, os, html
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def main():
    r = json.load(open(ROOT/'data/registry.json'))
    byhex = defaultdict(list)
    for e in r['deposits']:
        if e.get('hex'): byhex[e['hex']].append(e)
    (ROOT/'s/axn').mkdir(parents=True, exist_ok=True)
    idx = {}
    for hx, es in byhex.items():
        d = ROOT/'s/axn'/hx; d.mkdir(exist_ok=True)
        if len(es) == 1:
            e = es[0]; n = e['deposit_number']
            url = f"https://www.alexanarch.org/s/records/{n}/"
            idx[hx] = {"deposit_number": n, "axn": e['axn'], "record": url, "sha256": e.get('hash','')}
            ld = json.dumps({"@context":"https://schema.org","@type":"WebPage","identifier":e['axn'],
                             "mainEntityOfPage":url,"name":e.get('title','')}, ensure_ascii=False)
            (d/'index.html').write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(e['axn'])} — Alexanarch AXN resolver</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
<meta name="robots" content="index,follow">
<script type="application/ld+json">{ld}</script>
</head><body>
<p><strong>{html.escape(e['axn'])}</strong> resolves to deposit #{n}: <a href="{url}">{html.escape(e.get('title',''))}</a></p>
<p>canonical-text sha256: <code>{e.get('hash','')}</code></p>
<p>Resolver rule: <code>alexanarch.org/axn/&lt;HEX&gt;</code>. Machine index: <a href="/api/axn-index.json">/api/axn-index.json</a></p>
</body></html>""")
        else:
            rows = "\n".join(
              f'<p><strong>{html.escape(e["axn"])}</strong> — deposit #{e["deposit_number"]}: '
              f'<a href="https://www.alexanarch.org/s/records/{e["deposit_number"]}/">{html.escape(e.get("title","")[:90])}</a> '
              f'· sha256 <code>{e.get("hash","")[:16]}…</code></p>' for e in es)
            idx[hx] = {"disambiguation": True, "note": "hex assigned to multiple deposits (historical offset drift); full AXN glyphs disambiguate",
                       "records": [{"deposit_number": e["deposit_number"], "axn": e["axn"], "sha256": e.get("hash",""),
                                    "record": f"https://www.alexanarch.org/s/records/{e['deposit_number']}/"} for e in es]}
            (d/'index.html').write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>AXN hex {hx} — disambiguation — Alexanarch resolver</title>
<meta name="robots" content="index,follow"></head><body>
<h1>Hex {hx} — {len(es)} deposits (historical offset drift)</h1>
<p>Resolver policy: never silently select. Disambiguate by glyphs or sha256.</p>
{rows}
</body></html>""")
    json.dump({"name":"Alexanarch AXN resolver index","rule":"https://www.alexanarch.org/axn/<HEX>/",
               "canonical":"https://www.alexanarch.org/api/axn-index.json",
               "total": len(idx), "generated": r['deposits'][-1].get('date','') or '', "map": idx},
              open(ROOT/'api/axn-index.json','w'), ensure_ascii=False, separators=(",",":"))
    with open(ROOT/'sitemap-axn.xml','w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for hx in sorted(idx): f.write(f'  <url><loc>https://www.alexanarch.org/s/axn/{hx}/</loc></url>\n')
        f.write('</urlset>\n')
    print(f"axn resolver: {len(idx)} hexes ({sum(1 for v in idx.values() if v.get('disambiguation'))} disambiguation)")

if __name__ == "__main__":
    main()
