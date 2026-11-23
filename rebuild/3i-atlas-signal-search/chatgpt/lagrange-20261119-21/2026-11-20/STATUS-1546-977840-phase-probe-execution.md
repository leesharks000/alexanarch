# 1546.977840 MHz phase-memory probe: execution checkpoint (2026-11-20)

The user requested execution of the frozen line-centered probe in `PLAN-1546-977840-line-phase-injection-validated.md`.

## Actually executed in this session

Original executable extracted from the conversation file `GBT-1546-977840-phase-memory-probe.zip` (contains `line_phase_probe.py`; 5,881 bytes). Re-ran `OPENBLAS_NUM_THREADS=1 python line_phase_probe.py --self-test` in Python/NumPy/SciPy. Both tests passed, reproducing:
- injected amplitude=0.65 noise RMS, pre-whitening repeated QPSK period=256 → winning lag **256**, empirical family p=**0.025**, max ratio **1.3329779662740575**;
- matched noise only → winning lag **512**, family p=**0.625**, max ratio **1.110192592227311**.
- Frequency crop sanity check: FC=1546.875 MHz, F0=1546.9778403639793 MHz, FFT center bin 487480, 8192-bin range [483384,491576), df=2.793967723846438 Hz.

## Raw voltage acquisition attempted and failed

Attempted Python `urllib.request.urlopen` on the known canonical ON0017 public recording URL:

`https://bldata.berkeley.edu/ATLAS/GB_ATLAS_raw/blc23_guppi_61027_18497_DIAG_3I_ATLAS_0017.0000.raw`

Request made with HTTP Range bytes=0-127 to verify connectivity before a large transfer. Returned:

`URLError(gaierror(-3, 'Temporary failure in name resolution'))`.

No raw-voltage payload exists in the runtime's 18 MB local working set, and the public data had not been obtained in this session. Consequently **no telescope-data detections, OFF-control tests, or line-specific confirmation tests were executed**. No technical result about an extraterrestrial emitter may be inferred from this checkpoint.

## Ready-to-execute in a networked worker

Copy `line_phase_probe.py` from the conversation ZIP to a directory with an available `dm.py` checkout:

```bash
python line_phase_probe.py --self-test
python line_phase_probe.py --dm /path/to/alexanarch/rebuild/3i-atlas-signal-search/claude/voltages/delaymod --frames 16 --surrogates 39 --scan all > gbt_1546_phase_run.log
```

The implementation writes `line_phase_results.json`. Run in a working directory where this script has write permission. The 16-frame pilot is not comprehensive and may miss the original ON0017 burst; a full-duration ON0017 or burst-timestamp-localized run is required to judge that feature. An independent channel-48 survey already documented the unresolved line's signal power at the original frequency.

Do not label this checkpoint a voltage run. It is a successful synthetic self-test and failed external fetch.
