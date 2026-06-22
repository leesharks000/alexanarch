#!/usr/bin/env python3
"""
sovereign_ingestion.py — Gemini's Sovereign Ingestion Protocol.

Stateless parser that treats source documents as database records in disguise.
Designed to run even when the global schema is broken — the only surviving truth
is the raw text in the context window.

Four phases:

  1. Cold-Start Header Intercept
     Fuzzy regex extracts YAML front-matter. Pulls node_id, status, engages.
     Missing/corrupted? Mints ephemeral node_id from SHA-256 of first 500 words.

  2. Inline Signature Extraction
     Scans body for explicit markers: [MINT:], [FOUND:], [INVOKE:], [CITE:],
     [REVISE:], [POSITION:], [SPECIFY:], [DEVELOP:].
     Each discovery → local variable binding (term, sentence context, vector).

  3. Append-Only Ledger Emission
     NEVER edits existing rows. Transforms each binding into a flat deterministic
     transaction string. Appends to data/ledger/cha.ledger as a standalone line.
     Timestamped, no nested objects — survives truncation absolutely.

  4. Fuzzy Hash Verification
     On replay, evaluates ledger bottom-up. If a node identifier is fractured,
     semantic proximity fallback routes to closest conceptual vector.

Transaction grammar (extended from Gemini's 3 to cover the engagement test):

  TX_MINT      | NODE: {nid} | ENTITY: {eid} | TERM: {t} | VECTOR: {v}
  TX_FOUND     | NODE: {nid} | INSTITUTION: {i} | VECTOR: established
  TX_DEVELOP   | NODE: {nid} | ENTITY: {eid} | VECTOR: position_built
  TX_REVISE    | NODE: {nid} | ENTITY: {eid} | VECTOR: meaning_extended | CANARY: {c}
  TX_POSITION  | NODE: {nid} | ENTITY: {eid} | VECTOR: structural_role | ROLE: {r}
  TX_SPECIFY   | NODE: {nid} | ENTITY: {eid} | VECTOR: formal_operator
  TX_INVOKE    | NODE: {nid} | ADDRESS: {q} | OBSERVED: {bool} | STATUS: {s}
  TX_OBSERVE   | NODE: {nid} | ADDRESS: {q} | DATE: {d} | STATUS: {s} | SURFACE: {sf}
  TX_CITE      | NODE: {nid} | TARGET: {doi_or_axn}
  TX_SEVER     | NODE: {nid} | TARGET: {url_or_doi} | STATUS: {http_code}
  TX_HASH      | NODE: {nid} | SHA256: {h} | LENGTH: {n}    (ephemeral-node anchor)

Usage:
  python3 sovereign_ingestion.py <file_or_glob> [<file_or_glob> ...]

  # Examples:
  python3 sovereign_ingestion.py data/autonomous/AXN-01-autonomous.md
  python3 sovereign_ingestion.py 'data/autonomous/*.md'
  python3 sovereign_ingestion.py data/texts/AXN-001E-text.md   # no front-matter → falls back to hash
"""
import hashlib
import json
import os
import re
import sys
import glob as globmod
from pathlib import Path
from datetime import datetime, timezone


LEDGER_PATH = Path('data/ledger/cha.ledger')
INLINE_MARKER_RE = re.compile(
    r'\[(MINT|FOUND|INVOKE|CITE|REVISE|POSITION|SPECIFY|DEVELOP):\s*([^\]]+)\]',
    re.IGNORECASE
)


def now_iso():
    """ISO 8601 timestamp with Z."""
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha256_prefix(text, n_words=500):
    """SHA-256 of the first n_words of prose — ephemeral node anchor."""
    words = re.findall(r'\S+', text)[:n_words]
    payload = ' '.join(words)
    return hashlib.sha256(payload.encode('utf-8', errors='replace')).hexdigest()


# -------------------------- Phase 1: Cold-Start Header Intercept --------------------------

def extract_front_matter(text):
    """
    Fuzzy YAML front-matter extraction. Tolerates:
      - missing closing '---'
      - leading whitespace
      - missing opening (no front-matter at all → returns {})
      - corrupted fields (skip the broken line, keep going)

    Returns dict of best-effort parsed fields.
    """
    stripped = text.lstrip()
    if not stripped.startswith('---'):
        return {}
    # Try to find closing '---' on its own line
    # Skip first '---' line
    after_first = stripped[3:].lstrip('\n')
    # Find closing
    m = re.search(r'^---\s*$', after_first, re.MULTILINE)
    if m:
        yaml_text = after_first[:m.start()]
    else:
        # No closing — take everything until first non-key line or 100 lines max
        lines = after_first.split('\n')[:100]
        yaml_text = '\n'.join(lines)

    # Parse line-by-line without pyyaml dependency
    parsed = {}
    current_key = None
    current_list = None
    current_obj = None
    indent_stack = []

    for line in yaml_text.split('\n'):
        if not line.strip():
            continue
        if line.startswith('#'):
            continue

        # Top-level key: value
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$', line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            current_key = key
            current_list = None
            current_obj = None
            if value:
                # Strip quotes
                value = value.strip()
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                parsed[key] = value
            else:
                parsed[key] = None  # placeholder; may become list/dict
            continue

        # List item: '  - foo' or '  - key: value'
        m = re.match(r'^\s+-\s+(.*)$', line)
        if m and current_key:
            item_text = m.group(1).strip()
            if parsed[current_key] is None or isinstance(parsed[current_key], str):
                parsed[current_key] = []
            # Is it a key: value? (nested dict in list)
            kv_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$', item_text)
            if kv_match:
                k, v = kv_match.group(1), kv_match.group(2).strip()
                if (v.startswith('"') and v.endswith('"')) or \
                   (v.startswith("'") and v.endswith("'")):
                    v = v[1:-1]
                new_obj = {k: v}
                parsed[current_key].append(new_obj)
                current_obj = new_obj
            else:
                # Simple list item
                if (item_text.startswith('"') and item_text.endswith('"')) or \
                   (item_text.startswith("'") and item_text.endswith("'")):
                    item_text = item_text[1:-1]
                parsed[current_key].append(item_text)
                current_obj = None
            continue

        # Continuation of list item: '    key: value' (deeper indent)
        m = re.match(r'^\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$', line)
        if m and current_obj is not None:
            k, v = m.group(1), m.group(2).strip()
            if (v.startswith('"') and v.endswith('"')) or \
               (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
            current_obj[k] = v

    return parsed


def cold_start_header_intercept(text):
    """
    Phase 1: extract minimal core constants.

    Returns:
        {
            'node_id': str (from header or ephemeral SHA-based),
            'status': str or None,
            'engages': list (best-effort parsed),
            'is_ephemeral': bool (True if header was missing/corrupt),
            'all_fields': dict of all parsed fields
        }
    """
    fields = extract_front_matter(text)
    node_id = fields.get('node_id')
    is_ephemeral = False

    if not node_id:
        # Mint ephemeral from SHA-256 of first 500 words
        h = sha256_prefix(text)
        node_id = f'cha:node:ephemeral:{h[:16]}'
        is_ephemeral = True

    return {
        'node_id': node_id,
        'status': fields.get('status'),
        'engages': fields.get('engages', []) if isinstance(fields.get('engages'), list) else [],
        'observed_addresses': fields.get('observed_addresses', []) if isinstance(fields.get('observed_addresses'), list) else [],
        'is_ephemeral': is_ephemeral,
        'all_fields': fields,
        'doc_hash': sha256_prefix(text),
    }


# -------------------------- Phase 2: Inline Signature Extraction --------------------------

def strip_code_regions(text):
    """
    Replace content inside fenced code blocks (```...```) and inline backticks (`...`)
    with spaces of equal length. This neutralizes inline-marker *examples* in
    documentation without changing line numbers or other offsets.
    """
    # Fenced code blocks first
    def _blank_match(m):
        return ' ' * len(m.group(0))
    text = re.sub(r'```[\s\S]*?```', _blank_match, text)
    # Inline backticks (single)
    text = re.sub(r'`[^`\n]*`', _blank_match, text)
    return text


def extract_inline_markers(text):
    """
    Phase 2: find all [TYPE: argument] markers in the body.
    Markers inside fenced code blocks or inline backticks are ignored
    (they are documentation examples, not transaction markers).

    Returns list of dicts:
        {type, argument, sentence_context, line_number, vector}
    """
    findings = []
    scrubbed = strip_code_regions(text)
    lines = scrubbed.split('\n')
    orig_lines = text.split('\n')

    for line_idx, line in enumerate(lines):
        for m in INLINE_MARKER_RE.finditer(line):
            marker_type = m.group(1).upper()
            argument = m.group(2).strip()
            # Restore original sentence context (not the scrubbed version)
            orig_line = orig_lines[line_idx] if line_idx < len(orig_lines) else line
            # Get sentence context from original (clip to ~200 chars centered on marker)
            start_ctx = max(0, m.start() - 80)
            end_ctx = min(len(orig_line), m.end() + 80)
            sentence_context = orig_line[start_ctx:end_ctx].strip()

            # Map marker type → vector tag for ledger
            vector_map = {
                'MINT': 'coining',
                'FOUND': 'establishing',
                'INVOKE': 'address_claim',
                'CITE': 'citation',
                'REVISE': 'meaning_extension',
                'POSITION': 'structural_role',
                'SPECIFY': 'formal_operator',
                'DEVELOP': 'position_built',
            }

            findings.append({
                'type': marker_type,
                'argument': argument,
                'sentence_context': sentence_context,
                'line_number': line_idx + 1,
                'vector': vector_map.get(marker_type, 'unknown'),
            })

    return findings


def harvest_from_frontmatter(header_meta):
    """
    Convert front-matter 'engages' entries into synthetic markers.
    This means: even without inline [MINT:] markers, the front-matter alone
    yields a complete transaction set.
    """
    findings = []
    for e in header_meta.get('engages', []):
        if not isinstance(e, dict):
            continue
        entity = e.get('entity', '?')
        as_role = (e.get('as') or 'unclassified').lower()
        display = e.get('display_name', entity)

        type_map = {
            'minted': 'MINT',
            'founded': 'FOUND',
            'developed': 'DEVELOP',
            'revised': 'REVISE',
            'positioned': 'POSITION',
            'specified': 'SPECIFY',
            'engaged': 'ENGAGE',
            'unclassified': None,
        }
        marker_type = type_map.get(as_role)
        if marker_type:
            findings.append({
                'type': marker_type,
                'argument': display,
                'entity_id': entity,
                'sentence_context': f'(from front-matter engages: {entity} as {as_role})',
                'line_number': 0,  # header
                'vector': f'frontmatter_{as_role}',
            })
    # Observed addresses too
    for o in header_meta.get('observed_addresses', []):
        if not isinstance(o, dict):
            continue
        findings.append({
            'type': 'INVOKE',
            'argument': o.get('query', '?'),
            'address_id': o.get('address_id'),
            'sentence_context': f'(from front-matter: latest={o.get("latest_status")} on {o.get("latest_date")})',
            'line_number': 0,
            'vector': 'frontmatter_address_observed',
            'latest_status': o.get('latest_status'),
            'latest_date': o.get('latest_date'),
            'observation_count': o.get('observation_count'),
        })
    return findings


# -------------------------- Phase 3: Append-Only Ledger Emission --------------------------

def slugify(s):
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')


def emit_transaction(node_id, finding, source_file):
    """
    Build a flat single-line transaction string. NO nested objects.
    Each pipe-delimited field is self-contained.
    """
    ts = now_iso()
    t = finding['type']
    arg = finding['argument'].replace('|', '/').replace('\n', ' ')[:200]

    # Build TX based on type
    if t == 'MINT':
        eid = finding.get('entity_id') or f'cha:concept:{slugify(arg)}'
        tx = f'TX_MINT | NODE: {node_id} | ENTITY: {eid} | TERM: "{arg}" | VECTOR: {finding["vector"]}'
    elif t == 'FOUND':
        eid = finding.get('entity_id') or f'cha:institution:{slugify(arg)}'
        tx = f'TX_FOUND | NODE: {node_id} | INSTITUTION: {eid} | NAME: "{arg}" | VECTOR: established'
    elif t == 'DEVELOP':
        eid = finding.get('entity_id') or f'cha:concept:{slugify(arg)}'
        tx = f'TX_DEVELOP | NODE: {node_id} | ENTITY: {eid} | TERM: "{arg}" | VECTOR: position_built'
    elif t == 'REVISE':
        eid = finding.get('entity_id') or f'cha:concept:{slugify(arg)}'
        tx = f'TX_REVISE | NODE: {node_id} | ENTITY: {eid} | TERM: "{arg}" | VECTOR: meaning_extended'
    elif t == 'POSITION':
        eid = finding.get('entity_id') or f'cha:entity:{slugify(arg)}'
        tx = f'TX_POSITION | NODE: {node_id} | ENTITY: {eid} | NAME: "{arg}" | VECTOR: structural_role'
    elif t == 'SPECIFY':
        eid = finding.get('entity_id') or f'cha:operator:{slugify(arg)}'
        tx = f'TX_SPECIFY | NODE: {node_id} | ENTITY: {eid} | TERM: "{arg}" | VECTOR: formal_operator'
    elif t == 'INVOKE':
        addr = arg
        obs = 'true' if finding.get('latest_status') else 'false'
        st = finding.get('latest_status') or 'null'
        dt = finding.get('latest_date') or 'null'
        tx = f'TX_INVOKE | NODE: {node_id} | ADDRESS: "{addr}" | OBSERVED: {obs} | STATUS: {st} | DATE: {dt}'
    elif t == 'CITE':
        tx = f'TX_CITE | NODE: {node_id} | TARGET: "{arg}"'
    elif t == 'ENGAGE':
        eid = finding.get('entity_id') or f'cha:concept:{slugify(arg)}'
        tx = f'TX_ENGAGE | NODE: {node_id} | ENTITY: {eid} | TERM: "{arg}" | VECTOR: engaged_not_minted'
    else:
        tx = f'TX_UNKNOWN | NODE: {node_id} | TYPE: {t} | ARG: "{arg}"'

    # Add provenance suffix
    tx += f' | SOURCE: {source_file}'
    return f'[{ts}] | {tx}'


def emit_hash_anchor(node_id, doc_hash, length, source_file):
    """Anchor an ephemeral node by emitting its hash signature."""
    ts = now_iso()
    return f'[{ts}] | TX_HASH | NODE: {node_id} | SHA256: {doc_hash} | LENGTH: {length} | SOURCE: {source_file}'


def append_to_ledger(transactions, ledger_path=LEDGER_PATH):
    """Append transactions to ledger. Create parent dir if needed."""
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    # If ledger doesn't exist, write a header
    if not ledger_path.exists():
        header_lines = [
            '# cha.ledger — Append-Only Transaction Ledger',
            '# Format: [ISO8601] | TX_TYPE | KEY: value | KEY: value | ...',
            '# Each line is a standalone transaction. Truncation safe — no nested structures.',
            '# Schema versions transparently. New TX types are added without breaking old readers.',
            '# Replay: bottom-up reverse chronological. Fuzzy fallback: semantic proximity.',
            f'# Initialized: {now_iso()}',
            '',
        ]
        ledger_path.write_text('\n'.join(header_lines), encoding='utf-8')

    with ledger_path.open('a', encoding='utf-8') as f:
        for tx in transactions:
            f.write(tx + '\n')


# -------------------------- Phase 4: Fuzzy Hash Verification (replay) --------------------------

def replay_ledger(ledger_path=LEDGER_PATH):
    """
    Bottom-up replay of the ledger. Returns dict of {node_id: [transactions]}.
    Future: add fuzzy proximity fallback for fractured node_ids.
    """
    if not ledger_path.exists():
        return {}
    nodes = {}
    with ledger_path.open('r', encoding='utf-8') as f:
        lines = [l for l in f.readlines() if l.strip() and not l.lstrip().startswith('#')]
    # Iterate in reverse — latest claims win
    for line in reversed(lines):
        m = re.match(r'^\[([^\]]+)\]\s*\|\s*(TX_\w+)\s*\|\s*(.+)$', line.strip())
        if not m:
            continue
        ts, tx_type, payload = m.group(1), m.group(2), m.group(3)
        # Extract NODE: nid
        nm = re.search(r'NODE:\s*([^\s|]+)', payload)
        nid = nm.group(1) if nm else 'cha:node:unknown'
        nodes.setdefault(nid, []).append({
            'timestamp': ts,
            'tx_type': tx_type,
            'raw': line.rstrip(),
        })
    return nodes


# -------------------------- Main pipeline --------------------------

def ingest_file(filepath):
    """Run the full pipeline on one file. Returns count of transactions emitted."""
    path = Path(filepath)
    if not path.exists():
        return 0, f"file not found: {filepath}"
    text = path.read_text(encoding='utf-8', errors='replace')

    # Phase 1
    header = cold_start_header_intercept(text)

    transactions = []

    # Anchor: if ephemeral node, emit hash
    if header['is_ephemeral']:
        transactions.append(emit_hash_anchor(
            header['node_id'], header['doc_hash'], len(text), str(path)
        ))

    # Phase 2 — inline markers (primary)
    inline_findings = extract_inline_markers(text)
    # Phase 2b — front-matter harvest (secondary)
    fm_findings = harvest_from_frontmatter(header)

    # Combine, deduplicating (same type + same argument)
    seen = set()
    findings = []
    for f in inline_findings + fm_findings:
        key = (f['type'], f['argument'].lower())
        if key not in seen:
            seen.add(key)
            findings.append(f)

    # Phase 3 — emit transactions
    for f in findings:
        transactions.append(emit_transaction(header['node_id'], f, str(path)))

    # Append-only
    append_to_ledger(transactions)

    return len(transactions), {
        'node_id': header['node_id'],
        'is_ephemeral': header['is_ephemeral'],
        'inline_findings': len(inline_findings),
        'frontmatter_findings': len(fm_findings),
        'total_transactions': len(transactions),
    }


def main(argv):
    if len(argv) < 2:
        print(__doc__.split('Usage:')[1])
        return 1

    files = []
    for pattern in argv[1:]:
        if any(c in pattern for c in '*?['):
            files.extend(globmod.glob(pattern))
        else:
            files.append(pattern)

    if not files:
        print("No files matched.")
        return 1

    total_tx = 0
    for f in files:
        count, info = ingest_file(f)
        if isinstance(info, dict):
            ephem = ' [ephemeral]' if info.get('is_ephemeral') else ''
            print(f"  {f}{ephem}: {count} transactions emitted "
                  f"(inline={info['inline_findings']}, frontmatter={info['frontmatter_findings']}) "
                  f"node={info['node_id']}")
        else:
            print(f"  {f}: ERROR — {info}")
        total_tx += count

    print(f"\nTotal: {total_tx} transactions emitted to {LEDGER_PATH}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
