#!/usr/bin/env python3
"""
validate_resolver.py — Resolver acceptance gate (P0-1).

Enforces, mechanically, that the resolver's surfaces agree and that no
operational redirect exists without a verified identifier, confirmed-enough
membership, and a single existing target. Run with --strict in CI; any gate
failure exits 1.

Checks (audit gate, achievable-now subset):
  G1  canonical index parses; zero duplicate normalized dead_doi keys
  G2  every DOI syntactically valid within supported namespace or quarantined
  G3  zero fragment candidates with live targets in operational map
  G4  zero unresolved-parent entries with live targets in operational map
  G5  zero other-author entries with live targets
  G6  canonical/API map parity: same key set; every live target equals the
      canonical-derived target (no drift, no first/last-wins divergence)
  G7  every live record target exists on disk and in the registry
  G8  AXN agreement: mapping axn equals the target deposit's registry axn
      (checked where the target is an alexanarch record and both present)
  G9  top-level totals equal derived values (no stale hand-maintained counts)
  G10 dataset-set cardinality: member_count field equals len(members)
Emits:
  data/resolver-status.json           (derived counts, hashes, gate result)
  data/resolver-audit.json            (per-check summary)
  data/resolver-audit-failures.jsonl  (one line per failure)
"""

import hashlib
import json
import os
import re
import sys
import datetime
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'data', 'doi-resolution-index.json')
APIMAP = os.path.join(ROOT, 'api', 'doi-axn-map.json')
REGISTRY = os.path.join(ROOT, 'data', 'registry.json')
SETJSON = os.path.join(ROOT, 'datasets', 'set.json')

DOI_RE = re.compile(r'^10\.5281/zenodo\.\d{6,}$')
FRAG_RE = re.compile(r'^10\.5281/zenodo\.\d{1,5}$')


def is_fragment(doi):
    return bool(FRAG_RE.match(doi or ''))


def quarantine_reason(m):
    env = m.get('envelope')
    if env is not None:
        return env.get('quarantine')
    doi = m.get('dead_doi') or ''
    if is_fragment(doi):
        return 'identifier_fragment_candidate'
    if 'unresolved' in ((m.get('note') or '')).lower():
        return 'parent_work_unresolved'
    if m.get('mapping_type') == 'misclassified_other_author':
        return 'other_author'
    if not doi.startswith('10.5281/'):
        return 'unsupported_namespace'
    return None


def main():
    strict = '--strict' in sys.argv
    failures = []

    def fail(check, detail):
        failures.append({'check': check, 'detail': detail})

    idx = json.load(open(INDEX))
    api = json.load(open(APIMAP))
    reg = json.load(open(REGISTRY))
    maps = idx['mappings']
    amap = api.get('map', {})
    reg_by_num = {d['deposit_number']: d for d in reg['deposits']}

    # G1 duplicates
    deads = [m.get('dead_doi') for m in maps if m.get('dead_doi')]
    dups = [k for k, c in Counter(deads).items() if c > 1]
    for k in dups:
        fail('G1_duplicate_doi', k)

    # G2 syntax/namespace or quarantined
    for m in maps:
        doi = m.get('dead_doi') or ''
        if not DOI_RE.match(doi) and not quarantine_reason(m):
            fail('G2_invalid_unquarantined_doi', doi)

    # G3/G4/G5 quarantine enforcement in operational map
    for m in maps:
        q = quarantine_reason(m)
        if q and amap.get(m.get('dead_doi'), [None, None])[1]:
            fail({'identifier_fragment_candidate': 'G3_fragment_live',
                  'parent_work_unresolved': 'G4_unresolved_parent_live',
                  'other_author': 'G5_other_author_live',
                  'unsupported_namespace': 'G2_namespace_live'}[q],
                 m.get('dead_doi'))

    # G6 parity: key sets and target agreement with canonical derivation
    canon_keys = set(deads)
    api_keys = set(amap.keys())
    for k in canon_keys ^ api_keys:
        fail('G6_keyset_mismatch', k)
    by_dead = {m.get('dead_doi'): m for m in maps}
    for k, v in amap.items():
        m = by_dead.get(k)
        if not m:
            continue
        if quarantine_reason(m):
            want = None
        elif m.get('alexanarch_url'):
            want = m['alexanarch_url']
        else:
            lu = m.get('live_urls') or {}
            want = lu.get('repo') or lu.get('github') or lu.get('blog') or None
        if v[1] != want:
            fail('G6_target_drift', f'{k}: api={v[1]} canonical-derived={want}')
        if v[0] != (m.get('axn') or None):
            fail('G6_axn_drift', k)

    # G7 target existence; G8 AXN agreement
    recre = re.compile(r'/s/records/(\d+)/$')
    for m in maps:
        u = m.get('alexanarch_url')
        if not u or quarantine_reason(m):
            continue
        mm = recre.search(u)
        if not mm:
            continue
        n = int(mm.group(1))
        if not os.path.isdir(os.path.join(ROOT, 's', 'records', str(n))):
            fail('G7_missing_record_dir', f'{m.get("dead_doi")} -> {n}')
        dep = reg_by_num.get(n)
        if dep is None:
            fail('G7_not_in_registry', f'{m.get("dead_doi")} -> {n}')
        elif m.get('axn') and dep.get('axn') and m['axn'] != dep['axn']:
            fail('G8_axn_mismatch',
                 f'{m.get("dead_doi")} -> #{n}: map {m["axn"][:24]} vs registry {dep["axn"][:24]}')

    # G9 derived totals
    if idx.get('total_mappings') != len(maps):
        fail('G9_stale_total_mappings',
             f'declared {idx.get("total_mappings")} actual {len(maps)}')
    if idx.get('total_unique_dois') != len(set(deads)):
        fail('G9_stale_total_unique',
             f'declared {idx.get("total_unique_dois")} actual {len(set(deads))}')
    if api.get('version') != idx.get('version'):
        fail('G9_version_drift', f'api {api.get("version")} vs canonical {idx.get("version")}')

    # G10 dataset-set cardinality
    try:
        ds = json.load(open(SETJSON))
        if 'member_count' in ds and ds['member_count'] != len(ds.get('members', [])):
            fail('G10_set_cardinality',
                 f'member_count {ds["member_count"]} vs members {len(ds.get("members", []))}')
        desc = ds.get('description', '')
        for word, num in [('six', 6), ('seven', 7), ('eight', 8), ('five', 5)]:
            if word in desc.lower() and num != len(ds.get('members', [])):
                fail('G10_textual_count_stale', f'description says "{word}", members={len(ds["members"])}')
    except FileNotFoundError:
        pass

    # G11 envelope coverage (R1): every mapping self-explains
    no_env = [m.get('dead_doi') for m in maps if 'envelope' not in m]
    for d in no_env:
        fail('G11_envelope_missing', d)

    # G12 full redirect gate (R1 doctrine): every live target passes
    # validity+membership+relationship; no gated entry with a target is null
    VOK = {'verified_tombstone', 'verified_registered', 'verified_erased_registration'}
    ROK = {'same_work_restored', 'same_work_title_matched'}
    for m in maps:
        d = m.get('dead_doi'); env = m.get('envelope') or {}
        tgt = amap.get(d, [None, None])[1]
        is_fallback = tgt is not None and 'alexanarch.org/s/records/' not in tgt
        ok = (env.get('identifier_validity') in VOK and
              env.get('archive_membership') == 'confirmed' and
              not env.get('quarantine') and
              (env.get('relationship') in ROK or
               (env.get('relationship') == 'no_successor_known' and is_fallback)))
        if tgt is not None and not ok:
            fail('G12_gate_violation_live', f"{d}: {env.get('identifier_validity')}/"
                 f"{env.get('archive_membership')}/{env.get('relationship')}/q={env.get('quarantine')}")

    # G13 /go/ static safety (R2): rejection, never coercion
    go = open(os.path.join(ROOT, 'go', 'index.html')).read()
    if re.search(r"split\('\.'\)\.pop\(\)", go):
        fail('G13_go_coercion', 'namespace-coercion normalizer present')
    if 'No redirect will be attempted' not in go:
        fail('G13_go_rejection_missing', 'strict rejection message absent')

    # G14 immutable snapshot hashes (R3)
    snap_root = os.path.join(ROOT, 'datasets', 'zenodo-datacite-batch')
    for v in sorted(os.listdir(snap_root)):
        mp = os.path.join(snap_root, v, 'manifest.json')
        if not (os.path.isdir(os.path.join(snap_root, v)) and os.path.exists(mp)):
            continue
        man = json.load(open(mp))
        for r in man.get('files', []):
            if r['name'] == 'manifest.json':
                continue
            actual = hashlib.sha256(open(os.path.join(snap_root, v, r['name']), 'rb').read()).hexdigest()
            if actual != r['sha256']:
                fail('G14_snapshot_hash', f"{v}/{r['name']}")

    # emit artifacts
    q_counts = Counter(quarantine_reason(m) for m in maps if quarantine_reason(m))
    live = sum(1 for v in amap.values() if v[1])
    status = {
        'instrument': 'resolver-status',
        'generated': datetime.date.today().isoformat(),
        'resolver_version': idx.get('version'),
        'index_version': idx.get('version'),
        'mappings_total': len(maps),
        'live_redirects': live,
        'quarantined_total': len(amap) - live,
        'mapping_rows': len(maps),
        'unique_normalized_dois': len(set(deads)),
        'duplicate_doi_keys': len(dups),
        'operational_live_targets': live,
        'operational_null_targets': len(amap) - live,
        'quarantined': dict(q_counts),
        'canonical_sha256': hashlib.sha256(open(INDEX, 'rb').read()).hexdigest(),
        'api_map_sha256': hashlib.sha256(open(APIMAP, 'rb').read()).hexdigest(),
        'gate_failures': len(failures),
        'gate': 'PASS' if not failures else 'FAIL',
    }
    json.dump(status, open(os.path.join(ROOT, 'data', 'resolver-status.json'), 'w'), indent=1)
    audit = {'generated': status['generated'],
             'checks_failed': dict(Counter(f['check'] for f in failures)),
             'gate': status['gate']}
    json.dump(audit, open(os.path.join(ROOT, 'data', 'resolver-audit.json'), 'w'), indent=1)
    with open(os.path.join(ROOT, 'data', 'resolver-audit-failures.jsonl'), 'w') as f:
        for x in failures:
            f.write(json.dumps(x) + '\n')

    print(json.dumps(status, indent=1))
    if failures:
        print(f'\nGATE FAIL — {len(failures)} failure(s):')
        for x in failures[:15]:
            print('  ', x['check'], '|', x['detail'])
        sys.exit(1 if strict else 0)
    print('\nGATE PASS')


if __name__ == '__main__':
    main()
