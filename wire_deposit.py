#!/usr/bin/env python3
"""Wire deposit reading results into all data structures and regenerate static page."""

import json, html as htmlmod, re, os, sys

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


def regenerate_static_page(d, eidx):
    """Regenerate the static HTML page for a deposit with full enrichment."""
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
    fulltext = ''
    for path in [f'data/deposits/AXN-{hex_id}.md', f'data/texts/AXN-{hex_id}-text.md']:
        if os.path.exists(path):
            with open(path) as f:
                raw = f.read()
            if len(raw) > 200:
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
                break
    
    if not fulltext:
        fulltext = f'<p>{esc(d.get("description", ""))}</p>'
    
    # Keywords
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
    
    # Build page
    page = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(d["title"])} — Alexanarch</title><meta name="description" content="{esc(d.get('description','')[:160])}"><script type="application/ld+json">{jsonld}</script>
<style>@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap");:root{{--bg:#fafafa;--fg:#1a1a1a;--accent:#1a3a5c;--accent2:#c23b22;--dim:#777;--teal:#0a7c6a;--border:#e0e0e0;--surface:#fff;--sans:"IBM Plex Sans",sans-serif;--mono:"IBM Plex Mono",monospace}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:var(--sans);background:var(--bg);color:var(--fg);line-height:1.8;font-size:15px}}.wrap{{max-width:720px;margin:0 auto;padding:60px 24px}}a{{color:var(--accent);text-decoration:none}}a:hover{{color:var(--accent2)}}h1{{font-size:1.3em;font-weight:600;color:var(--accent);margin-bottom:8px}}h2{{font-size:1em;font-weight:500;color:var(--accent);margin-top:20px;margin-bottom:6px;border-bottom:1px solid var(--border);padding-bottom:3px}}p{{margin-bottom:10px;color:#333}}.nav{{display:flex;gap:12px;margin-bottom:24px;font-size:.85em;overflow-x:auto;white-space:nowrap}}.nav a{{color:#777;font-weight:500;text-decoration:none}}.nav a:hover{{color:var(--accent)}}.ft{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:20px;max-height:600px;overflow-y:auto;font-size:.88em;line-height:1.75;margin:8px 0;color:#333}}.ft h1,.ft h2,.ft h3{{color:var(--accent);margin:12px 0 6px}}.ft h1{{font-size:1.1em}}.ft h2{{font-size:1em;border-bottom:none}}.ft h3{{font-size:.95em}}.ft strong{{color:var(--fg)}}.ft blockquote{{border-left:3px solid var(--teal);padding-left:12px;color:#555;margin:8px 0}}.ft hr{{border:none;border-top:1px solid var(--border);margin:12px 0}}.footer{{margin-top:40px;padding-top:12px;border-top:1px solid var(--border);font-size:.75em;color:var(--dim)}}</style>
</head><body><div class="wrap">
<nav class="nav"><a href="/">Alexanarch</a> <a href="/s/browse/">Browse</a> <a href="/s/wiki/">Wiki</a> <a href="/s/graph/">Graph</a> <a href="/observatory/">Observatory</a> <a href="/deposit/">Deposit</a> <a href="/guide/">Guide</a> <a href="/manifest/">Manifest</a></nav>
<div style="font-family:var(--mono);font-size:1.1em;color:var(--teal);background:var(--surface);padding:12px;border-radius:6px;border-left:4px solid var(--teal);margin:12px 0">{esc(d["axn"])}</div>
<h1>{esc(d["title"])}</h1>
<div style="font-size:.85em;color:#777;margin-bottom:10px">{esc(d["creator"])} · {esc(d["date"])} · {esc(d.get("content_type",""))}</div>
<a style="display:inline-block;background:var(--teal);color:#fff;padding:6px 14px;border-radius:4px;font-size:.82em;text-decoration:none;margin:6px 0" href="/data/deposits/AXN-{hex_id}.md" download>↓ Download MD</a>
<div style="margin:8px 0">{kw_html}</div>
<h2>Description</h2>
<p style="font-size:.9em">{esc(d.get("description",""))}</p>
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
