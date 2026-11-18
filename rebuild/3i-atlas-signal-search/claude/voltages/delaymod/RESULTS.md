# GBT 3I/ATLAS raw voltages — delayed copy and modulation, results of plan v1

2026-11-17. Plan PLAN.md (sha256 633462c6…8c64, frozen 23:10:43Z before decoding). Products hashed in PRODUCTS.sha256; statistics in results.json; code dm.py, analyze.py (hashes in FREEZE.sha256, with two logged amendments: storage of Pmean/z1 for 0013 only, and the OFF-scan raw filenames).

Data: coarse channel 7, all six scans, 833 frames each (21.0 GB streamed by HTTP multi-range from bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/, nothing raw stored).

## Validation

- Orientation: the fixed tone at 1665.615127 MHz falls at fine index 1017157–1017160 (rawspec 1017158), 18× local median, under f = fc − (i − N/2)Δ.
- Gate: C03's comet-tracked z in scan 0013 = 3.00 (original 3.0). Passed.
- M1 control product (plain power) reproduces the original comet-frame excess: 11 clusters at 2.5/2.0 against 3.2 ± 1.7 for 40 false-drift frames (maximum 7). The original rawspec run gave 13 against 3.75 ± 2.05 (maximum 8).

## Results

| Test | What it looks for | Result |
|---|---|---|
| M1, x² | BPSK carrier (line at twice the carrier, comet-tracked, doubled drift) | 0 clusters; null 2.7 ± 1.5 (max 6). Below the null |
| M1, x⁴ | QPSK carrier (four times) | 4 clusters; null 3.5 ± 1.8 (max 7). At the null |
| M3 | Envelope sidebands / rates 2.8 Hz–2.86 kHz at the thirteen coordinates, against 100 controls | 0 ON-only features at every coordinate and every control |
| D1 | Delayed copy, 0.34 µs–0.179 s (X, Y, X–Y) | 0 ON-only lags under the true labelling; the other 19 labellings give 0–2 |
| D2 | Delayed copy, 44.8 ms–134 s, per 5.7-kHz bin | 0 ON-only (bin, lag) at 5/3 and 6/3, every labelling |
| M2 low | Envelope modulation 0.0067–22 Hz per 5.7-kHz bin | 0 ON-only, every labelling |
| M2 wide | Envelope lines 0–1.46 MHz, whole channel | 0 ON-only; other labellings 0–1 |

Features present but not ON-specific (outside the rules, reported):

- An envelope line at 52.90–52.91 kHz in five of six scans (z 8.1, 9.8, 6.7 ON; 6.1, 6.7 OFF; absent in OFF 0014): common to ON and OFF.
- OFF 0014 carries strong envelope lines at 78.2, 89.4, 156, 201, 321, 433 Hz (z 34–82) and the highest short-lag power autocorrelation of the six (0.023 X, 0.041 Y at 44.8 ms), consistent with its known broad power excursion; 78.2 Hz recurs weakly in ON 0017 (z 4.5).
- X–Y voltage cross-correlation peaks at 5–10 samples (1.7–3.4 µs) in all six scans: receiver-common.

## Reading

In this channel, under these forms, the thirteen and the comet frame gain nothing: no suppressed-carrier line follows the comet, no delayed copy or modulation is ON-specific, and the x² count sits below its own null. The plain-power excess is reproduced from the voltages by an independent decoder. Not covered: lags beyond 134 s, copies that change frequency, cross-band copies, other channels.
