#!/usr/bin/env python3
"""parse_refsec_queue.py — Stage C bulk pass (in-session heuristic layer).

Parses the freeform citation queue (refsec + tang loci) into structured
entries with bib: keys, merges nodes into external-works, and emits the
freeform edge file. Imperfect by declaration (MANUS 2026-07-18: "doesn't
need to be perfect — expanded thru the layer horizon"); refinement passes
retype relations and settle ontic status entry-by-entry later.

Ontic heuristics applied only where unambiguous:
  year > current year, or 'forthcoming'/'in press'  -> forward_library
  everything else                                   -> unverified

Outputs:
  data/worklists/refsec-parse-queue.json  entries -> parsed | triaged
  data/external-works.json                merged bib: nodes
  data/citation-graph-freeform.json       freeform edges (separate file so
                                          the mechanical extractor stays
                                          regenerable without clobbering)
"""
import json, re, hashlib, pathlib, datetime
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
CUR_YEAR = 2026

YEAR_RE = re.compile(r'\b(1[5-9]\d\d|20\d\d)\b')
ITAL_RE = re.compile(r'\*([^*]{4,200})\*')
QUOT_RE = re.compile(r'[“"]([^”"]{4,200})[”"]')
AUTHOR_LEAD_RE = re.compile(r'^([A-Z][\w\'-]+),\s+[A-Z][\w.\'-]+')
PUBWORDS = ('press', 'university', 'verso', 'routledge', 'journal', 'vol.', 'no.',
            'pp.', ' ed.', 'trans.', 'doi', 'isbn', 'publisher', 'books', 'review',
            'quarterly', 'zenodo', 'arxiv', 'retrieved', 'accessed', 'in press',
            'forthcoming', 'editions', 'oxford', 'cambridge', 'chicago', 'mit')

def norm(s):
    return re.sub(r'[^a-z0-9]+', '', s.lower())

def bibkey(authors, title, year, raw):
    base = (norm(authors or '') + '|' + norm(title or '') + '|' + (year or '')) \
        if (authors or title) else norm(raw)[:120]
    return 'bib:' + hashlib.sha256(base.encode()).hexdigest()[:12]

def score(raw):
    low = raw.lower()
    sc = 0
    if YEAR_RE.search(raw): sc += 1
    if ITAL_RE.search(raw) or QUOT_RE.search(raw): sc += 1
    if AUTHOR_LEAD_RE.match(raw): sc += 1
    if any(w in low for w in PUBWORDS): sc += 1
    if re.search(r'\(\d{4}\)', raw): sc += 1
    return sc

def parse_entry(raw):
    authors = title = venue = year = None
    m = AUTHOR_LEAD_RE.match(raw)
    if m:
        # authors = up to first period that isn't an initial
        seg = re.match(r'^(.{3,120}?\.)\s', raw)
        if seg:
            a = seg.group(1)
            if not re.search(r'\b[A-Z]\.$', a) or len(a) > 40:
                authors = a.rstrip('.')
    qm, im = QUOT_RE.search(raw), ITAL_RE.search(raw)
    ti = qm or im
    if ti:
        title = ti.group(1).strip().rstrip('.,')
        if qm and im:
            venue = im.group(1).strip().rstrip('.,')
    elif authors:
        rest = raw[len(authors) + 1:].strip()
        seg = re.match(r'^\s*(.{4,160}?)(?:\.|\bIn\b|\()', rest)
        if seg: title = seg.group(1).strip().rstrip('.,')
    pm = re.search(r'\((1[5-9]\d\d|20\d\d)[,)\s]', raw)
    years = YEAR_RE.findall(raw)
    year = pm.group(1) if pm else (years[-1] if years else None)
    # venue: text after title occurrence containing pubwords
    if title and not venue:
        tail = raw[raw.find(title) + len(title):]
        vm = re.search(r'([A-Z][^.]{4,120}(?:Press|University|Journal|Review|Books|Quarterly|Editions)[^.]{0,60})', tail)
        if vm: venue = vm.group(1).strip()
    return authors, title, venue, year

def ontic(raw, year):
    low = raw.lower()
    if 'forthcoming' in low or 'in press' in low:
        return 'forward_library'
    if year and int(year) > CUR_YEAR:
        return 'forward_library'
    return 'unverified'

def main():
    qp = ROOT / 'data' / 'worklists' / 'refsec-parse-queue.json'
    q = json.loads(qp.read_text())
    works = json.loads((ROOT / 'data' / 'external-works.json').read_text())
    nodes = works['works']
    edges = []
    stats = Counter()

    for e in q['entries']:
        if e.get('status') == 'parsed':
            stats['already_parsed'] += 1
            continue
        raw = e['raw']
        locus = e.get('locus', 'refsec')
        sc = score(raw)
        threshold = 2 if locus == 'refsec' else 3  # tang prose needs stronger signals
        if sc < threshold:
            e['status'] = 'triaged'
            e['triage'] = 'non_entry'
            stats[f'triaged_{locus}'] += 1
            continue
        authors, title, venue, year = parse_entry(raw)
        key = bibkey(authors, title, year, raw)
        st = ontic(raw, year)
        e['status'] = 'parsed'
        e['parsed'] = {'authors': authors, 'title': title, 'venue': venue,
                       'year': year, 'bibkey': key, 'ontic_status': st,
                       'confidence': min(sc / 5.0, 1.0)}
        stats[f'parsed_{locus}'] += 1
        if st == 'forward_library': stats['forward_library'] += 1
        n = nodes.setdefault(key, {'bibkey': key, 'cited_by': []})
        for f, v in (('authors', authors), ('title', title), ('venue', venue), ('year', year)):
            if v and not n.get(f): n[f] = v
        n['ontic_status'] = st if n.get('ontic_status') in (None, 'unverified') else n['ontic_status']
        if e['source_axn'] not in n['cited_by']:
            n['cited_by'].append(e['source_axn'])
        edges.append({'source_deposit': e['source_deposit'], 'source_axn': e['source_axn'],
                      'target_bibkey': key, 'via': f'{locus}_entry', 'locus': locus,
                      'relation': 'cites', 'ontic_status': st, 'raw': raw[:300]})

    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    q['dateModified'] = now
    q['pending'] = sum(1 for e in q['entries'] if e.get('status') == 'pending')
    q['parsed'] = sum(1 for e in q['entries'] if e.get('status') == 'parsed')
    q['triaged'] = sum(1 for e in q['entries'] if e.get('status') == 'triaged')
    qp.write_text(json.dumps(q, ensure_ascii=False, indent=1) + '\n')

    works['dateModified'] = now
    works['count'] = len(nodes)
    (ROOT / 'data' / 'external-works.json').write_text(json.dumps(works, ensure_ascii=False, indent=1) + '\n')

    (ROOT / 'data' / 'citation-graph-freeform.json').write_text(json.dumps({
        '@context': 'https://schema.org', '@type': 'Dataset',
        'name': 'Alexanarch Freeform Citation Graph (Stage C heuristic layer)',
        'description': 'Edges from freeform reference-section and TANG-body entries, parsed in-session (heuristic bulk pass; refinement retypes relations and settles ontic status). Separate from the mechanical external graph so each regenerates independently.',
        'dateModified': now, 'total_edges': len(edges), 'edges': edges,
    }, ensure_ascii=False, indent=1) + '\n')

    print(dict(stats))
    print(f"queue: parsed {q['parsed']} | triaged {q['triaged']} | pending {q['pending']}")
    print(f"external works now: {len(nodes)} | freeform edges: {len(edges)}")

if __name__ == '__main__':
    main()
