# GBT 3I/ATLAS: first mining pass through the newly available raw voltages

Lee Sharks research session · 16 November 2026 · completed bounded pass

**The raw voltages are accessible, match the original six scans, and already answer an important part of the pointing question.** ON17's initial discrepant header changes to `TRACK` about 1.61 seconds into the recording. All thirteen later file-boundary headers place it close to the comet. This supports the notebook's return-slew explanation and removes the first-file header as a sound basis for treating the entire scan as off target. The thirteen weak spectral features remain unresolved.

## What was checked

I read Nobel Glas and Orin Trace's *What the Filters Kept*, Alexanarch #1742 v1.2, and Lee Sharks's *A Firm No*, #1743 v1.1, and restored the latest private research checkpoint, which includes the 8 November high-time, S-band and shared-power tests. Those later results are preserved. No email was sent and no public deposit was made.

Sources:

- [New raw-data directory](https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/)
- [What the Filters Kept, #1742](https://www.alexanarch.org/s/records/1742/)
- [A Firm No, #1743](https://www.alexanarch.org/s/records/1743/)
- [Official rawspec implementation](https://github.com/UCBerkeleySETI/rawspec), particularly `rawspec.c`, `rawspec_rawutils.c` and `rawspec_gpu.cu`.
- [Official blimpy GUPPI reader](https://github.com/UCBerkeleySETI/blimpy/blob/master/blimpy/guppi.py).

The public directory lists 84 files: fourteen per scan, for scans 0013–0018 on MJD 61027, 18 December 2025 UTC. Exact HTTP byte counts sum to **1,349,765,554,176 bytes**, about 1.35 decimal TB. Each scan has 1,676 blocks and 299.931883 seconds of voltage samples. The node covers 187.5 MHz; coarse channel 7 is the original 2.93-MHz interval containing the thirteen features. File modification dates were not used as observation times.

These are 8-bit samples of two complex receiver polarizations. The on-disk `NPOL=4` counts four real-valued components; the official reader and rawspec code confirm two complex polarizations. The channel sample interval is about 0.341333 microseconds. The stored components retain phase information unavailable in the previously analyzed total-power products.

## New finding: the ON17 pointing record updates

The former fine-product header contained one initial position, about sixteen arcminutes from the comet. The raw files carry updating headers.

| Raw position in ON17 | Elapsed time | Recorded state | Position |
|---|---:|---|---|
| Blocks 0–8 | 0–1.43 s | UNKNOWN | Initial discrepant position, RA 162.993°, Dec 6.7017° |
| Block 9 | 1.61 s | TRACK | RA 162.727°, Dec 6.6894°, near the comet |
| First block of file 0001 | 22.91 s | TRACK | About 0.015 arcmin from interpolated comet position |
| First blocks of files 0001–0013 | 22.91–297.78 s | TRACK throughout | All within about 0.040 arcmin of interpolated comet position |

Positions were compared with interpolation/extrapolation of the six saved ICRF comet coordinates in the original candidate table. This is an approximate positional diagnostic, not new astrometry or a calibrated pointing-error bound. Header fields have finite precision, update cadence and possible latency. The 1.61-second value is the first observed header-state change, not a metrologically exact settling time.

**Interpretive consequence:** the raw record now directly supports on-target tracking after the initial snapshot. The initial 16-arcminute discrepancy should no longer be carried as evidence of sustained mispointing. Independent antenna telemetry is still not supplied; a source identification does not follow from the updated headers. This agrees with, and materially strengthens, the notebook's earlier inference from the night's header pattern and hydrogen profiles.

![Updating pointing headers](sandbox:/workspace/scratch/9f78dcee6678/atlas-raw-20261116/deliverables/GBT-ON17-updating-pointing-headers.png)

## Voltage extraction and decoder validation

Before decoding the selected voltages, the first-pass plan was saved. It fixed three windows per scan, at raw blocks 0–33, 816–849 and 1632–1665: the start, middle and end. They correspond to fine-product rows 0, 24 and 48 once packet continuity is checked.

Each window contains seventeen 1,048,576-point FFTs, or 6.084537 seconds. The selected channel supplies **1,283,457,024 voltage bytes**, 18.253611 seconds per scan—about **6.1% of each scan in one coarse channel**. This is a completed bounded pass, not an examination of all 1.35 TB.

The decoder reproduces the original scan-0013 fine spectrum for all three selected rows. Across 3,145,728 bins, the largest relative discrepancy is **1.358 × 10⁻⁶**, about 1.36 parts per million; row correlations exceed 0.9999999999998. No frequency offset or amplitude fit is used for that final check.

One implementation detail mattered. rawspec loads signed 8-bit samples using CUDA normalized-float textures, corresponding to `max(value/127, -1)`. Simply FFTing the integer values gives an almost exact-looking spectrum but leaves a small frequency-dependent difference. Matching the documented conversion removes it. The initial integer-input diagnostic is retained beside the corrected validation; neither was a source finding.

Further checks: twelve independently summed selected-bin DFT comparisons; direct scalar byte decoding; Parseval energy checks in all eighteen windows with maximum relative difference about 1.014 × 10⁻⁷; exact histogram sample counts; HTTP 206 range/length checks; hashes for all retained voltage and header excerpts. The sampled packet indices are contiguous. All 84 file sizes divide exactly into their block geometry, and the first packet indices at file boundaries progress as expected.

The 612 selected block headers report `NDROP=0` and `DROPBLK=0`. These checks do not audit every unselected block, and lifetime counters such as `DROPTOT` are not interpreted as percentages of this scan lost.

## What the first voltage samples show

**The known receiver-frame complex near 1665.615 MHz appears in both ON and OFF scans.** Separate polarization spectra now show that the strongest bin of this complex is dominated by receiver X: about 77–93% of its total power in the three-window sums. The peak is about 2.25–11.15 times its local total-power median across the six scans. These are uncalibrated receiver-basis measurements; they do not establish sky polarization or identify an emitter. The peak is selected within the known complex for description, not as a new candidate search.

![Known complex in separate receiver polarizations](sandbox:/workspace/scratch/9f78dcee6678/atlas-raw-20261116/deliverables/GBT-voltage-known-line-polarizations.png)

**C03 does not become an independently resolved signal in these short samples.** Its eighteen fixed three-bin measurements fall between about −1.65 and +0.86 local robust control units. These are descriptive, per-window measurements, with no per-scan frequency maximization. They are not the inherited full-scan detector scores. Sampling only 6.1% of the available time cannot adjudicate the prior faint full-cadence feature. The accompanying CSV records all thirteen coordinates for all eighteen windows, including separate X/Y powers and the number of valid local controls. Edge-of-band controls are omitted when their reference support would leave the coarse channel.

**Fast-power and quantization diagnostics are now available.** The approximately 1-ms coarse-band power samples span 0.918–1.054 times their individual window medians. Component endpoint occupancies span about 0.0018–0.0320%; full histograms and moments are retained. These are descriptive diagnostics, not calibrated burst exclusions. The previously found OFF14 dip at about 164.39 seconds lies outside these windows and was not retested.

Every inventoried first-file header and every selected block header records `CAL_MODE=OFF`, `CAL_FREQ=0`. This bears on the recorded calibration state but does not establish the physical cause of the previously observed approximately 11.11-Hz common component. It should not be labelled a noise-diode signal merely from its frequency.

## What changes, and what remains open

| Question | Status after this pass |
|---|---|
| Were these particular raw voltages retained and made accessible? | Yes; inventory and selected payloads verified. |
| Are they the original six observations? | Yes; scan IDs, clocks, geometry and spectral reconstruction agree. |
| Does the initial ON17 header describe its whole scan? | No; later raw headers update to near-comet TRACK positions. |
| Can polarization and phase-preserving analyses now be attempted? | Yes; two complex voltage streams are accessible. |
| Are the thirteen a confirmed source, or newly refuted? | Neither; this sparse first pass does not decide their origin. |
| Is this an independent epoch or telescope replication? | No; these are the original observations at an earlier processing stage. |

The next useful science pass is the full-cadence extraction of coarse channel 7, with the candidate coordinates fixed and a declared comparison among comet-tracked, receiver-fixed and nearby control paths. A phase-sensitive search must state the additional phase, drift and clock freedoms and account for its trials. Raw voltages make such tests possible; they do not supply signal strength or a known waveform. About 21.09 GB of channel-7 payload would cover all six scans, rather than downloading the full node. The saved acquisition code already supports verified range reads; expanding the scientific search requires an explicitly amended plan.

All prior thirteen-feature, sensitivity, normalization and follow-up findings remain distinguishable from this pass. The principal new result is that the raw pointing-status record supports ON17 being on target after its initial snapshot.

## Saved material

Six per-scan archives retain the selected native voltage bytes, corresponding headers, source byte ranges and SHA-256 manifests. The compact evidence archive contains the inventory, official source-code snapshots, original candidate coordinates and ephemeris, the independent native three-row reference, scripts, numerical checks, diagnostic summaries and recovery instructions. Full polarization spectra can be regenerated offline from the saved excerpts. The shared resume document is updated with the completed stage and exact saved identities.