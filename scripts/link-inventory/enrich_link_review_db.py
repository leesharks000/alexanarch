#!/usr/bin/env python3
"""enrich_link_review_db.py — enrich each link with resolver lookup and
mismatch analysis. Writes verdict column.

Verdict values:
  no_id                   — no DOI/AXN found in text or href; not a citation link
  consistent              — DOI in text matches DOI in href
  href_wrong_target       — DOI in text is fine but href points at wrong record
  href_disagrees_text     — DOI in text is different from DOI in href
  likely_prose_mismatch   — prose describes work X, but the linked DOI resolves to a
                             very different work; a better alt record exists in registry
  ambiguous               — prose weakly matches resolver title; no clear better alt
  ok                      — prose matches resolver title
  external_ok             — link is to an external/non-network resource, no mismatch to check
"""
import json, sqlite3, re
from pathlib import Path

DB = Path('/tmp/linkscan/links_review.db')
ALEX = Path('/home/claude/alexanarch')

# Load resolver state
api_map = json.load(open(ALEX / 'api' / 'doi-axn-map.json'))['map']
idx = json.load(open(ALEX / 'data' / 'doi-resolution-index.json'))['mappings']
reg = json.load(open(ALEX / 'data' / 'registry.json'))['deposits']
resolver_by_doi = {m['dead_doi']: m for m in idx}
record_by_num = {d['deposit_number']: d for d in reg}

# Precompute registry token sets for alt search
STOP = set(('the a an of and or to for on in by with from as is are at it its this that '
            'into through under over toward v v1 v2 v3 v4 vol volume ea axn cha nh os '
            'doi zenodo crimson hexagon hexagonal archive').split())
def tok(s):
    return set(re.findall(r'[a-z0-9]+', (s or '').lower())) - STOP
def jacc(a, b):
    return len(a & b) / max(1, len(a | b)) if a and b else 0.0

registry_index = [(d['deposit_number'], d.get('title','') or '', tok(d.get('title','') or ''))
                  for d in reg]

def resolver_lookup(doi):
    """Return (target_url, resolver_title, record_num, mapping_type, actual_record_title)."""
    if not doi: return (None, None, None, None, None)
    entry = api_map.get(doi)
    m = resolver_by_doi.get(doi, {})
    resolver_title = m.get('title')
    mapping_type = m.get('mapping_type')
    target = entry[1] if entry else None
    rec_num = None
    actual_rec_title = None
    if target and '/s/records/' in target:
        n = re.search(r'/s/records/(\d+)/', target)
        if n:
            rec_num = int(n.group(1))
            actual_rec_title = record_by_num.get(rec_num, {}).get('title', '')
    return (target, resolver_title, rec_num, mapping_type, actual_rec_title)

def best_alt(prose_tokens, exclude_rec):
    if not prose_tokens: return (None, None, 0.0)
    best = (None, None, 0.0)
    for n, title, tset in registry_index:
        if n == exclude_rec: continue
        j = jacc(prose_tokens, tset)
        if j > best[2]:
            best = (n, title, round(j, 3))
    return best

conn = sqlite3.connect(DB)
cur = conn.cursor()
sel = conn.cursor()

BATCH_SIZE = 2000
updates = []
processed = 0

for row in sel.execute('''
    SELECT id, anchor_text, href, context_before, context_after, context_prose,
           doi_in_text, doi_in_href, doi_in_context, href_record_num
    FROM links
'''):
    (row_id, anchor, href, cb, ca, prose,
     doi_text, doi_href, doi_ctx, href_rec) = row

    # Pick the DOI to resolve
    resolver_doi = doi_text or doi_href or doi_ctx
    resolver_target = resolver_title = resolver_record = mapping_type = actual_rec_title = None
    if resolver_doi:
        (resolver_target, resolver_title, resolver_record,
         mapping_type, actual_rec_title) = resolver_lookup(resolver_doi)

    # Compute jaccard: prose+anchor vs the actual target record title (better) or resolver title
    combined_prose = ' '.join(filter(None, [anchor, cb, ca, prose]))
    prose_tokens = tok(combined_prose)
    title_to_compare = actual_rec_title or resolver_title or ''
    resolver_tokens = tok(title_to_compare)
    j_prose_resolver = round(jacc(prose_tokens, resolver_tokens), 3) if resolver_tokens else None

    # Best alt record
    alt_rec = alt_title = None
    alt_j = 0.0
    if prose_tokens and resolver_record:
        alt_rec, alt_title, alt_j = best_alt(prose_tokens, resolver_record)
        if alt_title:
            alt_title = alt_title[:100]

    # Verdict logic
    verdict = 'unknown'
    confidence = 'low'
    if not resolver_doi:
        # Might still be an AXN or network link
        # If href points at an alexanarch record and anchor text matches → ok
        if href and 'alexanarch.org' in href:
            verdict = 'external_ok' if not href_rec else 'consistent'
        elif href and any(x in href.lower() for x in ('doi.org','zenodo.org')):
            verdict = 'external_ok'
        else:
            verdict = 'no_id'
        confidence = 'high'
    else:
        # We have a DOI. Compare all three
        if doi_text and doi_href and doi_text != doi_href:
            verdict = 'href_disagrees_text'
            confidence = 'high'
        elif href_rec is not None and resolver_record is not None and href_rec != resolver_record and href_rec != 0:
            # Current href points at a record; resolver says a different record. Only flag as
            # href_wrong_target if there's a clear better mapping
            if href_rec == 0:
                verdict = 'href_wrong_target'
                confidence = 'high'
            else:
                verdict = 'href_disagrees_resolver'
                confidence = 'medium'
        elif href_rec == 0:
            verdict = 'href_wrong_target'  # sentinel
            confidence = 'high'
        elif j_prose_resolver is not None and j_prose_resolver < 0.15 and alt_j is not None and alt_j >= 0.4:
            verdict = 'likely_prose_mismatch'
            confidence = 'high'
        elif j_prose_resolver is not None and j_prose_resolver < 0.25:
            verdict = 'ambiguous'
            confidence = 'medium'
        elif j_prose_resolver is not None and j_prose_resolver >= 0.4:
            verdict = 'ok'
            confidence = 'high'
        elif resolver_target:
            verdict = 'consistent'
            confidence = 'medium'

    updates.append((
        resolver_doi, resolver_target, (resolver_title or '')[:200] if resolver_title else None,
        resolver_record, mapping_type,
        j_prose_resolver, alt_rec, alt_title, alt_j,
        verdict, confidence,
        row_id
    ))
    if len(updates) >= BATCH_SIZE:
        cur.executemany('''
            UPDATE links SET resolver_doi=?, resolver_target=?, resolver_title=?,
                             resolver_record=?, resolver_mapping_type=?,
                             prose_vs_resolver_jaccard=?, best_alt_record=?,
                             best_alt_title=?, best_alt_jaccard=?,
                             verdict=?, verdict_confidence=?
            WHERE id=?
        ''', updates)
        conn.commit()
        processed += len(updates)
        updates.clear()
        if processed % 20000 == 0:
            print(f'  enriched {processed:,}...')

if updates:
    cur.executemany('''
        UPDATE links SET resolver_doi=?, resolver_target=?, resolver_title=?,
                         resolver_record=?, resolver_mapping_type=?,
                         prose_vs_resolver_jaccard=?, best_alt_record=?,
                         best_alt_title=?, best_alt_jaccard=?,
                         verdict=?, verdict_confidence=?
        WHERE id=?
    ''', updates)
    conn.commit()
    processed += len(updates)

print(f'\nenriched {processed:,} links')

# Summary
print('\n=== verdict distribution ===')
for verdict, n in cur.execute('SELECT verdict, COUNT(*) FROM links GROUP BY verdict ORDER BY COUNT(*) DESC').fetchall():
    print(f'  {verdict:30}  {n:>7,}')

print('\n=== mismatch counts by repo (top 20) ===')
for repo, n in cur.execute('''
    SELECT repo, COUNT(*) FROM links
    WHERE verdict IN ('likely_prose_mismatch','href_wrong_target','href_disagrees_resolver','href_disagrees_text')
    GROUP BY repo ORDER BY COUNT(*) DESC LIMIT 20
''').fetchall():
    print(f'  {n:>6}  {repo}')
