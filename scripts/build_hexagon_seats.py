#!/usr/bin/env python3
"""build_hexagon_seats.py — which room of the Crimson Hexagon seats each record, from the interface's canonical data.

WHY (2026-10-16). crimsonhexagonal.org's room pages link to the alexanarch records they seat; no alexanarch record
page linked back, and no alexanarch page listed the rooms. Lee Sharks: "we could instead prepare indexes connecting
crimsonhexagonal rooms to alexanarch records and vice versa". This file is the one source both directions read:
the record page's seat line (wire_deposit.py) and the rooms index /s/rooms/ (scripts/build_rooms_index.py).

Source: hexagon_canonical.json of leesharks000/crimson-hexagonal-interface (documents → rooms, with the assignment
recorded there: heuristic / reviewed / declared), and its public/rooms and public/works trees for the addresses.
Versions mapped to one AXN are merged (one record, the union of their seats).

    python3 scripts/build_hexagon_seats.py --interface ../crimson-hexagonal-interface
"""
import html, json, os, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = 'https://www.crimsonhexagonal.org'


def main():
    it = pathlib.Path(sys.argv[sys.argv.index('--interface') + 1])
    canon = json.load(open(it / 'hexagon_canonical.json'))
    reg = json.load(open(ROOT / 'data/registry.json')); H = {d['hex']: d for d in reg['deposits']}
    rooms = {}
    for r in canon['rooms']:
        slug = (r.get('page_url') or '').rstrip('/').split('/')[-1]
        p = it / 'public/rooms' / slug / 'index.html'
        if not slug or not p.exists():
            continue
        s = p.read_text(encoding='utf-8')
        name = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))).strip()
        m = re.search(r'Address: ([A-Z]:[a-z]+\.[0-9A-Za-z.-]+)', s)
        rooms[r['id']] = {'id': r['id'], 'locus': m.group(1) if m else r.get('hex_address') or r['id'], 'name': name,
                          'hex_address': r.get('hex_address'), 'url': f'{SITE}/rooms/{slug}', 'physics': r.get('physics'),
                          'desc': r.get('desc'), 'prompt': r.get('prompt'), 'cat': r.get('cat')}
    works = {x.upper() for x in os.listdir(it / 'public/works') if (it / 'public/works' / x / 'index.html').exists()}
    seats = {}
    for x in canon['documents']:
        a = x.get('axn') or ''
        if not a.startswith('AXN:') or a[4:8] not in H:
            continue
        d = H[a[4:8]]; n = str(d['deposit_number'])
        e = seats.setdefault(n, {'hex': d['hex'], 'rooms': [], 'assignment': x.get('assignment'),
                                 'works_url': f"{SITE}/works/{d['hex'].lower()}" if d['hex'] in works else None})
        for r in x.get('rooms') or []:
            if r in rooms and r not in e['rooms']:
                e['rooms'].append(r)
    seats = {n: e for n, e in seats.items() if e['rooms']}
    out = {'what': ('Records of the alexanarch registry seated in rooms of the Crimson Hexagon (crimsonhexagonal.org), from '
                    'the interface\'s hexagon_canonical.json; assignment as recorded there. Read by the record pages and /s/rooms/.'),
           'generated': '2026-10-16', 'rooms': rooms, 'seats': seats}
    (ROOT / 'data/hexagon-seats.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{len(seats)} records seated in {len({r for e in seats.values() for r in e["rooms"]})} rooms; '
          f'{sum(1 for e in seats.values() if e["works_url"])} with a works page')


if __name__ == '__main__':
    main()
