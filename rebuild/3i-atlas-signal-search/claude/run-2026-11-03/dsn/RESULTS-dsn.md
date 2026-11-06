# Results: the comet frame in the deep-space downlink band, GBT X band 8397.9–8450.7 MHz (plan PLAN-dsn.md, sha256 9f2d646d…; run 2026-11-05 to 2026-11-06 UTC)

Verdict: BOUNDED. None of the eighteen coarse channels exceeds its false frames (a lead needed 3; one or two would have been held out for replication). Nothing steady in the comet's frame stands above chance in 8397.9–8450.7 MHz, the deep-space allocation 8400–8450 MHz whole, in the Green Bank X-band cadence of 2025-12-18 (scans 0061–0066), at this detector's gate.

| Channel | Centre (MHz) | True ON | True swap | False frames ON | False max ON−swap | Fraction of false frames ≥ true | Verdict |
|---|---:|---:|---:|---|---:|---:|---|
| blc73_cc00 | 8437.500 | 4 | 2 | 3.2 ± 2.12 (max 8) | 5 | 0.35 | BOUNDS |
| blc73_cc01 | 8434.570 | 5 | 2 | 2.98 ± 1.68 (max 7) | 5 | 0.2 | BOUNDS |
| blc73_cc02 | 8431.641 | 5 | 3 | 3.27 ± 1.92 (max 8) | 5 | 0.225 | BOUNDS |
| blc73_cc03 | 8428.711 | 1 | 4 | 2.98 ± 1.8 (max 7) | 5 | 0.95 | BOUNDS |
| blc73_cc04 | 8425.781 | 4 | 6 | 3.3 ± 1.73 (max 8) | 6 | 0.475 | BOUNDS |
| blc73_cc05 | 8422.852 | 1 | 4 | 2.65 ± 1.56 (max 7) | 7 | 0.975 | BOUNDS |
| blc73_cc06 | 8419.922 | 4 | 4 | 3.12 ± 1.55 (max 6) | 5 | 0.4 | BOUNDS |
| blc73_cc07 | 8416.992 | 4 | 3 | 3.02 ± 2.08 (max 9) | 4 | 0.35 | BOUNDS |
| blc73_cc08 | 8414.062 | 4 | 5 | 2.88 ± 1.36 (max 5) | 5 | 0.4 | BOUNDS |
| blc73_cc09 | 8411.133 | 4 | 5 | 3.52 ± 1.96 (max 10) | 9 | 0.4 | BOUNDS |
| blc73_cc10 | 8408.203 | 2 | 6 | 2.67 ± 1.85 (max 7) | 5 | 0.75 | BOUNDS |
| blc73_cc11 | 8405.273 | 2 | 4 | 2.92 ± 1.66 (max 7) | 4 | 0.8 | BOUNDS |
| blc73_cc12 | 8402.344 | 1 | 3 | 2.8 ± 1.55 (max 6) | 4 | 0.95 | BOUNDS |
| blc73_cc13 | 8399.414 | 3 | 2 | 3.23 ± 2.1 (max 8) | 6 | 0.55 | BOUNDS |
| blc72_cc60 | 8449.219 | 2 | 4 | 3.15 ± 1.77 (max 8) | 4 | 0.825 | BOUNDS |
| blc72_cc61 | 8446.289 | 6 | 1 | 3.1 ± 1.83 (max 7) | 4 | 0.05 | BOUNDS |
| blc72_cc62 | 8443.359 | 4 | 4 | 3.58 ± 1.64 (max 7) | 6 | 0.475 | BOUNDS |
| blc72_cc63 | 8440.430 | 0 | 5 | 3.05 ± 1.52 (max 7) | 6 | 1.0 | BETWEEN (below every false frame) |

Across the band the true frame holds 56 clusters; the eighteen false-frame means sum to 55.4. The comet frame is ordinary here: every channel's true count lies inside or below its false frames.

Two channels, as description only. At 8446.289 MHz (blc72_cc61) the true count, 6, is matched or passed by 2 of the 40 false frames (5, 5, 6, 7 are the four highest), so the first criterion fails; its ON−swap difference, 5, is above every false frame's (maximum 4). One criterion of two is met and the decision needs both; with a chance of about 1/41 per channel for either criterion alone, about 0.44 such channels are expected in eighteen. Its clusters sit at rest frequencies 8445.36–8446.02 MHz and are listed in dsn.json. At 8440.430 MHz (blc72_cc63) the true frame holds no cluster, below every false frame (minimum 1); the runner labels a count outside the false range that does not exceed it BETWEEN, and here the count lies under the range, which is no lead.

Every true-frame cluster is listed in dsn.json with its rest and topocentric frequencies and its six scans' z, as the plan requires.

Deviations. (1) cf.py: the plan names one changed line (the ON and OFF scan lists); three further hard-coded references to scan 0013 had to point at the first ON scan of this cadence. Found when the first run stopped on the KeyError after fetching channel 0, fixed and recorded (commit 3bc3977) before any count was computed. (2) The run was interrupted four times and resumed each time from the first incomplete channel, the runner writing each channel's result only when that channel completes: two container restarts (2026-11-06 00:11 and 00:35 UTC, during channels 8 and 10) and two connection resets from the data server during channel 12 (resumed with a retry loop at 01:00 and 01:01 UTC). The first restart also removed the session's Python packages; they were reinstalled (numpy 2.5.4) before channel 8. Channels 0–7 were computed under the packages installed earlier in the session, whose versions were not recorded; the procedure (medians, boxcar sums, robust z, counting) does not depend on version in any way that changes a count. Order and completeness held as frozen: blc73 channels 0–13 in index order, then blc72 60–63, no channel skipped.

What this bounds. The deep-space downlink allocation, the receivers' most direct listening practice for spacecraft, in the sensitive instrument's public December cadence, in the comet's frame and at its range-acceleration, at the gate of the lheld detector (ON z ≥ 2.5 in all three, OFF z < 2.0 in all three). It does not bound a transmitter that drifts off the comet's frame, a burst shorter than the 6.085 s sample, or anything below the gate; the ATA's July look at these frequencies bounds only watt-class transmitters (chatgpt/C03-equal-strength-envelope-report-2026-11-05.md).

Files: PLAN-dsn.md, run_dsn.py, cf.py, fetch_cc.py (as in lheld/, with the deviation above), dsn.json (per channel: true, swap and false-frame counts and every true-frame cluster), run.log (with the interruptions marked). Raw spectra were fetched by name from the public directory and deleted after each channel; their header JSON files stay in raw/, outside the tree.
