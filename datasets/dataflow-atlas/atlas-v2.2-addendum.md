# Atlas v2.2 addendum — The Capture Registry: fixed shape, one intake path, order owned by the projector — 2026-09-05

## Why
The registry was rebuilt from the ground up in August because transcripts and images were being discarded on repair. By 2026-09-05 the canonical file had 73 top-level keys across 378 entries with no schema applied, 21 editorial sentences sitting in the derived `defects` field (16 carried in by the 2026-08-22 reconciliation of two divergent copies), and an order — grouped by section, restored 2026-08-30 — broken by every intake since, because every seat script built its entry by hand and appended it. `capture_intake.py` existed, specified ADMIT→ROUTE→NORMALISE→EMIT, and was used by no seating: it worked against the sealed rebuild shape and pointed at the sealed file. The full read-only map is CAPTURE-REGISTRY-MAP-2026-09-05.md (outputs; to be seated).

## What is now in force (ruled 2026-09-05, "adopted")
- **Schema**: `rebuild/capture-registry/EA-WG-CAPTURES-01.schema.json` — the record is the 14 universal + 23 near-universal keys; long-tail keys promoted (typed) or folded into `notes` under their original names; nothing dropped; `additionalProperties: false`. A new field is a schema change in its own commit.
- **`defects` vs `findings`**: `defects` is the derived controlled vocabulary (8 tokens) and is never written by hand; `findings` holds editorial sentences. The gallery renders them differently.
- **Intake**: `scripts/capture_intake.py <draft.json> --seat` is the only way an entry enters the file. It refuses missing contract fields, refuses unknown fields, derives defects/ids/cite, routes a repeated address to an observation, and inserts into the section.
- **Order**: the file is grouped by section (`_order`); the projector renders sections alphabetical and entries by issued query. Seating cannot disturb it.
- **Gate**: `scripts/check_capture_registry.py` — SCHEMA · NO-LOSS (transcript length and image sets never decrease against origin/main; no entry removed) · ORDER — run by `seat_capture_postflight.py`; SEATED is not declared unless it passes.

## Dataflow
draft.json → capture_intake.py (ADMIT/ROUTE/NORMALISE/VALIDATE/INSERT/EMIT) → data/EA-WG-CAPTURES-01.json → build_capture_gallery.py → captures/index.html (+ JSON-LD Dataset, Signposting) → seat_capture_postflight.py (check_capture_registry, tab/data/projection agreement) → commit ONCE → Hugging Face `captures` config on push (workflow path filter) → fleet windows (client fetch of the canonical file).

## Corrections carried
v2.1's statement that the fleet galleries were "stale static copies" was true of godkinggoogle only; leesharks.com/captures fetched this file at load and machinemediation rendered from a synced copy, both at 377 with main. The replacement windows are in place; their status (keep / revert) and the retirement of stale registry snapshots in fleet repos await the operator's ruling.
