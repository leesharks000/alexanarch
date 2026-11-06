# The Ka-band deep-space allocation (31.8–32.3 GHz): coverage check, 2026-11-06

Not a search: a check of whether any public 3I/ATLAS data reach the band. None do.

- Green Bank (bldata.berkeley.edu/ATLAS/GB_ATLAS/): four cadences of 2025-12-18 only (scans 0013–0018, 0029–0034, 0045–0050, 0061–0066). The X-band cadence's 31 nodes, read from the header of each node's scan-0061 rawspec.0000 file by hdr.py, span 7688.965–12376.465 MHz (spans.txt).
- Parkes (PKS_Jul_31_2025, and the September and October sessions, 403 below their roots): the UWL receiver, which ends below 4.1 GHz.
- MeerKAT (hit lists only): UHF, L and S receivers, below 3.6 GHz.
- ATA (two open sessions, 2025-07-03 and 2025-07-08): feeds that end near 11 GHz.

The deep-space downlink allocations reachable in public data are S (2290–2300 MHz, inside the Parkes full-band search of July) and X (8400–8450 MHz, dsn/). Ka is out of reach until data at 32 GHz are published.
