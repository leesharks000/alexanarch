#!/usr/bin/env python3
"""build_citation_field.py — the whole archive, every edge, no threshold.

The Dodecad graph suppressed everything below weight 12 so it would read as a
diagram. This does the opposite: all 9,453 citation edges at deposit level,
1,447 deposits on the ring, nothing filtered. The density IS the picture —
where the archive cites itself hardest, the field goes solid.

Deposits are placed by number, so the ring runs roughly chronologically and
the visible chords are the places where late work reaches back to early work.
Colour is by the creator's position where one exists; the Sharks-signed
majority is drawn in the ground tone rather than assigned a colour it hasn't
earned.

    python3 scripts/build_citation_field.py --write
"""
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'datasets/heteronyms/citation-field.svg'
S = 1000
C = S / 2
R = 432

HUE = {
    'johannes-sigil': '#c2453a', 'rex-fraction': '#d08a2e', 'rebekah-cranes': '#5f8fb0',
    'damascus-dancings': '#c9a132', 'talos-morrow': '#6f9f6f', 'sen-kuro': '#8a6b9b',
    'sparrow-wells': '#3f9d8f', 'ayanna-vox': '#c66544', 'ichabod-spellings': '#7d8590',
    'nobel-glas': '#00a88c', 'orin-trace': '#8b3a4a', 'jack-feist': '#b8912f',
}
GROUND = '#6a6a7e'


def build():
    edges = json.loads((ROOT / 'data/citation-graph.json').read_text())['edges']
    own = {int(k): v for k, v in json.loads(
        (ROOT / 'datasets/heteronyms/crosswalk.json').read_text()).get('_own', {}).items()} \
        if False else None
    reg = json.loads((ROOT / 'data/registry.json').read_text())['deposits']
    import re
    NAMES = {'Sigil': 'johannes-sigil', 'Cranes': 'rebekah-cranes', 'Fraction': 'rex-fraction',
             'Dancings': 'damascus-dancings', 'Morrow': 'talos-morrow', 'Kuro': 'sen-kuro',
             'Wells': 'sparrow-wells', 'Vox': 'ayanna-vox', 'Spellings': 'ichabod-spellings',
             'Glas': 'nobel-glas', 'Trace': 'orin-trace', 'Feist': 'jack-feist'}
    own = {}
    nums = []
    for d in reg:
        n = d['deposit_number']
        nums.append(n)
        c = str(d.get('creator') or '')
        for k, s in NAMES.items():
            if re.search(rf'\b{k}\b', c):
                own[n] = s
                break
    nums.sort()
    idx = {n: i for i, n in enumerate(nums)}
    N = len(nums)

    def pt(n):
        a = -math.pi / 2 + 2 * math.pi * idx[n] / N
        return C + R * math.cos(a), C + R * math.sin(a)

    drawn = []
    for e in edges:
        s, t = e.get('source_deposit'), e.get('target_deposit')
        if s not in idx or t not in idx or s == t:
            continue
        x1, y1 = pt(s)
        x2, y2 = pt(t)
        # pull the chord toward centre by how far apart the endpoints are:
        # near neighbours stay at the rim, distant reaches cross the middle
        gap = abs(idx[s] - idx[t]) / N
        gap = min(gap, 1 - gap) * 2
        k = 0.06 + 0.86 * gap
        bx, by = x1 + (C - x1) * k, y1 + (C - y1) * k
        bx2, by2 = x2 + (C - x2) * k, y2 + (C - y2) * k
        col = HUE.get(own.get(s), GROUND)
        op = 0.055 if own.get(s) is None else 0.16
        drawn.append(f'<path d="M{x1:.1f} {y1:.1f} C{bx:.1f} {by:.1f} {bx2:.1f} {by2:.1f} '
                     f'{x2:.1f} {y2:.1f}" fill="none" stroke="{col}" stroke-width="0.5" '
                     f'opacity="{op}"/>')

    rim = []
    for n in nums:
        x, y = pt(n)
        s = own.get(n)
        rim.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.9 if s else 1.0}" '
                   f'fill="{HUE.get(s, GROUND)}" opacity="{0.85 if s else 0.3}"/>')

    key = []
    for i, (s, col) in enumerate(HUE.items()):
        x = 40 + (i % 4) * 232
        y = S - 74 + (i // 4) * 20
        key.append(f'<circle cx="{x}" cy="{y - 4}" r="4" fill="{col}"/>'
                   f'<text x="{x + 12}" y="{y}" font-size="11" fill="{GROUND}" '
                   f'font-family="var(--mono,monospace)">{s.split("-")[-1]}</text>')

    return (f'<svg viewBox="0 0 {S} {S}" xmlns="http://www.w3.org/2000/svg" role="img">'
            '<title>The citation field: every edge in the archive</title>'
            f'<desc>{len(drawn):,} citation edges among {N:,} deposits, unfiltered. Chords '
            'reaching across the centre are late work citing early work. Colour is the '
            'creator\'s heteronymic position; deposits signed by the orthonym are drawn in the '
            'ground tone.</desc>'
            + ''.join(drawn) + ''.join(rim)
            + f'<text x="{C}" y="{C - 6}" text-anchor="middle" font-size="15" fill="{GROUND}" '
              f'opacity="0.75" font-family="var(--mono,monospace)">{len(drawn):,} citations</text>'
            + f'<text x="{C}" y="{C + 16}" text-anchor="middle" font-size="11" fill="{GROUND}" '
              f'opacity="0.5" font-family="var(--mono,monospace)">{N:,} deposits · nothing '
              f'filtered</text>'
            + ''.join(key) + '</svg>'), len(drawn), N, own


if __name__ == '__main__':
    svg, ne, nd, own = build()
    print(f'  {ne:,} edges · {nd:,} deposits · {len(own)} attributed to a position')
    if '--write' in sys.argv:
        OUT.write_text(svg)
        print(f'  written · {OUT.stat().st_size:,}b')
