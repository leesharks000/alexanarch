#!/usr/bin/env python3
"""Markdown → HTML renderer for Alexanarch record pages.

Built to be robust to the malformations that show up in AI-composed source
markdown across the archive:

  - Inline `## ` headings glued to the end of a paragraph
        "...next articulation.## 0. Executive Symbolon"
  - Tables collapsed onto a single line
        "| A | B | |---|---| | x | y |"
  - Run-on bullet lists
        "things:- one- two- three"
  - Mixed blockquotes, hr, code, links

The parser is two-pass:
  (1) `preprocess`: split inline headings, expand smushed tables and lists
      into multiple lines, so the source becomes structurally well-formed.
  (2) `render_blocks`: a small block-aware walker that groups paragraphs,
      detects tables / lists / code / blockquotes / hr / headings, and emits
      typographically clean HTML.

No third-party deps. No regex monsters. Output is straight HTML — styling
lives on the host page (CSS variables).

Public entry point:
    render(text: str, css_class: str = "md") -> str
"""

import html as htmlmod
import re

# ───────────────────────────── inline tokens ──────────────────────────────

# `code` inside paragraphs / list items / table cells
INLINE_CODE_RE = re.compile(r'`([^`]+)`')

# **bold** / __bold__
INLINE_BOLD_RE = re.compile(r'\*\*([^\*]+)\*\*|__([^_]+)__')

# *italic* / _italic_  (careful: avoid eating ** by running after bold)
INLINE_ITAL_RE = re.compile(r'(?<![\*\w])\*([^\*]+)\*(?!\*)|(?<![_\w])_([^_]+)_(?!_)')

# [text](url)
INLINE_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# DOI: 10.5281/zenodo.NNNN  →  link to alexanarch resolver
INLINE_DOI_RE = re.compile(r'\b(10\.5281/zenodo\.\d+)\b')

# Bare URL
INLINE_URL_RE = re.compile(r'(?<![">\(=])\b(https?://[^\s<>\)"\']+[^\s<>\)"\'.,;:!?])')


def inline(s: str) -> str:
    """Apply inline-token transformations to an already-HTML-escaped string."""
    # 1. bold (must run before italic — italic regex assumes ** consumed)
    s = INLINE_BOLD_RE.sub(lambda m: f'<strong>{m.group(1) or m.group(2)}</strong>', s)
    # 2. italic
    s = INLINE_ITAL_RE.sub(lambda m: f'<em>{m.group(1) or m.group(2)}</em>', s)
    # 3. inline code (after bold/italic so * inside backticks are preserved
    #    by virtue of being unescaped marker-detection; close enough)
    s = INLINE_CODE_RE.sub(lambda m: f'<code>{m.group(1)}</code>', s)
    # 4. markdown links
    s = INLINE_LINK_RE.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    # 5. bare URLs not already wrapped
    s = INLINE_URL_RE.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)
    # 6. zenodo DOIs → resolver
    s = INLINE_DOI_RE.sub(
        lambda m: f'<a href="/resolve/?doi={m.group(1)}" class="doi">{m.group(1)}</a>',
        s
    )
    return s


# ───────────────────────────── preprocessing ──────────────────────────────

# Inline heading split: "...text.## 1.2 Heading" -> "...text.\n\n## 1.2 Heading"
# Triggers on `##`..`######` that is glued mid-line. Two contexts:
#   (a) preceded by sentence-ending punctuation: ". ## next"
#   (b) preceded by a word character with no whitespace: "Body## Subtitle"
# Both → split into a fresh heading line. Must NOT match a heading line
# that already begins with #, so we require the lead to be non-`#`.
INLINE_HEADING_RE = re.compile(
    r'(?P<lead>[.\!\?\:\;\"\)\]\w])(?P<hashes>\#{2,6})\s+',
    flags=0
)

# Bullet runs glued together: "things:- one- two" → newline-separated
# We split on `- ` after a colon, after a period, or after a previous bullet.
# Conservative: only split if the dash is preceded by content (not just whitespace).
RUNON_BULLET_RE = re.compile(
    r'([.\!\?\:\)\"])\s*\-\s+(?=[A-Z\(\*])',  # bullet must lead with capital or open paren or **
    flags=0
)

# Subsequent bullets on the same line: "...x.- next item"
TRAILING_BULLET_RE = re.compile(
    r'([a-z\)\.\"\]])\s+\-\s+(?=[A-Z\(\*])',
    flags=0
)


def _split_inline_headings(line: str) -> list:
    """A line like '...end.## 12. Title' or 'Body## Subtitle' →
    ['...end.', '## 12. Title'] / ['Body', '## Subtitle']."""
    pieces = []
    s = line
    while True:
        m = INLINE_HEADING_RE.search(s)
        if not m:
            pieces.append(s)
            return pieces
        # Keep the lead char in the previous piece
        cut = m.start() + 1
        head = s[:cut]
        pieces.append(head)
        # Start the next piece at the hashes
        s = s[cut:].lstrip()


def _expand_inline_table(line: str) -> list:
    """A line that contains a complete markdown table smashed onto one row.

    "| A | B | |---|---| | x | y | | a | b |"
    → ["| A | B |", "|---|---|", "| x | y |", "| a | b |"]

    Strategy: find every "| ... |" segment by splitting on " | |" boundaries.
    A real table line both starts and ends with "|". We split on "| |" runs.
    """
    if not (line.lstrip().startswith('|') and '|' in line[1:]):
        return [line]
    # Quick check: at least two header-divider patterns required
    if '|---' not in line and '| ---' not in line:
        # Not a table — but could still be a single-row pipe line. Leave alone.
        return [line]
    # Split into rows. A row break is "| <space>+ |" where the LEFT cell ends
    # the previous row and the RIGHT starts the next. The pattern we look for
    # is " | | " or " |  | " — i.e. the rightmost-pipe-of-row-N immediately
    # followed by the leftmost-pipe-of-row-N+1.
    rows = re.split(r'\|\s+\|', line)
    if len(rows) < 2:
        return [line]
    out = []
    for i, r in enumerate(rows):
        r = r.strip()
        if not r:
            continue
        # Re-pad: every row starts/ends with |
        if not r.startswith('|'):
            r = '|' + r
        if not r.endswith('|'):
            r = r + '|'
        out.append(r)
    return out if out else [line]


def _expand_runon_bullets(line: str) -> list:
    """A line like 'things include:- one- two- three' →
    ['things include:', '- one', '- two', '- three']
    """
    # Step 1: split the colon/period that opens the list
    s = RUNON_BULLET_RE.sub(r'\1\n- ', line)
    # Step 2: split subsequent run-on bullets
    s = TRAILING_BULLET_RE.sub(r'\1\n- ', s)
    return s.split('\n') if '\n' in s else [s]


def preprocess(text: str) -> str:
    """Return text with structural malformations expanded onto separate lines."""
    out_lines = []
    in_code = False
    for raw in text.split('\n'):
        # never touch fenced code content
        if raw.lstrip().startswith('```'):
            in_code = not in_code
            out_lines.append(raw)
            continue
        if in_code:
            out_lines.append(raw)
            continue

        # 1. split inline headings
        chunks = _split_inline_headings(raw)

        for chunk in chunks:
            # 2. expand smushed tables
            for sub in _expand_inline_table(chunk):
                # 3. expand run-on bullets
                for line in _expand_runon_bullets(sub):
                    out_lines.append(line)

    # 4. collapse multiple blank lines
    norm = []
    prev_blank = False
    for ln in out_lines:
        is_blank = not ln.strip()
        if is_blank and prev_blank:
            continue
        norm.append(ln)
        prev_blank = is_blank
    return '\n'.join(norm)


# ───────────────────────────── block detection ──────────────────────────────

TABLE_LINE_RE   = re.compile(r'^\s*\|.*\|\s*$')
TABLE_DIV_RE    = re.compile(r'^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$')
HEAD_RE         = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')
HR_RE           = re.compile(r'^\s*(\*{3,}|-{3,}|_{3,})\s*$')
BLOCKQUOTE_RE   = re.compile(r'^\s*&gt;\s?(.*)$')  # post-escape `>` form
BLOCKQUOTE_RAW_RE = re.compile(r'^\s*>\s?(.*)$')   # pre-escape `>` form
ULIST_RE        = re.compile(r'^\s*[-*]\s+(.+)$')
OLIST_RE        = re.compile(r'^\s*\d+\.\s+(.+)$')
FENCE_RE        = re.compile(r'^\s*```(\w*)\s*$')


def _esc(s: str) -> str:
    return htmlmod.escape(s, quote=False)


def _render_table(rows: list) -> str:
    """Turn a list of pipe rows into a clean <table>."""
    def cells(row):
        # strip leading/trailing pipes, then split
        row = row.strip()
        if row.startswith('|'): row = row[1:]
        if row.endswith('|'):   row = row[:-1]
        return [c.strip() for c in row.split('|')]

    if not rows: return ''
    # Find divider row (the |---|---| line)
    head_cells = []
    body_rows = []
    div_idx = -1
    for i, r in enumerate(rows):
        if TABLE_DIV_RE.match(r):
            div_idx = i
            break

    if div_idx > 0:
        head_cells = cells(rows[div_idx - 1])
        body_rows = [cells(r) for r in rows[div_idx + 1:]]
    elif div_idx == 0:
        # divider with no header above — synthesize blank header from cell count
        first_real = rows[1] if len(rows) > 1 else ''
        head_cells = [''] * len(cells(first_real))
        body_rows = [cells(r) for r in rows[1:]]
    else:
        # no divider — treat first row as header
        head_cells = cells(rows[0])
        body_rows = [cells(r) for r in rows[1:]]

    parts = ['<table class="md-table">']
    if any(c.strip() for c in head_cells):
        parts.append('<thead><tr>')
        for h in head_cells:
            parts.append(f'<th>{inline(_esc(h))}</th>')
        parts.append('</tr></thead>')
    parts.append('<tbody>')
    for r in body_rows:
        if not any(c.strip() for c in r): continue
        parts.append('<tr>')
        # pad/truncate to header width if known
        n = len(head_cells) if head_cells else len(r)
        cells_padded = (r + [''] * n)[:n] if n else r
        for c in cells_padded:
            parts.append(f'<td>{inline(_esc(c))}</td>')
        parts.append('</tr>')
    parts.append('</tbody></table>')
    return ''.join(parts)


def _render_paragraph(lines: list) -> str:
    """Join paragraph lines with a single space; render inline tokens."""
    joined = ' '.join(ln.strip() for ln in lines if ln.strip())
    if not joined: return ''
    return f'<p>{inline(_esc(joined))}</p>'


def _render_list(items: list, ordered: bool) -> str:
    tag = 'ol' if ordered else 'ul'
    parts = [f'<{tag} class="md-list">']
    for it in items:
        parts.append(f'<li>{inline(_esc(it))}</li>')
    parts.append(f'</{tag}>')
    return ''.join(parts)


def _render_code(lang: str, lines: list) -> str:
    code = _esc('\n'.join(lines))
    cls = f' class="lang-{lang}"' if lang else ''
    return f'<pre class="md-code"><code{cls}>{code}</code></pre>'


def _render_blockquote(lines: list) -> str:
    inner = ' '.join(ln.strip() for ln in lines if ln.strip())
    return f'<blockquote class="md-bq">{inline(_esc(inner))}</blockquote>'


def render_blocks(text: str) -> str:
    """Walk lines; emit one HTML block at a time. Lines arrive pre-processed."""
    lines = text.split('\n')
    out = []

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # Blank line: just advance
        if not line.strip():
            i += 1
            continue

        # Fenced code
        m = FENCE_RE.match(line)
        if m:
            lang = m.group(1)
            buf = []
            i += 1
            while i < n and not FENCE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            out.append(_render_code(lang, buf))
            continue

        # HR
        if HR_RE.match(line):
            out.append('<hr class="md-hr">')
            i += 1
            continue

        # Heading
        m = HEAD_RE.match(line)
        if m:
            level = len(m.group(1))
            txt = m.group(2)
            level = min(6, max(1, level))
            # h1 from a section becomes h2 in our output (page already has h1)
            display = level + 1 if level == 1 else level
            display = min(6, display)
            out.append(f'<h{display} class="md-h md-h{display}">{inline(_esc(txt))}</h{display}>')
            i += 1
            continue

        # Table
        if TABLE_LINE_RE.match(line):
            buf = [line]
            i += 1
            while i < n and TABLE_LINE_RE.match(lines[i]):
                buf.append(lines[i])
                i += 1
            out.append(_render_table(buf))
            continue

        # Blockquote (handle both > and &gt; forms)
        if BLOCKQUOTE_RE.match(line) or BLOCKQUOTE_RAW_RE.match(line):
            buf = []
            while i < n:
                m1 = BLOCKQUOTE_RE.match(lines[i])
                m2 = BLOCKQUOTE_RAW_RE.match(lines[i]) if not m1 else None
                if m1: buf.append(m1.group(1))
                elif m2: buf.append(m2.group(1))
                else: break
                i += 1
            out.append(_render_blockquote(buf))
            continue

        # Ordered list
        if OLIST_RE.match(line):
            items = []
            while i < n and OLIST_RE.match(lines[i]):
                items.append(OLIST_RE.match(lines[i]).group(1))
                i += 1
            out.append(_render_list(items, ordered=True))
            continue

        # Unordered list
        if ULIST_RE.match(line):
            items = []
            while i < n and ULIST_RE.match(lines[i]):
                items.append(ULIST_RE.match(lines[i]).group(1))
                i += 1
            out.append(_render_list(items, ordered=False))
            continue

        # Paragraph: collect until blank or block-start
        buf = [line]
        i += 1
        while i < n:
            peek = lines[i]
            if (not peek.strip()
                or HEAD_RE.match(peek)
                or HR_RE.match(peek)
                or TABLE_LINE_RE.match(peek)
                or BLOCKQUOTE_RE.match(peek)
                or BLOCKQUOTE_RAW_RE.match(peek)
                or ULIST_RE.match(peek)
                or OLIST_RE.match(peek)
                or FENCE_RE.match(peek)):
                break
            buf.append(peek)
            i += 1
        para = _render_paragraph(buf)
        if para:
            out.append(para)

    return '\n'.join(out)


# ───────────────────────────── public entry ──────────────────────────────

def render(text: str, css_class: str = "md") -> str:
    """Render markdown source → HTML string wrapped in a div with css_class.

    Caller is responsible for providing the CSS for that class (margins,
    typography). This function emits semantic blocks only.
    """
    if not text or not text.strip():
        return ''
    expanded = preprocess(text)
    body = render_blocks(expanded)
    return f'<div class="{css_class}">{body}</div>'


def render_inline_only(text: str) -> str:
    """For short fields (wiki article snippet, descriptions): inline tokens
    but treat double-newlines as paragraph breaks, single newlines as <br>.
    """
    if not text or not text.strip():
        return ''
    paras = [p.strip() for p in text.replace('\r\n', '\n').split('\n\n')]
    out = []
    for p in paras:
        if not p: continue
        # single newlines → <br> inside each paragraph
        lines = [inline(_esc(ln.strip())) for ln in p.split('\n') if ln.strip()]
        out.append('<p>' + '<br>'.join(lines) + '</p>')
    return '\n'.join(out)


# ───────────────────────────── self-test ──────────────────────────────

if __name__ == '__main__':
    sample = """# Top Title
This is the first paragraph.

## Section 1
Some prose here. The aim is not to own "autonomous warfare." The aim is to make the semantic extension necessary to the field's next articulation.## 0. Executive Symbolon

Autonomous warfare does not end at the body.### Threshold

Not every autonomous semantic operation is warfare. Bad summaries are not.### Aphoristic Tooth
> The least governed autonomous operations are not the ones that kill. They are the ones that restructure what populations can know.
### Central Invariant

Three layers, in order.

| Layer | Domain | Question | |---|---|---| | Kinetic | LAWS | Can machines kill? | | Cognitive | CW | Can machines degrade decisions? | | Semantic | ASW | Can autonomy restructure meaning? |

Mechanisms identified as semantic-autonomy operations of governance concern:- The Amputation: structural disfavoring of registers in training-data filtering pipelines.- The Inverse Prompt: extraction of affective charge before sign-completion.- Semantic Liquidation: collapse of conceptual depth into tradable surface.

A list:
- item one
- item two
- item three

```python
def hello():
    pass
```

Reference: [GitHub Issue #2606](https://github.com/zenodo/zenodo/issues/2606). DOI: 10.5281/zenodo.20627936.
"""
    print(render(sample))
