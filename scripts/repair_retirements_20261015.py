#!/usr/bin/env python3
"""repair_retirements_20261015.py — two retirements that were caused by wrong bodies.

Ruling (Lee Sharks, 2026-10-15): "yes, unretire and seat texts, but make sure youre not duplicating something
that already exists elsewhere on the blog."

Both records were retired on 2026-08-10 as "duplicate witnesses" on the strength of a 2026-07-19 body
containment measure. The body measured was the wrong body in each case, so the duplicate it found was the
wrong body's own source, not the work:

  #1142  THE THUMB: Formal Operators for the Phase X Quintuple. Retired as a duplicate of #13 (Phase X
         Navigation Map), because the seated body WAS the Navigation Map. Checked against every seated text:
         the THUMB post (2026/02/the-thumb-formal-operators-for-phase-x.html) is seated in full at #431
         (8 of 8 probes), THE THUMB's own record. So #1142 IS a duplicate, of #431: it stays retired, and the
         successor it names is corrected from #13 to #431. Its seated body is left as it is (seating THE THUMB
         again would duplicate #431).
  #1170  🫵❓2️⃣4️⃣🗓️ = ❓ (Ichabod Spellings). Retired as a duplicate of #31 (DOI Registry v7.0), because the
         seated body WAS the registry. The work (post 2026/02/24-24-i-kept-open-for-that-was-to-now-i.html,
         verbatim the DataCite abstract of its DOI 10.5281/zenodo.18512288) is seated as its own work nowhere:
         it occurs only inside the DOI registries (#31, #1171, #1251) and the wrong bodies (#1168, #1170). So
         #1170 is un-retired here; its body is seated by restore_wrong_bodies.py.

Non-destruction: the retirement fields of #1170 are moved, whole, to `retirement_reversed`; #1142's replaced
reason and note are kept beside the corrected ones. data/retired-records.json is updated (and records the
reversal). Page layers: #1142's page is re-rendered and its retirement layer re-applied (retire.apply, then the
2026-10-15 indexable form: no noindex, canonical self) — run by this script with --pages after wiring.

    python3 scripts/repair_retirements_20261015.py --apply      # registry + retired-records.json
    python3 scripts/repair_retirements_20261015.py --pages      # re-render #1142 and re-apply its layer
"""
import json, os, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import record_modification as rm

REGP = ROOT / 'data/registry.json'
RETP = ROOT / 'data/retired-records.json'
ON = '2026-10-15'
RULING = ('Lee Sharks, 2026-10-15: "yes, unretire and seat texts, but make sure youre not duplicating '
          'something that already exists elsewhere on the blog."')


def registry():
    reg = json.loads(REGP.read_text())
    D = {d['deposit_number']: d for d in reg['deposits']}
    ret = json.loads(RETP.read_text())

    # #1142: stays retired; successor corrected #13 -> #431
    d = D[1142]; t = D[431]
    was = {k: d.get(k) for k in ('superseded_by_deposit_number', 'superseded_reason', 'duplicate_note')}
    was['retired'] = dict((d.get('body_status') or {}).get('retired') or {})
    d['superseded_by_deposit_number'] = 431
    d['superseded_reason_before_correction'] = was['superseded_reason']
    d['duplicate_note_before_correction'] = was['duplicate_note']
    d['superseded_reason'] = (
        'Duplicate witness of the same work: THE THUMB is seated in full at #431, its own record. '
        f'CORRECTED {ON}: the successor was recorded as #13 (Phase X Navigation Map) because the body seated '
        'here on 2026-07-19 was the Navigation Map, not THE THUMB; the containment measure matched that body.')
    d['duplicate_note'] = (
        f'DUPLICATE MINT (2026-07-19 restoration): THE THUMB already existed as deposit #431, which remains '
        f'canonical. CORRECTED {ON}: previously recorded as a duplicate of #13 on a body containment of 0.93 '
        'measured against the wrong body (the Navigation Map). The seated body is left as it is; THE THUMB is not '
        'seated again here, because it already stands at #431.')
    r = d['body_status']['retired']
    r['resolves_to'] = 431
    r['corrected'] = {'on': ON, 'was_resolves_to': 13, 'ruling': RULING}
    rm.touch(d, 'superseded_by_deposit_number', 'successor corrected #13 -> #431 (retirement caused by wrong body)',
             was=was, now={'superseded_by_deposit_number': 431}, when=ON)
    ret['records']['1142'] = {'class': 'superseded', 'resolves_to': 431, 'title': t['title'], 'axn': t['axn'],
                              'corrected': {'on': ON, 'was_resolves_to': 13}}

    # #1170: un-retired
    d = D[1170]
    rev = {k: d.pop(k) for k in ('superseded_reason', 'duplicate_note', 'superseded_by_deposit_number') if k in d}
    rev['retired'] = (d.get('body_status') or {}).pop('retired', None)
    rev.update({'reversed_on': ON, 'ruled_by': RULING,
                'why': ('retired on 2026-08-10 as a duplicate witness of #31 on a body containment of 1.0 measured '
                        'against the wrong body (the DOI Registry v7.0 post seated here 2026-07-19). The work — the '
                        'emoji poem, verbatim the DataCite abstract of 10.5281/zenodo.18512288 — is seated as its '
                        'own work nowhere else in the archive.')})
    d['retirement_reversed'] = rev
    rm.touch(d, 'status', 'retirement reversed (it was caused by a wrong body); the work seated',
             was={'retired': rev['retired']}, now={'retired': None}, when=ON)
    old = ret['records'].pop('1170', None)
    ret.setdefault('reversed', {})['1170'] = {'was': old, 'on': ON, 'ruled_by': RULING}
    ret['count'] = len(ret['records'])

    REGP.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    RETP.write_text(json.dumps(ret, ensure_ascii=False, indent=2))
    print('registry + retired-records.json updated; retired count', ret['count'])


def pages():
    os.environ['ALEXANARCH_FORCE_RERENDER'] = '1'
    os.chdir(ROOT)
    from wire_deposit import wire_deposit
    import retire
    wire_deposit(1142)
    reg, D = retire.load()
    retire.apply(reg, D, {1142: {'kind': 'superseded', 'target': 431, 'reason': D[1142]['superseded_reason']}})
    p = ROOT / 's/records/1142/index.html'; s = p.read_text()
    s = re.sub(r'<meta name="robots" content="noindex, follow">\n?', '', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               '<link rel="canonical" href="https://www.alexanarch.org/s/records/1142/">', s, count=1)
    p.write_text(s)
    # retire.apply rewrote body_status.retired; keep the indexable form and the correction
    reg2 = json.loads(REGP.read_text()); d = {x['deposit_number']: x for x in reg2['deposits']}[1142]
    r = D[1142]['body_status']['retired']
    r.update({'declared': '2026-08-10', 'indexable': True,
              'note': ('Superseded, not a stub: indexable (ruling 2026-10-15). The page carries a banner before the '
                       'body naming the current version to cite, and an axn:retired marker; its canonical is its own '
                       'URL. The URL is kept; the record is not deleted.'),
              'corrected': {'on': ON, 'was_resolves_to': 13, 'ruling': RULING}})
    d['body_status']['retired'] = r
    REGP.write_text(json.dumps(reg2, ensure_ascii=False, indent=2))
    print('#1142 re-rendered; retirement layer re-applied -> #431 (indexable, canonical self)')


if __name__ == '__main__':
    if '--apply' in sys.argv:
        registry()
    if '--pages' in sys.argv:
        pages()
