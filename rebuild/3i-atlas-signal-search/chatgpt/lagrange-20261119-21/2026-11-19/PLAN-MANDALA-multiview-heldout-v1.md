# 3I/ATLAS — Mandala multi-view held-out study v1
**Established:** 2026-11-19. Future-looking methodology; **not** a preregistration for any previously seen July/December results or thresholds.

## Purpose
Estimate recognition power and false passes across several specified signal families rather than select a maximum after examining each scan. Preserve the distinction between simulated injection recovery, structure in the observations, physical origin and intelligent agency.

## Exposed calibration history (never a validation set)
- BRIDE D19 target/reference contrast 2.8937503536 vs reported cutoff 1.9729156985, from selecting per-scan maxima; fixed winning pair (groups 7,15) failed recurrence.
- Pooled cutoff made July BRIDE and INVERSION, and December long-window BRIDE, mathematically unable to pass.
- The revised view-specific cutoffs were chosen after examining these outcomes.
- Synthetic recovery differs by routing: December burst at power 0.03 recovered 12/12 in expected view vs 8/12 by assigned primary views; linked pairs at 0.3 recovered 11/12 vs 10/12.
These results are informative development data, not fresh false-alarm calibration.

## Signal families / views
1. BURST: brief, excess-power transients with minimum contiguous time support.
2. LINK: separated-frequency simultaneous/lagged pairs, fixed lag and frequency offsets.
3. GAP: narrow emission with predeclared on/off temporal intervals.
4. BRIDE: temporal correlation among fixed nonadjacent group indices.
5. INVERSION: declared anti/phase-inverted relation between fixed groups.
6. PHASE: coherent structure possible only when voltage phase is retained.
7. STEADY: ordinary narrowband line as sensitivity control.
8. NULL/SHARED: equal-beam or frequency-shifted controls.
Use each family's predeclared normalization and attainable numeric range. A threshold above a view's mathematical maximum is invalid, not a zero-detection result.

## Calibration, selection and validation
- Partition entire **observing sessions**, not neighboring pixels or repeated injections on the same noise, into development/calibration/held-out evaluation. Name and hash exact session memberships before evaluation. Do not call prior exposed scans held-out.
- Calibrate each view at a predeclared per-view false-positive allowance on separate backgrounds; use a family-wise rule (e.g. max-statistic null distribution or multiplicity correction), not one pooled raw contrast scale.
- Fix routing before viewing outcomes. Report both oracle/expected-view and actual assigned-view recovery.
- Generate injections from frozen families with separate random seeds and record waveform parameters, amplitude, polarization, drift, beam localization and phase availability.
- For BRIDE and LINK, choose frequency groups and lag on development data; do **not** choose a new maximizing pair in each validation scan.
- Valid nulls preserve interference occupancy, autocorrelation and scan grouping; retain RFI coincidences rather than silently excluding them.
- Report recovery vs amplitude, false passes, per-family confusion matrix, untestable views and empirical uncertainty; do not generalize recovery from injected Q to unknown form distribution π.
- Separate four statements in every result: recognized injected form; measured anomalous structure; associated with target; demonstrated artificial origin.

## Stopping and reporting
No retuning on the held-out partition. If a rule needs alteration, start version 2 with a *new* held-out session and label version 1 failed/undecidable. A candidate must repeat at fixed relation in independent observation and survive physical/RFI alternatives before promotion.

**Result at freeze:** protocol recorded; no new sky tested in this document. Full BRIDE and Mandala packets still need recovery and hash validation.
