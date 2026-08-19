#!/usr/bin/env python3
"""check_surface_synchrony.py — one clock for the archive.

WHY THIS EXISTS (2026-08-12)

An external audit (LABOR) found the archive telling machine visitors three
different answers about how large it is:

    api/index.json          current_count 1444   (declares itself authoritative)
    s/browse/, search-index 1445
    data/registry.json      1456                 (canonical)

`api/index.json` says of itself: "Single source of truth ... If this file
disagrees with any other surface, this file wins and the other surface is
wrong." It was the most wrong of the three.

Two causes, both structural rather than accidental:

  1. The deposit pipeline regenerates record pages, sitemap, OAI and wiki —
     but NOT browse, search-index or api/index. Those move only on a full
     regenerate_surfaces run, so every deposit between full runs was invisible
     to the archive's own PRIMARY discovery index, which api/index.json
     instructs agents to use first.
  2. The api-index generator looked for the file at api/index.json while it has
     always lived at data/api/index.json, so that stage silently no-opped on
     every run and the authority counts froze at their last hand-edit.

The archive's whole argument is that machine-readable state should be
auditable. A surface that misreports its own extent undermines that at the
root, and a machine cannot tell a stale count from a true one.

WHAT THIS CHECKS

Registry head (max deposit_number in data/registry.json) against every
machine-facing surface that publishes a count or a highest-record claim.
Exit code 1 on any disagreement, so it can gate a commit or a deploy.

USAGE
    python3 scripts/check_surface_synchrony.py            # report + exit code
    python3 scripts/check_surface_synchrony.py --quiet    # exit code only
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def registry_head():
    reg = json.loads((ROOT / 'data' / 'registry.json').read_text())
    deposits = reg['deposits']
    gaps = (reg.get('known_gaps') or {}).get('deposit_numbers') or []
    return {
        'head': max(d.get('deposit_number', 0) for d in deposits),
        'count': len(deposits),
        'declared_total': reg.get('total_deposits'),
        # Extent = how many entries exist. With declared gaps, head - len(gaps)
        # is the exact expected extent; an UNdeclared gap still fails, which is
        # the point: a machine cannot distinguish a stale count from a true one,
        # so every gap must be declared or healed. Highest-record claims still
        # compare to head.
        'gaps': gaps,
        'expected_extent': max(d.get('deposit_number', 0) for d in deposits) - len(gaps),
    }


def probe_json(path, *keys):
    p = ROOT / path
    if not p.exists():
        return {'_missing': str(path)}
    try:
        doc = json.loads(p.read_text())
    except Exception as e:
        return {'_unparseable': '%s: %s' % (path, e)}
    out = {}
    for k in keys:
        cur, ok = doc, True
        for part in k.split('.'):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok and isinstance(cur, (int, float)):
            out[k] = cur
        elif ok and isinstance(cur, (list, dict)):
            out[k] = len(cur)
    return out


def probe_html_count(path, pattern=r'([\d,]+)\s+deposits'):
    p = ROOT / path
    if not p.exists():
        return {'_missing': str(path)}
    m = re.search(pattern, p.read_text(errors='replace'))
    return {'deposits_shown': int(m.group(1).replace(',', ''))} if m else {'_no_count_found': str(path)}


def main():
    quiet = '--quiet' in sys.argv
    r = registry_head()
    head = r['head']
    surfaces = [
        ('data/api/index.json', probe_json('data/api/index.json', 'registries.deposits.current_count')),
        ('data/api/search-index.json', probe_json('data/api/search-index.json', 'total_deposits', 'hex_labels')),
        ('data/state.json', probe_json('data/state.json', 'deposits.total', 'deposits.wiki_entries')),
        ('s/browse/index.html', probe_html_count('s/browse/index.html')),
    ]
    failures, notes = [], []
    for name, vals in surfaces:
        for k, v in vals.items():
            if k.startswith('_'):
                # A surface this check cannot READ is a failure, not a note. A
                # check that silently passes over what it cannot see reports a
                # green it has not earned — which is the same class of defect it
                # exists to catch.
                failures.append('%-28s UNREADABLE: %s' % (name, k.lstrip('_').replace('_', ' ')))
                continue
            if v != r['expected_extent']:
                failures.append('%-28s %-34s %s  (expected extent %d = head %d - %d declared gap(s))'
                                % (name, k, v, r['expected_extent'], head, len(r['gaps'])))
    if r['declared_total'] not in (None, r['count']):
        failures.append('%-28s %-34s %s  (actual entries %d)'
                        % ('data/registry.json', 'total_deposits', r['declared_total'], r['count']))
    if not quiet:
        print('registry head: %d  (entries %d, declared gaps %d, expected extent %d)' % (head, r['count'], len(r['gaps']), r['expected_extent']))
        for name, vals in surfaces:
            shown = ', '.join('%s=%s' % (k, v) for k, v in vals.items() if not k.startswith('_')) or '—'
            print('  %-28s %s' % (name, shown))
        for n in notes:
            print('  note: %s' % n)
        if failures:
            print('\nSURFACE SYNCHRONY FAILURES (%d):' % len(failures))
            for f in failures:
                print('  ✗ %s' % f)
            print('\nRun: python3 scripts/regenerate_surfaces.py')
            print('A machine cannot distinguish a stale count from a true one. '
                  'Every surface that publishes an extent must publish the same one.')
        else:
            print('\n✓ all machine-facing surfaces agree with registry head (%d)' % head)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
