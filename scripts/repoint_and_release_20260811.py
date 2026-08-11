#!/usr/bin/env python3
"""repoint_and_release_20260811.py — DOI Resolution Index v3.6 remediation.

Applies the two rules ratified 2026-08-11 (MANUS; rule M deferred):

  S — SUPERSEDED-target repoint. Any mapping whose routed target now carries
      registry status SUPERSEDED with superseded_by_deposit_number follows the
      pointer transitively (cycle-guarded) to the ACTIVE end of the chain.
      SUPERSEDED targets with no pointer are left untouched and reported.
      Per-row provenance in `supersession_repoint_20260811`.

  Q — Quarantine re-evaluation. `target_title_mismatch` verdicts were computed
      against pre-repair registry titles (PATHOLOGY-27 fixed the registry
      after the verdicts froze). Re-test against CURRENT registry titles:
        exact/prefix match + membership confirmed  -> quarantine released,
            relationship upgraded to same_work_title_matched where weaker,
            evidence appended.
        exact/prefix match + membership NOT confirmed -> quarantine moved to
            membership_not_confirmed (the accurate remaining reason; the
            title objection is withdrawn but no redirect until membership
            confirms — envelope doctrine R1).
        still-mismatch -> untouched.
      Per-row provenance in `quarantine_release_20260811`.

  Derived-field refresh (rule F: AXN/pointers are DERIVED, titles/DOIs are
  FROZEN): mapping `axn` is refreshed from the routed target's current
  registry AXN wherever they disagree (fixes the #3 hex-width staleness and
  every repoint). FROZEN fields — dead_doi, title, date, severance metadata,
  the 1,817/1,935 event quantities — are never regenerated.

After this script: run scripts/sync_resolver.py --apply, then
scripts/validate_resolver.py (read FULL output).
"""
import json, os, re, sys
from collections import Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'data', 'doi-resolution-index.json')
REGISTRY = os.path.join(ROOT, 'data', 'registry.json')
TODAY = date.today().isoformat()

def norm(t):
    return re.sub(r'[^a-z0-9]+', ' ', (t or '').lower()).strip()

def recnum(u):
    if not u: return None
    m = re.search(r'/s/records/(\d+)/?$', str(u))
    return int(m.group(1)) if m else None

def main():
    idx = json.load(open(INDEX))
    reg = json.load(open(REGISTRY))
    deps = {d['deposit_number']: d for d in reg['deposits']}
    maps = idx['mappings']
    stats = Counter()
    no_pointer = []

    def chain_end(n):
        seen = []
        while True:
            if n in seen:
                return None, seen, 'CYCLE'
            seen.append(n)
            d = deps.get(n)
            if d is None:
                return None, seen, 'MISSING'
            if d.get('status') != 'SUPERSEDED':
                return n, seen, d.get('status')
            nxt = d.get('superseded_by_deposit_number')
            if nxt is None:
                return None, seen, 'NO_POINTER'
            n = int(nxt)

    for m in maps:
        t = recnum(m.get('alexanarch_url') or m.get('alexanarch_record'))
        if t is None:
            continue
        d = deps.get(t)
        if d is None:
            continue

        # ---- Rule S ----
        if d.get('status') == 'SUPERSEDED':
            end, seen, endstat = chain_end(t)
            if end is None:
                stats[f's_skipped_{endstat.lower()}'] += 1
                no_pointer.append((m['dead_doi'], t, endstat))
            else:
                m['supersession_repoint_20260811'] = {
                    'from_deposit': t,
                    'to_deposit': end,
                    'chain': seen,
                    'prior_alexanarch_url': m.get('alexanarch_url'),
                    'prior_axn': m.get('axn'),
                    'rule': 'S (ratified 2026-08-11): SUPERSEDED target follows '
                            'superseded_by_deposit_number to ACTIVE chain end',
                }
                m['alexanarch_url'] = f'https://alexanarch.org/s/records/{end}/'
                m['alexanarch_record'] = f'/s/records/{end}/'
                t = end
                d = deps[end]
                stats['s_repointed'] += 1
                if len(seen) > 1 + 1:
                    stats['s_multihop'] += 1

        # ---- Derived AXN refresh (rule F) ----
        ax_now = (d.get('axn') or '').strip()
        ax_map = (m.get('axn') or '').strip()
        if ax_now and ax_map != ax_now:
            m.setdefault('supersession_repoint_20260811', {})  # only if S fired
            if 'prior_axn' not in m.get('supersession_repoint_20260811', {}):
                m['axn_refresh_20260811'] = {'prior_axn': ax_map,
                                             'rule': 'F: AXN is a DERIVED field'}
                if not m['supersession_repoint_20260811']:
                    del m['supersession_repoint_20260811']
            m['axn'] = ax_now
            stats['axn_refreshed'] += 1

        # ---- Rule Q ----
        env = m.get('envelope') or {}
        if env.get('quarantine') == 'target_title_mismatch':
            a, b = norm(m.get('title')), norm(d.get('title'))
            if a and a == b:
                mt = 'exact_current_title'
            elif a and b and (a.startswith(b[:60]) or b.startswith(a[:60])):
                mt = 'prefix_current_title'
            else:
                stats['q_still_mismatch'] += 1
                continue
            rec = {'match_type': mt,
                   'prior_quarantine': 'target_title_mismatch',
                   'prior_relationship': env.get('relationship'),
                   'rule': 'Q (ratified 2026-08-11): verdict recomputed against '
                           'current registry title (post-PATHOLOGY-27 repair)'}
            env.setdefault('evidence', []).append(
                {'type': f'title_reverified_current_registry:{mt}',
                 'source': '/data/registry.json', 'date': TODAY})
            env['last_verified'] = TODAY
            if env.get('archive_membership') == 'confirmed':
                env['quarantine'] = None
                if env.get('relationship') not in ('same_work_restored',
                                                  'same_work_title_matched'):
                    env['relationship'] = 'same_work_title_matched'
                stats[f'q_released_{mt.split("_")[0]}'] += 1
            else:
                env['quarantine'] = 'membership_not_confirmed'
                stats[f'q_requalified_membership_{mt.split("_")[0]}'] += 1
            m['quarantine_release_20260811'] = rec

    # version + logs
    idx['version'] = '3.6'
    idx['changelog'].append({
        'version': '3.6', 'date': TODAY,
        'note': 'Rules S and Q (ratified by MANUS 2026-08-11; rule M deferred). '
                'S: mappings routed to registry-SUPERSEDED duplicate-witness twins '
                'follow superseded_by_deposit_number transitively to the ACTIVE '
                'chain end; per-row provenance in supersession_repoint_20260811. '
                'Q: target_title_mismatch quarantines recomputed against current '
                '(post-PATHOLOGY-27) registry titles; exact/prefix matches with '
                'confirmed membership released with relationship upgraded to '
                'same_work_title_matched; matches without confirmed membership '
                'requalified to membership_not_confirmed; per-row provenance in '
                'quarantine_release_20260811. AXN refreshed as a DERIVED field '
                'wherever the mapping disagreed with the routed target\'s current '
                'registry AXN (rule F). FROZEN fields untouched. Diagnostic: '
                'audit/DOI-INDEX-PHASE1-2026-08-11 (session record).'})
    idx['correction_log'].append({
        'date': TODAY, 'operator': 'TACHYON',
        'directive_from': 'MANUS (Phase 2 ratification: "ratified, defer on m")',
        'method': 'repoint_and_release_20260811.py — see changelog v3.6',
    })

    json.dump(idx, open(INDEX, 'w'), ensure_ascii=False,
              indent=None, separators=(',', ':'))
    print(json.dumps({'stats': dict(stats),
                      'superseded_no_pointer_left_as_is': no_pointer}, indent=1))
    print('WROTE canonical index v3.6 — now run sync_resolver.py --apply '
          'and validate_resolver.py')

if __name__ == '__main__':
    main()
