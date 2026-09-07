#!/usr/bin/env python3
"""check_keyword_connectivity.py — no ACTIVE deposit is keyword-isolated.

An isolated deposit is invisible to keyword retrieval: nothing else in the archive
shares a term with it, so a composer that finds it finds only it. The gate:
every ACTIVE deposit carries at least one keyword, and at least one of its
keywords is shared with another ACTIVE deposit.
"""
import json, sys, collections
reg = json.load(open('data/registry.json'))
act = [d for d in reg['deposits'] if (d.get('status') or 'ACTIVE') == 'ACTIVE']
cnt = collections.Counter()
for d in act:
    for w in (d.get('keywords') or []):
        cnt[w.strip().lower()] += 1
none_, alone = [], []
for d in act:
    kws = [w.strip().lower() for w in (d.get('keywords') or []) if w and w.strip()]
    n = d.get('deposit_number')
    if not kws: none_.append(n)
    elif max(cnt[w] for w in kws) < 2: alone.append(n)
for n in none_[:10]: print(f"  FAIL  #{n}: no keywords")
for n in alone[:10]: print(f"  FAIL  #{n}: every keyword unique to it — isolated from keyword retrieval")
print(f"check_keyword_connectivity: {len(act)} active · {len(none_)} without keywords · {len(alone)} isolated")
sys.exit(1 if (none_ or alone) else 0)
