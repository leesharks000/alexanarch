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
        elif i.startswith("data/"):
            # ANY repo-relative path, not just data/captures/. The narrower test
            # sent 21 images under data/capture-mirrors/ and data/captures-images/
            # to the leesharks host, where every one 404s because the file lives
            # HERE. A path that starts with data/ is this repository's.
            out.append(IMG_BASES["repo"] + i)
        else:
            out.append(IMG_BASES["bare"] + i.lstrip("/"))
    return out



# Ten of the 266 findings carry <strong> and <em> in their body — deliberate
# emphasis written by the analyst, marking the exact phrase the layer returned.
# Blanket-escaping them printed the tags as literal text on the card, which is
# the opposite of what emphasis is for. This escapes everything, then restores
# ONLY those four tags. Nothing else survives: no attributes, no other element,
# no unbalanced tag. Any richer markup in a future entry renders as text, which
# is the safe direction to fail.
_EMPH = re.compile(r'&lt;(/?)(strong|em|b|i)&gt;')


def emphasise(text):
    out = html.escape(text or "")
    out = _EMPH.sub(r'<\1\2>', out)
    # a lone opening tag would leak into the rest of the card
    for t in ("strong", "em", "b", "i"):
        if out.count(f"<{t}>") != out.count(f"</{t}>"):
            return html.escape(text or "")
    return out

def para(text):
    """Analyst prose is written in paragraphs. Render them as paragraphs."""
    esc = html.escape
    return "".join(f'<p>{emphasise(b.strip())}</p>'
                   for b in re.split(r'\n\s*\n', str(text or '')) if b.strip())


def transcript_block(e, gallery=''):
    """THE FULL RECORD, collapsed by default and complete inside.

    These are rich records and have been displayed as such in every instantiation
    of the registry. A projection that carried only a one-paragraph finding put
    67% of the available prose out of reach — including 230 KB of analyst reading
    across 246 observations that reached NO surface at all until 2026-08-13.

    Everything is rendered STATICALLY inside <details> so a crawler reads it
    without executing anything, while a reader sees one line until they expand.
    The client JS only hides and shows whole cards, so this survives filtering.

    Order is deliberate: what the analyst saw, then what the analyst wrote at
    length, then the sources with their snippets, then the collisions, then the
    machine's own words, then the open questions. Evidence class travels with the
    transcript so OCR is never mistaken for a paste.
    """
    esc = html.escape
    reading = e.get("reading") or ""
    analysis = e.get("analysis") or ""
    tr = e.get("transcript") or ""
    cites = e.get("cite_list") or []
    coll = e.get("collisions") or []
    oq = e.get("oq") or []
    if not (reading or analysis or tr or cites or coll or oq or gallery):
        return ""

    meta = {
        "captured": e.get("date"), "surface": e.get("surface"),
        "auth state": e.get("auth"), "evidence class": e.get("ev"),
        "PER": e.get("per"),
        "PER units retained": (", ".join(k for k, v in (e.get("per_v") or {}).items() if v)
                               or "none") if e.get("per_v") else None,
        "failure modes": ", ".join(e.get("modes") or []) or None,
        "citations read": e.get("cites"),
        "observation id": e.get("obs_id"), "address id": e.get("addr_id"),
    }
    parts = []
    # ROUNDS FIRST, because a round divorced from its capture erases provenance.
    # MANUS: "a semantic address is what is typed in the search bar. that is a
    # round within one capture, presented as a capture, and fragmenting single
    # captures across records. ONE CAPTURE INCLUDES ALL ROUNDS IN THAT CAPTURE."
    rounds = e.get("rounds") or []
    if rounds:
        rows = "".join(
            f'<li><b>round {esc(str(r.get("n")))}</b>'
            + (f'<div class="cap-ct">{esc(str(r["prompt"]))}</div>' if r.get("prompt")
               else '<div class="cap-cn">not recovered</div>')
            + (f'<div class="cap-cn">{esc(str(r["note"]))}</div>' if r.get("note") else '')
            + '</li>' for r in rounds)
        parts.append('<div class="cap-tr-label">Rounds '
                     '<span class="cap-tr-warn">this record is a ROUND, not a capture</span></div>'
                     f'<ol class="cap-cites">{rows}</ol>')
    # THE REMAINING CAPTURES, inside the expand. The leesharks gallery put its
    # gallery in the collapsed entry-body and showed ONE thumbnail up top; a
    # capture with six screenshots should show its first and keep the rest one
    # click away, not stack them all in the header.
    if gallery:
        parts.append('<div class="cap-tr-label">Further capture images</div>' + gallery)
    # Row tint groups so the table reads at a glance: capture conditions in one
    # tone, measurement in another, identifiers in a third.
    GROUP = {"captured": "cond", "surface": "cond", "auth state": "cond", "evidence class": "cond",
             "PER": "meas", "PER units retained": "meas", "failure modes": "meas", "citations read": "meas",
             "observation id": "ident", "address id": "ident"}
    rows = "".join(f'<dt class="g-{GROUP.get(k,"cond")}">{esc(str(k))}</dt>'
                   f'<dd class="g-{GROUP.get(k,"cond")}">{esc(str(v))}</dd>'
                   for k, v in meta.items() if v not in (None, "", [], {}))
    if rows:
        parts.append('<div class="cap-tr-label">Capture record</div>'
                     f'<dl class="cap-tr-meta">{rows}</dl>')
    if reading:
        parts.append('<div class="cap-tr-label">Reading</div>'
                     f'<div class="cap-tr-prose">{para(reading)}</div>')
    if analysis:
        parts.append('<div class="cap-tr-label">Analysis '
                     '<span class="cap-tr-warn">analyst prose, not machine text</span></div>'
                     f'<div class="cap-tr-prose">{para(analysis)}</div>')
    if cites:
        rows = "".join(
            '<li>' +
            (f'<a href="{esc(c["url"])}" target="_blank" rel="noopener">{esc(str(c.get("site") or "source"))}</a>'
             if c.get("url") else f'<b>{esc(str(c.get("site") or "source"))}</b>') +
            (f' <span class="cap-rel">{esc(str(c.get("rel") or ""))}</span>' if c.get("rel") else '') +
            (f'<div class="cap-ct">{esc(str(c["title"]))}</div>' if c.get("title") else '') +
            (f'<div class="cap-cs">{esc(str(c["snip"]))}</div>' if c.get("snip") else '') +
            (f'<div class="cap-cn">{esc(str(c["note"]))}</div>' if c.get("note") else '') +
            '</li>' for c in cites)
        parts.append(f'<div class="cap-tr-label">Sources as cited ({len(cites)})</div>'
                     f'<ol class="cap-cites">{rows}</ol>')
    if coll:
        rows = "".join(
            f'<li><b>{esc(str(c.get("with") or ""))}</b>'
            f'<div class="cap-cn">via {esc(str(c.get("via") or ""))}</div>'
            + (f'<div class="cap-cs">{esc(str(c["ev"]))}</div>' if c.get("ev") else '')
            + '</li>' for c in coll)
        parts.append('<div class="cap-tr-label">Collision register</div>'
                     f'<ul class="cap-cites">{rows}</ul>')
    def split_source_strip(text, cites):
        """A paste carries the composed answer AND the source strip, run together.

        MANUS: "within the transcripts, citation cards appear as a garbled blob
        with no differentiation from transcript body." The citations are already
        extracted, so the strip is grep-identifiable — this finds where it starts
        and renders it apart, WITHOUT altering a byte of the verbatim record.

        Conservative by design: it only splits on a cited title or snippet found
        in the last 60% of the text, and only when two or more distinct cited
        sources appear at or after that point. One stray match is not a strip.
        """
        if not cites or len(text) < 400:
            return text, ""
        floor = int(len(text) * 0.40)
        marks = []
        for c in cites:
            for key in (c.get("title"), (c.get("snip") or "")[:60], c.get("site")):
                k = (key or "").strip()
                if len(k) < 14:
                    continue
                i = text.find(k, floor)
                if i >= 0:
                    marks.append(i)
                    break
        if len(marks) < 2:
            return text, ""
        cut = min(marks)
        return text[:cut].rstrip(), text[cut:].strip()

    if tr:
        cls = e.get("transcript_class") or ""
        note = " · ".join(x for x in (cls, e.get("transcript_complete"), e.get("transcript_read")) if x)
        answer, strip = split_source_strip(tr, cites)
        parts.append('<div class="cap-tr-label">Machine text, verbatim</div>'
                     + (f'<div class="cap-tr-warn-line">{esc(note)}</div>' if note else '')
                     + f'<div class="cap-tr-body" itemprop="text">{esc(answer)}</div>'
                     + ('<div class="cap-tr-striplabel">source strip, as pasted &mdash; '
                        'the same sources listed above, run together by the copy</div>'
                        f'<div class="cap-tr-strip">{esc(strip)}</div>' if strip else ''))
    # SUB-ROUNDS BELONG TO THE PARENT AND ARE NEVER A CAPTURE. Presenting them as
    # captures inflated the count and corrupted every per-capture measurement in
    # the dataset — PER, defect rates, voice quotient denominators, all of it.
    rl = e.get("rounds") or []
    if len(rl) > 1:
        rows = ""
        for r in rl:
            rows += ('<li><b>round ' + esc(str(r.get("n"))) + '</b> &middot; '
                     + esc(str(r.get("q") or "")) +
                     ('<div class="cap-cn">' + esc(str(r.get("note") or "")) + '</div>' if r.get("note") else '') +
                     ('<div class="cap-cs">' + esc(str(r.get("finding") or "")) + '</div>' if r.get("finding") else '') +
                     ('<div class="cap-tr-body">' + esc(str(r.get("text") or "")) + '</div>' if r.get("text") else '') +
                     '</li>')
        parts.append('<div class="cap-tr-label">Rounds in this capture ('
                     + str(len(rl)) + ')</div>'
                     '<ul class="cap-cites">' + rows + '</ul>')

    ses = e.get("session") or {}
    if ses.get("continues_into") or ses.get("continued_from"):
        # THE SESSION SURVIVES THE FRAGMENTATION. A session is bounded by the
        # paste; where the interface forced one sitting into separate pastes the
        # rounds are joined by the operator's own note, never merged, because a
        # published slug is permanent. Read as separate addresses these are
        # unrelated captures; read as one session the 12 June chain is a
        # controlled single-variable experiment.
        rows = ""
        for x in (ses.get("continued_from") or []):
            rows += ('<li>continues from <a href="#' + esc(x["slug"]) + '">'
                     + esc(str(x.get("q") or x["slug"])) + '</a>'
                     '<div class="cap-cn">' + esc(str(x.get("why") or "")) + '</div></li>')
        for x in (ses.get("continues_into") or []):
            rows += ('<li>continues into <a href="#' + esc(x["slug"]) + '">'
                     + esc(str(x.get("q") or x["slug"])) + '</a>'
                     '<div class="cap-cn">' + esc(str(x.get("why") or "")) + '</div></li>')
        parts.append('<div class="cap-tr-label">Session</div>'
                     '<ul class="cap-cites">' + rows + '</ul>')
    if oq:
        parts.append('<div class="cap-tr-label">Open questions</div>'
                     '<ul class="cap-cites">' + "".join(f'<li>{esc(str(x))}</li>' for x in oq) + '</ul>')
    n = sum(len(x) for x in (reading, analysis, tr))
    return ('<details class="cap-transcript"><summary>Full record'
            + (f' — {n:,} characters, {len(cites)} sources' if n else '')
            + '</summary>' + "".join(parts) + '</details>')

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

    # RE-RUN opens the SAME semantic address live, so a capture is a repeatable
    # experiment and any reader can see the current state against this dated
    # baseline. The URL is DATA, built by the pipeline and carried on the entry —
    # never assembled here, because the query must be reproduced exactly,
    # quotation marks included. Quoting is the decisive variable in this corpus:
    # «operative semiotics» held 5/5 archive cards quoted and 1/8 unquoted.
    rerun = e.get("rerun")
    rerun_btn = (
        f'<a class="cap-cite cap-act cap-rerun" data-act="rerun" '
        f'data-rerun="{esc(rerun)}" href="{esc(rerun)}" target="_blank" '
        f'rel="noopener" aria-label="Run this same query now and compare with '
        f'this capture">↻ Re-run</a>') if rerun else ''

    # THE DEFECT RIBBON IS ON THE FACE OF THE CARD, not behind an expander.
    # MANUS: "if its invisible i wont check it, if i dont check it it will
    # drift." Every defect here was invisible when it happened.
    defects = e.get("defects") or []
    LABEL = {
        'truncated-by-interface': 'answer truncated by interface — absence here is absence from the VISIBLE portion',
        'unsupported-citations': 'CITATIONS UNSUPPORTED by this transcript — do not count',
        'citations-null': 'citation apparatus not captured — count is NULL, not zero',
        'surface-unresolved': 'surface unresolved',
        'date-unresolved': 'date unresolved',
        'analysis-without-finding': 'analysis present, no finding written',
    }
    defect_ribbon = ('<div class="cap-defects">' + ''.join(
        f'<span class="cap-defect cap-defect-{esc(x)}" title="{esc(LABEL.get(x, x))}">{esc(x)}</span>'
        for x in defects) + '</div>') if defects else ''

    # IMAGE SHAPE FOLLOWS THE LEESHARKS GALLERY, which solved this already:
    # ONE thumbnail in the header at a fixed 80x140, the REST inside the expand,
    # and where there is no image a FRAME OF THE SAME SHAPE rather than a line of
    # text — so the column edge never breaks and a missing image is visibly a
    # missing image.
    #
    # Every img carries onerror="this.style.display='none'". Bare filenames used
    # to fall through to the leesharks mirror and 404 for the 312 images that
    # live in THIS repo, which printed a broken-image icon and its alt text as
    # body copy. Unresolved images are now omitted upstream; this is the belt to
    # that braces.
    urls = image_urls(e)
    alt = f'Screen capture for the query &quot;{esc(q)}&quot;, dated {esc(date)}.'
    if urls:
        imgs_html = (
            f'<a class="cap-thumb-link" href="{esc(urls[0])}" target="_blank" rel="noopener">'
            f'<img class="cap-thumb" loading="lazy" src="{esc(urls[0])}" alt="{alt}" '
            f'onerror="this.parentNode.outerHTML=\'<div class=&quot;cap-nothumb&quot;>image<br>404</div>\'">'
            f'</a>')
        extra = urls[1:]
        gallery = ('<div class="cap-gallery">' + "".join(
            f'<a href="{esc(u)}" target="_blank" rel="noopener">'
            f'<img loading="lazy" src="{esc(u)}" alt="{alt}" '
            f'onerror="this.parentNode.style.display=\'none\'"></a>' for u in extra)
            + '</div>') if extra else ''
    else:
        imgs_html = '<div class="cap-nothumb">no<br>image</div>'
        gallery = ''

    return (
        f'<div class="cap-card" id="{esc(slug)}" '
        f'data-section="{esc(e.get("s") or "Unsectioned")}" '
        f'data-status="{esc(mt.split()[0].lower())}" '
        f'data-defects="{esc(" ".join(defects))}" '
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
        f'<div class="cap-row">{imgs_html}'
        f'<div class="cap-body">'
        f'<div class="cap-desc" itemprop="description">{emphasise(d)}</div>'
        f'</div></div>'
        f'{transcript_block(e, gallery)}'
        f'<div class="cap-actions">'
        # THREE ACTIONS, ONE DELEGATED HANDLER. All carry class cap-act; the
        # container binds once. The working page records why: a per-render
        # handler "bound to nothing, and the action was a bare anchor to #slug
        # — it appeared to do nothing because it did nothing."
        f'<button type="button" class="cap-cite cap-act" data-act="cite" '
        f'data-cite="{esc(cite)}" data-citation="{esc(citation)}" '
        f'aria-label="Copy a citation for this capture">¶ Cite</button>'
        # COPY LINK is distinct from cite by design: cite yields something
        # pasteable into a document, this yields the bare address.
        f'<button type="button" class="cap-cite cap-act" data-act="link" '
        f'data-cite="{esc(cite)}" '
        f'aria-label="Copy the permalink to this capture">⛓ Link</button>'
        + rerun_btn +
        f'<a class="cap-permalink" href="{esc(cite)}" rel="bookmark">permalink</a>'
        f'</div>'
        f'{defect_ribbon}'
        f'</div>')


def main():
    if not REG.exists():
        print("SKIP: the Capture Registry is withdrawn from publication (quarantine/capture-registry-20260812/) and under reconstruction; nothing to process.")
        return 0
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
