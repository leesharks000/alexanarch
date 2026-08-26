#!/usr/bin/env python3
"""Probe G — tombstone-aware translation. The emitter DOES carry presence/reason/
successor, as prose in tombstones.md. Test: how much of the 111-case corpus fits
that line format, and can a consumer round-trip it back to structured fields?"""
import json, re
from collections import Counter
from pathlib import Path

TOMB_LINE = re.compile(
    r"^\*\s+\*\*(?P<id>[^*]+)\*\*\s+—\s+presence:\s*(?P<presence>\S+)\s+—\s+"
    r"tombstoned\s+(?P<date>\S+)\s+—\s+reason:\s*(?P<reason>[^—]+?)\s+—\s+"
    r"successor:\s*(?P<successor>\S+)\s*$")

# 1. round-trip the published tombstone
pub = Path("bundle/tombstones.md").read_text()
rt = [m.groupdict() for line in pub.splitlines() if (m := TOMB_LINE.match(line))]
print("ROUND-TRIP of published tombstones.md:", len(rt), "parsed")
for r in rt: print("  ", json.dumps(r))

# 2. render the corpus into that line format; count what fits
cases = json.loads(Path("cases.json").read_text())["cases"]
fits, misfits = [], Counter()
for c in cases:
    axes = c.get("axes") or {}
    presence = axes.get("presence")
    reason = (c.get("reason") or {}).get("reason")
    succ = c.get("successor")
    if not presence:
        misfits["no presence value"] += 1; continue
    if presence not in ("removed",):
        misfits[f"presence '{presence}' — line format says 'tombstoned'"] += 1; continue
    if not reason:
        misfits["no reason"] += 1; continue
    if not succ:
        misfits["no successor — field is not optional in the line grammar"] += 1; continue
    fits.append(f"* **{c['identifier']}** — presence: {presence} — tombstoned "
                f"{(c.get('recorded') or {}).get('last_verified','?')} — reason: {reason} "
                f"— successor: {succ}")
print(f"\nCORPUS → tombstone line format: {len(fits)}/{len(cases)} fit")
for k,v in misfits.most_common(): print(f"  {v:>4}  {k}")
Path("out-tombstones.md").write_text("# Removed Concepts\n\n" + "\n".join(fits) + "\n")

# 3. can the consumer round-trip what we wrote?
back = [m.groupdict() for line in Path("out-tombstones.md").read_text().splitlines()
        if (m := TOMB_LINE.match(line))]
print(f"\nROUND-TRIP of our rendering: {len(back)}/{len(fits)} re-parse")
if len(back) < len(fits):
    bad = [l for l in fits if not TOMB_LINE.match(l)][:2]
    for b in bad: print("  UNPARSEABLE:", b[:150])

# 4. which corpus fields still have no home even with tombstones counted
HOMED = {"identifier","axes","reason","successor","recorded","work_title","evidence"}
homeless = Counter()
for c in cases:
    for k in c:
        if k in HOMED or k in ("expected","in_v1","case_class","axis_subject"): continue
        homeless[k] += 1
print("\nfields with no emitter home even counting tombstones.md:")
for k,v in homeless.most_common(): print(f"  {v:>4}  {k}")
