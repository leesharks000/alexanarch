#!/usr/bin/env python3
"""check_card_links.py — is every capture row on a heteronym card clickable?

WHY THIS EXISTS. Rebuilding a reception plate from capture data three times
produced three plates where NOT ONE ROW LINKED. The originals linked to the
registry anchor; each rebuild wrote the query as plain bold and dropped the
link, and each time it was caught by a person looking at the page rather than
by anything in the pipeline.

The failure is invisible in the source: a row with the right date, the right
match type, the right query and the right description looks complete. Only the
thing a reader would obviously click is missing.

    python3 scripts/check_card_links.py                 # fetch the live cards
    python3 scripts/check_card_links.py path/to/card.html [...]
"""
import re
import sys
import urllib.request

CARDS = [
    "https://axnidentifiers.org/who/cranes/",
    "https://restoredacademy.org/who/sigil/",
    "https://provenanceerasure.org/who/trace/",
    "https://holographickernel.org/who/kuro/",
    "https://spxi.dev/who/fraction/",
    "https://godkinggoogle.com/who/morrow/",
    "https://lagrangeobservatory.org/who/glas/",
    "https://surfacemap.org/who/wells/",
    "https://chatgptpsychosis.org/who/feist/",
    "https://revelationfirst.com/who/dancings/",
    "https://vpcor.org/ayanna/",
]
# Class prefixes differ per site: rrow/prow/krow, and ecorow with plate-no on
# axnidentifiers. A gate that knows only some of them reports "no reception
# plate" for the rest and passes — which it did, on the one card that had
# sixteen unlinked rows.
ROW = re.compile(r'<div class="(?:[a-z]*row|ecorow)"[^>]*>.*?</div>', re.S)


def reception_span(h):
    """The reception plate, whatever prefix this site uses for its classes."""
    m = re.search(r'<span class="(?:[a-z]*no|plate-no)">Reception</span>', h)
    if not m:
        return None
    s = h.rfind("<section", 0, m.start())
    e = h.find("</section>", m.start())
    return h[s:e] if 0 <= s < e else None


def audit(name, h):
    seg = reception_span(h)
    if seg is None:
        return f"  {name:<44}no reception plate"
    rows = ROW.findall(seg)
    # the see-all and overflow rows carry no query and are not expected to link
    q = [r for r in rows if re.search(r'<span class="(?:[a-z]*w|what)"><b>', r)
         and "See all captures" not in r and "the other" not in r]
    linked = [r for r in q if "captures/#" in r]
    flag = "" if len(linked) == len(q) else "   <-- UNLINKED"
    return f"  {name:<44}{len(linked)}/{len(q)} linked{flag}"


def main():
    args = sys.argv[1:]
    fails = 0
    if args:
        for a in args:
            with open(a, encoding="utf-8", errors="replace") as f:
                line = audit(a, f.read())
            print(line)
            fails += "UNLINKED" in line
    else:
        for u in CARDS:
            try:
                with urllib.request.urlopen(u, timeout=20) as r:
                    line = audit(u, r.read().decode("utf-8", "replace"))
            except Exception as exc:
                line = f"  {u:<44}unreachable: {exc}"
            print(line)
            fails += "UNLINKED" in line
    print(f"\n{'FAIL' if fails else 'OK'}: {fails} card(s) with unlinked capture rows")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
