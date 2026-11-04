# RESULTS-shape (plan shape/PLAN-shape.md, sha256 776fa6aa...)

Injection (Parkes 2380, comet frame, scan 0, samples 4-14): D-shaped doublet recovered at stat 7.55 (+3 kHz, window 4); O-shaped tone at 7.10 (+5 kHz, window 4). Both in the comet frame only.

Deviation, recorded 2026-11-04: the first run's persistent-event count included groups formed by the +-2 channel dilation whose >= 4 channels were vetoed or outside the window (seen in Parkes 1420 bary/O, a reported group with on-source maxima 0.87, 0.72, 1.56). Counting corrected in shape.py (a group counts only if two on-source scans reach >= 4 at an unvetoed in-window channel within the group +-2); Parkes rerun as *_v2.json; GBT rerun in progress. First-run outputs kept.

Parkes, corrected counting (target / swap / frequency-control maximum / spacing controls):
- 2380: topo O 2/5/124; topo D 9/8/130 [3,6]; comet O 0/1/79; comet D 3/2/108 [1,0]; bary O 0/0/103; bary D 0/2/179 [1,1]. No lead. The controls at 2370-2390 MHz are much busier than 2380 itself.
- 1420.405752: topo O 5/5/8; topo D 8/5/16 [8,10]; comet O 0/1/2; comet D 3/3/4 [1,2]; bary O 3/1/2 LEAD; bary D 5/1/6 [5,4].

GBT, first-run counting: no lead in any of the 12 cells (2380: every cell's target at or below its control maximum; 1420: same).

The one lead: Parkes 1420 MHz, barycentric frame, single-tone template. Its three events: scan 0 window 0 at -11,868 Hz grid offset (stat 5.37); scan 0 window 6 at +2,710 Hz (5.03); a persistent group at +3,906 Hz with scans 2 and 4 at 4.02 and 4.01 (scan 0 at 0.87). Every one sits at its threshold. Against 2 in the busiest control and 1 in the swap. With 24 cells, each target exchangeable with its ten controls, a target strictly above all ten occurs by chance in about 1 cell in 11, about 2 of 24 expected. One lead is what noise gives. Not a candidate; recorded as the rule's output.
