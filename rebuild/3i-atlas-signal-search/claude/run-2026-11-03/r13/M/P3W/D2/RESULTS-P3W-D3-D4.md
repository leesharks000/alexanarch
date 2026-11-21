# RESULTS — P3W-D3 and P3W-D4: ON0015 Y+ 422–440

Both plans frozen before their products (FROZEN-P3W-D3.sha256, FROZEN-P3W-D4.sha256), at the author's word of 2026-11-21 13:21 ("lets tie up those loose ends").

## P3W-D3: gate 4 at full length

1. cc21, scan 0015, all 833 frames, both feeds; the ctrl25k and hidrift slices streamed as the target slice was (p3wd3_stream.log).
2. Gate 4 at (422, 440), Y+, against the full-length no-wrap shift null (39 surrogates, seed 556), p3wd3_gate.json:
   - ctrl25k: A 0.00205; surrogate median 0.00257, maximum 0.00617.
   - hidrift: A 0.00266; surrogate median 0.00272, maximum 0.00644.
3. A sits at the surrogate median in both control slices. The pair does not couple away from the target slice. **Gate 4 passes at full length**, so ON0015 Y+ 422–440 has passed all four of P3W-D's gates, the first candidate of the line to do so. P3W-D2's one failure (gate 4, read on 32-frame control crops) is withdrawn on the full-length reading.

## P3W-D4: the pair in every scan and every family

At full length (ser_00NN.npy), 39 surrogates, seed 557, p3wd4_pair.json. A / surrogate median / maximum / rank of A among the 39:

| scan | X+ | X− | Y+ | Y− | XY+ | XY− |
|---|---|---|---|---|---|---|
| 0013 ON | .0026/.0028/.0057/18 | .0037/.0027/.0060/29 | .0014/.0029/.0073/8 | .0022/.0026/.0056/16 | .0038/.0025/.0072/34 | .0035/.0029/.0065/26 |
| 0014 OFF | .0062/.0029/.0073/38 | .0022/.0025/.0064/18 | .0018/.0033/.0059/7 | .0015/.0028/.0054/9 | .0023/.0024/.0054/19 | .0028/.0026/.0049/24 |
| 0015 ON | .0032/.0025/.0066/29 | .0041/.0026/.0074/32 | **.0118/.0028/.0069/39** | .0026/.0023/.0069/21 | .0044/.0030/.0062/33 | .0055/.0027/.0057/38 |
| 0016 OFF | .0026/.0023/.0069/22 | .0030/.0020/.0050/29 | .0010/.0020/.0052/3 | .0046/.0029/.0056/33 | .0010/.0026/.0060/4 | .0025/.0022/.0052/25 |
| 0017 ON | .0027/.0030/.0061/16 | .0026/.0026/.0060/19 | .0040/.0020/.0058/33 | .0011/.0023/.0048/6 | .0045/.0022/.0063/36 | .0014/.0025/.0068/12 |
| 0018 OFF | .0040/.0024/.0059/33 | .0019/.0026/.0053/14 | .0014/.0024/.0051/7 | .0021/.0029/.0071/13 | .0038/.0025/.0066/33 | .0015/.0023/.0069/8 |

1. **Location.** No OFF scan has the pair above its surrogate maximum in any family; the nearest is 0014 X+ (0.0062 against 0.0073). The candidate is not set aside as off-comet.
2. **One ON scan.** Only 0015 Y+ exceeds its maximum (0.0118 against 0.0069, rank 39 of 39); 0013 Y+ is low (rank 8), 0017 Y+ middling (rank 33). Replication is not required (the author's rule); it is recorded.
3. **Y only.** X+ in 0015 is at rank 29 and XY+ at 33, both under their maxima; XY− in 0015 is near its maximum (0.0055 against 0.0057) and under it. The relation is in one feed. By the plan's fixed reading, a Y-only relation points to the instrument or to strongly linear interference, as the X-only features of channel 7 do.
4. **The aggregate rule stands.** P3W-D2's aggregate family test is 2 of 36, chance; this follow-up does not test it.

**Verdict.** ON0015 Y+ 422–440 passes all four of P3W-D's gates at full length, is absent from the OFF scans, appears in one ON scan only, and only in Y. It fails the aggregate requirement. Not a lead.
