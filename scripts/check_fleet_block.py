#!/usr/bin/env python3
"""check_fleet_block.py — does each site render the network block EXACTLY ONCE?

Written 2026-08-17 after NB-4 (atlas binding-v3.4). The marker-wrap left an
orphaned copy of the original block on fourteen sites, and every existing check
passed because it asked whether the MARKERS were present -- the marker count was
1 everywhere. A duplicate living OUTSIDE the markers is invisible to any check
that counts containers.

So this counts what a READER SEES: group headers in the rendered HTML. Exactly one
Archive, one Framework Sites, one Heteronym Institutions. Allied Sites is curated
and may appear zero or one time; it is never generated and never counted as a
fault.

    python3 scripts/check_fleet_block.py PATH...        # local checkouts
    python3 scripts/check_fleet_block.py --live         # fetch the live fleet
"""
import re
import sys
import pathlib
import json
import urllib.request

GROUPS = ("Archive", "Framework Sites", "Heteronym Institutions")


def counts(html):
    return {g: len(re.findall(r'<h4[^>]*>\s*' + re.escape(g) + r'\s*</h4>', html, re.I))
            for g in GROUPS}


def check_html(name, html):
    fails = []
    if 'FLEET-NETWORK-START' not in html and not any(counts(html).values()):
        return []                      # no block on this surface; not a fault
    c = counts(html)
    for g, n in c.items():
        if n > 1:
            fails.append(f"{name}: renders {n} '{g}' headers — the block is DUPLICATED")
        elif n == 0:
            fails.append(f"{name}: renders no '{g}' header — the block is broken or partial")
    if html.count('Machine entry') > 1:
        fails.append(f"{name}: renders {html.count('Machine entry')} Machine entry sections")
    return fails


def main():
    fails = []
    if '--live' in sys.argv:
        root = pathlib.Path(__file__).resolve().parents[1]
        man = json.loads((root / 'data/fleet-domains.json').read_text())
        for e in man['domains']:
            d = e['domain'] if isinstance(e, dict) else e
            url = f"https://{d}/"
            try:
                with urllib.request.urlopen(url, timeout=25) as r:
                    fails += check_html(d, r.read().decode('utf-8', 'replace'))
            except Exception as exc:
                print(f"  (unreachable: {d} — {str(exc)[:40]})")
    else:
        for a in sys.argv[1:]:
            for f in sorted(pathlib.Path(a).rglob('index.html')):
                if '.git' in str(f):
                    continue
                fails += check_html(str(f), f.read_text(errors='replace'))
    if fails:
        print(f"FAIL: {len(fails)} problem(s):")
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("OK: every surface renders the network block exactly once")


if __name__ == '__main__':
    main()
