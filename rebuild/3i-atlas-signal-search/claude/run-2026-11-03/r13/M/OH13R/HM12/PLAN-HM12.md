# PLAN-HM12: the unexamined branches and the dropped excesses, batch A

Frozen 22 November 2026, before any HM12 statistic is computed, at the author's word (17:53 EST): "lets examine unexamined branches and dropped excesses before closing". Batch A is the six that the kept products and files can answer tonight. Batch B, which needs voltages streamed again, is listed at the end and is not run here.

**What is looked for.** As in the whole series: "we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning."

**What has been read before.** The products below were read before by the runs that made them. None of the statistics in A1–A3 has been computed. HMR2's score file holds C10's R and p in every scan, but only ON 0013's were reported; the hold-out values have not been looked at.

## A1. HM11's track effect: where it lives

HM11 found the power character t (comet drift over mirrored drift, no scan sign) at 1st of 380 in 0017/0018, present in OFF as in ON.
- **Statistic.** Per scan, measure (P, D3) and feed: the comet cohort's c − f centred-rank contrast, its score (mean × √n), and its rank among 380, together with every coordinate's value. HM11's ranks and cohort products are reused unchanged (hm11.py imported).
- **Rule.** The effect is of these frequencies on this drift, not of the beam, if the OFF-only power rank is ≤ 19 (top 5% of 380) in at least two of the three OFF scans, in a feed. All else is reported.

## A2. The D3 excess against selection: its size

FD closed the D3 aggregate as a selection effect (p = 0.023) and said the size was not measured.
- **Statistic.** The true-frame mean Δ over the 11 candidates (FD's 2.18), against the per-false-frame mean Δ of the false-drift selections, FD's own kept values.
- **Rule.** The size exceeds what selection gives if the true mean is above every false frame's.

## A3. C10's phase concentration on the hold-out

HMR2's nearest reading was C10, R = 0.0906, p = 0.0011, in ON 0013 X.
- **Statistic.** HMR2's own R1 (Rayleigh R and p of arg D3 at d = 2) at C10 in every scan and feed, with its sidebands' highest R.
- **Rule.** HMR2's own: p < 1e-4 and R above every sideband, in ON 0015 or ON 0017, X, confirms. The ON 0013 value is a near miss, so this reads its continuation, not a confirmation of a pass.

## A4. r13 Part H, run and never written up

Part H (strength and injection outside L band, PLAN-r13 v2) has a product, r13/H.json, and no results file. RESULTS-r13 says it was not run; RESULTS-K says K started when it ended. H.json is read and written up as it stands, with the plan's rule (none: it reports strength and floors), and the conflict is settled from the file's own record.

## A5. M4b's one unexamined excess outside the known bands

M4b listed six class-A excesses. cc19, cc21, cc23, cc48 and cc50 were followed, or are Iridium and Inmarsat. cc01 (1684.57 MHz centre, 2 against 0) was not.
- **Reading.** Its events in M4b/events/cc01.json, by frequency, scan, drift and margin, set against the allocation at that frequency.
- It is read, not ruled: two events are too few for a count.

## A6. ChatGPT's voltage reports of 16 November

GBT-full-cadence-voltage-report-2026-11-16.md and GBT-raw-voltage-first-pass-report-2026-11-16.md (chatgpt/lagrange-2026-11-19/) are filed and have not been read in the record. They are read, and what they found is written into the results, as written.

## Batch B (not run here; each needs its own frozen plan and the network)

1. M4's 24 nominations from cc37 on, logged and not examined, and the fourteen channels whose details the 2026-11-20 restart took (cc14, cc15, cc19, cc30, cc32, cc37, cc39, cc43, cc45, cc46, cc49, cc50, cc51, cc55).
2. M4b's prescribed closer voltage look at class-A leads.
3. P1547B's ON0015 lag-2 item, "the one item worth the plan's scale-up".
4. ATA July 3 along the true drift at C08–C13.
5. N1625's shape test on its saved crops.

Failing a frozen test bars nothing. FROZEN-HM12.sha256 hashes this plan and hm12.py.
