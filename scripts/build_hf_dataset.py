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

def deposits():
    reg = json.load(open(ROOT/'data/registry.json'))['deposits']
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
            'license': d.get('license'), 'substrate_disclosure': d.get('substrate_disclosure'),
            'status': d.get('status'), 'superseded_by': d.get('superseded_by'),
            'version_series_id': d.get('version_series_id'),
            'wiki_article': d.get('wiki_article'),
            'related_deposits': json.dumps(d.get('related_deposits') or []),
            'defines_concepts': json.dumps(d.get('defines_concepts') or [], ensure_ascii=False),
            'record_url': f"https://alexanarch.org/s/records/{d['deposit_number']}/",
            'text': text, 'text_sha256': sha(text) if text else None, 'text_words': len(text.split()) if text else 0,
        })
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
    df['axn_uri'] = df['hex'].map(lambda h: f"https://alexanarch.org/s/axn/{h}/" if h else None)
    df['text_uri'] = df['deposit_number'].map(lambda n: next((f"https://alexanarch.org{d.get('full_text_path')}" for d in reg if d['deposit_number']==n and d.get('full_text_path')), None))
    df['doi_legacy'] = [ (d.get('doi') or d.get('zenodo_doi') or d.get('legacy_doi')) for d in reg ]
    df['attachments'] = [ json.dumps([ (a.get('url') or a.get('filename')) for a in (d.get('attachments') or []) ]) for d in reg ]
    ja = _jsonl('datasets/journals/assignments.jsonl')
    if not ja.empty and 'deposit' in ja.columns:
        df = df.merge(ja[['deposit','journal']].rename(columns={'deposit':'deposit_number','journal':'venue'}), on='deposit_number', how='left')
    return df

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

def heteronyms():   # the Dodecad and its adjacent/outside figures, with voice signatures and roles
    return _jsonl('datasets/heteronyms/heteronyms.jsonl')

def venues():       # the archive's own journals and presses (venue registry)
    v = json.load(open(ROOT/'datasets/venues/venues.json'))
    df = pd.DataFrame(v.get('journals') or [])
    for c in df.columns:
        if df[c].apply(lambda x: isinstance(x, (list, dict))).any():
            df[c] = df[c].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)
    return df

def journal_assignments():   # deposit -> venue assignment (the "where" of each deposit)
    return _jsonl('datasets/journals/assignments.jsonl')

def predictions():  # the falsification conditions extracted from every deposit, and their resolutions
    a = _jsonl('datasets/prediction-ledger/conditions.jsonl'); b = _jsonl('datasets/prediction-ledger/resolved.jsonl')
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
size_categories: [1K<n<10K]
tags: [scholarship, provenance, heteronymy, reception, aristotle, plato, poetry, archive, ai-mediated-authorship, content-addressed-identifiers, citation-graph]
configs:
{configs}
---
# The Crimson Hexagonal Archive — machine-readable representation

**What this is.** The Crimson Hexagonal Archive (alexanarch.org) is a self-governing scholarly and literary corpus by Lee Sharks and the twelve heteronyms of the Dodecad: {n_dep} deposits as of this build, each with a content-derived persistent identifier (AXN), a canonical text, a substrate disclosure, a license, and a place in a supersession chain. This dataset is a second, executable representation of that corpus: one row per record, full text as a string column, and every inter-record relation encoded as data keyed by stable identifiers, so that an agent can reconstruct a record, what it cites, what cites it, and its series neighbours from the dataset alone, without traversing the archive's web surfaces. It is rebuilt automatically from the archive's single source of truth (`data/` in `leesharks000/alexanarch`) on every new deposit.

**What a row means.** In `deposits`, a row is one deposit: `deposit_number` (integer, permanent, the archive's primary key), `axn` (the content-derived identifier, of the form `AXN:<hex>.<FAMILY>.<six glyphs>`; the sha256 of the canonical text is the record), `hex` (the four-digit position used in URIs), `title`, `creator` (the orthonym or heteronym as attributed), `date`, `family` (GENERATIVE, EMPIRICAL, GOVERNANCE, ARCHIVAL, UNCLASSIFIED), `content_type`, `description` (the abstract), `keywords`, `license`, `substrate_disclosure` (whether and how a language model participated in making the text), `status` (ACTIVE, SUPERSEDED, WITHDRAWN, …), `wiki_article` (a machine-written encyclopedia entry authored in session), `venue` (the archive's own journal the deposit belongs to), `text` (the canonical text, verbatim), `text_sha256`, `text_words`.

**Relations, as data.** `cites` and `cited_by`: JSON arrays of deposit numbers from the archive's citation graph (also `cites_axn` as identifiers). `related_deposits`: curated relations declared at deposit time. `superseded_by` / `supersedes`: the version chain. `version_series_id`, `series_previous`, `series_next`: neighbours in a declared series. `defines_concepts`: terms this deposit coins, with definitions (the same terms appear as rows in `lexicon`). `record_url`, `axn_uri`, `text_uri`: the canonical web addresses; `doi_legacy` where a pre-2026 Zenodo DOI existed (those DOIs were severed on 2026-06-19 — see `tombstones`). `attachments`: files ingested with the record.

**Other configs.** `sources` — book-length and formerly binary-only works recovered to text (All That Lies Within Me, 234k words; New Human; Cleis; the Logos papers). `heteronyms` — the Dodecad and adjacent figures, with voice signatures, roles, domains. `venues`, `journal_assignments` — the archive's journals and presses and which deposit belongs to which. `reception` — the register of twenty blind machine referee reports on one Aristotle sentence (#1574). `captures` — reception captures from the Capture Registry (how machine surfaces received the archive). `citations` — the full internal edge list. `lexicon` — the lexical minting registry. `predictions` — every falsification condition stated in a deposit, with resolutions. `studies` — the designed/conducted study dashboard. `tombstones` — the 1,136-row Zenodo kill ledger of 2026-06-19. `blog_posts` — the index of the authorial blog surface with AXN crosswalk. `sites` — one row per page of the public fleet of sites that surface the archive.

**Identifiers and citation.** Cite a deposit by its AXN and number: *Sharks, L. (2026). Title. Crimson Hexagonal Archive #N, AXN:hex.FAMILY. https://alexanarch.org/s/records/N/*. The node declaration is at `https://alexanarch.org/.well-known/axn-node.json`; the AXN resolver at `https://alexanarch.org/s/axn/<hex>/`.

**Provenance.** Archive founded 2026-06-19 after the termination of its Zenodo account. Nothing in this dataset has been edited for the dataset; retractions, nulls, superseded versions and withdrawn records are present with their status. Built {built}.

**License.** CC BY 4.0 for all text.
"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='hf-dataset'); ap.add_argument('--fleet', default=os.environ.get('FLEET_DIR'))
    a = ap.parse_args(); out = ROOT/a.out; out.mkdir(exist_ok=True)
    frames = {'deposits': deposits(), 'sources': sources(), 'heteronyms': heteronyms(), 'venues': venues(), 'journal_assignments': journal_assignments(), 'reception': reception(), 'captures': captures(), 'citations': citations(), 'lexicon': lexicon(), 'predictions': predictions(), 'studies': studies(), 'tombstones': tombstones(), 'blog_posts': blog_posts()}
    if a.fleet: frames['sites'] = sites(a.fleet)
    cfg = []
    for name, df in frames.items():
        if df is None or df.empty: print(f"  {name}: empty, skipped"); continue
        df = df.astype({c: 'string' for c in df.columns if df[c].dtype == object})
        df.to_parquet(out/f"{name}.parquet", index=False)
        cfg.append(f"- config_name: {name}\n  data_files: {name}.parquet")
        print(f"  {name}: {len(df):,} rows, {os.path.getsize(out/f'{name}.parquet')/1e6:.1f} MB")
    import datetime as dt
    (out/'README.md').write_text(CARD.format(configs='\n'.join(cfg), n_dep=len(frames['deposits']), built=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%MZ')))
    print('card written')

if __name__ == '__main__': main()
