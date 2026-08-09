#!/usr/bin/env python3
"""audit_chips.py — enforce the chip bibliographic standard across every fleet surface.

WHY THIS EXISTS

The standard is written down. MSP-ROLLOUT names the contract classes and types them
by link target; persistentidentifiers.org is the Chorus-certified reference and
renders every record link as `EA-CODE · #N · AXN:HEX.FAMILY.⬢⬢⬢⬢⬢⬢`. I read both,
agreed with both, converted 48 chips on one page to that form — and in the SAME
COMMIT added a chip with no AXN to the home page of the same site.

Written standards do not survive attention. A standard that depends on an agent
remembering it across two rounds of one conversation will not hold across
instances, sessions, or years. THE ONLY THING THAT HOLDS IS A CHECK THAT FAILS.

THE STANDARD, stated so a machine can test it

  1. A link to alexanarch.org/s/records/N/ MUST carry class="axn-chip".
  2. An axn-chip MUST contain the record's full AXN, byte-exact from registry.json,
     including the six-emoji glyph. Bare hex is forbidden.
  3. An axn-chip SHOULD carry the deposit number as #N.
  4. An axn-chip SHOULD carry the EA code where the record has one.
  5. A link that is NOT to a record MUST NOT carry class="axn-chip".

Rules 1, 2 and 5 fail the build. Rules 3 and 4 are reported.

    python3 scripts/audit_chips.py --path /home/claude/lo
    python3 scripts/audit_chips.py --fleet          # every local checkout
"""
import argparse, html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REC = re.compile(r'(?:www\.)?alexanarch\.org/s/records/(\d+)/')
AXN_IN = re.compile(r'AXN:[0-9A-F]{4}\.[A-Z]+\.')
ANCHOR = re.compile(r'<a\b([^>]*)>(.*?)</a>', re.S)
CLS = re.compile(r'class="([^"]*)"')
HREF = re.compile(r'href="([^"]*)"')


def registry():
    p = ROOT / 'data/registry.json'
    if not p.exists():
        p = pathlib.Path('/home/claude/live/data/registry.json')
    return {d['deposit_number']: d for d in json.loads(p.read_text())['deposits']}


def ea_of(d):
    blob = d.get('title', '') + ' ' + str(d.get('description') or '')[:400]
    m = re.search(r'\b(EA-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+)\b', blob)
    return m.group(1) if m else None


def audit_file(p, D):
    s = p.read_text(errors='replace')
    hard, soft = [], []
    for m in ANCHOR.finditer(s):
        attrs, inner = m.group(1), m.group(2)
        cls = (CLS.search(attrs).group(1) if CLS.search(attrs) else '')
        href = (HREF.search(attrs).group(1) if HREF.search(attrs) else '')
        text = html.unescape(re.sub(r'<[^>]+>', '', inner)).strip()
        is_chip = 'axn-chip' in cls
        rec = REC.search(href)

        if rec and not is_chip:
            n = int(rec.group(1))
            d = D.get(n)
            carries = bool(d and d['axn'] in text)
            (soft if carries else hard).append(
                f"record link without axn-chip class: #{rec.group(1)} — “{text[:40]}”"
                + ("  (AXN present in text; class missing — generator defect)" if carries else ""))
        if is_chip and not rec:
            hard.append(f"axn-chip on a non-record link: {href[:44]} — “{text[:40]}”")
        if is_chip and rec:
            n = int(rec.group(1))
            d = D.get(n)
            if not d:
                hard.append(f"#{n} not in registry")
                continue
            if d['axn'] not in text:
                hard.append(f"#{n} chip carries no AXN — “{text[:46]}”")
            elif AXN_IN.search(text) and d['axn'] not in text:
                hard.append(f"#{n} AXN does not match registry")
            if f"#{n}" not in text:
                soft.append(f"#{n} chip omits the deposit number")
            ea = ea_of(d)
            if ea and ea not in text:
                soft.append(f"#{n} chip omits its EA code {ea}")
    return hard, soft


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path')
    ap.add_argument('--fleet', action='store_true')
    a = ap.parse_args()
    D = registry()

    roots = ([pathlib.Path(a.path)] if a.path else
             [p for p in sorted(pathlib.Path('/home/claude').iterdir())
              if (p / 'index.html').exists() and (p / '.git').exists()] if a.fleet else
             [ROOT])

    total_h = 0
    for r in roots:
        files = [f for f in r.rglob('index.html') if '.git' not in str(f)]
        H, S = [], []
        for f in files:
            h, s_ = audit_file(f, D)
            H += [f"{f.relative_to(r)}: {x}" for x in h]
            S += [f"{f.relative_to(r)}: {x}" for x in s_]
        total_h += len(H)
        mark = 'OK  ' if not H else 'FAIL'
        print(f"  {mark} {r.name:<28} {len(files):>2} page(s) · "
              f"{len(H)} violation(s) · {len(S)} incomplete")
        for x in H[:8]:
            print(f"         {x}")
        if len(H) > 8:
            print(f"         … {len(H) - 8} more")
    print(f"\n{total_h} hard violation(s) across {len(roots)} surface(s)")
    return 1 if total_h else 0


if __name__ == '__main__':
    sys.exit(main())
