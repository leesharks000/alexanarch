# N1625 translated-shape experiment — executed software controls; telescope data still blocked

2026-11-20. Original frozen plan: [PLAN-N1625-translated-shape-recurrence.md](PLAN-N1625-translated-shape-recurrence.md).

**Status: no GBT voltage inference made.** Direct HTTP Range access to the public Berkeley ON0013 file failed in ChatGPT's compute environment: `URLError: [Errno -3] Temporary failure in name resolution`. The independent collaborating networked worker has previously streamed this telescope data, but no N1625 raw-voltage result was in either repository at this checkpoint.

## Implemented experiment
- Real-data runner written and executed for synthetic controls as `n1625.py` in the user-visible conversation ZIP `N1625-translated-shape-experiment.zip` (includes script, `selftest.json`, full `RESULT-execution-checkpoint.md`). Run `python n1625.py --self-test`.
- For real data: uses `dm.frames` cc21, all 6 scans, both feeds, 32 frames per scan, 65,536 native-bin FFT window centered 1625.2936106175184 MHz; +25 kHz neighboring control; 1625.120423734188 MHz high-drift control.
- Searches four-occurrence spectrogram recurrence across time lags [4,16,64,256,1024], frequency-bin translations −8…+8, 512-point local spectra, with **max-min** cosine score. Uses 199 32-block-order surrogate permutations for full run, and records two half-window diagnostics, frequency-bin participation and strongest-bin ablation. Null addresses spectral temporal ordering, not sky origin. Default full run is compute intensive.
- Synthesized motif built in complex FFT segments, inverse FFT into a complex baseband waveform, then measured through the same spectrogram filter; this is **before spectrogram whitening** but not native telescope voltage injection.
- **Positive controls:** artificial 6-bin translated motif recovered with correct lag **16** and shift **+2** in two halves. Example injected scale 1.0 score **0.18056**, null median **0.07403**, pilot p **0.05** (19 surrogates). Recovery **20/20** seeded motifs at scale 1, **17/20** at scale 0.5.
- **Nulls:** noise-only example p **0.45**; **5/100** independent noise-only realizations pass p≤0.05, roughly nominal; simulated stationary lone tone p **0.60**, hopping lone tone p **0.15**. These confounders are illustrative, not a comprehensive terrestrial interference set.
- Strongest spectral-bin removal: injected score drops from **0.18056 to 0.11143**, retaining >0.5 of score.
- Synthetic amplitude scale is an injected frequency-domain tone coefficient, **not a calibrated 1.0 signal/noise RMS**. Sensitivity on faint real GBT line shapes is unknown.

## Worker instructions
```bash
python n1625.py --self-test
OPENBLAS_NUM_THREADS=1 python n1625.py --dm /path/to/alexanarch/rebuild/3i-atlas-signal-search/claude/voltages/delaymod --frames 32 --surrogates 199 --scan all --output N1625-results.json
```

**Selection/confirmation limit:** 32 frames per scan are merely the first ~11.46 seconds. If the original ON0013 event occurred outside that window, an absent candidate means nothing about the event; locate it before declaring a non-detection. Any detected shape must survive fixed-parameter half-window checks and OFF-pointing controls with calibrated sensitivity, plus eventual all-frame scans.

**Result:** validated detector sensitivity to a constructed nonstationary multi-frequency motif; **no new extraterrestrial or comet signal identified**. Do not confuse software self-test with original-telescope-voltage execution.