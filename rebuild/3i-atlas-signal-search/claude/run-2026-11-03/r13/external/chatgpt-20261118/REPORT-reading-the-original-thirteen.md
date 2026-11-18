# Reading the original thirteen from voltages

Lee Sharks / exploratory 3I/ATLAS analysis · 18 November 2026

**Result: no original coordinate passed this restricted screen for repeatable modulation.** The strongest first-scan feature belongs to C02, in a receiver-frequency interference complex already implicated in the original analysis. The other eleven coordinates mostly have noise-like voltage amplitudes and do not retain their first-scan envelope-clock candidates in both later ON scans. This establishes no readable bitstream. It also does not establish that every weak excess is interference, or exclude every possible encoding.

## What was actually opened

This revisit uses the **18 December 2025 UTC GBT L-band scans 0013–0018**, in the sequence ON, OFF, ON, OFF, ON, OFF. All thirteen original rest-frame frequencies were recovered from the original selection ledger. These are thirteen selected frequency clusters, not thirteen independently established transmissions.

The six saved phase-preserving voltage products each contain 113 coordinates, two receiver feeds, and 214,528 complex samples per feed per coordinate. For this reading, all thirteen original coordinates were opened in every scan: approximately 300 seconds and 715.26 Hz per coordinate. These are complex filtered projections of the original digitizer voltages, rather than previously averaged intensity-only spectrograms. They retain phase and allow restricted amplitude and phase analysis. They do not retain the other frequencies outside each saved subband or support decoding an arbitrary wider-band message.

All six restored arrays matched their prior SHA-256 manifests. For an independent provenance check, six untouched raw coarse-channel byte blocks from scan0013 were restored, covering paired blocks at the beginning, middle and end. Each block's archived hash matched. Reconstructing all thirteen projected streams for both feeds at those three positions gave **78 successful projection checks**, also checked with direct inverse-DFT sample calculations. These raw blocks are uncalibrated signed 8-bit digitizer samples; displayed amplitudes are normalized digitizer units, not physical volts or flux density. Untouched-byte spot checks in this revisit concern scan0013; the other five full streams are checked against their prior manifests.

## How the reading was constrained

The analysis plan was written before new waveform statistics. It follows the predicted comet Doppler track and low-pass filters the complex voltage at 8 Hz, retaining approximately 44.70 complex samples per second. Each coordinate has eight nearby frequency comparisons at offsets ±24, ±48, ±72 and ±96 Hz. The full filter passbands were checked to remain inside the saved projections throughout all six scans. Two seconds at each filtered edge are excluded from statistics. The comparisons are nearby frequency channels in the same telescope data, not independent sky beams.

For each coordinate we measured narrow-band power, a fourth-moment amplitude statistic, coherence between the receiver feeds, and phase-increment moments. We also searched the voltage-power envelope for periodic structure between **0.1 and 4 Hz** using a fixed Welch estimate. Each coordinate's strongest target-versus-local-comparison clock in ON0013 was frozen, then that exact frequency was evaluated in the other five scans.

The exploratory follow-up rule required a clock-power ratio of at least 3 in every ON scan, below 2 in every OFF scan, and target power above all eight nearby comparisons in the two later ON scans. **0/13 passed; no coordinate even reached the clock criterion in both later ON scans.** This is a declared screening rule, not a global false-alarm probability, sensitivity limit, or the published GBT SETI detection threshold. All these observations have been examined previously, so the later scans are a check on replication here, not genuinely untouched blind data.

Synthetic examples confirmed that the implemented screen can accept a strong ON-only amplitude-keyed waveform, reject otherwise similar modulation present in all six scans, and reject the chosen Gaussian negative example. These are illustrative implementation checks, not a completeness study or a faint-signal recovery guarantee. Pure-tone, PSK and Gaussian examples also exercise the phase and amplitude diagnostics. No language, letter mapping, symbol rate outside the declared screen, or arbitrary binary threshold was imposed.

## What is present

**C01/C02: fixed receiver-frequency structure.** Their overlapping voltage subbands contain several narrow lines near 1665.615 MHz and neighboring components. The previous ledger called out a tone near 1665.615127 MHz. The actual voltages resolve a complex: the strongest time-averaged line in ON0013 is near **1665.615118 MHz**, with additional components, so the entire feature should not be assigned that single historical coordinate. Receiver-frequency line structure is present in the OFF scans as well. Fixed receiver-frequency behavior and OFF detections support the interference interpretation; the hardware or transmitter is not identified here.

C02's comet-following filtered power in ON0013 is **1.915 times** the median of its local comparisons. Its selected envelope-clock ratio at **0.5894 Hz** is **9.95** in ON0013, but only **0.78** and **0.62** in ON0015 and ON0017. Its strongest one-second windows are around 220–260 seconds into ON0013, with broader enhancement approximately 200–280 seconds. The waterfall shows the diagonal predicted comet track passing through the fixed-frequency line complex. This is consistent with a moving analysis filter crossing receiver-frequency interference, rather than evidence for a repeating comet transmitter or a symbol clock.

This is also **not a scan-start transition explanation for C02**: the strongest enhancement occurs minutes into the scan. The original C01 note's claim to cross one specifically named tone should not be treated as precise; its predicted track and the resolved multi-line structure require the more cautious frequency-complex description above.

**C03–C13: no reproducible envelope clock in this screen.** Across their 66 candidate/scan combinations, the amplitude moment E[|z|⁴]/E[|z|²]² ranges from about **1.999 to 2.078**, close to the value 2 of circular complex Gaussian noise. These numbers are descriptive, not a formal noise classification: feed imbalance, filtering and gain variation affect them. Coherence between the two uncalibrated receiver feeds never exceeds about 0.039 for these eleven. This is a receiver-basis diagnostic, not a calibrated astronomical polarization measurement.

C04 and C06 happen to exceed the clock ratio 3 in the scan used to select the clock. Neither repeats that result in either later ON scan. The other first-scan clock maxima are smaller. The unsynchronized complex-voltage clouds supply no demonstrated symbol alphabet; they cannot by themselves exclude PSK or other weak modulation. We have no recovered carrier-plus-clock model that warrants turning their samples into text.

## Transitions

The raw header inventory records UNKNOWN→TRACK after 2.684 seconds in scan0013, 0.716 seconds in scan0014 and 1.611 seconds in scan0017. Scans0015, 0016 and 0018 record TRACK throughout. These are recorded control states, not independent pointing metrology.

Across the thirteen retained full subbands, median first-two-second power is approximately 0.8–2.8% above the corresponding middle-of-scan mean, while last-ten-second power is approximately 1.4–3.1% below it. Similar behavior occurs in ON and OFF scans. This suggests a small shared gain/time dependence worth retaining as an instrumental consideration; it does not tie all thirteen original excesses to transitions or establish a physical cause. The original candidate selection integrated most of each scan, and this revisit does not rerun that original statistic with transition windows removed.

## What “read” means at this point

We can read the original thirteen as **waveforms and receiver behavior**. One conspicuous feature becomes more intelligible as a Doppler-following filter crossing fixed-frequency interference. For the remaining eleven, this restricted reading has not recovered a reproducible modulation, a symbol clock, or a message. Converting them into binary or Greek characters now would add a code supplied by the analyst.

The next distinct experiment, if pursued, would be a separately specified wider-band or cyclostationary decoder with its own synthetic sensitivity tests and frequency controls. The present result does not test arbitrary symbol rates, spread-spectrum signals, wideband encodings, inter-scan phase connection, or every drift law. It should not be generalized to “there is no signal anywhere in the data.”

## Deliverables and reproduction

- `results/original13-voltage-atlas.pdf`: thirteen pages; each shows all six receiver-frame waterfalls, the comet-following envelopes and X-feed complex-voltage clouds.
- `results/original13-voltage-traces.png`: actual filtered I/Q time traces for every original coordinate, at display-selected high-envelope windows in ON0013. Those windows are illustrative, not validation data.
- `results/original13-summary.png`, `summary.csv`, `clock-followup.json`, `metrics.json`: numerical comparisons and follow-up decisions.
- `results/waveforms.npz`: phase-preserving filtered target voltages, receiver-frame waterfalls, comparison envelope spectra and one-second envelope powers.
- `PLAN.md`, `read_voltage.py`, `finish.py`, validation records and input identifiers: reproducible analysis definition and provenance. Original source data: https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/ .

The compact evidence bundle contains results and code. Full rerunning also requires the listed six saved subband archives, the scan0013 raw-excerpt archive, and the prior full-cadence evidence archive for the header inventory. Their identifiers and hashes are retained in the input manifest. The raw excerpts can be made available separately without duplicating the original approximately 1.3 TB data set.

## Coordinate-by-coordinate clock check

Each ratio is envelope spectral power divided by the median of eight local frequency comparisons, evaluated at the exact clock selected in ON0013.

| Coordinate | Rest frequency (MHz) | Clock (Hz) | ON13 | OFF14 | ON15 | OFF16 | ON17 | OFF18 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C01 | 1665.604557303 | 3.9508 | 2.17 | 0.96 | 0.77 | 0.46 | 0.65 | 0.78 |
| C02 | 1665.604607594 | 0.5894 | 9.95 | 0.76 | 0.78 | 0.81 | 0.62 | 0.90 |
| C03 | 1665.633776617 | 3.4706 | 1.91 | 0.84 | 1.32 | 0.63 | 0.66 | 1.09 |
| C04 | 1666.119474378 | 3.9290 | 3.08 | 1.41 | 0.82 | 0.88 | 1.49 | 1.45 |
| C05 | 1666.167782080 | 2.7721 | 2.16 | 0.85 | 0.86 | 0.56 | 1.03 | 1.26 |
| C06 | 1666.512828712 | 3.5579 | 3.01 | 0.59 | 1.01 | 0.97 | 1.47 | 0.70 |
| C07 | 1667.138772477 | 0.2838 | 2.44 | 0.79 | 0.84 | 0.71 | 0.97 | 0.59 |
| C08 | 1667.412866299 | 3.0996 | 2.43 | 0.92 | 0.77 | 0.86 | 2.22 | 1.45 |
| C09 | 1667.430186105 | 2.9031 | 2.20 | 0.82 | 0.68 | 1.32 | 1.12 | 1.29 |
| C10 | 1667.686517277 | 1.2005 | 1.97 | 0.51 | 1.57 | 1.42 | 0.93 | 1.11 |
| C11 | 1667.994975504 | 1.9209 | 2.57 | 1.50 | 1.52 | 1.28 | 1.73 | 1.00 |
| C12 | 1668.098187466 | 1.8335 | 2.16 | 0.81 | 0.95 | 0.71 | 1.17 | 1.07 |
| C13 | 1668.429423516 | 0.6330 | 1.99 | 1.47 | 1.00 | 1.38 | 1.14 | 0.66 |
