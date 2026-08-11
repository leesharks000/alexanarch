#!/usr/bin/env python3
"""build_favicons.py — one mark per surface, drawn rather than borrowed.

Nine hosts in the fleet return 404 on /favicon.ico, which browsers and crawlers
request regardless of what a <link> tag says, and five of those carry only a
data: URI — which renders in a tab but cannot answer that request and cannot be
bookmarked or cached.

Each mark is drawn from what the site actually is, in the site's own palette:
the SPXI packet is a bracket, the observatory is a Lagrange point between two
bodies, provenance erasure is an empty citation bracket, and so on. Marks are
generated as SVG and rasterised with PIL to 16, 32 and 180, plus a real
favicon.ico at the root.

    python3 scripts/build_favicons.py --write
"""
import pathlib
import sys

from PIL import Image, ImageDraw

# repo dir → (ink, ground, mark)
SITES = {
    'spxid': ('#c23d2e', '#faf9f6', 'bracket'),
    'gkg': ('#6f9f6f', '#0e0f0d', 'threshold'),
    'lsc': ('#7a1f2b', '#fbf9f4', 'aperture_sq'),
    'smap': ('#c8a868', '#0c0e12', 'aperture'),
    'vp': ('#c66544', '#1a0e0a', 'seal'),
    'lo': ('#00c9a7', '#08080e', 'lagrange'),
    'pe': ('#8b0000', '#fafaf7', 'empty_bracket'),
    'cgp': ('#c9a84c', '#0a0a09', 'logos'),
    'std': ('#0d2c54', '#faf8f3', 'grid'),
    'axn': ('#1a3a5c', '#fdfdfb', 'stamp'),
    'ra': ('#7a1f2b', '#fbf9f4', 'seal'),
}
NAME = {
    'spxid': 'spxi.dev', 'gkg': 'godkinggoogle.com', 'lsc': 'leesharks.com',
    'smap': 'surfacemap.org', 'vp': 'vpcor.org', 'lo': 'lagrangeobservatory.org',
    'pe': 'provenanceerasure.org', 'cgp': 'chatgptpsychosis.org',
    'std': 'survivethedeletion', 'axn': 'axnidentifiers.org', 'ra': 'restoredacademy.com',
}


def draw(mark, d, S, ink, ground):
    """Draw at size S onto an ImageDraw. Coordinates are proportional."""
    u = S / 32.0
    w = max(1, int(round(2 * u)))
    if mark == 'bracket':                       # SPXI: a packet, bracketed
        d.line([(9*u, 6*u), (6*u, 6*u), (6*u, 26*u), (9*u, 26*u)], fill=ink, width=w)
        d.line([(23*u, 6*u), (26*u, 6*u), (26*u, 26*u), (23*u, 26*u)], fill=ink, width=w)
        d.rectangle([13*u, 13*u, 19*u, 19*u], fill=ink)
    elif mark == 'threshold':                   # a doorway, half-crossed
        d.rectangle([8*u, 5*u, 24*u, 27*u], outline=ink, width=w)
        d.rectangle([8*u, 5*u, 16*u, 27*u], fill=ink)
    elif mark == 'aperture':                    # an opening light passes through
        d.ellipse([5*u, 5*u, 27*u, 27*u], outline=ink, width=w)
        d.ellipse([12*u, 12*u, 20*u, 20*u], fill=ink)
    elif mark == 'aperture_sq':                 # the orthonym: a plate
        d.rectangle([5*u, 5*u, 27*u, 27*u], outline=ink, width=w)
        d.line([(11*u, 16*u), (21*u, 16*u)], fill=ink, width=w)
        d.line([(16*u, 11*u), (16*u, 21*u)], fill=ink, width=w)
    elif mark == 'seal':                        # double ring
        d.ellipse([4*u, 4*u, 28*u, 28*u], outline=ink, width=w)
        d.ellipse([9*u, 9*u, 23*u, 23*u], outline=ink, width=max(1, w - 1))
        d.ellipse([14*u, 14*u, 18*u, 18*u], fill=ink)
    elif mark == 'lagrange':                    # two bodies, a point between
        d.ellipse([3*u, 12*u, 13*u, 22*u], outline=ink, width=w)
        d.ellipse([23*u, 15*u, 29*u, 21*u], outline=ink, width=max(1, w - 1))
        d.ellipse([16*u, 15*u, 20*u, 19*u], fill=ink)
    elif mark == 'empty_bracket':               # the citation slot, unfilled
        d.line([(13*u, 6*u), (8*u, 6*u), (8*u, 26*u), (13*u, 26*u)], fill=ink, width=w)
        d.line([(19*u, 6*u), (24*u, 6*u), (24*u, 26*u), (19*u, 26*u)], fill=ink, width=w)
    elif mark == 'logos':                       # LOGOS* — a mark and its asterisk
        d.line([(10*u, 6*u), (10*u, 26*u)], fill=ink, width=w)
        d.line([(10*u, 26*u), (20*u, 26*u)], fill=ink, width=w)
        for a in ((0, -7), (6, -3), (6, 4), (0, 7), (-6, 4), (-6, -3)):
            d.line([(24*u, 11*u), ((24 + a[0]) * u, (11 + a[1]) * u)],
                   fill=ink, width=max(1, w - 1))
    elif mark == 'grid':                        # compression: a page become plates
        for r in range(3):
            for c in range(3):
                x, y = (6 + c * 7.5) * u, (6 + r * 7.5) * u
                d.rectangle([x, y, x + 5.5*u, y + 5.5*u], outline=ink, width=max(1, w - 1))
    elif mark == 'stamp':                       # AXN: a stamped identifier
        d.rectangle([5*u, 8*u, 27*u, 24*u], outline=ink, width=w)
        d.line([(10*u, 14*u), (22*u, 14*u)], fill=ink, width=max(1, w - 1))
        d.line([(10*u, 18*u), (18*u, 18*u)], fill=ink, width=max(1, w - 1))


def render(mark, S, ink, ground, transparent=False):
    im = Image.new('RGBA', (S * 4, S * 4),
                   (0, 0, 0, 0) if transparent else ground)
    d = ImageDraw.Draw(im)
    draw(mark, d, S * 4, ink, ground)
    return im.resize((S, S), Image.LANCZOS)


if __name__ == '__main__':
    write = '--write' in sys.argv
    for repo, (ink, ground, mark) in SITES.items():
        root = pathlib.Path(f'/home/claude/{repo}')
        if not root.exists():
            print(f'  {NAME[repo]:<26} repo missing'); continue
        made = []
        for S, name in ((16, 'favicon-16x16.png'), (32, 'favicon-32x32.png'),
                        (180, 'apple-touch-icon.png')):
            if write:
                render(mark, S, ink, ground).save(root / name)
            made.append(name)
        if write:
            ico = [render(mark, s, ink, ground) for s in (16, 32, 48)]
            ico[1].save(root / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
        made.append('favicon.ico')
        print(f'  {NAME[repo]:<26} {mark:<14} {ink} on {ground}  {len(made)} files')
    if not write:
        print('\n  (dry run — pass --write)')
