#!/usr/bin/env python3
"""repair_dates_from_text_20261017.py — a record's date is the date its own text states (2026-10-17).

WHY. The prediction triage registers each claim at its earliest statement, so it is dated by its deposit, and the
topical readers found deposits whose registry date the deposit's own text contradicts (operative-semiotics
data/reading/triage/TOPICAL-REPORT.md, "Dates"): 2026-01-01 placeholders on records whose text says when they were
dated or deposited, and #1389's 2026-03-22, taken from its predecessor's identifier (…_20260322), on a text headed
2026-06-04. Lee Sharks, 2026-10-17: "go with the in text date and repair the dates."

WHAT. For each record below: the line of its text that states the date is checked to hold the date string; then
`date` is set to it, `date_basis` records the line and the prior value, and the change is recorded with
record_modification.touch (field 'date'). Canonical bytes are not touched.

LEFT, and why:
  #1110, #1251  their texts' own front matter states the registry date (2026-01-13, 2026-01-17); the later material
                in them is the content of the blog posts they were recovered from, not a date the text gives itself.
  #1247, #1249, #1233, #206, #1239  no date stated in the text (#1249 is headed "June 2026", with no day).
  #205, #1222, #1224, #1244, #1245, #1248  the text itself states 2026-01-01.
USAGE  python3 scripts/repair_dates_from_text_20261017.py [--check]
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import record_modification as rm

RULING = 'Lee Sharks, 2026-10-17: "go with the in text date and repair the dates."'
# deposit: (date, the string on the dating line, what the line is)
FIX = {
    1226: ('2026-06-14', 'Date: 14 June 2026', 'the packet header'),
    1234: ('2026-04-16', '"datePublished": "2026-04-16"', 'the page\'s own schema.org datePublished'),
    1235: ('2026-04-04', '| Deposited | 2026-04-04', 'the deposit table'),
    1236: ('2026-04-05', '| Deposited | 2026-04-05', 'the deposit table'),
    1237: ('2026-04-01', '| **v1.3** | 2026-04-01', "the version table's row for this version"),
    1238: ('2026-04-17', '| Deposited | 2026-04-17', 'the deposit table'),
    1240: ('2026-04-02', '**Time Attestation:** 2026-04-02', 'the time attestation'),
    1241: ('2026-04-07', '**Date:** April 7, 2026', 'the header'),
    1242: ('2026-04-17', '| Deposited | 2026-04-17', 'the deposit table'),
    1243: ('2026-04-17', '| Deposited | 2026-04-17', 'the deposit table'),
    1246: ('2026-06-19', '19 June 2026', 'the header'),
    1389: ('2026-06-04', 'Crimson Hexagonal Archive · 2026-06-04', 'the header'),
}


def main():
    check = '--check' in sys.argv
    p = ROOT / 'data/registry.json'; reg = json.load(open(p))
    D = {int(d['deposit_number']): d for d in reg['deposits'] if d.get('deposit_number') is not None}
    done, fail = [], []
    for n, (date, needle, what) in FIX.items():
        d = D[n]
        L = (ROOT / d['full_text_path'].lstrip('/')).read_text(encoding='utf-8').split('\n')
        line = next((i + 1 for i, x in enumerate(L[:80]) if needle in x), None)
        if not line:
            fail.append(f'#{n}: {needle!r} not in the first 80 lines'); continue
        if d.get('date') == date:
            continue
        was = d.get('date')
        if not check:
            d['date'] = date
            d['date_basis'] = (f"In-text date: line {line} of the record's own text ({what}: {L[line - 1].strip()[:120]!r}). "
                               f"Prior registry date {was}. {RULING}")
            rm.touch(d, 'date', f'date repaired to the date the text states (line {line}). {RULING}', was=was, now=date)
        done.append(f'#{n} {was} -> {date} (l.{line})')
    if not check:
        open(p, 'w').write(json.dumps(reg, ensure_ascii=False, indent=2))
    print(('check: ' if check else '') + f'{len(done)} dated', *done, *(['FAIL'] + fail if fail else []), sep='\n  ')
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
