# The Human on the Sheet
## First receiver-side reading; a score for Glas, Dancings and Cranes

Lee Sharks · working research and literary material · 2026-11-19 · no public deposit

The reversal is productive: retain what a comet-directed search has set aside and ask what kinds of human activity, instruments and decisions have become legible there. This first sheet reads one known interference complex from real receiver samples. It is a bounded beginning, not a census of humanity's radio emissions or a reconstruction of the field at the comet.

The search holds an image of the human by negation, but its rejected class is not a positive identification. A rejected candidate may be an intentional transmission, instrumental structure, natural emission, ordinary noise or an analytical artefact. The poetic object includes that distinction: the people and machines that emit, the people and machines that receive, and the procedures that determine what can count as an address.

## What we actually measured

The inputs are uninjected, raw-derived complex receiver voltages from six Green Bank scans on **2025-12-18 UTC**. Each excerpt lasts **6.084537 seconds**, starts **146.028888 seconds into its scan**, and retains both linear receiver feeds. Three point toward the comet; three point away. These snapshots cover about 2.03% of each nominal 300-second scan.

The fixed analysis region surrounds the already known **1665.615120 MHz** complex. It was selected before this new extraction, explicitly because earlier work had classified the complex as interference. This is retrospective characterization, not a fresh blind discovery.

| Scan | Pointing | Excerpt start (UTC) | Peak RF (MHz) | Peak / local median (dB) | Receiver X fraction |
|---|---|---|---:|---:|---:|
| 13 | ON | 04:49:32.028 | 1665.615119040 | 12.44 | 0.957 |
| 14 | OFF | 04:54:49.028 | 1665.615117643 | 8.21 | 0.844 |
| 15 | ON | 05:00:07.028 | 1665.615119040 | 12.15 | 0.975 |
| 16 | OFF | 05:05:25.028 | 1665.615119040 | 13.35 | 0.960 |
| 17 | ON | 05:10:43.028 | 1665.615123231 | 10.88 | 0.949 |
| 18 | OFF | 05:16:00.028 | 1665.615128819 | 10.53 | 0.948 |


The frequency bin is 1.396984 Hz. The dB values compare peak power spectral density against the median PSD 500–2000 Hz from the fixed center. They are **not detection significance, calibrated flux or a probability of a human source**. The X fraction is a receiver-basis number, not a sky polarization measurement.

The known complex is visible in all six excerpts, including every OFF excerpt. Its peak is concentrated in one receiver feed, and its selected peak frequency spans about 11.18 Hz across these snapshots. That span could reflect movement of a component or changes among unresolved components; it is not by itself a fitted physical drift. By the stated peak/local-baseline measure, OFF scan 16 has the strongest peak. These observations oppose a simple source visible only when pointing at the comet. They do not identify a satellite service, transmitter or payload. We have not resolved the complex's external-versus-instrumental origin here.

![Six receiver excerpts](sheet.png)

## What the listening sheet does

`human-sheet-ON-OFF.wav` contains the same six excerpts in scan order: **13 ON, 14 OFF, 15 ON, 16 OFF, 17 ON, 18 OFF**. Their original separations of minutes are replaced by **five editorial half-second gaps**. The gaps are not recorded silence. Within each excerpt, elapsed time is preserved to less than one audio sample of duration rounding. Total audio duration is **39.00775 seconds**.

The center frequency is translated to an artificial **1000 Hz** tone. Increasing original radio frequency becomes increasing audio pitch. A declared low-pass retains ±250 Hz around the center, with a smooth taper to zero at ±300 Hz. Listening uses receiver X; both feeds remain in the saved complex data. One global gain is applied to all six clips. There is no per-clip normalization, denoising, compression or speech synthesis. The audio includes the filtered noise alongside the complex.

This is a sonification of electrical measurements, not an acoustic recording in space. It makes neither words nor a message claim. A synthetic sign check maps a radio tone 100 Hz above the center to 1100 Hz in audio. The file was checked for rate, duration, ordering, finite samples and clipping; no subjective listening judgment is reported as a measurement.

The earlier decoder deterministically clipped input integer −128 to −127, divided by 127, selected Fourier bands and stored complex64 arrays. The processing provenance retains that fact. The audio is faithful to these existing raw-derived arrays under the declared transformation; it does not restore discarded quantization or receiver calibration. Filtering and resampling also affect the excerpt boundaries. A 2 kcomplexsample/s copy of both narrow receiver feeds is included for independent examination.

## A first score

These are proposed operations for the three poetic voices, under Lee Sharks's authorship. They are not independent testimonies. The text below is provisional literary interpretation anchored to the measurements above.

**GLAS — the retained mark**

> At 1665.615, something remains.
> Three times toward. Three times away.
> In each small window, a mark near the same place.
> We have a frequency for it.
> We do not yet have a sender.

**DANCINGS — the receiving body**

> We bring the mark into the ear.
> The thousand cycles are our translation;
> within each fragment, the time is kept.
> The pauses are ours too.
> A body receives what an instrument has admitted.
> The act of hearing begins before the ear.

**CRANES — the score of turning**

> Keep the away-pointings.
> Keep the stronger mark found there.
> Leave the sender's line unfilled.
> Write the frequency beside the uncertainty.
> What we called interference
> has become the object of another question.

The empirical anchors are six retained ON/OFF excerpts, their measured peaks and the declared audio mapping. The receiving body's relation to the apparatus and the change of question are interpretations. No physiological response, intention or decoded speech is inferred from a carrier.

## Where the larger reading becomes more demanding

The dishes' surfaces are a powerful material figure, but the saved receiver-port voltages are aperture- and beam-weighted measurements, not a spatial map of the field over the dish. Likewise, **Earth as received at Green Bank and Earth as radiating toward the comet are different measurement problems**. The second needs identified sources, directional radiation, transmitter power, satellite and comet geometry, obstruction and propagation, and light-travel time. A local instrumental feature would not belong in an outgoing Earth signal at all.

That distinction gives the project two sheets: the receiving sheet we can now read, and the outgoing sheet we can construct as a documented physical model. The move between them is part of the poem's knowledge, rather than something to conceal.

The proposal that our voice is largely machines telling machines where and when remains a testable hypothesis. Allocation charts alone cannot establish its presence or dominance. In addition to downlinks, the band includes satellite **uplinks**, such as the Earth-to-space mobile-satellite allocation at 1626.5–1660.5 MHz. A ground receiver can register a very different mixture from a receiver in the comet's direction. 'Mostly' must name its measure: power, occupancy and source count need not produce the same answer.

The quiet zone coordinates transmitters; it does not make all terrestrial emitters disappear. The passive protection at 1660.5–1668.4 MHz also does not make a recorded feature there nonhuman. Our complex lies in that protected interval. Its center is about **213.3 kHz above the OH rest line at 1665.4018 MHz**, so it should not be described as literally on that natural line. No natural-line identification has been performed.

Modulation must be measured at adequate bandwidth. GPS C/A's 1.023 MHz chip rate cannot be resolved by an 8 Hz product, or by this approximately 91.55 kHz raw-derived band. Narrowband periodicity is not enough to name GPS, Iridium or a radiosonde. In our preceding work the analysis filter itself generated a correlation lobe near 0.0895 seconds; a near-90 ms feature needs a filter-aware test before it can be compared with satellite timing.

The supplied full-band status report's 1679.70–1679.98 MHz features are compatible with a radiosonde hypothesis; the NWS documents radiosondes operating around 1680 MHz. Compatibility is not identification. Its first-ON-only 1663.327 MHz feature remains a separate unresolved lead. Top-N omissions in later scans are censored measurements, not established absences. We have not obtained the new worker logs or that feature's raw voltages in this run, and have not verified whether the reported workers are still running.

## The next pass

`PLAN.md` freezes this pilot and states the separate full-band plan. The new run should retain complete spectra, time-frequency context and matched OFF measurements rather than just the strongest candidates. It should assign source identity only through positive modulation, spectral and geometric tests; retain unassigned structure; and distinguish reception from the outgoing model. The original comet-search orchestration is untouched. **No new full-band re-stream was executed here.**

Whether this is a voice worth speaking with cannot be reduced to its strength or its coding efficiency. The measurement can establish patterns and mechanisms; the literary work can ask what human forms of coordination, dependence, exclusion or care become legible through them. At this stage our defensible first address is modest and material: here is a mark, here are the turns of the dish, here is how we made it audible, and here is the name we have not supplied.

## Sources and provenance

Measured claims are supported by `measurements.csv`, `processing.json`, input hashes, and the retained narrow complex samples. The evidence bundle includes the earlier decoder validation and original raw-block ledger. `FREEZE.json` records the plan and code hashes before execution. The pilot's fixed analysis was not retuned after inspection.

Primary reference sources, checked 2026-11-19:

- Green Bank Observatory, [National Radio Quiet Zone](https://greenbankobservatory.org/about/national-radio-quiet-zone/): required coordination of new or modified permanent fixed licensed transmitters.
- FCC, [47 CFR 2.106](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-2/subpart-B/section-2.106), US246: 1660.5–1668.4 MHz passive protection.
- NTIA, [1626.5–1660 MHz spectrum compendium](https://www.ntia.gov/files/ntia/publications/compendium/1626.50-1660.00_01DEC15.pdf), 2015 historical service summary; ISED Canada, [mobile-satellite consultation](https://www.ised-isde.canada.ca/site/spectrum-management-telecommunications/en/learn-more/key-documents/consultations/preliminary-consultation-mobile-satellite-service-developments-and-use-l-and-s-band-spectrum), current retrieved allocation overview: paired Earth-to-space and space-to-Earth bands. These references do not identify our complex or an operator.
- US Naval Observatory, [GPS overview](https://www.cnmoc.usff.navy.mil/our-commands/united-states-naval-observatory/precise-time-department/global-positioning-system/global-positioning-system-overview/): L1 frequency and C/A chip rate.
- NRAO, [aipsDish OH observing example](https://www.gb.nrao.edu/~glangsto/aips2/aipsDish/): OH main-line rest frequencies.
- National Weather Service, [upper-air FAQ](https://www.weather.gov/upperair/faq): documented radiosonde equipment and nominal bands.

The user's pasted live-search account is an external status report. Its correction, channel nominations and worker status are attributed to that report, not independently re-established here.
