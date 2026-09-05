# Atlas v2.1 addendum — The capture projection: one canonical gallery, fleet windows — 2026-09-05

## Finding
The registry `data/EA-WG-CAPTURES-01.json` (v11.7, 378 entries) projects completely to `captures/index.html` on alexanarch: every entry anchored by slug, every transcript rendered in full (362 of 378 carry one; the 16 without predate the 2026-08-13 intake contract), images served from `data/captures/<slug>/` (image folders, not pages — there are no per-capture pages). The galleries on other fleet sites were stale static copies: godkinggoogle "258 receptions" with no transcripts and none of the seatings after mid-August; machinemediation a 15 KB stub. That is what "transcripts left out" and "seatings not reaching the projection" were: the windows, not the projection.

## Rule
The alexanarch gallery is the canonical projection (`_projection` in the registry file; ruled 2026-09-05). Fleet galleries are windows: they fetch the canonical JSON at page load, render the entries relevant to their host, and canonicalise to alexanarch. They hold no copy.

## Dataflow
EA-WG-CAPTURES-01.json → build_capture_gallery.py → captures/index.html (gate: seat_capture_postflight.py) → [client fetch] → fleet windows. Hub: the `captures` config rebuilds on push (workflow paths now include data/EA-WG-CAPTURES-01.json, data/citation-graph.json, data/doi-resolution-index.json, datasets/**).
