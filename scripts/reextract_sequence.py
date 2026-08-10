#!/usr/bin/env python3
"""reextract_sequence.py — repair the line breaks in the TLL sequence deposits.

THE DEFECT

The original extraction did `re.sub(r'<[^>]+>', '\\n', html)` — every tag became a
newline, INCLUDING INLINE ONES. So `<b>It is</b> an <i>ontological recursion</i>`
became three lines, and every sentence containing emphasis, a link, or a span was
shattered at each tag boundary. #1442 rendered 750 fragmented paragraphs: "It is an",
"ontological recursion", "It is", "structure catching up to pattern".

Same class as the frontmatter regex that ate 25,023 characters and the decimal point
that broke the forensics strip: a pattern written against how markup LOOKS rather
than what it MEANS.

THE FIX

Block-level elements end a line. Inline elements do not — they vanish, leaving their
text in place. `<br>` ends a line because that is what it is for.

THE GUARD

The repair must change whitespace and nothing else. Word content is compared before
and after: the same words, in the same order, with the same multiplicity. A
transcription repair that alters a word is not a repair.

    python3 scripts/reextract_sequence.py --check
    python3 scripts/reextract_sequence.py --apply
"""
import argparse
import html as htmlmod
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOCK = ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "blockquote",
         "pre", "section", "article", "ul", "ol", "table", "figure", "figcaption",
         "hr", "br")
BLOCK_RE = re.compile(r"</?(" + "|".join(BLOCK) + r")\b[^>]*>", re.I)
ANY_TAG = re.compile(r"<[^>]+>")


def extract(post_html):
    """Block tags break lines; inline tags disappear without breaking anything."""
    s = re.sub(r"<(script|style)\b.*?</\1>", " ", post_html, flags=re.S | re.I)
    s = BLOCK_RE.sub("\n", s)          # block boundaries become line breaks
    s = ANY_TAG.sub("", s)             # inline tags vanish, text stays put
    s = htmlmod.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def words(t):
    return re.findall(r"[0-9A-Za-z\u00c0-\u024f']+", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    seq = ROOT / "data/artifacts/tll-origin/sequence"
    src = ROOT / "data/artifacts/tll-origin/source"
    total_before = total_after = 0
    mismatched = []

    for d in (seq, src):
        for h in sorted(d.glob("*.html")):
            t = h.with_suffix(".txt")
            if not t.exists():
                continue
            raw = h.read_text(errors="replace")
            m = re.search(r"<div class=['\"]post-body[^>]*>(.*?)</div>\s*"
                          r"<div class=['\"]post-footer", raw, re.S)
            if not m:
                continue
            new = extract(m.group(1))
            old = t.read_text(errors="replace")

            wo, wn = words(old), words(new)
            if wo != wn:
                # the old extraction sometimes split a word across a tag boundary;
                # compare the concatenation to be certain nothing is lost
                if "".join(wo).lower() != "".join(wn).lower():
                    mismatched.append((t.name, len(wo), len(wn)))
                    continue

            frag_before = sum(1 for l in old.split("\n")
                              if l.strip() and len(l) < 95 and l.rstrip()[-1:].isalpha())
            frag_after = sum(1 for l in new.split("\n")
                             if l.strip() and len(l) < 95 and l.rstrip()[-1:].isalpha())
            total_before += frag_before
            total_after += frag_after
            if a.apply:
                t.write_text(new, encoding="utf-8")

    print(f"  fragmented lines: {total_before:,} → {total_after:,}")
    print(f"  files whose words did not survive: {len(mismatched)}")
    for n, x, y in mismatched[:6]:
        print(f"     {n}: {x} words → {y}")
    print(f"\n{'APPLIED' if a.apply else 'CHECK ONLY'}")
    return 1 if mismatched else 0


if __name__ == "__main__":
    sys.exit(main())
