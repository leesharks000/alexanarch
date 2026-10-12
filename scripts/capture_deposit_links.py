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
  0. document id — an EA- id in the card title that exactly one deposit title carries;
  2b. title segment — no whole-title match, and the card (25+ characters) matches one segment of a
              deposit title, its main title or a subtitle, split at ':', '—', '–', ' - ', '·', ';';
  3. several deposits share the title: an identifier in the card's own title or snippet ('#1635',
              'AXN:06C9') picks one; else the only one deposited by the capture's date; else, when
              every candidate's supersession pointers end at the same deposit (a version series or a
              duplicate witness), that record of standing — the archive's own ruling, not a choice here.
Otherwise the card stays UNRESOLVED with its candidates recorded.

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
PDF = re.compile(r"^\s*\((?:PDF|DOC|DOCX)\)\s*", re.I)
PIPE_TAIL = re.compile(r"\s+\|\s+.*$")              # Medium '| by Lee Sharks | Jul, 2026', SoundCloud '| Listen to…'
DOCID = re.compile(r"\(?\b(EA-[A-Z0-9]+(?:-[A-Z0-9]+)*(?:\.\d+)?)(?:\s+v[\d.]+)?\)?:?", re.I)
MIN = 20
SEG_MIN = 25                                          # a card matching one segment (main title or subtitle) of a deposit title
SEG = re.compile(r"\s*(?::|—|–|\s-\s|·|;)\s*")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def strip_ids(t):
    return DOCID.sub(" ", t or "")


def card_title(t):
    t = PDF.sub("", ELLIPSIS.sub("", t or ""))
    t = PIPE_TAIL.sub("", SUFFIX.sub("", t))
    return norm(ELLIPSIS.sub("", strip_ids(t)))


def doc_ids(t):
    return {m.group(1).upper() for m in DOCID.finditer(t or "")}


VER = re.compile(r"\bv(\d+(?:\.\d+)+)\b", re.I)


def versions(t):
    return set(VER.findall(t or ""))


class Index:
    def __init__(self, deposits):
        self.by_n = {d["deposit_number"]: d for d in deposits}
        self.by_axn = {}
        for d in deposits:
            a = (d.get("axn") or "")[4:8].upper()
            if re.fullmatch(r"[0-9A-F]{4}", a):
                self.by_axn.setdefault(a, d["deposit_number"])
        self.titles = [(norm(strip_ids(d.get("title"))), d["deposit_number"]) for d in deposits if len(norm(strip_ids(d.get("title")))) >= MIN]
        self.segments = [(norm(g), d["deposit_number"]) for d in deposits for g in SEG.split(strip_ids(d.get("title")))
                         if len(norm(g)) >= SEG_MIN]
        self.by_docid = {}
        for d in deposits:
            for i in doc_ids(d.get("title")):
                self.by_docid.setdefault(i, set()).add(d["deposit_number"])

    def ids_in(self, *texts):
        s = set()
        for t in texts:
            for m in re.finditer(r"(?<![\w/])#(\d{2,4})\b", t or ""):
                if int(m.group(1)) in self.by_n: s.add(int(m.group(1)))
            for m in re.finditer(r"AXN[-:]([0-9A-F]{4})", t or ""):
                if m.group(1) in self.by_axn: s.add(self.by_axn[m.group(1)])
        return s

    def standing(self, n):
        """The record of standing for a deposit: follow its supersession pointers to the end."""
        seen = set()
        while n in self.by_n and n not in seen:
            seen.add(n); d = self.by_n[n]
            nxt = d.get("superseded_by_deposit_number") or d.get("superseded_by")
            if not isinstance(nxt, int) or nxt not in self.by_n: break
            n = nxt
        return n

    def resolve(self, card, date=None):
        """Returns (deposit or None, basis, candidates). `date` is the capture's date, used only to
        narrow a version series to the versions that existed when the card was shown."""
        u = card.get("url") or ""
        m = re.search(r"alexanarch\.org/s/(?:records|wiki)/(\d+)", u)
        if m and int(m.group(1)) in self.by_n:
            return int(m.group(1)), "url", []
        m = re.search(r"AXN[-:]([0-9A-F]{4})", u)
        if m and m.group(1) in self.by_axn:
            return self.by_axn[m.group(1)], "url", []
        ids_c, ver_c = doc_ids(card.get("title")), versions(card.get("title"))
        for i in ids_c:
            hit = self.by_docid.get(i) or set()
            if len(hit) == 1:
                return next(iter(hit)), "document id", []
            vhit = {n for n in hit if versions(self.by_n[n].get("title")) & ver_c}
            if len(vhit) == 1:
                return vhit.pop(), "document id + version", []
        t = card_title(card.get("title"))
        if len(t) < MIN:
            return None, "title too short to match", []
        basis = "title"
        cands = sorted({n for dt, n in self.titles if dt.startswith(t) or t.startswith(dt)})
        if not cands and len(t) >= SEG_MIN:
            basis = "title segment"
            # a card may be cut short of a segment, or run past it by a date or version tag (12 characters),
            # never by a further title: "Hexagonal Contributor License v2.0 — Rhys Owens" is not the KADEEZY license
            cands = sorted({n for g, n in self.segments if g.startswith(t) or (t.startswith(g) and len(t) - len(g) <= 12)})
        if len(cands) == 1:
            return cands[0], basis, []
        if not cands:
            return None, "no deposit title matches", []
        if ids_c:
            narrowed = [n for n in cands if doc_ids(self.by_n[n].get("title")) & ids_c]
            if len(narrowed) == 1:
                return narrowed[0], basis + " + document id", cands
        if ver_c:
            narrowed = [n for n in cands if versions(self.by_n[n].get("title")) & ver_c]
            if len(narrowed) == 1:
                return narrowed[0], basis + " + version", cands
        ids = self.ids_in(card.get("title"), card.get("snip")) & set(cands)
        if len(ids) == 1:
            return ids.pop(), basis + " + identifier in card", cands
        if date:
            existed = [n for n in cands if (self.by_n[n].get("date") or "9999") <= date]
            if len(existed) == 1:
                return existed[0], basis + "; the only version deposited by the capture date", cands
        heads = {self.standing(n) for n in cands}
        if len(heads) == 1:
            return heads.pop(), basis + "; one version series, linked to the record of standing its supersession names", cands
        return None, "title shared by %d deposits; card does not say which" % len(cands), cands


def cards_of(e):
    """Every card on an entry and its observations, with the date it was shown."""
    for c in e.get("cite_list") or []:
        yield c, e.get("date")
    for o in e.get("observations") or []:
        if o.get("cite_list") is not e.get("cite_list"):
            for c in o.get("cite_list") or []:
                yield c, o.get("date") or e.get("date")


def apply(entries, idx, write=False):
    rep = collections.Counter(); per = []
    for e in entries:
        declared = list(e.get("related_deposits") or [])
        derived = []
        for c, dt in cards_of(e):
            n, basis, cands = idx.resolve(c, dt)
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
    unext = [e["slug"] for e in reg["entries"] if (e.get("cites") or 0) > 0 and not e.get("cite_list")]
    print(f"captures counting citations with no cards extracted (citations-unextracted): {len(unext)}")
    if write:
        for e in reg["entries"]:
            if e["slug"] in unext and "citations-unextracted" not in (e.get("defects") or []):
                e["defects"] = sorted(set((e.get("defects") or []) + ["citations-unextracted"]))
    if write:
        CANON.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
        print("written")


if __name__ == "__main__":
    main()
