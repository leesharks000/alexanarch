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
MAX_DESCRIPTION_CHARS = 50_000
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
    pattern = rf"###\s+{re.escape(label)}\s*\n\s*(.*?)(?=\n###|\Z)"
    m = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    val = m.group(1).strip()
    if val in ("_No response_", "None", "_None_"):
        return ""
    return val


def parse_issue_body(body: str) -> dict:
    """Extract all known fields from a deposit issue body.

    The issue template at .github/ISSUE_TEMPLATE/deposit.yml defines these
    field labels. If the template changes, update this function. The
    validate_deposit.py field map is the partial source of truth; this is
    the complete map.
    """
    return {
        "protocol_version": extract_field(body, "Protocol Version"),
        "title": extract_field(body, "Title"),
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


def next_hex_id(deposit_number: int) -> str:
    """Compute the opaque hex label for a deposit_number.

    Formula: hex_id = deposit_number + HEX_OFFSET, formatted as 4-digit
    uppercase hex. The offset is historical (from earlier renumbering);
    schema's pattern allows 2-4 digits.
    """
    value = deposit_number + HEX_OFFSET
    return f"{value:04X}"


def family_for_content_type(content_type: str) -> str:
    """Map an issue-form content_type value to an AXN family enum.

    Falls back to UNCLASSIFIED if the dropdown adds new values that
    weren't anticipated here. UNCLASSIFIED is valid per the schema's
    family enum.
    """
    # Strip suffix in parens, e.g. "Other (specify in description)" -> "Other"
    key = content_type.split("(")[0].strip() if content_type else ""
    return CONTENT_TYPE_TO_FAMILY.get(key, "UNCLASSIFIED")


# ─────────────────────────────────────────────────────────────────────────────
# CANONICAL TEXT FILE
# ─────────────────────────────────────────────────────────────────────────────

def build_canonical_text(fields: dict, deposit_number: int, hex_id: str) -> str:
    """Construct the canonical text file content (frontmatter + body).

    The resulting string IS the canonical bytes. SHA-256 of this becomes
    the deposit's `hash` field and the source of the AXN glyphs.

    The frontmatter is YAML-safe (no embedded HTML, no markdown rendering
    until s/records/ is generated). The body section is the depositor's
    submitted content (description + methodology + falsification + files
    listing), preserved verbatim — this is the canonical record.

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
    if fields.get("description"):
        body_sections.append(f"# {fields['title']}\n")
        body_sections.append(f"## Description\n\n{fields['description']}\n")
    if fields.get("methodology"):
        body_sections.append(f"## Methodology\n\n{fields['methodology']}\n")
    if fields.get("falsification"):
        body_sections.append(f"## Falsification Conditions\n\n{fields['falsification']}\n")
    if fields.get("files"):
        body_sections.append(f"## Files\n\n{fields['files']}\n")

    frontmatter = "\n".join(fm_lines)
    if keywords_yaml:
        # Insert keywords before closing --- by replacing the final line
        frontmatter = "\n".join(fm_lines[:-1]) + "\n" + keywords_yaml + "---"
    body = "\n".join(body_sections)
    return frontmatter + "\n\n" + body


# ─────────────────────────────────────────────────────────────────────────────
# REGISTRY ENTRY CONSTRUCTION
# ─────────────────────────────────────────────────────────────────────────────

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
        "description": fields["description"],
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
        "wiki_article": None,
        "wiki_status": "provisional",
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

    # Load current registry — needed for deposit_number computation
    registry_path = REPO_ROOT / "data" / "registry.json"
    with open(registry_path) as f:
        registry = json.load(f)

    deposit_number = next_deposit_number(registry)
    hex_id = next_hex_id(deposit_number)
    family = family_for_content_type(fields["content_type"])

    # Build canonical text content
    canonical_text = build_canonical_text(fields, deposit_number, hex_id)
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
    print(f"  ✓ dropdown values mapped; suffix-in-parens handled; unknown→UNCLASSIFIED")

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
