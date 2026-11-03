# The 13 comet-frame candidates, GBT 1667 MHz OH channel, 3I/ATLAS, 2025-12-18 UT

Data: Breakthrough Listen, Green Bank, blc23 rawspec `.0000.h5`, L-band cadence scans 0013–0018 (ON 0013/0015/0017 on 3I/ATLAS, OFF 0014/0016/0018), coarse channel 7 (1665.53–1668.46 MHz; 1,048,576 fine channels of 2.794 Hz; 49 steps of 6.08 s). Files at https://bldata.berkeley.edu/ATLAS/GB_ATLAS/.

Files:
- `oh13_candidates.csv`: one row per candidate per scan (78 rows).
- `oh13_candidates.json`: the same, nested, with the method and the result context.
- `code/`: the scripts that produced them.

Per scan, each candidate carries: file and URL; MJD start and mid; pointing RA (hours) and Dec (degrees) from the file header; the comet's JPL Horizons RA/Dec (degrees) and range-rate at mid-scan; the topocentric frequency and the fine-channel index (within the coarse channel, and in the whole file) at the first and last time step, i.e. the tracked path; and the tracked z in that scan.

## Selection (code/cometframe_raw.py, code/oh_scan.py)

1. `fetch_cc.py` reads one coarse channel from the remote file by HTTP range reads.
2. Each scan: each fine channel divided by its median over time, minus 1; a 3-channel boxcar; each time step rolled along the path a tone fixed in the comet's rest frame would take (JPL Horizons range-rate for C/2025 N1 at the GBT site), and summed; robust z (median, 1.4826 × MAD); the coarse channel's DC bins zeroed.
3. Scans aligned on the comet rest frame, f_rest = f_topo / (1 − deldot/c).
4. Kept: z ≥ 2.5 in all three ON scans and z < 2.0 in all three OFF scans at the same rest frequency, with ±1 channel tolerance.
5. Rows within 10 Hz merged: 13 clusters.

## Context

- At this cut the comet frame gives 13 clusters against 3.75 ± 2.05 (maximum 8) for 40 false-drift frames.
- At 2.0σ/1.5σ there is no excess (118 against 120.9 ± 12.5); at 3σ, 1.
- In the 1665 MHz OH channel (coarse channel 8) the comet frame gives 5 against 5.7 ± 2.2.
- C01 and C02 cross a fixed topocentric tone at 1665.615127 MHz present in all six scans, ON and OFF (code/spike.py): interference.
- Per step, the candidates average about 0.35σ, with no shared time pattern and no periodicity beyond a shuffle null (code/read_time.py); their rest frequencies show no spacing, mirror or whole-kHz structure beyond random sets (code/structure.py).
