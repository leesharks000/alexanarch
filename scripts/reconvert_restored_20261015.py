#!/usr/bin/env python3
"""reconvert_restored_20261015.py — re-convert today's restored texts so they carry the characters as published.

The restorations of 2026-10-15 converted each Blogger body with html2text at its default, under which entity-encoded
characters are replaced by ASCII stand-ins: "&#183;" became "*", "&mdash;" "--", curly quotes straight, accented
letters bare. #325 read "Exegetical map * Navigational infrastructure" where the post reads "Exegetical map ·
Navigational infrastructure". The repair standard is the text as published (Lee Sharks, 2026-10-15), so the
restored segment of each record is converted again with unicode_snob on (characters kept) and html2text's markdown
escapes dropped where the post has none (as fix_restored_md_escapes_20261015.py did for the escapes alone).

Only the restored segment is replaced: the provenance header and the retained appendix (non-destruction) are left
as they are; for #1025 (missing part) only the added part is. New hash, glyph and AXN in the same hex and family;
restoration.reconverted records the hash and AXN before.

    python3 scripts/reconvert_restored_20261015.py [--dry-run]
"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from restore_from_blog import fetch, extract_post
from restore_wrong_bodies import to_md, unescape          # unicode_snob on, escapes dropped
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

REPORTS = ['data/restoration-wrong-bodies-2026-10-15.json', 'data/restoration-wrong-bodies-2026-10-15b.json',
           'data/restoration-wrong-bodies-2026-10-15c.json']
APP = '\n\n---\n\n## Appendix — '


def main():
    dry = '--dry-run' in sys.argv
    reg = json.load(open(ROOT / 'data/registry.json')); D = {d['deposit_number']: d for d in reg['deposits']}
    done = []
    for rp in REPORTS:
        for e in json.load(open(ROOT / rp))['restored']:
            n, url = e['n'], e['url']; d = D[n]
            tp = ROOT / d['full_text_path'].lstrip('/'); t = tp.read_text(encoding='utf-8')
            _, body = extract_post(fetch(url).decode('utf-8', 'replace'))
            md = unescape(to_md(body or ''), body or '').strip()
            if (d.get('restoration') or {}).get('repair_kind') == 'missing_part':
                head, sep, part = t.rpartition('\n\n---\n\n## ')
                cut = part.find('\n\n') + 2
                new = head + sep + part[:cut] + md + '\n'
            else:
                a = t.find('\n\n---\n\n') + 7
                b = t.find(APP); b = b if b > 0 else len(t)
                new = t[:a] + md + t[b:]
            if new == t:
                continue
            done.append({'n': n, 'chars_before': len(t), 'chars_after': len(new)})
            if dry:
                continue
            tp.write_text(new, encoding='utf-8')
            h = hashlib.sha256(new.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
            d['restoration']['reconverted'] = {
                'on': '2026-10-15', 'hash_before': d['hash'], 'axn_before': d['axn'],
                'why': ('restored segment converted again with characters kept (html2text unicode_snob): the first '
                        'conversion had replaced entity-encoded characters with ASCII stand-ins')}
            d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
            d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
            d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
            d['body_status']['residual_chars'] = len(new)
    if not dry and done:
        json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)
    print(done)


if __name__ == '__main__':
    main()
