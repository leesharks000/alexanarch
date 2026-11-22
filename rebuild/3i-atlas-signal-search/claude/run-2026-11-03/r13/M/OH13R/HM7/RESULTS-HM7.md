# RESULTS-HM7: the thirteen at Parkes

Run under PLAN-HM7, frozen in 9285478b3 before any Parkes product was read. Three sessions (2025-07-31, 09-12, 10-05), node blc07, three comet/reference pairs each, plus Sep 12's three earlier comet scans (reported, no rule). Twelve candidate windows, 72 controls. Scored 22 November 2026, 14:08 EST. No amendment. No window came within 100 Hz of a coarse-channel DC bin in any session, so none was flagged.

## 1. R1, the Green Bank selection transposed

**No candidate passes in any session.** No candidate has Z ≥ 2.5 in all three comet scans and Z < 2.0 in all three reference scans. Single comet scans reach 2.4–2.5 only:

- C02, Jul 31 S2 (2.39) and Sep 12 S3 (2.42);
- C08, Sep 12 S3 (2.50);
- C03, Oct 5 S3 (2.46);
- C07, Oct 5 S3 (2.51).

Each is paired with ordinary values in the other comet scans of its session. Nothing replicates; R1 holds in zero sessions for every candidate.

## 2. R2, standing apart

D is the mean comet Z minus the mean reference Z.

| Candidate | Jul 31: D (pct) | Sep 12: D (pct) | Oct 5: D (pct) |
|---|---|---|---|
| C02 | 0.86 (92)* | 0.54 (68) | 0.08 (64) |
| C03 | −0.31 (39) | −0.11 (47) | 0.40 (76)* |
| C04 | 1.06 (93)* | −0.59 (26) | 0.30 (74) |
| C05 | 0.68 (88) | −0.73 (19) | 0.97 (90) |
| C06 | 0.31 (76) | −1.49 (1) | 0.57 (81) |
| C07 | 0.42 (81) | −0.34 (36) | 0.59 (81) |
| C08 | −0.59 (29) | 0.69 (76) | −0.12 (47) |
| C09 | 0.59 (85)* | 0.98 (86)* | 0.74 (82)* |
| C10 | −0.48 (35) | 1.22 (94)* | 0.30 (74)* |
| C11 | −1.03 (14) | 0.19 (54) | 0.09 (64) |
| C12 | 1.05 (93)* | 1.46 (97)* | −0.37 (39) |
| C13 | −1.27 (7) | −0.32 (36) | 0.42 (76) |

\* = above all of the candidate's own controls (R2). pct = percentile among all unflagged controls in the session.

**C09 stands above all its own controls in all three sessions**, at the 82nd–86th percentile of the pooled controls. No candidate is at or above the 99th percentile in any session. C12 is at the 93rd and 97th percentiles in two sessions and the 39th in the third. Twelve candidates in three sessions make 36 chances to stand above six controls; by chance about 1 in 7 (≈5 of 36) would. Here 10 of 36 do (binomial p ≈ 0.03, treating the 36 as independent; neighbouring windows share data, so this is generous). C09's three of three is the only one consistent across sessions; the chance that some candidate of twelve does so is about 12·(1/7)³ ≈ 0.035.

## 3. Family tests

| Session | All twelve: mean D, p | G1667 (C08–C11): mean D, p |
|---|---|---|
| Jul 31 | 0.107, 0.074 | −0.377, 0.72 |
| Sep 12 | 0.125, 0.31 | 0.768, **0.031** |
| Oct 5 | 0.330, **0.026** | 0.250, 0.20 |

Six family tests were run, and two fall below 0.05, each in a different session and family. The plan states no correction and no combination rule, so these are reported as they are. The chance of at least two of six independent tests falling below 0.05 under the null is about 3%; of at least one, about 26%. The all-twelve mean D is positive in all three sessions (0.11, 0.13, 0.33). That is consistent in sign and weak in size.

## 4. Sensitivity

A tone on the track, a·σ_k in one 2 Hz channel per 15 s integration, reaches Z ≥ 2.5:

| a | Jul 31 | Sep 12 | Oct 5 |
|---|---|---|---|
| 0.5 | 17% | 19% | 14% |
| 1 | 61% | 44% | 53% |
| 1.5 | 97% | 86% | 92% |
| 2 | 100% | 100% | 100% |

σ per channel is 0.13 of the median in every session. So HM7 detects, in every comet scan, a comet-frame tone carrying about **0.2 of the system power in a 2 Hz channel per 15 s integration** (a = 1.5). It detects about half of those at 0.13. No Green Bank candidate's power has been put on this scale (§6).

## 5. Descriptive: the 2 kHz strips of G1667, per IF (no rule)

Comet minus reference, centre channel over strip median, z against the window's own six controls (hm7_describe_2khz.json; the script was written after scoring, is descriptive, and is committed beside the plan's code):

- IF0 and IF1 (taken as XX and YY; the headers do not name the order): no candidate is consistently positive in either. The largest are C10 IF0 2.4 and C09 IF1 2.4 (Sep 12). C08 IF1 and C09 IF1 are −2.8 and −2.5 (Jul 31).
- IF2 and IF3 (cross products): their median is not a power scale, so the ratio is not meaningful. They are listed in the JSON but not read.
- The Green Bank X-feed excess has no counterpart here at 2 kHz. At that resolution a 2 Hz tone is diluted about a thousandfold, as the plan says.

## 6. What this says

At Parkes, on three dates, on each candidate's comet-frame track, none of the thirteen shows the Green Bank selection pattern. HM7 measured a floor at which a tone would have been seen in every comet scan, about 0.2 of the 2 Hz system power per 15 s, and nothing reached it consistently.

**What remains is weak and is reported as such:**

- the twelve candidates' mean contrast is positive in all three sessions;
- C09 stands above its own controls in all three;
- two of six family tests fall below 0.05.

None meets a frozen rule. None is at the strength that made the Green Bank selection. Failing a frozen test bars nothing.

**What HM7 cannot say:**

- **Whether the Green Bank candidates would have been visible at Parkes.** The telescope, the distance (2.5–2.8 au against Green Bank's December geometry) and the epoch all differ, and nothing scales the Green Bank power into Parkes flux. Putting the Green Bank candidates' tracked power on HM7's a-scale, per unit of system power, is the step that would let a non-detection here constrain them. It is the natural next test.
- **Anything about D3.** No Parkes voltages exist.

## Products

hm7.py; hm7_score.json; hm7-*.log; hm7_describe_2khz.py; hm7_describe_2khz.json; the three Horizons tables. The extracted arrays hm7_<session>_<scan>.npz are kept out of git, and their SHA-256 values are in RESULTS-HM7.sha256.
