#!/usr/bin/env python3
"""R2 parity check: canonical index, API map, and /resolve/ selection must
agree on every DOI. /resolve/ uses hits[0] over the mappings array; the API
map is dict-built. With duplicates hard-rejected upstream, this test proves
the two selection semantics coincide, and that every live API target equals
the canonical entry's target under the envelope gate."""
import json, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx = json.load(open(f'{ROOT}/data/doi-resolution-index.json'))
api = json.load(open(f'{ROOT}/api/doi-axn-map.json'))['map']
maps = idx['mappings']
fails = []
# first-occurrence selection (what /resolve/ shows)
first = {}
for m in maps:
    d = m.get('dead_doi')
    if d and d not in first:
        first[d] = m
if len(first) != len(maps):
    fails.append(f"duplicate keys present: rows={len(maps)} unique={len(first)}")
if set(first) != set(api):
    fails.append(f"key sets differ: canonical-only={len(set(first)-set(api))} api-only={len(set(api)-set(first))}")
def expected_target(m):
    env = m.get('envelope') or {}
    if env.get('quarantine'):
        return None
    if m.get('alexanarch_url'):
        return m['alexanarch_url']
    lu = m.get('live_urls') or {}
    return lu.get('repo') or lu.get('github') or lu.get('blog') or None
mismatch = 0
for d, m in first.items():
    exp = expected_target(m)
    got = api.get(d, [None, None])[1]
    if exp != got:
        mismatch += 1
        if mismatch <= 5:
            fails.append(f"target mismatch {d}: canonical→{exp} api→{got}")
if mismatch > 5:
    fails.append(f"...{mismatch} total target mismatches")
env_missing = sum(1 for m in maps if 'envelope' not in m)
if env_missing:
    fails.append(f"entries without envelope: {env_missing}")
if fails:
    print("PARITY FAIL"); [print(' -', f) for f in fails]; sys.exit(1)
live = sum(1 for v in api.values() if v[1] is not None)
print(f"PARITY OK: {len(api)} keys | {live} live | 0 duplicates | envelopes 100% | UI/API selection coincide")
