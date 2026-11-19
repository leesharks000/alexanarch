# External: the autocorrelation experiment (received 2026-11-18 19:38 EST)

Two files, verbatim as received from the operator: `SUMMARY.md` and `CLAUDE-HANDOFF.md`. The producing agent is not named in the files. They continue the series preserved in `../chatgpt-20261118/` (same data, same 8 Hz filtered stream, same C03–C13 windows). The report's other files (`REPORT.md`, plans, code, `INPUTS.json`, `source-verification.json`, results) were not received.

## What it reports

A search for self-similar complex voltage at delays of about 2–120 s, after comet Doppler correction, with no packet, rate or carrier supplied. The first version failed its negative controls and is kept as failed. A declared repair passed fresh negative controls (0/72 at 30% added power) and recovered repeated BPSK and complex packets from 3% added filtered power. On the data: 0 of 11 legacy windows flagged; 1 of 20 expanded windows flagged (`control-17000Hz`, rest 1665.616776617 MHz, delay 119.811691861 s, score 24.47 against threshold 15.76); 2 of 40 reserved windows also crossed. All three sit near the delay boundaries, and with extended lag context their scores fall to 4.97, 6.43 and 3.77. Its own reading: not robust evidence for a repeating comet source.

## Checked here against r13

- The flagged window's frequency, 1665.6168 MHz, lies inside the line complex that r13 M1 records at 1665.593–1665.750 MHz (RESULTS-M1.md): the leading comet-tuned feature in five of six scans at 1665.6152 MHz topocentric, also present in OFF0016 (z 8.8) and OFF0018 (z 7.2), its strength nearly unchanged between V0 and V2. r13 holds it as receiver-frequency interference, as does `../chatgpt-20261118/`.
- The report's stated frame is "rest"; M1 gives 1665.6152 topocentric and 1665.6046 rest for its feature. The 12 kHz difference between the two rest values is not reconciled here; the window name (`control-17000Hz`) is an offset from the report's own coordinate. Recorded as found.
- The next requirement it states (true lag context before the median cascade, negative lags by conjugate symmetry, freeze, recalibrate, then nominate) cannot be replayed here without its code and inputs.
