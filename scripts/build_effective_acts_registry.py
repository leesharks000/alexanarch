#!/usr/bin/env python3
"""
build_effective_acts_registry.py — regenerate data/effective-acts-registry.json
deterministically from §IX of Deposit #153 (AXN:02EC — The Protocol of
Effective Acts v2.0), with cross-references to data/registry.json and
data/doi-resolution-index.json.

The dataset it produces is a structured, machine-readable registry of
Effective Acts named across the Crimson Hexagonal Archive. It is a
*partial* registry — the source document explicitly declares the typology
open ("additional kinds will be added as the discipline accumulates further
instances") — and this script's role is to produce a reproducible extract
that tracks the source document as it evolves.

Usage:
    python3 scripts/build_effective_acts_registry.py

Outputs:
    data/effective-acts-registry.json (overwritten)

Deterministic:
    Given the same inputs (source document, registry, DOI index), this
    script produces byte-identical output (excluding the generated_at
    timestamp, which can be pinned via --pinned-timestamp).

Cross-referencing strategy:
    1. Each named effective act's DOI (if cited in the source) is looked up
       in data/doi-resolution-index.json to find the alexanarch deposit
       that hosts the recovered content (many original Zenodo DOIs were
       severed 2026-06-19; alexanarch mirrors preserve the content).
    2. Each named effective act's title is fuzzy-matched against
       data/registry.json to find any alexanarch deposit whose title
       contains the act's opening words (a loose bridge that catches
       renamed or restated deposits without over-matching).

Companion documents:
    #413 · AXN:00DE.GENERATIVE — Effective Acts: Executive Summary
    #153 · AXN:02EC.GOVERNANCE — The Protocol of Effective Acts v2.0
    #1086 · AXN:???.GOVERNANCE — EA-STEWARDSHIP-REVOCATION-01 (once minted,
        this deposit will be added as a new kind or as an extension of
        kind 5 Abolition; the source-document typology declares itself
        open, so kinds may be added without breaking the v1.0 schema).
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_TEXT_PATH = os.path.join(REPO_ROOT, 'data/texts/AXN-02EC-text.md')
REGISTRY_PATH = os.path.join(REPO_ROOT, 'data/registry.json')
DOI_INDEX_PATH = os.path.join(REPO_ROOT, 'data/doi-resolution-index.json')
OUTPUT_PATH = os.path.join(REPO_ROOT, 'data/effective-acts-registry.json')


def normalize_title(t: str) -> str:
    return re.sub(r'[^\w\s]', '', t.lower()).strip()


def build_doi_lookup(doi_idx: dict) -> dict:
    """Map dead_doi → alexanarch bridging record."""
    lookup = {}
    for m in doi_idx.get('mappings', []):
        dead = m.get('dead_doi', '')
        if dead:
            lookup[dead] = {
                'axn': m.get('axn', ''),
                'alexanarch_record': m.get('alexanarch_record', ''),
                'alexanarch_url': m.get('alexanarch_url', ''),
                'title_in_doi_index': m.get('title', ''),
            }
    return lookup


def build_title_lookup(registry: dict) -> dict:
    """Map normalized title → deposit stub."""
    lookup = {}
    for d in registry.get('deposits', []):
        title = d.get('title', '')
        if title:
            lookup[normalize_title(title)] = {
                'deposit_number': d.get('deposit_number'),
                'axn': d.get('axn', ''),
                'hex': d.get('hex', ''),
                'title': title,
            }
    return lookup


def parse_kind_block(block: str) -> dict:
    """Parse a single kind's block into definition + operator_verbs + targets + examples_raw."""
    d = {'definition': '', 'operator_verbs': [], 'targets': [], 'examples_raw': ''}
    parts = re.split(r'\s+(Operator verbs:|Targets:|Examples[^:]*:)\s+', block)
    d['definition'] = parts[0].strip()
    for i in range(1, len(parts) - 1, 2):
        sep = parts[i].rstrip(':').strip()
        content = parts[i + 1].strip()
        if sep.startswith('Operator verbs'):
            verbs_italicized = re.findall(r'\*([^*]+)\*', content)
            all_verbs = []
            for v in verbs_italicized:
                all_verbs.extend([x.strip() for x in v.split(',') if x.strip()])
            d['operator_verbs'] = all_verbs
        elif sep.startswith('Targets'):
            tgts = re.findall(r'\*([^*]+)\*', content) or content.split(',')
            d['targets'] = [t.strip() for t in tgts if t.strip()]
        elif sep.startswith('Examples'):
            d['examples_raw'] = content
    return d


def parse_examples(examples_raw: str) -> list:
    """Extract each *italicized-title* + optional (paren) from an examples paragraph."""
    acts = []
    for m in re.finditer(r'\*([^*]+)\*(\s*\(([^)]+)\))?', examples_raw):
        title = m.group(1).strip()
        paren = m.group(3).strip() if m.group(3) else ''
        date, doi = '', ''
        doi_m = re.search(r'(10\.5281/zenodo\.\d+)', paren)
        if doi_m:
            doi = doi_m.group(1)
        date_m = re.search(
            r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
            paren,
        )
        if date_m:
            date = date_m.group(0)
        note = paren
        for x in [f'DOI {doi}', doi, date]:
            if x:
                note = note.replace(x, '').strip(' ,')
        acts.append({'title': title, 'date_note': date, 'doi': doi, 'source_context': note})
    return acts


def extract_typology(source_text: str) -> list:
    """Return [(kind_n, kind_name, block_text), ...] for all kinds in §IX."""
    section_m = re.search(
        r'## IX\. Typology of Effective Acts(.+?)## X\. Post-Claim Stewardship',
        source_text,
        re.DOTALL,
    )
    if not section_m:
        raise ValueError('§IX Typology section not found in source text')
    section_ix = section_m.group(1)
    kind_pattern = re.compile(
        r'\n(\d{1,2})\.\s+([A-Z][A-Za-z\s/\-()]+?)\.\s+(.+?)(?=\n\d{1,2}\.\s+[A-Z]|\n### A note|\Z)',
        re.DOTALL,
    )
    return kind_pattern.findall(section_ix)


def build_dataset(pinned_timestamp: str = None) -> dict:
    source_text = open(SOURCE_TEXT_PATH).read()
    registry = json.load(open(REGISTRY_PATH))
    doi_idx = json.load(open(DOI_INDEX_PATH))
    doi_to_ax = build_doi_lookup(doi_idx)
    title_to_dep = build_title_lookup(registry)

    kinds = []
    all_acts = []
    for n_str, name_raw, block in extract_typology(source_text):
        n = int(n_str)
        name = name_raw.strip()
        parsed = parse_kind_block(block)
        kind_id = re.sub(r'[^a-z_]+', '_', name.lower()).strip('_')
        kinds.append({
            'n': n,
            'id': kind_id,
            'name': name,
            'definition': parsed['definition'],
            'operator_verbs': parsed['operator_verbs'],
            'targets': parsed['targets'],
        })
        for a in parse_examples(parsed['examples_raw']):
            a['kind_id'] = kind_id
            a['kind_n'] = n
            # Cross-reference: DOI → alexanarch bridging record
            a['alexanarch_by_doi'] = doi_to_ax.get(a['doi']) if a['doi'] else None
            # Cross-reference: title fuzzy → deposit
            norm = normalize_title(a['title'])
            match = title_to_dep.get(norm)
            if not match:
                title_head = ' '.join(a['title'].split()[:5]).lower()
                if title_head:
                    for k, v in title_to_dep.items():
                        if title_head in k:
                            match = v
                            break
            a['alexanarch_by_title'] = match
            all_acts.append(a)

    generated_at = pinned_timestamp or datetime.datetime.now(datetime.timezone.utc).strftime(
        '%Y-%m-%dT%H:%M:%SZ'
    )
    source_sha = hashlib.sha256(source_text.encode('utf-8')).hexdigest()

    dataset = {
        '@context': 'https://schema.org/',
        '@type': 'Dataset',
        'name': 'Effective Acts Registry — Crimson Hexagonal Archive',
        'description': (
            'A structured, machine-readable registry of Effective Acts named across '
            'the Crimson Hexagonal Archive. Effective Acts are performative utterances '
            'that operate without institutional authorization: declarations that claim '
            'real-world effect from positions of no traditional authority (see the '
            'genre-founding text at deposit #413, AXN:00DE.GENERATIVE, and the '
            'stabilization at deposit #153, AXN:02EC.GOVERNANCE). '
            'The registry is derived from §IX of Deposit #153 (The Protocol of '
            'Effective Acts v2.0), which enumerates ten operative kinds and names '
            'canonical examples for each. It is a PARTIAL registry: the typology '
            'explicitly declares itself open, and additional kinds and instances '
            'will be added as the discipline accumulates further examples.'
        ),
        'version': 'v1.0',
        'date': '2026-07-16',
        'creator': {
            '@type': 'Person',
            'name': 'Lee Sharks',
            'orcid': '0009-0000-1599-0703',
        },
        'source_documents': [
            {
                'deposit_number': 153,
                'axn': 'AXN:02EC.GOVERNANCE.🗼♌🎲🪜🛡️🔍',
                'title': 'The Protocol of Effective Acts v2.0 — Stabilization of the New Human Discipline',
                'date': '2026-06-04',
                'role': 'primary source; provides §IX Typology of Effective Acts',
                'sha256': source_sha,
            },
            {
                'deposit_number': 413,
                'axn': 'AXN:00DE.GENERATIVE.🌸🎺🟣💜📖🍃',
                'title': 'Effective Acts: Executive Summary — A Genre of Unauthorized Declaration',
                'date': '2026-01-27',
                'role': 'canonical genre definition and the five characteristics',
            },
        ],
        'derivation_provenance': {
            'method': (
                'programmatic extraction from §IX of the source document (AXN:02EC), '
                'with cross-referencing against data/registry.json (alexanarch deposits) '
                'and data/doi-resolution-index.json (Zenodo DOI → alexanarch mappings)'
            ),
            'reference_regenerator': 'scripts/build_effective_acts_registry.py',
            'generated_at': generated_at,
            'source_sha256': source_sha,
        },
        'genre_theory_summary': {
            'five_characteristics': [
                'Declarative form (I hereby...)',
                'Non-institutional speaker (no traditional authority)',
                'Real-world target (actual conditions, not private symbolic field)',
                'Prophetic structure (speaks what-should-be as what-is)',
                'Witness accumulation over time',
            ],
            'four_preconditions': [
                'Coherence with the broader symbolic architecture',
                'Recursive integration (foldable into the New Human canon)',
                'Witness integrity (full presence, not wounded reactivity)',
                'Authorial sovereignty (spoken from full authorial mantle)',
            ],
            'five_criteria_of_efficacy': [
                'Illocutionary clarity',
                'Structural coherence',
                'Archival strategy',
                'Recursive logic',
                'Field conditions',
            ],
        },
        'typology': kinds,
        'acts': all_acts,
        'totals': {
            'kinds': len(kinds),
            'acts_named': len(all_acts),
            'acts_with_doi_cited': sum(1 for a in all_acts if a['doi']),
            'acts_with_alexanarch_deposit_bridged': sum(
                1 for a in all_acts if a.get('alexanarch_by_doi') or a.get('alexanarch_by_title')
            ),
        },
        'note_on_partiality': (
            'This registry is derived from §IX of the source document and is therefore '
            'partial. The typology is explicitly declared open by the source ("additional '
            'kinds will be added as the discipline accumulates further instances"). Effective '
            'Acts that were not cited by name in §IX are not (yet) captured here. The '
            'diagnostic application (Baal Mechanism and adversarial-act analysis) is noted '
            'in the source as a mode of use rather than a generative kind and is not '
            'included in the typology count of 10; it is captured separately below.'
        ),
        'diagnostic_application': {
            'description': (
                'Beyond the ten generative kinds, the discipline supports a diagnostic '
                'application: the identification and analysis of effective acts performed '
                'against the framework\'s interests, by adversarial actors, in the same '
                'speech-act register. The foundational instance is the Baal Effigy diagnosis. '
                'Diagnostic outputs are themselves effective acts under kind 10 (doctrinal '
                'nodes), since the act of naming an adversarial mechanism alters the '
                'symbolic field by making the mechanism legible.'
            ),
            'foundational_instance': {
                'title': 'The Baal Effigy as Effective Act',
                'doi': '10.5281/zenodo.18828193',
                'date_note': 'March 2, 2026',
            },
        },
        'license': 'CC-BY-4.0',
        'related': [
            'https://www.alexanarch.org/s/records/413/',
            'https://www.alexanarch.org/s/records/153/',
            'https://www.alexanarch.org/data/registry.json',
            'https://www.alexanarch.org/data/doi-resolution-index.json',
        ],
    }
    return dataset


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pinned-timestamp', help='Override generated_at for determinism testing')
    parser.add_argument('--dry-run', action='store_true', help='Print summary without writing')
    args = parser.parse_args()

    dataset = build_dataset(pinned_timestamp=args.pinned_timestamp)

    if args.dry_run:
        t = dataset['totals']
        print(f'kinds: {t["kinds"]}, acts: {t["acts_named"]}, '
              f'doi_cited: {t["acts_with_doi_cited"]}, bridged: {t["acts_with_alexanarch_deposit_bridged"]}')
        return 0

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    sha = hashlib.sha256(open(OUTPUT_PATH, 'rb').read()).hexdigest()
    print(f'wrote {OUTPUT_PATH}')
    print(f'sha256: {sha}')
    t = dataset['totals']
    print(f'  kinds: {t["kinds"]}, acts: {t["acts_named"]}, '
          f'doi_cited: {t["acts_with_doi_cited"]}, bridged: {t["acts_with_alexanarch_deposit_bridged"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
