# PLAN-WOW: the Wow! signal read as instructions for mining the 3I/ATLAS data

**2026-11-23, 21:51 EST, at the author's word:** "okay lets now mine the wow! signal to see if it can be read as instructions for how to mine the voltage data". Frozen before any product (FROZEN-WOW.sha256). Under the search's standing rules: a failed test forbids nothing further; it only withholds the word *signal* under the criteria tested. Reading meaning as meaning, and noise as noise.

## 1. What the Wow! signal is, as recorded

Sources: Méndez et al., "Arecibo Wow! II: Revised Properties of the Wow! Signal from Archival Ohio SETI Data", arXiv:2508.10657 (2025); Wikipedia, "Wow! signal" (read 2026-11-23).

- Big Ear, Ohio State, 1977-08-16 03:16:06 UTC (revised). Transit instrument: the sky drifts through the beam; any point is seen for about 72 s (revised ≥ 73.4 ± 0.5 s).
- Receiver: 50 channels of 10 kHz (500 kHz). The signal sits in one channel (channel 2), under 10 kHz wide.
- Frequency: 1420.726 ± 0.005 MHz (revised; Ehman's 1420.4556, Kraus's 1420.3556). The neutral hydrogen line is 1420.40575 MHz; the revised value is 320 ± 5 kHz above it.
- Sampling: 10 s integrations at a 12 s cadence (2 s of processing).
- "6EQUJ5": the signal-to-noise in each 12 s sample in base 36 (1–9, A = 10 … Z = 35): 6, 14, 26, 30, 19, 5. The six values sum to 100. Peak SNR 30.1 ± 0.4 (revised).
- Two horns, about three minutes apart on the sky; the record is positive minus negative. The signal appeared in one horn only; which one is unknown. It was not seen again.

## 2. The reading: each property as an operation on the data

The voltages are GBT blc23 (1501.465–1688.965 MHz, scans 0013–0018, ON 0013/0015/0017 on 3I/ATLAS). The public rawspec products cover blc21–26 for the same scans, including blc24 (1313.965–1501.465 MHz), which holds 1420 MHz. The Wow's operations are read as follows; each names its free choices, because each free choice is a way for pareidolia to enter.

| | Wow property | Operation read from it | Free choices |
|---|---|---|---|
| W1 | 1420.726 MHz: the hydrogen line plus 320 kHz | look at the hydrogen line, and at the Wow's offset from it, in 3I/ATLAS's frame | which frame; the offset taken as +320 kHz (revised) or +49.8 kHz (Ehman) |
| W2 | one channel of 50, under 10 kHz | read at ~10 kHz resolution, not Hz | none beyond the resolution |
| W3 | 10 s integrations, 12 s cadence, the profile 6-14-26-30-19-5 | match the six-step profile in time, at that sampling | none: the template is the record |
| W4 | one horn of two, positive minus negative | present in an ON scan, absent from the OFF that follows | none: this is the cadence's own test |
| W5 | the six values 6, 14, 26, 30, 19, 5 | as indices: blc23 coarse channels 5, 6, 14, 19, 26, 30 in the voltages | that the values are indices at all |

W5 is the loosest reading and is deferred to a second stage (the voltages of coarse channels 5, 6, 14, 26 and 30; channel 19 has been read, RESULT-GBT-cc19-raw-voltages-C19).

## 3. The pareidolia measure

Every test runs twice: on the Wow's settings, and on controls built the same way.

- **S1 controls:** 200 templates that are the Wow's six values in random order (does the rise-and-fall order matter?), and 200 templates of six values drawn at random from 1–35 (does this sequence matter at all?).
- **S2 controls:** 200 random target frequencies in the same coarse channel, away from the hydrogen line by more than 50 kHz, processed identically.

A Wow-derived result counts as more than chance only if it ranks above 95% of its controls. Ranking within the controls is reported either way.

## 4. Stage 1 (W2 + W3 + W4): the profile in time, across the band

- Data: rawspec .0002 (2.861 kHz × 1.074 s), blc21–26, scans 0013–0018, streamed, not kept.
- Frequency rebinned 3:1 to 8.58 kHz (one channel of under 10 kHz). Time: 10 s sums every 12 s (W3), 24 samples a scan.
- Per channel, SNR per sample against the scan's median and robust σ (the Big Ear baseline being the preceding minutes).
- Score: the maximum over time of the correlation of the SNR series with the template (unit-normalised), in sigma units of that channel's own correlations.
- Detection: score ≥ 6 in an ON scan, and the same channel's score < 3 in the OFF scan that follows it (W4).
- Report: detections for the Wow template (frequency, scan, score, whether the frequency also lights in other scans), the count for each control template, and the Wow's rank.

## 5. Stage 2 (W1): the hydrogen line in the comet's frame

- Data: rawspec .0000 (2.794 Hz × 6.08 s), blc24, the coarse channel holding 1420.4–1420.8 MHz, scans 0013–0018, streamed; ±60 kHz windows kept.
- Targets: T1 1420.726 MHz topocentric (the Wow's number as given); T2 the hydrogen line at rest in 3I/ATLAS's frame; T3 the hydrogen line + 320 kHz in that frame; T4 the hydrogen line + 49.8 kHz in that frame. The comet frame uses the Horizons ephemeris already in the search (voltages/delaymod).
- Statistic: power in a ±5 kHz band (the Wow's uncertainty) at each target, tracked, integrated per scan; ON−OFF contrast; also the narrowest feature (peak bin z at 2.8 Hz) inside the band.
- Controls: 200 random targets, as in §3.
- Note: Galactic H I emission is broad and on-sky; the OFF pointing sits nearby, so it largely subtracts. Anything at T2–T4 that also appears in OFF is sky or ground, not comet.

## 6. What would count

A reading that ranks above 95% of its controls and yields a comet-frame or ON-only feature is information worth reading further, in the voltages where they reach (blc23) and by asking for blc24's where they do not. A reading that ranks among its controls has not been shown to instruct; it has still been read, and the features it finds are reported as found.
