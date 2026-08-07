#!/usr/bin/env python3
"""build_capture_gallery.py — the captures must be readable by the things they observe.

THE DEFECT THIS CLOSES
The capture registry is a record of how machine composition layers describe this
corpus. It was client-rendered, so a non-executing crawler received **717
characters of navigation and a heading — zero of 242 captures.** No JSON-LD, no
noscript, no static list; the registry absent from sitemap and ResourceSync; the
page carrying only rel=canonical.

Worse, every citation anchor existed only after JavaScript ran. Captures had just
been made citable by people and remained uncitable by machines — for a registry
whose entire subject is machine reception, that is close to self-defeating. Two
hundred and forty-two dated observations of machine behaviour, unreadable by
machines.

This is the fd8de940 disease in a second location: **the bytes are correct and
the publication is invisible.**

WHAT THIS DOES
Pre-renders every capture as an anchored card into the page, between markers, so
the complete list is in the HTML for crawlers, archival capture, and readers
without JavaScript. The existing script then takes over for filtering and paging
— progressive enhancement, the same shape used for browse and wiki. It also
writes a JSON-LD Dataset description and the Signposting links the page lacked.

Usage:  python3 scripts/build_capture_gallery.py
"""
import json, re, sys, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data/EA-WG-CAPTURES-01.json"
PAGE = ROOT / "captures/index.html"
BEGIN = "<!-- CAPTURES-STATIC-BEGIN -->"
END = "<!-- CAPTURES-STATIC-END -->"


def card(e):
    esc = html.escape
    slug = e.get("slug", "")
    d = (e.get("d") or "")
    mt = e.get("mt") or "unrated"
    cite = e.get("cite") or f"https://www.alexanarch.org/captures/#{slug}"
    return (
        f'<div class="cap-card" id="{esc(slug)}">'
        f'<div class="cap-head"><span class="cap-section">{esc(e.get("s") or "Unsectioned")}</span>'
        f'<span class="cap-date">{esc(e.get("date") or "")}</span></div>'
        f'<div class="cap-query">{esc(e.get("q") or "")}</div>'
        f'<div class="cap-status-row">'
        f'<span class="cap-status cap-status-{esc(mt.split()[0].lower())}">{esc(mt)}</span>'
        f'<span class="cap-sf">{esc(e.get("sf") or "")}</span></div>'
        f'<div class="cap-desc">{esc(d)}</div>'
        f'<div class="cap-actions"><a href="{esc(cite)}">¶ Cite</a></div>'
        f'</div>')


def main():
    r = json.loads(REG.read_text())
    entries = r["entries"]
    page = PAGE.read_text()

    cards = "\n".join(card(e) for e in entries)
    block = (f'{BEGIN}\n<noscript><p style="color:var(--dim);font-size:.9em">'
             f'Filtering and paging need JavaScript. The complete list of '
             f'{len(entries)} captures is below.</p></noscript>\n{cards}\n{END}')

    if BEGIN in page:
        page = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block, page, flags=re.S)
    else:
        anchor = '<div id="captures">Loading&hellip;</div>'
        if anchor not in page:
            print("FAIL: could not find the render target in captures/index.html", file=sys.stderr)
            return 1
        page = page.replace(anchor, f'<div id="captures">\n{block}\n</div>')

    # JSON-LD: the registry described as a dataset, once
    ld = {
        "@context": "https://schema.org", "@type": "Dataset",
        "name": "AI Overview Capture Registry (EA-WG-CAPTURES-01)",
        "description": ("Dated observations of how machine composition layers — AI Overviews, "
                        "AI Mode, and comparable summarisation surfaces — describe the Alexanarch "
                        "corpus. Each capture records the query, the sources the layer cited, what "
                        "it rendered, and the date, and is individually citable by its slug."),
        "url": "https://www.alexanarch.org/captures/",
        "identifier": "EA-WG-CAPTURES-01",
        "version": r.get("version"), "dateModified": r.get("date"),
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@type": "Person", "name": "Lee Sharks",
                    "identifier": "https://orcid.org/0009-0000-1599-0703"},
        "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json",
                          "contentUrl": "https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json"}],
        "size": f"{len(entries)} captures",
    }
    ldblock = ('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False)
               + "</script>\n")
    signposts = (
        '<link rel="describedby" href="https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json" type="application/json">\n'
        '<link rel="item" href="https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json" type="application/json">\n'
        '<link rel="cite-as" href="https://www.alexanarch.org/captures/">\n')
    page = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", page, flags=re.S)
    page = re.sub(r'<link rel="(describedby|item|cite-as)"[^>]*>\n?', "", page)
    page = page.replace("</head>", signposts + ldblock + "</head>", 1)

    PAGE.write_text(page)
    print(f"static gallery: {len(entries)} anchored cards rendered into the page "
          f"({len(page):,} bytes) + JSON-LD Dataset + Signposting")
    return 0


if __name__ == "__main__":
    sys.exit(main())
