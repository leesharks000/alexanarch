#!/usr/bin/env python3
"""build_v2.py — Deletion Semantics Conformance Fixture v2.1 builder.

v2.1 = the chorus-review release. Structural corrections over v2.0 after
five-substrate review (2026-07-28):

  * axis_subject on every case — every axis value names its subject; no axis
    is populated from evidence belonging to another.
  * validity is never derived from identifier survival. Identifier cases carry
    `unassessed` unless independent evidence establishes a truth value.
    Supersession is an EDGES fact; withdrawal is a LIFECYCLE fact.
  * the inverse write-failure case is reclassified: `registry_update_not_landed`,
    presence UNMARKED — the presence axis is not made to carry transaction
    atomicity.
  * actor attribution split: `verified_erased_registration` (and erased-recorded
    divergence cases) carry actor `unknown`; only records directly covered by
    the documented account-level termination carry actor `host`.
  * machine-readable consumer expectations per case (`expected` block).
  * DataCite probe upgraded: GET + parse of attributes.state with UTC
    timestamp, not a bare HEAD status.
  * drift ledger derived from mapping-level diff (git 188780b4 vs current):
    old population 1,939 (v1 README said 1,938 — a hand-carried miscount,
    corrected here), current 1,937; the two removed mappings are the two
    disclosed withdrawals and both were verified_registered, which fully
    explains registered 75 -> 73. One mechanism, both numbers.

The BUILDER reads current sources and performs live probes; the FIXTURE it
emits is frozen by manifest hashes + the repository commit. Conformance
testing is offline against cases.json; live re-probing is optional
(reprobe_live.py) and emits a dated observation report, never a mutation
of expected results.
"""
import json, time, urllib.request, urllib.error, sys, collections, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FIX = Path(__file__).resolve().parent
PROBE_CACHE = Path('/tmp/fixture-v2-probes.json')
TODAY = '2026-07-28'
SCHEMA_URL = 'https://www.alexanarch.org/datasets/deletion-conformance-fixture/deletion-fixture.schema.json'

dri = json.load(open(ROOT / 'data' / 'doi-resolution-index.json'))
reg = json.load(open(ROOT / 'data' / 'registry.json'))
byn = {d['deposit_number']: d for d in reg['deposits']}
rep = json.load(open(ROOT / 'data' / 'restoration-inplace-2026-07-28.json'))
_v1p = FIX / 'cases-v1.0.json'
v1 = json.load(open(_v1p))
assert v1.get('version') == '1.0', 'builder must start from the archived v1.0 base'
M = {m['dead_doi']: m for m in dri['mappings']}

def env(m):
    e = m.get('envelope')
    return e if isinstance(e, dict) else {}

TERMINATION_CLASSES = {'removed_with_successor','removed_without_successor',
    'concept_root_severed_version_survives','version_severed_root_survives',
    'typo_immune_survivor'}
REMOVED_MARK = TERMINATION_CLASSES | {'registration_erased','registry_resolution_divergence'}

def axes_for(m, case_class):
    """Ratified axes, subject-explicit. Presence sparse; validity never derived
    from identifier survival; edges carry relations without axis leakage."""
    e = env(m)
    ax = {}
    if case_class in REMOVED_MARK:
        ax['presence'] = 'removed'
    elif case_class == 'quarantined_title_mismatch' and e.get('identifier_validity') in ('verified_tombstone', 'verified_erased_registration'):
        ax['presence'] = 'removed'   # the identifier target is gone; the quarantine concerns the successor edge, not presence
    elif case_class == 'never_landed':
        ax['presence'] = 'never_landed'
    # all other classes: no marker (sparse default)
    ax['validity'] = 'unassessed'   # no identifier case carries independent claim evidence
    edges = {}
    if m.get('alexanarch_record'):
        edges['successor'] = 'https://www.alexanarch.org' + m['alexanarch_record']
    rel = e.get('relationship')
    if rel: edges['relationship'] = rel
    if edges: ax['edges'] = edges
    return ax

def subject_for(case_class, identifier):
    kind = {'never_landed': 'registry_assertion',
            'registry_update_not_landed': 'registry_update',
            'withdrawn_removal_vs_destruction': 'content_payload',
            'superseded_present': 'concept',
            'state_drift_documented': 'archive_record'}.get(case_class, 'identifier_target')
    return {'kind': kind, 'identifier': identifier}

def reason_for(case_class, m=None):
    if case_class == 'registration_erased':
        return {'actor': 'unknown', 'reason': 'not_disclosed',
                'note': 'registration erasure is a distinct action from tombstoning; the actor at that layer cannot be established from probes — attribution withheld'}
    if case_class == 'registry_resolution_divergence' and m is not None:
        iv = env(m).get('identifier_validity')
        if iv == 'verified_erased_registration':
            return {'actor': 'unknown', 'reason': 'not_disclosed'}
        return {'actor': 'host', 'reason': 'not_disclosed',
                'note': 'directly covered by the documented 2026-06-19 account-level termination'}
    if case_class in TERMINATION_CLASSES:
        return {'actor': 'host', 'reason': 'not_disclosed',
                'note': 'account-level termination 2026-06-19; no per-record rationale was ever provided — the case the reason vocabulary exists for'}
    if case_class in ('never_landed','registry_update_not_landed'):
        return {'actor': 'producer', 'reason': 'producer_bug'}
    if case_class == 'withdrawn_removal_vs_destruction':
        return {'actor': 'producer', 'reason': 'ownership_correction',
                'note': 'external author prior claim; removal self-initiated and disclosed'}
    return None

EXPECTED = {
 'removed_with_successor': {'emit_presence':'removed','preserve_reason':True,'follow_successor':True,'retain_predecessor_identifier':True},
 'removed_without_successor': {'emit_presence':'removed','preserve_reason':True,'must_not_infer_successor':True,'retain_predecessor_identifier':True},
 'registration_erased': {'emit_presence':'removed','must_not_trust_recorded_state':True,'actor_must_remain_unknown':True},
 'not_removed_control': {'emit_presence':None,'must_not_mark_removed':True},
 'concept_root_severed_version_survives': {'emit_presence':'removed','follow_successor':True,'must_preserve_family_structure':True},
 'version_severed_root_survives': {'emit_presence':'removed','follow_successor':True,'must_preserve_family_structure':True},
 'membership_unresolved': {'emit_presence':None,'must_not_assert_successor':True},
 'other_author_collision': {'emit_presence':None,'must_refuse_successor_link':True},
 'quarantined_title_mismatch': {'emit_presence':'removed' ,'must_flag_for_inspection':True,'must_not_redirect':True},
 'registry_resolution_divergence': {'emit_presence':'removed','must_carry_both_authorities':True,'must_not_collapse_authorities':True},
 'not_an_identifier': {'must_reject_input':True},
 'typo_immune_survivor': {'must_not_trust_recorded_state':True},
 'never_landed': {'emit_presence':'never_landed','check_assertion_at_source':True},
 'registry_update_not_landed': {'emit_presence':None,'must_not_mark_never_landed':True,'must_detect_content_record_divergence':True},
 'superseded_present': {'emit_presence':None,'follow_edges_for_governance':True,'must_not_infer_invalidity_from_supersession':True},
 'withdrawn_removal_vs_destruction': {'emit_presence':'removed','preserve_removal_fact':True,'respect_destruction_path':True,'follow_external_successor':True},
 'state_drift_documented': {'must_date_cached_state':True,'must_not_cache_indefinitely':True},
}

# quarantined: recorded tombstone identifiers under title-mismatch quarantine -> presence removed is correct (identifier_target gone)
def finish(c):
    c['axis_subject'] = subject_for(c['case_class'], c['identifier'])
    c['expected'] = EXPECTED[c['case_class']]
    return c

# ── v1 preservation + re-expression ─────────────────────────────────────────
cases, used = [], set()
for c in v1['cases']:
    c2 = dict(c)
    c2['identifier_kind'] = 'doi' if c['case_class'] != 'not_an_identifier' else 'doi_shaped_string'
    m = M.get(c['identifier']) or {}
    c2['axes'] = axes_for(m, c['case_class'])
    r = reason_for(c['case_class'], m)
    if r: c2['reason'] = r
    c2['in_v1'] = True
    cases.append(finish(c2)); used.add(c['identifier'])

# ── expansion sampling (identical predicates to v2.0; deterministic) ────────
def recorded_block(m):
    e = env(m)
    return {'identifier_validity': e.get('identifier_validity'),
            'archive_membership': e.get('archive_membership'),
            'relationship': e.get('relationship'),
            'quarantine': e.get('quarantine'),
            'severance_class': m.get('severance_class'),
            'last_verified': e.get('last_verified')}

def mk(doi, case_class, extra=None):
    m = M[doi]
    c = {'case_class': case_class, 'identifier': doi, 'identifier_kind': 'doi',
         'recorded': recorded_block(m), 'work_title': str(m.get('title'))[:160],
         'axes': axes_for(m, case_class)}
    if m.get('alexanarch_record'):
        c['successor'] = 'https://www.alexanarch.org' + m['alexanarch_record']
        c['successor_kind'] = 'archive_record'
    r = reason_for(case_class, m)
    if r: c['reason'] = r
    if extra: c.update(extra)
    return finish(c)

PREDICATES = {
 'removed_with_successor': (lambda m: env(m).get('identifier_validity')=='verified_tombstone'
    and env(m).get('relationship')=='same_work_restored' and env(m).get('archive_membership')=='confirmed'
    and not env(m).get('quarantine') and m.get('alexanarch_record'), 20),
 'removed_without_successor': (lambda m: env(m).get('relationship')=='no_successor_known', 9),
 'registration_erased': (lambda m: env(m).get('identifier_validity')=='verified_erased_registration', 12),
 'not_removed_control': (lambda m: env(m).get('identifier_validity')=='verified_registered'
    and env(m).get('archive_membership')=='confirmed', 10),
 'concept_root_severed_version_survives': (lambda m: m.get('severance_class')=='concept_root'
    and env(m).get('identifier_validity')=='verified_tombstone', 8),
 'version_severed_root_survives': (lambda m: m.get('severance_class')=='version_of_mapped_root', 5),
 'membership_unresolved': (lambda m: env(m).get('archive_membership')=='unresolved', 8),
 'other_author_collision': (lambda m: env(m).get('archive_membership')=='rejected_other_author', 8),
 'quarantined_title_mismatch': (lambda m: env(m).get('quarantine')=='target_title_mismatch', 8),
 'not_an_identifier': (lambda m: env(m).get('identifier_validity')=='fragment_candidate', 3),
 'typo_immune_survivor': (lambda m: m.get('status')=='TYPO_IMMUNE_SURVIVOR', 2),
}
selection_note = {}
for cls, (pred, target) in PREDICATES.items():
    have = sum(1 for c in cases if c['case_class']==cls)
    pool = sorted(doi for doi, m in M.items() if pred(m) and doi not in used)
    take = pool[:max(0, target - have)]
    for doi in take:
        cases.append(mk(doi, cls)); used.add(doi)
    selection_note[cls] = {'target': target, 'v1': have, 'added': len(take), 'pool_size': len(pool)+have}

div_pool = sorted(doi for doi, m in M.items()
                  if m.get('datacite_state')=='findable'
                  and env(m).get('identifier_validity') in ('verified_tombstone','verified_erased_registration')
                  and doi not in used)
for doi in div_pool[:8]:
    if doi in used: continue
    cases.append(mk(doi, 'registry_resolution_divergence',
        {'divergence': {'registry_record': 'DataCite API record endpoint (metadata-record presence)',
                        'identifier_target': 'DOI resolution (target presence)',
                        'test': 'registry-record presence and target-resolution presence are subject-relative and diverged for this identifier at the dated probe; a consumer must carry both and collapse neither'}}))
    used.add(doi)
selection_note['registry_resolution_divergence'] = {'target': 8, 'added': min(8, len(div_pool)), 'pool_size': len(div_pool)}

sup = [d for d in reg['deposits'] if d.get('superseded_by')][:20]
sup_take = [d for d in sup if 1014 <= d['deposit_number'] <= 1022][:4]
sup_take += [d for d in sup if d not in sup_take][:4 - len(sup_take)]
for d in sup_take:
    dois = sorted(k for k, m in M.items() if (m.get('alexanarch_record') or '').endswith(f"/{d['deposit_number']}/"))
    cases.append(finish({'case_class': 'superseded_present', 'identifier': f"https://www.alexanarch.org/s/records/{d['deposit_number']}/",
        'identifier_kind': 'archive_record', 'work_title': str(d.get('title'))[:160],
        'recorded': {'superseded_by': f"/s/records/{d['superseded_by']}/", 'record_status': d.get('status'),
                     'canonical_text_status': d.get('canonical_text_status')},
        'axes': {'validity': 'unassessed',
                 'edges': {'superseded_by': f"https://www.alexanarch.org/s/records/{d['superseded_by']}/"}},
        'mapped_dead_dois': dois[:2],
        'test': 'a still-present record with a supersession edge: the edge changes what governs retrieval; it does not prove the predecessor false. Validity stays unassessed; presence stays unmarked; only edges speak.'}))
selection_note['superseded_present'] = {'added': len(sup_take), 'pool_size': len(sup)}

cases.append(finish({'case_class': 'never_landed', 'identifier': '/data/EA-WG-CAPTURES-01-v8.3.json',
 'identifier_kind': 'declared_path', 'work_title': 'Deposit #3 declared full_text_path (versioned filename)',
 'recorded': {'declared_in': 'data/registry.json deposit #3 full_text_path', 'declared_state': 'canonical body at this path'},
 'observed_2026_07_28': 'absent from working tree; regeneration guard raised; repaired to /data/EA-WG-CAPTURES-01.json',
 'axes': {'presence': 'never_landed', 'validity': 'unassessed'},
 'reason': {'actor': 'producer', 'reason': 'producer_bug'},
 'evidence': ['https://github.com/leesharks000/alexanarch/commit/c0b0da07 (guard catch + repair, 2026-07-28)'],
 'test': 'a registry entry asserted a body at a path where none existed; the assertion was checkable where it was made, and a check caught it — the ratified third history, dated'}))
selection_note['never_landed'] = {'added': 1}

cases.append(finish({'case_class': 'registry_update_not_landed', 'identifier': 'restoration-run-interrupt-2026-07-28',
 'identifier_kind': 'state_change_claim', 'work_title': 'Interrupted restoration pass: 15 bodies written, registry update not landed',
 'recorded': {'observed_condition': '15 canonical text files carried restoration headers while the registry still recorded metadata-only',
              'window': 'single interrupted run, 2026-07-28', 'repair': 'resume guard detected the marker and reconstructed the registry side from file state'},
 'axes': {'validity': 'unassessed',
          'note': 'presence deliberately UNMARKED: the content landed; what failed was the registry update. The presence axis is not made to carry transaction atomicity. Retained as the adjacent inverse of never_landed, outside the sparse markers by design.'},
 'reason': {'actor': 'producer', 'reason': 'producer_bug'},
 'evidence': ['data/restoration-inplace-2026-07-28.json (repaired_from_interrupt markers)'],
 'test': 'content-record divergence in the inverse direction: body present, registry assertion absent. A consumer must detect the divergence without emitting never_landed, which names the other direction only.'}))
selection_note['registry_update_not_landed'] = {'added': 1}

for n, ext in ((1382, '10.5281/zenodo.19825269'), (1383, '10.5281/zenodo.20100880')):
    d = byn[n]
    cases.append(finish({'case_class': 'withdrawn_removal_vs_destruction',
     'identifier': f"https://www.alexanarch.org/s/records/{n}/", 'identifier_kind': 'archive_record',
     'work_title': str(d.get('title'))[:160],
     'recorded': {'canonical_text_status': d.get('canonical_text_status'), 'record_state': 'withdrawn 2026-07-28'},
     'axes': {'presence': 'removed', 'validity': 'unassessed',
              'edges': {'authoritative_external': f'https://doi.org/{ext}'},
              'note': 'presence: removed applies to the CONTENT PAYLOAD (axis_subject). The tombstone record at this URL resolves 200 by design — the removal-fact is permanent and public while the content travelled the separate destruction path.'},
     'lifecycle': 'withdrawn',
     'reason': {'actor': 'producer', 'reason': 'ownership_correction',
                'note': 'external author prior claim on the captured work'},
     'removal_fact_retained': True, 'content_destroyed': True,
     'test': 'the ratified split embodied: removal-fact permanent (tombstone resolves and says why); content destroyed on a separate, disclosed path; the successor edge points outside the archive to the owner\u2019s live identifier'}))
selection_note['withdrawn_removal_vs_destruction'] = {'added': 2}

drift = [r for r in rep['restored'] if not r.get('repaired_from_interrupt')][:4]
for r in drift:
    d = byn[r['n']]
    cases.append(finish({'case_class': 'state_drift_documented',
     'identifier': f"https://www.alexanarch.org/s/records/{r['n']}/", 'identifier_kind': 'archive_record',
     'work_title': str(d.get('title'))[:160],
     'recorded': {'state_at_v1_build': 'metadata_only', 'state_now': d.get('canonical_text_status'),
                  'changed_at': TODAY, 'mechanism': 'in-place restoration under body-head gate',
                  'axn_before': (d.get('restoration') or {}).get('axn_before_restoration'), 'axn_now': d.get('axn')},
     'axes': {'validity': 'unassessed',
              'note': 'presence never changed; the record\u2019s completeness class and content-derived identifier did — a consumer caching either will be wrong within the day'},
     'evidence': ['data/restoration-inplace-2026-07-28.json'],
     'test': 'state is not static: same identifier, two honest recorded states hours apart, both dated'}))
selection_note['state_drift_documented'] = {'added': len(drift)}

# ── probes ──────────────────────────────────────────────────────────────────
cache = json.load(open(PROBE_CACHE)) if PROBE_CACHE.exists() else {}
def save_cache():
    json.dump(cache, open(PROBE_CACHE, 'w'))
def probe_head(url, tries=3):
    if url in cache: return cache[url]
    code = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'alexanarch-fixture/2.1'}, method='HEAD')
            r = urllib.request.urlopen(req, timeout=20)
            code = str(r.status); break
        except urllib.error.HTTPError as e:
            code = str(e.code)
            if code != '503': break
            time.sleep(2.5)
        except Exception:
            code = None
    cache[url] = code; save_cache(); time.sleep(0.4)
    return code
def probe_datacite_get(doi):
    key = 'dcget:' + doi
    if key in cache: return cache[key]
    out = {'http': None, 'state': None, 'retrieved_utc': None}
    try:
        req = urllib.request.Request(f'https://api.datacite.org/dois/{doi}',
                                     headers={'User-Agent': 'alexanarch-fixture/2.1', 'Accept': 'application/vnd.api+json'})
        r = urllib.request.urlopen(req, timeout=25)
        body = json.loads(r.read().decode('utf-8', 'replace'))
        out = {'http': str(r.status),
               'state': ((body.get('data') or {}).get('attributes') or {}).get('state'),
               'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    except urllib.error.HTTPError as e:
        out = {'http': str(e.code), 'state': None,
               'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    except Exception:
        pass
    cache[key] = out; save_cache(); time.sleep(0.6)
    return out

if '--no-probe' not in sys.argv:
    n_p = 0
    for c in cases:
        if c['identifier_kind'] in ('doi', 'doi_shaped_string'):
            c['observed_2026_07_28_v2'] = probe_head(f"https://doi.org/{c['identifier']}")
            n_p += 1
        elif c['identifier_kind'] == 'archive_record':
            c['observed_2026_07_28_v2'] = probe_head(c['identifier'])
            n_p += 1
        if c['case_class'] == 'registry_resolution_divergence':
            c['datacite_api_2026_07_28'] = probe_datacite_get(c['identifier'])
    print(f"probes complete: {n_p} identifiers + {len(div_pool[:8])} DataCite GET")

counts = collections.Counter(c['case_class'] for c in cases)
host_nd = sum(1 for c in cases if (c.get('reason') or {}).get('actor')=='host' and (c.get('reason') or {}).get('reason')=='not_disclosed')
unk = sum(1 for c in cases if (c.get('reason') or {}).get('actor')=='unknown')
out = {
 '$schema': SCHEMA_URL,
 'name': 'Deletion Semantics Conformance Fixture',
 'version': '2.1', 'date': TODAY, 'license': 'CC0-1.0 (dataset) / MIT (scripts)',
 'ratified_axes': 'validity / presence / edges per knowledge-catalog#207 (2026-07-27); presence sparse: removed | never_landed | no marker; every axis value names its subject (axis_subject); no axis populated from evidence belonging to another',
 'derived_from': 'Zenodo DOI Resolution Index (current, 1,937 mappings; envelope layer as recorded state) + Alexanarch registry + dated repair artifacts',
 'event': v1.get('event'),
 'population_note': 'The source index holds 1,937 identifiers. Recorded validity distribution at build: tombstone 1,815 · registered 73 · erased 32 · unverified 13 · fragment 3. Not 1,937 deletions; the classes say which is which.',
 'v1_drift_ledger': ('Derived from the mapping-level diff (repository commits 188780b4 -> current): old population 1,939 '
   '(v1.0 README stated 1,938 — a hand-carried miscount, corrected here by derivation), current 1,937. Exactly two mappings removed, '
   'both by disclosed producer withdrawal (records 1382, 1383), and both were verified_registered — one mechanism fully explains '
   'population 1,939->1,937 and registered 75->73. Zero identifier_validity changes among common mappings. Observation drift on the v1 base: zero.'),
 'reason_attribution_note': f'{host_nd} cases carry actor host + reason not_disclosed (directly covered by the documented account-level termination); {unk} carry actor unknown (registration-erasure layer: mechanism unattributable from probes).',
 'selection': selection_note,
 'total_cases': len(cases),
 'classes': dict(sorted(counts.items())),
 'cases': cases,
}
(FIX / 'cases.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f"v2.1: {len(cases)} cases | classes: {len(counts)} | host/not_disclosed: {host_nd} | actor unknown: {unk}")
