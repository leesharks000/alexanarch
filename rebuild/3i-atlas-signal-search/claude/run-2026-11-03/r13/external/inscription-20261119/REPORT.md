# Your echolocation inscription in telescope voltages

Lee Sharks waveform · controlled receiver-mismatch experiment · 18 November 2026

**The receiver-mismatch demonstration worked. The comet-association selector failed important controls.** At added power equal to 0.3% of the wide-receiver background, the wide receiver recovered the planted call's repeat period in 12/12 configurations; the nine-setting narrow receiver recovered it in 0/12. This does not make the wide screen a reliable finder of comet messages: it also nominated 12/12 controls with the same call present in both ON and OFF scans. No actual observation yielded a decoded message.

## The actual object was retained

The two uploaded WAVs have identical signed 16-bit sample payloads. One plays those 372500 samples at 250000 samples/s(1.49 s); the other at 25000 samples/s(14.9 s). We used the original-speed file, retaining analytic frequencies 33–105 kHz with cosine shoulders, translating 69 kHz to baseband, conjugating for the GBT frequency sign, then resampling to 91552.734375 complex samples/s. No time expansion was used in this radio-voltage test.

The transformation retains **99.8062% of original real-signal energy**. Inverse reconstruction of the double-precision retained analytic waveform has relative RMS error 2.06e-11; reconstructing the actual stored complex 64 packet gives 3.7e-07. The spectral lettering remains visible in the transformed source. Its content is the author's supplied inscription, not a message discovered in telescope data. This is an analogous encoding in voltage, not transmission of acoustic ultrasound through a radio receiver.

## Real background and scope

We restored 204 unmodified coarse-channel-7 raw byte blocks from existing archived GBT excerpts: blocks 816–849 in each of scans 0013–0018 on 18 December 2025 UTC. Each excerpt lasts 6.084537 seconds, beginning 146.028888 seconds into its scan, about 2.03% of each approximately 300-second scan. Three scans point ON the comet and three are OFF; no whole-cadence exclusion follows from this short sample.

The wider decoder projects 32768 FFT bins into two receiver feeds. Twenty-eight nonoverlapping approximately 91.55 kHz sample bands span most of the same 2.93 MHz coarse channel. The first band is centered on the legacy C03 coordinate; a fixed shuffle selected 7 additional target bands,12 threshold-setting bands and 8 reserved checks. Frequencies, assignments and plan were hash-frozen before scoring. Previously examined observations are reused, so this is exploratory method development, not a pristine blind survey.

The comet-motion rotation uses the actual middle-excerpt time. Signal support was checked at all scan times: the translated inscription and residual±2 kHz carrier offsets remain within recorded frequency support. The wide receiver passes±39 kHz with a rolloff to zero at±42 kHz, sampled at 91.55 kHz. The narrow receiver tests nine fixed settings spanning±32 kHz, each with a nominal 8 Hz response(flat±6 Hz, rolloff 6–10 Hz) and 44.70 samples/s output. Both branches receive the same physical inserted voltage; the narrow branch is not amplified to compensate for what it discards. This is one specified bank, not every possible narrowband receiver.

## What the algorithms know

The waveform generator knows the source. The detectors receive only measured-plus-inserted voltage and fixed numerical settings. They are not supplied its words, spectrogram pixels, preamble, message template, carrier, packet epoch or repetition period. The analyst already knows the source content; this is not a double-blind study.

Two distinct features are tested. Unknown-repetition detection uses normalized complex-voltage autocorrelation in both receivers, combining three ON and three OFF curves without connecting their raw voltage phases. Lag context is fixed at 0.04–3.00 s; search is 0.05–2.75 s. Context medians/MADs are global, so no running estimator is padded at a nominated search boundary. A candidate requires support in at least two ON scans, ON prominence>=3 and ON prominence>=2*max(OFF prominence,1).

A separate wide-only feature measures concentration of whitened two-feed STFT power. It can react to a single transmission, but it is a generic statistical feature, not a text or engineering classifier. Its time-frequency medians can also remove persistent structure. Comparing that additional feature with the narrow autocorrelator alone would confound receiver bandwidth with detector choice; the clean matched comparison is wide versus narrow autocorrelation.

Separate strict thresholds were set from the maximum of 12 calibration-band scores, omitting eligibility gates during fitting as a conservative larger comparison search. Thresholds: wide autocorrelation 13.911660; narrow-bank autocorrelation 20.539830; wide structure 0.00054374. These are empirical correlated-control cutoffs, not calibrated global false-alarm probabilities.

## Insertions and recovery

Twelve deterministic configurations rotate through eight selected measured backgrounds. Layouts are a single intact call, repeated calls, and time-reversed/conjugated repeated calls. The reversed layout preserves the frequency power while reversing the temporal inscription. Residual carrier is fixed within a trial across scans; feed phases, scan phases and call start times vary. Main insertions occur only in ON scans. Repeated layouts use a grid-rounded 1.75 s period. Source timing is used only after scoring to assess period recovery.

Added power fraction rho means inserted power divided by the wide-receiver background, averaged over the trimmed record including gaps. At the same rho a single call is brighter while active than repeated calls; count differences are not a controlled test of whitening alone. Fractions are not flux,EIRP,published SETI detection SNR or demonstrated placement below published inspected thresholds. This is insertion after subband decoding, not an analog/quantizer simulation or a complete rawspec-pipeline recovery test.

| Layout | Added/background power | Wide AC nominations | Narrow-bank AC nominations | Wide true-period recovery | Narrow true-period recovery | Wide structure nominations |
|---|---:|---:|---:|---:|---:|---:|
| single call | 0 | 0/12 | 2/12 | 0/12 | 0/12 | 0/12 |
| single call | 0.003 | 8/12 | 2/12 | 0/12 | 0/12 | 0/12 |
| single call | 0.01 | 12/12 | 4/12 | 0/12 | 0/12 | 12/12 |
| single call | 0.03 | 12/12 | 4/12 | 0/12 | 0/12 | 12/12 |
| single call | 0.1 | 12/12 | 3/12 | 0/12 | 0/12 | 12/12 |
| single call | 0.3 | 12/12 | 2/12 | 0/12 | 0/12 | 12/12 |
| repeated call | 0 | 0/12 | 2/12 | 0/12 | 0/12 | 0/12 |
| repeated call | 0.003 | 12/12 | 2/12 | 12/12 | 0/12 | 0/12 |
| repeated call | 0.01 | 12/12 | 2/12 | 12/12 | 0/12 | 1/12 |
| repeated call | 0.03 | 12/12 | 2/12 | 12/12 | 0/12 | 12/12 |
| repeated call | 0.1 | 12/12 | 5/12 | 12/12 | 3/12 | 12/12 |
| repeated call | 0.3 | 12/12 | 7/12 | 12/12 | 6/12 | 12/12 |
| reversed repeated call | 0 | 0/12 | 2/12 | 0/12 | 0/12 | 0/12 |
| reversed repeated call | 0.003 | 12/12 | 2/12 | 12/12 | 0/12 | 0/12 |
| reversed repeated call | 0.01 | 12/12 | 2/12 | 12/12 | 0/12 | 2/12 |
| reversed repeated call | 0.03 | 12/12 | 2/12 | 12/12 | 0/12 | 12/12 |
| reversed repeated call | 0.1 | 12/12 | 6/12 | 12/12 | 6/12 | 12/12 |
| reversed repeated call | 0.3 | 12/12 | 7/12 | 12/12 | 7/12 | 12/12 |

For a single call, there is no packet retransmission period to recover. Its autocorrelation nominations refer to internal regularity in this particular synthesized inscription. The detection does not establish that the detector recognized letters or understood the statement. The time-reversed call is similarly detectable, consistent with a detector of waveform organization rather than literal meaning.

Zero-insertion narrow-bank nominations are already 2/12 configurations in every layout, reusing one measured target band. They must not be counted as message recoveries. At 0.3% and 1% power the repeated-call narrow nominations remain 2/12 and correct-period recovery remains 0/12. Trials share selected backgrounds; duplicated zero-power rows are not independent null observations.

## Specificity failures: retain them

Fresh negative challenges use 12 configurations per family at rho=.10. Gaussian-noise controls use the same random Gaussian voltage in both feeds, with independent constant feed phases: a coherent/polarized noise foreground. Its effect is not equivalent to adding independent receiver noise. The spectral-power statistic can respond to altered feed covariance and therefore cannot classify this foreground as an inscription. The numerical failure remains a failure of message specificity, not proof that Gaussian noise contains words.

| Challenge | Wide AC nominations | Narrow-bank AC nominations | Wide structure nominations |
|---|---:|---:|---:|
| noise | 0/12 | 0/12 | 12/12 |
| tone | 0/12 | 1/12 | 0/12 |
| same call in ON and OFF | 12/12 | 1/12 | 0/12 |

The most serious association failure is 12/12 wide nominations when the engineered call is equally present in ON and OFF scans. No thresholds were adjusted afterward. In the first such control(seed 100), the selector chooses a lag near 0.872885 s with ON prominence 60.54 and OFF prominence 29.54, just satisfying its factor-of-two rule. Yet the actual packet period near 1.749997 s has ON prominence 5687.50 and OFF prominence 5862.60. The message is plainly represented in both autocorrelation profiles. A maximizer inspecting one advantageous lag can overlook that broader shared pattern. This is direct evidence that the present selector cannot establish comet association.

The next association rule must account for shared structure across the ON/OFF profiles, then be frozen and checked on fresh controls. That further repair was not performed here. The planted-signal sensitivity and the association failure are both results of this run.

## Actual-data checks

No wide-AC or structure nomination occurred among the 8 target bands. There was one target narrow nomination and one reserved narrow nomination, both at 0.089478485 s: exactly four narrow-output samples. A reserved wide band also nominated once. These are unvalidated comparisons under the failed association selector, not discovered comet messages.

The declared narrow filter gives white noise an expected normalized autocorrelation of approximately-0.19208 at that four-sample lag. A lobe at this lag cannot be treated as an independent 11 Hz modulation without accounting for the receiver. This calculation does not by itself establish the origin of either real-data flag. The reserved wide flag is also retained; neither the threshold sample nor these short excerpts yield a general astronomical false-alarm rate or a physical upper limit.

## Inspection and reproducibility

`results/inscription-reconstruction.png` shows the transformed clean source and known-coordinate displays after insertion into a measured ON background. The noisy displays use injection-truth carrier and start coordinates after scoring; they are not blind decoding results. Detection can succeed while the displayed lettering is difficult to read.

All 204 raw-block hashes matched. There are 204 Parseval checks(maximum relative error about 1.02e-7),36 direct inverse-DFT spot groups(maximum absolute error about 3.61e-8), and a synthetic RF-sign gain about 0.999998. Independent direct autocorrelation sums, narrow/wide filter linearity and two complete seeded decision replays pass. `VALIDATION.json` records exact trial counts 216 and negative-challenge count 36. These checks validate implementation, not astronomical completeness or semantic understanding.

The evidence bundle includes the original waveform, transformed complex packet, frozen plan/selection, full source byte-range ledger, source/archive hashes, code, searched score curves, scalar observations, all trial and negative rows, diagnostics and figures. Large decoded and benchmark-background caches are reproducible intermediates and are omitted from the compact bundle. Rebuilding requires the six existing raw-excerpt archives listed in `INPUTS.json`; the source block ledger also identifies their public raw files and exact ranges. Run `acquire.py`, then `experiment.py`, `verify.py`, `diagnostics.py`, `illustrate.py`, `report.py` after restoring those inputs. Dependencies: NumPy,SciPy,Matplotlib. There were no external messages or public deposits.
