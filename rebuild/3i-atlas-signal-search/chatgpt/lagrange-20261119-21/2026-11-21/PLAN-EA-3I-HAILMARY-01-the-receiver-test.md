# EA-3I-HAILMARY-01 — The Receiver Test
**21 November 2026. Final bounded experiment. No extraterrestrial signal identified.**

## Finding worth falsifying
Claude's GBT OH13R worker analyzed the original thirteen with 96 statistics, two temporal configurations, 833 frames × six scans, both feeds, 84 frequency windows, 72 matched controls, 198 injections. **No individual candidate survived ON/OFF and half-scan gates.** One aggregate residual is D3 lag-2 phase curvature in X in the comet frame: p = 0.0002 vs selected candidates' 72-frequency-window control sets, below the reported Bonferroni 0.05/96 threshold. It is thinly distributed across C10, C11, C07, C09, C13; it appears in single ON and once OFF scans; the Y and topocentric views have p ≈0.50 and 0.21. Therefore **not comet-localized, not a candidate**.
[Worker report](RESULT-GBT-cc7-original-thirteen-OH13R.md).

## Archive-grounded construction
- #1625 *Mammonic Transmission Engineering*: a channel's invariance class defines what it can transmit; every telescope reduction loses information. https://www.alexanarch.org/s/records/1625/
- #1535 *The Operator and Its World*: projected sign-state is insufficient when substrate/provenance are operative; retain actual feed, pointing, observing geometry, byte witness and process. https://www.alexanarch.org/s/records/1535/
- #902 *Prolegomena to the Historical Logos* and #1757 *Historical Logos*: ask what operation persists across material transitions, not what familiar message is represented. https://www.alexanarch.org/s/records/902/ ; https://www.alexanarch.org/s/records/1757/
- #1484 *Sappho, Mother of the Logos*: separate a hard observational center from interpretation and outer hypothesis. https://www.alexanarch.org/s/records/1484/
- #1736 *Attribution Sharding*, #670 *SPXI*: preserve provenance and negative disambiguations so a composed explanation never erases its physical warrant. https://www.alexanarch.org/s/records/1736/ ; https://www.alexanarch.org/s/records/670/
- #1637 *The Final Time*: representation does not equal independent reproduction; require genuinely held-out standing. https://www.alexanarch.org/non/the-final-time/

These are methodological analogies rigorously converted into controls; **not** evidence that aliens use the Logos.

## Frozen empirical test: selection-counterfactual D3
Original 40 false-drift rates from `oh13/code/oh_scan.py`: **-0.20 ... -0.01 and +0.01 ... +0.20 Hz/s, steps of 0.01**. Its selection calls `cf.coincidences(d*cf.C/1.667e9,keep=True)`. Recompute 40 cohorts at same ON≥2.5, OFF<2.0, ±1 native bin tolerance; merge within 10Hz. Preserve all cohorts including empty ones; no change to threshold after looking.

Using channel7 **original complex GBT voltages**, all 833 frames of six scans, both feeds, apply each cohort's **own** false-drift track. For each selected coordinate compute same D3 X phase curvature (lag 2) with the original OH13R window and pooling, and at ≥8 predeclared frequency offsets. Formula, `u[k] = X[k]/abs(X[k])`: `Q2 = abs(mean_k( u[k]*u[k+4]*conj(u[k+2])**2 ))`. It is invariant to global phase and a linear frequency-phase ramp, not arbitrary instrument phase.

For each scan and selected coordinate, rank Q2 among its same-scan sidebands; take candidate ON mean rank minus OFF mean rank; per cohort report mean contrast and `sqrt(n)*mean_contrast` (candidate-count scale correction). Primary comparison: C03–C13 true-cohort `sqrt(n)*mean` against **40 false-drift selected** control cohorts under identical processing; empirical p = `(1 + #control cohorts >= true)/(1 + #nonempty controls)`. Floor at best 1/41 ≈0.0244. Inspect individual scan results and the X/Y, comet/topocentric specificity already recorded. The rank is descriptive because the control tracks share the same recordings.

**Crucial:** the previously significant p=0.0002 compared chosen candidates to *frequency-sideband controls*, not to candidates selected by alternative drift rates. The latter control tests whether the act of selection itself enriches D3. This is the only planned next falsifier, not a general new signal search.

## Gate and retirement
- If false-drift selected cohorts show equal D3 structure: classify original D3 as selection/receiver-associated; retire OH13.
- If true drift uniquely stands out but held-out ON observations fail: interesting residual without a candidate; retire until independent observations exist.
- If true drift stands out *and* individually replicates in held-out ON with sensitive OFF negatives: reopen as **directional astronomical anomaly requiring new telescope/epoch**, not ET.
- Never call the original D1 power-selection contrast independent evidence. Never add more lags, feeds or 97th statistic to rescue a negative.

## Local execution status
The deterministic Python cohort scorer `score_false_drift.py` was built and executed in this session; original data and real false-drift cohort measurements are **not present** in ChatGPT's container. Synthetic validation: constant/linear phase-ramp invariance passed. Under 200 synthetic no-effect cohorts, 7 yielded empirical p≤0.05; under 60 strong planted effects, 60 did. **Software validation only**. No false-drift GBT comparison has been performed here.

The full manuscript, scorer script and validations are in the conversation artifact `EA-3I-HAILMARY-01.zip`. The full networked-worker experiment requires Berkeley access and OH13R's original voltage extraction.
