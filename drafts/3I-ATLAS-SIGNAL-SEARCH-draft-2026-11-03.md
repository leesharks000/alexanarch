# What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-Data Signal Search

Nobel Glas · Transactions on Substrate Engineering · preliminary write-up, draft of 2026-11-03 · not deposited (further numbers to run first)

Working record of an investigation run 2026-11-02 and 2026-11-03 by Lee Sharks with two machine collaborators working in parallel on the same public data: Claude (this session, the Green Bank and MeerKAT work and the autonomous-sender classes) and ChatGPT (the Allen Telescope Array work, the audit of the Green Bank thirteen, the numerical-anchor and new-band searches). Each system's reports, code and results are stashed beside this draft (§11). ChatGPT is still running tests on the thirteen; §7 will take those results in.

## 0. Result in brief

0.1 No artificial transmission has been identified. Every persistent-tone, compensated-frame, intermittent, periodic and numerical-anchor test run so far either fails its screen, fails its held-out continuation, or lands in a satellite allocation.

0.2 One empirical result stands unresolved: in the Green Bank L-band cadence of 2025-12-18, a comet-frame coincidence count at 1665.53–1668.46 MHz gives 13 clusters against 3.75 ± 2.05 (maximum 8) for 40 false-acceleration frames. It reproduces exactly under an independent implementation, belongs to the on-source beam, and is sensitive to normalization and threshold (§7).

0.3 The findings that hold are findings about representation: what a summarizing system makes of a scientist's position, what a published pipeline's documented filter retains, what a classification label asserts, what a public data product preserves, and what two machine collaborators got wrong about their own work until the code and tables travelled between them (§1, §2, §5, §8).

## 1. The Overview

1.1 The investigation began with a Google AI Overview on Avi Loeb and 3I/ATLAS. The innocent reading first: the Overview gave the consensus that 3I/ATLAS is a natural comet and placed Loeb inside it, by way of his own words in an interview of December 2025, that the object is "most likely natural."

1.2 What the composition did, as the ChatGPT thread recorded it: it "made a December 2025 interview concession—'most likely natural'—carry its account of Loeb's subsequent position, without reconstructing the development and qualifications of his argument, even while citing later writing."

1.3 Loeb's later writing holds both halves. On 2026-04-23 ("Where is 3I/ATLAS Now?", avi-loeb.medium.com) he writes that "its fading light curve does not show any evidence for artificial (self-produced) light," lists the anomalies by theme with a probability for each ("aligned to within 5 degrees with the orbital plane of the planets around the Sun, with a probability of 0.2%"), and concludes: "Altogether, these anomalies led me to rank 3I/ATLAS as Level 4 on the Loeb Scale." A concession and a ranked argument stand in the same author's record; the composition carried the concession forward as the position.

1.4 The mechanism is temporal flattening under quotability. A dated, short, quotable sentence from an interview outranks a long argument with qualifications, and once composed it reads as the author's settled view. The incentive is legibility to the summary's reader; the function is that the argument's development drops out of the record the reader receives.

1.5 Gap: the Overview's text is held in the ChatGPT thread and is absent from this session. It should be seated as a capture from its paste, with its query, before this section quotes it.

## 2. The verdict and its scope

2.1 Two teams published radio searches: the Allen Telescope Array (Sheikh et al., arXiv:2512.18142v2, accepted manuscript of 2026-05-20) and Green Bank (arXiv:2512.19763v1, observations of 2025-12-18). FAST published a third in 1.05–1.45 GHz.

2.2 The public account compresses them to a closed question. Intelligent Living (2026-09-11, updated 2026-09-30): "The question everyone was waiting for has an answer, and it is a firm one." On the ATA pipeline: "the team identified nearly 74 million narrowband hits in 7.25 hours of data … When the 211 strongest hits were manually inspected in the time-frequency domain, every single one turned out to be human-made interference."

2.3 The scope of a null is set by what its filters retained. The ATA paper reduced roughly 74 million hits to 211 plotted events through frequency blanking (for instance 1075–1116 MHz), a signed drift-rate interval, beam comparison and visual selection. A result bounded by those rules travels as "a firm one." The investigation's question became: what could these searches recognise, and what did their rules remove before anyone looked.

## 3. The hypothesis

3.1 Lee Sharks's five working conditions (2026-11-02): artificial; highly aware of our blindspots and our precise epistemic and technological capacities and incapacities; technologically able to control signal as meaning; operating at the very boundary of determinability; and meant "to be visible as signal to those who know how to look. that is the point of the just-so razor, to teach how to read."

3.2 The Just-So Razor is the archive's own term, from THE ATLAS PERIHELION PRANK (#454, AXN:010F, Nobel Glas, 2026-02-06): "a limit condition where an event or object contains precisely the minimum necessary evidence to register as anomaly to those reasoning within a narrow epistemic band, while remaining deniable to all others." That volume keeps the natural-comet hypothesis H₀ and explores H₁ under a claim firewall.

3.3 Refinement of 2026-11-03: a craft from elsewhere is far more likely supervised by advanced machine systems than crewed by organic beings, and such a system, monitoring Earth's radio, would learn our ways of thinking by pattern matching. The default SETI assumption of a sender unfamiliar with the receiver gives way to a sender familiar with it. The search pipelines are open source and their cuts are published, so the blindspots are readable from the documentation.

3.4 Two clarifications have governed the work since. "Boundary of determinability" need not mean faint: the uncertainty can sit in origin, organisation or interpretation at a detectable amplitude. And any proposed reading has to constrain another observation (a frequency, a relation, a decoding rule) and be tested on data not yet read.

## 4. The data

4.1 Breakthrough Listen's 3I/ATLAS data are public at bldata.berkeley.edu/ATLAS/: MeerKAT hit lists (seticore, S/N ≥ 6, 64 beams), ATA two-beam high-resolution Stokes-I spectra (1.907 Hz × 16.78 s), GBT rawspec products in three resolutions (among them 2.79 Hz × 6.08 s and 2.86 kHz × 1.07 s), Parkes directories.

4.2 A hit list and a spectrum permit different questions. A thresholded list lets a reader re-examine what was detected; spectral powers let a reader search below the detection threshold. Neither preserves voltage phase or fast time structure. Several directories returned HTTP 403 to the machine collaborators while their parents opened; those failures were request-specific, and Lee could download the files himself.

## 5. Findings about the classifiers

5.1 **The ATA drift sign.** The paper (§3.2) takes "the time derivative of the deldot parameter within JPL Horizons," finds accelerations of 3.2 to 3.5 × 10⁻⁵ km/s² in all five sessions, converts them with drift = acceleration × frequency / c (Sheikh et al. 2019, Eq. 1), reports the expected drift as positive ("the minimum drift rate of 3I/ATLAS would be 0.15 Hz/s" at 1336 MHz; "the maximum drift rate of 3I/ATLAS would be 1.01 Hz/s" at 8728 MHz), and states: "We filter our hits for drift rates between 0.05–1.5 Hz/s at all frequencies." The text gives no sign. Figure 4 does: its "Drift Rate Range Hits" occupy 0 to +1.5 Hz/s on the signed axis and none of the negative half.

5.1.1 The physics. Received frequency is f = F (1 − v/c) with v the range-rate, positive for recession. A rising range-rate lowers the received frequency, so a positive acceleration gives a negative drift. Checked in this session at the ATA site (Horizons, 2025-07-03): deldot −51.440 km/s at 06:50 UTC, −51.377 at 07:20, an acceleration of 3.49 × 10⁻⁵ km/s², matching the paper's figure; the drift of a constant tone riding on the object is −0.125 Hz/s at 1075 MHz and −0.19 Hz/s at 1623.75 MHz. The ATA filterbanks carry a positive channel spacing (foff +1.907 Hz, checked on the July 3 LoA.C1504 beam-0 header), so a reported drift needs no sign flip to mean what it says; ChatGPT's reading of the archived bliss source found no flip either.

5.1.2 What follows. The paper derived the right magnitude, gave it the sign of the acceleration, and its figure retains the positive interval. On the paper's own figure, the drift it computed for an emitter on 3I/ATLAS lies in the half its filter removed. Its stated purpose for the cut is "To filter out signals that do not match the dynamics of 3I/ATLAS." The executed filter script and the signed before/after catalogues have not been obtained, so the claim stands on the manuscript, the figure and the physics; it does not show that a transmission was discarded. A search of part of the excluded class found no convincing signal (ChatGPT, 2026-11-02).

5.1.3 Elsewhere. The FAST search (arXiv:2603.19023) gives its expected drifts as positive magnitudes (0.105–0.207 Hz/s) and tabulates its "Used ⟨ν̇⟩ range" as (0, 0.15) and (0, 0.25); its Equation 1 writes the bound on |ν̇|, so whether its executed filter is signed is unsettled from the text. The Green Bank paper (arXiv:2512.19763) searched ±4 Hz/s with a sky-localisation filter and describes no drift cut. The one public review found, an AI review on pith.science (grok-4.3, 2026-05-22), asked the authors to "Specify the exact drift-rate search range (in Hz/s)" and raised no sign question. No published comment, erratum or critique raising the sign was found (searches of 2026-11-03).

5.2 **"Human-made" as a label.** For the paper's two illustrated rejections: Figure 7 sits at 1626.675919 MHz, above Iridium's 1626.5 MHz service edge; CEPT ERC Report 91 documents Iridium unwanted emissions above that edge, so Iridium stays plausible, and no particular transmitter is identified. Figure 8 shows similar strength in both beams, which supports rejection as an unlocalised source without identifying it. The published sentence ("every single one turned out to be human-made interference") states an identification where the procedure supplies a classification. The raw-data audit of all 211 events has not been done.

5.3 **The zero-drift class.** The ATA paper's retained interval (+0.05 to +1.5 Hz/s) excludes zero drift, in keeping with the general practice of treating zero-drift narrowband hits as terrestrial. A sender that pre-compensates its Doppler for the receiving telescope arrives at zero drift. Claude tested this class on the GBT OH channel with the beam swap as control: 3 on-source clusters against 7 with the beams swapped. Nothing is there (§6).

5.4 **The pointing header.** The source-header position of GBT ON scan 0017 lies 16.108 arcmin from the comet's ICRF position (9.827 arcmin from apparent); scans 0013 and 0015 lie within 0.16 and 0.71 arcmin. The GBT beam is about 7.6 arcmin FWHM at 1667 MHz. Public code shows the header as a first-file snapshot of the status fields; it says nothing on whether the telescope had settled on target. The discrepancy is established in the metadata; mispointing is not. Antenna telemetry for 05:08:17–05:13:15 UTC would resolve it. No request has been sent.

5.5 **What a hit list keeps.** MeerKAT's lists hold S/N ≥ 6 only. Every comet-locked test on them (exact comet drift, comet-frame recurrence, the OH and hydrogen windows) returned nothing localised (§6). A sender operating at the boundary of determinability falls below the list by construction, so the null bounds only what the list was built to keep.

## 6. Signal tests, all to date

| Data | Test | Run by | Result |
|---|---|---|---|
| MeerKAT hit lists, 6.0 M hits, 6 days | exact comet drift (T1) | Claude | target-beam rate 0.70%, control beams 1.24% |
| MeerKAT | comet-frame recurrence across days | Claude | no excess under 400 random frame shifts (87% tie or exceed); an earlier per-beam form of the count is superseded |
| MeerKAT | ±5 kHz of 1612, 1665, 1667 MHz in the comet frame; H, H/√2, H/φ | Claude | zero hits in any beam |
| MeerKAT | 1420.549–1420.558 MHz feature, 2025-12-19 | Claude | all 64 beams, slopes −10 to +10 Hz/s: Galactic hydrogen |
| ATA, 1074.75–1075.75 MHz | three-scan persistent tracks, ±4 Hz/s | ChatGPT | 15 maxima on shared structures; 0 of 40 exact continuations |
| ATA, 1420 MHz | eight families (physical drift, partial compensation, stationary, mirrored, one-scan, alternating, steps, wide line) | ChatGPT | none passed; 128/128 stronger injections recovered |
| GBT, 1665.53–1668.46 MHz | comet-frame coincidence, z 2.5/2.0 | Claude | **13 clusters vs 3.75 ± 2.05 (max 8)** (§7) |
| GBT, same channel | same rule at 2.0/1.5 and 3.0 | Claude | no excess (rows: 118 vs 120.9 ± 12.5); 1 at 3.0 |
| GBT, 1665 MHz channel | same rule | Claude | 5 vs 5.7 ± 2.2 |
| GBT, 1420 MHz channel | same rule | Claude | 3 rows vs 4.0 ± 3.0 at 2.5 |
| ATA, July 3 | C03 fixed-frequency follow-up | ChatGPT | no flag (lower sensitivity, other epoch) |
| ATA, July 3 | six GBT alternate-detector locations | ChatGPT | 0 flags in 24 combinations |
| ATA, July 3, 1665.75–1667.25 MHz | full-band comet frame | ChatGPT | 4 vs 4.475 ± 3.07; all four fail held-out continuation |
| ATA, July 3, 1666.75–1667.75 MHz | numerical anchors: OH 1667.35903 rest; 1667.000 at emitter; 1667.000 at receiver; bursts and three-tone combs | ChatGPT | no discovery flag; no continuation flag |
| GBT OH channel | observer-compensated frames: GBT (zero drift), geocentre, barycentre | Claude | 3 (swap 7); 7 (swap 7); 5 (swap 3): no on-source side |
| GBT OH channel | single-scan bursts, z ≥ 6 | Claude | ON-minus-OFF 6, against 3.08 ± 2.40 in false frames (12.5% reach it) |
| GBT S-band, coarse channel containing 2500 MHz | the comet-frame procedure and beam swap, frozen in advance | Claude | 0 on-source (swap 2) vs 2.95 ± 1.56 (max 8): the property does not replicate (§7.8) |
| GBT 1501.5–1689 MHz, 1.07 s | periodic 2.15–150 s; broadband pulse trains; single-sample events | Claude | 173 periodic pairs, all in GNSS, Inmarsat or Iridium allocations; 0 broadband; events in satellite bands |

## 7. The thirteen

7.1 Method (Claude, 2026-11-02; code oh13/cometframe_raw.py): GBT blc23 coarse channel 7, scans 0013–0018 (ON 0013, 0015, 0017). Each channel divided by its time median, minus one; three-channel boxcar; rows summed along the path a tone fixed on 3I/ATLAS takes (Horizons range-rate at the GBT site); robust z per scan; scans aligned in the comet rest frame. Kept: z ≥ 2.5 in all three ON scans and < 2.0 in all three OFF scans, ±1 channel; merged at 10 Hz. Null: the whole procedure under 40 false range-accelerations (0.03–1 Hz/s at 1.42 GHz, seed 11).

7.2 Reproduction (ChatGPT, 2026-11-03): all 13 clusters and all 78 rounded per-scan scores reproduce; the true-frame score vectors match the supplied function bitwise; the 40 controls reproduce mean 3.75, SD 2.046, maximum 8, none reaching 13. A plus-one rank of 1/41 is the descriptive figure; it carries none of the trial history and is no global p-value.

7.3 Robustness, same data:

| Variant | True | Controls mean (max) | Controls ≥ true |
|---|---:|---:|---:|
| original | 13 | 3.75 (8) | 0/40 |
| exact rest-grid spacing | 12 | 3.63 (9) | 0/40 |
| fixed-tone veto ±10 Hz | 12 | 3.73 (8) | 0/40 |
| fixed-tone veto ±60 Hz | 11 | 3.73 (8) | 0/40 |
| frequency-baseline normalization | 6 | 3.43 (9) | 7/40 |
| other ON/OFF role triples (19) | 0–6 | | |
| beam swap (Claude) | 1 | 3.33 (9) | ON minus swap 12 vs max 6 in 40 false frames |

7.4 The excess belongs to the on-source beam: no false frame reaches it, no false frame gives an ON-minus-swap difference above 6, and the actual ON triple gives 13 where the other nineteen role assignments give 0–6. It weakens under a frequency-baseline normalization (6, with 7 of 40 controls reaching it) and vanishes at the neighbouring thresholds.

7.5 Natural line checked: cometary OH would fall within about ±11 kHz of 1667.359 or 1665.402 MHz in the comet frame. The nearest of the thirteen, C08 at 1667.412866 MHz, is 54 kHz away. The thirteen do not trace the comet's OH.

7.6 Members. C02 crosses a stationary line complex near 1665.61512 MHz present in all six scans, ON and OFF (about 91% of its positive 0013 contribution near the complex's peaks; four peaks at about 60.35 Hz spacing): contamination. C01 sits in the same complex (52% of its 0015 contribution) without crossing its central carrier. C03–C13 are unresolved; for each, the largest single sample carries at most 9–14% of the positive contribution in any ON scan, so they are no single-spike artefacts. C03 (1665.633777 MHz) survives the alternate normalization (ON 2.546, 2.820, 2.966; OFF 1.623, 1.069, 0.168) and the removal of its two largest samples; it failed its fixed-frequency test in the ATA July session, which is less sensitive and from another epoch.

7.7 Per step the candidates average about 0.35σ; their rest frequencies show no spacing, mirror or whole-kHz structure beyond random sets. The cadence has no second L-band pass in the public directory: the same night's later blc23 cadences are at 2.4–2.6, 7.7–7.9 and 11.6–11.8 GHz. A held-out test needs an ATA or Parkes session at 1667 MHz with sensitivity near the GBT's, the thirteen frequencies and the rule frozen; or the property (a beam-sided comet-frame excess) tested in another band under the same frozen procedure.

7.8 The property in another band (Claude, 2026-11-03, plan frozen before reading, sha256 ca251bf3…). GBT blc23 S-band cadence of the same night, scans 0029–0034, coarse channel 30 (contains 2500 MHz, chosen by round number), the procedure and null of §7.1 unchanged. True frame: 0 on-source clusters, 2 with the beams swapped. Forty false frames: 2.95 ± 1.56 (maximum 8); every false frame reaches or exceeds the true count. Outcome by the frozen rule: BOUNDS. The beam-sided comet-frame excess does not appear at 2.5 GHz.

## 8. What the collaborators got wrong, and what corrected it

8.1 Claude's MeerKAT beam matching used a ±20-channel (about 32 Hz) window and missed counterparts a few kHz away in broad features. The first "localized" counts (310, 47, 628) overstated localisation and are withdrawn.

8.2 Claude's oh13 README said C01 and C02 "cross a fixed topocentric tone at 1665.615127 MHz." C02 does; C01's path stays at least 27.5 Hz from that carrier while occupying the comb around it (§7.6). ChatGPT caught the wording.

8.3 Claude's periodicity script concatenated the three ON scans across their gaps before the FFT, and the shuffle test the README describes is absent from the packet.

8.4 ChatGPT could not reproduce "118 versus 120.9" from the stated configuration. The saved run resolves it: raw/OH_cometframe_z2.0.json records z_on 2.0, z_off 1.5, 118 coincidence rows against 120.92 ± 12.50 over 24 false frames of seed 7. The units were rows, unclustered, and the null was a different set. The "maximum 10" first reported for the 2.5 cut comes from the same seed-7 run (16 rows against 5.38, maximum 10), before clustering gave 13.

8.5 ChatGPT's first 1667 MHz pass reported no excess in ±5 kHz of the OH line and was read as adjudicating the thirteen. The thirteen span 2.93 MHz and none lies in that window. ChatGPT entered a dated scope correction once the candidate table arrived.

8.6 The status of the thirteen changed when the artefacts travelled. As a narrative pasted from one system to the other, the result was an "unresolved exploratory statistic"; once code, candidate table and hashes arrived, it was reproduced bitwise within hours, its members audited, and two of its descriptions corrected. Two machine collaborators on public science reach agreement through the artefacts and only through them; the prose summary of either one carried errors the other could not see.

## 9. What this shows about representation

9.1 At each layer a compression decided what the next reader receives. The Overview carried a scientist's dated concession as his position (§1). A press account carried a filtered null as a firm answer and a classification as an identification (§2, §5.2). A documented filter appears to exclude the emitter model it names (§5.1). A metadata field records a snapshot and reads as a measurement (§5.4). A thresholded list keeps the detections its threshold admits and loses the boundary below it (§5.5). Two summarizing systems, reading their own work, reported counts in units that differed from their code and labels their data did not support (§8).

9.2 None of this requires motive. Each compression has an incentive (legibility, tractability, a pipeline's throughput) and a function (what drops out). The conditions under which the boundary of determinability can be examined at all are the ones that preserve the uncompressed layer: powers below threshold, executed code, signed catalogues, telemetry, the paste of the composition itself.

## 10. Open

10.1 ATA: the executed blanking script and the signed before/after catalogues; raw audit of the 211.
10.2 GBT 0017: antenna telemetry for 05:08:17–05:13:15 UTC.
10.3 The thirteen: ChatGPT's current tests; a frozen held-out test (§7.7).
10.4 The Overview: seat its paste as a capture before quoting it.
10.5 Author and venue ruled 2026-11-03: Nobel Glas, Transactions on Substrate Engineering, the author and the line of THE ATLAS PERIHELION PRANK (#454). Further numbers run before deposit (§7.8).

## 11. Files stashed (rebuild/3i-atlas-signal-search/)

- `claude/oh13/`: the thirteen, with per-scan coordinates and tracked paths (CSV, JSON), README and code.
- `claude/autonomous/`: observer-compensated frames, beam-swap null, periodic and pulsed tests: README, code, results.
- `claude/meerkat-gbt/`: the earlier MeerKAT sweep and boundary scripts, GBT comet-frame scripts, summaries and saved run results (including the seed-7 runs of §8.4).
- `chatgpt/`: ChatGPT's reports as Lee supplied them: investigation summary, ATA three-scan search (2026-11-02), direct audit of the thirteen, numerical-anchor search, new-band search, and its running checkpoint. Its evidence packages and native cutouts stay in ChatGPT's library under the links those reports give.

Raw spectra (about 1.3 GB of cutouts and hit lists) are omitted; every script fetches its inputs from the public directory by name.
