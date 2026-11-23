# 3I/ATLAS: comet-matched search INSIDE occupied human radio bands
**2026-11-20. Current scope: source-derived checkpoint and discriminating test design. Not a new voltage run.**

## Finding from original comet-frame M4 files (executed catalogue comparison)
The initial assertion "everything in a human communications allocation is ours" is an **inference**, not a signal-origin test. A hypothetical emitter on/near 3I/ATLAS could transmit at 1632 MHz or 1547 MHz. Allocations should determine interference priors, not categorical exclusion.

Canonical original channel-19 comet-frame records: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4/cc19.json

From each scan's saved top hits (M4, a comet-frame stack, **not** the M4b drift-search scores):

| ON/OFF top-hit pair | ON topocentric MHz | ON z | OFF topocentric MHz | OFF z | offset Hz |
|---|---:|---:|---:|---:|---:|
| ON0013 / OFF0014 | 1631.8351048976183 | 148.625 | 1631.8351160734892 | 18.203125 | +11.175871 |
| ON0017 / OFF0018 | 1632.0047210901976 | 41.6875 | 1632.0048021152616 | 8.3515625 | +81.025064 |

These show emissions at neighboring absolute recorded frequencies on and off target, consistent with RFI or beam sidelobes. They do NOT by themselves identify any physical emitter, prove continuous stationary trajectories, or exclude a weaker comet-associated signal coexisting with terrestrial power.

Original M4 report: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/RESULTS-M4.md . M4 nominated 59 signals over 60 channels, but 56? Check count: channel products were lost in a restart (see report); its bin-by-bin OFF veto in comet frame is inadequate for moving RFI.

Original M4b full-band report: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/RESULTS-M4b.md . All 64 channels: A 287 versus role-exchanged control A 506. All channels where the A count exceeded reverse-role A were in allocated human-transmission bands. M4b does **not** require exact 3I/ATLAS Doppler motion for A, only a piecewise-linear drift and broad time-window recurrence.

## Test: predeclare comet trajectory, then adjudicate by predictive performance

**Primary model C:** for each scan and each time sample calculate GBT observatory-relative line-of-sight velocity `v_C(t)` from the same JPL Horizons ephemeris used in frozen M4 (source `dm.ephem()`). A narrowband source whose carrier is fixed in the comet rest frame has predicted receiver frequency `f_C(t; f_rest)` (with documented Doppler sign and velocity conventions; classical `f_rest*(1 - v_rad(t)/c)` for positive recession, adequate to first order; relativistic correction consistently if needed). Fit **one frequency intercept** or reference `f_rest` on predesignated training scan ONLY. Predict the frequency-vs-time locus across the other five scans without refitting per scan.

**Alternative F:** stationary topocentric carrier, optionally with bounded/estimated local oscillator drift. Same training information and predictive scoring.

**Alternative S:** satellite/aircraft/terrestrial emitter model: source's geocentric trajectory at time of observation plus GBT motion; ephemerides or TLEs only if contemporaneous and applicable; match independent recorded candidates; allow transmission switching and channel changes and penalize additional model freedom. Without actual satellite ephemerides, report S as unassigned RFI rather than falsely eliminated.

**Null models:** reverse ON/OFF roles, genuine pointing-based controls, time-shifted and frequency-shifted tracks, acceleration-perturbed tracks (with perturbations large enough to dephase at the instrument's actual spectral resolution), and masked known strong RFI. Keep every selected channel in the measured trial family to control false positives.

**Signal metrics:** normalized power integrated along predicted trajectory per scan (with equal matched spectral widths), local off-track noise estimate, recovered line centroid and width, per-scan amplitude, two independent complex polarization streams, predicted vs observed frequency residuals, model fit and null rank. Treat human allocation as classification metadata, not a cut.

**Gate:** no positive comet-association nomination unless heldout ON scans have persistent predicted frequency paths within predeclared widths, OFF responses fit a directional source at comet coordinates (and not ordinary sidelobes), and model C predicts heldout samples better than both stationary F and independent interferer models. A single drift-slope match or A count is insufficient.

**Detection family limitation:** ordinary narrowband comet-rest-frame tones only. A signal deliberately mimicking a human satellite's spectrum, drifting independently from comet, or operating below sensitivity need not pass. Negative result is not universal absence of ET.

## Immediate target list for new raw-voltage run
1. **cc19 (~1631.8 MHz)**: suspicious frequency comb + exact nearby ON/OFF emissions and preserved M4/M4b event lists; best case study of whether comet frame resolves a faint component.
2. **cc48 (~1546.9 MHz) and cc50 (~1541.0 MHz)**: high A vs reversed controls, mostly zero topocentric drift; useful interference calibration / possible overlapped component tests. Do not assume ET from counts.
3. **cc21–cc24 (~1617–1626 MHz)**: many drifting Iridium-like events including moving satellite signals; strongest test for the risk of false comet-slope matches.
4. **cc08 (~1664 MHz)**: protected radio astronomy band, single-scan M4 lead near 1663.327 MHz; negative in M4b three-ON criterion; scientifically interesting control but low priority as ET survivor.

**Required data:** original `blc23` raw-voltage coarse channel for selected scans; exact per-integration UTC/MJD, tracking/pointing header, ephemeris, source `dm.py` constants, polarizations, scan roles. The original M4b `out2/out3` products were deleted after hashing; cannot reconstruct exact time-frequency tracks from `M4b/events` JSON alone.

### Key distinction
A human communications band can contain comet-associated emission. Signal **frequency** is a weak origin marker; **predictive kinematics + repeatability + spatial localization + matched false-positive controls** are the meaningful origin tests. The current findings favor RFI in cc19, but they do not constitute a dedicated hidden-comet-signal test.
