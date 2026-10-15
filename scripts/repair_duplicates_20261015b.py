#!/usr/bin/env python3
"""repair_duplicates_20261015b.py — two more active duplicates made legible (triage 2026-10-15, in:duplicate).

  #1346 -> #630   RENDER UNTO CAESAR (EA-CAESURA-01a): byte-identical body, same date; #630 is the record of standing.
  #1330 -> #541   EA-ARK-EMOJI-01 GLYPHIC CHECKSUM: #1330's body is the stripped rendering of #541 (same v0.2, same
                  date; 0.76 of #1330's shingles in #541, its tables, lists and code missing).
Made what the archive makes every duplicate (#1138, #1181, #891…): SUPERSEDED duplicate witnesses pointing at the
record of standing, cite-instead banner, indexable. Bodies unchanged. Not changed: #63/#976 and #105/#1370 (bodies
overlap 0.17 and 0.44 — not shown to be one text).
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
ON = '2026-10-15'
RULING = 'Lee Sharks, 2026-10-15: "make sure youre not duplicating something that already exists elsewhere"; "lets proceed"'
DUP = {1346: (630, 'byte-identical body, same date'), 1330: (541, "stripped rendering of #541's text (tables, lists, code missing)")}
regp = ROOT / 'data/registry.json'; retp = ROOT / 'data/retired-records.json'
reg = json.loads(regp.read_text()); D = {d['deposit_number']: d for d in reg['deposits']}; ret = json.loads(retp.read_text())
for n, (t, why) in DUP.items():
    d, T = D[n], D[t]
    assert d['status'] == 'ACTIVE' and T['status'] == 'ACTIVE'
    was = {'status': d['status'], 'superseded_by_deposit_number': d.get('superseded_by_deposit_number')}
    d['status'] = 'SUPERSEDED'; d['superseded_by_deposit_number'] = t
    d['duplicate_note'] = f'DUPLICATE ({ON}): {why}; the record of standing is #{t}.'
    d['superseded_reason'] = f'Duplicate witness of the same work: the record of standing is #{t} ({why}).'
    d.setdefault('body_status', {})['retired'] = {'class': 'superseded', 'resolves_to': t, 'declared': ON, 'indexable': True,
        'ruled_by': RULING, 'note': ('Superseded, not a stub: indexable (ruling 2026-10-15). The page carries a banner before '
        'the body naming the current version to cite, and an axn:retired marker; its canonical is its own URL.')}
    rm.touch(d, 'status', f'duplicate of #{t} ({why}); made a superseded duplicate witness', was=was,
             now={'status': 'SUPERSEDED', 'superseded_by_deposit_number': t}, when=ON)
    ret['records'][str(n)] = {'class': 'superseded', 'resolves_to': t, 'title': T['title'], 'axn': T['axn'], 'declared': ON}
ret['count'] = len(ret['records'])
regp.write_text(json.dumps(reg, ensure_ascii=False, indent=2)); retp.write_text(json.dumps(ret, ensure_ascii=False, indent=2))
print('duplicates:', DUP, '| retired', ret['count'])
