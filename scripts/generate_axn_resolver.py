#!/usr/bin/env python3
"""generate_axn_resolver.py — regenerate the AXN resolution layer from data/registry.json.

ENTITY MODEL (v2, EA-RETRIEVAL-DENSITY-01 Task 11). An AXN and the work it
identifies are two entities, not one page in two places:

  /s/records/<N>/   the WORK        schema.org/ScholarlyArticle, self-canonical
  /s/axn/<HEX>/     the IDENTIFIER  schema.org/DefinedTerm, self-canonical,
                                    about -> the work

v1 emitted every AXN page with rel=canonical pointing at the record AND a
zero-second meta refresh. Both signals instruct an indexer to consolidate the
URL away, so 1,406 sitemap entries were engineered not to be indexed. The
identifier is a distinct object — content-derived, hex-positioned, glyph-hashed,
citable independently of the work — and is now published as one: canonical to
itself, a member of a DefinedTermSet, related to the work by `about` and
`sameAs` rather than by canonical consolidation. No duplicate content is
created, because the two pages describe different things.

Writes: s/axn/<HEX>/index.html for every hex (disambiguation page for any hex
assigned to multiple deposits — resolver policy: never silently select),
s/axn/index.html (the DefinedTermSet), api/axn-index.json (machine map),
sitemap-axn.xml. Idempotent; called by regenerate_surfaces.py so every mint
refreshes resolution automatically.
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
            axn_url = f"https://www.alexanarch.org/s/axn/{hx}/"
            parts = str(e['axn']).split('.')
            family = parts[1] if len(parts) > 2 else ''
            glyphs = parts[-1] if len(parts) > 2 else ''
            ld_obj = {
                "@context": "https://schema.org",
                "@type": "DefinedTerm",
                "@id": axn_url,
                "url": axn_url,
                "name": e['axn'],
                "termCode": e['axn'],
                "identifier": [
                    {"@type": "PropertyValue", "propertyID": "AXN", "value": e['axn']},
                    {"@type": "PropertyValue", "propertyID": "AXN-hex", "value": hx},
                    {"@type": "PropertyValue", "propertyID": "sha256",
                     "value": e.get('hash', '')},
                ],
                "inDefinedTermSet": {
                    "@type": "DefinedTermSet",
                    "@id": "https://www.alexanarch.org/s/axn/",
                    "name": "AXN — Alexanarch content-derived identifiers",
                    "url": "https://www.alexanarch.org/s/axn/",
                },
                "description": (
                    f"AXN {hx} is the content-derived identifier of Alexanarch deposit "
                    f"#{n}. The hex marks position in the archive; the six-glyph suffix is "
                    f"a display hash of the canonical text's SHA-256, so the identifier is "
                    f"derived from the work rather than assigned to it. Family: {family}."),
                "about": {"@type": "ScholarlyArticle", "@id": url, "url": url,
                          "name": e.get('title', '')},
                "subjectOf": {"@type": "WebPage", "@id": url, "url": url},
                "sameAs": [url],
            }
            if family:
                ld_obj["termCode"] = e['axn']
                ld_obj["additionalProperty"] = [
                    {"@type": "PropertyValue", "name": "family", "value": family},
                    {"@type": "PropertyValue", "name": "glyph_hash", "value": glyphs},
                ]
            ld = json.dumps(ld_obj, ensure_ascii=False)
            (d/'index.html').write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(e['axn'])} — Alexanarch AXN resolver</title>
<link rel="canonical" href="{axn_url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="description" content="AXN {hx} — content-derived identifier of Alexanarch deposit #{n}. Hex position {hx}; family {html.escape(family)}; six-glyph display hash of the canonical text SHA-256.">
<script type="application/ld+json">{ld}</script>
</head><body>
<h1>{html.escape(e['axn'])}</h1>
<p><strong>AXN {hx}</strong> is the content-derived identifier of Alexanarch deposit
<a href="{url}">#{n}</a>. It is an identifier, not a copy of the work: the hex marks
position in the archive, and the six-glyph suffix is a display hash of the canonical
text&rsquo;s SHA-256, so the identifier is derived from the work rather than assigned to it.</p>
<dl>
<dt>Identifies</dt><dd><a href="{url}">{html.escape(e.get('title','') or ('Deposit #' + str(n)))}</a></dd>
<dt>Hex position</dt><dd><code>{hx}</code></dd>
<dt>Family</dt><dd><code>{html.escape(family) or '&mdash;'}</code></dd>
<dt>Glyph hash</dt><dd>{html.escape(glyphs)}</dd>
<dt>Canonical-text SHA-256</dt><dd><code>{e.get('hash','')}</code></dd>
<dt>Record</dt><dd><a href="{url}">{url}</a></dd>
</dl>
<p>Resolver rule: <code>alexanarch.org/axn/&lt;HEX&gt;</code> &middot;
term set: <a href="/s/axn/">AXN identifier set</a> &middot;
machine index: <a href="/api/axn-index.json">/api/axn-index.json</a></p>
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
