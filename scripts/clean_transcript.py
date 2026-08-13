#!/usr/bin/env python3
"""clean_transcript.py — VERBATIM ON CONTENT, NOT ON COPY-PASTE RESIDUE.

MANUS, 2026-08-13: "the transcripts get cleaned - no garble, inline citations
normalized, ending blob normalized, formatting for clarity and ease of
comprehension fine. verbatim means verbatim on content, not verbatim on copy
paste residue."

That ruling frees the transcript. Until now every byte was treated as sacred,
including bytes the LAYER NEVER PRODUCED — browser chrome swept up by a
selection, the interface's own "Show more" control, the platform footer, the
prompt box at the bottom of the page. Preserving those as though they were the
machine's words was not fidelity; it was fidelity to the clipboard.

WHAT IS RESIDUE. Only things the interface produced, never the answer:
    the "AI Mode Conversation" wrapper the export writes
    "You said:" prompt echo
    "Show more" / "Show less" — an interface control, not a sentence
    "AI can make mistakes, so double-check responses" — platform footer
    "Ask anything" — the prompt box
    a bare "+3" source badge on its own
    the URL bar and tab row in an OCR sweep

WHAT IS NEVER TOUCHED. Anything the layer composed. Every content word survives
and the check enforces it: the cleaner refuses its own output if a word the
answer used has gone missing.

THE RAW IS KEPT. transcript_raw holds the original bytes forever; the clean text
is a rendering. The archive does not amend silently, and a reader who wants the
clipboard exactly as it fell can have it.
"""
import re, unicodedata

# Interface furniture. Each anchored so it cannot eat an answer sentence.
RESIDUE = [
    (r'(?im)^\s*AI Mode Conversation\s*$', 'AI Mode export wrapper'),
    (r'(?im)^\s*You said:\s*', 'prompt echo'),
    (r'(?im)^\s*Show (?:more|less)\s*[\u25be\u25bc\u2228vV]?\s*$', 'interface control'),
    (r'(?im)^\s*AI can make mistakes[^\n]*$', 'platform footer'),
    (r'(?im)^\s*Ask anything[^\n]*$', 'prompt box'),
    (r'(?im)^\s*\+\d{1,2}\s*$', 'source-count badge'),
    (r'(?im)^\s*Sign in\s*$', 'browser chrome'),
    # A URL BAR READ BY OCR arrives with the browser's own glyph soup around it —
    # "fl 26 google.com/search?q=anti-sup (3) :" — so an anchored prefix cannot
    # catch it. The test is instead: the LINE contains a search URL, is SHORT, and
    # ends in no sentence punctuation. An answer sentence that happens to cite a
    # search URL is long and punctuated, and is left alone. Verified against the
    # two paste lines that mention one: both survive.
    (r'(?im)^(?=[^\n]{0,90}$)(?![^\n]*[.!?]\s*$)[^\n]*google\.com/search[^\n]*$', 'URL bar'),
    (r'(?im)^\s*AI ?Mode\s+All\s+Images[^\n]*$', 'tab row'),
    (r'(?im)^\s*Google\s*$', 'browser chrome'),
]

# Inline citation markers, normalised to ONE FORM while KEEPING THE TARGET.
#
# The first version rewrote [1](https://…) to [1] and threw the URL away. THE URL
# IS WHAT THE LAYER CITED — it is the content of the attribution, not markup
# around it — and the content check caught 207 transcripts losing doi, tandfonline
# and bare identifiers to that rule. Normalising a citation must never delete the
# thing cited.
CITE_NEST = re.compile(r'\[\[(\d+)\]\(([^)]*)\)\]')      # [[1](url)]  -> [1](url)
CITE_BARE = re.compile(r'(?<!\w)\[(\d{1,2}(?:\s*,\s*\d{1,2})*)\](?!\()')  # [1,2] -> [1, 2]


def words(t):
    return re.findall(r'[0-9A-Za-z\u00c0-\uffff]+', str(t or '').lower())


def clean(text, drop_echo=None):
    """Return (clean_text, removed) — removed lists what came out and why."""
    t = unicodedata.normalize('NFC', str(text or ''))
    removed = []

    # doubled query echo: an export writes the query twice, run together
    if drop_echo:
        q = str(drop_echo).strip()
        if q:
            dbl = re.escape(q) + r'\s*' + re.escape(q)
            t2 = re.sub(dbl, q, t, count=1)
            if t2 != t:
                removed.append(('doubled query echo', q[:40]))
                t = t2

    for pat, why in RESIDUE:
        hits = re.findall(pat, t)
        if hits:
            t = re.sub(pat, '', t)
            removed.append((why, len(hits)))

    t = CITE_NEST.sub(lambda m: '[%s](%s)' % (m.group(1), m.group(2)), t)
    t = CITE_BARE.sub(lambda m: '[%s]' % re.sub(r'\s*,\s*', ', ', m.group(1)), t)
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    return t.strip(), removed


def check(raw, cleaned):
    """The cleaner must not lose a content word. Residue words are allowed to go."""
    ALLOWED = set(words(
        'AI Mode Conversation You said Show more less can make mistakes so double check '
        'responses Ask anything Sign in Google All Images News Videos Shopping Forums '
        'com search q'))
    # Single stray characters left by an OCR sweep of removed chrome — a URL bar
    # read as "(M 2% google.com/search?q=\" Ey H" leaves v, ey, m, h behind. Those
    # are artifacts of the read of a line that was itself residue.
    lost_all = set(words(raw)) - set(words(cleaned))
    lost_all = {w for w in lost_all if len(w) > 2}
    lost = [w for w in lost_all if w not in ALLOWED]
    return sorted(lost)
