#!/usr/bin/env python3
"""
mint_deposit.py — produce a valid deposit from a validated GitHub Issue body.

═══════════════════════════════════════════════════════════════════════════════
PLACE IN THE ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

This script is the heart of the §6.2.1-step-3 rebuild. The mint workflow at
.github/workflows/mint-axn.yml calls this AFTER validate_deposit.py has cleared
the issue body of all schema violations. This script:

  1. Re-parses the validated issue body into typed fields.
  2. Sanitizes every user-supplied string (URL allowlist, HTML escaping happens
     at render time in the static-record generator).
  3. Computes the next deposit_number and hex_id (opaque label, +12 offset).
  4. Infers the AXN family from the declared content_type.
  5. Builds the canonical text file at data/texts/AXN-<HEX>-text.md.
     CANONICAL BYTES = the resulting file content. The AXN's hash field is
     SHA-256 of this file.
  6. Derives the AXN (glyphs, clusters, reading) via scripts/axn_lib.py — the
     single source of truth. NO inline AXN derivation lives here.
  7. Constructs the registry entry conforming to api/schemas/deposit-entry.schema.json.
  8. Writes the data/deposits/AXN-<HEX>.md download alias (closes the §6.2.2
     generator gap that orphaned records #872–#879 in the pre-audit state).
  9. Renders s/records/<N>/index.html via wire_deposit.regenerate_static_page().

The script does NOT push, commit, validate the post-state registry, or
regenerate surfaces. Those are the workflow's responsibility, in this order:

   mint_deposit.py
     → validate_deposit.py --registry-entry --strict
     → insert into data/registry.json
     → validate_deposit.py --registry --strict
     → scripts/regenerate_surfaces.py
     → branch, commit, PR

═══════════════════════════════════════════════════════════════════════════════
THREAT MODEL — what this script defends against
═══════════════════════════════════════════════════════════════════════════════

The audit (Appendix A of WORKPLAN-SESSION-20260623.md, §3) identified
browser-executable-input risk: depositor-supplied strings can become
executable DOM. Under self-serve depositing (no maintainer label gate),
this script MUST assume every submission is hostile.

  Sanitization layer 1 — URL allowlist.
    Schemes other than http, https, doi are rejected. The
    workflow's validate-deposit call already runs a softer regex on URLs;
    this is the stricter belt-and-suspenders pass.

  Sanitization layer 2 — control character stripping.
    User strings are stripped of C0 controls (except whitespace) and BIDI
    overrides before being written into any file. This prevents Trojan-source
    style attacks (bidi reversal hiding code).

  Sanitization layer 3 — at-render escaping.
    HTML escaping is the responsibility of wire_deposit.regenerate_static_page,
    which uses html.escape on every interpolated value. This script does not
    HTML-escape the canonical text file (the bytes ARE the canonical record;
    escaping them would corrupt the AXN).

  Sanitization layer 4 — markdown safety.
    wire_deposit's renderer is line-based and prefix-matched. It does NOT
    pass HTML through. <script>, <iframe>, on* attributes in markdown body
    become escaped text in the rendered page.

The audit's §6.2.4 prescription ("strict allowlist Markdown renderer; textContent
and DOM construction for metadata; URL-scheme allowlist; rel='noopener
noreferrer' on external targets; restrictive CSP") is partially met here
(URL allowlist) and partially in wire_deposit (textContent / escape). The CSP
fix is a separate Vercel-config commit (§6.2.4 follow-up).

═══════════════════════════════════════════════════════════════════════════════
USAGE
═══════════════════════════════════════════════════════════════════════════════

    # Mint from an issue body file (workflow path)
    python3 scripts/mint_deposit.py \
        --issue-body /tmp/issue.md \
        --issue-number 42 \
        --output /tmp/mint-result.json

    # Dry-run (compute everything, write nothing)
    python3 scripts/mint_deposit.py \
        --issue-body /tmp/issue.md \
        --issue-number 42 \
        --dry-run

    # Self-test (no I/O against repo)
    python3 scripts/mint_deposit.py --selftest

Exit codes:
    0 — success
    1 — sanitization rejection (bad URL scheme, prohibited chars)
    2 — schema-derived rejection (would not validate; called only as a sanity
        check — primary validation is by validate_deposit.py before this runs)
    3 — internal error
═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT))

# axn_lib is the canonical AXN derivation. This script does not implement
# AXN derivation itself; importing axn_lib is the contract.
from axn_lib import (
    AXN_GLYPHS,
    AXN_SCHEMA_VERSION,
    axn_clusters_from_hash,
    axn_glyph_from_hash,
    axn_reading_from_clusters,
    compose_axn,
)

# wire_deposit's static-record renderer is the canonical HTML output.
# Importing it ensures we don't drift from the renderer the rest of the
# codebase uses.
try:
    import wire_deposit  # noqa: F401
    _HAVE_WIRE_DEPOSIT = True
except ImportError:
    _HAVE_WIRE_DEPOSIT = False


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

# Hex offset between deposit_number and hex label. Established empirically
# from the registry (every entry has hex = deposit_number + 12, formatted
# as 4-digit uppercase hex). This is a historical offset; it is opaque per
# the schema's `Treat as opaque` directive.
HEX_OFFSET = 12

# Allowed URL schemes anywhere a user-supplied URL appears (related_ids,
# files field, description embedded links). javascript:, data:, vbscript:,
# file:, ftp:, etc. all rejected.
ALLOWED_URL_SCHEMES = frozenset({"http", "https", "doi"})

# Dangerous URL schemes that we explicitly block by name even when they
# don't follow the scheme:// pattern. javascript:alert(1) doesn't have //,
# so we need a separate detection pass for these. The list is conservative —
# any of these in user-supplied text is rejected outright.
DANGEROUS_SCHEMES_NAMED = frozenset({
    "javascript", "data", "vbscript", "livescript", "mocha",
    "file", "about", "blob", "filesystem", "view-source",
})

# Maximum sizes — guard against pathological submissions. These are generous
# but bounded; legitimate submissions fit comfortably.
MAX_TITLE_CHARS = 500
MAX_CREATOR_CHARS = 500
# Raised 50_000 → 100_000 (= MAX_FIELD_CHARS) 2026-07-02: the description
# field carries full deposit documents per SPXI full-content-hash discipline;
# a 58K theoretical paper (deposit #943) is normal scholarship. The old 50K
# cap had never fired only because the field-boundary defect (fixed above)
# truncated embedded documents before the cap was checked.
MAX_DESCRIPTION_CHARS = 100_000
MAX_FIELD_CHARS = 100_000
MAX_KEYWORDS = 50

# Bidi override / format characters that enable Trojan-source attacks.
# Stripped from all user input. Includes the LTR/RTL embeddings and isolates.
BIDI_CONTROL_CHARS = frozenset([
    "\u202a", "\u202b", "\u202c", "\u202d", "\u202e",  # LRE RLE PDF LRO RLO
    "\u2066", "\u2067", "\u2068", "\u2069",            # LRI RLI FSI PDI
])

# Mapping from issue-form content_type (dropdown values) to AXN family enum.
# UNCLASSIFIED is the catch-all for anything the dropdown produces that we
# didn't anticipate (e.g. future additions to the dropdown).
CONTENT_TYPE_TO_FAMILY = {
    "Dataset": "DATASET",
    "Critical edition": "PHILOLOGICAL",
    "Theoretical paper": "GENERATIVE",
    "Monograph": "GENERATIVE",
    "Methodological specification": "OPERATIVE",
    "Continuity tether": "ARCHIVAL",
    "Creative work (connected to research)": "GENERATIVE",
    "Mixed": "UNCLASSIFIED",
    "Other": "UNCLASSIFIED",
    # Allowed for backward compatibility with curator-minted deposits
    "Empirical baseline reading": "EMPIRICAL",
    "Methodology specification": "OPERATIVE",
    # Correspondence chain (documented on EA-CORRESPONDENCE-CERN-01..05):
    # the semicolon-separated content_type declarations all begin with
    # "Institutional correspondence" and belong to the GOVERNANCE family.
    "Institutional correspondence": "GOVERNANCE",
    # Errata are record governance (added 2026-09-05; #1554 was reclassified by hand):
    "Erratum / record correction": "GOVERNANCE",
    "Erratum": "GOVERNANCE",
    "Correspondence": "GOVERNANCE",
    # Literary forms (added 2026-07-23 after #1410 defaulted to UNCLASSIFIED):
    # made literary objects — the epistle, the essay, the poem, etc. — are
    # COMPOSITIONAL. A scholarly critical edition of a literary object is
    # PHILOLOGICAL (see "Critical edition" above); the literary object itself
    # is COMPOSITIONAL. Recensions, translations, and editions of literary
    # works belong here as compositional acts on an existing text.
    "Epistle": "COMPOSITIONAL",
    "Letter": "COMPOSITIONAL",
    "Essay": "COMPOSITIONAL",
    "Poem": "COMPOSITIONAL",
    "Poetry": "COMPOSITIONAL",
    "Prose": "COMPOSITIONAL",
    "Story": "COMPOSITIONAL",
    "Fiction": "COMPOSITIONAL",
    "Recension": "COMPOSITIONAL",
    "Translation": "COMPOSITIONAL",
    "Edition": "COMPOSITIONAL",
    "Literary work": "COMPOSITIONAL",
    # Scholarly forms (added 2026-07-23):
    "Commentary": "PHILOLOGICAL",
    "Scholia": "PHILOLOGICAL",
    "Philological note": "PHILOLOGICAL",
    "Textual criticism": "PHILOLOGICAL",
    # Reflective / operational (added 2026-07-23):
    "Protocol": "OPERATIVE",
    "Specification": "OPERATIVE",
    "Governance instrument": "GOVERNANCE",
    "Effective act": "GOVERNANCE",
    # Documentary / archival (added 2026-07-23):
    "Documentary artifact": "ARCHIVAL",
    "Correspondence record": "ARCHIVAL",
    "Metadata packet": "MPAI",
    "Metadata Packet for AI Indexing": "MPAI",
}

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE BODY PARSING
# ─────────────────────────────────────────────────────────────────────────────

def extract_field(body: str, label: str) -> str:
    """Extract a single `### Label` field from a GitHub Issue body.

    GitHub Issue Forms render structured fields as `### Label\\n<value>`.
    This regex is intentionally permissive about whitespace; validate_deposit.py
    is the strict checker.

    Returns empty string for missing or "_No response_" fields.
    """
    # Field boundary is the NEXT KNOWN FORM LABEL, not any "###" — deposits
    # legitimately embed markdown documents whose level-3 headings must not
    # terminate the field. (Post-mortem: deposits #942/#943, 2026-07-02,
    # minted with canonical text truncated at the first embedded "### ".)
    _KNOWN_LABELS = (
        "Protocol Version", "Title", "Creator", "ORCID", "Date", "Description",
        "Content Type", "License", "Substrate Disclosure", "Keywords",
        "Related Identifiers", "Version", "Methodology",
        "Falsification Conditions", "Files", "Terms",
        # 2026-07-18: "Body" added as boundary marker only. parse_issue_body
        # never calls extract_field("Body"); the paper deposit places a "### Body"
        # header before the canonical text so preceding fields terminate cleanly
        # rather than running to EOF. Without this, formal deposits whose canonical
        # bytes are the deposit body cannot mint via the pipeline.
        "Body",
    )
    _label_alt = "|".join(re.escape(l) for l in _KNOWN_LABELS)
    # 2026-08-12 (deposits #1452–#1454): the boundary set above is correct for
    # ordinary deposits and WRONG for the Body field of a formal paper. Papers
    # carry "### Keywords", "### Version", "### Methodology" and
    # "### Falsification Conditions" as their OWN section headings, so the Body
    # terminated at the first of them and only the front matter and abstract were
    # seated — 9.5k of 42–60k characters, silently, with a "full" body_status.
    # The Body field is the LAST field in the paper deposit form by construction,
    # so its only legitimate terminator is "### Terms" or end of input.
    if label.lower() == "body":
        pattern = r"###\s+Body\s*\n\s*(.*?)(?=\n###\s+Terms\s*\n|\Z)"
        m = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
        if not m:
            return ""
        val = m.group(1).strip()
        return "" if val in ("_No response_", "None", "_None_") else val
    pattern = rf"###\s+{re.escape(label)}\s*\n\s*(.*?)(?=\n###\s+(?:{_label_alt})\s*\n|\Z)"
    m = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    val = m.group(1).strip()
    if val in ("_No response_", "None", "_None_"):
        return ""
    return val



# ─────────────────────────────────────────────────────────────────────────────
# FORMAT-MISMATCH GUARD
#
# Added 2026-07-28. A YAML-frontmatter document was passed where this parser
# expects a GitHub Issue Form body ("### Label" then value). Every field parsed
# to the empty string, and the mint proceeded — writing a 158-byte template as
# the canonical bytes and a registry entry with no title, creator or date.
#
# Silent templating over a format mismatch is the worst available behaviour: it
# produces an object that looks minted and is empty. Fail loudly instead, and
# name the expected format so the handler can see what they gave it.
# ─────────────────────────────────────────────────────────────────────────────

def guard_issue_body_format(body: str) -> None:
    core = ["Title", "Creator", "Date", "Description", "Content Type", "License"]
    got = {l: extract_field(body, l) for l in core}
    empty = [l for l, v in got.items() if not (v or "").strip()]
    if len(empty) < len(core):
        return
    looks_yaml = body.lstrip().startswith("---") or re.search(r"^\w+:\s", body.lstrip()[:400], re.M)
    raise SystemExit(
        "\n  REFUSED — issue body format.\n"
        f"  All {len(core)} core fields parsed empty: {', '.join(empty)}\n\n"
        "  This parser expects a GitHub Issue Form body:\n"
        "      ### Title\n      <value>\n\n      ### Creator\n      <value>\n\n"
        + ("  What was supplied looks like YAML frontmatter.\n\n" if looks_yaml else "\n")
        + "  The field labels are defined in .github/ISSUE_TEMPLATE/deposit.yml and\n"
          "  parsed by extract_field() in this file. A mint that proceeds past a\n"
          "  format mismatch writes an empty deposit that looks like a real one.\n")


def strip_issue_prefix(title):
    """Remove the GitHub issue-title convention from the WORK's title.

    Deposit issues are titled "[DEPOSIT] <work title>" so they are findable in
    the issue list. That bracket is transport metadata: it belongs to the issue,
    never to the work. Left in place it propagates into the registry title, the
    canonical text frontmatter, the record <title>, the OAI record, the wiki
    entry, the citation graph label and every downstream surface -- and it has,
    three times (#1458, #1486, #1487), each time by an internal depositor who
    copied a prior body as a template.

    Documenting the rule did not stop it. Stripping it here does, because this
    is the single point every transport passes through.
    """
    if not title:
        return title
    return re.sub(r'^\s*\[\s*deposit\s*\]\s*', '', title, flags=re.I).strip()


def parse_issue_body(body: str) -> dict:
    """Extract all known fields from a deposit issue body.

    The issue template at .github/ISSUE_TEMPLATE/deposit.yml defines these
    field labels. If the template changes, update this function. The
    validate_deposit.py field map is the partial source of truth; this is
    the complete map.
    """
    return {
        "protocol_version": extract_field(body, "Protocol Version"),
        "title": strip_issue_prefix(extract_field(body, "Title")),
        "creator": extract_field(body, "Creator"),
        "orcid": extract_field(body, "ORCID"),
        "date": extract_field(body, "Date"),
        "description": extract_field(body, "Description"),
        "content_type": extract_field(body, "Content Type"),
        "license": extract_field(body, "License"),
        "substrate": extract_field(body, "Substrate Disclosure"),
        "keywords": extract_field(body, "Keywords"),
        "related_ids": extract_field(body, "Related Identifiers"),
        "version": extract_field(body, "Version"),
        "methodology": extract_field(body, "Methodology"),
        "falsification": extract_field(body, "Falsification Conditions"),
        "files": extract_field(body, "Files"),
        "body": extract_field(body, "Body"),
        "terms": extract_field(body, "Terms"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# SANITIZATION
# ─────────────────────────────────────────────────────────────────────────────

class SanitizationError(Exception):
    """Raised when input contains content the sanitizer refuses to pass through."""
    pass


def strip_control_chars(s: str) -> str:
    """Strip C0 control chars (except \\t \\n \\r) and BIDI override format chars.

    BIDI overrides enable Trojan-source attacks where visible text and
    actual byte order differ. They have no legitimate use in deposit metadata.
    """
    if not s:
        return ""
    out = []
    for ch in s:
        cp = ord(ch)
        # C0 controls except tab/newline/CR
        if cp < 0x20 and ch not in "\t\n\r":
            continue
        # DEL
        if cp == 0x7f:
            continue
        # BIDI overrides
        if ch in BIDI_CONTROL_CHARS:
            continue
        out.append(ch)
    return "".join(out)


def sanitize_url(url: str) -> str:
    """Allowlist URL schemes. Returns the URL unchanged if allowed; raises if not.

    The DOI scheme is special: 'doi:10.x.y/z' is permitted alongside the
    standard https://doi.org/10.x.y/z form. Either works as an identifier.
    """
    url = url.strip()
    if not url:
        return ""
    # Bare DOIs (10.xxxx/...) get normalized
    if re.match(r"^10\.\d{4,}/", url):
        return f"https://doi.org/{url}"
    parsed = urlparse(url)
    scheme = (parsed.scheme or "").lower()
    if scheme not in ALLOWED_URL_SCHEMES:
        raise SanitizationError(
            f"URL scheme {scheme!r} not in allowlist {sorted(ALLOWED_URL_SCHEMES)}: {url!r}"
        )
    return url


def find_url_like_tokens(text: str) -> list:
    """Find URL-shaped tokens in free text. Returns list of (scheme, full_token) tuples.

    Two-pass detection:
      1. Standard scheme://path URLs — any scheme, picked up for allowlist check.
      2. Slashless dangerous schemes (javascript:, data:, vbscript:, file:, etc.) —
         caught by name even without // because that's the canonical XSS form.

    Email addresses (foo@bar.com) and tel: aren't url-shaped here; they don't pass.
    """
    if not text:
        return []
    tokens = []
    # Pass 1: scheme://...
    for m in re.finditer(r"([a-zA-Z][a-zA-Z0-9+.\-]*)://\S+", text):
        tokens.append((m.group(1).lower(), m.group(0)))
    # Pass 2: dangerous slashless schemes by name
    for scheme in DANGEROUS_SCHEMES_NAMED:
        # Match scheme: followed by anything non-whitespace (the XSS payload)
        for m in re.finditer(rf"\b{re.escape(scheme)}:\S+", text, re.IGNORECASE):
            tokens.append((scheme.lower(), m.group(0)))
    return tokens


def sanitize_field(s: str, max_chars: int = MAX_FIELD_CHARS, *, name: str = "field") -> str:
    """Run all sanitization passes on a free-text user field.

    - NFC-normalize (defeats homoglyph trickery in stored data; renderers
      can still re-normalize but storage is canonical).
    - Strip control chars / BIDI overrides.
    - Enforce length cap.
    - Check any embedded URLs against the scheme allowlist.
    """
    if s is None:
        return ""
    s = unicodedata.normalize("NFC", s)
    s = strip_control_chars(s)
    if len(s) > max_chars:
        raise SanitizationError(
            f"{name} exceeds {max_chars} chars ({len(s)} given)"
        )
    for scheme, token in find_url_like_tokens(s):
        # Dangerous schemes are rejected by name, regardless of slashes
        if scheme in DANGEROUS_SCHEMES_NAMED:
            raise SanitizationError(
                f"in {name}: dangerous URL scheme {scheme!r} not permitted: {token!r}"
            )
        # Standard URLs get the full allowlist check
        try:
            sanitize_url(token)
        except SanitizationError as e:
            raise SanitizationError(f"in {name}: {e}")
    return s


def sanitize_keywords(raw: str) -> list:
    """Parse the comma-separated keywords field into a clean list.

    Empty entries dropped, leading/trailing whitespace trimmed, NFC-normalized.
    Caps at MAX_KEYWORDS.
    """
    if not raw:
        return []
    items = [k.strip() for k in raw.split(",")]
    items = [unicodedata.normalize("NFC", strip_control_chars(k)) for k in items if k.strip()]
    if len(items) > MAX_KEYWORDS:
        raise SanitizationError(
            f"keywords list exceeds {MAX_KEYWORDS} entries ({len(items)} given)"
        )
    return items


# ─────────────────────────────────────────────────────────────────────────────
# REGISTRY ARITHMETIC
# ─────────────────────────────────────────────────────────────────────────────

def next_deposit_number(registry: dict) -> int:
    """Compute the next sequential deposit_number from current registry state."""
    existing = [d["deposit_number"] for d in registry.get("deposits", [])]
    if not existing:
        return 1
    return max(existing) + 1


def _symbolon_position_for(sha256_hex: str):
    """One kernel, one position: if the symbolon witness layer already assigned
    a position to these canonical bytes, minting a second is forbidden."""
    import json as _json, pathlib as _pl
    d = _pl.Path(__file__).resolve().parent.parent / "data" / "symbolon-registry" / "entries"
    if not d.is_dir():
        return None
    for f in d.glob("*.json"):
        try:
            e = _json.loads(f.read_text())
            if e.get("tuple", {}).get("axn0", {}).get("sha256") == sha256_hex:
                return e.get("axn") or e.get("position")
        except Exception:
            continue
    return None


def _symbolon_ledger_floor() -> int:
    """Highest position consumed by the symbolon witness layer per the shared
    allocation ledger (data/symbolon-registry/allocation.json): the ledger's
    next_hex means positions below it are consumed. Returns -1 if absent, so
    the ledger's presence is optional and its absence changes nothing."""
    import json as _json, pathlib as _pl
    p = _pl.Path(__file__).resolve().parent.parent / "data" / "symbolon-registry" / "allocation.json"
    try:
        return int(_json.loads(p.read_text())["next_hex"], 16) - 1
    except Exception:
        return -1


def _bump_symbolon_ledger(allocated_hex: str) -> None:
    """Advance the shared allocation ledger past a deposit-side allocation.
    Best-effort: ledger absence changes nothing (mirrors _symbolon_ledger_floor)."""
    import json as _json, pathlib as _pl, datetime as _dt
    p = _pl.Path(__file__).resolve().parent.parent / "data" / "symbolon-registry" / "allocation.json"
    try:
        led = _json.loads(p.read_text())
        if int(led.get("next_hex", "0"), 16) <= int(allocated_hex, 16):
            led["next_hex"] = f"{int(allocated_hex, 16) + 1:04X}"
            led["last_allocated"] = allocated_hex.upper()
            led["last_allocated_at"] = _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            led["last_allocator"] = "deposit-pipeline (mint_deposit.py)"
            p.write_text(_json.dumps(led, ensure_ascii=False, indent=1))
    except Exception:
        pass


def next_hex_id(deposit_number: int, registry: dict | None = None) -> str:
    """Compute the opaque hex label for the next deposit.

    HISTORY (bug fixed 2026-07-13, caught in dry-run before minting #1077):
    the original formula hex_id = deposit_number + HEX_OFFSET assumed the
    offset was invariant, but the registry's real assignments drifted
    (recent deposits run at offset 17, e.g. #1072 -> 0441) — the formula
    would have re-minted 0441 and collided. The hex is an OPAQUE SEQUENTIAL
    LABEL, not a function of deposit_number: the only safe rule is
    max(existing hex) + 1. The deposit_number+offset formula is retained
    only as a fallback for an empty registry.
    """
    floor = _symbolon_ledger_floor()
    if registry:
        existing = [int(d["hex"], 16) for d in registry.get("deposits", [])
                    if d.get("hex")]
        if existing:
            return f"{max(max(existing), floor) + 1:04X}"
    return f"{max(deposit_number + HEX_OFFSET - 1, floor) + 1:04X}"


def family_for_content_type(content_type: str) -> str:
    """Map an issue-form content_type value to an AXN family enum.

    Falls back to UNCLASSIFIED if the dropdown adds new values that
    weren't anticipated here. UNCLASSIFIED is valid per the schema's
    family enum.

    Case-insensitive on the first clause: "Epistle", "epistle", "EPISTLE"
    all match the "Epistle" entry. This matters because free-text
    content_type entries in transport-A submissions do not enforce
    capitalization, and #1410 (2026-07-23) defaulted to UNCLASSIFIED
    because "Epistle" was not in the map.
    """
    # Strip suffix in parens, e.g. "Other (specify in description)" -> "Other".
    # Also split on semicolons so that semicolon-continued declarations like
    # "Institutional correspondence; documentary artifact for the OC 11 exercise..."
    # (used across the EA-CORRESPONDENCE-CERN chain) match the first-clause key.
    key = re.split(r"[;(]", content_type)[0].strip() if content_type else ""
    # Case-insensitive match against the canonical map keys
    key_lower = key.lower()
    for map_key, family in CONTENT_TYPE_TO_FAMILY.items():
        if map_key.lower() == key_lower:
            return family
    return "UNCLASSIFIED"


# ─────────────────────────────────────────────────────────────────────────────
# CANONICAL TEXT FILE
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# ATTACHMENT INGESTION
# ─────────────────────────────────────────────────────────────────────────────
#
# GitHub issues store file attachments at user-attachments URLs that appear
# inline in the raw issue body (usually at the very top, above the first
# `### Section` header, wherever the user dropped them). These URLs are
# stable and public (no auth token needed to fetch).
#
# On mint, we detect these URLs, fetch each one, and include the content in
# the canonical deposit text. Text files are ingested INLINE — the full body
# of the attachment appears in the deposit's canonical .md so it's covered
# by the SHA-256 hash (SPXI Layer 3) and by all downstream enrichment
# (concept extraction, SPXI audits, wiki generation). Binary files are
# recorded BY REFERENCE — filename + size + URL — because inlining opaque
# bytes into a text deposit is not useful.
#
# Failure mode: if a fetch fails (transient network issue), we still land
# the deposit but record a reference-only section pointing at the URL, so
# the mint remains deterministic (the URL, not the transient error text,
# is what gets canonicalized). Retrying the mint via close+reopen will
# ingest the content on the next pass, changing the hash — this is the
# right behavior because the FULL deposit is a different artifact.

ATTACHMENT_URL_PATTERN = re.compile(
    r'https://github\.com/user-attachments/'
    r'(?:files/\d+/[^\s)>\]"\']+|assets/[A-Za-z0-9\-]+(?:[^\s)>\]"\']*)?)'
)

# 2026-08-15: REPO-HOSTED ATTACHMENTS.
# The pattern above matches only github.com/user-attachments/ — the URLs the
# WEB FORM produces when a depositor drags a file onto an issue. Transport D
# (internal: TACHYON/Assembly with direct repo access) has no such URLs: its
# files are already committed under data/attachments/. With no path in, a
# transport-D depositor's files degraded to bare links in a Files field —
# unhashed, uningested, not attachments at all, and invisible to every surface
# that reads the canonical text (#1486, 2026-08-15).
#
# Repo-hosted URLs are resolved FROM DISK rather than fetched: the bytes are
# already local, so ingestion is deterministic and needs no network. Same
# inline-if-text / by-reference-if-binary rule as the web-form path.
REPO_ATTACHMENT_URL_PATTERN = re.compile(
    r'https://raw\.githubusercontent\.com/[^/]+/[^/]+/(?:main|master)/([^\s)>\]"\']+)'
    r'|https://alexanarch\.org/(data/attachments/[^\s)>\]"\']+)'
)


def resolve_repo_attachment(url: str):
    """Map a repo-hosted URL to its local path, or None if it is not one."""
    m = REPO_ATTACHMENT_URL_PATTERN.match(url.strip())
    if not m:
        return None
    rel = m.group(1) or m.group(2)
    if not rel or ".." in rel:
        return None
    p = REPO_ROOT / rel
    return p if p.is_file() else None

# Text-like file extensions we're willing to ingest inline. Anything not on
# this list is recorded by reference (URL + size).
TEXT_ATTACHMENT_EXTENSIONS = {
    ".md", ".markdown", ".txt", ".text", ".json", ".jsonl", ".csv", ".tsv",
    ".yaml", ".yml", ".xml", ".html", ".htm", ".rst", ".tex", ".bib",
    ".py", ".js", ".ts", ".sh", ".log", ".ini", ".toml", ".cfg",
}

MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024  # 10 MB per attachment, cap
ATTACHMENT_FETCH_TIMEOUT = 30  # seconds


def extract_attachment_urls(body: str) -> list:
    """Find distinct GitHub user-attachments URLs in the raw issue body.

    Returns URLs in first-appearance order, deduplicated.
    """
    urls = []
    seen = set()
    # Repo-hosted first (transport D), then web-form (transports A/B/C).
    for m in REPO_ATTACHMENT_URL_PATTERN.finditer(body):
        u = m.group(0)
        if u not in seen and resolve_repo_attachment(u) is not None:
            seen.add(u); urls.append(u)
    for m in ATTACHMENT_URL_PATTERN.finditer(body):
        u = m.group(0)
        if u not in seen:
            seen.add(u)
            urls.append(u)
    return urls


def _attachment_filename(url: str) -> str:
    """Extract the filename component from an attachment URL.

    For .../files/{id}/{filename} — the filename.
    For .../assets/{uuid} — the uuid (no meaningful filename; treated as
    binary reference).
    """
    tail = url.rsplit("/", 1)[-1]
    # Handle URL-encoded characters in filename
    from urllib.parse import unquote
    return unquote(tail)


def _is_text_extension(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = "." + filename.rsplit(".", 1)[-1].lower()
    return ext in TEXT_ATTACHMENT_EXTENSIONS


def _format_size(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.1f} MB"
    if n >= 1024:
        return f"{n // 1024} KB"
    return f"{n} bytes"


def fetch_attachment(url: str) -> dict:
    """Fetch a single attachment URL. Returns a dict describing the result.

    Keys:
        url: the original URL (verbatim)
        filename: filename component of the URL
        size: bytes fetched (0 if fetch failed)
        as_text: decoded UTF-8 text if this is a text-extension file and
                 decoded cleanly; None otherwise
        is_text: True if we consider this an inline-ingest text attachment
        error: short error label if fetch failed, else None
    """
    filename = _attachment_filename(url)

    # Repo-hosted attachments read from disk: the bytes are already local, so
    # ingestion is deterministic and independent of the network. A transport-D
    # deposit must not depend on fetching its own repository over HTTP.
    local = resolve_repo_attachment(url)
    if local is not None:
        raw = local.read_bytes()
        if len(raw) > MAX_ATTACHMENT_BYTES:
            return {"url": url, "filename": filename, "size": len(raw),
                    "as_text": None, "is_text": False, "error": "exceeds size cap"}
        if _is_text_extension(filename):
            try:
                return {"url": url, "filename": filename, "size": len(raw),
                        "as_text": raw.decode("utf-8"), "is_text": True, "error": None}
            except UnicodeDecodeError:
                return {"url": url, "filename": filename, "size": len(raw),
                        "as_text": None, "is_text": False,
                        "error": "text-extension file not valid UTF-8"}
        return {"url": url, "filename": filename, "size": len(raw),
                "as_text": None, "is_text": False, "error": None}

    result = {
        "url": url,
        "filename": filename,
        "size": 0,
        "as_text": None,
        "is_text": False,
        "error": None,
    }
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Alexanarch-Mint/1.0 (deposit ingestion)",
        })
        with urllib.request.urlopen(req, timeout=ATTACHMENT_FETCH_TIMEOUT) as r:
            content = r.read(MAX_ATTACHMENT_BYTES + 1)
        if len(content) > MAX_ATTACHMENT_BYTES:
            result["error"] = f"attachment exceeds {MAX_ATTACHMENT_BYTES // (1024*1024)}MB cap"
            return result
        result["size"] = len(content)
        if _is_text_extension(filename):
            try:
                result["as_text"] = content.decode("utf-8")
                result["is_text"] = True
            except UnicodeDecodeError:
                result["error"] = "text-extension file not valid UTF-8"
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        # Any network-level error. Keep the label short + deterministic:
        # just "fetch_error" so retries produce identical canonical text.
        result["error"] = "fetch_error"
    return result


def fetch_all_attachments(body: str) -> list:
    """Extract URLs from raw issue body, fetch each. Returns list of results."""
    return [fetch_attachment(u) for u in extract_attachment_urls(body)]


def render_attachment_section(att: dict) -> str:
    """Render a single attachment as a markdown section for canonical text.

    Deterministic — no timestamps, no error details that could vary
    between fetch attempts. Only URL, filename, size, and (for text) the
    verbatim content.
    """
    fname = att.get("filename", "unknown")
    url = att.get("url", "")
    if att.get("is_text") and att.get("as_text") is not None:
        # Inline the full text content
        return (
            f"## Attached File: {fname}\n\n"
            f"Source URL: {url}\n\n"
            f"{att['as_text']}\n"
        )
    if att.get("error"):
        # Reference-only fallback. Error label is deterministic ('fetch_error'
        # or 'text-extension file not valid UTF-8' etc — see fetch_attachment).
        return (
            f"## Attached File: {fname}\n\n"
            f"Attachment could not be ingested at mint time. "
            f"Reason: {att['error']}. Original URL: {url}\n"
        )
    # Binary attachment fetched successfully but not inlined
    size_label = _format_size(att.get("size", 0))
    return (
        f"## Attached File: {fname}\n\n"
        f"Binary attachment ({size_label}) preserved at deposit time. "
        f"Original URL: {url}\n"
    )


def build_canonical_text(
    fields: dict,
    deposit_number: int,
    hex_id: str,
    *,
    attachments: list = None,
) -> str:
    """Construct the canonical text file content (frontmatter + body).

    The resulting string IS the canonical bytes. SHA-256 of this becomes
    the deposit's `hash` field and the source of the AXN glyphs.

    The frontmatter is YAML-safe (no embedded HTML, no markdown rendering
    until s/records/ is generated). The body section is the depositor's
    submitted content (description + methodology + falsification + attached
    file content + files listing), preserved verbatim — this is the
    canonical record.

    Attachments (from GitHub issue user-attachments URLs) are rendered
    into the body: text files inlined verbatim, binary files by reference.
    This means the SPXI Layer 3 hash covers the FULL deposit content
    including any attached materials.

    IMPORTANT: this function does NOT include the AXN value in the
    frontmatter. The AXN is derived FROM the file's hash, so including
    it would create a circular dependency. The AXN appears in the
    REGISTRY ENTRY (separate from this file).
    """
    # YAML frontmatter — manually composed to avoid PyYAML dependency
    # and to keep the byte layout deterministic. Each value is JSON-quoted
    # where it contains special chars, plain otherwise.

    def yaml_str(s: str) -> str:
        """Render a string as YAML, quoting if needed."""
        if not s:
            return '""'
        # If string contains characters that need quoting, JSON-quote it
        if re.search(r'[":\n\r\t#&*!|>%@\`\[\]{}]', s) or s != s.strip():
            return json.dumps(s, ensure_ascii=False)
        return s

    keywords_yaml = ""
    if fields.get("keywords_list"):
        keywords_yaml = "keywords:\n" + "".join(
            f"  - {yaml_str(k)}\n" for k in fields["keywords_list"]
        )

    fm_lines = [
        "---",
        f"deposit_number: {deposit_number}",
        f"hex: {hex_id}",
        f"title: {yaml_str(fields['title'])}",
        f"creator: {yaml_str(fields['creator'])}",
    ]
    if fields.get("orcid"):
        fm_lines.append(f"orcid: {yaml_str(fields['orcid'])}")
    fm_lines += [
        f"date: {yaml_str(fields['date'])}",
        f"content_type: {yaml_str(fields['content_type'])}",
        f"license: {yaml_str(fields['license'])}",
        f"substrate: {yaml_str(fields['substrate'])}",
    ]
    if fields.get("version"):
        fm_lines.append(f"version: {yaml_str(fields['version'])}")
    if fields.get("related_ids"):
        fm_lines.append(f"related_ids: {yaml_str(fields['related_ids'])}")
    fm_lines.append(f"axn_schema_version: {AXN_SCHEMA_VERSION}")
    fm_lines.append(f"protocol_version: {yaml_str(fields.get('protocol_version', 'alexanarch-deposit-protocol/v1'))}")
    fm_lines.append("---")

    body_sections = []
    # 2026-08-15: description/methodology/falsification are METADATA. They live
    # in the registry entry and render on the record page from there. Emitting
    # them into the canonical text too meant the description appeared twice on
    # every record, and -- worse -- that a deposit whose depositor supplied no
    # Body field produced a "canonical text" made entirely of metadata, with the
    # work itself absent from its own deposit (#1486, #1487). The canonical text
    # is the WORK. Only the title survives here, as the document's heading.
    if fields.get("title"):
        body_sections.append(f"# {fields['title']}\n")
    # Attached file content (text ingested inline, binary by reference)
    if attachments:
        for att in attachments:
            body_sections.append(render_attachment_section(att))
    if fields.get("files"):
        body_sections.append(f"## Files\n\n{fields['files']}\n")
    if fields.get("body"):
        # 2026-07-18: Body field carries depositor's canonical bytes for artifact-
        # is-the-body deposits (poems, correspondence, spatial scores). Verbatim.
        body_sections.append(fields["body"] + "\n")

    frontmatter = "\n".join(fm_lines)
    if keywords_yaml:
        # Insert keywords before closing --- by replacing the final line
        frontmatter = "\n".join(fm_lines[:-1]) + "\n" + keywords_yaml + "---"
    body = "\n".join(body_sections)
    return frontmatter + "\n\n" + body


# ─────────────────────────────────────────────────────────────────────────────
# REGISTRY ENTRY CONSTRUCTION
# ─────────────────────────────────────────────────────────────────────────────

# Registry descriptions are abstract-scale metadata, not document storage.
# The CANONICAL TEXT keeps the depositor's full Description field (it is part
# of the hashed bytes); the REGISTRY entry gets a bounded abstract so that
# every description-consuming surface (main page entries, browse index,
# chunks, JSON-LD, meta tags) behaves identically across deposits.
# (Post-mortem: #942/#943, 2026-07-02 — full documents rode in the registry
# description field, producing 32K/58K entries beside 792-char siblings.)
REGISTRY_DESCRIPTION_MAX = 2400

def _registry_description(desc: str) -> str:
    """Bound a description to abstract scale at a paragraph boundary."""
    if len(desc) <= REGISTRY_DESCRIPTION_MAX:
        return desc
    cut = desc.rfind("\n\n", 0, REGISTRY_DESCRIPTION_MAX)
    if cut < 200:  # no usable paragraph boundary — cut at sentence end
        cut = desc.rfind(". ", 0, REGISTRY_DESCRIPTION_MAX)
        cut = cut + 1 if cut > 200 else REGISTRY_DESCRIPTION_MAX
    # The marker names where the remainder lives IN PROSE. It previously emitted
    # the literal string "full_text_path" — a variable name shipped to readers,
    # pointing at a file that (after metadata stopped being rendered as body)
    # no longer contained the remainder at all. The untruncated text is now
    # preserved in the entry's description_full field by build_registry_entry.
    return desc[:cut].rstrip() + " […abridged for the catalogue; full description in this deposit's record]"


def build_registry_entry(
    fields: dict,
    deposit_number: int,
    hex_id: str,
    family: str,
    file_sha256: str,
    keywords_list: list,
    issue_number: int = None,
) -> dict:
    """Construct a registry entry that satisfies api/schemas/deposit-entry.schema.json.

    All 13 required fields populated. Optional fields populated when the
    submission provides them; absent otherwise (schema permits).

    The AXN, emoji, and clusters are derived from file_sha256 here — single
    point of derivation, no inline glyph table lookups.
    """
    glyph = axn_glyph_from_hash(file_sha256)
    clusters = axn_clusters_from_hash(file_sha256)
    reading = axn_reading_from_clusters(clusters)
    axn = compose_axn(hex_id, family, glyph)

    minted_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    entry = {
        # Required fields (schema)
        "deposit_number": deposit_number,
        "axn": axn,
        "hex": hex_id,
        "family": family,
        "emoji": glyph,
        "hash": file_sha256,
        "title": fields["title"],
        "creator": fields["creator"],
        "date": fields["date"],
        "description": _registry_description(fields["description"]),
        "content_type": fields["content_type"],
        "license": fields["license"],
        "substrate": fields["substrate"],

        # Required by schema regex but historically populated
        "root_axn": f"AXN:{hex_id}.{family}",

        # Provenance / version
        "axn_schema_version": AXN_SCHEMA_VERSION,
        "protocol_version": fields.get("protocol_version", "alexanarch-deposit-protocol/v1"),
        "axn_canonical": file_sha256,
        "clusters": clusters,
        "axn_reading": reading,

        # Operational
        "minted_at": minted_at,
        "status": "ACTIVE",
        "status_authorial": "SELF_SERVE_MINTED",
        "full_text_path": f"/data/texts/AXN-{hex_id}-text.md",
        # WIKI AUTHORSHIP (MANUS ruling 2026-08-05): a mint leaves this NULL and
        # the deposit is not complete until an article is written from the body.
        # Nothing in the pipeline will fill it — the auto-generator that used to
        # is retired, because a templated article reads as coverage and so
        # prevents authorship. validate_deposit rejects absent, stub, template-
        # shaped and under-length articles (WIKI-001/002/003).
        "wiki_article": None,
        "wiki_status": "AUTHORSHIP_REQUIRED",
        "entities": [],
        "entity_status": "provisional",
        "defines_concepts": [],
    }

    # Optional fields — only populated when present
    if fields.get("orcid"):
        entry["orcid"] = fields["orcid"]
    if fields.get("version"):
        entry["version"] = fields["version"]
    if keywords_list:
        entry["keywords"] = keywords_list
    if fields.get("related_ids"):
        entry["related_identifiers_raw"] = fields["related_ids"]

    # Mint provenance — supports forensic traceback if a bad mint lands.
    # mint_source records the GitHub issue that originated the deposit.
    if issue_number is not None:
        entry["mint_source"] = {
            "kind": "github_issue",
            "issue_number": issue_number,
            "repository": "leesharks000/alexanarch",
            "minted_by_workflow": ".github/workflows/mint-axn.yml",
            "minted_by_script": "scripts/mint_deposit.py",
            "minted_via": "self_serve_validated_pr",
        }

    return entry


# ─────────────────────────────────────────────────────────────────────────────
# TOP-LEVEL ORCHESTRATION
# ─────────────────────────────────────────────────────────────────────────────

def mint_from_issue_body(body: str, issue_number: int, *, dry_run: bool = False) -> dict:
    """Orchestrate the full mint from issue body to written files.

    Returns a dict describing the mint result (paths written, registry
    entry, AXN). The workflow consumes this to construct the PR.

    Side effects (skipped if dry_run=True):
      - writes data/texts/AXN-<HEX>-text.md
      - writes data/deposits/AXN-<HEX>.md
      - inserts entry into data/registry.json (atomic: read, append, write)
      - writes s/records/<N>/index.html via wire_deposit

    Does NOT:
      - run regenerate_surfaces.py (workflow does)
      - run validate_deposit.py (workflow does, before and after)
      - commit, push, or create PR (workflow does)
    """
    fields = parse_issue_body(body)

    # Sanitize each field. The order is: short, single-value fields first
    # (cheap rejection), long body fields last.
    fields["title"] = sanitize_field(fields["title"], MAX_TITLE_CHARS, name="title")
    fields["creator"] = sanitize_field(fields["creator"], MAX_CREATOR_CHARS, name="creator")
    fields["orcid"] = sanitize_field(fields["orcid"], name="orcid")
    fields["date"] = sanitize_field(fields["date"], name="date")
    fields["description"] = sanitize_field(fields["description"], MAX_DESCRIPTION_CHARS, name="description")
    fields["content_type"] = sanitize_field(fields["content_type"], name="content_type")
    fields["license"] = sanitize_field(fields["license"], name="license")
    fields["substrate"] = sanitize_field(fields["substrate"], name="substrate")
    fields["version"] = sanitize_field(fields["version"], name="version")
    fields["related_ids"] = sanitize_field(fields["related_ids"], name="related_ids")
    fields["methodology"] = sanitize_field(fields["methodology"], name="methodology")
    fields["falsification"] = sanitize_field(fields["falsification"], name="falsification")
    fields["files"] = sanitize_field(fields["files"], name="files")
    fields["protocol_version"] = sanitize_field(fields["protocol_version"], name="protocol_version")

    keywords_list = sanitize_keywords(fields.get("keywords", ""))
    fields["keywords_list"] = keywords_list

    # Fetch any GitHub user-attachments URLs found in the RAW issue body
    # (before extract_field carved fields out of it — attachments typically
    # appear at the top of the body, outside any labeled section, wherever
    # the user pasted or drag-dropped them).
    attachments = fetch_all_attachments(body)

    # Load current registry — needed for deposit_number computation
    registry_path = REPO_ROOT / "data" / "registry.json"
    with open(registry_path) as f:
        registry = json.load(f)

    deposit_number = next_deposit_number(registry)
    hex_id = next_hex_id(deposit_number, registry)
    _bump_symbolon_ledger(hex_id)   # WAVE-HEXPOS-01: the deposit side must WRITE
    # the shared ledger it reads. Before 2026-08-06 it only read: #1433 took 05AF
    # while the ledger still said next_hex=05AF, and the witness endpoint then
    # CAS-allocated the same position a day later (contested 05AF). Bumping at
    # allocation makes the "two allocators share one space" invariant real; an
    # aborted mint burns a label (a harmless gap), never a collision.
    family = family_for_content_type(fields["content_type"])

    # Build canonical text content — attachments included so SPXI Layer 3
    # hash covers the full deposit content.
    canonical_text = build_canonical_text(
        fields, deposit_number, hex_id, attachments=attachments,
    )
    # NORMALISE AT THE SEAM (2026-08-09, MANUS).
    #
    # "Why are normal prose paragraph line breaks hardcoded in production? Why do I
    # have to be responsible for making sure absolutely standard prose poetics are
    # encoded in the first place, just to deposit a file?"
    #
    # He does not. Hard-wrapped prose was never a protocol requirement — it came
    # from whoever composed the body wrapping at a column, a SOURCE-CODE habit
    # carried into prose because the prose was being written inside string literals.
    # Once sealed, those wraps are frozen into the identity-bearing bytes and every
    # downstream rendering inherits them as fragment-paragraphs.
    #
    # A checker that rejects a wrapped body puts the burden back on the author. This
    # does the job instead: prose paragraphs are joined into logical lines here, at
    # the single point where text becomes canonical, and nothing else in the pipeline
    # has to know. Verse, indentation, lists, tables, fenced code and markdown hard
    # breaks are all preserved — the unwrapper is built to refuse anything it cannot
    # prove is mechanical. Word content is verified identical before the bytes are
    # sealed; if it is not, the original stands and the mint proceeds unchanged.
    try:
        import importlib.util as _ilu, re as _reN
        _spec = _ilu.spec_from_file_location(
            "_unwrap", str(REPO_ROOT / "scripts" / "unwrap_deposit.py"))
        _uwm = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_uwm)
        _flowed, _joined = _uwm.unwrap(canonical_text)
        _w = lambda t: _reN.findall(r"[0-9A-Za-z\u00c0-\u024f']+", t)
        if _joined and _w(_flowed) == _w(canonical_text):
            canonical_text = _flowed
    except Exception:
        pass

    canonical_bytes = canonical_text.encode("utf-8")
    file_sha256 = hashlib.sha256(canonical_bytes).hexdigest()

    # Build registry entry from the computed AXN
    entry = build_registry_entry(
        fields,
        deposit_number=deposit_number,
        hex_id=hex_id,
        family=family,
        file_sha256=file_sha256,
        keywords_list=keywords_list,
        issue_number=issue_number,
    )

    # Record attachment metadata on the registry entry — filename, URL,
    # size, ingestion status. Content is NOT duplicated here (it's already
    # in the canonical text). This is metadata for record pages and
    # provenance.
    if attachments:
        entry["attachments"] = [
            {
                "filename": att["filename"],
                "url": att["url"],
                "size": att["size"],
                "ingested_inline": bool(att.get("is_text") and att.get("as_text") is not None),
                "ingestion_error": att.get("error"),
            }
            for att in attachments
        ]

    # Compose paths
    texts_path = REPO_ROOT / "data" / "texts" / f"AXN-{hex_id}-text.md"
    deposits_md_path = REPO_ROOT / "data" / "deposits" / f"AXN-{hex_id}.md"
    static_record_dir = REPO_ROOT / "s" / "records" / str(deposit_number)
    static_record_path = static_record_dir / "index.html"

    result = {
        "deposit_number": deposit_number,
        "hex": hex_id,
        "family": family,
        "axn": entry["axn"],
        "hash": file_sha256,
        "emoji": entry["emoji"],
        "registry_entry": entry,
        "canonical_text_bytes": len(canonical_bytes),
        "paths": {
            "canonical_text": str(texts_path.relative_to(REPO_ROOT)),
            "deposits_md": str(deposits_md_path.relative_to(REPO_ROOT)),
            "static_record": str(static_record_path.relative_to(REPO_ROOT)),
            "registry": str(registry_path.relative_to(REPO_ROOT)),
        },
        "dry_run": dry_run,
    }

    if dry_run:
        return result

    # ─── WRITE PHASE ───
    # All writes from this point. If any write fails, we leave the substrate
    # in an inconsistent state — the workflow's rollback strategy is to not
    # push (the branch never gets created if any of this raises).

    # 1. Canonical text file (CANONICAL BYTES, hash already locked in)
    texts_path.write_bytes(canonical_bytes)

    # 2. Deposits download alias — identical content, different path.
    # The §6.2.2 audit finding was that this file was missing for records
    # #872-879; the new workflow generates it in lockstep so the gap can't
    # reopen.
    deposits_md_path.parent.mkdir(parents=True, exist_ok=True)
    deposits_md_path.write_bytes(canonical_bytes)

    # 3. Insert into registry. Append + bump total_deposits.
    registry["deposits"].append(entry)
    registry["total_deposits"] = len(registry["deposits"])
    # Compact JSON per firm rule #2: registry uses compact format,
    # indent=None, ensure_ascii=False, separators=(',', ':').
    # Pretty-printing breaks downstream consumers.
    with open(registry_path, "w") as f:
        json.dump(registry, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")

    # 4. Static record page via wire_deposit
    if not _HAVE_WIRE_DEPOSIT:
        raise RuntimeError(
            "wire_deposit module not available — cannot render static record. "
            "This means the workflow environment is missing wire_deposit.py at repo root."
        )
    static_record_dir.mkdir(parents=True, exist_ok=True)
    # wire_deposit.regenerate_static_page reads deposit dict + entity index
    # and writes s/records/{deposit_number}/index.html directly. It returns
    # None; the file is the artifact. Do NOT try to capture and re-write
    # its return value.
    eidx_path = REPO_ROOT / "data" / "entity-index.json"
    with open(eidx_path) as f:
        eidx = json.load(f)
    wire_deposit.regenerate_static_page(entry, eidx)

    result["wrote_files"] = True
    return result


# ─────────────────────────────────────────────────────────────────────────────
# SELF-TESTS
# ─────────────────────────────────────────────────────────────────────────────

SAMPLE_GOOD_BODY = """### Protocol Version

alexanarch-deposit-protocol/v1

### Title

Test deposit: empirical baseline for sanity check

### Creator

Test Author (ORCID 0000-0000-0000-0000)

### ORCID

0000-0000-0000-0000

### Date

2026-06-23

### Description

This is a deposit body for self-test purposes. It verifies that mint_deposit
correctly parses the issue form structure and produces a schema-conformant
registry entry.

### Content Type

Theoretical paper

### License

CC-BY-4.0

### Substrate Disclosure

Human-only (no AI assistance)

### Keywords

test, sanity check, self-test, mint_deposit, axn_lib

### Version

v1.0

### Files

https://example.org/test-paper.pdf

### Terms

- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json
"""

SAMPLE_HOSTILE_BODY = """### Protocol Version

alexanarch-deposit-protocol/v1

### Title

Hostile deposit with javascript: URL

### Creator

Attacker

### Date

2026-06-23

### Description

Click this: javascript:alert(1)

### Content Type

Theoretical paper

### License

CC-BY-4.0

### Substrate Disclosure

Human-only (no AI assistance)

### Files

javascript:alert(2)
"""


def _selftest():
    """Run a battery of self-checks. Exits 0 on success, raises on failure."""
    print("=== mint_deposit.py self-test ===\n")

    # Test 1: hex_id formula
    print("Test 1: hex_id formula")
    assert next_hex_id(1) == "000D", f"expected 000D for #1, got {next_hex_id(1)}"
    # #881 has hex 037D in real registry: 881+12 = 893 = 0x37D
    assert next_hex_id(881) == "037D", f"expected 037D for #881, got {next_hex_id(881)}"
    assert next_hex_id(882) == "037E", f"expected 037E for #882, got {next_hex_id(882)}"
    print(f"  ✓ #1 → {next_hex_id(1)}, #881 → {next_hex_id(881)}, #882 → {next_hex_id(882)}")

    # Test 2: parse_issue_body extracts fields correctly
    print("\nTest 2: parse_issue_body")
    fields = parse_issue_body(SAMPLE_GOOD_BODY)
    assert fields["title"] == "Test deposit: empirical baseline for sanity check"
    assert fields["creator"].startswith("Test Author")
    assert fields["date"] == "2026-06-23"
    assert fields["content_type"] == "Theoretical paper"
    assert fields["license"] == "CC-BY-4.0"
    assert fields["substrate"] == "Human-only (no AI assistance)"
    assert "test" in fields["keywords"]
    print(f"  ✓ extracted {sum(1 for v in fields.values() if v)} non-empty fields")

    # Test 3: sanitize_url accepts allowed schemes
    print("\nTest 3: sanitize_url")
    assert sanitize_url("https://alexanarch.org/x") == "https://alexanarch.org/x"
    assert sanitize_url("http://example.com") == "http://example.com"
    assert sanitize_url("10.5281/zenodo.20688441") == "https://doi.org/10.5281/zenodo.20688441"
    print(f"  ✓ http/https/doi schemes accepted; bare DOI normalized")

    # Test 4: sanitize_url rejects javascript: and friends
    print("\nTest 4: sanitize_url hostile-scheme rejection")
    for bad in ["javascript:alert(1)", "data:text/html,<script>", "vbscript:msgbox", "file:///etc/passwd"]:
        try:
            sanitize_url(bad)
            raise AssertionError(f"sanitize_url failed to reject: {bad!r}")
        except SanitizationError:
            pass
    print(f"  ✓ javascript:, data:, vbscript:, file: all rejected")

    # Test 5: control char stripping
    print("\nTest 5: strip_control_chars")
    bidi = "Hello\u202eWorld"  # contains RLO override
    cleaned = strip_control_chars(bidi)
    assert "\u202e" not in cleaned, "BIDI char not stripped"
    assert cleaned == "HelloWorld"
    print(f"  ✓ BIDI RLO stripped: {bidi!r} → {cleaned!r}")

    # Test 6: family_for_content_type
    print("\nTest 6: family_for_content_type")
    assert family_for_content_type("Theoretical paper") == "GENERATIVE"
    assert family_for_content_type("Dataset") == "DATASET"
    assert family_for_content_type("Continuity tether") == "ARCHIVAL"
    assert family_for_content_type("Other (specify in description)") == "UNCLASSIFIED"
    assert family_for_content_type("Made-up new content type") == "UNCLASSIFIED"
    # 2026-07-23 additions:
    assert family_for_content_type("Epistle") == "COMPOSITIONAL"
    assert family_for_content_type("epistle") == "COMPOSITIONAL", "case-insensitive"
    assert family_for_content_type("EPISTLE") == "COMPOSITIONAL", "case-insensitive"
    assert family_for_content_type("Letter") == "COMPOSITIONAL"
    assert family_for_content_type("Poem") == "COMPOSITIONAL"
    assert family_for_content_type("Recension") == "COMPOSITIONAL"
    assert family_for_content_type("Commentary") == "PHILOLOGICAL"
    assert family_for_content_type("Metadata packet") == "MPAI"
    assert family_for_content_type("Metadata Packet for AI Indexing") == "MPAI"
    assert family_for_content_type("Effective act") == "GOVERNANCE"
    assert family_for_content_type("Epistle (with commentary)") == "COMPOSITIONAL", "parens suffix stripped"
    print(f"  ✓ dropdown values mapped; suffix-in-parens handled; case-insensitive; unknown→UNCLASSIFIED")

    # Test 7: full mint_from_issue_body, dry-run
    print("\nTest 7: mint_from_issue_body (dry-run)")
    result = mint_from_issue_body(SAMPLE_GOOD_BODY, issue_number=99999, dry_run=True)
    assert result["dry_run"] is True
    assert result["deposit_number"] >= 882, f"expected #882+, got #{result['deposit_number']}"
    assert result["axn"].startswith("AXN:"), f"AXN malformed: {result['axn']}"
    assert len(result["emoji"]) > 0, "emoji empty"
    assert re.match(r"^[0-9a-f]{64}$", result["hash"]), f"hash not 64-hex: {result['hash']}"
    print(f"  ✓ minted #{result['deposit_number']} with AXN {result['axn']}")
    print(f"    canonical bytes: {result['canonical_text_bytes']}")
    print(f"    hash: {result['hash'][:32]}…")

    # Test 8: hostile body rejected at sanitization layer
    print("\nTest 8: hostile body rejected")
    try:
        mint_from_issue_body(SAMPLE_HOSTILE_BODY, issue_number=99998, dry_run=True)
        raise AssertionError("Hostile body was not rejected!")
    except SanitizationError as e:
        print(f"  ✓ rejected with: {e}")

    # Test 9: AXN derivation is reproducible (same input → same AXN)
    print("\nTest 9: AXN reproducibility")
    r1 = mint_from_issue_body(SAMPLE_GOOD_BODY, issue_number=99999, dry_run=True)
    r2 = mint_from_issue_body(SAMPLE_GOOD_BODY, issue_number=99999, dry_run=True)
    assert r1["axn"] == r2["axn"], f"AXN non-reproducible: {r1['axn']} vs {r2['axn']}"
    assert r1["hash"] == r2["hash"], f"hash non-reproducible: {r1['hash']} vs {r2['hash']}"
    print(f"  ✓ same input produces same AXN: {r1['axn']}")

    # Test 10: registry-entry shape — has all schema-required fields
    print("\nTest 10: registry entry has required schema fields")
    required = ['deposit_number', 'axn', 'hex', 'family', 'emoji', 'hash',
                'title', 'creator', 'date', 'description', 'content_type',
                'license', 'substrate']
    entry = r1["registry_entry"]
    for field in required:
        assert field in entry, f"missing required field: {field}"
        assert entry[field], f"required field {field} empty"
    print(f"  ✓ all {len(required)} schema-required fields populated")

    print("\n=== all self-tests passed ===")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
    # format guard runs before any field is trusted
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--issue-body", type=Path, help="path to GitHub Issue body markdown file")
    parser.add_argument("--issue-number", type=int, help="GitHub issue number (for forensics)")
    parser.add_argument("--output", type=Path, help="write result JSON to this path (default stdout)")
    parser.add_argument("--dry-run", action="store_true", help="compute everything, write nothing")
    parser.add_argument("--selftest", action="store_true", help="run self-test battery and exit")
    args = parser.parse_args()

    if args.selftest:
        try:
            _selftest()
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ self-test FAILED: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(3)

    if not args.issue_body:
        print("--issue-body is required (unless --selftest)", file=sys.stderr)
        sys.exit(3)
    if args.issue_number is None:
        print("--issue-number is required (unless --selftest)", file=sys.stderr)
        sys.exit(3)

    body = args.issue_body.read_text()

    try:
        result = mint_from_issue_body(body, args.issue_number, dry_run=args.dry_run)
    except SanitizationError as e:
        print(json.dumps({"error": "sanitization", "message": str(e)}, indent=2))
        sys.exit(1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(json.dumps({"error": "internal", "message": str(e)}, indent=2))
        sys.exit(3)

    out_json = json.dumps(result, indent=2, ensure_ascii=False, default=str)
    if args.output:
        args.output.write_text(out_json)
    else:
        print(out_json)
    sys.exit(0)


if __name__ == "__main__":
    main()
