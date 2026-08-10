#!/usr/bin/env python3
"""citable.py — resolve a deposit to something worth citing.

Sixty records hold a metadata capture, a description, or an external withdrawal
where the work should be. They were being linked into readings and bibliographies
constantly, because body_status.class said metadata_capture and nothing read it.

    python3 scripts/citable.py 1248 324 1036     # check specific records
    python3 scripts/citable.py --audit PATH      # find non-citable chips on a surface
"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = {d['deposit_number']: d for d in
       json.loads((ROOT/'data/registry.json').read_text())['deposits']}


def check(n):
    d = REG.get(n)
    if not d:
        return f"#{n}: NOT IN REGISTRY"
    bs = d.get('body_status') or {}
    if bs.get('citation_class') != 'NON-CITABLE':
        return f"#{n}: citable ({bs.get('class')})"
    if bs.get('superseded_by'):
        return (f"#{n}: NON-CITABLE — {bs.get('class')} — "
                f"CITE #{bs['superseded_by']} INSTEAD")
    return f"#{n}: NON-CITABLE — {bs.get('class')} — ORPHAN, no full version exists"


def audit(path):
    bad = []
    for f in pathlib.Path(path).rglob('*.html'):
        if '.git' in str(f):
            continue
        s = f.read_text(errors='replace')
        for m in re.finditer(r'/s/records/(\d+)/', s):
            n = int(m.group(1))
            bs = (REG.get(n) or {}).get('body_status') or {}
            if bs.get('citation_class') == 'NON-CITABLE':
                bad.append((str(f.relative_to(path)), n, bs.get('superseded_by')))
    seen = set(); out = []
    for f, n, sup in bad:
        if (f, n) in seen:
            continue
        seen.add((f, n)); out.append((f, n, sup))
    for f, n, sup in out:
        print(f"  {f}: #{n} is NON-CITABLE"
              + (f" — cite #{sup}" if sup else " — orphan, no full version"))
    print(f"\n{len(out)} non-citable citation(s)")
    return 1 if out else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--audit':
        sys.exit(audit(a[1] if len(a) > 1 else '.'))
    for x in a:
        print(check(int(x)))
