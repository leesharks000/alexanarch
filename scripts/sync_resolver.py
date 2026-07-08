#!/usr/bin/env python3
"""sync_resolver.py — canonical DOI Resolution Index integrity enforcement.

The canonical file is data/doi-resolution-index.json. This script is the ONLY
sanctioned path between the canonical index and its derived surfaces. Run it
after ANY edit to the canonical index. It:

  1. Enforces pointer invariants on every mapping:
       - alexanarch_url is the authoritative target (absolute URL or null).
       - alexanarch_record is a derived mirror: the root-relative form of
         alexanarch_url (/s/records/N/), or null when url is null.
       - The legacy /s/records/0/ zero-sentinel (in either field, relative or
         absolute) is normalized to null. Nulls encode "no target"; the
         classification lives in mapping_type, never in a fake pointer.
       - mapping_type in NO_TARGET_TYPES must have null pointers.
  2. Validates every non-null target: s/records/N/ exists on disk AND deposit
     N exists in data/registry.json. Violations fail the run (exit 1).
  3. Regenerates api/doi-axn-map.json from alexanarch_url, with the v3.8
     fallback semantics made durable: for no_alexanarch_equivalent entries the
     map value falls back to live_urls.repo/github > live_urls.blog, so
     rewriting consumers get a working URL even without an alexanarch record.
     misclassified_other_author entries get null — never map another author's
     DOI to a Lee Sharks record. Map value: [axn, url-or-null].
  4. Prints a stats block for resolve-page / deposit-page propagation.

Usage:
  python3 scripts/sync_resolver.py --check    # validate only, no writes
  python3 scripts/sync_resolver.py --apply    # normalize fields + regen api map

Protocol (deposit #912 rule 18, amended): alexanarch_record and alexanarch_url
are no longer edited in lockstep by hand — edit alexanarch_url only, then run
this script; alexanarch_record is derived. Read the FULL output; the final
"SYNC OK" line must be seen, not assumed.
"""
import json, os, re, sys, hashlib
from collections import Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'data', 'doi-resolution-index.json')
APIMAP = os.path.join(ROOT, 'api', 'doi-axn-map.json')
REGISTRY = os.path.join(ROOT, 'data', 'registry.json')

BASE = 'https://alexanarch.org'
NO_TARGET_TYPES = {'no_alexanarch_equivalent', 'misclassified_other_author'}

def recnum(u):
    """Extract record number from any pointer form; 0-sentinel and null → None."""
    if not u:
        return None
    m = re.search(r'/s/records/(\d+)/?$', str(u))
    if not m:
        return 'BADFMT'
    n = int(m.group(1))
    return None if n == 0 else n

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else '--check'
    if mode not in ('--check', '--apply'):
        print(__doc__); sys.exit(2)

    idx = json.load(open(INDEX))
    reg = json.load(open(REGISTRY))
    reg_nums = {d['deposit_number'] for d in reg['deposits']}
    maps = idx['mappings']

    fixes = Counter()
    errors = []
    for m in maps:
        doi = m.get('dead_doi', '?')
        u_n = recnum(m.get('alexanarch_url'))
        r_n = recnum(m.get('alexanarch_record'))
        if u_n == 'BADFMT':
            errors.append(f'BADFMT alexanarch_url {doi}: {m.get("alexanarch_url")!r}'); continue
        if r_n == 'BADFMT':
            fixes['record_badfmt_rederived'] += 1
            r_n = None  # will be re-derived below

        # No-target classifications must not point anywhere.
        if m.get('mapping_type') in NO_TARGET_TYPES:
            if m.get('alexanarch_url') is not None or m.get('alexanarch_record') is not None:
                fixes['no_target_type_pointers_nulled'] += 1
            m['alexanarch_url'] = None
            m['alexanarch_record'] = None
            continue

        # url authoritative; normalize sentinels to null.
        if u_n is None:
            if m.get('alexanarch_url') is not None:
                fixes['url_sentinel_nulled'] += 1
                m['alexanarch_url'] = None
            if m.get('alexanarch_record') is not None:
                fixes['record_nulled_with_url'] += 1
                m['alexanarch_record'] = None
            continue

        canonical_url = f'{BASE}/s/records/{u_n}/'
        canonical_rec = f'/s/records/{u_n}/'
        if m.get('alexanarch_url') != canonical_url:
            fixes['url_normalized'] += 1
            m['alexanarch_url'] = canonical_url
        if m.get('alexanarch_record') != canonical_rec:
            if r_n is not None and r_n != u_n:
                fixes['record_stale_repointed'] += 1
            else:
                fixes['record_form_normalized'] += 1
            m['alexanarch_record'] = canonical_rec

        # Target must exist.
        if not os.path.isdir(os.path.join(ROOT, 's', 'records', str(u_n))):
            errors.append(f'MISSING record dir {doi} -> s/records/{u_n}/')
        if u_n not in reg_nums:
            errors.append(f'NOT IN REGISTRY {doi} -> deposit {u_n}')

    # Stats
    n_target = sum(1 for m in maps if m.get('alexanarch_url'))
    n_axn = sum(1 for m in maps if m.get('axn'))
    types = Counter(m.get('mapping_type') or '(none)' for m in maps)
    print(f'mappings: {len(maps)} | with target: {n_target} '
          f'({100*n_target/len(maps):.0f}%) | with AXN: {n_axn} | no target: {len(maps)-n_target}')
    print('mapping_type:', dict(types.most_common()))
    if fixes:
        print('fixes:', dict(fixes))
    if errors:
        print(f'\n{len(errors)} ERRORS:')
        for e in errors[:20]:
            print('  ', e)
        print('SYNC FAILED — canonical index has invalid targets; nothing written.')
        sys.exit(1)

    def map_url(m):
        """Resolution target for the api map, with v3.8 fallback semantics."""
        if m.get('alexanarch_url'):
            return m['alexanarch_url']
        if m.get('mapping_type') == 'misclassified_other_author':
            return None  # other author's work — never map to a Lee Sharks record
        lu = m.get('live_urls') or {}
        return lu.get('repo') or lu.get('github') or lu.get('blog') or None

    if mode == '--check':
        dirty = sum(fixes.values())
        print('CHECK ONLY — no writes.' + (f' ({dirty} normalizations pending; run --apply)' if dirty else ' Index is normalized.'))
        # Also verify api map freshness against what --apply would produce
        want = {m['dead_doi']: [m.get('axn') or None, map_url(m)] for m in maps}
        try:
            have = json.load(open(APIMAP)).get('map', {})
            stale = sum(1 for k, v in want.items() if have.get(k) != v)
            print(f'api map drift vs canonical: {stale} entries differ' + ('' if stale == 0 else ' — run --apply'))
        except FileNotFoundError:
            print('api map missing — run --apply')
        sys.exit(0)

    # --apply: write canonical (compact per house rule) + regen api map
    idx['dateModified'] = date.today().isoformat()
    with open(INDEX, 'w') as f:
        json.dump(idx, f, ensure_ascii=False, indent=None, separators=(',', ':'))
    api = {
        'name': 'Alexanarch DOI→AXN map (derived)',
        'description': 'Derived from data/doi-resolution-index.json (canonical) by scripts/sync_resolver.py. '
                       'Value: [sovereign AXN or null, resolution URL or null]. URL is the alexanarch record '
                       'when one exists; for no_alexanarch_equivalent DOIs it falls back to the live repo or '
                       'blog source; null = no known live target (see mapping_type in canonical index).',
        'version': idx.get('version'),
        'dateModified': idx['dateModified'],
        'map': {m['dead_doi']: [m.get('axn') or None, map_url(m)] for m in maps},
    }
    with open(APIMAP, 'w') as f:
        json.dump(api, f, ensure_ascii=False, indent=None, separators=(',', ':'))
    h = hashlib.sha256(open(INDEX, 'rb').read()).hexdigest()
    print(f'wrote {os.path.relpath(INDEX, ROOT)} (sha256 {h[:16]}…) and {os.path.relpath(APIMAP, ROOT)}')
    print('SYNC OK')

if __name__ == '__main__':
    main()
