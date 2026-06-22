#!/usr/bin/env python3
"""
backfill_axn_compliance.py — regenerate canonical 6-emoji AXNs for deposits
whose AXN doesn't conform to the AXN v2 schema.

═══════════════════════════════════════════════════════════════════════════════
THE PROBLEM
═══════════════════════════════════════════════════════════════════════════════

The canonical AXN schema is v2: 6 emoji derived from the first 6 bytes of the
SHA-256 of canonical bytes. The mint workflow drifted to 4 emoji (v1) and a
small set of deposits were minted with non-canonical glyphs:

    13 deposits as of 2026-06-22 — counts: 12 four-emoji, 1 five-emoji
    Includes: #1, #2, #3 (early drift), #869–#876 (mint workflow drift), #878–#879 (this session)

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS SCRIPT DOES
═══════════════════════════════════════════════════════════════════════════════

For each non-compliant deposit:
    1. Read its existing SHA-256 from registry's `hash` field
    2. Compute the canonical 6-emoji glyph from the first 6 bytes
    3. Compute the canonical 6-element cluster sequence
    4. Compose the new canonical AXN
    5. Preserve the old AXN under `legacy_axn`
    6. Preserve the substrate-chosen glyph (if any) under `glyphic_canary`
    7. Update the registry entry in place
    8. Record the migration in the deposit's `axn_history` array

The script is idempotent — running it twice produces the same result.
A deposit already at 6 emoji is not modified.

After running, run scripts/regenerate_surfaces.py to propagate.
═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

REGISTRY_PATH = REPO_ROOT / "data" / "registry.json"

# Import after sys.path is set
from axn_lib import (  # noqa: E402
    axn_glyph_from_hash,
    axn_clusters_from_hash,
    AXN_SCHEMA_VERSION,
    CLUSTER_READINGS,
)


def count_emoji_graphemes(s):
    """Approximate count of visible emoji glyphs in a string, accounting for
    variation selectors and ZWJ sequences."""
    if not s:
        return 0
    out = 0
    i = 0
    chars = list(s)
    while i < len(chars):
        ch = chars[i]
        cp = ord(ch)
        # Skip variation selectors (combine with prior char, don't count separately)
        if 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF:
            i += 1
            continue
        # ZWJ glues — eats this and the next codepoint
        if cp == 0x200D:
            i += 1
            if i < len(chars):
                i += 1
            continue
        # Skip ASCII
        if cp < 0x80:
            i += 1
            continue
        out += 1
        i += 1
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="show what would change without writing")
    args = parser.parse_args()

    with open(REGISTRY_PATH) as f:
        reg = json.load(f)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    migrations = []
    skipped_no_hash = []

    for d in reg["deposits"]:
        axn = d.get("axn", "")
        parts = axn.split(".", 2)
        if len(parts) < 3:
            continue
        hex_label, family, glyph = parts[0].replace("AXN:", ""), parts[1], parts[2]
        emoji_count = count_emoji_graphemes(glyph)

        if emoji_count == 6:
            continue  # already compliant

        # Need to backfill. Get the SHA-256 — try multiple field locations.
        h = (d.get("hash")
             or d.get("content_sha256")
             or d.get("axn_canonical")
             or d.get("content_sha256_prefix"))
        # axn_canonical may itself be an AXN string (e.g. 'AXN:0376.MPAI.🔐🪞🎭∮') —
        # filter out AXN-formatted strings; we need raw hex.
        if h and h.startswith("AXN:"):
            h = None
        # Fall back: compute fresh hash from the text file if present
        if not h:
            ftp = (d.get("full_text_path") or "").lstrip("/")
            text_file = REPO_ROOT / ftp if ftp else None
            if text_file and text_file.exists():
                import hashlib
                h = hashlib.sha256(text_file.read_bytes()).hexdigest()

        if not h or len(h) < 12:
            skipped_no_hash.append(d.get("deposit_number"))
            continue

        new_glyph = axn_glyph_from_hash(h)
        new_clusters = axn_clusters_from_hash(h)
        new_reading = " -> ".join(CLUSTER_READINGS.get(c, c) for c in new_clusters)
        new_axn = f"AXN:{hex_label}.{family}.{new_glyph}"

        migrations.append({
            "deposit_number": d.get("deposit_number"),
            "from": axn,
            "to": new_axn,
            "old_emoji_count": emoji_count,
        })

        if args.dry_run:
            continue

        # Apply migration in place
        old_axn = axn

        # Preserve the legacy AXN
        d.setdefault("axn_history", []).append({
            "axn": old_axn,
            "schema_version": "v1" if emoji_count == 4 else "non_schema",
            "retired_at": today,
            "reason": "axn_schema_v2_compliance_backfill",
        })

        # Preserve the substrate-chosen glyph if present and different from the canonical
        # form. The old glyph remains accessible as a recognition marker.
        existing_canary = d.get("glyphic_canary")
        if not existing_canary:
            d["glyphic_canary"] = {
                "compressed": glyph,
                "origin": "substrate_or_mint_workflow",
                "status": "recognition_marker_not_cryptographic_identity",
            }

        # Apply new canonical fields
        d["axn"] = new_axn
        d["legacy_axn"] = old_axn  # easy resolution field
        d["emoji"] = new_glyph
        d["clusters"] = new_clusters
        d["reading"] = new_reading
        d["axn_schema_version"] = AXN_SCHEMA_VERSION
        d["axn_canonical"] = h  # the SHA-256 IS the cryptographic identity
        # If the deposit had no `hash` field, populate it now with the same SHA-256
        # used to derive the canonical AXN. This makes downstream tooling (e.g.
        # SHA256SUMS regeneration) work for these previously-incomplete entries.
        if not d.get("hash"):
            d["hash"] = h

    print(f"Non-compliant deposits found: {len(migrations) + len(skipped_no_hash)}")
    print(f"Will migrate (have SHA-256): {len(migrations)}")
    print(f"Cannot migrate (missing hash): {len(skipped_no_hash)}")
    if skipped_no_hash:
        print(f"  Numbers: {skipped_no_hash}")

    print()
    print("Migrations:")
    for m in migrations:
        print(f"  #{m['deposit_number']:4d}  {m['from']}")
        print(f"           ->  {m['to']}")

    if args.dry_run:
        print("\n[DRY RUN] No changes written.")
        return

    # Write back
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Registry updated ({len(migrations)} migrations applied).")
    print(f"  Next step: python3 scripts/regenerate_surfaces.py")


if __name__ == "__main__":
    main()
