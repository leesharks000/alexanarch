# The raw voltages: GBT 3I/ATLAS, 2025-12-18, L band, scans 0013–0018, blc23

**Source.** Breakthrough Listen raw voltages (GUPPI RAW), whole node blc23, the six cadence scans 0013–0018 (ON 0013/0015/0017 on 3I/ATLAS, OFF 0014/0016/0018), about 1.3 TB. They were made public at https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/ by Matt Lebofsky on 2026-11-17 (00:36 UTC), at Lee Sharks's request of 2026-11-08 to 11-10. Only coarse channels 7 (1665.53–1668.46 MHz, the 1667 OH line) and 8 (1662.60–1665.53 MHz, the 1665 OH line) were read. Each 128 MiB block contributed only its 2 MiB slice for the channel, by HTTP range read. Nothing was downloaded whole. The SHA-256 of the channel bytes read for each scan is in `out/meta_*.json`.

**Header.** BLOCSIZE 134217728; OBSNCHAN 64; NBITS 8; NPOL 4 (X, Y complex); TBIN 0.3413 µs; OBSFREQ 1595.2148 MHz; OBSBW −187.5 MHz; CHAN_BW −2.9297 MHz; 128 blocks per 16 GiB file; 14 files and 1,676 blocks (299.9 s) per scan.

**Frequency mapping, checked.** Sky frequency = fc + sign(CHAN_BW) × baseband. The fixed interference tone that the public products put at 1665.615127 MHz is found in the voltages at 1665.615119 MHz, within one 5.59 Hz bin.

## Code
- `voltreduce.py SCAN CH`: channelizes into 2^19-point spectra (5.59 Hz × 0.179 s) of both polarizations. It keeps the scan-integrated full Stokes spectrum (`integ_*`). For channel 7 it also keeps the full-time-resolution full-Stokes window (±32 bins) along the comet-frame path of each of the 13 candidates of `../oh13` (`cand_*`).
- `analyze_cand.py`: tracked-path power, Stokes and periodicity per candidate per scan.
- `contrast_null.py`: ON−OFF contrast along each candidate's path against 48 parallel paths in the same windows.
- `blind_pol.py CH`: the whole coarse channel, integrated: bins whose power or fractional V, Q or U depart from the channel's own distribution (|z| ≥ 6), with ON/OFF persistence.
- `fixedlines.py`: fixed-frequency bands across the six scans, against 3,000 reference windows.
- `zoom.py`: full-Stokes waterfalls of chosen ranges.
- `track1663.py`: the 1663.3–1663.5 MHz feature, per 30 s.
- Stokes convention: I = XX+YY, Q = XX−YY, U = 2Re(XY*), V = −2Im(XY*). No calibrator solution is applied (Croft, 2026-11-09), so the polarization fractions are instrumental, uncalibrated values. They are comparable within the data, not across instruments.

## Findings

**1. The 13 candidates.**
- C02 recovers as the fixed interference tone, strongly linearly polarized (Q +11.8σ in 0013).
- ON−OFF contrast against parallel paths: C03 (1665.6338 MHz) z = 2.84, with 0 of 48 parallel paths as high. The other ten run from −1.4 to +1.6. The combined score over C03–C13 is +2.78. This is not independent of the selection: the voltages are the bytes the public products were made from, so a weak recovery is expected.
- What the voltages add is new: full polarization and 0.18 s resolution. No candidate shows circular or linear polarization above about 2.5σ, a spectrum-level transient, or a periodicity. C03 is flat across each third of every scan, with V/I within ±0.02.

**2. Channel 7, blind.**
- A linearly polarized fixed tone at 1665.75011 MHz is present in all six scans (interference).
- A fixed pair at 1666.0045 and 1666.0091 MHz (4.6 kHz apart) is left-circular (V −5 to −17σ) and negative-Q. It is present in all six scans at a topocentric frequency stable to about 15 Hz. A comet-frame source would drift about 185 Hz across the session. Its scan-to-scan level follows the known tones: strongest in 0013, a sharp drop in 0014, then intermediate. This is interference of a family not reported before, with no comb members at ±4.6 kHz.

**3. Channel 8, blind: a strong drifting transmitter.**
- It runs from 1663.31 MHz at the start of 0013 to 1663.42 MHz at the end of 0017, at z of 9 to 214 per 30 s, rising at about 30 to 110 Hz/s. In 0018 it turns back down at about 265 Hz/s, to 1663.34 MHz by the scan's end.
- It is several kHz wide, with polarization varying between circular and linear.
- It is continuous across every ON/OFF boundary. At the end of 0013 it sits at 1663.3247 and at the start of 0014 at 1663.3236; at the end of 0016, 1663.3955, and at the start of 0017, 1663.3987; at the end of 0017, 1663.4186, and at the start of 0018, 1663.4098.
- Continuous in time regardless of pointing, it is a transmitter in the sidelobes, not a source in the beam.
- A linear fixed tone at 1665.3451 MHz is also interference.

**4. Bottom line.** In the two OH coarse channels, with full polarization and 0.18 s resolution, nothing separates from interference or from the statistics of the selection.
- Every strong feature found is either fixed in topocentric frequency or continuous through the OFF scans.
- The comet-frame candidates show no polarization or time structure.
- C03 alone keeps a weak ON excess, and that excess is not independent evidence.

## Limits
- One node (blc23) of the GBT session, two coarse channels, one resolution (5.59 Hz) for the candidate tracking.
- The public selection was at 2.79 Hz. A 2^20 rerun at that resolution is the next check for C03.
- No calibrator solution has been applied.
- The disclosure order stands: hashed and published here before anything is sent to Breakthrough Listen.

**What is committed.** The code, this note, the JSON results and the logs are committed. The reduced arrays (`out/*.npz`, 326 MB) are hashed in `SHA256SUMS-out.txt` but not committed, because the session cannot carry them. They are re-derivable from the public voltages with the code here, and the channel-byte hashes in `out/meta_*.json` fix what was read.

`out/DELETED-for-disk.sha256` records two earlier working parquet files deleted to free disk for this run. Both are re-derivable from the public hit lists.
