#!/usr/bin/env python3
"""render_pearl_machine_text.py — machine-facing Pearl and Other Poems from PDF geometry.

The 2014 book (AXN:0472 attachment) is born-digital but its text stream embeds
tab+CR after every word — a composition artifact that wrecks flow-based
extraction, which is why earlier attempts lost the whitespace. This renderer
ignores text flow entirely: it takes per-word bounding boxes and re-renders
each page onto a character grid, so horizontal indentation and vertical field
both survive at character resolution. The page is a field, not a container;
the grid is the field made portable.

Calibration: char cell 5.07pt (document median); line pitch measured per page
(default 13pt); left anchor resolved per page against the book's two mirrored
margin classes (36pt / 43pt) so recto and verso indent identically.

Output: data/attachments/AXN-0472/pearl-and-other-poems-machine-text.txt
The PDF remains the artwork; this is the score, at fidelity.
"""
import pdfplumber, statistics, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data/attachments/AXN-0472/pearl-and-other-poems-2014.pdf"
OUT = ROOT / "data/attachments/AXN-0472/pearl-and-other-poems-machine-text.txt"
CHAR_W = 5.07
ANCHORS = (36.0, 43.0)
TOP_TRIM = 36.0  # uniform top margin; a poem dropped down the page keeps its drop


def clean(t):
    t = t.replace("\t", "").replace("\r", "").replace("\xa0", " ")
    t = t.replace("\u00ad", "").replace("\u2010", "-").replace("\u2011", "-")
    while "--" in t:
        t = t.replace("--", "-")
    return t.strip()


def render_page(page, pitch):
    words = []
    for w in page.extract_words(use_text_flow=False, keep_blank_chars=False):
        t = clean(w["text"])
        if t:
            words.append((w["top"], w["x0"], w["x1"], t))
    if not words:
        return ""
    # left anchor: nearest mirrored margin class if present, else page min
    xs = [x0 for _, x0, _, _ in words]
    anchor = min(xs)
    for a in ANCHORS:
        if any(abs(x - a) <= 2.5 for x in xs):
            anchor = a
            break
    # cluster into lines by top coordinate
    words.sort(key=lambda w: (w[0], w[1]))
    lines, cur, cur_top = [], [], None
    for top, x0, x1, t in words:
        if cur_top is None or abs(top - cur_top) <= 2.5:
            cur.append((x0, x1, t))
            cur_top = top if cur_top is None else min(cur_top, top)
        else:
            lines.append((cur_top, cur))
            cur, cur_top = [(x0, x1, t)], top
    lines.append((cur_top, cur))
    # place lines at rows; render each line as a character raster
    # snap runs of near-equal consecutive gaps to their run median, so a
    # uniform leading never straddles a rounding boundary mid-stanza
    gaps = [b - a for (a, _), (b, _) in zip(lines, lines[1:])]
    snapped, i = list(gaps), 0
    while i < len(gaps):
        j = i
        while j + 1 < len(gaps) and abs(gaps[j + 1] - gaps[i]) < 2.5:
            j += 1
        med = statistics.median(gaps[i:j + 1])
        for k in range(i, j + 1):
            snapped[k] = med
        i = j + 1
    out_rows = {}
    prev_row = None
    for idx, (top, ws) in enumerate(lines):
        if prev_row is None:
            row = max(0, round((top - TOP_TRIM) / pitch))
        else:
            row = prev_row + max(1, round(snapped[idx - 1] / pitch))
        prev_row = row
        while row in out_rows:
            row += 1  # two clusters landing on one row: keep both, adjacent
        buf = ""
        prev_x1 = None
        for x0, x1, t in sorted(ws):
            if prev_x1 is None:
                col = max(0, round((x0 - anchor) / CHAR_W))
                buf = " " * col + t
            else:
                gap = x0 - prev_x1
                n = 1 if gap < 1.9 * CHAR_W else max(2, round(gap / CHAR_W))
                buf += " " * n + t
            prev_x1 = x1
        out_rows[row] = buf.rstrip()
    n = max(out_rows) + 1
    return "\n".join(out_rows.get(r, "") for r in range(n))


def main():
    pdf = pdfplumber.open(SRC)
    # global body pitch: single-line steps only (9-17pt band), document-wide
    gaps = []
    for page in pdf.pages:
        tops = sorted({round(w["top"], 1) for w in page.extract_words()})
        gaps += [b - a for a, b in zip(tops, tops[1:]) if 9 < b - a < 17]
    pitch = statistics.median(gaps) if gaps else 13.0
    pages = []
    for i, page in enumerate(pdf.pages, 1):
        body = render_page(page, pitch)
        pages.append(f"· · ·  page {i}  · · ·\n\n{body}".rstrip())
    header = """PEARL AND OTHER POEMS — machine-facing text at whitespace fidelity
Lee Sharks · New Human Press · 2014 · ISBN 978-0692313077
Canonical deposit: #1121 · AXN:0472 · https://www.alexanarch.org/s/records/1121/
The PDF is the artwork; this file is the score, rendered from per-word PDF
geometry onto a character grid (scripts/render_pearl_machine_text.py), so that
lineation, indentation, and the vertical field of each page survive extraction.
Pages are delimited by "· · ·  page N  · · ·"; blank rows are the book's own
whitespace, preserved at line resolution. ∮ = 1

"""
    OUT.write_text(header + "\n\n\n".join(pages) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, {len(pages)} pages)")


if __name__ == "__main__":
    sys.exit(main())
