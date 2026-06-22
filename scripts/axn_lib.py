"""
axn_lib.py — canonical AXN identifier generation for Alexanarch.

The AXN format is:
    AXN:<HEX>.<FAMILY>.<EMOJI>

Where:
    HEX     — uppercase hex label (label, not necessarily hex of deposit_number)
    FAMILY  — semantic family from {GOVERNANCE, EMPIRICAL, GENERATIVE, ARCHIVAL,
              PHILOLOGICAL, STRUCTURAL, COMPOSITIONAL, OPERATIVE, HETERONYMIC,
              MPAI, UNCLASSIFIED}
    EMOJI   — 6-emoji canonical glyph, derived from the first 6 bytes of the
              SHA-256 of the canonical bytes (title + creator + description + body).

The 256-glyph AXN_GLYPHS table maps each byte value (0..255) to a Unicode
emoji. The 256-entry CLUSTERS table maps the same bytes to a semantic cluster
name. Both arrays are CANONICAL — they are the authoritative source for both
the mint workflow and any Python tooling.

Schema version: AXN v2 (6-emoji from first 6 bytes of SHA-256).
The earlier AXN v1 used 4 emoji from the first 4 bytes; the workflow drift to
v1 occurred independently and was corrected on 2026-06-22.
"""

AXN_SCHEMA_VERSION = "v2"
AXN_BYTES_USED = 6

AXN_GLYPHS = [
    "🌑", "🌒", "🌓", "🌔",
    "🌕", "🌖", "🌗", "🌘",
    "⭐", "🌟", "💫", "☀️",
    "🌙", "🪐", "🌍", "🌊",
    "🔥", "💧", "🌪️", "⚡",
    "❄️", "🌋", "🏔️", "🌿",
    "🍃", "🌱", "🌾", "🪨",
    "💎", "🧊", "🌈", "☁️",
    "🏛️", "🏗️", "🧱", "🪜",
    "🚪", "🪟", "🏠", "🏰",
    "⛩️", "🕌", "🗼", "🌉",
    "⚓", "🛡️", "🔔", "🏺",
    "🔧", "🔩", "⚙️", "🔗",
    "🪝", "🧲", "⚖️", "🔬",
    "🔭", "🧪", "🧫", "🧬",
    "💡", "🔮", "🪄", "🗝️",
    "📜", "📖", "📝", "✏️",
    "🖊️", "📋", "📌", "📎",
    "🔖", "📚", "🗂️", "📦",
    "🏷️", "🪧", "📐", "📏",
    "🧭", "🗺️", "🏴", "🚩",
    "⛳", "🎯", "🔍", "👁️",
    "🔎", "🪞", "🗡️", "🛤️",
    "⛵", "🚀", "🛸", "🌀",
    "⌛", "⏰", "🕐", "🕑",
    "🕒", "🕓", "🕔", "🕕",
    "🕖", "🕗", "🕘", "🕙",
    "🕚", "🕛", "⌛", "🔄",
    "🌸", "🌺", "🌻", "🌹",
    "🍀", "🌲", "🌳", "🍁",
    "🍂", "🍄", "🐚", "🪸",
    "🦋", "🐝", "🕊️", "🦅",
    "♠️", "❤️", "♦️", "♣️",
    "🎭", "🎪", "🎨", "🎵",
    "🎶", "🎹", "🎻", "🎺",
    "🥁", "🎲", "🃏", "🀄",
    "➕", "➖", "✖️", "➗",
    "♾️", "∮", "⊕", "⊗",
    "△", "▽", "◇", "○",
    "●", "□", "■", "▲",
    "🜁", "🝊", "☿", "♃",
    "♄", "♅", "♆", "☉",
    "☽", "♈", "♉", "♊",
    "♋", "♌", "♍", "♎",
    "👁‍🗨", "🤲", "👐", "🙏",
    "✊", "🤝", "👆", "👇",
    "👈", "👉", "🫵", "🖐️",
    "✋", "🫶", "🤙", "👋",
    "🚨", "🔴", "🟠", "🟡",
    "🟢", "🔵", "🟣", "⚪",
    "⚫", "🟤", "💜", "💙",
    "💚", "💛", "🧡", "❤️",
    "🔺", "🔻", "◀️", "▶️",
    "🔼", "🔽", "⏩", "⏪",
    "⏫", "⏬", "↗️", "↘️",
    "↙️", "↖️", "🔃", "🔀",
    "🌅", "🌄", "🌃", "🌆",
    "🌇", "🏙️", "🌌", "🎆",
    "🎇", "✨", "🌠", "💥",
    "🔆", "🔅", "⭕", "❌",
    "🏁", "🎬", "🔚", "🔙",
    "🔛", "🔝", "🔜", "⏹️",
    "⏏️", "🔒", "🔓", "🔐",
    "🗿", "🪦", "♻️", "∞",
]

assert len(AXN_GLYPHS) == 256, f"AXN_GLYPHS must have 256 entries, has {len(AXN_GLYPHS)}"

CLUSTERS = [
    "Celestial", "Celestial", "Celestial", "Celestial",
    "Celestial", "Celestial", "Celestial", "Celestial",
    "Celestial", "Celestial", "Celestial", "Celestial",
    "Celestial", "Celestial", "Celestial", "Celestial",
    "Elemental", "Elemental", "Elemental", "Elemental",
    "Elemental", "Elemental", "Elemental", "Elemental",
    "Elemental", "Elemental", "Elemental", "Elemental",
    "Elemental", "Elemental", "Elemental", "Elemental",
    "Architectural", "Architectural", "Architectural", "Architectural",
    "Architectural", "Architectural", "Architectural", "Architectural",
    "Architectural", "Architectural", "Architectural", "Architectural",
    "Architectural", "Architectural", "Architectural", "Architectural",
    "Instrumental", "Instrumental", "Instrumental", "Instrumental",
    "Instrumental", "Instrumental", "Instrumental", "Instrumental",
    "Instrumental", "Instrumental", "Instrumental", "Instrumental",
    "Instrumental", "Instrumental", "Instrumental", "Instrumental",
    "Scriptural", "Scriptural", "Scriptural", "Scriptural",
    "Scriptural", "Scriptural", "Scriptural", "Scriptural",
    "Scriptural", "Scriptural", "Scriptural", "Scriptural",
    "Scriptural", "Scriptural", "Scriptural", "Scriptural",
    "Navigational", "Navigational", "Navigational", "Navigational",
    "Navigational", "Navigational", "Navigational", "Navigational",
    "Navigational", "Navigational", "Navigational", "Navigational",
    "Navigational", "Navigational", "Navigational", "Navigational",
    "Temporal", "Temporal", "Temporal", "Temporal",
    "Temporal", "Temporal", "Temporal", "Temporal",
    "Temporal", "Temporal", "Temporal", "Temporal",
    "Temporal", "Temporal", "Temporal", "Temporal",
    "Organic", "Organic", "Organic", "Organic",
    "Organic", "Organic", "Organic", "Organic",
    "Organic", "Organic", "Organic", "Organic",
    "Organic", "Organic", "Organic", "Organic",
    "Symbolic", "Symbolic", "Symbolic", "Symbolic",
    "Symbolic", "Symbolic", "Symbolic", "Symbolic",
    "Symbolic", "Symbolic", "Symbolic", "Symbolic",
    "Symbolic", "Symbolic", "Symbolic", "Symbolic",
    "Mathematical", "Mathematical", "Mathematical", "Mathematical",
    "Mathematical", "Mathematical", "Mathematical", "Mathematical",
    "Mathematical", "Mathematical", "Mathematical", "Mathematical",
    "Mathematical", "Mathematical", "Mathematical", "Mathematical",
    "Alchemical", "Alchemical", "Alchemical", "Alchemical",
    "Alchemical", "Alchemical", "Alchemical", "Alchemical",
    "Alchemical", "Alchemical", "Alchemical", "Alchemical",
    "Alchemical", "Alchemical", "Alchemical", "Alchemical",
    "Gestural", "Gestural", "Gestural", "Gestural",
    "Gestural", "Gestural", "Gestural", "Gestural",
    "Gestural", "Gestural", "Gestural", "Gestural",
    "Gestural", "Gestural", "Gestural", "Gestural",
    "Signal", "Signal", "Signal", "Signal",
    "Signal", "Signal", "Signal", "Signal",
    "Signal", "Signal", "Signal", "Signal",
    "Signal", "Signal", "Signal", "Signal",
    "Structural", "Structural", "Structural", "Structural",
    "Structural", "Structural", "Structural", "Structural",
    "Structural", "Structural", "Structural", "Structural",
    "Structural", "Structural", "Structural", "Structural",
    "Liminal", "Liminal", "Liminal", "Liminal",
    "Liminal", "Liminal", "Liminal", "Liminal",
    "Liminal", "Liminal", "Liminal", "Liminal",
    "Liminal", "Liminal", "Liminal", "Liminal",
    "Terminal", "Terminal", "Terminal", "Terminal",
    "Terminal", "Terminal", "Terminal", "Terminal",
    "Terminal", "Terminal", "Terminal", "Terminal",
    "Terminal", "Terminal", "Terminal", "Terminal",
]

assert len(CLUSTERS) == 256, f"CLUSTERS must have 256 entries, has {len(CLUSTERS)}"


# Cluster reading -> 1-word semantic family name for the 6-glyph reading
CLUSTER_READINGS = {
    "Celestial": "Origin",
    "Elemental": "Force",
    "Architectural": "Foundation",
    "Instrumental": "Method",
    "Scriptural": "Text",
    "Navigational": "Search",
    "Temporal": "Duration",
    "Organic": "Growth",
    "Symbolic": "Play",
    "Mathematical": "Proof",
    "Alchemical": "Transmutation",
    "Gestural": "Touch",
    "Signal": "Alarm",
    "Structural": "Direction",
    "Liminal": "Threshold",
    "Terminal": "Closure",
}


def axn_glyph_from_hash(sha256_hex):
    """Given the full SHA-256 hex digest of canonical bytes, return the
    canonical 6-emoji AXN glyph.
    """
    if len(sha256_hex) < 12:
        raise ValueError(f"sha256_hex too short: {len(sha256_hex)} chars (need >=12)")
    # First 6 bytes = first 12 hex chars
    bytes_used = bytes.fromhex(sha256_hex[:12])
    return "".join(AXN_GLYPHS[b] for b in bytes_used)


def axn_clusters_from_hash(sha256_hex):
    """Given the full SHA-256 hex digest, return the 6-element cluster list."""
    if len(sha256_hex) < 12:
        raise ValueError(f"sha256_hex too short")
    bytes_used = bytes.fromhex(sha256_hex[:12])
    return [CLUSTERS[b] for b in bytes_used]


def axn_reading_from_clusters(clusters):
    """Given a clusters list, return the human-readable 'Origin -> Force -> ...' reading."""
    return " -> ".join(CLUSTER_READINGS.get(c, c) for c in clusters)


def compose_axn(hex_label, family, glyph):
    """Compose a full AXN string: AXN:<HEX>.<FAMILY>.<EMOJI>"""
    return f"AXN:{hex_label}.{family}.{glyph}"


def derive_axn(sha256_hex, hex_label, family):
    """Convenience: derive full canonical AXN from sha256 + position + family."""
    return compose_axn(hex_label, family, axn_glyph_from_hash(sha256_hex))


# Sanity self-tests, run when imported
def _selftest():
    # 6 emoji
    g = axn_glyph_from_hash("0123456789abcdef" + "0" * 48)
    # First 6 bytes: 0x01 0x23 0x45 0x67 0x89 0xab
    expected = AXN_GLYPHS[0x01] + AXN_GLYPHS[0x23] + AXN_GLYPHS[0x45] + AXN_GLYPHS[0x67] + AXN_GLYPHS[0x89] + AXN_GLYPHS[0xab]
    assert g == expected, f"glyph derivation broken: got {g}, want {expected}"
    # Clusters
    cs = axn_clusters_from_hash("00" * 32)
    assert len(cs) == 6, f"clusters should be 6, got {len(cs)}"
    # All-zero bytes -> all Celestial
    assert cs == ["Celestial"] * 6, f"expected all Celestial, got {cs}"


_selftest()
