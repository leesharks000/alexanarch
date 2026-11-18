# RESULTS-ocad: the comet frame in the S, C and X cadences of 2025-12-18

Plan: PLAN-ocad.md (sha256 in PLAN.sha256), frozen 2026-11-17 before any spectrum was read. Order fixed in order.json before the first channel. Code run_ocad.py (CODE.sha256). Completed 2026-11-18 14:15:59 UTC.

## Result

**64 of 64 channels complete, in the fixed order. None exceeds its false frames.**

**The eight named-line channels.** T is the comet-frame count, μ ± σ the false-frame count, max the largest false count, and d_max the largest false ON − swap difference.

| Line (rest, MHz) | Channel | T | swap | false μ ± σ | max | d_max |
|---|---|---|---|---|---|---|
| CH3OH 6668.5192 | C blc33 cc28 | 2 | 2 | 3.42 ± 1.96 | 8 | 7 |
| OH 6035.0932 | C blc36 cc52 | 1 | 3 | 3.45 ± 2.04 | 8 | 6 |
| OH 6030.7485 | C blc36 cc53 | 1 | 1 | 3.20 ± 2.25 | 8 | 6 |
| H2CO 4829.6594 | C blc67 cc15 | 1 | 8 | 2.77 ± 1.96 | 9 | 5 |
| OH 4765.562 | C blc67 cc37 | 3 | 1 | 3.67 ± 1.77 | 8 | 6 |
| OH 4750.656 | C blc67 cc42 | 4 | 6 | 2.88 ± 1.73 | 6 | 4 |
| OH 4660.242 | C blc72 cc09 | 2 | 2 | 3.23 ± 1.89 | 9 | 4 |
| CH3OH 12178.597 | X blc21 cc03 | 6 | 3 | 4.78 ± 2.16 | 10 | 7 |

**Random channels.** 0 of 56 exceed (6 in S, 27 in C, 23 in X). The expected count by chance is 56/41 = 1.37. The largest E = (T − μ)/max(σ, 0.5) is 2.20, at X blc73 cc53. No channel has a false mean above 8, so none was set aside as interference-filled.

**Reading.** At this detector's gate, no channel of the three untouched cadences carries a comet-frame count above its null, and neither do the methanol, OH and formaldehyde lines in them.

## Deviations

- **Restarts.** The run was resumed four times: once after a container restart, and three times after the session's two-hour background limit (run.log). Each channel's result is written before the next is read.
- **A snapshot commit.** A 20-channel snapshot (ocad.json.snapshot, STATUS.md) was committed on 2026-11-18 before completion, at the operator's prompt to stash the files. It is superseded by ocad.json here.

## A caution found afterwards (r13/F_check.txt)

The 40 false frames are not exchangeable with the true frame. Across both the L-band survey and this one, false frames with small offsets rank higher than those with large offsets (Spearman ρ 0.74 in L band, 0.40 here). The true frame, at zero offset, is therefore favoured by the "above every false frame" rule.

Here the bias works only against a null result being too strong, and the result is null. It must be carried into any positive reading of this detector, and into the aggregate rank of r13 part F.
