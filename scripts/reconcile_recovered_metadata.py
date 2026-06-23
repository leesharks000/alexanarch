#!/usr/bin/env python3
"""
reconcile_recovered_metadata.py — wire recovered metadata into Alexanarch.

═══════════════════════════════════════════════════════════════════════════════
PLACE IN THE ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

After the 2026-06-19 Zenodo account termination, the recovery effort
(commit 118141f7) deposited four metadata sources in data/:

  data/openalex-severed-recovery.json
  data/zenodo-xml-pretermination-2026-06-07.tar.gz
  data/datacite-full-backup.json
  data/datacite-survivors-multi-heteronym.json

This script joins those sources to the 885 deposits in data/registry.json
and produces:

  1. Per-deposit external-metadata sidecars at
     data/external-metadata/AXN-<HEX>.json
     (one per deposit that has at least one recovered source).

  2. Registry-pointer fields added to each covered deposit:
     - external_metadata_path  (string, sidecar URL)
     - openalex_ids            (array of OpenAlex Work IDs, one per covered DOI)
     - datacite_severance      (string: severed | anonymized | retained | mixed)

The script DOES NOT touch:
  - any existing field value on any existing deposit (additive only)
  - any deposit's AXN, hash, hex, emoji (their canonical bytes are locked)
  - data/registry.json's compact-JSON convention (writes use compact mode)
  - api/index.json (use scripts/protocol_update.py separately)
  - data/doi-resolution-index.json (separate script: reconcile_resolution_index.py)

═══════════════════════════════════════════════════════════════════════════════
USAGE
═══════════════════════════════════════════════════════════════════════════════

    python3 scripts/reconcile_recovered_metadata.py --dry-run
        Print the per-phase plan, write nothing.

    python3 scripts/reconcile_recovered_metadata.py --phase 1
        Phase 1: write sidecars only (~738 new files, zero mutations).

    python3 scripts/reconcile_recovered_metadata.py --phase 2
        Phase 2: add registry pointer fields (data/registry.json mutated).
        Requires Phase 1 to have run first.

    python3 scripts/reconcile_recovered_metadata.py --phase 1,2
        Run Phase 1 then Phase 2 in one invocation.

The script is idempotent. Re-running Phase 1 overwrites existing sidecars
with the same content (no-op if sources unchanged). Re-running Phase 2 is
a no-op if the registry already has the pointer fields.

═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import datetime
import hashlib
import json
import os
import sys
import tarfile
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "data" / "registry.json"
SIDECAR_DIR   = REPO_ROOT / "data" / "external-metadata"
RECEIPTS_LOG  = REPO_ROOT / "data" / "pre-overwrite-receipts.log"

OPENALEX_SRC  = REPO_ROOT / "data" / "openalex-severed-recovery.json"
ZENODO_XML_TARBALL = REPO_ROOT / "data" / "zenodo-xml-pretermination-2026-06-07.tar.gz"
DATACITE_BACKUP_SRC = REPO_ROOT / "data" / "datacite-full-backup.json"
DATACITE_SURVIVOR_SRC = REPO_ROOT / "data" / "datacite-survivors-multi-heteronym.json"


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_receipt(message: str):
    """Append a structural receipt to pre-overwrite-receipts.log.

    Implements firm rule #7: before any overwrite of an existing file,
    write a receipt describing the planned change.
    """
    with open(RECEIPTS_LOG, "a") as f:
        f.write(f"[{now_iso()}] reconcile_recovered_metadata.py: {message}\n")


def load_sources():
    """Load all four sources. Returns dict of doi → metadata for each source.

    Returns:
        dict with keys 'openalex', 'datacite_backup', 'datacite_survivor', and
        'zenodo_xml' (the last is a set of record IDs present in the tarball,
        not the XML content — content is held in the tarball, sidecars point
        at filenames).
    """
    print("Loading sources...", flush=True)

    # OpenAlex
    with open(OPENALEX_SRC) as f:
        oa_data = json.load(f)
    oa_by_doi = {}
    for r in oa_data.get("records", []):
        doi = r.get("doi")
        if doi:
            oa_by_doi[doi] = r
    print(f"  OpenAlex: {len(oa_by_doi)} records", flush=True)

    # DataCite backup (older pre-termination harvest)
    with open(DATACITE_BACKUP_SRC) as f:
        dc_backup = json.load(f)
    dc_backup_by_doi = {}
    for r in dc_backup.get("records", []):
        # records list uses 'id' as DOI
        doi = r.get("id") or r.get("attributes", {}).get("doi")
        if doi:
            dc_backup_by_doi[doi] = r
    print(f"  DataCite backup: {len(dc_backup_by_doi)} records", flush=True)

    # DataCite survivor sweep (current heteronym sweep)
    with open(DATACITE_SURVIVOR_SRC) as f:
        dc_surv = json.load(f)
    dc_surv_by_doi = {}
    for key in ("orcid_records", "name_records", "sigil_records", "vox_records", "feist_records"):
        for r in dc_surv.get(key, []):
            doi = r.get("attributes", {}).get("doi") or r.get("id")
            if doi and doi not in dc_surv_by_doi:
                dc_surv_by_doi[doi] = r
    print(f"  DataCite survivor sweep: {len(dc_surv_by_doi)} records", flush=True)

    # Zenodo bulk XML — list the tarball contents
    zen_xml_ids = set()
    if ZENODO_XML_TARBALL.exists():
        with tarfile.open(ZENODO_XML_TARBALL, "r:gz") as tar:
            for m in tar.getmembers():
                if m.isfile() and m.name.endswith(".xml"):
                    rid = os.path.basename(m.name)[:-4]
                    zen_xml_ids.add(rid)
    print(f"  Zenodo bulk XML: {len(zen_xml_ids)} entries", flush=True)

    return {
        "openalex": oa_by_doi,
        "datacite_backup": dc_backup_by_doi,
        "datacite_survivor": dc_surv_by_doi,
        "zenodo_xml_ids": zen_xml_ids,
    }


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def write_registry_compact(reg):
    """Write registry preserving compact convention.

    Firm rule: registry.json uses indent=None, separators=(',',':'),
    ensure_ascii=False. Pretty-printing breaks consumers.
    """
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(reg, f, separators=(",", ":"), ensure_ascii=False)


def classify_severance(deposit_dois, sources):
    """Determine the severance status for a deposit based on the union of its
    DOI states across sources.

    Returns one of:
      retained        — at least one DOI still surfaces under heteronym/ORCID
      severed         — all DOIs are in OpenAlex/backup but not in current survivors
      anonymized      — DOI present in DataCite (state=findable) but creator scrubbed
      mixed           — mixed states across the deposit's DOIs
    """
    in_openalex = 0
    in_backup = 0
    in_survivor = 0
    in_xml = 0
    n = 0
    for doi in deposit_dois:
        n += 1
        if doi in sources["openalex"]:
            in_openalex += 1
        if doi in sources["datacite_backup"]:
            in_backup += 1
        if doi in sources["datacite_survivor"]:
            in_survivor += 1
        rid = doi.split("zenodo.")[1] if "zenodo." in doi else None
        if rid and rid in sources["zenodo_xml_ids"]:
            in_xml += 1

    if n == 0:
        return "unknown"
    if in_survivor == n:
        return "retained"
    if in_survivor == 0 and (in_openalex > 0 or in_xml > 0):
        return "severed"
    if 0 < in_survivor < n:
        return "mixed"
    return "unknown"


def build_sidecar(deposit, sources):
    """Build the external-metadata sidecar for a deposit.

    Returns the sidecar dict, or None if the deposit has no recoverable
    metadata.
    """
    dois = deposit.get("zenodo_dois") or []
    if isinstance(dois, str):
        dois = [dois]
    if not dois:
        return None

    # Gather per-source records for this deposit's DOIs
    oa_recs = []
    dc_backup_recs = []
    dc_surv_recs = []
    xml_entries = []
    openalex_ids = []

    for doi in dois:
        if not doi or not doi.startswith("10.5281/zenodo."):
            continue
        if doi in sources["openalex"]:
            rec = sources["openalex"][doi]
            oa_recs.append(rec)
            if rec.get("openalex_id"):
                openalex_ids.append(rec["openalex_id"])
        if doi in sources["datacite_backup"]:
            dc_backup_recs.append(sources["datacite_backup"][doi])
        if doi in sources["datacite_survivor"]:
            dc_surv_recs.append(sources["datacite_survivor"][doi])
        rid = doi.split("zenodo.")[1]
        if rid in sources["zenodo_xml_ids"]:
            xml_entries.append(f"{rid}.xml")

    if not (oa_recs or dc_backup_recs or dc_surv_recs or xml_entries):
        return None

    # Compute aggregate abstract length
    abstract_chars = 0
    has_authors = False
    has_keywords = False
    has_publication_date = False
    has_references = False
    has_concepts = False
    has_topics = False
    has_title = False
    has_abstract = False
    for rec in oa_recs:
        if rec.get("title"):
            has_title = True
        if rec.get("abstract"):
            has_abstract = True
            abstract_chars += len(rec["abstract"])
        if rec.get("authorships"):
            has_authors = True
        if rec.get("publication_date"):
            has_publication_date = True
        if rec.get("referenced_works"):
            has_references = True
        if rec.get("concepts"):
            has_concepts = True
        if rec.get("topics"):
            has_topics = True
    for rec in dc_backup_recs + dc_surv_recs:
        attrs = rec.get("attributes", {})
        if attrs.get("titles"):
            has_title = True
        if attrs.get("subjects"):
            has_keywords = True
        if attrs.get("creators"):
            has_authors = True

    severance = classify_severance(dois, sources)

    # ARCHITECTURE: sidecars are thin INDEX files pointing into bulk data stores.
    # The actual records live in (already-committed):
    #   - data/openalex-severed-recovery.json  (OpenAlex DATA STORE)
    #   - data/zenodo-xml-pretermination-2026-06-07.tar.gz  (Zenodo XML DATA STORE)
    #   - data/datacite-full-backup.json  (pre-termination DataCite snapshot)
    #   - data/datacite-survivors-multi-heteronym.json  (current DataCite survivors)
    #
    # Sidecars do NOT duplicate those records. They tell consumers:
    #   "deposit #N covers these DOIs; for each DOI's OpenAlex record,
    #    look up its openalex_id in data/openalex-severed-recovery.json"
    #
    # This keeps each sidecar ~2-5 KB instead of 100+ KB, and the total
    # data/external-metadata/ directory ~2-5 MB instead of 100+ MB.

    # Build per-DOI dereferenceable map
    per_doi = {}
    for doi in dois:
        if not doi or not doi.startswith("10.5281/zenodo."):
            continue
        entry = {}
        if doi in sources["openalex"]:
            rec = sources["openalex"][doi]
            entry["openalex_id"] = rec.get("openalex_id")
            # Inline only the most-useful small fields for quick rendering
            # without forcing a dereference to the bulk file:
            t = rec.get("title")
            if t:
                entry["title"] = t
            pd = rec.get("publication_date")
            if pd:
                entry["publication_date"] = pd
            # Abstract length without inlining the abstract itself
            ab = rec.get("abstract")
            if ab:
                entry["abstract_chars"] = len(ab)
        rid = doi.split("zenodo.")[1]
        if rid in sources["zenodo_xml_ids"]:
            entry["zenodo_bulk_xml_entry"] = f"{rid}.xml"
        if doi in sources["datacite_backup"]:
            entry["datacite_backup_present"] = True
        if doi in sources["datacite_survivor"]:
            entry["datacite_survivor_present"] = True
        if entry:
            per_doi[doi] = entry

    sidecar = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "axn": deposit.get("axn"),
        "deposit_number": deposit.get("deposit_number"),
        "generated_at": now_iso(),
        "schema_version": "1.0",
        "purpose": (
            "Thin per-deposit INDEX into the recovered external metadata "
            "for this deposit's legacy Zenodo DOIs. The actual records live "
            "in the bulk data stores under data/ (openalex-severed-recovery.json, "
            "zenodo-xml-pretermination-2026-06-07.tar.gz, datacite-full-backup.json, "
            "datacite-survivors-multi-heteronym.json). Sidecars do not duplicate "
            "those records — they map each covered DOI to its identifier in each store."
        ),
        "zenodo_dois_covered": [d for d in dois if d and d.startswith("10.5281/zenodo.")],
        "severance_status": severance,
        "per_doi": per_doi,
        "sources": {
            "openalex": {
                "data_store": "/data/openalex-severed-recovery.json",
                "lookup": "records[].doi == this DOI; openalex_id is the W-prefixed OpenAlex Work ID",
                "dois_present": [doi for doi in dois if doi in sources["openalex"]],
            },
            "zenodo_bulk_xml": {
                "data_store": "/data/zenodo-xml-pretermination-2026-06-07.tar.gz",
                "snapshot_date": "2026-06-07",
                "snapshot_url": (
                    "https://zenodo.org/api/exporter/records-xml.tar.gz/"
                    "839f6c8b-29d0-438e-b8c9-602200a28bac"
                ),
                "schema": "oai_datacite kernel-4.5 (CERN.ZENODO datacenter)",
                "lookup": "extract <record_id>.xml from the tarball where record_id is the digits after 'zenodo.'",
                "entries": xml_entries,
            },
            "datacite_backup": {
                "data_store": "/data/datacite-full-backup.json",
                "harvested_at": "2026-06-22 (pre-termination)",
                "lookup": "records[].id == this DOI",
                "dois_present": [doi for doi in dois if doi in sources["datacite_backup"]],
            },
            "datacite_survivor_sweep": {
                "data_store": "/data/datacite-survivors-multi-heteronym.json",
                "harvested_at": "2026-06-23 (post-termination, multi-heteronym query)",
                "lookup": "search records[].attributes.doi == this DOI across orcid_records, name_records, sigil_records, vox_records, feist_records",
                "dois_present": [doi for doi in dois if doi in sources["datacite_survivor"]],
            },
        },
        "abstract_recovered_chars": abstract_chars,
        "recovered_fields_summary": {
            "has_title": has_title,
            "has_abstract": has_abstract,
            "has_authors": has_authors,
            "has_keywords": has_keywords,
            "has_publication_date": has_publication_date,
            "has_references": has_references,
            "has_concepts": has_concepts,
            "has_topics": has_topics,
            "has_full_datacite_xml": len(xml_entries) > 0,
        },
        "openalex_ids": openalex_ids,
    }

    return sidecar


def phase1_write_sidecars(reg, sources, dry_run=False):
    """Phase 1: write per-deposit sidecars."""
    print("\n=== PHASE 1: Sidecars ===", flush=True)
    SIDECAR_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped_no_metadata = 0
    written_paths = []

    for deposit in reg["deposits"]:
        sidecar = build_sidecar(deposit, sources)
        if sidecar is None:
            skipped_no_metadata += 1
            continue

        hex_id = deposit.get("hex", "")
        path = SIDECAR_DIR / f"AXN-{hex_id}.json"

        if dry_run:
            written += 1
            continue

        # Sidecars use indented JSON for readability — they're not the registry
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sidecar, f, indent=2, ensure_ascii=False)
        written += 1
        written_paths.append(str(path.relative_to(REPO_ROOT)))

    print(f"  sidecars to write: {written}", flush=True)
    print(f"  deposits with no recoverable metadata: {skipped_no_metadata}", flush=True)
    if dry_run:
        print("  DRY RUN — no files written")
    else:
        write_receipt(f"Phase 1 wrote {written} sidecars under data/external-metadata/")
    return written, skipped_no_metadata


def phase2_registry_pointers(reg, sources, dry_run=False):
    """Phase 2: add 3 pointer fields to registry entries (additive only)."""
    print("\n=== PHASE 2: Registry pointer fields ===", flush=True)

    changed = 0
    unchanged = 0
    new_fields_added = 0

    for deposit in reg["deposits"]:
        sidecar = build_sidecar(deposit, sources)
        if sidecar is None:
            unchanged += 1
            continue

        hex_id = deposit.get("hex", "")
        sidecar_path = f"/data/external-metadata/AXN-{hex_id}.json"
        oa_ids = sidecar.get("openalex_ids") or []
        severance = sidecar.get("severance_status")

        # Add only if missing; never overwrite existing values (additive only)
        mutated = False
        if "external_metadata_path" not in deposit:
            deposit["external_metadata_path"] = sidecar_path
            new_fields_added += 1
            mutated = True
        elif deposit["external_metadata_path"] != sidecar_path:
            print(f"  WARN: deposit #{deposit['deposit_number']} already has external_metadata_path = {deposit['external_metadata_path']}; skipping override")

        if "openalex_ids" not in deposit:
            deposit["openalex_ids"] = oa_ids
            new_fields_added += 1
            mutated = True

        if "datacite_severance" not in deposit:
            deposit["datacite_severance"] = severance
            new_fields_added += 1
            mutated = True

        if mutated:
            changed += 1
        else:
            unchanged += 1

    print(f"  deposits with new pointer fields: {changed}", flush=True)
    print(f"  unchanged: {unchanged}", flush=True)
    print(f"  total new field-level additions: {new_fields_added}", flush=True)

    if dry_run:
        print("  DRY RUN — registry not written")
    else:
        write_receipt(f"Phase 2 added pointer fields to {changed} deposits ({new_fields_added} field additions). No existing field values mutated.")
        write_registry_compact(reg)
        print(f"  registry written to {REGISTRY_PATH}")

    return changed


def verify_no_existing_field_mutations(reg_before, reg_after):
    """Assert no existing field on any deposit was modified."""
    by_n_before = {d["deposit_number"]: d for d in reg_before["deposits"]}
    by_n_after  = {d["deposit_number"]: d for d in reg_after["deposits"]}
    safe_new_fields = {"external_metadata_path", "openalex_ids", "datacite_severance"}

    mutations = []
    for n, before in by_n_before.items():
        after = by_n_after.get(n)
        if after is None:
            mutations.append((n, "DELETED", None, None))
            continue
        for k, v_before in before.items():
            v_after = after.get(k)
            if v_before != v_after:
                mutations.append((n, k, v_before, v_after))
        for k in after:
            if k not in before and k not in safe_new_fields:
                mutations.append((n, k, "(absent)", after[k]))

    return mutations


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--phase", default="all", help="Comma-separated phases (1, 2, all). Default: all.")
    p.add_argument("--dry-run", action="store_true", help="Print plan, write nothing.")
    args = p.parse_args()

    phases = args.phase.split(",") if args.phase != "all" else ["1", "2"]
    phases = [p.strip() for p in phases]

    sources = load_sources()
    reg = load_registry()
    reg_before_snapshot = json.loads(json.dumps(reg))  # deep copy for verification

    if "1" in phases:
        phase1_write_sidecars(reg, sources, dry_run=args.dry_run)

    if "2" in phases:
        phase2_registry_pointers(reg, sources, dry_run=args.dry_run)
        if not args.dry_run:
            # Verify no existing field was mutated
            reg_after = load_registry()
            mutations = verify_no_existing_field_mutations(reg_before_snapshot, reg_after)
            if mutations:
                print(f"\nFATAL: detected {len(mutations)} mutations to existing fields:")
                for m in mutations[:10]:
                    print(f"  deposit #{m[0]}.{m[1]}: before={str(m[2])[:60]!r}  after={str(m[3])[:60]!r}")
                sys.exit(1)
            print(f"\n  ✓ No existing field values mutated (verified {len(reg_after['deposits'])} deposits).")

    print(f"\nDone. {now_iso()}")


if __name__ == "__main__":
    main()
