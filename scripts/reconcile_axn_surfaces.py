#!/usr/bin/env python3
"""reconcile_axn_surfaces.py — after any re-glyphing, bring every AXN-bearing
derived surface back into agreement with data/registry.json (which governs).

Surfaces: api/doi-axn-map.json (map[doi] = [axn, record_url]) and
data/doi-resolution-index.json per-mapping axn fields (matched by
alexanarch_record link, falling back to unique-hex match; hex 0365 is
excluded from hex-fallback as a known storage-collision hex).

Prints counts; exits 1 if validate_resolver still reports G8/G6 afterwards.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
reg = json.load(open(ROOT / 'data' / 'registry.json'))
byn = {d['deposit_number']: d['axn'] for d in reg['deposits']}
byhex = {}
for d in reg['deposits']:
    byhex.setdefault(d.get('hex'), []).append(d['deposit_number'])

# api/doi-axn-map.json
mp = json.load(open(ROOT / 'api' / 'doi-axn-map.json'))
fixed_map = 0
for doi, v in mp['map'].items():
    if isinstance(v, list) and v and isinstance(v[0], str) and v[0].startswith('AXN:'):
        n = None
        if len(v) > 1 and isinstance(v[1], str):
            m = re.search(r'/s/records/(\d+)/', v[1])
            if m:
                n = int(m.group(1))
        if n is None:
            hx = v[0].split('.')[0].split(':')[1]
            if hx != '0365' and len(byhex.get(hx, [])) == 1:
                n = byhex[hx][0]
        if n in byn and v[0] != byn[n]:
            v[0] = byn[n]
            fixed_map += 1
json.dump(mp, open(ROOT / 'api' / 'doi-axn-map.json', 'w'), ensure_ascii=False, indent=1)

# data/doi-resolution-index.json
dri = json.load(open(ROOT / 'data' / 'doi-resolution-index.json'))
fixed_dri = 0
for m in dri['mappings']:
    ax = m.get('axn')
    if not isinstance(ax, str) or not ax.startswith('AXN:'):
        continue
    n = None
    mm = re.search(r'/s/records/(\d+)/', str(m.get('alexanarch_record') or ''))
    if mm:
        n = int(mm.group(1))
    if n is None:
        hx = ax.split('.')[0].split(':')[1]
        if hx != '0365' and len(byhex.get(hx, [])) == 1:
            n = byhex[hx][0]
    if n in byn and ax != byn[n]:
        m['axn'] = byn[n]
        fixed_dri += 1
json.dump(dri, open(ROOT / 'data' / 'doi-resolution-index.json', 'w'), ensure_ascii=False, indent=1)

print(f"reconciled: doi-axn-map {fixed_map} | resolution-index {fixed_dri}")
out = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'validate_resolver.py')],
                     capture_output=True, text=True).stdout + ''
bad = out.count('G8_axn_mismatch') + out.count('G6_axn_drift')
print(f"validate: G8+G6 findings = {bad}")
sys.exit(1 if bad else 0)
