#!/usr/bin/env python3
"""check_snapshot_freshness.py — a frozen counter must announce itself.

WHY THIS EXISTS (2026-08-12)

data/view-counts.json stopped advancing on 2026-08-09 13:02 UTC. The scheduled
run on 11 August failed at its authenticated canary and, because the aggregator
fails closed, the previous snapshot stayed in place and kept being served. The
site went on displaying a two-day-old figure as though it were current, and
nothing anywhere said otherwise. It took an external audit to notice.

That is the failure mode this archive exists to document, occurring in the
archive's own instrument: a surface that cannot distinguish "no new data" from
"no new data reaching me" will report the first when the truth is the second.

The snapshot failing is acceptable — GoatCounter retains the underlying data
and a later run recovers it. The snapshot failing SILENTLY is not.

WHAT THIS CHECKS

The age of data/view-counts.json's generated_at against the workflow cadence.
The schedule is every other day, so anything past the threshold means at least
one scheduled run did not land.

USAGE
    python3 scripts/check_snapshot_freshness.py               # report + exit code
    python3 scripts/check_snapshot_freshness.py --max-age 4   # custom threshold
"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'data' / 'view-counts.json'
# The workflow cron is '0 5 */2 * *' — every other day at 05:00 UTC. In healthy
# operation the snapshot is therefore never older than ~2 days plus the hours
# since the last scheduled slot. A threshold of 3 days catches ONE missed run
# without firing on normal cadence.
#
# Set to 4 in the first draft, which passed cleanly against the 2026-08-09
# freeze this script was written to detect — a gate calibrated so loosely it
# reported green on the very incident that motivated it. Recorded here because
# it is the same defect the gate exists to catch, committed while building it.
CADENCE_DAYS = 2
DEFAULT_MAX_AGE_DAYS = CADENCE_DAYS + 1


def main():
    max_age = DEFAULT_MAX_AGE_DAYS
    if '--max-age' in sys.argv:
        max_age = float(sys.argv[sys.argv.index('--max-age') + 1])

    if not SNAP.exists():
        print('✗ %s is absent — the displayed counter has no source at all.' % SNAP.name)
        return 1

    snap = json.loads(SNAP.read_text())
    gen = snap.get('generated_at')
    if not gen:
        print('✗ %s has no generated_at — its age cannot be established, '
              'so its currency cannot be claimed.' % SNAP.name)
        return 1

    ts = datetime.fromisoformat(gen.replace('Z', '+00:00'))
    age = (datetime.now(timezone.utc) - ts).total_seconds() / 86400.0
    total = snap.get('total')
    paths = len(snap.get('paths') or {})

    print('snapshot generated_at : %s' % gen)
    print('age                   : %.1f days (threshold %.1f)' % (age, max_age))
    print('total / paths         : %s / %d' % (total, paths))

    if age > max_age:
        print('\n✗ STALE. At least one scheduled snapshot did not land.')
        print('  The site is displaying a %.1f-day-old figure as though current.' % age)
        print('  Check: GitHub Actions → "GoatCounter snapshot" → most recent run.')
        print('  A 404 at the /api/v0/me canary means the API TOKEN is invalid or')
        print('  deleted — not an API change and not a collection failure. The')
        print('  /count tracker is a separate path and keeps collecting regardless.')
        return 1

    print('\n✓ snapshot is current')
    return 0


if __name__ == '__main__':
    sys.exit(main())
