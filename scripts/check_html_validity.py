#!/usr/bin/env python3
"""check_html_validity.py — structural HTML faults that silently wreck a page.

MANUS screenshots, 2026-08-04: the browse page's tail was destroyed — superseded
rows read "AXN:… · superseded by" with no target, and every target link appeared
as a long orphaned column of #NNNN after the final row.

CAUSE: the browse card IS an <a>, and the superseded badge nested a second <a>
inside it. Nested anchors are invalid HTML; every browser closes the outer
anchor at the inner one and hoists the remainder. The generator was correct
line-by-line and wrong structurally — which is exactly the class a per-record
check cannot see, because no single record is malformed.

CHECKS
  NESTED_ANCHOR   <a> inside <a> — the browse-tail bug
  UNCLOSED_TAG    div/section/main open-close imbalance beyond tolerance
  ORPHAN_TAIL     content after the generator's own END marker

Exit 1 on any fault. Runs over generated surfaces, not per record.
"""
import glob
import os
import re
import sys

NESTED = re.compile(r'<a [^>]*>(?:(?!</a>).)*?<a ', re.S)
SURFACES = ['s/browse/index.html', 's/index.html', 's/wiki/index.html',
            's/search/index.html', 's/graph/index.html',
            's/records/1/index.html', 's/records/1307/index.html']


def check(paths=None):
    problems = []
    for f in (paths or SURFACES) + sorted(glob.glob('s/*/index.html'))[:12]:
        if not os.path.exists(f):
            continue
        h = open(f, encoding='utf-8', errors='replace').read()
        n = len(NESTED.findall(h))
        if n:
            problems.append((f, 'NESTED_ANCHOR', f'{n} anchors inside anchors — browsers will hoist the inner links'))
        for tag in ('div', 'section', 'main'):
            o = len(re.findall(rf'<{tag}\b', h))
            c = len(re.findall(rf'</{tag}>', h))
            if abs(o - c) > 2:
                problems.append((f, 'UNCLOSED_TAG', f'<{tag}> open {o} / close {c}'))
        m = re.search(r'END-OF-BROWSE-ROWS', h)
        if m and len(re.findall(r'schema.org/CreativeWork', h[m.end():])) > 0:
            problems.append((f, 'ORPHAN_TAIL', 'cards appear after the END marker'))
    print(f'html validity: {len(set(p[0] for p in problems))} surfaces with faults, {len(problems)} findings')
    for f, k, d in problems:
        print(f'   {k:14} {f}: {d}')
    return problems


if __name__ == '__main__':
    sys.exit(1 if check() else 0)
