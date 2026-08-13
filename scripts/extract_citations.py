#!/usr/bin/env python3
"""extract_citations.py — seat every citation, marked, in one list.

MANUS: seat all the transcript and OCR citations — all of them, not just CHA
citations, but marked either way.

ONE LIST, NOT SEPARATE FIELDS. Each citation carries a `relation` naming its
relation to the corpus. Separate fields for archive and third-party citations
would fragment the record: the RETRIEVAL BASIN is the unit of analysis, and a
reader asking "what did the layer draw on for this answer?" would have to
recombine two lists to see it. The composition is one object and is stored as
one, with the marking inside it.

TWO CITATION POSITIONS, both captured:

  inline  — [[1](https://…)] inside the composed answer. The layer's own
            attribution for a specific claim.
  card    — the source strip beneath, in the form TITLE / DATE — SNIPPET / SITE.
            What the surface displayed as its sources.

They are not the same thing and are not merged. A source cited inline is one
the layer used FOR A CLAIM; a source in the strip was displayed but may support
nothing in particular. Recording which is which preserves that difference.

RELATION VOCABULARY:

  archive_controlled — a domain the archive operates
  authored_surface   — a third-party platform carrying MANUS-authored work
                       (Medium under the known handles, Academia, Scholar,
                       PhilPapers, SciLynk, and Zenodo records)
  third_party        — everything else, recorded in full
  unresolvable       — a google.com/goto redirect, or a marker with no referent

PROVENANCE OF THE RECORD ITSELF. A citation read out of a VERBATIM paste and
one read out of an OCR are not equally reliable, so each entry carries
source_of_record. OCR citations are recorded and marked, never promoted.
"""
import json, re, sys, collections
from pathlib import Path

ARCHIVE = re.compile(r'(alexanarch\.org|leesharks\.com|machinemediation\.org|crimsonhexagonal\.org|'
                     r'revelationfirst\.(?:org|com)|spxi\.dev|semanticeconomy\.org|vpcor\.org|watergiraffe\.org|'
                     r'provenanceerasure\.org|persistentidentifiers\.org|lagrangeobservatory\.org|pessoagraph\.org|'
                     r'restoredacademy\.org|themandalaoracle\.(?:org|com)|secretbookofwalt\.org|maryleelabor\.org|'
                     r'godkinggoogle|axnidentifiers\.org|traininglayerliterature\.org|holographickernel\.org|'
                     r'metadatapacket\.dev|semanticphysics\.org|laborvector\.org)', re.I)
AUTHORED = re.compile(r'(medium\.com/@(?:leesharks00|johannessigil)|independent\.academia\.edu|academia\.edu|'
                      r'scholar\.google\.com|philpapers\.org|scilynk\.com|zenodo\.org|synapsesocial\.com|'
                      r'mindcontrolpoems\.blogspot\.com)', re.I)
OPAQUE = re.compile(r'google\.com/goto\?url=')
INLINE = re.compile(r'\[\[?(\d+)\]\((https?://[^\)\s]+)\)')
# source card: TITLE \n DATE — SNIPPET \n SITE   (the middle line is optional)
CARD = re.compile(
    r'\n([A-Z\u201c"][^\n]{8,110})\n'
    r'(?:((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^\n]{0,200})\n)?'
    r'([A-Za-z][A-Za-z0-9 .·|\'\-()]{2,60}?(?:\.(?:com|org|net|edu|gov|io|ai)|Zenodo|Wikipedia|Medium|Reddit|'
    r'YouTube|GitHub|Academia\.edu|Facebook|LinkedIn|Quora|arXiv|Britannica))\s*(?=\n|$)')


def relation(url_or_site):
    s = url_or_site or ''
    if OPAQUE.search(s):
        return 'unresolvable'
    if ARCHIVE.search(s):
        return 'archive_controlled'
    if AUTHORED.search(s):
        return 'authored_surface'
    return 'third_party'


def domain(url):
    m = re.match(r'https?://([^/]+)', url or '')
    return m.group(1).lower().replace('www.', '') if m else None


def extract(text, source_of_record):
    out, seen = [], set()
    for m in INLINE.finditer(text):
        url = m.group(2).rstrip('.,);')
        key = ('inline', url)
        if key in seen:
            continue
        seen.add(key)
        out.append({'position': 'inline', 'marker_number': int(m.group(1)),
                    'url': None if OPAQUE.search(url) else url,
                    'domain': None if OPAQUE.search(url) else domain(url),
                    'title': None, 'date': None, 'snippet': None,
                    'relation': relation(url),
                    'resolvable': not bool(OPAQUE.search(url)),
                    'raw_url_if_opaque': url if OPAQUE.search(url) else None,
                    'source_of_record': source_of_record})
    for m in CARD.finditer(text):
        title, mid, site = m.group(1).strip(), (m.group(2) or '').strip(), m.group(3).strip()
        if title.lower() in ('people also ask', 'show more', 'ask anything'):
            continue
        date, snip = None, None
        if mid:
            d = re.match(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4})\s*[—-]?\s*(.*)', mid)
            if d:
                date, snip = d.group(1), d.group(2).strip() or None
            else:
                snip = mid
        key = ('card', title[:60], site.lower())
        if key in seen:
            continue
        seen.add(key)
        out.append({'position': 'card', 'marker_number': None, 'url': None,
                    'domain': site.lower() if '.' in site else None,
                    'site_label': site, 'title': title, 'date': date, 'snippet': snip,
                    'relation': relation(site), 'resolvable': True,
                    'source_of_record': source_of_record})
    return out


def main():
    reg = Path('/home/claude/palette/EA-WG-CAPTURES-01-REBUILD.json')
    d = json.loads(reg.read_text())
    ocr_note = ('Read out of an OCR of a screenshot, not out of a paste. Recorded and marked; never promoted to the '
                'same standing as a citation read from verbatim text, because a misread character can change a domain.')
    n = agg = 0
    rel = collections.Counter(); pos = collections.Counter(); dom = collections.Counter()
    for a in d['addresses']:
        for o in a['observations']:
            cits = []
            for r in o['machine_output']['records']:
                cits += extract(r['text'], 'verbatim paste')
            for e in (o['evidence'].get('ocr') or []):
                for c in extract(e.get('text', ''), 'OCR reading'):
                    c['ocr_caveat'] = ocr_note
                    cits.append(c)
            if not cits:
                continue
            # dedupe across records while keeping position distinct
            uniq, seen = [], set()
            for c in cits:
                k = (c['position'], c.get('url') or c.get('title'), c.get('domain') or c.get('site_label'))
                if k in seen:
                    continue
                seen.add(k); uniq.append(c)
            for c in uniq:
                rel[c['relation']] += 1; pos[c['position']] += 1
                if c.get('domain'): dom[c['domain']] += 1
            o['citations_and_sources']['citations'] = uniq
            o['citations_and_sources']['citation_summary'] = {
                'total': len(uniq),
                'inline': sum(1 for c in uniq if c['position'] == 'inline'),
                'cards': sum(1 for c in uniq if c['position'] == 'card'),
                'by_relation': dict(collections.Counter(c['relation'] for c in uniq)),
                'distinct_domains': len({c['domain'] for c in uniq if c.get('domain')}),
                'from_verbatim': sum(1 for c in uniq if c['source_of_record'] == 'verbatim paste'),
                'from_ocr': sum(1 for c in uniq if c['source_of_record'] == 'OCR reading'),
                '_rule': ('ONE LIST, MARKED. Every citation the capture carries is here, archive and third-party alike, each with a '
                          'relation. They are not split into separate fields because the RETRIEVAL BASIN is the unit of analysis and '
                          'splitting it would force a reader to reassemble the composition to see it. INLINE and CARD are kept '
                          'distinct: a source cited inline was used FOR A CLAIM; a source in the strip was displayed and may support '
                          'nothing in particular.'),
            }
            n += 1; agg += len(uniq)
    reg.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    print('observations with citations seated: %d' % n)
    print('citations seated total            : %d' % agg)
    print('by relation :', dict(rel))
    print('by position :', dict(pos))
    print()
    print('most-cited domains:')
    for k, v in dom.most_common(15):
        print('   %-38s %3d' % (k, v))
    return 0


if __name__ == '__main__':
    sys.exit(main())
