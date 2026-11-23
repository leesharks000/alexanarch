# C48 / 1547 MHz: pre-voltage discrimination — executed catalogue audit
Date: 2026-11-20.
Canonical source: [M4b/events/cc48.json](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/events/cc48.json); also original [M4/cc48.json](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4/cc48.json). Frozen M4b protocol and settings have not been altered.

## Summary
- Center frequency 1546.875 MHz, channel approximate coverage 1545.41–1548.34 MHz. Mobile satellite downlink allocation likely heavily occupied; an allocation is **not** a source identification.
- Complete M4b totals: **58 Class A ON vs 8 Class A reverse-role OFF**; Class B 158 ON vs 263 reverse-role OFF.
- M4b `events` saves the 40 strongest ON-source events; `control_top` only the 15 strongest reverse-role detections; these subsets **cannot** represent the full Class A populations.
- 39/40 of the saved ON events have exactly zero assigned topocentric drift, the remaining one +0.01458 Hz/s; 'zero' means resolved as zero on the frozen discrete drift grid.
- The busiest saved interval is **1547.65–1547.80 MHz**, selected *post hoc*: **20/40 ON-source retained events** (all from ON0015), and **5/15 reverse-role OFF-source retained events**, all from OFF0014. The 20 ON detections are primarily Class B; 4 are A.
- Within this interval, mean saved `z_local`: ON **16.7205**, OFF **25.83**; distinct selections, so this is not a calibrated ON/OFF amplitude comparison. They show strong off-pointing interference within the same general slice, not exactly the same physical carriers.
- Nearest frequency distances between each of 20 ON peaks and any of five OFF peaks: 0 within 1 kHz, 1 within 2 kHz, **10 within 5 kHz**, 13 within 10 kHz. A mismatch of a few kHz does not exclude drifting or frequency-hopping terrestrial carriers.
- For the nine retained ON Class A detections (not all 58), the number whose **already saved `off_along` max** lies below a stricter veto limit while `on_along` minimum remains >=5:
  - 5.0 (frozen): 9/9
  - 4.5: 6/9
  - 4.0: 4/9
  - 3.5: 3/9
  - 3.0: 2/9
  - 2.5: 0/9.
  This is threshold *sensitivity of saved records*, **not** a recalculation of the 58-event Class A total or a validated alternative detector. A changed veto would require rerunning the entire family, including injected controls.

## What the archived M4 comet-frame survey says
`M4/cc48.json` keeps only the 10 strongest comet-frame hits per scan: 88 ON13, 97 OFF14, 80 ON15, 51 OFF16, 458 ON17, 69 OFF18 total candidates. Its `on_hits_beyond_every_off` is empty. None of its top-ten scan events lies in the crowded 1547.65–1547.80 slice; this simply illustrates differing ranking/selection rules, not absence of energy.

## Adjudication
The high ON-source class A excess is worth voltage inspection but **not** a comet association. Strong near-zero-drift OFF-source events occur inside the same 150 kHz slice and the Class A saved detections are sensitive to veto boundaries. Unlike cc19, there is no established comb in this slice. Preliminary reading: complex satellite-downlink interference; not yet identified to a specific satellite or modulation protocol.

## Frozen next experiment — C48 raw voltage
Adapt the *already tested* C19 code, keeping all its input hashes and error corrections where applicable. Do not use its fixed 67,433 Hz comb or cc19 conclusions as assumptions.

1. **Source targets** from all nine retained C48 Class A locations (predeclared), all 20 ON15 peaks in 1547.65–1547.80 MHz (exploratory training set), five retained reverse-role OFF14 peaks in that interval as interference controls, plus 20 evenly spaced and 100 pseudorandom comparison frequencies drawn from the same interval with >=500 Hz exclusion from listed targets.
2. Re-extract all six scans, both polarizations and all 833 frames. **Explicitly hash the native sample products**; avoid C19's documented float16 overflow; retain per-row RMS-normalized power and medians.
3. Evaluate **fixed topocentric, comet ephemeris, and locally fitted linear drift** with *the same fitting degrees of freedom*; fit ON13 only and score OFF14/16/18 and ON15/17 as heldout. For the ON15-discovered window, explicitly split training ON15 and heldout ON17 (and OFF14/16/18); do not pretend it was selected before ON15.
4. Compute calibrated per-scan power versus pointing, temporal fading, polarization, carrier hopping and common envelope in the 150-kHz cluster. Distinguish a changing multi-carrier downlink from a coherent sky-localized narrowband emitter.
5. Prespecify RFI injection controls and a fake-track/fake-frequency family with global trial accounting; do not relax the OFF veto after seeing the result.
6. Positive comet association requires genuine ON localization (not a mere high A count) plus predictive track and absence from all OFF controls at realistic sidelobe gains. If a candidate fails, report the extent of sensitivity recovered by injections.
7. Do **not** confuse zero observed drift with zero source acceleration: programmable emission can precompensate Doppler. For such alternatives, independent sky localization remains essential.

### Access status
Raw channel-48 voltages were **not obtained in this session**: local runtime DNS for `bldata.berkeley.edu` fails. The C19 code and its complete voltage run are available in the other collaborator's networked environment. This is an executed *catalogue* audit, not a C48 voltage result.
