#!/usr/bin/env python3
"""Extract source cards from the seated transcripts of captures flagged citations-unextracted (2026-10-12).

Repair mode. Belief: these captures count citations (cites > 0) but their cite_list is empty because the
extraction step was skipped, not because the transcript lacks the cards. Each card is read from the
transcript as it was seated; nothing is inferred. Two forms are read:
  A. one line per card, 'Site — Title — [Date —] snippet' (the registry's cleaned form);
  B. the raw Google block: a site line, a title line, a snippet line beginning 'Mon D, YYYY — '.
Inline chips ('[Medium +1]', '@ SciLynk +3') name a site, not a work; they are not extracted as cards.
Cards carry rel None (relation not yet classified) and a note saying where they came from; the deposit
resolver (scripts/capture_deposit_links.py) then links them. A capture whose transcript yields no card is
left as it is, with its defect.

  python3 .../extract_cards.py            # dry run
  python3 .../extract_cards.py --write
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
CANON = ROOT / "data/EA-WG-CAPTURES-01.json"
DASH = " — "
DATE = re.compile(r"^(?:[A-Z][a-z]{2} \d{1,2}, \d{4}|\d+ (?:days?|hours?|weeks?|months?) ago)$")
DATE_LEAD = re.compile(r"^((?:[A-Z][a-z]{2} \d{1,2}, \d{4})|\d+ (?:days?|hours?|weeks?|months?) ago) — ")
SITE_CH = re.compile(r"^[\w.·\-’' ]{2,40}$")


class _Site:
    """A site name: site characters, at most three words ('Medium·Lee Sharks', 'www.alexanarch.org', 'PhilPapers').
    An OCR line break can otherwise make a title fragment ('A Work Plan for Retrieval-Layer') read as a site."""
    def match(self, x):
        return bool(SITE_CH.match(x)) and len(x.replace("·", " ").split()) <= 3


SITE = _Site()
NOTE = "extracted 2026-10-12 from the seated transcript (repair: citations-unextracted); relation not yet classified"


def form_a(lines):
    out = []
    for x in lines:
        x = re.sub(r"^\d+\.\s+", "", x.strip())
        parts = x.split(DASH)
        if len(parts) < 3 or not SITE.match(parts[0].strip()) or len(parts[1].strip()) < 8:
            continue
        site, title, rest = parts[0].strip(), parts[1].strip(), parts[2:]
        if rest and DATE.match(rest[0].strip()):
            rest = rest[1:]
        out.append({"site": site, "title": title, "snip": DASH.join(rest).strip()})
    return out


def form_b(lines):
    L = [x.strip() for x in lines if x.strip()]
    out = []
    for i in range(2, len(L)):
        if DATE_LEAD.match(L[i]) and SITE.match(L[i - 2]) and len(L[i - 1]) >= 8 and not DATE_LEAD.match(L[i - 1]):
            out.append({"site": L[i - 2], "title": L[i - 1], "snip": DATE_LEAD.sub("", L[i])})
    return out


def extract(t):
    lines = (t or "").split("\n")
    cards = form_a(lines) or form_b(lines)
    seen, uniq = set(), []
    for c in cards:
        k = (c["site"], c["title"])
        if k not in seen:
            seen.add(k); uniq.append(c)
    return uniq


def main():
    write = "--write" in sys.argv
    reg = json.loads(CANON.read_text(encoding="utf-8"))
    F = [e for e in reg["entries"] if "citations-unextracted" in (e.get("defects") or [])]
    got = 0
    for e in F:
        cards = extract(e.get("transcript"))
        flag = "" if len(cards) == e.get("cites") else f"  (cites {e.get('cites')})"
        print(f"{e['slug'][:58]:58} {len(cards)} card(s){flag}")
        if "--show" in sys.argv:
            for c in cards: print("      ", c["site"], "|", c["title"][:80])
        if cards and len(cards) > (e.get("cites") or 0):
            print("      skipped: more cards than the capture counts — the transcript holds results outside the panel")
            continue
        if cards:
            got += 1
            if write:
                e["cite_list"] = [{"n": i, "site": c["site"], "rel": None, "title": c["title"], "snip": c["snip"], "url": None, "note": NOTE}
                                  for i, c in enumerate(cards, 1)]
                e["defects"] = sorted(set(e["defects"]) - {"citations-unextracted"})
    print(f"{got} of {len(F)} captures yield cards")
    if write:
        CANON.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8"); print("written")


if __name__ == "__main__":
    main()
