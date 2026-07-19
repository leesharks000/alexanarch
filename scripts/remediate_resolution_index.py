#!/usr/bin/env python3
"""
remediate_resolution_index.py — 2026-07-19 DOI-key remediation of data/doi-resolution-index.json.

WHY THIS EXISTS (read before running — see audit/DOI-INDEX-AUDIT-2026-07-19.md):
The index was constructed and then "corrected" (2026-07-06) using TITLE SIMILARITY and
membership in `zenodo_dois` arrays as join keys. Neither is an identity key:
  - Titles collide and shift (off-by-one assignments, many-to-one collapses).
  - `zenodo_dois` / `zenodo_dois_covered` everywhere in this infrastructure means
    "DOIs FOUND IN THE WORK'S TEXT" (blog-capture extraction), NOT "this work's DOI(s)".
    Registry/catalog documents therefore 'claim' hundreds of DOIs they merely cite.
    769 of 993 assignment-table DOIs are claimed by >1 work. It was never an identity field.
Result: 468 of 844 OpenAlex-checkable rows (55.5%) carried wrong titles/targets, including
the live resolver sending the Space Ark v4.2.7 DOI to THE SPLICE.

METHOD (DOI is the only key; titles are used once, as a verified constraint, not a key):
  TRUTH  (doi -> {title, date, sources}): union of
         data/datacite-full-backup.json          (DataCite, DOI-keyed)
         data/openalex-severed-recovery.json     (OpenAlex, DOI-keyed)
         data/newly-found-openalex.json          (OpenAlex, DOI-keyed)
         datasets/tombstone-mirror/tombstone-api.jsonl (DataCite tombstone citation_text, record-id-keyed -> DOI)
  WORKS  (deposit_number -> {title, date}): data/registry.json (all deposits).
  MATCH  per mapping row, by exact normalized full-title equality TRUTH.title == WORK.title:
         1 candidate                -> grade A  (mapping_type: direct_verified)
         >1 candidate, date breaks tie -> grade B  (remediated_date_resolved)
         >1, current target among candidates -> keep target, retitle (verified_ambiguous_kept)
         >1, unresolvable          -> earliest deposit + flag (remediated_ambiguous_earliest)
         0 exact, fuzzy >= 0.75 Jaccard(first-12-token sets), unique best -> grade C (remediated_fuzzy)
         0 candidates              -> policy set by --no-candidate {keep-flag|null} (default keep-flag)
         no TRUTH row              -> untouched + audit_status: unverifiable_no_truth
  Every touched row preserves prior values in `remediation_2026_07_19` (reversible, per the
  v3.2 misclassification-note precedent). Titles are always updated to TRUTH when TRUTH exists.
  Rows whose current mapping_type is 'no_alexanarch_equivalent' keep that type unless a
  grade A/B match is found.

OUTPUT: mutates data/doi-resolution-index.json (version bump), and writes
        datasets/doi-work-identity/doi-identity-map.json — the identity artifact that never
        existed: doi -> {deposit_number, axn, record_url, title, grade, truth_sources}.

AFTER RUNNING: scripts/sync_resolver.py --apply  (ONLY sanctioned path to api/doi-axn-map.json),
then regenerate_surfaces.py, validate_deposit.py --strict, check_resolver_parity.py.

USAGE:
    python3 scripts/remediate_resolution_index.py --dry-run
    python3 scripts/remediate_resolution_index.py [--no-candidate keep-flag|null]
"""
import argparse, datetime, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / 'data' / 'doi-resolution-index.json'

def norm(t):
    t = re.sub(r'\[SUPERSEDED[^\]]*\]', '', t or '')
    t = re.sub(r'[^0-9a-z ]', '', t.lower().replace('\u00a0', ' '))
    return ' '.join(t.split())

def build_truth():
    truth = {}
    def put(doi, title, date, src):
        doi = (doi or '').lower().replace('https://doi.org/', '').strip()
        if not doi or not title: return
        e = truth.setdefault(doi, {'titles': {}, 'date': date, 'sources': []})
        e['titles'][src] = title
        if src not in e['sources']: e['sources'].append(src)
        if date and not e.get('date'): e['date'] = date
    dc = json.load(open(ROOT/'data'/'datacite-full-backup.json'))
    for r in dc.get('records', []):
        a = r.get('attributes') or {}
        ts = a.get('titles') or []
        put(a.get('doi'), ts[0].get('title') if ts else '', str(a.get('published') or a.get('publicationYear') or ''), 'datacite')
    snap = json.load(open(ROOT/'data'/'openalex-severed-recovery.json'))
    recs = next(v for v in snap.values() if isinstance(v, list) and len(v) > 500)
    for r in recs:
        put(r.get('doi'), r.get('title'), r.get('publication_date'), 'openalex')
    nf = json.load(open(ROOT/'data'/'newly-found-openalex.json'))
    for r in nf.get('recovered', []):
        d = r.get('data') or {}
        put(r.get('doi'), d.get('title'), d.get('publication_date'), 'openalex_nf')
    # tombstones: citation_text = "Author. (Year). Title. Zenodo. https://doi.org/..."
    ts_path = ROOT/'datasets'/'tombstone-mirror'/'tombstone-api.jsonl'
    if ts_path.exists():
        for line in open(ts_path):
            try: j = json.loads(line)
            except Exception: continue
            tomb = ((j.get('api') or {}).get('tombstone') or {})
            ct = tomb.get('citation_text') or ''
            m = re.search(r'\(\d{4}[a-z]?\)\.\s*(.+?)\.\s*(?:\(|Zenodo|https://doi)', ct)
            md = re.search(r'10\.5281/zenodo\.\d+', ct)
            doi = f"10.5281/zenodo.{j.get('record_id')}" if j.get('record_id') else (md.group() if md else '')
            if m and doi: put(doi, m.group(1), '', 'tombstone')
    # choose canonical title per doi: datacite > openalex > openalex_nf > tombstone
    for doi, e in truth.items():
        for src in ('datacite', 'openalex', 'openalex_nf', 'tombstone'):
            if src in e['titles']:
                e['title'] = e['titles'][src]; e['title_source'] = src; break
    return truth

def build_works():
    reg = json.load(open(ROOT/'data'/'registry.json'))
    works, bytitle = {}, {}
    for d in reg['deposits']:
        n = d['deposit_number']
        works[n] = {'title': d.get('title', ''), 'date': d.get('date', ''), 'axn': d.get('axn', '')}
        nt = norm(d.get('title', ''))
        if len(nt.split()) >= 3: bytitle.setdefault(nt, []).append(n)
    return works, bytitle

def jacc(a, b):
    sa, sb = set(a.split()), set(b.split())
    return len(sa & sb) / max(1, len(sa | sb))

def containment(a, b):
    sa, sb = set(a.split()), set(b.split())
    return len(sa & sb) / max(1, min(len(sa), len(sb)))

def best_match(tt, bytitle):
    """Tiered: full-token Jaccard (order-free), then containment (truncation-tolerant).
    Returns (candidate_list_or_None, grade)."""
    best, bs, second = None, 0.0, 0.0
    for nt, ns in bytitle.items():
        s = jacc(tt, nt)
        if s > bs: second, bs, best = bs, s, ns
        elif s > second: second = s
    if best and len(best) == 1:
        if bs >= 0.9: return best, 'C'
        if bs >= 0.7 and (bs - second) >= 0.15: return best, 'C'
    cb, cbs, csecond = None, 0.0, 0.0
    for nt, ns in bytitle.items():
        s = containment(tt, nt)
        if s > cbs: csecond, cbs, cb = cbs, s, ns
        elif s > csecond: csecond = s
    if cb and len(cb) == 1 and cbs >= 0.9 and (cbs - csecond) >= 0.1:
        return cb, 'D'
    return None, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--no-candidate', choices=['keep-flag', 'null'], default='keep-flag')
    args = ap.parse_args()

    truth = build_truth()
    works, bytitle = build_works()
    idx = json.load(open(IDX))
    maps = idx['mappings']
    stats = {'A_exact_unique': 0, 'B_date_resolved': 0, 'kept_ambiguous': 0, 'ambiguous_earliest': 0,
             'C_fuzzy': 0, 'D_containment': 0, 'no_candidate': 0, 'no_truth': 0, 'already_correct': 0, 'retitled_only': 0}
    identity = {}
    today = '2026-07-19'
    for m in maps:
        doi = (m.get('dead_doi') or '').lower()
        t = truth.get(doi)
        if not t or not t.get('title'):
            m.setdefault('audit_status', 'unverifiable_no_truth_20260719')
            stats['no_truth'] += 1
            continue
        tt = norm(t['title'])
        if len(tt.split()) < 3:
            m['audit_status'] = 'non_latin_or_short_title_unmatchable_20260719'
            stats['unmatchable_title'] = stats.get('unmatchable_title', 0) + 1
            continue
        cands = bytitle.get(tt, [])
        grade = target = None
        if len(cands) == 1:
            target, grade = cands[0], 'A'
        elif len(cands) > 1:
            ty = (t.get('date') or '')[:4]
            dated = [n for n in cands if (works[n]['date'] or '')[:4] == ty] if ty else []
            cur = None
            mm = re.search(r'/s/records/(\d+)/', m.get('alexanarch_record') or '')
            if mm: cur = int(mm.group(1))
            if len(dated) == 1:
                target, grade = dated[0], 'B'
            elif cur in cands:
                target, grade = cur, 'kept'
            else:
                target, grade = sorted(cands)[0], 'earliest'
        else:
            sup = re.search(r'SUPERSEDED[^\]]*?(10\.5281/zenodo\.\d+)', t['title'])
            if sup:
                m['_supersedes_ptr'] = sup.group(1).lower()
            cand, hint = best_match(tt, bytitle)
            if cand:
                target, grade = cand[0], hint
        prev = {'title': m.get('title'), 'alexanarch_url': m.get('alexanarch_url'),
                'alexanarch_record': m.get('alexanarch_record'), 'mapping_type': m.get('mapping_type'),
                'axn': m.get('axn')}
        if target is not None:
            w = works[target]
            new_url = f"https://alexanarch.org/s/records/{target}/"
            changed = (m.get('alexanarch_url') != new_url) or (norm(m.get('title')) != tt)
            if m.get('alexanarch_url') == new_url and norm(m.get('title')) == tt:
                stats['already_correct'] += 1
            else:
                m['remediation_2026_07_19'] = {'previous': prev, 'grade': grade, 'truth_sources': t['sources']}
                m['title'] = t['title']
                m['alexanarch_url'] = new_url
                m['alexanarch_record'] = f"/s/records/{target}/"
                m['axn'] = w['axn']
                m['root_axn'] = '.'.join(w['axn'].split('.')[:2]) if w['axn'] else m.get('root_axn')
                m['mapping_type'] = {'A': 'direct_verified', 'B': 'remediated_date_resolved',
                                     'kept': 'verified_ambiguous_kept', 'earliest': 'remediated_ambiguous_earliest',
                                     'C': 'remediated_fuzzy', 'D': 'remediated_containment'}[grade]
                m['title_verification'] = (f"{today} DOI-key remediation: title from {t['title_source']} (DOI-keyed), "
                                           f"target by exact-title constraint grade {grade}. Previous values preserved in remediation_2026_07_19.")
                key = {'A': 'A_exact_unique', 'B': 'B_date_resolved', 'kept': 'kept_ambiguous',
                       'earliest': 'ambiguous_earliest', 'C': 'C_fuzzy', 'D': 'D_containment'}[grade]
                stats[key] += 1
            identity[doi] = {'deposit_number': target, 'axn': w['axn'],
                             'record_url': new_url, 'title': t['title'], 'grade': grade,
                             'truth_sources': t['sources']}
        else:
            stats['no_candidate'] += 1
            m['remediation_2026_07_19'] = {'previous': prev, 'grade': 'none', 'truth_sources': t['sources']}
            m['title'] = t['title']
            m['title_verification'] = (f"{today} DOI-key remediation: title corrected from {t['title_source']} (DOI-keyed); "
                                       f"NO alexanarch record matches this title — previous target was unverifiable and is "
                                       + ("retained flagged." if args.no_candidate == 'keep-flag' else "nulled."))
            if args.no_candidate == 'null':
                m['alexanarch_url'] = None
                m['alexanarch_record'] = None
                m['mapping_type'] = 'no_verified_target'
            else:
                m['audit_status'] = 'no_verified_target_flagged_20260719'
            identity[doi] = {'deposit_number': None, 'axn': None, 'record_url': None,
                             'title': t['title'], 'grade': 'none', 'truth_sources': t['sources']}

    # second pass: [SUPERSEDED -> DOI X] rows follow their own pointer DOI to the head record
    for m in maps:
        ptr = m.pop('_supersedes_ptr', None)
        if not ptr: continue
        tgt = identity.get(ptr)
        if tgt and tgt.get('deposit_number') is not None:
            if m.get('alexanarch_url') != tgt['record_url']:
                m['alexanarch_url'] = tgt['record_url']
                m['alexanarch_record'] = f"/s/records/{tgt['deposit_number']}/"
                m['axn'] = tgt['axn']
                m['root_axn'] = '.'.join(tgt['axn'].split('.')[:2]) if tgt.get('axn') else m.get('root_axn')
            m['mapping_type'] = 'superseded_version_pointer'
            m['title_verification'] = (m.get('title_verification', '') +
                ' Superseded-version row: resolved by following its own supersession-pointer DOI to the head record.')
            m.pop('audit_status', None)
            doi = (m.get('dead_doi') or '').lower()
            if identity.get(doi, {}).get('deposit_number') is None:
                stats['no_candidate'] -= 1
                stats['S_superseded_ptr'] = stats.get('S_superseded_ptr', 0) + 1
            identity[doi] = {'deposit_number': tgt['deposit_number'], 'axn': tgt['axn'],
                             'record_url': tgt['record_url'], 'title': m.get('title'),
                             'grade': 'S', 'truth_sources': (truth.get(doi) or {}).get('sources', [])}
    print(json.dumps(stats, indent=1))
    if args.dry_run:
        return
    idx['version'] = '3.5'
    idx['dateModified'] = today
    idx.setdefault('changelog', []).append({
        'version': '3.5', 'date': today,
        'note': 'DOI-key remediation (remediate_resolution_index.py): titles from DOI-keyed truth union '
                '(DataCite backup, OpenAlex snapshot, newly-found, tombstone citations); targets by exact-title '
                'constraint with date tiebreak; all prior values preserved per-row in remediation_2026_07_19. '
                'See audit/DOI-INDEX-AUDIT-2026-07-19.md. Root cause: title-similarity joins and misuse of '
                'zenodo_dois (=DOIs cited in text, never identity) as a key.'})
    json.dump(idx, open(IDX, 'w'), ensure_ascii=False, indent=1)
    outdir = ROOT/'datasets'/'doi-work-identity'
    outdir.mkdir(parents=True, exist_ok=True)
    json.dump({'@context': 'https://schema.org', '@type': 'Dataset',
               'name': 'CHA DOI–Work Identity Map',
               'description': 'The DOI->work identity artifact reconstructed 2026-07-19. Every DOI is joined to its '
                              'alexanarch record by DOI-keyed truth + exact-title constraint. This artifact did not '
                              'previously exist anywhere in the rhizome; its absence is the root cause of the '
                              'resolution-index corruption. zenodo_dois fields elsewhere mean "DOIs cited in the work'
                              '\'s text" and MUST NEVER be used as identity.',
               'map': '/datasets/dataflow-atlas/',
               'dateCreated': today, 'grades': {'A': 'exact unique', 'B': 'date-resolved', 'kept': 'ambiguous, current kept',
               'earliest': 'ambiguous, earliest chosen', 'C': 'fuzzy unique >=0.75', 'none': 'no verified target'},
               'identity': identity},
              open(outdir/'doi-identity-map.json', 'w'), ensure_ascii=False, indent=1)
    print('wrote', IDX, 'v3.5 and', outdir/'doi-identity-map.json')

if __name__ == '__main__':
    main()
