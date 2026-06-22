#!/usr/bin/env python3
"""
Alexanarch Data Consolidation Pipeline
═══════════════════════════════════════
Enriches the existing 866 deposits so that citations, entities,
and wiki articles form a richly interlinked knowledge structure.

Phases:
  A. Entity normalization — strip metadata noise, build canonical index
  B. Citation resolution — map dead Zenodo DOIs to live AXN locations
  C. Concept extraction — extract minted terms from full text (pilot)
  D. Cross-reference generation — entity-index, citation-graph, concept-map

Usage:
  python consolidate.py --phase A      # Entity normalization only
  python consolidate.py --phase B      # Citation resolution only
  python consolidate.py --phase C      # Concept extraction (pilot batch)
  python consolidate.py --phase all    # Everything
  python consolidate.py --report       # Status report, no changes
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent
NOW = datetime.now(timezone.utc).isoformat()

# ══════════════════════════════════════════════════════════════
# PHASE A: Entity Normalization
# ══════════════════════════════════════════════════════════════

# Predicates that are work-level metadata, not concept-level knowledge.
# These duplicate information already in the registry record.
METADATA_PREDICATES = {
    'belongs_to_family', 'created_by', 'is_part_of', 'is_type', 'engages',
}

# Predicates that define concepts — the high-value triples
DEFINITION_PREDICATES = {
    'defined_in', 'defines', 'proposed_in', 'proposes', 'invented_by',
}

# Predicates that relate concepts to each other
RELATION_PREDICATES = {
    'extends', 'extended_by', 'critiques', 'critiqued_in',
    'enables', 'addresses', 'affects', 'applies_to', 'applied_to',
    'references', 'referenced_in', 'cites', 'documents', 'documented_in',
    'uses', 'maps', 'repairs', 'removes_public_access_to',
    'is_instance_of', 'may_exhibit', 'accepts', 'accepted_by',
    'denied_by', 'measured_by', 'operates', 'produced',
    'governs', 'governed_by', 'cross_links', 'engages',
    'should_resolve',
}


def normalize_entity_name(name):
    """Normalize an entity name for canonical matching."""
    s = name.strip()
    # Remove leading/trailing quotes
    s = s.strip('"\'')
    # Collapse whitespace
    s = re.sub(r'\s+', ' ', s)
    return s


def canonical_key(name):
    """Generate a lowercase canonical key for deduplication."""
    s = normalize_entity_name(name)
    # Remove leading articles for matching purposes
    s = re.sub(r'^(the|a|an)\s+', '', s, flags=re.IGNORECASE)
    return s.lower().strip()


def is_cha_concept(subject, predicate, entity_type):
    """
    Determine if an entity triple represents a CHA-minted concept
    vs. metadata noise vs. generic reference.

    CHA concepts are: multi-word terms, defined/proposed within the archive,
    typed as 'concept' or 'method', or appearing with definition predicates.
    """
    subj_lower = subject.lower().strip()

    # Definitely a concept if it uses a definition predicate
    if predicate in DEFINITION_PREDICATES:
        return True

    # Typed as concept or method
    if entity_type in ('concept', 'method'):
        return True

    # Multi-word, capitalized, not a generic phrase
    words = subject.split()
    if len(words) >= 2 and not subj_lower.startswith(('the ', 'a ')):
        # Filter out work titles that got captured as entities
        if predicate in METADATA_PREDICATES:
            return False
        return True

    # Single-word terms that are clearly conceptual
    concept_singles = {
        'spxi', 'tachyon', 'obelus', 'alexanarch', 'heteronym',
        'dodecad', 'manus', 'logos',
    }
    if subj_lower in concept_singles:
        return True

    return False


def phase_a_normalize(registry):
    """
    Phase A: Normalize entities across all deposits.

    1. Separate concept triples from metadata noise
    2. Normalize entity names
    3. Build canonical entity index
    4. Return enriched deposits and entity index
    """
    deposits = registry['deposits']
    entity_index = {}  # canonical_key → entity record
    deposit_updates = {}  # deposit_number → updated entities list

    concept_count = 0
    metadata_count = 0
    noise_count = 0

    for d in deposits:
        dn = d.get('deposit_number', '')
        axn = d.get('axn', '')
        entities = d.get('entities', [])

        concepts = []  # concept-level triples to keep
        metadata = []  # metadata triples to separate

        for e in entities:
            if not isinstance(e, dict):
                continue

            subj = e.get('subject', '')
            pred = e.get('predicate', '')
            obj = e.get('object', '')
            etype = e.get('type', '')
            evidence = e.get('evidence_status', '')
            note = e.get('note', '')

            if not subj:
                noise_count += 1
                continue

            # Classify
            if pred in METADATA_PREDICATES:
                metadata_count += 1
                metadata.append(e)
                continue

            # Normalize
            norm_subj = normalize_entity_name(subj)
            ckey = canonical_key(subj)

            # Build or update canonical entity record
            if ckey not in entity_index:
                entity_index[ckey] = {
                    'canonical_name': norm_subj,
                    'canonical_key': ckey,
                    'display_names': set(),
                    'defined_in': [],       # AXNs where this concept is defined
                    'referenced_in': [],    # AXNs where this concept appears
                    'predicates': set(),
                    'type': etype or 'concept',
                    'evidence_status': evidence,
                    'wikidata_qid': None,
                    'triples': [],
                    'related_concepts': set(),
                }

            rec = entity_index[ckey]
            rec['display_names'].add(subj)
            rec['predicates'].add(pred)

            if pred in DEFINITION_PREDICATES:
                if axn and axn not in rec['defined_in']:
                    rec['defined_in'].append(axn)
            else:
                if axn and axn not in rec['referenced_in']:
                    rec['referenced_in'].append(axn)

            # Track concept-to-concept relationships
            obj_ckey = canonical_key(obj) if obj else ''
            if obj_ckey and not obj.startswith('AXN:'):
                rec['related_concepts'].add(obj_ckey)

            # Store the triple with normalized names
            rec['triples'].append({
                'subject': norm_subj,
                'predicate': pred,
                'object': obj,
                'source_axn': axn,
                'source_deposit': dn,
                'type': etype,
                'evidence_status': evidence,
            })

            concept_count += 1
            concepts.append({
                'subject': norm_subj,
                'predicate': pred,
                'object': obj,
                'type': etype,
                'evidence_status': evidence,
                'canonical_key': ckey,
                'note': note,
            })

        deposit_updates[dn] = concepts

    # Serialize sets for JSON
    for ckey, rec in entity_index.items():
        rec['display_names'] = sorted(rec['display_names'])
        rec['predicates'] = sorted(rec['predicates'])
        rec['related_concepts'] = sorted(rec['related_concepts'])
        rec['total_deposits'] = len(set(rec['defined_in'] + rec['referenced_in']))

    print(f"  Phase A: {concept_count} concept triples kept, "
          f"{metadata_count} metadata triples separated, "
          f"{noise_count} noise filtered")
    print(f"  Canonical entities: {len(entity_index)}")

    # Identify high-value CHA-minted concepts
    minted = {k: v for k, v in entity_index.items()
              if v['defined_in'] or v['total_deposits'] >= 2
              or any(p in DEFINITION_PREDICATES for p in v['predicates'])}
    print(f"  CHA-minted concepts (defined or cross-deposit): {len(minted)}")

    return entity_index, deposit_updates


# ══════════════════════════════════════════════════════════════
# PHASE B: Citation Resolution
# ══════════════════════════════════════════════════════════════

def load_doi_index():
    """Load the DOI Resolution Index."""
    path = REPO_ROOT / 'data' / 'doi-resolution-index.json'
    if not path.exists():
        print("  WARN: DOI Resolution Index not found", file=sys.stderr)
        return {}
    with open(path) as f:
        idx = json.load(f)

    # Build DOI → mapping lookup
    lookup = {}
    for m in idx.get('mappings', []):
        doi = m.get('dead_doi', '')
        if doi:
            lookup[doi] = m
    return lookup


def phase_b_citations(registry, doi_lookup):
    """
    Phase B: Resolve citations.

    1. For each citation with a Zenodo DOI, look up the DOI Resolution Index
    2. Add resolved_axn, resolved_url, is_internal fields
    3. Build deposit-to-deposit citation edges
    """
    deposits = registry['deposits']

    # Build title→AXN lookup for internal matching
    title_to_axn = {}
    axn_to_dn = {}
    for d in deposits:
        t = (d.get('title') or '').strip().lower()
        axn = d.get('axn', '')
        dn = d.get('deposit_number', '')
        if t and axn:
            title_to_axn[t] = axn
        if axn:
            axn_to_dn[axn] = dn

    citation_graph = []  # (source_dn, target_dn, target_axn, via)
    resolved_count = 0
    unresolved_count = 0
    internal_count = 0
    deposits_enriched = 0

    for d in deposits:
        dn = d.get('deposit_number', '')
        axn = d.get('axn', '')
        citations = d.get('citations', [])
        if not isinstance(citations, list) or not citations:
            continue

        enriched = False
        for c in citations:
            if not isinstance(c, dict):
                continue

            cdoi = c.get('doi', '')
            ctitle = (c.get('title') or '').strip().lower()

            # Try DOI resolution
            if cdoi:
                bare = cdoi.replace('https://doi.org/', '').replace('http://doi.org/', '')
                mapping = doi_lookup.get(bare)
                if mapping:
                    c['resolved_axn'] = mapping.get('axn', '')
                    c['resolved_url'] = mapping.get('alexanarch_url', '')
                    if not c['resolved_url']:
                        # Fall back to blog URL
                        live = mapping.get('live_urls', {})
                        c['resolved_url'] = live.get('blog', live.get('registry', ''))
                    c['is_internal'] = bool(c['resolved_axn'])
                    resolved_count += 1
                    enriched = True

                    # Build citation graph edge
                    if c['resolved_axn']:
                        target_dn = axn_to_dn.get(c['resolved_axn'], '')
                        if target_dn:
                            citation_graph.append({
                                'source_deposit': dn,
                                'source_axn': axn,
                                'target_deposit': target_dn,
                                'target_axn': c['resolved_axn'],
                                'via': 'doi_resolution',
                                'doi': cdoi,
                            })
                            internal_count += 1
                else:
                    unresolved_count += 1

            # Try title matching for non-DOI citations
            elif ctitle and ctitle in title_to_axn:
                c['resolved_axn'] = title_to_axn[ctitle]
                c['is_internal'] = True
                resolved_count += 1
                enriched = True
                target_dn = axn_to_dn.get(c['resolved_axn'], '')
                if target_dn:
                    citation_graph.append({
                        'source_deposit': dn,
                        'source_axn': axn,
                        'target_deposit': target_dn,
                        'target_axn': c['resolved_axn'],
                        'via': 'title_match',
                    })
                    internal_count += 1

        if enriched:
            deposits_enriched += 1

    print(f"  Phase B: {resolved_count} citations resolved, "
          f"{unresolved_count} unresolved, "
          f"{internal_count} internal edges")
    print(f"  Deposits with enriched citations: {deposits_enriched}")

    return citation_graph


# ══════════════════════════════════════════════════════════════
# PHASE C: Concept Extraction from Full Text
# ══════════════════════════════════════════════════════════════

def extract_concepts_from_text(text, deposit_axn, deposit_num):
    """
    Extract CHA-minted concepts from a deposit's full text.

    CHA concepts are low-frequency, long-tail semantic addresses:
    multi-word terms naming unique conceptual distinctions.

    Patterns:
    1. Bold + em-dash definition: **Term** — definition text
       Including enumerated: (N) the **Term** — definition
    2. Bold terms with evidence tags: **Term** ... [Observed]
    3. SPXI-style definitions: Term: a/the description
    4. Recurring capitalized multi-word phrases (3+ uses, unique to CHA)

    Filters OUT: work titles, heteronym names, person names, generic terms
    """
    concepts = []
    seen = set()

    # Known heteronym/person names to exclude
    person_names = {
        'lee sharks', 'johannes sigil', 'rex fraction', 'ayanna vox',
        'rev. ayanna vox', 'rebekah cranes', 'orin trace', 'dr. orin trace',
        'nobel glas', 'talos morrow', 'damascus dancings', 'sparrow wells',
        'sen kuro', 'yusef kenning', 'ichabod spellings', 'jack feist',
        'mary lee', 'rhys owens', 'alice thornburgh', 'florian morin',
        'john guzlowski', 'zenodotus of ephesus', 'fernando pessoa',
    }

    # Generic terms to exclude
    generic_terms = {
        'creative commons', 'united states', 'new york', 'june 2026',
        'march 2026', 'primary datasets', 'observed fact', 'structural condition',
        'unproven proposition', 'evidence legend', 'critical editions',
    }

    def should_exclude(term):
        t = term.lower().strip()
        if t in person_names or t in generic_terms:
            return True
        if len(t) < 4:
            return True
        # Exclude pure dates, versions
        if re.match(r'^(v\d|january|february|march|april|may|june|july|august|september|october|november|december)\b', t, re.I):
            return True
        return False

    # 1. Bold + em-dash definitions (the primary CHA pattern)
    #    Handles: **Term** — definition
    #    Also: (N) the **Term** — definition
    #    Also: **Term**: definition
    bold_defs = re.findall(
        r'(?:\(\d+\)\s+(?:the\s+)?)?'           # optional (N) the
        r'\*\*([^*]{2,60})\*\*'                   # bold term
        r'\s*[-—:]+\s*'                           # separator
        r'([^.;]{10,300}[.;])',                   # definition up to period/semicolon
        text
    )
    for term, definition in bold_defs:
        term = term.strip().rstrip(':')
        if should_exclude(term):
            continue
        ckey = canonical_key(term)
        if ckey not in seen and len(term.split()) >= 2:
            seen.add(ckey)
            concepts.append({
                'subject': normalize_entity_name(term),
                'predicate': 'defined_in',
                'object': deposit_axn,
                'type': 'concept',
                'evidence_status': 'observed',
                'canonical_key': ckey,
                'definition': definition.strip()[:200],
                'extraction_method': 'bold_definition',
            })

    # 2. Standalone bold terms (concepts emphasized but not defined with em-dash)
    #    Must be 2+ words and not already captured
    standalone_bold = re.findall(r'\*\*([^*]{3,60})\*\*', text)
    bold_counts = Counter(normalize_entity_name(b) for b in standalone_bold)
    for term, count in bold_counts.items():
        if should_exclude(term):
            continue
        ckey = canonical_key(term)
        if ckey not in seen and len(term.split()) >= 2 and count >= 1:
            # Only include if used as a concept (not a heading or label)
            # Check if it appears in conceptual context
            pattern = re.escape(f'**{term}**')
            contexts = re.findall(f'.{{0,40}}{pattern}.{{0,80}}', text)
            is_concept = any(
                re.search(r'(define|introduce|propose|term|concept|call|name)', ctx, re.I)
                or '—' in ctx or ':' in ctx
                for ctx in contexts
            )
            if is_concept or count >= 3:
                seen.add(ckey)
                concepts.append({
                    'subject': normalize_entity_name(term),
                    'predicate': 'referenced_in',
                    'object': deposit_axn,
                    'type': 'concept',
                    'evidence_status': 'inferred',
                    'canonical_key': ckey,
                    'extraction_method': 'bold_emphasis',
                    'occurrences': count,
                })

    # 3. SPXI/formal definitions: **Term (Acronym):** definition
    formal_defs = re.findall(
        r'\*\*([^*]{3,80})\*\*\s*[:]\s*'
        r'([A-Za-z][^.]{10,300}\.)',
        text
    )
    for term, definition in formal_defs:
        term = term.strip()
        if should_exclude(term):
            continue
        ckey = canonical_key(term)
        if ckey not in seen and len(term.split()) >= 2:
            seen.add(ckey)
            concepts.append({
                'subject': normalize_entity_name(term),
                'predicate': 'defined_in',
                'object': deposit_axn,
                'type': 'concept',
                'evidence_status': 'observed',
                'canonical_key': ckey,
                'definition': definition.strip()[:200],
                'extraction_method': 'formal_definition',
            })

    # 4. Recurring capitalized multi-word phrases (3+ occurrences)
    #    These are CHA terms used throughout but perhaps never bold-defined
    cap_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b', text)
    phrase_counts = Counter(cap_phrases)
    for phrase, count in phrase_counts.items():
        if count >= 3:
            ckey = canonical_key(phrase)
            if ckey not in seen and not should_exclude(phrase) and len(phrase.split()) >= 2:
                seen.add(ckey)
                concepts.append({
                    'subject': normalize_entity_name(phrase),
                    'predicate': 'referenced_in',
                    'object': deposit_axn,
                    'type': 'concept',
                    'evidence_status': 'inferred',
                    'canonical_key': ckey,
                    'extraction_method': 'recurring_phrase',
                    'occurrences': count,
                })

    return concepts


def phase_c_extract(registry, entity_index, pilot_deposits=None):
    """
    Phase C: Extract concepts from full text.

    If pilot_deposits is None, processes all deposits with full text.
    Otherwise, processes only the specified deposit numbers.
    """
    deposits = registry['deposits']
    texts_dir = REPO_ROOT / 'data' / 'texts'
    deposits_dir = REPO_ROOT / 'data' / 'deposits'

    new_concepts = 0
    deposits_processed = 0

    for d in deposits:
        dn = d.get('deposit_number', '')
        axn = d.get('axn', '')
        hex_id = d.get('hex', '')

        if pilot_deposits and dn not in pilot_deposits:
            continue

        # Find full text
        text = None
        # Try deposits dir first (richest)
        dep_path = deposits_dir / f'AXN-{str(hex_id).zfill(4)}.md'
        if dep_path.exists():
            with open(dep_path) as f:
                text = f.read()
        else:
            # Try texts dir
            txt_path = texts_dir / f'AXN-{str(hex_id).zfill(4)}-text.md'
            if txt_path.exists():
                with open(txt_path) as f:
                    text = f.read()

        if not text or len(text) < 200:
            continue

        deposits_processed += 1
        concepts = extract_concepts_from_text(text, axn, dn)

        for c in concepts:
            ckey = c['canonical_key']
            if ckey not in entity_index:
                entity_index[ckey] = {
                    'canonical_name': c['subject'],
                    'canonical_key': ckey,
                    'display_names': [],
                    'defined_in': [],
                    'referenced_in': [],
                    'predicates': [],
                    'type': c.get('type', 'concept'),
                    'evidence_status': c.get('evidence_status', ''),
                    'wikidata_qid': None,
                    'triples': [],
                    'related_concepts': [],
                    'total_deposits': 0,
                }

            rec = entity_index[ckey]

            # Add to appropriate list
            if c['predicate'] in DEFINITION_PREDICATES:
                if axn not in rec.get('defined_in', []):
                    rec.setdefault('defined_in', []).append(axn)
            else:
                if axn not in rec.get('referenced_in', []):
                    rec.setdefault('referenced_in', []).append(axn)

            if c['subject'] not in rec.get('display_names', []):
                if isinstance(rec.get('display_names'), set):
                    rec['display_names'].add(c['subject'])
                else:
                    rec.setdefault('display_names', []).append(c['subject'])

            if c['predicate'] not in rec.get('predicates', []):
                if isinstance(rec.get('predicates'), set):
                    rec['predicates'].add(c['predicate'])
                else:
                    rec.setdefault('predicates', []).append(c['predicate'])

            # Store definition if found
            if c.get('definition'):
                rec['definition'] = c['definition']

            # Store the triple
            rec.setdefault('triples', []).append({
                'subject': c['subject'],
                'predicate': c['predicate'],
                'object': c['object'],
                'source_axn': axn,
                'source_deposit': dn,
                'type': c.get('type', ''),
                'evidence_status': c.get('evidence_status', ''),
                'extraction_method': c.get('extraction_method', ''),
            })

            new_concepts += 1

    # Update total_deposits counts
    for ckey, rec in entity_index.items():
        defined = rec.get('defined_in', [])
        referenced = rec.get('referenced_in', [])
        rec['total_deposits'] = len(set(defined + referenced))

    print(f"  Phase C: {new_concepts} new concept triples from {deposits_processed} deposits")

    return entity_index


# ══════════════════════════════════════════════════════════════
# PHASE D: Cross-Reference Generation
# ══════════════════════════════════════════════════════════════

def phase_d_generate(entity_index, citation_graph, registry):
    """
    Phase D: Generate cross-reference indices.

    Writes:
    - data/entity-index.json — canonical concept registry
    - data/citation-graph.json — deposit-to-deposit citation edges
    - data/concept-map.json — concept bridging structure
    """
    output_dir = REPO_ROOT / 'data'

    # 1. Entity Index
    # Sort by total_deposits descending, then by name
    sorted_entities = sorted(
        entity_index.values(),
        key=lambda x: (-x.get('total_deposits', 0), x.get('canonical_name', ''))
    )

    # Filter to entities that are genuinely interesting
    # (defined somewhere, or appear in 2+ deposits, or have definitions)
    # EXCLUDE: heteronym names, work titles, noise terms
    exclude_keys = {
        'johannes sigil', 'rex fraction', 'talos morrow', 'rebekah cranes',
        'ayanna vox', 'rev. ayanna vox', 'nobel glas', 'orin trace',
        'dr. orin trace', 'damascus dancings', 'sparrow wells', 'sen kuro',
        'yusef kenning', 'ichabod spellings', 'jack feist', 'lee sharks',
        'mary lee', 'tl;dr', 'title', 'crimson hexagon',
        'crimson hexagonal archive', 'hexagonal archive',
        'id', 'florian morin', 'zenodo',
    }

    # Also exclude entities whose canonical name matches a deposit title
    deposit_titles = set()
    for d in registry.get('deposits', []):
        t = (d.get('title') or '').strip()
        if t:
            deposit_titles.add(canonical_key(t))
            # Also add first-40-char prefix for long titles
            if len(t) > 40:
                deposit_titles.add(canonical_key(t[:40]))

    # Exclude AXN identifiers used as entity subjects
    axn_pattern = re.compile(r'^axn:', re.I)

    significant = [
        e for e in sorted_entities
        if (e.get('defined_in')
            or e.get('total_deposits', 0) >= 2
            or e.get('definition'))
        and e.get('canonical_key', '') not in exclude_keys
        and e.get('canonical_key', '') not in deposit_titles
        and not axn_pattern.match(e.get('canonical_key', ''))
    ]

    ei_output = {
        '@context': 'https://schema.org',
        '@type': 'DefinedTermSet',
        'name': 'Crimson Hexagonal Archive — Canonical Concept Index',
        'description': (
            'Registry of minted terms and concepts from the CHA: '
            'low-frequency, long-tail semantic addresses that name '
            'unique conceptual distinctions. Each entry tracks where '
            'the concept is defined, where it is referenced, and how '
            'it relates to other concepts in the archive.'
        ),
        'publisher': {
            '@type': 'Organization',
            'name': 'Alexanarch',
            'url': 'https://alexanarch.org'
        },
        'dateModified': NOW[:10],
        'total_concepts': len(significant),
        'total_with_definitions': sum(1 for e in significant if e.get('definition')),
        'total_cross_deposit': sum(1 for e in significant if e.get('total_deposits', 0) >= 2),
        'concepts': significant,
    }

    with open(output_dir / 'entity-index.json', 'w') as f:
        json.dump(ei_output, f, indent=2, ensure_ascii=False, default=list)
    print(f"  → data/entity-index.json: {len(significant)} significant concepts")

    # 2. Citation Graph
    # Build cited_by reverse index
    cited_by = defaultdict(list)
    for edge in citation_graph:
        cited_by[edge['target_deposit']].append({
            'citing_deposit': edge['source_deposit'],
            'citing_axn': edge['source_axn'],
            'via': edge['via'],
        })

    cg_output = {
        '@context': 'https://schema.org',
        '@type': 'Dataset',
        'name': 'CHA Internal Citation Graph',
        'description': (
            'Deposit-to-deposit citation edges within the Crimson Hexagonal Archive. '
            'Built by resolving dead Zenodo DOIs through the DOI Resolution Index '
            'and matching citation titles to deposit titles.'
        ),
        'dateModified': NOW[:10],
        'total_edges': len(citation_graph),
        'total_deposits_citing': len(set(e['source_deposit'] for e in citation_graph)),
        'total_deposits_cited': len(cited_by),
        'edges': citation_graph,
        'cited_by': {str(k): v for k, v in cited_by.items()},
    }

    with open(output_dir / 'citation-graph.json', 'w') as f:
        json.dump(cg_output, f, indent=2, ensure_ascii=False)
    print(f"  → data/citation-graph.json: {len(citation_graph)} edges, "
          f"{len(cited_by)} deposits cited")

    # 3. Concept Map — which concepts bridge which deposits
    concept_bridges = []
    for ckey, rec in entity_index.items():
        all_deposits = list(set(
            rec.get('defined_in', []) + rec.get('referenced_in', [])
        ))
        if len(all_deposits) >= 2:
            concept_bridges.append({
                'concept': rec.get('canonical_name', ckey),
                'canonical_key': ckey,
                'defined_in': rec.get('defined_in', []),
                'referenced_in': rec.get('referenced_in', []),
                'total_deposits': len(all_deposits),
                'related_concepts': rec.get('related_concepts', []),
                'definition': rec.get('definition', ''),
            })

    concept_bridges.sort(key=lambda x: -x['total_deposits'])

    cm_output = {
        '@context': 'https://schema.org',
        '@type': 'Dataset',
        'name': 'CHA Concept Map',
        'description': (
            'Concepts that bridge multiple deposits in the Crimson Hexagonal Archive. '
            'Each entry shows where a concept is defined and where it is referenced, '
            'making the thematic structure of the archive navigable.'
        ),
        'dateModified': NOW[:10],
        'total_bridging_concepts': len(concept_bridges),
        'bridges': concept_bridges,
    }

    with open(output_dir / 'concept-map.json', 'w') as f:
        json.dump(cm_output, f, indent=2, ensure_ascii=False, default=list)
    print(f"  → data/concept-map.json: {len(concept_bridges)} bridging concepts")


# ══════════════════════════════════════════════════════════════
# STATUS REPORT
# ══════════════════════════════════════════════════════════════

def status_report(registry):
    """Print a status report of current data interlinking."""
    deposits = registry['deposits']

    # Citations
    with_cit = sum(1 for d in deposits if d.get('citations') and isinstance(d.get('citations'), list) and d['citations'])
    total_cit = sum(len(d.get('citations', [])) for d in deposits if isinstance(d.get('citations'), list))
    resolved = sum(1 for d in deposits for c in d.get('citations', [])
                   if isinstance(c, dict) and c.get('resolved_axn'))

    # Entities
    total_ent = sum(len(d.get('entities', [])) for d in deposits)
    concept_ent = sum(1 for d in deposits for e in d.get('entities', [])
                      if isinstance(e, dict) and e.get('predicate') not in METADATA_PREDICATES)
    with_canonical = sum(1 for d in deposits for e in d.get('entities', [])
                         if isinstance(e, dict) and e.get('canonical_key'))

    # Wiki
    with_wiki = sum(1 for d in deposits if d.get('wiki_article') and len(str(d.get('wiki_article', ''))) > 50)

    # Cross-reference files
    ei_exists = (REPO_ROOT / 'data' / 'entity-index.json').exists()
    cg_exists = (REPO_ROOT / 'data' / 'citation-graph.json').exists()
    cm_exists = (REPO_ROOT / 'data' / 'concept-map.json').exists()

    print("═══════════════════════════════════════════════")
    print("  Alexanarch Data Consolidation — Status Report")
    print("═══════════════════════════════════════════════")
    print(f"\n  Deposits: {len(deposits)}")
    print(f"\n  Citations:")
    print(f"    Deposits with citations: {with_cit}/{len(deposits)}")
    print(f"    Total citation entries: {total_cit}")
    print(f"    Resolved to AXN: {resolved}")
    print(f"\n  Entities:")
    print(f"    Total triples: {total_ent}")
    print(f"    Concept triples (non-metadata): {concept_ent}")
    print(f"    With canonical key: {with_canonical}")
    print(f"\n  Wiki articles: {with_wiki}/{len(deposits)}")
    print(f"\n  Cross-reference indices:")
    print(f"    entity-index.json: {'✓' if ei_exists else '✗'}")
    print(f"    citation-graph.json: {'✓' if cg_exists else '✗'}")
    print(f"    concept-map.json: {'✓' if cm_exists else '✗'}")
    print()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Alexanarch Data Consolidation")
    parser.add_argument('--phase', type=str, default='all',
                        choices=['A', 'B', 'C', 'all'],
                        help='Which phase to run')
    parser.add_argument('--report', action='store_true',
                        help='Print status report only')
    parser.add_argument('--pilot', type=int, nargs='*',
                        help='Deposit numbers for Phase C pilot (default: first 50)')
    parser.add_argument('--save-registry', action='store_true',
                        help='Write enriched citations back to registry.json')
    args = parser.parse_args()

    # Load registry
    with open(REPO_ROOT / 'data' / 'registry.json') as f:
        registry = json.load(f)

    if args.report:
        status_report(registry)
        return

    print("═══════════════════════════════════════════════")
    print("  Alexanarch Data Consolidation Pipeline")
    print(f"  {NOW}")
    print("═══════════════════════════════════════════════")

    entity_index = {}
    citation_graph = []

    # Phase A
    if args.phase in ('A', 'all'):
        print("\n[A] Entity normalization...")
        entity_index, deposit_updates = phase_a_normalize(registry)

    # Phase B
    if args.phase in ('B', 'all'):
        print("\n[B] Citation resolution...")
        doi_lookup = load_doi_index()
        citation_graph = phase_b_citations(registry, doi_lookup)

        if args.save_registry:
            # Write back enriched citations
            with open(REPO_ROOT / 'data' / 'registry.json', 'w') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)
            print("  → Updated registry.json with resolved citations")

    # Phase C
    if args.phase in ('C', 'all'):
        print("\n[C] Concept extraction from full text...")
        if args.pilot is not None:
            pilot = args.pilot if args.pilot else list(range(1, 51))
        else:
            pilot = list(range(1, 51))  # Default: first 50 deposits
        print(f"  Pilot batch: deposits {min(pilot)}-{max(pilot)}")
        entity_index = phase_c_extract(registry, entity_index, set(pilot))

    # Phase D (always runs if any phase ran)
    if entity_index or citation_graph:
        print("\n[D] Generating cross-reference indices...")
        phase_d_generate(entity_index, citation_graph, registry)

    print("\n═══════════════════════════════════════════════")
    print("  ∮ = 1")
    print("═══════════════════════════════════════════════")


if __name__ == '__main__':
    main()
