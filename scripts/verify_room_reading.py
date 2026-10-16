#!/usr/bin/env python3
"""verify_room_reading.py — check a room reader's output (data/room-readings/RRnn.json) against what it claims.

    python3 scripts/verify_room_reading.py data/room-readings/RR01.json [--write]

Laws record; they do not block — failures are written into RRnn.verified.json and a seat that fails is not applied.
  QUEUED   every queued record has an entry; no entry for a record outside the batch
  LOCUS    each seat's locus is a codebook id; relation in the fixed set; confidence in the fixed set
  QUOTE    each basis quote occurs verbatim (whitespace- and quote-normalised) in the record's text within its lines
           (±3), or in the queued metadata when lines == "metadata"
  PRIMARY  at most one primary seat
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
REL = {'constitutes', 'develops', 'applies', 'documents', 'belongs'}
CONF = {'high', 'medium', 'low'}
norm = lambda s: ' '.join(str(s).replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('**', '').split())


def main():
    bp = pathlib.Path(sys.argv[1]); out = json.load(open(bp))
    loci = {x['id'] for x in json.load(open(ROOT / 'data/room-readings/codebook.json'))['loci']}
    q = next(b for b in json.load(open(ROOT / 'data/room-readings/queue.json'))['batches'] if b['batch_id'] == out['batch_id'])
    rows = {r['deposit']: r for r in q['deposits']}
    res = {'batch_id': out['batch_id'], 'checks': []}; ok_seats = 0; bad_seats = 0
    for e in out.get('deposits', []):
        n = e.get('deposit'); f = []; good = []
        if n not in rows:
            res['checks'].append({'deposit': n, 'fails': ['QUEUED: not in batch'], 'seats_ok': []}); continue
        row = rows[n]
        lines = pathlib.Path(row['text']).read_text(encoding='utf-8', errors='replace').split('\n') if row.get('text') else []
        meta = norm(json.dumps({k: row.get(k) for k in ('title', 'description', 'keywords', 'content_type', 'creator', 'date')}, ensure_ascii=False)
                    + ' ' + ' '.join(str(row.get(k) or '') for k in ('title', 'description')) + ' ' + ' '.join(map(str, row.get('keywords') or [])))
        prim = 0
        for k, s in enumerate(e.get('seats') or []):
            sf = []
            if s.get('locus') not in loci: sf.append(f'LOCUS {k}: {s.get("locus")!r} not in codebook')
            if s.get('relation') not in REL: sf.append(f'LOCUS {k}: relation {s.get("relation")!r}')
            if s.get('confidence') not in CONF: sf.append(f'LOCUS {k}: confidence {s.get("confidence")!r}')
            prim += bool(s.get('primary'))
            b = s.get('basis') or {}; qt = norm(b.get('quote', '')); ln = b.get('lines')
            if not qt:
                sf.append(f'QUOTE {k}: empty')
            elif ln == 'metadata' or not lines:
                if qt not in meta: sf.append(f'QUOTE {k}: not in metadata: {qt[:60]!r}')
            elif isinstance(ln, list) and len(ln) == 2:
                win = norm('\n'.join(lines[max(0, int(ln[0]) - 4):int(ln[1]) + 3]))
                if qt not in win:
                    sf.append(f'QUOTE {k}: not verbatim at {ln}' + (' (present elsewhere)' if qt in norm('\n'.join(lines)) else '') + f': {qt[:60]!r}')
            else:
                sf.append(f'QUOTE {k}: lines {ln!r}')
            f += sf
            if sf: bad_seats += 1
            else: good.append(k); ok_seats += 1
        if prim > 1: f.append(f'PRIMARY: {prim} primary seats')
        res['checks'].append({'deposit': n, 'fails': f, 'seats_ok': good})
    seen = {e.get('deposit') for e in out.get('deposits', [])}
    for n in rows:
        if n not in seen: res['checks'].append({'deposit': n, 'fails': ['QUEUED: no entry'], 'seats_ok': []})
    res['summary'] = {'entries': len(out.get('deposits', [])), 'queued': len(rows), 'seats_ok': ok_seats, 'seats_failed': bad_seats,
                      'records_with_fails': sum(1 for c in res['checks'] if c['fails'])}
    print(json.dumps(res['summary']))
    if '--write' in sys.argv:
        bp.with_suffix('.verified.json').write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
