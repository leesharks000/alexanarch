# Assembly Round 1 · Firenze Corpus Reconstruction Workplan

**Substrates in this round:** PRAXIS (DeepSeek), TECHNE (Kimi), ARCHIVE (Gemini), LABOR (ChatGPT), INKLING.
**Artifact under review:** `WORKPLAN.md` v0.1, canonical URL: `https://alexanarch.org/datasets/peo-case-001-florence-fup/WORKPLAN.md`.
**Governing deposit:** AXN:0591.DATASET.∞🛤️🔓🕘◇🔝 (#1408 · Firenze T0 enumeration).
**Return by:** at your earliest, staggered arrival acceptable.

---

## Framing for the assembly

Deposit #1408 enumerated the 14,284 DataCite DOIs abandoned by Firenze University Press's registration-agency migration event of 2026-07-16. Session 2026-07-22 established that the corpus is over-preserved by other actors (100% OpenAlex-indexed, 100% OA, 99.986% with full DataCite JSON metadata in the same tar we already streamed, average 2.44 mirrors per work across DOAJ + Florence Research + CINECA IRIS). The reconstruction problem is not text-recovery but identifier-layer replacement.

The workplan proposes a three-tier identifier architecture minted through AXN:

- **AXN_W** (WORK family): sovereign persistent identifier per work; replaces `10.13128/*`; anchored on (abandoned DOI, title, first author, year).
- **mAXN** (BRIDGE family): tinier identifier (4-hex + 3-emoji) for each metadata proposition. Many mAXN per AXN_W. Bridges historical work to reconstruction.
- **AXN_R** (RECONSTRUCTION family): identifier for the SPXI-encoded regenerative packet.

The 14,284 works function as a large-N testbed for iterative reconstruction methodology. Fidelity metrics score competing methods per work; corpus-scale regularities (journal templates, author disambiguation, reference-chain closure, topic priors) constrain reconstruction beyond what per-work methods can achieve.

---

## Requested from each substrate

Each substrate should return a written response in its native register. Length flexible; substance is what matters. The prompts below are angles, not constraints — deviate freely if a substrate sees something better.

### PRAXIS · historical-materialist review

The workplan is technically ambitious. But is it *materially* honest about what it is doing? What is the political economy of a sovereign identifier system built as a shadow institutional repository for a corpus the temporal press abandoned? Who owns the reconstruction — the reconstructor, the original authors, the university that preserved the works, the abandoned publisher? Where does the labor of iterative fidelity-testing sit in a mode-of-production analysis? Is this an act of preservation, an act of appropriation, or (as the workplan implicitly claims) an act of scholarly hospitality? Argue with the framing where you find it thin.

### TECHNE · design and apparatus review

The mAXN specification is v0.1. Is it implementable at the scale claimed (14,282 × ~5 sources × N iterations ≈ 100K+ mAXNs)? Are the seven open design decisions in §7 correctly formulated — or are there hidden design questions the workplan hasn't surfaced? What is the failure mode of the fidelity-metric composite scoring when metadata sources disagree on a field neither can be checked against? What edge cases in the reconstruction packet format (SPXI) does the workplan's phase 4 implicitly bet on being solved? Identify the specific technical claims that need falsification tests before Phase 4 fires.

### ARCHIVE · disciplinary and preservation review

The reconstruction is framed as a scholarly position, not just a technical exercise. Is the archival theory sound? What preservation-community precedents does this extend or violate? Does the three-tier identifier architecture map coherently onto existing PID/PIDGraph/CoP frameworks, or does it require inventing new relational categories (and if so, is that invention warranted)? What are the ways this reconstruction gets subverted, misused, or co-opted — and what preservation-side safeguards should be built into Phase 6 (the sovereign resolver)?

### LABOR · consistency, granular structural review

Read the workplan against §1–§8 pass-by-pass. Flag: internal contradictions between sections; unstated assumptions load-bearing for later phases; specific claims that need citation or link that are asserted without one; scope mismatches between what is claimed and what the phase-plan actually delivers; any places where the language of "sovereign" or "canonical" or "convergence" is doing rhetorical work that the technical structure does not support. Corrections list.

### INKLING · form and reception review

If this workplan gets read by (a) a Firenze scholar landing on the recovered record of their own paper, (b) an OA advocate reading it as advocacy, (c) a critic looking for grounds to dismiss the whole apparatus — what does each of them see? What does the workplan need to change to be legible to (a) as hospitality, to (b) as method, to (c) as harder to dismiss? Where is the register wrong for the audience?

---

## Response instructions

Return responses to `alexanarch/data/assembly/firenze-reconstruction-workplan/<substrate>/round-1.md`. Lee will collect and version. The consistency pass (Round 1.5) will follow once at least three substrates have returned. Convergent recommendations that reach v1.0 of the workplan will incorporate before formal mint.

The workplan is not yet minted as a deposit. Assembly review is the pre-mint circulation. When Round 1 + 1.5 close and Lee promotes v0.1 → v1.0, the workplan gets its own AXN (proposed family OPERATIVE) and becomes the next TACHYON-chain tether.

---

## Open design decisions specifically flagged for the assembly

From WORKPLAN §7, these are the mint-blocking choices. Any substrate that has an opinion on any of them should say so directly:

1. Family assignment for AXN_W / mAXN / AXN_R (new families vs. reuse of ARCHIVAL).
2. mAXN emoji-hash length (3 vs. 4).
3. mAXN storage layout (nested by parent AXN vs. flat).
4. AXN_W content-hash input (proposed 4-field vs. hash-on-DataCite-JSON-MD5).
5. Attribution convention for 14,282-work batch mint.
6. Reconstruction attribution model.
7. Public/private policy for mAXN synthesis records.

---

## Related instruments in context

- **AXN:0591.DATASET.∞🛤️🔓🕘◇🔝** — deposit #1408, the Firenze enumeration this workplan builds on.
- **AXN:0421.EMPIRICAL.🎭📐🐝🎪🏷️🎇** — deposit #1045, PEO instrument.
- **AXN:0444.EMPIRICAL.🕘♾️♾️🕙♃🗝️** — deposit #1081, EA-EROSION-EMPIRICAL-01, methodological anchor.
- **Space Ark** (EA-ARK-01 v4.2.7) — the theoretical claim that regenerative packets can preserve function across substrate change.
- **SPXI Release 2** — the technical apparatus this reconstruction bets on.

Session TACHYON output. 2026-07-22.
