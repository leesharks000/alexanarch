#!/usr/bin/env python3
"""extract_cards.py — PROPOSER for the bottom citation-card block.

RULING, MANUS 2026-08-13: "accept card counts as authored per capture against
the frame and keep the script a proposer."

Four segmentation schemes were tried and each fixed the failure in front of it
while breaking one behind: title-suffix false splits, unknown sites dropped
silently, lexicon growth making prose read as card starts, and an ellipsis
boundary rule that rejected real cards whose snippet was not truncated.
Conservation passed at zero loss throughout — which is exactly the point:
conservation proves nothing was LOST, never that boundaries were placed right.
A card split in two conserves every character.

So this script PROPOSES. The authored count, against the frame, is authoritative.
`_boundary_confident` marks whether a proposed start follows a truncated snippet;
it is a hint for the author, never a filter.

Citation extraction is MECHANICAL; cleaning and analysis are AUTHORED. A card
block has a rigid grammar the clipboard preserves:

    {site}{title}{date} — {snippet}

but with NO delimiters between site and title. Segmentation therefore runs off a
LEXICON of site names harvested from the 708 citations already seated, extended
by the domain-shaped tokens present in the text itself. A segment that does not
begin with a known site REFUSES the capture rather than guessing a boundary.
"""
import json, re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
DATE = re.compile(r'([A-Z][a-z]{2} \d{1,2}, \d{4}) — ')
DOMAINY = re.compile(r'(?:www\.)?[a-zA-Z0-9][a-zA-Z0-9\-]*\.(?:org|com|edu|net|io|dev|co\.uk)')

ADDITIONS = ROOT / "rebuild/capture-registry/intake-20260813/lexicon-additions.json"

def lexicon():
    """Known site names. Every addition was surfaced by a REFUSAL, never invented."""
    s = set()
    if ADDITIONS.exists():
        for a in json.loads(ADDITIONS.read_text())["added"]:
            s.add(a["site"])
    p = json.loads(PROJ.read_text())
    for e in p["entries"]:
        for c in (e.get("cite_list") or []):
            if c.get("site"): s.add(c["site"].strip())
        for o in (e.get("observations") or []):
            for c in (o.get("cite_list") or []):
                if c.get("site"): s.add(c["site"].strip())
    return s

SUFFIX = re.compile(r'(?: - |·|\| )$')

def find_sites(text, lex):
    """Every position where a card STARTS.

    TWO DEFECTS THIS GUARDS, both found on the 2026-08-13 batch:

    1. TITLE-SUFFIX FALSE SPLIT. Google ends a card title with " - {Site}", so a
       naive scan split «[2512.23929] Stable envelopes for critical loci - arXiv»
       into two cards. A site occurrence preceded by " - ", "·" or "| " is a
       title suffix, NEVER a card boundary.
    2. UNKNOWN SITE DROPPED. «MIKROE» is in no lexicon and is not domain-shaped,
       so its card vanished and its text was absorbed into the previous
       snippet — conservation still passed while the citation count was wrong.
       Unknown sites are DETECTED and REFUSE the capture.
    """
    def boundary(i):
        """GUARD 3 — a card starts only where the PREVIOUS card ended.

        Growing the lexicon to 342 sites introduced a new false split: a site
        name that is also ordinary prose. «SeaArk Boats» and «Ocean Alexander»
        occur inside titles and snippets, and raw-15 segmented into 43 cards
        where the display showed 18. Google truncates every snippet with an
        ellipsis, so a genuine card boundary is preceded by "..." or "…" — or
        it is the first card, at the body/tail boundary.
        """
        if i == 0: return True
        pre = text[max(0, i-4):i].rstrip()
        return pre.endswith("...") or pre.endswith("\u2026")

    hits = []
    for site in lex:
        if len(site) < 4: continue
        for m in re.finditer(re.escape(site), text):
            if SUFFIX.search(text[max(0, m.start()-3):m.start()]):
                continue                      # guard 1 — title suffix
            hits.append((m.start(), m.end(), site, boundary(m.start())))
    for m in DOMAINY.finditer(text):
        if SUFFIX.search(text[max(0, m.start()-3):m.start()]):
            continue
        hits.append((m.start(), m.end(), m.group(0), boundary(m.start())))
    hits.sort(key=lambda h: (h[0], -(h[1]-h[0])))
    out, last = [], -1
    for s, e, name, conf in hits:
        if s >= last:
            out.append((s, e, name, conf)); last = e
    return out


def unknown_site_cards(tail, sites):
    """A date anchor with no card start between it and the previous one means a
    card whose site the lexicon does not know. Refuse; do not guess."""
    starts = [s for s, _, _, _ in sites] + [len(tail)]
    missing = []
    for m in DATE.finditer(tail):
        prev = max([s for s in starts if s <= m.start()], default=None)
        nxt = min([s for s in starts if s > m.start()], default=len(tail))
        if prev is None:
            missing.append(m.group(1)); continue
        seg_before = tail[prev:m.start()]
        if DATE.search(seg_before):           # two dates, one card start
            missing.append(m.group(1))
    return missing

def extract(tail, lex):
    """Segment the tail into cards. Returns (cards, residue, refusals)."""
    sites = find_sites(tail, lex)
    if not sites: return [], tail, ["no card start found"]
    refusals = ["unknown site — card dated %s has no recognised site name" % d
                for d in unknown_site_cards(tail, sites)]
    cards = []
    for i, (s, e, name, conf) in enumerate(sites):
        end = sites[i+1][0] if i+1 < len(sites) else len(tail)
        seg = tail[e:end]
        d = DATE.search(seg)
        if d:
            title, date, snip = seg[:d.start()], d.group(1), seg[d.end():]
        else:
            title, date, snip = seg, None, ""
        cards.append({"n": i+1, "site": name, "rel": None, "_boundary_confident": conf,
                      "title": title.strip(" -–—.") or None,
                      "date_shown": date,
                      "snip": (snip.strip() or None), "url": None, "note": None})
    residue = tail[:sites[0][0]].strip()
    return cards, residue, refusals

if __name__ == "__main__":
    lex = lexicon()
    print("lexicon: %d known site names" % len(lex), file=sys.stderr)
    txt = pathlib.Path(sys.argv[1]).read_text()
    split = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    cards, residue = extract(txt[split:], lex)
    print(json.dumps({"n_cards": len(cards), "residue_before_first_card": residue[:120],
                      "cards": cards}, indent=1, ensure_ascii=False))
