#!/usr/bin/env python3
"""
build_lexical_overlay.py — derive data/lexical-overlay.json from LMR + entity-index + semantic-addresses.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS EXISTS
═══════════════════════════════════════════════════════════════════════════════

/lexical/ currently fetches lexical-minting-registry.json alone (3.52 MB).
Each term card shows term, definition, type, defining-deposit link — nothing
about engagement.

But we have richer per-term data already on disk:

  entity-index.json carries — for the 7,045 LMR terms that survived noise
  filtering into the curated concept layer — engagement_type, reference_count,
  defined_in (deposit number), entity_triples count, classified status.

  semantic-addresses.json carries — for the 348 concepts also tested as
  canonical queries — observation_class distribution and observation counts.

Naively fetching entity-index from /lexical/ would push the page from 3.52 MB
to ~8.5 MB. So instead, we precompute a small overlay file with ONLY the
fields the lexical surface needs, indexed by term name.

═══════════════════════════════════════════════════════════════════════════════
WHAT IT WRITES
═══════════════════════════════════════════════════════════════════════════════

data/lexical-overlay.json
  {
    "version": "1.0",
    "generated_at": "<iso8601>",
    "source_files": ["lmr (sha256 head)", "ei (sha256 head)", "sa (sha256 head)"],
    "stats": {
      "lmr_terms": N,
      "engaged": N,                 # in both LMR and entity-index
      "raw_only": N,                # LMR-only
      "ei_only": N,
      "addressed": N,               # with at least one semantic address
    },
    "overlay": {
      "<term>": {
        "engaged": bool,                       # in entity-index?
        "engagement_type": str,                # minted / specified / developed / ...
        "reference_count": int,                # Phase C
        "entity_triples_count": int,
        "classified": bool,
        "concept_type": str,                   # extracted / specification / structural / ...
        "address_count": int,                  # how many canonical queries point here
        "address_classes": {                   # class distribution (only if address_count > 0)
          "subjunctive": N,
          "observed_address": N,
          "verified_non_address": N,
          "unrated": N
        }
      },
      ...
    }
  }

Terms NOT in the overlay are by definition LMR-only (raw, not yet curated).
The /lexical/ page treats absence as "raw" — no special engagement display.

═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LMR_PATH = REPO_ROOT / "data" / "lexical-minting-registry.json"
EI_PATH = REPO_ROOT / "data" / "entity-index.json"
SA_PATH = REPO_ROOT / "data" / "semantic-addresses.json"
OUT_PATH = REPO_ROOT / "data" / "lexical-overlay.json"


def sha256_head(path):
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    return h[:16]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true",
                        help="report stats without writing")
    args = parser.parse_args()

    print("Loading data/lexical-minting-registry.json ...", flush=True)
    lmr = json.loads(LMR_PATH.read_text())
    lmr_terms_set = {t["term"] for t in lmr.get("terms", [])}
    print(f"  {len(lmr_terms_set):,} unique terms")

    print("Loading data/entity-index.json ...", flush=True)
    ei = json.loads(EI_PATH.read_text())
    ei_concepts = ei.get("concepts", {})
    print(f"  {len(ei_concepts):,} concepts")

    print("Loading data/semantic-addresses.json ...", flush=True)
    sa = json.loads(SA_PATH.read_text())
    addresses = sa.get("addresses", {})
    print(f"  {len(addresses):,} addresses")

    # Build address-by-concept index: concept_name -> [list of observation_class]
    address_by_concept = {}
    for addr in addresses.values():
        for ref in addr.get("refers_to", []):
            address_by_concept.setdefault(ref, []).append(addr.get("observation_class") or "unrated")

    # Build the overlay
    overlay = {}
    for term in (set(lmr_terms_set) & set(ei_concepts.keys())):
        c = ei_concepts[term]
        entry = {
            "engaged": True,
            "engagement_type": c.get("engagement_type") or "unclassified",
            "reference_count": int(c.get("reference_count") or 0),
            "entity_triples_count": len(c.get("entity_triples") or []),
            "classified": bool(c.get("classified")),
            "concept_type": c.get("type") or "unknown",
            "defined_in": c.get("defined_in"),
        }
        if term in address_by_concept:
            classes = address_by_concept[term]
            entry["address_count"] = len(classes)
            entry["address_classes"] = dict(Counter(classes))
        overlay[term] = entry

    # Stats
    raw_only = len(lmr_terms_set - set(ei_concepts.keys()))
    ei_only = len(set(ei_concepts.keys()) - lmr_terms_set)
    addressed = sum(1 for v in overlay.values() if "address_count" in v)

    stats = {
        "lmr_terms": len(lmr_terms_set),
        "engaged": len(overlay),
        "raw_only": raw_only,
        "ei_only": ei_only,
        "addressed": addressed,
    }

    out = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_files": {
            "lexical_minting_registry": sha256_head(LMR_PATH),
            "entity_index": sha256_head(EI_PATH),
            "semantic_addresses": sha256_head(SA_PATH),
        },
        "stats": stats,
        "overlay": overlay,
    }

    print("\n=== STATS ===")
    for k, v in stats.items():
        print(f"  {k:18s} {v:>8,}")

    # Engagement-type distribution among engaged terms
    eng_types = Counter(v["engagement_type"] for v in overlay.values())
    print("\nEngagement type distribution (among engaged terms):")
    for et, n in eng_types.most_common():
        print(f"  {et:18s} {n:>8,}")

    # Address-class distribution across addressed terms
    if addressed:
        all_classes = Counter()
        for v in overlay.values():
            if "address_classes" in v:
                all_classes.update(v["address_classes"])
        print(f"\nAddress-class distribution (across {addressed} addressed concepts):")
        for cls, n in all_classes.most_common():
            print(f"  {cls:25s} {n:>8,}")

    if args.dry_run:
        # estimate output size
        size = len(json.dumps(out, ensure_ascii=False).encode("utf-8"))
        compact_size = len(json.dumps(out, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        print(f"\n[DRY RUN] Would write {size:,} bytes pretty / {compact_size:,} bytes compact to {OUT_PATH}")
        return

    # Write compact (this is data, like the other registry chunks)
    OUT_PATH.write_text(
        json.dumps(out, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"\nWrote {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
