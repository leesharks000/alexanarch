#!/usr/bin/env python3
"""repair_round_20261015c.py — the loose ends of 2026-10-15 ("lets fix all of that").

#950 — link the 13 planning documents its DataCite record names.
#696 — its header (Status / Sources / Parent documents / Date) was joined into one line at conversion; restored
       verbatim from the post of its date (mindcontrolpoems 2026/04/metadatapacket-forward-library-planning).
#987 — the same planning document (same date; the Markdown-source formatting of it). #696 matches the published post
       and is the earlier record: #987 is made a superseded duplicate witness of #696.
#1451 — carried superseded_by #1482, but #1482 names it as its "Prior" in the tether chain; no tether supersedes
       another (every other tether is ACTIVE with no pointer). The pointer is moved to tether_next.
#1305 — the body still carries the semi-restored apparatus ("Full text not yet recovered") of a record ruled a
       complete packet (#1300 ruling); a status line in the form of 2026-08-04 (16+ records) says so.

Ruling: Lee Sharks, 2026-10-15, "i dunno man. your call." The record keeps its body (the monograph; #1488's text says
"its body lives at #950"); its title and DataCite description name "13 planning documents, algorithms, diagnostic
maps" that the body did not carry or link. The 13 are in the repository at data/attachments/operative-semiotics-idp/
(the same files #1488 links); they are linked from the body, before the captured DataCite record.
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm
from repair_from_readings_20261015 import textfix, ON
from repair_restorations_20261015 import RULING

DOCS = ['PROSODIC_ASYMMETRY_ALGORITHM', 'FOUR_TERM_PROSODIC_ALGORITHM', 'NB2_PROSODIC_MAP', 'MISSING_PIECES_MAP',
        'PHASE_1_GAP_MAP_AND_MINING_TARGETS', 'PHASE_2_ARCHIVE_MINING_RESULTS', 'MIDDLE_NOTEBOOKS_WORK_PLAN',
        'WORK_PLAN_SUPPLEMENT_MUSES_AND_FPC', 'GRUNDRISSE_WORK_PLAN', 'CATHEDRAL_WORK_PLAN', 'HESPERUS_UPGRADE_PLAN',
        'SOURCE_EXTRACTION_REPORT', 'OS_NINE_VOLUME_SERIES_ARCHITECTURE']
D = 'data/attachments/operative-semiotics-idp'
ANCHOR = '## Complete DataCite record (verbatim, captured 2026-07-03)'


def f950(t):
    if f'{D}/PROSODIC_ASYMMETRY_ALGORITHM.md](' in t:
        return t
    for n in DOCS:
        assert (ROOT / D / f'{n}.md').exists(), n
    assert t.count(ANCHOR) == 1
    block = ('## Planning documents (attached)\n\nThe 13 planning documents, algorithms and diagnostic maps this record '
             'deposits (named in its DataCite record below):\n\n' + '\n'.join(f'- [{n}.md](/{D}/{n}.md)' for n in DOCS)
             + '\n\n---\n\n')
    return t.replace(ANCHOR, block + ANCHOR)


POST696 = ROOT / 'data/repair-maps/posts/696-metadatapacket-forward-library-planning-2026-04-26.txt'   # the post as fetched 2026-10-15


def f696(t):
    old = next((l for l in t.split('\n') if l.startswith('Status:') and 'locked downSources:' in l), None)
    if not old:
        return t
    P = [re.sub(r'^\s*\d+\t', '', l) for l in open(POST696, encoding='utf-8').read().split('\n')]
    i = next(k for k, l in enumerate(P) if l.startswith('Status:'))
    new = '\n'.join(P[i:i + 4])
    assert new.replace('  \n', '').replace(' ', '').replace('\xa0', '') == old.replace(' ', '').replace('\xa0', ''), (new, old)
    return t.replace(old, new)


def f1305(t):
    line = ('**Status (derived COMPLETE_PACKET):** ✓ Complete deposit packet. The semi-restored declaration below ("Full '
            'text not yet recovered") appeared here and was FALSE for this record\'s current state (complete-as-packet, '
            'the #1300 ruling); noted 2026-10-15 under the state-conformance rule.')
    if 'derived COMPLETE_PACKET' in t:
        return t
    k = t.find('*Full text not yet recovered.')
    assert k > 0
    return t[:k] + line + '\n\n' + t[k:]


def main():
    p = ROOT / 'data/registry.json'; reg = json.load(open(p)); D = {d['deposit_number']: d for d in reg['deposits']}
    done = []
    if textfix(D[950], f950, 'the 13 planning documents named by the record linked from the body (data/attachments/operative-semiotics-idp/)'):
        done.append(950)
    if textfix(D[696], f696, 'header lines joined at conversion restored verbatim from the post of the record\'s date'):
        done.append(696)
    if textfix(D[1305], f1305, 'status line: the semi-restored declaration in the body is false for a complete packet'):
        done.append(1305)
    d, T = D[987], D[696]
    if d['status'] == 'ACTIVE':
        was = {'status': 'ACTIVE', 'superseded_by_deposit_number': None}
        d['status'] = 'SUPERSEDED'; d['superseded_by_deposit_number'] = 696
        d['duplicate_note'] = (f'DUPLICATE ({ON}): the record of standing is #696 — the same planning document of the same '
                               'date; #696 matches the published post (mindcontrolpoems 2026/04), #987 carries the '
                               'Markdown-source formatting of the same text.')
        d['superseded_reason'] = 'Duplicate witness of the same work: the record of standing is #696.'
        d.setdefault('body_status', {})['retired'] = {'class': 'superseded', 'resolves_to': 696, 'declared': ON,
            'indexable': True, 'ruled_by': RULING, 'note': ('Superseded, not a stub: indexable (ruling 2026-10-15). The page '
            'carries a banner before the body naming the current version to cite, and an axn:retired marker; its '
            'canonical is its own URL.')}
        rm.touch(d, 'status', 'duplicate of #696; made a superseded duplicate witness', was=was,
                 now={'status': 'SUPERSEDED', 'superseded_by_deposit_number': 696}, when=ON)
        ret = json.load(open(ROOT / 'data/retired-records.json'))
        ret['records']['987'] = {'class': 'superseded', 'resolves_to': 696, 'title': T['title'], 'axn': T['axn'], 'declared': ON}
        ret['count'] = len(ret['records'])
        json.dump(ret, open(ROOT / 'data/retired-records.json', 'w'), ensure_ascii=False, indent=2)
        done.append(987)
    d = D[1451]
    if d.get('superseded_by_deposit_number'):
        was = {k: d.pop(k) for k in ('superseded_by_deposit_number', 'superseded_by_axn', 'superseded_by_url') if k in d}
        d['tether_next'] = {'deposit_number': 1482, 'axn': was.get('superseded_by_axn'), 'url': was.get('superseded_by_url')}
        rm.touch(d, 'superseded_by_deposit_number', 'mislabelled: #1482 names #1451 as its "Prior" in the tether chain, '
                 'not a supersession; moved to tether_next', was=was, now={'tether_next': 1482}, when=ON)
        done.append(1451)
    p.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
    print(done)


if __name__ == '__main__':
    main()
