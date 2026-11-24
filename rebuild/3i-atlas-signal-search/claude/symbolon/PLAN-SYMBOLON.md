# PLAN-SYMBOLON: the Wow! signal read as one half of a symbolon, and the 3I/ATLAS data searched for the half that fits it

**2026-11-24, 18:00 EST, at the author's word:** "lets develop and run the symbolon key searches". Frozen before any product (FROZEN-SYMBOLON.sha256). Under the search's standing rules: a failed test forbids nothing further; it only withholds the word *signal* under the readings tested. Reading meaning as meaning, and noise as noise.

## 0. Why a second reading

PLAN-WOW (claude/wow/) read the Wow!'s recorded properties as instructions, each property as an operation to repeat on the 3I/ATLAS data: the same profile, the same frequency, the same width. The verdict: under those readings the Wow! instructs nothing beyond what the search already does; the profile selects satellites; W5 is open.

A symbolon is read differently. It is a token broken in two; each party keeps a half; the halves are proved by the fit of the break. The other half is not a copy of the first. It is its complement: it fits where the first is broken. Read as a symbolon, the Wow! does not say "find another one of me". It says "find what fits me". Each reading below takes one recorded property of the Wow! and asks for its complement, not its repetition.

## 1. The Wow!, as recorded (as in PLAN-WOW §1)

Big Ear, 1977-08-16 03:16:06 UTC (revised); 1420.726 ± 0.005 MHz (revised; Ehman's value +49.8 kHz above the hydrogen line, the revised +320 kHz); one 10 kHz channel; 10 s integrations every 12 s; SNR 6, 14, 26, 30, 19, 5; one horn of two, the record positive minus negative. Sources: Méndez et al., arXiv:2508.10657 (2025); Wikipedia, "Wow! signal".

## 2. The readings

- **K1, the break read from the other side: time reversed.** The profile 5, 19, 30, 26, 14, 6. Matched in time as PLAN-WOW stage 1 matched the Wow's own (10 s every 12 s, 8.58 kHz, ON score ≥ 6 and the OFF after it < 3), across blc21–26.
- **K2, the other horn: sign inverted.** The Wow was recorded positive minus negative, present in one horn and absent from the other. Its complement is the same profile going down: a dip of the Wow's shape, ON only. The correlation of the SNR series with the negated template, same detection rule. (An event whose profile p completes the Wow to a flat line, p = c − Wow, is the same template after zero-meaning; K2 covers it.)
- **K3, the mirror in frequency.** The Wow sits above the hydrogen line by +320 kHz (revised) or +49.8 kHz (Ehman). Its complement sits below by the same: targets T5 H − 320 kHz and T6 H − 49.8 kHz in 3I/ATLAS's frame, and T7 1420.08550 MHz topocentric (the Wow's number mirrored about the line). Read as PLAN-WOW stage 2 read T1–T4: blc24 .0000 (2.79 Hz × 6.08 s), ±5 kHz, tracked, ON/OFF contrast per pair, peak-bin z, against the same 200 random control targets (same seed).
- **K4, the halves joined.** The symbolon is proved by the two halves together. For each offset δ (320 kHz, 49.8 kHz) the joint statistic is the smaller of the two ON/OFF contrasts at H + δ and H − δ (comet frame): both halves must be present for it to be high. Controls: 200 symmetric pairs c ± δ around random centres c in the same coarse channel, more than 50 kHz from H and from the targets, processed identically.

**Not run, and why.** W5's six values as channel numbers, and their mirror (blc23 coarse channels 64 − n: 59, 58, 50, 45, 38, 34), need the voltages or the .0000 products of twelve coarse channels (about 14 GB streamed in .0000; about 200 GB in voltages); they stay open, with this cost recorded. The date (the Wow in 1977, the scans on 2025-12-18) offers no operation on these data.

## 3. The pareidolia measure

- K1 and K2: the 200 smooth single-peaked controls of PLAN-WOW amendment 1 (same generator, same seed), negated for K2, and the 200 random six-value sequences. The count of ON-only events for the reading is ranked within each set. Because K1's and K2's templates are themselves single-peaked, the smooth controls are the test that matters: a rank inside the middle of the smooth controls means the reading selects what any single-peaked shape selects.
- K3: rank of each target's mean ON/OFF contrast within the 200 random targets; peak-bin z inside ±5 kHz per scan, read against the ~3,600-bin noise maximum (z ≈ 3.5–4).
- K4: rank of the joint statistic within the 200 symmetric control pairs.

A reading counts as more than chance only above 95% of its controls. Rank is reported either way, and whatever a reading finds is listed as found and read.

## 4. What would count

A reading that ranks above 95% of its controls and yields an ON-only or comet-frame feature is worth reading further: its frequencies, its time course, whether the feature at one half has a partner at the other. A reading that ranks among its controls has not been shown to fit; it has still been read, and what it finds is reported.

## 5. Data and code

GBT 2025-12-18, scans 0013–0018 (ON 0013/0015/0017 on 3I/ATLAS), public rawspec products at bldata.berkeley.edu, streamed, not kept. K1 and K2: `symb_k12.py` (the rawspec .0002 of blc21–26, as wow_s1b.py). K3 and K4: `symb_k34.py` (blc24 .0000, as wow_s2.py, with the comet frame from voltages/delaymod). Products hashed in SYMBOLON-PRODUCTS.sha256.
