#!/usr/bin/env python3
"""pdf_to_markdown.py — faithful PDF → markdown for deposit seating.

WHY THIS EXISTS (MANUS finding 2026-08-04, #1327): seating raw `pdftotext`
output writes the EXTRACTOR'S hard wraps into the deposit body. The renderer
then treats every ~70-character wrap as its own paragraph, headings lose
heading status, and words split across line breaks ("Inter-\nvention") survive
into the archive. The line breaks in a PDF text dump are an artifact of page
geometry, not of the work.

WHAT THIS DOES
  1. De-hyphenates across line breaks (Inter-\nvention -> Intervention),
     protecting genuine hyphenated compounds (Mathematic-Semantic).
  2. Reflows hard-wrapped PROSE into real paragraphs, joining continuation
     lines and breaking on blank lines.
  3. Detects headings — ALL-CAPS lines, roman/decimal section numbers, short
     lines followed by blank — and emits markdown headings.
  4. LEAVES VERSE AND INDENTED BLOCKS ALONE. A line that is short, indented,
     or sits in a run of short lines is prosodic structure, not a wrap.
     Reflowing verse would destroy lineation — the Day and Night lesson.
  5. Strips running heads/folios (repeated page furniture, bare page numbers).

Usage: pdf_to_markdown.py IN.pdf [OUT.md]
"""
import re
import subprocess
import sys
from collections import Counter

WRAP_BAND = (45, 95)          # a prose wrap lands in this width band
SHORT = 45                     # lines this short are probably not wraps


def extract(pdf_path):
    r = subprocess.run(['pdftotext', '-layout', pdf_path, '-'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f'pdftotext failed: {r.stderr[:200]}')
    return r.stdout


def strip_furniture(lines):
    """Remove bare page numbers and running heads repeated across pages."""
    counts = Counter(l.strip() for l in lines if 3 < len(l.strip()) < 60)
    repeated = {t for t, c in counts.items() if c >= 4}
    out = []
    for l in lines:
        s = l.strip()
        if re.fullmatch(r'\d{1,3}', s):
            continue
        if s in repeated and not re.search(r'[.:;,]$', s) and len(s.split()) <= 8:
            continue
        out.append(l)
    return out


def is_heading(s, nxt_blank):
    t = s.strip()
    if not t or len(t) > 90:
        return False
    letters = [c for c in t if c.isalpha()]
    allcaps = letters and sum(c.isupper() for c in letters) / len(letters) > 0.85
    numbered = bool(re.match(r'^(?:§?\s*[IVXLC]+\.|§?\s*\d+(?:\.\d+)*\.?)\s+\S', t))
    if allcaps and len(t.split()) <= 14:
        return True
    if numbered and nxt_blank:
        return True
    if numbered and len(t) < 70:
        return True
    # Title-case short line with no terminal punctuation, followed by blank:
    # section headings like "The Borromean Binding".
    if (nxt_blank and len(t) < 60 and not re.search(r'[.,;:?!]$', t)
            and 2 <= len(t.split()) <= 9):
        words = [w for w in t.split() if w[:1].isalpha()]
        if words and sum(1 for w in words if w[:1].isupper()) / len(words) >= 0.6:
            return True
    return False


def dehyphenate(a, b):
    """Join a line ending in '-' with the next, if it is a true wrap-break."""
    m = re.search(r'([A-Za-z]{2,})-$', a)
    if not m:
        return None
    nxt = b.lstrip()
    if not nxt or not nxt[0].islower():
        return None          # next word capitalised: likely a real compound
    return a[: m.start(1)] + m.group(1) + nxt


def looks_like_verse(block):
    """A run whose lines are mostly short or indented is prosody, not wrapping."""
    ls = [l for l in block if l.strip()]
    if len(ls) < 2:
        return False
    short = sum(1 for l in ls if len(l.strip()) < SHORT) / len(ls)
    indented = sum(1 for l in ls if l[:1] in (' ', '\t')) / len(ls)
    return short > 0.6 or indented > 0.6


def convert(text):
    # Normalize PDF hyphen variants BEFORE anything else: U+2010 HYPHEN,
    # U+2011 NON-BREAKING HYPHEN and U+00AD SOFT HYPHEN all appear as
    # line-break hyphens in pdftotext output and defeat an ASCII-only regex
    # (the "Inter‐ vention" defect, MANUS screenshot 2026-08-04).
    text = text.replace('\u00ad', '').replace('\u2010', '-').replace('\u2011', '-')
    # pdftotext -layout often renders a wrap-break as "word- continuation"
    # on ONE line; rejoin those before block analysis.
    text = re.sub(r'([A-Za-z]{2,})-\s+([a-z])', r'\1\2', text)
    lines = strip_furniture(text.split('\n'))

    # group into blocks separated by blank lines
    blocks, cur = [], []
    for l in lines:
        if l.strip():
            cur.append(l)
        else:
            if cur:
                blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)

    out = []
    for blk in blocks:
        # single-line block that reads as a heading
        if len(blk) == 1 and is_heading(blk[0], True):
            t = blk[0].strip()
            level = '##' if t.isupper() and len(t.split()) <= 8 else '###'
            out.append(f'{level} {t}')
            continue
        if looks_like_verse(blk):
            out.append('\n'.join(l.rstrip() for l in blk))   # preserve as-is
            continue
        # prose: reflow, de-hyphenating across wraps
        para, buf = [], ''
        for i, l in enumerate(blk):
            s = l.strip()
            if is_heading(l, i + 1 >= len(blk) or not blk[i + 1].strip()):
                if buf:
                    para.append(buf); buf = ''
                t = s
                level = '##' if t.isupper() and len(t.split()) <= 8 else '###'
                para.append(f'{level} {t}')
                continue
            if not buf:
                buf = s
                continue
            joined = dehyphenate(buf, s)
            if joined is not None:
                buf = joined
            elif len(buf) >= WRAP_BAND[0]:
                buf = buf + ' ' + s          # continuation of a wrapped line
            else:
                para.append(buf); buf = s    # short line: treat as its own unit
        if buf:
            para.append(buf)
        out.append('\n\n'.join(para))

    md = '\n\n'.join(out)
    md = re.sub(r'\n{4,}', '\n\n\n', md)
    md = re.sub(r'[ \t]+\n', '\n', md)
    return md.strip() + '\n'


def main():
    src = sys.argv[1]
    md = convert(extract(src))
    if len(sys.argv) > 2:
        open(sys.argv[2], 'w').write(md)
        print(f'wrote {sys.argv[2]} ({len(md):,} chars)')
    else:
        sys.stdout.write(md)


if __name__ == '__main__':
    main()
