#!/usr/bin/env python3
"""record_state.py — THE canonical derivation of a record's declared state.

WHY THIS EXISTS (MANUS, 2026-08-04: "I need conformance between banners and all
other status emitters. How do we get that as a rule rather than a manual catch?
Our data structure is not good.")

The defect is structural, not clerical. A record's state was spread across at
least eleven fields on two levels — `status`, `superseded_by_deposit_number`,
`superseded_reason`, `body_status.class`, `.capture_completeness`,
`.lacuna_mark`, `.withdrawal`, `.full_version`, `.external_manifestation`,
`.related_instances`, `.named_in` — and every emitter (page banner, OAI record,
disposition, description prose, wiki) read a DIFFERENT SUBSET. Three times in
one session a record was ruled one way in data and kept announcing something
else on the page (#941 pointer with ACTIVE status; #1300 complete packet
announcing itself semi-restored; related_instances inscribed but unrendered).
Each was caught by MANUS reading a page. That is not a process.

THE RULE: no emitter reads state fields directly. Every emitter calls
`derive_state(record)` and renders what it returns. A record has exactly ONE
declared state. `check_state_conformance.py` fails the build if any emitter's
output disagrees with the derivation.

PRECEDENCE (first match wins — most decisive claim about the object governs):
  1. WITHDRAWN_EXTERNAL  foreign capture withdrawn by ruling
  1b. WITHDRAWN         record withdrawn (outranks absence: not awaiting recovery)
  2. LACUNA              work declared absent after channel exhaustion
  3. SUPERSEDED          this record yields to another record of standing
  4. COMPLETE_PACKET     a capture that is complete AS the object it is
  5. CAPTURE_PAIRED      capture whose complete work is elsewhere in-archive
  6. CAPTURE_EXTERNAL    capture whose manifestation is a live external surface
  7. CAPTURE_UNPAIRED    capture with no known complete version
  8. FULL                the work is seated here
"""
import json
import os
import sys

STATES = ('WITHDRAWN_EXTERNAL', 'WITHDRAWN', 'LACUNA', 'SUPERSEDED', 'COMPLETE_PACKET',
          'CAPTURE_PAIRED', 'CAPTURE_EXTERNAL', 'CAPTURE_UNPAIRED', 'FULL')


def _bs(d):
    b = d.get('body_status')
    return b if isinstance(b, dict) else {}


def derive_state(d):
    """Return the single canonical state object for a record.

    Keys: state, label, detail, pointer (deposit number or url or None),
    citable (may this page be cited as the full text), harvest_note.
    """
    b = _bs(d)
    dn = d.get('deposit_number')

    if b.get('withdrawal') or b.get('class') == 'withdrawn_external':
        w = b.get('withdrawal') or {}
        return dict(state='WITHDRAWN_EXTERNAL', pointer=None, citable=False,
                    label='⊘ Withdrawn — external work',
                    detail=str(w.get('effect') or
                              'A foreign capture withdrawn by ruling; this record is a typed '
                              'tombstone, not a deposit awaiting recovery.'),
                    harvest_note='withdrawn-external')

    if d.get('status') == 'WITHDRAWN':
        # Withdrawal is a more decisive claim about the object than absence of
        # its text: a withdrawn record is not awaiting recovery. Ordered above
        # LACUNA after #1382/#1383 showed the renderer's withdrawn branch and
        # the derivation disagreeing (conformance check, 2026-08-04).
        lm = b.get('lacuna_mark') or {}
        return dict(state='WITHDRAWN', pointer=None, citable=False,
                    label='⊘ Withdrawn',
                    detail=str(lm.get('statement') or b.get('withdrawal_reason') or
                               'This record has been withdrawn; it is not a deposit awaiting recovery.'),
                    harvest_note='withdrawn')

    if b.get('lacuna_mark') or b.get('lacuna') in (True, 'true', 'TRUE'):
        lm = b.get('lacuna_mark') or {}
        return dict(state='LACUNA', pointer=None, citable=False,
                    label='◌ Lacuna — work declared absent',
                    detail=str(lm.get('statement') or
                               'The work is declared absent after documented channel exhaustion.'),
                    harvest_note='lacuna')

    sup = d.get('superseded_by_deposit_number')
    if sup:
        return dict(state='SUPERSEDED', pointer=sup, citable=False,
                    label='⚠ Superseded',
                    detail=str(d.get('superseded_reason') or
                               f'The record of standing for this work is #{sup}.'),
                    harvest_note='superseded')

    if b.get('class') == 'metadata_capture':
        fv = b.get('full_version') or {}
        cc = str(b.get('capture_completeness') or '')
        if cc.startswith('complete'):
            return dict(state='COMPLETE_PACKET', pointer=fv.get('deposit_number'), citable=True,
                        label='✓ Complete deposit packet',
                        detail=(f'This record is complete as what it is ({cc})'
                                + (f'; the work it packages is at #{fv["deposit_number"]}.'
                                   if fv.get('deposit_number') else '.')),
                        harvest_note='complete-packet')
        if fv.get('deposit_number'):
            return dict(state='CAPTURE_PAIRED', pointer=fv['deposit_number'], citable=False,
                        label='◐ Semi-restored capture — the complete work exists in this archive',
                        detail=str(fv.get('basis') or
                                   'This record preserves the metadata capture; read the complete version for the full text.'),
                        harvest_note='capture-paired')
        em = b.get('external_manifestation') or {}
        if em.get('url'):
            return dict(state='CAPTURE_EXTERNAL', pointer=em['url'], citable=False,
                        label='◐ Capture of a live surface',
                        detail=str(em.get('role') or em.get('basis') or
                                   'The manifestation of this work is the live surface named below.'),
                        harvest_note='capture-external')
        return dict(state='CAPTURE_UNPAIRED', pointer=None, citable=False,
                    label='◐ Semi-restored metadata capture',
                    detail=('This record preserves metadata and a partial body only. The complete work '
                            'is not yet restored in this archive; do not cite this page as the full text.'),
                    harvest_note='capture-unpaired')

    return dict(state='FULL', pointer=None, citable=True,
                label='', detail='', harvest_note='full')


def load_registry(path='data/registry.json'):
    with open(path, encoding='utf-8', errors='replace') as fh:
        return json.load(fh)


if __name__ == '__main__':
    reg = load_registry()
    from collections import Counter
    c = Counter(derive_state(d)['state'] for d in reg['deposits'])
    for s in STATES:
        if c.get(s):
            print(f'{c[s]:6}  {s}')
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        d = [x for x in reg['deposits'] if x['deposit_number'] == n][0]
        print(json.dumps(derive_state(d), ensure_ascii=False, indent=1))
