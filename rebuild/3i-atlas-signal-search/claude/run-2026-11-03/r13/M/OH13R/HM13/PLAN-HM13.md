# PLAN-HM13: batch B, parts B1 and B4

Frozen 22 November 2026, 18:15 EST, before any HM13 product exists, at the author's word (18:00 EST): "yup lets freeze & run", answering PLAN-HM12's batch B. B2, B3 and B5 get their own plans after these start.

**What is looked for.** As in the whole series: "we are committed to not turning noise into meaning out of self flattery or desperation. and we are equally committed to reading meaning as meaning." Failing a frozen test bars nothing.

**What has been read before.** B1: the counts of the ten channels' nominations (RESULTS-M4, m4.log), and their M4/ccNN.json top-hit files and M4b events, are known; the nominations' frequencies, scans and batteries were never read, and the files that held them were lost on 2026-11-20. B4: the ATA July 3 session was read by RESULTS-ata-look at ten other frequencies; nothing at C08–C13 has been read in ATA data.

## B1. M4's ten lost channels, recovered and examined

Channels cc30, cc32, cc37, cc39, cc43, cc45, cc46, cc49, cc51, cc55 (centres 1599.609 to 1526.367 MHz). RESULTS-M4 counts 1, 3, 1, 1, 2, 3, 2, 6, 2, 4 nominations (25). cc14, cc15, cc19 and cc50 are not rerun: their own plans (C14, C15, C19, C4850) followed them.

**Run (hm13b1.sh), the frozen code unchanged:** per channel, `mvb.py CC SCAN` for the six scans (the stacks the M4b run made for these channels), then `mvolt.py CC` (M4's voltage battery and nomination rule, PLAN-M3). M4/ccNN.json and M4b/events/ccNN.json, which survive, are not rewritten. Each volt/ccNN.json is hashed into HM13/VOLT-HM13.sha256 and copied into HM13/volt/ as soon as it is written. The stacks are then deleted, as M4b did.

**Gates, before any nomination is read:**
- G1, reproduction: the twelve stack hashes per channel equal M4b-PRODUCTS.sha256.
- G2, counts: each channel's nomination count equals RESULTS-M4's.
- A channel failing either is reported as failing and its nominations are read only as unreproduced.

**Reading each nomination (hm13b1_read.py, frozen with this plan).** Its scan, feed, topocentric frequency, z, battery (W1 and its envelope frequency, k4), and:
- *off-source*: a top hit of any OFF scan in M4/ccNN.json within ±50 Hz topocentric (the cc03 test);
- *recurrence*: in comet-frame frequency (each scan's stack reference velocity f0_v0), the number of ON scans whose hits lie within ±2 bins (±5.6 Hz) of it;
- the allocation at its frequency (ITU Region 2 / FCC table), recorded, not ruled.

**Rule.** A nomination is **closed** if off-source. Otherwise it is a **lead**: *recurring* if it recurs in two or more ON scans, *single-scan* if not. A recurring lead is passed to B2 (the closer voltage look). Single-scan leads are listed with cc08's.

## B4. ATA July 3 along the true drift at C08–C13

**Run:** `ata/look_v2.py OH13R/HM13/look_hm13.json OH13R/HM13/targets_hm13.json`, the method of RESULTS-ata-look unchanged (±30 kHz windows; true comet path from Horizons at the ATA site, its sign-flipped twin and dish-fixed, each with beam swap; avg z ≥ 4 or sample z ≥ 5 with the other beam quiet). Targets, rest frequencies in MHz: C08 1667.412866, C09 1667.430186, C10 1667.686517, C11 1667.994976, C12 1668.098187, C13 1668.429424. C08 and C09 are 17 kHz apart and their windows overlap; each is scored at its own frequency.

**Statistic (hm13b4.py, frozen with this plan).** For each target and each of the six labels (comet, comet_swap, flipped, flipped_swap, topo, topo_swap): the scan-average ("avg") features of all 16 scans, clustered by off_Hz (single linkage, ±4 Hz); a cluster's persistence is the number of distinct scans in it. Max persistence per label.

**Rule.** A target is a **lead** if the comet label has a cluster of persistence ≥ 3 and every other label's max persistence at that target is ≤ 2. RESULTS-ata-look found max 2 everywhere at its ten frequencies, comet path and backgrounds alike.

**Bounds stated in advance.** One session (July 3, 2025, ~3.5 months before perihelion); 16.78 s resolution; the thresholds above; ATA July 3 has no frame calibrator, and at the object's July distance natural OH is not expected.

FROZEN-HM13.sha256 hashes this plan, hm13b1.sh, hm13b1_read.py, hm13b4.py and targets_hm13.json.
