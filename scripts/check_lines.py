#!/usr/bin/env python3
"""Developmental edges must be reciprocal, resolve, and run backward in time.

A body of thought that develops across months is invisible to a composer if its
records carry no edge to one another: measured 2026-09-08, 1,234 of 1,406 ACTIVE
deposits had zero deposit-to-deposit edge of any kind, including a model-collapse
line of 45 records spanning January to September in which only the last four were
linked. Keyword co-membership is not a developmental relation; `line` names the body,
`develops_from`/`developed_by` order it, and this gate keeps the order honest.
"""
import json, sys

reg = json.load(open('data/registry.json', encoding='utf-8'))
deps = reg['deposits']; lines = reg.get('lines') or {}
D = {x['deposit_number']: x for x in deps}
fail = []

for x in deps:
    n = x['deposit_number']
    ln = x.get('line')
    if ln and ln not in lines:
        fail.append(f"#{n}: line '{ln}' is not declared in registry.lines")
    if x.get('line_parent') and not ln:
        fail.append(f"#{n}: has line_parent but no line")
    for fld, inv in (('develops_from', 'developed_by'), ('developed_by', 'develops_from')):
        for e in (x.get(fld) or []):
            t = e.get('deposit')
            if t not in D:
                fail.append(f"#{n}: {fld} names #{t}, which does not exist"); continue
            if not any(r.get('deposit') == n for r in (D[t].get(inv) or [])):
                fail.append(f"#{n}: {fld} #{t}, but #{t} does not name #{n} in {inv} (not reciprocal)")
            if not e.get('what'):
                fail.append(f"#{n}: {fld} #{t} lacks 'what' — an edge must say what the step adds")
    # develops_from must point backward in time
    for e in (x.get('develops_from') or []):
        t = e.get('deposit')
        if t in D:
            a, b = (D[t].get('date') or ''), (x.get('date') or '')
            if a and b and a > b:
                fail.append(f"#{n} ({b}): develops_from #{t} ({a}) — a step cannot develop from something later")

byline = {}
for x in deps:
    if x.get('line'): byline.setdefault(x['line'], []).append(x['deposit_number'])
for f in fail:
    print('  FAIL ' + f)
print(f"check_lines: {len(lines)} lines declared · {sum(len(v) for v in byline.values())} deposits placed · "
      f"{sum(len(x.get('develops_from') or []) for x in deps)} developmental edges · {len(fail)} failure(s)")
for ln, ns in sorted(byline.items()):
    print(f"    {ln}: {len(ns)}")
sys.exit(1 if fail else 0)
