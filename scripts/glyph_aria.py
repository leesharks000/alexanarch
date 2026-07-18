#!/usr/bin/env python3
"""glyph_aria.py — accessible/machine-parseable labels for AXN glyph sequences.

The six-emoji glyph is the AXN's human-verifiable checksum. To screen readers
and text-only parsers, an unlabeled emoji run is noise or silence. This module
derives an aria-label that names each glyph character via the Unicode Character
Database, making the checksum pronounceable and machine-parseable without
changing the visible rendering.

Usage:
    from glyph_aria import axn_aria_label
    axn_aria_label("AXN:0455.ARCHIVAL.🧫∞🍃⏪🧡♄")
    -> "AXN 0455 ARCHIVAL. Glyph checksum: petri dish, infinity, leaf
        fluttering in wind, black left-pointing double triangle, orange
        heart, saturn."

Variation selectors (U+FE0F etc.) and zero-width joiners are skipped; they
modify presentation, not identity.
"""
import unicodedata

_SKIP = {"\ufe0e", "\ufe0f", "\u200d"}  # variation selectors, ZWJ


def glyph_names(glyph: str) -> list:
    """Name each meaningful character in a glyph sequence."""
    names = []
    for ch in glyph:
        if ch in _SKIP:
            continue
        try:
            names.append(unicodedata.name(ch).lower())
        except ValueError:
            names.append(f"U+{ord(ch):04X}")
    return names


def axn_aria_label(axn: str) -> str:
    """Full accessible label for an AXN string of the form HEX.FAMILY.GLYPH."""
    body = axn[4:] if axn.startswith("AXN:") else axn
    parts = body.split(".", 2)
    if len(parts) == 3:
        hex_id, family, glyph = parts
        names = glyph_names(glyph)
        return (f"AXN {hex_id} {family}. Glyph checksum: "
                + ", ".join(names) + ".")
    return f"AXN {body}"


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print(axn_aria_label(arg))
