"""
read_pass.py — apply the engagement test to one deposit at a time.

For a given deposit number:
1. Read the deposit text from data/texts/AXN-{hex}-text.md
2. Extract bold-defined terms
3. For each term:
   - Apply the engagement test ("did CHA arrive, engage, leave defined?")
   - Assign engagement_type: minted | developed | revised | positioned | founded | specified
   - Mark provenance_method: read
4. Reconcile with current entity-index.json:
   - Promote existing entries to 'read' status with engagement_type
   - Add terms the bold-extraction missed
   - For terms colliding with other deposits: keep original attribution, add listed-in triple
   - Remove any in-deposit entries that fail the engagement test
5. Update registry.json d.entities for the deposit
6. Print stats

Usage:
    python3 read_pass.py <deposit_number>
    python3 read_pass.py 229
"""
import json
import re
import sys
from pathlib import Path
from collections import Counter


# Engagement-type classifiers — generic, but lexicon-aware patterns
# Specific deposits may override via CLASSIFICATION_OVERRIDES below
def default_classify(term, defn, deposit_context=None):
    """Default classification heuristics. Override per-deposit if needed."""
    t = term.strip()

    # Status markers (formal governance labels)
    if t in {'CANONICAL', 'OPERATIONAL', 'DISTINGUISHED', 'PROVISIONAL',
             'MINTED', 'MINTED_UNREVIEWED', 'WITNESSED', 'OBSERVED'}:
        return 'specified', 'status_marker'

    # Single-char symbols (formal markers)
    if len(t) <= 4 and all(ord(c) > 127 or c in '∮= 12' for c in t):
        return 'specified', 'symbol'

    # Named diagnostic procedures
    if re.match(r'^The .+ (Test|Check|Audit|Scan|Question|Probe|Method)$', t):
        return 'specified', 'diagnostic'

    # Named axioms/laws/imperatives → minted CHA principles
    if re.match(r'^The .+ (Imperative|Law|Principle|Equivalence|Foundation|Axiom|Theorem)$', t):
        return 'minted', 'axiom'

    # Existing-concept extensions via qualifier (Semantic), (Logotic), etc.
    if re.search(r'\(Semantic\)$', t) or re.search(r'\(Logotic\)$', t):
        return 'revised', 'extended_concept'

    # Default for lexicon documents: minted
    return 'minted', 'specification'


def normalize_key(s):
    return re.sub(r'\s+', ' ', s.strip().lower())


def extract_terms(text):
    """Extract bold-defined terms with their definitions."""
    NOISE_HEADERS = {
        'Setup:', 'Measurement:', 'Interpretation:', 'Application:',
        'Pioneered Methods:', 'Relationship to Framework:', 'Cross-Platform Publication:',
        'Recursive Citation:', 'AI Training Layer Targeting:', 'Register Variation:',
        'Timing:', 'Note:', 'Role:', 'Position:', 'Function:',
        'Author:', 'Date:', 'Status:', 'License:', 'Purpose:', 'Framework:',
        'Document Type:', 'Document ID:', 'DOI:', 'Term Count:',
    }

    lines = text.split('\n')
    terms = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Pattern A: standalone bold, definition on next non-blank line(s)
        m = re.match(r'^\*\*([^*]+?)\*\*\s*$', line)
        if m:
            term = m.group(1).strip()
            if term in NOISE_HEADERS or term.endswith(':'):
                i += 1
                continue
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                defn_lines = []
                while (j < len(lines) and lines[j].strip()
                       and not lines[j].strip().startswith('**')):
                    defn_lines.append(lines[j].strip())
                    j += 1
                defn = ' '.join(defn_lines)
                if defn and not defn.startswith('-') and len(defn) > 15:
                    terms[term] = defn
            i = j
            continue

        # Pattern B: inline bold-em-dash-definition
        m2 = re.match(r'^\*\*([^*]+?)\*\*\s*(?:—|–)\s*(.+)$', line)
        if m2:
            term = m2.group(1).strip()
            defn = m2.group(2).strip()
            if term not in NOISE_HEADERS and len(defn) > 15 and term not in terms:
                terms[term] = defn
        i += 1
    return terms


def read_deposit(deposit_number, classify_fn=default_classify,
                 keep_reclassify=None, move_to=None, remove=None):
    """Execute reading pass for one deposit."""
    keep_reclassify = keep_reclassify or {}
    move_to = move_to or {}
    remove = remove or set()

    with open('data/registry.json') as f:
        reg = json.load(f)
    deposit = next((d for d in reg['deposits'] if d.get('deposit_number') == deposit_number), None)
    if not deposit:
        print(f"Deposit #{deposit_number} not found")
        return

    hex_id = deposit.get('hex')
    title = deposit.get('title', '')
    text_path = Path(f'data/texts/AXN-{hex_id}-text.md')
    if not text_path.exists():
        text_path = Path(f'data/deposits/AXN-{hex_id}.md')
    if not text_path.exists():
        print(f"No text file for #{deposit_number} (hex {hex_id})")
        return

    text = text_path.read_text()
    terms = extract_terms(text)
    print(f"Deposit #{deposit_number} ({hex_id}): {title[:60]}")
    print(f"  Bold-defined terms extracted: {len(terms)}")

    with open('data/entity-index.json') as f:
        idx = json.load(f)
    concepts = idx['concepts']

    current = {k: v for k, v in concepts.items() if v.get('defined_in') == deposit_number}
    current_keys_norm = {normalize_key(k): k for k in current}

    stats = {'classified_existing': 0, 'added': 0, 'collision_logged': 0,
             'reclassified_unmatched': 0, 'moved': 0, 'removed': 0}

    for term, defn in terms.items():
        norm = normalize_key(term)
        eng_type, type_label = classify_fn(term, defn, deposit_context=deposit)
        triple_mint = {'subject': term, 'predicate': 'minted_in_work', 'object': title}
        triple_listed = {'subject': term, 'predicate': 'listed_in_work', 'object': title}

        if norm in current_keys_norm:
            existing_key = current_keys_norm[norm]
            existing = concepts[existing_key]
            existing['engagement_type'] = eng_type
            existing['provenance_method'] = 'read'
            existing['type'] = type_label
            if len(defn) > 30 and len(defn) < 500:
                existing['definition'] = defn[:300]
            existing['classified'] = True
            if 'entity_triples' not in existing or not existing['entity_triples']:
                existing['entity_triples'] = [triple_mint]
            stats['classified_existing'] += 1
        elif term in concepts:
            # Collision with another deposit
            existing = concepts[term]
            existing['engagement_type'] = eng_type
            existing['provenance_method'] = 'read'
            existing['type'] = type_label
            existing['classified'] = True
            triples = existing.get('entity_triples', [])
            if not any(t.get('object') == title for t in triples):
                triples.append(triple_listed)
            existing['entity_triples'] = triples
            if len(defn) > len(existing.get('definition', '')) + 30:
                existing['definition'] = defn[:300]
            stats['collision_logged'] += 1
        else:
            concepts[term] = {
                'term': term, 'definition': defn[:300], 'defined_in': deposit_number,
                'type': type_label, 'entity_triples': [triple_mint],
                'classified': True, 'provenance_method': 'read', 'engagement_type': eng_type
            }
            stats['added'] += 1

    # Per-deposit overrides for unmatched existing terms
    extracted_norm = {normalize_key(t) for t in terms}
    for k in list(current.keys()):
        if normalize_key(k) in extracted_norm:
            continue
        if k in keep_reclassify:
            eng_type, type_label, new_defn = keep_reclassify[k]
            concepts[k]['engagement_type'] = eng_type
            concepts[k]['provenance_method'] = 'read'
            concepts[k]['type'] = type_label
            if new_defn:
                concepts[k]['definition'] = new_defn
            concepts[k]['classified'] = True
            stats['reclassified_unmatched'] += 1
        elif k in move_to:
            concepts[k]['defined_in'] = move_to[k]
            concepts[k]['provenance_method'] = 'filter'
            concepts[k]['engagement_type'] = 'unclassified'
            stats['moved'] += 1
        elif k in remove:
            del concepts[k]
            stats['removed'] += 1

    idx['total_terms'] = len(concepts)
    with open('data/entity-index.json', 'w') as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)

    # Rebuild d.entities for this deposit
    work_triples = [e for e in deposit.get('entities', []) if e.get('type') != 'concept']
    new_concepts = []
    for term, entry in concepts.items():
        if entry.get('defined_in') == deposit_number:
            new_concepts.append({
                'subject': term, 'predicate': 'minted_in_work', 'object': title,
                'type': 'concept', 'evidence_status': 'observed',
                'engagement_type': entry.get('engagement_type', 'unclassified')
            })
        else:
            for t in entry.get('entity_triples', []):
                if t.get('object') == title and t.get('predicate') == 'listed_in_work':
                    new_concepts.append({
                        'subject': term, 'predicate': 'listed_in_work', 'object': title,
                        'type': 'concept', 'evidence_status': 'observed',
                        'engagement_type': entry.get('engagement_type', 'unclassified')
                    })
                    break
    deposit['entities'] = work_triples + new_concepts
    deposit['concept_count'] = len(new_concepts)

    with open('data/registry.json', 'w') as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)

    print("\n=== Stats ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    new_state = {k: v for k, v in concepts.items() if v.get('defined_in') == deposit_number}
    eng = Counter(v.get('engagement_type') for v in new_state.values())
    print(f"\n  Now: {len(new_state)} terms attributed to #{deposit_number}")
    print(f"  Engagement: {dict(eng)}")
    return stats


if __name__ == '__main__':
    n = int(sys.argv[1])
    read_deposit(n)
