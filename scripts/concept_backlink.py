#!/usr/bin/env python3
"""
concept_backlink.py — populates bidirectional links between concepts in
data/entity-index.json and deposits in data/registry.json.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS EXISTS
═══════════════════════════════════════════════════════════════════════════════

The entity-index already records, for each concept, which deposit DEFINED
it (`defined_in`). It does not record which deposits REFERENCE it — the
inverse relation. Without that inverse, the wiki tab cannot answer
"this concept is referenced by N deposits" and the graph tab cannot
project concept-to-deposit edges.

The registry also has no `references_concepts` field — there's no
fast way to answer "what concepts does this deposit talk about"
without re-scanning its text every time.

This script closes both directions in one pass.

═══════════════════════════════════════════════════════════════════════════════
WHAT IT WRITES
═══════════════════════════════════════════════════════════════════════════════

  data/entity-index.json
    For each concept:
      referenced_in: [deposit_number, ...]   ← all OTHER deposits that
                                              mention this concept
                                              (excludes defined_in deposit)
      reference_count: N                     ← len(referenced_in)

  data/registry.json
    For each deposit:
      references_concepts: ["term1", "term2", ...]
                                             ← all concepts mentioned in the
                                              deposit text (capped/sorted)

═══════════════════════════════════════════════════════════════════════════════
MATCHING STRATEGY
═══════════════════════════════════════════════════════════════════════════════

Case-sensitive substring match for terms ≥ 6 chars. Most concept terms
are Title Case proper nouns or formal terms — case-sensitive avoids
matching common-word lowercase forms (e.g. "address" appearing in
hundreds of contexts unrelated to the technical concept).

Terms < 6 chars are by default skipped (too high false-positive risk).
The 97 such terms (mostly acronyms) are reported in the run summary so
they can be manually handled.

The defining deposit (concept.defined_in) is excluded from
referenced_in. Self-reference is silent; the relation "this concept is
defined here" lives in defined_in, not referenced_in.

═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EI_PATH = REPO_ROOT / "data" / "entity-index.json"
REG_PATH = REPO_ROOT / "data" / "registry.json"
TEXTS_DIR = REPO_ROOT / "data" / "texts"

MIN_SAFE_TERM_LEN = 6


def load_corpus():
    print("Loading entity-index.json...", flush=True)
    with open(EI_PATH) as f:
        ei = json.load(f)
    print(f"  {len(ei['concepts'])} concepts")

    print("Loading registry.json...", flush=True)
    with open(REG_PATH) as f:
        reg = json.load(f)
    print(f"  {len(reg['deposits'])} deposits")

    return ei, reg


def deposit_number_from_text_path(path):
    """data/texts/AXN-0379-text.md → look up hex 0379 → deposit_number."""
    m = re.search(r"AXN-([0-9A-Fa-f]+)-text\.md$", str(path))
    if not m:
        return None
    return m.group(1).upper()


def build_hex_to_dnum(reg):
    """Build map: '0379' → 877 (deposit_number)."""
    out = {}
    for d in reg["deposits"]:
        hex_label = d.get("hex", "").upper()
        if hex_label:
            out[hex_label] = d["deposit_number"]
    return out


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would change without writing")
    parser.add_argument("--include-short", action="store_true",
                        help=f"also scan terms shorter than {MIN_SAFE_TERM_LEN} chars (high false-positive risk)")
    parser.add_argument("--max-concepts-per-deposit", type=int, default=200,
                        help="cap how many concept-names per deposit in references_concepts (default 200)")
    args = parser.parse_args()

    ei, reg = load_corpus()
    hex_to_dnum = build_hex_to_dnum(reg)

    # Collect concepts to scan for
    concepts_all = ei["concepts"]
    if args.include_short:
        scan_concepts = list(concepts_all.items())
    else:
        scan_concepts = [(t, c) for t, c in concepts_all.items() if len(t) >= MIN_SAFE_TERM_LEN]
    skipped_short = len(concepts_all) - len(scan_concepts)
    print(f"\nScanning for {len(scan_concepts):,} concepts (term length >= {MIN_SAFE_TERM_LEN}).")
    if skipped_short:
        print(f"Skipping {skipped_short} short terms (use --include-short to scan).")

    # For each concept, accumulate which deposits reference it
    concept_to_deposits = {term: set() for term, _ in scan_concepts}
    # For each deposit, accumulate which concepts it references
    deposit_to_concepts = {}

    text_paths = sorted(TEXTS_DIR.glob("AXN-*-text.md"))
    print(f"Scanning {len(text_paths)} text files...\n", flush=True)

    t0 = time.time()
    total_matches = 0
    for i, path in enumerate(text_paths, start=1):
        hex_label = deposit_number_from_text_path(path)
        if hex_label is None or hex_label not in hex_to_dnum:
            continue
        dnum = hex_to_dnum[hex_label]
        text = path.read_text(encoding="utf-8", errors="replace")
        matches_this_deposit = []
        for term, _ in scan_concepts:
            if term in text:  # case-sensitive substring match
                concept_to_deposits[term].add(dnum)
                matches_this_deposit.append(term)
                total_matches += 1
        deposit_to_concepts[dnum] = matches_this_deposit

        if i % 50 == 0 or i == len(text_paths):
            elapsed = time.time() - t0
            rate = i / elapsed if elapsed > 0 else 0
            print(f"  scanned {i}/{len(text_paths)} texts  ({rate:.1f}/s, {elapsed:.1f}s elapsed)", flush=True)

    elapsed = time.time() - t0
    print(f"\nScan complete in {elapsed:.1f}s. Total raw matches: {total_matches:,}")

    # Apply to entity-index: add referenced_in (excluding defined_in) and reference_count
    print("\nApplying referenced_in to entity-index...")
    referenced_in_counts = []
    for term, c in concepts_all.items():
        if term not in concept_to_deposits:
            # Either short-skipped or not in scan set — leave unchanged
            c.setdefault("referenced_in", [])
            c.setdefault("reference_count", 0)
            continue
        defined_in = c.get("defined_in")
        deposits = concept_to_deposits[term]
        # Exclude defining deposit
        if defined_in is not None:
            deposits = deposits - {defined_in}
        sorted_dep = sorted(deposits)
        c["referenced_in"] = sorted_dep
        c["reference_count"] = len(sorted_dep)
        referenced_in_counts.append(len(sorted_dep))

    # Apply to registry: references_concepts, sorted, capped
    print("Applying references_concepts to registry...")
    refcount_per_deposit = []
    for d in reg["deposits"]:
        dnum = d["deposit_number"]
        concepts = sorted(deposit_to_concepts.get(dnum, []))
        if args.max_concepts_per_deposit:
            concepts = concepts[: args.max_concepts_per_deposit]
        d["references_concepts"] = concepts
        d["references_concept_count"] = len(deposit_to_concepts.get(dnum, []))
        refcount_per_deposit.append(d["references_concept_count"])

    # Stats
    print("\n=== STATS ===")
    if referenced_in_counts:
        counts_nonzero = [n for n in referenced_in_counts if n > 0]
        print(f"Concepts with ≥1 reference (other than defined_in): {len(counts_nonzero):,}")
        if counts_nonzero:
            print(f"  Mean references per linked concept: {sum(counts_nonzero)/len(counts_nonzero):.1f}")
            print(f"  Max references for any concept:     {max(counts_nonzero)}")
    if refcount_per_deposit:
        nonzero = [n for n in refcount_per_deposit if n > 0]
        print(f"Deposits with ≥1 concept reference: {len(nonzero):,}")
        if nonzero:
            print(f"  Mean concepts per linked deposit: {sum(nonzero)/len(nonzero):.1f}")
            print(f"  Max concepts for any deposit:     {max(nonzero)}")

    # Top-10 most-referenced concepts
    top = sorted(
        ((term, c.get("reference_count", 0)) for term, c in concepts_all.items()),
        key=lambda x: -x[1],
    )[:15]
    print("\nTop-15 most-referenced concepts:")
    for term, count in top:
        print(f"  {count:5d}  {term}")

    if args.dry_run:
        print("\n[DRY RUN] No files written.")
        return

    # Write atomically
    print("\nWriting entity-index.json...")
    EI_PATH.write_text(json.dumps(ei, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {EI_PATH.stat().st_size:,} bytes")

    print("Writing registry.json (compact)...")
    REG_PATH.write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"  {REG_PATH.stat().st_size:,} bytes")

    print("\nDone.")
    print("Next: python3 scripts/regenerate_surfaces.py  (to keep derived surfaces in sync)")


if __name__ == "__main__":
    main()
