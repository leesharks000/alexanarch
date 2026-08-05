#!/usr/bin/env python3
"""check_body_hygiene.py — find conversion defects in canonical bodies.

MANUS, 2026-08-04, on #1225: "check the formatting and garbling... how do we
find and fix the rest?"

This is the finder. Four defect classes, each with a signature that cannot be
confused with authorial intent, each discovered the hard way this session:

  ENTITIES     raw HTML entities (&#8212; &nbsp; &amp;) left in canonical text.
               A conversion never decoded them. 37 records, 4,068 instances.
  RUNON        block structure collapsed — a "paragraph" of many thousands of
               characters where the source held <p> tags. #1225 held a 31,422-
               char blob; #1396 held 125,213. Source HTML had 79 <p> all along.
  GLUED        heading markers welded mid-line ("thermodynamics## Table of
               Contents") — the capture pipeline ate the newline. 580 records.
  HARDWRAP     extractor page-wraps preserved as line breaks, with hyphen
               splits across them ("Inter-\\nvention"). PDF seating defect.

EXEMPTIONS (structural, not judgment calls):
  · site-source deposits — a deployed HTML page IS one block; RUNON is expected
  · verse/poetry — short lines are prosody, never HARDWRAP
  · fenced code — never reflowed, never measured

Usage:
    python3 scripts/check_body_hygiene.py            # summary
    python3 scripts/check_body_hygiene.py -v         # per-record
    python3 scripts/check_body_hygiene.py --json OUT # machine-readable queue

Exit 1 if any defect is found, so it can gate a propagation run alongside
check_state_conformance.py.
"""
import json
import os
import re
import sys

MARK = 'Canonical bytes below the rule.'
ENT = re.compile(r'&(?:#\d{2,5}|nbsp|amp|quot|lt|gt|mdash|ndash|rsquo|lsquo|ldquo|rdquo|hellip);')
GLUE = re.compile(r'[^\n\s]#{2,6} ')
RUNON_CHARS = 6000
VERSE_TYPES = {'Poetry', 'Patent-poem', 'Creative work (mixed)', 'Scripture'}


def _rd(p):
    return open(p, encoding='utf-8', errors='replace').read()


def body_of(d):
    hexid = d.get('hex')
    for p in (f'data/texts/AXN-{hexid}-text.md', f'data/deposits/AXN-{hexid}.md'):
        if os.path.exists(p):
            raw = _rd(p)
            return raw.split(MARK, 1)[1] if MARK in raw else re.sub(r'^---.*?---\s*', '', raw, flags=re.S)
    return ''


def is_site_source(d, body):
    bs = d.get('body_status') or {}
    if isinstance(bs, dict) and bs.get('external_manifestation'):
        return True
    return body.count('<') > 200 and '```html' in body


def scan(d):
    """Return list of (defect, detail) for one record."""
    body = body_of(d)
    if len(body) < 600:
        return []
    out = []
    # code fences excluded from all measurement
    parts = body.split('```')
    prose = ''.join(parts[i] for i in range(0, len(parts), 2))

    ents = ENT.findall(prose)
    if len(ents) >= 3:
        out.append(('ENTITIES', f'{len(ents)} raw entities'))

    if not is_site_source(d, body):
        paras = [p for p in prose.split('\n\n') if p.strip()]
        if paras:
            longest = max(len(p) for p in paras)
            if longest > RUNON_CHARS:
                out.append(('RUNON', f'longest block {longest:,} chars'))

    glued = len(GLUE.findall(prose))
    total_h = len(re.findall(r'#{2,6} ', prose))
    if glued >= 3 and total_h and glued / total_h > 0.5:
        out.append(('GLUED', f'{glued}/{total_h} heading markers welded mid-line'))

    if (d.get('content_type') or '') not in VERSE_TYPES:
        lines = [l for l in prose.split('\n') if l.strip()]
        if len(lines) >= 30:
            hyph = sum(1 for l in lines if re.search(r'[a-z][-\u2010\u2011]$', l.rstrip()))
            band = sum(1 for l in lines if 52 <= len(l.rstrip()) <= 82) / len(lines)
            if hyph >= 5 and band > 0.4:
                out.append(('HARDWRAP', f'{hyph} hyphen line-splits, {band:.0%} of lines in wrap band'))
    return out


def main():
    reg = json.loads(_rd('data/registry.json'))
    findings = {}
    for d in reg['deposits']:
        f = scan(d)
        if f:
            findings[d['deposit_number']] = f
    from collections import Counter
    kinds = Counter(k for v in findings.values() for k, _ in v)
    print(f'body hygiene: {len(reg["deposits"])} records scanned, '
          f'{len(findings)} with defects')
    for k, v in kinds.most_common():
        print(f'   {v:5}  {k}')
    if '-v' in sys.argv:
        for n in sorted(findings):
            for k, detail in findings[n]:
                print(f'   #{n} [{k}] {detail}')
    if '--json' in sys.argv:
        out = sys.argv[sys.argv.index('--json') + 1]
        json.dump({str(k): v for k, v in findings.items()}, open(out, 'w'), indent=1)
        print(f'queue written: {out}')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
