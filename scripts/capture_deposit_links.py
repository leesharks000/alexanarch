#!/usr/bin/env python3
"""Resolve a capture's source cards to the deposits they are (2026-10-12).

Citation extraction records each card as the interface showed it: site, title, snippet, and a URL
only when the paste carried one (most pasted cards do not). Nothing turned a card into a deposit
number, so a capture's `related_deposits` was filled only when a session wrote it in by hand:
441 of 591 captures had none on 2026-10-12, though their cards named the works.

This module is the join. A card resolves to a deposit by, in order:
  1. url    — a record, wiki or AXN address in the card's URL;
  2. title  — the card title (site suffix and ellipsis removed, at least 20 characters normalised)
              is a prefix of exactly one deposit title, or one deposit title is a prefix of it;
  3. title + identifier — several deposits share the title (a version series): an identifier in
              the card's own title or snippet ('#1635', 'AXN:06C9', 'AXN-06C9') picks one of them.
A title shared by several deposits and not narrowed by an identifier stays UNRESOLVED, with its
candidates recorded; the card does not say which version it was, so no version is chosen for it.

The resolution is written onto the card itself ("deposit", "deposit_basis"), so every link in
`related_deposits` can be traced to the card it came from. Hand-declared links are kept; derived
ones are added to them.

  python3 scripts/capture_deposit_links.py              # dry run: report what would be linked
  python3 scripts/capture_deposit_links.py --write      # write card resolutions and related_deposits
"""
import json, re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANON = ROOT / "data/EA-WG-CAPTURES-01.json"
REG = ROOT / "data/registry.json"

SUFFIX = re.compile(r"\s*(?:[—|·-]\s*(?:Alexanarch|Zenodo|Medium|Academia\.edu|GitHub|figshare|Figshare|"
                    r"Lee Sharks|Crimson Hexagonal Archive|SciLynk|TD Commons)[^—|]*)+$", re.I)
ELLIPSIS = re.compile(r"\s*(?:\.\.\.|…)\s*$")
MIN = 20


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def card_title(t):
    t = ELLIPSIS.sub("", t or "")
    t = SUFFIX.sub("", t)
    return norm(ELLIPSIS.sub("", t))


class Index:
    def __init__(self, deposits):
        self.by_n = {d["deposit_number"]: d for d in deposits}
        self.by_axn = {}
        for d in deposits:
            a = (d.get("axn") or "")[4:8].upper()
            if re.fullmatch(r"[0-9A-F]{4}", a):
                self.by_axn.setdefault(a, d["deposit_number"])
        self.titles = [(norm(d.get("title")), d["deposit_number"]) for d in deposits if len(norm(d.get("title"))) >= MIN]

    def ids_in(self, *texts):
        s = set()
        for t in texts:
            for m in re.finditer(r"(?<![\w/])#(\d{2,4})\b", t or ""):
                if int(m.group(1)) in self.by_n: s.add(int(m.group(1)))
            for m in re.finditer(r"AXN[-:]([0-9A-F]{4})", t or ""):
                if m.group(1) in self.by_axn: s.add(self.by_axn[m.group(1)])
        return s

    def resolve(self, card):
        """Returns (deposit or None, basis, candidates)."""
        u = card.get("url") or ""
        m = re.search(r"alexanarch\.org/s/(?:records|wiki)/(\d+)", u)
        if m and int(m.group(1)) in self.by_n:
            return int(m.group(1)), "url", []
        m = re.search(r"AXN[-:]([0-9A-F]{4})", u)
        if m and m.group(1) in self.by_axn:
            return self.by_axn[m.group(1)], "url", []
        t = card_title(card.get("title"))
        if len(t) < MIN:
            return None, "title too short to match", []
        cands = sorted({n for dt, n in self.titles if dt.startswith(t) or t.startswith(dt)})
        if len(cands) == 1:
            return cands[0], "title", []
        if not cands:
            return None, "no deposit title matches", []
        ids = self.ids_in(card.get("title"), card.get("snip")) & set(cands)
        if len(ids) == 1:
            return ids.pop(), "title + identifier in card", cands
        return None, "title shared by %d deposits; card does not say which" % len(cands), cands


def cards_of(e):
    yield from (e.get("cite_list") or [])
    for o in e.get("observations") or []:
        if o.get("cite_list") is not e.get("cite_list"):
            yield from (o.get("cite_list") or [])


def apply(entries, idx, write=False):
    rep = collections.Counter(); per = []
    for e in entries:
        declared = list(e.get("related_deposits") or [])
        derived = []
        for c in cards_of(e):
            n, basis, cands = idx.resolve(c)
            rep[basis if n is None else "linked by " + basis] += 1
            if write:
                if n is not None:
                    c["deposit"], c["deposit_basis"] = n, basis
                    c.pop("deposit_candidates", None)
                elif cands:
                    c["deposit_candidates"] = cands
            if n is not None and n not in derived:
                derived.append(n)
        new = [n for n in derived if n not in declared]
        if new:
            per.append((e["slug"], bool(declared), new))
            if write:
                e["related_deposits"] = declared + new
    return rep, per


def main():
    write = "--write" in sys.argv
    reg = json.loads(CANON.read_text(encoding="utf-8"))
    idx = Index(json.loads(REG.read_text(encoding="utf-8"))["deposits"])
    before = sum(1 for e in reg["entries"] if e.get("related_deposits"))
    rep, per = apply(reg["entries"], idx, write)

    linked_now = before + sum(1 for s, had, n in per if not had)
    print("cards:", dict(rep))
    print(f"captures with a deposit link: {before} → {linked_now} of {len(reg['entries'])}")
    print(f"captures gaining links: {len(per)} ({sum(1 for s, had, n in per if not had)} had none)")
    if "--list" in sys.argv:
        for s, had, n in per:
            print(f"  {s}: +{n}" + ("" if not had else "  (added to declared)"))
    if write:
        CANON.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
        print("written")


if __name__ == "__main__":
    main()
