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
    return pd.DataFrame(rows)

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

CARD = """---
license: cc-by-4.0
pretty_name: Crimson Hexagonal Archive (Alexanarch)
language: [en, el]
size_categories: [1K<n<10K]
tags: [scholarship, provenance, heteronymy, reception, aristotle, plato, poetry, archive, ai-mediated-authorship, content-addressed-identifiers]
configs:
{configs}
---
# The Crimson Hexagonal Archive

The complete corpus of the Crimson Hexagonal Archive (alexanarch.org) — {n_dep} content-addressed scholarly deposits by Lee Sharks and the twelve heteronyms of the Dodecad, with their canonical texts, wiki entries, citation graph, lexical registry, reception captures, and the recovered book-length sources — projected from the archive's single source of truth (`data/` in `leesharks000/alexanarch`) and rebuilt on every mint.

Every row carries its AXN identifier (a content-derived identifier: the sha256 of the canonical text is the record), its substrate disclosure (which of these texts were made in dialogue with language models, and how), its license, and its status in the archive's supersession chain. Nothing here has been edited for this dataset; the retractions, nulls, and superseded versions are present as such.

**Configs.** `deposits` — one row per deposit, full text. `sources` — book-length and formerly docx-only works recovered to text (All That Lies Within Me, 234k words; New Human; Cleis; the Logos papers). `reception` — the register of twenty blind machine referee reports on one Aristotle sentence (#1574, "The Particle"). `captures` — reception captures from the Capture Registry. `citations` — internal citation edges. `lexicon` — the lexical minting registry of the archive's coinages. `sites` — one row per page of the public fleet of sites that surface the archive (godkinggoogle.com, semanticeconomy.org, machinemediation.org, operativesemiotics.org, revelationfirst.com, and the rest).

**Provenance.** Archive founded 2026-06-19 after the termination of its Zenodo account; every deposit is served at `https://alexanarch.org/s/records/{{deposit_number}}/` and resolvable by AXN at `/s/axn/{{hex}}/`. Node declaration: `https://alexanarch.org/.well-known/axn-node.json`. Built {built}.

**License.** CC BY 4.0 for all text. Attribution: Lee Sharks, Crimson Hexagonal Archive, with the AXN of the deposit.
"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='hf-dataset'); ap.add_argument('--fleet', default=os.environ.get('FLEET_DIR'))
    a = ap.parse_args(); out = ROOT/a.out; out.mkdir(exist_ok=True)
    frames = {'deposits': deposits(), 'sources': sources(), 'reception': reception(), 'captures': captures(), 'citations': citations(), 'lexicon': lexicon()}
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
