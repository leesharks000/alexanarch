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
import json, os, html
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
            lm = non_lm[hx] if hx in non_lm else cap_lm[hx] if hx in cap_lm else max(((e.get('date_modified') or e.get('date') or '')[:10] for e in byhex[hx]), default='')
            lm_tag = f'<lastmod>{lm}</lastmod>' if lm else ''
            f.write(f'  <url><loc>https://www.alexanarch.org/s/axn/{hx}/</loc>{lm_tag}</url>\n')
        f.write('</urlset>\n')
    print(f"axn resolver: {len(idx)} hexes ({sum(1 for v in idx.values() if v.get('disambiguation'))} disambiguation)")

if __name__ == "__main__":
    main()
