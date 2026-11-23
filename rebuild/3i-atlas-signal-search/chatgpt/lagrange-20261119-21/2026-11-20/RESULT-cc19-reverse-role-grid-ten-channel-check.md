# 3I/ATLAS — cc19 fixed-family follow-up, ten-channel reverse-role frequency-grid test
Date: 2026-11-20. **Executed on original M4b event JSON, not raw voltage.**

## Method
Fetched the original `M4b/events/ccNN.json` for ten selected GBT coarse channels: 03,08,14,19,21,22,23,38,48,50.

For each channel's `events` (source-pointing) and `control_top` (role-exchanged off-pointing), independently find the best approximately periodic single grid:
- For all frequency pairs f_i,f_j in the saved list and integer tooth gaps g=1..20, set spacing s=(f_j-f_i)/g;
- keep 65000 <=s<=70000 Hz;
- select integer grid positions n=round((f-f_i)/s) whose residual is <=25 Hz;
- report the maximum **distinct matched integer positions**. A best match of 2 is trivial, because two anchors define a grid.
- This intentionally tests only one grid in each saved list, not the full two-offset cc19 model. The frequency range and tolerance were previously chosen from cc19 and are post-hoc.

| channel | on events saved | reverse-role events saved | best ON grid | best reverse-role grid |
|---|---:|---:|---:|---:|
|03|18|15|2|2|
|08|19|6|2|0|
|14|24|12|2|0|
|19|19|15|**8**|2|
|21|40|15|3|2|
|22|40|15|3|2|
|23|40|15|3|2|
|38|40|15|5|2|
|48|40|15|3|2|
|50|40|15|3|2|

The channel-19 source-pointing event catalogue is more regular than any of these saved controls. **Not a p-value**: channel occupancy, saved-list truncation (40 events ON vs 15 control limit), prior search selection, and correlated instrumental signals differ between lists. The cc19 catalogue has 17 of 19 events in ON0013, 1 in ON0015 and 1 in ON0017; all 14 teeth of the dual comb were selected in ON0013. No *full family* is replicated in another target scan within the event list.

## Better falsifiable followup
On Claude's original raw-voltage products:
1. Fix f_A0, f_B0 and shared period from prior ON13 catalogue; never re-optimize the grid separately on test scans.
2. For every scan 0013–0018 and common timestamps, record spectral-power/centroids of all 14 predicted lines, even if below threshold; use a frequency window that admits comet Doppler trajectory while separating neighboring lines.
3. Compute same scan's matched-grid statistic for translated grid phases, random periods, swapped ON/OFF roles and adjacent communications-band channels at matched frequency occupancy.
4. Measure time-dependent tooth gaps `f_n(t)-f_m(t)` and compare to independent per-tooth fits with proper uncertainties. A stable comb spacing need not be a celestial source.
5. Compare comet-ephemeris vs stationary topocentric and moving-satellite models on heldout scans and sky-pointing controls, penalizing free parameters.

## Standing
A numerical organization remains in the **saved catalogue**, not independently confirmed as a physical source nor an extraterrestrial emitter. Frequency-only matches alone do not establish transmitter identity, motion, phase coherence, persistence or origin.

Original source per channel: `https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/M4b/events/ccNN.json`.
