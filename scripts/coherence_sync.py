#!/usr/bin/env python3
"""coherence_sync.py — EA-AVAILABILITY-INTEGRITY-01, Task T3 (audit #1413, H3).

One function, one guarantee: after any mint or registry mutation, every
surface that states a count, a timestamp, or claims governance agrees with
the registry — and the governing index carries content hashes so an agent
can verify surface coherence without trusting prose.

Synchronizes: api/index.json (deposit count, timestamps, surface sha256
block) and llms.txt (deposit count, DOI mapping counts). Called by
deposit_pipeline stage_commit; also runnable standalone. Idempotent."""
import json, hashlib, re, datetime, sys

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()

def main():
    reg = json.load(open('data/registry.json'))
    n, reg_updated = reg['total_deposits'], reg['last_updated']
    now = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')

    api = json.load(open('data/api/index.json'))
    api['last_updated'] = now[:10]
    dep = api.setdefault('registries', {}).setdefault('deposits', {})
    dep['current_count'] = n
    dep['last_updated'] = reg_updated
    surfaces = {p: sha(p) for p in (
        'data/registry.json', 'data/api/search-index.json', 'data/api/body-index.json',
        'data/api/axn-index.json', 'data/doi-resolution-index.json')}
    api['surface_hashes'] = {'algorithm': 'sha256', 'hashed_at': now, 'files': surfaces}
    json.dump(api, open('data/api/index.json', 'w'), ensure_ascii=False, indent=2)

    dr = json.load(open('data/doi-resolution-index.json'))
    mappings = len(dr['mappings'])
    unique = len({m.get('dead_doi') for m in dr['mappings']})
    t = open('llms.txt').read()
    t = re.sub(r'archive of \d[\d,]* deposits', f'archive of {n} deposits', t)
    t = re.sub(r'\d[\d,]*\s+severed DOIs mapped', f'{mappings:,} DOI mappings ({unique:,} unique severed DOIs)', t)
    open('llms.txt', 'w').write(t)
    print(f"coherence_sync: deposits={n} reg_updated={reg_updated} "
          f"doi mappings={mappings} unique={unique} | {len(surfaces)} surfaces hashed")

if __name__ == '__main__':
    main()


# ── F1 (2026-08-06): the federation declaration is COMPUTED on every commit.
# It once advertised 342 fewer deposits than the archive held, for nineteen days.
# A stale root head is how a federation silently diverges, so the number is made
# uncomputable by hand rather than merely corrected.
try:
    import subprocess as _sp, sys as _sys, pathlib as _pl
    _sp.run([_sys.executable, str(_pl.Path(__file__).resolve().parent / "generate_node_declaration.py")],
            check=False)
except Exception as _e:
    print(f"  (node declaration not regenerated: {_e})")
