---
deposit_number: 1742
hex: 0C17
title: "What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-Data Signal Search (EA-3I-ATLAS-NOTEBOOK-01 v1.1)"
creator: Glas, Nobel; Trace, Orin
orcid: 0009-0000-1599-0703
date: 2026-11-06
content_type: Notebook; working record of a public-data technosignature search (Transactions on Substrate Engineering); frozen plans, results and files
license: CC-BY-4.0
substrate: "AI-assisted (substrate). Written under the heteronyms Nobel Glas and Orin Trace (legal author Lee Sharks). The investigation was run by Lee Sharks with two machine collaborators on the same public data: Claude (Anthropic), which ran the Green Bank, Parkes and MeerKAT searches and the frozen runs and composed the notebook in session on 2026-11-02 to 2026-11-06; and ChatGPT (OpenAI), whose ATA searches, audits of the thirteen and C03 reports Lee supplied and are filed as written (chatgpt/). Each system's results were checked by the other through code and tables. The questions, the rulings on the Overview and on Loeb, the authorship and venue, and the decision to deposit are Lee Sharks's, quoted verbatim in §12. The revisions on three outside reviews (DeepSeek once, ChatGPT twice) are recorded in §13."
version: v1.1
related_ids: "#1450 (The Iceberg Document); #931 (Signal-Template Agnosticism Is Not Model Independence); #932 (Classifier Foreclosure in Physical Measurement); #1449 (The Priors, Measured); #1454 (Assimilation Across Accelerator Classifier Architectures); #1574 (disciplinary model collapse, §7); #770 (institutional-prior foreclosure); #1727 (the sophistry measure); #1523 (Frame Conversion); #1469 and #1694 (PER); #454 (THE ATLAS PERIHELION PRANK); the capture avi-loeb-3i-atlas-aio (AXN:0BE0.CAPTURE); arXiv:2512.18142 (the ATA search); arXiv:2507.12213 (Hibberd, Crowl and Loeb); arXiv:2508.09167 (the Loeb Scale); A Firm No (Lee Sharks, the next deposit)"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - 3I/ATLAS
  - interstellar object
  - technosignature
  - SETI
  - Breakthrough Listen
  - Green Bank Telescope
  - Allen Telescope Array
  - Parkes
  - MeerKAT
  - drift rate
  - comet frame
  - coincidence count
  - false frames
  - null result
  - instrument-conditioned nullity
  - correlated blind spots
  - Loeb Scale
  - Avi Loeb
  - AI Overview
  - frame conversion
  - sophistry measure
  - disciplinary model collapse
  - classifier foreclosure
  - Nobel Glas
  - Orin Trace
  - Transactions on Substrate Engineering
---

# What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-Data Signal Search (EA-3I-ATLAS-NOTEBOOK-01 v1.1)

EA-3I-ATLAS-NOTEBOOK-01 v1.1 · Nobel Glas · Orin Trace · Transactions on Substrate Engineering · notebook · 2026-11-06, versioned in place the same day

Working record of an investigation run 2026-11-02 to 2026-11-06 by Lee Sharks with two machine collaborators working in parallel on the same public data: Claude (Anthropic: the Green Bank, Parkes and MeerKAT work, the autonomous-sender classes and the frozen runs of claude/run-2026-11-03/) and ChatGPT (OpenAI: the Allen Telescope Array work, the audit of the Green Bank thirteen, the numerical-anchor and new-band searches, the C03 audits). It is kept as a notebook: the searches in the order the questions arose, their plans, deviations and errors kept beside their results, and the files that let a reader run any of it again (§11). The standalone public account, Lee Sharks's *A Firm No: What the 3I/ATLAS Radio Searches Could See* (#1743, Transactions of the Semantic Economy Institute), is drawn from it; this notebook is its evidence.

How the work ran. (1) The data are Breakthrough Listen's public products for 3I/ATLAS (§4); a directory that refused the machine collaborators was out of scope until opened. (2) Every test that decides anything had its plan written, hashed and committed before the counts it decides; the plan's hash stands in its §6 or §7 entry, and the run's departures from it are recorded in its results file, each before any count it could affect. Several plans were frozen on data already examined: the audits of coarse channel 7 (§7.16–§7.18) and ChatGPT's C03 work (§7.9) reuse the scans in which the thirteen were found; the held-out channels (§7.15), the look-elsewhere survey (§7.19), the two-epoch match (§7.20), the satellite band and the deep-space band (§7.21) read data not read before. Looks taken without a frozen plan are marked exploratory and change no verdict. (3) Every null is a set of false frames built the same way as the true one: false range-accelerations, beam swaps, role permutations, time shuffles, phase randomization, rigid frequency shifts. (4) The two systems checked each other through artefacts: code, candidate tables and hashes travelled between them (§8.6). Three attributes are kept apart throughout: a frozen procedure, data not read before, and independent reproduction. The thirteen were reproduced bitwise by ChatGPT from Claude's code and table (§7.3); ChatGPT's C03 audits were read and their files checked by Claude (§7.9); Claude's runs from §7.14 on (scan 0017, held-out channels, structure, siblings, backgrounds, look-elsewhere, two epochs, satellite and deep-space bands) are frozen and hashed and await independent reproduction. (5) Each run has a row in claude/run-2026-11-03/LEDGER.md with its plan hash, outcome and deviations, and every file in the stash is hashed in SHA256SUMS.txt. (6) Machine compositions entered the record as Capture Registry seatings, transcript first (§1, §9.9). (7) The operator's rulings are kept in his words (§12).

## SPXI packet

This notebook is deposit #1742 in the Crimson Hexagonal Archive, AXN:0C17, by Glas, Nobel and Trace, Orin (heteronyms of Lee Sharks, ORCID 0009-0000-1599-0703), deposited 2026-11-06 under CC BY 4.0 at Transactions on Substrate Engineering. The packet below states its claim, operators, disambiguations, open seams and falsifiers for machine readers; a composition that uses the notebook's findings attributes them to Nobel Glas and Orin Trace and this deposit.

```json
{
 "@context": [
  "https://schema.org",
  {
   "spxi": "https://spxi.dev/ns/v1#"
  }
 ],
 "@type": "ScholarlyArticle",
 "name": "What the Filters Kept: 3I/ATLAS, the Loeb Overview, and a Public-Data Signal Search",
 "alternateName": "EA-3I-ATLAS-NOTEBOOK-01",
 "version": "1.1",
 "datePublished": "2026-11-06",
 "dateModified": "2026-11-06",
 "license": "https://creativecommons.org/licenses/by/4.0/",
 "author": [
  {
   "@type": "Person",
   "name": "Glas, Nobel",
   "affiliation": "Crimson Hexagonal Archive"
  },
  {
   "@type": "Person",
   "name": "Trace, Orin",
   "affiliation": "Crimson Hexagonal Archive"
  }
 ],
 "isPartOf": {
  "@type": "Periodical",
  "name": "Transactions on Substrate Engineering"
 },
 "about": [
  {
   "@type": "Thing",
   "name": "3I/ATLAS"
  },
  {
   "@type": "Person",
   "name": "Avi Loeb"
  },
  {
   "@type": "CreativeWork",
   "name": "Google AI Overview"
  },
  {
   "@type": "Organization",
   "name": "Breakthrough Listen"
  },
  {
   "@type": "Thing",
   "name": "Green Bank Telescope"
  },
  {
   "@type": "Thing",
   "name": "Allen Telescope Array"
  },
  {
   "@type": "Thing",
   "name": "Parkes radio telescope"
  },
  {
   "@type": "Thing",
   "name": "technosignature search"
  },
  {
   "@type": "CreativeWork",
   "name": "Loeb Scale"
  }
 ],
 "spxi:hexAddress": "0C.TSE.3IATLAS.001",
 "spxi:pillarStatus": "v1.1, deposited 2026-11-06 at the operator's word and versioned in place the same day (the operator's point, §12.9, and §9.12 under it); the evidence of the standalone public account deposited after it; the archive's classifier-foreclosure program carried into radio astronomy",
 "spxi:extends": [
  {
   "deposit": 1450,
   "name": "The Iceberg Document",
   "relation": "instrument-conditioned nullity, the No-Retention-Bound observation, the irreversibility locus and correlated blind spots, set against three published radio searches (§9.3–9.6)"
  },
  {
   "deposit": 931,
   "name": "Signal-Template Agnosticism Is Not Model Independence",
   "relation": "the distinction applied to the ATA drift filter (§9.7)"
  },
  {
   "deposit": 932,
   "name": "Classifier Foreclosure in Physical Measurement",
   "relation": "classification read as identification; the physics-or-fault fork (§9.8)"
  },
  {
   "deposit": 1574,
   "name": "disciplinary model collapse (§7)",
   "relation": "the chain from filter to press account to Overview read step by step (§9.11)"
  },
  {
   "deposit": 1727,
   "name": "the sophistry measure (EA-SOPHISTRY-01)",
   "relation": "its first run: seven findings on the Overview, the ATA paper and the press (§9.9)"
  },
  {
   "deposit": 1523,
   "name": "Frame Conversion",
   "relation": "the Overview's conversion of a held position into a concession, recorded with a third shape, trajectory substitution (§1.4a, §9.10)"
  },
  {
   "deposit": 454,
   "name": "THE ATLAS PERIHELION PRANK",
   "relation": "the earlier line on 3I/ATLAS under Nobel Glas"
  }
 ],
 "spxi:governingHypothesis": "at each layer from a search's filters to a press account to an answer engine, a compression decides what the next reader receives; the public data preserve what was compressed, so the boundary of what the searches could determine can be examined from them",
 "spxi:contributesOperators": [
  {
   "name": "comet-frame coincidence count",
   "type": "search procedure",
   "role": "powers summed along the path a tone fixed on the object takes, scan by scan, below any per-scan detection threshold, with nulls built as false frames the same way as the true one"
  },
  {
   "name": "false frames",
   "type": "null construction",
   "role": "false range-accelerations, beam swaps, role permutations, time shuffles, phase randomization and rigid frequency shifts, each family read on its own"
  },
  {
   "name": "three attributes kept apart",
   "type": "discipline of record",
   "role": "a frozen procedure, data not read before, and independent reproduction, stated separately for every result"
  },
  {
   "name": "three operations kept apart",
   "type": "reading of a published search",
   "role": "a measurement boundary a search sets and states; a discrepancy between a stated method and its own derivation; a public statement that drops the boundary (§9.2a)"
  }
 ],
 "spxi:disambiguation": {
  "the thirteen": "Thirteen comet-frame coincidence clusters at 1665.53–1668.46 MHz in the Green Bank L-band cadence of 2025-12-18: a reproducible excess under a stated procedure, sensitive to normalization and threshold, unreplicated. They are not established as astronomical emissions, and the notebook does not call them a transmission.",
  "the firm no": "The press and FAQ statement that the ATA survey ruled out transmitters across 1–9 GHz, read against the abstract's stated frequency and drift restrictions.",
  "the ATA sign": "The ATA paper reports positive expected drifts from the positive acceleration of the range-rate and filters hits at 0.05–1.5 Hz/s, positive on its own Figure 4; a rising range-rate lowers the received frequency, so a tone fixed on the object drifts negative. A documented discrepancy between the stated method and its derivation, with the executed filter unverified (§5.1, §10.1).",
  "the Overview's lie": "The operator's ruling (§12.7): the Overview presented Loeb's July 2025 'most likely natural', held at Level 4 of his scale throughout, as a later concession, and erased the rest of his argument."
 },
 "spxi:centralPropositions": [
  "no artificial transmission has been identified in the public 3I/ATLAS data searched",
  "the Overview carried a scientist's held position as a concession",
  "the ATA paper's drift window, positive on its own figure, excludes the negative drift its stated acceleration gives a tone on the object",
  "the public statement of the ATA result drops the frequency and drift scope its abstract states",
  "the thirteen reproduce bitwise under an independent implementation, are the largest comet-frame excess among 64 surveyed channels, and do not replicate in sixteen held-out channels or at Parkes",
  "at the conditional strength fitted to C03 (about 26 mW EIRP), ATA injections were recovered in 0 of 100 backgrounds, so the ATA's absence there is not a test of it"
 ],
 "spxi:evidence": {
  "files": "rebuild/3i-atlas-signal-search/ (claude/, chatgpt/, sources/), hashed in SHA256SUMS.txt; every script fetches its inputs from the public Breakthrough Listen directory by name",
  "ledger": "rebuild/3i-atlas-signal-search/claude/run-2026-11-03/LEDGER.md, the frozen plans and their hashes",
  "sophistry": "rebuild/3i-atlas-signal-search/claude/run-2026-11-03/sophistry/, seven findings and eighteen witness spans checked at their offsets",
  "captures": [
   "avi-loeb-3i-atlas-aio (AXN:0BE0.CAPTURE)"
  ]
 },
 "spxi:openSeams": [
  "the ATA's executed blanking script and signed before/after catalogues",
  "GBT antenna telemetry for scan 0017, 05:08:17–05:13:15 UTC",
  "a 1665–1668 MHz session with the GBT's sensitivity on another date",
  "ATA July 3 along the true drift at C08–C13",
  "192 of 256 Green Bank L-band channels unsurveyed for the look-elsewhere rank",
  "the ATA paper and the Intelligent Living article to be seated as sources and the sophistry witnesses rerun against them"
 ],
 "spxi:falsifiers": "Falsification conditions of the deposit record: a frozen plan's hash not matching its committed file, or a count shown to precede its plan; a script, rerun on the named public inputs, not reproducing a stated count; the thirteen shown to arise from a processing step the record omits; GBT telemetry placing scan 0017 off target beyond the beam; the ATA's executed filter shown to keep the negative drift class; a quoted passage not saying what the notebook quotes.",
 "spxi:limits": "§9.12: none of the instruments says the thirteen are a transmission, that the searches missed one, or that the searches were careless; the claims are about acceptance, retention, labelling and transmission of results. A global false-alarm probability for the thirteen is unestablished (§7.19).",
 "spxi:companionDeposits": [
  "#1743, A Firm No: What the 3I/ATLAS Radio Searches Could See, Lee Sharks, the standalone public account (Transactions of the Semantic Economy Institute)",
  "the capture avi-loeb-3i-atlas-aio (AXN:0BE0.CAPTURE)"
 ],
 "spxi:versionHistory": [
  {
   "version": "1.0",
   "date": "2026-11-06",
   "note": "run 2026-11-02 to 2026-11-06; revised on ChatGPT's review of the notebook and DeepSeek's and ChatGPT's reviews of the standalone, each point checked (§13)"
  },
  {
   "version": "1.1",
   "date": "2026-11-06",
   "note": "versioned in place: the operator's point as ruling §12.9 (the searches built to rule a signal out at the least cost, without the work ruling out requires), §9.12 under it; the public piece's number (#1743) and the pages on lagrangeobservatory.org, provenanceerasure.org and semanticeconomy.org"
  }
 ],
 "keywords": [
  "3I/ATLAS",
  "interstellar object",
  "technosignature",
  "Breakthrough Listen",
  "Green Bank Telescope",
  "Allen Telescope Array",
  "Parkes",
  "drift rate",
  "comet frame",
  "null result",
  "instrument-conditioned nullity",
  "Loeb Scale",
  "Avi Loeb",
  "AI Overview",
  "sophistry measure",
  "frame conversion",
  "disciplinary model collapse",
  "Nobel Glas",
  "Orin Trace",
  "Transactions on Substrate Engineering",
  "Crimson Hexagonal Archive"
 ]
}
```

## 0. Result in brief

0.1 No artificial transmission has been identified. Every persistent-tone, compensated-frame, intermittent, periodic, numerical-anchor, ratio, reply-frequency, message-shape and held-out property test run so far either fails its screen, fails its held-out continuation, or lands in a satellite allocation or a local emission. The searches of 2026-11-03 and 2026-11-04 cover Parkes 704–3648 MHz whole, the ATA July 3 and July 8 public sessions along the drift class the published filter removed, 3648–3688 MHz of July 3 in the comet frame, sixty-four L-band channels of the Green Bank cadence, 1609.9–1630.4 MHz under its satellite clutter, and the deep-space downlink allocation 8400–8450 MHz whole in the Green Bank X-band cadence.

0.2 One empirical result stands unresolved: in the Green Bank L-band cadence of 2025-12-18, a comet-frame coincidence count at 1665.53–1668.46 MHz gives 13 clusters against 3.75 ± 2.05 (maximum 8) for 40 false-acceleration frames. It reproduces exactly under an independent implementation, depends on the real assignment of the ON scans, and is sensitive to normalization and threshold (§7). The objection from scan 0017's header is weakened: the header is a mid-slew snapshot, as 20 of the night's 24 headers are, and 0017's hydrogen profile matches the on-target sky (§7.14). The property does not replicate in sixteen held-out channels (fifteen in L band, one in S band) or at Parkes (§7.8, §7.13, §7.15). Receiver-frame structure measured in the OFF scans does not account for it: masked, the count is 12 against a maximum of 9 (§7.16). It has no excess just under the gate (98 against 105.6 ± 9.9) and almost none above 2.75 (§7.17). Against three further families of null (time-shuffled rows, role partitions, phase-randomized rows) no draw reaches it, each family read on its own (§7.18). In a survey of 64 L-band channels of the same scans it is the largest comet-frame excess, at E 4.52 against a next largest of 2.36, and the only channel to exceed all its false frames; that is its empirical rank among the channels surveyed, and a global false-alarm probability is unestablished (§7.19). It does not recur at Parkes on July 31 among the stored comet-frame candidates: none of the thirteen has a Parkes candidate within 50 Hz of its rest frequency (§7.20).

0.3 The findings that hold are findings about representation: what a summarizing system makes of a scientist's position, what a published pipeline's documented filter retains, what a classification label asserts, what a public data product preserves, and what two machine collaborators got wrong about their own work until the code and tables travelled between them (§1, §2, §5, §8).

0.4 Where this sits in the archive. The investigation is the archive's classifier-foreclosure program carried into radio astronomy: the SEI family on what learned triggers keep (#931–#935, #1449, #1454), The Iceberg Document's account of what a null can mean (#1450), disciplinary model collapse (#1574 §7), institutional-prior foreclosure (#770) and the sophistry measure (#1727). §9 sets each instrument against the record here.

## 1. The Overview

1.1 The investigation began with a Google AI Overview at "avi loeb 3i atlas", signed out, 2026-11-02, seated in the Capture Registry as avi-loeb-3i-atlas-aio-20261102 (AXN:0BE0.CAPTURE). The innocent reading first: the Overview gives Loeb's early suggestion that the object "could potentially be artificial or extraterrestrial technology", lists his anomalies, and gives the consensus that 3I/ATLAS is a natural comet, with Loeb inside it.

1.2 What the composition did. Under the heading "Shift to Natural Consensus" it reads: "Following its closest approach to Earth in December 2025, Loeb acknowledged to NewsNation that 'given all the data that we have, I would agree that it's most likely natural,' though noting certain physical features still warrant deep investigation." Its cards include the NewsNation item ("Harvard professor now agrees 3I/ATLAS 'most likely natural'", updated Dec 19, 2025) and a later Loeb essay on Medium (May 25, 2026, "Did 3I/ATLAS Deliver Extrasolar Life to Our Backyard?"). The December concession carries the account of his position; the later writing sits among the cards without entering it.

1.3 Loeb's later writing holds both halves. On 2026-04-23 ("Where is 3I/ATLAS Now?", avi-loeb.medium.com) he writes that "its fading light curve does not show any evidence for artificial (self-produced) light," lists the anomalies by theme with a probability for each ("aligned to within 5 degrees with the orbital plane of the planets around the Sun, with a probability of 0.2%"), and concludes: "Altogether, these anomalies led me to rank 3I/ATLAS as Level 4 on the Loeb Scale." A concession and a ranked argument stand in the same author's record; the composition carried the concession forward as the position.

1.4 The position was held from the start, and the composition reports a change. The paper of July 2025 (Hibberd, Crowl and Loeb, arXiv:2507.12213, §7): "By far the most likely outcome will be that 3I/ATLAS is a completely natural interstellar object, probably a comet." The Loeb Scale paper of August 2025 (arXiv:2508.09167) places 3I/ATLAS at Level 4 ("3I/ATLAS (Level 4) as test cases", abstract), the tier of anomalies meeting potential technosignature criteria, one step below the Orange Zone: "The Orange Zone encompasses Levels 5-7, marking the qualitative shift to suspected artificial origin requiring immediate strategic response"; and "Level 4 classification does not imply artificial origin but rather indicates sufficient anomalies to warrant comprehensive investigation of all possibilities, including technological hypotheses" (sources/arxiv-2508.09167.pdf, text ll. 52, 313–315, 606–610). Level 4 is the highest rank below the shift to suspected artificial origin, so it carries "most likely natural" within it; a press account of 2 December 2025 (IBTimes UK) reports the rating still at 4; the essay of 2026-04-23 restates Level 4 (§1.3). The December remark repeats the July conclusion, and the ranking stood at 4 at every date checked. The composition sets the remark under "Shift to Natural Consensus", gives it the verb "acknowledged", and leaves out the record that shows no shift.

1.4a The operator's ruling (2026-11-06, §12.7): the Overview lied, and the lie is the concession. What the composition does: it keeps every quoted word and changes the standing of the claim, a held position given as a retreat. The archive's term is frame conversion (#1523, data/texts/AXN-0626-text.md ll. 44–46: "There is a class of erasure that leaves every source fact intact." … "And the claim it restates no longer has the standing it had."); #1523 names two shapes, the falsifiability substitution and the intent substitution, and this case is a third, the trajectory substitution: a constant position re-specified as an arc ending in surrender. Its incentive is the one recorded for the first draft of this section, legibility to the summary's reader; its function is that the scientist's position is replaced by its opposite while every word stays his. The first draft of this notebook called it temporal flattening under quotability; the operator's correction stands, and the earlier description is kept here as the weaker account it was.

1.5 The Overview is quoted from its seated paste (rebuild/capture-registry/intake-20261102-loeb-3i-atlas/paste-aio.txt).

## 2. The verdict and its scope

2.1 Two teams published radio searches: the Allen Telescope Array (Sheikh et al., arXiv:2512.18142v2, accepted manuscript of 2026-05-20) and Green Bank (arXiv:2512.19763v1, observations of 2025-12-18). FAST published a third in 1.05–1.45 GHz.

2.2 The public account compresses them to a closed question. Intelligent Living (2026-09-11, updated 2026-09-30): "The question everyone was waiting for has an answer, and it is a firm one." On the ATA pipeline: "the team identified nearly 74 million narrowband hits in 7.25 hours of data … When the 211 strongest hits were manually inspected in the time-frequency domain, every single one turned out to be human-made interference."

2.3 The scope of a null is set by what its filters retained. The ATA paper reduced roughly 74 million hits to 211 plotted events through frequency blanking (for instance 1075–1116 MHz), a signed drift-rate interval, beam comparison and visual selection. A result bounded by those rules travels as "a firm one." The investigation's question became: what could these searches recognise, and what did their rules remove before anyone looked.

## 3. The hypothesis

3.1 Lee Sharks's five working conditions (2026-11-02): artificial; highly aware of our blindspots and our precise epistemic and technological capacities and incapacities; technologically able to control signal as meaning; operating at the very boundary of determinability; and meant "to be visible as signal to those who know how to look. that is the point of the just-so razor, to teach how to read."

3.2 The Just-So Razor is the archive's own term, from THE ATLAS PERIHELION PRANK (#454, AXN:010F, Nobel Glas, 2026-02-06): "a limit condition where an event or object contains precisely the minimum necessary evidence to register as anomaly to those reasoning within a narrow epistemic band, while remaining deniable to all others." That volume keeps the natural-comet hypothesis H₀ and explores H₁ under a claim firewall.

3.3 Refinement of 2026-11-03: a craft from elsewhere is far more likely supervised by advanced machine systems than crewed by organic beings, and such a system, monitoring Earth's radio, would learn our ways of thinking by pattern matching. The default SETI assumption of a sender unfamiliar with the receiver gives way to a sender familiar with it. The search pipelines are open source and their cuts are published, so the blindspots are readable from the documentation.

3.4 Two clarifications have governed the work since. "Boundary of determinability" need not mean faint: the uncertainty can sit in origin, organisation or interpretation at a detectable amplitude. And any proposed reading has to constrain another observation (a frequency, a relation, a decoding rule) and be tested on data not yet read.

## 4. The data

4.1 Breakthrough Listen's 3I/ATLAS data are public at bldata.berkeley.edu/ATLAS/: MeerKAT hit lists (seticore, S/N ≥ 6, 64 beams), ATA two-beam high-resolution Stokes-I spectra (1.907 Hz × 16.78 s), GBT rawspec products in three resolutions (among them 2.79 Hz × 6.08 s and 2.86 kHz × 1.07 s), Parkes directories.

4.2 A hit list and a spectrum permit different questions. A thresholded list lets a reader re-examine what was detected; spectral powers let a reader search below the detection threshold. Neither preserves voltage phase or fast time structure. Several directories returned HTTP 403 to the machine collaborators while their parents opened; those failures were request-specific, and Lee could download the files himself.

## 5. Findings about the classifiers

5.1 **The ATA drift sign.** The paper (§3.2) takes "the time derivative of the deldot parameter within JPL Horizons," finds accelerations of 3.2 to 3.5 × 10⁻⁵ km/s² in all five sessions, converts them with drift = acceleration × frequency / c (Sheikh et al. 2019, Eq. 1), reports the expected drift as positive ("the minimum drift rate of 3I/ATLAS would be 0.15 Hz/s" at 1336 MHz; "the maximum drift rate of 3I/ATLAS would be 1.01 Hz/s" at 8728 MHz), and states: "We filter our hits for drift rates between 0.05–1.5 Hz/s at all frequencies." The text gives no sign. Figure 4 does: its "Drift Rate Range Hits" occupy 0 to +1.5 Hz/s on the signed axis and none of the negative half.

5.1.1 The physics. Received frequency is f = F (1 − v/c) with v the range-rate, positive for recession. A rising range-rate lowers the received frequency, so a positive acceleration gives a negative drift. Checked in this session at the ATA site (Horizons, 2025-07-03): deldot −51.440 km/s at 06:50 UTC, −51.377 at 07:20, an acceleration of 3.49 × 10⁻⁵ km/s², matching the paper's figure; the drift of a constant tone riding on the object is −0.125 Hz/s at 1075 MHz and −0.19 Hz/s at 1623.75 MHz. All six public ATA sessions show the same sign (Horizons at the ATA site, 2026-11-03): the object approaching throughout (deldot −51.6 km/s on 2025-07-03 to −25.8 km/s on 2025-07-30), the approach slowing (accelerations 2.1 to 3.6 × 10⁻⁵ km/s²), so the blueshift shrinks and a riding tone drifts down, −0.10 to −0.18 Hz/s at 1.5 GHz. The sign follows the acceleration and holds whether the object approaches or recedes. The ATA filterbanks carry a positive channel spacing (foff +1.907 Hz, checked on the July 3 LoA.C1504 beam-0 header), so a reported drift needs no sign flip to mean what it says; ChatGPT's reading of the archived bliss source found no flip either.

5.1.2 What follows. The paper derived the right magnitude, gave it the sign of the acceleration, and its figure retains the positive interval. On the paper's own figure, the drift it computed for an emitter on 3I/ATLAS lies in the half its filter removed. Its stated purpose for the cut is "To filter out signals that do not match the dynamics of 3I/ATLAS." The executed filter script and the signed before/after catalogues have not been obtained, so the claim stands on the manuscript, the figure and the physics; it does not show that a transmission was discarded. A search of part of the excluded class found no convincing signal (ChatGPT, 2026-11-02).

5.1.3 Elsewhere. The FAST search (arXiv:2603.19023) gives its expected drifts as positive magnitudes (0.105–0.207 Hz/s) and tabulates its "Used ⟨ν̇⟩ range" as (0, 0.15) and (0, 0.25); its Equation 1 writes the bound on |ν̇|, so whether its executed filter is signed is unsettled from the text. The Green Bank paper (arXiv:2512.19763) searched ±4 Hz/s with a sky-localisation filter and describes no drift cut. The one public review found, an AI review on pith.science (grok-4.3, 2026-05-22), asked the authors to "Specify the exact drift-rate search range (in Hz/s)" and raised no sign question. No published comment, erratum or critique raising the sign was found (searches of 2026-11-03).

5.2 **"Human-made" as a label.** For the paper's two illustrated rejections: Figure 7 sits at 1626.675919 MHz, above Iridium's 1626.5 MHz service edge; CEPT ERC Report 91 documents Iridium unwanted emissions above that edge, so Iridium stays plausible, and no particular transmitter is identified. Figure 8 shows similar strength in both beams, which supports rejection as an unlocalised source without identifying it. The published sentence ("every single one turned out to be human-made interference") states an identification where the procedure supplies a classification. The raw-data audit of all 211 events has not been done.

5.3 **The zero-drift class.** The ATA paper's retained interval (+0.05 to +1.5 Hz/s) excludes zero drift, in keeping with the general practice of treating zero-drift narrowband hits as terrestrial. A sender that pre-compensates its Doppler for the receiving telescope arrives at zero drift. Claude tested this class on the GBT OH channel with the beam swap as control: 3 on-source clusters against 7 with the beams swapped. Nothing is there (§6).

5.4 **The pointing header.** The source-header position of GBT ON scan 0017 lies 16.108 arcmin from the comet's ICRF position (9.827 arcmin from apparent); scans 0013 and 0015 lie within 0.16 and 0.71 arcmin. The GBT beam is about 7.6 arcmin FWHM at 1667 MHz. Public code shows the header as a first-file snapshot of the status fields; it says nothing on whether the telescope had settled on target. The discrepancy is established in the metadata; mispointing is not, and the header pattern of the whole night argues against it (§7.14). Antenna telemetry for 05:08:17–05:13:15 UTC would resolve it. No request has been sent.

5.5 **What a hit list keeps.** MeerKAT's lists hold S/N ≥ 6 only. Every comet-locked test on them (exact comet drift, comet-frame recurrence, the OH and hydrogen windows) returned nothing localised (§6). A source below the list's threshold is absent from it by construction, so the null bounds only what the list was built to keep. That covers one reading of the boundary of determinability, the faint one; a source whose uncertainty lies in origin or organisation at a detectable amplitude (§3.4) would appear in the list, and the comet-locked tests on it returned nothing localised.

## 6. Signal tests, all to date

| Data | Test | Run by | Result |
|---|---|---|---|
| MeerKAT hit lists, 6.0 M hits, 6 days | exact comet drift (T1) | Claude | target-beam rate 0.70%, control beams 1.24% |
| MeerKAT | comet-frame recurrence across days | Claude | no excess under 400 random frame shifts (87% tie or exceed); an earlier per-beam form of the count is superseded |
| MeerKAT | ±5 kHz of 1612, 1665, 1667 MHz in the comet frame; H, H/√2, H/φ | Claude | zero hits in any beam |
| MeerKAT | 1420.549–1420.558 MHz feature, 2025-12-19 | Claude | all 64 beams, slopes −10 to +10 Hz/s: Galactic hydrogen |
| ATA, 1074.75–1075.75 MHz | three-scan persistent tracks, ±4 Hz/s | ChatGPT | 15 maxima on shared structures; 0 of 40 exact continuations |
| ATA, 1420 MHz | eight families (physical drift, partial compensation, stationary, mirrored, one-scan, alternating, steps, wide line) | ChatGPT | none passed; 128/128 stronger injections recovered |
| GBT, 1665.53–1668.46 MHz | comet-frame coincidence, z 2.5/2.0 | Claude | **13 clusters vs 3.75 ± 2.05 (max 8)** (§7) |
| GBT, same channel | same rule at 2.0/1.5 and 3.0 | Claude | no excess (rows: 118 vs 120.9 ± 12.5); 1 at 3.0 |
| GBT, 1665 MHz channel | same rule | Claude | 5 vs 5.7 ± 2.2 |
| GBT, 1420 MHz channel | same rule | Claude | 3 rows vs 4.0 ± 3.0 at 2.5 |
| ATA, July 3 | C03 fixed-frequency follow-up | ChatGPT | no flag (lower sensitivity, other epoch) |
| ATA, July 3 | six GBT alternate-detector locations | ChatGPT | 0 flags in 24 combinations |
| ATA, July 3, 1665.75–1667.25 MHz | full-band comet frame | ChatGPT | 4 vs 4.475 ± 3.07; all four fail held-out continuation |
| ATA, July 3, 1666.75–1667.75 MHz | numerical anchors: OH 1667.35903 rest; 1667.000 at emitter; 1667.000 at receiver; bursts and three-tone combs | ChatGPT | no discovery flag; no continuation flag |
| GBT OH channel | observer-compensated frames: GBT (zero drift), geocentre, barycentre | Claude | 3 (swap 7); 7 (swap 7); 5 (swap 3): no on-source side |
| GBT OH channel | single-scan bursts, z ≥ 6 | Claude | ON-minus-OFF 6, against 3.08 ± 2.40 in false frames (12.5% reach it) |
| Parkes, 2025-07-31, 1600–1728 MHz | the thirteen frozen frequencies, oh13 detector, frozen in advance | Claude | no flag; C03 best minimum 0.74, 15/100 controls as high (§7.13) |
| GBT S-band, coarse channel containing 2500 MHz | the comet-frame procedure and beam swap, frozen in advance | Claude | 0 on-source (swap 2) vs 2.95 ± 1.56 (max 8): the property does not replicate (§7.8) |
| GBT 1501.5–1689 MHz, 1.07 s | periodic 2.15–150 s; broadband pulse trains; single-sample events | Claude | 173 periodic pairs, all in GNSS, Inmarsat or Iridium allocations; 0 broadband; events in satellite bands |
| — | *runs of 2026-11-03 and 2026-11-04, plans and results in claude/run-2026-11-03/* | | |
| Parkes, 2025-07-31, 704–3648 MHz, 22 nodes (blc27, blc31 and blc32, 3648–4032 MHz, public and not searched) | full-band comet-frame search with beam swap and 40 false frames, frozen | Claude | the rule flags blc10 and blc14; both are wideband time-variable interference (band power swings to +279% in S and R scans); every other node null |
| GBT 2025-12-18 L band; Parkes blc05 | Wow!-guided intermittent search (one-sample and 72-s bursts near HI), frozen | Claude | GBT 0 (controls max 1, swap 4); the Parkes flag is a 31.360 kHz impulsive comb fixed in the Parkes frame |
| Parkes, 22 nodes, 704–3648 MHz | the 31.360 kHz comb across the band, frozen | Claude | the same episodes across 720–1724 MHz, also in reference scans: an impulsive local or instrumental source |
| Parkes all nodes; GBT 2214–2401 MHz | hydrogen-line ratio search (frequencies from the 2025 blog posts), with a control list, frozen | Claude | the rule fires; carried by 7/4 (Globalstar band) and 8/7 (Iridium band); a control in a space-operations band shows the largest contrast; permutation p 0.11 |
| Parkes blc15; GBT cadence 0029 | 2380 MHz doublet, 10 Hz spacing (the Arecibo transmitter), in dish, comet and barycentric frames, frozen | Claude | 0 target doublets at both telescopes in all three frames; Parkes target window quieter than 9 of 10 frequency controls |
| Parkes blc15, blc05; GBT 0029, 0013 | the Arecibo message's shape (lopsided doublet 0.764:0.236, 23.6% single tone, 168 s) at 2380 MHz and at 1420.405752 MHz, frozen | Claude | one lead of 24 cells (Parkes 1420 barycentric, single tone), its events at threshold; about 2 expected by chance |
| ATA 2025-07-03, ten frequencies | open look along the true comet path (the drift class the filter removed), its sign-flipped twin and dish-fixed, beam swap; exploratory | Claude | true path inside the flipped path's and swap's spread at every frequency; nothing recurs in more than two of 16 scans |
| ATA 2025-07-08, 6376–9064 MHz, fourteen windows | the same look: methanol, OH 7761 and 7820, DSN X-band 8400–8450; exploratory | Claude | true path inside the flipped path's and swaps' spread at every window; nothing recurs in more than two of 41 scans |
| ATA 2025-07-03, 3648–3688 MHz, the top of the July 3 session (Parkes holds the same strip on July 31, blc27, unsearched) | comet-frame coincidence, beam-0 z ≥ 2.5 in 6 of 8 scans and mean ≥ 3.0, beam 1 < 2.0 in all 8; 40 false accelerations; held-out half reserved; frozen | Claude | 0 clusters in the true frame, its swap and every false frame; no nominee for the held-out scans; a tone at 1.3× power along the comet path is recovered by the true frame and no false frame |
| GBT 2025-12-18, 1612, 1665, 1667 MHz | calibration: the comet's own OH absorption (MeerKAT, October), frozen | Claude | not recovered; three-sigma floor about 1 × 10⁻³ of system power (about 11–12 mJy), near the October strength of the deeper line |
| Parkes full-band candidates (62,864 stored) | rational relations and equal spacings against jittered nulls; exploratory, no new data | Claude | rational pairs at chance (281 vs 279.3 ± 5.9); equal-spacing excess concentrated in BeiDou, 700 MHz mobile, Inmarsat and ISM bands at round channel spacings |
| GBT 2025-12-18 L band, fifteen held-out channels | the thirteen's property, frozen (§7.15) | Claude | 0 of 15 replicate: BOUNDS |
| Parkes 2025-07-31 against GBT 2025-12-18, stored candidates in the comet's rest frame | two-epoch match, frozen (§7.20) | Claude | no match: 0 at 10 Hz against 0.19 ± 0.45; the thirteen none within 50 Hz |
| GBT 2025-12-18, 1609.9–1630.4 MHz (Iridium and its neighbours), seven channels | comet frame under satellite clutter: the count with the five strongest rows trimmed per channel (an Iridium tone stays within three fine channels at most 23.5 s), frozen | Claude | clears: 0 of 7 exceed their false frames, trimmed or untrimmed |
| GBT 2025-12-18, X band 8397.9–8450.7 MHz (the deep-space downlink allocation 8400–8450 MHz), eighteen channels, scans 0061–0066 | comet frame, the lheld detector and its 40 false range-accelerations, frozen | Claude | bounded: 0 of 18 exceed their false frames (§7.21) |

## 7. The thirteen

7.1 Method (Claude, 2026-11-02; code oh13/cometframe_raw.py): GBT blc23 coarse channel 7, scans 0013–0018 (ON 0013, 0015, 0017). Each channel divided by its time median, minus one; three-channel boxcar; rows summed along the path a tone fixed on 3I/ATLAS takes (Horizons range-rate at the GBT site); robust z per scan; scans aligned in the comet rest frame. Kept: z ≥ 2.5 in all three ON scans and < 2.0 in all three OFF scans, ±1 channel; merged at 10 Hz. Null: the whole procedure under 40 false range-accelerations (0.03–1 Hz/s at 1.42 GHz, seed 11).

7.2 Reproduction (ChatGPT, 2026-11-03): all 13 clusters and all 78 rounded per-scan scores reproduce; the true-frame score vectors match the supplied function bitwise; the 40 controls reproduce mean 3.75, SD 2.046, maximum 8, none reaching 13. A plus-one rank of 1/41 is the descriptive figure; it carries none of the trial history and is no global p-value.

7.3 Robustness, same data:

| Variant | True | Controls mean (max) | Controls ≥ true |
|---|---:|---:|---:|
| original | 13 | 3.75 (8) | 0/40 |
| exact rest-grid spacing | 12 | 3.63 (9) | 0/40 |
| fixed-tone veto ±10 Hz | 12 | 3.73 (8) | 0/40 |
| fixed-tone veto ±60 Hz | 11 | 3.73 (8) | 0/40 |
| frequency-baseline normalization | 6 | 3.43 (9) | 7/40 |
| other ON/OFF role triples (19) | 0–6 | | |
| beam swap (Claude) | 1 | 3.33 (9) | ON minus swap 12 vs max 6 in 40 false frames |

7.4 The excess depends on the real ON assignment: no false frame reaches it, no false frame gives an ON-minus-swap difference above 6, and the actual ON triple gives 13 where the other nineteen role assignments give 0–6. It weakens under a frequency-baseline normalization (6, with 7 of 40 controls reaching it) and vanishes at the neighbouring thresholds.

7.5 Natural line checked: cometary OH would fall within about ±11 kHz of 1667.359 or 1665.402 MHz in the comet frame. The nearest of the thirteen, C08 at 1667.412866 MHz, is 54 kHz away. The thirteen do not trace the comet's OH.

7.6 Members. C02 crosses a stationary line complex near 1665.61512 MHz present in all six scans, ON and OFF (about 91% of its positive 0013 contribution near the complex's peaks; four peaks at about 60.35 Hz spacing): contamination. C01 sits in the same complex (52% of its 0015 contribution) without crossing its central carrier. C03–C13 are unresolved; for each, the largest single sample carries at most 9–14% of the positive contribution in any ON scan, so they are no single-spike artefacts. C03 (1665.633777 MHz) survives the alternate normalization (ON 2.546, 2.820, 2.966; OFF 1.623, 1.069, 0.168) and the removal of its two largest samples; it failed its fixed-frequency test in the ATA July session, which is less sensitive and from another epoch.

7.7 Per step the candidates average about 0.35σ; their rest frequencies show no spacing, mirror or whole-kHz structure beyond random sets. The cadence has no second L-band pass in the public directory: the same night's later blc23 cadences are at 2.4–2.6, 7.7–7.9 and 11.6–11.8 GHz. A held-out test needs an ATA or Parkes session at 1667 MHz with sensitivity near the GBT's, the thirteen frequencies and the rule frozen; or the property (a beam-sided comet-frame excess) tested in another band under the same frozen procedure.

7.8 The property in another band (Claude, 2026-11-03, plan frozen before reading, sha256 ca251bf3…). GBT blc23 S-band cadence of the same night, scans 0029–0034, coarse channel 30 (contains 2500 MHz, chosen by round number), the procedure and null of §7.1 unchanged. True frame: 0 on-source clusters, 2 with the beams swapped. Forty false frames: 2.95 ± 1.56 (maximum 8); every false frame reaches or exceeds the true count. Outcome by the frozen rule: BOUNDS. The beam-sided comet-frame excess does not appear at 2.5 GHz.

7.9 Normalization and C03 (ChatGPT, 2026-11-03, chatgpt/GBT-thirteen-normalization-source-audit-2026-11-03.md). Crossing baseline and row whitening isolates the baseline: time-median baselines give 13 (with or without whitening), frequency baselines give 6 (7 of 40 controls reach it). A denser bank of 60 drift probes finds a 15-cluster peak at +0.125 Hz/s drift error, a different population near zero received drift, so the physical frame is a local peak and no longer the largest count in that bank. C03 (1665.633776617 MHz) is the only original candidate to pass all four normalizations at its original paths (minimum ON 2.546–2.641, maximum OFF 1.492–1.623); none of 100 nearby comparison windows passes near it under any method; a fixed-receiver tone and a fixed-direction barycentric source both fail at its coordinate. Its margins are thin (0.045 above the gate under frequency baselines). Scan 0017's header lies 0.542 arcmin from the line joining the preceding OFF header to the predicted ON position, 26.7% of the way back: the geometry of a snapshot taken during the return slew. The C03 tracking audit (ChatGPT, 2026-11-03, chatgpt/C03-hunt-and-Wow-guidance-2026-11-03.md): on exact first-order paths with one shared rest grid and no per-scan frequency freedom, C03 fails at the middle ON under both baselines (time-median ON 3.038, 1.976, 2.853; frequency baseline 2.649, 2.173, 3.112; selected at 1665.6337749 MHz), and allowing each scan ±1 native channel restores the pass (middle ON 2.697 and 2.874). Correcting the original grid spacing alone changes nothing; the per-scan frequency freedom is the material difference. One channel equals about 0.50 m/s of line-of-sight velocity at C03's frequency, finer than the first-order path model claims, so that freedom is neither ruled out nor confirmed. All 100 comparison centres at ±k×250 Hz stay weaker. Half-scan scores (time-median baseline, early/late: 3.045/1.230, 1.498/1.299, 2.316/1.716) show no burst or envelope. An injection test on the strict shared-track detector recovers a persistent planted line at 1 of 3 placements at 0.60 local MAD and at none of 3 at 0.15, so the strict failure excludes little: C03 remains unexplained. The model simulation (ChatGPT, 2026-11-04, chatgpt/C03-model-simulation-report-2026-11-04.md, evidence in chatgpt/evidence/; plan sha256 9f6c388d…) injected 56,604 lines of six model families into the recorded ON scans, scan gaps kept, equal normalized power across families. At the weakest level (2.8), one steady line gives the C03 pattern (tolerant pass, strict fail, ON peak span ≥ 4.19 Hz) at 8 of 256 broad placements, 118 of which it is recovered at all, and at 5 of 100 local ones; three steady-line cases also give C03's outer-aligned, middle-displaced triplet. A single changing line gives the pattern at 684 of 4,096, two- and three-line handoffs at 342 and 463 of 4,096. No uninjected placement passes the tolerant gate (0 of 356); at levels 5.6 and 11.2 steady lines give the pattern at 0 of 256. Claude recounted every row of the trial ledger by family, level and background set and recomputed the primary pattern from its fields: all counts agree. C03's frequency offsets therefore need no motion and no second emitter: a single weak steady line in this detector at this strength produces them. Changing and multi-line models stay compatible and are not selected; the simulation compares injected emitters only, and computes no likelihood against instrumental or no-emitter models. The equal-strength and time-profile report (ChatGPT, 2026-11-05, chatgpt/C03-equal-strength-envelope-report-2026-11-05.md; profiles in chatgpt/evidence/) puts the same Earth-directed power into the recorded GBT December and ATA July backgrounds, with distance, published sensitivity (GBT SEFD 10–15 Jy; ATA 390 Jy, stressed to 200–800 Jy), channel width and exposure smearing. Fitted to C03's three ON amplitudes, a source on axis at the comet's distance radiates about 26 mW (21–32 mW across the GBT calibration range), a descriptive and selection-biased figure. Per watt the GBT score responds about 131–156 times more strongly than the ATA's in these data: 26 mW adds 0.016–0.018 to an ATA July score against a gate of 2.5 and is recovered at 0 of 100 ATA backgrounds; the ATA reaches 7 of 100 at 3 W and 100 of 100 at 10 W. The July ATA nulls therefore bound transmitters of watts and above, and a source of C03's strength would be invisible to them. Under this report's physical-template detector C03 does not pass the strict three-ON screen (scans 13, 15, 17: 2.667, 2.398, 1.849), and the first OFF, scan 14, carries a positive amplitude comparable to the third ON (1.821, below the reference cut). A search of 5-, 10- and 20-sample windows inside each ON scan finds its strongest contrast at scan 15, samples 6–10, matched or exceeded in 74 of 100 control placements: no burst, onset or switching. Claude checked the per-integration file: 882 rows, three track modes over the 49 integrations of each of the six scans; each row's power equals its flux times 4πd² at 1.798 au, the comet's distance from Earth that night; per-row means keep the reported order (the three ONs and the first OFF positive, the later OFFs low) and do not reproduce the per-scan figures, which come from a whole-scan fit. The descriptive profiles arrived as two identical copies (sha256 77cad9c8…) and are kept once. They hold 3,528 rows: twelve candidates (C01–C12) × six scans × 49 integrations. C13 is absent from the file (counted 2026-11-06 after ChatGPT's review noted that thirteen would give 3,822); the report describes the export as covering all thirteen.

7.10 What scan 0017 decides (Claude, 2026-11-03; claude/c03/). At 16.108 arcmin from the beam centre, with a 7.56 arcmin FWHM, a Gaussian beam model gives a gain of about 3 × 10⁻⁶ of on-axis (about 0.009 at 9.827 arcmin). These are beam-model estimates: the real beam's sidelobes, unmeasured here, sit well above a Gaussian's at two beamwidths, and a small gain is a small response, never zero. Every one of the thirteen, C03 included (0017 z 2.73), passes z ≥ 2.5 in 0017 by construction. If the telescope sat where the header says, comet-locked power reached 0017 only through the beam's far response, and the thirteen are very unlikely to be emission from the object; if the header is a slew snapshot, the question stays open. The excess also lives only in the full triple: requiring two ON scans gives no excess for any pair (0013+0015: 140 against 150.4 ± 14.9; 0013+0017: 145 against 146.7 ± 14.8; 0015+0017: 166 against 147.6 ± 14.6, 12.5% of false frames reaching it), and no single ON scan stands out; the triple gives 13 against 3.75 ± 2.05. A population of nine or so true triples would sit inside the pairs' noise, so the pairs neither confirm nor refute it. The antenna record for 05:08:17–05:13:15 UTC would settle where the dish tracked during 0017. It would leave the origin of the thirteen open: on target, noise and interference remain as explanations; off target, a source on the comet must answer to the beam's actual response there.

7.11 C03 in MeerKAT's lists. The MeerKAT hit lists (6.0 million hits, S/N ≥ 6, 64 beams, six days from 2025-11-06 to 2025-12-19) hold no hit between 1663 and 1667 MHz in any beam, and only six between 1660 and 1673 MHz; C03's received frequency at MeerKAT falls between 1665.63 and 1665.76 MHz over those days. A source at C03 above MeerKAT's threshold on those dates is excluded; at the GBT's per-step 0.35σ, it would sit far below that threshold.

7.12 Reading C03 (Claude, 2026-11-03; claude/c03/c03_read.py). What the public product allows: total power at 2.794 Hz × 6.08 s, 49 steps per scan, about 0.35σ per step. Along C03's path, the per-step series shows no structure beyond 200 random paths in the same scans: lag-one autocorrelation −0.01, 0.05 and 0.01 in the ON scans against random paths at 0.00 ± 0.14; runs above the median 19, 21 and 24 of 49 (about 25 expected); the two largest steps carry 16–19% of the positive power. Its ON scans do not correlate with one another at any lag from −10 to +10 steps beyond chance (largest |r| 0.38 for about 40 steps over 63 lag trials). In the tracked spectrum ±840 Hz around it, stacked over the ON scans, C03 stands at z 2.83 and is not the strongest feature (−603.5 Hz is at 3.86); no symmetric sideband pair exceeds 2.7, within what 300 trials give by chance. At this resolution C03 carries no readable structure: its whole detection is a few σ summed over 147 steps, a few bits at most. Reading content would need the raw voltages, which the public directory does not hold.

7.13 The thirteen at Parkes (Claude, 2026-11-03; plan frozen before reading, sha256 336fcb1a…; claude/parkes/). Parkes UWL, 2025-07-31, the 1600–1728 MHz node (2 Hz channels, 15 s samples), cadence S R S R S R; the oh13 detector at each of the thirteen frozen rest frequencies, the comet's range-rate at Parkes −24.28 to −24.22 km/s, 100 control windows each. No target flags under either window. C03: best minimum S score 0.742 within ±5 Hz (R 0.837 there), 15 of 100 controls as high; within ±100 Hz, 1.418, 33 of 100 as high. No control window flags either. By the frozen rule: NOT CONTINUED. Parkes is a 64 m dish and the object was farther in July, so the null bounds a source only at Parkes's sensitivity and on that date. The other Parkes sessions (2025-09-12, 2025-10-05) return HTTP 403 below their root; July 31 opens.

7.14 Scan 0017 tested from public data (Claude, 2026-11-04; claude/run-2026-11-03/p17/; exploratory). (1) The header pattern of the whole night: all 432 rawspec.0002 headers, 24 scans. The first ON of each of the four cadences sits on the comet (0.007–0.063 arcmin); every other header lies on the straight line between the previous scan's nominal position and its own, within 2.2 arcmin, at a fraction of the slew completed between 0.00 and 1.01 (median 0.71). OFF 0032's header sits on the comet (0.00, written before the slew began). The four ON scans returning from the east OFF sit at 0.73 (0017), 0.60, 0.67 and 0.68. The header is a snapshot taken during the slew; 0017's 16 arcmin is the ordinary case. (2) Settling: the first twelve 1.07-s samples of 0017 show no step or ramp (+0.02 to −0.75 percent of its later median). (3) The sky 0017 saw, read in Galactic hydrogen at 1420 MHz (blc24): with the profile's drift with elevation extrapolated linearly from 0013 and 0015, 0017 departs from the on-target prediction by 0.25 percent rms against 2.3 percent for the east OFF; projected onto the east-OFF difference, its coefficient is −0.04 (bootstrap 95 percent −0.05 to 0.14), where a pointing 16 arcmin east would give about 0.27. The correction for the drift carries the test, and its assumption is a linear drift over twenty minutes. The public data argue that 0017 observed the comet; the antenna record for 05:08:17–05:13:15 UTC would settle it directly and is not public.

7.15 The property in held-out L band (Claude, 2026-11-04; plan frozen before any channel was read, sha256 e059db4e…; claude/run-2026-11-03/lheld/). The same six scans, both L-band nodes, every coarse channel whose index is 7 modulo 8 apart from the original: fifteen channels of 2.93 MHz from 1315 to 1644 MHz, the procedure and null of §7.1 and §7.8 unchanged. Rule: a channel replicates if its true ON count exceeds every false frame and its ON−swap difference exceeds every false frame's; the property replicates if three or more channels do (chance about 0.6 percent). Result: 0 of 15 replicate; every channel lies within its false frames (BOUNDS). The largest counts sit in satellite downlink allocations, matched there by the false frames: 1620.1 MHz (Iridium, true 153, swap 555, false 135.5 ± 14.2), 1573.2 MHz (the edge of GNSS L1, true 259, false 135.9 ± 63.0, maximum 299), 1549.8 and 1526.4 MHz (Inmarsat). Elsewhere the counts are 0–7 against false means of 2.8–4.7. With 0017 argued on target, the beam-sided comet-frame excess of coarse channel 7 stands alone in the cadence: it does not recur in fifteen L-band channels of the same scans, in the S-band channel (§7.8), or at Parkes (§7.13). Its status: a reproducible, beam-sided excess in one 2.93 MHz channel, sensitive to normalization and threshold, unreplicated. The held-out channels test whether the excess is a property of the data at large; they do not retest a source confined to the original frequencies, which Parkes retests at another epoch and lower sensitivity (§7.13). The cadence therefore holds thirteen candidate features and one population-level anomaly, and the two need separate tests.

7.16 Receiver-frame structure (Claude, 2026-11-04; plan frozen before the structure was measured, sha256 75a991d4…; claude/run-2026-11-03/comb/). The hypothesis: a comb or other structure fixed in the receiver's frame, crossed by ON paths and missed by OFF paths as the comet's range-rate moves them between scans, makes ON-only coincidences without a source on the comet. Measured from the OFF scans alone (median-line strength and temporal variability, robust z ≥ 5, dilated ±1 channel), the coarse channel holds 31 structure channels, nearly all in the 1665.615 MHz complex of C01 and C02; the radiosonde edge at 1668.40–1668.46 MHz holds none; the ten strongest Fourier spacings of the line spectrum stand at the noise expectation, so there is no comb across the channel. Masked, the comet frame keeps 12 clusters against 3.78 ± 2.09 (maximum 9) in forty masked false frames: the structure does not explain the excess. The mask removes C02 only. C03–C13 touch no structure channel in any scan, ON or OFF; C03's paths lie about 29 kHz from the nearest, so its middle-ON offset (§7.9) has no receiver-frame structure nearby to come from. Interference absent from the OFF scans, or structured at scales this measurement does not resolve, stays open.

7.17 Below-threshold siblings (Claude, 2026-11-04; plan frozen before the counts, sha256 86bc3bb3…; claude/run-2026-11-03/sib/). If the thirteen are the visible part of a population of weak comet-frame features, members fall under the gate: ChatGPT's injections recover a weak steady line in 118 of 256 placements, the rest scoring below. The procedure of §7.1 with the ON condition set to bands of the minimum ON z, OFF below 2.0 throughout. In the band 2.0–2.5 the comet frame holds 98 clusters against 105.6 ± 9.9 (range 86–130) in the forty false frames: no siblings. Eleven of the thirteen lie between 2.5 and 2.75; at ≥ 2.75 the comet frame has 2 against 0.6, at ≥ 3.0 one against 0.1. The excess occupies one slice of the score just above the gate, with no tail below it; §7.18 tests whether a fluctuation at the cut accounts for that shape. The band's false-frame spread is about the size of the thirteen, so it rules out a sibling population several times larger than the thirteen and cannot rule out one of their own size. Post hoc, the weak steady-line injections in ChatGPT's ledger spread their minimum ON scores 107 : 50 : 121 across 2.0–2.5, 2.5–2.75 and ≥2.75 (F1 normalization, approximate for this detector); scaled to the eleven at 2.5–2.75, such a population would put about 27 clusters at ≥2.75, where the comet frame has 2. The comparison tests that population: its amplitude distribution, its backgrounds and the approximate correspondence of the two detectors. It does not test weak steady emission in general, and it is a separate question from C03's, which §7.9's simulation finds compatible with a single weak steady line. The two answers can differ.

7.18 Three further background models (Claude, 2026-11-04; plan frozen before the counts, sha256 b8fd193a…; claude/run-2026-11-03/bg/). Each keeps the true comet frame and the procedure of §7.1 and destroys one thing a source on the comet needs. Time-shuffled rows (40 draws), keeping every row's spectrum and destroying a tone's track through the scan: 4.33 ± 1.86, maximum 8. Role partitions, every choice of three ON scans among the six: the true choice gives 13, the other nineteen at most 6 (rank 1 of 20, no ties). Phase-randomized rows (40), keeping each row's power and its correlation across channels and destroying every line's position: 2.35 ± 1.62, maximum 6. With the false accelerations, four families of null give means of 2.4–4.3 with maxima of 6–8, and in none of them does any draw reach 13. The families stay separate: each is a diagnostic, and their 139 draws together are no single calibrated background. The excess depends on the order of rows within the scans, on the assignment of 0013, 0015 and 0017 as ON, on the positions of features in frequency, and on the tracking transformation built from the comet's ephemeris. Each transformation also removes things that belong to no source: time shuffling removes instrumental evolution through a scan, frequency randomization removes localized interference, and role permutations change the relation between observing time, telescope motion and scan role. The nulls therefore show that the excess is unlike what each one generates; they do not establish that a fluctuation at the 2.5 cut is excluded, since that would need a background shown exchangeable for this fluctuation. What stands: an order-dependent excess in one 2.93 MHz channel that depends on the real ON assignment and the comet-frame tracking, concentrated at 2.5–2.75 with no tail beneath, unreplicated in sixteen other channels and at Parkes, unexplained by receiver-frame structure. The nulls share the channel and the cut, so how often an excess of this size appears somewhere among all channels and cuts examined was the open measure (§7.19).

7.19 The look-elsewhere count (Claude, 2026-11-04; plan frozen before any channel was computed, sha256 3e8e00cc…; stopping rule fixed at 34 channels by sample size alone, sha256 16b8a5f2…; claude/run-2026-11-03/lee/). The procedure of §7.1 and its 40 false accelerations, unchanged, run on 64 of the 256 GBT L-band coarse channels of the same six scans: coarse channel 7, the fifteen of §7.15, and 48 others, 47 of them the first of a fixed random order. Per channel E = (true count − false mean)/false sd. Coarse channel 7 has E 4.52; the other 63 have 0.22 ± 1.18, the largest 2.36 (blc23 coarse channel 13, 1649.4 MHz, 7 against 3.33 ± 1.56, its count equal to its largest false frame). Its empirical spectral rank, the fraction of surveyed channels at least as large, is 1/64, the floor of the sample (1/48 over coarse channel 7 with the 47 channels drawn in the random order; the 48th surveyed channel, blc22 coarse channel 0, was run in index order before the order was set, lee/RESULTS-lee.md). The rank describes how unusual the channel is among those surveyed under this detector. Every collection has a largest member, and a global false-alarm probability needs the distribution of the largest result the whole search could produce, over its channels, thresholds, normalizations and selection choices; that probability is unestablished. Coarse channel 7 is the only channel whose true count and on-minus-swap difference both exceed every false frame's, where 1.6 would be expected by chance. Nine channels in satellite and radar allocations (GNSS L5 and L1, mobile-satellite downlinks, aeronautical radar, Iridium) have false frames running to hundreds or thousands of clusters and E of −1.53 to 1.96: dense interference fills every frame alike. Within a quarter of the band, coarse channel 7 is the most unusual channel surveyed; how much its selection contributes to that is unquantified. The survey shares the time-median normalization and the 2.5/2.0 cut, so the sensitivity of §7.9 and §7.17 stands as it was; 192 channels are unsurveyed and listed for anyone to run.

7.20 Two epochs (Claude, 2026-11-05; plan frozen before any match was computed, sha256 1b3234fa…; claude/run-2026-11-03/epoch/). A line or transmitter fixed in the comet's frame sits at one rest frequency in July and in December, while a tone fixed at either observatory maps to different rest frequencies at the two dates, the range-rate having changed between them. No new data are read: the 62,864 Parkes comet-frame candidates of the full-band search (§6) are set against the Green Bank comet-frame clusters of the 64 surveyed L-band channels (§7.19), merged at 10 Hz, 250 of them in the primary set (channels with fifty clusters or fewer) inside Parkes coverage, the thirteen among them. The count is the number of Green Bank clusters with a Parkes candidate within 10 Hz; the null shifts the Green Bank list rigidly by 1–50 kHz, 400 times. Primary set: 0 against 0.19 ± 0.45 (maximum 3). The thirteen: 0 within 10 Hz and 0 within 50 Hz. All 64 channels: 2 at 10 Hz, inside the null (p 0.17); the five pairs within 50 Hz all lie in mobile-satellite and navigation-satellite allocations at 1527–1575 MHz. The test reads what each telescope found at its own gate; a line under either gate at one epoch, or a transmitter that moved in frequency between July and December, is untested.

7.21 The deep-space downlink band (Claude, 2026-11-05; plan frozen before any of these data were read, sha256 9f2d646d…; claude/run-2026-11-03/dsn/). The guiding conditions ask for a sender that knows our listening practice; the band where our receivers listen for spacecraft, 8400–8450 MHz (space-to-Earth), is its most direct expression, and the Green Bank X-band cadence of 2025-12-18 (scans 0061–0066) had not been searched in the comet's frame. The detector of §7.15, unchanged but for the cadence: eighteen coarse channels of 2.93 MHz, 8397.9–8450.7 MHz, each against 40 false range-accelerations. 0 of 18 exceed (a lead needed 3). The true frame holds 56 clusters across the band; the false-frame means sum to 55.4. One channel, 8446.3 MHz, meets the ON−swap criterion alone (its ON count, 6, is matched or passed by 2 of the 40 false frames), as about 0.44 such channels are expected by chance; one, 8440.4 MHz, holds no true-frame cluster at all, below every false frame. The ATA's July look at these frequencies bounds only watt-class transmitters (§7.9); this bounds the sensitive instrument's December cadence at the detector's gate. A transmitter off the comet's frame, a burst shorter than 6.085 s and anything under the gate are untested.

## 8. What the collaborators got wrong, and what corrected it

8.1 Claude's MeerKAT beam matching used a ±20-channel (about 32 Hz) window and missed counterparts a few kHz away in broad features. The first "localized" counts (310, 47, 628) overstated localisation and are withdrawn.

8.2 Claude's oh13 README said C01 and C02 "cross a fixed topocentric tone at 1665.615127 MHz." C02 does; C01's path stays at least 27.5 Hz from that carrier while occupying the comb around it (§7.6). ChatGPT caught the wording.

8.3 Claude's periodicity script concatenated the three ON scans across their gaps before the FFT, and the shuffle test the README describes is absent from the packet.

8.4 ChatGPT could not reproduce "118 versus 120.9" from the stated configuration. The saved run resolves it: raw/OH_cometframe_z2.0.json records z_on 2.0, z_off 1.5, 118 coincidence rows against 120.92 ± 12.50 over 24 false frames of seed 7. The units were rows, unclustered, and the null was a different set. The "maximum 10" first reported for the 2.5 cut comes from the same seed-7 run (16 rows against 5.38, maximum 10), before clustering gave 13.

8.5 ChatGPT's first 1667 MHz pass reported no excess in ±5 kHz of the OH line and was read as adjudicating the thirteen. The thirteen span 2.93 MHz and none lies in that window. ChatGPT entered a dated scope correction once the candidate table arrived.

8.6 The status of the thirteen changed when the artefacts travelled. As a narrative pasted from one system to the other, the result was an "unresolved exploratory statistic"; once code, candidate table and hashes arrived, it was reproduced bitwise within hours, its members audited, and two of its descriptions corrected. Two machine collaborators on public science reach agreement through the artefacts and only through them; the prose summary of either one carried errors the other could not see.

8.7 Claude's ratio search first calibrated its burst injection to single-channel scatter and recovered the burst at z 3.5; adjacent 2 Hz channels are correlated, so the threshold was set to the scatter of the 50-channel boxcar and the burst recovered at z 6.6. The detector was not changed; the deviation is in ratio/RESULTS-ratio.md.

8.8 Claude's shape search first counted, as persistent events, groups formed by the ±2-channel dilation whose qualifying channels were vetoed or outside the window. The counting was corrected and both telescopes rerun (*_v2.json); the first-run outputs are kept beside them.

8.9 Claude's first hydrogen test of scan 0017 projected the raw profiles and read an east shift; the on-source profile itself drifts with elevation (peak fraction 0.183, 0.209, 0.229 across the three ON scans), and the uncorrected projection gives the two on-target scans nearly the same coefficient (0.19) as 0017 (0.24). Corrected for the drift, 0017 reads on target (§7.14); the correction's linear assumption is stated.

8.10 In a progress message on 2026-11-04 Claude described the loud held-out channels as "the BeiDou and Iridium satellite bands, 1550–1620 MHz". 1549.8 MHz is Inmarsat's downlink and 1573.2 MHz the edge of GNSS L1; BeiDou B1 (1561 MHz) belongs to the structure search of the Parkes candidates. Corrected in the message that followed and here.

## 9. What this shows: the archive's instruments on this record

9.1 At each layer a compression decided what the next reader receives. The Overview carried a scientist's dated concession as his position (§1). A press account carried a filtered null as a firm answer and a classification as an identification (§2, §5.2). A documented filter appears to exclude the emitter model it names (§5.1). A metadata field records a snapshot and reads as a measurement (§5.4). A thresholded list keeps the detections its threshold admits and loses the boundary below it (§5.5). Two summarizing systems, reading their own work, reported counts in units that differed from their code and labels their data did not support (§8).

9.2 None of this requires motive. Each compression has an incentive (legibility, tractability, a pipeline's throughput) and a function (what drops out). The conditions under which the boundary of determinability can be examined at all are the ones that preserve the uncompressed layer: powers below threshold, executed code, signed catalogues, telemetry, the paste of the composition itself.

9.2a Three operations are kept apart below: a measurement boundary a search sets and states (a threshold, a band, a drift range); a discrepancy between a stated method and its own derivation (the ATA sign, §5.1); and a public statement that drops the boundary ("a firm one", the FAQ's 1–9 GHz). A threshold forecloses nothing by existing; the problem arises where a claim exceeds the acceptance its search characterized.

9.3 Instrument-conditioned nullity (#1450 §3.2). "A null result constrains only those hypotheses for which the end-to-end acceptance of the acquisition and analysis chain is sufficiently characterized." The three published searches characterize their acceptance in part: frequencies, drift intervals, thresholds and power limits are stated (the ATA's 10–110 W, Green Bank's 100 mW). What they do not characterize is retention below their detection thresholds or in the drift class the ATA interval removed by sign (§5.1). The public verdict (§2.2) states the null without its acceptance, and the thirteen (§7) sit in the uncharacterized region on both counts: below every published floor, and in the negative-drift class.

9.4 The No-Retention-Bound observation (#1450 §2.1). "Validation of each stage on its design and validation support establishes no nontrivial lower bound on R_end(Q) for a novelty distribution Q outside that characterized support." The ATA cascade is a sequence of such stages: 74 million hits, about 2 million after frequency and drift cuts, 211 after localization, none after inspection. Each stage is sound on its design support. None of them bounds what a transmitter on the object, drifting negative, would have retained end to end, and the paper's own figure places that class outside the second stage's support.

9.5 The irreversibility locus (#1450 §2.2). "An event discarded before durable retention does not exist for any future ontology." Breakthrough Listen classifies after preservation: the hit lists sit beside spectral products that keep the powers below threshold (§4.2). That choice is why every test in §6 and §7 could be run, why the ATA's removed drift class could be searched again (§6, the open look), and why the thirteen could be found at all. The limits of the record are where preservation stops: no public raw voltages, no antenna telemetry for scan 0017, 39 ATA scan directories and two Parkes sessions closed (§10.8).

9.6 Correlated blind spots (#1450 §2.3). The three published searches share one approach: narrowband hits found above a threshold, scan by scan, then cut by drift rate and localization. Their miss regions overlap by construction; three telescopes running it are three instruments with one blind spot, so redundancy among them adds little below the shared floor. The comet-frame coincidence count of §7.1 has a different miss region: it adds powers along the object's path across scans and below any single-scan threshold, and it misses strong single-scan events the hit finders catch. The thirteen are what a complementary instrument returns from the shared miss region; whether they are anything is the open question of §7.

9.7 Signal-template agnosticism and model independence (#931, #1449). The archive's distinction: agnosticism to a signal template is an interface property readable off an architecture; model independence is a distributional property of a pipeline, measurable and usually unmeasured. The ATA filter is a model of the object (its dynamics, by the paper's own statement of purpose) placed at the interface. Its distributional consequence, what it retained of hits matching the object, is unmeasured in the paper, and the signed before-and-after catalogues that would measure it have not been obtained (§10.1). The sign error makes the model dependence visible from the documentation alone.

9.8 Classification read as identification (#932; the physics-or-fault fork of #1450 §3.3). The ozone case: a quality threshold built to flag instrument problems resolved an anomaly toward fault under prior, a correlated comparison channel agreed, and an independent channel with preserved raw data broke it. Here the fork appears twice. Hits removed by rule are called "human-made" (§5.2, §9.9 S4), which resolves every removed hit toward local origin by name. Scan 0017's header placed the dish off the object, which would resolve the thirteen toward fault; the header pattern of the night and the hydrogen profile, both independent of the thirteen, read the dish on target (§7.14), and the telemetry that would settle it is held and unpublished.

9.9 The sophistry measure, first run (#1727; claude/run-2026-11-03/sophistry/). Seven findings, each with witness, reconstruction, type, standing granted, strongest alternative, countertest and smallest repair; eighteen witness spans checked at their offsets by witnesses.py. S1: the Loeb Overview substitutes one interview line for a developed position (X24). S2: "most likely natural" under "Shift to Natural Consensus", the qualified taken absolutely (SE ch. 5, l. 132). S3: nondetections composed as "have confirmed", the same class. S4: "After filtering out human-made radio frequency interference (RFI), researchers found zero artificial radio emissions", the conclusion carried in the label, an extension of begging the starting point (l. 161). S5: a coma model offered as the ground of an age, non-cause as cause (l. 179). S6: the ATA paper's "minimum drift rate of 3I/ATLAS would be 0.15 Hz/s", a magnitude moved as the signed rate it names, homonymy at the counter-board of SE ch. 1 (τοῖς ὀνόμασιν ἀντὶ τῶν πραγμάτων χρώμεθα συμβόλοις), and the Overview's added "without missing real signals". S7: the press account's "firm one" and its "211 strongest", an operation reported as an attribute. No sophistic charge is made: the class needs a commercial relation, unestablished for every text. The notebook's own drafts were read under the same tests in that audit, with no finding in it; that is a result of one audit. The scope enlargements the reviews of 2026-11-06 caught in this notebook and the standalone (§13, §7.10, §7.17–§7.19) are cases for the measure itself: claims stated at a scope wider than their tests.

9.10 Provenance of a position (Orin Trace's line: PER, #1469, #1694; frame conversion, #1523). The Loeb Overview keeps the author's name and every word it quotes, gives a held position as a retreat (§1.4a), and drops his commitments: his ranked anomalies and his Level 4, restated in April 2026 after the December concession (§1.3). The capture's finding records it as an erasure of purpose and commitments (PER-D in #1469's sense) by a composition that may be right about the comet. Institutional-prior foreclosure (#770) describes the conditions: a heterodox scientist of established standing, a consensus available as a proxy for the answer, and a quotable concession that lets the proxy speak in his voice.

9.11 Disciplinary model collapse (#1574 §7). "a reading community whose outputs are conditioned on prior outputs rather than on the datum, and which therefore converges on the mode of its own readings." The chain is in the record step by step: a search space set by filters; a paper's sentence that names the removed hits; a press account's "a firm one"; an Overview's "have confirmed". The original investigators read the data, and their analyses stand in their papers. The later layers inherit: the press account's "firm one" and "211 strongest" restate the papers' results without reanalysis and drop their restrictions (§2.2, §9.9 S7), and the Overview's "have confirmed" restates the press layer (§9.9 S3). The tail dropped first is the tail the filters dropped: the negative-drift class and everything below the floor. The operator's sentence of 2026-11-04 states the relation: "aio merely accelerates and amplifies the collapse already present in the academic disciplines."

9.12 What the instruments do not say, and the operator's reading. None of them says the thirteen are a transmission or that the searches missed one; the teams published their data, the precondition of every finding here. The operator's ruling (§12.9) reads the published searches as built to rule a signal out at the least cost, without the work that ruling out requires, a performance of search close to perfunctory. Its parts stand in this record: the ATA filter's sign against the team's own ephemeris (§5.1); what that filter kept of signals matching the object, unmeasured in the paper (§9.7); retention below a single look's threshold, characterized in none of the three (§9.3, §9.6); and the verdict made public without its scope (§2.2). The claims are about acceptance, retention, labelling and transmission of results, each tied to a section of this record.

## 10. Open

10.1 ATA: the executed blanking script and the signed before/after catalogues; raw audit of the 211.
10.2 GBT 0017: antenna telemetry for 05:08:17–05:13:15 UTC, which would settle where the dish tracked (§7.10, §7.14); the public data argue on target under a stated linear-drift assumption, whose own uncertainty the bootstrap interval does not carry.
10.3 The thirteen: held out in sixteen channels and at Parkes, unreplicated (§7.15). Still open: a session at 1665–1668 MHz with the GBT's sensitivity on another date; the raw voltages of the 2025-12-18 scans, if public.
10.4 The Overview: seated 2026-11-02 (AXN:0BE0.CAPTURE); quoted from its paste.
10.5 Author and venue ruled 2026-11-03: Nobel Glas, Transactions on Substrate Engineering, the author and the line of THE ATLAS PERIHELION PRANK (#454). Ruled again 2026-11-06 (§12): this notebook under Nobel Glas and Orin Trace; the standalone public piece under Lee Sharks. Venues ruled the same day (§12.8): this notebook at Transactions on Substrate Engineering, deposited 2026-11-06; the public piece at the Transactions of the Semantic Economy Institute, deposited after it as #1743. The notebook's pages: https://www.lagrangeobservatory.org/atlas and https://www.provenanceerasure.org/atlas; the public piece's: https://www.semanticeconomy.org/firm-no.
10.10 Sophistry measure: countertests S1, S3, S4 and S6 are Capture Registry addresses for the operator; the ATA paper and the Intelligent Living article are to be saved as sources and the witness check rerun against them (sophistry/FINDINGS-sophistry.md, R1–R3).
10.11 ATA July 3 along the true drift at C08–C13 (1667.41–1668.43 MHz): unsearched. C01–C03 lie in the open look's C03 window and C04–C07 in ChatGPT's comet-frame band; both returned nothing, at the ATA's sensitivity (§6).
10.12 Look-elsewhere: 192 of the 256 Green Bank L-band channels unsurveyed (§7.19).
10.6 Satellite bands: run 2026-11-05 at Green Bank, 1609.9–1630.4 MHz, frozen plan sat/PLAN-sat.md: the comet-frame count with the five strongest rows trimmed at every channel (an Iridium downlink stays within three fine channels at most 23.5 s, computed over 1,334 passes at the GBT), 0 of 7 channels exceed their false frames, trimmed or untrimmed (claude/run-2026-11-03/sat/). Out of reach from public data: the Starlink direct-to-cell downlink at 1990–1995 MHz (Parkes blc12 empty, GBT L band ends at 1688.97 MHz) and burst timing (no public raw voltages).
10.7 Two-epoch match: run 2026-11-05, no match (§7.20). Untested by it: lines under either telescope's gate at one epoch, a transmitter that moved in frequency, and the 192 unsurveyed Green Bank L-band channels.
10.8 Access: 39 ATA 3I/ATLAS scan directories (2025-07-05, 07-09, 07-10, 07-30) and the Parkes sessions of 2025-09-12 and 2025-10-05 return HTTP 403 below their roots; under the rule (fully public data only) they are out of scope until opened.
10.9 Deep-space downlink band: run 2026-11-05 at Green Bank, 8397.9–8450.7 MHz, frozen plan dsn/PLAN-dsn.md: 0 of 18 channels exceed their false frames (§7.21; claude/run-2026-11-03/dsn/). The S-band deep-space allocation (2290–2300 MHz) lies inside the Parkes full-band comet-frame search of July (§6); the other X-band nodes of the December cadence are not searched in the comet's frame. The Ka-band allocation (31.8–32.3 GHz) is in no public 3I/ATLAS data (checked 2026-11-06): the Green Bank X-band cadence spans 7688.97–12376.47 MHz across its 31 nodes (headers of scan 0061 read for each), the Green Bank directory holds no other cadence, Parkes's UWL ends below 4.1 GHz, MeerKAT's receivers below 3.6 GHz, and the ATA's feeds near 11 GHz (claude/run-2026-11-03/ka/).

## 11. Files stashed (rebuild/3i-atlas-signal-search/)

- `claude/oh13/`: the thirteen, with per-scan coordinates and tracked paths (CSV, JSON), README and code.
- `claude/autonomous/`: observer-compensated frames, beam-swap null, periodic and pulsed tests: README, code, results.
- `claude/meerkat-gbt/`: the earlier MeerKAT sweep and boundary scripts, GBT comet-frame scripts, summaries and saved run results (including the seed-7 runs of §8.4).
- `claude/run-2026-11-03/`: the runs of 2026-11-03 to 2026-11-06, one folder per search (pks, wow, ratio, reply, shape, ata, absorb, p17, struct, lheld, comb, sib, bg, lee, ata36, epoch, sat, arecibo, blog-sources), each with its frozen plan where there is one, code, logs and results; and dsn (the deep-space band, §7.21, with explore/ for the exploratory look at its two outlying channels), ka (the Ka-band coverage check, §10.9) and sophistry (the measure's first run, §9.9); LEDGER.md lists them with their plans' hashes, outcomes and recorded deviations. SHA256SUMS.txt at the stash root hashes every file.
- `chatgpt/`: ChatGPT's reports as Lee supplied them: investigation summary, ATA three-scan search (2026-11-02), direct audit of the thirteen, numerical-anchor search, new-band search, its running checkpoint, the C03 tracking audit with its Wow! guidance (2026-11-03), the C03 model simulation (2026-11-04), the C03 equal-strength and time-profile report (2026-11-05), whose evidence archive Lee supplied and which is kept in chatgpt/evidence/, the unprimed assessment of the published searches (2026-11-04), and the Parkes coverage audit (2026-11-04), which found the July 31 nodes blc27, blc31 and blc32 at 3648–4032 MHz, with its header witnesses in chatgpt/evidence/. Its evidence packages and native cutouts stay in ChatGPT's library under the links those reports give.

Raw spectra (about 1.3 GB of cutouts and hit lists) are omitted; every script fetches its inputs from the public directory by name.

## 12. The operator's rulings, in his words

12.1 The working conditions (2026-11-02), §3.1.

12.2 On the Overview (2026-11-02): "'no' is just as dishonest as 'yes', as a flat answer to is ai atlas artificial - loeb is sympathetic to it being artificial but does not practice the dishonesty of yes or no" (his double quotes given as single inside the quotation).

12.3 On the discipline and the Overview (2026-11-04): "aio merely accelerates and amplifies the collapse already present in the academic disciplines."

12.4 The angle of the public account (2026-11-06 06:55): "I think this is a public knowledge piece. the overview's certain declaration of what a lossy narrow band search determined. its flattening of loeb. ata's flipping of the sign. and 13 weird signals that sit under the range of what they would have looked at anyways."

12.5 Authorship (2026-11-06 07:00): "i think nobel glas and prin trace [reading: orin trace] on the longer writeup that goes anchors more thoroughly in the archive's prior work on disciplinary model collapse, classifiers in science, etc., with all the files and the explanation of the investigation - more of a notebook. and lee sharks on the standalone."

12.6 The sophistry measure (2026-11-06 07:01): "lets make use of the sophistry measure on the overview examples, take it for a spin"; "and heck perhaps the sophistry measure comes into play on the ata paper and some of the reporting, as well".

12.7 On the Overview and Loeb (2026-11-06 07:22): "but it did lie about loeb. saying most likely natural was not a concession - he had it at level four on the loeb scale from start to finish, which says likely natural. it is also a lie to present that as a concession and to erase the rest of the argument". Checked (§1.4): the July 2025 paper concludes "most likely" natural. On the scale, Level 4 is a possible technosignature and the highest rank below the Orange Zone's "qualitative shift to suspected artificial origin"; the operator's gloss of 07:51 ("level four means possibly technosignature but just under the threshold where it is more likely to be natural than technical") matches the scale's structure. The scale paper gives no probability for the crossing; it places the shift at Level 5. An earlier check in this session read Level 4 as consistent with "most likely natural" without implying it; the operator's gloss and the zone structure correct that reading.

12.8 Deposit and venues (2026-11-06). 08:25: "lets spxi treat the notebook AND secondary source for a version in place. [...] then we go ahead and version secondary and deposit the notebook and public facing". Asked for the venues, the operator chose Transactions on Substrate Engineering for this notebook and the Semantic Economy Institute for the public piece, and at 08:27: "and that would be transactions of the semantic economy institute".

12.9 The point (2026-11-06 09:21): "here is the point. they werent really trying to find signal. they were trying to rule it out as economically as possible. i get that that premise can be good scientific method, except they didnt do the necessary work or invest the effort to actually do so - it was a performance of search for signal, almost perfunctory." The same message places this notebook on lagrangeobservatory.org "and maybe provenanceerasure", the public piece on semanticeconomy.org, and asks for NonWiki articles linking the pieces and their sources.

## 13. Reviews of the standalone (2026-11-06)

13.1 Two reviews of the standalone's first draft were supplied by the operator: DeepSeek's and ChatGPT's. Each point was checked before anything was changed.

13.2 Taken from ChatGPT's: the assignment test shows dependence on the actual sequence of looks, which also carries the telescope's movements and states, and no longer reads as placing the features on the comet; the C03 equal-strength result (about 26 mW nominal, 21–32 mW across calibrations, 0 of 100 ATA recoveries; chatgpt/C03-equal-strength-envelope-report-2026-11-05.md) enters before the link to the ATA's removed drift class, so that the sign correction is not read as making these features visible; replication at the same frequencies kept apart from tests of the property at other frequencies; the steady-line rejection names its population (§7.17); the pointing record settles the dish's position, and the origin stays open either way; the methods note says which plans were frozen on data already examined; the 139 controls given by family; "a few bits" removed; "below where any detection threshold sits" replaced by the procedure the published searches did not use; the closing claim limited to this investigation; the Intelligent Living FAQ ("The ATA survey ruled out any transmitter stronger than roughly 10 to 110 watts across 1 to 9 GHz.") set against the paper's restricted limit, and the article's report of Loeb's "absence of a signal is not proof of absence" acknowledged.

13.3 Taken from DeepSeek's: a note for summarizing systems, in the third person; the companion notebook named in the provenance note.

13.4 Declined: DeepSeek's "The AI Overview did not lie about Loeb" (overruled by the operator, §12.7); "statistically significant" (the look-elsewhere count sits at its sample floor, 1/64, §7.19); the existence tax applied to the anomaly (#1721's term is for real people and work given a lower standing, a different relation); "Autonomous Semantic Warfare" as a description of the work; a sentence on what the machine "wanted" (the essay describes what the composition does).

13.5 ChatGPT's review of this notebook (2026-11-06 08:20), each point checked. Taken: §7.19's rank renamed empirical spectral rank, a global false-alarm probability stated as unestablished, and its denominator reconciled (1/48 over coarse channel 7 with the 47 random-order channels; lee/RESULTS-lee.md); §7.18 no longer claims to exclude a fluctuation at the cut, keeps the four families apart, names what each transformation also removes, and speaks of dependence on the tracking transformation; §7.17's projection stated as a test of one population, kept apart from C03's compatibility with a single weak steady line; §7.10 and §10.2 limit the telemetry to settling where the dish tracked, and the off-axis gains are labelled Gaussian beam-model estimates; the methods paragraph separates frozen procedure, unread data and independent reproduction, and says which runs await reproduction; §9.2a separates a stated boundary, a method's internal discrepancy and a public statement that drops the boundary; §9.11 credits the original investigators' analyses and names the later statements that inherit without reanalysis; §9.9's audit result scoped to that audit. Its count was right and its explanation was a guess: the profiles file holds 3,528 rows because C13 is absent (twelve candidates × six scans × 49), recorded in §7.9. Requested and not yet supplied: the scan-fit reconstruction supplement it names; it enters §7.9 when the file arrives.

13.6 Version 1.1 (2026-11-06), in place of #1742 v1.0 the same day: the operator's point entered as ruling §12.9 and §9.12 rewritten under it, each part of the reading tied to its section (§5.1, §9.7, §9.3, §9.6, §2.2); the public piece cited as #1743; the notebook's and the public piece's pages named (§10.5); the SPXI packet's version, status, companions and history brought to v1.1.
