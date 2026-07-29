#!/usr/bin/env python3
"""verify_offline.py — DEFAULT verifier. No network.

Validates the committed fixture against its own invariants: schema shape,
counts, the sparse presence rule, subject-explicit axes, validity discipline,
consumer-expectation presence, and repository evidence for the two local
write-failure cases. Conformance testing runs against the committed
cases.json; nothing here touches the network.

License: MIT.
"""
import json, sys, collections
from pathlib import Path

FIX = Path(__file__).resolve().parent
c = json.load(open(FIX / 'cases.json'))
errors, checked = [], 0

def err(msg): errors.append(msg)

# counts agree with data
counts = collections.Counter(x['case_class'] for x in c['cases'])
if c['total_cases'] != len(c['cases']): err(f"total_cases {c['total_cases']} != {len(c['cases'])}")
if dict(sorted(counts.items())) != c['classes']: err("classes table does not match case data")

ALLOWED_PRESENCE = {'removed', 'never_landed'}
NO_MARKER_CLASSES = {'not_removed_control','membership_unresolved','other_author_collision',
                     'not_an_identifier','superseded_present','state_drift_documented',
                     'registry_update_not_landed'}
for x in c['cases']:
    checked += 1
    cid = f"{x['case_class']}:{x['identifier']}"
    # subject-explicit axes
    if 'axis_subject' not in x or 'kind' not in x['axis_subject']:
        err(f"{cid}: missing axis_subject")
    if 'expected' not in x:
        err(f"{cid}: missing consumer expectations")
    ax = x.get('axes', {})
    p = ax.get('presence')
    if p is not None and p not in ALLOWED_PRESENCE:
        err(f"{cid}: illegal presence marker '{p}' (sparse axis)")
    if x['case_class'] in NO_MARKER_CLASSES and p is not None:
        err(f"{cid}: presence marker forbidden for this class (sparse default)")
    if x['case_class'] == 'never_landed' and p != 'never_landed':
        err(f"{cid}: never_landed class must carry the marker")
    if x['case_class'] == 'registry_update_not_landed' and p is not None:
        err(f"{cid}: inverse case must NOT carry a presence marker")
    # validity discipline: never derived from identifier survival
    v = ax.get('validity')
    if v == 'holds':
        err(f"{cid}: validity 'holds' requires independent claim evidence; none is carried in this fixture")
    # expectations consistency
    ep = x['expected'].get('emit_presence', '__absent__')
    if ep != '__absent__' and ep != p:
        err(f"{cid}: expected.emit_presence={ep} disagrees with axes.presence={p}")
# local evidence for write-failure cases (repository-relative)
root = FIX.parent.parent
for x in c['cases']:
    if x['case_class'] == 'registry_update_not_landed':
        if not (root / 'data' / 'restoration-inplace-2026-07-28.json').exists():
            err("registry_update_not_landed: evidence artifact missing from repository")

print(f"verify_offline: {checked} cases checked · {len(errors)} error(s)")
for e in errors: print("  ✗", e)
sys.exit(1 if errors else 0)
