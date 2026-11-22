# PLAN-HM13-B3B5: batch B, parts B3 and B5 (B2's coverage stated)

Frozen 22 November 2026, 18:40 EST, before any B3 or B5 product, under the author's word of 18:00 EST ("yup lets freeze & run"). PLAN-HM13 (B1, B4) is frozen and running. Failing a frozen test bars nothing.

## B2. M4b's closer voltage look at class-A leads: where it stands

PLAN-M4b: "Class A is a lead for a closer voltage look." RESULTS-M4b §10 named where it would look first: the cc19, cc48 and cc50 carriers. Those three were looked at in the raw voltages, all 833 frames, by PLAN-C19 and PLAN-C4850 (RESULTS-C19: a line comb in OFF as in ON, fixed topocentric frequency; RESULTS-C4850: cc50 one off-target emitter, cc48's saved class-A events at median OFF/ON 0.74). cc01 was read in RESULTS-HM12 A5 (zero drift, met-sat band). Of the six excess channels, cc23 has no excess over its control (44 against 42). **The one class-A excess with no closer look is cc21** (19 against 8; 1625.12–1625.29 MHz, drifts −7.35 to +1.69 Hz/s, the Iridium band). It gets its own plan after B1 finishes, since it needs the same streaming. One mechanical question is stated now, before any reading: Iridium's TDMA frame is 90 ms, an envelope line at 11.11 Hz, the frequency of the unassigned component in ChatGPT's raw-power report (RESULTS-HM12 A6). Whether cc21's class-A events carry an 11.11 Hz envelope is to be measured there, not assumed.

## B3. P1547B's ON0015 lag-2 item, scaled up

RESULTS-P1547B: in ON0015, both feeds, phase-increment memory at lag 2 stood at p = 0.05 (16 frames, 19 surrogates) and did not reproduce in ON0017; it called this "the one item worth the plan's scale-up (all 833 frames, 199 surrogates)".

**Run (hm13b3.py SCAN):** P1547B's code path unchanged (its slice at 1547.720 MHz, its 1,025-bin median normalization, its magnitude-keeping random-phase surrogates), all 833 frames, 199 surrogates, both feeds, all six scans. Only filter A at lag 2 is accumulated (the parameter fixed by P1547B; no family maximum). Surrogates 0–18 use P1547B's seeds (seed0 + k); surrogates 19–198 use 2026112200 + 1000·i + 500·q + k, so that the feeds and scans do not share them.

**Gate G0 (reproduction), before any full-scan value is read:** after the first 16 frames, the real lag-2 value and surrogates 0–18 equal pb_SCAN.json's A[0] and sA[:, 0] (relative difference below 1e-9).

**Statistic.** Per scan and feed: the lag-2 value over all frames, p = (1 + surrogates ≥ real)/200, the ratio to the surrogate median; and the same in four frame blocks (0–207, 208–415, 416–623, 624–832), each against its own surrogates' block values.

**Rule.** A **lead** if, in one feed, ON0015 and ON0017 are both above all 199 surrogates (p = 0.005) and no OFF scan has p ≤ 0.05 in that feed. **It lasts through the scan** if ON0015's four blocks all have p ≤ 0.05. Anything else is reported as what it is, including any pattern across the six scans.

## B5. N1625's shape test on its saved crops

RESULTS-N1625: the self-test passed motif recovery (20/20 at all strengths) and noise (7/100 against an allowance of 10); the stationary tone was not flagged; the hopping tone was flagged at p = 0.05, the floor with 19 permutations in a single realization. The frozen criterion ("neither tone is flagged") stopped the run.

**Amendment, made here and declared.** One realization at a 0.05 floor cannot distinguish a tone the score responds to from the noise rate (5%). The criterion for the two tones is replaced by a rate: each tone at rms 1.0 in 20 seeds (tone 9100–9119, hop 9200–9219), 199 permutations a trial; **accepted if each is flagged (p ≤ 0.05) in at most 3 of 20** (the upper 95% bound of a 5% rate in 20). The motif check is repeated at the new permutation count: rms 1.0, seeds 1200–1204, accepted if recovered in at least 4 of 5. The noise criterion stands as passed. Code: N1625/n1625a.py unchanged; hm13b5_selftest.py calls its test() with these seeds and counts.

**If accepted:** `n1625a.py scan SCAN` for the six scans and `n1625a.py gates`, unchanged, with PLAN-N1625-run's gates (discovery on ON0013's first half; holdout on its second half at p ≤ 0.05 at the same L and s; reported in ON0015, ON0017, the OFF scans and the two control slices; a candidate also standing in the controls or the OFF scans is interference or uncertain, not a lead). **If not accepted,** the run stops again, and that is reported.

FROZEN-HM13-B3B5.sha256 hashes this plan, hm13b3.py and hm13b5_selftest.py.
