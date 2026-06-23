#!/usr/bin/env python3
"""
reconcile_resolution_index.py — wire recovered metadata into the DOI Resolution Index.

═══════════════════════════════════════════════════════════════════════════════
PLACE IN THE ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

Separate from reconcile_recovered_metadata.py (which handles registry + sidecars).
This script mutates ONLY data/doi-resolution-index.json:

  Inputs:
    data/doi-resolution-index.json              (v3.1, 1817 mappings)
    data/openalex-severed-recovery.json         (844 records)
    data/datacite-survivors-multi-heteronym.json
    data/zenodo-xml-pretermination-2026-06-07.tar.gz
    data/newly-found-openalex.json              (21 + 2 typo deposits)
    data/ghost-records-categorized.json         (59 misclassifications)
    data/registry.json                          (for AXN/record cross-reference)

  Output: data/doi-resolution-index.json v3.2 with these additive changes:

    For mappings with recovered metadata (851 of them):
      + openalex_id                 (string)
      + metadata_recovered_from     (array: ["openalex", "zenodo_bulk_xml", ...])
      + severance_status            (string: severed | retained | anonymized | mixed | post_window)
      + external_metadata_path      (string, where the deposit's sidecar lives)
      + abstract_recovered_chars    (integer)

    For the 59 misclassified mappings:
      + misclassification_note      (string)
      ~ mapping_type                "direct" → "misclassified_other_author"

    For the 2 typo-creator deposits (Sharkd, Craned):
      NEW mappings (additive — total_mappings becomes 1819):
      + severance_status: "typo_immunity"
      + typo_note: explanation

    Top-level:
      ~ version                     "3.1" → "3.2"
      ~ total_mappings              1817 → 1819
      ~ last_updated                bumped
      + changelog                   v3.2 entry appended

NO existing field VALUES on any mapping are mutated except:
  - mapping_type on the 59 misclassified entries (with note explaining why)
  - top-level version/total_mappings/last_updated

The 59 misclassification flag is reversible (the previous mapping_type is
preserved in misclassification_note via "was: direct, ..."). The 2 new
mappings are pure additions.

═══════════════════════════════════════════════════════════════════════════════
USAGE
═══════════════════════════════════════════════════════════════════════════════

    python3 scripts/reconcile_resolution_index.py --dry-run
        Print the plan, write nothing.

    python3 scripts/reconcile_resolution_index.py
        Apply the changes to data/doi-resolution-index.json.

The script is idempotent. Re-running after success is a no-op (it checks
version=='3.2' and exits if already at the target version).

═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import datetime
import json
import os
import sys
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RES_INDEX_PATH = REPO_ROOT / "data" / "doi-resolution-index.json"
RECEIPTS_LOG   = REPO_ROOT / "data" / "pre-overwrite-receipts.log"

OPENALEX_SRC          = REPO_ROOT / "data" / "openalex-severed-recovery.json"
DATACITE_SURV_SRC     = REPO_ROOT / "data" / "datacite-survivors-multi-heteronym.json"
ZENODO_XML_TARBALL    = REPO_ROOT / "data" / "zenodo-xml-pretermination-2026-06-07.tar.gz"
NEWLY_FOUND_SRC       = REPO_ROOT / "data" / "newly-found-openalex.json"
GHOST_RECORDS_SRC     = REPO_ROOT / "data" / "ghost-records-categorized.json"
REGISTRY_PATH         = REPO_ROOT / "data" / "registry.json"


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_receipt(message: str):
    with open(RECEIPTS_LOG, "a") as f:
        f.write(f"[{now_iso()}] reconcile_resolution_index.py: {message}\n")


def load_sources():
    """Load the recovery sources and build per-DOI lookups."""
    print("Loading sources...", flush=True)

    with open(OPENALEX_SRC) as f:
        oa_data = json.load(f)
    oa_by_doi = {r["doi"]: r for r in oa_data.get("records", []) if r.get("doi")}
    print(f"  OpenAlex: {len(oa_by_doi)} records", flush=True)

    with open(DATACITE_SURV_SRC) as f:
        surv = json.load(f)
    surv_dois = set(surv.get("dois") or [])
    print(f"  DataCite survivors: {len(surv_dois)} DOIs", flush=True)

    xml_ids = set()
    if ZENODO_XML_TARBALL.exists():
        with tarfile.open(ZENODO_XML_TARBALL, "r:gz") as tar:
            for m in tar.getmembers():
                if m.isfile() and m.name.endswith(".xml"):
                    xml_ids.add(os.path.basename(m.name)[:-4])
    print(f"  Zenodo bulk XML: {len(xml_ids)} entries", flush=True)

    with open(NEWLY_FOUND_SRC) as f:
        newly = json.load(f)
    print(f"  Newly-found CHA deposits: {newly.get('newly_found_count', 0)}", flush=True)

    with open(GHOST_RECORDS_SRC) as f:
        ghosts = json.load(f)
    misclassified = ghosts.get("misclassified_in_resolution_index") or []
    misclassified_dois = {g["doi"] for g in misclassified}
    print(f"  Misclassifications to flag: {len(misclassified_dois)}", flush=True)

    with open(REGISTRY_PATH) as f:
        reg = json.load(f)
    # Build doi → deposit lookup via registry.zenodo_dois
    doi_to_deposit = {}
    for d in reg["deposits"]:
        zd = d.get("zenodo_dois") or []
        if isinstance(zd, str):
            zd = [zd]
        for doi in zd:
            if doi and doi.startswith("10.5281/zenodo."):
                doi_to_deposit[doi] = d

    return {
        "openalex": oa_by_doi,
        "datacite_survivors": surv_dois,
        "zenodo_xml_ids": xml_ids,
        "newly_found": newly,
        "misclassified": misclassified_dois,
        "doi_to_deposit": doi_to_deposit,
    }


def classify_severance(doi, sources):
    in_survivor = doi in sources["datacite_survivors"]
    in_openalex = doi in sources["openalex"]
    rid = doi.split("zenodo.")[1] if "zenodo." in doi else None
    in_xml = rid in sources["zenodo_xml_ids"] if rid else False

    if in_survivor:
        return "retained"
    if in_openalex or in_xml:
        return "severed"
    return "unknown"


def collect_recovery_sources(doi, sources):
    out = []
    if doi in sources["openalex"]:
        out.append("openalex")
    rid = doi.split("zenodo.")[1] if "zenodo." in doi else None
    if rid and rid in sources["zenodo_xml_ids"]:
        out.append("zenodo_bulk_xml")
    if doi in sources["datacite_survivors"]:
        out.append("datacite_survivor_sweep")
    return out


def reconcile_index(dry_run=False):
    sources = load_sources()

    with open(RES_INDEX_PATH) as f:
        res = json.load(f)

    if res.get("version") == "3.2":
        print(f"\nResolution index already at v3.2. No changes.")
        return

    if res.get("version") != "3.1":
        print(f"\nWARN: resolution index is at v{res.get('version')}, not v3.1. Aborting; manual review needed.")
        sys.exit(1)

    stats = {
        "mappings_total_before": len(res["mappings"]),
        "metadata_recovered": 0,
        "misclassified_flagged": 0,
        "typo_immunity_added": 0,
        "no_change": 0,
    }

    # Pass 1: enrich each existing mapping with recovery fields
    for m in res["mappings"]:
        doi = m.get("dead_doi")
        if not doi or not doi.startswith("10.5281/zenodo."):
            stats["no_change"] += 1
            continue

        # Misclassification flag (first, because it's mutually exclusive with recovery)
        if doi in sources["misclassified"]:
            if m.get("mapping_type") != "misclassified_other_author":
                prev_mapping_type = m.get("mapping_type", "(absent)")
                m["mapping_type"] = "misclassified_other_author"
                m["misclassification_note"] = (
                    f"Title and creator on DataCite indicate this DOI belongs to a different "
                    f"depositor; was incorrectly cataloged in the resolution index during sift. "
                    f"Previous mapping_type: '{prev_mapping_type}'. Retained as historical record."
                )
                stats["misclassified_flagged"] += 1
            continue

        # Recovery enrichment
        rec_sources = collect_recovery_sources(doi, sources)
        if not rec_sources:
            stats["no_change"] += 1
            continue

        # additive only — never override existing keys we add
        added_any = False
        if "metadata_recovered_from" not in m:
            m["metadata_recovered_from"] = rec_sources
            added_any = True
        if "severance_status" not in m:
            m["severance_status"] = classify_severance(doi, sources)
            added_any = True

        # OpenAlex enrichment
        if doi in sources["openalex"]:
            rec = sources["openalex"][doi]
            if "openalex_id" not in m and rec.get("openalex_id"):
                m["openalex_id"] = rec["openalex_id"]
                added_any = True
            if "abstract_recovered_chars" not in m and rec.get("abstract"):
                m["abstract_recovered_chars"] = len(rec["abstract"])
                added_any = True

        # Sidecar pointer (only if the registry knows about this DOI)
        if "external_metadata_path" not in m and doi in sources["doi_to_deposit"]:
            d = sources["doi_to_deposit"][doi]
            hex_id = d.get("hex", "")
            m["external_metadata_path"] = f"/data/external-metadata/AXN-{hex_id}.json"
            added_any = True

        if added_any:
            stats["metadata_recovered"] += 1
        else:
            stats["no_change"] += 1

    # Pass 2: add the 2 typo-immunity mappings
    typo_dois = {
        "10.5281/zenodo.18357446": {
            "mistyped_creator": "Sharkd, Lee",
            "canonical_creator": "Sharks, Lee",
            "title": "The Mantle of the Blind Poet: Founding Document and Bestowal — Crimson Hexagon Archive",
            "date": "2026-01-24",
        },
        "10.5281/zenodo.18463722": {
            "mistyped_creator": "Craned, Rebekah",
            "canonical_creator": "Cranes, Rebekah",
            "title": "Google AI Overview: Complete Traversal of the Crimson Hexagon DOI: 10.5281/zenodo...",
            "date": "2026-02-03",
        },
    }
    existing_dois = {m["dead_doi"] for m in res["mappings"]}
    for doi, info in typo_dois.items():
        if doi in existing_dois:
            continue
        new_mapping = {
            "dead_doi": doi,
            "doi_url": f"https://doi.org/{doi}",
            "sovereign_id": "(pending Phase 4 mint)",
            "title": info["title"],
            "date": info["date"],
            "live_urls": {"datacite": f"https://api.datacite.org/dois/{doi}"},
            "status": "TYPO_IMMUNE_SURVIVOR",
            "mapping_type": "typo_immunity",
            "severance_status": "typo_immunity",
            "typo_note": (
                f"Creator string on DataCite has a one-character typo ({info['mistyped_creator']}). "
                f"Canonical heteronym is '{info['canonical_creator']}'. Likely typo at deposit time. "
                f"Record escaped account-level severance because creator name didn't match the "
                f"canonical heteronym pattern."
            ),
            "datacite_creators": [info["mistyped_creator"]],
            "datacite_state": "findable",
            "metadata_recovered_from": ["openalex", "datacite_survivor_sweep"],
            "openalex_id": (sources["openalex"].get(doi) or {}).get("openalex_id"),
        }
        res["mappings"].append(new_mapping)
        stats["typo_immunity_added"] += 1

    # Top-level updates
    new_total = len(res["mappings"])
    res["version"] = "3.2"
    res["total_mappings"] = new_total
    res["last_updated"] = now_iso()
    res["dateModified"] = now_iso()

    # Changelog entry
    cl = res.get("changelog") or []
    cl.append({
        "version": "3.2",
        "date": now_iso()[:10],
        "description": (
            f"Recovery wiring (commit 118141f7). {stats['metadata_recovered']} mappings enriched "
            f"with openalex_id + metadata_recovered_from + severance_status + external_metadata_path "
            f"+ abstract_recovered_chars. {stats['misclassified_flagged']} mappings flagged as "
            f"misclassified_other_author (mapping_type changed; full prior values preserved in "
            f"misclassification_note). {stats['typo_immunity_added']} new mappings added for "
            f"typo-immune survivors (Sharkd/Craned). total_mappings: "
            f"{stats['mappings_total_before']} → {new_total}."
        ),
    })
    res["changelog"] = cl

    print(f"\n=== Reconcile Resolution Index v3.1 → v3.2 ===")
    print(f"  Mappings before:           {stats['mappings_total_before']}")
    print(f"  Mappings after:            {new_total}")
    print(f"  Metadata-recovered flags:  +{stats['metadata_recovered']}")
    print(f"  Misclassified flags:       +{stats['misclassified_flagged']}")
    print(f"  Typo-immunity additions:   +{stats['typo_immunity_added']}")
    print(f"  Unchanged mappings:        {stats['no_change']}")

    if dry_run:
        print("\n  DRY RUN — resolution index not written")
        return

    write_receipt(
        f"v3.1 → v3.2: enriched {stats['metadata_recovered']} mappings, "
        f"flagged {stats['misclassified_flagged']} misclassifications, "
        f"added {stats['typo_immunity_added']} typo-immunity entries. "
        f"total_mappings: {stats['mappings_total_before']} → {new_total}."
    )
    # Resolution index uses indented JSON (it's hand-readable, not registry)
    with open(RES_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print(f"\n  ✓ Resolution index written to {RES_INDEX_PATH}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dry-run", action="store_true", help="Print plan, write nothing.")
    args = p.parse_args()
    reconcile_index(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
