# What the boundary search can recover

3I/ATLAS · GBT 18 December 2025 UTC · analysis 18 November 2026

**The previous all-three-ON clock rule can miss genuine inserted messages.** Combining weak amplitude and phase evidence across the ON scans improves recovery in this experiment, especially for BPSK and for a transmitter absent from the middle ON scan. The measured C03–C13 observations still yield **zero nominations** under the new screen. Sensitivity remains poor at the weakest tested levels, and an interference control produces one false nomination, so this is not an exclusion of arbitrary faint communication.

## Main results

Twelve deterministic message/carrier/epoch configurations per modulation family were added to copies of the measured voltage backgrounds. The backgrounds rotate through eleven previously selected coordinates, so these are not twelve independent random observations. The added power fraction rho is measured **inside the final 8 Hz low-pass filtered complex stream**, including message zero slots and inactive burst periods. It is not the published GBT detection SNR, a flux density, EIRP, or a statement about being below the published inspected threshold.

At rho = 0.10, the new screen detected 12/12 amplitude-keyed messages, 7/12 BPSK messages, and 9/12 intermittent messages. At rho = 0.30 it detected 12/12 of each family; the previous rule detected zero BPSK and zero intermittent messages at that same level. At rho <= 0.03, neither screen detected any of the tested insertions. These are discrete observed recovery counts for the specified waveforms and configurations, not a fitted universal sensitivity boundary.

Detection and reading differ. The configured packet receiver recovered every payload exactly in all families at rho = 1.0, but recovered only 2/12 amplitude-keyed, 8/12 BPSK and 9/12 intermittent payloads exactly at rho = 0.30. Its known preamble, rate and packet-start bracket are substantial information supplied by the experiment. No such communication standard has been established for the actual observations.

## What changed in the detector

Coordinates remain fixed to C03–C13; C01/C02 are not promoted back into the candidate set. The input consists of the previously verified phase-preserving two-feed voltage subbands. The same Horizons comet-motion correction, 8 Hz low-pass filter, decimation to 44.70348 samples/s and two-second edge exclusions are used. All 66 newly recomputed correct-track filtered streams exactly match the corresponding previous saved streams.

Two feature families are evaluated: envelope periodicity at cyclic frequencies 0.1–4 Hz, and squared-complex-voltage spectral structure at cyclic frequencies -8 to +8 Hz. The second can detect BPSK-like phase structure but can also respond to ordinary tones; it does not identify a modulation standard. Each feature is normalized by identically processed nearby frequency comparisons. The score is the mean log feature ratio across ON scans minus its mean across OFF scans. Scan phases are never connected coherently.

The screen requires geometric-mean ON feature ratio >=1.5, with at least two ON ratios >1.25, rather than demanding a strong clock in all three ON scans. It evaluates 357 envelope-frequency cells and 1,467 squared-phase cells per coordinate. These frequency cells and the control searches are correlated.

The nuisance threshold was frozen before the final injection analysis: **1.671673**, the maximum eligible score across 176 local-comparison searches and 132 wrong-motion searches (both feature families included). Local comparisons lie at ±24, ±48, ±72 and ±96 Hz. Wrong tracks perturb the predicted motion by slopes ±0.05, ±0.10 and ±0.20 Hz/s about each scan midpoint. These are deliberately wrong local tracks, not independent ephemerides or sky observations. All filter passbands remain within the retained 715.26 Hz projections.

The strongest correct-track result is **C06, score 1.347900**, an envelope feature near 1.8772 Hz. It does not outrank the nuisance controls. The highest nuisance score is also in the C06 neighborhood, but on a wrong track of -0.10 Hz/s, at a different cyclic frequency near 0.3929 Hz. This supplies no preference for the comet-associated interpretation of the measured modulation features.

## The messages inserted

Each packet contains a 16-bit 0xDDAA preamble followed by 104 ASCII payload bits, `ATLAS TEST NN`, and repeats at two symbols/s. The families are return-to-zero on/off keying (RZ OOK), BPSK, and intermittent RZ OOK. Carrier offsets are random within ±2 baseband Hz, fixed across scans within each trial; receiver-feed phases, scan phases and packet epochs vary. The detector receives none of the packet bits, carrier, epoch or symbol-rate truth.

Continuous OOK and BPSK are inserted only in the three ON scans. Intermittent OOK is inserted only in ON0013 and ON0017 during scan-time windows [5,85] and [155,235] seconds; ON0015 contains no insertion. The three OFF scans are unchanged in the main recovery trials. Because rho includes inactive periods, burst power while active is higher than its whole-window average; recovery counts are not a general ranking of modulation families.

Inserted waveforms are constructed at the 715.26 Hz subband sample rate and passed through the same final FIR/decimation filter before scaling and addition to measured backgrounds. This is a voltage-subband injection experiment. It does not simulate digitizer quantization, analog receiver response, arbitrary propagation, or wideband modulation outside the retained projections. At two measured raw-derived waveform witnesses, filtering before/after additive insertion agrees to a maximum complex-amplitude error of 1.20e-7.

## Packet recovery assumptions

The separate packet receiver estimates carrier from a voltage or squared-voltage FFT without using the inserted carrier. It searches eight packet epochs in the declared [5,5.5] second bracket at the declared rate of two symbols/s, learns feed gains and decision levels from the known 16-bit preamble, then decodes the next 104 bits. Only afterward are payload bits compared against injection truth. No payload bits participate in epoch selection or gain fitting.

Thus exact payload recovery is a test of a configured receiver with a known preamble and rate, not blind discovery of an unknown code. Poor performance at low power includes carrier and preamble acquisition failures as well as symbol errors. The blind detector and configured receiver can succeed or fail separately; both counts and their intersection are retained.

## False nominations and limits

All zero-insertion rows produce zero nominations, but those rows reuse eleven measured backgrounds and are not independent null trials. Likewise the nuisance searches used to choose the threshold cannot estimate its false-alarm rate: they fall below the final strict cutoff by construction.

A separate sanity check inserted strong modulation in **both ON and OFF scans**, with matching carrier and duty cycle within each family. **One of twelve such controls was nominated**: intermittent-family seed 3, envelope frequency 3.7980 Hz, score 1.689465. It is a false association with the ON scans in this controlled experiment. Its frequency differs from the inserted two-symbol/s clock. The threshold and detector were not adjusted after this failure. Twelve controls are insufficient for a calibrated false-alarm probability, and the one false nomination is a reason to demand independent confirmation for any future nomination.

The experiment therefore supports a specific repair: the old all-three-ON envelope gate can reject actual phase-modulated or intermittent inserted messages, and a joint amplitude/phase screen can recover some of them. It also exposes the remaining limitation: no insertions at 0.3%, 1% or 3% of filtered background power were detected here. We cannot use this null result to exclude those weak test messages, much less an unspecified alien encoding.

This is an exploratory revisit of already inspected, previously selected coordinates. It tests a small waveform family, finite motion/frequency ranges, one rate, and a specific packet receiver. It does not establish a universal sensitivity curve or a published astronomical upper limit.

## Reproducibility

`PLAN.md` and its hash record the experiment. `IMPLEMENTATION-NOTES.md` identifies corrections to the initial injection implementation before interpreting final curves; measured baseline features, detector and threshold did not change. The report uses only the corrected run. Every trial, payload error count, estimated carrier, measured target score, control score, waveform seed and injected packet is retained.

The evidence bundle includes measured filtered target backgrounds, local/wrong-motion feature spectra, previous-gate comparison spectra and powers, a measured raw-derived linearity witness, code, ephemeris metadata and prior voltage provenance checks. Run `python3 experiment.py` with NumPy, SciPy and Matplotlib to replay the calibration using those cached inputs. Recomputing the raw-subband comparison features from scratch additionally requires the six prior full-cadence subband arrays listed in `INPUTS-original-voltage-sources.json`. Cached features suffice to reproduce scores, thresholds, receiver trials and figures.

## Recovery counts

Each entry uses 12 configurations and 104 payload bits per configuration. Exact-payload recovery is receiver-assisted, independent of whether the blind screen nominates the waveform.

| Family | Added power / background | Joint detections | Previous gate | Exact payloads | Detected and exact | Payload BER |
|---|---:|---:|---:|---:|---:|---:|
| ook | 0 | 0/12 | 0/12 | 0/12 | 0/12 | 0.5016 |
| ook | 0.003 | 0/12 | 0/12 | 0/12 | 0/12 | 0.4976 |
| ook | 0.01 | 0/12 | 0/12 | 0/12 | 0/12 | 0.4519 |
| ook | 0.03 | 0/12 | 0/12 | 0/12 | 0/12 | 0.3269 |
| ook | 0.1 | 12/12 | 10/12 | 0/12 | 0/12 | 0.1234 |
| ook | 0.3 | 12/12 | 12/12 | 2/12 | 2/12 | 0.0216 |
| ook | 1 | 12/12 | 12/12 | 12/12 | 12/12 | 0.0000 |
| bpsk | 0 | 0/12 | 0/12 | 0/12 | 0/12 | 0.5168 |
| bpsk | 0.003 | 0/12 | 0/12 | 0/12 | 0/12 | 0.5128 |
| bpsk | 0.01 | 0/12 | 0/12 | 0/12 | 0/12 | 0.5208 |
| bpsk | 0.03 | 0/12 | 0/12 | 0/12 | 0/12 | 0.4856 |
| bpsk | 0.1 | 7/12 | 0/12 | 0/12 | 0/12 | 0.0473 |
| bpsk | 0.3 | 12/12 | 0/12 | 8/12 | 8/12 | 0.0032 |
| bpsk | 1 | 12/12 | 6/12 | 12/12 | 12/12 | 0.0000 |
| intermittent | 0 | 0/12 | 0/12 | 0/12 | 0/12 | 0.5016 |
| intermittent | 0.003 | 0/12 | 0/12 | 0/12 | 0/12 | 0.5024 |
| intermittent | 0.01 | 0/12 | 0/12 | 0/12 | 0/12 | 0.4848 |
| intermittent | 0.03 | 0/12 | 0/12 | 0/12 | 0/12 | 0.2500 |
| intermittent | 0.1 | 9/12 | 0/12 | 1/12 | 1/12 | 0.0441 |
| intermittent | 0.3 | 12/12 | 0/12 | 9/12 | 9/12 | 0.0024 |
| intermittent | 1 | 12/12 | 0/12 | 12/12 | 12/12 | 0.0000 |
