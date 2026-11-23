# RESULTS-HM13: batch B, the unexamined branches that needed the network

Run 22–23 November 2026 under PLAN-HM13 (B1, B4; commit b85525b9f), PLAN-HM13-B3B5 (B3, B5; commit 23641fa61) and PLAN-HM13-B2 with B2b (B2; commits 3c6177717, 513440cf3, amended cbef1cf9d), each frozen and committed before its products. Failing a frozen test bars nothing.

## Errors in the plans, recorded first

1. **PLAN-HM13-B3B5 states its freeze time as 18:40 EST.** It was committed at about 18:14 EST (commit 23641fa61's timestamp), before any B3 or B5 product. The commit time is the record.
2. **PLAN-HM13's gate G1 could not pass as written.** It asked that the regenerated stack files hash identically to M4b-PRODUCTS.sha256. Every file differs. The files carry no zip timestamps (checked), so the bytes differ in their compressed content; the arrays could not be compared because the original stacks were deleted when M4b ran. A byte-level gate on compressed numerical files was the wrong gate to freeze. What was checked in its place, after the freeze and declared here: each channel's hits were re-derived from the regenerated stacks with M4's own mhits.py and compared with the kept M4/ccNN.json (G1b.jsonl). G2 (nomination counts) stands as frozen.
3. **Two runs were stopped at the session's two-hour limit for background work and restarted:** B1 during the voltage battery of cc43 and cc45 (their stacks were kept and reused), and B3 during ON 0013 (0015 and 0017 complete). Both restarts are noted in their logs.
4. **B2b's first run was void.** hm13b2b.py stored its per-frame windows as float16, and 72.6% of the stored powers overflowed to inf; every frame then read as off. PLAN-HM13-B2b-AMEND-1 (commit cbef1cf9d, before run 2) changes the storage to float32 and nothing else. The amendment dates run 1's streams 09:14–09:25 EST; they ran from about 09:14 to 09:20, and the amendment was committed at 09:21.
5. **PLAN-HM13-B2b rule 1 says 20,000 simulated noise frames gave "none" above the on threshold.** They gave 1 (5 × 10⁻⁵). The bound it states, below 10⁻⁴ per frame, holds. Recorded in the amendment.

## B1. M4's ten lost channels: the counts reproduce; no recurring lead

All ten channels rerun with the frozen code (mvb.py, then mvolt.py). Products: hm13b1.json, volt/ (hashed in VOLT-HM13.sha256), v0/, HM13-STACKS.sha256, G1b.jsonl.

1. **G2 passed in all ten.** The nomination counts are RESULTS-M4's: cc30 1, cc32 3, cc37 1, cc39 1, cc43 2, cc45 3, cc46 2, cc49 6, cc51 2, cc55 4 (25).
2. **G1, as frozen, failed in all ten** (above, error 2). **The content check passed in the eight it could reach:** for cc37, cc39, cc43, cc45, cc46, cc49, cc51 and cc55, the hit counts and the ranked top hits (bin and z) of every scan equal M4's kept files exactly. cc30 and cc32 were deleted before the check was set up and rest on G2.
3. **By the frozen rule: 4 closed (off-source), 21 single-scan leads, no recurring lead.**

| channel | scan, feed | MHz (topocentric) | z | envelope line (W1) | standing | allocation |
|---|---|---|---|---|---|---|
| cc30 | 0015 Y | 1600.9927 | 42.2 | 0.199 Hz | single-scan | RNSS (GLONASS L1) |
| cc32 | 0015 X, Y, X | 1593.4784, 1593.2787, 1593.1506 | 10.8–11.4 | 0.10–0.12 Hz | single-scan (3) | RNSS |
| cc37 | 0013 X | 1579.0020 | 26.0 | 0.702 Hz | single-scan | RNSS (GPS L1 band) |
| cc39 | 0013 X | 1572.8640 | 20.1 | 0.692 Hz | single-scan | RNSS (GPS L1 band) |
| cc43 | 0017 Y | 1562.5173 | 30.7 | 0.129 Hz | closed | RNSS |
| cc43 | 0017 X | 1561.0964 | 9.4 | 49.998 Hz | single-scan | RNSS (BeiDou B1I, 1561.098) |
| cc45 | 0013 X, Y | 1555.8935 | 15.0 | 16.651 Hz | single-scan (2) | MSS downlink |
| cc45 | 0013 X | 1556.7001 | 9.7 | 12.501 Hz | single-scan | MSS downlink |
| cc46 | 0017 Y | 1553.5882 | 15.6 | 0.105 Hz | closed | MSS downlink |
| cc46 | 0017 X | 1553.0184 | 13.2 | 49.998 Hz | single-scan | MSS downlink |
| cc49 | 0013 Y | 1544.1657, 1544.2372, 1544.2274 | 32–326 | 0.11–0.12 Hz | single-scan (3) | MSS downlink |
| cc49 | 0015 X | 1543.2963 | 30.6 | 25.002 Hz | single-scan | MSS downlink |
| cc49 | 0017 X, Y | 1544.1508 | 54.8 | 1.000 Hz | single-scan (2) | MSS downlink |
| cc51 | 0015 X, Y | 1537.5271 | 29.2 | 0.10–0.13 Hz | closed (2) | MSS downlink |
| cc55 | 0013 X | 1526.9854 | 9.5 | 7.156 Hz | single-scan | MSS downlink |
| cc55 | 0015 Y; 0017 X, X | 1527.0987, 1527.0997, 1527.0986 | 8.3–12.3 | 7.155 Hz; 45.148 Hz | single-scan (3) | MSS downlink |

4. **Reading the leads (not ruled).** Every one of the 25 lies in an allocated band of our own transmissions: 1559–1610 MHz radionavigation-satellite (GPS L1's band, BeiDou B1I at 1561.098 MHz, GLONASS L1) or 1525–1559 MHz mobile-satellite downlink (Inmarsat). The envelope lines are the rates of framed digital transmissions: 49.998, 25.002, 12.501 and 1.000 Hz, and 7.155 Hz repeated across three scans. cc55's line at 1527.0986–1527.0997 MHz stands at the same topocentric frequency in ON 0015 and ON 0017; a source on the comet would have moved between them by the change in the comet's Doppler, and the rule's comet-frame recurrence test misses a source fixed in the observatory's frame for that reason. cc49's 1544.1657 MHz (z 326) appears in ON 0013 and ON 0017 in M4's hit files, beside the 1544.495 MHz carrier that stands in every scan, OFF included. "Off-source" was tested against the OFF scans' top hits only; a nomination absent from those lists is not shown to be absent from the OFF scans.
5. **What this closes.** M4's lost nominations are recovered and read. None recurs on the comet's drift; none lies outside the satellite allocations. As RESULTS-M4b found for its class-A excesses, what the search nominates in these bands is ours, and, as recorded there, what resembles our own transmission is set aside as ours.

## B2. cc21 at Iridium's 90 ms frame: the frame fills the channel; no lead

The class-A excesses in cc19, cc48 and cc50 were looked at in the raw voltages by C19 and C4850, and cc01 by HM12 A5; cc23 has no excess over its control. cc21 (19 class-A events against 8 in its control, the Iridium band) is looked at here, under PLAN-HM13-B2 (commit 3c6177717, 08:50 EST) and PLAN-HM13-B2b (513440cf3, amended cbef1cf9d), both committed before their products. The question named in advance was whether its events carry an envelope at 11.11 Hz, Iridium's 90 ms frame, the frequency of the unassigned component in ChatGPT's raw-power report. Products: b2.json, b2b.json, b2_selftest.json; the arrays hashed in B2-PRODUCTS.sha256, B2-SELFTEST.sha256 and B2b-PRODUCTS.sha256, not committed for size.

1. **Self-test passed** (b2_selftest.json). A tone gated 8.28 ms in every 90 ms and drifting −7.35 Hz/s was flagged at 0.075σ (H_I about 300,000 against a threshold of 29) and at 0.03σ (about 17,500). Noise alone flagged 1 of 942 valid tiles, against an allowance of 6.
2. **The frame fills the channel, in every scan, ON and OFF.** Valid tiles flagged (X, Y) of 942: ON 0013 859, 859; OFF 0014 821, 854; ON 0015 755, 722; OFF 0016 895, 897; ON 0017 679, 695; OFF 0018 801, 752. The thresholds stand at 197–481, against about 29 in noise: the control frequencies carry envelope structure of their own (the plan's limit 3). Of the 938 tiles flagged in an ON scan, 937 are flagged in an OFF scan as well. The one ON-only tile (353, 1626.43 MHz, ON 0015) is at the rate noise gives.
3. **The question asked in advance: yes.** All three saved class-A events carry the 11.11 Hz envelope in their own scan. That is H_I/θ 11.1 for N1625's event (1625.293611 MHz, ON 0013), and 1.25 for both 0015 events (1625.120424 and 1625.120737 MHz). So do 36 of the 40 saved ON events and all 15 role-reversed events.
4. **The class-A events are not at the comet.** At their recorded bins, the strongest OFF scan holds more power than their own ON scan: 75.9 times for N1625's event, and 1.9 and 40.7 times for the 0015 pair. RESULTS-N1625's Part 2 found the same event's family in OFF scans as in ON.
5. **Twenty-one events pass the location rule, and none is steady** (B2b). All 21 are class B, each seen by M4b in one ON scan. By PLAN-C4850's location test their OFF power is below 1% of their ON power or at noise, the case its limit 2 names. Their time structure: each is on in 0.4–3.0% of its scan's frames (3–25 of 833), in bursts. Five of ON 0015's events, at 1624.72–1624.85 MHz, are all on between 141 and 153 s. Seven of ON 0017's eleven are first on between 8.8 and 51.7 s. No event reaches the rule's 80% in any quarter. Each has too few on frames for the drift fit. Comet-track power stands at 1.13–1.19 times the window median, the value noise gives (about 1.19). By the rule, none is a lead. They are short bursts that come and go within one scan, and 19 of the 21 carry the 90 ms frame.
6. **Reading (not ruled).** cc21's excess is Iridium's, measured now by its own frame and no longer by band and drift alone. That is RESULTS-M4b's reading 8 at a finer grain: what resembles our own transmission is set aside as ours, and here the 90 ms frame stands in nearly every slice of the channel, at every pointing. As for HM12 A6's 11.11 Hz component, which is in all six scans' raw power and strongest in OFF 0016: a 90 ms frame filling this band in every scan is a candidate mechanism for it. It is not shown to be that mechanism (the plan's reading 3), since A6 measured raw power in a different product.

## B3. P1547B's lag-2 item, scaled up: not a lead

All 833 frames, 199 surrogates, both feeds, six scans. Gate G0 passed in every scan and feed: after 16 frames the real value and surrogates 0–18 equal P1547B's to the last digit (relative difference 0).

Lag-2 phase memory at 1547.720 MHz (×10⁻⁴; real over surrogate median; p; p in the four frame blocks):

| scan | X | Y |
|---|---|---|
| ON 0013 | 12.6, 10.4×, 0.005 (0.175, 0.005, 0.005, 0.005) | 9.2, 8.4×, 0.005 (0.005, 0.005, 0.01, 0.045) |
| OFF 0014 | 11.5, 10.6×, 0.005 (all 0.005) | 21.7, 20.5×, 0.005 (all 0.005) |
| ON 0015 | 11.0, 9.4×, 0.005 (all 0.005) | 12.8, 11.2×, 0.005 (0.005, 0.005, 0.005, 0.015) |
| OFF 0016 | 8.9, 8.1×, 0.005 (0.005, 0.005, 0.485, 0.005) | 13.6, 12.4×, 0.005 (0.005, 0.005, 0.005, 0.05) |
| ON 0017 | 19.6, 17.2×, 0.005 (0.01, 0.005, 0.005, 0.005) | 11.2, 10.1×, 0.005 (0.005, 0.005, 0.005, 0.08) |
| OFF 0018 | 13.2, 10.7×, 0.005 (0.055, 0.005, 0.02, 0.005) | 11.2, 9.1×, 0.005 (0.04, 0.015, 0.005, 0.005) |

1. **By the rule, not a lead.** ON 0015 and ON 0017 are above all 199 surrogates in both feeds, and so is every OFF scan. The rule required no OFF scan at p ≤ 0.05.
2. **The relation is real and lasts through every scan.** It stands at 8 to 20 times its surrogates in all six scans and both feeds, in almost every quarter of every scan. It is not a fluctuation, and it is not the comet: it is as strong in the OFF pointings as in the ON.
3. **What P1547B saw was its sample size.** With 16 frames and 19 surrogates, the relation reached the p floor in ON 0015 and not in ON 0017; at 833 frames it is everywhere. P1547B's own limit 3 named the likely mechanism: a slight non-whiteness of the instrument's response within the normalization window gives a lag-2 relation among phase increments. That reading fits a relation present at all pointings; it is not established here.

## B4. ATA July 3 along the true drift at C08–C13: no lead

All six targets read in all 16 scans, both beams, no errors (96 runs). Maximum persistence of a scan-average feature at one rest frequency (±4 Hz), per path:

| target | comet | comet swap | flipped | flipped swap | dish-fixed | dish-fixed swap |
|---|---|---|---|---|---|---|
| C08 1667.412866 | 1 | 1 | 1 | 1 | 1 | 1 |
| C09 1667.430186 | 2 | 1 | 1 | 1 | 2 | 1 |
| C10 1667.686517 | 1 | 1 | 1 | 1 | 1 | 1 |
| C11 1667.994976 | 2 | 1 | 1 | 1 | 2 | 2 |
| C12 1668.098187 | 1 | 2 | 1 | 1 | 2 | 2 |
| C13 1668.429424 | 1 | 1 | 1 | 1 | 2 | 2 |

The rule asked for a comet-path persistence of 3 or more with every other path at 2 or fewer. The comet path reaches 2 at C09 and C11, where the dish-fixed path also reaches 2. As at RESULTS-ata-look's ten frequencies, the true drift class holds nothing at C08–C13 on July 3 that its twins do not hold equally.

## B5. N1625's shape test on its saved crops: not a lead

**Amended self-test (accepted).** Stationary tone flagged in 2 of 20 seeds, hopping tone in 1 of 20 (allowance 3 each); the motif at rms 1.0 recovered 5 of 5, at 199 permutations. The single flag that stopped N1625 was the noise rate.

**On the data** (first 32 frames of each scan; target 1625.2936106 MHz, +25 kHz control, high-drift control; both feeds; 199 permutations):
1. **Discovery, ON 0013 first half:** X gives a candidate at L = 256, s = 1, p = 0.035; Y none (p = 0.135).
2. **Holdout, ON 0013 second half, same L and s: p = 0.93.** The gate fails.
3. At that (L, s): ON 0013 whole, target, p = 0.005, and its +25 kHz control p = 0.03; OFF 0016's +25 kHz control p = 0.05; ON 0015 and ON 0017 at the surrogates' level (0.80, 0.475).
4. Across the 36 full-family tests, one reaches p ≤ 0.05 (OFF 0014, Y, target, p = 0.015), about what chance gives.

The translated-shape idea finds nothing at 1625.29 MHz that the controls and the OFF scans do not carry. RESULTS-N1625's Part 2 (the event's family is present in OFF scans as in ON) stands.

## Reading

Batch B is closed, and no branch gives a lead. B3 found a real, steady phase relation that belongs to every pointing, not the comet. B1 recovered M4's 25 lost nominations, reproduced its counts and hits, and found no recurring lead; all 25 are in the navigation- and mobile-satellite allocations. B2 gave cc21 its closer look: Iridium's 90 ms frame is in the class-A events and in nearly the whole channel, ON and OFF. The class-A events are stronger off the comet than on it, and the 21 events that pass the location test are bursts of seconds. With cc21, every class-A excess of M4b has had its closer voltage look.
