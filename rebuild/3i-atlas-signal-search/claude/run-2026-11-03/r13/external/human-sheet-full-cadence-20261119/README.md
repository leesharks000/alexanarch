# External: The Human on the Sheet, the retained complex over time (received 2026-11-19 13:46 EST)

Two files, verbatim as received from the operator: `REPORT.md` (the full-cadence follow-up to `../human-sheet-20261119/`) and `aligned-comb.png` (its carrier-aligned display, attached separately). The producing agent is not named. Its evidence bundle (the "prior 42 MB full-cadence bundle", with the C01 voltages for all six scans) was not received. Working research and literary material, not a deposit.

## What it reports

1. The 1665.615 MHz complex stays visible through the analysed 297.8 s of all six scans, ON and OFF, in all 618 overlapping windows above a descriptive cut.
2. The carrier wanders slowly, with slopes from −0.036 to +0.046 Hz/s. Against one free offset, the residual is 4.24 Hz around a constant frequency and 65.78 Hz around the comet-shaped path.
3. It has companion lines at about ±60, ±120 and ±180 Hz, with offsets −180.04, −119.97, −60.07, +60.07, +119.97 and +180.04 Hz, passing in 43–344 of 618 windows.
4. The envelope (|V|²) shows no clean 60 Hz separation from the comparison frequencies, so mains coupling and simple AM are not established. Origin is unresolved; receiver-chain or site diagnostics are named as what would decide it.

## Checked here

- Comet slopes: recomputed from dm.py's ephemeris at each scan's mid-point as −f·dv/dt/c at 1665.615 MHz. Scans 0013–0018 give −0.1093, −0.1129, −0.1161, −0.1193, −0.1231 and −0.1263 Hz/s, against the report's −0.1093, −0.1127, −0.1161, −0.1195, −0.1229 and −0.1263. They agree to within 0.0002 Hz/s.
- Window arithmetic: the bin is 91552.734375/524288 = 0.174623 Hz, the window 5.726623 s, and (297.784399 − 5.7266)/2.8633 + 1 = 103 windows per scan. All as stated.
- The prior "four peaks at about 60.35 Hz spacing" is #1742's text, as the report says. The report corrects it toward 60.07 Hz offsets.
- Not checked: the PSD levels, the comb pass counts and the envelope figures. They need the bundle.
