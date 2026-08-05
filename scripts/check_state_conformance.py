#!/usr/bin/env python3
"""check_state_conformance.py — the RULE that replaces the manual catch.

MANUS, 2026-08-04: "I need conformance between banners and all other status
emitters. How do we get that as a rule rather than a manual catch?"

This is that rule. `record_state.derive_state()` is the single source of a
record's declared state; this script asserts that every EMITTER agrees with it:

  · page banner      s/records/<n>/index.html renders the derived label
  · page citability   a non-citable record must warn against citing the page
  · OAI record        carries the derived state and citability
  · pointer surfacing a derived pointer must appear as a link on the page

Exit code 1 on any divergence, with the divergences listed. Wire it into every
propagation run (§5b step 4) so a state that exists in data but not on a page
fails the build instead of waiting to be noticed by a human reading the site.

HISTORY THIS PREVENTS (all one session, all caught by MANUS by eye):
  #941   supersession pointer + reason, status ACTIVE -> banner never rendered
  #1300  ruled complete-as-packet, page still announced "semi-restored"
  ×20    related_instances inscribed, renderer had no block for them
  ×12    body_status.lacuna true, no page ever said so
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_state import derive_state, load_registry  # noqa: E402

NOT_CITABLE_HINT = re.compile(
    r'do not cite this page|not-citable|not yet restored|declared absent|Withdrawn|Superseded',
    re.I)


def check(limit=None, verbose=False):
    reg = load_registry()
    try:
        oi = {r['id']: r for r in json.load(open('data/oai-index.json'))['records']}
    except Exception:
        oi = {}
    problems = []
    checked = 0
    for d in reg['deposits']:
        n = d['deposit_number']
        page_path = f's/records/{n}/index.html'
        if not os.path.exists(page_path):
            continue
        st = derive_state(d)
        page = open(page_path, encoding='utf-8', errors='replace').read()
        checked += 1

        # 1. banner label present for every non-FULL state
        if st['state'] != 'FULL':
            key = re.sub(r'^[^A-Za-z]+', '', st['label']).split('—')[0].strip()[:28]
            if key and key not in page:
                problems.append((n, st['state'], f'banner label absent from page ("{key}")'))

        # 2. non-citable records must say so somewhere on the page
        if not st['citable'] and not NOT_CITABLE_HINT.search(page):
            problems.append((n, st['state'], 'record is not citable-as-full-text but the page does not say so'))

        # 3. a derived pointer must be reachable from the page
        p = st.get('pointer')
        if isinstance(p, int) and f'/s/records/{p}/' not in page:
            problems.append((n, st['state'], f'derived pointer #{p} not linked on page'))
        if isinstance(p, str) and p.startswith('http') and p.split('//')[1].split('/')[0] not in page:
            problems.append((n, st['state'], f'derived external manifestation {p} not linked on page'))

        # 4. OAI agreement
        r = oi.get(n)
        if r is not None:
            if r.get('state') != st['state']:
                problems.append((n, st['state'], f'OAI state is {r.get("state")}'))
            if r.get('citable') is not None and bool(r['citable']) != bool(st['citable']):
                problems.append((n, st['state'], 'OAI citability disagrees'))

        if limit and checked >= limit:
            break

    print(f'state conformance: {checked} records checked, {len(problems)} divergences')
    if problems:
        from collections import Counter
        kinds = Counter(p[2].split('(')[0].strip() for p in problems)
        for k, v in kinds.most_common():
            print(f'   {v:5}  {k}')
        if verbose:
            for n, s, why in problems[:60]:
                print(f'   #{n} [{s}] {why}')
    return problems


if __name__ == '__main__':
    v = '-v' in sys.argv
    probs = check(verbose=v)
    sys.exit(1 if probs else 0)
