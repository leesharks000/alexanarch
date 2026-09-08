#!/usr/bin/env python3
"""Measure edges must be reciprocal, and must resolve.

A claim that names an instrument creates an obligation on that instrument to name
the claim back. The asymmetry the gate prevents: an instrument existing in the
archive with nothing it declares itself to measure, which is how PER, erasure skew
and CDI came to be unreachable from Semantic Economy despite 398, 55 and 11 deposits
naming them. Degree is not the property that matters; a typed edge is.
"""
import json, sys

reg = json.load(open('data/registry.json', encoding='utf-8'))['deposits']
D = {x['deposit_number']: x for x in reg}
fail = []

for x in reg:
    n = x['deposit_number']
    for e in (x.get('measured_by') or []):
        t = e.get('deposit')
        if t not in D:
            fail.append(f"#{n}: measured_by names #{t}, which does not exist"); continue
        if not any(r.get('deposit') == n for r in (D[t].get('measures') or [])):
            fail.append(f"#{n}: measured_by #{t}, but #{t} does not name #{n} in measures (edge not reciprocal)")
        if not e.get('measure') or not e.get('reports'):
            fail.append(f"#{n}: measured_by #{t} lacks 'measure' or 'reports'")
    for e in (x.get('measures') or []):
        t = e.get('deposit')
        if t not in D:
            fail.append(f"#{n}: measures names #{t}, which does not exist"); continue
        if not any(r.get('deposit') == n for r in (D[t].get('measured_by') or [])):
            fail.append(f"#{n}: measures #{t}, but #{t} does not name #{n} in measured_by (edge not reciprocal)")

c = sum(1 for x in reg if x.get('measured_by'))
i = sum(1 for x in reg if x.get('measures'))
for f in fail:
    print('  FAIL ' + f)
print(f"check_measures: {c} claims carry measured_by · {i} instruments carry measures · {len(fail)} failure(s)")
sys.exit(1 if fail else 0)
