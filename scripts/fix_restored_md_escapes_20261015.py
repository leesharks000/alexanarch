#!/usr/bin/env python3
"""fix_restored_md_escapes_20261015.py — remove the converter's markdown escapes from bodies restored 2026-10-15.

restore_wrong_bodies.py converts the Blogger body with html2text, which escapes characters that would otherwise
start markdown syntax ("0\\." so a numbered heading is not read as a list, "tō \\+ inflected", "\\-"). The record
renderer does not read markdown escapes, so the backslash is shown to the reader as text: "☀️ \\+ 🌙". The repair
standard is the text as published (Lee Sharks, 2026-10-15), and the published post has no backslash there.

For each record named in the 2026-10-15 restoration reports, inside the RESTORED text only (the provenance header
and the retained appendix are not touched): every backslash-escape \\X (X one of + - . * _ # ! [ ] ( ) ` > | ~) is
removed when the published post's own text (data/blog-index.json) does not contain that two-character sequence.
New hash, glyph and AXN in the same hex and family; the restoration dict records the hash and AXN before.
Restore_wrong_bodies.py now applies the same step at conversion, so later runs do not need this.

    python3 scripts/fix_restored_md_escapes_20261015.py [--dry-run]
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn
import hashlib

ESC = re.compile(r'\\([+\-.*_#!\[\]()`>|~])')
REPORTS = ['data/restoration-wrong-bodies-2026-10-15.json', 'data/restoration-wrong-bodies-2026-10-15b.json',
           'data/restoration-wrong-bodies-2026-10-15c.json']


def unescape(md, published):
    """drop html2text's escapes that the published text does not carry"""
    return ESC.sub(lambda m: m.group(0) if m.group(0) in published else m.group(1), md)


def main():
    dry = '--dry-run' in sys.argv
    reg = json.load(open(ROOT / 'data/registry.json'))
    D = {d['deposit_number']: d for d in reg['deposits']}
    B = {p['url']: p['text'] for p in json.load(open(ROOT / 'data/blog-index.json'))['posts']}
    done = []
    for rp in REPORTS:
        if not (ROOT / rp).exists():
            continue
        for e in json.load(open(ROOT / rp))['restored']:
            n, url = e['n'], e['url']
            d = D[n]; tp = ROOT / d['full_text_path'].lstrip('/')
            t = tp.read_text(encoding='utf-8')
            pub = B.get(url, '')
            if d.get('restoration', {}).get('repair_kind') == 'missing_part':
                head, sep, part = t.rpartition('\n\n---\n\n## ')
                cut = part.find('\n\n') + 2
                new = head + sep + part[:cut] + unescape(part[cut:], pub)
            else:
                a = t.find('\n\n---\n\n') + 7
                b = t.find('\n\n---\n\n## Appendix — ')
                b = b if b > 0 else len(t)
                new = t[:a] + unescape(t[a:b], pub) + t[b:]
            k = len(ESC.findall(t)) - len(ESC.findall(new))
            if not k:
                continue
            done.append({'n': n, 'escapes_removed': k})
            if dry:
                continue
            tp.write_text(new, encoding='utf-8')
            h = hashlib.sha256(new.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
            rs = d['restoration']
            rs['escape_fix'] = {'on': '2026-10-15', 'escapes_removed': k, 'hash_before': d['hash'], 'axn_before': d['axn'],
                                'why': "html2text's markdown escapes removed where the published post does not carry them; "
                                       "the renderer showed them as literal backslashes"}
            d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
            d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
            d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
            d['body_status']['residual_chars'] = len(new)
    if not dry and done:
        json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)
    print(done)


if __name__ == '__main__':
    main()
