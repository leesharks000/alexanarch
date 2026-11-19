# External: A Relation Survives the Turning, phase geometry and a radio-poem score (received 2026-11-19 13:46 EST)

Three files, verbatim as received from the operator: `a-relation-survives-evidence-2026-11-19.zip` (the evidence bundle, 27 files), `POEM.md` (the draft radio-poem score, identical to the copy in the zip) and `phase-sheet.png` (identical to the copy in the zip). The producing agent is not named. It is the phase experiment that follows `../human-sheet-full-cadence-20261119/`. Working research and an authored literary draft, not a deposit.

## What it reports

1. Over 52 non-overlapping windows per scan, it measures the closure of carrier C and companions U and L: T = U·L·(C*)². The phase of the coherence Q is invariant to a common phase and to the time reference.
2. Pooled over the six scans, feed X, ±60 Hz: 149 of 312 windows eligible, coherence 0.698, closure 144.38°. That is in the pre-declared PM-compatible sector, but not pure PM. 128 phase randomizations reach at most 0.263.
3. ±120 Hz closes at 113.24° and ±180 Hz at 116.76° ("other stable geometry"). OFF scan 16 is unresolved (coherence 0.589). The relation holds in ON and OFF scans alike.
4. 300 synthetic controls were committed before the measured extraction (`CONTROLS-BEFORE-DATA.json`). Fixed three-tone controls show that a stable closure does not identify a modulation process.
5. The source and mechanism are unidentified. No comet-associated candidate is claimed.

## Checked here

- All 27 files in the zip match its `SHA256.json`. `FREEZE.json` holds the plan, code and input hashes; `CONTROLS-BEFORE-DATA.json` holds the control-result hashes.
- The AM/PM rule checks out by expansion. Simple AM, (1 + m cos ωt), gives U = L = m/2, so T = m²/4 and the closure is 0°. Narrowband PM, e^{iβ sin ωt} ≈ 1 + (β/2)(e^{iωt} − e^{−iωt}), gives U = β/2 and L = −β/2, so T = −β²/4 and the closure is 180°.
- The eligible-window counts the poem opens on (33, 15, 29, 31, 20, 21) are the report's per-scan table.
- Not re-run: the coefficient replay and the controls. `replay_coefficients.py` is standalone and can be run from the zip.

## Where it stands against r13

- It concerns only the 1665.615 MHz complex, which r13 holds as interference (RESULTS-M1.md). The full-band M4 run is untouched.
- The poem, *A Relation Survives the Turning*, is a draft under Lee Sharks for Glas, Dancings and Cranes. It is held here as received, for his ruling.
