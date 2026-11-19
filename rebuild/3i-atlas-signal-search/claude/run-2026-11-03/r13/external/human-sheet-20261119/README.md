# External: The Human on the Sheet, first reading (received 2026-11-19 09:05 EST)

Three files, verbatim as received from the operator: `READING.md`, `human-sheet-ON-OFF.wav` and `human-sheet-first-reading-2026-11-19.zip` (the evidence bundle, 18 files). The producing agent is not named. It is the pilot for the reading Lee named *Glas, Dancings and Cranes*. It is working research and literary material, not a deposit.

## What it does

1. It reads the known 1665.615 MHz complex in the same six 6.08 s excerpts as `../inscription-20261119/`, with no injection.
2. The complex is present in all six excerpts, the OFF ones included. OFF0016 has the strongest peak (13.35 dB over the local median). The peak spans about 11 Hz across the scans and sits mostly in feed X (0.84–0.98).
3. It makes a sonification: the six excerpts in scan order, centred on an audio tone of 1000 Hz (±250 Hz retained), one global gain, with half-second editorial gaps. 39.008 s at 8 kHz.
4. It gives a first score for the three voices, under Lee's authorship.
5. Its frozen plan for the full-band human reading keeps complete spectra and matched OFF measurements. It treats a top-N omission as censored, and assigns identity only by positive modulation, spectral and geometric tests.

## Checked here

- Every one of the 18 files in the zip matches its `SHA256.json` entry. The zip's `READING.md` and WAV are byte-identical to the separately attached ones.
- `FREEZE.json` hashes `PLAN.md` and `read_sheet.py` as they stand.
- WAV: 8000 Hz, mono, 16-bit, 39.00775 s, as stated.
- Times: scan 0013 starts at 17226 s = 04:47:06 UTC; plus 146.029 s gives 04:49:32.029, as listed. Scan 0014 starts at 17543 s = 04:52:23, giving 04:54:49.029. Both agree with dm.py's SCANS.
- Frequency: its peak at 1665.6151 MHz agrees with M1's 1665.6152 MHz feature (RESULTS-M1.md). Its presence in every OFF excerpt agrees with M1's OFF0016 and OFF0018 detections.

## What it corrects in the session's own account (2026-11-19 08:28)

1. The complex is not "right against" the OH line. It is 213.3 kHz above the 1665.4018 MHz rest line. It sits in the 1660.5–1668.4 MHz passive band, which does not make it non-human.
2. GPS C/A's 1.023 MHz chips cannot be resolved in the M products (357.6 Hz) or in a 91.55 kHz band. Naming a service by modulation needs bandwidth matched to it.
3. The band holds Earth-to-space uplinks as well as downlinks (mobile-satellite, 1626.5–1660.5 MHz). "Mostly" has to name its measure: power, occupancy or source count.
4. Earth as received at Green Bank and Earth as radiating toward the comet are two measurement problems. The second is a model built from identified sources, beams, geometry and light-travel time.
