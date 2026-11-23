# GBT cc7, the original thirteen (OH13R), object first under 96 representations, all 833 frames: nothing resolves; a thin aggregate phase-curvature excess without a candidate; no lead

**2026-11-21.** At the author's word: 'lets return to the initial hits. bring all the new filters to bear, in different configurations, on the assumption that we may not be able to recognize what is there. object first.' The battery includes ChatGPT's frozen OH13 phase-curvature statistic (D3), and ChatGPT's own 16-frame pilot (PLAN-OH13-unknown-shape-retrospective.md, oh13_phase_curvature.py) was executed unchanged on the voltages, which its container cannot reach.

Canonical run, frozen plan, code, products and hashes: [PLAN-OH13R.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/OH13R/PLAN-OH13R.md), [RESULTS-OH13R.md](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/OH13R/RESULTS-OH13R.md), [battery.py](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/OH13R/battery.py), [OH13R-PRODUCTS.sha256](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/OH13R/OH13R-PRODUCTS.sha256), [ChatGPT's pilot as run](https://github.com/leesharks000/alexanarch/blob/main/rebuild/3i-atlas-signal-search/claude/run-2026-11-03/r13/M/OH13R/chatgpt-pc/README.md).

The text below is RESULTS-OH13R as committed there.


Run 2026-11-21 under PLAN-OH13R with amendment 1 (FROZEN-OH13R-2.sha256: plan 2e48d2b9…, common.py 2ba25023…, extract.py 8ab6201b…, battery.py eccbfd03…; all checked after the run). Channel 7, all 833 frames of all six scans: 84 windows (C03–C13; C02 as the interference reference; 72 matched controls), 1,088 native bins each, both feeds (win_00NN.npy, hashed in WIN.sha256, kept out of git for size). 96 statistics in two frame configurations; 198 injections; the reading (reading.json).

## 1. The object

Portraits first (object/C02–C13.png, object/portraits.json): comet-frame dynamic spectra at native resolution (2.79 Hz, rows of 17 frames), X and Y separately, the integrated profile ±64 bins, and the centre-bin phase over the scan, in all six scans.

- **C03–C13: nothing is visible.** Within ±8 Hz of the track, the scan-integrated power sits within ±3% of each window's median in every scan and feed (the noise of that band is about ±1.3% per feed). One value stands at 4σ, C04 X in ON 0017 (1.053), with nothing beside it in the other ON scans. The centre-bin phases wander as noise does.
- **C02 shows what interference looks like here**: in X only, a comb of parallel narrow lines crossing the comet frame (fixed in the topocentric frame), the same in ON and OFF scans.

## 2. What each detector can see at the candidates' level (injections)

Synthetic objects on the comet track, in six control windows, in the ON scans only, at 1×, 3× and 10× the power the original selection implies (about 0.16 of a native bin's noise power, summed over the centre band). Count of the six windows that resolve under the frozen rule, and the detectors that resolve them:

| class | 1× | 3× | 10× |
|---|---|---|---|
| a. steady tone | **5/6** (D1, D2, D4) | 6/6 | 6/6 |
| b. tone, random-walk phase | 2/6 (D2) | 5/6 (D1, D2, D9b) | 6/6 |
| c. quadratic-phase chirp, ±64 bins | 0 | 0 | 0 |
| d. three-wave triple | 0 | 0 | 6/6 (D1 only) |
| e. coupled two-part pair | 0 | 1/6 (D1) | 6/6 (D1, D5) |
| f. same signal in both feeds | 1/6 (D6) | 6/6 (D1, D6) | 6/6 |
| g. recurring spectral shape | 0 | 0 | 0 |
| h. tone switched at 1.3 Hz | **5/6** (D2, D4) | 6/6 | 6/6 (+D8) |
| i. 50 ms bursts | 0 | 6/6 (D1, D4) | 6/6 (+D9a) |
| j. pattern copied 200 bins away | 0 | 1/6 (D1) | 6/6 (D1) |
| k. delayed copy | 0 | 0 | 0 |

So at the level at which the thirteen were selected, the battery would resolve a steady comet-frame tone or a modulated one in five windows of six, a phase-wandering tone or a two-feed signal sometimes, and the rest only at 3× or 10× or not at all. D3 (phase curvature), D7 (shape recurrence) and D11 (delayed copy) do not resolve their own classes at any of these levels; D4 and D5 resolve theirs only through power or at 10×. These detectors are blind here, and their silence on the candidates is not absence.

## 3. The candidates

1. **Nothing resolves.** No candidate, under any of the 96 statistics, holds p ≤ 0.10 against the controls in all three ON scans, stays above 0.10 in all three OFF scans, and stands in both halves. No control does either (0 of 6,912 window-statistics), so the rule's null rate is below what these data can show, and 0 of 1,056 candidate-statistics is consistent with it.
2. **The interference reference is recognized and set aside.** C02 is low in all six scans, ON and OFF, under D1, D5 (X−, R(64)), D10 and D11 in X: the battery sees the ground tone and the location rule rejects it.
3. **The aggregate tests.** Of the 96 aggregate tests (the candidates' mean ON−OFF contrast against 10,000 random sets of 11 controls), 9 reach p ≤ 0.05 against 4.8 expected. Two pass Bonferroni (0.05/96 = 0.00052):
   - **D1, X, comet frame: p 0.0003.** This is the power the thirteen were selected on (X+Y summed then; X here), and an excess of it among them is the selection seen again, not new evidence.
   - **D3 at lag 2, X, comet frame: p 0.0002** (two random sets of 10,000 as high). This is phase curvature, |mean u[k]u[k+4]conj(u[k+2])²| over ±64 native bins per frame, which the selection did not measure. A steady tone injected even at 10× leaves it unmoved (p 0.01–0.99 across windows and scans), so it is not the selected power leaking through.
   - Next, below Bonferroni: D5 (R(64), XY−, comet) p 0.0006; D9b (Y, topocentric) p 0.0022.
4. **What carries the D3 excess.** It is spread thinly across five candidates, and no one of them is a source:
   - ON−OFF contrast: C10 7.81 and C11 5.83 exceed every control (maximum 4.39); C07 4.40, C09 4.11, C13 3.47; the other six run from −2.96 to 1.49.
   - Per scan (ON 0013, 0015, 0017 / OFF 0014, 0016, 0018): C10 0.027, 0.041, 0.22 / 0.89, 0.90, 0.75; C11 0.014, 0.26, 0.014 / 0.027, 0.81, 0.75; C07 0.63, 0.027, 0.15; C09 0.26, 0.41, 0.027.
   - It is in X only (D3 lag 2 in Y, comet: p 0.50) and in the comet frame only (in the topocentric frame, p 0.21). An X-only feature is what C03 showed under the earlier polarization split; X-only points to linear polarization along the X feed, as the ground interference here is.
5. **Verdict under the plan: no lead.** The plan makes a lead require a resolving candidate. Here there is an aggregate signature with no resolving candidate: a small curvature excess, carried by single scans of several candidates, once in an OFF scan (C11, OFF 0014), in one feed and one frame.

## 4. ChatGPT's pilot, run here

ChatGPT's 16-frame phase-curvature script, frozen in Lagrange, was run unchanged on the voltages (chatgpt-pc/): its self-test passes; on the data no candidate holds p ≤ 0.05 in both halves in the ON scans and not in the OFF scans; the nearest, C11 Y in ON 0015, shows the same in OFF 0014 and 0018. Its ideal-phase null gives 8.9% of 2,664 measurements at p ≤ 0.05, which its own warning anticipates.

## 5. What this establishes, and what it does not

- Under 96 representations of the raw voltages, all 833 frames, both feeds and both frames, against 72 matched controls processed identically, none of the thirteen stands apart in a way that holds in all three ON scans, avoids the OFF scans and holds in both halves.
- At the selected level, a steady or modulated comet-frame tone would have resolved in about five windows of six. The thirteen are not that.
- Several representations (chirp, recurring shape, delayed copy, and at 1× the three-wave and two-part forms) cannot see their own classes at this level. For those, nothing here excludes anything.
- One unrecognized relation is measured among the candidates and not among the controls: the lag-2 phase curvature in X in the comet frame, at Bonferroni level, thinly spread. It is not attributable to any one candidate, and it is not localized.
- **The decisive next test, not run here:** the same single statistic, frozen, applied to windows chosen by the original detector at its 40 false-drift rates (oh13/code; RESULTS M1). If those selections show the same curvature excess, it belongs to the original detector's selection; if they do not, it is specific to the comet frame and wants the full location treatment.

Products: PLAN-OH13R.md, common.py, extract.py, battery.py, the FROZEN files, WIN.sha256, win_00NN.json, object/, stats_part0/1.json, inject_part0/1.json, reading.json, chatgpt-pc/ and this file, hashed in OH13R-PRODUCTS.sha256. The .log files are console logs and are not hashed.
