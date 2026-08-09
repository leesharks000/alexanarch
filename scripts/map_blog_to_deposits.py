#!/usr/bin/env python3
"""map_blog_to_deposits.py — provisional blog-post ↔ deposit mapping, 2026 onward.

SCOPE, as ruled by MANUS: posts published 2026-01-01 or later. That is when Zenodo
depositing began, so from that date almost every post should correspond to a record.
The 1,734 posts before it are a different corpus and are not in scope.

EVERY PAIRING IN THIS FILE IS PROVISIONAL. Not one has been read. The status field
on each entry says so, and nothing downstream may treat a provisional pairing as a
finding. Promotion to `confirmed` requires a human — or an agent acting as one —
to open the post, open the record, and compare the works. Grep is not reading.

WHY THE WARNING IS THIS LOUD
Earlier today a matcher of exactly this kind reported that 34% of 2026 posts had no
deposit. The real figure was 3%, and most of that was punctuation: a colon, an EA-
prefix, a version string, an `r.25` room number. The number was wrong by a factor
of ten and was reported as a finding about the archive when the fault was in the
tool. A second script replaced ten deposited bodies on the strength of a guard that
had never been tested, and had to be reverted in full.

So this script does three things differently:

  1. It VALIDATES ITSELF FIRST against hand-checked pairs and refuses to write the
     mapping if it does not reproduce them. An instrument that cannot recover known
     answers has no business producing unknown ones.

  2. It writes `status: provisional` on every entry, with `read: false`, and records
     what evidence would settle each case.

  3. It reports its own confidence band per pairing rather than a single number, so
     the weak ones are visible instead of averaged away.

    python3 scripts/map_blog_to_deposits.py --validate
    python3 scripts/map_blog_to_deposits.py --build
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "blog-index.json"
OUT = ROOT / "data" / "blog-deposit-map.json"
EPOCH = "2026-01-01"

STOP = {"the", "and", "for", "with", "from", "that", "this", "not", "are", "was", "its",
        "their", "into", "onto", "than", "then", "when", "what", "which", "a", "of", "in",
        "on", "to", "as", "by", "an", "is"}
PRE = re.compile(r"^\s*(EA-[A-Z0-9-]+(\s+v?\d+(\.\d+)*)?[:\-\u2013\u2014]\s*|r\.\d+\s+|"
                 r"Document \d+[:]?\s*|Crimson Hexagon[:]\s*|TL;DR:\d+\s*[\u2014-]\s*|"
                 r"title:\s*[\"'])", re.I)
SUF = re.compile(r"\s*[\u2014\u2013|-]{1,2}\s*(crimson hexagon(al)? archive|alexanarch|"
                 r"new human( 2)?)\s*$", re.I)


def norm(t):
    t = re.sub(r"\[[^\]]*\]", " ", t or "")
    for _ in range(3):
        t = PRE.sub("", t.strip())
    for _ in range(3):
        t = SUF.sub("", t.strip())
    t = re.sub(r"\bv\d+(\.\d+)*\b", "", t, flags=re.I)
    t = re.sub(r"10\.5281/zenodo\.\d+", "", t)
    return " ".join(re.sub(r"[^0-9a-z' ]", " ", t.lower()).split())


def toks(t):
    return {w for w in norm(t).split() if len(w) > 2 and w not in STOP}


def load():
    posts = json.loads(INDEX.read_text())["posts"]
    posts = [p for p in posts if p.get("published", "") >= EPOCH]
    reg = json.loads((ROOT / "data/registry.json").read_text())["deposits"]
    dep = [(d["deposit_number"], toks(d.get("title", "")), d.get("title", ""))
           for d in reg]
    return posts, [d for d in dep if d[1]]


def best_match(title, dep):
    pt = toks(title)
    if not pt:
        return None, 0.0, None
    top = (None, 0.0, None)
    second = 0.0
    for n, dt, dtitle in dep:
        # Symmetric coverage lets an EA-prefixed deposit title meet a bare blog
        # headline. But dividing by the SHORTER title makes a near-empty token set
        # match everything: a sample of ten found #1410, whose title is Japanese and
        # normalises to almost no ASCII, matching a French-titled post at 1.00, and
        # #937 "Gw.TACHYON" — one token — matching any post containing that word.
        # A title with fewer than three usable tokens carries too little to identify
        # a work, so it must match on the FULL set, not on the intersection of a
        # stub.
        denom = min(len(pt), len(dt))
        if denom < 3:
            cov = len(pt & dt) / max(len(pt), len(dt))
        else:
            cov = len(pt & dt) / denom
        if cov > top[1]:
            second = top[1]
            top = (n, cov, dtitle)
        elif cov > second:
            second = cov
    return top[0], top[1], (top[2], second)


# Pairs established by opening both sides earlier today. The matcher must recover
# these, and must NOT invent a deposit for the two known-absent works.
VALIDATION = [
    ("THE BOTANICAL EFFECTIVE ACT Extending Semantic Labor Recognition to Plants", 37),
    ("The Endogenous Sophon: Disciplinary Inversion and the Double Enclosure in", 934),
    ("r.25 THE UNDERWATER CONSTRUCTION AUTHORITY (DOLPHINDIANA) Room Specificati", 566),
    ("CERN's Destruction of the Crimson Hexagon: An Erratum for a Work Whose Mat", 1426),
    ("THE THOUSAND DOLLAR SHARPIE Signature as Compressed Portraiture on U.S. Cu", 612),
    ('title: "Institute for Diagrammatic Poetics: Institutional Charter" documen', 321),
    ("Witness 1 \u2014 TECHNE / Kimi-K2 (i): Formal Mechanism Enumeration Substrate p", None),
    ("Sign the Strike A signature surface that makes no claim about who assented", None),
]
THRESHOLD = 0.75


def validate(dep, quiet=False):
    ok = 0
    for title, expect in VALIDATION:
        n, cov, _ = best_match(title, dep)
        got = n if cov >= THRESHOLD else None
        hit = got == expect
        ok += hit
        if not quiet:
            print(f"  {'OK  ' if hit else 'MISS'} expect {str(expect):<6} got {str(got):<6} "
                  f"cov {cov:.2f}  {title[:48]}")
    return ok, len(VALIDATION)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    posts, dep = load()

    if a.validate or a.build:
        ok, total = validate(dep, quiet=a.build)
        if a.build and ok < total:
            print(f"REFUSING TO BUILD: matcher scores {ok}/{total} on hand-checked pairs. "
                  f"An instrument that cannot recover known answers may not produce unknown "
                  f"ones.", file=sys.stderr)
            return 1
        if a.validate:
            print(f"\n{ok}/{total} correct")
            if not a.build:
                return 0 if ok == total else 1

    entries, unmapped = [], []
    for p in posts:
        n, cov, extra = best_match(p["title"], dep)
        dtitle, second = (extra or ("", 0.0))
        if cov >= THRESHOLD:
            band = ("strong" if cov >= 0.95 else "good" if cov >= 0.85 else "weak")
            entries.append({
                "post_title": p["title"][:220], "post_url": p["url"],
                "published": p["published"], "post_chars": p["chars"],
                "deposit_number": n, "deposit_title": dtitle[:220],
                "title_coverage": round(cov, 3),
                "margin_over_runner_up": round(cov - second, 3),
                "confidence_band": band,
                "status": "provisional", "read": False,
                "settles_it": ("Open the post and the record and compare the works. A shared "
                               "DOI in both bodies, or a shared document ID or hex coordinate, "
                               "settles it outright; a title alone does not."),
            })
        else:
            unmapped.append({"post_title": p["title"][:220], "post_url": p["url"],
                             "published": p["published"], "post_chars": p["chars"],
                             "closest_deposit": n, "closest_coverage": round(cov, 3),
                             "status": "no_deposit_found", "read": False})

    bands = {b: sum(1 for e in entries if e["confidence_band"] == b)
             for b in ("strong", "good", "weak")}
    OUT.write_text(json.dumps({
        "generated": "2026-08-08",
        "scope": f"blog posts published {EPOCH} or later \u2014 the Zenodo-deposit era",
        "posts_in_scope": len(posts),
        "mapped": len(entries), "unmapped": len(unmapped),
        "confidence_bands": bands,
        "status_of_every_entry": "provisional",
        "warning": ("NOT ONE PAIRING IN THIS FILE HAS BEEN READ. Every entry is a nomination "
                    "produced by title comparison. Promotion to confirmed requires opening the "
                    "post and the record and comparing the works; grep is not reading. Earlier "
                    "on the day this was generated, a matcher of this kind reported that 34% of "
                    "2026 posts had no deposit when the true figure was 3%, the difference being "
                    "punctuation. Treat every line here as a question."),
        "validation": {"pairs": len(VALIDATION),
                       "note": "The matcher reproduces all hand-checked pairs; the build "
                               "refuses to run otherwise."},
        "entries": entries, "unmapped_posts": unmapped,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\nscope: posts from {EPOCH} onward  ({len(posts):,})")
    print(f"  provisionally mapped : {len(entries):,}")
    print(f"     strong (>=0.95)   : {bands['strong']:,}")
    print(f"     good   (>=0.85)   : {bands['good']:,}")
    print(f"     weak   (>=0.75)   : {bands['weak']:,}   <- read these first")
    print(f"  no deposit found     : {len(unmapped):,}")
    print(f"\nwritten to {OUT}  (every entry status=provisional, read=false)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
