#!/usr/bin/env python3
"""Wire deposit reading results into all data structures and regenerate static page."""

import json, html as htmlmod, re, os, sys

# Import canonical navbar renderer (single source of truth: data/navigation.json)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts.render_navbar import render_navbar
from scripts.glyph_aria import axn_aria_label as _axn_aria

# --- EA-RETRIEVAL-DENSITY-01 Task 6 ---
_DOI_INDEX_CACHE = None


def _load_doi_index():
    """AXN (full string and bare hex) -> sorted list of doi.org URLs.

    Joins on the mappings[].axn field (1929/1938 rows carry it); live_urls in
    that file are blog/registry links, not record pages, so axn is the key."""
    global _DOI_INDEX_CACHE
    if _DOI_INDEX_CACHE is not None:
        return _DOI_INDEX_CACHE
    out = {}
    try:
        with open('data/doi-resolution-index.json') as fh:
            idx = json.load(fh)
        for row in idx.get('mappings', []):
            axn = row.get('axn')
            url = row.get('doi_url') or (
                f"https://doi.org/{row['dead_doi']}" if row.get('dead_doi') else None)
            if not axn or not url:
                continue
            for key in {axn, (re.match(r'AXN:([0-9A-Fa-f]{4})', axn).group(1).upper()
                              if re.match(r'AXN:([0-9A-Fa-f]{4})', axn) else axn)}:
                out.setdefault(key, set()).add(url)
        out = {k: sorted(v) for k, v in out.items()}
    except Exception:
        pass
    _DOI_INDEX_CACHE = out
    return out


def _split_frontmatter(raw):
    """Return (meta_dict, body). Tolerates blank lines after the opening fence
    (the #110 shape: '---\n\n\ntitle: ...'), which the markdown renderer was
    treating as a horizontal rule."""
    if not re.match(r'^\s*---\s*\n', raw):
        return {}, raw
    lines = raw.split('\n')
    start = next((i for i, l in enumerate(lines) if l.strip() == '---'), None)
    if start is None:
        return {}, raw
    close = None
    for i in range(start + 1, min(len(lines), start + 200)):
        if lines[i].strip() == '---':
            close = i
            break
    meta, block = {}, None
    if close is not None:
        block = lines[start + 1:close]
        body = '\n'.join(lines[close + 1:])
    else:
        # unterminated fence: consume the leading run of key: value lines
        end = start + 1
        seen = False
        for i in range(start + 1, len(lines)):
            s = lines[i]
            if not s.strip():
                if seen and not re.match(r'^\s', s):
                    pass
                end = i + 1
                continue
            if re.match(r'^\s*#{0,6}\s*[A-Za-z_][A-Za-z0-9_]{1,30}:\s', s) or re.match(r'^\s*-\s+\S', s) or re.match(r'^\s+\S', s):
                seen = True
                end = i + 1
                continue
            break
        if not seen:
            return {}, raw
        block = lines[start + 1:end]
        body = '\n'.join(lines[end:])
    key = None
    for l in (block or []):
        m = re.match(r'^\s*#{0,6}\s*([A-Za-z_][A-Za-z0-9_]{1,30}):\s*(.*)$', l)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            meta[key] = val if val else []
        elif key and re.match(r'^\s*-\s+', l):
            if not isinstance(meta.get(key), list):
                meta[key] = []
            meta[key].append(re.sub(r'^\s*-\s+', '', l).strip().strip('"').strip("'"))
    return meta, body.lstrip('\n')


_MD_STRIP = [
    (re.compile(r'```.*?```', re.S), ' '),
    (re.compile(r'!\[[^\]]*\]\([^)]*\)'), ' '),
    (re.compile(r'\[([^\]]*)\]\([^)]*\)'), r'\1'),
    (re.compile(r'^\s{0,3}#{1,6}\s*', re.M), ''),
    (re.compile(r'[*_`>|]+'), ' '),
    (re.compile(r'^\s*-{3,}\s*$', re.M), ' '),
]

ARTICLE_BODY_CAP = 250_000


def _w13_reflow(seg):
    """W13 tier 1.5 (MANUS view-flags 2026-08-04): display-level reflow for
    capture-collapsed structure, applied OUTSIDE code fences, bytes untouched.

    (a) MASHED TABLES — whole markdown tables collapsed onto one line
        ("| H1 | H2 | |---|---| | r1a | r1b | | r2a |…"): isolate the
        separator run onto its own line and split row joints ("| | ") so the
        line renderer's table buffer can rebuild a real table.
    (b) GLUED LISTS — list items joined mid-line ("Ground- §I. The Five
        AxiomsI.1…", "Define:- fuel(E) = …"): split at dash-space preceded
        IMMEDIATELY by a non-space. Math minus signs (" - ", " − "), en/em
        dashes, and in-word hyphens never match. Gated: a line splits only
        if it shows ':- ' (glued list opener) or >=2 glue hits, or is a
        heading with >=1 hit (headings legitimately never contain '- ').
    """
    out = []
    _glue = re.compile(r'(?<=\S)- (?=\S)')
    for ln in seg.split('\n'):
        s = ln
        if s.lstrip().startswith('|') and re.search(r'\|(?:\s*:?-{3,}:?\s*\|)+', s) and '| |' in s.replace('|  |', '| |'):
            s = re.sub(r'\s*(\|(?:\s*:?-{3,}:?\s*\|)+)\s*', r'\n\1\n', s)
            s = re.sub(r'\|\s+\|\s+', '|\n| ', s)
            out.append(s)
            continue
        hits = _glue.findall(s)
        heading = s.startswith('#')
        if (':- ' in s) or (len(hits) >= 2) or (heading and len(hits) >= 1):
            s = _glue.sub('\n- ', s)
        out.append(s)
    return '\n'.join(out)


def _plain_body(body):
    """Markdown -> plain text for schema.org articleBody."""
    t = body
    for rx, rep in _MD_STRIP:
        t = rx.sub(rep, t)
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{3,}', '\n\n', t).strip()
    if len(t) > ARTICLE_BODY_CAP:
        cut = t.rfind('\n\n', 0, ARTICLE_BODY_CAP)
        t = t[:cut if cut > 0 else ARTICLE_BODY_CAP].rstrip() + '\n\n[…full text continues; see encoding.contentUrl]'
    return t


def _kw_list(d, fm):
    """Registry keywords may be a list, a comma string, or a raw markdown list."""
    kw = d.get('keywords') or []
    if isinstance(kw, str):
        kw = [x.strip() for x in kw.split(',')]
    fkw = fm.get('keywords') or []
    if isinstance(fkw, str):
        fkw = [x.strip() for x in fkw.split(',')]
    # frontmatter subject terms lead; registry terms (often generic) follow
    seen = set()
    merged = []
    for k in (list(fkw) + list(kw)):
        if k and k.lower() not in seen:
            seen.add(k.lower())
            merged.append(k)
    kw = merged
    if isinstance(kw, str):
        if '\n-' in kw or kw.lstrip().startswith('-'):
            kw = [re.sub(r'^\s*-\s*', '', x).strip() for x in kw.split('\n')]
        else:
            kw = [x.strip() for x in kw.split(',')]
    return [k for k in (kw or []) if k and len(k) < 120][:40]
# --- end Task 6 helpers ---

_CAPTURE_BY_DEPOSIT = None


def _captures_for_deposit(dn):
    """Reception record for a deposit, from data/capture-deposit-links.json
    (Task 7). Returns [] when the map is absent."""
    global _CAPTURE_BY_DEPOSIT
    if _CAPTURE_BY_DEPOSIT is None:
        _CAPTURE_BY_DEPOSIT = {}
        try:
            with open('data/capture-deposit-links.json', encoding='utf-8') as fh:
                for slug, rec in json.load(fh).get('links', {}).items():
                    for edge in rec.get('deposits', []):
                        _CAPTURE_BY_DEPOSIT.setdefault(edge['deposit_number'], []).append({
                            'slug': slug,
                            'query': rec.get('query'),
                            'date': rec.get('date'),
                            'match_type': rec.get('match_type'),
                            'section': rec.get('section'),
                            'primary': edge.get('primary', False),
                        })
        except Exception:
            pass
        for v in _CAPTURE_BY_DEPOSIT.values():
            v.sort(key=lambda x: (not x['primary'], x.get('date') or ''), reverse=False)
    return _CAPTURE_BY_DEPOSIT.get(dn, [])
# --- end Task 7 helper ---



def wire_deposit(deposit_number, concepts=None, wiki_article=None, entity_triples=None):
    """
    Wire reading results for a single deposit into:
    - registry.json (defines_concepts, references_concepts, wiki_article, entity_triples)
    - entity-index.json (new concepts)
    - entity-index-reading.json (running log)
    - s/records/N/index.html (regenerated static page)
    """
    
    # Load data
    with open('data/registry.json') as f:
        reg = json.load(f)
    with open('data/entity-index.json') as f:
        eidx = json.load(f)
    with open('data/entity-index-reading.json') as f:
        ridx = json.load(f)
    
    # Find deposit
    dep = None
    for d in reg['deposits']:
        if d['deposit_number'] == deposit_number:
            dep = d
            break
    if not dep:
        print(f"ERROR: deposit #{deposit_number} not found")
        return
    
    # 1. Add new concepts to indexes
    if concepts:
        defines = []
        for c in concepts:
            term = c['term']
            defines.append(term)
            
            # Add to canonical index
            eidx['concepts'][term] = {
                "definition": c['definition'],
                "defined_in": deposit_number,
                "type": c.get('type', 'theoretical'),
                "referenced_in": [],
                "reference_count": 0
            }
            
            # Add to running log
            ridx['concepts'].append({
                "term": term,
                "definition": c['definition'],
                "defined_in": deposit_number,
                "type": c.get('type', 'theoretical')
            })
        
        dep['defines_concepts'] = defines
        eidx['total_concepts'] = len(eidx['concepts'])
        ridx['total_concepts'] = len(ridx['concepts'])
    
    # 2. Update wiki article
    if wiki_article:
        dep['wiki_article'] = wiki_article
    
    # 3. Update entity triples
    if entity_triples:
        dep['entity_triples'] = entity_triples
    
    # 4. Mark as read
    if deposit_number not in ridx['deposits_read']:
        ridx['deposits_read'].append(deposit_number)
        ridx['deposits_read'].sort()
    
    # 5. Regenerate static page
    regenerate_static_page(dep, eidx)
    
    # 6. Save everything
    with open('data/registry.json', 'w') as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
    with open('data/entity-index.json', 'w') as f:
        json.dump(eidx, f, indent=2, ensure_ascii=False)
    with open('data/entity-index-reading.json', 'w') as f:
        json.dump(ridx, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ #{deposit_number}: {dep['title'][:50]}")
    if concepts:
        print(f"    concepts: {', '.join(c['term'] for c in concepts)}")
    if wiki_article:
        print(f"    wiki: {len(wiki_article)} chars")
    if entity_triples:
        print(f"    triples: {len(entity_triples)}")


def _compose_meta_description(d, max_len=155, min_target=120):
    """Compose a rich meta description for SERP snippets.
    
    Meta description is the ~155-char snippet Google shows under the SERP title.
    Records with short descriptions (< 120 chars) were previously truncated at
    that length, causing Google to prefer the browse page's abundant text over
    the record page for many queries.
    
    Strategy: if description is already long enough, use it (word-safe truncate);
    otherwise extend with the informative tail of wiki_article's opening sentence
    ("is a N-word content-type by author, a heteronym within..."), which is a
    reliably rich pattern authored by publish_wiki_entries.py.
    """
    desc = (d.get('description') or '').strip()
    wiki = (d.get('wiki_article') or '').strip()
    keywords = d.get('keywords', []) or []
    title = (d.get('title') or '').strip()
    
    def _truncate_at_word(s, limit):
        """Truncate at last word boundary before limit; no mid-word cuts."""
        if len(s) <= limit:
            return s
        cut = s[:limit].rsplit(' ', 1)[0]
        return cut.rstrip('.,;: ') + '…'
    
    # Case 1: description is already long enough — use it (word-safe truncate)
    if len(desc) >= min_target:
        return _truncate_at_word(desc, max_len)
    
    # Case 2: short description — mine wiki_article for a rich extension
    if wiki:
        # Wiki entries reliably follow this shape:
        #   "TITLE" is a N-word CONTENT_TYPE by AUTHOR, ...
        # The "TITLE" quoted at the start is redundant with the SERP title;
        # skip it, and rewrite "is a" as "It is a" so the extension reads as
        # a proper sentence when it follows the description.
        import re as _re
        m = _re.match(r'^["\u201c\u201d]?[^"\u201c\u201d]{0,300}["\u201c\u201d]?\s+is\s+(a|an)\s+', wiki)
        if m:
            # keep the "a"/"an" and everything after; prepend "It" to form
            # "It is a 49,530-word dataset by Jack Feist..."
            wiki_tail = 'It is ' + wiki[m.end() - len(m.group(1)) - 1:].lstrip()
        else:
            wiki_tail = wiki
        
        # Take first sentence of the tail
        parts = wiki_tail.replace('!', '.').replace('?', '.').split('. ')
        wiki_lead = parts[0].strip()
        if len(wiki_lead) < 60 and len(parts) > 1:
            wiki_lead = (wiki_lead + '. ' + parts[1]).strip()
        if wiki_lead and not wiki_lead.endswith('.'):
            wiki_lead = wiki_lead + '.'
        
        # Compose: if desc is a substring of wiki_lead, just use wiki_lead
        # (avoids "Mobile Ontological... Mobile Ontological..." duplication)
        if desc and desc.rstrip('.').lower() in wiki_lead.lower():
            combined = wiki_lead
        elif desc:
            combined = desc.rstrip('.') + '. ' + wiki_lead
        else:
            combined = wiki_lead
        
        # If still too short after wiki extension, try one more sentence
        if len(combined) < min_target and len(parts) > 2:
            addition = parts[2].strip()
            if addition and not addition.endswith('.'):
                addition = addition + '.'
            combined = combined.rstrip('.') + '. ' + addition
        
        return _truncate_at_word(combined, max_len)
    
    # Case 3: no wiki — augment desc with keywords
    if desc and keywords:
        kw_str = ', '.join(k for k in keywords[:6] if k)
        return _truncate_at_word(f'{desc.rstrip(".")} — {kw_str}.', max_len)
    
    # Case 4: fall back to raw description (may be short)
    if desc:
        return _truncate_at_word(desc, max_len)
    
    # Case 5: nothing available — use title
    return _truncate_at_word(title, max_len)



_TRAVERSAL_CACHE = {}


def _traversal_graphs():
    """Load and index the citation / capture / concept graphs once per process.

    These files are computed by the enrichment scripts and, until 2026-07-30,
    were never rendered anywhere: the archive's intellectual structure existed
    only as JSON. The traversal block below makes it walkable — for readers and
    for crawlers, which previously could enter at any record and find no exit
    but the 940 KB master index.
    """
    if _TRAVERSAL_CACHE:
        return _TRAVERSAL_CACHE
    import collections, pathlib
    _ROOT = pathlib.Path(__file__).resolve().parent
    _errs = []
    cites = collections.defaultdict(list)   # source -> [(target, via)]
    cited = collections.defaultdict(list)   # target -> [(source, via)]
    caps = collections.defaultdict(list)    # deposit -> [(slug, query, date)]
    concept_of = {}                         # deposit -> concept dict
    try:
        cg = json.load(open(_ROOT / 'data' / 'citation-graph.json'))
        for e in cg.get('edges', []):
            s, t = e.get('source_deposit'), e.get('target_deposit')
            if not s or not t or s == t:
                continue
            cites[s].append((t, e.get('via')))
            cited[t].append((s, e.get('via')))
    except Exception as e:
        _errs.append(f"citation-graph: {e}")
    try:
        cl = json.load(open(_ROOT / 'data' / 'capture-deposit-links.json'))
        for slug, rec in (cl.get('links') or {}).items():
            for dep in (rec.get('deposits') or []):
                n = dep.get('deposit_number')
                if n:
                    caps[n].append((slug, rec.get('query'), rec.get('date')))
    except Exception as e:
        _errs.append(f"capture-links: {e}")
    try:
        cm = json.load(open(_ROOT / 'data' / 'concept-map.json'))
        for c in cm.get('concepts', []):
            for v in c.get('versions', []):
                if v.get('deposit_number'):
                    concept_of[v['deposit_number']] = c
    except Exception as e:
        _errs.append(f"concept-map: {e}")
    if _errs:
        print("  [traversal] graph load failures:", "; ".join(_errs), file=sys.stderr)
    _TRAVERSAL_CACHE.update(cites=cites, cited=cited, caps=caps, concept=concept_of)
    return _TRAVERSAL_CACHE


def _traversal_html(d, registry):
    """Render prev/next, citation edges, concept siblings, and capture links."""
    if not registry:
        return ''
    esc = lambda s: htmlmod.escape(str(s)) if s else ''
    g = _traversal_graphs()
    dn = d['deposit_number']
    nums = sorted(x['deposit_number'] for x in registry.get('deposits', []))
    bynum = {x['deposit_number']: x for x in registry.get('deposits', [])}
    i = nums.index(dn) if dn in nums else -1
    prev_n = nums[i - 1] if i > 0 else None
    next_n = nums[i + 1] if 0 <= i < len(nums) - 1 else None

    def link(n, extra=''):
        e = bynum.get(n)
        if not e:
            return ''
        t = esc(e['title'])[:88]
        return (f'<a href="/s/records/{n}/" style="color:var(--accent);text-decoration:none">'
                f'#{n} {t}</a>{extra}')

    rows = []
    if prev_n or next_n:
        nav = []
        if prev_n:
            nav.append(f'← {link(prev_n)}')
        if next_n:
            nav.append(f'{link(next_n)} →')
        rows.append('<div style="display:flex;justify-content:space-between;gap:1.5rem;'
                    'font-size:.85em;margin:.4rem 0">'
                    + ''.join(f'<span style="flex:1">{x}</span>' for x in nav) + '</div>')

    VIA = {'doi_resolution': 'via DOI', 'deposit_number_reference': 'by deposit number',
           'ea_id_reference': 'by EA identifier', 'axn_reference': 'by AXN',
           'axn_hex_reference': 'by AXN hex', 'artifact_anchor': 'by artifact anchor'}

    def edge_list(pairs, label, limit=12):
        if not pairs:
            return ''
        seen = {}
        for n, via in pairs:
            seen.setdefault(n, via)
        items = list(seen.items())
        shown = items[:limit]
        lis = ''.join(f'<li style="margin:.15rem 0">{link(n)} '
                      f'<span style="opacity:.6;font-size:.85em">{esc(VIA.get(via, via or ""))}</span></li>'
                      for n, via in shown)
        more = (f'<li style="opacity:.6;margin:.15rem 0">+{len(items) - limit} more</li>'
                if len(items) > limit else '')
        return (f'<div style="margin:.7rem 0"><div style="font-weight:600;font-size:.85em;'
                f'margin-bottom:.2rem">{label} ({len(items)})</div>'
                f'<ul style="margin:0;padding-left:1.1rem;font-size:.85em">{lis}{more}</ul></div>')

    rows.append(edge_list(g['cites'].get(dn, []), 'This deposit cites'))
    rows.append(edge_list(g['cited'].get(dn, []), 'Cited by'))

    c = g['concept'].get(dn)
    if c and len(c.get('versions', [])) > 1:
        sibs = [v for v in c['versions'] if v.get('deposit_number') != dn]
        lis = ''.join(f'<li style="margin:.15rem 0">{link(v["deposit_number"])}'
                      f'{" <span style=\"opacity:.6;font-size:.85em\">current</span>" if v.get("is_current") else ""}</li>'
                      for v in sibs[:8])
        rows.append(f'<div style="margin:.7rem 0"><div style="font-weight:600;font-size:.85em;'
                    f'margin-bottom:.2rem">Other versions of this work ({len(sibs)})</div>'
                    f'<ul style="margin:0;padding-left:1.1rem;font-size:.85em">{lis}</ul>'
                    f'<div style="font-size:.8em;opacity:.7;margin-top:.2rem">'
                    f'Work concept: <a href="{esc(c.get("concept_url",""))}" '
                    f'style="color:var(--accent)">{esc(c.get("title_base",""))}</a></div></div>')

    caps = g['caps'].get(dn, [])
    if caps:
        lis = ''.join(f'<li style="margin:.15rem 0"><a href="https://www.machinemediation.org/captures/#{esc(s)}" '
                      f'style="color:var(--accent);text-decoration:none">{esc(q)[:70]}</a> '
                      f'<span style="opacity:.6;font-size:.85em">{esc(dt)}</span></li>'
                      for s, q, dt in caps[:6])
        rows.append(f'<div style="margin:.7rem 0"><div style="font-weight:600;font-size:.85em;'
                    f'margin-bottom:.2rem">Machine-composition captures referencing this deposit ({len(caps)})</div>'
                    f'<ul style="margin:0;padding-left:1.1rem;font-size:.85em">{lis}</ul></div>')

    rows = [r for r in rows if r]
    if not rows:
        return ''
    return ('<section style="margin:1.6rem 0;padding:.9rem 1.1rem;border:1px solid var(--rule,rgba(127,127,127,.22));'
            'border-radius:.5rem"><h2 style="margin:0 0 .5rem;font-size:1em">Traversal</h2>'
            + ''.join(rows) + '</section>')



_APPENDIX_MARK = "Appendix — metadata-capture body"



def _drop_duplicated_description(fulltext, description):
    """Remove the body's opening Description block when it restates the field above it.

    A capture body typically opens with `## Description` followed by the same
    prose already rendered in the record's Description section. The reader then
    reads the identical paragraph twice before learning whether the record holds
    anything. Canonical bytes are immutable, so the duplicate is dropped at
    render rather than edited out of the file.

    Matching is by leading prefix, not similarity: a heuristic that guesses at
    resemblance is how this archive has repeatedly asserted things it had not
    checked.
    """
    if not fulltext or not description:
        return fulltext
    # Strip HTML tags as well as markdown: by the time this runs the pipeline has
    # already converted the body line-by-line, so the block begins "<p>…". Four
    # earlier attempts (2026-07-31) patched the branch logic while the normalizer
    # silently failed every prefix comparison on that one tag.
    def norm(x):
        t = re.sub(r"<[^>]+>", " ", str(x))
        t = re.sub(r"[*_`#]", "", t)
        return re.sub(r"\s+", " ", t).strip().lower()
    # The capture sentence may lead the body block, the description field, both,
    # or neither: a 2026-07-30 pass stripped it from some fields and could not
    # touch any immutable body. Discount it on BOTH sides before comparing —
    # stripping one side only misaligns every comparison by exactly that phrase.
    _lead = re.compile(
        r"^semi-restored record\s*\(metadata capture only;?\s*no full text\)\.?\s*", re.I)
    d = _lead.sub("", norm(description))[:160]
    if len(d) < 60:
        return fulltext
    # The pipeline hands this HTML, not markdown. Match both forms rather than
    # assuming one: assuming the input shape is how the first three attempts at
    # this fix silently did nothing.
    m = re.search(r"<h[23]>\s*Description\s*</h[23]>", fulltext, re.I)
    html_mode = bool(m)
    if not m:
        m = re.search(r"^##+\s*Description\s*$", fulltext, re.M)
    if not m:
        return fulltext
    after = fulltext[m.end():]
    a = norm(after)
    # The body's block is typically the capture sentence + the same description
    # now held in the field. Discount the known prefix before comparing, since a
    # 2026-07-30 reconciliation pass stripped that sentence from the field but
    # could not touch the immutable body.
    a = _lead.sub("", a)
    if not a[:160].startswith(d[:120]):
        return fulltext
    # cut from the Description heading to the next heading of the same or higher level
    if html_mode:
        nxt = re.search(r"<h[123][ >]", after, re.I)
    else:
        nxt = re.search(r"^##+\s+\S", after, re.M)
    tail = after[nxt.start():] if nxt else ""
    return fulltext[:m.start()].rstrip() + ("\n\n" + tail.lstrip() if tail.strip() else "\n")


def _mark_superseded_appendix(html):
    """Visually and semantically mark a retained metadata-capture appendix.

    Restored records keep the superseded capture body per non-destruction. That
    is correct: the record's own history stays on the page. But rendered as
    plain prose, its field dump ("content_type: Semi-restored record …") scans —
    to a reader, a crawler, and a composition layer — as a live declaration of
    the record's current status, which it is not.

    So the appendix is kept and marked. That is the obelus applied to the
    archive's own body: the doubted passage stays on the page, and the mark says
    what it is.
    """
    i = html.find(_APPENDIX_MARK)
    if i == -1:
        return html
    # back up to the start of the element containing the marker
    start = html.rfind("<", 0, i)
    start = html.rfind("<p", 0, i)
    if start == -1:
        start = i
    banner = (
        '<div class="superseded-appendix" role="note" '
        'aria-label="Superseded metadata-capture appendix, retained for the record" '
        'style="margin:1.4rem 0;padding:.9rem 1.1rem;border-left:3px solid rgba(127,127,127,.45);'
        'background:rgba(127,127,127,.06);opacity:.72;font-size:.92em">'
        '<div style="font-weight:600;margin-bottom:.35rem;opacity:.85">'
        '⊖ Superseded — metadata-capture body, retained</div>'
        '<div style="margin-bottom:.6rem">Everything below records this deposit\'s '
        '<em>former</em> state, when only a metadata capture was held. The full text '
        'above is the canonical body. Status fields appearing in this appendix are '
        'historical and do not describe the record as it now stands.</div>'
    )
    return html[:start] + banner + html[start:] + "</div>"


def regenerate_static_page(d, eidx, registry=None):
    """Regenerate the static HTML page for a deposit with full enrichment.

    registry: optional full registry dict. If provided, enables version-chain
    blocks (banner for superseded/draft, version history list for series).
    If None, version blocks are omitted (faster but less informative).
    """
    esc = lambda s: htmlmod.escape(str(s)) if s else ''
    dn = d['deposit_number']
    hex_id = d.get('hex', '')
    if not hex_id:
        # v1.1.2 (MANUS 2026-07-09): recent entries carry the hex only inside
        # the axn string (e.g. "AXN:0431.ARCHIVAL.…"); derive it so full-text
        # candidate paths and download links resolve.
        m = re.match(r'AXN:([0-9A-Fa-f]{4})\.', d.get('axn', '') or '')
        if m:
            hex_id = m.group(1)
    
    # JSON-LD
    _rec_url = f"https://www.alexanarch.org/s/records/{dn}/"
    _ld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "name": d['title'],
        "headline": str(d['title'])[:110],
        "author": {"@type": "Person", "name": d['creator']},
        "datePublished": d['date'],
        **({"dateModified": d['date_modified']} if d.get('date_modified') else {}),
        "identifier": d['axn'],
        "description": d.get('description', '')[:300],
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "publisher": {"@type": "Organization", "name": "Alexanarch"},
        "keywords": ", ".join(d.get('keywords', []) if isinstance(d.get('keywords'), list) else []),
        "url": _rec_url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": _rec_url},
        "inLanguage": "en",
        "isPartOf": {"@type": "Collection", "name": "Alexanarch",
                     "url": "https://www.alexanarch.org/"},
    }
    # T6 (EA-AVAILABILITY-INTEGRITY-01, ⟡2 RESOLVED): canonical-text status is
    # machine-declared on every record — creativeWorkStatus carries the enum,
    # conditionsOfAccess mirrors it in crawler-conventional prose.
    _cts = d.get('canonical_text_status')
    if _cts:
        _ld["creativeWorkStatus"] = _cts
        _ld["conditionsOfAccess"] = {
            "canonical_full_text": "Open access; complete canonical text embedded in this page and its structured data.",
            "recovered_full_text": "Open access; complete text recovered and seated as the canonical body after the 2026 repository termination.",
            "metadata_only": "Metadata capture only; the canonical full text of this work is not held by this archive.",
            "attachment_only": "Open access attachment; canonical content is the linked file, not page prose.",
            "tombstone": "Tombstoned record; see body for disposition.",
            "withdrawn": "Withdrawn record; see body for the withdrawal notice and the authoritative external identifier.",
        }.get(_cts, _cts)
    _caps = _captures_for_deposit(dn)
    if _caps:
        _ld["subjectOf"] = [{
            "@type": "Observation",
            "name": f"Retrieval capture: {c['query']}",
            "url": f"https://www.machinemediation.org/captures/#{c['slug']}",
            "datePublished": c.get('date'),
            "measurementTechnique": c.get('match_type'),
            "isPartOf": {"@type": "Dataset", "name": "EA-WG-CAPTURES-01",
                         "url": "https://www.machinemediation.org/data/registry.json"},
        } for c in _caps[:10]]
        _ld["interactionStatistic"] = {
            "@type": "InteractionCounter",
            "interactionType": "https://schema.org/ViewAction",
            "name": "retrieval captures recorded",
            "userInteractionCount": len(_caps),
        }
    _didx = _load_doi_index()
    _dois = _didx.get(d.get('axn', ''), []) or _didx.get((hex_id or '').upper(), [])
    if _dois:
        _ld["sameAs"] = _dois
    jsonld = json.dumps(_ld, ensure_ascii=False)
    
    # Read full text
    # v1.1.1 fix: prefer the registry's declared full_text_path (the canonical
    # source of truth). Fall back to whichever existing file is largest, so a
    # stub alias never shadows a populated text file.
    # Guard (MANUS, 2026-07-05): if the registry declares a full_text_path
    # but the file isn't there yet, do NOT silently fall through to the
    # description block — that produces description-only record pages when
    # the wire step races the text write (the AXN:041F regression).
    _declared = d.get('full_text_path')
    if _declared and not os.path.exists(_declared.lstrip('/')):
        raise RuntimeError(
            f"wire_deposit #{dn}: full_text_path {_declared} declared "
            f"in registry but the file does not exist on disk; refusing to render "
            f"a description-only page. Write the canonical text first, then wire."
        )
    fulltext = ''
    candidates = []
    declared = d.get('full_text_path')
    if declared:
        candidates.append(declared.lstrip('/'))
    # Also consider both conventional paths, plus deposit-number-named files
    # (v1.1.2: #1056-#1058 were saved as AXN-{deposit_number}.md)
    for p in [f'data/deposits/AXN-{hex_id}.md', f'data/texts/AXN-{hex_id}-text.md',
              f'data/deposits/AXN-{dn}.md']:
        if p not in candidates:
            candidates.append(p)

    best_path = None
    best_size = 0
    # T1 fix (EA-AVAILABILITY-INTEGRITY-01, 2026-07-28): a declared, existing
    # full_text_path is AUTHORITATIVE. Largest-wins applies only among
    # fallback candidates when the registry declares nothing — otherwise a
    # larger hex-keyed sibling shadows the canonical body (the #869/#856
    # hex-0365 collision: #869 served #856's 22KB text over its own declared
    # 2KB dataset-pointer body). The declared-but-missing case still raises
    # above, so the anti-stub guard's intent is preserved.
    if declared and os.path.exists(declared.lstrip('/')):
        best_path = declared.lstrip('/')
        best_size = os.path.getsize(best_path)
    else:
        for path in candidates:
            if os.path.exists(path):
                size = os.path.getsize(path)
                if size > best_size:
                    best_size = size
                    best_path = path

    if best_path and best_size > 0:
        # JSON source: render a dataset callout + download link, NOT inline-as-prose
        # (treating JSON as markdown turns every line into a <p>, producing
        #  unreadable multi-MB pages)
        if best_path.endswith(('.pdf', '.zip', '.png', '.jpg', '.epub')):
            # T6 hardening (2026-07-28): binary attachments are never inlined
            # or text-decoded — render a download callout. (Regression guard:
            # #344's declared PDF body crashed the fleet pass and was briefly
            # text-mangled before git restore.)
            size_mb = best_size / (1024 * 1024)
            fulltext = (f'**Attachment:** [{best_path.split("/")[-1]}](/{best_path}) '
                        f'({size_mb:.1f} MB). The canonical content of this deposit is '
                        f'the attached file; this page is its address and description.')
            best_path = None  # prevent any text read below
        elif best_path and best_path.endswith('.json'):
            json_size_kb = best_size // 1024
            json_size_mb = best_size / (1024 * 1024)
            size_label = f"{json_size_mb:.1f} MB" if best_size > 1024 * 1024 else f"{json_size_kb} KB"
            desc = esc(d.get('description', '').strip()) or 'Machine-readable dataset.'
            fulltext = (
                f'<p>{desc}</p>'
                f'<div style="background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:14px 18px;margin:16px 0">'
                f'<div style="font-size:.78em;color:#777;margin-bottom:4px">DATASET · machine-readable</div>'
                f'<div style="font-family:var(--mono);font-size:.88em;margin-bottom:8px">{esc(best_path)}</div>'
                f'<div style="font-size:.85em;color:#555;margin-bottom:10px">{size_label} · JSON · {esc(d.get("license", "CC-BY-4.0"))}</div>'
                f'<a href="/{esc(best_path)}" style="display:inline-block;background:var(--teal);color:#fff;padding:6px 14px;border-radius:4px;font-size:.82em;text-decoration:none">↓ Download JSON</a>'
                f'</div>'
                f'<p style="font-size:.85em;color:#777">The full dataset is the canonical artifact for this deposit. The Markdown download button above provides metadata only.</p>'
            )
        else:
            with open(best_path) as f:
                raw = f.read()
            # Task 6: frontmatter is metadata, not prose. Strip it from the
            # rendered body (375/1379 deposits were emitting it as <p> text)
            # and retain it for structured data.
            _fm, raw = _split_frontmatter(raw)
            # W13 tier 1: unglue collapsed heading markers for the plain-text
            # machine surface too (outside code fences), so articleBody carries
            # readable structure. Bytes untouched.
            _fp = raw.split('```')
            for _pi in range(0, len(_fp), 2):
                _fp[_pi] = re.sub(r'(?<=[^\n])(#{2,6} )', r'\n\n\1', _fp[_pi])
            raw = '```'.join(_fp)
            _plain = _plain_body(raw)
            # W10: restoration wrapper (methodology/recovery apparatus) precedes
            # the work inside canonical bytes; machine consumers of articleBody
            # get the WORK — apparatus stays in the bytes and the page's
            # apparatus section, provenance in description/encoding fields.
            _w10 = 'Canonical bytes below the rule'
            if _plain and _w10 in _plain:
                _plain = _plain.split(_w10, 1)[1].lstrip(' .\n*-_')
            if _plain:
                _ld["articleBody"] = _plain
                _ld["wordCount"] = len(_plain.split())
            _ld["encoding"] = {
                "@type": "MediaObject",
                "contentUrl": "https://www.alexanarch.org/" + best_path.lstrip('/'),
                "encodingFormat": "text/markdown",
                "contentSize": str(best_size),
            }
            _kws = _kw_list(d, _fm)
            if _kws:
                _ld["keywords"] = ", ".join(_kws)
            if _fm.get('series'):
                _ld.setdefault("isPartOf", {})
                _ld["isPartOf"] = [
                    {"@type": "Collection", "name": "Alexanarch",
                     "url": "https://www.alexanarch.org/"},
                    {"@type": "PublicationIssue", "name": str(_fm['series'])},
                ]
                _ld["identifier"] = [d['axn'], str(_fm['series'])]
            jsonld = json.dumps(_ld, ensure_ascii=False)
            # W13 TIER 1 (MANUS word 2026-08-04): display-level unglue for the
            # collapsed-formatting class (580 records, capture-pipeline origin).
            # Heading markers glued mid-line ("…thermodynamics## Table of
            # Contents### Prolegomenon") never reach the line converter as
            # headings; insert paragraph breaks before glued `##`+ markers so
            # structure renders. Bytes untouched — reversible presentation
            # transform. 2+ hashes + space avoids C#-style single-hash tokens;
            # fenced code blocks are exempted by splitting on ``` fences.
            _fence_parts = raw.split('```')
            for _pi in range(0, len(_fence_parts), 2):  # even indices = outside fences
                _fence_parts[_pi] = re.sub(r'(?<=[^\n])(#{2,6} )', r'\n\n\1', _fence_parts[_pi])
                _fence_parts[_pi] = _w13_reflow(_fence_parts[_pi])
            raw = '```'.join(_fence_parts)
            lines = raw.split('\n')
            ft_lines = []
            in_pre = False
            pre_buf = []
            _img_re = re.compile(r'^!\[([^\]]*)\]\((/?data/attachments/[A-Za-z0-9._/\-]+)\)\s*$')
            _pre_style = ('font-family:var(--mono);font-size:.82em;background:#f8f9fa;'
                          'border:1px solid var(--border);border-radius:6px;padding:12px 14px;'
                          'margin:12px 0;white-space:pre;overflow-x:auto;line-height:1.55;color:#333')
            _tbl_buf = []
            _list_buf = []
            def _flush_table(buf):
                # buf: escaped |-lines. A separator row (---) marks the previous row as header.
                _rows = []
                _hdr_idx = -1
                for _r in buf:
                    _cells = [c.strip() for c in _r.strip().strip('|').split('|')]
                    if _cells and all(re.fullmatch(r':?-{3,}:?', c) for c in _cells if c != ''):
                        _hdr_idx = len(_rows) - 1
                        continue
                    if any(c for c in _cells):
                        _rows.append(_cells)
                if not _rows:
                    return ''
                _ncol = max(len(r) for r in _rows)
                _h = ['<div style="overflow-x:auto;margin:14px 0"><table style="border-collapse:collapse;font-size:.86em">']
                for _i, _r in enumerate(_rows):
                    _tag = 'th' if _i == _hdr_idx else 'td'
                    _st = ('border:1px solid var(--border);padding:5px 9px;text-align:left;vertical-align:top;'
                           + ('background:var(--surface);font-weight:600;' if _tag == 'th' else ''))
                    _r = _r + [''] * (_ncol - len(_r))
                    _h.append('<tr>' + ''.join(f'<{_tag} style="{_st}">{c}</{_tag}>' for c in _r) + '</tr>')
                _h.append('</table></div>')
                return ''.join(_h)
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('```'):
                    if not in_pre:
                        in_pre = True
                        pre_buf = []
                    else:
                        pre_content = '\n'.join(esc(l) for l in pre_buf)
                        ft_lines.append(f'<pre style="{_pre_style}">{pre_content}</pre>')
                        in_pre = False
                        pre_buf = []
                    continue
                if in_pre:
                    pre_buf.append(line)
                    continue
                img_match = _img_re.match(stripped)
                if img_match:
                    alt = esc(img_match.group(1))
                    src = img_match.group(2)
                    if not src.startswith('/'):
                        src = '/' + src
                    ft_lines.append(
                        f'<figure style="margin:16px 0;text-align:center">'
                        f'<img src="{esc(src)}" alt="{alt}" '
                        f'style="max-width:100%;height:auto;border:1px solid var(--border);border-radius:6px">'
                        f'</figure>'
                    )
                    continue
                line = esc(line)
                # W13 tier 1.5: table buffer — consecutive |-lines become a real table
                if line.lstrip().startswith('|'):
                    _tbl_buf.append(line.strip())
                    continue
                elif _tbl_buf:
                    ft_lines.append(_flush_table(_tbl_buf))
                    _tbl_buf = []
                # W13 tier 1.5: list buffer — consecutive '- ' lines become a <ul>
                if line.startswith('- '):
                    _li = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line[2:])
                    _li = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', _li)
                    _list_buf.append(_li)
                    continue
                elif _list_buf:
                    ft_lines.append('<ul style="margin:8px 0 8px 22px;padding:0">' + ''.join(f'<li style="margin:3px 0">{x}</li>' for x in _list_buf) + '</ul>')
                    _list_buf = []
                if line.startswith('# '): ft_lines.append(f'<h1>{line[2:]}</h1>')
                elif line.startswith('## '): ft_lines.append(f'<h2>{line[3:]}</h2>')
                elif line.startswith('### '): ft_lines.append(f'<h3>{line[4:]}</h3>')
                elif line.startswith('#### '): ft_lines.append(f'<h4>{line[5:]}</h4>')
                elif line.startswith('---'): ft_lines.append('<hr>')
                elif line.startswith('&gt;'): ft_lines.append(f'<blockquote style="border-left:3px solid var(--teal);padding-left:12px;color:#555;margin:8px 0">{line[4:]}</blockquote>')
                elif line.strip():
                    line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
                    line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', line)
                    # SOURCE-282 addendum (2026-08-04): leading whitespace is
                    # prosodic structure (indentation clusters, staggered
                    # arrangements); preserve it instead of letting HTML
                    # collapse it. Applies only to lines that carry it.
                    if line[:1] in (' ', '\t'):
                        ft_lines.append(f'<p style="white-space:pre-wrap;margin:2px 0">{line}</p>')
                    else:
                        ft_lines.append(f'<p>{line}</p>')
                else: ft_lines.append('')
            if _tbl_buf:
                ft_lines.append(_flush_table(_tbl_buf))
            if _list_buf:
                ft_lines.append('<ul style="margin:8px 0 8px 22px;padding:0">' + ''.join(f'<li style="margin:3px 0">{x}</li>' for x in _list_buf) + '</ul>')
            if in_pre and pre_buf:
                pre_content = '\n'.join(esc(l) for l in pre_buf)
                ft_lines.append(f'<pre style="{_pre_style}">{pre_content}</pre>')
            fulltext = '\n'.join(ft_lines)
    
    if not fulltext:
        # v1.1.2 fix (MANUS 2026-07-09): never silently duplicate the description
        # into the Full Text section — that was the regression producing
        # description-only full-text blocks across #1056, #1057, #1058. If the
        # full text file genuinely does not exist and none is declared, emit an
        # explicit notice so the deposit is visibly incomplete rather than
        # falsely appearing complete-with-Full-Text.
        fulltext = (
            '<p style="color:#777;font-style:italic;font-size:.9em">'
            'No separate full-text file is present on disk for this deposit. '
            'The Description above is the extent of the recorded content; '
            'a Full Text file may be added later at '
            f'<code style="font-family:var(--mono);font-size:.85em">data/deposits/AXN-{esc(hex_id)}.md</code>.'
            '</p>'
        )
    
    # Retained metadata-capture appendices are marked, not removed: the record
    # keeps its own history, and the mark says the history is history.
    fulltext = _drop_duplicated_description(fulltext, d.get('description'))
    fulltext_marked = _mark_superseded_appendix(fulltext)

    # W10 WRAPPER-APPARATUS SEPARATION (2026-08-04, exemplar #1167): restoration
    # records carry the recovery wrapper (Methodology, Falsification Conditions,
    # Recovery note) INSIDE the canonical bytes, above the marker line
    # "Canonical bytes below the rule." — so Full Text opened with apparatus,
    # not the work. Presentation-level fix, kernel-orthodox: bytes untouched;
    # the wrapper renders as a collapsed apparatus section and Full Text is
    # anchored at the canonical rule.
    apparatus_html = ''
    _W10_MARK = 'Canonical bytes below the rule'
    if _W10_MARK in fulltext_marked:
        _i = fulltext_marked.find(_W10_MARK)
        _cut = fulltext_marked.find('</p>', _i)
        _cut = (_cut + 4) if _cut != -1 else (_i + len(_W10_MARK))
        apparatus_html = (
            '<details style="margin:12px 0;background:var(--surface);border-radius:6px;padding:8px 12px">'
            '<summary style="cursor:pointer;font-weight:600;color:#777;font-size:.9em">'
            'Restoration apparatus — methodology, falsification conditions, recovery note '
            '(provenance of the recovered bytes; the work follows below)</summary>'
            '<div class="ft" style="font-size:.88em;color:#555">' + fulltext_marked[:_cut] + '</div></details>'
        )
        fulltext_marked = fulltext_marked[_cut:]

    # Keywords
    # Version chain blocks (banner for superseded/draft, history list for series)
    version_banner = ''
    version_history = ''
    status = d.get('status', 'ACTIVE')
    version = d.get('version', '')
    series_id = d.get('version_series_id')
    superseded_by_n = d.get('superseded_by_deposit_number')
    superseded_reason = d.get('superseded_reason', '')

    if d.get('lifecycle_state') == 'withdrawn_external':
        # Typed tombstone (MANUS foreign-capture policy + SHAPE doctrine v1.0):
        # an over-captured external work. The page names the rightful author and
        # DOI and serves none of their content. Highest-priority state.
        w = d.get('withdrawn', {})
        version_banner = (
            '<div style="background:#fee2e2;border-left:4px solid #b91c1c;padding:12px 16px;'
            'border-radius:6px;margin:12px 0;font-size:.92em">'
            '<div style="font-weight:600;color:#7f1d1d;margin-bottom:4px">✕ Withdrawn — external work (typed tombstone)</div>'
            '<div style="color:#7f1d1d">This position was created by an over-inclusive metadata capture. '
            f'The work is by <strong>{esc(w.get("rightful_author",""))}</strong> and is not a holding of this archive. '
            f'It belongs to its author at DOI <a href="https://doi.org/{esc(w.get("rightful_doi",""))}" '
            f'style="color:#b91c1c;font-weight:500">{esc(w.get("rightful_doi",""))}</a>. '
            'No content of the work is served here.</div>'
            '</div>'
        )
    elif registry and status == 'SUPERSEDED' and superseded_by_n:
        by_v = ''
        for sib in registry.get('deposits', []):
            if sib.get('deposit_number') == superseded_by_n:
                by_v = sib.get('version', '')
                break
        version_banner = (
            '<div style="background:#fef3c7;border-left:4px solid #d97706;padding:12px 16px;'
            'border-radius:6px;margin:12px 0;font-size:.92em">'
            + (
                # Version-supersession language ONLY when the two version strings
                # genuinely differ (SAMEVER class fix, 2026-08-04): a record whose
                # version equals its successor's — or where either label is absent —
                # is a record supersession (duplicate witness, record of standing),
                # and "this is v1.0, current version v1.0" is self-refuting.
                f'<div style="font-weight:600;color:#92400e;margin-bottom:4px">⚠ Superseded — this is version {esc(version)}</div>'
                f'<div style="color:#78350f">Current version: <a href="/s/records/{superseded_by_n}/" '
                f'style="color:var(--accent);font-weight:500">#{superseded_by_n} {esc(by_v)}</a></div>'
                if version and by_v and version.strip() != by_v.strip() else
                f'<div style="font-weight:600;color:#92400e;margin-bottom:4px">⚠ Superseded</div>'
                f'<div style="color:#78350f">The record of standing for this work is <a href="/s/records/{superseded_by_n}/" '
                f'style="color:var(--accent);font-weight:500">#{superseded_by_n}</a></div>'
            )
            + (f'<div style="color:#78350f;font-size:.88em;margin-top:6px">{esc(superseded_reason)}</div>' if superseded_reason else '')
            + '</div>'
        )
    elif d.get('body_status', {}).get('class') == 'metadata_capture':
        # Semi-restored pointer banner (2026-07-30, MANUS-directed): a capture
        # must never present as the whole work. Two truthful states:
        #   full_version present  -> point forward to the complete deposit
        #   absent                -> say plainly the complete work is not yet
        #                            restored here (restoration candidate)
        fv = d.get('body_status', {}).get('full_version') or {}
        if fv.get('deposit_number'):
            version_banner = (
                '<div style="background:#e0f2fe;border-left:4px solid #0369a1;padding:12px 16px;'
                'border-radius:6px;margin:12px 0;font-size:.92em">'
                '<div style="font-weight:600;color:#0c4a6e;margin-bottom:4px">◐ Semi-restored capture — the complete work exists in this archive</div>'
                f'<div style="color:#075985">Complete version: <a href="/s/records/{fv["deposit_number"]}/" '
                f'style="color:var(--accent);font-weight:500">#{fv["deposit_number"]} — {esc(fv.get("title",""))[:90]}</a>'
                f' <span style="font-size:.85em;opacity:.8">({esc(fv.get("axn",""))})</span></div>'
                f'<div style="color:#075985;font-size:.85em;margin-top:6px">Pairing basis: {esc(fv.get("basis",""))}. '
                'This record preserves the metadata capture; read the complete version for the full text.</div>'
                '</div>'
            )
        else:
            version_banner = (
                '<div style="background:#fef3c7;border-left:4px solid #d97706;padding:12px 16px;'
                'border-radius:6px;margin:12px 0;font-size:.92em">'
                '<div style="font-weight:600;color:#92400e;margin-bottom:4px">◐ Semi-restored metadata capture</div>'
                '<div style="color:#78350f">This record preserves metadata and a partial body only. '
                'The complete work is <strong>not yet restored in this archive</strong>; do not cite this page as the full text. '
                'It is queued for restoration (see <code>data/worklists/semi-restored-pairing-queue.json</code>).</div>'
                '</div>'
            )
    elif status == 'DRAFT_PENDING':
        reason = d.get('draft_pending_reason', '')
        version_banner = (
            '<div style="background:#f3f4f6;border-left:4px solid #6b7280;padding:12px 16px;'
            'border-radius:6px;margin:12px 0;font-size:.92em">'
            '<div style="font-weight:600;color:#374151;margin-bottom:4px">⏳ Draft — body not yet written</div>'
            f'<div style="color:#4b5563">This deposit\'s identifier and metadata are minted, but the body has not been written.'
            + (f' {esc(reason)}' if reason else '')
            + '</div></div>'
        )

    mods = d.get('modifications') or []
    mods_html = ''
    if mods:
        rows = ''.join(
            f'<li style="margin:.25rem 0"><span style="opacity:.7">{esc(m.get("date",""))}</span> — '
            f'<strong style="font-weight:600">{esc(m.get("field",""))}</strong>: {esc(m.get("reason",""))}</li>'
            for m in mods[-8:])
        mods_html = ('<section style="margin:1.2rem 0;padding:.8rem 1rem;border-left:3px solid var(--rule,rgba(127,127,127,.3));'
                     'font-size:.85em"><div style="font-weight:600;margin-bottom:.3rem">Record modifications</div>'
                     f'<ul style="margin:0;padding-left:1.1rem">{rows}</ul>'
                     '<div style="opacity:.65;margin-top:.4rem;font-size:.92em">The deposited text is immutable; '
                     'these are changes to the record\'s metadata and declared state.</div></section>')

    traversal_html = _traversal_html(d, registry)


    if registry and series_id:
        siblings = sorted(
            (s for s in registry.get('deposits', []) if s.get('version_series_id') == series_id),
            key=lambda x: x.get('deposit_number', 0)
        )
        if len(siblings) > 1:
            is_supersession_series = any(s.get('superseded_by_deposit_number') for s in siblings)
            label = 'Version history' if is_supersession_series else 'Series entries'
            items = []
            for sib in siblings:
                sib_n = sib.get('deposit_number')
                sib_v = sib.get('version', '')
                sib_status = sib.get('status', 'ACTIVE')
                is_current = (sib_n == dn)
                bullet = '●' if is_current else '○'
                tail = ''
                if sib_status == 'SUPERSEDED':
                    tail = ' <span style="color:#999;font-size:.85em">(superseded)</span>'
                elif sib_status == 'ACTIVE' and is_supersession_series:
                    tail = ' <span style="color:var(--teal);font-size:.85em">— current</span>'
                if is_current:
                    items.append(
                        f'<li style="font-weight:500">{bullet} #{sib_n} {esc(sib_v)}{tail} '
                        f'<span style="color:#777;font-weight:normal">← this deposit</span></li>'
                    )
                else:
                    items.append(f'<li>{bullet} <a href="/s/records/{sib_n}/">#{sib_n} {esc(sib_v)}</a>{tail}</li>')
            version_history = (
                f'<h2>{label}</h2>'
                f'<p class="subtle" style="color:#777;font-size:.85em;margin-bottom:8px">'
                f'Series: <code style="font-family:var(--mono);font-size:.85em">{esc(series_id)}</code></p>'
                f'<ul style="list-style:none;padding-left:0;font-size:.92em;line-height:1.8">'
                + ''.join(items) + '</ul>'
            )

    _files = d.get('files') or []

    files_html = ''

    if _files:

        def _fmt_bytes(b):

            return f'{b/1048576:.1f} MB' if b >= 1048576 else f'{b/1024:.0f} KB'

        _btns = ' '.join(

            f'<a style="display:inline-block;background:var(--teal);color:#fff;padding:6px 14px;'

            f'border-radius:4px;font-size:.82em;text-decoration:none;margin:6px 4px 6px 0" '

            f'href="{f["path"]}" download>↓ {f["filename"]} ({_fmt_bytes(f["bytes"])})</a>'

            for f in _files)

        _shas = '<br>'.join(f'<code style="font-size:.72em;color:#888">sha256 {f["sha256"]}</code>' for f in _files)

        files_html = f'<h2>Files</h2><div style="border:1px solid #ddd;border-radius:6px;padding:10px 14px;margin:8px 0">{_btns}<div style="margin-top:6px">{_shas}</div></div>'


    kw_html = ''.join(f'<span style="display:inline-block;background:#f0f4f8;color:var(--accent);padding:2px 8px;border-radius:10px;font-size:.78em;margin:2px">{esc(k)}</span>' for k in d.get('keywords', []))
    
    # Wiki article section
    wiki_html = ''
    if d.get('wiki_article'):
        wiki_text = esc(d['wiki_article'])
        wiki_text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', wiki_text)
        wiki_text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', wiki_text)
        wiki_html = f'<h2>Wiki Article</h2>\n<div style="background:#f8f9fa;border:1px solid var(--border);border-radius:6px;padding:16px;margin:8px 0;font-size:.88em;line-height:1.75;color:#333">{wiki_text}</div>'
    
    # Concepts section
    concepts_html = ''
    defines = d.get('defines_concepts', [])
    if defines:
        concept_items = []
        for term in defines:
            info = eidx['concepts'].get(term, {})
            defn = esc(info.get('definition', ''))
            ctype = esc(info.get('type', ''))
            concept_items.append(f'<div style="margin:6px 0;padding:8px;background:#f0f8f0;border-left:3px solid var(--teal);border-radius:0 4px 4px 0"><strong style="color:var(--teal)">{esc(term)}</strong> <span style="font-size:.75em;color:#999">[{ctype}]</span><br><span style="font-size:.85em;color:#444">{defn}</span></div>')
        concepts_html = f'<h2>Concepts Defined</h2>\n' + '\n'.join(concept_items)
    
    # Entity triples section
    triples_html = ''
    if d.get('entity_triples'):
        triple_items = []
        for t in d['entity_triples'][:15]:
            s, p, o = esc(t.get('subject','')), esc(t.get('predicate','')), esc(t.get('object',''))
            triple_items.append(f'<div style="font-family:var(--mono);font-size:.78em;color:#555;padding:2px 0">{s} → <span style="color:var(--teal)">{p}</span> → {o}</div>')
        triples_html = f'<h2>Entity Graph</h2>\n<div style="background:#fafafa;border:1px solid var(--border);border-radius:4px;padding:10px;margin:8px 0">' + '\n'.join(triple_items) + '</div>'
    
    # External-metadata sidecar surfacing (Phase 5 wiring)
    external_metadata_html = ''
    ext_path = d.get('external_metadata_path')
    if ext_path:
        sev = d.get('datacite_severance', '')
        oa_ids = d.get('openalex_ids') or []
        oa_count = len([x for x in oa_ids if x])
        sev_color = {'severed': 'var(--accent2)', 'retained': 'var(--teal)', 'mixed': 'var(--accent)', 'typo_immunity': 'var(--teal)'}.get(sev, 'var(--dim)')
        sev_label = {'severed': 'severed from DataCite', 'retained': 'retained in DataCite', 'mixed': 'mixed severance', 'typo_immunity': 'typo-immunity (escaped severance)'}.get(sev, sev or '—')
        ext_path_html = esc(ext_path)
        parts = ['<h2>External Metadata</h2>',
                 '<div style="background:#f7f9fb;border:1px solid var(--border);border-radius:6px;padding:14px;margin:8px 0;font-size:.88em;line-height:1.6">']
        parts.append(f'<div style="margin-bottom:8px"><strong>Sidecar:</strong> <a href="{ext_path_html}" style="font-family:var(--mono);font-size:.85em">{ext_path_html}</a></div>')
        parts.append(f'<div style="margin-bottom:8px"><strong>DataCite severance status:</strong> <span style="color:{sev_color};font-weight:500">{esc(sev_label)}</span></div>')
        if oa_count:
            oa_links_parts = []
            for oid in oa_ids:
                if not oid: continue
                short = oid.replace('https://openalex.org/', '')
                oa_links_parts.append(f'<li style="margin:2px 0"><a href="{esc(oid)}" style="font-family:var(--mono);font-size:.83em">{esc(short)}</a></li>')
            oa_links = '\n'.join(oa_links_parts)
            parts.append(f'<div style="margin-bottom:4px"><strong>OpenAlex Work IDs ({oa_count}):</strong></div><ul style="list-style:disc inside;font-size:.83em;color:#666">{oa_links}</ul>')
        zd = d.get('zenodo_dois') or []
        if isinstance(zd, str): zd = [zd] if zd else []
        if zd:
            doi_items_parts = []
            for doi in zd[:10]:
                doi_items_parts.append(f'<li style="margin:2px 0"><span style="font-family:var(--mono);font-size:.83em;color:#666">{esc(doi)}</span></li>')
            doi_items = ''.join(doi_items_parts)
            more = f'<li style="color:#999;font-size:.83em">…and {len(zd)-10} more</li>' if len(zd) > 10 else ''
            parts.append(f'<div style="margin-top:8px;margin-bottom:4px"><strong>Legacy Zenodo DOIs ({len(zd)}):</strong></div><ul style="list-style:disc inside;font-size:.83em;color:#666">{doi_items}{more}</ul>')
        parts.append('<div style="margin-top:8px;color:var(--dim);font-size:.78em">External metadata recovered post-severance (non-authoritative). The sidecar maps each DOI to its locator in the bulk data stores.</div>')
        parts.append('</div>')
        external_metadata_html = '\n'.join(parts)

    # Build page
    # W13 tier 1.5: KaTeX for records carrying display math. Injected only when
    # $$ blocks are present; throwOnError:false degrades conversion-mangled
    # LaTeX to visible source instead of breaking the page. \Chi macro covers
    # the capture-era capital-chi mangle. Bytes untouched — presentation only.
    _katex_head = ''
    if '$$' in fulltext_marked:
        _katex_head = (
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">'
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>'
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" '
            'onload="renderMathInElement(document.body,{delimiters:[{left:\'$$\',right:\'$$\',display:true}],'
            'throwOnError:false,macros:{\'\\\\Chi\':\'\\\\mathrm{X}\'}})"></script>'
        )
    page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(d["title"])} — Alexanarch</title><meta name="description" content="{esc(_compose_meta_description(d))}"><meta property="og:title" content="{esc(str(d["title"])[:95])}"><meta property="og:description" content="{esc(_compose_meta_description(d))}"><meta property="og:url" content="{_rec_url}"><meta property="og:type" content="article"><meta property="og:site_name" content="Alexanarch"><meta name="twitter:card" content="summary"><script type="application/ld+json">{jsonld}</script>{_katex_head}
<link rel="resourcesync" href="https://www.alexanarch.org/.well-known/resourcesync">
<link rel="alternate" type="application/xml" title="OAI-PMH 2.0" href="https://www.alexanarch.org/oai?verb=Identify">
<link rel="canonical" href="https://www.alexanarch.org/s/records/{dn}/">
<meta name="citation_title" content="{esc(d["title"])}">
<meta name="citation_author" content="{esc(d["creator"])}">
<meta name="citation_publication_date" content="{esc(d["date"])}">
<meta name="citation_online_date" content="{esc(d["date"])}">
<meta name="citation_journal_title" content="{esc(d.get("journal") or "Alexanarch")}">
<meta name="citation_publisher" content="{esc(d.get("publisher") or "Alexanarch")}">
<meta name="citation_abstract" content="{esc(d.get("description",""))}">
<meta name="citation_public_url" content="https://www.alexanarch.org/s/records/{dn}/">
<meta name="citation_fulltext_html_url" content="https://www.alexanarch.org/s/records/{dn}/">
<meta name="citation_pdf_url" content="https://www.alexanarch.org/papers/AXN-{hex_id.zfill(4)}.pdf">
<meta name="citation_language" content="en">
<meta name="DC.title" content="{esc(d["title"])}">
<meta name="DC.creator" content="{esc(d["creator"])}">
<meta name="DC.date" content="{esc(d["date"])}" scheme="DCTERMS.W3CDTF">
<meta name="DC.identifier" content="https://www.alexanarch.org/s/axn/{hex_id}/" scheme="DCTERMS.URI">
<meta name="DC.description" content="{esc(d.get("description",""))}">
<meta name="DC.language" content="en" scheme="DCTERMS.RFC3066">
<meta name="DC.type" content="{esc(d.get("content_type",""))}">
<meta name="DC.rights" content="CC BY 4.0">
<meta name="DC.publisher" content="{esc(d.get("publisher") or "Alexanarch")}">
<meta name="DC.source" content="https://www.alexanarch.org/">
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.8;font-size:15px}}.wrap{{max-width:720px;margin:0 auto;padding:60px 24px}}a{{color:var(--accent);text-decoration:none}}a:hover{{color:var(--accent2)}}h1{{font-size:1.3em;font-weight:600;color:var(--accent);margin-bottom:8px}}h2{{font-size:1em;font-weight:500;color:var(--accent);margin-top:20px;margin-bottom:6px;border-bottom:1px solid var(--border);padding-bottom:3px}}p{{margin-bottom:10px;color:#333}}.nav{{display:flex;gap:12px;margin-bottom:24px;font-size:.85em;overflow-x:auto;white-space:nowrap}}.nav a{{color:#777;font-weight:500;text-decoration:none}}.nav a:hover{{color:var(--accent)}}.ft{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:20px;max-height:600px;overflow-y:auto;font-size:.88em;line-height:1.75;margin:8px 0;color:#333}}.ft h1,.ft h2,.ft h3{{color:var(--accent);margin:12px 0 6px}}.ft h1{{font-size:1.1em}}.ft h2{{font-size:1em;border-bottom:none}}.ft h3{{font-size:.95em}}.ft strong{{color:var(--fg)}}.ft blockquote{{border-left:3px solid var(--teal);padding-left:12px;color:#555;margin:8px 0}}.ft hr{{border:none;border-top:1px solid var(--border);margin:12px 0}}.footer{{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}}</style>
</head><body><div class="wrap">
{render_navbar()}
<div role="text" aria-label="{esc(_axn_aria(d["axn"]))}" style="font-family:var(--mono);font-size:1.1em;color:var(--teal);background:var(--surface);padding:12px;border-radius:6px;border-left:4px solid var(--teal);margin:12px 0">{esc(d["axn"])}</div>
{version_banner}
<h1>{esc(d["title"])}</h1>
<div style="font-size:.85em;color:#777;margin-bottom:10px">{esc(d["creator"])} · {esc(d["date"])} · {esc(d.get("content_type",""))}{f' · <span style="color:var(--accent);font-weight:500">{esc(version)}</span>' if (version and (version != 'v1.0' or series_id)) else ''}</div>
<a style="display:inline-block;background:var(--teal);color:#fff;padding:6px 14px;border-radius:4px;font-size:.82em;text-decoration:none;margin:6px 0" href="/data/deposits/AXN-{hex_id}.md" download>↓ Download MD</a> <a style="display:inline-block;background:var(--accent);color:#fff;padding:6px 14px;border-radius:4px;font-size:.82em;text-decoration:none;margin:6px 0 6px 4px" href="/papers/AXN-{hex_id.zfill(4)}.pdf">↓ PDF</a>
<div style="margin:8px 0">{kw_html}</div>
<h2>Description</h2>
<p style="font-size:.9em">{esc(d.get("description",""))}</p>
{external_metadata_html}
{version_history}
{mods_html}
{files_html}
{traversal_html}
{wiki_html}
{concepts_html}
{triples_html}
<h2>Full Text</h2>
{apparatus_html}
<div class="ft">{fulltext_marked}</div>
<script data-goatcounter="https://alexanarch.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<div class="footer"><strong>Alexanarch</strong> · Self-governing static archive<div style="color:var(--accent)">∮ = 1</div></div>
</div></body></html>'''
    
    os.makedirs(f's/records/{dn}', exist_ok=True)
    with open(f's/records/{dn}/index.html', 'w') as f:
        f.write(page)


if __name__ == '__main__':
    # Test with deposit #1
    wire_deposit(1)
    print("Test complete.")
