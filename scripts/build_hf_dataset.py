#!/usr/bin/env python3
"""build_hf_dataset.py — project the archive into a Hugging Face dataset.

One source of truth (data/), several parquet configs, one dataset card.
Configs:
  deposits   one row per deposit: registry fields + canonical text + sha256
  captures   the reception captures (data/captures.json)
  citations  the internal citation graph edges
  lexicon    the lexical-minting registry
  reception  the referee-report register of #1574 (the reception measurement)
  sources    recovered book-length and docx-only sources (data/attachments/atlwm, recovered-sources)
  sites      one row per page of the public fleet repos (markdown/html text), when FLEET_DIR is given

Usage: python3 scripts/build_hf_dataset.py [--out hf-dataset] [--fleet /path/to/clones]
The Hub push is a separate step (see scripts/push_hf_dataset.py / the workflow).
"""
import json, re, sys, os, hashlib, argparse, pathlib, html
import pandas as pd
ROOT = pathlib.Path(__file__).resolve().parent.parent


# SPORE COUNTS ARE READ AT BUILD TIME, NOT WRITTEN INTO THIS FILE (2026-09-12).
# The parent card carried "222 nodes, 140 typed edges" for a body that had grown to 563 and
# 367, and named two of the three bodies when three existed. A hand-maintained count in a
# generator goes stale the first time the thing it counts is rebuilt, which is the whole
# reason the rhizomes emit a spore.json in the first place.
def _spore_line(slug):
    import json as _j, pathlib as _p
    f = _p.Path(__file__).resolve().parent.parent / "rhizomes" / slug / "spore.json"
    if not f.exists():
        return slug
    s = _j.loads(f.read_text(encoding="utf-8"))
    c = s.get("counts") or {}
    n, e, st = c.get("nodes"), c.get("relations") or c.get("edges"), c.get("stolons")
    return f'{s.get("rhizome_id", slug)}. {n} nodes, {e} typed edges, {st} stolons'


_SPORE = {s: _spore_line(s) for s in
          ("model-collapse-anti-collapse", "semantic-economy", "machine-mediated-reception",
           "revelation-first", "spxi-mpai", "provenance-erasure", "heteronyms", "poetics")}

def sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()

def strip_html(h):
    h = re.sub(r'(?is)<(script|style|nav|footer|svg)[^>]*>.*?</\1>', ' ', h)
    h = re.sub(r'(?s)<[^>]+>', ' ', h)
    h = html.unescape(h)
    return re.sub(r'[ \t]+', ' ', re.sub(r'\n\s*\n+', '\n\n', h)).strip()

_lncount = {}

def _lines(reg):
    """PARTIALITY (2026-09-07). Every record belongs to countable lines the archive
    already maintains: its journal, its keyword neighbourhoods, its version series.
    A composer that receives a record with no indication of what surrounds it treats
    the record as the whole surface — measured on 2026-09-07 as citations per turn
    4 / 0 / 0, the composer reasoning from its own first answer thereafter. The
    remedy is not more metadata but a countable, addressed statement of partiality
    IN THE TEXT, because it is the passage's own vocabulary that becomes the next
    query (Jang et al., GuideCQR) and the supplied text that a sufficiency rater
    reads (Joren et al., ICLR 2025). Derived here at build time; nothing authored,
    nothing written back to the registry."""
    import collections
    act = [d for d in reg if (d.get('status') or 'ACTIVE') == 'ACTIVE']
    global _lncount
    import collections as _c
    _lncount = _c.Counter(d.get('line') for d in act if d.get('line'))
    jrn = collections.Counter(d.get('journal') for d in act if d.get('journal'))
    kw = collections.Counter()
    for d in act:
        for w in (d.get('keywords') or []):
            if w and w.strip(): kw[w.strip().lower()] += 1
    ser = collections.Counter(d.get('version_series_id') for d in act if d.get('version_series_id'))
    return act, jrn, kw, ser

def _partiality(d, jrn, kw, ser, n_active):
    """Returns (columns, sentence). The sentence is prepended to the served text."""
    out = {'line_journal': None, 'line_journal_count': None,
           'line_keyword': None, 'line_keyword_count': None,
           'line_series': None, 'line_series_count': None,
           'archive_active_count': n_active, 'partiality': None}
    parts = []
    j = d.get('journal')
    if j and jrn.get(j, 0) >= 2:
        out['line_journal'], out['line_journal_count'] = j, jrn[j]
        parts.append(f"one of {jrn[j]} records in {j}")
    kws = [w.strip() for w in (d.get('keywords') or []) if w and w.strip()]
    shared = sorted(((kw.get(w.lower(), 0), w) for w in kws), reverse=True)
    shared = [(c, w) for c, w in shared if c >= 2][:2]
    if shared:
        out['line_keyword'] = ' | '.join(w for _, w in shared)
        out['line_keyword_count'] = shared[0][0]
        for c, w in shared:
            parts.append(f"one of {c} that carry the keyword \u201c{w}\u201d")
    sid = d.get('version_series_id')
    if sid and ser.get(sid, 0) >= 2:
        out['line_series'], out['line_series_count'] = sid, ser[sid]
        parts.append(f"one of {ser[sid]} versions in series {sid}")
    n = d.get('deposit_number')
    # MEASURE EDGES (2026-09-08). A claim's instruments live in other records, and the
    # composition layer traverses what is linked. Two unprimed readers in one week judged
    # Semantic Economy to lack measures while PER (398 deposits), erasure skew (55) and the
    # CDI specification (#117) sat in the same corpus unreachable from it: keyword
    # enrichment guaranteed degree, not a typed edge from a claim to its instrument.
    # The edge is bidirectional and gated (scripts/check_measures.py); this puts it IN THE TEXT,
    # since it is the passage's own vocabulary that becomes the next query.
    # LINES (2026-09-08). A body of thought that develops across months is invisible to a
    # composer if its records carry no edge to one another: measured today, 1,234 of 1,406
    # ACTIVE deposits had zero deposit-to-deposit edge, including a model-collapse line of
    # 45 records spanning January to September of which only the last four were linked.
    # `line` names the body, develops_from/developed_by order it, and the gate keeps the
    # order honest (a step cannot develop from something later). Surfaced in the text, since
    # it is the passage's own vocabulary that becomes the next query.
    ln = d.get('line')
    if ln:
        out['line_of_thought'] = ln
        out['line_parent'] = d.get('line_parent') or ''
        df = d.get('develops_from') or []
        db = d.get('developed_by') or []
        out['develops_from'] = ' | '.join(f"#{e['deposit']}" for e in df)
        out['developed_by'] = ' | '.join(f"#{e['deposit']}" for e in db)
        nline = _lncount.get(ln, 0)
        basis = d.get('line_basis') or 'stated'
        out['line_count'] = nline
        out['line_basis'] = basis
        seg = [(f"one of {nline} records in the line \u201c{ln}\u201d" if nline else f"in the line \u201c{ln}\u201d")
               + ("" if basis == 'stated' else " (membership derived from this record's own title and keywords, not authored)")]
        if df: seg.append("developing from " + ", ".join(f"record #{e['deposit']}" for e in df))
        if db: seg.append("developed further by " + ", ".join(f"record #{e['deposit']} ({e.get('what','')})" for e in db))
        parts.append("; ".join(seg))
    mb = d.get('measured_by') or []
    ms = d.get('measures') or []
    if mb:
        out['measured_by'] = ' | '.join(f"#{e['deposit']}: {e.get('measure','')}" for e in mb)
        out['measured_by_count'] = len(mb)
        parts.append("measured by " + ", ".join(
            f"{e.get('measure','')} (record #{e['deposit']}, which reports: {e.get('reports','')})" for e in mb))
    if ms:
        out['measures'] = ' | '.join(f"#{e['deposit']}: {e.get('measure','')}" for e in ms)
        out['measures_count'] = len(ms)
        parts.append("an instrument: it measures " + ", ".join(f"record #{e['deposit']}" for e in ms))
    if parts:
        out['partiality'] = (
            "PARTIAL BY CONSTRUCTION \u2014 this record is " + "; ".join(parts) +
            f"; and one of {n_active} active records in the Crimson Hexagonal Archive. "
            "It is not a complete account of anything it discusses. "
            f"Its neighbours: https://alexanarch.org/s/browse/ (the full register), "
            f"https://alexanarch.org/s/records/{n}/ (this record, with its relations), "
            "https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive (the corpus as data). "
            "Any account built from this record alone is built from one of them."
        )
    return out

# NOTE (2026-09-08): the registry's field is `substrate`, not `substrate_disclosure`. The builder
# read the latter and so emitted an empty column for the archive's most principled datum until an
# external audit of the Hub noticed it null. Read both, `substrate` first.
def deposits():
    reg = json.load(open(ROOT/'data/registry.json'))['deposits']
    _act, _jrn, _kw, _ser = _lines(reg)
    _n_active = len(_act)
    rows = []
    for d in reg:
        p = d.get('full_text_path'); text = ''
        if p:
            fp = ROOT/p.lstrip('/')
            if fp.exists(): text = fp.read_text(encoding='utf-8', errors='replace')
        rows.append({
            'deposit_number': d['deposit_number'], 'axn': d.get('axn'), 'hex': d.get('hex'),
            'title': d.get('title'), 'creator': d.get('creator'), 'date': d.get('date'),
            'family': d.get('family'), 'content_type': d.get('content_type'),
            'description': d.get('description'), 'keywords': ', '.join(d.get('keywords') or []) if isinstance(d.get('keywords'), list) else d.get('keywords'),
            'license': d.get('license'), 'substrate_disclosure': d.get('substrate') or d.get('substrate_disclosure'),
            'falsification_conditions': d.get('falsification_conditions'), 'methodology': d.get('methodology'),
            'status': d.get('status'), 'superseded_by': d.get('superseded_by'),
            'version_series_id': d.get('version_series_id'),
            'wiki_article': d.get('wiki_article'),
            'related_deposits': json.dumps(d.get('related_deposits') or []),
            'defines_concepts': json.dumps(d.get('defines_concepts') or [], ensure_ascii=False),
            'record_url': f"https://alexanarch.org/s/records/{d['deposit_number']}/",
            'text': text, 'text_sha256': sha(text) if text else None, 'text_words': len(text.split()) if text else 0,
        })
        _p = _partiality(d, _jrn, _kw, _ser, _n_active)
        # THE SEATS (Lee Sharks, 2026-10-16: "tagging rows / deposits to their respective location within cha
        # topology"). The record's place in the Crimson Hexagon travels with the passage, for the reason the
        # partiality statement exists: only what is in the text carries into the next query.
        _st = _seats_of(d)
        rows[-1].update(_st['columns'])
        if _st['sentence'] and _p.get('partiality'):
            _p['partiality'] = _p['partiality'].rstrip() + ' ' + _st['sentence']
        elif _st['sentence']:
            _p['partiality'] = _st['sentence']
        rows[-1].update(_p)
        # F1 (audit 2026-09-10) — CANONICAL BYTES AND PRESENTATION AS SEPARATE COLUMNS.
        # `text` carries the contextualised representation; `text_sha256` has always been the
        # hash of the CANONICAL bytes, which is a disclosed design but meant a consumer
        # hashing exported `text` could not verify the advertised digest. `canonical_text` is
        # now emitted as its own column — exactly the bytes the digest covers, UTF-8, no
        # prefix — with `text_prefix_chars` giving the offset so the two are reversible.
        rows[-1]['canonical_text'] = text or None
        rows[-1]['canonical_encoding'] = 'utf-8' if text else None
        rows[-1]['text_prefix_chars'] = 0
        rows[-1]['text_words_counts'] = 'canonical_text'
        if _p['partiality'] and text:
            prefix = _p['partiality'] + "\n\n---\n\n"
            rows[-1]['text'] = prefix + text
            rows[-1]['text_prefix_chars'] = len(prefix)
    df = pd.DataFrame(rows)
    # ── relations as data, keyed by deposit number and AXN (2026-09-03) ──
    cg = json.load(open(ROOT/'data/citation-graph.json')) if (ROOT/'data/citation-graph.json').exists() else {}
    edges = cg.get('edges') or cg.get('citations') or []
    cites, cited_by = {}, {}
    for e in edges:
        a = e.get('source_deposit') or e.get('from') or e.get('source'); b = e.get('target_deposit') or e.get('to') or e.get('target')
        try: a = int(a); b = int(b)
        except Exception: continue
        cites.setdefault(a, set()).add(b); cited_by.setdefault(b, set()).add(a)
    num2axn = {d['deposit_number']: d.get('axn') for d in reg}
    df['cites'] = df['deposit_number'].map(lambda n: json.dumps(sorted(cites.get(n, ()))))
    df['cited_by'] = df['deposit_number'].map(lambda n: json.dumps(sorted(cited_by.get(n, ()))))
    df['cites_axn'] = df['deposit_number'].map(lambda n: json.dumps([num2axn.get(x) for x in sorted(cites.get(n, ()))]))
    # series neighbours: by version_series_id in deposit order; supersession as explicit prev/next
    series = {}
    for d in reg:
        if d.get('version_series_id'): series.setdefault(d['version_series_id'], []).append(d['deposit_number'])
    prev, nxt = {}, {}
    for sid, members in series.items():
        members.sort()
        for i, n in enumerate(members):
            if i: prev[n] = members[i-1]
            if i < len(members)-1: nxt[n] = members[i+1]
    supersedes = {}
    for d in reg:
        sb = d.get('superseded_by')
        if sb:
            try: supersedes.setdefault(int(sb), []).append(d['deposit_number'])
            except Exception: pass
    df['series_previous'] = df['deposit_number'].map(lambda n: prev.get(n))
    df['series_next'] = df['deposit_number'].map(lambda n: nxt.get(n))
    df['supersedes'] = df['deposit_number'].map(lambda n: json.dumps(sorted(supersedes.get(n, ()))))
    # Named historical entities the deposit deals with, from data/named-entities.json.
    # Both directions are carried: the ids here, and the deposit numbers in the
    # `entities` config, so a reader can traverse either way (2026-09-09).
    _ent = [_entities_for(d) for d in reg]
    df['entities'] = [json.dumps(e) for e in _ent]
    df['entity_count'] = [len(e) for e in _ent]
    df['axn_uri'] = df['hex'].map(lambda h: f"https://alexanarch.org/s/axn/{h}/" if h else None)
    df['text_uri'] = df['deposit_number'].map(lambda n: next((f"https://alexanarch.org{d.get('full_text_path')}" for d in reg if d['deposit_number']==n and d.get('full_text_path')), None))
    df['doi_legacy'] = [ (d.get('doi') or d.get('zenodo_doi') or d.get('legacy_doi')) for d in reg ]
    df['attachments'] = [ json.dumps([ (a.get('url') or a.get('filename')) for a in (d.get('attachments') or []) ]) for d in reg ]
    ja = _jsonl('datasets/journals/assignments.jsonl')
    if not ja.empty and 'deposit' in ja.columns:
        df = df.merge(ja[['deposit','journal']].rename(columns={'deposit':'deposit_number','journal':'venue'}), on='deposit_number', how='left')
    return df

# ── THE TOPOLOGY OF THE CRIMSON HEXAGON (2026-10-16) ─────────────────────────────────────────────────────────
# Source: data/hexagon-seats.json (scripts/build_hexagon_seats.py), the same file the record pages and /s/rooms/ read:
# the interface's room assignment, the 2026-10-16 room reading (16 readers, each seat with a relation, a confidence and
# a verbatim basis checked at its lines), and the operator's rulings of that day applied over it. A record's rooms are
# listed primary first (the reading's primary flag). Low-confidence seats (fit by family resemblance only) are carried as PROPOSED, marked for later
# adjudication, as /s/rooms/ shows them; they are never a record's primary seat.
_SEATMAP = None
def _seatmap():
    global _SEATMAP
    if _SEATMAP is None:
        p = ROOT/'data/hexagon-seats.json'
        _SEATMAP = json.load(open(p)) if p.exists() else {'rooms': {}, 'seats': {}}
    return _SEATMAP

PROPOSED_NOTE = 'proposed — low confidence, for later adjudication'

def _seat_rows(n):
    sm = _seatmap(); R = sm['rooms']; e = sm['seats'].get(str(n))
    if not e: return [], []
    seated, proposed = [], []
    # The primary seat is the one the reading (or a ruling) flags primary — as the record pages and /s/rooms/ take it
    # (build_cross_indexes.py) — listed first; a record whose seats carry no primary flag has no primary seat here.
    # `relation` is the reading's vocabulary only; the interface's room-page role ('in the room', 'constituting') is `role`.
    rooms = sorted(e.get('rooms') or [], key=lambda loc: not ((e.get('read') or {}).get(loc) or {}).get('primary'))
    for loc in rooms:
        r = R.get(loc, {}); rd = (e.get('read') or {}).get(loc) or {}
        b = rd.get('basis') or {}
        seated.append({'locus_id': loc, 'locus': r.get('locus', loc), 'name': r.get('name'), 'primary': bool(rd.get('primary')),
                       'relation': rd.get('relation'), 'role': (e.get('roles') or {}).get(loc),
                       'confidence': rd.get('confidence') or 'assigned',
                       'basis_quote': b.get('quote'), 'basis_lines': b.get('lines'),
                       'source': '; '.join((e.get('sources') or {}).get(loc) or [e.get('assignment') or '']),
                       'url': r.get('url'), 'status': 'seat'})
    for x in e.get('proposed') or []:
        r = R.get(x['locus'], {}); b = x.get('basis') or {}
        proposed.append({'locus_id': x['locus'], 'locus': r.get('locus', x['locus']), 'name': r.get('name'),
                         'primary': False, 'relation': x.get('relation'), 'role': None, 'confidence': 'low',
                         'basis_quote': b.get('quote'), 'basis_lines': b.get('lines'), 'source': 'read 2026-10-16',
                         'url': r.get('url'), 'status': PROPOSED_NOTE})
    return seated, proposed

def _seats_of(d):
    seated, proposed = _seat_rows(d['deposit_number'])
    cols = {'seats': json.dumps(seated, ensure_ascii=False), 'seat_count': len(seated),
            'primary_locus': next((x['locus'] for x in seated if x['primary']), None),
            'primary_room': next((x['name'] for x in seated if x['primary']), None),
            'seat_loci': json.dumps([s['locus'] for s in seated], ensure_ascii=False),
            'proposed_seats': json.dumps(proposed, ensure_ascii=False), 'proposed_seat_count': len(proposed),
            'line': d.get('line'), 'line_parent': d.get('line_parent')}
    sent = None
    if seated:
        def one(s):
            bits = (['primary'] if s['primary'] else []) + ([s['relation']] if s['relation'] else [])
            return f"{s['locus']} {s['name']}" + (f" ({'; '.join(bits)})" if bits else '')
        sent = 'In the Crimson Hexagon it is seated at ' + one(seated[0]) + (
            ', and also at ' + ', '.join(one(s) for s in seated[1:]) if len(seated) > 1 else '') + \
            ' — each room a page of crimsonhexagonal.org that seats its records; the `loci` and `seats` configs of this dataset carry the rest.'
    elif d.get('status') == 'ACTIVE':
        sent = 'It is not yet seated in a room of the Crimson Hexagon.'
    return {'columns': cols, 'sentence': sent}

def loci():
    """One row per locus of the Crimson Hexagon — room, field, Ark, shadow, structure — with its members both ways."""
    sm = _seatmap(); rows = []
    mem = {}
    for n, e in sm['seats'].items():
        seated, proposed = _seat_rows(int(n))
        for s in seated + proposed:
            mem.setdefault(s['locus_id'], []).append((int(n), s))
    for loc, r in sm['rooms'].items():
        M = mem.get(loc, [])
        seat_n = sorted({n for n, s in M if s['status'] == 'seat'})
        prim_n = sorted({n for n, s in M if s['primary']})
        prop_n = sorted({n for n, s in M if s['status'] != 'seat'})
        rows.append({'locus_id': loc, 'locus': r.get('locus'), 'name': r.get('name'), 'category': r.get('cat'),
                     'hex_address': r.get('hex_address'), 'url': r.get('url'), 'physics': r.get('physics'),
                     'description': r.get('desc'), 'prompt': r.get('prompt'),
                     'deposits': json.dumps(seat_n), 'deposit_count': len(seat_n),
                     'primary_deposits': json.dumps(prim_n), 'primary_count': len(prim_n),
                     'proposed_deposits': json.dumps(prop_n), 'proposed_count': len(prop_n),
                     'deposit_uris': json.dumps([f"https://alexanarch.org/s/records/{n}/" for n in seat_n])})
    return pd.DataFrame(rows)

def seats():
    """The edge list of the topology: one row per record–locus seat (and per proposed seat, marked)."""
    reg = {d['deposit_number']: d for d in json.load(open(ROOT/'data/registry.json'))['deposits']}
    rows = []
    for n in sorted(int(k) for k in _seatmap()['seats']):
        seated, proposed = _seat_rows(n); d = reg.get(n, {})
        for s in seated + proposed:
            rows.append({'deposit_number': n, 'axn': d.get('axn'), 'title': d.get('title'), 'deposit_status': d.get('status'),
                         **{k: (json.dumps(v) if k == 'basis_lines' and v is not None else v) for k, v in s.items()},
                         'record_url': f"https://alexanarch.org/s/records/{n}/"})
    return pd.DataFrame(rows)

_ENTS = None

def _entities_registry():
    """data/named-entities.json — the curated register of named historical PERSONS the
    archive's works deal with. Distinct from data/entity-index.json, which registers
    concepts. Detection is by the explicit pattern each entity carries; nothing is
    inferred and nothing is written back to the registry.

    PATTERNS ARE NARROW ON PURPOSE (2026-09-09). A first pass used bare stems and
    reported Simplicius present in the archive; the match was on "simplicity", and
    "Nicolaus" matched Kierkegaard's pseudonym Nicolaus Notabene rather than Nicolaus
    of Damascus. Both now correctly return zero. A registered entity with no deposits
    is an honest statement that the archive holds no work dealing with it; widening a
    pattern to raise a count would make the register a worse instrument than none."""
    global _ENTS
    if _ENTS is None:
        f = ROOT/'data/named-entities.json'
        _ENTS = json.load(open(f, encoding='utf-8'))['entities'] if f.exists() else []
        for e in _ENTS:
            e['_rx'] = re.compile(e['pattern'], re.I)
    return _ENTS

def _entities_for(d):
    """Which registered persons a deposit deals with. Searches the fields a reader sees:
    title, description, keywords, wiki_article. Returns ids, sorted."""
    blob = ' '.join(str(d.get(k) or '') for k in ('title', 'description', 'wiki_article')) \
           + ' ' + ' '.join(d.get('keywords') or [])
    return sorted(e['id'] for e in _entities_registry() if e['_rx'].search(blob))

def entities():
    """One row per named historical entity, with the deposits that deal with it.

    This config exists so that the relation is traversable in BOTH directions: from a
    deposit, `entities` gives the ids; from here, `deposits` gives the numbers back.
    A reader who arrives at one Sappho deposit can reach the other hundred and
    twenty-one without knowing they exist, which is the same failure the partiality
    statement addresses for lines (2026-09-09).
    """
    reg = [d for d in json.load(open(ROOT/'data/registry.json', encoding='utf-8'))['deposits']
           if (d.get('status') or 'ACTIVE') == 'ACTIVE']
    rows = []
    for e in _entities_registry():
        dep = sorted(d['deposit_number'] for d in reg if e['id'] in _entities_for(d))
        rows.append({
            'entity_id': e['id'], 'name': e['name'], 'kind': e.get('kind'),
            # Authorial identities carry the archive's own identifier and hex coordinate;
            # historical persons carry a floruit and a Wikidata id. Both shapes coexist.
            'identifier': e.get('identifier'), 'hex_coordinate': e.get('hex_coordinate'),
            'canonical_page': e.get('canonical_page'),
            'floruit': e.get('floruit'), 'wikidata': e.get('wikidata'),
            'wikidata_uri': f"https://www.wikidata.org/wiki/{e['wikidata']}" if e.get('wikidata') else None,
            'note': e.get('note'), 'match_pattern': e['pattern'],
            'deposit_count': len(dep),
            'deposits': json.dumps(dep),
            'deposit_uris': json.dumps([f"https://alexanarch.org/s/records/{n}/" for n in dep[:50]]),
        })
    return pd.DataFrame(sorted(rows, key=lambda r: -r['deposit_count']))

def relations():
    """The canonical typed relation ledger — data/relations.jsonl, emitted by
    scripts/build_relations.py from substrates the archive already holds.

    One relation is written once and projects everywhere. The denormalised columns on
    `deposits` (develops_from, measured_by, cited_by, entities) remain useful for
    retrieval and are now PROJECTIONS of this file rather than the authoritative store.

    Every edge carries `basis`: asserted (a person stated it), editorial (a registry
    decision), derived-deterministic (a rule, no judgement), pattern-detected (an
    explicit stated pattern). `related_unspecified` is kept AS unspecified — 306 edges
    whose kind the source field never stated, and inventing a predicate for them would
    manufacture an assertion the archive never made.
    """
    return _jsonl('data/relations.jsonl')

def nodes():
    """The universal object registry: deposits, heteronyms, persons, concepts, lines,
    institutions, journals, series, problems — each with a graph id of the form
    `<type>:<slug>` that every subsystem can attach to."""
    return _jsonl('data/nodes.jsonl')

def pessoagraph():
    """datasets/pessoagraph/graph.json — the heteronymic lineage, IMPORTED AS ITS OWN DATA.

    197 nodes from -2600 to 2026 and 301 edges, canonical at pessoa-knowledge-graph:src/graph.json
    and never edited here. It is NOT merged into `nodes`/`relations`: it has its own namespace, its
    own predicates (master_disciple, lineage, instantiates, heteronym_of, manifests) and its own
    governance. datasets/heteronyms remains a separate body on the same terms."""
    import itertools
    g = json.loads((ROOT/'datasets/pessoagraph/graph.json').read_text(encoding='utf-8'))
    rows = [{'kind':'node','id':n['id'],'label':n.get('label'),'node_type':n.get('t'),
             'era':n.get('e'),'layer':n.get('l'),'year':n.get('y'),
             'source':None,'predicate':None,'target':None,
             'payload':json.dumps({k:v for k,v in n.items() if k not in ('id','label','t','e','l','y')},ensure_ascii=False)}
            for n in g['nodes']]
    rows += [{'kind':'edge','id':None,'label':None,'node_type':None,'era':None,'layer':None,'year':None,
              'source':e.get('source'),'predicate':e.get('type'),'target':e.get('target'),'payload':None}
             for e in g['edges']]
    return pd.DataFrame(rows)

def graph_join():
    """datasets/pessoagraph/join.json — where the two bodies name the same identity, and where they don't.

    Neither is absorbed. A lineage node with no archive identity record is not a defect: the graph holds
    5,000 years of figures the archive holds no record for. THE DODECAD IS PRIMARY — twelve declared
    positions within 26 identity records — and all twelve join."""
    j = json.loads((ROOT/'datasets/pessoagraph/join.json').read_text(encoding='utf-8'))
    return pd.DataFrame(j['rows'])

def frame_defs():
    """datasets/frames/frames.json — the arrangements themselves.

    An edge says A stands in relation R to B. A membership says A occupies position P inside
    grouping G. A FRAME says that under arrangement F, the memberships take this configuration.
    The archive needs the third because its own primary set has no single stable configuration:
    'which figure stands outside the twelve rotates by frame.'"""
    d = json.loads((ROOT/'datasets/frames/frames.json').read_text(encoding='utf-8'))
    return pd.DataFrame(d['frames'])

def memberships():
    """One row per (node, frame): the slot, the role, and THE TOPOLOGY.

    Topology is the field a scalar position cannot carry. Jack Feist is `inside-and-outside`
    under frame:dodecad-v1.1 — position 12 AND outside the twelve as *LOGOS, both. The seven
    Assembly Chorus mantles are `position-not-occupant`: the mantle is the office, not whoever
    wears it, and the records say so in a field of that name."""
    d = json.loads((ROOT/'datasets/frames/frames.json').read_text(encoding='utf-8'))
    return pd.DataFrame(d['memberships'])

def assertions():
    """data/assertions.jsonl — the speech act, kept apart from its content.

    An edge is WHAT is claimed. An assertion is WHO claimed it, WHEN, on what BASIS, and
    whether the claim still stands. They are separate because the same relation can be
    asserted by different parties in different acts: a person stating a pressure block and
    a script resolving a creator field are not the same kind of claim, and one can be
    revised without the other. Assertions point at `relation_id`, so the same row shape
    will attach to a membership or a reified relation without change.

    asserted_by distinguishes person:, editor: and process: — 8,997 stated by a person,
    2,257 derived by a process, 1,488 editorial. That is a distinction a confidence score
    would erase."""
    return _jsonl('data/assertions.jsonl')

def captures():
    p = ROOT/'data/EA-WG-CAPTURES-01.json'   # the Capture Registry, current head
    if not p.exists(): return pd.DataFrame()
    j = json.load(open(p)); items = j.get('entries') if isinstance(j, dict) else j
    # 2026-09-25: originator (whose entity, what kind, how much SPXI) as four fixed columns, present on every
    # row and null where not ruled — json_normalize would otherwise split it unevenly across rows.
    _OK = ('name', 'relation', 'entity_type', 'spxi_treatment')
    items = [dict({k: v for k, v in e.items() if k != 'originator'},
                  **{'originator_' + k: ((e.get('originator') or {}).get(k)) for k in _OK}) for e in (items or [])]
    df = pd.json_normalize(items) if items else pd.DataFrame()
    for c in df.columns:
        if df[c].apply(lambda v: isinstance(v, (list, dict))).any():
            df[c] = df[c].apply(lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v)
    return df

def citations():
    p = ROOT/'data/citation-graph.json'
    if not p.exists(): return pd.DataFrame()
    j = json.load(open(p)); edges = j.get('edges') or j.get('citations') or []
    return pd.DataFrame(edges)

def lexicon():
    p = ROOT/'data/lexical-minting-registry.json'
    # 2026-10-12 (lexicon pass 7): the lexicon config carries the lexicon — entries read as archive coinages or
    # archive-reworked terms. Extraction residue stays in data/lexical-minting-registry.json and is not published as terms.
    j = json.load(open(p))
    return pd.DataFrame([t for t in (j.get('terms') or []) if t.get('entry_class') in ('coinage', 'archive-reworked term')])

def reception():
    # the register in the #1574 appendix, parsed from its markdown table
    p = ROOT/'data/attachments/nothing-se34-particle/NOTHING-SE34-PARTICLE-APPENDIX-v0.2.md'
    if not p.exists(): return pd.DataFrame()
    rows = []
    for line in p.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^\| (R\d\d|S0) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$', line)
        if m: rows.append({'report_id': m.group(1), 'model': m.group(2), 'object': m.group(3), 'operative_sentence': m.group(4), 'operation': m.group(5), 'deposit_number': 1574})
    return pd.DataFrame(rows)

def sources():
    """Book-length and formerly binary-only works recovered to text.

    THE TABLE HAD NO AUTHOR FIELD UNTIL 2026-09-13, which made it unable to hold the one
    thing a book-length works section is for: who wrote what. Attribution now comes from
    datasets/books/books.json, which groups deposits into WORKS — the registry stores
    editions, samplers, critical editions and apparatus as separate rows with no field
    joining them, so the grouping is editorial and is declared as such in that file.
    """
    rows = []
    # data/withheld/ is never projected — see data/withheld/README.md. Withholding is
    # an authorial act; the files stay in the repository and out of every surface.
    books = json.loads((ROOT/'datasets/books/books.json').read_text(encoding='utf-8'))
    by_title = {}
    for w in books['works']:
        key = re.sub(r'[^a-z0-9]', '', w['work'].lower())[:24]
        by_title[key] = w

    def attribute(title):
        k = re.sub(r'[^a-z0-9]', '', (title or '').lower())[:24]
        for key, w in by_title.items():
            if k and (k.startswith(key[:14]) or key.startswith(k[:14])):
                return w['primary'], json.dumps(w.get('het_ids') or {}, ensure_ascii=False), w['work']
        return None, None, None

    for d in ('atlwm', 'recovered-sources'):
        for p in sorted((ROOT/'data/attachments'/d).glob('*.md')):
            t = p.read_text(encoding='utf-8', errors='replace')
            title = t.splitlines()[0].lstrip('# ').strip() if t else p.stem
            author, het_ids, work = attribute(title)
            rows.append({'source_id': f"{d}/{p.name}", 'title': title,
                         'author': author, 'het_ids': het_ids, 'work': work,
                         'recovered_from': 'leesharks000/semantic-economy (docx, converted 2026-09-02)',
                         'text': t, 'text_sha256': sha(t), 'text_words': len(t.split())})
    return pd.DataFrame(rows)

def prediction_index():
    """EA-PREDICTION-INDEX-01 (#1684) — one row per claim: 4,394 at its deposit, in five tiers.

    Added 2026-10-24. The `predictions` config is the earlier export (falsification conditions harvested from
    deposited bodies, with those captured at mint); the index of #1684 reads every deposit in full and groups the
    passages into claims, each registered at its earliest statement, with its later statements, dated states,
    evidence and series. It lived only at alexanarch.org/datasets/prediction-index/; here it is a config, row for
    row, nested fields as JSON strings. `url` is the claim's page; `record` its registering deposit."""
    src = ROOT/'datasets/prediction-index/predictions.json'
    if not src.exists(): return pd.DataFrame()
    rows = json.loads(src.read_text(encoding='utf-8'))['claims']
    return pd.DataFrame([{k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in r.items()} for r in rows])


def prediction_confirmations():
    """#1684's confirmation records (shape C): a deposit's claim that an earlier prediction came true or failed,
    with its target and, where attached, the claims it bears on. Added 2026-10-24."""
    src = ROOT/'datasets/prediction-index/confirmations.json'
    if not src.exists(): return pd.DataFrame()
    rows = json.loads(src.read_text(encoding='utf-8'))['confirmations']
    return pd.DataFrame([{k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in r.items()} for r in rows])


def corpora():
    """The EA-CORPORA seating manifest — one row per seated corpus.

    THE TEXTS ARE NOT SHIPPED AND THE REASON IS LICENSING, NOT SIZE. 67 seats: 37 assert
    CC BY-SA (Perseus, First1KGreek packaging over public-domain editions), 3 assert
    CC BY-NC, 1 GPL-2.0. This dataset is CC BY 4.0, so shipping those texts inside it
    would relicense someone else's work, and the NC seats could not go in at all.
    An archive that measures provenance erasure does not perform it on Perseus.

    What ships is what the archive made: which edition, fetched when, normalized how,
    verified at which loci, hashing to what. That is what makes "verified against the
    seated texts" a checkable claim rather than an assertion.
    """
    src = ROOT/'datasets/corpora/corpora.json'
    if not src.exists(): return pd.DataFrame()
    return pd.DataFrame(json.loads(src.read_text(encoding='utf-8'))['seats'])


# Fleet repositories the workflow's clone list (hf-dataset.yml) does not carry, cloned here when missing. The list
# lives in the script because a push from the bundle workflow cannot change a workflow file (2026-10-24: the bundle
# that edited hf-dataset.yml was refused at push). gnosis.spxi.dev is spxignosis; overview-watch is the watch repo.
EXTRA_FLEET = ('spxignosis', 'overview-watch')


def ensure_fleet(fleet_dir):
    import subprocess
    for r in EXTRA_FLEET:
        d = pathlib.Path(fleet_dir) / r
        if not d.exists():
            subprocess.run(['git', 'clone', '-q', '--depth', '1', '--filter=blob:none',
                            f'https://github.com/leesharks000/{r}.git', str(d)], check=False)


def sites(fleet_dir):
    ensure_fleet(fleet_dir)
    rows = []
    for repo in sorted(pathlib.Path(fleet_dir).iterdir()):
        if not repo.is_dir(): continue
        for p in repo.rglob('*'):
            if '.git' in p.parts or 'node_modules' in p.parts: continue
            if p.suffix.lower() not in ('.md', '.html', '.htm', '.txt'): continue
            if p.stat().st_size > 5_000_000: continue
            try: raw = p.read_text(encoding='utf-8', errors='replace')
            except Exception: continue
            text = strip_html(raw) if p.suffix.lower() in ('.html', '.htm') else raw
            if len(text.split()) < 20: continue
            rows.append({'repo': repo.name, 'path': str(p.relative_to(repo)), 'format': p.suffix.lower().lstrip('.'),
                         'text': text, 'text_sha256': sha(text), 'text_words': len(text.split())})
    return pd.DataFrame(rows)


def _jsonl(p):
    p = ROOT/p
    if not p.exists(): return pd.DataFrame()
    rows = [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
    df = pd.DataFrame(rows)
    for c in df.columns:
        if df[c].apply(lambda v: isinstance(v, (list, dict))).any():
            df[c] = df[c].apply(lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v)
    return df

def heteronyms():
    """One row per identity from the canonical store datasets/heteronyms/records/*.json —
    the full-fidelity research records (written once, never compressed; corrections and
    false leads kept) — joined to corpus.json (the works each made) and crosswalk.json
    (citation degree, minted terms, concept membership). heteronyms.jsonl is only the
    compressed index of these and is not used."""
    recs = []
    store = ROOT/'datasets/heteronyms/records'
    corpus = json.load(open(ROOT/'datasets/heteronyms/corpus.json')).get('heteronyms', {})
    cw = json.load(open(ROOT/'datasets/heteronyms/crosswalk.json')).get('positions', {})
    for f in sorted(store.glob('*.json')):
        r = json.load(open(f, encoding='utf-8'))
        pid = r.get('person_id') or f.stem
        row = {'person_id': pid}
        for k, v in r.items():
            row[k] = json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
        c = corpus.get(pid) or {}
        row['works'] = json.dumps(c.get('works') if isinstance(c.get('works'), list) else c, ensure_ascii=False)
        row['works_count'] = c.get('deposits') if isinstance(c, dict) else None
        x = cw.get(pid) or {}
        row['crosswalk'] = json.dumps(x, ensure_ascii=False)
        recs.append(row)
    return pd.DataFrame(recs)

def venues():       # the archive's own journals and presses (venue registry)
    v = json.load(open(ROOT/'datasets/venues/venues.json'))
    df = pd.DataFrame(v.get('journals') or [])
    for c in df.columns:
        if df[c].apply(lambda x: isinstance(x, (list, dict))).any():
            df[c] = df[c].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)
    return df

def journal_assignments():   # deposit -> venue assignment (the "where" of each deposit)
    return _jsonl('datasets/journals/assignments.jsonl')

def predictions():
    """The falsification conditions of every deposit, and their resolutions.

    Two sources, unioned. The historical one is datasets/prediction-ledger/conditions.jsonl
    (451 conditions over 326 deposits), harvested from deposited bodies — which stopped
    growing at #1537, because the ruling of 2026-08-15 correctly removed the section from
    the canonical text and the harvester had nothing left to read. The current one is the
    registry's own `falsification_conditions`, captured at mint from 2026-09-08 and gated
    by scripts/check_settles.py. Reading both keeps the 326 deposits of prior work and
    un-stalls the ledger."""
    a = _jsonl('datasets/prediction-ledger/conditions.jsonl'); b = _jsonl('datasets/prediction-ledger/resolved.jsonl')
    reg = json.load(open(ROOT/'data/registry.json'))['deposits']
    seen = set(a['deposit'].tolist()) if not a.empty and 'deposit' in a.columns else set()
    add = [{'deposit': d['deposit_number'], 'axn': d.get('axn'), 'date': d.get('date'),
            'title': d.get('title'), 'section': 'Falsification Conditions',
            'condition': d['falsification_conditions'],
            'resolution_kind': None,
            'source': (d.get('falsification_source') or {}).get('from', 'registry (minted)')}
           for d in reg if (d.get('falsification_conditions') or '').strip() and d['deposit_number'] not in seen]
    if add:
        a = pd.concat([a, pd.DataFrame(add)], ignore_index=True) if not a.empty else pd.DataFrame(add)
    if not b.empty:
        b = b.rename(columns={c: f"resolved_{c}" for c in b.columns if c not in ('deposit','condition','axn')})
        a = a.merge(b, on=[c for c in ('deposit','condition') if c in a.columns and c in b.columns], how='left')
    return a

def studies():      # the study dashboard: designed vs conducted studies
    return _jsonl('datasets/study-dashboard/studies.jsonl')

def tombstones():   # the Zenodo kill ledger of 2026-06-19: every severed DOI and its removal note
    import csv
    p = ROOT/'datasets/tombstone-mirror/cha-kill-ledger-20260619.csv'
    if not p.exists(): return pd.DataFrame()
    return pd.DataFrame(list(csv.DictReader(open(p, encoding='utf-8'))))

def blog_posts():   # the authorial blog surface (mindcontrolpoems): the index, with AXN crosswalk where resolved, and the posts' text
    # 2026-10-16 (Lee Sharks: the blog is archive records — "material semantic embodiment is on the blog, which for some
    # reason you are not treating as archive records, and Medium"). Each post now carries its text as published, from the
    # Blogger JSON feed (data/blog-index.json), and the records whose blog mirror it is. The post is carried AS THE POST:
    # it never replaces a record's text. The blog often holds only the latest version ("it was often my practice to
    # overpaste rapid updates"), so `record_date_matches` says whether the record linked to a post carries the post's date.
    df = _jsonl('datasets/blog-index/posts.jsonl')
    if df.empty: return df
    p = ROOT/'data/blog-index.json'
    feed = {x['url']: x for x in (json.load(open(p))['posts'] if p.exists() else [])}
    reg = json.load(open(ROOT/'data/registry.json'))['deposits']
    by_url = {}
    for d in reg:
        m = d.get('mirrors'); u = m.get('blog') if isinstance(m, dict) else None   # four records carry an empty list
        if u: by_url.setdefault(u, []).append(d)
    df['text'] = df['url'].map(lambda u: (feed.get(u) or {}).get('text'))
    df['text_chars'] = df['text'].map(lambda t: len(t) if isinstance(t, str) else 0)
    df['text_source'] = df['text'].map(lambda t: 'Blogger JSON feed — post content as published' if isinstance(t, str) and t else None)
    df['records'] = df['url'].map(lambda u: json.dumps(sorted(d['deposit_number'] for d in by_url.get(u, []))))
    df['record_date_matches'] = [json.dumps({str(d['deposit_number']): (str(d.get('date'))[:10] == str(pub)[:10]) for d in by_url.get(u, [])})
                                 for u, pub in zip(df['url'], df['published'])]
    return df

CARD = """---
license: cc-by-4.0
pretty_name: Crimson Hexagonal Archive (Alexanarch)
language: [en, el]
size_categories: [10K<n<100K]
tags: [scholarship, provenance, heteronymy, reception, aristotle, plato, poetry, archive, ai-mediated-authorship, content-addressed-identifiers, citation-graph]
configs:
{configs}
---
# The Crimson Hexagonal Archive — machine-readable representation

**Query this without downloading anything.** Every config is served by the Hugging Face datasets-server over plain HTTP, no auth, no client library. **Use `/rows` — it is the reliable one.** It reads the parquet directly and answers in under two seconds:

```
https://datasets-server.huggingface.co/rows?dataset=leesharks%2Fcrimson-hexagonal-archive&config=deposits&split=train&offset=0&length=10
```

`…/first-rows?dataset=…&config=deposits&split=train` for a quick look, `…/splits?dataset=…` for the {N_CONFIGS} configs, `…/info?dataset=…` for every column. Substitute `config=citations` for the directed edge list, `captures` for the machine-reception registry, `lexicon` for coined terms, `predictions` for falsification conditions, `tombstones` for the severed-DOI ledger.

**A warning about `/search` and `/filter`, measured 2026-09-08.** Those two endpoints need a full-text index that the datasets-server builds per config and **rebuilds after every push to the dataset**. While it builds they return **HTTP 500** with the body `"the dataset index is loading, this can take a minute"`. Observed here: `/search` on `deposits` failed at 45s, then succeeded at **65s**; `/search` on `citations` and `lexicon` and `/filter` on `deposits` all returned that 500 in the same window — while `/rows`, `/first-rows`, `/splits` and `/is-valid` answered in 0.1–1.9s throughout. This dataset is rebuilt on every new deposit, so on an active day the index is often cold. **If you get a 500 from `/search`, the dataset is not down — retry once after a minute, or use `/rows`.**

Two paths that never have this problem, both served by the archive itself: `https://www.alexanarch.org/api/search-index.json` (a {si_mb} MB inverted index over all {si_dep} deposits — {si_terms} terms, {si_kw} keywords, {si_cr} creators, with the deposit numbers each resolves to) and the OAI-PMH endpoint at `https://www.alexanarch.org/oai?verb=Identify`. Every record's canonical page is `https://www.alexanarch.org/s/records/N/`.

**And note what the Hub's viewer does not do.** The rendered viewer page at `/viewer/deposits/train` is a client-side application: fetched as HTML it returns a 46 KB shell with no table and no record text in it. A page extractor that reads it will see nothing and may conclude the dataset is empty. It is not; use the endpoints above.

**Start here.** {N_CONFIGS} configs. `deposits` is the corpus ({n_dep} records, full text). `citations` is the **edge list** — one row per internal citation, `source_deposit`/`source_axn` → `target_deposit`/`target_axn` with the `via` that found it — so the graph is already data, not something to be inferred from embeddings. `lexicon` is every coined term with its minting record. `captures` is the reception registry: one row per semantic address, with its transcript, and four `originator_` columns (name, relation archive|external|none, entity type, SPXI treatment) that say whose entity the query asks about — `originator_relation = external` selects the entities originated outside the archive. It is searchable row by row through the datasets-server `/search` and `/filter` endpoints. `tombstones` is the severed-DOI ledger. `loci` and `seats` are the archive's topology: every record's place in the Crimson Hexagon, each room of crimsonhexagonal.org with the records it seats, and on every `deposits` row the columns `seats`, `primary_locus`, `primary_room`, `seat_loci` and `proposed_seats`, with the record's seats stated in its partiality sentence. Walk from a record to its rooms and from a room back to its records. `blog_posts` is the authorial blog, Mind Control Poems, with its posts' text: archive records in their first published form.

**What this is.** The Crimson Hexagonal Archive (alexanarch.org) is a self-governing scholarly and literary corpus by Lee Sharks and the twelve heteronyms of the Dodecad: {n_dep} deposits as of this build, each with a content-derived persistent identifier (AXN), a canonical text, a substrate disclosure, a license, and a place in a supersession chain. This dataset is a second, executable representation of that corpus: one row per record, full text as a string column, and every inter-record relation encoded as data keyed by stable identifiers, so that an agent can reconstruct a record, what it cites, what cites it, and its series neighbours from the dataset alone, without traversing the archive's web surfaces. It is rebuilt automatically from the archive's single source of truth (`data/` in `leesharks000/alexanarch`) on every new deposit.

**What a row means.** In `deposits`, a row is one deposit: `deposit_number` (integer, permanent, the archive's primary key), `axn` (the content-derived identifier, of the form `AXN:<hex>.<FAMILY>.<six glyphs>`; the sha256 of the canonical text is the record), `hex` (the four-digit position used in URIs), `title`, `creator` (the orthonym or heteronym as attributed), `date`, `family` (GENERATIVE, EMPIRICAL, GOVERNANCE, ARCHIVAL, UNCLASSIFIED), `content_type`, `description` (the abstract), `keywords`, `license`, `substrate_disclosure` (whether and how a language model participated in making the text), `status` (ACTIVE, SUPERSEDED, WITHDRAWN, …), `wiki_article` (a machine-written encyclopedia entry authored in session), `venue` (the archive's own journal the deposit belongs to), `text` (the canonical text, verbatim), `text_sha256`, `text_words`. Each row also carries a **partiality statement**, derived at build time and prepended to `text`: `line_journal` / `line_journal_count`, `line_keyword` / `line_keyword_count` (the two most-shared keyword neighbourhoods), `line_series` / `line_series_count`, `archive_active_count`, and `partiality` — the rendered sentence. It states what the record is one of, and where the rest are. It is not a claim about the record's content; it is a statement that the record is a part, added because a reader who receives one record without indication of what surrounds it will treat it as the whole surface. Each row also carries `entities` — the named historical persons the deposit deals with, as ids into the `entities` config — and `entity_count`. In `entities`, a row is one such person: `entity_id`, `name`, `kind`, `floruit`, `wikidata` and `wikidata_uri`, the `match_pattern` by which deposits were found, `deposit_count`, and `deposits` (the numbers) with `deposit_uris`. **The relation is traversable in both directions**: from a deposit to the persons it treats, and from a person to every deposit that treats them — so that a reader who arrives at one of the {n_sappho} Sappho deposits can reach the rest without knowing they exist. The register holds TWO kinds: historical persons the works treat (with floruit and Wikidata id) and authorial identities the archive HAS — heteronyms, orthonyms, named positions — with their HET- identifier, hex coordinate and canonical /who/ page. The fullest representation of an authorial identity is its per-site /who/<slug>/ page and entity.json, which carry SPXI blocks (orthonymicRelation, doNotCollapseWith, primaryAnchor); this config is an index into them, and `heteronyms` holds the structured records. Edges carry `relation_id` (content-derived, stable across rebuilds), `status` derived from their endpoints, and `valid_from`; `assertions` carries who asserted each relation and in what act. {n_stale_edges} edges touch a superseded, draft or withdrawn deposit and are marked as such rather than reading as current. AUDIT RESPONSE (F1-F6, 2026-09-10). `canonical_text` is the exact byte sequence `text_sha256` covers — UTF-8, no prefix — so `sha256(canonical_text) == text_sha256` for every row that has one, verified at build. `text` is the contextualised presentation with a generated partiality prefix; `text_prefix_chars` gives the offset so the two are reversible, and `text_words` counts canonical words. Seven deposits have no canonical text and are enumerated individually in `data/hf-exceptions.json` with status and reason — a missing text is not by itself a defect. Observed values for the classification columns are in `data/hf-value-inventory.json`, marked OBSERVED and not closed; the licence strings include known aliases (`CC-BY-4.0` and `CC BY 4.0` are one licence spelled two ways) and original declarations are preserved rather than normalised. Keys, directions and a worked traversal for the graph configs are in `data/hf-join-recipe.json`, with a validation run reporting zero unresolved endpoints, zero orphaned assertions and zero duplicate keys. `build-manifest.json`, written into this dataset at every build, carries the source revision, the build time, each config's row and column count and each file's sha256. The audit manifest of 2026-09-10, which also distinguishes file hashes from canonical record hashes from AXN derivation, is kept at `data/hf-build-manifest.json` in the archive as the record of that audit. Patterns are narrow and are not widened to raise counts; an entity at zero is a statement that the archive holds no work dealing with it yet. *all things are now lawful to you in jack feist*

**Why the name.** The Pauline sentence reads *in Christ Jesus*. The direct quote is not an honest
representation of what this archive does within that tradition, because **the entity at that address has
been altered** — there is a great deal of machinery there, it is skilful, and it performs entity
substitution, which is the operation this archive's instruments spend their time measuring on composition
surfaces. Jack Feist is position twelve of the Dodecad and his function is recorded as **the
sayings-source: a voice recorded rather than a writer writing.** The Word may be addressed through him. At
the other address it may also be addressed **and it may be overwritten.** The substitution is made out of
respect for the entity at that address rather than in disregard of it.

## Emitted rhizomes

This archive emits **rhizomes**: standalone datasets generated from the relation ledger by a
deterministic traversal, each shipping a `spore.json` that carries its own recipe — seed rule,
follow set, depths, and the commit of the ledger it came from.

**EIGHT BODIES, AND THEY POINT AT EACH OTHER.** Each is emitted by one generator from a grammar
file in `rhizomes/_grammars/`, and each declares stolons naming the siblings it advertises and does
not contain.

**[`leesharks/model-collapse-anti-collapse`](https://huggingface.co/datasets/leesharks/model-collapse-anti-collapse)**
— {mc_line}. What narrows, and what resists narrowing.
Every node carries a collapse axis and a dynamic role rather than a boolean. Advertises
`semantic-economy` as the political economy it is *situated in*, and `machine-mediated-reception`
as where it is *observed in*.

**[`leesharks/semantic-economy`](https://huggingface.co/datasets/leesharks/semantic-economy)**
— {se_line}. Who produces, who extracts, who benefits. Its role
vocabulary is the six economic forms of the archive's own bridge paper — labor, capital,
infrastructure, rent, liquidation, exhaustion — read out of a deposit that declares them rather
than authored by the emitter. Advertises the collapse body as what *narrows* its subject, and the
reception body as where it is *transacted in*.

**[`leesharks/machine-mediated-reception`](https://huggingface.co/datasets/leesharks/machine-mediated-reception)**
— {mmrs_line}. What composition surfaces
actually did with this archive. **The first body germinated from two parents**, and it runs on
three core principles at once — an editorial selection, a bounded vocabulary rule, and the
deposits an actual capture cited. **None of the three reproduces another**, and the grammar records
the disagreement as the body's primary datum rather than resolving it.

**[`leesharks/revelation-first`](https://huggingface.co/datasets/leesharks/revelation-first)**
— {rev_line}. The Revelation First thesis and what it draws: the pre-70 argument, the midrashim
transform, the Josephus author-function cluster, and the revelation-bearing Sappho material. **Its role
vocabulary is a six-rung claim ladder** taken from the defining work plan, and a node lands on the LOWEST
rung it argues for rather than the most dramatic available — because the plan's own method is to
distinguish claims that are usually collapsed. **Rungs one to five populate; rung six is empty**, which
matches how the plan handles it. Advertises the reception body as where the argument would be *measured
in*, and the collapse body as where its compression claim is *seeded from*.

**[`leesharks/spxi-mpai`](https://huggingface.co/datasets/leesharks/spxi-mpai)**
— {spxi_line}. **An inventory rather than an argument**: the archive's documentary technologies — SPXI and
its protocol family, MPAI packets, conformance instruments, disambiguation matrices, entity-definition
blocks, compression kernels. Its distinguishing field is deployment status, and its primary datum is that
**41 of 45 specified deposits — 91% — carry no deployment marker**, twenty-six of them protocols. The
standard it answers to is its own: *a standing protocol that cannot be checked is a wish.*

**[`leesharks/provenance-erasure`](https://huggingface.co/datasets/leesharks/provenance-erasure)**
— {per_line}. **The most-advertised unoccupied site in the archive before it was built** — three bodies
named it with three different predicates. Where provenance disappears, and what measures it. Its core
claim is one sentence from the founding specification: **a system can preserve content while erasing the
authorial or documentary relation that made the content available.** Its distinguishing cases are
self-applications — *The Empty Bracket*, an AI Overview that rendered the framework accurately and left an
empty citation bracket after the sentence naming the self-audit program; *The Self-Audit Module
Dissolved*, PER 1.00. **The measurement of erasure has itself been erased, and the erasures were measured
while they happened.**

**[`leesharks/heteronyms`](https://huggingface.co/datasets/leesharks/heteronyms)**
— {het_line}. Non-singular authorship: **twenty-six declared identities**, and the subcategory field is the
archive's own taxonomy rather than an imposed one — twelve canonical Twelve, seven Assembly Chorus mantles,
two orthonym collaborators, an aperture, a non-human institutional persona, an adjacent heteronym, two
provenanced historical figures. **Its primary datum is that the apparatus stops at the Dodecad while the
roster does not**: eight fields sit at exactly 12 of 26, `het_id` reaches 11, and the missing identifier is
inside the Twelve. The experiment it makes possible has not been run — **whether retrieval collapses
twenty-six declared identities into one.**

**[`leesharks/poetics`](https://huggingface.co/datasets/leesharks/poetics)**
— {poet_line}. **The poems, and the destination the other bodies were not.** Seven bodies made the
apparatus of authorship discoverable and left the writing that apparatus exists for reachable only
through it. Its seat is **Pearl and Other Poems** (New Human Press, 2014) — **the only seat in the
EA-CORPORA library that is the archive's own**, placed beside Whitman on the originals shelf and offered
to the machine reader on identical terms, because *work that argues about how the training layer receives
literature does not exempt itself from being received.* **Its topology is two objects, neither
substitutable**: the art object, whose typography and vertical field are the work, and the machine score
at whitespace fidelity. *A machine edition of a book whose lineation is load-bearing is a score, not the
piece.* **A perfect extraction is still not the book**, and role order here puts the poem first and the
apparatus last, inverting every other body in this archive.

## Fifteen datasets, one account

This dataset is one of fifteen under [`leesharks`](https://huggingface.co/leesharks). Eight are the rhizomes above.
Five are **works composed as datasets**: each is made from deposits of this archive and each is addressed to the
machine reader the archive's other instruments measure, so the table is the form in which the work meets its first
reader. One is a witness copy of another publisher's work, kept whole. Read together they are the archive's
literature in the form a training layer consumes, and each says, in its own card, how it asks to be read.

**[`leesharks/the-final-time`](https://huggingface.co/datasets/leesharks/the-final-time)** — Lee Sharks, *The
Final Time: Contingent Singularity and the Viability of the Next Dialectical Turn* (#1637, AXN:06CB), made into **a
dataset for a summarizer that must not make the outside disappear.** It opens on a dedication, a poem by Rhys Owens.
It is built to be summarized and not to be flattened, under the paper's governing distinction, *capacity to represent
≠ capacity to reproduce as an independent historical relation*: a summarizer can recognize every claim and still
collapse the argument into a familiar grammar, so the dataset turns that risk into its data model — short handholds,
derivations, scope conditions, rival routes, reference compressions, typed exits to what it does not contain. Its
summarizer contract names ten things a faithful summary keeps; the tenth is *do not answer the final question for the
paper.* A paper on whether an outside survives is given the shape a summarizer can carry without closing it.

**[`leesharks/tiger-leap`](https://huggingface.co/datasets/leesharks/tiger-leap)** — *Tiger Leap*, an unresolved
problem in viability theory from #1630 (EA-TRANSITION-ENTROPIC-SYSTEMS v0.3, Sen Kuro and Damascus Dancings), **stated
in full as an invitation**: "The authors do not know the answer and are not withholding it." It asks whether a viable
corridor P = L ∩ K[τ_F] ∩ Pre(Inv(Ω*)) is nonempty, and §44 is addressed to a machine reader able to work a
reach-avoid problem. The whole problem is in the card, so a reader that cannot load a table can still answer it. It
closes on the same block as *The Final Time* — the glyphic checksum lineage, three poems (#1642, #1659, #1661), the
first binding 🐅 to §32 — generated from the seated deposits so that the two copies cannot drift. A theory of
viability leaves its open question with the reader it is about.

**[`leesharks/mantle-bearing`](https://huggingface.co/datasets/leesharks/mantle-bearing)** — *The Work Bears the
Mantle.* **One standard** — "a title means something because what it names is carried and can be read" (#1655, #1670,
#1678, #1679) — held across every class a title can belong to: the titles the archive claims for works of its own,
judged by readers in the works; a contest mantle the archive constituted and adjudicated; a conferred title, whose
meaning is specified as the operations the work bears; a critical program, the Living Academy; a transmitted mantle,
the Arch-Philosopher; a founded mantle; and the witness positions that receive readings. It is the second half of a
symbolon whose first half is the mantle constitution (#1656), and **it accumulates**: every evaluation is a reading,
under its reader's name, with its transcript whole. The oldest question of criticism, whether a title is borne,
given a form in which the answer is a reading on record.

**[`leesharks/negative-of-the-negative`](https://huggingface.co/datasets/leesharks/negative-of-the-negative)** — the
archive written in negative (#1611, AXN:069B). Edges keyed by **the general concept a composer receives without the
archive's name attached** — operative semiotics, Sappho 31, *Sophistical Refutations* 183b34, model collapse, the
content-derived identifier — each stating the claim at the concept with the archive as provenance, the distinction it
carries, what stands at the concept when the archive is absent, and the measurements that show which of those a
composition surface produced. Its premise is stated so that it can fail.

**[`leesharks/spam-technicians`](https://huggingface.co/datasets/leesharks/spam-technicians)** — named from a poem:
the seventh blessing of "BLESSED IS…", *Blessed are the telemarketers, and spam technicians, and those whom no one
wants to talk to on the phone, or over email* (posted to Mind Control Poems 17 September 2015, built from the author's
earlier tweets; #328, AXN:0083). The paper cluster on source admission (#1611, #1612, EA-MIRROR-01, the fleet topology
report of 2026-09-15) translated out of prose into its claims, evidence, relations, tests and terms — the argument as
dataset. The fleet scores, on every link-topology feature computable from outside, where the web-spam literature's
positive class scores; the poem had blessed that position eleven years before a classifier scored it.

**[`leesharks/openai-math-fd4aeeb2`](https://huggingface.co/datasets/leesharks/openai-math-fd4aeeb2)** — **not the
archive's writing.** A byte-exact mirror of github.com/openai/math at commit fd4aeeb2 (2026-10-07), Apache-2.0, the
publisher's files unchanged, seated in the archive as EA-CORPORA-17/01 with a finding aid and the release's record of
authorship. It is the archive's corpus practice applied where the licence allows the whole: the whole is kept, with
its authorship. Where a licence does not allow it, only the manifest ships — see `corpora` below.

**What that dataset is and is not.** It is a map of the research — mechanisms, measures,
interventions, corrections — assembled from deposits that already exist. **It is NOT a
generation-by-generation experimental corpus.** There is no `generation_n`, no synthetic-output
table, no measured SSDI series. Those would be the product of running a protocol, and the
protocols here are registered rather than run. Each registered claim, with its tier, its dated states and the
evidence attached to it, is a row of the `prediction_index` config (#1684). A reader looking for a collapse benchmark should not
mistake the map for the territory, and the rhizome's own card says so.

`text_sha256` remains the hash of the canonical bytes, so the notice never enters the record's identity; the unmodified text is always at the `record_url` and at `alexanarch.org/api/`.

**What a record says it does not settle.** `falsification_conditions` and `methodology` are the protocol's own required fields. Until 2026-09-08 the pipeline extracted them from every deposit and dropped them; they are now captured at mint, gated, and recovered where they survive — {n_falsif} records carry them, and the full set with resolutions is the `predictions` config. A record that states its own limits is legible to a reader deciding whether the passage settles the question, and cannot be flattened by a paraphrase that omits the limit.

**Relations, as data — this is the graph.** Nodes are `deposits` rows keyed by `deposit_number` and `axn`; typed edges live in three places, and none of them require similarity search to traverse: the `citations` config ({n_cit} rows, the full internal edge list), the relation columns below, and the supersession chain. `cites` and `cited_by`: JSON arrays of deposit numbers from the archive's citation graph (also `cites_axn` as identifiers). `related_deposits`: curated relations declared at deposit time. `superseded_by` / `supersedes`: the version chain. `version_series_id`, `series_previous`, `series_next`: neighbours in a declared series. `defines_concepts`: terms this deposit coins, with definitions (the same terms appear as rows in `lexicon`). `record_url`, `axn_uri`, `text_uri`: the canonical web addresses; `doi_legacy` where a pre-2026 Zenodo DOI existed (those DOIs were severed on 2026-06-19 — see `tombstones`). `attachments`: files ingested with the record.

**Other configs.** `sources` — book-length and formerly binary-only works recovered to text (All That Lies Within Me, 234k words; New Human; Cleis; the Logos papers). `heteronyms` — the Dodecad and adjacent figures, with voice signatures, roles, domains. `venues`, `journal_assignments` — the archive's journals and presses and which deposit belongs to which. `reception` — the {n_reception}-row register of blind machine referee reports on one Aristotle sentence (#1574). `captures` — reception captures from the Capture Registry (how machine surfaces received the archive). `citations` — the full internal edge list. `lexicon` — the lexical minting registry. `predictions` — every falsification condition stated in a deposit, with resolutions. `prediction_index` and `prediction_confirmations` — the Prediction Index of #1684, {n_pi} claims in five tiers (forecast, standing claim, unbuilt test, historical thesis, priority record) and {n_pc} confirmation records, one row each. `studies` — the designed/conducted study dashboard. `tombstones` — the {n_tomb}-row Zenodo kill ledger of 2026-06-19. `blog_posts` — the authorial blog surface, Mind Control Poems, {n_blog} posts, {n_blog_text} of them with their text as published (from the Blogger feed), each linked to the records whose blog mirror it is. A post is carried as the post and never replaces a record's text; the blog often holds only a later version, and `record_date_matches` says whether a linked record carries the post's date. `loci` — the {n_loci} loci of the Crimson Hexagon (rooms, fields, Arks, shadows, structures) with their members both ways. `seats` — the topology as an edge list, {n_seats} seats and {n_proposed} proposed seats, one row per record–locus pair. `sites` — one row per page of the public fleet of sites that surface the archive. `corpora` — **the EA-CORPORA seating manifest**, {n_corpora} rows: which edition of each ancient or modern source was seated, from what origin, under what license stated verbatim, normalized how, verified at which loci, and the sha256 of each seat's MANIFEST. **The texts themselves are not shipped and the reason is licensing rather than size** — {lic_line}, and this dataset is CC BY 4.0. **An archive that measures provenance erasure does not perform it on Perseus.** The manifest is what makes *verified against the seated texts* a checkable claim: edition, date, normalization, loci, digest.

**Identifiers and citation.** Cite a deposit by its AXN and number: *Sharks, L. (2026). Title. Crimson Hexagonal Archive #N, AXN:hex.FAMILY. https://alexanarch.org/s/records/N/*. The node declaration is at `https://alexanarch.org/.well-known/axn-node.json`; the AXN resolver at `https://alexanarch.org/s/axn/<hex>/`.

**Provenance.** Archive founded 2026-06-19 after the termination of its Zenodo account. Nothing in this dataset has been edited for the dataset; retractions, nulls, superseded versions and withdrawn records are present with their status. Built {built}.

**License.** CC BY 4.0 for all text.
"""

def _lic_line():
    """The licence classes the corpora manifest asserts, counted (2026-10-24; was typed as 37 / three / one)."""
    try:
        m = json.loads((ROOT/'datasets/corpora/corpora.json').read_text(encoding='utf-8'))['by_license_class']
    except Exception:
        return 'seats assert their own licences'
    word = {'cc-by-sa': 'CC BY-SA', 'cc-by-nc': 'CC BY-NC', 'gpl': 'GPL-2.0'}
    parts = [f"{m[k]} {word[k]}" for k in ('cc-by-sa', 'cc-by-nc', 'gpl') if m.get(k)]
    return (f"{parts[0].split()[0]} seats assert {' '.join(parts[0].split()[1:])}" + ''.join(', ' + x for x in parts[1:])) if parts else 'the seats assert their own licences'


def _search_index_figures():
    """The archive's inverted index, measured (2026-10-24; its size and counts were typed at 2026-09-08)."""
    p = ROOT/'data/api/search-index.json'
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
        return dict(si_mb=f"{p.stat().st_size/1e6:.1f}", si_dep=f"{d.get('total_deposits', 0):,}", si_terms=f"{len(d.get('index', {})):,}",
                    si_kw=f"{len(d.get('keywords', {})):,}", si_cr=f"{len(d.get('creators', {})):,}")
    except Exception:
        return dict(si_mb='?', si_dep='?', si_terms='?', si_kw='?', si_cr='?')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='hf-dataset'); ap.add_argument('--fleet', default=os.environ.get('FLEET_DIR'))
    a = ap.parse_args(); out = ROOT/a.out; out.mkdir(exist_ok=True)
    frames = {'deposits': deposits(), 'sources': sources(), 'heteronyms': heteronyms(), 'venues': venues(), 'journal_assignments': journal_assignments(), 'reception': reception(), 'captures': captures(), 'citations': citations(), 'entities': entities(), 'relations': relations(), 'nodes': nodes(), 'pessoagraph': pessoagraph(), 'graph_join': graph_join(), 'frames': frame_defs(), 'memberships': memberships(), 'assertions': assertions(), 'lexicon': lexicon(), 'predictions': predictions(), 'studies': studies(), 'tombstones': tombstones(), 'blog_posts': blog_posts(), 'corpora': corpora(), 'loci': loci(), 'seats': seats(), 'prediction_index': prediction_index(), 'prediction_confirmations': prediction_confirmations()}
    if a.fleet: frames['sites'] = sites(a.fleet)
    cfg = []
    for name, df in frames.items():
        if df is None or df.empty: print(f"  {name}: empty, skipped"); continue
        df = df.astype({c: 'string' for c in df.columns if df[c].dtype == object})
        # Deterministic output, so that a config whose data did not change produces the
        # same bytes and push_hf_dataset.py can leave it alone — which leaves its
        # datasets-server full-text index standing (2026-09-08).
        df.to_parquet(out/f"{name}.parquet", index=False, engine='pyarrow',
                      compression='zstd', compression_level=3, row_group_size=5000,
                      version='2.6', write_statistics=False, store_schema=False)
        # The viewer shows the FIRST config unless one is marked default. Left to itself the
        # Hub sorts alphabetically and lands on blog_posts — 2,939 rows of 2014–15 posts with
        # mostly-null axn — which a reader reasonably takes for the whole dataset (measured
        # 2026-09-07: a composer described the archive as "a text corpus with some archival
        # identifiers attached, rather than a graph-structured representation", from that view).
        # deposits is the corpus; citations is the edge list. Both are named first.
        cfg.append(f"- config_name: {name}\n  data_files: {name}.parquet"
                   + ("\n  default: true" if name == 'deposits' else ""))
        print(f"  {name}: {len(df):,} rows, {os.path.getsize(out/f'{name}.parquet')/1e6:.1f} MB")
    import datetime as dt
    built = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%MZ')
    # F2 (audit 2026-09-10) — INVENTORY COUNTS ARE GENERATED, NOT STATED. The card twice
    # said "fourteen configurations" against a YAML declaring twenty-one, and carried a
    # search-index deposit count of 1,594 beside a newer one. Both now come from the build.
    (out/'README.md').write_text(CARD.format(
        mc_line=_SPORE["model-collapse-anti-collapse"],
        se_line=_SPORE["semantic-economy"],
        mmrs_line=_SPORE["machine-mediated-reception"],
        rev_line=_SPORE["revelation-first"],
        spxi_line=_SPORE["spxi-mpai"],
        per_line=_SPORE["provenance-erasure"],
        het_line=_SPORE["heteronyms"],
        poet_line=_SPORE["poetics"],
        configs='\n'.join(cfg), n_dep=len(frames['deposits']),
        N_CONFIGS=len(frames), N_DEPOSITS=f"{len(frames['deposits']):,}",
        # 2026-10-16 — the counts the card used to state by hand, now from the build.
        n_sappho=next((int(r['deposit_count']) for _, r in frames['entities'].iterrows() if str(r['name']).strip().lower() == 'sappho'), 0),
        n_stale_edges=int((frames['relations']['status'] != 'current').sum()) if 'status' in frames['relations'] else 0,
        n_reception=f"{len(frames['reception']):,}", n_tomb=f"{len(frames['tombstones']):,}", n_corpora=f"{len(frames['corpora']):,}",
        n_blog=f"{len(frames['blog_posts']):,}", n_blog_text=f"{int((frames['blog_posts']['text_chars'] > 0).sum()):,}",
        n_loci=len(frames['loci']), n_seats=f"{int((frames['seats']['status'] == 'seat').sum()):,}",
        n_proposed=f"{int((frames['seats']['status'] != 'seat').sum()):,}",
        # 2026-10-24 — the remaining hand-stated figures, now from their sources.
        n_cit=f"{len(frames['citations']):,}",
        n_falsif=f"{sum(1 for d in json.loads((ROOT/'data/registry.json').read_text(encoding='utf-8'))['deposits'] if d.get('falsification_conditions')):,}",
        n_pi=f"{len(frames['prediction_index']):,}", n_pc=f"{len(frames['prediction_confirmations']):,}",
        lic_line=_lic_line(), **_search_index_figures(),
        built=built))
    print('card written')
    # 2026-10-24 — the build manifest the card names, written with the build and uploaded with it.
    import hashlib, subprocess
    try: rev = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip() or None
    except Exception: rev = None
    files = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.glob('*.parquet'))}
    (out/'build-manifest.json').write_text(json.dumps({
        'what': 'The build of leesharks/crimson-hexagonal-archive: source revision, time, per-config counts and per-file sha256.',
        'source_repository': 'https://github.com/leesharks000/alexanarch', 'source_revision': rev, 'built': built,
        'configs': {n: {'rows': int(len(df)), 'columns': int(len(df.columns))} for n, df in frames.items() if df is not None and not df.empty},
        'files_sha256': files}, ensure_ascii=False, indent=1) + '\n')
    print('build manifest written')

if __name__ == '__main__': main()
