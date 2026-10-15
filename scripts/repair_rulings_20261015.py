#!/usr/bin/env python3
"""repair_rulings_20261015.py — two rulings of Lee Sharks, 2026-10-15 (ruling sheet, items 2 and 4).

2. "recompute." Six records whose registry hash (the AXN) was the hash of the SECOND store (data/deposits) while the
   page, PDF and index render the canonical text (registry full_text_path): #1204, #1250, #1344, #1382, #1383, #1521.
   (#1250 The reward of love: the page shows the poem, the AXN hashed a July restoration of the Ezra Pound post.)
   Each AXN is re-derived from the canonical text; the hash and AXN before are kept (axn_rederived).
4. "why not link to the relevant blog post generally?" Figures in #502, #507, #509 pointed at claude.ai/chat/<file>,
   which resolves for no reader (the posts carry the same links). Each figure becomes a link, under its own caption,
   to the post of the record's date, where the figures are hosted:
     #502 (2026-02-22) -> 2026/02/whose-face-is-on-twenty-curatorial.html
     #509 (2026-02-23) -> 2026/02/whose-face-is-on-twenty-curatorial_23.html
     #507 (2026-02-23) -> 2026/02/all-spoils-of-babylon-curatorial.html

    python3 scripts/repair_rulings_20261015.py --apply
"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = '2026-10-15'
BLOG = 'https://mindcontrolpoems.blogspot.com/'
RECOMPUTE = [1204, 1250, 1344, 1382, 1383, 1521]
FIG = {502: '2026/02/whose-face-is-on-twenty-curatorial.html', 509: '2026/02/whose-face-is-on-twenty-curatorial_23.html',
       507: '2026/02/all-spoils-of-babylon-curatorial.html'}
IMG = re.compile(r'!\[([^\]]*)\]\(https://claude\.ai/chat/[^)\s]+\)')


def reglyph(d, text):
    h = hashlib.sha256(text.encode('utf-8')).hexdigest(); g = axn_glyph_from_hash(h)
    before = {'hash': d.get('hash'), 'axn': d.get('axn')}
    d['hash'] = h; d['axn_canonical'] = h; d['emoji'] = g
    d['axn'] = compose_axn(d['hex'], d.get('family', 'ARCHIVAL'), g)
    d['clusters'] = axn_clusters_from_hash(h); d['reading'] = axn_reading_from_clusters(d['clusters'])
    return before


def main():
    if '--apply' not in sys.argv:
        print(__doc__); return
    reg = json.load(open(ROOT / 'data/registry.json')); D = {d['deposit_number']: d for d in reg['deposits']}
    for n in RECOMPUTE:
        d = D[n]; t = (ROOT / d['full_text_path'].lstrip('/')).read_text(encoding='utf-8')
        b = reglyph(d, t)
        d['axn_rederived'] = {'on': ON, 'from': d['full_text_path'], 'hash_before': b['hash'], 'axn_before': b['axn'],
                              'why': 'the stored hash was of the second store (data/deposits); the page renders this text',
                              'ruled_by': 'Lee Sharks, 2026-10-15: "recompute."'}
        rm.touch(d, 'axn', 'AXN re-derived from the canonical text the page renders (was the hash of the second store)',
                 was=b['axn'], now=d['axn'], when=ON)
        print('recomputed', n, b['axn'], '->', d['axn'])
    for n, post in FIG.items():
        d = D[n]; tp = ROOT / d['full_text_path'].lstrip('/'); t = tp.read_text(encoding='utf-8')
        new, k = IMG.subn(lambda m: f'[{m.group(1)}]({BLOG}{post})', t)
        if not k:
            continue
        tp.write_text(new, encoding='utf-8'); b = reglyph(d, new)
        d['links_repaired'] = {'on': ON, 'figures_linked_to_post': k, 'post': BLOG + post, 'hash_before': b['hash'],
                               'axn_before': b['axn'], 'ruled_by': 'Lee Sharks, 2026-10-15: "why not link to the relevant blog post generally?"'}
        rm.touch(d, 'body_status', f'{k} figure links (claude.ai/chat files) now link to the post of the record\'s date',
                 was={'axn': b['axn']}, now={'axn': d['axn']}, when=ON)
        print('figures', n, k)
    json.dump(reg, open(ROOT / 'data/registry.json', 'w'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
