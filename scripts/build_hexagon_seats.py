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
        if not slug or not p.exists():                       # a locus without a room page (the arks, two shadows): named, unlinked
            rooms[r['id']] = {'id': r['id'], 'locus': r.get('hex_address') or r['id'], 'name': r['name'], 'hex_address': r.get('hex_address'),
                              'url': None, 'physics': r.get('physics'), 'desc': r.get('desc'), 'prompt': r.get('prompt'), 'cat': r.get('cat')}
            continue
        s = p.read_text(encoding='utf-8')
        name = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))).strip()
        m = re.search(r'Address: ([A-Z]:[a-z]+\.[0-9A-Za-z.-]+)', s)
        rooms[r['id']] = {'id': r['id'], 'locus': m.group(1) if m else r.get('hex_address') or r['id'], 'name': name,
                          'hex_address': r.get('hex_address'), 'url': f'{SITE}/rooms/{slug}', 'physics': r.get('physics'),
                          'desc': r.get('desc'), 'prompt': r.get('prompt'), 'cat': r.get('cat')}
    # 2026-10-16 RULINGS (data/room-readings/rulings-applied-2026-10-16.json): loci the room belt does not hold — the
    # transversal structures (Armature, Secret Name, Pearl) and UMBML, "a meta structure of cha" — and notes on loci.
    RP = ROOT / 'data/room-readings/rulings-applied-2026-10-16.json'
    RU = json.load(open(RP)) if RP.exists() else {}
    for L in RU.get('loci', []):
        rooms[L['id']] = {'id': L['id'], 'locus': L['id'], 'name': L['name'], 'hex_address': None, 'url': L['url'],
                          'physics': None, 'desc': L['desc'], 'prompt': None, 'cat': 'structure', 'type': L['type'],
                          'ruling': {'clause': L['clause'], 'by': RU['ruled_by']}}
    for rid, nt in (RU.get('locus_notes') or {}).items():
        if rid in rooms:
            rooms[rid]['note'] = dict(nt, by=RU['ruled_by'])
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
            if r in rooms:
                e.setdefault('sources', {}).setdefault(r, []).append(f"canonical ({x.get('assignment') or 'unrecorded'})")
    # 2026-10-16 (Lee Sharks: "the l body has a whole standalone page with seated text on crimsonhexagonal"): the room
    # pages seat works the canonical document list does not — the constituting documents of R:r.36 The Λ-Body, Ruby
    # Moot, Pergamum and the rest (322 seats on 294 records). Every record link on a room page, outside the adjacency
    # and surface-map sections, is a seat; its section heading gives its role.
    pages = {r['id']: it / 'public/rooms' / (r.get('page_url') or '').rstrip('/').split('/')[-1] / 'index.html'
             for r in canon['rooms'] if (r.get('page_url') or '').rstrip('/')}
    for L in RU.get('loci', []):                             # the structure pages seat their constituting work the same way
        pages[L['id']] = it / 'public' / L['url'].split('crimsonhexagonal.org/')[1] / 'index.html'
    for rid, p in pages.items():
        if rid not in rooms or not p.exists():
            continue
        page = p.read_text(encoding='utf-8')
        page = re.sub(r'<!-- ROOM-READING:BEGIN -->.*?<!-- ROOM-READING:END -->', '', page, flags=re.S)   # the reading's own projection
        for sec in re.split(r'<h2>', page)[1:]:
            head = html.unescape(re.sub(r'<[^>]+>', '', sec.split('</h2>')[0])).strip()
            if re.search(r'Adjacent|Surface Map|Generated attribution', head):
                continue
            role = 'constituting' if re.search(r'Constituting|Core documents|in full|constituting|Chain documents|Anatomy', head) else 'in the room'
            for n in dict.fromkeys(re.findall(r'alexanarch\.org/s/records/(\d+)/', sec)):
                d = next((x for x in reg['deposits'] if str(x['deposit_number']) == n), None)
                if not d:
                    continue
                e = seats.setdefault(n, {'hex': d['hex'], 'rooms': [], 'assignment': 'room page',
                                         'works_url': f"{SITE}/works/{d['hex'].lower()}" if d['hex'] in works else None})
                e.setdefault('roles', {})
                if rid not in e['rooms']:
                    e['rooms'].append(rid)
                if e['roles'].get(rid) != 'constituting':
                    e['roles'][rid] = role
                src = e.setdefault('sources', {}).setdefault(rid, [])
                if 'room page' not in src:
                    src.append('room page')
    # 2026-10-16 ROOM READING (Lee Sharks: "the deposits need to be all related to the respective rooms they develop in
    # crimson hexagon … this is an interpretive read"). 16 readers, every ACTIVE record, each seat with a relation, a
    # confidence and a verbatim basis checked at its lines (data/room-readings/, scripts/apply_room_readings.py).
    # High and medium seats are seats; low seats (fit by family resemblance only) are kept as proposals, not shown.
    rp = ROOT / 'data/room-readings/seats-read-2026-10-16.json'
    if rp.exists():
        for n, ss in json.load(open(rp))['seats'].items():
            d = next((x for x in reg['deposits'] if str(x['deposit_number']) == n), None)
            if not d:
                continue
            e = seats.setdefault(n, {'hex': d['hex'], 'rooms': [], 'assignment': 'read 2026-10-16',
                                     'works_url': f"{SITE}/works/{d['hex'].lower()}" if d['hex'] in works else None})
            for x in sorted(ss, key=lambda x: not x['primary']):
                if x['locus'] not in rooms:
                    continue
                if x['confidence'] == 'low':
                    e.setdefault('proposed', []).append({k: x[k] for k in ('locus', 'relation', 'basis', 'batch')}); continue
                if x['locus'] not in e['rooms']:
                    e['rooms'].append(x['locus'])
                e.setdefault('read', {})[x['locus']] = {k: x[k] for k in ('relation', 'confidence', 'primary', 'basis', 'batch')}
                src = e.setdefault('sources', {}).setdefault(x['locus'], [])
                if 'read 2026-10-16' not in src:
                    src.append('read 2026-10-16')
                if x['relation'] == 'constitutes':
                    e.setdefault('roles', {})[x['locus']] = 'constituting'
    # 2026-10-16 RULINGS, applied over the reading. Moves first (the Encyclotron, R:r.15 → R:r.05: only a seat the reading
    # alone gave is moved), then ruled seats. A ruled primary seat takes the primary flag from the reader's.
    by_n = {str(d['deposit_number']): d for d in reg['deposits']}
    for mv in RU.get('moves', []):
        for n in map(str, mv['deposits']):
            e = seats.get(n)
            if not e:
                continue
            e['proposed'] = [x for x in e.get('proposed', []) if x['locus'] != mv['from']]
            src = (e.get('sources') or {}).get(mv['from'], [])
            x = (e.get('read') or {}).get(mv['from'])
            if x and src == ['read 2026-10-16']:
                e['read'].pop(mv['from']); e['sources'].pop(mv['from']); e['rooms'].remove(mv['from'])
                (e.get('roles') or {}).pop(mv['from'], None)
                if mv['to'] not in e['read']:
                    e['read'][mv['to']] = dict(x, batch=f"{x['batch']}; moved {mv['from']} → {mv['to']} by ruling 2026-10-16")
                    if mv['to'] not in e['rooms']:
                        e['rooms'].append(mv['to'])
                    e['sources'].setdefault(mv['to'], []).append('ruled 2026-10-16')
                e.setdefault('moved', []).append({'from': mv['from'], 'to': mv['to'], 'clause': mv['clause']})
    for g in RU.get('seats', []):
        for n in map(str, g['deposits']):
            d = by_n[n]
            e = seats.setdefault(n, {'hex': d['hex'], 'rooms': [], 'assignment': 'ruled 2026-10-16',
                                     'works_url': f"{SITE}/works/{d['hex'].lower()}" if d['hex'] in works else None})
            rd = e.setdefault('read', {})
            if g['primary']:
                for x in rd.values():
                    x['primary'] = False
            prev = rd.get(g['locus'])
            rd[g['locus']] = {'relation': g['relation'], 'confidence': 'ruled', 'primary': g['primary'] or bool(prev and prev.get('primary')),
                              'basis': {'ruling': RU['ruled_by'], 'group': g['group']}, 'batch': 'ruled 2026-10-16'}
            if g['locus'] not in e['rooms']:
                e['rooms'].append(g['locus'])
            e['proposed'] = [x for x in e.get('proposed', []) if x['locus'] != g['locus']]
            src = e.setdefault('sources', {}).setdefault(g['locus'], [])
            if 'ruled 2026-10-16' not in src:
                src.append('ruled 2026-10-16')
            if g['relation'] == 'constitutes':
                e.setdefault('roles', {})[g['locus']] = 'constituting'
    # Low seats are kept and shown in the index, marked for later adjudication (ruling 2026-10-16); a record seated only
    # at low confidence stays in the file with no rooms.
    seats = {n: e for n, e in seats.items() if e['rooms'] or e.get('proposed')}
    out = {'what': ('Records of the alexanarch registry seated in rooms of the Crimson Hexagon (crimsonhexagonal.org), from '
                    'the interface\'s hexagon_canonical.json; assignment as recorded there. Read by the record pages and /s/rooms/.'),
           'generated': '2026-10-16', 'rooms': rooms, 'seats': seats}
    (ROOT / 'data/hexagon-seats.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{len(seats)} records seated in {len({r for e in seats.values() for r in e["rooms"]})} rooms; '
          f'{sum(1 for e in seats.values() if e["works_url"])} with a works page')


if __name__ == '__main__':
    main()
