# RESULTS-M4b: the drift search over the full band

Written 2026-11-20, when the 64th channel finished. Plan: PLAN-M4b.md, frozen 2026-11-19 (hashes in PLAN-M4b.sha256), thresholds Z_HIT 10, Z_VETO 5, K 0.5, BLK 1024, unchanged. Events per channel in M4b/events/ccNN.json; stack hashes in M4b-PRODUCTS.sha256 (the stacks deleted, as planned).

## The count

1. All 64 coarse channels of blc23 (1500–1688 MHz topocentric), six scans each (ON 0013, 0015, 0017; OFF 0014, 0016, 0018), 18 December 2025, Green Bank.
2. Class A (present along one track in all three ON scans, absent from every OFF scan): **287** across the band. The role-exchanged control (OFF as ON): **506**. Class B: 6192 against 5917.
3. Pointing at the comet produced fewer class-A events than pointing away from it. Across the band, nothing in the ON scans exceeds what the OFF scans produce by the same rule.
4. Six channels have more class-A events than their control:

| Channel | Class A | Control A | Where the listed events lie | Drift of the listed events |
|---|---:|---:|---|---|
| cc01 | 2 | 0 | 1683.26–1685.07 MHz, scan 0017 only | 0 Hz/s |
| cc19 | 6 | 0 | 1631.75–1632.08 MHz, scans 0013 and 0017 | 0, −0.117, +0.058 Hz/s |
| cc21 | 19 | 8 | 1625.12–1625.29 MHz | −7.35 to +1.69 Hz/s |
| cc23 | 44 | 42 | (none among the listed events) | — |
| cc48 | 58 | 8 | 1545.48–1548.27 MHz, all three ON scans | 0, +0.015 Hz/s |
| cc50 | 34 | 3 | 1540.26–1540.28 MHz, scan 0013 | 0 Hz/s |

Each channel's file lists its 40 strongest events; the counts above are of all events.

## Reading

5. Every excess lies in an allocated band of our own transmissions. cc48 and cc50 are inside the 1525–1559 MHz mobile-satellite downlink (Inmarsat); cc19 inside the 1626.5–1660.5 MHz uplink of ground terminals to those satellites; cc21 and cc23 inside 1616–1626.5 MHz (Iridium), where the fast drifts are those of low-orbit satellites; cc01 inside 1675–1710 MHz, the meteorological-satellite downlink.
6. The listed events in cc01, cc19, cc48 and cc50 have zero or near-zero drift in the observatory's frame. A source moving with 3I/ATLAS would carry the comet's topocentric drift. A fixed or geostationary emitter does not.
7. In the OFF scans these events reach z of about 1–5 inside the window, below the veto (5) and not absent: the shape of a strong carrier entering the sidelobes as the telescope moves.
8. The excesses are read as terrestrial and orbital interference. That is the correct first reading. It is also the measured instance of the point recorded on #1789 (next-version note, 2026-11-20): what resembles our own transmission is set aside as ours, so in these bands the search could not have heard a sender whose emission looked like ours, whatever it sent.
9. No class-A event in the band carries a nonzero drift that matches the comet's own motion and stands outside the allocated bands.

## What was not done

10. The closer voltage look the plan prescribes for class-A leads was not run on these channels. The excesses' properties (band, zero drift, sidelobe presence) set where it would look first: per-scan time profiles of the cc19, cc48 and cc50 carriers against the satellite ephemerides.
11. A container restart on 2026-11-20 lost the products of cc59 and cc62 before they were committed; both were rerun from the network and gave the same counts.

## Channels

| Channel | Centre (MHz) | A | B | Control A | Control B |
|---|---:|---:|---:|---:|---:|
| cc00 | 1687.5000 | 0 | 12 | 0 | 11 |
| cc01 | 1684.5703 | 2 | 4 | 0 | 1 |
| cc02 | 1681.6406 | 0 | 0 | 0 | 6 |
| cc03 | 1678.7109 | 1 | 17 | 2 | 36 |
| cc04 | 1675.7812 | 0 | 0 | 0 | 8 |
| cc05 | 1672.8516 | 0 | 1 | 0 | 1 |
| cc06 | 1669.9219 | 0 | 0 | 0 | 0 |
| cc07 | 1666.9922 | 0 | 3 | 0 | 3 |
| cc08 | 1664.0625 | 0 | 19 | 0 | 6 |
| cc09 | 1661.1328 | 0 | 0 | 0 | 0 |
| cc10 | 1658.2031 | 0 | 0 | 0 | 2 |
| cc11 | 1655.2734 | 0 | 1 | 0 | 3 |
| cc12 | 1652.3438 | 0 | 0 | 0 | 0 |
| cc13 | 1649.4141 | 0 | 2 | 0 | 0 |
| cc14 | 1646.4844 | 0 | 24 | 0 | 12 |
| cc15 | 1643.5547 | 0 | 7 | 0 | 0 |
| cc16 | 1640.6250 | 0 | 0 | 0 | 0 |
| cc17 | 1637.6953 | 0 | 0 | 0 | 1 |
| cc18 | 1634.7656 | 0 | 2 | 0 | 10 |
| cc19 | 1631.8359 | 6 | 13 | 0 | 16 |
| cc20 | 1628.9062 | 0 | 0 | 0 | 20 |
| cc21 | 1625.9766 | 19 | 430 | 8 | 520 |
| cc22 | 1623.0469 | 25 | 757 | 31 | 927 |
| cc23 | 1620.1172 | 44 | 780 | 42 | 933 |
| cc24 | 1617.1875 | 1 | 358 | 7 | 472 |
| cc25 | 1614.2578 | 0 | 0 | 0 | 6 |
| cc26 | 1611.3281 | 0 | 0 | 0 | 8 |
| cc27 | 1608.3984 | 0 | 1 | 0 | 6 |
| cc28 | 1605.4688 | 0 | 2 | 0 | 13 |
| cc29 | 1602.5391 | 0 | 32 | 1 | 194 |
| cc30 | 1599.6094 | 0 | 25 | 1 | 260 |
| cc31 | 1596.6797 | 0 | 1 | 0 | 20 |
| cc32 | 1593.7500 | 0 | 0 | 0 | 4 |
| cc33 | 1590.8203 | 0 | 4 | 0 | 2 |
| cc34 | 1587.8906 | 0 | 2 | 0 | 0 |
| cc35 | 1584.9609 | 0 | 16 | 0 | 10 |
| cc36 | 1582.0312 | 0 | 27 | 1 | 9 |
| cc37 | 1579.1016 | 0 | 219 | 0 | 47 |
| cc38 | 1576.1719 | 0 | 286 | 1 | 76 |
| cc39 | 1573.2422 | 0 | 348 | 0 | 35 |
| cc40 | 1570.3125 | 0 | 88 | 1 | 21 |
| cc41 | 1567.3828 | 0 | 5 | 0 | 23 |
| cc42 | 1564.4531 | 0 | 2 | 0 | 9 |
| cc43 | 1561.5234 | 0 | 8 | 0 | 6 |
| cc44 | 1558.5938 | 12 | 294 | 15 | 350 |
| cc45 | 1555.6641 | 33 | 522 | 133 | 250 |
| cc46 | 1552.7344 | 12 | 216 | 28 | 78 |
| cc47 | 1549.8047 | 27 | 216 | 93 | 385 |
| cc48 | 1546.8750 | 58 | 158 | 8 | 263 |
| cc49 | 1543.9453 | 3 | 157 | 9 | 185 |
| cc50 | 1541.0156 | 34 | 565 | 3 | 81 |
| cc51 | 1538.0859 | 3 | 276 | 10 | 118 |
| cc52 | 1535.1562 | 3 | 53 | 66 | 337 |
| cc53 | 1532.2266 | 1 | 37 | 24 | 40 |
| cc54 | 1529.2969 | 0 | 159 | 12 | 33 |
| cc55 | 1526.3672 | 3 | 39 | 10 | 14 |
| cc56 | 1523.4375 | 0 | 0 | 0 | 9 |
| cc57 | 1520.5078 | 0 | 0 | 0 | 10 |
| cc58 | 1517.5781 | 0 | 0 | 0 | 6 |
| cc59 | 1514.6484 | 0 | 2 | 0 | 0 |
| cc60 | 1511.7188 | 0 | 1 | 0 | 15 |
| cc61 | 1508.7891 | 0 | 0 | 0 | 5 |
| cc62 | 1505.8594 | 0 | 1 | 0 | 0 |
| cc63 | 1502.9297 | 0 | 0 | 0 | 1 |
