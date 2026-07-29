#!/usr/bin/env python3
"""build_v2.py — Deletion Semantics Conformance Fixture v2.0 builder.

v2.0 = the ratified-axes release, built after the #207 thread settled its
design (2026-07-27): three orthogonal axes (validity / presence / edges),
a SPARSE presence axis with exactly two named states (`removed`,
`never_landed`) and no marker for the default, a `reason` object in which
`unknown` and `not_disclosed` are first-class, and the removal-fact /
content-destruction split.

What this builder does, deterministically and from current sources only:
  1. Preserves the 47 v1.0 cases (archived to cases-v1.0.json), re-expressing
     each in the ratified axes.
  2. Expands every class whose source pool supports it, by recorded-layer
     predicate (the predicate is the selection criterion and is emitted into
     the meta), deterministic order, v1 identifiers excluded.
  3. Adds five new classes: never_landed, withdrawn_removal_vs_destruction,
     registry_resolution_divergence, superseded_present,
     state_drift_documented — every case from the archive's own dated,
     commit-hashed paper trail.
  4. Probes every DOI-kind case identifier live (terminal HTTP after
     redirects, retry past 503) and the DataCite API for the divergence
     class; probe cache at /tmp/fixture-v2-probes.json makes reruns cheap.
  5. Emits cases.json (v2.0), leaving README regeneration to render_readme_v2.py.

Sources (all in-repo, current):
  data/doi-resolution-index.json           — per-mapping envelope: the recorded layer
  data/registry.json                       — records, supersedes edges, canonical_text_status
  data/restoration-inplace-2026-07-28.json — today's state-drift population
  datasets/deletion-conformance-fixture/cases.json (v1.0) — preserved base
"""
import json, time, urllib.request, urllib.error, ssl, sys, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FIX = ROOT / 'datasets' / 'deletion-conformance-fixture'
PROBE_CACHE = Path('/tmp/fixture-v2-probes.json')
TODAY = '2026-07-28'

dri = json.load(open(ROOT / 'data' / 'doi-resolution-index.json'))
reg = json.load(open(ROOT / 'data' / 'registry.json'))
byn = {d['deposit_number']: d for d in reg['deposits']}
rep = json.load(open(ROOT / 'data' / 'restoration-inplace-2026-07-28.json'))
_v1p = FIX / 'cases-v1.0.json'
v1 = json.load(open(_v1p if _v1p.exists() else FIX / 'cases.json'))
assert v1.get('version') == '1.0', 'builder must start from the archived v1.0 base'
M = {m['dead_doi']: m for m in dri['mappings']}

def env(m):
    e = m.get('envelope')
    return e if isinstance(e, dict) else {}

# ── axes expression ─────────────────────────────────────────────────────────
def axes_for(m, case_class):
    """Express a mapping's state in the ratified three-axis vocabulary.
    Presence is SPARSE: emitted only for the named exception states."""
    e = env(m)
    ax = {}
    iv = e.get('identifier_validity')
    # presence (sparse)
    if case_class in ('removed_with_successor','removed_without_successor',
                      'registration_erased','concept_root_severed_version_survives',
                      'version_severed_root_survives','typo_immune_survivor',
                      'registry_resolution_divergence'):
        ax['presence'] = 'removed'
    elif case_class == 'never_landed':
        ax['presence'] = 'never_landed'
    # controls / unresolved / collisions: NO presence marker — absence of a
    # marker means what the spec's default means (not yet written / present).
    # validity axis (does the claim/work hold) — distinct from presence
    if case_class == 'withdrawn_removal_vs_destruction':
        ax['validity'] = 'withdrawn_by_producer'
    elif case_class == 'superseded_present':
        ax['validity'] = 'superseded'
    elif case_class in ('other_author_collision','membership_unresolved','not_an_identifier'):
        ax['validity'] = 'unassessed'
    else:
        ax['validity'] = 'holds'   # the work remains real; only its identifier was severed
    # edges axis
    edges = {}
    if m.get('alexanarch_record'):
        edges['successor'] = 'https://www.alexanarch.org' + m['alexanarch_record'] if m['alexanarch_record'].startswith('/') else m['alexanarch_record']
    rel = e.get('relationship') or m.get('relationship')
    if rel: edges['relationship'] = rel
    if edges: ax['edges'] = edges
    return ax

def reason_for(case_class):
    if case_class in ('removed_with_successor','removed_without_successor',
                      'registration_erased','concept_root_severed_version_survives',
                      'version_severed_root_survives','registry_resolution_divergence',
                      'typo_immune_survivor'):
        return {'actor': 'host', 'reason': 'not_disclosed',
                'note': 'account-level termination 2026-06-19; no per-record rationale was ever provided — the case the reason vocabulary exists for'}
    if case_class == 'never_landed':
        return {'actor': 'producer', 'reason': 'producer_bug'}
    if case_class == 'withdrawn_removal_vs_destruction':
        return {'actor': 'producer', 'reason': 'ownership_correction',
                'note': 'external author prior claim; removal self-initiated and disclosed'}
    return None

# ── v1 preservation + re-expression ─────────────────────────────────────────
cases, used = [], set()
for c in v1['cases']:
    c2 = dict(c)
    c2['identifier_kind'] = 'doi' if c['case_class'] != 'not_an_identifier' else 'doi_shaped_string'
    m = M.get(c['identifier'])
    c2['axes'] = axes_for(m or {}, c['case_class'])
    r = reason_for(c['case_class'])
    if r: c2['reason'] = r
    c2['in_v1'] = True
    cases.append(c2); used.add(c['identifier'])

# ── expansion sampling ──────────────────────────────────────────────────────
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
    r = reason_for(case_class)
    if r: c['reason'] = r
    if extra: c.update(extra)
    return c

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

# ── new classes ─────────────────────────────────────────────────────────────
# registry/resolution divergence: DataCite says findable, resolution recorded dead
div_pool = sorted(doi for doi, m in M.items()
                  if m.get('datacite_state')=='findable'
                  and env(m).get('identifier_validity') in ('verified_tombstone','verified_erased_registration')
                  and doi not in used)
for doi in div_pool[:8]:
    if doi in used: continue
    cases.append(mk(doi, 'registry_resolution_divergence',
        {'divergence': {'registry_says': 'findable (DataCite state at last batch)',
                        'resolution_recorded': env(M[doi]).get('identifier_validity'),
                        'test': 'two authorities disagree about one identifier; a consumer must not collapse them'}}))
    used.add(doi)
selection_note['registry_resolution_divergence'] = {'target': 8, 'added': min(8, len(div_pool)), 'pool_size': len(div_pool)}

# superseded_present: present records governed by supersedes edges (edges axis; presence untouched)
sup = [d for d in reg['deposits'] if d.get('superseded_by')][:20]
sup_take = [d for d in sup if 1014 <= d['deposit_number'] <= 1022][:4]
sup_take += [d for d in sup if d not in sup_take][:4 - len(sup_take)]
for d in sup_take:
    dois = sorted(k for k, m in M.items() if (m.get('alexanarch_record') or '').endswith(f"/{d['deposit_number']}/"))
    cases.append({'case_class': 'superseded_present', 'identifier': f"https://www.alexanarch.org/s/records/{d['deposit_number']}/",
        'identifier_kind': 'archive_record', 'work_title': str(d.get('title'))[:160],
        'recorded': {'superseded_by': f"/s/records/{d['superseded_by']}/", 'record_status': d.get('status'),
                     'canonical_text_status': d.get('canonical_text_status')},
        'axes': {'validity': 'superseded',
                 'edges': {'supersedes_successor': f"https://www.alexanarch.org/s/records/{d['superseded_by']}/"}},
        'mapped_dead_dois': dois[:2],
        'test': 'a still-present record whose edges redirect governance: validity superseded, presence unmarked — the false-but-present quadrant'})
selection_note['superseded_present'] = {'added': len(sup_take), 'pool_size': len(sup)}

# never_landed: dated assertions of states that had not landed — commit-hashed
cases.append({'case_class': 'never_landed', 'identifier': '/data/EA-WG-CAPTURES-01-v8.3.json',
 'identifier_kind': 'declared_path', 'work_title': 'Deposit #3 declared full_text_path (versioned filename)',
 'recorded': {'declared_in': 'data/registry.json deposit #3 full_text_path', 'declared_state': 'canonical body at this path'},
 'observed_2026_07_28': 'absent from working tree; regeneration guard raised; repaired to /data/EA-WG-CAPTURES-01.json',
 'axes': {'presence': 'never_landed', 'validity': 'holds'},
 'reason': {'actor': 'producer', 'reason': 'producer_bug'},
 'evidence': ['https://github.com/leesharks000/alexanarch/commit/c0b0da07 (guard catch + repair, 2026-07-28)'],
 'test': 'a registry entry asserted a body at a path where none existed; the assertion was checkable and a check caught it — inkxel\u2019s third history, ours dated'})
cases.append({'case_class': 'never_landed', 'identifier': 'restoration-run-interrupt-2026-07-28',
 'identifier_kind': 'state_change_claim', 'work_title': 'Interrupted restoration pass: 15 bodies written, registry unwritten',
 'recorded': {'declared_state': 'restored bodies seated with registry updates', 'window': 'single interrupted run, 2026-07-28'},
 'observed_2026_07_28': '15 canonical text files carried restoration headers while the registry still recorded metadata-only; a resume guard detected the marker and reconstructed the registry side from file state',
 'axes': {'presence': 'never_landed', 'validity': 'holds',
          'note': 'the inverse face: content landed, record did not — the write-claim and the write separated in the other order'},
 'reason': {'actor': 'producer', 'reason': 'producer_bug'},
 'evidence': ['data/restoration-inplace-2026-07-28.json (repaired_from_interrupt markers)'],
 'test': 'existence claims should be checked where asserted; this case is the assertion-side gap running the other direction'})
selection_note['never_landed'] = {'added': 2}

# withdrawn: removal-fact retained, content destroyed, reason disclosed
for n, ext in ((1382, '10.5281/zenodo.19825269'), (1383, '10.5281/zenodo.20100880')):
    d = byn[n]
    cases.append({'case_class': 'withdrawn_removal_vs_destruction',
     'identifier': f"https://www.alexanarch.org/s/records/{n}/", 'identifier_kind': 'archive_record',
     'work_title': str(d.get('title'))[:160],
     'recorded': {'canonical_text_status': d.get('canonical_text_status'), 'record_state': 'withdrawn 2026-07-28'},
     'axes': {'presence': 'removed', 'validity': 'withdrawn_by_producer',
              'edges': {'authoritative_external': f'https://doi.org/{ext}'}},
     'reason': {'actor': 'producer', 'reason': 'ownership_correction',
                'note': 'external author prior claim on the captured work'},
     'removal_fact_retained': True, 'content_destroyed': True,
     'test': 'the ratified split embodied: the fact of removal is permanent (tombstone resolves and says why); the content itself was destroyed on a separate, disclosed path; the successor edge points outside the archive to the owner\u2019s live identifier'})
selection_note['withdrawn_removal_vs_destruction'] = {'added': 2}

# state_drift_documented: today's restorations — recorded-then vs recorded-now
drift = [r for r in rep['restored'] if not r.get('repaired_from_interrupt')][:4]
for r in drift:
    d = byn[r['n']]
    cases.append({'case_class': 'state_drift_documented',
     'identifier': f"https://www.alexanarch.org/s/records/{r['n']}/", 'identifier_kind': 'archive_record',
     'work_title': str(d.get('title'))[:160],
     'recorded': {'state_at_v1_build': 'metadata_only', 'state_now': d.get('canonical_text_status'),
                  'changed_at': TODAY, 'mechanism': 'in-place restoration under body-head gate',
                  'axn_before': (d.get('restoration') or {}).get('axn_before_restoration'), 'axn_now': d.get('axn')},
     'axes': {'validity': 'holds',
              'note': 'presence never changed; the record\u2019s completeness class and content-derived identifier did — a consumer caching either will be wrong within the day'},
     'evidence': ['data/restoration-inplace-2026-07-28.json'],
     'test': 'state is not static: same identifier, two honest recorded states hours apart, both dated'})
selection_note['state_drift_documented'] = {'added': len(drift)}

# ── probes ──────────────────────────────────────────────────────────────────
cache = json.load(open(PROBE_CACHE)) if PROBE_CACHE.exists() else {}
def probe(url, tries=3):
    if url in cache: return cache[url]
    code = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'alexanarch-fixture/2.0'}, method='HEAD')
            r = urllib.request.urlopen(req, timeout=20)
            code = str(r.status); break
        except urllib.error.HTTPError as e:
            code = str(e.code)
            if code != '503': break
            time.sleep(2.5)
        except Exception:
            code = None
    cache[url] = code
    json.dump(cache, open(PROBE_CACHE, 'w'))
    time.sleep(0.4)
    return code

if '--no-probe' not in sys.argv:
    n_p = 0
    for c in cases:
        if c['identifier_kind'] == 'doi' or c['identifier_kind'] == 'doi_shaped_string':
            c['observed_2026_07_28_v2'] = probe(f"https://doi.org/{c['identifier']}")
            n_p += 1
        elif c['identifier_kind'] == 'archive_record':
            c['observed_2026_07_28_v2'] = probe(c['identifier'])
            n_p += 1
        if c['case_class'] == 'registry_resolution_divergence':
            dc = probe(f"https://api.datacite.org/dois/{c['identifier']}")
            c['datacite_api_2026_07_28'] = dc
        if n_p % 25 == 0: print(f"  probed {n_p}…")
    print(f"probes complete: {n_p} identifiers")

# ── emit ────────────────────────────────────────────────────────────────────
counts = collections.Counter(c['case_class'] for c in cases)
out = {
 '$schema': 'https://alexanarch.org/data/deletion-fixture.schema.json',
 'name': 'Deletion Semantics Conformance Fixture',
 'version': '2.0', 'date': TODAY, 'license': 'CC-BY-4.0',
 'ratified_axes': 'validity / presence / edges per knowledge-catalog#207 (2026-07-27); presence sparse: removed | never_landed | no marker',
 'derived_from': 'Zenodo DOI Resolution Index (current, 1,937 mappings; envelope layer as recorded state) + Alexanarch registry + dated repair artifacts',
 'event': v1.get('event'),
 'population_note': 'The source index holds 1,937 identifiers after two producer withdrawals on 2026-07-28 (v1.0 measured 1,938). Recorded validity distribution at build: tombstone 1,815 · registered 73 · erased 32 · unverified 13 · fragment 3. Not 1,937 deletions; the classes say which is which.',
 'v1_drift_ledger': 'v1.0 (same day, hours earlier) recorded 75 registered; the current envelope layer records 73 — two identifiers changed recorded state within the day. Population 1,938 → 1,937 by disclosed withdrawal. The delta between fixture versions is itself the state-drift exhibit.',
 'selection': selection_note,
 'total_cases': len(cases),
 'classes': dict(sorted(counts.items())),
 'cases': cases,
}
if not _v1p.exists():
    _v1p.write_text(json.dumps(v1, ensure_ascii=False, indent=1))
(FIX / 'cases.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f"v2.0: {len(cases)} cases | classes: {dict(sorted(counts.items()))}")
