#!/usr/bin/env python3
"""restore_wrong_bodies.py — seat the published text into deposits whose seated body is a different work
(wrong body) or only the deposit's metadata capture (missing body).

Ruling (Lee Sharks, 2026-10-15): "lets restore the ones we can" — wrong bodies first, located "elsewhere in the
archive or in the blog. almost everything is on the blog." Repair standard (same day): the text as he published it.

Follows the recorded-correction protocol of restore_in_place.py (2026-07-04 / 07-19 / 07-28): fetch the post, extract
the Blogger body, convert to markdown with the same converter, legal-name hygiene scan (held on a hit), seat the
body under a provenance header, RETAIN the previously seated body as an appendix (non-destruction), new hash, new
glyph, AXN recomposed in the same hex and family, restoration dict and remediation note.

The candidate list is ruled, not gated: each entry was matched to its post and its identity checked by hand (the
post carries the deposit's DOI or hex, or its exact title and date); the basis is recorded per record.

USAGE: python3 scripts/restore_wrong_bodies.py RULED.json [--dry-run] [--report PATH]
       RULED.json = {"<deposit>": {"url": ..., "kind": "wrong_body"|"missing_body"|"truncated_body"|"missing_part", "basis": ...,
                                   "part_heading": ... (missing_part only)}, ...}
       missing_part (ruling 2026-10-15, "flesh it out wherever the full text is available"): the deposit's own
       file list names a part that was never seated; the recovered part is added after the seated body.
Report: --report (default data/restoration-wrong-bodies-2026-10-15.json; give each later run its own)
"""
import argparse, datetime, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from restore_from_blog import fetch, extract_post
from legal_name import contains_legal_name  # hashed guard (b18dfa7c88)
import html2text
_H = html2text.HTML2Text(); _H.body_width = 0; _H.unicode_snob = True
# unicode_snob (2026-10-15): html2text's default replaces entity-encoded characters with ASCII stand-ins (&#183; -> '*', &mdash; -> '--', curly quotes -> straight, accented letters -> bare); the published text keeps them.
to_md = lambda h: _H.handle(h)
# html2text escapes markdown-significant characters ("0\\.", "\\+"); the record renderer does not read escapes and
# would show the backslash. Drop an escape unless the published HTML itself carries that sequence (2026-10-15).
_ESC = re.compile(r'\\([+\-.*_#!\[\]()`>|~])')
unescape = lambda md, src: _ESC.sub(lambda m: m.group(0) if m.group(0) in src else m.group(1), md)
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

TODAY = '2026-10-15'
REPORT = ROOT / 'data' / 'restoration-wrong-bodies-2026-10-15.json'
RULING = ('Lee Sharks, 2026-10-15: "lets restore the ones we can" (wrong bodies first, from the blog or elsewhere in '
          'the archive); repair standard: the text as he published it. Identity of each post checked by hand; '
          'the basis is recorded per record.')
KIND = {'wrong_body': ('the body previously seated here was a different work (wrong body)',
                       'body previously seated here — a different work, superseded'),
        'missing_body': ("the body previously seated here was only the deposit's metadata capture (missing body)",
                         'metadata-capture body, superseded'),
        'truncated_body': ('the body previously seated here was cut short (truncated body)',
                           'truncated body previously seated here, superseded'),
        # a part the deposit names (its own file list) that was never seated; the seated body stays as it is
        'missing_part': ("a part this deposit names in its own file list was never seated (missing part)", None)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ruled'); ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--report', default=str(REPORT), help='report path (one per run; never overwrite an earlier run)')
    a = ap.parse_args()
    ruled = {int(k): v for k, v in json.load(open(a.ruled)).items()}
    reg = json.load(open(ROOT / 'data' / 'registry.json'))
    byn = {d['deposit_number']: d for d in reg['deposits']}
    out = {'restored': [], 'held': [], 'would_restore': []}
    for n, r in sorted(ruled.items()):
        d = byn[n]; url = r['url']
        try:
            html = fetch(url).decode('utf-8', 'replace')
        except Exception as ex:
            out['held'].append({'n': n, 'reason': 'fetch', 'detail': str(ex)[:200]}); continue
        ptitle, body = extract_post(html)
        md = unescape(to_md(body or ''), body or '').strip()
        if not md:
            out['held'].append({'n': n, 'reason': 'empty_post', 'detail': url}); continue
        if contains_legal_name(html, substring=True) or contains_legal_name(md, substring=True):
            out['held'].append({'n': n, 'reason': 'legal_name_hygiene', 'detail': url}); continue
        if a.dry_run:
            out['would_restore'].append({'n': n, 'url': url, 'post_title': ptitle, 'chars': len(md)}); continue
        hex_id, family = d['hex'], d.get('family', 'ARCHIVAL')
        old_axn, old_hash = d.get('axn'), d.get('hash')
        tp = (d.get('full_text_path') or f'/data/texts/AXN-{hex_id}-text.md').lstrip('/')
        old_body = (ROOT / tp).read_text(errors='replace').strip() if (ROOT / tp).exists() else ''
        dois = ', '.join(d.get('zenodo_dois') or []) or '(none recorded)'
        what, apphead = KIND[r['kind']]
        header = (
            f"# {d.get('title')}\n\n"
            f"**{d.get('creator')}** · restored {TODAY}\n\n"
            f"**AXN:** AXN:{hex_id} — Alexanarch deposit #{n} (self-reference in root form by pre-hash necessity)\n"
            f"**Restoration status:** RESTORED — {what}. The published text, recovered from {url}, is seated here as "
            f"the canonical body. Identity: {r['basis']}. The previously seated body is retained below as an appendix.\n"
            f"**DOI(s):** {dois}\n\n---\n\n")
        if r['kind'] == 'missing_part':
            # the existing body is the deposit's other part: kept in place, unchanged; the recovered part follows
            header = header.replace('The previously seated body is retained below as an appendix.',
                                    f"The previously seated body is kept in place, unchanged, as the deposit's other part; "
                                    f"the recovered part follows it, under its own heading.")
            text = header + old_body + f"\n\n---\n\n## {r['part_heading']}\n\n" + md + "\n"
        else:
            appendix = (f"\n\n---\n\n## Appendix — {apphead} {TODAY} (retained per non-destruction)\n\n" + old_body + "\n") if old_body else ''
            text = header + md + appendix
        (ROOT / tp).write_text(text, encoding='utf-8')
        h = hashlib.sha256(text.encode('utf-8')).hexdigest(); glyph = axn_glyph_from_hash(h)
        d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = glyph
        d['axn'] = compose_axn(hex_id, family, glyph)
        d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
        d['full_text_path'] = '/' + tp
        rs = d.get('restoration') if isinstance(d.get('restoration'), dict) else {}
        rs.update({'fulltext': 'restored', 'fulltext_source': url, 'restored_at': TODAY, 'repair_kind': r['kind'],
                   'identity_basis': r['basis'], 'axn_before_restoration': old_axn, 'hash_before_restoration': old_hash,
                   'ruled_by': RULING})
        d['restoration'] = rs
        d['remediation_note'] = (f"{TODAY} RECORD REPAIR ({r['kind'].replace('_', ' ')}): {what}; the published text from "
                                 f"{url} seated as canonical; new hash and glyph; " + ("the seated part kept in place." if r['kind'] == 'missing_part' else "the previous body retained as appendix."))
        d['canonical_text_status'] = 'recovered_full_text'
        prev = d.get('body_status') if isinstance(d.get('body_status'), dict) else {}
        d['body_status'] = {'class': 'full', 'lacuna': False, 'recovery_status': 'RESTORED-20261015',
                            'recovered_from': url, 'residual_chars': len(text),
                            'audited_at': datetime.datetime.now(datetime.UTC).isoformat(),
                            'audit_version': 'restore_wrong_bodies-20261015',
                            'class_before_restoration': prev.get('class')}
        d['date_modified'] = TODAY
        out['restored'].append({'n': n, 'kind': r['kind'], 'url': url, 'post_title': ptitle, 'chars': len(md),
                                'axn_old': old_axn, 'axn_new': d['axn'], 'hash_old': old_hash, 'hash_new': h})
    if not a.dry_run:
        reg['last_updated'] = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
        json.dump(reg, open(ROOT / 'data' / 'registry.json', 'w'), ensure_ascii=False, indent=2)
        json.dump({'run_at': datetime.datetime.now(datetime.UTC).isoformat(), 'ruling': RULING,
                   'counts': {k: len(v) for k, v in out.items()}, **out},
                  open(a.report, 'w'), ensure_ascii=False, indent=1)
    for k, v in out.items():
        for x in v:
            print(k.upper()[:4], x)
    print({k: len(v) for k, v in out.items()})


if __name__ == '__main__':
    main()
