# Wow!-guided intermittent search — results (2026-11-03)

Plan: PLAN-wow.md, sha256 10ecba29335d295e5b48dfae59557a71bf99f3b7b3b69460baffb831790877c1, frozen before the window was read.

Injection. GBT: 1-channel 10.7-s burst recovered z 10.4; 4-channel 72-s burst z 8.3. Parkes: 10 kHz burst z 7.4; the 2 Hz tone placed at 1420.0 MHz (as written in the plan) was not recovered: the integer-MHz channel carries excess variance (row std 0.34 against 0.11-0.19 in its neighbours) and the veto removes it; placed at 1420.1234 MHz it was recovered at z 10.8 (wow_pks_inj2.py, wow_pks_inject2.json). The detector was not changed.

Deviation, recorded. The plan named all four GBT blc24 cadences; only 0013-0018 is at L band (1313.96-1501.46 MHz). 0029-0034 is at 2214-2401 MHz, 0045-0050 at 7501-7689, 0061-0066 at 11439-11626; none covers the window and none was searched.

GBT (cadence 0013-0018): target 0; controls [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]; swap 4. No lead.

Parkes blc05, the frozen rule's output: P target 64 against controls max 37 and swap 39; P2 target 23 against controls max 26; an event within the anchor tolerance: lead = True under the rule.

Diagnosis of the flag.
- 44 of the 50 target-window events in the middle S scan (scan index 2) lie on a comb of spacing 31.360 kHz (fit; teeth at 1420.402360 + n x 0.031360 MHz, +-0.5 kHz); chance expectation 1.6.
- Stacking the teeth (+-6 Hz) over 1417-1425 MHz in every 15-s sample of all six scans: z 11.6 and 13.0 in scan 0 samples 10-11; 11.7 and 9.1 in scan 2 samples 7-8; 12.4 and 11.9 in scan 4 samples 10-11; no R sample above 5.4 (scan 5 sample 11; control-spacing maximum in that sample 4.0). Control spacings 31.250, 30.000, 33.333 kHz: no sample above 4.6.
- Extent (scan 0 samples 10-11, 4 MHz chunks over 1344-1472 MHz): z 11.8 at 1420-1424, 7.6 at 1424-1428, 3.2 at 1416-1420, <= 3.1 elsewhere. The comb occupies about 1417-1426 MHz, inside the protected band, across the hydrogen line.
- Tooth position by scan (shift search, 2 Hz steps): -2, -4, 0 Hz. Riding with the comet (Horizons deldot -24.272, -24.256, -24.239 km/s at the three events) the teeth would move 0, -74.9, -156.2 Hz. The comb is fixed in Parkes topocentric frequency to within a few hertz across 23 minutes.
- Timing: one ~30-s episode per S scan, 105-180 s into the scan; episodes 637 s and 726 s apart. Three episodes all landing in S scans has a chance of about 1 in 8 if the episodes are unrelated to pointing.
- The in-tolerance event (1420.40236 MHz, 3.4 kHz below the HI rest frequency, topocentric) is a tooth of the comb; with teeth every 31.36 kHz and a 30 kHz tolerance band, a tooth near some anchor is expected.

Reading. The comb is an artificial, structured emission (or an instrumental artefact) fixed in the observatory's frame. Fixity in the Parkes frame is the signature of a local origin; a distant sender produces it only by correcting for Parkes's own motion. The on-source-only timing is weak evidence at 1 in 8. Not a Wow!-class candidate on the comet-frame hypothesis.

Also in the protected band: a single-sample spike of z 3314 at 1424.97057 MHz, scan 0 sample 0, and a z 96.5 one-channel spike at 1419.764244 MHz in the same sample (both at the first sample of the first file).

## Follow-up: the comb across the band (PLAN-comb.md, sha256 516e43a4a75f17002a47629f74ba94d7515c2a51713fe313ab6bd8904c6a7995)

Fold at 31.360 kHz in the first S scan's episode samples (10-11) against baseline samples, 4 MHz chunks; validation blc05 1420-1424 MHz z 11.0 at -3 Hz phase (passes). Nodes blc02-07 and blc10 complete (224 chunks); the rest running.
- The 31.360 kHz periodicity is present in many bands during the same episode, at different grid phases: 968, 1064 (35 Hz phase), 1120, 1160-1204, 1248, 1268-1276, 1472, 1492-1500 (z 3024 against control-spacing maximum 51), 1544, 1560, 1616, 1644, 1716-1724 MHz.
- Time profiles (all 120 samples, tooth grid at each chunk's phase):
  - 1496-1500 MHz: S0 samples 9-12 and 18-19 (to z 2714), S2 samples 6-8 (to 881), S4 samples 9-13 (to 560); every R sample <= 3.4. The same episodes as 1420.
  - 1720-1724 MHz: S0 samples 10-11 (53, 29), S2 samples 7-8 (10, 10); R <= 3.5.
  - 1248-1252 MHz: S0 sample 11 (581), S2 sample 9 (156), and R3 sample 4 (232).
  - 1164-1168 MHz: S0 samples 9-11 (to 189), S2 samples 13-16 (to 10), and R3 samples 0-7 (to 21).
- Reading. The 1420 comb is one piece of an impulsive event that reaches the receiver across at least 1164-1724 MHz in the same 15-s samples, on separate frequency nodes (the UWL digitises the whole band together). The same 31.360 kHz structure appears in reference scans at 1164 and 1248 MHz, so the phenomenon is not confined to on-source pointings. A terrestrial or instrumental impulsive source seen by the whole receiver. Not a candidate.
- All 22 nodes complete (704 chunks). Chunks called: 720 (z 318), 904-940 (five, to 57), 968-1724 (twenty-two), 2144-2228 (three, to 16), 3556 (z 6.0, at threshold). None in 1728-2112 or 2232-3552 apart from the last. The episode's 31.360 kHz structure is concentrated in 720-1724 MHz.
