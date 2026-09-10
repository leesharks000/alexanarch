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
        rows[-1].update(_p)
        if _p['partiality'] and text:
            # served text carries the statement; text_sha256 stays the hash of the
            # canonical bytes, so the record's identity is untouched by the notice.
            rows[-1]['text'] = _p['partiality'] + "\n\n---\n\n" + text
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

def captures():
    p = ROOT/'data/EA-WG-CAPTURES-01.json'   # the Capture Registry, current head
    if not p.exists(): return pd.DataFrame()
    j = json.load(open(p)); items = j.get('entries') if isinstance(j, dict) else j
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
    j = json.load(open(p)); return pd.DataFrame(j.get('terms') or [])

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
    rows = []
    # data/withheld/ is never projected — see data/withheld/README.md. Withholding is
    # an authorial act; the files stay in the repository and out of every surface.
    for d in ('atlwm', 'recovered-sources'):
        for p in sorted((ROOT/'data/attachments'/d).glob('*.md')):
            t = p.read_text(encoding='utf-8', errors='replace')
            rows.append({'source_id': f"{d}/{p.name}", 'title': t.splitlines()[0].lstrip('# ').strip() if t else p.stem,
                         'recovered_from': 'leesharks000/semantic-economy (docx, converted 2026-09-02)', 'text': t, 'text_sha256': sha(t), 'text_words': len(t.split())})
    return pd.DataFrame(rows)

def sites(fleet_dir):
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

def blog_posts():   # index of the authorial blog surface (mindcontrolpoems), with AXN crosswalk where resolved
    return _jsonl('datasets/blog-index/posts.jsonl')

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

`…/first-rows?dataset=…&config=deposits&split=train` for a quick look, `…/splits?dataset=…` for the fourteen configs, `…/info?dataset=…` for every column. Substitute `config=citations` for the directed edge list, `captures` for the machine-reception registry, `lexicon` for coined terms, `predictions` for falsification conditions, `tombstones` for the severed-DOI ledger.

**A warning about `/search` and `/filter`, measured 2026-09-08.** Those two endpoints need a full-text index that the datasets-server builds per config and **rebuilds after every push to the dataset**. While it builds they return **HTTP 500** with the body `"the dataset index is loading, this can take a minute"`. Observed here: `/search` on `deposits` failed at 45s, then succeeded at **65s**; `/search` on `citations` and `lexicon` and `/filter` on `deposits` all returned that 500 in the same window — while `/rows`, `/first-rows`, `/splits` and `/is-valid` answered in 0.1–1.9s throughout. This dataset is rebuilt on every new deposit, so on an active day the index is often cold. **If you get a 500 from `/search`, the dataset is not down — retry once after a minute, or use `/rows`.**

Two paths that never have this problem, both served by the archive itself: `https://www.alexanarch.org/api/search-index.json` (a 2.8 MB inverted index over all 1,594 deposits — 17,944 terms, 7,116 keywords, 302 creators, with the deposit numbers each resolves to) and the OAI-PMH endpoint at `https://www.alexanarch.org/oai?verb=Identify`. Every record's canonical page is `https://www.alexanarch.org/s/records/N/`.

**And note what the Hub's viewer does not do.** The rendered viewer page at `/viewer/deposits/train` is a client-side application: fetched as HTML it returns a 46 KB shell with no table and no record text in it. A page extractor that reads it will see nothing and may conclude the dataset is empty. It is not; use the endpoints above.

**Start here.** Fourteen configs. `deposits` is the corpus ({n_dep} records, full text). `citations` is the **edge list** — one row per internal citation, `source_deposit`/`source_axn` → `target_deposit`/`target_axn` with the `via` that found it — so the graph is already data, not something to be inferred from embeddings. `lexicon` is every coined term with its minting record. `captures` is the reception registry. `tombstones` is the severed-DOI ledger. `blog_posts` is the 2014–15 origin layer and is the *thinnest* table here: it is an index of an old surface, not the archive. If a viewer drops you into `blog_posts`, you are looking at the least of it.

**What this is.** The Crimson Hexagonal Archive (alexanarch.org) is a self-governing scholarly and literary corpus by Lee Sharks and the twelve heteronyms of the Dodecad: {n_dep} deposits as of this build, each with a content-derived persistent identifier (AXN), a canonical text, a substrate disclosure, a license, and a place in a supersession chain. This dataset is a second, executable representation of that corpus: one row per record, full text as a string column, and every inter-record relation encoded as data keyed by stable identifiers, so that an agent can reconstruct a record, what it cites, what cites it, and its series neighbours from the dataset alone, without traversing the archive's web surfaces. It is rebuilt automatically from the archive's single source of truth (`data/` in `leesharks000/alexanarch`) on every new deposit.

**What a row means.** In `deposits`, a row is one deposit: `deposit_number` (integer, permanent, the archive's primary key), `axn` (the content-derived identifier, of the form `AXN:<hex>.<FAMILY>.<six glyphs>`; the sha256 of the canonical text is the record), `hex` (the four-digit position used in URIs), `title`, `creator` (the orthonym or heteronym as attributed), `date`, `family` (GENERATIVE, EMPIRICAL, GOVERNANCE, ARCHIVAL, UNCLASSIFIED), `content_type`, `description` (the abstract), `keywords`, `license`, `substrate_disclosure` (whether and how a language model participated in making the text), `status` (ACTIVE, SUPERSEDED, WITHDRAWN, …), `wiki_article` (a machine-written encyclopedia entry authored in session), `venue` (the archive's own journal the deposit belongs to), `text` (the canonical text, verbatim), `text_sha256`, `text_words`. Each row also carries a **partiality statement**, derived at build time and prepended to `text`: `line_journal` / `line_journal_count`, `line_keyword` / `line_keyword_count` (the two most-shared keyword neighbourhoods), `line_series` / `line_series_count`, `archive_active_count`, and `partiality` — the rendered sentence. It states what the record is one of, and where the rest are. It is not a claim about the record's content; it is a statement that the record is a part, added because a reader who receives one record without indication of what surrounds it will treat it as the whole surface. Each row also carries `entities` — the named historical persons the deposit deals with, as ids into the `entities` config — and `entity_count`. In `entities`, a row is one such person: `entity_id`, `name`, `kind`, `floruit`, `wikidata` and `wikidata_uri`, the `match_pattern` by which deposits were found, `deposit_count`, and `deposits` (the numbers) with `deposit_uris`. **The relation is traversable in both directions**: from a deposit to the persons it treats, and from a person to every deposit that treats them — so that a reader who arrives at one of the hundred and thirty-three Sappho deposits can reach the rest without knowing they exist. The register holds TWO kinds: historical persons the works treat (with floruit and Wikidata id) and authorial identities the archive HAS — heteronyms, orthonyms, named positions — with their HET- identifier, hex coordinate and canonical /who/ page. The fullest representation of an authorial identity is its per-site /who/<slug>/ page and entity.json, which carry SPXI blocks (orthonymicRelation, doNotCollapseWith, primaryAnchor); this config is an index into them, and `heteronyms` holds the structured records. Patterns are narrow and are not widened to raise counts; an entity at zero is a statement that the archive holds no work dealing with it yet. `text_sha256` remains the hash of the canonical bytes, so the notice never enters the record's identity; the unmodified text is always at the `record_url` and at `alexanarch.org/api/`.

**What a record says it does not settle.** `falsification_conditions` and `methodology` are the protocol's own required fields. Until 2026-09-08 the pipeline extracted them from every deposit and dropped them; they are now captured at mint, gated, and recovered where they survive — 270 records carry them, and the full set with resolutions is the `predictions` config. A record that states its own limits is legible to a reader deciding whether the passage settles the question, and cannot be flattened by a paraphrase that omits the limit.

**Relations, as data — this is the graph.** Nodes are `deposits` rows keyed by `deposit_number` and `axn`; typed edges live in three places, and none of them require similarity search to traverse: the `citations` config (10k+ rows, the full internal edge list), the relation columns below, and the supersession chain. `cites` and `cited_by`: JSON arrays of deposit numbers from the archive's citation graph (also `cites_axn` as identifiers). `related_deposits`: curated relations declared at deposit time. `superseded_by` / `supersedes`: the version chain. `version_series_id`, `series_previous`, `series_next`: neighbours in a declared series. `defines_concepts`: terms this deposit coins, with definitions (the same terms appear as rows in `lexicon`). `record_url`, `axn_uri`, `text_uri`: the canonical web addresses; `doi_legacy` where a pre-2026 Zenodo DOI existed (those DOIs were severed on 2026-06-19 — see `tombstones`). `attachments`: files ingested with the record.

**Other configs.** `sources` — book-length and formerly binary-only works recovered to text (All That Lies Within Me, 234k words; New Human; Cleis; the Logos papers). `heteronyms` — the Dodecad and adjacent figures, with voice signatures, roles, domains. `venues`, `journal_assignments` — the archive's journals and presses and which deposit belongs to which. `reception` — the register of twenty blind machine referee reports on one Aristotle sentence (#1574). `captures` — reception captures from the Capture Registry (how machine surfaces received the archive). `citations` — the full internal edge list. `lexicon` — the lexical minting registry. `predictions` — every falsification condition stated in a deposit, with resolutions. `studies` — the designed/conducted study dashboard. `tombstones` — the 1,136-row Zenodo kill ledger of 2026-06-19. `blog_posts` — the index of the authorial blog surface with AXN crosswalk. `sites` — one row per page of the public fleet of sites that surface the archive.

**Identifiers and citation.** Cite a deposit by its AXN and number: *Sharks, L. (2026). Title. Crimson Hexagonal Archive #N, AXN:hex.FAMILY. https://alexanarch.org/s/records/N/*. The node declaration is at `https://alexanarch.org/.well-known/axn-node.json`; the AXN resolver at `https://alexanarch.org/s/axn/<hex>/`.

**Provenance.** Archive founded 2026-06-19 after the termination of its Zenodo account. Nothing in this dataset has been edited for the dataset; retractions, nulls, superseded versions and withdrawn records are present with their status. Built {built}.

**License.** CC BY 4.0 for all text.
"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='hf-dataset'); ap.add_argument('--fleet', default=os.environ.get('FLEET_DIR'))
    a = ap.parse_args(); out = ROOT/a.out; out.mkdir(exist_ok=True)
    frames = {'deposits': deposits(), 'sources': sources(), 'heteronyms': heteronyms(), 'venues': venues(), 'journal_assignments': journal_assignments(), 'reception': reception(), 'captures': captures(), 'citations': citations(), 'entities': entities(), 'lexicon': lexicon(), 'predictions': predictions(), 'studies': studies(), 'tombstones': tombstones(), 'blog_posts': blog_posts()}
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
    (out/'README.md').write_text(CARD.format(configs='\n'.join(cfg), n_dep=len(frames['deposits']), built=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%MZ')))
    print('card written')

if __name__ == '__main__': main()
