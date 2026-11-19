# M4b calibration, round 2: cc08 (2026-11-19)

Channel cc08 (centre 1664.062500 MHz) lies inside the protected radio-astronomy band. It was chosen as a quiet channel. M4 nominated one hit here (closed).

## What was run

`mvb.py 8 SCAN M4b/cal2/{on,off}/inj.json`; products out3/cc08_SCANinj.npz.
- **ON scans:** 15 synthetic linear chirps, continuous in absolute time from scan 0013's start, so that each lies on one track across the three ON scans. Rates −0.05, +0.3, −1, +2 and −4 Hz/s (sky), at r = 0.4, 0.8 and 1.6.
- **OFF scans:** none.

`mdhits.py 8 inj` gives `cc08-inj-events.json`; the per-injection recovery is in `cc08-injection-recovery.txt`.

## Outcome (local statistic, Z_HIT 10, Z_VETO 5, K 0.5)

Class by injection (A = found in all three ON scans along one track, absent from all OFF scans):

| rate (Hz/s) | r = 0.4 | r = 0.8 | r = 1.6 |
|---|---|---|---|
| −0.05 | A (z 24–35) | A (38–47) | A (80–93) |
| +0.3 | A (14–19) | A (35–37) | A (69–72) |
| −1 | — (z ~6) | A (18–21) | A (20–40) |
| +2 | — | B in two scans (10–12) | A (21–23) |
| −4 | — | — (6–10) | A (20–23) |

- **False events.** In the role-exchanged control: class A 0, class B 6. One non-injected class-A event at first: a coarse-resolution ghost 4.6 kHz from the strong −1 Hz/s injection, at a wrong drift. The merge rule was revised to absorb ghosts. A weaker event whose start lies inside a stronger event's swept band in the same scan is that event's ghost. After the revision: real A 30 (the ten detected injections × three scans), B 20; control A 0, B 6.
- **cc30 re-read with the revised merge.** A 3, B 32; control A 1, B 262 (round 1 gave 3/32 and 1/270).

## What it fixes

- **Sensitivity (class A).** Down to r = 0.4 at |rate| ≤ 0.3 Hz/s; r = 0.8 to 1 Hz/s; r = 1.6 to 4 Hz/s. r is the tone's power over its bin's mean noise power per 0.36 s frame. Losses at higher drift follow the coarser resolutions' √L.
- **Thresholds kept:** Z_HIT 10, Z_VETO 5, K 0.5. On the quiet channel they give no false class-A events and recover every injection the resolution allows. In the GLONASS channel the false class-A rate is 1 per channel.
- cc30's poorer recovery at drift (round 1) is the channel's background, not the method.
