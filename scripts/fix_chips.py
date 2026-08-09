#!/usr/bin/env python3
"""fix_chips.py — bring a satellite surface to the chip standard, one site at a time.

NOT A BATCH. Runs against one --path, prints every change it would make, and only
writes with --apply. The reason is on the record: a reformat pass earlier in this
session replaced ten deposited bodies with later versions of the same works because
its guard had never been tested. This one shows its work before it does any.

THREE CASES, and the third needs a human.

  A · chip carries no AXN        → rewrite the chip text to EA · #N · AXN
  B · record link lacks the class → add class, rewrite text to the chip form
  C · axn-chip on a non-record   → strip the class; the link stays a link

CASE B HAS AN EXCEPTION THE AUDIT CANNOT SEE. A record link inside a sentence is
prose, and converting it to an identifier string destroys the sentence to satisfy a
checker. "Read the rhizome MPAI" is a call to action; "the erasure audit" in a row
of three links is a chip position. The difference is whether removing the anchor
text leaves a grammatical sentence. Links whose anchor text begins with a verb, or
that sit inside a <p> with more than a short run of surrounding words, are reported
as PROSE and left alone unless --force-prose is given.
"""
import argparse, html, json, pathlib, re, sys

REG = json.loads(pathlib.Path('/home/claude/live/data/registry.json').read_text())['deposits']
D = {d['deposit_number']: d for d in REG}
REC = re.compile(r'(?:www\.)?alexanarch\.org/s/records/(\d+)/')
VERB_LEAD = re.compile(r'^(read|see|view|open|browse|visit|download|explore|follow|'
                       r'the full|full text|more|here)\b', re.I)


def ea_of(d):
    blob = d.get('title', '') + ' ' + str(d.get('description') or '')[:400]
    m = re.search(r'\b(EA-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\b', blob)
    return m.group(1) if m else None


def chip_text(n):
    d = D[n]
    ea = ea_of(d)
    return " &middot; ".join(([ea] if ea else []) + [f"#{n}", d['axn']])


def looks_like_prose(s, m):
    """A link is prose if its anchor starts with a verb of navigation, or if it sits
       mid-sentence — a lowercase word immediately before it and no block boundary."""
    inner = html.unescape(re.sub(r'<[^>]+>', '', m.group(0))).strip()
    if VERB_LEAD.match(inner):
        return True
    before = re.sub(r'<[^>]+>', '', s[max(0, m.start() - 90):m.start()]).rstrip()
    after = re.sub(r'<[^>]+>', '', s[m.end():m.end() + 60]).lstrip()
    mid = bool(re.search(r'[a-z,]$', before)) and bool(re.match(r'[a-z]', after))
    return mid


def process(path, apply, force_prose):
    changes = {'A': [], 'B': [], 'C': [], 'PROSE': []}
    for p in sorted(pathlib.Path(path).rglob('index.html')):
        if '.git' in str(p):
            continue
        s = p.read_text(errors='replace')
        orig = s
        out, last = [], 0
        for m in re.finditer(r'<a\b([^>]*)>(.*?)</a>', s, re.S):
            attrs, inner = m.group(1), m.group(2)
            cm = re.search(r'class="([^"]*)"', attrs)
            hm = re.search(r'href="([^"]*)"', attrs)
            if not hm:
                continue
            cls = cm.group(1) if cm else ''
            is_chip = 'axn-chip' in cls
            rec = REC.search(hm.group(1))
            text = html.unescape(re.sub(r'<[^>]+>', '', inner)).strip()
            new = None

            if rec and int(rec.group(1)) in D:
                n = int(rec.group(1))
                if D[n]['axn'] in text:
                    continue
                if not is_chip and looks_like_prose(s, m) and not force_prose:
                    changes['PROSE'].append(f"{p.name}: #{n} — “{text[:44]}”")
                    continue
                na = (attrs if is_chip else
                      (attrs.replace(f'class="{cls}"', f'class="{cls} axn-chip"') if cm
                       else attrs + ' class="axn-chip"'))
                new = f'<a{na}>{chip_text(n)}</a>'
                changes['A' if is_chip else 'B'].append(
                    f"{p.name}: #{n} “{text[:36]}” → {chip_text(n)[:52]}")
            elif is_chip and not rec:
                stripped = ' '.join(w for w in cls.split() if w != 'axn-chip')
                na = (attrs.replace(f'class="{cls}"', f'class="{stripped}"') if stripped
                      else re.sub(r'\s*class="[^"]*"', '', attrs))
                new = f'<a{na}>{inner}</a>'
                changes['C'].append(f"{p.name}: strip class — “{text[:40]}” → {hm.group(1)[:38]}")

            if new:
                out.append(s[last:m.start()])
                out.append(new)
                last = m.end()
        out.append(s[last:])
        s = ''.join(out)
        if apply and s != orig:
            p.write_text(s)
    return changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--force-prose', action='store_true')
    a = ap.parse_args()
    c = process(a.path, a.apply, a.force_prose)
    for k, label in (('A', 'chip completed with AXN'), ('B', 'class added + chip form'),
                     ('C', 'axn-chip stripped from non-record link'),
                     ('PROSE', 'PROSE LINK — left alone, needs a human')):
        if c[k]:
            print(f"\n  {label}: {len(c[k])}")
            for x in c[k][:10]:
                print(f"     {x}")
            if len(c[k]) > 10:
                print(f"     … {len(c[k]) - 10} more")
    print(f"\n{'APPLIED' if a.apply else 'DRY RUN'} — "
          f"{sum(len(v) for k, v in c.items() if k != 'PROSE')} change(s), "
          f"{len(c['PROSE'])} prose link(s) skipped")
    return 0


if __name__ == '__main__':
    sys.exit(main())
