#!/usr/bin/env python3
"""repair_restorations_20261015.py — apply the verified restore readings RQ01–RQ03 (data/repair-maps/readings/).

Each restoration is content copied verbatim from the published post (checked: verify_repair_reading.py, the
<batch>.verified.json files; every `content` occurs in its source at its source_lines). Applied bottom-up so line
numbers stay those the reader read. A replacement swaps the damaged span; an insertion goes after the line named,
with a blank line either side where the neighbours are not blank.

Left on purpose:
  #1165 — the poems are on no blog post (the post both stores cite as "recovery source" is the companion analysis,
          seated as #1165's neighbour #562); the reader's spans come from the second store, not from published text,
          so the repair standard (the text as published) cannot be checked. Kept as the call of 2026-10-15 ("leave").
  #545 as_published · #1047, #1411 no_defect.
Duplicate: #1372 -> #103 (RQ03), made a superseded duplicate witness, the archive's form for every duplicate.
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from repair_from_readings_20261015 import reglyph, ON

SKIP = {1165}
RULING = ('Lee Sharks, 2026-10-15: repair "broken, missing, and mislabelled files / and citations"; readers "long as '
          'they have provenance" — data/repair-maps/readings/')


def apply(lines, R):
    def key(r):
        sd = r.get('seated_lines')
        return (sd[0], 1) if sd else (r['after_line'] + 1, 0)
    for r in sorted(R, key=key, reverse=True):
        new = r['content'].split('\n')
        sd = r.get('seated_lines')
        if sd:
            lines[sd[0] - 1:sd[1]] = new
        else:
            i = r['after_line']
            if i < len(lines) and lines[i].strip():
                new = new + ['']
            if i > 0 and lines[i - 1].strip():
                new = [''] + new
            lines[i:i] = new
    return lines


def main():
    p = ROOT / 'data/registry.json'; reg = json.load(open(p)); D = {d['deposit_number']: d for d in reg['deposits']}
    ret = json.load(open(ROOT / 'data/retired-records.json')); done = []
    for b in ('RQ01', 'RQ02', 'RQ03'):
        ver = json.load(open(ROOT / f'data/repair-maps/readings/{b}.verified.json'))
        fails = {c['deposit']: [x for x in c['fails'] if x.startswith(('RESTORE', 'QUOTE', 'VERDICT'))] for c in ver['checks']}
        for e in json.load(open(ROOT / f'data/repair-maps/readings/{b}.json'))['deposits']:
            n = int(e['deposit']); d = D[n]
            if e['verdict'] == 'duplicate_of':
                t = int(e['target']); T = D[t]
                if d['status'] != 'ACTIVE' or T['status'] != 'ACTIVE':
                    continue
                was = {'status': d['status'], 'superseded_by_deposit_number': d.get('superseded_by_deposit_number')}
                d['status'] = 'SUPERSEDED'; d['superseded_by_deposit_number'] = t
                d['duplicate_note'] = f'DUPLICATE ({ON}, reading {b}): the record of standing is #{t}. {e["note"][:240]}'
                d['superseded_reason'] = f'Duplicate witness of the same work: the record of standing is #{t}.'
                d.setdefault('body_status', {})['retired'] = {'class': 'superseded', 'resolves_to': t, 'declared': ON,
                    'indexable': True, 'ruled_by': RULING, 'note': ('Superseded, not a stub: indexable (ruling 2026-10-15). '
                    'The page carries a banner before the body naming the current version to cite, and an axn:retired '
                    'marker; its canonical is its own URL.')}
                rm.touch(d, 'status', f'duplicate of #{t} (reading {b}); made a superseded duplicate witness', was=was,
                         now={'status': 'SUPERSEDED', 'superseded_by_deposit_number': t}, when=ON)
                ret['records'][str(n)] = {'class': 'superseded', 'resolves_to': t, 'title': T['title'], 'axn': T['axn'], 'declared': ON}
                done.append(('duplicate', n)); continue
            if e['verdict'] != 'restore_sections' or n in SKIP:
                continue
            assert not fails.get(n), (n, fails[n])
            tp = ROOT / d['full_text_path'].lstrip('/'); t = tp.read_text(encoding='utf-8')
            new = '\n'.join(apply(t.split('\n'), e['restorations']))
            if new == t:
                continue
            tp.write_text(new, encoding='utf-8'); bf = reglyph(d, new)
            what = (f'{len(e["restorations"])} spans lost in conversion restored verbatim from the published post '
                    f'(reading {b}, verified)')
            d.setdefault('readings_repaired', []).append({'on': ON, 'what': what, 'hash_before': bf['hash'], 'axn_before': bf['axn']})
            rm.touch(d, 'body_status', what, was={'axn': bf['axn']}, now={'axn': d['axn']}, when=ON)
            done.append(('restore', n))
    ret['count'] = len(ret['records'])
    json.dump(ret, open(ROOT / 'data/retired-records.json', 'w'), ensure_ascii=False, indent=2)
    s = json.dumps(reg, ensure_ascii=False, indent=2); p.write_text(s)
    print(done)


if __name__ == '__main__':
    main()
