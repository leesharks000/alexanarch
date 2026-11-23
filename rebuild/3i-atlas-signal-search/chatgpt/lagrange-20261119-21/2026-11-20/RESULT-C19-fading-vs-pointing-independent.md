# Independent C19 raw-voltage summary audit — temporal fading versus telescope pointing
2026-11-20. Followup to Claude's raw-data results newly published in Lagrange Observatory.

**Canonical data:** [RESULT-GBT-cc19-raw-voltages-C19.md](RESULT-GBT-cc19-raw-voltages-C19.md), which reports raw-voltage analyses of six GBT December 18 2025 scans, both polarizations. This note reanalyzes **only its per-scan six-number power summaries**, not the original voltage bytes. Reproduction: [audit_c19_fade_pointing.py](audit_c19_fade_pointing.py).

## Question and model
Does the power primarily follow ON/OFF pointing, as a localized source at the comet should, or decline with chronological scan order, independently of pointing? Fit to ln(power above the local median). Indices 0..5 are an ordinal proxy for acquisition time (not exact timestamps). ON indicator [1,0,1,0,1,0]. Models: intercept, ON-only, time-only, time+ON. Ordinary least squares, report residual sum of squares and BIC = n ln(RSS/n)+k ln(n) with n=6. BIC comparisons descriptive with tiny correlated repeated-scan samples.

Input powers across ON13/OFF14/ON15/OFF16/ON17/OFF18:
- A n=2 [67.99, 16.48, 19.38, 10.09, 3.11, 2.22].
- B n=1 [15.35, 4.99, 4.34, 3.21, 2.75, 3.11].
- 15 catalogue lines [18.12, 6.49, 6.45, 4.58, 4.64, 4.24].

## Numerical outcomes
| Signal | Model | log-power slope per scan | coefficient on ON | RSS | BIC |
|---|---|---:|---:|---:|---:|
|A n=2|pointing only|n/a|+0.802|6.997|4.506|
|A n=2|time only|-0.650|n/a|0.559|-10.656|
|A n=2|time + pointing|-0.636|+0.166|0.521|-9.285|
|B n=1|pointing only|n/a|+0.434|1.727|-3.890|
|B n=1|time only|-0.288|n/a|0.560|-10.644|
|B n=1|time + pointing|-0.274|+0.160|0.525|-9.241|
|15 catalogue lines|pointing only|n/a|+0.486|1.113|-6.523|
|15 catalogue lines|time only|-0.246|n/a|0.409|-12.533|
|15 catalogue lines|time + pointing|-0.224|+0.263|0.314|-12.324|

The time-only model outperforms pointing-only by BIC differences 15.16, 6.75, 6.01 respectively. Adding ON pointing to time does not improve BIC for any of the three summaries; it modestly reduces RSS, as expected with more degrees of freedom. This is **supporting evidence for time-dominated fading**, independently quantifying the raw-voltage report's read-off.

A caveat: ON is temporally interleaved with OFF, so time and pointing are not perfectly separated; six observations do not support a precision source model. The OFF power is in some scans comparable to adjacent ON even though the pointings are 60 arcminutes apart; this provides a more robust spatial exclusion of a compact on-comet narrowband source than drift slope alone. No calibrated full telescope sidelobe beam map is used here; the quoted 30dB expected attenuation in the C19 parent report depends on an assumed main-beam response.

## Attempt at terrestrial source identification
The center frequency ~1632 MHz falls inside the allocated 1626.5–1660.5 MHz Earth-to-space mobile satellite service band (47 CFR Part 25). This establishes a strong interference prior, **not the actual emitter's identity**.
- ETSI GEO-Mobile Radio Interface standard states 31.25 kHz carrier spacing for one specified L-band service set: https://www.theiteh.com/catalog/standards/etsi/effd4631-80be-44d8-9d1e-d87d534c5ead/etsi-ts-101-376-5-5-v3-4-1-2015-10
- Iridium NEXT engineering statement lists 41.667 kHz carrier spacing in **a different** 1616–1626.5 MHz band: https://fcc.report/IBFS/SAT-MOD-20131227-00148/1031348.pdf
- Neither matches the observed 67.433 kHz spacing. This is *not* evidence of nonhuman transmission: there are many possible radio interfaces, sidebands, periodic interference sources, and mixing artifacts, and the search for standards has not identified this emitter.

## Decision
The original hypothesis of a weak 3I-associated transmitter embedded in the cc19 interference family has **no positive support** from this test. The family itself is real, temporally variable and enters the beam even during OFF pointings. Followup justified if interested in an **unidentified terrestrial/orbital interference emitter**, not as a prioritized comet technosignature.

Highest-value next astronomical work: independently test cc48 (~1547 MHz) and cc50 (~1541 MHz) with raw voltages, using Claude's already demonstrated C19 processing machinery and predeclared ON/OFF, time-trend, frequency and satellite hypotheses. These channels are in the opposite mobile-satellite downlink allocation and had high frozen M4b Class A excesses. Require raw source-level analysis, not more retrospective matching of thresholded hits.
