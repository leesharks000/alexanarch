#!/usr/bin/env python3
"""
validate_external_metadata.py — verify external-metadata sidecars against schema.

═══════════════════════════════════════════════════════════════════════════════
PLACE IN THE ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

Sanity-check every file in data/external-metadata/ against
api/schemas/external-metadata.schema.json. Reports:

  - JSON parse failures
  - required-field violations (axn, deposit_number, generated_at, schema_version,
    purpose, zenodo_dois_covered, sources)
  - DOI format violations on zenodo_dois_covered entries
  - severance_status enum violations
  - AXN format violations (must match v2 regex)
  - cross-reference violations: sidecar's axn and deposit_number must match
    an entry in data/registry.json

Exit code: 0 if all sidecars pass, 1 if any fail.

═══════════════════════════════════════════════════════════════════════════════
USAGE
═══════════════════════════════════════════════════════════════════════════════

    python3 scripts/validate_external_metadata.py
        Walk data/external-metadata/ and validate each file.

    python3 scripts/validate_external_metadata.py --strict
        Exit nonzero on the first violation.

    python3 scripts/validate_external_metadata.py --file data/external-metadata/AXN-0001.json
        Validate a single sidecar.

═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SIDECAR_DIR = REPO_ROOT / "data" / "external-metadata"
REGISTRY_PATH = REPO_ROOT / "data" / "registry.json"
SCHEMA_PATH = REPO_ROOT / "api" / "schemas" / "external-metadata.schema.json"

DOI_RE = re.compile(r"^10\.5281/zenodo\.[0-9]+$")
AXN_RE = re.compile(r"^AXN:[0-9A-Fa-f]{2,4}\.[A-Z]+\..+$")
VALID_SEVERANCE = {"severed", "anonymized", "retained", "post_window", "typo_immunity", "mixed", "unknown"}
REQUIRED = ["axn", "deposit_number", "generated_at", "schema_version", "purpose", "zenodo_dois_covered", "sources"]


def load_registry_lookup():
    """Build a {(axn, deposit_number): True} set for cross-reference."""
    with open(REGISTRY_PATH) as f:
        reg = json.load(f)
    return {(d.get("axn"), d.get("deposit_number")) for d in reg["deposits"]}


def validate_sidecar(path: Path, registry_lookup):
    """Validate a single sidecar. Returns list of (rule_id, message) failures."""
    failures = []

    # 0. JSON parse
    try:
        with open(path) as f:
            sc = json.load(f)
    except json.JSONDecodeError as e:
        return [("EM-000", f"JSON parse error: {e}")]
    except Exception as e:
        return [("EM-000", f"file read error: {e}")]

    # 1. Required fields
    for k in REQUIRED:
        if k not in sc:
            failures.append(("EM-001", f"missing required field: {k}"))

    # 2. schema_version pin
    if sc.get("schema_version") != "1.0":
        failures.append(("EM-002", f"schema_version must be '1.0', got {sc.get('schema_version')!r}"))

    # 3. AXN format
    axn = sc.get("axn", "")
    if not AXN_RE.match(axn):
        failures.append(("EM-003", f"axn does not match v2 regex: {axn!r}"))

    # 4. deposit_number range
    dn = sc.get("deposit_number")
    if not isinstance(dn, int) or dn < 1:
        failures.append(("EM-004", f"deposit_number must be positive integer, got {dn!r}"))

    # 5. severance_status enum (optional field)
    sev = sc.get("severance_status")
    if sev is not None and sev not in VALID_SEVERANCE:
        failures.append(("EM-005", f"severance_status {sev!r} not in {sorted(VALID_SEVERANCE)}"))

    # 6. zenodo_dois_covered entries
    dois = sc.get("zenodo_dois_covered") or []
    if not isinstance(dois, list):
        failures.append(("EM-006", f"zenodo_dois_covered must be array, got {type(dois).__name__}"))
    else:
        for doi in dois:
            if not isinstance(doi, str) or not DOI_RE.match(doi):
                failures.append(("EM-006", f"invalid Zenodo DOI: {doi!r}"))

    # 7. sources must be a dict with at least one known subkey
    sources = sc.get("sources")
    if not isinstance(sources, dict):
        failures.append(("EM-007", f"sources must be object, got {type(sources).__name__ if sources is not None else 'None'}"))
    elif not sources:
        failures.append(("EM-007", "sources object is empty — sidecar carries no recovered metadata"))

    # 8. Cross-reference to registry: (axn, deposit_number) must be in registry
    if (axn, dn) not in registry_lookup:
        failures.append(("EM-008", f"sidecar (axn={axn!r}, deposit_number={dn}) does not match any registry entry"))

    # 9. Filename matches axn hex
    hex_match = re.match(r"^AXN:([0-9A-Fa-f]{2,4})\.", axn)
    if hex_match:
        hex_id = hex_match.group(1)
        expected_filename = f"AXN-{hex_id}.json"
        if path.name != expected_filename:
            failures.append(("EM-009", f"filename {path.name} does not match expected {expected_filename}"))

    return failures


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--strict", action="store_true", help="Exit nonzero on first violation.")
    p.add_argument("--file", help="Validate single sidecar file (path relative to repo root).")
    args = p.parse_args()

    if not SIDECAR_DIR.exists() and not args.file:
        print(f"INFO: {SIDECAR_DIR} does not exist yet (Phase 1 not run). Nothing to validate.")
        return

    registry_lookup = load_registry_lookup()

    if args.file:
        files = [Path(args.file) if Path(args.file).is_absolute() else REPO_ROOT / args.file]
    else:
        files = sorted(SIDECAR_DIR.glob("AXN-*.json"))

    total = 0
    failed_files = 0
    total_failures = 0

    for f in files:
        total += 1
        failures = validate_sidecar(f, registry_lookup)
        if failures:
            failed_files += 1
            total_failures += len(failures)
            print(f"FAIL {f.relative_to(REPO_ROOT)}:")
            for rule_id, msg in failures:
                print(f"  [{rule_id}] {msg}")
            if args.strict:
                sys.exit(1)

    if total == 0:
        print("WARN: no sidecars found in", SIDECAR_DIR)
        return

    print(f"\nValidated {total} sidecars; {failed_files} files with failures; {total_failures} total violations.")
    if failed_files > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
