# RESULTS-HM12: the unexamined branches and the dropped excesses, batch A

Run 22 November 2026 under PLAN-HM12, frozen and committed before any statistic (9969ebe13). Statistics are in hm12.json.

## A1. HM11's track effect lives in two scans, ON 0013 and OFF 0018

The comet cohort's c − f power contrast in X, by scan, rank among 380 (false mean beside it):

| scan | ON 0013 | OFF 0014 | ON 0015 | OFF 0016 | ON 0017 | OFF 0018 |
|---|---|---|---|---|---|---|
| X | **2** (0.42) | 243 (−0.04) | 31 (0.42) | 257 (−0.03) | 28 (0.41) | **3** (−0.00) |
| Y | 176 | 105 | 83 | 247 | 135 | 135 |

1. **By the rule, the effect is not shown to belong to the frequencies.** The rule asked for an OFF-only rank of 19 or better in two of the three OFF scans. X gives 243, 257 and 3; Y gives 105, 247 and 135.
2. **What carried HM11's "1st of 380 in 0017/0018" is OFF 0018 alone, 3rd of 380 in X.** In 0018 the contrast is spread over C03, C07, C10, C12 and C13 (+0.75 to +0.88). It sits in one OFF scan, in one feed, with the comet out of the beam. That is a feature of that scan at those frequencies, of the kind HM6 recorded in OFF 0014 (READ-HM5-frames), not a property of the comet's track.
3. **In ON the drifting-window bias is again the base.** The false cohorts carry c − f near 0.42 in every ON scan and near 0 in every OFF. Against it, the comet ranks 2nd in ON 0013, the first pair again, and 31st and 28th in the later ON scans.
4. Y carries nothing in any scan.

## A2. The D3 excess is within what selection gives

The true-frame mean Δ over the 11 candidates is 2.18. FD's 39 non-empty false-drift frames have mean Δ 0.59 and maximum 7.48. The true value ranks 6th of 40 (p = 0.15) and does not exceed every false frame. **The size of the D3 excess is within selection**, as well as its presence (FD, p = 0.023). This closes the item FD left open.

## A3. C10's phase concentration does not continue

R1 at C10, X (Rayleigh R, p; the sidebands' highest R):

- ON 0013: 0.0906, p 0.0011 (sidebands up to 0.0616): the near miss, as HMR2 gave it.
- ON 0015: 0.0171, p 0.78 (sidebands up to 0.0427).
- ON 0017: 0.0457, p 0.18 (sidebands up to 0.0709).
- OFF 0018: 0.0628, p 0.038, above its sidebands (0.046): higher than in either later ON.

**Not confirmed in either hold-out**, and weaker there than in an OFF scan. C10 stays a near miss found in one scan.

## A4. r13 Part H ran in part

r13/H.json holds the plan's channel choice and results for **4 of the 12** channels: the four named-line channels with the highest T, X blc21 cc03 (12177 MHz) and C blc67 cc42, cc37 and blc33 cc28 (4752, 4767 and 6667 MHz). It holds no entries for the eight random channels or for the injections. So K's note ("K was queued behind part H and started when H ended", RESULTS-K) and RESULTS-r13's "has not been run" are both partly right: H started, wrote four channels and stopped. The file does not say why.

None of the four exceeds its false frames:

| channel | T | swap | false frames | max |
|---|---|---|---|---|
| 12177 MHz | 6 | 3 | 4.78 ± 2.16 | 10 |
| 4752 MHz | 4 | 6 | 2.88 ± 1.73 | 6 |
| 4767 MHz | 3 | 1 | 3.67 ± 1.77 | 8 |
| 6667 MHz, methanol | 2 | 2 | 3.42 ± 1.96 | 8 |

Strength (S) ranks are 30th, 11th, 14th and 13th of 41. The out-of-band detection floors that Part H was to give were not produced.

## A5. M4b's cc01 excess is the scans', not the comet's

cc01 is centred at 1684.57 MHz. Two class-A events, both in ON 0017, at 1685.0689 and 1683.2584 MHz, z 10.88 and 10.51, both with zero drift. A tone fixed on the comet would drift, and zero drift is the receiver's or the ground's frame. Around them, single-level hits run 0, 1, 10, 3, 13 and 1 across the six scans, OFF scans included. The band is the meteorological-satellite downlink allocation, 1675–1710 MHz, and the radiosonde telemetry of cc03 (1679.7–1680.0 MHz, RESULTS-M4) is next to it. These are terrestrial or orbital transmissions at zero drift, not a lead.

## A6. ChatGPT's voltage reports of 16 November, as written

- **First pass (GBT-raw-voltage-first-pass-report).** The raw files carry updating pointing headers.
  - In ON 0017, blocks 0–8 (0–1.43 s) are UNKNOWN at the initial discrepant position.
  - From block 9 (1.61 s) the state is TRACK near the comet.
  - From 22.91 s to 297.78 s every file's first block is within about 0.040 arcmin of the comet's interpolated position.
  - "The initial 16-arcminute discrepancy should no longer be carried as evidence of sustained mispointing."

  This bears on the notebook's §7.10, §7.14 and §10.2, and it agrees with r13: the off-target time is the start of the scan.
- **Full cadence (GBT-full-cadence-voltage-report).**
  - The C03 strict power score reproduces from the voltages (ON 2.67, 2.40, 1.85), and the strict three-ON gate still fails.
  - The coherent-tone family puts C03 at 18, 34 and 38 of 100 controls in the three ON scans, with an OFF scan nearer the top than any ON: "no exceptional, ON-specific support for C03".
  - Injection: 0.01 of the receiver rms in both feeds is recovered 11 of 11.
- **The 11.11 Hz component**, around which the data request of 2026-11-08 was framed, is in all six scans' raw power. Its peak-to-local-median ratio is 8.29, 9.25, 5.27, **377.76**, 47.98 and 42.36 (0013–0018), largest in OFF 0016: "inconsistent with treating the component as ON-specific. Its physical origin is unassigned." The notebook had not recorded this line or its fate; it is a dropped excess, closed by ChatGPT's measurement as not ON-specific.

## Reading

Of batch A:

- **Closed:**
  - the D3 excess's size (within selection);
  - C10's near miss (does not continue);
  - cc01 (zero-drift transmissions in an allocated band);
  - the 11.11 Hz line (in every scan, strongest in an OFF).
- **Narrowed:** HM11's track effect is OFF 0018 in X plus the first pair, not a property of the comet's track.
- **Written up:** r13 Part H, 4 of 12 channels, none exceeding.
- **Recorded:** ChatGPT's header finding, which supports ON 0017 tracking after its first 1.6 s.

The one result that keeps returning is the first pair: ON 0013 is 2nd of 380 on c − f, as it was 20th in the HM8 contrast and 1st in D3. No batch-A reading explains it.

Batch B (PLAN-HM12) remains: M4's unexamined and lost nominations, M4b's voltage look, P1547B's lag-2 item, ATA July 3 at C08–C13, N1625's shape test. Each needs its own frozen plan and the network.
