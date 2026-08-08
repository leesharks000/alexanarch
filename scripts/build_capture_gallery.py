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


IMG_BASES = {
    # Bare filenames were written against the leesharks gallery's own captures
    # directory; entries added later carry absolute URLs. Neither form was ever
    # rendered by ANY gallery — the JS render function never referenced imgs at
    # all — so a citation to a capture has always landed on text describing an
    # image nobody could see.
    "bare": "https://leesharks.com/captures/",
    "repo": "https://www.alexanarch.org/",
}


def image_urls(e):
    """Resolve the three recorded forms into fetchable URLs."""
    out = []
    for i in (e.get("imgs") or e.get("images") or []):
        if not isinstance(i, str):
            continue
        if i.startswith("http"):
            out.append(i)
        elif i.startswith("data/captures/"):
            out.append(IMG_BASES["repo"] + i)
        else:
            out.append(IMG_BASES["bare"] + i.lstrip("/"))
    return out


def card(e):
    esc = html.escape
    slug = e.get("slug", "")
    d = e.get("d") or ""
    mt = e.get("mt") or "unrated"
    q = e.get("q") or slug
    date = e.get("date") or ""
    cite = e.get("cite") or f"https://www.alexanarch.org/captures/#{slug}"

    # DUALLY FUNCTIONAL. The button copies a citation a person can paste; the card
    # carries the same facts as schema.org microdata a crawler can extract without
    # executing anything. Previously the action was a bare anchor to #slug — which
    # navigated to the card the reader was already looking at, and so appeared to
    # do nothing at all.
    citation = (f'Sharks, Lee. "{q}" [machine-composition capture {slug}], {date}. '
                f'AI Overview Capture Registry (EA-WG-CAPTURES-01), Alexanarch. {cite}')

    urls = image_urls(e)
    if urls:
        thumbs = "".join(
            f'<a href="{esc(u)}" target="_blank" rel="noopener">'
            f'<img loading="lazy" src="{esc(u)}" '
            f'alt="Screen capture for the query &quot;{esc(q)}&quot;, dated {esc(date)}.">'
            f'</a>' for u in urls)
        imgs_html = f'<div class="cap-imgs">{thumbs}</div>'
    else:
        imgs_html = ('<div class="cap-noimg">no capture image held for this entry</div>')

    return (
        f'<div class="cap-card" id="{esc(slug)}" '
        f'data-section="{esc(e.get("s") or "Unsectioned")}" '
        f'data-status="{esc(mt.split()[0].lower())}" '
        f'itemscope itemtype="https://schema.org/CreativeWork">'
        f'<meta itemprop="identifier" content="{esc(cite)}">'
        f'<meta itemprop="isPartOf" content="EA-WG-CAPTURES-01">'
        f'<meta itemprop="creator" content="Sharks, Lee">'
        f'<meta itemprop="citation" content="{esc(citation)}">'
        f'<div class="cap-head"><span class="cap-section">{esc(e.get("s") or "Unsectioned")}</span>'
        f'<span class="cap-date" itemprop="dateCreated">{esc(date)}</span></div>'
        f'<div class="cap-query" itemprop="name">{esc(e.get("q") or "")}</div>'
        f'<div class="cap-status-row">'
        f'<span class="cap-status cap-status-{esc(mt.split()[0].lower())}">{esc(mt)}</span>'
        f'<span class="cap-sf">{esc(e.get("sf") or "")}</span></div>'
        f'{imgs_html}'
        f'<div class="cap-desc" itemprop="description">{esc(d)}</div>'
        f'<div class="cap-actions">'
        f'<button type="button" class="cap-cite" data-cite="{esc(cite)}" '
        f'data-citation="{esc(citation)}" '
        f'aria-label="Copy a citation for this capture">¶ Cite</button>'
        f'<a class="cap-permalink" href="{esc(cite)}" rel="bookmark">permalink</a>'
        f'</div>'
        f'</div>')


def main():
    r = json.loads(REG.read_text())
    entries = r["entries"]
    page = PAGE.read_text()

    cards = "\n".join(card(e) for e in entries)
    block = (f'{BEGIN}\n<noscript><p style="color:var(--dim);font-size:.9em">'
             f'Filtering and paging need JavaScript. The complete list of '
             f'{len(entries)} captures is below.</p></noscript>\n{cards}\n{END}')

    # The pager buttons were previously injected by the old JS render(); when render
    # became a DOM filter they vanished, leaving a reader able to see one page of 242
    # captures with no way to reach the rest. They are now real markup, and this
    # guard keeps a regeneration from dropping them again.
    if 'id="prev"' not in page:
        page = page.replace('<div class="pager" id="pager"></div>',
            '<div class="pager" id="pager">\n'
            '  <button id="prev" type="button">\u2039 previous</button>\n'
            '  <span id="pageinfo"></span>\n'
            '  <button id="next" type="button">next \u203a</button>\n</div>')

    if BEGIN in page:
        page = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block, page, flags=re.S)
    else:
        anchor = '<div id="captures">Loading&hellip;</div>'
        if anchor not in page:
            print("FAIL: could not find the render target in captures/index.html", file=sys.stderr)
            return 1
        page = page.replace(anchor, f'<div id="captures">\n{block}\n</div>')

    # THE FLOW, DISPLAYED. A gallery renders FROM the registry and never TO it, and
    # that has to be visible on the surface itself — not only in the source file —
    # because the surface is where a machine or a person forms the idea that this is
    # a place to write. Emitted as visible text AND as machine-readable JSON so a
    # crawler meets it without executing anything.
    flow = r.get("_FLOW") or {}
    if flow:
        steps = "".join(f"<li>{html.escape(x)}</li>" for x in flow.get("flow", []))
        flow_html = (
            '<section id="capture-flow" style="border:1px solid var(--border);border-left:3px solid '
            'var(--accent);border-radius:6px;padding:14px 16px;margin:18px 0;font-size:.86em;'
            'line-height:1.6">'
            '<div style="font-weight:600;margin-bottom:6px">Capture registry — data flow</div>'
            f'<div style="color:var(--dim);margin-bottom:8px">{html.escape(flow.get("READ_THIS_FIRST",""))}</div>'
            f'<div><b>Source of truth:</b> <code>{html.escape(flow.get("source_of_truth",""))}</code></div>'
            f'<ol style="margin:8px 0 8px 1.1em;padding:0">{steps}</ol>'
            f'<div style="color:var(--dim)"><b>Citation:</b> {html.escape(flow.get("citation",""))}</div>'
            f'<div style="color:var(--dim);margin-top:5px">{html.escape(flow.get("slugs_are_permanent",""))}</div>'
            '<div style="margin-top:8px"><a href="/data/EA-WG-CAPTURES-01.json">the registry itself</a>'
            ' &middot; <a href="/datasets/capture-registry/">published dataset</a></div>'
            '</section>')
        ld_flow = ('<script type="application/ld+json">' +
                   json.dumps({"@context":"https://schema.org","@type":"CreativeWork",
                               "name":"Capture registry data flow",
                               "isPartOf":{"@type":"Dataset","name":"EA-WG-CAPTURES-01"},
                               "text":flow.get("READ_THIS_FIRST",""),
                               "step":flow.get("flow",[]),
                               "url":"https://www.alexanarch.org/captures/#capture-flow"},
                              ensure_ascii=False) + "</script>")
        page = re.sub(r'<section id="capture-flow".*?</section>\n?', "", page, flags=re.S)
        page = re.sub(r'<script type="application/ld\+json">\{"@context": ?"https://schema.org", ?"@type": ?"CreativeWork".*?</script>\n?', "", page, flags=re.S)
        marker = '<div id="captures">'
        if marker in page:
            page = page.replace(marker, flow_html + "\n" + ld_flow + "\n" + marker, 1)

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
    # Strip only the Dataset block. A blanket strip also removed the data-flow
    # declaration emitted moments earlier — the flow is the thing this file exists
    # to make unmissable, and a cleanup regex was quietly deleting it.
    page = re.sub(r'<script type="application/ld\+json">\s*\{"@context":\s*"https://schema\.org",\s*"@type":\s*"Dataset".*?</script>\n?', "", page, flags=re.S)
    page = re.sub(r'<link rel="(describedby|item|cite-as)"[^>]*>\n?', "", page)
    page = page.replace("</head>", signposts + ldblock + "</head>", 1)

    PAGE.write_text(page)
    print(f"static gallery: {len(entries)} anchored cards rendered into the page "
          f"({len(page):,} bytes) + JSON-LD Dataset + Signposting")
    return 0


if __name__ == "__main__":
    sys.exit(main())
