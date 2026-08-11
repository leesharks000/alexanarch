#!/usr/bin/env python3
"""build_dodecad_graph.py — the Dodecad drawn from its own citation data.

Every diagram on the heteronym pages was hand-placed: I read the records and
decided what to draw. This one is DERIVED. Node size is citation in-degree,
edge weight is the number of position-level citations, and the layout is
ordered by in-degree so the archive's centre of gravity falls where the data
puts it rather than where I would.

Source: datasets/heteronyms/crosswalk.json, itself a join of the citation
graph (9,453 deposit edges collapsed to 1,910 position edges by creator
field), the lexical minting registry, the concept map and the wiki.

    python3 scripts/build_dodecad_graph.py            # report
    python3 scripts/build_dodecad_graph.py --write    # emit the SVG
"""
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / 'datasets/heteronyms/crosswalk.json'
OUT = ROOT / 'datasets/heteronyms/dodecad-graph.svg'

LABEL = {
    'johannes-sigil': 'Sigil', 'rex-fraction': 'Fraction', 'rebekah-cranes': 'Cranes',
    'damascus-dancings': 'Dancings', 'talos-morrow': 'Morrow', 'sen-kuro': 'Kuro',
    'sparrow-wells': 'Wells', 'ayanna-vox': 'Vox', 'ichabod-spellings': 'Spellings',
    'nobel-glas': 'Glas', 'orin-trace': 'Trace', 'jack-feist': 'Feist',
}
W, H = 880, 620
CX, CY, R = 440, 300, 232
MIN_EDGE = 12  # below this the graph becomes a hairball and says nothing


def layout(positions):
    """Rank by in-degree; place around a circle with the most-cited at top."""
    order = sorted(positions, key=lambda s: -positions[s]['citation_in_degree'])
    pts = {}
    n = len(order)
    for i, s in enumerate(order):
        a = -math.pi / 2 + (2 * math.pi * i / n)
        pts[s] = (CX + R * math.cos(a), CY + R * math.sin(a), a)
    return order, pts


def build():
    J = json.loads(CROSSWALK.read_text())
    P = J['positions']
    order, pts = layout(P)
    maxin = max(v['citation_in_degree'] for v in P.values()) or 1
    edges = []
    for s, v in P.items():
        for t, n in v['cites'].items():
            if n >= MIN_EDGE and t in pts:
                edges.append((s, t, n))
    edges.sort(key=lambda e: e[2])
    maxw = max((e[2] for e in edges), default=1)

    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img">',
           '<title>The Dodecad as a citation network</title>',
           '<desc>Twelve heteronymic positions. Node size is citation in-degree, edge '
           'thickness is the number of position-level citations. Derived from the archive\'s '
           'citation graph, not composed.</desc>',
           '<defs><marker id="dg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
           'markerHeight="5" orient="auto"><path d="M1 1L9 5L1 9" fill="none" '
           'stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></marker></defs>',
           '<g fill="none" stroke="currentColor">']
    for s, t, n in edges:
        x1, y1, _ = pts[s]
        x2, y2, _ = pts[t]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        r1 = 14 + 26 * (P[s]['citation_in_degree'] / maxin)
        r2 = 16 + 26 * (P[t]['citation_in_degree'] / maxin)
        sx, sy = x1 + dx / d * r1, y1 + dy / d * r1
        ex, ey = x2 - dx / d * r2, y2 - dy / d * r2
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        bx, by = mx + (CX - mx) * .18, my + (CY - my) * .18
        op = .12 + .5 * (n / maxw)
        sw = .5 + 3.2 * (n / maxw)
        out.append(f'<path d="M{sx:.0f} {sy:.0f} Q{bx:.0f} {by:.0f} {ex:.0f} {ey:.0f}" '
                   f'stroke-width="{sw:.2f}" opacity="{op:.2f}" marker-end="url(#dg)"/>')
    out.append('</g>')
    for s in order:
        x, y, a = pts[s]
        v = P[s]
        r = 14 + 26 * (v['citation_in_degree'] / maxin)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="currentColor" '
                   f'opacity="0.13"/>')
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="none" '
                   f'stroke="currentColor" stroke-width="1" opacity="0.55"/>')
        lx = x + math.cos(a) * (r + 26)
        ly = y + math.sin(a) * (r + 26)
        anch = 'middle' if abs(math.cos(a)) < .4 else ('start' if math.cos(a) > 0 else 'end')
        out.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anch}" font-size="13" '
                   f'fill="currentColor" font-family="var(--mono,monospace)">{LABEL[s]}</text>')
        out.append(f'<text x="{lx:.0f}" y="{ly + 15:.0f}" text-anchor="{anch}" font-size="9.5" '
                   f'fill="currentColor" opacity="0.6" font-family="var(--mono,monospace)">'
                   f'{v["citation_in_degree"]} cited &middot; {v["minted_term_count"]} terms</text>')
    out.append(f'<text x="{CX}" y="{CY - 8}" text-anchor="middle" font-size="11" '
               f'fill="currentColor" opacity="0.5" font-family="var(--mono,monospace)">'
               f'{sum(e[2] for e in edges):,} citations</text>')
    out.append(f'<text x="{CX}" y="{CY + 10}" text-anchor="middle" font-size="9" '
               f'fill="currentColor" opacity="0.4" font-family="var(--mono,monospace)">'
               f'edges below {MIN_EDGE} omitted</text>')
    out.append('</svg>')
    return '\n'.join(out), P, order, edges


if __name__ == '__main__':
    svg, P, order, edges = build()
    print(f'  {len(order)} nodes · {len(edges)} edges at or above {MIN_EDGE}')
    print(f'  ranked by in-degree: {", ".join(LABEL[s] for s in order)}')
    print(f'  heaviest: ' + ', '.join(
        f'{LABEL[a]}→{LABEL[b]} {n}' for a, b, n in sorted(edges, key=lambda e: -e[2])[:5]))
    if '--write' in sys.argv:
        OUT.write_text(svg)
        print(f'  written · {OUT} · {OUT.stat().st_size:,}b')
