#!/usr/bin/env python3
"""
enrich_resolver_evidence.py — R1 truth layer (resolver hardening, EA-DISTRO-01 freeze).

Adds a per-entry evidence envelope to every mapping in the canonical
DOI Resolution Index, so the index explains itself: identifier validity,
archive membership, explicit relationship, evidence list, quarantine reason.

Evidence sources (all in-repo, all public):
  - datasets/negshape-deletion-bibliography/deletion-bibliography.json
      (membership audit: ORCID / affiliation / registered-creator census /
       sovereign-registry chain — Appendix B of EA-NEGSHAPE-01, #1075)
  - datasets/tombstone-mirror/tombstone-api.jsonl
      (authority's own HTTP 410 tombstones w/ citation_text: verified_tombstone)
  - data/datacite-full-backup.json (extant DataCite metadata: verified_registered)
  - data/registry.json (target existence, AXN, title agreement)

Idempotent: recomputes envelopes from sources on every run.
Never removes fields; bumps index version minor.
"""

import json
import os
import re
import sys
import datetime
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda p: json.load(open(os.path.join(ROOT, p)))

TODAY = datetime.date.today().isoformat()

idx = J('data/doi-resolution-index.json')
reg = J('data/registry.json')
nb = J('datasets/negshape-deletion-bibliography/deletion-bibliography.json')
backup = J('data/datacite-full-backup.json')

membership = {e['doi']: (e['membership_review_status'], e['membership_basis'])
              for e in nb['entries']}
registered = {r['attributes']['doi'] for r in backup['records']
              if r.get('attributes', {}).get('doi')}
erased = set(backup.get('not_found_dois', []))

tombstones = {}
ts_path = os.path.join(ROOT, 'datasets/tombstone-mirror/tombstone-api.jsonl')
with open(ts_path) as f:
    for line in f:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get('http_status') == 410 and r.get('record_id'):
            tombstones[f"10.5281/zenodo.{r['record_id']}"] = {
                'fetched': r.get('fetched'),
                'citation_text': (r.get('api', {}).get('tombstone', {})
                                   .get('citation_text', ''))[:200],
            }

rec_by_no = {d['deposit_number']: d for d in reg['deposits']}


def is_fragment(doi):
    if not doi or not doi.startswith('10.5281/zenodo.'):
        return False
    tail = doi.rsplit('.', 1)[-1]
    return tail.isdigit() and len(tail) < 6


def validity(doi):
    ev = []
    if not doi.startswith('10.5281/'):
        return 'unsupported_namespace', ev
    if is_fragment(doi):
        return 'fragment_candidate', ev
    if doi in tombstones:
        ev.append({'type': 'authority_tombstone_410',
                   'source': '/datasets/tombstone-mirror/tombstone-api.jsonl',
                   'observed_at': tombstones[doi]['fetched']})
        return 'verified_tombstone', ev
    if doi in registered:
        ev.append({'type': 'datacite_metadata_extant',
                   'source': '/data/datacite-full-backup.json'})
        return 'verified_registered', ev
    if doi in erased:
        ev.append({'type': 'datacite_404_in_tracked_set',
                   'source': '/data/datacite-full-backup.json (not_found_dois)'})
        return 'verified_erased_registration', ev
    return 'syntactically_valid_unverified', ev


REL_BY_TYPE = {
    'direct_verified': 'same_work_restored',
    'direct': 'same_work_restored',
    'title_match_repoint': 'same_work_title_matched',
    'registry_referenced': 'referenced_in_registry_document',
    'phase4_mint': 'same_work_restored',
    'misclassified_other_author': 'none_other_author',
    'no_alexanarch_equivalent': 'no_successor_known',
}


def relationship(m, mem_status):
    if mem_status in ('rejected_collision',):
        return 'none_other_author'
    mt = m.get('mapping_type') or ''
    if 'unresolved' in ((m.get('note') or '')).lower():
        return 'referenced_in_registry_document'
    if mt.startswith('provisional_'):
        return 'related_work_provisional'
    return REL_BY_TYPE.get(mt, 'unclassified')


def quarantine(m, val, mem_status, rel):
    doi = m.get('dead_doi') or ''
    if val == 'unsupported_namespace':
        return 'unsupported_namespace'
    if val == 'fragment_candidate':
        return 'identifier_fragment_candidate'
    if mem_status == 'rejected_collision':
        return 'membership_rejected_collision'
    if mem_status == 'other_author' or rel == 'none_other_author':
        return 'other_author'
    if rel == 'referenced_in_registry_document':
        return 'parent_work_unresolved'
    if mem_status not in ('confirmed',):
        return 'membership_not_confirmed'
    if rel == 'related_work_provisional':
        return 'relationship_provisional'
    return None


maps = idx['mappings']
env_stats = {'validity': Counter(), 'membership': Counter(),
             'relationship': Counter(), 'quarantine': Counter()}
title_checked = 0

for m in maps:
    doi = m.get('dead_doi') or ''
    val, ev = validity(doi)
    mem_status, mem_basis = membership.get(doi, (None, None))
    if mem_status is None:
        # not in the deletion enumeration: classify conservatively by type
        mt = m.get('mapping_type') or ''
        if mt in ('direct_verified', 'phase4_mint'):
            mem_status, mem_basis = 'probable', 'resolver_mapping_only'
        else:
            mem_status, mem_basis = 'unresolved', 'not_in_membership_audit'
    else:
        ev.append({'type': f'membership_audit:{mem_basis}',
                   'source': ('/datasets/negshape-deletion-bibliography/'
                              'deletion-bibliography.json')})

    rel = relationship(m, mem_status)

    # target cross-checks against registry
    mm = re.match(r'/s/records/(\d+)/', m.get('alexanarch_record') or '')
    if mm:
        dep = rec_by_no.get(int(mm.group(1)))
        if dep:
            ev.append({'type': 'target_record_exists',
                       'source': '/data/registry.json',
                       'locator': f"deposit {dep['deposit_number']}"})
            if m.get('axn') and dep.get('axn') and m['axn'] == dep['axn']:
                ev.append({'type': 'axn_agreement', 'source': '/data/registry.json'})
            ttl = (m.get('title') or '').strip().lower()
            if ttl and ttl[:60] == (dep.get('title') or '').strip().lower()[:60]:
                ev.append({'type': 'title_prefix_agreement',
                           'source': '/data/registry.json'})
                title_checked += 1
    if doi in tombstones and tombstones[doi]['citation_text']:
        ev.append({'type': 'authority_citation_text',
                   'source': '/datasets/tombstone-mirror/tombstone-api.jsonl'})

    q = quarantine(m, val, mem_status, rel)

    m['envelope'] = {
        'identifier_validity': val,
        'archive_membership': mem_status,
        'membership_basis': mem_basis,
        'relationship': rel,
        'quarantine': q,
        'evidence': ev,
        'last_verified': TODAY,
    }
    env_stats['validity'][val] += 1
    env_stats['membership'][mem_status] += 1
    env_stats['relationship'][rel] += 1
    if q:
        env_stats['quarantine'][q] += 1

idx['version'] = 'v3.12.0'
idx['envelope_generated'] = TODAY
idx['envelope_stats'] = {k: dict(v) for k, v in env_stats.items()}
idx['envelope_doctrine'] = (
    'Per-entry evidence envelope (R1 truth layer). An operational redirect '
    'requires: identifier_validity in {verified_tombstone, verified_registered, '
    'verified_erased_registration}, archive_membership = confirmed, '
    'relationship in {same_work_restored, same_work_title_matched}, '
    'quarantine = null. All other entries resolve to inspection, not redirect.')

with open(os.path.join(ROOT, 'data/doi-resolution-index.json'), 'w') as f:
    json.dump(idx, f, ensure_ascii=False, indent=None, separators=(',', ':'))

print(json.dumps({
    'entries': len(maps),
    'envelope_coverage': f"{len(maps)}/{len(maps)}",
    'title_agreements': title_checked,
    **{k: dict(v) for k, v in env_stats.items()},
}, indent=1))
