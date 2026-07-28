#!/usr/bin/env python3
"""doi_ownership_gate.py — EA-AVAILABILITY-INTEGRITY-01, Task T18(c).

Ownership gate for the DOI resolution index and any future DataCite sift.
No DOI may be mapped as an archive dead-DOI unless it passes, in the
precedence the Assembly ratified (chorus Q8):

  1. ORCID — a creator nameIdentifier matching the archive's ORCID;
  2. Registry-creator match — any creator name appearing in the set of
     names parsed from the registry's own MANUS-confirmed creator strings;
  3. Otherwise: FLAG for MANUS. The gate never removes on its own —
     removal of a mapping is a MANUS ruling (precedent: T18, deposits
     #1382/#1383, ruled 2026-07-28).

Modes:
  --sweep   check every mapping with datacite_state=findable (live DOIs
            are the risk class: a live external DOI mapped as ours is a
            provenance inversion)
  --check DOI ...   gate specific DOIs (for sift-merge time)
"""
import json, re, sys, urllib.request, concurrent.futures

ORCID = '0009-0000-1599-0703'

# DataCite-side creator typos on archive-owned records, verified by MANUS-side
# sweep 2026-07-28 (live Zenodo records; account terminated, unfixable there):
KNOWN_TYPOS = {'sharkd, lee', 'craned, rebekah'}

def registry_name_set():
    reg = json.load(open('data/registry.json'))
    names = set()
    for d in reg['deposits']:
        for part in re.split(r'[;/]| and ', str(d.get('creator',''))):
            p = part.strip()
            if not p or 'ebendorfer' in p.lower():   # the one MANUS-excluded external
                continue
            p = re.sub(r'\(.*?\)', '', p).strip()
            if ',' in p:
                last, first = [x.strip() for x in p.split(',', 1)]
                names.add(f'{first} {last}'.lower()); names.add(p.lower())
            else:
                names.add(p.lower())
                bits = p.split()
                if len(bits) == 2: names.add(f'{bits[1]}, {bits[0]}'.lower())
    return names

def gate_one(doi, names):
    try:
        j = json.loads(urllib.request.urlopen(f'https://api.datacite.org/dois/{doi}', timeout=20).read())
        a = j['data']['attributes']
    except Exception as e:
        return doi, 'unfetchable', str(e)[:60]
    if a.get('state') != 'findable':
        return doi, 'not-findable', a.get('state')
    creators = a.get('creators', [])
    ids = [ni.get('nameIdentifier','') for c in creators for ni in c.get('nameIdentifiers',[])]
    if any(ORCID in (i or '') for i in ids):
        return doi, 'owned-orcid', ''
    cnames = [str(c.get('name','')).lower() for c in creators]
    if any(cn in KNOWN_TYPOS for cn in cnames):
        return doi, 'owned-known-typo', ''
    if any(cn in names or any(n in cn for n in names if len(n) > 8) for cn in cnames):
        return doi, 'owned-registry-creator', ''
    return doi, 'FLAG-FOR-MANUS', str([c.get('name') for c in creators])[:80]

def main():
    names = registry_name_set()
    if '--check' in sys.argv:
        dois = sys.argv[sys.argv.index('--check')+1:]
    else:
        dr = json.load(open('data/doi-resolution-index.json'))
        dois = [m['dead_doi'] for m in dr['mappings']
                if str(m.get('datacite_state','')).lower() == 'findable']
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda d: gate_one(d, names), dois))
    from collections import Counter
    print(f'gated {len(res)} DOIs against {len(names)} registry names:',
          dict(Counter(r[1] for r in res)))
    flags = [r for r in res if r[1] == 'FLAG-FOR-MANUS']
    for d, _, c in flags: print('  FLAG:', d, c)
    return 1 if flags else 0

if __name__ == '__main__':
    sys.exit(main())
