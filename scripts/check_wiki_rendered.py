#!/usr/bin/env python3
"""A record whose wiki is authored must have it on the page.

The record page renders wiki_article only where wiki_status marks the text as
authored; provisional, pending and AUTHORSHIP_REQUIRED entries are deliberately
withheld, because the surface does not publish unauthored prose under a record's
name. That gate is correct and this check does not touch it.

What it catches is the gap that stranded #1601, #1602 and #1603 on 2026-09-09:
a wiki written into the registry, then regenerate_surfaces.py run — which does
NOT rebuild record pages — so the page kept its pre-wiki state. Record pages are
rebuilt by the pipeline's `record` stage (wire_deposit.regenerate_static_page),
and a registry edit that adds an authored wiki must be followed by it.
"""
import json, os, re, html, sys

AUTHORED = {'AUTHORED_IN_SESSION', 'AUTHORED', 'authored', 'authored-in-session',
            'authored_in_session', 'canonical'}

def norm(s):
    # The renderer converts markdown emphasis to <strong>/<em> before escaping,
    # so the registry string's ** and * never appear on the page. Strip them from
    # both sides or the comparison yields false positives on every wiki that opens
    # in bold — 12 of them on 2026-09-09, which is how this check first ran.
    s = html.unescape(s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('**', '').replace('*', '')
    return re.sub(r'\s+', ' ', s).lower()

reg = json.load(open('data/registry.json', encoding='utf-8'))
fail, checked = [], 0
for d in reg['deposits']:
    n = d.get('deposit_number')
    w = (d.get('wiki_article') or '').strip()
    if not n or not w or d.get('wiki_status') not in AUTHORED:
        continue
    if (d.get('status') or 'ACTIVE') != 'ACTIVE':
        continue
    p = f's/records/{n}/index.html'
    if not os.path.exists(p):
        fail.append(f"#{n}: authored wiki, but no record page at {p}"); continue
    checked += 1
    if norm(w)[:50] not in norm(open(p, encoding='utf-8', errors='replace').read()):
        fail.append(f"#{n}: wiki_status={d.get('wiki_status')} but the text is not on the page "
                    f"— run the pipeline's `record` stage for this deposit")

for f in fail:
    print('  FAIL ' + f)
print(f"check_wiki_rendered: {checked} authored wikis checked · {len(fail)} failure(s)")
sys.exit(1 if fail else 0)
