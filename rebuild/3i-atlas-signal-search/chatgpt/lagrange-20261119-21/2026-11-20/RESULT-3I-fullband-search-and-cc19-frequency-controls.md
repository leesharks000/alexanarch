# 3I/ATLAS search checkpoint — completed full-band M4b and cc19 matched-channel frequency test
**20 November 2026, after the 64-channel M4b run completed.**

## Full band, frozen detector
Primary source: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/RESULTS-M4b.md

GBT 2025-12-18 scans 0013–0018, channel frequencies ~1500–1688 MHz, 64 coarse channels. Frozen detector: Class A 287 on the three target scans vs 506 in reversed roles. Six channels have a positive Class-A count difference (cc01, cc19, cc21, cc23, cc48, cc50), all in terrestrial/orbital communications allocations. Source report says no Class A event in the surveyed band with comet-matching nonzero drift outside allocated bands. The separate M4 original method nominated 59 signals but its saved per-candidate voltage-battery files were mostly lost in a container restart; source: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/RESULTS-M4.md

## Independent catalogue inspection, 16 channel samples (exploratory)
Fetched each exact source `M4b/events/ccNN.json` via the GitHub connector, read the retained `events` frequencies, and applied this explicit pair-anchored frequency grid search to **all A+B saved events**:

For each pair of event-frequency coordinates `f_i,f_j`, for each integer gap `g=1..20`, set candidate spacing `s=(f_j-f_i)/g`. Retain `65000 <= s <= 70000` Hz. For each other event `f_k`, compute nearest integer `n=round((f_k-f_i)/s)` and a residual `abs(f_k-f_i-n*s)`. Count *distinct integer positions* with residual <=25 Hz. The maximum across anchor pairs and gap counts is reported. A score of 2 is a trivial two-event match. A no-pair channel can score 0.

| cc | retained events | Class A full count | control A | best number of aligned positions |
|---:|---:|---:|---:|---:|
| 03 | 18 | 1 | 2 | 2 |
| 08 | 19 | 0 | 0 | 2 |
| 14 | 24 | 0 | 0 | 2 |
| 15 | 7 | 0 | 0 | 0 |
| 19 | 19 | 6 | 0 | **8** |
| 29 | 32 | 0 | 1 | 2 |
| 30 | 25 | 0 | 1 | 2 |
| 35 | 16 | 0 | 0 | 2 |
| 36 | 27 | 0 | 1 | 3 |
| 37 | 40 (truncated) | 0 | 0 | 3 |
| 38 | 40 (truncated) | 0 | 1 | **5** |
| 39 | 40 (truncated) | 0 | 0 | 3 |
| 40 | 40 (truncated) | 0 | 1 | 3 |
| 41 | 5 | 0 | 0 | 2 |
| 42 | 2 | 0 | 0 | 2 |
| 43 | 8 | 0 | 0 | 2 |

For cc19, a pair-derived spacing of 67437.71955370903 Hz matches eight distinct aligned positions within 25 Hz. Its seven additional nominally matched weaker lines include the Class-B grid siblings recovered in the prior analysis. This only tests frequency regularity among **already selected event locations**; it cannot establish contemporaneous physical signals.

### Defeat conditions and cautions
- Channel samples were not random; they are 16 investigator-selected channels, with highly variable saved-list sizes.
- The frequency search [65,70] kHz, the 25 Hz tolerance and the emphasis on cc19 are post-hoc, not blind. Because each trial fits anchoring pairs, a count of two is trivial. No global p-value or controlled look-elsewhere result is available.
- Reversed-role samples `control_top` were not used in this 16-channel grid comparison; a follow-up should perform the **same pair-grid optimization on equally complete reversed-role event lists** and resampled synthetic RFI datasets.
- A small number of parallel carriers could be related by instrumentation or telecommunications channel structure. The region of cc19 (1626.5–1660.5 MHz) is a licensed Earth-to-space MSS band, not a protected or RFI-clean region (47 CFR §25.202).
- The full-band run is negative for comet-following narrowband technosignatures under the plan's gates. Frequency organization within one interference-rich channel is a testable anomaly, not a detected ET sender.

## Other candidate family deliberately retained
Original M4 notes: https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4/NOTES-NOMINATIONS.md
cc08 at ~1663.3270 MHz has a single ON13 feed-Y event, local z=7.25, W1=29.7 at 0.181 Hz, k4=2.19, not repeated among ON15/ON17 top events and not among OFF top events. Protected radio-astronomy allocation is not a guarantee of RFI absence. The M4b drift analysis at cc08 returns A=0 vs control A=0. This is not a survivor; inspecting its fixed-frequency per-scan power is the specific falsifiable next step.

## Productive next search
Shift effort from single strong narrowband detections to *nonstandard modulation and relational structure* in interference-quieter frequency ranges and independent epochs. Use native per-integration voltage/spectral arrays, compare fixed preselected positions to off-source and alternate time/frequency frames, include injected controls and record non-detections. Follow-up must not reinterpret selected source lists as unbiased samples.
