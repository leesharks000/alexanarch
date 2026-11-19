# r13 Part M, stages 2 and 3: results

Frozen plans: PLAN-M2.md (23:00:29Z) and PLAN-M3.md (23:06:12Z), both committed before any product existed. Products: M2.json, volt/cc26.json, volt/cc00.json, volt/cc40.json, volt/cc63.json; logs m2.log, m3.log.

## Stage 2: the weirdest single on-comet hit (coarse channels 26, 0, 63, 40)

Each ON and OFF scan stacked in the comet frame with 100 false frames; a hit is z ≥ 4, comet-tuned by margin ≥ 1 against frames at least 6 bins distinct, and absent within ±3 bins from the vetoes.

| Channel (centre MHz) | ON hits 0013 / 0015 / 0017 | OFF hits 0014 / 0016 / 0018 | Top weirdness ON | Top weirdness OFF |
|---|---|---|---|---|
| cc26 (1611.33) | 27 / 32 / 28 | 25 / 24 / 30 | 5.41 | 5.49 |
| cc00 (1687.50) | 34 / 41 / 42 | 21 / 27 / 12 | 20.53 | 13.79 |
| cc63 (1502.93) | 22 / 20 / 27 | 14 / 23 / 12 | 2.76 | 2.60 |
| cc40 (1570.31) | 25 / 18 / 38 | 14 / 19 / 228 | 2.97 | 5.57 |

ON counts sit within or just above the OFF counts in every channel. The one large ON lead, cc00 0015 at 1687.5066 MHz (z 23.8, weirdness 20.5), lies 0.006 MHz from the coarse-channel centre in a channel whose OFF0016 carries weirdness 13.8 at 1687.5307 MHz. The strongest cc26 feature, 1611.0115 MHz, appears in OFF0014, ON0015 and OFF0016 alike.

## Stage 3: weird as voltage

For the ten highest-z hits per ON scan (30 per channel, 120 in all), voltages along the comet track (±64 bins) were tested against six local comparisons and three OFF series. Nomination required W1 (envelope periodicity, frame-rate harmonics excluded) above 1.5× every reference, or the suppressed-carrier flag (pr2 and pr2/pr1 each above 1.5× every reference).

**Nominations: 0 of 120.** Closest approaches:

| Channel | Highest W1 / max reference W1 | at | Highest pr2 / max reference pr2 |
|---|---|---|---|
| cc26 | 1.37 (0017#9, X, 28.2 Hz, 1612.777 MHz) | | 1.21 |
| cc00 | 1.23 (0015#2, X, 11.4 Hz, 1687.531 MHz) | | 1.31 |
| cc63 | 1.29 (0017#3, Y, 11.0 Hz, 1504.268 MHz) | | 1.20 |
| cc40 | 1.12 (0013#3, Y, 7.4 Hz, 1570.723 MHz) | | 1.19 |

No hit's voltages are more periodic in envelope, or more carrier-suppressed, than the same band's local comparisons and the OFF series by the frozen margin. k4 is reported in the files and not used.

## Run notes

- cc63's first M3 attempt read cc63_0018.npz while M2 was still writing it (BadZipFile) and was rerun after cc40; a container restart stopped the rerun at 0018, and it was restarted from the start of the channel. All four volt files are complete.
- One M2 download retried after a connection reset (0013, cc40) and completed.

## Reading

Within these four coarse channels and this battery, no on-comet hit is structured in its voltages beyond its own neighbourhood and the OFF scans. Under the operator's method ("if it seems to be signal, use it to determine where else to look") there is no lead to follow from M. The external autocorrelation report of the same date (../external/autocorr-20261118) likewise finds no robust candidate; its one flag lies in the 1665.6 MHz complex held as interference.
