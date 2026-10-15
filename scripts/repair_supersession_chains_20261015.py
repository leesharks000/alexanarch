#!/usr/bin/env python3
"""repair_supersession_chains_20261015.py — every superseded edition points at its current edition, in one hop.

check_supersession_terminal.py reported 15 forward pointers that lead to an edition which is itself superseded
(a CHAIN: the reader who follows one pointer is still stale), one of them a LOOP. Broken pointers are in the scope
of record repair (Lee Sharks, 2026-10-15: "broken, missing, and mislabelled files / and citations").

  #11, #327, #363 -> #385 -> #31     DOI Registry v5.0/v2.0/v3.0: pointed at v6, now at #31 (v7.0, the terminal)
  #364, #386     -> #1129 -> #30     Fractal Navigation Map v5.0/v5.3: now at #30 (the terminal)
  #1115 -> #334 -> #1653, #1117 -> #333 -> #1652, #1118 -> #332 -> #1651
                                     the three Mantle Specifications: now at the current mantle objects
  #1546 -> #1551 -> #1552            When Suppression Becomes Expensive: now at #1552
  #1648 -> #1654 -> #1681            SPXI ≠ AEO: now at #1681
  #1664 -> #1665 -> #1671            The Negative of the Negative, v2: now at #1671
  #1585 -> #1589 -> #1594 (-> none)  The First Draft: #1594 was SUPERSEDED with no pointer; #1605 states "Supersedes
                                     #1594 (v0.42, 2026-09-06), which superseded #1589 and #1585" — all three now at #1605
  LOOP #66 <-> #1182 (and #1181 -> #1182)
                                     Hexagonal Licensing Protocol. #1181 and #1182 are duplicate mints of 2026-07-19
                                     whose own notes say "this work already existed as deposit #66, which remains
                                     canonical"; #66 nonetheless carried SUPERSEDED -> #1182, with no reason recorded,
                                     which closed the loop. #66 is restored to ACTIVE (its pointer removed, recorded);
                                     #1181 and #1182 point at #66.

Each change is recorded with record_modification.touch (was/now); data/retired-records.json resolves_to follows.
Pages: a record whose page carries the retirement layer is re-rendered and the layer re-applied in its
2026-10-15 indexable form (banner naming the record to cite, axn:retired, canonical self); others are re-wired.

    python3 scripts/repair_supersession_chains_20261015.py --apply   # registry + retired-records.json
    python3 scripts/repair_supersession_chains_20261015.py --pages   # pages
    python3 scripts/repair_supersession_chains_20261015.py --status  # ACTIVE records that carry a forward pointer

STATUS (found by check_state_conformance.py after the repoint): five records carry a forward pointer to a later
edition of the same work but are marked ACTIVE, so their pages draw no superseded banner. Each successor checked:
  #356 (FNM modular seed for v5.0) -> #30 (FNM v7.0, terminal of the family)
  #825 (Capture Registry v6.0) -> #1676 (v12.167, "continuing the deposit chain from v6.0")
  #1449 (Inversion Battery v0.1) and #1455 (v0.2) -> #1456 (v0.3, "Successor to deposit #1455")
  #1483 (the Ω erratum v1.0) -> #1484 (v1.1, terminal document of the sequence)
Set to SUPERSEDED. NOT changed: #1451 -> #1482 is one TACHYON continuity tether pointing at the next; a tether is
not superseded by the next one, so the pointer is more likely a chain link stored in the supersession field.
"""
import json, os, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts')); sys.path.insert(0, str(ROOT))
import record_modification as rm

REGP = ROOT / 'data/registry.json'; RETP = ROOT / 'data/retired-records.json'
ON = '2026-10-15'
RULING = ('Lee Sharks, 2026-10-15: repair "broken, missing, and mislabelled files / and citations"; '
          '"lets proceed - this is a lot of repairs to make"')
REPOINT = {11: 31, 327: 31, 363: 31, 364: 30, 386: 30, 1115: 1653, 1117: 1652, 1118: 1651, 1546: 1552,
           1648: 1681, 1664: 1671, 1585: 1605, 1589: 1605, 1594: 1605, 1181: 66, 1182: 66}
UNSUPERSEDE = {66: ('#1181 and #1182 are duplicate mints whose own notes say "this work already existed as deposit '
                    '#66, which remains canonical"; #66 carried SUPERSEDED -> #1182 with no reason recorded, which '
                    'made a loop (#66 -> #1182 -> #66). Restored to ACTIVE.')}
PAGES = sorted(set(REPOINT) | set(UNSUPERSEDE))


def apply():
    reg = json.loads(REGP.read_text()); D = {d['deposit_number']: d for d in reg['deposits']}
    ret = json.loads(RETP.read_text())
    for n, why in UNSUPERSEDE.items():
        d = D[n]; was = {'status': d.get('status'), 'superseded_by_deposit_number': d.get('superseded_by_deposit_number')}
        d['status'] = 'ACTIVE'; d.pop('superseded_by_deposit_number', None)
        d['supersession_reversed'] = {'on': ON, 'was': was, 'why': why, 'ruled_by': RULING}
        rm.touch(d, 'status', 'supersession loop removed: ' + why, was=was, now={'status': 'ACTIVE'}, when=ON)
    for n, t in REPOINT.items():
        d = D[n]; was = d.get('superseded_by_deposit_number')
        assert D[t].get('superseded_by_deposit_number') is None and D[t].get('status') == 'ACTIVE', (n, t)
        d['superseded_by_deposit_number'] = t
        d.setdefault('supersession_repointed', []).append({'on': ON, 'was': was, 'now': t, 'ruled_by': RULING,
            'why': 'chain' if was is not None else 'superseded with no pointer'})
        rm.touch(d, 'superseded_by_deposit_number',
                 f'forward pointer {"#%s" % was if was is not None else "(none)"} -> #{t}: points at the current edition in one hop',
                 was=was, now=t, when=ON)
        r = (d.get('body_status') or {}).get('retired')
        if r:
            r['resolves_to'] = t; r.setdefault('corrected', {'on': ON, 'was_resolves_to': was})
        if str(n) in ret['records']:
            ret['records'][str(n)].update({'resolves_to': t, 'title': D[t]['title'], 'axn': D[t]['axn'],
                                           'corrected': {'on': ON, 'was_resolves_to': ret['records'][str(n)].get('resolves_to')}})
    REGP.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    RETP.write_text(json.dumps(ret, ensure_ascii=False, indent=2))
    print('repointed', len(REPOINT), '| un-superseded', list(UNSUPERSEDE))


def pages():
    os.chdir(ROOT)
    retired = [n for n in PAGES if 'axn:retired' in (ROOT / f's/records/{n}/index.html').read_text(errors='replace')]
    os.environ['ALEXANARCH_FORCE_RERENDER'] = '1'
    from wire_deposit import wire_deposit
    import retire
    for n in PAGES:
        wire_deposit(n)
    reg, D = retire.load()
    keep = {n: dict(D[n]['body_status']['retired']) for n in retired}
    retire.apply(reg, D, {n: {'kind': 'superseded', 'target': D[n]['superseded_by_deposit_number'],
                              'reason': D[n].get('superseded_reason') or 'duplicate'} for n in retired})
    for n in retired:
        p = ROOT / f's/records/{n}/index.html'; s = p.read_text()
        s = re.sub(r'<meta name="robots" content="noindex, follow">\n?', '', s, count=1)
        s = re.sub(r'<link rel="canonical" href="[^"]*">',
                   f'<link rel="canonical" href="https://www.alexanarch.org/s/records/{n}/">', s, count=1)
        p.write_text(s)
    # retire.apply rewrites body_status.retired in its own copy only; the registry keeps the record made by --apply
    print('pages re-wired', len(PAGES), '| retirement layer re-applied', retired)


STATUS = [356, 825, 1449, 1455, 1483]


def status():
    reg = json.loads(REGP.read_text()); D = {d['deposit_number']: d for d in reg['deposits']}
    for n in STATUS:
        d = D[n]; t = d['superseded_by_deposit_number']
        assert d.get('status') == 'ACTIVE' and D[t].get('status') == 'ACTIVE', n
        d['status'] = 'SUPERSEDED'
        rm.touch(d, 'status', f'marked ACTIVE while carrying a forward pointer to a later edition (#{t}); status follows the pointer',
                 was='ACTIVE', now='SUPERSEDED', when=ON)
    REGP.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    print('status -> SUPERSEDED:', STATUS)


if __name__ == '__main__':
    if '--status' in sys.argv:
        status()
    if '--apply' in sys.argv:
        apply()
    if '--pages' in sys.argv:
        pages()
