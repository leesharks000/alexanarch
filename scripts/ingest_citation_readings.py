#!/usr/bin/env python3
"""ingest_citation_readings.py — seat an in-session reading of reference-section segments.

Stage C of the citation graph, done by reading (No-Double-Draw: in session, never via
API). A reader goes through the segments of data/worklists/refsec-parse-queue.json and
writes one line per work found, in a batch file:

    <seg>|N                                    the segment is not a reference
    <seg>|W|authors|title|container|year|kind|status|own|basis

  <seg>       the 12-hex segment key: sha256("<deposit>|<raw>")[:12]
  kind        book · article · chapter · paper · preprint · thesis · report · web · post ·
              legal · scripture · classical · dataset · software · media · archive · other
  status      R real (the reader identifies the work) · U unverified (plausible, not
              identified) · F forward_library (cited ahead of its existence: a later date,
              "forthcoming", a future field's scholarship — a Retrocausal Citation Entry,
              not a historical publication record) · X fictive_retro (an invented past work)
  own         1 when the work is the archive's own (a heteronym or the archive as author)
  basis       optional: why the status, when it is not obvious

One segment may carry several W lines (a note citing three works). Later batches
replace earlier readings of the same segment. The readings file is authoritative over
the heuristic parse: refsec_parse.py marks a read segment parsed (or not_reference)
and parse_refsec_queue.py emits one edge per work read.

An own work with status R is checked against the registry: a title that matches a
deposit records it (deposit field); one that matches none keeps the reader's status
and says so in basis.

    python3 scripts/ingest_citation_readings.py <batch.txt> [...] [--reader "TACHYON 2026-10-13"]
"""
import hashlib, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUEUE = ROOT / 'data' / 'worklists' / 'refsec-parse-queue.json'
OUT = ROOT / 'data' / 'citation-readings.json'

KINDS = {'book', 'article', 'chapter', 'paper', 'preprint', 'thesis', 'report', 'web', 'post', 'legal',
         'scripture', 'classical', 'dataset', 'software', 'media', 'archive', 'other'}
STATUS = {'R': 'real', 'U': 'unverified', 'F': 'forward_library', 'X': 'fictive_retro'}
STATUS_DOC = {
    'real': 'the reader identifies the work as existing',
    'unverified': 'plausible; not identified by the reader',
    'forward_library': 'Retrocausal Citation Entry · Forward Library · not a historical publication record: '
                       'the citing text itself marks the work as not yet existing — "forthcoming", '
                       '"pending deposit", "in progress", "projected", a date after the citing text, '
                       'or a declared Forward Library / projected-reception section. Never inferred by '
                       'comparing dates: a citation of a work deposited after the citing deposit\'s '
                       'registry date, with no such mark, is read as real (the text may have been revised)',
    'fictive_retro': 'an invented past work, cited as though it existed',
}


DESCRIPTION = ('In-session readings of the reference-section segments in '
               'data/worklists/refsec-parse-queue.json: each work named in a segment, with authors, title, '
               'container, year, kind and ontic status, or the finding that the segment names no work. '
               'Authoritative over the heuristic parse. Every refsec-locus segment is read. In the tang locus, '
               'segments the heuristic classed as prose or apparatus are read only when they carry citation '
               'features (a parenthesised year, a DOI, an italic title with a year, "et al.", ISBN, arXiv or a URL); '
               'the rest keep their heuristic class. Segments stored at 1,200 characters are read as far as stored, '
               'and the basis says so. A basis line records corrections the reader noticed (misattributions, '
               'wrong DOIs or subtitles, conflicting years) without altering what the text says. '
               'Written by scripts/ingest_citation_readings.py.')


def norm(s):
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())


def seg_key(dep, raw):
    return hashlib.sha256(f'{dep}|{raw}'.encode()).hexdigest()[:12]


def main():
    args = [a for a in sys.argv[1:]]
    reader = 'TACHYON 2026-10-13'
    if '--reader' in args:
        i = args.index('--reader'); reader = args[i + 1]; del args[i:i + 2]
    q = json.loads(QUEUE.read_text())['entries']
    segs = {seg_key(e['source_deposit'], e['raw']): e for e in q}
    reg = json.loads((ROOT / 'data' / 'registry.json').read_text())
    titles = {}
    for d in reg['deposits']:
        t = norm(d.get('title'))
        for L in (60, 40):
            if len(t) >= L:
                titles.setdefault(t[:L], d['deposit_number'])
    doc = json.loads(OUT.read_text()) if OUT.exists() else {
        '@context': 'https://schema.org', '@type': 'Dataset',
        'name': 'Alexanarch — reference sections read',
        'description': ('In-session readings of the reference-section segments in '
                        'data/worklists/refsec-parse-queue.json: each work named in a segment, with '
                        'authors, title, container, year, kind and ontic status. Authoritative over '
                        'the heuristic parse. Written by scripts/ingest_citation_readings.py.'),
        'status_vocabulary': STATUS_DOC, 'kinds': sorted(KINDS), 'readings': {}}
    doc['description'] = DESCRIPTION
    doc['status_vocabulary'] = STATUS_DOC
    doc['kinds'] = sorted(KINDS)
    R = doc['readings']
    batch = {}
    bad = []
    for path in args:
        for ln, line in enumerate(pathlib.Path(path).read_text().splitlines(), 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            f = [x.strip() for x in line.split('|')]
            k = f[0]
            if k not in segs:
                bad.append(f'{path}:{ln} unknown segment {k}'); continue
            if len(f) >= 2 and f[1] == 'N':
                batch[k] = {'class': 'not_reference', 'works': []}
                continue
            if len(f) < 9 or f[1] != 'W':
                bad.append(f'{path}:{ln} malformed: {line[:80]}'); continue
            authors, title, container, year, kind, st, own = f[2:9]
            basis = f[9] if len(f) > 9 else ''
            if kind not in KINDS or st not in STATUS:
                bad.append(f'{path}:{ln} kind/status {kind}/{st}'); continue
            w = {'authors': authors or None, 'title': title or None, 'container': container or None,
                 'year': year or None, 'kind': kind, 'ontic_status': STATUS[st], 'own': own == '1'}
            if basis:
                w['basis'] = basis
            if w['own'] and title:
                t = norm(title)
                dep = titles.get(t[:60]) or titles.get(t[:40])
                if dep:
                    w['deposit'] = dep
            r = batch.setdefault(k, {'class': 'reference', 'works': []})
            if r['class'] == 'not_reference':
                r['class'] = 'reference'
            r['works'].append(w)
    if bad:
        print('\n'.join(bad)); sys.exit(1)
    for k, r in batch.items():
        e = segs[k]
        r.update({'deposit': e['source_deposit'], 'locus': e.get('locus'), 'read_by': reader})
        R[k] = r
    doc['count'] = len(R)
    doc['works_read'] = sum(len(r['works']) for r in R.values())
    from collections import Counter
    doc['by_status'] = dict(Counter(w['ontic_status'] for r in R.values() for w in r['works']).most_common())
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=0, sort_keys=False) + '\n')
    print(f'seated {len(batch)} segment readings ({sum(len(r["works"]) for r in batch.values())} works); '
          f'file: {doc["count"]} segments, {doc["works_read"]} works, {doc["by_status"]}')


if __name__ == '__main__':
    main()
