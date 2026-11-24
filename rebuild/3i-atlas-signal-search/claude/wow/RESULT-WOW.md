# The Wow! signal read as instructions for mining the 3I/ATLAS data: the operations it gives select what any single-peaked shape selects, and the hydrogen line holds nothing in the comet's frame

**2026-11-23/24.** At the author's word (21:51 EST): "okay lets now mine the wow! signal to see if it can be read as instructions for how to mine the voltage data". Plan frozen before any product: PLAN-WOW.md, FROZEN-WOW.sha256 (02:56 UTC); amendment 1 frozen before it was read: AMENDMENT-1.md, FROZEN-WOW-A1.sha256. Products hashed in WOW-PRODUCTS.sha256.

## 1. The reading

The Wow! signal's recorded properties (Méndez et al., arXiv:2508.10657, 2025; Wikipedia, "Wow! signal") were each read as an operation:

| | Property | Operation |
|---|---|---|
| W1 | 1420.726 ± 0.005 MHz, the hydrogen line + 320 kHz (revised; Ehman's value + 49.8 kHz) | look at the hydrogen line, and at those offsets, in 3I/ATLAS's frame |
| W2 | one 10 kHz channel of 50 | read at ~10 kHz |
| W3 | 10 s integrations every 12 s; SNR 6, 14, 26, 30, 19, 5 ("6EQUJ5"; the six sum to 100) | match that six-step profile in time |
| W4 | one horn of two, positive minus negative | in an ON scan, not in the OFF that follows |
| W5 | the six values as numbers | blc23 coarse channels 5, 6, 14, 19, 26, 30 (deferred) |

## 2. Stage 1: the profile in time (W2–W4), blc21–26, 939–2064 MHz

The Wow template was matched against every 8.58 kHz channel of the public rawspec products (.0002) of all six nodes, in all six scans, at 10 s per 12 s. Detection: score ≥ 6 in an ON scan, < 3 in the OFF after it.

- **The Wow template finds 4,245 ON-only events.** 2,933 of them light in no other scan.
- **They are satellites.**
  - The densest clusters are GLONASS L1 at 1593–1595 MHz and GPS L1 near 1575 MHz.
  - Iridium sits at 1621–1626 MHz, with the strongest single event at 1615.77 MHz in ON 0017, score 1,460.
  - There is a uniform band at 1186–1195 MHz in blc25, about 116 events per MHz.
  - These are transmitters crossing a sidelobe, and a crossing rises and falls the way a source drifting through Big Ear's beam did.
- **Against the frozen controls**, the Wow ranks above 65–97% of the 200 permutations of its own values and 57–95% of the 200 random sequences, depending on the node. Across all nodes it ranks above 82% of the random sequences.
- **Against smooth single-peaked shapes (amendment 1)**, it ranks above 3–73%, depending on the node.
  - The permutation result shows only that the events are smooth bumps.
  - Across all nodes it finds 4,245 events against a median of 4,247 for the 200 smooth controls: exactly the middle of its class.
- **Reading.** Among single-peaked shapes the Wow's own profile picks out nothing. As an instruction, W3 says "look for a rise and fall over a minute", and in these data that finds satellites.

## 3. Stage 2: the hydrogen line in the comet's frame (W1), blc24, 1419.43–1422.36 MHz

Four targets were read in the full-resolution product (.0000, 2.79 Hz × 6.08 s) at ±5 kHz, the Wow's own uncertainty:

| Target | Mean ON/OFF − 1 | Contrast per pair | Rank vs 200 random targets |
|---|---|---|---|
| T1, 1420.726 topocentric | 0.036 | 0.096, 0.003, 0.008 | 0.055 |
| T2, the hydrogen line in the comet's frame | 0.040 | 0.100, 0.016, 0.006 | 0.055 |
| T3, hydrogen + 320 kHz, comet frame | 0.036 | 0.096, 0.004, 0.009 | 0.055 |
| T4, hydrogen + 49.8 kHz, comet frame | 0.042 | 0.104, 0.018, 0.004 | 0.625 |

- **No excess.** The control targets' mean contrast is 0.0415, ranging from −0.005 to 0.086.
- **T1–T3 sit lower than 94.5% of the controls.** Strong Galactic H I emission in both pointings flattens an ON/OFF ratio, so the line region reads low. That is the sky, not the comet.
- **The first pair runs high everywhere, controls included.** It is a gain step between scans 0013 and 0014.
- **No narrow core.** The peak bin inside each ±5 kHz band reaches z 1.8 to 3.9 in ON and OFF scans alike, which is the maximum of about 3,600 noise bins.

## 4. W5, read but not run

The six values taken as blc23 coarse channels give 1671.39–1674.32 (5), 1668.46–1671.39 (6), 1645.03–1647.96 (14), 1630.38–1633.31 (19), 1609.86–1612.79 (26) and 1598.16–1601.09 MHz (30).

- **One lands on a spectral line.** Channel 26 holds the 1612.231 MHz OH line.
- **That is not unusual.** Three of blc23's 64 channels hold OH lines, so a random six-channel draw reaches one 26% of the time.
- **What running it would cost.** The voltages of channels 5, 6, 14, 26 and 30 would be about 100 GB of range reads. Channel 19's are already read (RESULT-GBT-cc19-raw-voltages-C19).

## 5. What this establishes

- The Wow! signal, read as procedure, gives a time profile, a channel width, an ON/OFF rule and a frequency pointer.
- On these data, the time profile selects what every single-peaked shape selects: satellites.
- The frequency pointer lands on the hydrogen line, where neither the Wow's number nor its offsets in the comet's frame hold a feature.
- The ON/OFF rule and the channel width are the search's own already.
- **Verdict:** under the readings tested, the Wow does not instruct beyond what the search already does. W5 remains open.
- **What the reading did teach.** The beam-transit envelope that made the Wow look like a source is, at GBT in 2025, the signature of a satellite crossing a sidelobe. A single-horn, single-pass, rise-and-fall event is exactly what a sidelobe transmitter produces when the pointing moves away from it.
