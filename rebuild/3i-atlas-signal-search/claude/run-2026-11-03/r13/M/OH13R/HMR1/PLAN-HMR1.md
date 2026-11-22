# PLAN-HMR1 — reading before attribution, first step: is there sequence at all?

Frozen 22 November 2026, before any HMR1 product is read, at the author's word. His question (11:17): "can we attempt to read the material on the x as message prior to determining what it is? that is a separate series of tests and procedures that can be practiced prior to an external determination. measures for determining pareidolia directly without external confirmation of source." His ruling (11:21): "yes lets freeze that first reading."

**The reading series (HMR).** Reading and attribution are kept apart. A reading is a procedure, and its pareidolia is measured from inside the data: the same procedure is run where no message can be (sidebands, the OFF scan, the Y feed, surrogates that keep the series' lower-order statistics), and the rate at which it "finds" structure there is reported beside what it finds at the comet. As in HM3–HM6, in the author's words: "we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning."

**Why this step comes first.** READ-HM5-frames found the C08–C11 excess to be a steady shift of the whole distribution, with no bursts and no co-movement at lag 0. A steady excess carries almost nothing as a sequence at 0.36 s per frame. So the first reading asks only whether the per-frame series at the comet's coordinates has sequential structure beyond chance. If it does, there is something to read at this resolution. If it does not, the reading moves inside the frames, to the phase sequence that D3 measures in aggregate (the next plan).

**What the measures can and cannot show, stated now.** Structure beyond surrogates rules out noise of the same spectrum and distribution. It does not by itself show language or intent: in the Indus-script dispute (Rao 2009; Sproat 2010, 2014), entropy measures of this kind did not separate linguistic from non-linguistic structured systems. A pass here means "there is sequence to read", nothing more.

**Code check before freezing.** hmr1.py was run on two windows into the session scratchpad, to check that it runs and writes the right structure. No value was read. The compressor was changed from lzma to zlib at that point for run time (0.045 s against 0.00002 s per call), before any value was read.

1. **Data.** HM5's kept per-frame series (hm5_0013.npz, hm5_0014.npz): power (frP) and D3 (frD), X and Y, for the 95 comet windows, the 11 coordinates C03–C13 and their 84 sidebands, 833 frames each, ON 0013 and OFF 0014. Nothing else; no voltages are read.
2. **Measures**, for every series (95 windows × 2 statistics × 2 feeds × 2 scans = 760):
   - **M1, lag dependence.** Ljung–Box Q over lags 1–50, against 1000 shuffles of the same series (z and p).
   - **M2, structure beyond spectrum.** The series cut into four quantile symbols and compressed (zlib, level 9). The compressed length is set against 1000 IAAFT surrogates, which keep the power spectrum and the value distribution and randomize the rest. Shorter than the surrogates means structure beyond linear (z and p).
   - **M3, lagged co-structure among C08–C11.** The largest |cross-correlation| over lags −20 to +20 frames (about ±7 s) for each of the six pairs, against the same measure on sideband pairs taken one sideband from each coordinate.
   - Random seed 20261122.
3. **The reading rule, stated now.** Threshold T = 3.3, about one-sided p = 0.0005, which covers the 44 comet tests in each scan (11 coordinates × 2 measures × 2 statistics) at a family rate under 0.05.
   - **Sequence at the comet:** in ON 0013, X, a coordinate's M1 or M2 z is at least T and above every one of its own sidebands.
   - **Not the comet:** the same coordinate passes as strongly in OFF 0014 or in Y.
   - **The procedure's pareidolia rate:** the number of sidebands at or over T, per scan, statistic and feed, reported beside every pass. A pass is read against that rate.
   - **M3:** the C08–C11 mean pair value above the sideband pairs' 95th percentile in ON X is co-structure in time among the four. Reported in all four scan–feed cells.
   - **Nothing passing** means no sequential structure at frame resolution. The reading moves inside the frames.
4. **Hold-out.** HM5 kept per-frame series only for 0013 and 0014. A coordinate that passes is carried to a frozen confirmation on ON scans 0015 and 0017. That needs a voltage run, planned and frozen before its product is read. Without it, a pass stands as found in one scan.
5. **What stays fixed.** No other measure, lag range, symbol count, threshold or window within HMR1, and nothing tuned after the score. Any amendment is recorded before results. Further readings are frozen from what HMR1 shows before their own product is read; failing a frozen test bars nothing.
