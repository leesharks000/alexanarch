# External: the inscription experiment (received 2026-11-19 08:37 EST)

One file, verbatim as received from the operator: `REPORT.md` (dated 18 November 2026). The producing agent is not named in it. The evidence bundle it describes (waveform, transformed packet, frozen plan, byte-range ledger, code, score curves, trial rows, figures, `INPUTS.json`, `VALIDATION.json`) was not received.

## What it reports

The operator's echolocation call (#1786's attachment, original-speed WAV) was band-limited, translated to baseband and resampled to 91552.734375 complex samples/s, then added in voltage to 204 raw blocks of coarse channel 7 from the same six scans (blocks 816–849 of each, 6.08 s per scan). Two receivers got the same inserted voltage: a wide one (±39 kHz) and a bank of nine narrow ones (8 Hz each).

1. Sensitivity: the wide receiver recovered the repeated call's period in 12/12 configurations from 0.3% added power; the narrow bank recovered it in 0/12 until 10%.
2. Specificity: the wide selector also nominated 12/12 controls in which the same call was in ON and OFF alike. It picked one advantageous lag (0.873 s) where ON beat OFF by two, while the true period (1.750 s) stood equally in both.
3. The wide structure feature nominated 12/12 coherent-noise controls.
4. On the data: no wide nominations among the 8 target bands; two narrow nominations at exactly four output samples (0.0895 s), where the filter itself puts an autocorrelation lobe; one reserved wide nomination. No message found.

Its own reading: the receiver-mismatch demonstration worked; the comet-association selector failed, and the repair is not yet made.

## Checked here against r13

- Arithmetic checked: 2.9296875 MHz / 32 = 91552.734375 samples/s; / 2048 = 44.7035 samples/s for the narrow output; four samples at that rate = 0.0894785 s; 372500 samples at 250 kHz = 1.49 s, at 25 kHz = 14.9 s; 6.084537 s of a 300 s scan = 2.03%. All as stated.
- Not checked: the score tables, thresholds, the −0.192 filter lobe and the hash ledger. They need the bundle.
- **The narrow-receiver result applies to r13 M directly.** M2 finds hits as single 2.794 Hz bins at z ≥ 4; M3 reads ±64 bins around each, a 357.6 Hz band (PLAN-M3 §2). A signal spread across tens of kHz, like the call, puts its power across about 26,000 bins and makes no M2 hit at the powers tested here. M2–M4 cannot see a wideband inscription. Their null is a null for narrowband signals.
- **The association failure is the same failure as M4's cc03.** M3 nominates when W1 beats the OFF series at the hit's own bin (PLAN-M3, nomination rule). cc03's twelve nominations stand at frequencies that also appear in all three OFF scans' top hits (M4/NOTES-NOMINATIONS.md). Like the report's selector, the rule compares at one point where ON wins, while the shared structure stands beside it. Two instruments, one defect: association is tested locally, not across the ON/OFF profiles.
- **Boundaries.** Nine of cc03's twelve W1 lines lie at 0.101–0.133 Hz, at the lower edge of W1's 0.1–50 Hz range. The autocorrelation flags (`../autocorr-20261118/`) also sat near their delay boundaries. Boundary placement is recorded with each, as the report does.

## What it changes

Nothing in the frozen M4 run, which continues as frozen. The next plan after M4 must: (1) test association across the whole ON/OFF profile (shared structure at any lag or frequency nearby defeats a nomination); (2) add a wide receiver, so the band is searched for spread signals as well as lines; (3) be frozen and calibrated on fresh controls before nominating, as this report says.
