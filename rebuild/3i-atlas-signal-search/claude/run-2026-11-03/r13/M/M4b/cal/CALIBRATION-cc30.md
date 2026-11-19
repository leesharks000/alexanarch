# M4b calibration, round 1: cc30 (2026-11-19)

Channel cc30 (centre 1599.609375 MHz) lies wholly inside the GLONASS L1 band and holds the two carriers M4 nominated (1599.962 and 1600.310 MHz). It is the hardest channel for a drift search, and so a first calibration, not the last.

## What was run

`mvb.py 30 SCAN M4b/cal/{on,off}/inj.json` for the six scans; products in out3/cc30_SCANinj.npz (hashes to follow with M4b-PRODUCTS).
- **ON scans (0013, 0015, 0017):** 14 synthetic linear chirps added to both feeds before the FFT. Rates 0, ±0.1, ±0.3, ±1, ±2, ±4, ±6 Hz/s, at r = 0.2 and 0.8 (tone power over the bin's mean noise power, per frame). Each chirp restarts at its start frequency in each scan.
- **All six scans:** two persistent tones (0 and 0.05 Hz/s, r = 0.8) continuing in absolute time across the scans.

`mdhits.py 30 inj` gives `cc30-inj-events.json`; `cal_look.py` gives `cc30-injection-recovery.txt`, the local statistic at every injected track, per scan.

## The finding that changed mdhits

With z scaled by one MAD across the whole coarse channel, the GLONASS broadband occupancy produced about 10⁵ cells with z ≥ 10 per scan at 2.79 Hz resolution. These were concentrated in the occupied part of the band and favoured the extreme drifts (±62–63). The hit statistic was therefore made **local**: each resolution's per-cell maximum over drifts is rescaled by the median and MAD of that maximum in blocks of 1024 cells. On the local statistic, ON hits fall to about 5,000 per scan at 2.79 Hz, 15–73 at 11.2 Hz and 6–25 at 44.7 Hz. The association step was vectorised (it had looped over every hit).

## Outcome (local statistic, Z_HIT 10, Z_VETO 5, K 0.5)

1. **Slow, strong tones are recovered.** Recovery for r = 0.8 by rate:

   | Rate | Recovery |
   |---|---|
   | 0 Hz/s | z 57–67 in all three ON scans; nothing in the OFF scans; class A |
   | ±0.1 Hz/s | z 18–38 |
   | ±0.3 Hz/s | z 17–23 |

   The drifting tones are class B because each restarts in each scan, so they do not lie on one track. That is an artefact of the injection design, not of the rule.
2. **Fast tones are not reliably recovered in this channel.** At r = 0.8: −1 Hz/s gives z 4–12; +2 Hz/s gives 2–10; ±4 and ±6 Hz/s give ≤ 6.
3. **Weak tones are not recovered.** At r = 0.2, none rose above the background at any rate.
4. **The veto holds.** Both persistent tones are present along their tracks in the OFF scans and are vetoed. Both GLONASS carriers are present in every scan, at local z 18–302, and are vetoed. No GLONASS event survives.
5. **The control rate is high in this channel.** Real-scan events: A 3, B 32; the A events are the r = 0.8, 0 Hz/s injection, seen once from each ON scan. Role-exchanged control: A 1, B 270. The control's strongest events are an intermittent emitter near 1600.992 MHz. It is present in some scans and absent along the track in others, so it passes the veto where it is absent. One appears as class A in the control (OFF 0018, −1.66 Hz/s).

## What this settles and what it leaves

- Class A works as designed: an injected source present on-comet in all three ON scans and absent off-comet is found at high z, and persistent sources and GLONASS are rejected.
- Class B is background-limited in a channel like cc30. Its count has to be read against the channel's control. The 1600.992 MHz emitter shows how an intermittent source passes.
- Sensitivity at drifts of 1 Hz/s and above is poor in this channel. Whether that is the channel's background or the method's loss at drift is not decided by this round.

## Before freezing

A second round on a quiet channel, with the injections continuous in absolute time across the ON scans, so that drifting injections are tested for class A. Rates 0.05–4 Hz/s at r = 0.4, 0.8 and 1.6. This would give the sensitivity curve, and with it Z_HIT and Z_VETO for the plan.
