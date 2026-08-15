#!/usr/bin/env python3
"""Wire deposit reading results into all data structures and regenerate static page."""

import json, html as htmlmod, re, os, sys
import pathlib as _ppath

# Import canonical navbar renderer (single source of truth: data/navigation.json)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'scripts'))
from record_state import derive_state   # single canonical state; see scripts/record_state.py
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
        t = _inline_md(esc(e['title'])[:88])
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
    # W14b (2026-08-09): the cut fires only when the section actually RESTATES
    # the field — its normalized length must not materially exceed the field's.
    # Before this guard, a section whose opening matched but which carried
    # additional content (tables, extended prose beyond the field) was
    # swallowed whole; observed on #1 (tables lost) the moment the W14
    # heading-duplication heal stopped defeating the prefix match. A dedup
    # that can delete content the field does not hold is not a dedup.
    _section = after[:nxt.start()] if nxt else after
    if len(norm(_section)) > max(len(norm(description)) * 1.25, len(norm(description)) + 200):
        return fulltext
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


def _render_inline(text):
    """Render a description's inline markdown. Added 2026-08-06.

    The description block escaped its field and emitted it raw, so authored
    emphasis reached readers as literal underscores and asterisks — MANUS on
    #1121: "record conformance at the human display end is a mess." The same
    defect had been found and fixed on the wiki pages the day before; it was
    present here and went unnoticed because every check measured FIELDS rather
    than reading a RENDERED PAGE end to end. Escaping happens first.
    """
    import re as _re
    t = htmlmod.escape(str(text or ''))
    t = _re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = _re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    t = _re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t



def _inline_md(t):
    """Inline markdown for body lines: links, bold, em, code. Added 2026-08-10.

    Two gaps found by reading rendered pages one at a time rather than counting.
    Headings emitted line[N:] with NO inline pass, so '## **Title**' kept its
    asterisks and '# [Name](url)' kept its brackets — the work's own primary
    link, dead text on the page. List items ran bold and em but not links, so
    every '- ORCID: [id](https://orcid.org/id)' rendered literally: 51 of them
    on #90 alone. Input is already HTML-escaped.
    """
    # (?<!!) leaves image syntax alone: '![](url)' is the image renderer's,
    # and matching it here produced '<a>![</a>](url)' on #1113 and #1112.
    # [^<>] stops a match spanning an anchor this pass has already made.
    t = re.sub(r'(?<!!)\[([^\]\n<>]{1,120})\]\((https?://[^\s)<>]+|/[^\s)<>]+)\)',
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    # non-greedy and asterisk-permitting: bold frequently wraps an italic,
    # '**Kierkegaard (*Fear and Trembling*, 1843):**', and a [^*] class cannot
    # span the inner pair — three such on #99 alone.
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', t)
    return t



def _kernel_split(raw):
    """Separate a leading holographic kernel from the work. Added 2026-08-10.

    Some deposits open with an HTML comment and a JSON-LD block. #828 states
    what they are: "HOLOGRAPHIC KERNEL — CANONICAL PROVENANCE. Any extraction
    stripping this block produces a ghost document." They are a deliberate
    anti-extraction device and MUST stay in the canonical bytes.

    I removed one from #137 to fix a display problem, which was the wrong fix in
    the wrong layer. Canonical bytes are not edited to change how a page looks.
    The kernel is separated for PRESENTATION only, rendered as a collapsed block
    ahead of the work, and the bytes are untouched.
    """
    # a kernel may sit behind a leading horizontal rule (#402)
    raw = re.sub(r'\\A(\\s*-{3,}\\s*\\n)+', '', raw)
    m = re.match(r'\s*(<!--.*?-->)\s*(\{.*?\n\})\s*', raw, re.S)
    if not m:
        m2 = re.match(r'\s*(<!--.*?-->)\s*', raw, re.S)
        return (m2.group(1), raw[m2.end():]) if m2 else (None, raw)
    return (m.group(1) + '\n' + m.group(2), raw[m.end():])


def _clean_apparatus(html_frag):
    """Convert markdown headings the body renderer left literal inside the
    restoration wrapper. Added 2026-08-06.

    The W10 split happens AFTER html conversion, so any heading line the body
    renderer did not convert survives into the apparatus block as a literal
    '# Title' — visible on all 128 wrapper records. The wrapper is apparatus,
    so its headings render as bold lines rather than document headings, which
    keeps them out of the page's heading outline.
    """
    import re as _re
    def _h(m):
        return '<p style="font-weight:600;margin:8px 0 2px">' + m.group(2).strip() + '</p>'
    out = _re.sub(r'(?m)^\s*(#{1,6})\s+(.+?)\s*$', _h, html_frag)
    out = _re.sub(r'(>)\s*(#{1,6})\s+([^<]+)', lambda m: m.group(1) + '<strong>' + m.group(3).strip() + '</strong>', out)
    html_frag = _inline_md(html_frag) if '**' in html_frag else html_frag
    return out


def _html_escape(t):
    return (t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))


def regenerate_static_page(d, eidx, registry=None):
    _kernel_html = ''
    """Regenerate the static HTML page for a deposit with full enrichment.

    registry: optional full registry dict. If provided, enables version-chain
    blocks (banner for superseded/draft, version history list for series).
    If None, version blocks are omitted (faster but less informative).
    """
    esc = lambda s: htmlmod.escape(str(s)) if s else ''
    dn = d['deposit_number']
    # SURGICAL-LAYER GUARD (2026-08-15, atlas addendum v1.3). Record pages are
    # renderer output PLUS post-render surgical layers (the superseded-record
    # retirement apparatus: noindex, axn:retired, repointed canonical, the
    # cite-instead banner). This renderer does not know how to reproduce them,
    # so re-rendering such a page DESTROYS them — proven on #1400, 2026-08-15,
    # reverted. Refuse unless explicitly forced; this converts "did not look"
    # (the one failure class no gate catches) into "cannot proceed".
    _page_path = _ppath.Path(f's/records/{dn}/index.html')
    if _page_path.exists() and 'axn:retired' in _page_path.read_text(encoding='utf-8', errors='replace') \
            and not os.environ.get('ALEXANARCH_FORCE_RERENDER'):
        raise RuntimeError(
            f"REFUSED: s/records/{dn}/ carries the retirement apparatus (axn:retired), "
            f"which this renderer would strip. See atlas addendum v1.3. "
            f"Set ALEXANARCH_FORCE_RERENDER=1 only if you will re-apply the surgical layers.")
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
        **({"version": d['version']} if d.get('version') else {}),
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
                _fp[_pi] = re.sub(r'(?<=[^\n#])(#{2,6} )', r'\n\n\1', _fp[_pi])
            raw = '```'.join(_fp)
            _kernel, raw = _kernel_split(raw)
            _plain = _plain_body(raw)

            _kernel_html = ('<details style="margin:0 0 12px"><summary style="cursor:pointer;'
                            'font-family:ui-monospace,monospace;font-size:.78em;letter-spacing:'
                            '.1em;text-transform:uppercase;color:#8a6a20">Holographic kernel — '
                            'canonical provenance</summary><pre style="white-space:pre-wrap;'
                            'font-size:.76em;color:#666;margin:8px 0 0;overflow-x:auto">'
                            + _html_escape(_kernel) + '</pre></details>') if _kernel else ''
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
            _COMMA_MANGLE = re.compile(r'(?<=[a-zA-Z0-9})\]]) , (?=\\(?!ldots|dots|cdots|quad|qquad|text|mathrm\b|mbox))')
            def _fix_math_span(m):
                # W13 tier 1.5 addendum (MANUS view-flag 2026-08-04): the LaTeX
                # thin-space \, lost its backslash in capture conversion and
                # became a literal comma (" -\sigma , \nabla" was "-\sigma \,
                # \nabla"). Deterministic signature: space-comma-space followed
                # by a backslash command, with the legitimate ", \ldots" family
                # excluded. Display-level; bytes carry the mangle until tier 2.
                return '$$' + _COMMA_MANGLE.sub(r' \\, ', m.group(1)) + '$$'
            for _pi in range(0, len(_fence_parts), 2):  # even indices = outside fences
                _fence_parts[_pi] = re.sub(r'(?<=[^\n#])(#{2,6} )', r'\n\n\1', _fence_parts[_pi])
                _fence_parts[_pi] = re.sub(r'\$\$(.+?)\$\$', _fix_math_span, _fence_parts[_pi], flags=re.S)
                _fence_parts[_pi] = _w13_reflow(_fence_parts[_pi])
            raw = '```'.join(_fence_parts)
            lines = raw.split('\n')
            # W14 wrap-mode switch: paragraph merging activates ONLY for bodies
            # that are statistically hard-wrapped (many mid-length prose lines
            # ending mid-sentence). House canonical bodies flow one line per
            # paragraph, and line-oriented blocks (SPXI provenance stanzas,
            # key:value rows, flush-left verse) use single newlines
            # meaningfully — those bodies render line-per-<p> exactly as
            # before. Known-answer tested against #1 (verse+stanzas), #1437
            # (flowing), #1443 (hard-wrapped) on 2026-08-09.
            _prose_idx = [i for i, l in enumerate(lines)
                          if l.strip() and l[:1] not in (' ', '\t')
                          and not l.lstrip().startswith(('#', '|', '-', '>', '`', '!', '<'))]
            def _next_nonblank(i):
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        return lines[j].lstrip()
                return ''
            # Wrap evidence requires a lowercase CONTINUATION on the following
            # line: key:value stanzas ("**Packet ID:** …" rows) and headed
            # blocks never continue lowercase, while a hard-wrapped sentence
            # almost always does. This is what keeps #1437's metadata stanzas
            # rendering line-per-<p> while #1443's wrapped prose merges.
            _wrapped = [i for i in _prose_idx
                        if 55 <= len(lines[i]) <= 95
                        and not lines[i].rstrip().rstrip('*_').endswith(('.', ':', ';', '!', '?'))
                        and _next_nonblank(i)[:1].islower()]
            _wrap_mode = len(_prose_idx) >= 8 and (len(_wrapped) / len(_prose_idx)) > 0.25
            ft_lines = []
            in_pre = False
            pre_buf = []
            _img_re = re.compile(r'^!\[([^\]]*)\]\((/?data/attachments/[A-Za-z0-9._/\-]+)\)\s*$')
            _pre_style = ('font-family:var(--mono);font-size:.82em;background:#f8f9fa;'
                          'border:1px solid var(--border);border-radius:6px;padding:12px 14px;'
                          'margin:12px 0;white-space:pre;overflow-x:auto;line-height:1.55;color:#333')
            _tbl_buf = []
            _list_buf = []
            _p_buf = []
            def _p_flush():
                # W14 (2026-08-09, #1443/#1444 repair): paragraphs accumulate across
                # single newlines and flush at structural boundaries. Canonical bodies
                # flow, but a hard-wrapped source must not render as one <p> per
                # wrap. Inline emphasis is applied to the JOINED text so bold/italic
                # spanning a source wrap survives.
                if _p_buf:
                    _joined = ' '.join(_p_buf)
                    _joined = _inline_md(_joined)
                    ft_lines.append(f'<p>{_joined}</p>')
                    _p_buf.clear()
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
                # Ruled rather than boxed: a horizontal rule under the header and a
                # hairline between rows, which is how a scholarly table is set. Full
                # gridlines make a table look like a spreadsheet and read like one.
                _h = ['<div style="overflow-x:auto;margin:18px 0">'
                      '<table style="border-collapse:collapse;font-size:.88em;line-height:1.5;'
                      'width:100%;min-width:340px">']
                for _i, _r in enumerate(_rows):
                    _tag = 'th' if _i == _hdr_idx else 'td'
                    _last = (_i == len(_rows) - 1)
                    if _tag == 'th':
                        _st = ('border-bottom:1.5px solid var(--fg,#333);padding:7px 12px 6px 0;'
                               'text-align:left;vertical-align:bottom;font-weight:600;'
                               'font-size:.92em;letter-spacing:.03em;text-transform:uppercase;'
                               'white-space:nowrap;')
                    else:
                        _st = ('padding:8px 12px 8px 0;text-align:left;vertical-align:top;'
                               + ('' if _last else 'border-bottom:1px solid var(--border);'))
                    _r = _r + [''] * (_ncol - len(_r))
                    _h.append('<tr>' + ''.join(f'<{_tag} style="{_st}">{_inline_md(c)}</{_tag}>' for c in _r) + '</tr>')
                _h.append('</table></div>')
                return ''.join(_h)
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('```'):
                    _p_flush()
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
                    _p_flush()
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
                    _p_flush()
                    _tbl_buf.append(line.strip())
                    continue
                elif _tbl_buf:
                    ft_lines.append(_flush_table(_tbl_buf))
                    _tbl_buf = []
                # W13 tier 1.5: list buffer — consecutive '- ' lines become a <ul>
                if line.startswith('- '):
                    _p_flush()
                    _li = _inline_md(line[2:])
                    _list_buf.append(_li)
                    continue
                elif _list_buf:
                    ft_lines.append('<ul style="margin:8px 0 8px 22px;padding:0">' + ''.join(f'<li style="margin:3px 0">{x}</li>' for x in _list_buf) + '</ul>')
                    _list_buf = []
                # W14: each structural line flushes the paragraph buffer and
                # CONTINUES — the missing continue here was the heading-duplication
                # defect (a converted <hN> followed by the literal '<p># ...' from
                # the fall-through into the image chain below, live on every
                # heading-bearing record rendered since the 2026-08-04 image block).
                if line.startswith('# '): _p_flush(); ft_lines.append(f'<h1>{_inline_md(line[2:])}</h1>'); continue
                if line.startswith('## '): _p_flush(); ft_lines.append(f'<h2>{_inline_md(line[3:])}</h2>'); continue
                if line.startswith('### '): _p_flush(); ft_lines.append(f'<h3>{_inline_md(line[4:])}</h3>'); continue
                if line.startswith('#### '): _p_flush(); ft_lines.append(f'<h4>{_inline_md(line[5:])}</h4>'); continue
                if line.startswith('---') or re.fullmatch(r'\s*(\*\s*){3,}', line) \
                        or re.fullmatch(r'\s*(_\s*){3,}', line):
                    # '***', '****', '___' are horizontal rules too; four asterisks
                    # rendered as literal '****' on the visual-schema records.
                    _p_flush(); ft_lines.append('<hr>'); continue
                if line.startswith('&gt;'): _p_flush(); ft_lines.append(f'<blockquote style="border-left:3px solid var(--teal);padding-left:12px;color:#555;margin:8px 0">{_inline_md(line[4:])}</blockquote>'); continue
                # IMAGE RENDERING (MANUS 2026-08-04: "long image url blob — why
                # not just include the image?"). Markdown image syntax and bare
                # image URLs were rendering as 240-character raw URLs. 88 records,
                # 134 references. Render the image; keep the URL reachable via the
                # link, and never inline anything but a known image host.
                line = re.sub(r'^\s*\*\*(!?\[[^\]]*\]\([^)]+\))\*\*\s*$', r'\1', line)
                _im = re.match(r'^\s*!?\[[^\]]*\]\((https?://[^\s\)]+|/[^\s\)]+\.(?:png|jpe?g|gif|webp|svg))(?:\s+&quot;[^&]*&quot;)?\)\s*$', line, re.I) \
                      or re.match(r'^\s*(https?://\S+\.(?:png|jpe?g|gif|webp))\s*$', line, re.I) \
                      or re.match(r'^\s*[-*]\s+(https://blogger\.googleusercontent\.com/img/\S+)\s*$', line) \
                      or re.match(r'^\s*(https://blogger\.googleusercontent\.com/img/\S+)\s*$', line)
                if _im:
                    _p_flush()
                    _u = _im.group(1)
                    ft_lines.append(
                        f'<figure style="margin:14px 0"><a href="{esc(_u)}" target="_blank" rel="noopener">'
                        f'<img src="{esc(_u)}" alt="" loading="lazy" '
                        f'style="max-width:100%;height:auto;border-radius:6px;border:1px solid var(--border)">'
                        f'</a></figure>')
                    continue
                elif line[:1] in (' ', '\t') and line.strip():
                    # SOURCE-282 addendum (2026-08-04): leading whitespace is
                    # prosodic structure (indentation clusters, staggered
                    # arrangements); preserve it instead of letting HTML
                    # collapse it. Applies only to lines that carry it —
                    # rendered per-line with per-line emphasis, byte-compatible
                    # with the pre-W14 output for poetry records.
                    _p_flush()
                    _l = _inline_md(line)
                    ft_lines.append(f'<p style="white-space:pre-wrap;margin:2px 0">{_l}</p>')
                elif line.strip():
                    if _wrap_mode:
                        # Line-precise continuation: merge only when the PREVIOUS
                        # buffered line is shaped like a mid-sentence wrap (long,
                        # no terminal punctuation) AND this line reads as its
                        # continuation. Key:value stanza rows and short standalone
                        # lines therefore keep their own <p> even inside a
                        # hard-wrapped body (#1437's packet header, tested).
                        _prev = _p_buf[-1] if _p_buf else ''
                        _cont = (_p_buf
                                 and len(_prev) >= 45
                                 and not _prev.rstrip().rstrip('*_').endswith(('.', ':', ';', '!', '?'))
                                 and (line[:1].islower() or line[:1] == '('
                                      or _prev.rstrip().endswith((',', '\u2014', '\u2013'))))
                        if not _cont:
                            _p_flush()
                        _p_buf.append(line)
                    else:
                        ft_lines.append(f'<p>{_inline_md(line)}</p>')
                else:
                    _p_flush(); ft_lines.append('')
            _p_flush()
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
    # Apparatus lifted OUT of the body by scripts/separate_apparatus.py is
    # rendered here, after the work. Nothing was destroyed — it moved to where
    # apparatus belongs, and the store path is published on the record.
    lifted_apparatus_html = ''
    _ap = d.get('apparatus_path')
    if _ap:
        try:
            import json as _json
            _a = _json.load(open('.' + _ap))
            _parts = []
            if _a.get('head_apparatus'):
                _parts.append('<div style="font-family:ui-monospace,monospace;font-size:.82em;'
                              'white-space:pre-wrap;color:#555">' + _inline_md(_html_escape(_a['head_apparatus'])) + '</div>')
            if _a.get('tail_apparatus'):
                _parts.append('<details style="margin-top:10px"><summary style="cursor:pointer;'
                              'font-size:.85em;color:#666">Superseded metadata-capture body '
                              '(retained, not destroyed) — this describes an earlier state of the '
                              'record and does not describe it as it now stands</summary>'
                              '<div style="font-family:ui-monospace,monospace;font-size:.78em;'
                              'white-space:pre-wrap;color:#666;margin-top:8px">'
                              + _inline_md(_html_escape(_a['tail_apparatus'])) + '</div></details>')
            if _parts:
                lifted_apparatus_html = (
                    '<h2>Processing apparatus</h2><div style="background:#fafafa;border:1px solid '
                    'var(--border);border-radius:6px;padding:14px;margin:10px 0">'
                    '<div style="font-size:.85em;color:#666;margin-bottom:8px">Restoration and '
                    'modification notes, lifted out of the deposited body so the body is the work. '
                    'Nothing was destroyed: the full lifted text is at '
                    '<a href="' + _ap + '">' + _ap + '</a>.</div>' + ''.join(_parts) + '</div>')
        except Exception:
            lifted_apparatus_html = ''

    # ONE H1 PER PAGE. The body carries the work's own title, and the record page
    # already declares it — so a reader's outline showed the same document three
    # times and a crawler saw three competing document headings. In-body headings
    # are demoted one level; the page keeps a single h1.
    # AN UNCLOSED TAG ON A LINE IS TEXT, NOT MARKUP. Documents that DISCUSS html
    # were having their examples eaten by the browser: SPXI for Websites (#72)
    # writes "One <h1 per page (entity name)" as a conformance rule, and the page
    # emitted it raw, so the browser opened a heading and swallowed the sentence.
    # The rule that a tag must close on its own line separates prose about markup
    # from markup, without a whitelist and without touching legitimate embedded html.
    def _escape_unclosed(line):
        out, i = [], 0
        while i < len(line):
            c = line[i]
            if c == '<' and i + 1 < len(line) and (line[i+1].isalpha() or line[i+1] == '/'):
                close = line.find('>', i)
                if close == -1:
                    out.append('&lt;'); i += 1; continue
            out.append(c); i += 1
        return ''.join(out)
    fulltext_marked = '\n'.join(_escape_unclosed(l) for l in fulltext_marked.split('\n'))

    fulltext_marked = re.sub(r'<h3([ >])', r'<h4\1', fulltext_marked)
    fulltext_marked = re.sub(r'</h3>', '</h4>', fulltext_marked)
    fulltext_marked = re.sub(r'<h2([ >])', r'<h3\1', fulltext_marked)
    fulltext_marked = re.sub(r'</h2>', '</h3>', fulltext_marked)
    fulltext_marked = re.sub(r'<h1([ >])', r'<h2\1', fulltext_marked)
    fulltext_marked = re.sub(r'</h1>', '</h2>', fulltext_marked)

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
            '<div class="ft" style="font-size:.88em;color:#555">' + _clean_apparatus(fulltext_marked[:_cut]) + '</div></details>'
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
        # CURRENT MEANS CURRENT (2026-08-08). The pointer names the IMMEDIATE
        # successor, which is right — a chain v1 -> v2 -> v3 is a lineage and each
        # link is true. But the banner said "Current version: #N" about that
        # immediate successor, and on a chain of any length the immediate successor
        # is not current. #1216 announced #832 as current while #832's own page
        # announced it was superseded by #1217. Seventeen records pointed at a
        # superseded record under the word "Current", the longest chain running six
        # deep. Resolve to the TERMINAL for the label; keep the immediate link
        # beside it so the lineage stays visible and nothing is flattened away.
        _by_index = {sib.get('deposit_number'): sib for sib in registry.get('deposits', [])}

        def _sup_target(rec):
            _bs = (rec or {}).get('body_status') or {}
            return _bs.get('superseded_by') or (rec or {}).get('superseded_by_deposit_number')

        _terminal = superseded_by_n
        _hops = 0
        _seen = {dn, superseded_by_n}
        while True:
            _nxt = _sup_target(_by_index.get(_terminal))
            if not _nxt or _nxt in _seen or _nxt not in _by_index:
                break
            _seen.add(_nxt)
            _terminal = _nxt
            _hops += 1
            if _hops > 12:      # a cycle guard: a lineage this long is a defect itself
                break
        _chain_note = ''
        if _terminal != superseded_by_n:
            _imm = _by_index.get(superseded_by_n) or {}
            _chain_note = (
                f'<div style="color:#78350f;font-size:.86em;margin-top:6px">'
                f'Immediate successor: <a href="/s/records/{superseded_by_n}/" '
                f'style="color:var(--accent)">#{superseded_by_n} {esc(_imm.get("version",""))}</a>'
                f' &middot; {_hops + 1} step(s) to current.</div>')
        superseded_by_n = _terminal
        by_v = (_by_index.get(_terminal) or {}).get('version', '')
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
            + _chain_note
            + (f'<div style="color:#78350f;font-size:.88em;margin-top:6px">{esc(superseded_reason)}</div>' if superseded_reason else '')
            + '</div>'
        )
    elif derive_state is not None and derive_state(d)['state'] in (
            'LACUNA', 'WITHDRAWN_EXTERNAL', 'COMPLETE_PACKET',
            'CAPTURE_PAIRED', 'CAPTURE_EXTERNAL', 'CAPTURE_UNPAIRED'):
        # STATE CONFORMANCE (MANUS 2026-08-04): the banner no longer computes
        # state from scattered fields. scripts/record_state.py derives ONE
        # canonical state and every emitter renders it. See that module's
        # docstring for why (three data-vs-page divergences in one session,
        # each caught by a human reading a page).
        _st = derive_state(d)
        _colour = {'LACUNA': ('#fef3c7', '#d97706', '#92400e', '#78350f'),
                   'WITHDRAWN_EXTERNAL': ('#fee2e2', '#b91c1c', '#7f1d1d', '#991b1b'),
                   'COMPLETE_PACKET': ('#dcfce7', '#16a34a', '#14532d', '#166534')}.get(
                       _st['state'], ('#e0f2fe', '#0369a1', '#0c4a6e', '#075985'))
        _bg, _bar, _head_c, _body_c = _colour
        _ptr = _st.get('pointer')
        _link = ''
        if isinstance(_ptr, int):
            _link = (f'<div style="color:{_body_c}">Complete version: '
                     f'<a href="/s/records/{_ptr}/" style="color:var(--accent);font-weight:500">#{_ptr}</a></div>')
        elif isinstance(_ptr, str) and _ptr.startswith('http'):
            _link = (f'<div style="color:{_body_c}">Live manifestation: '
                     f'<a href="{esc(_ptr)}" style="color:var(--accent);font-weight:500">{esc(_ptr)}</a></div>')
        version_banner = (
            f'<div style="background:{_bg};border-left:4px solid {_bar};padding:12px 16px;'
            f'border-radius:6px;margin:12px 0;font-size:.92em">'
            f'<div style="font-weight:600;color:{_head_c};margin-bottom:4px">{esc(_st["label"])}</div>'
            + _link
            + f'<div style="color:{_body_c};font-size:.88em;margin-top:6px">{esc(_st["detail"])[:600]}</div>'
            + ('' if _st['citable'] else
               f'<div style="color:{_body_c};font-size:.85em;margin-top:6px;font-style:italic">'
               'Do not cite this page as the full text of the work.</div>')
            + '</div>'
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
        wiki_html = (
            f'<h2>Wiki Article</h2>\n'
            f'<div style="background:#f8f9fa;border:1px solid var(--border);border-radius:6px;'
            f'padding:16px;margin:8px 0;font-size:.88em;line-height:1.75;color:#333">{wiki_text}'
            f'<div style="margin-top:12px;padding-top:9px;border-top:1px solid var(--border);'
            f'font-size:.88em;color:#666">Also published as a standalone entry: '
            f'<a href="/s/wiki/{d["deposit_number"]}/" style="color:var(--accent)">'
            f'/s/wiki/{d["deposit_number"]}/</a></div></div>')
    
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
    # RELATED-INSTANCE / EXTERNAL-MANIFESTATION rendering (2026-08-04): pointers
    # that live only in data are invisible pointers — the #941 lesson. A record
    # whose work exists elsewhere must SAY SO on the page.
    _bs = d.get('body_status') or {}
    rel_block = ''
    _ri = _bs.get('related_instances') if isinstance(_bs, dict) else None
    if _ri and _ri.get('instances'):
        _items = ''.join(
            f'<li style="margin:3px 0"><a href="/s/records/{i["deposit_number"]}/" style="color:var(--accent)">'
            f'#{i["deposit_number"]}</a> — {esc(str(i.get("title",""))[:80])} '
            f'<span style="color:#888;font-size:.9em">({esc(str(i.get("match","")))} match {esc(str(i.get("score","")))}, '
            f'{i.get("body_chars",0):,} chars)</span></li>'
            for i in _ri['instances'])
        rel_block += (
            '<div style="background:var(--surface);border-left:4px solid var(--teal);padding:10px 14px;'
            'border-radius:6px;margin:12px 0;font-size:.9em">'
            '<div style="font-weight:600;margin-bottom:4px">Other instances of this work in the archive</div>'
            f'<ul style="margin:6px 0 6px 20px;padding:0">{_items}</ul>'
            '<div style="color:#666;font-size:.88em">Recorded as relations only — which instance supersedes which is not asserted here.</div></div>')
    _tri = _bs.get('triptych') if isinstance(_bs, dict) else None
    if _tri and _tri.get('components'):
        _items = ''.join(
            (f'<li style="margin:3px 0"><a href="/s/records/{c["deposit_number"]}/" style="color:var(--accent)">'
             f'#{c["deposit_number"]}</a> — {esc(str(c.get("role","")))}'
             + (f' <span style="color:#888">{esc(str(c.get("title",""))[:60])}</span>' if c.get('title') else '')
             + '</li>')
            for c in _tri['components'])
        rel_block += (
            '<div style="background:var(--surface);border-left:4px solid var(--teal);padding:10px 14px;'
            'border-radius:6px;margin:12px 0;font-size:.9em">'
            f'<div style="font-weight:600;margin-bottom:4px">{esc(str(_tri.get("relation","Related components")))}</div>'
            f'<ul style="margin:6px 0 6px 20px;padding:0">{_items}</ul>'
            + (f'<div style="color:#666;font-size:.88em">{esc(str(_tri.get("partial_witness","")))}</div>'
               if _tri.get('partial_witness') else '')
            + '</div>')

    for _k, _hd in (('analysed_by', 'Analysed in'), ('analysis_of', 'This record analyses')):
        _rel = _bs.get(_k) if isinstance(_bs, dict) else None
        if _rel and _rel.get('deposit_number'):
            rel_block += (
                '<div style="background:var(--surface);border-left:4px solid var(--teal);padding:10px 14px;'
                'border-radius:6px;margin:12px 0;font-size:.9em">'
                f'<div style="font-weight:600;margin-bottom:4px">{_hd}</div>'
                f'<a href="/s/records/{_rel["deposit_number"]}/" style="color:var(--accent)">'
                f'#{_rel["deposit_number"]} — {esc(str(_rel.get("title",""))[:80])}</a>'
                f'<div style="color:#666;font-size:.88em;margin-top:4px">{esc(str(_rel.get("relation","")))}</div></div>')

    # WIKI LINK (MANUS 2026-08-06): the wiki page links to its record, but the
    # record never linked back — a one-directional relation on a surface MANUS
    # identifies as "a primary compression surface for the work" and which AI
    # Overview is already citing. A reader on a record could not reach its
    # article.
    # The wiki callout used to sit HERE, above the record, duplicating the full
    # article rendered further down — a reader met a box advertising an article
    # they were about to be given in its entirety. The article stays inline; the
    # link becomes a quiet pointer beside it, so the wiki page remains reachable
    # (it is separately harvested and cited) without announcing itself twice.
    pass

    # HELD ARTIFACTS (2026-08-08). The registry's `attachments` array was carried in
    # the data and rendered nowhere, so a record could hold a file and give a reader
    # no way to fetch it. Surfaced here with size, page count and SHA-256, because a
    # download whose hash is not shown cannot be checked against the record that
    # serves it — and an archive that asks to be mirrored has to make that cheap.
    _atts = d.get('attachments') or []
    _served = [a for a in _atts if isinstance(a, dict)
               and str(a.get('url', '')).startswith('https://www.alexanarch.org/')]
    if _served:
        _rows = []
        for a in _served:
            _meta = []
            if a.get('size'):
                _meta.append(f"{a['size']:,} bytes")
            if a.get('pages'):
                _meta.append(f"{a['pages']} pages")
            if a.get('sha256'):
                _meta.append(f"sha256 {esc(str(a['sha256'])[:16])}\u2026")
            _rows.append(
                '<div style="padding:7px 0;border-top:1px solid var(--border)">'
                f'<a href="{esc(a["url"])}" style="color:var(--accent);font-weight:500">'
                f'{esc(a.get("filename", "file"))}</a> '
                f'<span style="color:#888;font-size:.88em">({" \u00b7 ".join(_meta)})</span>'
                + (f'<div style="color:#666;font-size:.88em;margin-top:2px">'
                   f'{esc(str(a.get("role", "")))}</div>' if a.get('role') else '')
                + '</div>')
        rel_block += (
            '<div style="background:var(--surface);border-left:4px solid var(--accent);'
            'padding:10px 14px;border-radius:6px;margin:12px 0;font-size:.9em">'
            '<div style="font-weight:600;margin-bottom:2px">Held artifacts &mdash; '
            f'{len(_served)} file{"s" if len(_served) != 1 else ""}, served by this archive</div>'
            '<div style="color:#666;font-size:.88em;margin-bottom:2px">Fetch, hash, compare. '
            'Copying requires no permission and verification requires no trust in this archive.</div>'
            + ''.join(_rows) + '</div>')

    _pt = _bs.get('primary_text_attachment') if isinstance(_bs, dict) else None
    if _pt and _pt.get('attachment'):
        rel_block += (
            '<div style="background:var(--surface);border-left:4px solid var(--teal);padding:10px 14px;'
            'border-radius:6px;margin:12px 0;font-size:.9em">'
            '<div style="font-weight:600;margin-bottom:4px">Primary text — downloadable</div>'
            f'<a href="{esc(_pt["attachment"])}" style="color:var(--accent)">'
            f'{esc(_pt["attachment"].split("/")[-1])}</a> '
            f'<span style="color:#888;font-size:.9em">({_pt.get("bytes",0):,} bytes · '
            f'sha256 {esc(str(_pt.get("sha256",""))[:16])}…)</span>'
            f'<div style="color:#666;font-size:.88em;margin-top:4px">{esc(str(_pt.get("role","")))}. '
            f'{esc(str(_pt.get("note","")))}</div>'
            + (f'<div style="color:#666;font-size:.88em;margin-top:4px">Analysis: '
               f'<a href="/s/records/{_pt["analysis_deposit"]}/" style="color:var(--accent)">#{_pt["analysis_deposit"]}</a> · '
               f'Primary: <a href="/s/records/{_pt["primary_deposit"]}/" style="color:var(--accent)">#{_pt["primary_deposit"]}</a></div>'
               if _pt.get('analysis_deposit') else '')
            + '</div>')

    _ni = _bs.get('named_in') if isinstance(_bs, dict) else None
    if _ni and _ni.get('records'):
        _top = _ni['records'][:6]
        _li = ''.join(
            f'<li style="margin:3px 0"><a href="/s/records/{i["deposit_number"]}/" style="color:var(--accent)">'
            f'#{i["deposit_number"]}</a> — {esc(str(i.get("title",""))[:78])}</li>' for i in _top)
        _more = len(_ni['records']) - len(_top)
        rel_block += (
            '<div style="background:var(--surface);border-left:4px solid #d97706;padding:10px 14px;'
            'border-radius:6px;margin:12px 0;font-size:.9em">'
            '<div style="font-weight:600;margin-bottom:4px">Where this work is named in the archive</div>'
            f'<ul style="margin:6px 0 6px 20px;padding:0">{_li}</ul>'
            + (f'<div style="color:#888;font-size:.88em">…and {_more} more.</div>' if _more > 0 else '')
            + '<div style="color:#666;font-size:.88em;margin-top:4px">These records register or cite the work; '
              'none contains its text. The full text is not yet in the archive.</div></div>')

    _em = _bs.get('external_manifestation') if isinstance(_bs, dict) else None
    if _em and _em.get('url'):
        rel_block += (
            '<div style="background:var(--surface);border-left:4px solid var(--teal);padding:10px 14px;'
            'border-radius:6px;margin:12px 0;font-size:.9em">'
            '<div style="font-weight:600;margin-bottom:4px">Live manifestation</div>'
            f'<a href="{esc(_em["url"])}" style="color:var(--accent)">{esc(_em["url"])}</a>'
            f'<div style="color:#666;font-size:.88em;margin-top:4px">{esc(str(_em.get("role") or _em.get("basis") or ""))[:200]}</div></div>')

    page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(d["title"])} — Alexanarch</title><meta name="description" content="{esc(_compose_meta_description(d))}"><meta property="og:title" content="{esc(str(d["title"])[:95])}"><meta property="og:description" content="{esc(_compose_meta_description(d))}"><meta property="og:url" content="{_rec_url}"><meta property="og:type" content="article"><meta property="og:site_name" content="Alexanarch"><meta name="twitter:card" content="summary"><script type="application/ld+json">{jsonld}</script>{_katex_head}
<link rel="resourcesync" href="https://www.alexanarch.org/.well-known/resourcesync">
<link rel="alternate" type="application/xml" title="OAI-PMH 2.0" href="https://www.alexanarch.org/oai?verb=Identify">
<link rel="alternate" type="application/json" title="Record JSON" href="https://www.alexanarch.org/data/records/{d["deposit_number"]}.json">
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
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.8;font-size:15px}}.wrap{{max-width:720px;margin:0 auto;padding:60px 24px}}a{{color:var(--accent);text-decoration:none}}a:hover{{color:var(--accent2)}}h1{{font-size:1.3em;font-weight:600;color:var(--accent);margin-bottom:8px}}h2{{font-size:1em;font-weight:500;color:var(--accent);margin-top:20px;margin-bottom:6px;border-bottom:1px solid var(--border);padding-bottom:3px}}p{{margin-bottom:10px;color:#333}}.nav{{display:flex;gap:12px;margin-bottom:24px;font-size:.85em;overflow-x:auto;white-space:nowrap}}.nav a{{color:#777;font-weight:500;text-decoration:none}}.nav a:hover{{color:var(--accent)}}.ft{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:20px;max-height:600px;overflow-y:auto;font-size:.88em;line-height:1.75;margin:8px 0;color:#333}}.ft h1,.ft h2,.ft h3{{color:var(--accent);margin:12px 0 6px}}.ft h1{{font-size:1.1em}}.ft h2{{font-size:1em;border-bottom:none}}.ft h3{{font-size:.95em}}.ft strong{{color:var(--fg)}}.ft blockquote{{border-left:3px solid var(--teal);padding-left:12px;color:#555;margin:8px 0}}.ft hr{{border:none;border-top:1px solid var(--border);margin:12px 0}}.footer{{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}}</style>
</head><body><div class="wrap">
{render_navbar()}
<div role="text" aria-label="{esc(_axn_aria(d["axn"]))}" style="font-family:var(--mono);font-size:1.1em;color:var(--teal);background:var(--surface);padding:12px;border-radius:6px;border-left:4px solid var(--teal);margin:12px 0">{esc(d["axn"])}</div>
{version_banner}
{rel_block}
<h1>{esc(d["title"])}</h1>
<div style="font-size:.85em;color:#777;margin-bottom:10px">{esc(d["creator"])} · {esc(d["date"])} · {esc(d.get("content_type",""))}{f' · <span style="color:var(--accent);font-weight:500">{esc(version)}</span>' if (version and (version != 'v1.0' or series_id)) else ''}</div>
<a style="display:inline-block;background:var(--teal);color:#fff;padding:6px 14px;border-radius:4px;font-size:.82em;text-decoration:none;margin:6px 0" href="/data/deposits/AXN-{hex_id}.md" download>↓ Download MD</a> <a style="display:inline-block;background:var(--accent);color:#fff;padding:6px 14px;border-radius:4px;font-size:.82em;text-decoration:none;margin:6px 0 6px 4px" href="/papers/AXN-{hex_id.zfill(4)}.pdf">↓ PDF</a>
<div style="margin:8px 0">{kw_html}</div>
<h2>Description</h2>
<p style="font-size:.9em">{_render_inline(d.get("description",""))}</p>
{files_html}
{wiki_html}
{concepts_html}
{triples_html}
<h2>Full Text</h2>
{apparatus_html}
<div class="ft">{_kernel_html}{fulltext_marked}</div>
{lifted_apparatus_html}
<!-- APPARATUS BLOC — everything below records how this record was processed,
     not what the work says. It follows the work because a reader came for the
     work. (MANUS standing rule, 2026-08-06: recording of method or modification
     does not appear in body text.) -->
{external_metadata_html}
{version_history}
{mods_html}
{traversal_html}
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
