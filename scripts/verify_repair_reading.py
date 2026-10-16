#!/usr/bin/env python3
"""verify_repair_reading.py — check a repair reader's output, and what it actually read.

    python3 scripts/verify_repair_reading.py data/repair-maps/readings/RP01.json [<transcript.jsonl>] [--write]

Per record (laws record; they do not block — every failure is written into <batch>.verified.json):
  QUEUED   the record is in the batch queue, and every queued record has an entry
  VERDICT  one of the fixed verdicts, with the fields that verdict needs
  COVER    read_ranges cover lines 1..lines_total of the seated text (lines_total must match the file)
  QUOTE    each evidence quote occurs verbatim (whitespace-normalised) in the file named, within its lines (±2);
           quotes from a post (file = a blog URL) are checked against the live post converted as the readers saw it
  AUDIT    with a transcript: the line numbers the Read tool actually returned for the seated text, against the
           claimed read_ranges (claimed-but-not-returned lines are the measure)
The transcript is stored by sha256 only.
"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
VERDICTS = {'no_defect': [], 'as_published': [], 'seat_post': ['url', 'kind'], 'duplicate_of': ['target'],
            'content_type': ['value'], 'title': ['value'], 'attach_link': [], 'needs_ruling': [],
            'restore_sections': ['restorations'], 'seat_second_store': []}   # restore readers (queue2.json)
LN = re.compile(r'^\s*(\d+)\t', re.M)
norm = lambda s: ' '.join(s.replace('’', "'").replace('“', '"').replace('”', '"').split())
_posts = {}


def post_lines(url):
    if url not in _posts:
        from restore_from_blog import fetch, extract_post
        from restore_wrong_bodies import to_md, unescape
        _, b = extract_post(fetch(url).decode('utf-8', 'replace'))
        _posts[url] = unescape(to_md(b or ''), b or '').split('\n')
    return _posts[url]


def text_of(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return '\n'.join(x.get('text', '') for x in c if isinstance(x, dict))
    return ''


def audit(tp, paths):
    raw = pathlib.Path(tp).read_bytes(); calls, seen = {}, {}
    for l in raw.decode('utf-8', 'replace').splitlines():
        try:
            r = json.loads(l)
        except Exception:
            continue
        for c in (r.get('message') or {}).get('content') or [] if isinstance((r.get('message') or {}).get('content'), list) else []:
            if not isinstance(c, dict):
                continue
            if c.get('type') == 'tool_use' and c.get('name') == 'Read' and (c.get('input') or {}).get('file_path') in paths:
                calls[c['id']] = c['input']['file_path']
            elif c.get('type') == 'tool_result' and c.get('tool_use_id') in calls:
                seen.setdefault(calls[c['tool_use_id']], set()).update(int(x) for x in LN.findall(text_of(c.get('content'))))
    return hashlib.sha256(raw).hexdigest(), seen


def main():
    bp = pathlib.Path(sys.argv[1]); tp = next((a for a in sys.argv[2:] if not a.startswith('--')), None)
    out = json.loads(bp.read_text())
    qf = 'queue2.json' if out['batch_id'].startswith('RQ') else 'queue.json'
    q = next(b for b in json.load(open(ROOT / 'data/repair-maps/readings' / qf))['batches'] if b['batch_id'] == out['batch_id'])
    rows = {int(r['deposit']): r for r in q['deposits']}
    tsha, seen = audit(tp, {r['text'] for r in rows.values()}) if tp else (None, {})
    res = {'batch_id': out['batch_id'], 'transcript_sha256': tsha, 'checks': []}
    for e in out.get('deposits', []):
        n = e.get('deposit'); f = []
        if n not in rows:
            res['checks'].append({'deposit': n, 'fails': ['QUEUED: not in batch']}); continue
        row = rows[n]; lines = pathlib.Path(row['text']).read_text(encoding='utf-8', errors='replace').split('\n')
        v = e.get('verdict')
        if v not in VERDICTS:
            f.append(f'VERDICT: {v!r}')
        else:
            f += [f'VERDICT: {v} lacks {k}' for k in VERDICTS[v] if not e.get(k)]
        tot = len(lines) - (1 if lines and lines[-1] == '' else 0)
        if e.get('lines_total') != tot:
            f.append(f'COVER: lines_total {e.get("lines_total")} but file has {tot}')
        cov = set()
        for a, b in e.get('read_ranges') or []:
            cov.update(range(int(a), int(b) + 1))
        miss = [i for i in range(1, tot + 1) if i not in cov]
        if miss:
            f.append(f'COVER: {len(miss)} of {tot} lines not in read_ranges')
        for k, ev in enumerate(e.get('evidence') or []):
            src = ev.get('file', ''); qt = norm(ev.get('quote', ''))
            try:
                L = post_lines(src) if src.startswith('http') else pathlib.Path(src).read_text(encoding='utf-8', errors='replace').split('\n')
            except Exception as ex:
                f.append(f'QUOTE {k}: cannot open {src[:80]} ({str(ex)[:60]})'); continue
            if not qt or qt not in norm('\n'.join(L)):
                f.append(f'QUOTE {k}: not verbatim in {src[-60:]}: {qt[:60]!r}'); continue
            ln = ev.get('lines') or []
            if len(ln) == 2 and qt not in norm('\n'.join(L[max(0, ln[0] - 3):ln[1] + 2])):
                f.append(f'QUOTE {k}: verbatim but not at lines {ln}')
        for k, r in enumerate(e.get('restorations') or []):     # RESTORE: content verbatim in its source, at its lines
            src = r.get('source', ''); ct = r.get('content', '')
            try:
                L = post_lines(src) if src.startswith('http') else pathlib.Path(src).read_text(encoding='utf-8', errors='replace').split('\n')
            except Exception as ex:
                f.append(f'RESTORE {k}: cannot open {src[:80]} ({str(ex)[:60]})'); continue
            sl = r.get('source_lines') or []
            if not ct.strip():
                f.append(f'RESTORE {k}: empty content')
            elif len(sl) == 2 and norm(ct) not in norm('\n'.join(L[max(0, sl[0] - 3):sl[1] + 2])):
                f.append(f'RESTORE {k}: content not verbatim in {src[-50:]} at {sl}')
            sd = r.get('seated_lines')
            if sd and not (1 <= sd[0] <= sd[1] <= tot):
                f.append(f'RESTORE {k}: seated_lines {sd} outside 1..{tot}')
            if not 0 <= int(r.get('after_line') or 0) <= tot:
                f.append(f'RESTORE {k}: after_line outside the text')
        aud = None
        if tp:
            got = seen.get(row['text'], set())
            aud = {'lines_returned': len(got & set(range(1, tot + 1))), 'claimed_not_returned': len((cov & set(range(1, tot + 1))) - got)}
            if aud['claimed_not_returned']:
                f.append(f'AUDIT: {aud["claimed_not_returned"]} claimed lines never returned by Read')
        res['checks'].append({'deposit': n, 'verdict': v, 'fails': f, 'audit': aud})
    for n in rows:
        if n not in {e.get('deposit') for e in out.get('deposits', [])}:
            res['checks'].append({'deposit': n, 'fails': ['QUEUED: no entry']})
    res['summary'] = {'entries': len(out.get('deposits', [])), 'with_fails': sum(1 for c in res['checks'] if c['fails'])}
    print(json.dumps(res['summary']))
    for c in res['checks']:
        for x in c['fails']:
            print(f"  #{c['deposit']}: {x}")
    if '--write' in sys.argv:
        bp.with_suffix('.verified.json').write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
