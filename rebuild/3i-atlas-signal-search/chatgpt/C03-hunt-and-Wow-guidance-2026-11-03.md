# C03: frequency tolerance, recovery, and what Wow! can guide

3 November 2026. The fixed C03 continuation is complete. All six spectral inputs are the already examined Green Bank L-band scans of 18 December 2025. No independent observing-epoch confirmation or transmitter identification was obtained. The Wow! review supplies next-search constraints; no new Wow!-coded signal search was performed here.

**C03 remains unexplained, with a more precise limitation than the earlier normalization result: it passes with the original small per-scan frequency tolerance, but fails a strict shared-frequency detector. The injection experiment also shows that this strict detector misses many of the weak known signals tested. Neither outcome establishes a human source or rules out a source on the comet.**

## What changed in the C03 assessment

The exported nominal first-order rest coordinate is 1665.633776617 MHz. Its many digits identify an analysis coordinate; they do not establish sub-hertz physical accuracy. Native channels are approximately 2.794 Hz wide. The gates remain ON score at least 2.5 in all three ON scans and OFF score below 2 in all three OFF scans. These are empirical median/MAD screening scores, not independently calibrated Gaussian significances.

Two normalizations were retained: T0 divides each channel by its time median; F1 divides by a per-row interpolated 1024-channel median baseline and then whitens each row by its median/MAD. This pass changes tracking and frequency freedoms, not those definitions.

| Treatment, within nominal coordinate ±5 Hz | T0: ON 13 / 15 / 17 | F1: ON 13 / 15 / 17 | Original gate |
|---|---|---|---|
| Original coarse-frequency shifts, original grid mapping, ±one-bin per-scan maxima | 2.997 / 2.639 / 2.734 | 2.546 / 2.820 / 2.966 | Pass both |
| Correct reference rest-grid spacing, retaining coarse shifts and tolerance | 2.997 / 2.639 / 2.734 | 2.546 / 2.820 / 2.966 | Pass both |
| Exact per-frequency first-order paths, one shared half-native-bin rest grid, no per-scan frequency maximum | 3.038 / 1.976 / 2.853 | 2.649 / 2.173 / 3.112 | Fail both: middle ON |
| Same exact profiles with ±one-native-bin per-scan tolerance | 3.038 / 2.697 / 2.853 | 2.649 / 2.874 / 3.112 | Pass both |

Each row uses its own best joint gate margin, with identical freedom for the comparison windows; scores are not all sampled at the same coordinate across treatments. Strict shared-track selection is at 1665633774.8646162 Hz for both baselines. The ±100 Hz strict search selects the same coordinate and still fails. Correcting the original grid spacing alone does not remove C03. Allowing separate small frequency choices in the scans is the material difference.

The exact treatment computes f_observed = F × (1 − radial_velocity/c) at each integration center. Every scan uses one common metadata-defined frequency grid with interior support for three-native-bin smoothing, without circular wrapping. Its median/MAD calibration uses the entire common coarse-channel rest grid before tolerance maxima. “Exact” here means exact evaluation of this first-order path model on that grid, with nearest-channel sampling. It is not a complete relativistic, frequency-standard, channel-response, or ephemeris uncertainty treatment. A tolerance of a few hertz therefore cannot simply be declared physically illegitimate.

All 100 matched local comparison centers, ±k×250 Hz for k=1…50, have weaker gate margins under each treatment at both ±5 and ±100 Hz; none passes. These are reused neighborhoods of an already selected feature, not an independent discovery test or a global false-alarm probability. The correction weakens a strong shared-track characterization of C03 while preserving its local distinction under the specified comparisons.

## Timing

The first 24 and last 25 integrations were separately calibrated over the full common frequency grid. They were evaluated at the frequency selected from the full cadence, without retuning either half. Actual time gaps remain intact.

| ON scan | T0 early / late score | F1 early / late score |
|---|---|---|
| 13 | 3.045 / 1.230 | 2.285 / 1.473 |
| 15 | 1.498 / 1.299 | 1.521 / 1.564 |
| 17 | 2.316 / 1.716 | 2.538 / 1.872 |

Half-scan scores are descriptive. They do not have to exceed a full-scan threshold for a real weak signal. These numbers do not establish a burst, a Wow!-like envelope, or a message. Every per-integration contribution is retained in results/per-integration.csv. The frequency/time figure shows the small displacement of the middle ON profile and the noisy time contributions. Actual antenna tracking during ON17 remains unresolved; a scalar header coordinate is not an antenna time series.

## Known-power injection recovery

All 18 fixed configurations were completed under both T0 and F1: three placements (nominal C03 −1000, +1000, +2000 Hz), three amplitudes (0.15, 0.30, 0.60 local raw-row MAD units), and two occupancies (all three ON scans, or middle ON only). OFF powers were unchanged.

The deterministic Gaussian power line has sigma 0.6 native channels; it is integrated over channel edges and averaged over 16 sub-times per exposure along the saved trajectory. Row noise is measured before injection in ±5 kHz, excluding ±50 Hz. The line is added to float32 powers before normalization, and full normalization and common-grid calibration are recomputed. These are idealized power-domain component tests, not voltage simulations, flux/EIRP limits, or survey completeness estimates.

| Amplitude | Persistent all-ON recovery, T0 | Persistent all-ON recovery, F1 | Newly passing middle-ON pair, T0 | Newly passing middle-ON pair, F1 |
|---|---|---|---|---|
| 0.15 | 0/3 placements | 0/3 | 1/3 | 0/3 |
| 0.30 | 0/3 | 1/3 | 1/3 | 1/3 |
| 0.60 | 1/3 | 1/3 | 3/3 | 2/3 |

These are ±5 Hz results. The middle-pair column counts flags created by injection, excluding a placement whose F1 pair already passed before injection. The full ledger records both preexisting and injected flags, exact-coordinate scores, shared-frequency selection and all individual pairs. The middle-pair results are the same for the two occupancy configurations because the other ON scans do not enter that pair's detector. Middle-only injections fail the three-ON persistence gate in every configuration, as expected from their occupancy.

The important sensitivity limit is demonstrated rather than assumed: the persistent detector recovers only one of three placements at the strongest tested amplitude. C03's strict-track failure therefore supplies no broad exclusion of weak physical emitters. Conversely, the planted lines do not explain C03 or prove it is an emitter.

## What the earlier series and Wow! actually contribute

The original [Wow! concordance](https://mindcontrolpoems.blogspot.com/2025/10/concordance-between-wow-signal-and.html), credited to Johannes Sigil, explicitly presents resonance rather than confirmation. Its current body links the six printed intensities to doubling, primes, ratios and quantities in the early Atlas series. The retrieved current HTML and extracted text are preserved. This pass does not establish a historically frozen version of that body or reverify every astronomical quantity in it.

There are four useful constraints, with distinct evidence roles:

1. **Intermittency.** [Kipping and Gray (2022)](https://arxiv.org/abs/2206.08374) model a stochastic repeater using the Big Ear logs and follow-up coverage. Their analysis makes observing windows and duty cycle explicit. It supports testing intermittent source families rather than requiring three ON detections; it does not demonstrate that Wow! was such a source or that C03 shares its origin.
2. **Instrumental timing and quantization.** [Ehman's detailed account](https://www.bigear.org/Wow30th/wow30th.htm) explains the ten-second integrations, roughly twelve-second record cadence, adaptive background estimates, and integer intensity display. The record 6EQUJ5 denotes intensity ranges. Its shape is compatible with a source crossing Big Ear's beam. The roughly 72-second record is not an established universal transmission period. A tracking telescope should not be required to reproduce that envelope. Under the user's receiver-aware hypothesis, a display-addressed code remains an admissible separate proposal, but its quantizer, gain assumptions, codebook and control family must be fixed before validation. Factorizations of the rounded display values alone do not transfer an emitted message to another receiver.
3. **Frequency provenance.** [Méndez et al. (2025), arXiv:2508.10657v1](https://arxiv.org/html/2508.10657v1) propose 1420.726 ±0.005 MHz, revising older values through channel-order and local-oscillator corrections checked against other archival signals. The abstract page currently describes a preprint intended for submission. This is a proposed calibration revision, not a reason to silently discard older values or treat the origin as settled. A search using a historical Wow! frequency must carry its source version, bandwidth and frequency-frame transformation; neither 1420.4556 nor 1420.726 MHz can simply be relabelled the emitter's rest frequency.
4. **Geometry.** [Loeb's 28 September 2025 article](https://avi-loeb.medium.com/was-the-wow-signal-emitted-from-3i-atlas-d18d4f0d1f1e) itself reports about nine degrees of separation from 3I/ATLAS's inferred 1977 direction, not overlap with a Wow! localization. Its light-travel-time adjustment is part of the emission/arrival calculation, not an independent date coincidence. A shared-location claim would need backward propagation of an orbit solution with uncertainties, both possible Wow! beam positions and their errors; a new association model would have to explain the separation. No such association has been established here.

The earlier series' strongest methodological lead remains a restricted relation that transfers: a decoder learned on one observation should predict something in unused data. Unit-invariant ratios and deliberate human-unit/display echoes are different test branches. Receiver awareness does not invalidate the latter, but it does not remove their trial cost. The previously documented arithmetic error 70/4.5 ≈ 14/9 still needs correction; related orbital quantities cannot be counted as independent coincidences.

## Where those clues can guide the next search

**The practical new lead is the Green Bank hydrogen-frequency data in node blc24, paired with a bounded intermittent detector.** This is a different spectral region of the same cadence, not another observing epoch. It offers unused powers for this specific follow-up, with appropriate background and frequency-frame checks. No blc24 spectral values were interpreted in this pass.

The public index provides exact six scan-13–18 high-resolution filenames. Their URLs are saved in sources/prospective-GBT-hydrogen-urls.json. Header inspection of scan13 establishes coverage 1313.9648465–1501.4648438 MHz, approximately 2.794 Hz channels and 6.084537-second integrations. Thus the physical hydrogen line and the two historical Wow! frequency proposals fall inside its instrumental coverage. They remain different hypotheses with different frame requirements, rather than interchangeable centers for finding whichever peak is strongest.

A next finite pass should freeze the physical hydrogen rest-frequency branch first, explicit time-window durations, motion model, allowed frequency error, independent comparison windows, injection family and reserved observations. Preserve scan gaps and include single-ON events. Simultaneous spatial controls are preferable; sequential OFF nondetection cannot by itself localize an intermittent event to the comet. Natural hydrogen emission, gain changes and interference remain competing explanations for any selected structure. A receiver-conventional Wow! echo could be a separate finite branch after its encoding/frame rules are specified.

This is a search design supported by the historical example, not a claim that Wow! and 3I/ATLAS are connected. The current C03 result supplies no specifically AI-operated-source signature.

## Other public products and observation coverage

All eight requested GBT headers were resolved through bounded public range reads, including HDF5 metadata near file ends. Only metadata were interpreted. Exact URLs, attributes, read ranges and byte hashes are retained. Neighboring high-resolution nodes have contiguous center-frequency ranges:

| Node | Scan13 low–high channel centers, MHz |
|---|---|
| blc21 | 1876.4648465–2063.9648438 |
| blc22 | 1688.9648465–1876.4648438 |
| blc23 | 1501.4648465–1688.9648438 |
| blc24 | 1313.9648465–1501.4648438 |
| blc25 | 1126.4648465–1313.9648438 |
| blc26 | 938.9648465–1126.4648438 |

These headers provide no duplicate neighboring-node coverage of C03. Two other blc23 products of the same observation have 2861.023 Hz /1.073742 s and 366210.938 Hz /0.000349525 s spectral/time resolution respectively. They may test broader or faster structure, but cannot independently resolve a few-hertz C03 tone, and they are not new sky observations.

The official [Breakthrough Listen overview](https://seti.berkeley.edu/atlas/overview.html) lists Parkes UWL coverage 704–4032 MHz on 31 July, 12 September and 5 October 2025. Public epoch indexes and their child links are saved. This pass did not resolve new Parkes per-file metadata or interpret Parkes powers. It does not turn earlier child-link 403 responses into a claim of universal data inaccessibility. Appropriate independent-epoch confirmation remains outstanding; actual ON17 tracking remains outstanding. No external contact was made.

## Reproduction and checks

- Six native NPZ archives passed saved SHA-256 and ZIP CRC checks; all six restored NPY hashes match the prior ledger.
- 156 legacy per-candidate/per-scan scores reproduce within 1e-12. This validates preservation of the previous normalization result.
- All 36 independently accumulated full/half scalar scores agree with the vector scores to less than 1e-12.
- Zero-amplitude injection leaves the tested full native power array bitwise unchanged. All 18 two-normalization configurations and their uninjected comparators are retained.
- core.py, inputs/, results/, source_map.py, sources/, checksums, logs and the figure are included in the evidence package. Full score-vector caches and six large powers are excluded; their existing Library identities are in inputs/native-input-ledger.json. The script regenerates score caches from those powers. It requires NumPy and SciPy; source_map.py additionally requires h5py for metadata inspection.

The earlier original-thirteen results remain historical results. This report refines C03's model dependence; it does not replace source-unknown with a human-source label, claim a detection, or treat a model-dependent null as a verdict on artificiality.
