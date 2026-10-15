#!/usr/bin/env python3
"""rerender_records.py — re-render record pages with the registry, keeping their post-render layers.

Two ways of re-rendering one record page lose things, and this script does neither:
  - wire_deposit(n) calls regenerate_static_page(d, eidx) WITHOUT the registry, and the version blocks need it:
    the "Superseded — current version" banner and the Version history list are not drawn. (Found 2026-10-15:
    18 pages touched by the day's repairs had lost one or the other.)
  - regenerate_static_page refuses a page carrying the retirement apparatus (axn:retired) because it would strip
    it; forcing it does strip it.
So: render with the registry (as propagate_record_state.py does), and for a record whose registry entry carries
body_status.retired, re-apply the layer with retire.apply and then the 2026-10-15 form of it — superseded
records are indexable (no robots noindex, canonical self); a stub keeps noindex and its canonical to the
successor ("superseded records are allowed to be indexed. it was only a specific class of unrecoverable
metadata stubs that was to be no indexed").

    python3 scripts/rerender_records.py 1142 1170 66 ...
"""
import json, os, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts')); sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ['ALEXANARCH_FORCE_RERENDER'] = '1'
import wire_deposit
import retire


def main(nums):
    reg = json.load(open(ROOT / 'data/registry.json'))
    by = {d['deposit_number']: d for d in reg['deposits']}
    try:
        eidx = json.load(open(ROOT / 'data/entity-index.json'))
    except Exception:
        eidx = {}
    layered = []
    for n in nums:
        wire_deposit.regenerate_static_page(by[n], eidx, reg)
        r = (by[n].get('body_status') or {}).get('retired')
        if r:
            layered.append((n, r))
    if layered:
        reg2, D = retire.load()
        retire.apply(reg2, D, {n: {'kind': r.get('class', 'superseded'), 'target': r.get('resolves_to'),
                                   'reason': D[n].get('superseded_reason') or D[n].get('duplicate_note') or ''}
                               for n, r in layered})
        for n, r in layered:
            if r.get('class') == 'stub':
                continue
            p = ROOT / f's/records/{n}/index.html'; s = p.read_text()
            s = re.sub(r'<meta name="robots" content="noindex, follow">\n?', '', s, count=1)
            s = re.sub(r'<link rel="canonical" href="[^"]*">',
                       f'<link rel="canonical" href="https://www.alexanarch.org/s/records/{n}/">', s, count=1)
            p.write_text(s)
        # retire.apply rewrote body_status.retired only in its own copy; the registry is not written here
    print(f'rendered {len(nums)} with the registry; retirement layer re-applied to {[n for n, _ in layered]}')


if __name__ == '__main__':
    main([int(a) for a in sys.argv[1:]])
