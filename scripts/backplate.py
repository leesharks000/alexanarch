#!/usr/bin/env python3
"""backplate.py — the version history, on the current record only.

MANUS, 2026-08-10: "we also need to make a plate at bottom of those records, so
it is possible to navigate backwards from most recent — thats the only place you
should be able to go backwards from."

The direction rule is the point. A superseded record links FORWARD to its
successor and nowhere else; the current record is the only place that links
BACK. So a reader can always find the history, and can never wander into it by
following a chain of dead links.

    python3 scripts/backplate.py --plan
    python3 scripts/backplate.py --apply
"""
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGP = ROOT / 'data/registry.json'

PLATE = """<section id="version-history" style="margin:26px 0 0;border-top:1px solid var(--border);
padding-top:14px">
<h2 style="font-size:1em;font-weight:500;color:var(--accent);margin-bottom:4px">Version history</h2>
<p style="font-size:.85em;color:#777;margin-bottom:8px">This is the current record.
{n} earlier {word} kept at {their} own address, each pointing here. They are not citable; this
page is.</p>
<div style="font-size:.86em;line-height:1.7">{rows}</div>
</section>"""

ROW = ('<div style="padding:4px 0;border-bottom:1px solid var(--border)">'
       '<a href="/s/records/{n}/" style="color:var(--accent);text-decoration:none">#{n}</a> '
       '<span style="color:#888;font-family:ui-monospace,monospace;font-size:.85em">'
       '{kind}</span> — {title}{why}</div>')


def build():
    reg = json.loads(REGP.read_text())
    D = {d['deposit_number']: d for d in reg['deposits']}
    back = collections.defaultdict(list)
    for d in reg['deposits']:
        r = (d.get('body_status') or {}).get('retired')
        if r and r.get('resolves_to'):
            back[r['resolves_to']].append((d['deposit_number'], r['class'],
                                           (d.get('superseded_reason') or '')[:90]))
    return reg, D, back


def apply(reg, D, back, dry=True):
    done = 0
    for t, ws in sorted(back.items()):
        p = ROOT / f's/records/{t}/index.html'
        if not p.exists():
            continue
        s = p.read_text(errors='replace')
        if 'id="version-history"' in s:
            continue
        rows = ''.join(
            ROW.format(n=n, kind='metadata capture' if k == 'stub' else 'duplicate witness',
                       title=D[n]['title'][:64],
                       why=(f' <span style="color:#999">— {why}</span>' if why else ''))
            for n, k, why in sorted(ws))
        plate = PLATE.format(n=len(ws), word='witness is' if len(ws) == 1 else 'witnesses are',
                             their='its' if len(ws) == 1 else 'their', rows=rows)
        m = re.search(r'<div class="footer">|</div>\s*</body>', s)
        if not m:
            continue
        if not dry:
            s = s[:m.start()] + plate + s[m.start():]
            p.write_text(s)
            D[t].setdefault('body_status', {})['version_history_plate'] = {
                'witnesses': [n for n, _, _ in ws], 'declared': '2026-08-10',
                'rule': ('Backward navigation lives only on the current record. A superseded '
                         'record links forward and nowhere else.')}
        done += 1
    return done


if __name__ == '__main__':
    reg, D, back = build()
    dry = '--apply' not in sys.argv
    n = apply(reg, D, back, dry=dry)
    print(f"  {len(back)} current records with witnesses · {n} plate(s) "
          f"{'to add' if dry else 'added'}")
    if not dry:
        REGP.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
        print("  registry updated")
