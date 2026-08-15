"""Shared text handling for the Sappho–Philo program.

Every search in this program is DIACRITIC-BLIND. Philo's editions, the LXX
witnesses and the TEI disagree on accents and breathings; a diacritic-sensitive
grep silently under-reports and would have produced a false null on the
name-census. strip() is therefore the single normalization point.
"""
import re, html, unicodedata, pathlib

def strip(s: str) -> str:
    """Lowercase, decompose, drop combining marks. Diacritic-blind form."""
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                   if not unicodedata.combining(c))

def tei_text(xml: str) -> str:
    """TEI/XML -> running text. Drops header and editorial notes."""
    x = re.sub(r'<teiHeader.*?</teiHeader>', ' ', xml, flags=re.S)
    x = re.sub(r'<note.*?</note>', ' ', x, flags=re.S)
    x = re.sub(r'<[^>]+>', ' ', x)
    return re.sub(r'[ \t]+', ' ', html.unescape(x))

def wiki_text(page: str) -> str:
    """Wikisource HTML -> running text (parser-output div only)."""
    m = re.search(r'<div class="mw-parser-output">(.*?)<div class="printfooter"', page, re.S)
    body = m.group(1) if m else page
    body = re.sub(r'<(script|style).*?</\1>', ' ', body, flags=re.S)
    return re.sub(r'[ \t]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', body)))

def index_map(raw: str):
    """Normalized string + map from normalized offset -> raw offset.
    Lets a diacritic-blind hit be reported with its original accented text."""
    nc, im = [], []
    for i, c in enumerate(raw):
        for cc in unicodedata.normalize('NFD', c.lower()):
            if not unicodedata.combining(cc):
                nc.append(cc); im.append(i)
    return ''.join(nc), im
