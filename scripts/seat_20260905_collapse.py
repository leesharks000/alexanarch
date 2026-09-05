#!/usr/bin/env python3
"""seat_20260905_collapse.py — RETIRED as a seat script (2026-09-05, same day).

The first version of this file built the entry dict by hand and appended it — the pattern every seat script
since 2026-08-13 had followed, and the reason the registry's shape drifted (73 keys) and its order broke on
every intake. From 2026-09-05 the single seat path is:

    python3 scripts/capture_intake.py <draft.json> --seat      # ADMIT → ROUTE → NORMALISE → VALIDATE → INSERT-in-section → EMIT
    python3 scripts/build_capture_gallery.py
    python3 scripts/seat_capture_postflight.py                  # runs check_capture_registry.py: schema · no-loss · order

A draft is a flat record with, at minimum, q, date, surface, auth, ev, s, transcript, d; any other field must
already be in rebuild/capture-registry/EA-WG-CAPTURES-01.schema.json. The draft for this capture is kept at
rebuild/capture-registry/intake-20260905/draft-cha-model-collapse-chatgpt-unprimed-20260905.json and re-running
intake on it is refused as an already-seated address (ROUTE → observation), which is the test.
"""
raise SystemExit(__doc__)
