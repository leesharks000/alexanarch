# Frozen plan: two-epoch match, Parkes 2025-07-31 against Green Bank 2025-12-18, in the comet's rest frame (written 2026-11-05 ~13:50 EST, before any match is computed)

Question. Does any comet-frame cluster found at Green Bank on 2025-12-18 recur, at the same rest frequency, among the comet-frame candidates found at Parkes on 2025-07-31, more often than chance? A transmitter or line fixed in the comet's frame would sit at one rest frequency at both epochs; interference fixed at the observatory would not, since the range-rate differs between the two dates and the comet-frame shift with it (a topocentric tone maps to different rest frequencies at the two epochs).

Inputs (no new data read; all already stored and hashed in this folder).
- Parkes: pks/fb_blc*.json, every true-frame candidate (`cands`, field f_rest_MHz), 22 nodes, 62,864 candidates; detector and frame as pks/PLAN-fullband.md (sha256 2337ec83…).
- Green Bank: lee/lee.json, the 64 surveyed coarse channels of blc22–blc25, field `freqs` (the true-frame ON channels at the comet frame, rest frequency, as written by lee/run_lee.py and lheld/run_lheld.py; blc23 coarse channel 7 is the thirteen). Channels are merged into clusters at 10 Hz before matching, as the thirteen were.
- Overlap: a Green Bank cluster is counted only where Parkes searched the same rest frequency (inside a Parkes node's span, outside the 300-channel block edges is not reconstructible from the stored files, so node span is used).

Statistic. For tolerance d, M(d) = the number of Green Bank clusters with at least one Parkes candidate within d of its rest frequency.
- Primary set: the surveyed channels with 50 or fewer true-frame clusters (the dense channels, blc23 cc23 at 1620 MHz and cc39 at 1573 MHz and any other above 50, are interference-dominated, already reported, and their `freqs` are truncated at 200 in lee.json). Secondary set: all 64.
- Primary tolerance d = 10 Hz (the cluster-merge width at both telescopes; a Horizons range-rate error of 1 m/s moves 1.6 GHz by about 5 Hz). Secondary tolerance d = 50 Hz.
- The thirteen: M13(d), the number of the thirteen with a Parkes candidate within d.

Null. The Green Bank cluster list shifted rigidly by Δ: 400 shifts, Δ drawn uniformly from [−50, −1] ∪ [+1, +50] kHz (numpy default_rng seed 5), each shifted cluster counted only where it still falls inside Parkes coverage. The shift keeps both lists' own spacing and density; it breaks only the rest-frequency coincidence. p = fraction of shifts with M ≥ the true M.

Decision. A lead: primary set, d = 10 Hz, p ≤ 0.01. For the thirteen: M13(10 Hz) ≥ 1 with p ≤ 0.01. Every matched pair is listed whatever the outcome, with its Parkes node, both rest frequencies, the difference, and the Parkes candidate's six scan scores. Secondary set and secondary tolerance are reported and do not decide. Nothing in this plan changes after the first match is computed.
