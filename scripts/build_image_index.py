#!/usr/bin/env python3
"""build_image_index.py — every image on the authorial blog, tagged to its post.

The blog index built earlier stripped HTML to plain text, so image markup did not
survive it. This re-reads the Blogger feed with markup intact and records, for each
image: its source URL, the post that carries it, the post's date and title, its
ordinal position in the post, its alt text, and whatever caption or nearby text
Blogger wrapped it in.

Pagination advances by entries RETURNED, not by page size requested. Blogger
truncates the feed by response weight: a request for 500 posts with full content
comes back with 43 to 86 of them, and stepping the cursor by 500 silently skips
most of the corpus — the first blog index built that way covered 574 of 2,809 posts
and reported success.

    python3 scripts/build_image_index.py
"""
import html as htmlmod
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "blog-image-index.json"
FEED = ("https://mindcontrolpoems.blogspot.com/feeds/posts/default"
        "?alt=json&max-results=500&start-index={i}")

IMG = re.compile(r"<img\b[^>]*>", re.I)
ATTR = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
# Blogger wraps images in an <a> to the full-size original; that href is the
# better source than the thumbnail in src.
ANCHORED = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>\s*(<img\b[^>]*>)', re.I)


def fetch(i):
    req = urllib.request.Request(FEED.format(i=i), headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=90))["feed"]


def images_in(raw_html, post):
    """Every <img> in document order, with its full-size href when Blogger provides one."""
    full_for = {}
    for m in ANCHORED.finditer(raw_html):
        full_for[m.group(2)] = m.group(1)

    out = []
    for n, m in enumerate(IMG.finditer(raw_html), 1):
        tag = m.group(0)
        attrs = dict(ATTR.findall(tag))
        src = attrs.get("src", "")
        if not src:
            continue
        full = full_for.get(tag, "")
        # text immediately after the image often carries Blogger's caption
        after = htmlmod.unescape(re.sub(r"<[^>]+>", " ", raw_html[m.end():m.end() + 220]))
        after = re.sub(r"\s+", " ", after).strip()
        out.append({
            "src": src,
            "full": full if full and full != src else "",
            "alt": htmlmod.unescape(attrs.get("alt", "")).strip(),
            "title_attr": htmlmod.unescape(attrs.get("title", "")).strip(),
            "width": attrs.get("width", ""),
            "height": attrs.get("height", ""),
            "ordinal": n,
            "caption_hint": after[:180],
            "post_url": post["url"],
            "post_title": post["title"],
            "post_date": post["published"],
        })
    return out


def main():
    posts, images, i, total = 0, [], 1, None
    while True:
        feed = fetch(i)
        if total is None:
            total = int(feed["openSearch$totalResults"]["$t"])
            print(f"  blog reports {total:,} posts", file=sys.stderr)
        entries = feed.get("entry") or []
        if not entries:
            break
        for e in entries:
            url = next((l["href"] for l in e.get("link", []) if l.get("rel") == "alternate"), "")
            post = {
                "url": url,
                "title": htmlmod.unescape(e["title"]["$t"]).strip(),
                "published": e.get("published", {}).get("$t", "")[:10],
            }
            raw = e.get("content", {}).get("$t", "")
            images.extend(images_in(raw, post))
            posts += 1
        i += len(entries)
        if posts % 400 < len(entries):
            print(f"  {posts:,}/{total:,} posts · {len(images):,} images", file=sys.stderr)
        if i > total:
            break

    # de-duplicate on (src, post_url): the same image repeated in one post is one row
    seen, rows = set(), []
    for im in images:
        k = (im["src"], im["post_url"])
        if k in seen:
            continue
        seen.add(k)
        rows.append(im)

    with_img = len({r["post_url"] for r in rows})
    OUT.write_text(json.dumps({
        "source": "https://mindcontrolpoems.blogspot.com/",
        "built": "2026-08-09",
        "posts_scanned": posts,
        "posts_reported_by_blog": total,
        "complete": posts >= total * 0.98,
        "posts_with_images": with_img,
        "image_count": len(rows),
        "purpose": ("Triage surface for separating machine-generated images and visual schemas "
                    "from photographs, scans, handwriting and other analog artifacts. "
                    "Classification is recorded by MANUS, not inferred here."),
        "images": rows,
    }, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(rows):,} images across {with_img:,} of {posts:,} posts -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
