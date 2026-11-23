# PLAN-N1625 — phase-invariant transient recurrence in GBT cc21 (frozen 2026-11-20)

## Status
Frozen experiment proposal, **NOT yet executed on raw GBT voltages**. No alien or comet signal confirmed. Networked collaborator has already demonstrated direct streaming from the exact public Berkeley GBT files in channels 19, 48, and 50; cc21 is stored in the same raw files.

## Why this range
Recoverable M4b catalogue `leesharks000/alexanarch/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/events/cc21.json`:
- cc21 centre 1625.9765625 MHz, narrow location **1625.2936106175184 MHz** in ON0013 has detector z_local **58.1**, fitted drift **+1.690990951372353 Hz/s** at level 4.
- Frozen `on_along`: ON0015 7.21 and ON0017 17.74; `off_along`: OFF0014 1.32, OFF0016 0.79, OFF0018 2.33.
- Full cc21 M4b population 19 ON Class A vs 8 role-reversed Class A, with 430 ON Class B vs 520 OFF-source Class B. Very substantial interference foreground.
- The catalogue is *not* independent confirmation or sky localization; scores at the comet-tracked frequency are detector outputs, not measured beam attenuation.
- Alternative second cc21 target **1625.120423734188 MHz** ON0015, z39 at drift −6.0642 Hz/s, nearly coincident 1625.1207366585732 MHz at −7.347 Hz/s, is an explicit control for high-drift/hopping in same channel.
- cc22 has 25 A ON /31 reverse A; cc23 44 A ON /42 reverse A. Start with cc21 to bound compute and exploit a high ON/role-reversal imbalance.

## Distinct blind spot being tested
A signal may change central frequency, phase and amplitude yet repeat a **multi-frequency spectrotemporal shape**. Pure phase memory and line-spectrum searches require a certain representation; this test scores repeated *shape* with a free, bounded time-frequency translation but does not assume chirp sign or linear drift. This differs from simply boosting a catalogue Class A score.

## Fixed extraction
- Original public GBT December 18, 2025 scans 0013–0018, both X/Y complex voltages, channel cc21 (FC 1625.9765625 MHz).
- Fixed subband 1625.2936106175184 MHz ±91.55 kHz, 65,536 full-FFT bins at 2.7939677 Hz each.
- Use **32 raw frames from each scan** (~11.46 s; roughly 768 MiB channel payloads across six scans). For ON0013 split first 16 / last 16 for discovery/holdout; do not retune on second half. The original M4b event may occur later: if absent in first 32, this is a pilot-only *non-observation*, not elimination of the candidate.
- Crop full-frame complex FFT then invert to local analytic time series and split into 512-sample blocks, compute short-time power spectra. Normalize each time slice by its median, use robust broadband scale normalization and clip large outliers; keep the original unnormalized spectra for follow-up, do not erase actual line evidence.

## One new filter: translated spectral-shape recurrence
- Construct time-block vectors of robust-normalized log-power for each 512-bin spectrum.
- For each block, subtract broad baseline (frequency smoothing at 33 short-FFT bins), then normalize to unit L2 with a floor determined from stationary 20% quantile, not separately optimized on target.
- Find cosine similarity of **nonadjacent** blocks separated by lags [4,16,64,256,1024] short-time blocks while permitting integer frequency shifts −8…+8 short-FFT bins (one family score: maximum over lag, shift, and start time, with fixed minimum of four repeating occurrences). Exclude zero frequency shift only as an *additional reported* statistic; don't suppress stable unknown nonzero patterns.
- Each matched recurrence must involve at least four distinct frequency bins carrying non-negligible weight (participation ratio >= 4) to avoid re-detecting a lone line. Repeat the scoring after removing the single most energetic bin, as a leave-one-bin-out robustness control.
- Freeze all lags/shifts/thresholds, do **not** optimize detector after ON0013.
- Primary null: **199 phase- and amplitude-preserving block-order permutations** within each scan/feed, preserving each 512-bin block spectrum exactly and preserving coarse time-dependent interference with permutation in 32-block tiles. Compare maxima over the full same lag/shift/start/shape family. This null tests temporal ordering, not terrestrial sky origin.
- Independent controls: identical frozen filter in OFF0014/16/18, nearby +25 kHz slice, and cc21's 1625.1204237 MHz high-drift feature; also compare X/Y receiver feeds.

## Injection and failure criterion
Inject into **raw complex voltage before spectral estimation**:
1. Noise only; must not produce false positives beyond empirical rate.
2. Four-to-eight-tone packet motif repeating at a fixed block lag with random common phase, random envelope and random ±2-bin shifts; matched total RMS [0.25,0.5,1] noise. Requires >=80% recovery at RMS=1 over 20 random injection seeds and <10% false alarms in 100 null trials at pilot α=0.05.
3. One stationary narrow tone and one unrelated hopping tone, each matched in integrated power; the requirement of four-bin participation and leave-one-bin-out must not misclassify either as a structured motif.
4. Data must pass the per-scan surrogate and a same-feature held-out ON0013 half without retuning; an ON-selective candidate must then be checked in ON0015/17 and OFF scans at predicted time/frequency with proper detection sensitivity. Iridium modulation and intermodulation remain major alternatives.
5. If model injections fail, stop: do not interpret a non-detection as evidence against unknown signal. If the ON feature does not survive independent ON/OFF controls, report interference/uncertain, not a comet lead.

## Notes
This is exploratory detector-family development on a user-selected band, not a blind survey. The score is a *temporal-structure* anomaly, not a probability of extraterrestrial origin. Compute is spent on the filter's null and injection recoverability, not extending frequency coverage.
