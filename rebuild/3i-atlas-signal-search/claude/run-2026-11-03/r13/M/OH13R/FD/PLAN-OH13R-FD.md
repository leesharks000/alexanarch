# PLAN-OH13R-FD: does the lag-2 curvature excess belong to the selection or to the comet frame?

Frozen before any FD product and before the false-drift selections were reproduced, at the author's word (2026-11-21 13:21, "lets tie up those loose ends"), on RESULTS-OH13R §3.3–3.5 and §5.

## The question

OH13R found one statistic the selection did not measure with an aggregate excess among the eleven candidates: D3 at lag 2, X feed, comet frame (p 0.0002), spread thinly, no candidate resolving. If the original detector's selection itself produces that excess (ON power ≥ 2.5 and OFF < 2.0 along a track, X+Y summed), windows the same detector selects along **false** tracks will show it too. If they do not, the excess is specific to the comet frame.

## Method

1. **The false-drift selections.** The original detector (oh13/code/cometframe_raw.py) is rerun unchanged on the public products (fetch_cc.py, coarse channel 7, scans 0013–0018) at the 40 false-drift offsets of oh13/code/oh_cluster.py (default_rng(11)), z_on 2.5, z_off 2.0, rows within 10 Hz merged. Each selection is a rest frequency and its false track, v(t) = deldot(t) + dv·(t − T0)·86400 as in cometframe_raw.py. The Horizons table is the one dm.py uses (voltages/delaymod/horizons-gbt-20251218.txt) if the live call fails.
2. **Windows and controls.** For each selection, a 1,024-bin topocentric window of channel 7 centred on its false track at each scan's mid, and six matched controls by OH13R's rule (offsets ±3.2, ±6.4, ±9.6 kHz, then ±12.8, ±16.0, ±19.2; no overlap with another window of the same false frame; 1.5 kHz clear of the known lines; 15 kHz clear of the edges), all on the same false track. A selection whose window would fall within 1.5 kHz of a known line is scored as a reference and left out of the aggregate, as C02 was. The eleven true-frame candidates and their 72 controls (dv = 0) are run the same way, as a check against OH13R.
3. **The statistic, unchanged.** OH13R's D3 (battery.py feats): each frame's window spectrum is de-Dopplered along its track (time series × exp(−iΦ), Φ = 2π∫off dt, per frame exactly as common.dedop), and Q_d = |mean_k u[k]u[k+2d]conj(u[k+d])²| over the centre ±64 bins, averaged over frames; d = 1, 2, 4, 8, 16, 32; X and Y. It is computed as channel 7 streams (fdstream.py), so no windows are stored. The statistic under test is d = 2, X; the others are reported.
4. **The test.** Per scan, each window's empirical p against all control windows of the same kind (false-drift controls for false-drift selections; the 72 OH13R controls for the true-frame candidates), controls leaving themselves out; Δ = Σ_ON −ln p − Σ_OFF −ln p; the mean Δ over the selections against 10,000 random equal-sized sets of their controls.
5. **Decision.**
   - The true-frame check must reproduce OH13R's D3 lag-2 X result (aggregate p ≤ 0.001), or the streaming implementation is wrong and the run stops.
   - If the false-drift selections give aggregate p ≤ 0.05 at d = 2, X: the excess belongs to the original detector's selection, and OH13R's aggregate is closed as a selection effect.
   - If they give p > 0.05: the excess is specific to the comet frame. That is not a lead (no candidate resolves); it is a reason for a new frozen plan with the full location treatment.

## Amendment 1 (before any FD statistic was computed)

fdstream.py failed on every scan without computing anything: `from common import *` brought in OH13R's `HERE`, so the script looked for fd_selections.json in the OH13R directory. One line restores the script's own directory after the import. A second defect sat behind it: the line defining the per-frame offsets and the window count (`off_f`, `nw`) had been folded into the end of a comment, so it would have raised a NameError; it is restored as its own line, with the same expression. Nothing else changes. Step 1 had run: the original detector reproduced the catalogue exactly at dv = 0 (13 clusters, the same rest frequencies) and found 150 clusters over the 40 false-drift offsets (mean 3.75, maximum 8), as RESULTS M1 and the catalogue's context record (3.75 ± 2.05, maximum 8).
