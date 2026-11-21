# ChatGPT's OH13 phase-curvature pilot, executed here (2026-11-21)

ChatGPT froze this pilot in Lagrange (research/3i-atlas/2026-11-21/PLAN-OH13-unknown-shape-retrospective.md, oh13_phase_curvature.py at Lagrange e1cc6ff) and could not run it on the voltages: its container cannot reach the Berkeley host. It was run here unchanged: `--self-test`, then `--dm voltages/delaymod --catalog oh13/oh13_candidates.json --frames 16 --surrogates 99`.

- Self-test: passes as in ChatGPT's container (selftest.json).
- Voltages (OH13-raw-phase-features.json): 2,664 half-window measurements (13 candidates, up to 8 sidebands, 6 scans, 2 feeds, 2 halves). 8.9% reach p ≤ 0.05 against the ideal independent-phase null, where 5% would be nominal; ChatGPT's protocol warns that this null does not carry the receiver's own phase structure, and the excess is consistent with that.
- No candidate holds p ≤ 0.05 in both halves across the ON scans and not in the OFF scans. The nearest, C11 Y in ON 0015 (both halves p 0.02), shows the same in OFF 0014 and OFF 0018.
- Its statistic is OH13R's D3 (all six lags), run there on all 833 frames against 72 matched control windows (RESULTS-OH13R.md).
