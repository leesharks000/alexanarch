#!/usr/bin/env python3
"""resolve_links.py — repoint surface links at current records.

Every /s/records/N/ link on a surface is checked against data/retired-records.json.
Superseded records and metadata stubs are repointed at their successor; orphans
are reported so a builder can state the absence instead of linking a capture.

REPOINTS ONLY. It never deletes a row — a greedy deletion pattern once cut a
heteronym page from 32 records to 9, and the rule since is that a repair may
move a link but not remove content.

    python3 scripts/resolve_links.py PATH            # report
    python3 scripts/resolve_links.py PATH --apply    # repoint
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RET = json.loads((ROOT / 'data/retired-records.json').read_text())['records']
_REG_RAW = json.loads((ROOT / 'data/registry.json').read_text())
SERIES = {d['deposit_number']: d['version_series'] for d in _REG_RAW['deposits']
          if d.get('version_series') and not d['version_series'].get('is_head')}
REG = {d['deposit_number']: d for d in
       json.loads((ROOT / 'data/registry.json').read_text())['deposits']}


def ea(d):
    m = re.search(r'\b(EA-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\b',
                  d.get('title', '') + ' ' + str(d.get('description') or '')[:400])
    return m.group(1) if m else None


def chip(n):
    d = REG[n]
    e = ea(d)
    return " &middot; ".join(([e] if e else []) + [f"#{n}", d['axn']])


def run(path, apply=False):
    moved = orphans = 0
    for f in sorted(pathlib.Path(path).rglob('*.html')):
        if '.git' in str(f):
            continue
        s = f.read_text(errors='replace')
        o = s
        for n in sorted({int(m.group(1)) for m in re.finditer(r'/s/records/(\d+)/', s)}):
            info = RET.get(str(n))
            if not info:
                vs = SERIES.get(n)
                if vs:
                    print(f"  {f.name}: #{n} is {vs['version']} of "
                          f"{vs['series']} — head is #{vs['head']} ({vs['head_version']}). "
                          'Citable for its own date; cite the head for the current work.')
                continue
            t = info['resolves_to']
            if not t:
                orphans += 1
                print(f"  {f.name}: #{n} is an ORPHAN capture — state the absence, do not link")
                continue
            print(f"  {f.name}: #{n} → #{t}")
            moved += 1
            if apply:
                s = re.sub(
                    rf'href="(?:https://www\.alexanarch\.org)?/s/records/{n}/"'
                    r'(?:\s+data-axn="[^"]*")?>[^<]*</a>',
                    f'href="https://www.alexanarch.org/s/records/{t}/" '
                    f'data-axn="{REG[t]["axn"]}">{chip(t)}</a>', s)
        if apply and s != o:
            f.write_text(s)
    print(f"\n  {moved} repointed, {orphans} orphan reference(s)")
    return 1 if orphans else 0


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    sys.exit(run(a[0] if a else '.', '--apply' in sys.argv))
