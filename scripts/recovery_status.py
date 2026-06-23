#!/usr/bin/env python3
"""Recovery status taxonomy for the Alexanarch file-salvage operation.

The archive's recovery effort to date has operated at the metadata layer.
Phase 8 distinguishes file recovery from text recovery — the deposited
artifact is not the same as a description-field paragraph that happens to be
long, no matter how textually complete the paragraph is.

This module is the canonical reference for the seven-value status enum,
the display-layer mapping, and the helpers used by salvage_zenodo.py and
the renderer.

Public surface:
    STATUS_*                          — string constants for each enum value
    ALL_STATUSES                       — ordered list (best → worst)
    STATUS_META                        — dict: status -> display metadata
    rollup(per_file_statuses)          — deposit-level status from per-file list
    is_file_recovery(status)           — True for ORIGINAL/UNVERIFIED/MANIFEST
    is_text_only(status)               — True for TEXT/RECONSTRUCTION
    display_label(status)              — section header for a status
    display_badge_color(status)        — CSS color variable name
    display_note(status)               — explanatory line under the header
"""

# ───────────────────────────── enum ──────────────────────────────

STATUS_ORIGINAL_FILE_RECOVERED   = "ORIGINAL_FILE_RECOVERED"
STATUS_FILE_RECOVERED_UNVERIFIED = "FILE_RECOVERED_UNVERIFIED"
STATUS_FILE_MANIFEST_ONLY        = "FILE_MANIFEST_ONLY"
STATUS_TEXT_RECOVERED_FROM_METADATA = "TEXT_RECOVERED_FROM_METADATA"
STATUS_TEXTUAL_RECONSTRUCTION    = "TEXTUAL_RECONSTRUCTION"
STATUS_METADATA_ONLY             = "METADATA_ONLY"
STATUS_UNRECOVERED_FILE          = "UNRECOVERED_FILE"

# A deposit-level status that means "the constituent files have different
# statuses". Used only at the deposit level, never per-file.
STATUS_MIXED = "MIXED"

# Ordering: best recovery first, worst last. This is also the rollup priority.
# When multiple files exist with different statuses, the deposit-level rollup
# is MIXED (an honest acknowledgment that some files are recovered better
# than others); we do NOT collapse to the worst, because that under-states
# recovered files, and we do NOT collapse to the best, because that over-
# states unrecovered ones.
ALL_STATUSES = [
    STATUS_ORIGINAL_FILE_RECOVERED,
    STATUS_FILE_RECOVERED_UNVERIFIED,
    STATUS_FILE_MANIFEST_ONLY,
    STATUS_TEXT_RECOVERED_FROM_METADATA,
    STATUS_TEXTUAL_RECONSTRUCTION,
    STATUS_METADATA_ONLY,
    STATUS_UNRECOVERED_FILE,
]


# ───────────────────────────── display metadata ──────────────────────────────

STATUS_META = {
    STATUS_ORIGINAL_FILE_RECOVERED: {
        "label": "Deposited File",
        "note":  "Original bytes recovered; MD5 verified against Zenodo's published checksum.",
        "color": "var(--teal)",
        "rank":  1,
        "is_file": True,
        "is_verified": True,
    },
    STATUS_FILE_RECOVERED_UNVERIFIED: {
        "label": "Recovered File",
        "note":  "Original bytes recovered; no published checksum available to verify.",
        "color": "var(--teal-dim, #5a9c91)",
        "rank":  2,
        "is_file": True,
        "is_verified": False,
    },
    STATUS_FILE_MANIFEST_ONLY: {
        "label": "File Manifest",
        "note":  "Filename, size, and checksum are known; bytes are missing.",
        "color": "var(--amber, #b8860b)",
        "rank":  3,
        "is_file": False,
        "is_verified": False,
    },
    STATUS_TEXT_RECOVERED_FROM_METADATA: {
        "label": "Textual Content (recovered from metadata)",
        "note":  "Depositor-authored text recovered from the record's metadata. "
                 "Not the deposited file. Original filename, MIME, embedded "
                 "assets, formatting, and exact bytes are not preserved.",
        "color": "var(--dim)",
        "rank":  4,
        "is_file": False,
        "is_verified": False,
    },
    STATUS_TEXTUAL_RECONSTRUCTION: {
        "label": "Reconstructed Text",
        "note":  "Text reconstructed from partial sources. Not the deposited "
                 "artifact. Provenance shown.",
        "color": "var(--accent2)",
        "rank":  5,
        "is_file": False,
        "is_verified": False,
    },
    STATUS_METADATA_ONLY: {
        "label": "Metadata Record",
        "note":  "Bibliographic record recovered. No substantive artifact "
                 "or text content available.",
        "color": "var(--dim)",
        "rank":  6,
        "is_file": False,
        "is_verified": False,
    },
    STATUS_UNRECOVERED_FILE: {
        "label": "File Missing",
        "note":  "Evidence that a file existed under this DOI, but no bytes "
                 "have been recovered.",
        "color": "var(--accent2)",
        "rank":  7,
        "is_file": False,
        "is_verified": False,
    },
    STATUS_MIXED: {
        "label": "Mixed Recovery",
        "note":  "Constituent files have different recovery statuses. See "
                 "the file list for per-file detail.",
        "color": "var(--accent)",
        "rank":  3,  # near the file-manifest tier — never claims full recovery
        "is_file": False,
        "is_verified": False,
    },
}


# ───────────────────────────── helpers ──────────────────────────────

def rollup(per_file_statuses):
    """Compute a deposit-level status from a list of per-file statuses.

    Rules:
      - empty list → METADATA_ONLY (the deposit has no constituent files at all)
      - all the same → that status
      - all are file-recovery statuses (ranks 1-3) and best is recovered →
            best file status if all the same, else MIXED
      - any file-recovery present alongside non-file statuses → MIXED
      - all non-file → the best (lowest rank) non-file status

    The rollup is deliberately conservative: it never claims a higher
    recovery level than the constituent files justify.
    """
    if not per_file_statuses:
        return STATUS_METADATA_ONLY
    unique = set(per_file_statuses)
    if len(unique) == 1:
        return next(iter(unique))
    # Multiple distinct statuses → MIXED, except when all are non-file in
    # which case the best non-file status is correct.
    has_file = any(STATUS_META[s]["is_file"] for s in unique
                   if s in STATUS_META and STATUS_META[s]["is_file"])
    has_manifest = STATUS_FILE_MANIFEST_ONLY in unique
    if has_file or has_manifest:
        return STATUS_MIXED
    # All non-file (text, reconstruction, metadata-only, unrecovered)
    # → pick the best by rank (lowest)
    ranked = sorted(unique, key=lambda s: STATUS_META.get(s, {}).get("rank", 99))
    return ranked[0]


def is_file_recovery(status):
    """True if status represents bytes (or manifest pointing to bytes)."""
    meta = STATUS_META.get(status, {})
    return bool(meta.get("is_file")) or status == STATUS_FILE_MANIFEST_ONLY


def is_text_only(status):
    """True if status is text-recovery (no file)."""
    return status in (STATUS_TEXT_RECOVERED_FROM_METADATA,
                      STATUS_TEXTUAL_RECONSTRUCTION)


def display_label(status):
    return STATUS_META.get(status, {}).get("label", status)


def display_badge_color(status):
    return STATUS_META.get(status, {}).get("color", "var(--dim)")


def display_note(status):
    return STATUS_META.get(status, {}).get("note", "")


def validate(status):
    """Raise ValueError if status is not a recognized enum value."""
    if status not in STATUS_META:
        raise ValueError(f"unknown recovery status: {status!r}; "
                         f"expected one of {sorted(STATUS_META)}")
    return status


# ───────────────────────────── self-test ──────────────────────────────

if __name__ == "__main__":
    # rollup checks
    assert rollup([]) == STATUS_METADATA_ONLY
    assert rollup([STATUS_ORIGINAL_FILE_RECOVERED]) == STATUS_ORIGINAL_FILE_RECOVERED
    assert rollup([STATUS_ORIGINAL_FILE_RECOVERED, STATUS_ORIGINAL_FILE_RECOVERED]) == STATUS_ORIGINAL_FILE_RECOVERED
    assert rollup([STATUS_ORIGINAL_FILE_RECOVERED, STATUS_FILE_MANIFEST_ONLY]) == STATUS_MIXED
    assert rollup([STATUS_TEXT_RECOVERED_FROM_METADATA, STATUS_METADATA_ONLY]) == STATUS_TEXT_RECOVERED_FROM_METADATA
    assert rollup([STATUS_FILE_MANIFEST_ONLY, STATUS_UNRECOVERED_FILE]) == STATUS_MIXED

    # category checks
    assert is_file_recovery(STATUS_ORIGINAL_FILE_RECOVERED)
    assert is_file_recovery(STATUS_FILE_MANIFEST_ONLY)
    assert not is_file_recovery(STATUS_TEXT_RECOVERED_FROM_METADATA)
    assert is_text_only(STATUS_TEXT_RECOVERED_FROM_METADATA)
    assert not is_text_only(STATUS_ORIGINAL_FILE_RECOVERED)

    # validate
    try:
        validate("nope")
        assert False, "should have raised"
    except ValueError:
        pass

    print("recovery_status: all self-tests passed.")
    print()
    print("Display preview:")
    for s in ALL_STATUSES:
        print(f"  {s}")
        print(f"    label: {display_label(s)}")
        print(f"    note:  {display_note(s)}")
        print(f"    color: {display_badge_color(s)}")
        print()
