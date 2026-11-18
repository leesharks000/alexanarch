# PLAN-M stage 1: single-pass leads by drift tuning

Written 2026-11-18. The author, 17:49: "we dont have to find something that repeats. we have to find something that is structured and correlated with the comet in any one pass, and if it seems to be signal, use it to determine where else to look. we *dont know what we're looking for*, is the thing." This stage is a nomination screen. It produces leads, not detections; what a lead is decides where the next look goes. Hash in PLAN-M.sha256.

## Data

r13 part J's saved products: each scan's sparse z ≥ 2 lists of the P1 stack (m = 1), V2 (the telemetry's off-target rows dropped), for the comet frame and 400 false-drift frames. Across one scan the comet's Doppler drift moves about 12 bins (33 Hz). A tone following the comet is sharpest at the comet's drift; a fixed terrestrial tone is sharpest at zero drift.

## Nomination, one scan at a time

1. Candidates are comet-frame positions with z ≥ 4. DC is masked, as in J.
2. Each frame is registered to the comet frame by its v0, as J registers scans.
3. A frame is *distinct* from the comet if its drift over the scan differs by at least 6 bins.
4. A candidate is nominated if its comet-frame z exceeds the largest z, within ±2 bins of its registered position, of every distinct frame, by at least 1.0. That is, its tuning peaks at the comet.
5. Nominations within 4 bins are one lead.

## Controls, the same procedure

- **OFF passes.** The three OFF scans are nominated exactly as the ON scans. They point away from the comet, so a comet-tuned lead there is chance or sidelobe.
- **Pseudo-targets.** 40 false frames, drawn with default_rng(29), are each taken as the target in place of the comet. They are nominated against all other frames, including the comet frame, under the same distinctness rule.

## Reading

Per scan, report the comet's lead count against the OFF scans' and the pseudo-targets' counts. Each lead is listed: scan, bin, offset from the coarse-channel centre in Hz, comet z, margin, and drift tuning. An ON lead that does not stand out against these controls is listed, not pursued. A lead that does stand out goes to stage 2. Stage 2 is the structure battery on its voltages (envelope, phase and harmonic structure), and then a search wherever the lead's own properties point. Stage 2 is written after stage 1 is read.

## Limits

This stage sees only what the 49-integration stack sees: power steady enough to rise to z ≥ 4 within one look. Structure that switches inside the look is stage 2's object.
