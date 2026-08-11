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

ROOT = pathlib.Path(__file__).resolve().parents[1]
FLEET = ROOT / 'data/fleet-domains.json'
RECORDS = ROOT / 'datasets/heteronyms/records'
START = '<!-- FLEET-NETWORK-START generated from data/fleet-domains.json -->'
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
                         'watergiraffe.org', 'pessoagraph.org', 'chatgptpsychosis.org']),
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
    fleet = set(json.loads(FLEET.read_text()))
    who = {**holders(), **EXTRA}
    grouped = {d for _, ds in GROUPS for d in ds}
    ungrouped = sorted(fleet - grouped)
    parts = [START]
    # ALLIED SITES IS NOT GENERATED. It carries people rather than fleet
    # domains — Alice Thornburgh, Florian Morin, Enli Lucente's Strutturista
    # della Psiche — plus profile links. A first pass regenerated it from the
    # domain list and DELETED all of that. The generator writes the three
    # canonical groups; Allied Sites stays hand-held.
    for label, domains in GROUPS:
        parts.append(
            f'<h4 style="font-size:0.78em;color:var(--accent,#1a3a5c);margin:10px 15px 4px 15px;'
            f'text-transform:uppercase;letter-spacing:0.04em;font-weight:500">{label}</h4>')
        parts.append('<div style="padding:0 15px;display:grid;'
                     'grid-template-columns:repeat(2,minmax(0,1fr));column-gap:24px;row-gap:4px;'
                     'font-size:0.82em;line-height:1.7">')
        for d in domains:
            if d not in fleet:
                continue
            tag = who.get(d)
            parts.append(
                f'<div><a href="https://{d}/">{d}</a>'
                + (f' <span style="color:var(--text-dim,#999)">({tag})</span>' if tag else '')
                + '</div>')
        parts.append('</div>')
    parts.append(END)
    return '\n'.join(parts), fleet, who


def apply(paths, block):
    n = 0
    for path in paths:
        for p in sorted(pathlib.Path(path).rglob('*.html')):
            if '.git' in str(p):
                continue
            s = p.read_text(errors='replace')
            if START in s:
                s2 = re.sub(re.escape(START) + r'.*?' + re.escape(END), block, s, flags=re.S)
            elif 'Crimson Hexagonal Archive — Network' in s:
                m = re.search(r'(Crimson Hexagonal Archive — Network</h3>\s*'
                              r'<div[^>]*>[^<]*</div>)', s)
                if not m:
                    continue
                tail = re.search(r'<h4[^>]*>\s*Archive\s*</h4>', s[m.end():])
                if not tail:
                    continue
                # stop at Allied Sites where present, so it is never touched
                stop = s.find('<h4', m.end())
                allied = re.search(r'<h4[^>]*>\s*Allied Sites\s*</h4>', s[m.end():])
                stop = m.end() + allied.start() if allied else s.find(
                    '<div class="mspcolophon', m.end())
                if stop < 0:
                    stop = s.find('</body>', m.end())
                s2 = s[:m.end()] + '\n' + block + '\n' + s[stop:]
            else:
                continue
            if s2 != s:
                p.write_text(s2)
                n += 1
    return n


if __name__ == '__main__':
    block, fleet, who = build()
    grouped = {d for _, ds in GROUPS for d in ds}
    print(f'  {len(fleet)} canonical domains · {len(grouped & fleet)} grouped · '
          f'{len(fleet - grouped)} allied')
    print(f'  in GROUPS but NOT canonical: {sorted(grouped - fleet) or "none"}')
    print(f'  attributions from records: '
          f'{ {k: v for k, v in who.items() if k not in EXTRA} }')
    if '--apply' in sys.argv:
        paths = [a for a in sys.argv[1:] if not a.startswith('--')]
        print(f'  written to {apply(paths, block)} page(s)')
