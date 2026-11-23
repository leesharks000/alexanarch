# PLAN-HM13-B2b: the time structure of B2's rule-leads

Frozen after B2's products (commit 4ad861222) and before any B2b product; hashes in FROZEN-HM13-B2b.sha256. Failing a frozen test bars nothing.

## Why

PLAN-HM13-B2 rule 5 makes a lead only what PLAN-C4850's rule calls one. By that rule's location test, 21 of cc21's 40 saved ON events pass: their power in every OFF scan, at the fixed bin and on the comet track, is below 1% of their ON power or at noise (b2.json). All 21 are class B: M4b found each in one ON scan only. PLAN-C4850's limit 2 is the case: "A source that fades or switches can mimic an ON-only line in one scan pair. A lead is checked against both neighbouring OFF scans and its time structure in Pf before it is called one." The location test already covers both neighbouring OFF scans. B2 did not save per-frame power, so the time structure has not been read. This plan reads it. Until it does, the 21 are rule-leads, not leads.

## Data

cc21, the three ON scans (0013, 0015, 0017), both polarizations, all 833 frames, streamed by dm.frames.

## Products (hm13b2b.py SCAN)

Per frame, for each rule-lead of the scan, the power spectrum ±256 bins (±715 Hz) around its recorded bin, and the power on the comet track ±2 bins. The window holds a drift of up to 2.4 Hz/s for the whole scan; the fastest of the 21 is 1.52 Hz/s. Hashes in B2b-PRODUCTS.sha256.

## Rule (hm13b2b.py read)

1. Per frame, polarizations summed: peak = the largest bin in the window over the window's median. The frame is **on** if peak > 12. For noise alone (two polarizations summed, 513 bins) the chance per frame is below 10⁻⁴ (20,000 simulated frames: none).
2. Duty = the fraction of on frames in each quarter of the scan (frames 0–207, 208–415, 416–623, 624–832).
3. A rule-lead is **steady** if its duty is at least 0.8 in every quarter. **It is a lead only if it is steady.** A source on the comet stays in the beam for the whole ON scan, so its line is present throughout unless the source itself switches. A line present in part of the scan is recorded as switching or passing, PLAN-C4850 limit 2, and not as a lead.
4. Recorded, not ruled: the first and last on times; the drift fitted to the peak bin over on frames (one refit within 16 bins); the comet's topocentric drift in that scan from the ephemeris (−0.107, −0.113 and −0.120 Hz/s in 0013, 0015 and 0017, computed before this plan as −FC·Δv/(c·Δt)); and the median comet-track power over the window median.

## Reading set before the data

1. If none is steady, B2 has no lead, and the 21 are read as what their envelopes say: 19 of the 21 carry Iridium's 90 ms frame in their own scan.
2. A steady rule-lead is a lead for its own plan. Before that plan, its drift is compared with the comet's; a drift that is not the comet's is recorded as against it, as M4b's reading 9 sets.

## Inputs (sha256)

In FROZEN-HM13-B2b.sha256: this plan, hm13b2b.py, b2.json, voltages/delaymod/dm.py.
