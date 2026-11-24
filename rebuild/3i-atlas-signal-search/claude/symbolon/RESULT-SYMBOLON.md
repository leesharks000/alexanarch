# The Wow! signal read as half of a symbolon, and the 3I/ATLAS data searched for the half that fits: no reading fits beyond its controls

**2026-11-24.** At the author's word (18:00 EST): "lets develop and run the symbolon key searches". Plan frozen before any product: PLAN-SYMBOLON.md, FROZEN-SYMBOLON.sha256 (23:02 UTC), with symb_k12.py and symb_k34.py. Products hashed in SYMBOLON-PRODUCTS.sha256. Data: GBT 2025-12-18, scans 0013–0018, public rawspec products, streamed, not kept.

## K1, the break read from the other side: the profile time-reversed (5, 19, 30, 26, 14, 6), blc21–26

- **4,849 events that light in a scan on the comet and not in the OFF after it.** The 200 smooth single-peaked controls give a median of 4,247. K1 ranks above 81% of them, and above 92% of the 200 random sequences.
- **By node, against the smooth controls:** blc21 0.92, blc22 0.66, blc23 0.76, blc24 0.555, blc25 0.675, blc26 0.955.
- **The one node above 95% is blc26 (939–1126 MHz).** 929 of its 1,009 events fall in 960–1215 MHz, the aeronautical band of the DME and transponder pulses, densest at 986–990 MHz and 1110–1125 MHz. The strongest are at 987.9–989.2 MHz in ON 0017, with scores up to 1,919. These also light in the OFF scans 0014 and 0016; 426 of the node's events light in some OFF scan. They are aircraft, not the comet.
- **Reading.** The reversed profile is a fast rise and a slower fall. In these data it selects pulsed aviation transmitters a little more often than a symmetric bump does, and nothing in the comet's direction alone.

## K2, the other horn: the Wow's shape going down, a dip ON only, blc21–26

- **2,088 events.** The negated smooth controls give a median of 3,211, so K2 ranks above only 13% of them (and 24% of the random sequences).
- **By node:** 0.095, 0.015, 0.265, 0.135, 0.145, 0.16.
- **Reading.** Dips of the Wow's shape are rarer than dips of an ordinary single-peaked shape. The other horn holds nothing.

## K3, the mirror in frequency: blc24 .0000, 2.79 Hz × 6.08 s, ±5 kHz, against the 200 random targets of PLAN-WOW

- **T5, the hydrogen line − 320 kHz in the comet frame:** mean ON/OFF − 1 = 0.0429, rank 0.945.
- **T7, 1420.0855 MHz topocentric (the Wow's number mirrored about the line, 0.25 kHz from T5):** 0.0429, rank 0.945.
- **T6, the hydrogen line − 49.8 kHz in the comet frame:** 0.0412, rank 0.200.
- **The controls:** mean 0.0410, ranging from −0.005 to 0.086.
- **Why T5 and T7 rank high.** The controls bunch tightly: their median is 0.0415 and their 95th percentile 0.0430. T5 and T7 sit 0.0014 above that median, at the edge of the bunch and far inside the controls' range. Their upper halves, T3 (+320 kHz) and T1, read low (0.055) because strong Galactic H I in both pointings flattens the ratio there, which is the sky.
- **No narrow core.** The peak bin inside ±5 kHz reaches z 3.1–4.2 and the trough −3.1 to −4.0, in ON and OFF scans alike, which is the extreme of about 3,600 noise bins.

## K4, the halves joined: the smaller of the contrasts at H + δ and H − δ, against 200 symmetric pairs around random centres

- **δ = 320 kHz:** joint 0.0362, rank 0.155 (controls median 0.0413).
- **δ = 49.8 kHz:** joint 0.0412, rank 0.315 (controls median 0.0414).
- **Reading.** The halves together hold nothing that a random symmetric pair does not.

## What this establishes

- **No symbolon reading fits beyond 95% of its controls.** The pooled ranks are K1 0.81 and K2 0.13; the targets are K3 0.945, 0.945 and 0.200; the joined halves are K4 0.155 and 0.315.
- **K1's single node over the line is aircraft,** lit in the OFF scans as well.
- **K3's mirror targets reach 0.945 by sitting where the ordinary channels sit.** Nothing in them is narrow, and nothing is ON-only.
- **Verdict.** Under the readings tested, the Wow! does not find its other half in these data. The readings were read, and what they found is reported: pulsed aviation at 960–1215 MHz, and the Galactic hydrogen line's own shape.
- **Still open.** W5 and its mirror (the six values as blc23 coarse channels, and 64 − n): about 14 GB of .0000 streamed, or about 200 GB of voltages.
