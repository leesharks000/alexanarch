#!/usr/bin/env python3
"""retire.py — make dead records resolve forward instead of being cited.

MANUS, 2026-08-10: "lets retire the metadata stubs and fold the superceded
records into most recent, as we go, so that links always resolve to most recent
or complete."

Two populations, one behaviour. A SUPERSEDED record has a live successor and
redirects to it. A NON-CITABLE stub holds a metadata capture where the work
should be; where a successor exists it redirects, and where none does it says
so plainly rather than presenting the capture as the work.

Both keep their URL. Nothing is deleted — deletion would hide the severance,
which is the thing this archive exists to document. What changes is that the
page stops behaving like the work: it carries a canonical link to the successor,
a robots noindex so it stops being indexed as though it were the work, and a
banner a reader meets before the body.

    python3 scripts/retire.py --plan     # what would change
    python3 scripts/retire.py --apply    # do it
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGP = ROOT / 'data/registry.json'

BANNER_SUP = """<div style="border:1px solid #c8b78a;background:#fdfaf1;padding:14px 18px;
margin:0 0 18px;border-radius:4px;font-size:.92em;line-height:1.6">
<div style="font-family:ui-monospace,monospace;font-size:.78em;letter-spacing:.12em;
text-transform:uppercase;color:#8a6a20;margin-bottom:6px">Superseded record</div>
This record is a {kind} of a work that has a current version. It is kept because removing it
would hide the record's history, but it should not be cited.
<div style="margin-top:8px"><b>Cite instead:</b>
<a href="/s/records/{target}/" style="color:#1a3a5c">#{target} — {ttitle}</a></div>
</div>"""

BANNER_STUB = """<div style="border:1px solid #d8a9a9;background:#fdf4f4;padding:14px 18px;
margin:0 0 18px;border-radius:4px;font-size:.92em;line-height:1.6">
<div style="font-family:ui-monospace,monospace;font-size:.78em;letter-spacing:.12em;
text-transform:uppercase;color:#a41623;margin-bottom:6px">Metadata capture — not the work</div>
The body of this record is a captured description, not the work it describes. It was assembled
after the work was severed at its original host and no authorial surface survived to recover.
{tail}
</div>"""

TAIL_ORPHAN = ("<div style=\"margin-top:8px\"><b>No full-text version exists anywhere in the "
               "archive.</b> This is a real loss, recorded rather than concealed.</div>")
TAIL_TARGET = ('<div style="margin-top:8px"><b>Cite instead:</b> '
               '<a href="/s/records/{target}/" style="color:#1a3a5c">#{target} — '
               '{ttitle}</a></div>')


def load():
    reg = json.loads(REGP.read_text())
    return reg, {d['deposit_number']: d for d in reg['deposits']}


def targets(D):
    """Resolve each dead record to the record a reader should land on."""
    out = {}
    for d in D.values():
        n = d['deposit_number']
        bs = d.get('body_status') or {}
        sup = d.get('superseded_by_deposit_number')
        stub = bs.get('citation_class') == 'NON-CITABLE'
        if not sup and not stub:
            continue
        # follow the chain, in case a successor is itself superseded
        t, seen = sup or bs.get('superseded_by'), {n}
        while t and t in D and t not in seen:
            seen.add(t)
            nxt = D[t].get('superseded_by_deposit_number')
            if not nxt or nxt in seen:
                break
            t = nxt
        out[n] = {'target': t if t in D else None,
                  'kind': 'stub' if stub else 'superseded',
                  'reason': (d.get('superseded_reason') or bs.get('citation_rule') or '')[:200]}
    return out


def apply(reg, D, plan):
    changed = 0
    for n, info in plan.items():
        p = ROOT / f's/records/{n}/index.html'
        if not p.exists():
            continue
        s = p.read_text(errors='replace')
        if 'axn:retired' in s:
            continue
        t = info['target']
        tt = (D[t]['title'][:70] if t else '')
        if info['kind'] == 'stub':
            tail = (TAIL_TARGET.format(target=t, ttitle=tt) if t else TAIL_ORPHAN)
            banner = BANNER_STUB.format(tail=tail)
        else:
            kind = 'duplicate witness' if 'uplicate' in info['reason'] else 'fragment'
            banner = BANNER_SUP.format(kind=kind, target=t, ttitle=tt)
        head = ('<meta name="robots" content="noindex, follow">\n'
                f'<meta name="axn:retired" content="{info["kind"]}">\n')
        if t:
            head += f'<link rel="canonical" href="https://www.alexanarch.org/s/records/{t}/">\n'
        s = re.sub(r'<link rel="canonical"[^>]*>', '', s)
        s = s.replace('</head>', head + '</head>', 1)
        m = re.search(r'<div class="wrap">', s)
        if m:
            s = s[:m.end()] + '\n' + banner + s[m.end():]
        else:
            s = s.replace('<body>', '<body>' + banner, 1)
        p.write_text(s)
        # and record it on the deposit
        d = D[n]
        d.setdefault('body_status', {})['retired'] = {
            'class': info['kind'], 'resolves_to': t,
            'declared': '2026-08-10',
            'note': ('Page carries noindex, a canonical link to the successor where one exists, '
                     'and a banner before the body. The URL is kept; the record is not deleted, '
                     'because deletion would hide the severance.')}
        changed += 1
    return changed


if __name__ == '__main__':
    reg, D = load()
    plan = targets(D)
    orph = [n for n, v in plan.items() if not v['target']]
    print(f"  {len(plan)} records to retire "
          f"({len(plan) - len(orph)} redirect, {len(orph)} orphaned)")
    if '--apply' in sys.argv:
        n = apply(reg, D, plan)
        REGP.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
        print(f"  applied to {n} page(s); registry updated")
    else:
        for k, v in list(plan.items())[:8]:
            print(f"    #{k} [{v['kind']}] → {v['target'] or 'ORPHAN'}")
