#!/usr/bin/env python3
"""propagate_record_state.py — one repair, one state, everywhere.

Runs the full propagation pipeline (RECORD-SHAPE-AND-PROPAGATION v1.0) for the
given deposit numbers. A repair is not complete until this has run.

Usage: python3 scripts/propagate_record_state.py 1308 1344 1382 1383
"""
import json, sys, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT))


def tombstone_text(entry):
    w = entry.get("withdrawn", {})
    author = w.get("rightful_author", "the rightful author")
    doi = w.get("rightful_doi", "")
    return f"""---
deposit_number: {entry['deposit_number']}
hex: {entry['hex']}
title: "WITHDRAWN — external work (typed tombstone)"
content_type: Withdrawn — external work (typed tombstone)
lifecycle_state: withdrawn_external
axn_schema_version: v2
---

# WITHDRAWN — EXTERNAL WORK

This position ({entry.get('axn','')}) was created by an over-inclusive DataCite
full-metadata capture during the post-termination restoration campaign.

The work it captured — **"{w.get('original_title', entry.get('title',''))}"** — is by
**{author}** and is NOT a holding of this archive. It belongs to its author at
DOI **{doi}**, where it should be cited and accessed.

The captured metadata and content have been removed. This position is retained
as a typed tombstone (no 404) to document the capture-and-withdrawal honestly
rather than silently erase it. No content of {author}'s work is served here,
and no archive identifier (ORCID or otherwise) attaches to their work.

*MANUS foreign-capture tombstone policy (site audit 2026-07-31); propagated
under RECORD-SHAPE-AND-PROPAGATION v1.0.*
"""


def main(nums):
    reg = json.load(open(ROOT / "data/registry.json"))
    deps = reg["deposits"] if isinstance(reg, dict) else reg
    by = {d["deposit_number"]: d for d in deps}

    # Step 1 — tombstone staged texts for withdrawn_external
    changed = False
    for n in nums:
        e = by.get(n)
        if not e:
            print(f"#{n}: not in registry — skipped"); continue
        if e.get("lifecycle_state") == "withdrawn_external":
            w = e.setdefault("withdrawn", {})
            if "original_title" not in w and "WITHDRAWN" not in str(e.get("title","")):
                w["original_title"] = e.get("title","")
            p = ROOT / f"data/texts/AXN-{e['hex']}-text.md"
            p.write_text(tombstone_text(e))
            print(f"#{n}: staged text → typed tombstone")
            changed = True
    if changed:
        json.dump(reg, open(ROOT / "data/registry.json", "w"), ensure_ascii=False, indent=2)

    # Step 2 — derive display fields
    subprocess.run([sys.executable, "scripts/status_reconcile.py", "--apply"], cwd=ROOT, check=False)

    # Step 3 — record pages
    import wire_deposit
    reg = json.load(open(ROOT / "data/registry.json"))
    by = {d["deposit_number"]: d for d in reg["deposits"]}
    try:
        eidx = json.load(open(ROOT / "data/entity-index.json"))
    except Exception:
        eidx = {}
    for n in nums:
        if n in by:
            try:
                wire_deposit.regenerate_static_page(by[n], eidx)
                print(f"#{n}: record page regenerated")
            except Exception as ex:
                print(f"#{n}: page regen failed: {ex}")

    # Steps 4–6 — derived surfaces
    subprocess.run([sys.executable, "scripts/regenerate_surfaces.py", "--only",
                    "chunks,browse,browse-index,search-index,wiki,sitemap"], cwd=ROOT, check=False)
    subprocess.run([sys.executable, "scripts/build_central_registry.py"], cwd=ROOT, check=False)
    subprocess.run([sys.executable, "scripts/build_oai_index.py"], cwd=ROOT, check=False)
    print("propagation complete:", nums)


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]])
