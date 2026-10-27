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
import sys as _sys_axd, pathlib as _pl_axd
_sys_axd.path.insert(0, str(_pl_axd.Path(__file__).resolve().parent))
import axn_derivation as _axd
import json, os, html, re
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def _md_inline(t):
    """The wiki article's inline emphasis (**bold**, *italic*), escaped and rendered."""
    import re as _re
    t = html.escape(t)
    t = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return _re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)


def main():
    r = json.load(open(ROOT/'data/registry.json'))
    byhex = defaultdict(list)
    for e in r['deposits']:
        if e.get('hex'): byhex[e['hex']].append(e)
    (ROOT/'s/axn').mkdir(parents=True, exist_ok=True)
    # Seats of the originals shelf carry AXNs under the hex of the deposit that numbers them (family ORIGINAL).
    _seats = defaultdict(list)
    try:
        for _c in json.load(open(ROOT/'data/api/corpora.json'))['corpora']:
            if str(_c.get('axn','')).startswith('AXN:'):
                _seats[_c['axn'].split(':',1)[1].split('.',1)[0]].append(_c)
    except Exception:
        pass
    idx = {}
    for hx, es in byhex.items():
        d = ROOT/'s/axn'/hx; d.mkdir(exist_ok=True)
        if len(es) == 1:
            e = es[0]; n = e['deposit_number']
            url = f"https://www.alexanarch.org/s/records/{n}/"
            idx[hx] = {"deposit_number": n, "axn": e['axn'], "record": url, "sha256": e.get('hash','')}
            _pf = [x.get('axn') for x in (e.get('axn_prior') or []) if x.get('axn')]
            if _pf: idx[hx]["prior"] = _pf
            axn_url = f"https://www.alexanarch.org/s/axn/{hx}/"
            parts = str(e['axn']).split('.')
            family = parts[1] if len(parts) > 2 else ''
            glyphs = parts[-1] if len(parts) > 2 else ''
            # axn/v2.2 record_dimensions: a record whose mint input was not retained is not described
            # as derived from its served text; the stored hash, its status and the served bytes are shown apart.
            _md = e.get('mint_derivation') or {}
            _cur = (e.get('manifestations') or {}).get('current') or {}
            _fe = e.get('founding_event') or {}
            # 2026-10-27 (MANUS: "axns should match their records"): every AXN derives from the record's text; a record
            # re-derived that day carries its prior forms, which resolve here and in /api/axn-aliases.json.
            _prior = [x.get('axn') for x in (e.get('axn_prior') or []) if x.get('axn')]
            _rd = e.get('axn_rederived') or {}
            if isinstance(_rd, dict) and _rd.get('axn_before'): _prior.insert(0, _rd['axn_before'])
            if _fe.get('batch_axn'): _prior.insert(0, _fe['batch_axn'])
            _prior = [x for x in dict.fromkeys(_prior) if x != e['axn']]
            _wiki = str(e.get('wiki_article') or '').strip()
            _desc = (f"AXN {hx} is the content-derived identifier of Alexanarch deposit "
                     f"#{n}. The hex marks position in the archive; the six-glyph suffix is "
                     f"a display hash of the canonical text's SHA-256, so the identifier is "
                     f"derived from the work rather than assigned to it. Family: {family}."
                     + (f" Prior forms, which name the same record: {'; '.join(_prior)}." if _prior else ""))
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
                "description": _desc,
                "about": {"@type": "ScholarlyArticle", "@id": url, "url": url,
                          "name": e.get('title', ''), **({"description": _wiki} if _wiki else {})},
                "subjectOf": {"@type": "WebPage", "@id": url, "url": url},
            }
            # 2026-10-27: no sameAs. The identifier is not the work; "about" names what it identifies.
            for _p in _prior:
                ld_obj["identifier"].append({"@type": "PropertyValue", "propertyID": "AXN-prior", "value": _p,
                                             "description": "a prior form of this AXN; it names the same record"})
            if _md:
                ld_obj["identifier"][2]["description"] = f"stored mint hash; {_md.get('status','')}"
                _swp = _axd.ld_swhid_property(e)
                if _swp: ld_obj["identifier"].append(_swp)
                if _cur.get('sha256'):
                    ld_obj["identifier"].append({"@type": "PropertyValue", "propertyID": "sha256-served",
                                                 "value": _cur['sha256'], "description": "SHA-256 of the bytes the record serves"})
            if family:
                ld_obj["termCode"] = e['axn']
                ld_obj["additionalProperty"] = [
                    {"@type": "PropertyValue", "name": "family", "value": family},
                    {"@type": "PropertyValue", "name": "glyph_hash", "value": glyphs},
                ]
            ld = json.dumps(ld_obj, ensure_ascii=False)
            _meta_txt = _wiki or (f"AXN {hx} — content-derived identifier of Alexanarch deposit #{n}. Hex position {hx}; family {family}; six-glyph display hash of the canonical text SHA-256.")
            if len(_meta_txt) > 320:
                _cut = _meta_txt[:320]; _meta_txt = _cut[:_cut.rfind(' ')] + ' …'
            _meta = f'<meta name="description" content="{html.escape(_meta_txt)}">'
            _intro = (f'<p><strong>AXN {hx}</strong> is the content-derived identifier of Alexanarch deposit\n'
                      f'<a href="{url}">#{n}</a>. It is an identifier, not a copy of the work: the hex marks\n'
                      f'position in the archive, and the six-glyph suffix is a display hash of the canonical\n'
                      f'text&rsquo;s SHA-256, so the identifier is derived from the work rather than assigned to it.</p>')
            if _wiki:
                _intro += ('\n<section><h2>The work</h2>\n' + ''.join(f'<p>{_md_inline(par.strip())}</p>' for par in _wiki.split('\n\n') if par.strip())
                           + f'\n<p><a href="{url}">The record, with the full text</a></p></section>')
            _seatrows = ''
            if _seats.get(hx):
                _seatrows = ('<dt>Originals seated</dt><dd>' + '<br>'.join(
                    f'<code>{html.escape(c["axn"])}</code> &mdash; seat {html.escape(c["seat"].split("-")[-1])}, '
                    f'<a href="https://traininglayerliterature.org/originals/{c["corpus"]}/">{html.escape(c["corpus"])}</a> '
                    f'(<a href="https://www.alexanarch.org/data/corpora/{c["corpus"]}/MANIFEST.sha256">MANIFEST</a>)'
                    for c in sorted(_seats[hx], key=lambda c: c["seat"])) + '</dd>')
                for c in _seats[hx]:
                    ld_obj["identifier"].append({"@type": "PropertyValue", "propertyID": "AXN-seat", "value": c["axn"],
                                                 "description": f"seat {c['seat'].split('-')[-1]} of the originals shelf ({c['corpus']}): glyphs of the SHA-256 of its MANIFEST.sha256"})
                ld = json.dumps(ld_obj, ensure_ascii=False)
            _hashrows = f"<dt>Canonical-text SHA-256</dt><dd><code>{e.get('hash','')}</code></dd>"
            if _prior:
                _hashrows += "<dt>Prior forms</dt><dd>" + "<br>".join(f"<code>{html.escape(x)}</code>" for x in _prior) + " &mdash; each names this record (<a href=\"/api/axn-aliases.json\">/api/axn-aliases.json</a>)</dd>"
            if _md.get('hash') and _md.get('hash') != e.get('hash'):
                _hashrows += (f"<dt>Stored hash at mint</dt><dd><code>{_md.get('hash','')}</code> &mdash; {html.escape(str(_md.get('status','')).replace('_',' '))}; "
                              "<a href=\"/data/axn-derivation-ledger.json\">derivation ledger</a></dd>")
            (d/'index.html').write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(e['axn'])} — Alexanarch AXN resolver</title>
<link rel="canonical" href="{axn_url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
{_meta}
<script type="application/ld+json">{ld}</script>
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></head><body>
<h1>{html.escape(e['axn'])}</h1>
{_intro}
<dl>
<dt>Identifies</dt><dd><a href="{url}">{html.escape(e.get('title','') or ('Deposit #' + str(n)))}</a></dd>
<dt>Hex position</dt><dd><code>{hx}</code></dd>
<dt>Family</dt><dd><code>{html.escape(family) or '&mdash;'}</code></dd>
<dt>Glyph hash</dt><dd>{html.escape(glyphs)}</dd>
{_hashrows}
<dt>Record</dt><dd><a href="{url}">{url}</a></dd>
{_seatrows}
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
<meta name="robots" content="index,follow"><script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></head><body>
<h1>Hex {hx} — {len(es)} deposits (historical offset drift)</h1>
<p>Resolver policy: never silently select. Disambiguate by glyphs or sha256.</p>
{rows}
</body></html>""")
    # /non entries (axn/v2.3 non_entries, 2026-10-24): the identifier page names the entry and its page; earlier
    # versions of the row are listed, each still an identifier of the composition it named.
    non_lm = {}
    _nl = ROOT/'datasets/negative-of-the-negative/v2/axn.json'
    if _nl.exists():
        _names = {x['entity']: x['name'] for x in json.load(open(ROOT/'datasets/negative-of-the-negative/v2/panel/panel.json'))['entities']}
        for k, x in sorted(json.load(open(_nl))['entries'].items()):
            hx = x['hex']
            if hx in idx:
                print(f"axn resolver: /non entry {k} at {hx} collides with a deposit; not written", file=_sys_axd.stderr); continue
            name = _names.get(k, k)
            url = f"https://www.alexanarch.org/non/{k}/"
            axn_url = f"https://www.alexanarch.org/s/axn/{hx}/"
            hist = x.get('history') or []
            idx[hx] = {"source": "non-entry", "entity": k, "axn": x['axn'], "root": x['root'], "record": url, "sha256": x['sha256'],
                       "row": f"https://www.alexanarch.org/{x['row']}", "versions": [{"axn": h['axn'], "sha256": h['sha256'], "until": h['until']} for h in hist]}
            non_lm[hx] = x.get('version_date') or x['minted']
            _desc = (f"{x['axn']} is the content-derived identifier of the entry {name} in the Negative of the Negative (alexanarch.org/non). "
                     f"The hex marks its position in the archive's one AXN sequence; NON is the family of /non entries; the six-glyph suffix is a "
                     f"display hash of the SHA-256 of the entry's row file, so each composition of the row is its own version.")
            ld = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": axn_url, "url": axn_url, "name": x['axn'], "termCode": x['axn'],
                  "identifier": [{"@type": "PropertyValue", "propertyID": "AXN", "value": x['axn']},
                                 {"@type": "PropertyValue", "propertyID": "AXN-root", "value": x['root']},
                                 {"@type": "PropertyValue", "propertyID": "AXN-hex", "value": hx},
                                 {"@type": "PropertyValue", "propertyID": "sha256", "value": x['sha256'], "description": "SHA-256 of the row file"}],
                  "inDefinedTermSet": {"@type": "DefinedTermSet", "@id": "https://www.alexanarch.org/s/axn/", "name": "AXN — Alexanarch content-derived identifiers",
                                       "url": "https://www.alexanarch.org/s/axn/"},
                  "description": _desc, "about": {"@type": "CreativeWork", "@id": url, "url": url, "name": f"{name} — The Negative of the Negative"},
                  "subjectOf": {"@type": "WebPage", "@id": url, "url": url}, "sameAs": [url],
                  "additionalProperty": [{"@type": "PropertyValue", "name": "family", "value": "NON"},
                                         {"@type": "PropertyValue", "name": "glyph_hash", "value": x['axn'].split('.')[-1]}]}
            hrows = "".join(f"<dt>Earlier version, until {html.escape(h['until'])}</dt><dd><code>{html.escape(h['axn'])}</code> &mdash; sha256 <code>{h['sha256']}</code> &mdash; {html.escape(h.get('reason',''))}</dd>" for h in hist)
            d = ROOT/'s/axn'/hx; d.mkdir(exist_ok=True)
            (d/'index.html').write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(x['axn'])} — Alexanarch AXN resolver</title>
<link rel="canonical" href="{axn_url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="description" content="{html.escape(_desc)}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></head><body>
<h1>{html.escape(x['axn'])}</h1>
<p>{html.escape(_desc)}</p>
<dl>
<dt>Identifies</dt><dd><a href="{url}">{html.escape(name)}</a>, an entry of the Negative of the Negative</dd>
<dt>Root</dt><dd><code>{html.escape(x['root'])}</code> (the entry across its compositions)</dd>
<dt>Hex position</dt><dd><code>{hx}</code></dd>
<dt>Family</dt><dd><code>NON</code></dd>
<dt>Glyph hash</dt><dd>{html.escape(x['axn'].split('.')[-1])}</dd>
<dt>Row SHA-256</dt><dd><code>{x['sha256']}</code> &mdash; <a href="/{x['row']}">the row</a></dd>
{hrows}
<dt>Ledger</dt><dd><a href="/datasets/negative-of-the-negative/v2/axn.json">/datasets/negative-of-the-negative/v2/axn.json</a></dd>
</dl>
<p>Resolver rule: <code>alexanarch.org/axn/&lt;HEX&gt;</code> &middot;
term set: <a href="/s/axn/">AXN identifier set</a> &middot;
machine index: <a href="/api/axn-index.json">/api/axn-index.json</a></p>
</body></html>""")
    # Capture positions (2026-10-27, MANUS: "one observation / analysis / measure should have one axn" — "one position per
    # address"). The page of a capture position carries each observation with its analysis and measures, so the
    # identifier is never reached without the reading it names.
    cap_lm = {}
    _cl = ROOT/'data/captures/axn.json'
    if _cl.exists():
        _toc = {}
        try:
            for _r in json.load(open(ROOT/'captures/index.json'))['records']:
                _toc[_r['slug']] = _r
                for _o in (_r.get('observations') or []):
                    _toc.setdefault(_o['slug'], {'record_url': _o['url']})
        except Exception:
            pass
        def _txt(v, n):
            v = ' '.join(str(v or '').split())
            return v if len(v) <= n else v[:v.rfind(' ', 0, n)] + ' …'
        for slug, a in sorted(json.load(open(_cl))['addresses'].items()):
            hx = a['hex']
            if hx in idx:
                print(f"axn resolver: capture {slug} at {hx} collides; not written", file=_sys_axd.stderr); continue
            rec = (_toc.get(slug) or {}).get('record_url') or f"https://www.alexanarch.org/captures/{slug}/"
            axn_url = f"https://www.alexanarch.org/s/axn/{hx}/"
            obs = sorted(a['observations'].items(), key=lambda kv: (str(kv[1].get('date') or ''), kv[0]))
            idx[hx] = {"source": "capture", "root": a['root'], "q": a.get('q'), "record": rec,
                       "observations": [{"axn": o['axn'], "sha256": o['sha256'], "date": o.get('date'), "surface": o.get('surface'),
                                         "sealed": f"https://www.alexanarch.org{o['file']}",
                                         **({"prior": [h['axn'] for h in o['history']]} if o.get('history') else {})} for _, o in obs]}
            cap_lm[hx] = max([str(o.get('date_derived') or '') for _, o in obs] or [a.get('allocated', '')])
            blocks, ids, desc_first = [], [], ''
            for k, o in obs:
                try:
                    sd = json.load(open(ROOT/o['file'].lstrip('/')))
                except Exception:
                    sd = {"analysis": {}, "measures": {}, "observation": {}}
                an, me = sd.get('analysis') or {}, sd.get('measures') or {}
                d_ = an.get('d') or ''
                if not desc_first and d_: desc_first = d_
                orl = (_toc.get(k) or {}).get('record_url') or rec
                per = me.get('per')
                rows = [f"<dt>Observation</dt><dd>{html.escape(str(o.get('surface') or ''))}, {html.escape(str(o.get('date') or ''))} &middot; <a href=\"{orl}\">the capture</a></dd>"]
                if d_: rows.append(f"<dt>Description</dt><dd>{html.escape(_txt(d_, 900))}</dd>")
                if an.get('reading'): rows.append(f"<dt>Reading</dt><dd>{html.escape(_txt(an['reading'], 1400))}</dd>")
                if an.get('analysis'): rows.append(f"<dt>Analysis</dt><dd>{html.escape(_txt(an['analysis'], 1400))}</dd>")
                if an.get('mt'): rows.append(f"<dt>Match</dt><dd>{html.escape(str(an.get('match') or ''))} &mdash; {html.escape(_txt(an['mt'], 400))}</dd>")
                if per is not None: rows.append(f"<dt>PER</dt><dd>{html.escape(str(per))}" + (f" &mdash; {html.escape(_txt(me['per_note'], 300))}" if me.get('per_note') else '') + "</dd>")
                if me.get('cites') not in (None, ''): rows.append(f"<dt>Citations</dt><dd>{html.escape(str(me['cites']))}" + (f" ({html.escape(str(me['archive_controlled_cites']))} archive-controlled)" if me.get('archive_controlled_cites') not in (None, '') else '') + "</dd>")
                rows.append(f"<dt>Sealed observation</dt><dd><a href=\"{o['file']}\">{html.escape(o['file'])}</a> &mdash; SHA-256 <code>{o['sha256']}</code></dd>")
                for h in (o.get('history') or []):
                    rows.append(f"<dt>Earlier form, until {html.escape(h['until'])}</dt><dd><code>{html.escape(h['axn'])}</code> &mdash; {html.escape(h.get('reason',''))}</dd>")
                blocks.append(f"<section><h2><code>{html.escape(o['axn'])}</code></h2>\n<dl>{''.join(rows)}</dl></section>")
                ids.append({"@type": "PropertyValue", "propertyID": "AXN", "value": o['axn'], "url": orl,
                            "description": f"observation of {o.get('surface') or ''}, {o.get('date') or ''}, sealed with its analysis and measures; SHA-256 {o['sha256']}"})
            q = str(a.get('q') or '')
            _desc = (f"{a['root']} is the position of the Capture Registry address for the query \u201c{q}\u201d. Each observation at the address "
                     f"(one surface, one date) is one AXN, its glyphs derived from the SHA-256 of the observation sealed with its analysis and measures.")
            _meta_txt = _txt((f"Query \u201c{q}\u201d: " + desc_first) if desc_first else _desc, 320)
            ld = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": axn_url, "url": axn_url, "name": a['root'], "termCode": a['root'],
                  "identifier": [{"@type": "PropertyValue", "propertyID": "AXN-root", "value": a['root']},
                                 {"@type": "PropertyValue", "propertyID": "AXN-hex", "value": hx}] + ids,
                  "inDefinedTermSet": {"@type": "DefinedTermSet", "@id": "https://www.alexanarch.org/s/axn/", "name": "AXN — Alexanarch content-derived identifiers",
                                       "url": "https://www.alexanarch.org/s/axn/"},
                  "description": _desc, "about": {"@type": "Dataset", "@id": rec, "url": rec, "name": f"Capture: {q}"},
                  "subjectOf": {"@type": "WebPage", "@id": rec, "url": rec},
                  "additionalProperty": [{"@type": "PropertyValue", "name": "family", "value": "CAPTURE"}]}
            d = ROOT/'s/axn'/hx; d.mkdir(exist_ok=True)
            (d/'index.html').write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(a['root'])} — {html.escape(_txt(q, 80))} — Alexanarch AXN resolver</title>
<link rel="canonical" href="{axn_url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="description" content="{html.escape(_meta_txt)}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></head><body>
<h1>{html.escape(a['root'])}</h1>
<p>{html.escape(_desc)}</p>
<dl>
<dt>Query</dt><dd>{html.escape(q)}</dd>
<dt>Identifies</dt><dd><a href="{rec}">the capture record</a> of the Capture Registry</dd>
<dt>Hex position</dt><dd><code>{hx}</code></dd>
<dt>Family</dt><dd><code>CAPTURE</code></dd>
<dt>Ledger</dt><dd><a href="/data/captures/axn.json">/data/captures/axn.json</a></dd>
</dl>
{chr(10).join(blocks)}
<p>Resolver rule: <code>alexanarch.org/axn/&lt;HEX&gt;</code> &middot;
term set: <a href="/s/axn/">AXN identifier set</a> &middot;
machine index: <a href="/api/axn-index.json">/api/axn-index.json</a></p>
</body></html>""")
    # /non register positions (2026-10-27, MANUS: "yes, they should probably also have a[n axn]"): one position per
    # address of the /non register, one AXN per observation sealed with its reading and measures; an observation seated in
    # both registers carries the Capture Registry's AXN and is shown with it.
    pan_lm = {}
    _pl = ROOT/'datasets/negative-of-the-negative/v2/register-axn.json'
    if _pl.exists():
        def _t2(v, n):
            v = ' '.join(str(v or '').split())
            return v if len(v) <= n else v[:v.rfind(' ', 0, n)] + ' …'
        for slug, a in sorted(json.load(open(_pl))['addresses'].items()):
            if 'hex' not in a:
                continue
            hx = a['hex']
            if hx in idx:
                print(f"axn resolver: /non register address {slug} at {hx} collides; not written", file=_sys_axd.stderr); continue
            axn_url = f"https://www.alexanarch.org/s/axn/{hx}/"
            reg_url = "https://www.alexanarch.org/datasets/negative-of-the-negative/v2/register.json"
            ent_url = f"https://www.alexanarch.org/non/{a['entity']}/" if a.get('entity') else reg_url
            obs = sorted(a['observations'].items(), key=lambda kv: (str(kv[1].get('date') or ''), kv[0]))
            idx[hx] = {"source": "non-register", "root": a['root'], "q": a.get('q'), "entity": a.get('entity'), "record": reg_url,
                       "observations": [{"axn": o['axn'], "date": o.get('date'), "surface": o.get('surface'), **({"sha256": o['sha256'], "sealed": "https://www.alexanarch.org" + o['file']} if o.get('file') else {"shared_with_capture_registry": o.get('shared_with_capture_registry')})} for _, o in obs]}
            pan_lm[hx] = max([str(o.get('date_derived') or o.get('date') or '') for _, o in obs] or [a.get('allocated', '')])
            blocks, ids = [], []
            for k, o in obs:
                rows = [f"<dt>Observation</dt><dd>{html.escape(str(o.get('surface') or ''))}, {html.escape(str(o.get('date') or ''))} &middot; <code>{html.escape(str(o.get('obs_id') or ''))}</code></dd>"]
                if o.get('file'):
                    try:
                        sd = json.load(open(ROOT/o['file'].lstrip('/')))
                    except Exception:
                        sd = {}
                    rd, me = sd.get('reading') or {}, sd.get('measures') or {}
                    if 'archive_present' in rd:
                        rows.append(f"<dt>Archive</dt><dd>{'present' if rd['archive_present'] else 'absent'}" + (f" &mdash; {html.escape(_t2(rd.get('archive_basis'), 900))}" if rd.get('archive_basis') else '') + "</dd>")
                    if me.get('cites') not in (None, ''):
                        rows.append(f"<dt>Citations</dt><dd>{html.escape(str(me['cites']))}</dd>")
                    if me.get('sf'):
                        rows.append(f"<dt>Source strip</dt><dd>{html.escape(_t2(me['sf'], 400))}</dd>")
                    rows.append(f"<dt>Sealed observation</dt><dd><a href=\"{o['file']}\">{html.escape(o['file'])}</a> &mdash; SHA-256 <code>{o['sha256']}</code></dd>")
                    for h in (o.get('history') or []):
                        rows.append(f"<dt>Earlier form, until {html.escape(h['until'])}</dt><dd><code>{html.escape(h['axn'])}</code> &mdash; {html.escape(h.get('reason',''))}</dd>")
                else:
                    sh = o.get('shared_with_capture_registry') or {}
                    h_ = str(sh.get('root', '')).split(':')[-1].split('.')[0]
                    rows.append(f"<dt>Seated in both registers</dt><dd>one observation, one AXN: the Capture Registry's, at <a href=\"/s/axn/{h_}/\"><code>{html.escape(sh.get('root', ''))}</code></a>, sealed with its analysis and measures (<a href=\"{html.escape(sh.get('sealed', ''))}\">{html.escape(sh.get('sealed', ''))}</a>)</dd>")
                blocks.append(f"<section><h2><code>{html.escape(o['axn'])}</code></h2>\n<dl>{''.join(rows)}</dl></section>")
                ids.append({"@type": "PropertyValue", "propertyID": "AXN", "value": o['axn'], "description": f"observation of {o.get('surface') or ''}, {o.get('date') or ''}"})
            q = str(a.get('q') or '')
            _desc = (f"{a['root']} is the position of the /non register address for the query \u201c{q}\u201d on {a.get('surface') or ''}: public knowledge "
                     f"at an address of the /non panel, where the archive is most often not represented. Each observation is one AXN, its glyphs derived "
                     f"from the SHA-256 of the observation sealed with its reading and measures.")
            ld = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": axn_url, "url": axn_url, "name": a['root'], "termCode": a['root'],
                  "identifier": [{"@type": "PropertyValue", "propertyID": "AXN-root", "value": a['root']},
                                 {"@type": "PropertyValue", "propertyID": "AXN-hex", "value": hx}] + ids,
                  "inDefinedTermSet": {"@type": "DefinedTermSet", "@id": "https://www.alexanarch.org/s/axn/", "name": "AXN — Alexanarch content-derived identifiers",
                                       "url": "https://www.alexanarch.org/s/axn/"},
                  "description": _desc, "about": {"@type": "Dataset", "@id": reg_url, "url": reg_url, "name": f"/non register: {q}"},
                  "additionalProperty": [{"@type": "PropertyValue", "name": "family", "value": "PANEL"}]}
            d = ROOT/'s/axn'/hx; d.mkdir(exist_ok=True)
            (d/'index.html').write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(a['root'])} — {html.escape(_t2(q, 80))} — Alexanarch AXN resolver</title>
<link rel="canonical" href="{axn_url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="description" content="{html.escape(_t2(_desc, 320))}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></head><body>
<h1>{html.escape(a['root'])}</h1>
<p>{html.escape(_desc)}</p>
<dl>
<dt>Query</dt><dd>{html.escape(q)}</dd>
<dt>Entity of the panel</dt><dd><a href="{ent_url}">{html.escape(str(a.get('entity') or ''))}</a></dd>
<dt>Register</dt><dd><a href="{reg_url}">{reg_url}</a></dd>
<dt>Hex position</dt><dd><code>{hx}</code></dd>
<dt>Family</dt><dd><code>PANEL</code></dd>
<dt>Ledger</dt><dd><a href="/datasets/negative-of-the-negative/v2/register-axn.json">/datasets/negative-of-the-negative/v2/register-axn.json</a></dd>
</dl>
{chr(10).join(blocks)}
<p>Resolver rule: <code>alexanarch.org/axn/&lt;HEX&gt;</code> &middot;
term set: <a href="/s/axn/">AXN identifier set</a> &middot;
machine index: <a href="/api/axn-index.json">/api/axn-index.json</a></p>
</body></html>""")
    # Releases (2026-10-27, adopted: "mint when preserving the distinction will matter later"): one position per
    # continuing object (a dataset, an instrument, a site); one AXN per frozen release. Continuity, version, location.
    rel_lm = {}
    _rl = ROOT/'data/releases/axn.json'
    if _rl.exists():
        _kind_name = {"dataset": "dataset", "instrument": "instrument", "site": "site"}
        for key, L in sorted(json.load(open(_rl))['objects'].items()):
            hx = L['hex']
            if hx in idx:
                print(f"axn resolver: release object {key} at {hx} collides; not written", file=_sys_axd.stderr); continue
            axn_url = f"https://www.alexanarch.org/s/axn/{hx}/"
            rs = L.get('releases') or []
            idx[hx] = {"source": "release", "kind": L['kind'], "object": key, "root": L['root'], "name": L.get('name'),
                       "locations": L.get('locations') or [],
                       "releases": [{k: x[k] for k in ("axn", "label", "date", "sha256", "basis", "files", "bytes", "manifest", "file", "frozen", "base_commit") if k in x} for x in rs]}
            rel_lm[hx] = max([x['date'] for x in rs] or [L.get('allocated', '')])
            what = {"manifest": "the SHA-256 of its manifest (every constituent file with the SHA-256 of its bytes)",
                    "file": "the SHA-256 of the file itself"}
            blocks, ids = [], []
            for rr in reversed(rs):
                rows = [f"<dt>Release</dt><dd>{html.escape(rr['label'])} &middot; frozen {html.escape(rr['date'])}</dd>",
                        f"<dt>SHA-256</dt><dd><code>{rr['sha256']}</code> &mdash; {what.get(rr['basis'], '')}</dd>",
                        f"<dt>Size</dt><dd>{rr['files']:,} file{'s' if rr['files'] != 1 else ''}, {rr['bytes']:,} bytes</dd>"]
                if rr.get('manifest'):
                    rows.append(f"<dt>Manifest</dt><dd><a href=\"{rr['manifest']}\">{html.escape(rr['manifest'])}</a> &mdash; verify from the repository root with <code>sha256sum -c</code></dd>")
                if rr.get('frozen'):
                    rows.append(f"<dt>Frozen copy</dt><dd><a href=\"{rr['frozen']}\">{html.escape(rr['frozen'])}</a> (of <code>{html.escape(rr['file'])}</code>)</dd>")
                if rr.get('base_commit'):
                    rows.append(f"<dt>Commit</dt><dd><a href=\"https://github.com/leesharks000/alexanarch/tree/{rr['base_commit']}\"><code>{rr['base_commit']}</code></a> &mdash; the release is this commit&rsquo;s tree, HTML pages and sitemaps left out</dd>")
                if rr.get('note'):
                    rows.append(f"<dt>Note</dt><dd>{html.escape(rr['note'])}</dd>")
                blocks.append(f"<section><h2><code>{html.escape(rr['axn'])}</code></h2>\n<dl>{''.join(rows)}</dl></section>")
                ids.append({"@type": "PropertyValue", "propertyID": "AXN", "value": rr['axn'], "description": f"release {rr['label']}, frozen {rr['date']}; SHA-256 {rr['sha256']}"})
            nm = L.get('name') or key
            _desc = (f"{L['root']} is the position of the {_kind_name.get(L['kind'], L['kind'])} {nm} in the archive's one AXN sequence. "
                     f"The position names the {L['kind']} across its releases; each release is one AXN, its glyphs derived from "
                     f"the SHA-256 of what the release freezes. Locations can change; a release keeps its identity.")
            loc_html = "<br>".join(f'<a href="{html.escape(u)}">{html.escape(u)}</a>' for u in (L.get('locations') or []))
            extra = ""
            if L.get('governs'):
                extra += f"<dt>Governs</dt><dd>{html.escape(str(L['governs']))}</dd>"
            if L.get('source'):
                extra += "<dt>Constituted by</dt><dd>" + "<br>".join(f"<code>{html.escape(x)}</code>" for x in L['source']) + "</dd>"
            ld = {"@context": "https://schema.org", "@type": "DefinedTerm", "@id": axn_url, "url": axn_url, "name": L['root'], "termCode": L['root'],
                  "identifier": [{"@type": "PropertyValue", "propertyID": "AXN-root", "value": L['root']},
                                 {"@type": "PropertyValue", "propertyID": "AXN-hex", "value": hx}] + ids,
                  "inDefinedTermSet": {"@type": "DefinedTermSet", "@id": "https://www.alexanarch.org/s/axn/", "name": "AXN — Alexanarch content-derived identifiers",
                                       "url": "https://www.alexanarch.org/s/axn/"},
                  "description": _desc,
                  "about": {"@type": {"dataset": "Dataset", "instrument": "CreativeWork", "site": "WebSite"}.get(L['kind'], "Thing"),
                            "name": nm, **({"url": L['locations'][0]} if L.get('locations') else {})},
                  "additionalProperty": [{"@type": "PropertyValue", "name": "family", "value": L['family']}]}
            d = ROOT/'s/axn'/hx; d.mkdir(exist_ok=True)
            (d/'index.html').write_text(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(L['root'])} — {html.escape(nm)} — Alexanarch AXN resolver</title>
<link rel="canonical" href="{axn_url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta name="description" content="{html.escape(_desc)}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></head><body>
<h1>{html.escape(L['root'])}</h1>
<p>{html.escape(_desc)}</p>
<dl>
<dt>Identifies</dt><dd>{html.escape(nm)} ({html.escape(L['kind'])})</dd>
<dt>Hex position</dt><dd><code>{hx}</code></dd>
<dt>Family</dt><dd><code>{html.escape(L['family'])}</code></dd>
<dt>Locations</dt><dd>{loc_html or '&mdash;'}</dd>
{extra}
<dt>Ledger</dt><dd><a href="/data/releases/axn.json">/data/releases/axn.json</a></dd>
</dl>
{chr(10).join(blocks)}
<p>Resolver rule: <code>alexanarch.org/axn/&lt;HEX&gt;</code> &middot;
term set: <a href="/s/axn/">AXN identifier set</a> &middot;
machine index: <a href="/api/axn-index.json">/api/axn-index.json</a></p>
</body></html>""")
    # Typed relations (data/axn-relations.json, scripts/build_axn_relations.py): each page carries the relations its hex
    # has, in both directions, with the field each was read from.
    _rf = ROOT/'data/axn-relations.json'
    if _rf.exists():
        R = json.load(open(_rf))
        rels = R['relations']
        names = {}
        for _hx, v in idx.items():
            nm_ = v.get('name') or v.get('q') or v.get('entity') or (f"deposit #{v['deposit_number']}" if v.get('deposit_number') else '')
            if v.get('deposit_number') and byhex.get(_hx):
                nm_ = byhex[_hx][0].get('title') or nm_
            names[_hx] = nm_
        OUT = {"follows": "Follows", "opens": "Opens", "grounds_in": "Grounds in", "read": "Read", "appeared_in": "Drew on",
               "about": "About", "mentions": "Mentions", "mentions_instrument": "Mentions", "pair_of": "Paired with",
               "documented_in": "Documented in", "scored_by": "Scored by", "distorts": "Distorts"}
        IN = {"follows": "Followed by", "opens": "Opened by", "grounds_in": "Grounds", "read": "Read by", "appeared_in": "Drawn on by",
              "about": "Subject of", "mentions": "Mentioned by", "mentions_instrument": "Mentioned by", "pair_of": "Paired with",
              "documented_in": "Documents", "scored_by": "Scores", "distorts": "Distorted by"}
        def _hx(a):
            m_ = re.match(r"AXN:([0-9A-F]+)", str(a)); return m_.group(1) if m_ else None
        def _ref(a, label=None):
            h_ = _hx(a)
            if h_:
                t_ = names.get(h_, '')
                return f'<a href="/s/axn/{h_}/"><code>{html.escape(a)}</code></a>' + (f" &mdash; {html.escape(str(t_)[:110])}" if t_ else "")
            return f'<a href="{html.escape(a)}">{html.escape(label or a)}</a>'
        CAP = 60
        n_pages = 0
        for h_, ent in R['by_hex'].items():
            f_ = ROOT/'s/axn'/h_/'index.html'
            if not f_.exists():
                continue
            parts, ld_rel = [], {"isBasedOn": [], "subjectOf": []}
            for direction, ids_, lab in (("out", ent['out'], OUT), ("in", ent['in'], IN)):
                groups = defaultdict(list)
                for i_ in ids_:
                    groups[rels[i_]['verb']].append(rels[i_])
                for verb, rs_ in sorted(groups.items()):
                    items = []
                    for r_ in rs_[:CAP]:
                        other = r_['object'] if direction == "out" else r_['subject']
                        b_ = f' <span style="color:#666">({html.escape(str(r_.get("basis"))[:160])}; <code>{html.escape(r_["field"] or "")}</code>)</span>' if r_.get('basis') else f' <span style="color:#666">(<code>{html.escape(r_["field"] or "")}</code>)</span>'
                        items.append(f"<li>{_ref(other, r_.get('object_label') if direction == 'out' else None)}{b_}</li>")
                        if str(other).startswith("AXN:") or str(other).startswith("http"):
                            u_ = f"https://www.alexanarch.org/s/axn/{_hx(other)}/" if _hx(other) else other
                            ld_rel["isBasedOn" if direction == "out" else "subjectOf"].append({"@id": u_, "name": other, "description": verb})
                    more = f"<li>and {len(rs_) - CAP} more &mdash; <a href=\"/data/axn-relations.json\">/data/axn-relations.json</a></li>" if len(rs_) > CAP else ""
                    parts.append(f"<dt>{lab.get(verb, verb)}</dt><dd><ul style=\"margin:0;padding-left:18px\">{''.join(items)}{more}</ul></dd>")
            if not parts:
                continue
            sec = ('<section><h2>Relations</h2>\n<p>Read from the fields that record them (<a href="/data/axn-relations.json">/data/axn-relations.json</a>); '
                   'a hash names bytes and supplies no relation.</p>\n<dl>' + "".join(parts) + '</dl></section>\n')
            ldr = {"@context": "https://schema.org", "@id": f"https://www.alexanarch.org/s/axn/{h_}/", **{k: v[:200] for k, v in ld_rel.items() if v}}
            t_ = f_.read_text()
            if '<section><h2>Relations</h2>' in t_:
                continue
            t_ = t_.replace("<p>Resolver rule:", sec + "<p>Resolver rule:", 1)
            t_ = t_.replace("</head>", f'<script type="application/ld+json">{json.dumps(ldr, ensure_ascii=False)}</script>\n</head>', 1)
            f_.write_text(t_); n_pages += 1
            idx[h_]["relations"] = {"out": len(ent['out']), "in": len(ent['in'])}
        print(f"axn resolver: relations on {n_pages} pages ({len(rels)} relations)")
    json.dump({"name":"Alexanarch AXN resolver index","rule":"https://www.alexanarch.org/axn/<HEX>/",
               "canonical":"https://www.alexanarch.org/api/axn-index.json",
               "total": len(idx), "generated": r['deposits'][-1].get('date','') or '', "map": idx},
              open(ROOT/'data/api/axn-index.json','w'), ensure_ascii=False, separators=(",",":"))
    with open(ROOT/'sitemap-axn.xml','w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        # 2026-10-15: <lastmod> added. The AXN page changes when its record changes, so it carries the
        # record's own last modification (record_modification.last_modified: date_modified, else the
        # deposit date); a disambiguation page carries the latest of its records. Never the run date.
        for hx in sorted(idx):
            lm = non_lm[hx] if hx in non_lm else cap_lm[hx] if hx in cap_lm else rel_lm[hx] if hx in rel_lm else pan_lm[hx] if hx in pan_lm else max(((e.get('date_modified') or e.get('date') or '')[:10] for e in byhex[hx]), default='')
            lm_tag = f'<lastmod>{lm}</lastmod>' if lm else ''
            f.write(f'  <url><loc>https://www.alexanarch.org/s/axn/{hx}/</loc>{lm_tag}</url>\n')
        f.write('</urlset>\n')
    print(f"axn resolver: {len(idx)} hexes ({sum(1 for v in idx.values() if v.get('disambiguation'))} disambiguation)")

if __name__ == "__main__":
    main()
