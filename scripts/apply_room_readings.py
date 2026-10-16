#!/usr/bin/env python3
"""apply_room_readings.py — merge the verified room readings (data/room-readings/RRnn.json) into one seat file.

Ruling (Lee Sharks, 2026-10-16): "the deposits need to be all related to the respective rooms they develop in crimson
hexagon … much of this requires creating new edges. this is an interpretive read". Readers with provenance
(READER-PROMPT.md): every seat carries a relation, a confidence and a verbatim basis checked at its lines
(scripts/verify_room_reading.py → RRnn.verified.json). Only seats that passed are taken.

Writes data/room-readings/seats-read-2026-10-16.json:
  {"seats": {"<deposit>": [{"locus", "relation", "primary", "confidence", "basis", "room_cue", "batch"}]},
   "disagreements": [{"deposit", "current", "batch"}], "aliases_applied": [...], "summary": {...}}
build_hexagon_seats.py folds it in as source "read 2026-10-16" beside the canonical and room-page seats; existing
seats are never removed (a reader's "disagree" is listed for review, not applied).
Alias: the codebook gives the Frozen Sin Archive (address R:r.32) the id r30 and the Ruby Moot (address R:r.30) the id
r42; a reader who wrote the address number as the id ("r32") meant r30 — applied only when the seat's own room_cue
names the Frozen Sin Archive.
"""
import collections, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
RD = ROOT / 'data/room-readings'


def main():
    loci = {x['id']: x for x in json.load(open(RD / 'codebook.json'))['loci']}
    out = {}; dis = []; alias = []; skipped = collections.Counter(); conf = collections.Counter(); batches = []
    for f in sorted(RD.glob('RR[0-9][0-9].json')):
        vf = f.with_suffix('.verified.json')
        if not vf.exists():
            continue
        r = json.load(open(f)); v = {c['deposit']: c for c in json.load(open(vf))['checks']}; batches.append(r['batch_id'])
        for e in r.get('deposits', []):
            n = e.get('deposit'); c = v.get(n) or {}
            ok = set(c.get('seats_ok') or [])
            for k, s in enumerate(e.get('seats') or []):
                loc = s.get('locus')
                if k not in ok:
                    if loc == 'r32' and re.search(r'Frozen Sin', (s.get('room_cue') or '') + ' ' + ((s.get('basis') or {}).get('quote') or '')) and not [x for x in c.get('fails', []) if f'QUOTE {k}' in x]:
                        alias.append({'deposit': n, 'from': 'r32', 'to': 'r30', 'batch': r['batch_id']}); loc = 'r30'
                    else:
                        skipped[r['batch_id']] += 1; continue
                if loc not in loci:
                    skipped[r['batch_id']] += 1; continue
                out.setdefault(str(n), []).append({'locus': loc, 'relation': s['relation'], 'primary': bool(s.get('primary')),
                                                   'confidence': s['confidence'], 'basis': s.get('basis'), 'room_cue': s.get('room_cue'),
                                                   'batch': r['batch_id']})
                conf[s['confidence']] += 1
            if isinstance(e.get('current'), str) and e['current'].startswith('disagree'):
                dis.append({'deposit': n, 'current': e['current'], 'batch': r['batch_id']})
    summ = {'batches': batches, 'records_seated': len(out), 'seats': sum(len(x) for x in out.values()), 'by_confidence': dict(conf),
            'skipped_failed': dict(skipped), 'disagreements': len(dis),
            'by_locus': dict(collections.Counter(s['locus'] for x in out.values() for s in x).most_common())}
    (RD / 'seats-read-2026-10-16.json').write_text(json.dumps({'what': __doc__.split('\n')[0], 'ruled_by': 'Lee Sharks, 2026-10-16',
                                                               'seats': out, 'disagreements': dis, 'aliases_applied': alias,
                                                               'summary': summ}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({k: summ[k] for k in ('batches', 'records_seated', 'seats', 'by_confidence', 'skipped_failed', 'disagreements')}))


if __name__ == '__main__':
    main()
