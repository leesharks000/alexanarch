"""references_lib.py — a deposit's standard works-cited list, read out of its text.

WHY THIS EXISTS
---------------
The author, 2026-11-23 20:40: "we have to keep standard works cited lists alongside axn citations - aggregators read
citations as authority. full stop. google scholar wont index without it." An audit of #1700–#1804 that evening found
the journal papers of mid-November giving their sources as prose paragraphs, footnotes or not at all, and no record
page emitting citation_reference tags. Adopted at 20:48: repair the papers in place, emit the tags, record the gap at
deposit. This module is the one reading of "a standard list" all three use.

THE RULE
--------
A standard list is the LAST section of the text headed References, Works cited, Bibliography or Sources (a markdown
heading of any level, or a bold line, optionally numbered), whose body gives one work per line: a list item or a
paragraph of its own. An entry is a line that names a year (1500–2099), a DOI or a URL and is under 600 characters;
subheadings, footnote definitions, labelled prose lines ('Read in full: …') and lines running more than four works
together by semicolons are not entries. A section of
prose paragraphs therefore yields no entries, which is the finding the deposit check records.
"""
import re

HEAD = re.compile(r'^\s{0,3}(?:#{1,6}\s*|\*\*)\s*(?:\d+\.?\s*)?(References|Works [Cc]ited|Bibliography|Sources)\b[^\n]*$', re.M)
YEAR = re.compile(r'\bn\.d\.|\b(1[5-9]\d\d|20\d\d)\b|doi\.org|doi:|https?://', re.I)
MD_LINK = re.compile(r'\[([^\]]+)\]\((https?://[^)\s]+)\)')


def section(text):
    """The body of the last standard-list section, or None."""
    ms = list(HEAD.finditer(text or ""))
    if not ms:
        return None
    m = ms[-1]
    body = text[m.end():]
    level = len(re.match(r'\s*(#*)', m.group(0)).group(1))
    if level:
        stop = re.search(r'^\s{0,3}#{1,%d}\s+(?!#)' % level, body, re.M)
        body = body[:stop.start()] if stop else body
    return body


def plain(line):
    """An entry as plain text for a citation_reference tag: list marker, emphasis and link syntax removed, URLs kept."""
    s = re.sub(r'^\s*(?:[-*+]\s+|\d+\.\s+|\[\d+\]\s*)', '', line.strip())
    s = MD_LINK.sub(lambda m: m.group(1) if m.group(2) in m.group(1) else f'{m.group(1)} {m.group(2)}', s)
    s = re.sub(r'(\*\*|__|\*|_)(\S(?:.*?\S)?)\1', r'\2', s)
    s = s.replace('`', '')
    return re.sub(r'\s+', ' ', s).strip()


def entries(text):
    """The entries of the deposit's standard list, as plain strings, in order."""
    body = section(text)
    if body is None:
        return []
    out = []
    for line in body.split('\n'):
        l = line.strip()
        if not l or l.startswith('#') or len(l) >= 600 or l.startswith('|'):
            continue
        if re.match(r'^\*\*[^*]{1,80}\*\*:?$', l) or re.match(r'^\*[^*]{1,80}\*:?$', l):
            continue  # a subheading set in bold or italic
        if not YEAR.search(l) or l.startswith('[^'):
            continue  # no year, DOI or URL; or a footnote definition, which is a note, not a list entry
        if re.match(r'^(?:[-*+]\s+)?[*_]{0,2}[A-Z][^.:;]{0,40}:[*_]{0,2}\s', l) or l.count(';') > 3:
            continue  # a labelled prose line ('Read in full: …', 'Primary: …') or several works run together
        p = plain(l)
        if len(p) >= 12:
            out.append(p)
    return out


def finding(text, content_type=""):
    """What the deposit check records: ('list', n) when a standard list has entries, else the kind of absence."""
    n = len(entries(text))
    if n:
        return {"state": "list", "entries": n}
    if section(text) is not None:
        return {"state": "section without entries", "entries": 0}
    if len(re.findall(r'^\[\^[^\]]+\]:', text or "", re.M)) >= 3:
        return {"state": "footnotes only", "entries": 0}
    return {"state": "none", "entries": 0}
