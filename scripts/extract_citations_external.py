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

APPARATUS_DOMAINS = {'creativecommons.org', 'spdx.org', 'schema.org', 'www.w3.org', 'purl.org', 'licensebuttons.net',
                     # page furniture: fonts, CDNs, placeholders, local hosts — present in the text, not cited
                     'fonts.googleapis.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com', 'cdn.jsdelivr.net', 'unpkg.com',
                     'example.org', 'example.com', 'localhost', '127.0.0.1'}
# Hosts where a link names a place on a platform (a profile, a repository, a
# share link, a search, an API) rather than a cited work. Kept as data under
# via=url_platform; the outside-works view shows them only on request.
PLATFORM_DOMAINS = {'orcid.org', 'zenodo.org', 'about.zenodo.org', 'support.zenodo.org', 'github.com',
                    'raw.githubusercontent.com', 'gist.github.com', 'blogger.googleusercontent.com',
                    'share.google', 'claude.ai', 'chatgpt.com', 'chat.openai.com', 'gemini.google.com',
                    'google.com', 'support.google.com', 'developers.google.com', 'scholar.google.com',
                    'search.google.com', 'datacite.org', 'api.datacite.org', 'commons.datacite.org',
                    'search.datacite.org', 'huggingface.co', 'perplexity.ai', 'bing.com', 'copilot.microsoft.com',
                    'web.archive.org', 'archive.org', 'openaire.eu', 'explore.openaire.eu',
                    'academia.edu', 'independent.academia.edu', 'scholar.archive.org', 'semanticscholar.org',
                    'researchgate.net', 'linkedin.com', 'x.com', 'twitter.com', 'substack.com'}
SELF_PLATFORM_DOMAINS = {'mindcontrolpoems.blogspot.com', 'm.facebook.com', 'www.facebook.com', 'facebook.com', 'medium.com', 'soundcloud.com'}
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXTS = ROOT / 'data' / 'texts'

OWN_DOMAINS = {
    'alexanarch.org', 'www.alexanarch.org', 'machinemediation.org',
    'www.machinemediation.org', 'leesharks.com', 'www.leesharks.com',
    'crimsonhexagonal.org', 'persistentidentifiers.org', 'spxi.dev',
    'semanticphysics.org', 'themandalaoracle.com', 'gravitywell-1.onrender.com',
    'alexanarch.freeforums.net',  # the archive's discussion forum (site nav)
}

def fleet_domains():
    """The archive's own sites, from data/fleet-domains.json (the fleet manifest)."""
    p = ROOT / 'data' / 'fleet-domains.json'
    if not p.exists():
        return set()
    return {d['domain'].lower() for d in json.loads(p.read_text()).get('domains', []) if d.get('domain')}

def in_domains(dom, doms):
    dom = dom[4:] if dom.startswith('www.') else dom
    return any(dom == x or dom.endswith('.' + x) for x in doms)

DOI_RE = re.compile(r'\b(10\.\d{4,9}/[^\s\)\]\">,;]+)')
URL_RE = re.compile(r'https?://[^\s\)\]\">]+')
ARXIV_RE = re.compile(r'\barXiv:\s?(\d{4}\.\d{4,5})(v\d+)?', re.I)
ISBN_RE = re.compile(r'\bISBN[:\s-]*((?:97[89][- ]?)?(?:\d[- ]?){9}[\dXx])\b')
TANG_RE = re.compile(r'(Total Axial Negation Graph|\bTANG\b|\bOCTANG\b)', re.I)
# A reference section opens at a markdown heading OR a bold line naming one.
# "Cross-references" and "non-citations" are internal apparatus and stay out.
REFSEC_RE = re.compile(r'^(#{1,4}|\*\*)(?![^\n]*\b(?:cross-?references|non-citations)\b)[^\n]{0,40}\b('
                       r'Works Cited|Works Referenced|References|Bibliography|Sources|Select(?:ed)? Bibliography|'
                       r'Further Reading|Literature Cited|Reference List|External(?: / Archive)? Citations|'
                       r'Forward Library|Primary Sources|Secondary Sources)\b[^\n]{0,30}$', re.I | re.M)
HEADING_RE = re.compile(r'^(#{1,6})\s+\S', re.M)
# a line that begins a new bibliographic entry (as opposed to continuing one)
ENTRY_START = re.compile(r'^\s*(?:[-*\u2022+]\s+|\d{1,3}[.)]\s+|\[\^?\w{1,4}\]:?\s|\u2014{2,3}|-{3}|'
                         r'[A-Z\u00C0-\u024F][\w\'\u2019\-]+(?:\s[A-Z][\w\'\u2019\-]+){0,3}[,.(]|\*[A-Z]|"[A-Z]|\u201c[A-Z])')
# inline-flattened lists: " - Surname, I. (" repeated on one line
INLINE_SPLIT = re.compile(r'\s[-\u2022]\s(?=(?:[A-Z\u00C0-\u024F][\w\'\u2019\-]+(?:\s[A-Z][\w\'\u2019\-]+)?,\s|\d{1,2}\s?U\.S\.C))')


def refsec_spans(body):
    """Every reference section in a body: (start, end) after its heading line.

    A section ends at the next heading of the same or higher level (sub-headings such
    as "### Primary sources" stay inside it); a bold-line opener ends at the next
    heading of any level."""
    spans = []
    for m in REFSEC_RE.finditer(body):
        level = len(m.group(1)) if m.group(1).startswith('#') else 7
        end = len(body)
        for h in HEADING_RE.finditer(body, m.end()):
            if len(h.group(1)) <= level and not REFSEC_RE.match(body, h.start()):
                end = h.start(); break
        if spans and m.start() < spans[-1][1]:
            continue  # nested inside the previous section
        spans.append((m.end(), end))
    return spans


def segment_entries(sec):
    """One entry per bibliographic item: lines that begin an entry start one; other
    non-blank lines continue the entry before them; blank lines close it."""
    out, cur = [], []
    def flush():
        if cur:
            out.append(' '.join(' '.join(cur).split()))
            cur.clear()
    for line in sec.split('\n'):
        if not line.strip():
            flush(); continue
        if line.lstrip().startswith('#'):
            # a heading inside the section opens an entry of its own (in annotated
            # bibliographies the heading IS the citation; a sub-section label stays
            # short and is read as such)
            flush()
            cur.append(line.strip().lstrip('#').strip())
            continue
        if cur and ENTRY_START.match(line):
            flush()
        cur.append(line.strip())
    flush()
    res = []
    for e in out:
        parts = INLINE_SPLIT.split(e) if len(re.findall(r'\b(1[5-9]\d\d|20\d\d)\b', e)) > 1 else [e]
        res.extend(p.strip() for p in parts if p.strip())
    return res

def norm_doi(d):
    # Trailing markdown and punctuation (` * _ ' " ” ’ . , ; : ! ?) is not part of
    # a DOI. Before 2026-10-13 only . ) ] were stripped, so `10.5281/zenodo.N``
    # missed the own-DOI test and an archive DOI was filed as a foreign work.
    d = d.lower().rstrip('`*_\'"\u201d\u2019.,;:!?)]>')
    m = re.match(r'(10\.5281/zenodo\.\d+)', d)
    return m.group(1) if m else d

def norm_url(u):
    u = u.rstrip(".,;:)]'\"*`_")
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

    # The archive's own legacy DOIs that no deposit resolves: the registry's
    # zenodo_dois fields, and the DataCite captures of the archive's account
    # (queried by ORCID and by heteronym creator names). A citation of one of
    # these is a citation of the archive, never of a foreign work.
    for d in reg['deposits']:
        for z in d.get('zenodo_dois') or []:
            if isinstance(z, str):
                own_dois.add(norm_doi(z))
    own_unresolved = set()
    for cand in ['data/datacite-full-backup.json', 'data/datacite-survivors-multi-heteronym.json',
                 'data/heteronym-doi-sift.json']:
        p = ROOT / cand
        if p.exists():
            own_unresolved |= set(re.findall(r'10\.5281/zenodo\.\d+', p.read_text().lower()))
    own_unresolved -= own_dois
    fleet = fleet_domains() | OWN_DOMAINS

    edges, nodes = [], {}
    refsec_texts = 0
    tang_texts = 0
    queue_entries = []

    def add_edge(src_num, src_axn, bibkey, via, locus, raw):
        edges.append({'source_deposit': src_num, 'source_axn': src_axn,
                      'target_bibkey': bibkey, 'via': via, 'locus': locus,
                      'relation': 'cites', 'ontic_status': 'unverified',
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

        # TANG rule (MANUS 2026-07-18): a TANG's entire body IS its citation set
        # (genre spec deposit #542: TANG = <T,C,E,L,S,P>, C = total citation set).
        # Detection: title or early body names the genre. Full body segments into
        # the Stage C queue with locus='tang'; relation typing per the TANG edge
        # vocabulary happens at parse time.
        title_zone = s[:600] + body[:800]
        is_tang = bool(TANG_RE.search(title_zone))
        if is_tang:
            tang_texts += 1
            for entry in re.split(r'\n\s*\n', body):
                e = ' '.join(entry.split())
                if len(e) > 25 and not e.startswith('#'):
                    queue_entries.append({'source_deposit': num, 'source_axn': axn,
                                          'raw': e[:600], 'locus': 'tang',
                                          'status': 'pending'})

        # refsec spans (locus classification + Stage B segmentation)
        spans = refsec_spans(body)
        if spans:
            refsec_texts += 1
        for a, b in spans:
            for e in segment_entries(body[a:b]):
                if len(e) > 25 and not e.startswith('#'):
                    queue_entries.append({'source_deposit': num, 'source_axn': axn,
                                          'raw': e[:1200], 'locus': 'refsec',
                                          'status': 'pending'})

        def locus(pos):
            return 'refsec' if any(a <= pos < b for a, b in spans) else 'inline'

        for mm in DOI_RE.finditer(body):
            d = norm_doi(mm.group(1))
            if d.startswith('10.5281'):
                if d in own_dois:
                    continue  # internal; handled by citation_extractor.py
                via = 'own_zenodo_unresolved' if d in own_unresolved else 'foreign_zenodo'
                add_edge(num, axn, 'doi:' + d, via, locus(mm.start()), mm.group(0))
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
            if 'doi.org' in dom or not dom:
                continue  # DOI already captured via DOI_RE
            if dom.endswith('.internal') or dom.endswith('.local'):
                via = 'url_apparatus'
            elif in_domains(dom, fleet):
                via = 'url_fleet'          # the archive's own sites (fleet manifest)
            elif dom in APPARATUS_DOMAINS:
                via = 'url_apparatus'
            elif dom in SELF_PLATFORM_DOMAINS:
                via = 'url_self_platform'
            elif in_domains(dom, PLATFORM_DOMAINS):
                via = 'url_platform'
            else:
                via = 'url'                # an outside host
            add_edge(num, axn, 'url:' + u, via, locus(mm.start()), mm.group(0))

    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    (ROOT / 'data' / 'citation-graph-external.json').write_text(json.dumps({
        '@context': 'https://schema.org', '@type': 'Dataset',
        'name': 'Alexanarch External Citation Graph (Stage A: mechanical)',
        'edge_fields': {'relation': 'TANG edge vocabulary (genre spec, deposit #542): cites | critiques | builds_upon | temporal_precedence | methodological_lineage | contradiction. Mechanical extraction defaults to cites; Stage C retypes.',
                        'ontic_status': 'real (verified existent) | forward_library (cited before existence) | fictive_retro (invented past work) | unverified (default until Stage C/D classification). Fictive and forward citations are first-class literary structure, never broken links.'},
        'description': 'External citation edges extracted mechanically from canonical texts: external-prefix DOIs, Zenodo DOIs the archive does not hold, URLs, arXiv IDs, ISBNs. Freeform reference-section entries are parsed into citation-graph-freeform.json.',
        'via_classes': {
            'doi': 'a DOI outside Zenodo', 'arxiv': 'an arXiv identifier', 'isbn': 'an ISBN',
            'foreign_zenodo': 'a Zenodo DOI not found among the archive\'s own DOIs',
            'own_zenodo_unresolved': 'one of the archive\'s own legacy Zenodo DOIs (DataCite captures of the account) that no deposit resolves; a citation of the archive, not an outside work',
            'url': 'a link to an outside host', 'url_fleet': 'a link to one of the archive\'s own sites (data/fleet-domains.json)',
            'url_platform': 'a link to a place on a platform (profile, repository, share link, search, API) rather than a cited work',
            'url_self_platform': 'a link to the author\'s own platform account (blog, Medium, SoundCloud, Facebook)',
            'url_apparatus': 'licence, schema, font, CDN, placeholder or local host: page furniture, not cited'},
        'dateModified': now, 'total_edges': len(edges), 'edges': edges,
    }, ensure_ascii=False, indent=1) + '\n')

    (ROOT / 'data' / 'external-works.json').write_text(json.dumps({
        'description': 'External works cited by the archive — identifier-keyed nodes (Stage A). Freeform bib: nodes accrue in Stage C; Crossref/Wikidata resolution in Stage D.',
        'dateModified': now, 'count': len(nodes),
        'works': {k: nodes[k] for k in sorted(nodes)},
    }, ensure_ascii=False, indent=1) + '\n')

    # merge queue: preserve every entry that has reached a TERMINAL status.
    # Terminal = parsed, or a triage class naming what the segment actually is
    # (refsec_parse.py). Only `pending` is regenerated. Without this, each run
    # reset finished triage to pending and the same non-references were re-queued
    # forever — work recorded as owed where none was.
    TERMINAL = {'parsed', 'relation_line', 'legal_citation', 'apparatus',
                'prose', 'provenance_row', 'bare_url', 'nav_relation', 'footnote', 'tang_prose', 'not_reference'}
    qp = ROOT / 'data' / 'worklists' / 'refsec-parse-queue.json'
    parsed_keep = []
    retired = 0
    if qp.exists():
        old = json.loads(qp.read_text())
        # A finished entry is kept only while its text is still a segment of the
        # current segmentation; an entry from an older segmentation (several
        # references run together, cut at 600 characters) is retired, and its
        # parts re-enter the queue on their own.
        current = {(e['source_deposit'], e['raw']) for e in queue_entries}
        olds = [e for e in old.get('entries', []) if e.get('status') in TERMINAL]
        parsed_keep = [e for e in olds if (e['source_deposit'], e['raw']) in current]
        retired = len(olds) - len(parsed_keep)
        done = {(e['source_deposit'], e['raw']) for e in parsed_keep}
        seen = set(); fresh = []
        for e in queue_entries:
            k = (e['source_deposit'], e['raw'])
            if k in done or k in seen:
                continue
            seen.add(k); fresh.append(e)
        queue_entries = fresh
    qp.write_text(json.dumps({
        'description': 'Stage B/C queue: freeform reference-section entries awaiting in-session interpretive parsing (No-Double-Draw: TACHYON parses in-session; never via API). Parsed entries carry structured records and bib: keys.',
        'dateModified': now,
        'pending': len(queue_entries),
        'parsed': sum(1 for e in parsed_keep if e.get('status') == 'parsed'),
        'triaged': sum(1 for e in parsed_keep if e.get('status') != 'parsed'),
        'retired_from_older_segmentation': retired,
        'entries': parsed_keep + queue_entries,
    }, ensure_ascii=False, indent=1) + '\n')

    print(f'edges: {len(edges)} | external nodes: {len(nodes)} | refsec texts: {refsec_texts} | TANG texts: {tang_texts} | queue pending: {len(queue_entries)} (terminal kept: {len(parsed_keep)})')
    from collections import Counter
    print('via:', Counter(e['via'] for e in edges).most_common())
    doms = Counter(url_domain(e['target_bibkey'][4:]) for e in edges if e['via'] == 'url')
    print('top cited external domains:', doms.most_common(10))

if __name__ == '__main__':
    main()
