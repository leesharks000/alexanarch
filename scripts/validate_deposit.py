#!/usr/bin/env python3
"""
validate_deposit.py — validates deposit submissions against the canonical
protocol at api/deposit-protocol.json.

Used by:
    1. .github/workflows/mint-axn.yml — to reject malformed [DEPOSIT] issues
    2. .github/workflows/validate-registry.yml — pre-commit CI on PRs
    3. Local development — agents can run this before submitting

USAGE
═════
    # Validate an issue body (parsed from GitHub Issue)
    python3 scripts/validate_deposit.py --issue-body issue.md

    # Validate a single registry entry (JSON)
    python3 scripts/validate_deposit.py --registry-entry deposit.json

    # Validate the entire registry against all invariants
    python3 scripts/validate_deposit.py --registry data/registry.json

    # Strict mode (exit non-zero on any failure)
    python3 scripts/validate_deposit.py --strict ...

The exit code is 0 on success, 1 on validation failure, 2 on script error.

VALIDATION RULES
════════════════
Rules are defined in api/deposit-protocol.json under validation_rules.
Each failure is reported as: [<RULE_ID>] <description> (<context>)
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

PROTOCOL_PATH = REPO_ROOT / "api" / "deposit-protocol.json"


def count_emoji_graphemes(s):
    """Approximate emoji grapheme count, accounting for VS/ZWJ."""
    if not s:
        return 0
    out = 0
    i = 0
    chars = list(s)
    while i < len(chars):
        ch = chars[i]
        cp = ord(ch)
        if 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF:
            i += 1
            continue
        if cp == 0x200D:
            i += 1
            if i < len(chars):
                i += 1
            continue
        if cp < 0x80:
            i += 1
            continue
        out += 1
        i += 1
    return out


def load_protocol():
    with open(PROTOCOL_PATH) as f:
        return json.load(f)


def extract_field_from_issue_body(body, label):
    """Extract a `### Label` field from a GitHub Issue body."""
    pattern = rf"###\s+{re.escape(label)}\s*\n\s*(.*?)(?=\n###|\Z)"
    m = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    if m:
        val = m.group(1).strip()
        if val in ("_No response_", "None", ""):
            return ""
        return val
    return ""


def validate_issue_body(body, protocol):
    """Validate a deposit issue body against the protocol. Returns list of (rule_id, msg)."""
    failures = []
    current_pv = protocol["protocol_version"]

    # PV-001: protocol_version field present and matches current
    declared_pv = extract_field_from_issue_body(body, "Protocol Version")
    if not declared_pv:
        failures.append(("PV-001",
                         f"Missing required field '### Protocol Version'. "
                         f"Must equal '{current_pv}'. See {protocol['canonical_docs']['this_protocol']}."))
    elif declared_pv != current_pv:
        failures.append(("PV-001",
                         f"Protocol version mismatch. Declared '{declared_pv}', current is '{current_pv}'. "
                         f"Re-read {protocol['canonical_docs']['this_protocol']} and update."))

    # REQ-001..005: required fields present and non-empty
    required = protocol["required_deposit_fields"]
    label_map = {
        "title": "Title",
        "creator": "Creator",
        "description": "Description",
        "content_type": "Content Type",
        "license": "License",
        "substrate": "Substrate Disclosure",
    }
    for i, (field_key, label) in enumerate(label_map.items(), start=1):
        rule_id = f"REQ-{i:03d}"
        val = extract_field_from_issue_body(body, label)
        if not val:
            failures.append((rule_id, f"Missing or empty required field '### {label}'."))

    # Terms acknowledgement — must include the protocol-read confirmation
    terms_section = extract_field_from_issue_body(body, "Terms")
    if "deposit-protocol.json" not in terms_section and "I read the deposit protocol" not in terms_section:
        failures.append(("PV-002",
                         "Terms section must include the checked confirmation: "
                         "'- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json'"))

    return failures


def validate_registry_entry(entry, protocol):
    """Validate a single registry entry."""
    failures = []
    rules = {r["id"]: r for r in protocol["validation_rules"]["rules"]}

    # AXN-001: AXN format
    axn = entry.get("axn", "")
    if not re.match(r"^AXN:[0-9A-F]{2,4}\.[A-Z]+\.[^.]{1,}$", axn):
        failures.append(("AXN-001", f"AXN does not match canonical format: {axn!r}"))

    # AXN-002: emoji count = 6
    parts = axn.split(".", 2)
    if len(parts) >= 3:
        emoji = parts[2]
        n = count_emoji_graphemes(emoji)
        if n != 6:
            failures.append(("AXN-002", f"AXN emoji must be 6 graphemes per AXN v2; got {n} in {axn!r}"))

    # AXN-003: hash is 64-char hex
    h = entry.get("hash", "")
    if not re.match(r"^[0-9a-f]{64}$", h or ""):
        failures.append(("AXN-003", f"hash must be a 64-char lowercase hex SHA-256; got {h!r}"))

    return failures


def validate_registry(reg, protocol):
    """Validate the full registry against consistency invariants."""
    failures = []

    # CONSISTENCY-001: total_deposits == len(deposits)
    if reg.get("total_deposits") != len(reg.get("deposits", [])):
        failures.append(("CONS-001",
                         f"total_deposits ({reg.get('total_deposits')}) != len(deposits) ({len(reg.get('deposits', []))})"))

    # AXN-004: deposit_numbers are contiguous from 1
    deposit_numbers = [d.get("deposit_number") for d in reg["deposits"]]
    if sorted(deposit_numbers) != list(range(1, len(deposit_numbers) + 1)):
        failures.append(("AXN-004",
                         f"deposit_numbers are not contiguous 1..N (N={len(deposit_numbers)})"))

    # Per-entry validation
    for d in reg["deposits"]:
        entry_failures = validate_registry_entry(d, protocol)
        for rid, msg in entry_failures:
            failures.append((rid, f"#{d.get('deposit_number')}: {msg}"))

    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--issue-body", type=Path, help="path to a GitHub Issue body markdown file")
    parser.add_argument("--registry-entry", type=Path, help="path to a single deposit JSON")
    parser.add_argument("--registry", type=Path, help="path to data/registry.json (full validation)")
    parser.add_argument("--strict", action="store_true", help="exit non-zero on any failure")
    args = parser.parse_args()

    protocol = load_protocol()
    all_failures = []
    targets_validated = 0

    if args.issue_body:
        with open(args.issue_body) as f:
            body = f.read()
        failures = validate_issue_body(body, protocol)
        all_failures.extend(failures)
        targets_validated += 1
        print(f"Validated issue body {args.issue_body}: {len(failures)} failure(s)")

    if args.registry_entry:
        with open(args.registry_entry) as f:
            entry = json.load(f)
        failures = validate_registry_entry(entry, protocol)
        all_failures.extend(failures)
        targets_validated += 1
        print(f"Validated registry entry: {len(failures)} failure(s)")

    if args.registry:
        with open(args.registry) as f:
            reg = json.load(f)
        failures = validate_registry(reg, protocol)
        all_failures.extend(failures)
        targets_validated += 1
        print(f"Validated registry ({len(reg['deposits'])} deposits): {len(failures)} failure(s)")

    if targets_validated == 0:
        print("No targets specified. Pass --issue-body, --registry-entry, or --registry.")
        sys.exit(2)

    if all_failures:
        print()
        print("FAILURES:")
        for rid, msg in all_failures:
            print(f"  [{rid}] {msg}")
        print()
        print(f"Current protocol_version: {protocol['protocol_version']}")
        print(f"Protocol JSON: {protocol['canonical_docs']['this_protocol']}")
        print(f"Deposit flow doc: {protocol['canonical_docs']['deposit_flow']}")
        if args.strict:
            sys.exit(1)
    else:
        print()
        print(f"✓ All checks passed against protocol {protocol['protocol_version']}")


if __name__ == "__main__":
    main()
