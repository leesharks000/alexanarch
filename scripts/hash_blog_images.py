#!/usr/bin/env python3
"""hash_blog_images.py — group the blog's images by what they LOOK like.

WHY THIS IS NEEDED

MANUS reports reusing generated images across long stretches of posts. By URL that
reuse is invisible: only 18 of 1,970 images appear in more than one post, 2% of
rows. The reason is Blogger — inserting the same file into a new post RE-UPLOADS it
under a fresh asset key, so an image used across thirty posts has thirty distinct
URLs and reads as thirty distinct images to any metadata-level check.

The duplication is visual, not referential, and nothing in the index can see it.
This fetches every image and computes a difference hash, so visually identical and
near-identical images collapse into one decision.

WHAT A dHASH IS AND IS NOT

Each image is reduced to greyscale at 9x8 and each pixel compared to its right
neighbour: 64 bits recording where the image gets brighter or darker. Identical
images produce identical hashes; the same image at a different SIZE or JPEG quality
produces a hash within a few bits. It is robust to rescaling and recompression,
which is exactly what Blogger does on re-upload.

It is NOT a similarity judgement about content. Two different diagrams with the
same layout can land close together. Groups formed here are candidates for one
decision, not an assertion that the images are the same work — the triage still
shows every member so a wrong grouping is visible rather than hidden.

    python3 scripts/hash_blog_images.py
    python3 scripts/hash_blog_images.py --threshold 4
"""
import argparse
import io
import json
import pathlib
import sys
import time
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
IDX = ROOT / "data" / "blog-image-index.json"
OUT = ROOT / "data" / "blog-image-hashes.json"


def dhash(im, s=8):
    im = im.convert("L").resize((s + 1, s), Image.LANCZOS)
    px = list(im.getdata())
    bits = 0
    n = 0
    for y in range(s):
        row = y * (s + 1)
        for x in range(s):
            if px[row + x] > px[row + x + 1]:
                bits |= 1 << n
            n += 1
    return bits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=int, default=3,
                    help="max differing bits to treat as the same image (0 = exact)")
    ap.add_argument("--limit", type=int, default=0, help="hash at most N this run")
    ap.add_argument("--group", action="store_true", help="group what is already hashed")
    a = ap.parse_args()

    rows = json.loads(IDX.read_text())["images"]
    part = ROOT / "data" / "blog-image-hashes.partial.json"
    if part.exists():
        st = json.loads(part.read_text())
        out, failed = st["images"], st["failed"]
    else:
        out, failed = [], []
    done = {o["src"] for o in out} | {f["src"] for f in failed}
    todo = [r for r in rows if r["src"] not in done]
    if a.limit:
        todo = todo[:a.limit]
    print(f"  {len(done):,} already hashed · {len(todo):,} this run", file=sys.stderr)
    t0 = time.time()
    for n, r in enumerate(todo, 1):
        try:
            raw = urllib.request.urlopen(
                urllib.request.Request(r["src"], headers={"User-Agent": "Mozilla/5.0"}),
                timeout=30).read()
            im = Image.open(io.BytesIO(raw))
            w, h = im.size
            out.append({"src": r["src"], "post_url": r["post_url"],
                        "post_title": r["post_title"], "post_date": r["post_date"],
                        "ordinal": r["ordinal"], "alt": r["alt"],
                        "dhash": dhash(im), "w": w, "h": h, "bytes": len(raw)})
        except Exception as e:
            failed.append({"src": r["src"], "post_url": r["post_url"],
                           "error": type(e).__name__})
        if n % 100 == 0:
            part.write_text(json.dumps({"images": out, "failed": failed}))
            print(f"  {n:,}/{len(todo):,} · {len(failed)} failed · "
                  f"{time.time() - t0:.0f}s", file=sys.stderr)
    part.write_text(json.dumps({"images": out, "failed": failed}))
    if not a.group and len(out) + len(failed) < len(rows):
        print(f"\n  partial: {len(out):,} hashed, {len(failed)} failed, "
              f"{len(rows) - len(out) - len(failed):,} remaining. Run again to continue.")
        return 0

    # group by hamming distance — union-find over the threshold
    parent = list(range(len(out)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        a_, b_ = find(i), find(j)
        if a_ != b_:
            parent[b_] = a_

    # exact matches first (cheap), then near-matches within the threshold
    exact = {}
    for i, o in enumerate(out):
        exact.setdefault(o["dhash"], []).append(i)
    for members in exact.values():
        for j in members[1:]:
            union(members[0], j)
    if a.threshold:
        keys = list(exact)
        for x in range(len(keys)):
            for y in range(x + 1, len(keys)):
                if bin(keys[x] ^ keys[y]).count("1") <= a.threshold:
                    union(exact[keys[x]][0], exact[keys[y]][0])

    groups = {}
    for i in range(len(out)):
        groups.setdefault(find(i), []).append(i)

    ordered = sorted(groups.values(), key=len, reverse=True)
    for gid, members in enumerate(ordered):
        for i in members:
            out[i]["group"] = gid
            out[i]["group_size"] = len(members)

    multi = [g for g in ordered if len(g) > 1]
    OUT.write_text(json.dumps({
        "built": "2026-08-09",
        "method": "dhash 8x8, union-find over hamming distance",
        "threshold_bits": a.threshold,
        "images_hashed": len(out),
        "fetch_failures": len(failed),
        "distinct_groups": len(ordered),
        "groups_with_more_than_one": len(multi),
        "rows_collapsed": sum(len(g) - 1 for g in multi),
        "note": ("A group is a candidate for ONE classification decision, not an assertion "
                 "that its members are the same work. The triage shows every member."),
        "failed": failed,
        "images": out,
    }, ensure_ascii=False), encoding="utf-8")

    print(f"\n  hashed {len(out):,} of {len(rows):,} ({len(failed)} failed)")
    print(f"  distinct visual groups: {len(ordered):,}")
    print(f"  groups with more than one member: {len(multi):,}")
    print(f"  decisions saved by grouping: {sum(len(g) - 1 for g in multi):,}")
    if multi:
        print("\n  largest groups:")
        for g in ordered[:6]:
            if len(g) < 2:
                break
            o = out[g[0]]
            print(f"    {len(g):>4} copies  {o['post_date']}…  {o['src'][-42:]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
