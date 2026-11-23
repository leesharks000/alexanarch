# GBT cc19: two interleaved 67.433 kHz frequency sequences in the original M4b catalogue

**Analysis date:** 2026-11-20. **Status:** executed numerical catalogue analysis of already viewed data, not a new sky observation or transmitter attribution.

Source: [original cc19.json](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/events/cc19.json), [frozen detector plan](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/PLAN-M4b.md), [reproduction script](reproduce_cc19_comb.py).

## Finding

**14 of the 19 original ON-scan event records** (Class A or B), representing 14 distinct frequency locations, belong to **two interleaved arithmetic frequency sequences** each with essentially the same ~67.433 kHz step. The assignments were discovered after looking at the catalogue and cannot be counted as a blind test of a comb.

Group A: 8 records at grid positions −2,−1,0,1,3,4,5,6; four Class A and four Class B.
- Ordinary least-squares step **67,434.483 Hz**; RMS residual **9.65 Hz**; largest absolute residual ~14.94 Hz.
- Frequencies MHz: 1631.6126212477684; 1631.680078804493; 1631.7475084215403; 1631.8149492144585; 1631.949809845537; 1632.017232477665; 1632.0846900343895; 1632.1521028876305.
- The absent n=2 position near 1631.88238 MHz has nearby, but drifting, OFF-scan reverse-role events (e.g. 1631.882536690682 MHz, z=28.48, 155.6 Hz off an endpoint-defined grid). Their physical identity is **unconfirmed**.

Group B: 6 Class B records at grid positions −3,−1,0,2,4,5.
- Ordinary least-squares step **67,431.491 Hz**; RMS residual **4.51 Hz**; largest absolute residual ~9.22 Hz.
- Frequencies MHz: 1631.5653710626066; 1631.7002344876528; 1631.7676529288292; 1631.9025233387947; 1632.0373895578086; 1632.1048219688237.

A shared-spacing least-squares model with two separate intercepts gives:
- Common spacing **67,433.172 Hz**
- Grid intercept displacement **20,152.417 Hz**
- RMS residual **8.87 Hz** over 14 records; largest absolute residual **20.18 Hz**

This is substantially tighter than the search's coarsest ~44.7 Hz cells. It is a **catalogue feature**, not necessarily a real spectral comb: event-selection, binning, RFI harmonics and reused frequency grids must be audited in raw power/voltage.

There are six Class A *nominations*, not six independent signals: the 1632.017 MHz line was nominated in ON13 and ON17. The five distinct A frequencies consist of four in group A and an additional off-grid A at 1631.863676011562 MHz.

## Interpretation, hypotheses, falsifiers

The repeated spacing in both Class A and weaker Class B makes **related RFI or receiver-side periodicity** more plausible than unrelated exceptional emitters. The region is inside the 1626.5–1645.5 MHz Inmarsat maritime mobile-satellite earth-to-space band; this is not a transmitter ID. Telecom systems also use multiple different channel rasters; **no 67.433 kHz Inmarsat carrier standard was independently established** in this investigation.

A ~67.432 kHz sweep frequency appears in unrelated video display specifications, and screen/clock harmonics are documented RFI sources; this offers a generic *electronic clock* hypothesis, **not evidence that a screen caused these features**. These numerical coincidences do not identify origin. Independent authoritative information: [FCC 47 CFR 80.377](https://www.law.cornell.edu/cfr/text/47/80.377), [NRAO RFI guidance](https://science.nrao.edu/facilities/vla/docs/manuals/obsguide/rfi), [RFI in digital electronics](https://sites.nationalacademies.org/cs/groups/pgasite/documents/webpage/pga_183634.pdf).

Immediate discriminators on original cc19 raw voltages or native power:
1. Test whether **both sequences are present at the same absolute time** and share amplitude envelopes (common oscillator/intermodulation), with fixed frequency windows; distinguish independent bursts.
2. Test exact frequency stability and line widths across ON and OFF scans, not just events passing a wide cross-scan association window. Preserve positive and null outcomes.
3. Check whether the same **67,433 Hz spacing** continues elsewhere in cc19's full 2.93 MHz channel or in adjacent coarse channels; broadband clock leakage should often produce additional harmonics.
4. Inspect per-polarization phase/coherence and power, time bursts, pointing and telescope status; compare against stationary topocentric, moving satellite and comet Doppler models.
5. Use disjoint observations for any prospective significance calculation. A source discovered by fitting 14 selected catalogue events cannot borrow the original zero-control-A count as the false-alarm probability of this post-hoc comb hypothesis.

## What was and was not executed
Two separate least-squares fits and a shared-step/two-intercept least-squares fit were computed from the actual original JSON event frequencies. The supplied Python script reproduces them and verifies frequency membership against a downloaded original `cc19.json`. The original M4b `out3` spectra were deleted after hashing; the original GBT raw voltage server was **not accessible from this execution environment**. No direct waveforms, transmitter ephemeris, amplitude synchrony or source ID were measured.
