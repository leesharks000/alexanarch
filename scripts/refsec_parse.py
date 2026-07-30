#!/usr/bin/env python3
"""
refsec_parse.py — triage and parse the freeform reference-section queue.

NO-DOUBLE-DRAW: this is mechanical, deterministic work. No API calls. Entries
that resist deterministic parsing are left `pending` for in-session judgment
rather than guessed at.

THE TRIAGE FINDING: a large share of the queue is not bibliography. Reference
sections in the corpus interleave true citations with relation tables, statute
strings, apparatus fragments, and prose. Marking a non-reference `pending`
forever is the same defect as marking silence a falsity: it records absence of
work where no work is owed. Each non-reference is therefore given a terminal
status naming what it actually is, and leaves the pending pool.

STATUSES
  parsed          real bibliographic reference; fields extracted
  relation_line   identifier + relation + gloss (a citation-graph row, not a
                  bibliography entry; the edge is already carried by
                  citation_extractor.py / extract_citations_external.py)
  legal_citation  statute, code, or case reference
  apparatus       table header, column label, or structural fragment
  prose           sentence or bio text swept in by section segmentation
  pending         resisted deterministic parse; awaits in-session judgment

BIBKEY: bib:<sha256(normalized raw)[:12]> — deterministic and reproducible.
Pre-existing bibkeys are left untouched.
"""
import json, re, hashlib, sys
from pathlib import Path
from collections import Counter

QUEUE = Path(__file__).resolve().parents[1] / "data/worklists/refsec-parse-queue.json"

YEAR = re.compile(r"\b(1[4-9]\d{2}|20[0-3]\d)\b")
DOI_RELATION = re.compile(r"^10\.\d{4,}/\S+\s+(References|Cites|IsCitedBy|Continues|IsPartOf|Requires|Extends|Supersedes|IsSupplementTo|IsVersionOf)\b", re.I)
BARE_DOI_LINE = re.compile(r"^(https?://(dx\.)?doi\.org/)?10\.\d{4,}/\S+\s*[—–-]?\s*\S")
LEGAL = re.compile(r"(\b\d+\s+U\.?S\.?C\.?\b|§|\bF\.\s?(Supp|2d|3d)\b|\bv\.\s+[A-Z]|\bNo\.\s+\d+[-–]\d+\b.*\(\d{4}\))")
APPARATUS_PREFIX = re.compile(r"^(Captured\s|Full text not yet|Recovery status|Body status|Deposit\s+#|Status:|Note:|Abstract:|Keywords:|Identifier\b|Relation\b|Description\b|Subjects?:|Version\b|License\b|Creator\b)", re.I)
APPARATUS_EXACT = {
    "identifier relation description", "identifier relation", "relation description",
    "title author year", "author title year", "references", "bibliography",
    "works cited", "notes", "sources", "citation", "citations", "doi title relation",
}
ITALIC = re.compile(r"\*[^*]{4,}\*|_[^_]{4,}_")
QUOTED = re.compile(r"[\"“][^\"”]{6,}[\"”]")
AUTHOR_LEAD = re.compile(r"^([A-Z][\w''\-]+(?:,\s*[A-Z][\w''\.\- ]+)?(?:,?\s*(?:and|&|with)\s+[A-Z][\w''\.\- ]+)*)[\.,]\s")
PAREN_YEAR = re.compile(r"^(.{3,120}?)\s*\((1[4-9]\d{2}|20[0-3]\d)\)[\.,]?\s*(.*)$")
PUBLISHER_HINT = re.compile(r"\b(Press|Verso|Routledge|Blackwell|Wiley|Springer|MIT|Harvard|Yale|Oxford|Cambridge|Chicago|Minnesota|Duke|Columbia|Princeton|Stanford|Continuum|Polity|Penguin|Norton|Vintage|Semiotext|Zone Books|PublicAffairs|NYU|Palgrave|Sage|Brill|Bloomsbury)\b")
BARE_URL = re.compile(r"^https?://\S+$")
NAV_RELATION = re.compile(r"^(IDP\s+Nav\s+Map|WG\s+Cycle|Nav\s+Map)\b.*\b[a-z_]+_(of|to|for|by|with|from)\b|\b(maps_sightings_of|traverses_to|provides_primary_text_for|anchors_to|derives_from)\b")
LIST_FRAGMENT = re.compile(r"^[-*\u2022]\s+\*{0,2}")
PROVENANCE_ROW = re.compile(r"(Reddit|share\.google|Screenshot|Ghost\s+(Banned|Locked)|Tethered|AIO\b|session transcript|account\s+u/|Medium\s+post|TikTok|Substack|Blogger|Zenodo record|capture\s+(id|ref))", re.I)
DISPLAY_FRAGMENT = re.compile(r"^\*{1,2}[^*]+\*{1,2}(\s+\*{1,2}[^*]+\*{1,2})*\s*$")
VENUE_HINT = re.compile(r"\b(Journal|Review|Quarterly|Proceedings|Transactions|Studies|Magazine|Annals|Bulletin|Critical Inquiry|New Left|boundary 2|October|Big Data & Society|Science|Nature)\b")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def bibkey(raw):
    return "bib:" + hashlib.sha256(norm(raw).lower().encode("utf-8")).hexdigest()[:12]


def classify(raw):
    s = norm(raw)
    low = s.lower().strip(" .:|—-")
    if not s:
        return "apparatus", None
    if low in APPARATUS_EXACT or (len(s.split()) <= 3 and not YEAR.search(s)):
        return "apparatus", None
    if APPARATUS_PREFIX.match(s) and not ITALIC.search(s):
        return "apparatus", None
    if BARE_URL.match(s):
        return "bare_url", None
    if NAV_RELATION.search(s):
        return "nav_relation", None
    if LIST_FRAGMENT.match(s) and not ITALIC.search(s) and not YEAR.search(s):
        return "apparatus", None
    if PROVENANCE_ROW.search(s) and not QUOTED.search(s):
        return "provenance_row", None
    if DISPLAY_FRAGMENT.match(s) and not YEAR.search(s):
        # bold/italic display text: byline blocks, epigraphs, pull quotes
        return ("prose" if len(s.split()) > 5 else "apparatus"), None
    if DOI_RELATION.match(s) or (BARE_DOI_LINE.match(s) and " References " in s):
        return "relation_line", None
    if LEGAL.search(s) and not ITALIC.search(s):
        return "legal_citation", None
    # prose: long sentence, no citation shape
    if not ITALIC.search(s) and not QUOTED.search(s) and not YEAR.search(s):
        if len(s.split()) > 6 or s.endswith((".", "!", "?")):
            return "prose", None
        return "apparatus", None
    return "reference", s


def parse_reference(s):
    """Deterministic field extraction. Conservative: returns None rather than guess."""
    authors = title = venue = year = None
    conf = 0.5
    ym = YEAR.search(s)
    if ym:
        year = ym.group(1)
        conf += 0.1
    it = ITALIC.search(s)
    q = QUOTED.search(s)
    it_text = it.group(0).strip("*_").strip() if it else None
    q_text = q.group(0).strip('"\u201c\u201d').strip().rstrip(".") if q else None

    # Standard convention: quoted = article title, italic = venue/journal or book title.
    if q_text and it_text:
        title, venue = q_text, it_text
        conf += 0.2
    elif it_text and VENUE_HINT.search(it_text) and not q_text:
        # italic is a journal name with no quoted title present: venue known, title not
        venue = it_text
        head = s[:it.start()].strip()
        am0 = AUTHOR_LEAD.match(head)
        if am0:
            rest = head[am0.end():].strip().rstrip(".,")
            if len(rest) >= 8:
                title = rest
                authors = am0.group(1).strip().rstrip(".")
                conf += 0.15
        if not title:
            return None                      # journal without a title: leave pending
    elif it_text:
        title = it_text
        conf += 0.15
    elif q_text:
        title = q_text
        conf += 0.15

    am = AUTHOR_LEAD.match(s)
    if am and not authors and (not title or not am.group(1).startswith(title[:12])):
        authors = am.group(1).strip().rstrip(".")
        conf += 0.15

    if not title:
        pm = PAREN_YEAR.match(s)
        if pm:
            authors = authors or pm.group(1).strip().rstrip(".,")
            year = year or pm.group(2)
            parts = [x.strip() for x in re.split(r"\.\s+", pm.group(3).strip()) if x.strip()]
            if parts and len(parts[0]) >= 8:
                title = parts[0].rstrip(".")
                conf += 0.15
                if len(parts) > 1:
                    venue = venue or parts[1].rstrip(".")

    if not venue:
        tail = s[it.end():] if it else s
        vm = VENUE_HINT.search(tail) or PUBLISHER_HINT.search(tail)
        if vm:
            venue = vm.group(0)
            conf += 0.05

    if not title or len(title) < 8:
        return None
    if APPARATUS_PREFIX.match(title) or title.endswith(":"):
        return None
    if not authors and not year and not venue:
        return None                          # a bare phrase is not a reference
    return {
        "authors": authors, "title": title, "venue": venue, "year": year,
        "bibkey": bibkey(s), "ontic_status": "unverified",
        "confidence": round(min(conf, 0.95), 2),
    }


def main():
    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    entries = q["entries"]
    counts = Counter()
    for e in entries:
        if e.get("status") != "pending":
            counts["already_" + str(e.get("status"))] += 1
            continue
        raw = e.get("raw", "")
        kind, s = classify(raw)
        if kind != "reference":
            e["status"] = kind
            e["triage"] = "deterministic; not a bibliographic reference"
            counts[kind] += 1
            continue
        p = parse_reference(s)
        if p is None:
            counts["pending"] += 1
            continue
        e["status"] = "parsed"
        e["parsed"] = p
        counts["parsed"] += 1
    q["pending"] = sum(1 for e in entries if e.get("status") == "pending")
    q["parsed"] = sum(1 for e in entries if e.get("status") == "parsed")
    q["dateModified"] = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    q["bibkey_convention"] = "bib:<sha256(normalized raw)[:12]>; deterministic from 2026-07-30"
    q["triage_statuses"] = {
        "parsed": "bibliographic reference, fields extracted",
        "relation_line": "identifier+relation row; edge carried by the citation graph, not bibliography",
        "legal_citation": "statute, code, or case reference",
        "apparatus": "table header, column label, or structural fragment",
        "prose": "sentence or bio text swept in by section segmentation",
        "bare_url": "URL-only entry; the edge is already carried in citation-graph-external via `url`",
        "nav_relation": "navigation-map relation row; internal graph edge, not bibliography",
        "provenance_row": "capture/provenance table row (platform, account, state, date); apparatus of the capture registry, not bibliography",
        "pending": "resisted deterministic parse; awaits in-session judgment",
    }
    QUEUE.write_text(json.dumps(q, indent=1, ensure_ascii=False), encoding="utf-8")
    print("── refsec triage/parse ──")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {k:22s} {v}")
    print(f"\n  queue now: parsed={q['parsed']} pending={q['pending']} total={len(entries)}")


if __name__ == "__main__":
    main()
