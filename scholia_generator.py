#!/usr/bin/env python3
"""
scholia_generator.py — generate autonomous-document versions of CHA deposits.

For a given deposit number, produces an autonomous markdown document with:
  1. YAML front-matter (machine-readable schema declaration)
  2. The original prose body (unmodified)
  3. Closing scholia (prose-formatted self-contained lexicon)

Output: data/autonomous/AXN-{hex}-autonomous.md

Per the layered model in WORKPLAN-SESSION-20260622.md:
  Layer 1: front-matter — generated from entity-index + semantic-addresses + registry
  Layer 2: inline markers — NOT generated; manual at composition for new deposits
  Layer 3: closing scholia — generated from front-matter, prose-formatted

The autonomous doc carries its own schema. A fresh AI thread fed only this file
has the full context: what was minted/founded/engaged, what addresses were claimed,
what reception data exists, what DOIs to cite.

Usage:
    python3 scholia_generator.py <deposit_number>
    python3 scholia_generator.py 870 229 1   # multiple

Idempotent: re-running regenerates the autonomous doc from current JSON state.
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone


def load_data():
    """Load the three canonical data sources."""
    with open('data/entity-index.json') as f:
        idx = json.load(f)
    with open('data/semantic-addresses.json') as f:
        sa = json.load(f)
    with open('data/registry.json') as f:
        reg = json.load(f)
    return idx, sa, reg


def find_deposit(reg, deposit_number):
    """Return the deposit record for a given number, or None."""
    for d in reg.get('deposits', []):
        if d.get('deposit_number') == deposit_number:
            return d
    return None


def find_prose_text(deposit):
    """Locate the canonical prose text for a deposit."""
    hex_id = deposit.get('hex')
    candidates = [
        Path(f'data/texts/AXN-{hex_id}-text.md'),
        Path(f'data/deposits/AXN-{hex_id}.md'),
    ]
    if deposit.get('full_text_path'):
        candidates.insert(0, Path(deposit['full_text_path'].lstrip('/')))
    for p in candidates:
        if p.exists():
            return p, p.read_text(encoding='utf-8', errors='replace')
    return None, None


def collect_minted_concepts(idx, deposit_number):
    """Return concepts where defined_in == deposit_number."""
    concepts = idx['concepts']
    minted = []
    for term, attrs in concepts.items():
        if attrs.get('defined_in') == deposit_number:
            minted.append((term, attrs))
    # Sort by engagement type (minted/founded first) then alphabetically
    type_order = {'minted': 0, 'founded': 1, 'specified': 2, 'developed': 3,
                  'revised': 4, 'positioned': 5, 'unclassified': 6}
    minted.sort(key=lambda x: (type_order.get(x[1].get('engagement_type'), 99), x[0]))
    return minted


def collect_addresses_for_concepts(sa, concept_names):
    """Return addresses whose refers_to contains any of the given concepts."""
    addresses = sa.get('addresses', {})
    concept_set = set(concept_names)
    results = []
    for aid, a in addresses.items():
        if concept_set & set(a.get('refers_to', [])):
            results.append((aid, a))
    return results


def yaml_front_matter(deposit, minted, addresses_for_deposit):
    """Render YAML front-matter for the autonomous document."""
    title = deposit.get('title', '?')
    deposit_number = deposit.get('deposit_number')
    hex_id = deposit.get('hex')
    axn = deposit.get('axn')
    doi = deposit.get('doi')

    # Concept engagement summary
    engages = []
    for term, attrs in minted:
        engages.append({
            'entity': f"cha:concept:{slugify(term)}",
            'display_name': term,
            'as': attrs.get('engagement_type', 'unclassified'),
        })

    # Engaged-but-not-minted (from deposit.entities, predicate 'engaged_in_work')
    for ent in deposit.get('entities', []):
        if ent.get('predicate') == 'engaged_in_work':
            engages.append({
                'entity': f"cha:concept:{slugify(ent['subject'])}",
                'display_name': ent['subject'],
                'as': 'engaged',
            })

    # Address claims (only most-cited / observed)
    observed_addr_summary = []
    for aid, a in addresses_for_deposit:
        if a.get('observation_class') == 'observed_address':
            observed_addr_summary.append({
                'address_id': aid,
                'query': a.get('canonical_query'),
                'latest_status': a.get('latest_status'),
                'latest_date': a.get('latest_observation_date'),
                'observation_count': len(a.get('observations', [])),
            })

    # Build YAML manually for stable formatting (avoid pyyaml dep)
    lines = ['---']
    lines.append(f'node_id: cha:node:deposit:{deposit_number:04d}')
    lines.append(f'deposit_number: {deposit_number}')
    lines.append(f'hex: "{hex_id}"')
    if axn:
        lines.append(f'axn: "{axn}"')
    if doi:
        lines.append(f'doi: "{doi}"')
    lines.append(f'title: {yaml_str(title)}')
    if deposit.get('creator'):
        lines.append(f'creator: {yaml_str(deposit["creator"])}')
    if deposit.get('orcid'):
        lines.append(f'orcid: "{deposit["orcid"]}"')
    if deposit.get('date'):
        lines.append(f'date: "{deposit["date"]}"')
    if deposit.get('version'):
        lines.append(f'version: "{deposit["version"]}"')
    if deposit.get('status'):
        lines.append(f'status: {deposit["status"]}')

    if engages:
        lines.append('engages:')
        for e in engages:
            lines.append(f'  - entity: {e["entity"]}')
            lines.append(f'    display_name: {yaml_str(e["display_name"])}')
            lines.append(f'    as: {e["as"]}')

    if observed_addr_summary:
        lines.append('observed_addresses:')
        for o in observed_addr_summary:
            lines.append(f'  - address_id: {o["address_id"]}')
            lines.append(f'    query: {yaml_str(o["query"])}')
            lines.append(f'    latest_status: {o.get("latest_status") or "null"}')
            lines.append(f'    latest_date: "{o.get("latest_date") or ""}"')
            lines.append(f'    observation_count: {o["observation_count"]}')

    # Cite the canonical data sources
    lines.append('data_sources:')
    lines.append('  - data/registry.json')
    lines.append('  - data/entity-index.json')
    lines.append('  - data/semantic-addresses.json')

    # Cold-start fallback: SHA-256 hash of prose body for ephemeral node_id
    # (computed at generation time, useful when front-matter is stripped)
    lines.append(f'generated_at: "{datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"')
    lines.append('autonomous_doc_version: 1.0')
    lines.append('---')
    return '\n'.join(lines)


def yaml_str(s):
    """Wrap a string for YAML, choosing quote style safely."""
    s = str(s)
    if any(ch in s for ch in ['"', '\n', '\\', ':', '#', '[', ']', '{', '}']):
        # Use single quotes with escapes
        s_escaped = s.replace("'", "''")
        return f"'{s_escaped}'"
    return f'"{s}"'


def slugify(s):
    """Convert term to a slug for cha:concept identifiers."""
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')


def closing_scholia(deposit, minted, addresses_for_deposit):
    """Render the prose-formatted closing scholia."""
    lines = ['', '---', '', '## SCHOLIA', '']
    title = deposit.get('title', '?')
    lines.append(f'*Self-contained lexicon for: {title}*')
    lines.append('')

    # Group by engagement type
    by_type = {}
    for term, attrs in minted:
        et = attrs.get('engagement_type', 'unclassified')
        by_type.setdefault(et, []).append((term, attrs))

    type_titles = {
        'minted': 'Minted (coined from nothing in this deposit)',
        'founded': 'Founded (institutions, journals, rooms established here)',
        'specified': 'Specified (formal operators, protocols, status markers)',
        'developed': 'Developed (existing concepts built up with CHA positions)',
        'revised': 'Revised (existing concepts whose meaning was extended here)',
        'positioned': 'Positioned (existing entities placed in structural roles)',
        'unclassified': 'Other terms attributed to this deposit',
    }

    type_order = ['minted', 'founded', 'specified', 'developed', 'revised', 'positioned', 'unclassified']
    for et in type_order:
        if et not in by_type:
            continue
        items = by_type[et]
        lines.append(f'### {type_titles[et]}')
        lines.append('')
        for term, attrs in items:
            defn = (attrs.get('definition') or '').strip()
            lines.append(f'**{term}** — {defn}')
            lines.append('')

    # Address claims with observation history
    observed = [a for aid, a in addresses_for_deposit
                if a.get('observation_class') == 'observed_address']
    if observed:
        lines.append('### Observed Addresses (search queries that retrieved this deposit\'s concepts)')
        lines.append('')
        for a in observed:
            q = a.get('canonical_query')
            status = a.get('latest_status') or '?'
            date = a.get('latest_observation_date') or '?'
            n = len(a.get('observations', []))
            lines.append(f'- `{q}` — latest: {status} on {date} ({n} observation{"s" if n != 1 else ""})')
        lines.append('')

    subjunctive = [a for aid, a in addresses_for_deposit
                   if a.get('observation_class') == 'subjunctive']
    if subjunctive and len(subjunctive) <= 25:  # Don't dump 1,000+ entries
        lines.append('### Subjunctive Addresses (catalogued, not yet observed)')
        lines.append('')
        for a in subjunctive:
            q = a.get('canonical_query')
            lines.append(f'- `{q}`')
        lines.append('')
    elif subjunctive:
        lines.append(f'### Subjunctive Addresses')
        lines.append(f'')
        lines.append(f'*{len(subjunctive)} subjunctive addresses point to concepts in this deposit — see `data/semantic-addresses.json` for full list.*')
        lines.append('')

    # Citations from deposit
    if deposit.get('references') or deposit.get('citations'):
        lines.append('### Citations')
        lines.append('')
        for ref in deposit.get('references', []) or deposit.get('citations', []):
            lines.append(f'- {ref}')
        lines.append('')

    # Closing colophon
    lines.append('---')
    lines.append('')
    lines.append(f'*Generated by scholia_generator.py from canonical state at {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}*')
    lines.append('*This document is autonomous: the front-matter declares its schema, the closing scholia carries its definitions.*')
    lines.append('')
    lines.append('∮ = 1')

    return '\n'.join(lines)


def generate_autonomous_doc(deposit_number, output_dir=Path('data/autonomous')):
    """Main: generate the autonomous document for one deposit."""
    idx, sa, reg = load_data()
    deposit = find_deposit(reg, deposit_number)
    if not deposit:
        return None, f"Deposit #{deposit_number} not found in registry"

    hex_id = deposit.get('hex')
    prose_path, prose = find_prose_text(deposit)
    if not prose:
        prose = f"*Canonical prose for deposit #{deposit_number} not found locally. " \
                f"Refer to {deposit.get('full_text_path', 'archive surface')}.*"

    minted = collect_minted_concepts(idx, deposit_number)
    concept_names = [t for t, _ in minted]
    addresses_for_deposit = collect_addresses_for_concepts(sa, concept_names)

    # If prose already has its own front-matter (like the workplan), preserve it as-is
    # but still append closing scholia for the generated index.
    has_existing_frontmatter = prose.lstrip().startswith('---\n')

    if has_existing_frontmatter:
        # Keep original front-matter, just append scholia at end if not already there
        out = prose.rstrip()
        if '## SCHOLIA' not in out and '# SCHOLIA' not in out:
            out += '\n' + closing_scholia(deposit, minted, addresses_for_deposit)
    else:
        front = yaml_front_matter(deposit, minted, addresses_for_deposit)
        scholia = closing_scholia(deposit, minted, addresses_for_deposit)
        out = front + '\n\n' + prose.rstrip() + '\n' + scholia

    # Write
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f'AXN-{hex_id}-autonomous.md'
    out_path.write_text(out, encoding='utf-8')
    return out_path, None


def main(argv):
    if len(argv) < 2:
        print("Usage: python3 scholia_generator.py <deposit_number> [<deposit_number> ...]")
        return 1
    for arg in argv[1:]:
        try:
            n = int(arg)
        except ValueError:
            print(f"  SKIP (not a number): {arg}")
            continue
        out, err = generate_autonomous_doc(n)
        if err:
            print(f"  #{n}: ERROR — {err}")
        else:
            print(f"  #{n}: wrote {out} ({out.stat().st_size:,} bytes)")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
