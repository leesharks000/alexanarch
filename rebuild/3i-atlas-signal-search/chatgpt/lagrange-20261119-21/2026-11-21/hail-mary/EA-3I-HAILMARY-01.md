# EA-3I-HAILMARY-01 — The Receiver Test
## One last bounded search for unrecognized structure in the original thirteen

**21 November 2026 · research instrument / experimental record · no extraterrestrial detection**

### 0. The finding that motivated this last experiment

The GBT OH13R worker has already processed six 18-Dec-2025 scans, all 833 raw-voltage frames per scan, X/Y polarizations, 84 spectral windows, 96 statistics in two frame configurations and 198 synthetic injections. No original candidate satisfies its three ON / three OFF / half-scan acceptance rule. At the original candidates' signal level, the battery recovers many tone-like injections, but not numerous nonstandard classes. Negative results for the latter are not exclusions.

Its **one unusual aggregate residual** is D3 lag-2 phase curvature, X feed, in the comet-aligned representation: a tail of 2/10,000 against 11-candidate groups drawn from 72 frequency-matched controls, meeting the reported Bonferroni 0.05/96 threshold. It is thinly distributed: C10 and C11 are prominent, C07/C09/C13 contribute, the other candidates do not. **No candidate replicates across all ON scans**. The same D3 family in Y has p ≈0.50, and in topocentric alignment p ≈0.21. An OFF observation also exhibits the property for C11. The original discovery searched a comet-aligned power statistic: the residual may be a consequence of selection or receiver structure, not a comet-associated source.

Source: [OH13R worker result](https://github.com/leesharks000/lagrange-observatory/blob/main/research/3i-atlas/2026-11-21/RESULT-GBT-cc7-original-thirteen-OH13R.md). The raw voltage products are hosted by Berkeley; source hashes and full worker provenance are in the corresponding OH13R record.

### 1. An archive-derived search philosophy, translated into *falsifiable* operations

| Source | What its argument actually says | Engineering translation | Defeater |
|---|---|---|---|
| *Mammonic Transmission Engineering* #1625 | A channel conveys the invariants of its substitution regime and drops other properties; its compression profile is its transmission protocol | Treat every measurement transformation as an explicit equivalence class; record what phase, polarization, time and frequency information it destroys | No anomalous structure remains after equal transformations of selected and control samples |
| *The Operator and Its World* #1535 | A sign-state projection fails as a complete account when substrate, provenance and institutional standing are causally operative | Preserve the actual telescope receiver/feed, pointing, Doppler alignment, byte provenance, filtering and noise-floor conditions, not just a shape label | Apparent structure depends on instrument feed or selection procedure rather than pointing to the comet |
| *Prolegomena to the Historical Logos* #902 and *Historical Logos* #1757 | Transmission is tested by recurrence of an operation across media and receiver-completion, not mere lexical sameness | Test structural invariance across comet, topocentric, false-drift, ON/OFF and held-out time views, *without presuming the structure is a message* | The operation fails to recur in independent ON data or occurs equally in counterfactual readers |
| *Sappho, Mother of the Logos* #1484 | Declares separate hard, interpretive and hypothetical evidence rings | Grade observations as raw measured fact, statistical inference, or origin hypothesis; never promote one ring by rhetorical force | Missing independent localization; no upgrade from interesting structure to intelligent origin |
| *Attribution Sharding* #1736 and SPXI #670 | Composition or retrieval can preserve surface plausibility while erasing specification/provenance; explicit disambiguation and persistence matter | Retain raw checksum, experimental masks, full control population, and code; label terrestrial, instrumental, indeterminate and target-specific hypotheses distinctly | Reproducibility failure or an omitted/contaminated denominator |
| *The Final Time* #1637 | Representation is not the same as the independent reproduction of a relation | A feature must replicate without being tuned to the new frame or scan | Single-scan significance, including strong p-values, cannot cross the standing threshold |

These mappings are **our new experimental constructions**, not claims that the literary-philosophical texts predict a radio signal.

### 2. The last empirical intervention: 40 false receivers

**Question:** Is the original comet-selected X-feed D3 excess different from the population yielded when the *same original candidate-finding algorithm* selects features under the **40 false Doppler accelerations** already specified by `oh13/code/oh_scan.py`?

The historical 40 false-drift rates are *not* newly tuned: **−0.20 to −0.01 and +0.01 to +0.20 Hz/s, increments of 0.01**. `oh_scan.py` calls `cf.coincidences(d*cf.C/1.667e9,keep=True)` and clusters coordinates within 10 Hz. This is a unique opportunity to test the residual not only against arbitrary nearby frequency windows but against **the exact type of selection that produced the initial thirteen**.

**Freeze: no new search families.** D3 phase curvature at separation d=2, X feed, comet-vs-false-drift aligned. Its complex-unit Fourier-phase invariant is:

`Q_2 = |mean_k [u_k u_(k+4) conj(u_(k+2))^2]|`, where `u_k=X_k/|X_k|`.

This cancels constant phase and frequency-linear phase ramps. It does not cancel arbitrary channel or nonlinear receiver phase. Its use here was prompted by OH13R (exploratory), so this is a **confirmatory *selection-bias* challenge, not a blind pre-registered discovery**.

#### Required worker procedure

1. Recover **all 41 original selection frames** (true 0 plus original 40 false rates) from the same raw spectral windows, at the exact ON>=2.5, OFF<2.0, ±1-bin, 10 Hz clustering specification. Keep the selected frequencies and scores, not just counts. Preserve empty cohorts.
2. Reread complex **channel 7 GBT voltages**, all 833 frames × six scans, X/Y, at each selected coordinate, applying the tracked frequency trajectory of that frame. Preserve 1088-bin complex windows and all metadata; do not borrow the true comet velocity for false drifts.
3. Measure Q2 over the **same original OH13R ±64-bin aperture and time pooling**, and also at >=8 fixed frequency-offset sidebands per coordinate with equal masks and clip rules. Ideally reuse OH13R's D3 implementation unchanged, not a rewritten estimate.
4. Compute within each scan an empirical percentile rank of target Q2 against its sidebands. For each candidate let its contrast be the *mean rank in three ON scans minus mean rank in three OFF scans*. For each drift cohort average candidate contrasts and multiply by sqrt(cohort size), to put unequal group sizes on roughly comparable scales; retain raw unscaled means and group counts too.
5. Compare the true **C03–C13** cohort (C01/C02 excluded as known interferer, retained separately as diagnostic) to the **40 selection-matched false-drift cohorts**, not to 40 arbitrary frequencies. The exact rank p is `(1 + #false cohorts >= true)/(1 + #nonempty false cohorts)`; the floor is at best 1/41 ≈0.0244. False cohorts are not independent recordings and cannot justify a smaller physical discovery p-value.
6. Do **not** add the OH13R D1 power result to the evidence: D1 was the original selection. Do not optimize D3 lag, feed or frame after inspecting outcomes. Report all individual scan scores and instrument controls, including any false-drift groups matching or exceeding the comet group.
7. Only if the original cohort outranks all false-drift cohorts and a held-out subset within ON independently carries the same frozen relation, run a *separate* receiver-consistency check (topocentric vs comet, alternate spectral windows, feed calibration). More transforms are used to falsify the survivor, not select a winner.

#### Why the false-drift control is decisive

The original 72-frequency-window null asks whether D3 is uncommon *at the thirteen already selected locations*. It does not answer whether **the act of selecting weak comet-aligned power coincidences** preferentially selects frequencies with the same phase curvature. The latter is the present null. A significant result after that correction would narrow the explanation, but still would not locate a source at the comet or show intelligence.

### 3. Executed validation in this environment

The accompanying self-contained scorer, `score_false_drift.py`, was executed on **synthetic cohort fixtures**, not astronomical data. It verifies phase-ramp invariance, exactly 41 frame labels, rank-score computation and the direction of the aggregate statistic. In **200 synthetic no-effect experiments**, 7 reached nominal tail `p<=0.05` (3.5%). In **60 deliberately strong-effect experiments**, 60 reached that threshold. This validates only the scorer and an artificial effect; it is not calibrated to the real telescope's correlated RFI and cannot predict its performance.

**The full false-drift voltage experiment has not run here**; the Berkeley raw recording is inaccessible to the current runtime. The worker's OH13R run, published on 21 November, is the latest available original-telescope result.

### 4. Interpretation gates and retirement rule

- **Same structure in false-drift cohorts:** selection machinery or a ubiquitous source explains the residual. Retire the thirteen as unconfirmed under these methods.
- **Unusual only at comet drift, but not independently reproduced in ON:** interesting selection-specific anomaly, no candidate, no sky attribution; retire pending new observations.
- **Unusual at comet drift and independent ON replication, absent in sufficiently sensitive OFF:** reopen as a directional *astronomical anomaly requiring independent telescope and observation epoch*, not an alien signal.
- **Any positive with OFF contamination, noncomet frequency behavior or feed-only dependence:** treat as RFI/instrument candidate until physically discriminated.

Stop after this result. Do not expand to a 97th detector when a negative returns. The strongest durable result may be a formal map of what the instrument's representations can and cannot admit.

### 5. Primary readings

- #1625, *Mammonic Transmission Engineering*: https://www.alexanarch.org/s/records/1625/
- #1535, *The Operator and Its World*: https://www.alexanarch.org/s/records/1535/
- #902, *Prolegomena to the Historical Logos*: https://www.alexanarch.org/s/records/902/
- #1757, *Historical Logos — Framework Hologram*: https://www.alexanarch.org/s/records/1757/
- #1484, *Sappho, Mother of the Logos*: https://www.alexanarch.org/s/records/1484/
- #1736, *Attribution Sharding*: https://www.alexanarch.org/s/records/1736/
- #670, *SPXI as Concept*: https://www.alexanarch.org/s/records/670/
- #1637, *The Final Time*: https://www.alexanarch.org/non/the-final-time/

**Bottom line:** the best last search is *not* a looser definition of signal. It is a stronger counterfactual receiver designed to explain or falsify the only residual the previous unprecedented search did not resolve.
