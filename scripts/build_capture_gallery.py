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



MT_CLASSES = ("ADOPTION", "ZERO RESULT", "ZERO INDEX", "WOUND GAUGE")  # mt values that are evidentiary classes, beside the match

# 2026-10-12: every NESTED reference to the registry carries the fields Google's Dataset report requires —
# description, license, creator. A bare {"@type":"Dataset","name":…} is parsed as a Dataset item of its own and
# reported invalid ('Missing field "description"', 34–35 items in Search Console, 2026-10-09). Same object as the
# record pages' subjectOf reference (wire_deposit.py).
CAPTURE_DATASET_REF = {
    "@type": "Dataset", "@id": "https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json",
    "name": "EA-WG-CAPTURES-01 — the Capture Registry",
    "description": ("Dated captures of how machine surfaces (AI overviews, answer engines, search snippets) retrieved and "
                    "composed from the Crimson Hexagonal Archive; each capture records the query, the surface, the match "
                    "type, and the deposits it drew on."),
    "url": "https://www.alexanarch.org/captures/",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "creator": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
}


def _pd_label(pd):
    """The dimensional PER as one line (PER-dim rubric v1.0, 2026-10-19; v1.1, 2026-10-20): the gate, then PER and PER-M/C/D; the historical
    scalar is shown beside it, never replaced."""
    if not pd:
        return None
    sc = pd.get("scores") or {}
    f = lambda v: "—" if v is None else ("%.2f" % v)
    g = pd.get("gate")
    if g == "abn":
        return "PER undefined (ABN: the answer denies the target)"
    if g in ("control", "no_atom_set"):
        return "PER not scored (%s)" % ("control" if g == "control" else "no atom set")
    lead = "PER %s" % f(sc.get("PER"))
    if g == "target_absent":
        lead += " (target absent: %s)" % pd.get("reached")
    out = lead + " · M %s · C %s · D %s" % (f(sc.get("M")), f(sc.get("C")), f(sc.get("D")))
    # rubric v1.1 (2026-10-20): inversions and standing substitutions are recorded beside the scores
    inv, ss = len(pd.get("inversions") or []), len(pd.get("standing_substitutions") or [])
    if inv:
        out += " · %d inversion%s" % (inv, "" if inv == 1 else "s")
    if ss:
        out += " · %d standing substitution%s" % (ss, "" if ss == 1 else "s")
    if pd.get("tombstone_pointer"):
        out += " · tombstone pointer"
    return out

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

def mark_inline_cites(text):
    """Inline citation markers are invisible inside prose. Mark them ONCE.

    A composed answer carries its attributions as bracketed markers run straight
    into the sentence, so a reader cannot see where the layer attributed and
    where it simply asserted — the distinction this registry exists to measure.

    IDEMPOTENT BY CONSTRUCTION. The first version ran three regexes in sequence,
    and the third matched the [1] that the first had already wrapped, producing
    912 nested spans. This one finds every marker in a SINGLE pass over the
    escaped text and rebuilds the string, so a marker cannot be wrapped twice
    however many times the function is applied.
    """
    out = html.escape(text or "")
    pat = re.compile(
        r'\[\[(\d+)\]\([^)]*\)\]'            # [[1](url)]
        r'|\[(\d+)\]\([^)]*\)'                 # [1](url)
        r'|(?<!\w)\[(\d{1,2}(?:\s*,\s*\d{1,2})*)\](?!\()')   # [1] or [1, 2]
    def wrap(m):
        n = m.group(1) or m.group(2) or m.group(3)
        return f'<span class="cap-inline-cite">[{n}]</span>'
    return pat.sub(wrap, out)


def split_source_strip(text, cites):
    """A paste carries the composed answer AND the source strip, run together.

    The citations are already extracted, so the strip is grep-identifiable. This
    finds where it begins so the answer reads as the answer, WITHOUT altering a
    byte of the verbatim record — only the rendering separates them.

    CAUTION IS THE WHOLE DESIGN HERE. Cutting a transcript in the wrong place
    would silently truncate what the layer said, which is worse than leaving a
    blob. Three guards, all of which must pass:

      1. TWO OR MORE distinct cited sources must be found. One stray match is
         not a strip.
      2. The match must fall in the last 60% of the text.
      3. THE MATCHED STRING MUST NOT APPEAR IN THE FIRST 40%. A title that also
         occurs in the answer body is a phrase the layer used, not a strip
         boundary, and cutting there would amputate the answer.

    Guard 3 is what lets the title floor come down from 14 characters to 10 —
    six transcripts had two or more cited titles sitting uncut in their tails
    purely because the titles were short.
    """
    if not cites or len(text) < 400:
        return text, ""
    floor = int(len(text) * 0.40)
    head = text[:floor]
    marks = []
    for c in cites:
        for key, minlen in ((c.get("title"), 10), ((c.get("snip") or "")[:60], 14), (c.get("site"), 14)):
            k = (key or "").strip()
            if len(k) < minlen:
                continue
            if k in head:            # guard 3 — it is answer text, not a boundary
                continue
            i = text.find(k, floor)
            if i >= 0:
                marks.append(i)
                break
    if len(marks) < 2:
        return text, ""
    cut = min(marks)
    # Never cut so early that the "answer" is shorter than the strip by a wide
    # margin — that pattern means the match was inside the answer after all.
    if cut < len(text) * 0.15:
        return text, ""
    return text[:cut].rstrip(), text[cut:].strip()


def reflow_ocr(text):
    """Render-only normalisation of an OCR stream. THE STORED RECORD IS UNTOUCHED.

    An OCR stream is a screenshot read by a machine: the line breaks are wherever
    the IMAGE wrapped, not where the answer did, so a sentence arrives cut into
    four. Rendering that raw makes the answer look like garble the layer produced,
    when the garble is an artifact of the read.

    Three conservative operations, none of which can lose a character:
      1. Lift the leading `--- filename.png ---` marker out as a caption.
      2. Rejoin a line to the next when the break is MID-SENTENCE — the line does
         not end in terminal punctuation and the next begins lowercase or with a
         continuation. A break before a bullet, a heading, a URL or a capitalised
         new sentence is KEPT, because that break was in the answer.
      3. Collapse runs of blank lines.

    Nothing is deleted. Rejoining inserts a space and never removes text, so the
    rendered string contains every word the OCR produced, in order.
    """
    t = str(text or "")
    cap = ""
    m = re.match(r'\s*---\s*([^\n]+?)\s*---\s*\n', t)
    if m:
        cap = m.group(1)
        t = t[m.end():]
    lines = [l.rstrip() for l in t.split("\n")]
    out = []
    for ln in lines:
        if not ln.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        if not out or out[-1] == "":
            out.append(ln.strip())
            continue
        prev = out[-1]
        starts_new = bool(re.match(r'^([\u2022\-\*\u00b7\u25aa]|\d+[\.\)]|https?:|=|\+|\|)', ln.strip())) \
            or ln.strip()[:1].isupper() and re.search(r'[\.\!\?:]$', prev) \
            or re.match(r'^[A-Z][A-Za-z ]{0,28}:$', ln.strip())
        ends_closed = bool(re.search(r'[\.\!\?:;\u2014]$', prev))
        if starts_new or ends_closed:
            out.append(ln.strip())
        else:
            out[-1] = prev + " " + ln.strip()
    body = "\n".join(out).strip()
    return cap, body


def _urlq(q):
    import urllib.parse
    return urllib.parse.quote_plus(str(q or ""))


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
    if not (reading or analysis or tr or cites or coll or oq or gallery or e.get("findings")):
        return ""

    meta = {
        "captured": e.get("date"), "surface": e.get("surface"),
        "auth state": e.get("auth"), "evidence class": e.get("ev"),
        "PER (dimensional, rubric v1.1)": _pd_label(e.get("per_dim")) if (e.get("per_dim") or {}).get("spec") == "PER-dim rubric v1.1" else None,
        "PER (dimensional, rubric v1.0)": _pd_label(e.get("per_dim_v1_0") or (e.get("per_dim") if (e.get("per_dim") or {}).get("spec") != "PER-dim rubric v1.1" else None)),
        "PER (historical scalar)": e.get("per"),
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
        # 2026-09-30 (operator ruling): the label is plain 'Rounds'. The old warning, 'this record is a ROUND,
        # not a capture', was written for records that had split one session across several entries; it rendered
        # on every multi-round capture, where it is false.
        parts.append('<div class="cap-tr-label">Rounds</div>'
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
             "PER (dimensional, rubric v1.1)": "meas", "PER (dimensional, rubric v1.0)": "meas", "PER (historical scalar)": "meas", "PER units retained": "meas", "failure modes": "meas", "citations read": "meas",
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
    # FINDINGS INSIDE THE EXPAND (2026-09-30, operator ruling: "bullet point entries should be displayed
    # elsewhere, not randomly strewn about"). From 2026-09-05 they rendered on the card face below the actions,
    # so the 102 entries carrying them read differently from every other card. They sit here, after Reading
    # and before Analysis, as analyst text beside analyst text. The data field is unchanged.
    findings = e.get("findings") or []
    if findings:
        parts.append('<div class="cap-tr-label">Findings</div>'
                     '<ul class="cap-tr-prose cap-findings">' + ''.join(f'<li>{esc(x)}</li>' for x in findings) + '</ul>')
    if analysis:
        parts.append('<div class="cap-tr-label">Analysis '
                     '<span class="cap-tr-warn">analyst prose, not machine text</span></div>'
                     f'<div class="cap-tr-prose">{para(analysis)}</div>')
    if coll:
        rows = "".join(
            f'<li><b>{esc(str(c.get("with") or ""))}</b>'
            f'<div class="cap-cn">via {esc(str(c.get("via") or ""))}</div>'
            + (f'<div class="cap-cs">{esc(str(c["ev"]))}</div>' if c.get("ev") else '')
            + '</li>' for c in coll)
        parts.append('<div class="cap-tr-label">Collision register</div>'
                     f'<ul class="cap-cites">{rows}</ul>')
    if tr:
        cls = e.get("transcript_class") or ""
        note = " · ".join(x for x in (cls, e.get("transcript_complete"), e.get("transcript_read")) if x)
        answer, strip = split_source_strip(tr, cites)
        # AN OCR STREAM IS NOT A VERBATIM TRANSCRIPT. It is a screenshot read by a
        # machine, with browser furniture, header chrome and page tail mixed into
        # the answer, line breaks wherever the image wrapped, and character errors
        # throughout. Calling it "machine text, verbatim" invites a reader to
        # treat garble as something the layer said. It is labelled for what it is.
        _isocr = (e.get("ev") == "ocr") or ("OCR" in str(cls).upper())
        _ocap, _obody = reflow_ocr(answer) if _isocr else ("", "")
        _lbl = ('OCR stream <span class="cap-tr-warn">screenshot read by machine &mdash; '
                'chrome, line breaks and character errors are artifacts of the read, '
                'NOT of the answer</span>') if _isocr else 'Machine text, verbatim'
        parts.append(f'<div class="cap-tr-label">{_lbl}</div>'
                     + (f'<div class="cap-tr-warn-line">{esc(note)}</div>' if note else '')
                     + (('<div class="cap-ocr-cap">' + esc(_ocap) + '</div>' if _ocap else '')
                        + f'<div class="cap-tr-body cap-tr-ocr" itemprop="text">{esc(_obody)}</div>'
                        if _isocr else
                        f'<div class="cap-tr-body" itemprop="text">{mark_inline_cites(answer)}</div>'))
        # The strip is no longer rendered separately — each segment now sits with
        # its own source above, so the reader sees one list, not two.
    # EACH DATED OBSERVATION EXPANDS ON ITS OWN. A record observed twice is two
    # encounters; a flat list gave no way to read one without the others, and no
    # way to tell them apart at a glance. Each is its own <details>, anchored on
    # its own slug, so a link to an observation opens that observation.
    _obs = e.get("observations") or []
    if len(_obs) > 1:
        _rows = ""
        for _i, _o in enumerate(_obs, 1):
            _bits = " &middot; ".join(x for x in (
                str(_o.get("surface") or ""), str(_o.get("auth") or ""),
                ("%s evidence" % _o["ev"]) if _o.get("ev") else "",
                ("%s sources" % _o["cites"]) if _o.get("cites") else "sources not captured",
                _pd_label(_o.get("per_dim")) or "",
                ("historical PER %s" % _o["per"]) if _o.get("per") is not None else "") if x)
            _in = ""
            if _o.get("d"):
                _in += f'<div class="cap-obsfind">{emphasise(str(_o["d"]))}</div>'
            if _o.get("defects"):
                _in += ('<div class="cap-defects">' +
                        "".join(f'<span class="cap-defect">{esc(x)}</span>' for x in _o["defects"]) +
                        '</div>')
            if _o.get("reading"):
                _in += ('<div class="cap-tr-label">Reading</div>'
                        f'<div class="cap-tr-prose">{para(_o["reading"])}</div>')
            _av = _o.get("availability")
            if _av:
                # COMPOSITIONAL SUBSTITUTION UNDER AVAILABILITY (#740 §2.3, operationalised 2026-10-19): the conditions,
                # each read off the record and cited, never weighted; the reached kind is the reading's
                _in += ('<div class="cap-tr-label">Availability <span class="cap-tr-warn">#740 §2.3 · '
                        + esc(str(_av.get("class") or "conditions not all held")) + '</span></div>'
                        + '<ul class="cap-cites">' + "".join(f'<li>{esc(str(h))}</li>' for h in _av.get("held") or [])
                        + "".join(f'<li><i>not held:</i> {esc(str(h))}</li>' for h in _av.get("not_held") or []) + '</ul>'
                        + (f'<div class="cap-cn">reached: {esc(str(_av.get("reached")))}</div>' if _av.get("reached") else '')
                        + (f'<div class="cap-cn">{esc(str(_av.get("basis")))}</div>' if _av.get("basis") else ''))
            if _o.get("transcript"):
                _ans, _ = split_source_strip(_o["transcript"], _o.get("cite_list") or [])
                _in += ('<div class="cap-tr-label">Machine text, verbatim</div>'
                        f'<div class="cap-tr-body">{mark_inline_cites(_ans)}</div>')
            _oc = _o.get("cite_list") or []
            if _oc:
                _r = ""
                for _c in _oc:
                    _nm = esc(str(_c.get("site") or "source"))
                    _hd = (f'<a href="{esc(_c["url"])}" target="_blank" rel="noopener">{_nm}</a>'
                           if _c.get("url") else f'<b>{_nm}</b>')
                    _r += ('<li><div class="cap-srchead">' + _hd
                           + (f' <span class="cap-rel">{esc(str(_c.get("rel") or ""))}</span>' if _c.get("rel") else '')
                           + '</div>'
                           + (f'<div class="cap-ct">{esc(str(_c["title"]))}</div>' if _c.get("title") else '')
                           + (f'<div class="cap-cs">{esc(str(_c["snip"]))}</div>' if _c.get("snip") else '')
                           + '</li>')
                _in += (f'<div class="cap-tr-label">Sources ({len(_oc)})</div>'
                        f'<ol class="cap-srclist">{_r}</ol>')
            elif "citations-null" in (_o.get("defects") or []):
                _in += ('<div class="cap-tr-label">Sources</div>'
                        '<div class="cap-tr-warn-line">NOT CAPTURED \u2014 count is NULL, not zero.</div>')
            if _o.get("analysis"):
                _in += ('<div class="cap-tr-label">Analysis '
                        '<span class="cap-tr-warn">analyst prose, not machine text</span></div>'
                        f'<div class="cap-tr-prose">{para(_o["analysis"])}</div>')
            # DO NOT REPEAT THE CARD'S OWN ID. An address slug is inherited
            # from whichever observation was seated first, so on 104 addresses
            # that observation's <details> carried the same id as the card that
            # contains it — invalid HTML, and #slug is ambiguous between the two.
            # The card already anchors it, so the capture remains citable at
            # exactly the same URL; only the redundant inner id is dropped.
            # read the card slug from the entry: the local `slug` is not bound
            # until line ~482, well below this block
            _oid = (f' id="{esc(_o["slug"])}"'
                    if _o.get("slug") and _o["slug"] != e.get("slug") else "")
            _rows += (f'<details class="cap-obs"{_oid}>'
                      f'<summary><b>{esc(str(_o.get("date") or "undated"))}</b> '
                      f'<span class="cap-obsn">observation {_i} of {len(_obs)}</span> '
                      f'<span class="cap-rel">{_bits}</span></summary>'
                      f'<div class="cap-obsbody">{_in}</div></details>')
        parts.insert(0, f'<div class="cap-tr-label">Observations ({len(_obs)}) '
                        '<span class="cap-tr-warn">one record &mdash; each encounter opens on its own</span></div>'
                        f'<div class="cap-obswrap">{_rows}</div>')

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
    if cites:
        # ONE CITATION SECTION, NOT THREE. The extracted card and its as-pasted
        # segment are THE SAME SOURCE seen two ways — what the layer showed, and
        # what the copy produced. Splitting them across "Sources as cited" and
        # "Source strip" made two lists of the same thing and left the reader to
        # match them up. They are merged here, one entry per source.
        strip_for = {}
        if tr:
            _, _strip = split_source_strip(tr, cites)
            if _strip:
                cuts = []
                for c in cites:
                    for key in (c.get("title"), c.get("site")):
                        k = (key or "").strip()
                        if len(k) < 8:
                            continue
                        i = _strip.find(k)
                        if i >= 0:
                            cuts.append((i, c))
                            break
                cuts.sort(key=lambda z: z[0])
                for n_, (i, c) in enumerate(cuts):
                    j = cuts[n_ + 1][0] if n_ + 1 < len(cuts) else len(_strip)
                    strip_for[id(c)] = _strip[i:j].strip()
                if cuts and cuts[0][0] > 0:
                    strip_for["__unattributed__"] = _strip[:cuts[0][0]].strip()
        rows = ""
        for c in cites:
            nm = esc(str(c.get("site") or "source"))
            head = (f'<a href="{esc(c["url"])}" target="_blank" rel="noopener">{nm}</a>'
                    if c.get("url") else f'<b>{nm}</b>')
            rel = esc(str(c.get("rel") or ""))
            seg = strip_for.get(id(c))
            rows += ('<li>'
                     f'<div class="cap-srchead">{head}'
                     + (f' <span class="cap-rel">{rel}</span>' if rel else '') + '</div>'
                     + (f'<div class="cap-ct">{esc(str(c["title"]))}</div>' if c.get("title") else '')
                     + (f'<div class="cap-cs">{esc(str(c["snip"]))}</div>' if c.get("snip") else '')
                     + (f'<div class="cap-cn">{esc(str(c["note"]))}</div>' if c.get("note") else '')
                     + (f'<div class="cap-aspasted"><span class="cap-aspasted-l">as pasted</span>'
                        f'{esc(seg)}</div>' if seg else '')
                     + '</li>')
        un = strip_for.get("__unattributed__")
        if un:
            rows += ('<li><div class="cap-srchead cap-srchead-un"><b>unattributed segment</b> '
                     '<span class="cap-rel">no cited source matches this text</span></div>'
                     f'<div class="cap-aspasted">{esc(un)}</div></li>')
        parts.append(f'<div class="cap-tr-label">Sources ({len(cites)}) '
                     '<span class="cap-tr-warn">as cited, and as the copy produced them</span></div>'
                     f'<ol class="cap-srclist">{rows}</ol>')

    if oq:
        parts.append('<div class="cap-tr-label">Open questions</div>'
                     '<ul class="cap-cites">' + "".join(f'<li>{esc(str(x))}</li>' for x in oq) + '</ul>')
    n = sum(len(x) for x in (reading, analysis, tr))
    # NULL IS NOT ZERO. A record whose citation apparatus was never captured has
    # an UNKNOWN source count, not a count of nought. Writing "0 sources" on a
    # card that also carries the citations-null defect makes the interface
    # contradict the measurement it is displaying.
    if cites:
        srcs = f', {len(cites)} sources'
    elif "citations-null" in (e.get("defects") or []):
        srcs = ', sources not captured'
    else:
        srcs = ', 0 sources'
    return ('<details class="cap-transcript"><summary>Full record'
            + (f' \u2014 {n:,} characters{srcs}' if n else '')
            + '</summary>' + "".join(parts) + '</details>')

def card(e, record=False):
    """One capture card. record=True renders it for the capture's own record page
    (build_capture_records.py, 2026-10-01): the finding uncut and the full record open."""
    esc = html.escape
    slug = e.get("slug", "")
    # THE CARD CUTS ITS OWN BLURB. The full finding lives in the data so every
    # renderer can choose; cutting upstream gave three mirrors a 330-character
    # stub they could not undo.
    _dfull = str(e.get("d") or "")
    if len(_dfull) > 330 and not record:
        _cut = _dfull[:330]
        _m = re.search(r'[\.\!\?\u2014;]\s[^\.]*$', _cut)
        _cut = _cut[:_m.start() + 1] if _m and _m.start() > 180 else _cut.rsplit(' ', 1)[0]
        d = _cut.rstrip(' ,;\u2014-') + '\u2026'
    else:
        d = _dfull
    mt = e.get("mt") or "unrated"
    # THE STATUS IS THE ADDRESS'S MATCH (2026-10-11): `match`, read off the address at intake ("exact is quoted. broad is
    # unquoted."). mt had come to hold CAPTURE and descriptive titles, which rendered as statuses ('the', 'deleuze'); it now
    # adds a second badge only where it carries an evidentiary class of its own.
    match = e.get("match") or "INDETERMINATE"
    mt_class = next((c for c in MT_CLASSES if str(mt).startswith(c)), None)
    status_attr = match + ("|" + mt_class if mt_class else "")
    q = e.get("q") or slug
    date = e.get("date") or ""
    cite = e.get("cite") or f"https://www.alexanarch.org/captures/{slug}/"

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
    # RE-RUN DEFAULTS TO GENERAL SEARCH. MANUS: "general search should be
    # default." AI Mode is a SECOND button, offered only where AI Mode was a
    # native capture surface for this record — never the default, because the
    # default must not pre-decide the surface being measured.
    #
    # INCOGNITO CANNOT BE OPENED FROM A LINK. No web page may open a private
    # window: it is a browser security boundary with no parameter and no API.
    # The Link button copies the URL so it can be pasted into one. pws=0 is NOT
    # used — it is undocumented and unverified, and an unverified parameter on a
    # measurement URL is exactly the kind of thing that manufactures a finding.
    _q = e.get("q") or ""
    _base = ("https://www.google.com/search?q=" + _urlq(_q)) if _q else ""
    _surfaces = e.get("surfaces") or []
    rerun_btn = ""
    if _base:
        rerun_btn = (f'<a class="cap-cite cap-act cap-rerun" data-act="rerun" '
                     f'data-rerun="{esc(_base)}" href="{esc(_base)}" target="_blank" rel="noopener" '
                     f'title="Runs this query in general Google search. To run it signed out, copy '
                     f'the link and open it in a private window — a page cannot open one for you.">'
                     f'\u21bb Re-run</a>')
        _alt = e.get("rerun_alt")
        if _alt:
            # THE OTHER FORM OF THE SAME ADDRESS. Quoting is the decisive measured
            # variable here, and the two forms have come apart entirely on at
            # least one term. One click puts them side by side.
            _au = "https://www.google.com/search?q=" + _urlq(_alt["q"])
            rerun_btn += (f'<a class="cap-cite cap-act cap-rerun cap-rerun-alt" data-act="rerun" '
                          f'data-rerun="{esc(_au)}" href="{esc(_au)}" target="_blank" rel="noopener" '
                          f'title="{esc(_alt["why"])}">\u21bb {esc(_alt["label"])}</a>')
        if any("AI Mode" in str(x) for x in _surfaces):
            _ai = _base + "&udm=50"
            rerun_btn += (f'<a class="cap-cite cap-act cap-rerun cap-rerun-ai" data-act="rerun" '
                          f'data-rerun="{esc(_ai)}" href="{esc(_ai)}" target="_blank" rel="noopener" '
                          f'title="AI Mode was a native capture surface for this record.">'
                          f'\u21bb AI Mode</a>')

    # THE DEFECT RIBBON IS ON THE FACE OF THE CARD, not behind an expander.
    # MANUS: "if its invisible i wont check it, if i dont check it it will
    # drift." Every defect here was invisible when it happened.
    defects = e.get("defects") or []
    LABEL = {
        'truncated-by-interface': 'answer truncated by interface — absence here is absence from the VISIBLE portion',
        'unsupported-citations': 'CITATIONS UNSUPPORTED by this transcript — do not count',
        'citations-null': 'citation apparatus not captured — count is NULL, not zero',
        'citations-unextracted': 'citations counted but no source card extracted — sources not resolvable to deposits',
        'surface-unresolved': 'surface unresolved',
        'date-unresolved': 'date unresolved',
        'analysis-without-finding': 'analysis present, no finding written',
    }
    defect_ribbon = ('<div class="cap-defects">' + ''.join(
        f'<span class="cap-defect cap-defect-{esc(x)}" title="{esc(LABEL.get(x, x))}">{esc(x)}</span>'
        for x in defects) + '</div>') if defects else ''
    # FINDINGS (2026-09-05): editorial sentences that used to sit in `defects` and rendered as orange chips.
    # From 2026-09-30 they render inside the expand (transcript_block), not on the card face.

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
    ds = e.get("dates") or ([date] if date else [])
    datespan = (f"{ds[0]} \u2013 {ds[-1]}  ({len(e.get('observations') or [])} obs)"
                if len(ds) > 1 else (ds[0] if ds else ""))

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

    # EVERY CAPTURE GETS AN ANCHOR, INCLUDING THE SOLITARY ONES.
    # ONE SURFACE + ONE SEMANTIC ADDRESS + ONE DATE = ONE CAPTURE, citable at
    # captures/#{observation_slug}. Multi-observation addresses take that anchor
    # from the <details> above. A SINGLE-observation address renders no <details>,
    # so when its one observation carries a slug of its own — three do, named for
    # what they found rather than for the address — that slug resolved nowhere
    # and the capture could not be cited.
    # ONLY WHERE NO <details> RENDERS. A multi-observation address already
    # anchors each capture on its own <details class="cap-obs" id="{slug}">, so
    # emitting an alias there produces TWO elements with the same id — invalid
    # HTML, and the browser jumps to whichever comes first. That is what happened
    # when this guard was dropped on 2026-08-14: ~240 duplicate ids. The alias
    # exists solely for the SOLITARY case, where no <details> is written and an
    # observation slug that differs from the card id would otherwise resolve
    # nowhere.
    # ORIGINATOR (2026-09-25): whose entity the query asks about, when ruled — on the face of the card, as a
    # data attribute a filter can use, and as microdata. Out-universe entities must not read as the archive's own.
    _o = e.get("originator") or {}
    _rel = {"archive": "inside the archive", "external": "outside the archive (out-universe)",
            "none": "no originated entity"}.get(_o.get("relation"), _o.get("relation") or "")
    origin_line = ""
    if _o:
        _bits = [x for x in (_o.get("name"), _rel, _o.get("entity_type")) if x]
        _tr = f' · SPXI treatment: {_o["spxi_treatment"]}' if _o.get("spxi_treatment") else ""
        origin_line = (f'<div class="cap-origin" style="font-size:.8em;color:#666;margin:2px 0 4px">'
                       f'Originator: {esc(" · ".join(_bits))}{esc(_tr)}</div>'
                       f'<meta itemprop="about" content="{esc(" · ".join(_bits))}">')

    # NOTICE (2026-10-23): a dated notice the operator attaches to a capture (e.g. SPXI treatment of the entity discontinued).
    # Authored apparatus on the face of the card; the captured composition is untouched.
    _nt = e.get("notice") or {}
    notice_line = ""
    if _nt.get("text"):
        notice_line = (f'<div class="cap-notice" style="font-size:.82em;border-left:3px solid #b08;padding:3px 8px;margin:4px 0 6px">'
                       f'<strong>Notice, {esc(_nt.get("date_label") or _nt.get("date") or "")}.</strong> {esc(_nt["text"])}</div>')

    # THE RECORD THE RUN WAS MEANT TO REACH (2026-10-11). Operator: "captures would need to include links to the title and link they
    # were *supposed* to point to, even when they dont appear in overview cards". A title or identifier run carries `intended`; the
    # card links the record and its exact-title search, and says whether the composition cited the record page.
    _it = e.get("intended") or {}
    intended_line = ""
    if _it.get("record"):
        # 2026-10-12: reached is absent when the capture's cards were never extracted — unknown, not false
        _reach = ("whether the composition cited it is not recorded (its source cards were not extracted)" if "reached" not in _it
                  else "cited in the composition" if _it["reached"] else "not cited in the composition")
        _srch = (f' · <a href="{esc(_it["search"])}" target="_blank" rel="noopener">Search this title</a>'
                 if _it.get("search") else "")
        if _it.get("search_exact"):
            _srch += f' <a href="{esc(_it["search_exact"])}" target="_blank" rel="noopener">(exact match)</a>'
        intended_line = (f'<div class="cap-intended" style="font-size:.8em;color:#666;margin:2px 0 4px">'
                         f'Intended record: <a href="{esc(_it["record"])}" itemprop="mentions">#{esc(str(_it.get("deposit") or ""))}'
                         f' — {esc(_it.get("title") or "")}</a>{_srch} · {_reach}</div>')

    _obs_all = e.get("observations") or []
    _alias = "".join(
        '<span class="cap-alias" id="%s"></span>' % esc(_o["slug"])
        for _o in _obs_all
        if len(_obs_all) == 1 and _o.get("slug") and _o["slug"] != slug
    )

    return (
        f'<div class="cap-card" id="{esc(slug)}" '
        f'data-section="{esc(e.get("s") or "Unsectioned")}" '
        f'data-status="{esc(status_attr)}" '
        f'data-defects="{esc(" ".join(defects))}" '
        f'data-origin="{esc(_o.get("relation") or "")}" '
        f'itemscope itemtype="https://schema.org/CreativeWork">' + _alias +
        f'<meta itemprop="identifier" content="{esc(cite)}">'
        f'<meta itemprop="isPartOf" content="EA-WG-CAPTURES-01">'
        f'<meta itemprop="creator" content="Sharks, Lee">'
        f'<meta itemprop="citation" content="{esc(citation)}">'
        f'<div class="cap-head"><span class="cap-section">{esc(e.get("s") or "Unsectioned")}</span>'
        f'<span class="cap-date" itemprop="dateCreated">{esc(datespan)}</span></div>'
        f'<div class="cap-query" itemprop="name">{esc(e.get("q") or "")}</div>' + origin_line + notice_line + intended_line +
        f''
        f'<div class="cap-status-row">'
        f'<span class="cap-status cap-status-{esc(match.replace(" ", "-"))}">{esc(match)}</span>'
        + (f'<span class="cap-status cap-status-{esc(mt_class.replace(" ", "-"))}">{esc(mt_class)}</span>' if mt_class else '') +
        f'<span class="cap-sf">{esc(e.get("sf") or "")}</span></div>'
        f'<div class="cap-row">{imgs_html}'
        f'<div class="cap-body">'
        f'<div class="cap-desc" itemprop="description">{emphasise(d)}</div>'
        f'</div></div>'
        f'{(transcript_block(e, gallery).replace("<details class=\"cap-transcript\">", "<details class=\"cap-transcript\" open>", 1) if record else transcript_block(e, gallery))}'
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
    # ORDER IS THE PROJECTOR'S (2026-09-05): the gallery renders entries A–Z by the ISSUED query — leading
    # quote/whitespace stripped for ordering only, numeric-aware, accent/case/punctuation-insensitive;
    # date then slug break ties. Deterministic. Seating cannot disturb this, wherever it lands in the file.
    import unicodedata as _ud, re as _re
    def _qkey(e):
        q = str(e.get("q") or "").lstrip('«"\'‘’“” \t').strip()
        q = "".join(ch for ch in _ud.normalize("NFKD", q) if not _ud.combining(ch)).lower()
        q = "".join(ch for ch in q if ch.isalnum() or ch.isspace())
        return [(0, int(t)) if t.isdigit() else (1, t) for t in _re.split(r"(\d+)", q)]
    # A–Z ACROSS THE WHOLE GALLERY by issued query (the rule #74 established and the operator merged);
    # sections remain as filter chips, not as display blocks. The FILE stays grouped by section (intake
    # inserts into its section; check_capture_registry ORDER); file order and display order are decoupled.
    entries = sorted(entries, key=lambda e: (_qkey(e), str(e.get("date") or ""), e.get("slug") or ""))
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
        extras = "".join(
            f'<div style="color:var(--dim);margin-top:5px">{html.escape(flow[k])}</div>'
            for k in ("writing_to_this_file", "version_moves_with_content", "surface_discrimination")
            if flow.get(k))
        # COLLAPSED <details>, NOT AN OPEN <section>. The page carried a
        # hand-written <details id="capture-flow"> that this emitter's removal
        # regex — which matched only its own <section> form — could not see. When
        # _FLOW was added to the projection on 2026-08-14 the dormant emitter
        # woke and produced a SECOND block: same id, half-empty, because it reads
        # READ_THIS_FIRST/source_of_truth/flow/citation and the new _FLOW used
        # different key names. Two blocks, one duplicate id, labels with nothing
        # after them. One block now, generated from data, in the form the page
        # already used.
        flow_html = (
            '<details id="capture-flow" class="cap-flow"><summary>Capture registry — data flow '
            '<span class="cap-flow-tag">machine-facing</span></summary><div class="cap-flow-body">'
            f'<div style="color:var(--dim);margin-bottom:8px">{html.escape(flow.get("READ_THIS_FIRST",""))}</div>'
            f'<div><b>Source of truth:</b> <code>{html.escape(flow.get("source_of_truth",""))}</code></div>'
            f'<ol style="margin:8px 0 8px 1.1em;padding:0">{steps}</ol>'
            f'<div style="color:var(--dim)"><b>Citation:</b> {html.escape(flow.get("citation",""))}</div>'
            f'<div style="color:var(--dim);margin-top:5px">{html.escape(flow.get("slugs_are_permanent",""))}</div>'
            + extras +
            '<div style="margin-top:8px"><a href="/data/EA-WG-CAPTURES-01.json">the registry itself</a>'
            ' &middot; <a href="/datasets/capture-registry/">published dataset</a></div>'
            '</div></details>')
        ld_flow = ('<script type="application/ld+json">' +
                   json.dumps({"@context":"https://schema.org","@type":"CreativeWork",
                               "name":"Capture registry data flow",
                               "isPartOf":CAPTURE_DATASET_REF,
                               "text":flow.get("READ_THIS_FIRST",""),
                               "step":flow.get("flow",[]),
                               "url":"https://www.alexanarch.org/captures/#capture-flow"},
                              ensure_ascii=False) + "</script>")
        # remove BOTH historical forms, or the old one survives beside the new one
        page = re.sub(r'<section id="capture-flow".*?</section>\n?', "", page, flags=re.S)
        page = re.sub(r'<details id="capture-flow".*?</details>\n?', "", page, flags=re.S)
        page = re.sub(r'<script type="application/ld\+json">\{"@context": ?"https://schema.org", ?"@type": ?"CreativeWork".*?</script>\n?', "", page, flags=re.S)
        # ABOVE THE COUNT, NOT BELOW THE FILTERS. The flow block states what may
        # write to this registry and what merely renders from it. A reader — or a
        # program — meets the filters and the card list first and forms the idea
        # that this is a place to write before ever reaching the rule. It belongs
        # ahead of the count, where the surface introduces itself.
        marker = '<div class="stats" id="stats">'
        if marker not in page:                       # fall back to the old anchor
            marker = '<div id="captures">'
        if marker in page:
            page = page.replace(marker, flow_html + "\n" + ld_flow + "\n" + marker, 1)

    # SUPERSESSION, VISIBLE (2026-09-25). Composition surfaces kept reporting a severed Zenodo release as the
    # registry. The current version and the supersession statement sit above the count, as text a crawler
    # reads without executing anything. Idempotent: the previous line is removed before the new one is placed.
    sup = r.get("_supersedes") or {}
    # The registry's own count (intake keeps observation_count); the page used to recount, taking an address
    # with no observation list as one, and drifted (846 against 848 at v12.202).
    n_obs = r.get("observation_count") or sum(len(x.get("observations") or []) or 1 for x in entries)
    page = re.sub(r'<p id="cap-current"[^>]*>.*?</p>\n?', "", page, flags=re.S)
    if sup.get("statement"):
        # CANONICAL, STATED FIRST (ruling, Lee Sharks, 2026-10-01: "we need to make it clearer that
        # alexanarch/captures is canonical"). A composition surface named a window as the live registry and a
        # severed Zenodo release as its record. The statement now sits directly under the introduction, ahead
        # of the data-flow notes, with the counts computed here so they cannot go stale, and it names the two
        # routes a fetcher with a size ceiling can use: the table of contents and the per-capture record pages.
        # ONE DESCRIPTION (operator, 2026-10-14: "can we compress these into one description?"). The fixed
        # introduction (<p class="sub">, deposit #3, semantic address, observation, windows) and this canonical
        # statement are merged here; the introduction is removed from the page so the two cannot drift apart.
        page = re.sub(r'<p class="sub">The <a href="/records/\?id=3">Capture Registry</a> \(deposit #3\) records .*?</p>\n?', "", page, count=1, flags=re.S)
        last = sup.get("last_severed_count")
        cur = (f'<p id="cap-current" style="font-size:.9em;margin:8px 0 12px;padding:8px 10px;border-left:3px solid var(--teal)">'
               f'<b>The canonical Capture Registry (EA-WG-CAPTURES-01, <a href="/records/?id=3">deposit #3</a>): version '
               f'{html.escape(str(r.get("version") or ""))}, {html.escape(str(r.get("date") or ""))}; {len(entries)} addresses, {n_obs} observations.</b> '
               f'It records MACHINE-MEDIATED RECEPTION EVENTS across composition, retrieval, selection, aggregation and related computational '
               f'surfaces. Each record is a SEMANTIC ADDRESS; each dated encounter with it is an OBSERVATION with its own conditions, evidence '
               f'(the original images, where captured), sources, measurements and reading. Each capture is cited at its record page, '
               f'<code>/captures/{{slug}}/</code>; each query has a page at <a href="/addresses/">/addresses/</a>; the table of contents is '
               f'<a href="/captures/index.json">/captures/index.json</a>. <a href="https://www.godkinggoogle.com/captures/">godkinggoogle.com</a>, '
               f'<a href="https://www.leesharks.com/captures/">leesharks.com</a> and <a href="https://www.machinemediation.org/captures/">machinemediation.org</a> '
               f'are windows that render from this registry and hold no copy. It supersedes every Zenodo release '
               f'({html.escape(str(sup.get("severed_releases") or "v1.1–v8.3")).replace("Zenodo ", "")}{f", the last at {last} captures" if last else ""}), '
               f'severed when the host terminated the account on {html.escape(str(sup.get("severed_on") or "2026-06-19"))}; any count, version or finding read '
               f'from those releases is out of date.</p>')
        _mk = '<details id="capture-flow"'
        if _mk not in page:
            _mk = '<div class="stats" id="stats">'
        if _mk not in page:
            _mk = '<div id="captures">'
        if _mk in page:
            page = page.replace(_mk, cur + "\n" + _mk, 1)
    # THE COMPLETE INDEX, EARLY (2026-10-15). The page is ~12.6 MB of HTML and Googlebot reads the first
    # 2 MB of an HTML resource (Google, "Inside Googlebot", March 2026); links to only 108 of the 666 capture
    # records fell inside that prefix, the rest beyond where the crawler stops. One plain-HTML row per
    # address — the issued query, its record page, dates, surfaces — sits directly under the canonical
    # statement, ahead of the data-flow notes and the cards, so every record is linked within the first
    # ~0.25 MB. Collapsed for a reader; ordinary markup for a fetcher. Same A–Z order as the cards. Each row
    # links the capture's own record page (/captures/{slug}/, cf. build_capture_records.record_url) and its
    # card on this page (#slug). The cards, their anchors and the record pages are untouched.
    IDX_B, IDX_E = "<!-- CAP-INDEX-BEGIN -->", "<!-- CAP-INDEX-END -->"
    page = re.sub(re.escape(IDX_B) + r".*?" + re.escape(IDX_E) + r"\n?", "", page, flags=re.S)
    _rows = []
    for e in entries:
        _slug = e.get("slug") or ""
        _ds = sorted({str(x) for x in (e.get("dates") or [e.get("date")]) if x})
        _sf = [str(x) for x in (e.get("surfaces") or [e.get("surface")]) if x]
        _dt = _ds[0] if len(_ds) < 2 else f"{_ds[0]} – {_ds[-1]} ({len(_ds)})"
        _rows.append(f'<li><a href="/captures/{html.escape(_slug)}/">{html.escape(str(e.get("q") or _slug))}</a>'
                     f' <span class="ci-m">{html.escape(_dt)} · {html.escape(", ".join(dict.fromkeys(_sf)))}'
                     f' · <a href="#{html.escape(_slug)}">card</a></span></li>')
    cap_index = (f'{IDX_B}\n<details id="cap-index" style="font-size:.88em;margin:0 0 12px">'
                 f'<summary><b>Index of all {len(entries)} addresses</b> — each links its record page '
                 f'(<code>/captures/{{slug}}/</code>) and its card below</summary>'
                 f'<style>#cap-index ol{{margin:8px 0 0 1.4em;padding:0;line-height:1.5}}'
                 f'#cap-index .ci-m{{color:var(--dim);font-size:.9em}}</style>'
                 f'<ol>' + "".join(_rows) + f'</ol></details>\n{IDX_E}\n')
    for _mk in ('<details id="capture-flow"', '<div class="stats" id="stats">', '<div id="captures">'):
        if _mk in page:
            page = page.replace(_mk, cap_index + _mk, 1)
            break

    # TITLE AND DESCRIPTION FROM THE DATA (2026-10-01). The title carried a name nobody searches
    # ("AI Overview Captures") and the description counts frozen at 453 / 401.
    page = re.sub(r'<title>.*?</title>', '<title>AI Overview Capture Registry (EA-WG-CAPTURES-01) — canonical record — Alexanarch</title>', page, count=1, flags=re.S)
    _desc = (f'The canonical, current Capture Registry (EA-WG-CAPTURES-01), version {r.get("version")}, {r.get("date")}: '
             f'{len(entries)} addresses and {n_obs} dated observations of how machine composition surfaces compose named entities. '
             f'Supersedes every Zenodo release (v1.1–v8.3, severed 2026-06-19). Table of contents at /captures/index.json; '
             f'each capture at /captures/{{slug}}/.')
    page = re.sub(r'<meta name="description" content="[^"]*">', lambda _: f'<meta name="description" content="{html.escape(_desc)}">', page, count=1)

    # JSON-LD: the registry described as a dataset, once
    ld = {
        "@context": "https://schema.org", "@type": "Dataset",
        "name": "AI Overview Capture Registry (EA-WG-CAPTURES-01)",
        "description": ("Dated observations of how machine composition layers — AI Overviews, "
                        "AI Mode, ChatGPT and comparable surfaces — compose named entities: the "
                        "Alexanarch corpus and entities originated outside it (each entry's originator "
                        "says whose). Each capture records the query, the sources the layer cited, what "
                        "it rendered, and the date, and is individually citable by its slug. "
                        + ((r.get("_supersedes") or {}).get("statement") or "")).strip(),
        "url": "https://www.alexanarch.org/captures/",
        "identifier": "EA-WG-CAPTURES-01",
        "version": r.get("version"), "dateModified": r.get("date"),
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {"@type": "Person", "name": "Lee Sharks",
                    "identifier": "https://orcid.org/0009-0000-1599-0703"},
        "alternateName": ["AI Overview Capture Registry", "The Capture Registry", "EA-WG-CAPTURES-01"],
        "isAccessibleForFree": True,
        "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json",
                          "name": "table of contents — one row per capture, with each record's URL",
                          "contentUrl": "https://www.alexanarch.org/captures/index.json"},
                         {"@type": "DataDownload", "encodingFormat": "application/json",
                          "name": "the full registry in one file",
                          "contentUrl": "https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json"}],
        "size": f"{len(entries)} addresses, {sum(len(x.get('observations') or []) or 1 for x in entries)} observations",
    }
    ldblock = ('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False)
               + "</script>\n")
    signposts = (
        '<link rel="describedby" href="https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json" type="application/json">\n'
        '<link rel="item" href="https://www.alexanarch.org/data/EA-WG-CAPTURES-01.json" type="application/json">\n'
        '<link rel="alternate" href="https://www.alexanarch.org/captures/index.json" type="application/json" title="table of contents">\n'
        '<link rel="cite-as" href="https://www.alexanarch.org/captures/">\n')
    # Strip only the Dataset block. A blanket strip also removed the data-flow
    # declaration emitted moments earlier — the flow is the thing this file exists
    # to make unmissable, and a cleanup regex was quietly deleting it.
    page = re.sub(r'<script type="application/ld\+json">\s*\{"@context":\s*"https://schema\.org",\s*"@type":\s*"Dataset".*?</script>\n?', "", page, flags=re.S)
    page = re.sub(r'<link rel="(describedby|item|cite-as)"[^>]*>\n?', "", page)
    page = re.sub(r'<link rel="alternate" href="https://www\.alexanarch\.org/captures/index\.json"[^>]*>\n?', "", page)
    page = page.replace("</head>", signposts + ldblock + "</head>", 1)

    # SPXI instrument label (method 0.9), from data/spxi-instruments.json (2026-10-14)
    sys.path.insert(0, str(ROOT / "scripts"))
    from spxi_instrument_label import label as _spxi_label
    page = _spxi_label(page, "https://www.alexanarch.org/captures/")
    PAGE.write_text(page)
    # RUNTIME GATE. node --check is a SYNTAX check and passed all day while the
    # page was broken: an undefined identifier is legal syntax and fails only
    # when executed. Two real faults hid behind three clean syntax reports —
    # CAPTURE_SOURCES destroyed with the fallback it lived beside, and a defect
    # filter calling a function scoped inside another block's closure. Execute
    # the page's scripts against a stub DOM before declaring a build good.
    import subprocess
    _g = subprocess.run(["node", "scripts/check_gallery_js.js", str(PAGE)],
                        capture_output=True, text=True)
    if _g.returncode != 0:
        print(_g.stdout + _g.stderr)
        raise SystemExit("RUNTIME GATE FAILED — page written but its scripts throw. Fix before publishing.")
    print("  " + _g.stdout.strip())

    print(f"static gallery: {len(entries)} anchored cards rendered into the page "
          f"({len(page):,} bytes) + JSON-LD Dataset + Signposting")
    return 0


if __name__ == "__main__":
    sys.exit(main())
