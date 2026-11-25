# The Wow! as guide and as key: looks, not tests

**The frame, in the author's words (2026-11-24, 22:13–22:15 EST).** "we dont need to confirm by frozen estimates a signal. we are trying to hypothesize a situation in which the wow! signal came from 3i atlas as an artificial vessel intentionally and use it as a clue to find signal in the 2025 data"; "the signal itself would confirm its artificial nature. that is the only kind of confirmation i would accept: structured, legible message"; "we assume that the problem would be a) locating signal, and especially b) recognizing it, but if located and recognized, parseable as message"; "we are even hypothetically treating the wow! signal as if it were an intentionally sent cryptographic key for the 2025 data"; "those are the speculative parameters were working with".

Under this frame the 1977 velocity is not a pass/fail (PLAN-WOW3 R1 asked the wrong kind of question of it). It is a conversion: it turns the Wow's received frequency into the vessel's own.

## look1.py — the vessel's own frequency

If the Wow! was sent at a frequency fixed in the object's frame, that frequency is the received one taken back through the object's 1977 range-rate from Big Ear (−43.011 km/s on the present orbit): **1420.5222 MHz** (revised), 1420.2518 MHz (Ehman). At Green Bank on 2025-12-18 these arrive at 1420.5312 and 1420.2608 MHz.

blc24 .0000 (2.79 Hz × 6.08 s), scans 0013–0018, de-Dopplered to the comet frame, ±6 kHz around each:
- **No line steady in the comet frame.** The strongest column per scan is z 3.8–5.6, and the highest (5.6) is in an OFF scan.
- **No bursts beyond the noise tail.** 6–14 single pixels at z ≥ 5 per scan of about 210,000, in OFF scans as in ON; the largest, z 8.4, is one pixel in ON 0013.
- The revised frequency sits on the slope of the Galactic hydrogen emission (peak 1420.57–1420.58), where the level is higher.
- Only the first of the four Green Bank cadences is read here.

## key_hop.py — the six values as a hop sequence

6, 14, 26, 30, 19, 5 read as the channel, in Big Ear's 10 kHz channels above an anchor, where the signal sits in each successive 12 s step. blc24 .0002, five anchors (the hydrogen line and the two own-frame frequencies in the comet frame; the hydrogen line and 1420.726 topocentric), six cyclic phases.
- **The de-hopped stream holds nothing.** Mean z per scan −0.18 to +0.16. Against 200 random six-value keys the Wow key ranks from 0.02 to 0.96, with no anchor high in all three ON scans (the hydrogen line in the comet frame: 0.85, 0.96, 0.59; OFF 0.45, 0.18, 0.17).
- The de-hopped series are kept in key_hop.json, to be read.

Random keys are kept as the pareidolia measure: what any key of the same form pulls out of the same data.
