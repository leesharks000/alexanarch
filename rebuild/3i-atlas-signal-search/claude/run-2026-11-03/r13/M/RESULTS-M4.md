# RESULTS-M4: stages 2 and 3 over the full band

Written 2026-11-20, when the band was complete. Plan: PLAN-M4.md (frozen 2026-11-18; the code of PLAN-M2 and PLAN-M3 unchanged). M2/M3 hold cc00, cc26, cc40 and cc63; M4 covers the other 60 channels. Stack hashes in M4-PRODUCTS.sha256 (stacks deleted, as planned). Hits per channel in M4/ccNN.json.

## The count

1. 59 nominations in 16 of the 60 channels, by the plan's rule (W1 above 1.5× the largest of nine references, or the suppressed-carrier flag). Per channel below, as logged by mvolt.py.
2. Of the nominations examined: cc03's twelve are radiosonde telemetry at 1679.70–1679.98 MHz, present in the OFF scans; cc08's one is a single-scan lead at 1663.3270 MHz, in ON0013 only (both in M4/NOTES-NOMINATIONS.md). PLAN-M4b (19 November, at cc34) records every nomination to that point as a drifting emitter passing the bin-by-bin veto, or closed (cc03; cc30, GLONASS L1). The nominations from cc37 on (cc37, cc39, cc43, cc45, cc46, cc49, cc50, cc51, cc55: 24 in all) were logged and not examined.
3. M4's veto compares OFF scans bin by bin in the comet frame, so a drifting emitter passes it. That blind spot is why the drift search (M4b, RESULTS-M4b.md) was added at the boundary; M4b finds no class-A excess over its control outside the allocated bands.

## What was lost

4. The voltage-battery files (volt/ccNN.json), which hold each nomination's scan, frequency and clearing ratio, were to be hashed at the end of the run and were not committed as the run went. A container restart on 2026-11-20 took them, except cc59, cc61 and cc62, which are committed with this file (VOLT.sha256). The counts survive in m4.log and m4b.log; the details survive for cc03 and cc08 in the notes. The details of cc14 (16), cc15 (1), cc19 (1), cc30 (1), cc32 (3), cc37 (1), cc39 (1), cc43 (2), cc45 (3), cc46 (2), cc49 (6), cc50 (3), cc51 (2), cc55 (4) are lost. They can be recovered only by rerunning those channels' stacks from the network (mv.py, then mvolt.py, about an hour per channel); the frozen code would give the same files.

## Channels

| Channel | Centre (MHz) | Nominations |
|---|---:|---:|
| cc01 | 1684.5703 | 0 |
| cc02 | 1681.6406 | 0 |
| cc03 | 1678.7109 | 12 |
| cc04 | 1675.7812 | 0 |
| cc05 | 1672.8516 | 0 |
| cc06 | 1669.9219 | 0 |
| cc07 | 1666.9922 | 0 |
| cc08 | 1664.0625 | 1 |
| cc09 | 1661.1328 | 0 |
| cc10 | 1658.2031 | 0 |
| cc11 | 1655.2734 | 0 |
| cc12 | 1652.3438 | 0 |
| cc13 | 1649.4141 | 0 |
| cc14 | 1646.4844 | 16 |
| cc15 | 1643.5547 | 1 |
| cc16 | 1640.6250 | 0 |
| cc17 | 1637.6953 | 0 |
| cc18 | 1634.7656 | 0 |
| cc19 | 1631.8359 | 1 |
| cc20 | 1628.9062 | 0 |
| cc21 | 1625.9766 | 0 |
| cc22 | 1623.0469 | 0 |
| cc23 | 1620.1172 | 0 |
| cc24 | 1617.1875 | 0 |
| cc25 | 1614.2578 | 0 |
| cc27 | 1608.3984 | 0 |
| cc28 | 1605.4688 | 0 |
| cc29 | 1602.5391 | 0 |
| cc30 | 1599.6094 | 1 |
| cc31 | 1596.6797 | 0 |
| cc32 | 1593.7500 | 3 |
| cc33 | 1590.8203 | 0 |
| cc34 | 1587.8906 | 0 |
| cc35 | 1584.9609 | 0 |
| cc36 | 1582.0312 | 0 |
| cc37 | 1579.1016 | 1 |
| cc38 | 1576.1719 | 0 |
| cc39 | 1573.2422 | 1 |
| cc41 | 1567.3828 | 0 |
| cc42 | 1564.4531 | 0 |
| cc43 | 1561.5234 | 2 |
| cc44 | 1558.5938 | 0 |
| cc45 | 1555.6641 | 3 |
| cc46 | 1552.7344 | 2 |
| cc47 | 1549.8047 | 0 |
| cc48 | 1546.8750 | 0 |
| cc49 | 1543.9453 | 6 |
| cc50 | 1541.0156 | 3 |
| cc51 | 1538.0859 | 2 |
| cc52 | 1535.1562 | 0 |
| cc53 | 1532.2266 | 0 |
| cc54 | 1529.2969 | 0 |
| cc55 | 1526.3672 | 4 |
| cc56 | 1523.4375 | 0 |
| cc57 | 1520.5078 | 0 |
| cc58 | 1517.5781 | 0 |
| cc59 | 1514.6484 | 0 |
| cc60 | 1511.7188 | 0 |
| cc61 | 1508.7891 | 0 |
| cc62 | 1505.8594 | 0 |
