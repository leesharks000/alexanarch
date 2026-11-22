# RESULTS-HMR2: reading D3

Run under PLAN-HMR2, frozen in 0434a91c8 before any product was read. Scans 0013–0018, all 833 frames, both feeds, 95 windows. Scored 22 November 2026, 14:00 EST. No amendment.

## 1. Reproduction

It holds. The maximum |D3| (d = 2) difference from HM5 is 8.7e-7 (0013) and 1.6e-6 (0014). The maximum relative power difference is 9.1e-5 and 9.7e-6. All are inside the frozen tolerances (1e-5, 1e-4). The readings below were then read.

## 2. At the comet: ON 0013, X

No reading passes at any coordinate.

| Coord | R1: R, p | R1: highest sideband R | R4: envelope peak / median (Hz) |
|---|---|---|---|
| C03 | 0.0176, 0.77 | 0.0353 | 14.8 (12.94) |
| C04 | 0.0430, 0.21 | 0.0673 | 16.4 (31.66) |
| C05 | 0.0340, 0.38 | 0.0802 | 12.2 (9.49) |
| C06 | 0.0560, 0.074 | 0.0873 | 14.7 (40.95) |
| C07 | 0.0240, 0.62 | 0.0544 | 13.9 (44.34) |
| C08 | 0.0198, 0.72 | 0.0365 | 12.4 (15.83) |
| C09 | 0.0176, 0.77 | 0.0329 | 17.0 (17.20) |
| **C10** | **0.0906, 0.0011** | 0.0616 | 13.2 (31.87) |
| C11 | 0.0091, 0.93 | 0.0478 | 14.8 (13.74) |
| C12 | 0.0168, 0.79 | 0.0663 | 16.0 (41.48) |
| C13 | 0.0321, 0.42 | 0.0651 | 16.8 (23.92) |

- **R1 (phase locking):** no coordinate has p < 1e-4. C10 is the nearest: R = 0.0906, above every one of its sidebands (highest 0.0616), with p = 0.0011. It does not meet the frozen rule. It is the largest R among the comet coordinates in 0013 X. Under the frozen rule nothing is carried to the hold-out.
- **R2 (lag profile):** reported in hmr2_score.json. With no locked phase at any lag there is no modulation spacing to name (§3, R2 is read with R1).
- **R3 (sequence):** no coordinate reaches p ≤ 0.001 in any of the four tests.
- **R4 (envelope modulation):** no coordinate reaches 20× the median. The highest is C09, at 17.0.

So no reading passes at the comet in 0013 X, and none goes to the hold-out.

## 3. Elsewhere at comet coordinates

Under §4 these count as the procedure finding structure where the comet is not, or outside the frozen route.

- **0013 Y, C09, R4:** peak 20.6× at 11.30 Hz. This is the Y feed, at the same coordinate that is highest (17.0) in X.
- **0017 X, C11, R4:** peak 21.2× at 41.57 Hz. This is a hold-out scan, but nothing was carried to it from 0013. 0017 X is also the scan where the sidebands pass R4 most often (4 of 84).

## 4. Base rates (sidebands, 84 per scan and feed)

- **R1:** 0 everywhere.
- **R3:** 1 in 0013 X and 1 in 0015 Y; 0 elsewhere.
- **R4:**
  - 0 or 1 in most scan-feeds;
  - 3 in 0017 Y and 4 in 0017 X;
  - 0 in 0014 Y, 0015 Y, 0016 Y and 0018 Y.

The comet coordinates' R4 passes (one in Y 0013, one in X 0017) are at or below these sideband rates.

## 5. C12's hold-out from HMR1

- **0015:** Ljung–Box p = 0.043, above every sideband.
- **0017:** p = 0.249, above every sideband.

The rule (p ≤ 0.004 and above every sideband, in either scan) is **not met**. C12's HMR1 finding stays found in one scan (0013, p = 0.004). In both hold-outs it ranks above every one of its sidebands, but at strengths that do not reach the rule.

## 6. What this says

Read inside the frames, D3 at the comet carries no locked phase, no sequence and no envelope rhythm beyond what its sidebands, OFF, Y and surrogates show. That holds across all 833 frames of the scans HM5 and HM6 used. The two R4 passes at comet coordinates are in Y and in an unselected hold-out scan, at rates the sidebands also reach. C10's phase concentration is the nearest thing to a reading here, and it is below the frozen threshold by an order of magnitude in p. As PLAN-HMR2 §7 holds, failing a frozen test bars nothing.

What HMR2 does not touch: the HM5/HM6 power contrast (the X shift that follows the comet's drift) stands as reported. HMR2 asked whether D3's phase carries readable structure inside the frames, and in these readings it does not.

## Products

hmr2.py; hmr2_0013–0018.json; hmr2_score.json; hmr2-*.log; hmr2_selections.json. The per-frame arrays hmr2_0013–0018.npz (56 MB each) are kept out of git, and their SHA-256 values are in RESULTS-HMR2.sha256.
