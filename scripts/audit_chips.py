#!/usr/bin/env python3
"""audit_chips.py — enforce the chip bibliographic standard across every fleet surface.

SCOPE — THE LIBRARY IS EXCLUDED (MANUS ruling, 2026-08-09)

The chip standard governs SATELLITE SURFACES, not alexanarch. The library retains
its own format because IT IS THE SOURCE: its record pages are what the chips on
every other surface point AT, and a citing convention has no business rewriting the
thing it cites. An earlier run of this script reported 4,324 violations on
alexanarch. Those were not violations. They were the library's own house format,
and flagging them was the same category error as a bibliography demanding that a
book's own title page conform to the bibliography's citation style.

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

  1. A record link IN A DECLARED IDENTIFIER SLOT MUST carry class="axn-chip".
  2. An axn-chip MUST contain the record's full AXN, byte-exact from registry.json,
     including the six-emoji glyph. Bare hex is forbidden.
  3. An axn-chip SHOULD carry the deposit number as #N.
  4. An axn-chip SHOULD carry the EA code where the record has one.
  5. A link that is NOT to a record MUST NOT carry class="axn-chip".

Rules 1, 2 and 5 fail the build. Rules 3 and 4 are reported.

RULE 1 IS SCOPED, AND THE SCOPE IS NOT A HEURISTIC (2026-08-27)

Rule 1 formerly applied to every record link anywhere. Under the corrected
REC pattern that is 58,395 links, and only 4,338 of them have anchor text
that is already an identifier. The remaining 54,057 are links whose text is
a title or a phrase — 'DOIs != Permanent Identifiers', 'the call for papers',
'Zenodotus' Book-Burning'. Enforcing rule 1 across them would replace fifty
thousand readable links with hex strings to satisfy a checker, which is the
standard eating the site it was written to describe.

The scope is taken from what the surfaces already do rather than invented
here. On survivethedeletion, every one of the twenty-three correct chips sits
in <span class="sid">, and the three record links that carry no chip are in
running prose — a colophon sentence and a footer parenthetical. The archive's
own where/ page does the same with <span class="name"> inside .ecorow. The
markup already declares where an identifier belongs; a chip position is a SLOT,
not a guess about anchor text.

SLOTS is therefore an adoption ledger, not a detector. A surface joins the
standard by naming its identifier slot here, and only then do its links come
under rule 1. That makes the rollout auditable one surface at a time and keeps
the red count true instead of aspirational. Candidates not yet adopted are
listed below them; adding one is a deliberate act, and the links it governs
become violations the moment it is added, which is the point.

    python3 scripts/audit_chips.py --path /home/claude/lo
    python3 scripts/audit_chips.py --fleet          # every local checkout
"""
import argparse, html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
# A RECORD LINK IS A RECORD LINK WHETHER OR NOT IT NAMES THE HOST. This pattern
# required an absolute URL until 2026-08-27, so every relative /s/records/N/
# failed to match — which meant a correctly-formed chip on a relative link was
# reported under rule 5 as "axn-chip on a non-record link". Eight such reports
# were standing, all of them false, and the fixer's case C would have STRIPPED
# the class from correct markup to satisfy them. An auditor that misreads its
# own subject does not merely miscount; it directs a repair at healthy tissue.
REC = re.compile(r'(?:(?:www\.)?alexanarch\.org)?/s/records/(\d+)/')
AXN_IN = re.compile(r'AXN:[0-9A-F]{4}\.[A-Z]+\.')

# ADOPTED IDENTIFIER SLOTS. A record link is under rule 1 only inside one of
# these. Add a class here when a surface adopts the standard — not before.
SLOTS = (
    'sid',        # survivethedeletion and the MSP satellites: the source-id span
    'name',       # where/: the .ecorow heteronym roster
)
# CANDIDATES, not yet adopted — each is an identifier position in everything but
# the class name, and each is a deliberate decision to make:
#   'meta'   datasets/refrain-index/: the 'first attested' and 'exemplars' rows,
#            115 links whose anchor text is already a bare #N
SLOT_OPEN = re.compile(
    r'<(?:span|div|td|li)\b[^>]*class="[^"]*\b(?:' + '|'.join(SLOTS) + r')\b[^"]*"[^>]*>\s*$')


def in_slot(before):
    """True when the anchor opens directly inside a declared identifier slot."""
    return bool(SLOT_OPEN.search(before))
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

        # DOORS ARE NOT CHIPS. The MSP contract has .doors — a flex row of verb-led
        # navigation whose links carry .w-chip — and it is a different class from
        # .axn-chip with a different job: a door says what you can DO, a chip says
        # what a thing IS. "Read the specification" inside <div class="doors"> is a
        # door correctly formed, and demanding an identifier there would replace a
        # verb with a hex string. Recognised by the w-chip class rather than by
        # guessing from the anchor text.
        if 'w-chip' in cls:
            continue
        if rec and not is_chip and in_slot(s[max(0, m.start() - 160):m.start()]):
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

    # The library is the source and keeps its own format. Named by directory and by
    # the presence of data/registry.json, so a rename cannot silently re-include it.
    def _is_library(p):
        return (p / 'data' / 'registry.json').exists()

    roots = ([pathlib.Path(a.path)] if a.path else
             [p for p in sorted(pathlib.Path('/home/claude').iterdir())
              if (p / 'index.html').exists() and (p / '.git').exists()
              and not _is_library(p)] if a.fleet else
             [ROOT])
    if a.fleet:
        print("  scope: satellite surfaces. alexanarch is excluded — the library is the\n"
              "         source and retains its own format (MANUS ruling 2026-08-09).\n")

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
