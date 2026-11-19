# RESULTS-C14: the cc14 nomination is a single burst, 0.7 s long, in ON0013

Plan: PLAN-C14.md, frozen 2026-11-19T14:52:29Z (PLAN-C14.sha256). Products: z.json and v_0013.npz … v_0018.npz.

## 1. Uncapped z at the two predictions (z.json)

| Scan | Role | Comet: max z | False frames reaching it | Fixed: max z | False frames reaching it |
|---|---|---:|---:|---:|---:|
| 0013 | ON | 1570 | 0 | 1570 | 0 |
| 0014 | OFF | < 2 | – | < 2 | – |
| 0015 | ON | < 2 | – | < 2 | – |
| 0016 | OFF | < 2 | – | < 2 | – |
| 0017 | ON | 3.49 | 0 | < 2 | – |
| 0018 | OFF | < 2 | – | 2.80 | 53 |

1. In ON0013 the two predictions coincide. None of the 100 false-motion stacks reaches it.
2. At the comet prediction, ON0015 has nothing above z 2. ON0017 has z 3.5, which no false stack reaches in that window; it is weak, and it is not the burst (§2.4).

## 2. The voltages

Frames are 0.358 s. The wide view covers ±1024 bins (5.72 kHz) in 64 groups of 89 Hz.

1. ON0013 has one event, frames 664–665, 237.83–238.19 s into the scan (about 04:51:04 UTC, given the scan start of 04:47:06). The frames on either side are at noise (1.0× the median).
2. In frame 664, the power at the predicted bin is 2,303× the median in feed X and 4,557× in feed Y. Across the whole 5.72 kHz view, the median group is 15× (X) and 28× (Y), and 56–60 of the 64 groups are above 3×. In frame 665 the peak has fallen to 49× and 106×, while the whole view stands at 25× and 47×.
3. So it is a burst, about 0.7 s long, peaked at 1645.270 MHz and wider than the 5.72 kHz view. Its peak falls first and its broad part persists one frame longer. Feed Y is about twice feed X throughout.
4. No other scan holds it. The largest wide-view excursions elsewhere are 2–10×, in single frames, as in OFF0018 (10×). That is where M3's k4 of 1457 and its suppressed-carrier flag come from: a series that is noise except for two frames.

## 3. The cc15 coincidence

M4's cc15 nomination (ON0013, bin 958936, 1642.3403 MHz, z 14.5) is one bin from cc14's (958935) in the same scan, 2.9297 MHz lower: the same position in the adjacent coarse channel. No other channel's top hits in any scan fall within ±35 bins of that position (M4/cc*.json, M2.json). There are two readings, and this plan cannot separate them:

1. The burst is wider than 2.9 MHz, and the peak position repeats because of the channelizer's response to it.
2. The cc15 hit is an instrumental image of the cc14 burst.

The test is the cc15 voltages at 237.8 s in ON0013, with the same wide view. That needs a plan of its own.

## 4. Reading

The nomination fails the comet criterion: it is in one ON scan only, as a single 0.7 s burst. A source on the comet would recur at the comet prediction in ON0015 and ON0017.

What it is: one short, strong emission, wider than 5.7 kHz, in the 1626.5–1660.5 MHz Earth-to-space mobile-satellite band (external/human-sheet-20261119, sources). That shape fits a burst from a terminal on or near the Earth, or an instrumental transient. Naming a service needs the positive tests of PLAN-C14's limits, none of them run here. It is recorded as the first measured burst for the human-sheet reading: when it came, how long it lasted, how wide it was in the view, and its feed ratio.

Recorded as found: the cc14 nomination is closed for the comet search. The burst is kept open for the human-sheet reading, with §3's test as the next step.
