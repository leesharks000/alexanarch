# PLAN-HM8: the X power excess, in the other pairs and on Parkes's scale

Frozen 22 November 2026, before any HM8 product is read, at the author's word (14:08 EST: "and then lets touch the hm5/hm6 power excess in x"). It takes the two steps RESULTS-HM6 and RESULTS-HM7 left open:

- HM6's "drift test on 0015 and 0017", which asks whether the comet-drift dependence holds beyond the first pair;
- HM7's "natural next test", putting the Green Bank excess on HM7's Parkes scale, so that HM7's null can be read as a constraint or not.

**What is looked for.** As in the whole series, in the author's words: "we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning."

**What is already known.** HM6 found X power at C08–C11 rising with the comet's drift in the first pair (0013/0014): the mean ON − OFF rank was 0.80 on track c, 0.31 on d and −0.39 on f. C09 was as strong fixed at the dish. HM4 found the cohort weak in the other pairs.

**Code check before freezing.** hm8.py ran `scan` on 8 frames of 0015–0018 into the session scratchpad, then `score`, to check that it runs and writes the right structure. That score also computed Part B from HMR2's full products and printed it to a scratchpad log. The log and the score file were deleted unread. Only the output keys were listed. Nothing below was set from them.

## A. The three tracks in the other two pairs

1. **Data.**
   - Scans 0015, 0016, 0017 and 0018, all 833 frames, both feeds.
   - hm6.py unchanged (its SHA-256 is in FROZEN-HM6.sha256), run through hm8.py, with outputs in HM8/.
   - The same 11,452 windows: the comet cohort and 379 false cohorts.
   - The same tracks: c (the window's drift), d (dish-fixed), f (the drift mirrored).
   - The first pair is read from HM6's committed outputs.
2. **Reproduction.** For each new scan, track c power at every comet window (frame mean, X and Y) must equal HMR2's stored per-frame power, averaged over frames, to a relative 1e-4. If it does not, nothing in A is read.
3. **Rule, per pair (as PLAN-HM6 §3, X power):**
   - **follows the comet:** the C08–C11 mean ON − OFF rank on c is greater than on both d and f;
   - **fixed at the dish:** d ≥ c;
   - **otherwise:** not decided.

   C09 is reported per track in each pair. D3 and Y are reported, not ruled.
4. **What would extend HM6's finding:** "follows the comet" in at least one of 0015/0016 and 0017/0018. The mean over all three pairs is reported for each track.

## B. The Green Bank excess on HM7's scale

5. **The excess.** For each comet coordinate C03–C13 and each pair, in X and in Y, from HMR2's per-frame power (track c, the same definition as HM4 §D: the centre bin over the mean of the window's 129 bins):

   e = (frame-mean ON − frame-mean OFF) at the coordinate − the median of the same over its sidebands.

   e is in units of the local system power per native bin (2.794 Hz). The X value used is the mean of e over the three pairs.
6. **The translation**, with every factor stated now:

   a = e × (SEFD_GBT / SEFD_Parkes) × (d_GBT / d_Parkes)² × (2.794 / 2.0) × ½ / σ_Parkes.

   - **SEFD:** GBT L-band 10 Jy; Parkes UWL near 1.6 GHz between 25 and 40 Jy. These are from memory and not checked against the observatories' documents, so a range is carried.
   - **Distance:** a source of constant luminosity scales with the comet's distance squared. d_GBT = 1.798 au (Horizons, 2025-12-18). d_Parkes = 2.817, 2.548 and 2.483 au for the three sessions.
   - **Channel width:** a tone narrower than both channels puts the same power into a narrower channel of system noise, so its fraction of the channel scales by 2.794 / 2.0.
   - **½:** an excess in one feed enters Parkes's total power against the noise of both.
   - **σ_Parkes:** HM7's measured σ per 2 Hz channel per 15 s, over the median (0.130, 0.130, 0.130).

   The result is a range of predicted a per coordinate and session.
7. **Reading B.** Against HM7's measured floor:
   - a ≥ 1.5, detected in every comet scan;
   - a ≈ 1, about half.

   A coordinate whose predicted a is at least 1.5 in a session, under the whole SEFD range, is one HM7's null **constrains**: if it were steady and comet-borne, Parkes should have seen it. Below 1, HM7's null **does not constrain** it. Between, partly. That variability between July and December would break the comparison is stated now: the translation assumes a steady source.

## C. What stays fixed

No other pair, track, window, factor or threshold, and nothing tuned after the score. Any amendment is recorded before results. A run stopped by the time limit is resumed from the start of the unfinished scan and marked in the log. Failing a frozen test bars nothing.

FROZEN-HM8.sha256 hashes this plan and hm8.py.
