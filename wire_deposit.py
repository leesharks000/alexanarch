#!/usr/bin/env python3
"""Wire deposit reading results into all data structures and regenerate static page."""

import json, html as htmlmod, re, os, sys

# Import canonical navbar renderer (single source of truth: data/navigation.json)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts.render_navbar import render_navbar

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


def regenerate_static_page(d, eidx, registry=None):
    """Regenerate the static HTML page for a deposit with full enrichment.

    registry: optional full registry dict. If provided, enables version-chain
    blocks (banner for superseded/draft, version history list for series).
    If None, version blocks are omitted (faster but less informative).
    """
    esc = lambda s: htmlmod.escape(str(s)) if s else ''
    dn = d['deposit_number']
    hex_id = d.get('hex', '')
    
    # JSON-LD
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "name": d['title'],
        "author": {"@type": "Person", "name": d['creator']},
        "datePublished": d['date'],
        "identifier": d['axn'],
        "description": d.get('description', '')[:300],
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "publisher": {"@type": "Organization", "name": "Alexanarch"},
        "keywords": ", ".join(d.get('keywords', [])),
    }, ensure_ascii=False)
    
    # Read full text
    # v1.1.1 fix: prefer the registry's declared full_text_path (the canonical
    # source of truth). Fall back to whichever existing file is largest, so a
    # stub alias never shadows a populated text file.
    fulltext = ''
    candidates = []
    declared = d.get('full_text_path')
    if declared:
        candidates.append(declared.lstrip('/'))
    # Also consider both conventional paths
    for p in [f'data/deposits/AXN-{hex_id}.md', f'data/texts/AXN-{hex_id}-text.md']:
        if p not in candidates:
            candidates.append(p)

    best_path = None
    best_size = 0
    for path in candidates:
        if os.path.exists(path):
            size = os.path.getsize(path)
            if size > best_size:
                best_size = size
                best_path = path

    if best_path and best_size > 200:
        # JSON source: render a dataset callout + download link, NOT inline-as-prose
        # (treating JSON as markdown turns every line into a <p>, producing
        #  unreadable multi-MB pages)
        if best_path.endswith('.json'):
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
            lines = raw.split('\n')
            ft_lines = []
            for line in lines:
                line = esc(line)
                if line.startswith('# '): ft_lines.append(f'<h1>{line[2:]}</h1>')
                elif line.startswith('## '): ft_lines.append(f'<h2>{line[3:]}</h2>')
                elif line.startswith('### '): ft_lines.append(f'<h3>{line[4:]}</h3>')
                elif line.startswith('---'): ft_lines.append('<hr>')
                elif line.startswith('| '): ft_lines.append(f'<div style="font-family:var(--mono);font-size:.8em">{line}</div>')
                elif line.startswith('&gt;'): ft_lines.append(f'<blockquote style="border-left:3px solid var(--teal);padding-left:12px;color:#555;margin:8px 0">{line[4:]}</blockquote>')
                elif line.strip():
                    line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
                    line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', line)
                    ft_lines.append(f'<p>{line}</p>')
                else: ft_lines.append('')
            fulltext = '\n'.join(ft_lines)
    
    if not fulltext:
        fulltext = f'<p>{esc(d.get("description", ""))}</p>'
    
    # Keywords
    # Version chain blocks (banner for superseded/draft, history list for series)
    version_banner = ''
    version_history = ''
    status = d.get('status', 'ACTIVE')
    version = d.get('version', '')
    series_id = d.get('version_series_id')
    superseded_by_n = d.get('superseded_by_deposit_number')
    superseded_reason = d.get('superseded_reason', '')

    if registry and status == 'SUPERSEDED' and superseded_by_n:
        by_v = ''
        for sib in registry.get('deposits', []):
            if sib.get('deposit_number') == superseded_by_n:
                by_v = sib.get('version', '')
                break
        version_banner = (
            '<div style="background:#fef3c7;border-left:4px solid #d97706;padding:12px 16px;'
            'border-radius:6px;margin:12px 0;font-size:.92em">'
            f'<div style="font-weight:600;color:#92400e;margin-bottom:4px">⚠ Superseded — this is version {esc(version)}</div>'
            f'<div style="color:#78350f">Current version: <a href="/s/records/{superseded_by_n}/" '
            f'style="color:var(--accent);font-weight:500">#{superseded_by_n} {esc(by_v)}</a></div>'
            + (f'<div style="color:#78350f;font-size:.88em;margin-top:6px">{esc(superseded_reason)}</div>' if superseded_reason else '')
            + '</div>'
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
    page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(d["title"])} — Alexanarch</title><meta name="description" content="{esc(d.get('description','')[:160])}"><script type="application/ld+json">{jsonld}</script>
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.8;font-size:15px}}.wrap{{max-width:720px;margin:0 auto;padding:60px 24px}}a{{color:var(--accent);text-decoration:none}}a:hover{{color:var(--accent2)}}h1{{font-size:1.3em;font-weight:600;color:var(--accent);margin-bottom:8px}}h2{{font-size:1em;font-weight:500;color:var(--accent);margin-top:20px;margin-bottom:6px;border-bottom:1px solid var(--border);padding-bottom:3px}}p{{margin-bottom:10px;color:#333}}.nav{{display:flex;gap:12px;margin-bottom:24px;font-size:.85em;overflow-x:auto;white-space:nowrap}}.nav a{{color:#777;font-weight:500;text-decoration:none}}.nav a:hover{{color:var(--accent)}}.ft{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:20px;max-height:600px;overflow-y:auto;font-size:.88em;line-height:1.75;margin:8px 0;color:#333}}.ft h1,.ft h2,.ft h3{{color:var(--accent);margin:12px 0 6px}}.ft h1{{font-size:1.1em}}.ft h2{{font-size:1em;border-bottom:none}}.ft h3{{font-size:.95em}}.ft strong{{color:var(--fg)}}.ft blockquote{{border-left:3px solid var(--teal);padding-left:12px;color:#555;margin:8px 0}}.ft hr{{border:none;border-top:1px solid var(--border);margin:12px 0}}.footer{{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}}</style>
</head><body><div class="wrap">
{render_navbar()}
<div style="font-family:var(--mono);font-size:1.1em;color:var(--teal);background:var(--surface);padding:12px;border-radius:6px;border-left:4px solid var(--teal);margin:12px 0">{esc(d["axn"])}</div>
{version_banner}
<h1>{esc(d["title"])}</h1>
<div style="font-size:.85em;color:#777;margin-bottom:10px">{esc(d["creator"])} · {esc(d["date"])} · {esc(d.get("content_type",""))}{f' · <span style="color:var(--accent);font-weight:500">{esc(version)}</span>' if (version and (version != 'v1.0' or series_id)) else ''}</div>
<a style="display:inline-block;background:var(--teal);color:#fff;padding:6px 14px;border-radius:4px;font-size:.82em;text-decoration:none;margin:6px 0" href="/data/deposits/AXN-{hex_id}.md" download>↓ Download MD</a>
<div style="margin:8px 0">{kw_html}</div>
<h2>Description</h2>
<p style="font-size:.9em">{esc(d.get("description",""))}</p>
{external_metadata_html}
{version_history}
{wiki_html}
{concepts_html}
{triples_html}
<h2>Full Text</h2>
<div class="ft">{fulltext}</div>
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
