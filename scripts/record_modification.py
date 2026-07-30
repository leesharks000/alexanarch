#!/usr/bin/env python3
"""record_modification.py — the archive's own provenance of change.

WHY THIS EXISTS
---------------
Until 2026-07-30 the archive could say when a deposit was published and nothing
about when it was changed. That is an odd gap in a project whose subject is
provenance: the registry recorded the world's erasures and not its own repairs.
On a single day in July the archive seated five full-version pointers, cleared a
misattached ORCID from a third party's work, corrected a title that disagreed
with its own canonical bytes, and repaired five empty substrate declarations —
and afterwards no record could tell you any of it happened.

THE CHANGE RULE (the whole point)
---------------------------------
`date_modified` means THE RECORD CHANGED — not that a script ran.

  A modification is:   a change to the deposited record's own metadata or the
                       state it declares about itself. Title, creator, ORCID,
                       description, keywords, license, status, substrate,
                       body_status and its pointers, version relations,
                       corrections.

  NOT a modification:  regenerating the static page; re-running enrichment;
                       recomputing derived surfaces (citation graph, concept
                       map, sitemaps, browse index); fleet-wide sweeps that
                       touch a page without changing what the record says.

This distinction is the difference between a field worth having and the one it
replaces. `<lastmod>` currently carries the regeneration date, which is why
search engines discount it: it announces change on records that did not change.
A field that only moves when the record moves is a claim that can be checked.

CANONICAL BYTES ARE STILL IMMUTABLE
-----------------------------------
Nothing here edits deposited text. Modifications live in the registry and on the
surfaces; the text a deposit minted with is the text it keeps. `date_modified`
tracks the record's metadata and declared state, not its body.
"""
import json
from datetime import datetime, timezone

MODIFIABLE = {
    "title", "creator", "orcid", "description", "keywords", "license",
    "status", "substrate", "content_type", "body_status", "version",
    "superseded_by_deposit_number", "superseded_reason", "related_ids",
    "canonical_text_status", "version_series_id",
}


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def touch(entry, field, reason, was=None, now=None, when=None):
    """Record a modification on a registry entry and stamp date_modified.

    Appends to entry['modifications'] and sets entry['date_modified']. Pass
    `when` to backfill a known past change; defaults to today.
    """
    when = when or today()
    rec = {"date": when, "field": field, "reason": reason}
    if was is not None:
        rec["was"] = was if isinstance(was, (str, int, float, bool)) else json.dumps(was)[:200]
    if now is not None:
        rec["now"] = now if isinstance(now, (str, int, float, bool)) else json.dumps(now)[:200]
    entry.setdefault("modifications", []).append(rec)
    prior = entry.get("date_modified")
    entry["date_modified"] = max(prior, when) if prior else when
    return entry


def last_modified(entry):
    """The date to publish in <lastmod> and schema.org dateModified.

    Falls back to the publication date: absence of date_modified means the
    record has not been modified since deposit, which is a truthful claim.
    """
    return entry.get("date_modified") or entry.get("date")


def diff_touch(entry, before, reason, when=None):
    """Compare a snapshot against the entry and record every real change.

    Use around any operation that mutates registry entries; only fields in
    MODIFIABLE count, so page regeneration and enrichment cannot mark a record
    as changed.
    """
    n = 0
    for k in MODIFIABLE:
        old, new = before.get(k), entry.get(k)
        if old != new:
            touch(entry, k, reason, was=old, now=new, when=when)
            n += 1
    return n
