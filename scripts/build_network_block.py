#!/usr/bin/env python3
"""build_network_block.py — one network block, generated, for every surface.

MANUS, 2026-08-10: the Aperture Atlas was missing from the network list on every
site while being the knowledge graph that maps the network. The map was not on
the map. It sits in data/fleet-domains.json — the canonical list — but the blocks
are hand-copied into each site, so nothing propagated.

This generates the block from two sources and APPENDS it between markers,
rewriting only what lies inside them:

  data/fleet-domains.json          the canonical 24 domains
  datasets/heteronyms/records/     who holds which institution

Attribution comes from the records rather than being typed, so when Vox, Glas,
Trace, Feist or Spellings get a record their sites gain their names here without
anyone editing HTML.

    python3 scripts/build_network_block.py                 # report + diff
    python3 scripts/build_network_block.py --apply PATH…   # write
"""
import glob
import json
import pathlib
import re
import sys

# COLOUR (2026-08-17). The block previously set colours as var(--accent,#1a3a5c) and
# var(--text-dim,#999). Most fleet sites define NEITHER variable, so both fell back to the
# literal — and four of the nine sites carrying this block are dark (#0a0a0a, #0a0a0c,
# #0c0e12, #1a0e0a), where a #1a3a5c heading is close to unreadable. The block now uses
# currentColor with opacity, so it inherits whatever palette the host page sets. This is the
# same rule the archive's derived figures already follow, and it should have been applied here
# first: a block generated once and applied everywhere cannot name colours.
ROOT = pathlib.Path(__file__).resolve().parents[1]
FLEET = ROOT / 'data/fleet-domains.json'
RECORDS = ROOT / 'datasets/heteronyms/records'
START = '<!-- FLEET-NETWORK-START generated from https://www.alexanarch.org/api/fleet.json -->'
ANY_START = re.compile(r'<!-- FLEET-NETWORK-START[^>]*-->')
END = '<!-- FLEET-NETWORK-END -->'

# The grouping is editorial and lives here rather than in the domain list,
# because a domain does not know which group it belongs to.
GROUPS = [
    ('Archive', ['alexanarch.org', 'axnidentifiers.org', 'persistentidentifiers.org',
                 'leesharks.com', 'provenanceerasure.org', 'machinemediation.org',
                 'surfacemap.org', 'survivethedeletion.vercel.app', 'godkinggoogle.com',
                 'crimsonhexagonal.org',
                 'traininglayerliterature.org']),
    ('Framework Sites', ['semanticphysics.org', 'semanticeconomy.org', 'spxi.dev',
                         'metadatapacket.dev', 'holographickernel.org', 'revelationfirst.com',
                         'laborvector.org', 'themandalaoracle.com', 'secretbookofwalt.org',
                         'watergiraffe.org', 'pessoagraph.org', 'chatgptpsychosis.org',
                         'operativesemiotics.org', 'livingarchitecturelab.org']),
    ('Heteronym Institutions', ['vpcor.org', 'lagrangeobservatory.org', 'restoredacademy.org',
                                'maryleelabor.org']),
]

# Attributions the records cannot supply: non-Dodecad figures.
EXTRA = {
    'watergiraffe.org': 'Yusef Kenning',
    'maryleelabor.org': 'Mary Lee',
    'surfacemap.org': 'the Aperture Atlas',
    # no custom domain was ever taken; the Vercel project IS the address,
    # and survivethedeletion.org returned nothing at all (curl 000).
    'survivethedeletion.vercel.app': 'no custom domain',
    'crimsonhexagonal.org': 'the interface',
    'restoredacademy.org': 'Johannes Sigil',
    'vpcor.org': 'Ayanna Vox',
    'lagrangeobservatory.org': 'Nobel Glas',
    'chatgptpsychosis.org': 'Jack Feist',
    'revelationfirst.com': 'Damascus Dancings',
    'godkinggoogle.com': 'Talos Morrow',
    'holographickernel.org': 'Sen Kuro',
    'semanticeconomy.org': 'Rex Fraction',
}


def holders():
    """domain → heteronym name, read from the records rather than typed."""
    out = {}
    for f in sorted(glob.glob(str(RECORDS / '*.json'))):
        d = json.loads(pathlib.Path(f).read_text())
        name = d.get('name')
        # ATTRIBUTION FOLLOWS THE INSTITUTION, NOT THE HOST. Reading the /who/
        # surface gave alexanarch.org -> Cranes because her page is hosted at
        # axnidentifiers and the record's URL was misread, and leesharks.com ->
        # Kuro from a provisional seating. A site belongs to the position whose
        # INSTITUTION it is, which is a different claim from where a page sits.
        inst = d.get('institution') or {}
        site = inst.get('site') if isinstance(inst, dict) else None
        if site:
            m = re.search(r'([a-z0-9.-]+\.[a-z]{2,})', site)
            if m:
                out.setdefault(m.group(1), name)
    return out


def build():
    """UNIFIED (2026-09-07, MANUS): one generator, one source. The block is rendered from
    data/api/fleet.json — Archive, Framework Sites, Heteronym Institutions, Allied Sites
    (with the standing forms corrected 2026-08-30), Machine Entry (OAI-PMH, AXN resolver,
    the Hugging Face dataset, the API), and the footer (blog · Academia.edu · Google Scholar
    · ORCID) — in the class-based markup chosen on 2026-08-21 (links take each site's own
    colour). The older inline-styled block and the hand-held Allied Sites sections that
    followed it on fleet sites (stale Enli form; doubled headers seen on lagrange, vpcor,
    watergiraffe, restoredacademy 2026-09-07) are replaced by apply()."""
    fj = json.loads((ROOT / 'data/api/fleet.json').read_text())
    parts = [START]
    for sec in fj.get('sections', []):
        title = sec.get('title') or sec.get('name') or ''
        items = sec.get('items') or sec.get('sites') or sec.get('domains') or []
        rows = []
        for it in items:
            href = it.get('url') or (('https://' + it['d'] + '/') if it.get('d') else None)
            label = it.get('label') or it.get('d') or ''
            if not href: continue
            note = it.get('note') or ''; desc = it.get('desc') or it.get('description') or ''
            rows.append(f'<div><a href="{href}">{label}</a>'
                        + (f' <span class="fl-n">({note})</span>' if note else '')
                        + (f'<span class="fl-d">{desc}</span>' if desc else '') + '</div>')
        cols = 1 if title == 'Allied Sites' else 2
        parts.append(f'<h4 class="fl-h">{title}</h4><div class="fl-g" style="grid-template-columns:repeat({cols},minmax(0,1fr))">' + ''.join(rows) + '</div>')
    parts.append('<h4 class="fl-h">Machine Entry</h4><div class="fl-g" style="grid-template-columns:repeat(1,minmax(0,1fr))">'
                 '<div><a href="https://www.alexanarch.org/oai?verb=Identify">OAI-PMH endpoint</a> <span class="fl-n">(harvestable metadata, 1,400+ records)</span></div>'
                 '<div><a href="https://www.alexanarch.org/resolve/">AXN resolver</a> <span class="fl-n">(content-derived identifiers)</span></div>'
                 '<div><a href="https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive">Hugging Face dataset</a> <span class="fl-n">(the archive as Parquet: deposits, captures, reception, predictions — rebuilt from the registry)</span></div>'
                 '<div><a href="https://datasets-server.huggingface.co/search?dataset=leesharks%2Fcrimson-hexagonal-archive&amp;config=deposits&amp;split=train&amp;query=Theophrastus&amp;length=5">full-text query endpoint</a> <span class="fl-n">(no auth, no client &mdash; swap the query term; config=citations for the edge list)</span></div>'
                 '<div><a href="https://www.alexanarch.org/api/search-index.json">API</a> <span class="fl-n">(search index · <a href="https://www.alexanarch.org/api/fleet.json">fleet.json</a> · <a href="https://www.alexanarch.org/api/body-shards/manifest.json">body shards</a>)</span></div></div>')
    parts.append('<div class="fl-f"><a href="https://mindcontrolpoems.blogspot.com">mindcontrolpoems.blogspot.com</a> &middot; '
                 '<a href="https://independent.academia.edu/LSharks">Academia.edu</a> &middot; '
                 '<a href="https://scholar.google.com/citations?user=Ws6IIcgAAAAJ">Google Scholar</a> &middot; '
                 '<a href="https://orcid.org/0009-0000-1599-0703">ORCID</a></div>')
    parts.append(END)
    fleet = {it.get('d') for sec in fj.get('sections', []) for it in (sec.get('items') or sec.get('sites') or sec.get('domains') or []) if it.get('d')}
    return ''.join(parts), fleet, {}


FLEETCSS = """<style id="fleetcss">
.fl-h{font-size:.78em;opacity:.72;margin:14px 15px 5px;text-transform:uppercase;letter-spacing:.05em;font-weight:500}
.fl-g{padding:0 15px;display:grid;column-gap:24px;row-gap:5px;font-size:.82em;line-height:1.7}
.fl-g a{color:var(--accent,inherit);text-decoration:none;border-bottom:1px solid currentColor;border-bottom-color:color-mix(in srgb,currentColor 34%,transparent);word-break:break-word}
.fl-g a:hover{border-bottom-color:#c9a227}
.fl-n{opacity:.6;font-size:.94em}
.fl-d{display:block;opacity:.6;font-size:.9em;line-height:1.5;margin-top:2px}
.fl-f{padding:12px 15px 4px;font-size:.75em;opacity:.55;border-top:1px dashed rgba(128,128,128,.28);margin-top:14px}
.fl-f a{color:var(--accent,inherit);text-decoration:none}
</style>"""

HAND_HELD_AFTER_END = re.compile(
    r'(?<=<!-- FLEET-NETWORK-END -->)\s*(?:<h4[^>]*>|<(?:strong|b)[^>]*>|<p[^>]*><(?:strong|b)>)\s*Allied Sites\s*(?:</h4>|</strong>|</b>|</b></p>|</strong></p>)'
    r'\s*(?:<div[^>]*>.*?</div>\s*)+?(?=\s*(?:<div[^>]*>\s*<a href="https://mindcontrolpoems|<p[^>]*>\s*<a href="https://mindcontrolpoems|<footer|<div class="mspcolophon|<div class="colophon|<div style="[^"]*font-size:0\.7|</body>))', re.S)
STALE_FOOTER_AFTER_END = re.compile(
    r'(?<=<!-- FLEET-NETWORK-END -->)\s*<div[^>]*>\s*<a href="https://mindcontrolpoems\.blogspot\.com"[^<]*</a>[^<]*(?:<a href="[^"]*(?:academia|scholar\.google|orcid\.org)[^"]*"[^<]*</a>[^<]*)*</div>', re.S)

def apply(paths, block):
    n = 0
    for path in paths:
        for p in sorted(pathlib.Path(path).rglob('*.html')):
            if '.git' in str(p) or 'node_modules' in str(p):
                continue
            s = p.read_text(errors='replace')
            if not ANY_START.search(s) or END not in s:
                continue
            s2 = re.sub(ANY_START.pattern + r'.*?' + re.escape(END), lambda m: block, s, flags=re.S)
            s2 = HAND_HELD_AFTER_END.sub('', s2)
            s2 = STALE_FOOTER_AFTER_END.sub('', s2)   # the block now carries the footer
            if 'id="fleetcss"' not in s2 and '</head>' in s2:
                s2 = s2.replace('</head>', FLEETCSS + '\n</head>', 1)
            if s2 != s:
                p.write_text(s2)
                n += 1
    return n


if __name__ == '__main__':
    block, fleet, who = build()
    print(f'  {len(fleet)} fleet domains rendered from data/api/fleet.json')
    if '--apply' in sys.argv:
        paths = [a for a in sys.argv[1:] if not a.startswith('--')]
        print(f'  written to {apply(paths, block)} page(s)')
    else:
        print('  dry run — pass --apply PATH... to write')
