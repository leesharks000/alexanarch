#!/usr/bin/env python3
"""index_blog.py — build and search a complete local index of the authorial blog.

WHY THIS EXISTS, STATED PLAINLY
Every restoration pass over this corpus guessed. It took a deposit title, derived
a candidate URL from it, fetched that one URL, and scored the result against a
threshold. When the guess was wrong the work was recorded as unrecoverable. When
the guess was right but the title had drifted, the gate rejected it anyway.

Nobody indexed the blog. The Blogger feed at /feeds/posts/default enumerates every
post with its full content, 500 at a time, and has done so throughout. 2,800+
posts, title and body, fetchable in a few minutes. MANUS found records by hand,
one at a time, that this index finds in milliseconds.

MEASURED FAILURES THIS REPLACES

  #1287  LLM Hallucination Incident Report. The correct post was FOUND and scored
         head_containment 0.43 against a 0.75 gate, because the queue's truth title
         carried the work's DOI — 18368527, 5281, zenodo — and the blog post
         PREDATES THE DEPOSIT BY FIVE WEEKS and therefore cannot cite it.

  #1272  Integrity-Coherence Audit. The correct URL sat in the queue's
         candidate_blog_urls field while the matcher scored six different URLs.
         head_containment 0.67, and the three absent tokens were "crimson",
         "hexagon", "archive" — the platform suffix that this archive's own W11
         title-hygiene rule declares is NOT part of a work title.

Both are one root cause: THE GATE MEASURED THE DEPOSIT'S METADATA AGAINST THE WORK.
A title carrying a DOI is a citation. A title carrying a publication surface is an
imprint line. Neither is what the author wrote at the top of the page.

WHAT THIS DOES INSTEAD
Indexes every post once. Searches title AND body. Normalises away DOIs, platform
suffixes and version strings before comparing. Returns ranked candidates with the
evidence for a human to read, and never asserts a match.

    python3 scripts/index_blog.py --build
    python3 scripts/index_blog.py --search "integrity coherence audit"
    python3 scripts/index_blog.py --find-missing        # every capture record at once
"""
import argparse, html, json, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "blog-index.json"
FEED = ("https://mindcontrolpoems.blogspot.com/feeds/posts/default"
        "?alt=json&max-results=500&start-index={i}")

# Noise the deposit title carries and the authorial page never does.
SUFFIX = re.compile(
    r"\s*[\u2014\u2013|\-]{1,2}\s*(crimson hexagon(al)? archive|alexanarch|"
    r"new human( 2)?|pergamon press|semantic economy institute)\s*$", re.I)
DOI = re.compile(r"\b(10\.5281|zenodo|doi)\b[^\s]*", re.I)
VER = re.compile(r"\bv\d+(\.\d+)*\b", re.I)
BRACKET = re.compile(r"\[[^\]]*\]")


def norm(t):
    t = BRACKET.sub(" ", t or "")
    t = DOI.sub(" ", t)
    t = VER.sub(" ", t)
    for _ in range(3):
        t = SUFFIX.sub("", t.strip())
    t = t.lower().replace("\u2014", " ").replace("\u2013", " ").replace("\u00a0", " ")
    return " ".join(re.sub(r"[^0-9a-z ]", " ", t).split())


def toks(t):
    return {w for w in norm(t).split() if len(w) > 3}


def build():
    # PAGINATE BY WHAT CAME BACK, NOT BY WHAT WAS ASKED FOR. Blogger truncates the
    # feed by RESPONSE SIZE rather than entry count: a request for 500 posts with
    # full content returns 43 to 86 of them. Advancing the cursor by the requested
    # page size therefore skips most of the blog silently — the first run of this
    # script indexed 574 of 2,809 posts and reported success, which is the same
    # class of error it was written to fix.
    posts, i, total = [], 1, None
    while True:
        req = urllib.request.Request(FEED.format(i=i),
                                     headers={"User-Agent": "Mozilla/5.0"})
        feed = json.load(urllib.request.urlopen(req, timeout=90))["feed"]
        if total is None:
            total = int(feed["openSearch$totalResults"]["$t"])
            print(f"  blog reports {total:,} posts", file=sys.stderr)
        entries = feed.get("entry") or []
        if not entries:
            break
        for e in entries:
            url = next((l["href"] for l in e.get("link", []) if l.get("rel") == "alternate"), "")
            raw = e.get("content", {}).get("$t", "")
            text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
            posts.append({
                "title": html.unescape(e["title"]["$t"]).strip(),
                "url": url,
                "published": e.get("published", {}).get("$t", "")[:10],
                "chars": len(re.sub(r"\s+", " ", text)),
                "text": re.sub(r"\s+", " ", text).strip()[:4000],
            })
        i += len(entries)
        if len(posts) % 400 < len(entries):
            print(f"  {len(posts):,} / {total:,}", file=sys.stderr)
        if i > total:
            break
    INDEX.write_text(json.dumps(
        {"source": "https://mindcontrolpoems.blogspot.com/",
         "note": ("Complete post index built from the Blogger JSON feed, which enumerates "
                  "every post with its content and has done so throughout. Every restoration "
                  "pass before 2026-08-08 guessed a URL from a deposit title instead."),
         "count": len(posts), "blog_reports": total,
         "complete": len(posts) >= total * 0.98, "posts": posts}, ensure_ascii=False), encoding="utf-8")
    print(f"indexed {len(posts)} posts -> {INDEX}")
    return 0


def load():
    if not INDEX.exists():
        print("no index; run --build first", file=sys.stderr)
        sys.exit(2)
    return json.loads(INDEX.read_text(encoding="utf-8"))["posts"]


def score(q_toks, p):
    """Title containment first — the author's own headline is the strongest signal —
    with body containment as the fallback a title-only gate never had."""
    t_toks = toks(p["title"])
    if not t_toks:
        return 0.0, 0.0
    tc = sum(1 for w in q_toks if w in t_toks) / max(1, len(q_toks))
    body = norm(p["text"][:2500])
    bc = sum(1 for w in q_toks if w in body) / max(1, len(q_toks))
    return tc, bc


def search(query, posts, k=6):
    q = toks(query)
    out = []
    for p in posts:
        tc, bc = score(q, p)
        s = max(tc, bc * 0.85)
        if s >= 0.5:
            out.append((round(s, 2), round(tc, 2), round(bc, 2), p))
    out.sort(key=lambda r: -r[0])
    return out[:k]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--search")
    ap.add_argument("--find-missing", action="store_true")
    a = ap.parse_args()

    if a.build:
        return build()

    posts = load()

    if a.search:
        for s, tc, bc, p in search(a.search, posts):
            print(f"  {s:.2f}  title {tc:.2f} body {bc:.2f}  {p['published']}  "
                  f"{p['title'][:62]}")
            print(f"        {p['url']}")
        return 0

    if a.find_missing:
        reg = json.loads((ROOT / "data/registry.json").read_text())["deposits"]
        caps = [d for d in reg
                if (d.get("body_status") or {}).get("class") == "metadata_capture"]
        print(f"searching {len(posts):,} indexed posts for {len(caps)} capture records\n")
        hits = 0
        for d in caps:
            res = search(d.get("title", ""), posts, k=1)
            if res and res[0][0] >= 0.7:
                hits += 1
                s, tc, bc, p = res[0]
                print(f"  #{d['deposit_number']:<6} {s:.2f}  {d.get('title','')[:44]}")
                print(f"         -> {p['url']}")
        print(f"\n{hits} of {len(caps)} capture records have a strong blog candidate.")
        print("None is a finding. Each is a post to open and read.")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
