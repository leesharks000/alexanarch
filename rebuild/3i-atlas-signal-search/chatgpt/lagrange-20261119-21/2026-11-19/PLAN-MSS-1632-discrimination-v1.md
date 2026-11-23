# 3I/ATLAS — 1631.75–1632.08 MHz interference discrimination v1
**Established:** 2026-11-19 (America/Detroit), after reviewing the reported six events and their ON/OFF outcomes. **This is a retrospective follow-up plan, not a preregistration of the original discovery.** No new raw events were decoded as part of this plan.

## Existing observation (already exposed)
The 2026-11-19 manuscript *What Arrival Cannot Do* reports six features in 1631.75–1632.08 MHz across three on-comet ATA observations, none in the paired off-comet observations or one analysis control. Underlying per-event timestamps, exact frequencies, amplitudes, beams, drift slopes, candidate catalogue and raw files are NOT included in the current recovered handoff. The published allocation 1626.5–1660.5 MHz is Earth-to-space mobile-satellite; this band assignment establishes interference plausibility, not a source identification.

## Competing explanations
- H_RFI: mobile-satellite earth-terminal or other terrestrial/intermodulation interference, including sidelobes, multipath, beam response or pipeline-selection effects.
- H_comet: radiation physically co-moving with 3I/ATLAS, with unspecified natural or artificial cause.
- H_noise: chance/selective noise structure under exploratory trials.
- H_other: unresolved mechanism; never silently assign its probability to H_comet.

## Mandatory inputs before executing the candidate test
For all six candidates: native UTC sample intervals, fixed channel centres in Hz, native line drift and uncertainty, both beam powers (and calibration if present), rest-frame transform used, exact scan IDs and source URLs, detection algorithm, threshold, search extent and trial ledger. Missing fields trigger an explicit 'not testable' outcome. Archive source hashes.

## Locked investigation sequence
1. **Instrument/time integrity:** verify scan start, integration cadence, native frequency grid, beam designation, and JPL ephemeris at observatory site. Do not rely solely on file-title timestamps.
2. **RFI band context:** compare each feature to 1626.5–1660.5 MHz MSS uplink allocation and documented services; distinguish the broad allocation from an identified individual transmitter. Search local/sidelobe and simultaneous reference-beam appearances and adjacent time/frequency occupancy. No automatic veto.
3. **Pair-locked replication:** freeze the exact six native frequencies and their original physical drift trajectories as selected; evaluate all three original ON and OFF pairs and available independent scans, with *no* per-scan frequency maximization. Report frequencies, scores and negative observations for all six.
4. **Model competition:** fit (i) stationary recorded RF, (ii) comet-frame drift using JPL site-specific radial velocity, (iii) reasonable terrestrial/satellite-drift alternatives where ephemerides permit. Compare equal-complexity predictive losses under the same window and tolerance. If satellite orbital/TLE data are unavailable, say 'not tested'; never claim exclusion.
5. **Beam discrimination:** evaluate target/reference ratio on same epochs and frequency paths, accounting for sidelobes and pointing. An ON-only event is insufficient to establish astronomical localization.
6. **Nulls:** reassign beam roles, shift ephemeris frame, use nearby time/frequency bands with matched RFI occupancy and preserve temporal correlation. State all trial families; report empirical counts, not a global p-value unless warranted by the complete trial ledger.
7. **Blind continuation:** reserve independent later observations if truly unread; if already inspected, label them exploratory. Register outcomes as repeat / inconsistent / undecidable.

## Decision rules (fixed for this follow-up, not calibrated significance thresholds)
- **RFI supported:** independent evidence matches a known terrestrial/satellite transmitter or a reproducible stationary/shared-beam mechanism. A mere allocation match is not enough for identification.
- **Comet association supported:** pre-specified fixed paths predict held-out spectral evolution and beam-localized recurrence materially better than stationary and RFI alternatives. Association does NOT imply artificiality.
- **Noise/selection supported:** maxima disappear when frequency/path is held fixed or are typical of matched nulls.
- **Unresolved:** absent evidence or mixed results. Missing data must never be recorded as nondetection.

## Outputs
`event-ledger.csv`, `model-comparison.csv`, `rfi-coverage.md`, `NULLS.md`, `RUN-MANIFEST.json`; every assertion linked to original data, run code, and hashes.

## External reference
47 CFR §25.202 allocation: https://www.law.cornell.edu/cfr/text/47/25.202
National Academies treatment of MSS uplink allocations: https://www.nationalacademies.org/read/26611/chapter/4

**Result at freeze:** discrimination not run; candidate-level source data not available from the recovered handoff. No transmitter, comet-associated emitter, or technosignature identified.
