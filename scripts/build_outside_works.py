#!/usr/bin/env python3
"""build_outside_works.py — one row per work the archive cites, for /citations.

READS
  data/citation-graph-freeform.json   parsed reference-section and TANG entries
  data/citation-graph-external.json   mechanical DOIs, arXiv IDs, ISBNs, Zenodo DOIs, URLs
  data/registry.json                  deposit titles (to recognise the archive's own works)

WRITES
  data/outside-works.json             rows, sortable by the /citations "Outside works" view
  data/outside-works.csv              the same rows, flat

A ROW is one cited work. Parsed entries are grouped by first-author surname and
normalised title; an identifier (DOI, arXiv, ISBN) found inside a parsed entry
ties the mechanical edge for that identifier to the same row, so the row has a
title. Identifier and URL edges with no parsed entry become rows of their own.

KIND
  book · article · reference    parsed entries (venue shape decides; reference when neither)
  doi · arxiv · isbn            an identifier with no parsed entry
  zenodo                        a Zenodo DOI not among the archive's own
  web                           a link to an outside host
  platform                      a place on a platform (profile, repository, share link, API)
  archive                       the archive's own work: a heteronym author, or a title that
                                matches a deposit, or one of its own unresolved legacy DOIs

Parsing is heuristic (refsec_parse.py); every row carries a raw sample so the
reader can see what was parsed. Nothing here is verified against the world:
ontic_status stays as the graphs give it.

    python3 scripts/build_outside_works.py           # write
    python3 scripts/build_outside_works.py --check   # report whether the committed files are current
"""
import csv, io, json, re, sys, pathlib, datetime
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / 'data' / 'outside-works.json'
OUT_CSV = ROOT / 'data' / 'outside-works.csv'

# The heteronyms and the archive's collective signatures. A work by one of
# these is the archive's own, whatever venue the entry names.
OWN_SURNAMES = {'sharks', 'sigil', 'fraction', 'cranes', 'vox', 'dancings', 'morrow', 'glas',
                'kuro', 'wells', 'trace', 'feist', 'spellings', 'kenning', 'tachyon'}
OWN_PHRASES = ('crimson hexagonal', 'semantic economy institute', 'the assembly', 'assembly chorus')

DOI_IN = re.compile(r'\b(10\.\d{4,9}/[^\s\)\]\">,;`*]+)', re.I)
ARXIV_IN = re.compile(r'arXiv[:\s]*(\d{4}\.\d{4,5})', re.I)
ISBN_IN = re.compile(r'ISBN[:\s-]*((?:97[89][- ]?)?(?:\d[- ]?){9}[\dXx])\b')
ARTICLE_HINT = re.compile(r'\b(Journal|Review|Quarterly|Proceedings|Transactions|Studies|Magazine|Annals|Bulletin|'
                          r'Inquiry|Science|Nature|arXiv|PNAS|Letters|Philology|Classical|Conference|Workshop|'
                          r'NeurIPS|ICML|ACL|EMNLP|CHI|First Monday|Society|Mind|Phronesis|Mnemosyne)\b')
BOOK_HINT = re.compile(r'\b(Press|University|Verso|Routledge|Blackwell|Wiley|Springer|Penguin|Norton|Vintage|'
                       r'Semiotext|Zone Books|Polity|Continuum|Bloomsbury|Brill|Palgrave|Sage|Clarendon|Teubner|'
                       r'Loeb|Harper|Knopf|Random House|Basic Books|Beacon|Belknap|Oxford|Cambridge|Chicago|'
                       r'Columbia|Princeton|Stanford|Yale|Harvard|Duke|Minnesota|Cornell|MIT)\b')


def norm(s):
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())


def norm_doi(d):
    d = d.lower().rstrip('`*_\'"”’.,;:!?)]>')
    m = re.match(r'(10\.5281/zenodo\.\d+)', d)
    return m.group(1) if m else d


def surname(authors):
    a = (authors or '').strip()
    if not a:
        return ''
    first = re.split(r'\s*(?:;|&|\band\b|\bet al\b)\s*', a)[0]
    first = first.split(',')[0] if ',' in first else first.split()[-1]
    return norm(first)


def is_own(authors, title, raw):
    low = ' '.join([authors or '', raw or '']).lower()
    if any(p in low for p in OWN_PHRASES):
        return True
    names = re.split(r'\s*(?:;|&|\band\b|,)\s*', (authors or '').lower())
    return any(norm(n.split()[-1] if n.split() else n) in OWN_SURNAMES or norm(n) in OWN_SURNAMES
               for n in names if n.strip())


def kind_of(p, raw):
    venue = p.get('venue') or ''
    if ARTICLE_HINT.search(venue) or re.search(r'\b\d+\s*\(\d+\)|\bvol\.|\bpp?\.\s*\d', raw, re.I):
        return 'article'
    if BOOK_HINT.search(venue) or BOOK_HINT.search(raw) or ISBN_IN.search(raw):
        return 'book'
    return 'reference'


JUNK_TITLE = re.compile(r'^(?:\(?\d{4}[a-z]?\)?[.,]?|citation|citations|references?|sources?|notes?|et al\.?)$', re.I)


def clean_title(t):
    t = re.sub(r'^\(?\d{4}[a-z]?\)?[.,:]?\s*', '', (t or '').strip())   # "(2024). Title" -> "Title"
    t = re.sub(r'^et al\.?\s*', '', t).strip(' .,;')
    return t


# a venue parsed into the title slot ("arXiv preprint arXiv:2212.08073", "Advances in Neural
# Information Processing Systems"): the row shows the entry as written instead
VENUEISH = re.compile(r'^(arXiv\b|Advances in Neural|(In )?Proceedings\b|Communications of the ACM|Journal of\b|Nature\s+\d)', re.I)


def title_key(t, a):
    n = norm(t)
    n = re.sub(r'^(the|a|an)(?=[a-z])', '', n)
    # long titles key alone, so spellings of the author ("Shumailov, I." / "Shumailov, Ilia, et al" /
    # none) do not split one work into several rows; short titles ("On the Sublime") need the surname
    return 'w:' + (n[:45] if len(n) >= 24 else surname(a) + '|' + n)


def build():
    reg = json.loads((ROOT / 'data' / 'registry.json').read_text())
    title_to_dep = {}
    for d in reg['deposits']:
        t = norm(d.get('title', ''))
        if len(t) >= 16:
            title_to_dep.setdefault(t[:60], d['deposit_number'])

    ff = json.loads((ROOT / 'data' / 'citation-graph-freeform.json').read_text())['edges']
    ex = json.loads((ROOT / 'data' / 'citation-graph-external.json').read_text())['edges']

    rows = {}
    id_to_row = {}
    set_aside = 0

    def row(key, **init):
        r = rows.get(key)
        if r is None:
            r = rows[key] = dict({'id': key, 'title': None, 'authors': None, 'year': None, 'venue': None,
                                  'kind': None, 'identifiers': [], 'deposit': None, 'cited_by': set(),
                                  'raw': None, 'confidence': None, 'ontic_status': 'unverified'}, **init)
        return r

    # 1. parsed entries
    # read entries first, so a row takes its fields from the reading where there is one
    ff = sorted(ff, key=lambda e: 0 if e.get('read') else 1)
    for e in ff:
        if e.get('read'):
            t, a = (e.get('title') or '').strip(), e.get('authors')
            if not t:
                set_aside += 1; continue
            key = title_key(t, a)
            r = row(key)
            if not r.get('read'):
                for f in ('title', 'authors', 'year', 'venue'):
                    r[f] = e.get(f) or r[f]
                r['raw'], r['confidence'] = e.get('raw'), 1.0
            st = e.get('ontic_status') or 'unverified'
            # the work's status across its citations: a work any citation identifies as
            # existing is real; one cited ahead of its existence in some deposit keeps that
            # fact in forward_in. Otherwise forward > fictive > unverified.
            RANK = {'real': 3, 'forward_library': 2, 'fictive_retro': 1, 'unverified': 0}
            if not r.get('read') or RANK.get(st, 0) > RANK.get(r['ontic_status'], 0):
                r['ontic_status'] = st
            if st == 'forward_library':
                r.setdefault('forward_in', set()).add(e['source_deposit'])
            r['read'] = True
            if e.get('basis') and not r.get('basis'):
                r['basis'] = e['basis']
            r['form'] = e.get('kind')
            r['kind'] = 'archive' if (e.get('own') or e.get('deposit')) else e.get('kind')
            if e.get('deposit'):
                r['deposit'] = e['deposit']
            r['cited_by'].add(e['source_deposit'])
            raw = e.get('raw') or ''
            for m in DOI_IN.finditer(raw):
                i = 'doi:' + norm_doi(m.group(1)); id_to_row.setdefault(i, key)
                if i not in r['identifiers']: r['identifiers'].append(i)
            for m in ARXIV_IN.finditer(raw):
                i = 'arxiv:' + m.group(1); id_to_row.setdefault(i, key)
                if i not in r['identifiers']: r['identifiers'].append(i)
            for m in ISBN_IN.finditer(raw):
                i = 'isbn:' + re.sub(r'[- ]', '', m.group(1)); id_to_row.setdefault(i, key)
                if i not in r['identifiers']: r['identifiers'].append(i)
            continue
        t, a = clean_title(e.get('title')), e.get('authors')
        if not t or len(t) < 8 or t.endswith(':') or JUNK_TITLE.match(t):
            set_aside += 1      # a parse with no usable title; the entry stays in the freeform graph
            continue
        if VENUEISH.match(t):
            raw0 = re.sub(r'\s+', ' ', e.get('raw') or '').strip()
            e = dict(e, title=raw0[:160], venue=e.get('venue') or t, confidence=min(e.get('confidence') or 0.5, 0.4))
            t = e['title']
        e = dict(e, title=t)
        key = title_key(t, a)
        r = row(key)
        if r.get('read'):
            r['cited_by'].add(e['source_deposit'])   # a reading already settled this work
            continue
        for f in ('title', 'authors', 'year', 'venue'):
            if e.get(f) and not r[f]:
                r[f] = e[f]
        if not r['raw'] or (e.get('confidence') or 0) > (r['confidence'] or 0):
            r['raw'], r['confidence'] = e.get('raw'), e.get('confidence')
        if e.get('ontic_status') and e['ontic_status'] != 'unverified':
            r['ontic_status'] = e['ontic_status']
        r['cited_by'].add(e['source_deposit'])
        dep = title_to_dep.get(norm(t)[:60])
        if dep:
            r['deposit'] = dep
        raw = e.get('raw') or ''
        for m in DOI_IN.finditer(raw):
            i = 'doi:' + norm_doi(m.group(1)); id_to_row.setdefault(i, key)
            if i not in r['identifiers']: r['identifiers'].append(i)
        for m in ARXIV_IN.finditer(raw):
            i = 'arxiv:' + m.group(1); id_to_row.setdefault(i, key)
            if i not in r['identifiers']: r['identifiers'].append(i)
        for m in ISBN_IN.finditer(raw):
            i = 'isbn:' + re.sub(r'[- ]', '', m.group(1)); id_to_row.setdefault(i, key)
            if i not in r['identifiers']: r['identifiers'].append(i)
        if r['deposit'] or is_own(r['authors'], r['title'], raw):
            r['kind'] = 'archive'
        elif r['kind'] != 'archive':
            r['kind'] = kind_of(r, raw)

    # 2. mechanical edges
    VIA_KIND = {'doi': 'doi', 'arxiv': 'arxiv', 'isbn': 'isbn', 'foreign_zenodo': 'zenodo',
                'own_zenodo_unresolved': 'archive', 'url': 'web', 'url_platform': 'platform'}
    for e in ex:
        k = VIA_KIND.get(e['via'])
        if not k:
            continue  # url_fleet, url_self_platform, url_apparatus: the archive's own or furniture
        bk = e['target_bibkey']
        if bk.startswith('doi:'):
            bk = 'doi:' + norm_doi(bk[4:])
        if bk in id_to_row:
            rows[id_to_row[bk]]['cited_by'].add(e['source_deposit'])
            continue
        r = row(bk, kind=k)
        if bk not in r['identifiers']:
            r['identifiers'].append(bk)
        if not r['raw']:
            r['raw'] = e.get('raw')
        if k in ('web', 'platform'):
            r['venue'] = bk[4:].split('/')[0]
            r['title'] = bk[4:]
        elif not r['title']:
            r['title'] = bk.split(':', 1)[1]   # the identifier is the only name the text gives
        r['cited_by'].add(e['source_deposit'])

    out = []
    for r in rows.values():
        cb = sorted(r['cited_by'])
        y = r['year']
        extra = {k: r[k] for k in ('form', 'basis') if r.get(k)}
        if r.get('forward_in') and r['ontic_status'] == 'real':
            extra['forward_in'] = sorted(r['forward_in'])   # cited ahead of its existence here
        extra['read'] = bool(r.get('read'))
        out.append({'id': r['id'], 'kind': r['kind'] or 'reference', 'title': r['title'], 'authors': r['authors'], **extra,
                    'year': y, 'venue': r['venue'], 'identifiers': r['identifiers'], 'deposit': r['deposit'],
                    'cited_by_count': len(cb), 'cited_by': cb, 'raw': (r['raw'] or '')[:300],
                    'confidence': r['confidence'], 'ontic_status': r['ontic_status']})
    out.sort(key=lambda x: (-x['cited_by_count'], (x['authors'] or x['title'] or '').lower()))
    return out, set_aside


def render(out, set_aside=0):
    from collections import Counter
    kinds = Counter(r['kind'] for r in out)
    doc = {
        '@context': 'https://schema.org', '@type': 'Dataset',
        'name': 'Alexanarch — works cited',
        'description': ('One row per work the archive cites: parsed reference-section entries '
                        '(citation-graph-freeform.json) merged with mechanically extracted DOIs, arXiv IDs, '
                        'ISBNs, Zenodo DOIs and outside links (citation-graph-external.json). Parsing is '
                        'heuristic; each row carries a raw sample. Kind "archive" marks the archive\'s own '
                        'works; "platform" marks links to a place on a platform rather than a work. '
                        'Nothing is verified against the world.'),
        'url': 'https://www.alexanarch.org/citations/#outside',
        'license': 'https://creativecommons.org/licenses/by/4.0/',
        'creator': {'@type': 'Person', 'name': 'Lee Sharks', 'identifier': 'https://orcid.org/0009-0000-1599-0703'},
        'isBasedOn': ['https://www.alexanarch.org/data/citation-graph-freeform.json',
                      'https://www.alexanarch.org/data/citation-graph-external.json'],
        'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'text/csv',
                          'contentUrl': 'https://www.alexanarch.org/data/outside-works.csv'}],
        'builder': 'scripts/build_outside_works.py',
        'total_works': len(out),
        'by_kind': dict(kinds.most_common()),
        'citing_deposits': len({n for r in out for n in r['cited_by']}),
        'parsed_entries_set_aside': set_aside,
        'by_ontic_status': dict(Counter(r['ontic_status'] for r in out).most_common()),
        'read': sum(1 for r in out if r.get('read')),
        'ontic_status_vocabulary': {
            'real': 'the reader identifies the work as existing',
            'unverified': 'not identified: plausible, or parsed but not yet read',
            'forward_library': 'Retrocausal Citation Entry · Forward Library · not a historical publication record',
            'fictive_retro': 'an invented past work, cited as though it existed'},
        'fields': {'kind': 'book | article | chapter | paper | preprint | thesis | report | web | post | legal | scripture | classical | dataset | software | media | other | reference | doi | arxiv | isbn | zenodo | platform | archive',
                   'forward_in': 'for a real work: deposits that cited it ahead of its existence (forthcoming, DOI to be minted)',
                   'read': 'true when the entry was read in session (data/citation-readings.json); false when parsed by heuristic only',
                   'form': 'for kind archive: the form of the archive\'s own work as read (book, post, archive deposit...)',
                   'basis': 'the reader\'s note on a status that is not obvious',
                   'deposit': 'the deposit whose title the cited title matches (kind archive)',
                   'cited_by': 'deposit numbers citing the work', 'raw': 'one source entry as written',
                   'confidence': 'parser confidence for parsed entries (refsec_parse.py)'},
        'works': out,
    }
    js = json.dumps(doc, ensure_ascii=False, separators=(',', ':')) + '\n'
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(['kind', 'authors', 'title', 'year', 'venue', 'identifiers', 'cited_by_count', 'cited_by', 'deposit', 'raw'])
    for r in out:
        w.writerow([r['kind'], r['authors'] or '', r['title'] or '', r['year'] or '', r['venue'] or '',
                    ' '.join(r['identifiers']), r['cited_by_count'], ' '.join(map(str, r['cited_by'])),
                    r['deposit'] or '', r['raw']])
    return js, buf.getvalue(), kinds


def main():
    out, set_aside = build()
    js, cs, kinds = render(out, set_aside)
    if '--check' in sys.argv:
        cur = OUT_JSON.exists() and OUT_JSON.read_text() == js and OUT_CSV.exists() and OUT_CSV.read_text() == cs
        print('outside-works: current' if cur else 'outside-works: STALE — run scripts/build_outside_works.py')
        sys.exit(0 if cur else 1)
    OUT_JSON.write_text(js)
    OUT_CSV.write_text(cs)
    print(f'outside-works: {len(out)} works · ' + ' · '.join(f'{k} {v}' for k, v in kinds.most_common())
          + f' · {OUT_JSON.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
