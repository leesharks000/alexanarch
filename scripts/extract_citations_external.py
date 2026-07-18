#!/usr/bin/env python3
"""extract_citations_external.py — Stage A of the Total Citation Graph.

Mechanical extraction of EXTERNAL citations from all canonical texts:
  - external-prefix DOIs (anything not 10.5281)
  - foreign Zenodo DOIs (10.5281 absent from Resolution Index and doi-axn-map)
  - URLs (normalized; own-fleet domains excluded)
  - arXiv IDs; ISBNs
Also segments explicit reference sections into a parse queue for Stage C
(in-session interpretive parsing; No-Double-Draw: never via API).

Outputs (idempotent, fully regenerated each run):
  data/citation-graph-external.json   edges
  data/external-works.json            identifier-keyed nodes
  data/worklists/refsec-parse-queue.json  freeform entries, status=pending
                                          (existing parsed entries preserved)

Deterministic; safe to wire as a deposit_pipeline stage (Stage E).
"""
import json, re, hashlib, pathlib, datetime

APPARATUS_DOMAINS = {'creativecommons.org', 'spdx.org', 'schema.org', 'www.w3.org', 'purl.org', 'licensebuttons.net'}
SELF_PLATFORM_DOMAINS = {'mindcontrolpoems.blogspot.com', 'm.facebook.com', 'www.facebook.com', 'facebook.com', 'medium.com', 'soundcloud.com'}
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXTS = ROOT / 'data' / 'texts'

OWN_DOMAINS = {
    'alexanarch.org', 'www.alexanarch.org', 'machinemediation.org',
    'www.machinemediation.org', 'leesharks.com', 'www.leesharks.com',
    'crimsonhexagonal.org', 'persistentidentifiers.org', 'spxi.dev',
    'semanticphysics.org', 'themandalaoracle.com', 'gravitywell-1.onrender.com',
}

DOI_RE = re.compile(r'\b(10\.\d{4,9}/[^\s\)\]\">,;]+)')
URL_RE = re.compile(r'https?://[^\s\)\]\">]+')
ARXIV_RE = re.compile(r'\barXiv:\s?(\d{4}\.\d{4,5})(v\d+)?', re.I)
ISBN_RE = re.compile(r'\bISBN[:\s-]*((?:97[89][- ]?)?(?:\d[- ]?){9}[\dXx])\b')
REFSEC_RE = re.compile(r'^#{1,4}[^\n]{0,40}\b(Works Cited|References|Bibliography|Sources)\b[^\n]{0,25}$', re.I | re.M)
HEADING_RE = re.compile(r'^#{1,4}\s+\S', re.M)

def norm_doi(d):
    return d.rstrip('.').rstrip(')').rstrip(']').lower()

def norm_url(u):
    u = u.rstrip(".,;:)]'\"")
    u = re.sub(r'#.*$', '', u)
    u = re.sub(r'^https?://', '', u).rstrip('/')
    return u

def url_domain(u):
    return u.split('/')[0].lower()

def main():
    reg = json.loads((ROOT / 'data' / 'registry.json').read_text())
    by_hex = {}
    for d in reg['deposits']:
        hexid = d['axn'].split(':')[1].split('.')[0]
        by_hex[hexid] = (d['deposit_number'], d['axn'])

    # own-DOI universe: resolution index + doi-axn map
    own_dois = set()
    for cand in ['data/doi-resolution-index.json', 'data/doi-axn-map.json']:
        p = ROOT / cand
        if p.exists():
            j = json.loads(p.read_text())
            def harvest(o):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if isinstance(k, str) and k.startswith('10.5281'):
                            own_dois.add(norm_doi(k))
                        harvest(v)
                elif isinstance(o, list):
                    for v in o: harvest(v)
                elif isinstance(o, str) and o.startswith('10.5281'):
                    own_dois.add(norm_doi(o))
            harvest(j)

    edges, nodes = [], {}
    refsec_texts = 0
    queue_entries = []

    def add_edge(src_num, src_axn, bibkey, via, locus, raw):
        edges.append({'source_deposit': src_num, 'source_axn': src_axn,
                      'target_bibkey': bibkey, 'via': via, 'locus': locus,
                      'raw': raw[:300]})
        n = nodes.setdefault(bibkey, {'bibkey': bibkey, 'cited_by': []})
        if src_axn not in n['cited_by']:
            n['cited_by'].append(src_axn)

    for t in sorted(TEXTS.glob('AXN-*-text.md')):
        s = t.read_text(encoding='utf-8', errors='replace')
        hexid = t.name[len('AXN-'):-len('-text.md')]
        if hexid not in by_hex:
            continue
        num, axn = by_hex[hexid]
        body = s.split('---', 2)[-1]

        # refsec span (locus classification + Stage B segmentation)
        rs = REFSEC_RE.search(body)
        refsec_span = (rs.end(), len(body)) if rs else None
        if rs:
            nxt = HEADING_RE.search(body, rs.end())
            refsec_span = (rs.end(), nxt.start() if nxt else len(body))
            refsec_texts += 1
            sec = body[refsec_span[0]:refsec_span[1]]
            for entry in re.split(r'\n\s*\n', sec):
                e = ' '.join(entry.split())
                if len(e) > 25 and not e.startswith('#'):
                    queue_entries.append({'source_deposit': num, 'source_axn': axn,
                                          'raw': e[:600], 'status': 'pending'})

        def locus(pos):
            return 'refsec' if refsec_span and refsec_span[0] <= pos < refsec_span[1] else 'inline'

        for mm in DOI_RE.finditer(body):
            d = norm_doi(mm.group(1))
            if d.startswith('10.5281'):
                if d in own_dois:
                    continue  # internal; handled by citation_extractor.py
                add_edge(num, axn, 'doi:' + d, 'foreign_zenodo', locus(mm.start()), mm.group(0))
            else:
                add_edge(num, axn, 'doi:' + d, 'doi', locus(mm.start()), mm.group(0))
        for mm in ARXIV_RE.finditer(body):
            add_edge(num, axn, 'arxiv:' + mm.group(1), 'arxiv', locus(mm.start()), mm.group(0))
        for mm in ISBN_RE.finditer(body):
            isbn = re.sub(r'[- ]', '', mm.group(1))
            add_edge(num, axn, 'isbn:' + isbn, 'isbn', locus(mm.start()), mm.group(0))
        for mm in URL_RE.finditer(body):
            u = norm_url(mm.group(0))
            dom = url_domain(u)
            if dom in OWN_DOMAINS or 'doi.org' in dom or not dom:
                continue  # own-fleet, or DOI already captured via DOI_RE
            via = 'url_apparatus' if dom in APPARATUS_DOMAINS else ('url_self_platform' if dom in SELF_PLATFORM_DOMAINS else 'url')
            add_edge(num, axn, 'url:' + u, via, locus(mm.start()), mm.group(0))

    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    (ROOT / 'data' / 'citation-graph-external.json').write_text(json.dumps({
        '@context': 'https://schema.org', '@type': 'Dataset',
        'name': 'Alexanarch External Citation Graph (Stage A: mechanical)',
        'description': 'External citation edges extracted mechanically from canonical texts: external-prefix DOIs, foreign Zenodo DOIs, URLs (own-fleet excluded), arXiv IDs, ISBNs. Freeform reference-section entries pending Stage C in-session parsing (see worklists/refsec-parse-queue.json).',
        'dateModified': now, 'total_edges': len(edges), 'edges': edges,
    }, ensure_ascii=False, indent=1) + '\n')

    (ROOT / 'data' / 'external-works.json').write_text(json.dumps({
        'description': 'External works cited by the archive — identifier-keyed nodes (Stage A). Freeform bib: nodes accrue in Stage C; Crossref/Wikidata resolution in Stage D.',
        'dateModified': now, 'count': len(nodes),
        'works': {k: nodes[k] for k in sorted(nodes)},
    }, ensure_ascii=False, indent=1) + '\n')

    # merge queue: preserve any already-parsed entries
    qp = ROOT / 'data' / 'worklists' / 'refsec-parse-queue.json'
    parsed_keep = []
    if qp.exists():
        old = json.loads(qp.read_text())
        parsed_keep = [e for e in old.get('entries', []) if e.get('status') == 'parsed']
        done_raw = {e['raw'] for e in parsed_keep}
        queue_entries = [e for e in queue_entries if e['raw'] not in done_raw]
    qp.write_text(json.dumps({
        'description': 'Stage B/C queue: freeform reference-section entries awaiting in-session interpretive parsing (No-Double-Draw: TACHYON parses in-session; never via API). Parsed entries carry structured records and bib: keys.',
        'dateModified': now,
        'pending': len(queue_entries), 'parsed': len(parsed_keep),
        'entries': parsed_keep + queue_entries,
    }, ensure_ascii=False, indent=1) + '\n')

    print(f'edges: {len(edges)} | external nodes: {len(nodes)} | refsec texts: {refsec_texts} | queue pending: {len(queue_entries)} (parsed kept: {len(parsed_keep)})')
    from collections import Counter
    print('via:', Counter(e['via'] for e in edges).most_common())
    doms = Counter(url_domain(e['target_bibkey'][4:]) for e in edges if e['via'] == 'url')
    print('top cited external domains:', doms.most_common(10))

if __name__ == '__main__':
    main()
