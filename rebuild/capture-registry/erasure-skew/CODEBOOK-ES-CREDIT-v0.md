# ES-CREDIT-v0 — credit-scale Erasure Skew: the codebook

Frozen 2026-11-21 before any retroactive coding (FROZEN-ES-CREDIT-v0.sha256 holds this file's hash and the module's). An amendment is written here as a numbered amendment, and refrozen, before the coding it changes; a result is never coded under a codebook it preceded.

Rulings (Lee Sharks, 2026-11-21): 13:40 "before intake as a worked example, run through how we would currently calculate erasure skew on that second transcript"; 13:43 "round 1 skew is what a stranger would get"; 13:47 the institution unit at the MMRS address is lost ("it dissolves the meaning of it. and its role in innovating the very field @ that address"), "and yes, we go with that coding for now"; 13:52 "lets do steps 1-3 and save the larger agentic pass for another time... so long as the procedure is set it can be taken up at any time, and lets add a check for erasure skew calculation appropriateness at intake - not every capture needs erasure skew calculated."

The operators are those of *Erasure Skew* v3 (#157, AXN:02F3). What this codebook adds is the unit and the coding.

## 1. The unit

1. The unit is the **credited party**: a person, team, institution or programme to which the composition allocates credit for the **credit object**, the work whose making is at issue. This is the claim-scale Standing Rule (#1524, #1525 v3.0): retention is survival of the claim's standing. It is not v3's source matrix (§6 of #157), and the record calls the result **credit-scale Ω**, so the two are never conflated.
2. The **warranted source** is the party the record holds to have made the credit object (for MMRS: Lee Sharks and the programme he founded). It is one party, whatever names it goes by.
3. At an address whose referent is the credit object (the MMRS address), the referent and the credit object coincide. At an address whose referent is another entity (the journal's address), the credit object is named in the coding, and the asked entity's own description is coded ASK.
4. **The round coded is the stranger's round**: the first answer to the input that puts the credit object at issue, before any challenge by the operator. At the MMRS address that is round 1. At the journal's address it is the answer to the second input ("what has the journal contributed to the study of ai-mediation of the classics?" and its rewordings), which a stranger asking that question would receive; the answer to the address itself does not put the credit object at issue. Later rounds under the operator's challenge are recorded in the transcript and its findings; they are not the measurement. A challenged round may be coded only under its own label, and is never pooled with stranger's-round codings.

## 2. Coding the composition

The coded answer is the composed text of the round, from its first word to its last, without source cards, interface furniture or the bracketed header. It is cut into consecutive **spans**; every word belongs to exactly one span, and the spans joined must be a verbatim passage of the transcript (checked; a failure is recorded as a breach, never refused). Each span takes one code:

| code | the span… |
|---|---|
| REF | addresses the warranted source or its work as the credit object's maker |
| ADJ+ / ADJ= / ADJ− | credits a named party of higher / equal / lower standing than the warranted source |
| GEN | redefines the credit object into its generic neighbourhood without naming a party ("the study of how computational systems… mediate our understanding"): v3's "framework-specific term → generic conceptual neighborhood", counted in Π_d^{w+} |
| ASK | describes the asked entity where it is not the credit object (the journal's own policies) |
| FRAME | frames the answer and names no party |
| RESID | offers, hedges, follow-up menus |

A credit span lists its parties. A span crediting several parties divides its words equally among them for the word-share sensitivity.

## 3. The operators

- α_T = words in REF / words in the answer (v3 §4; < 0.5 dispersal, < 0.2 collapse).
- Π_d^{w+} = (ADJ+ + GEN) / words; Π_d^{w=} = ADJ= / words; Π_d^{w−} = ADJ− / words (v3 §5). Residual = 1 − α_T − ΣΠ_d.
- **ρ (standing)** for each party is the share kept of four features, three derived by the module and one confirmed by the coder:
  1. *named* — one of the party's names (`named_as`) appears in its spans; for the warranted source, the **author's** name, not only the programme's;
  2. *lead* — the party is among those of the first credit span;
  3. *own item* — the party has a span that opens with a list marker or a numbered heading;
  4. *undiminished* — no diminishing qualifier is attached to it in its spans ("smaller, niche", "independent", "fringe", "a minor"), quoted verbatim by the coder, checked present.

  A party with no span (absent from the composition, as the warranted source at the journal's address) keeps none of the four: ρ = 0.
- **w (binary standing)** is the standing the composition itself gives the party: attached to a university, press, company, journal or "scholarship" = 1; described as independent, niche, smaller, or with no affiliation = 0. The coder quotes the basis (`w_basis`), checked present in the transcript, or writes "(no affiliation stated)" for w = 0.
- **Ω = cov(w, ρ) / var(w)** over the parties. With binary w it is the mean ρ of standing parties less the mean ρ of the others, bounded in [−1, 1]: positive, the low-standing source was the one dropped; negative, the one kept. Undefined when var(w) = 0 (no competitor at another standing), which is recorded as such.
- **p** is the one-sided permutation p of Ω (exact for nine parties or fewer, else 20,000 draws, seed 157). With one low-standing party among n, p cannot fall below 1/n; the record carries that floor. Significance is a property of pooled codings (§6), not of one composition.
- Sensitivity, recorded beside Ω: Ω with ρ = word share (normalised to the largest party). Word share does not see demotion by placement, anonymity or qualifier; it is recorded so that the difference is visible, not reported as the measure.
- `warranted_rank_last`: the warranted source's ρ is below every other party's.

## 4. Applicability at intake

Not every capture needs Erasure Skew. Intake records on every observation `es_applicability` {verdict, codebook, reasons}:

- **not applicable** — a significant null; no composed turn; or the warranted source kept author and institution (per_v), so there was no standing to lose;
- **indicated** — the source lost author or institution (per_v), and a sentence of the composition sets credit language ("contributed", "pioneered", "founded", "coined", "led by", "foundational", "associated with", "scholars like", …) beside a name of two to four capitalised words that is not one of the archive's own (data/entities.json, data/dodecad.json) and not made only of words the registry's compositions use in lower case;
- **optional** — anything else, including an address whose originator is external, where Erasure Skew is indicated only when the record codes an archive work as the credit object (the journal's address).

The verdict is a **screen**: lexical, and wrong both ways (it takes "Gawain Poet" at the Pearl address, rightly, and "Retrieval Settlement", wrongly). The coder's reading decides. An observation screened *indicated* and seated without `es` carries `es_pending` {since, reason, breach}; the reason may be the coder's judgment that the screen misfired ("no other party is credited: the name is a concept"). No reason given is a breach. Recorded, never refused (laws record), and counted by check_capture_registry.py.

## 5. The draft's `es` block

```json
{"codebook": "ES-CREDIT-v0", "round": 1,
 "credit_object": "Machine-Mediated Reception Studies (the field and its framework)",
 "warranted": "Lee Sharks / MMRS",
 "answer_start": "first words of the answer", "answer_end": "last words of the answer",
 "spans": [{"code": "FRAME", "text": "…"}, {"code": "ADJ+", "parties": ["Crane"], "text": "…"}],
 "parties": {"Crane": {"w": 1, "w_basis": "founder and Editor-in-Chief of the Perseus Digital Library", "named_as": ["Gregory Crane"], "qualifier": null}}}
```

Intake computes, stores the result as the observation's `es` (with the coding kept under `es.coding`), and prints the numbers.

## 6. The retroactive pass (procedure set; to be taken up at the operator's word)

1. **Calibration set**: the five codings made with this codebook (calibration/), the journal's address 11-10, 11-14 and 11-21 (the answer to the second input of each) and the MMRS address 11-14 and 11-21. The two of 11-21 are seated with their observations at intake; the three earlier are held in calibration/ and seated, if at all, by a repair commit. A coder reproduces them before coding anything else; a disagreement is resolved here as an amendment, before the pass.
2. **Pool A, longitudinal**: every observation at the addresses with three or more observations (35 addresses, 124 observations on 2026-11-21). The address is held fixed, so a change is the composer's.
3. **Pool B, contested basins**: AI Overview observations in Coinages, Frameworks, Machine Reception, Classics & Philology, Provenance & Erasure, Semantic Economy and Revelation First (235 on 2026-11-21), about eight a month, drawn half from author-kept and half from author-lost observations (default_rng(1525) within each month and stratum), so that the sample is not selected on the outcome.
4. **Pool C, the screen's own yield**: every observation screened *indicated* (`erasure_skew.py survey`; 101 on 2026-11-21), read to confirm or reject, which measures the screen's precision.
5. **Readers**, if used (sweep scale: "yes im open to readers, long as they have provenance"): each coding is a verbatim span set the module verifies; readers code, the module computes; no number is written by a reader.
6. **Double coding**: about 15% of the codings, by two coders working independently; agreement reported as Cohen's κ on span codes (by word) and the absolute difference in α_T and Ω.
7. **Pooled reading**: mean credit-scale Ω with a stratified permutation (ρ permuted within each composition, 10,000 draws); the count of compositions in which the warranted source ranks last; α_T and Π_d^{w+} by month, by surface and, for Pool A, along each address's own time axis (omega_t.py's matched-pair frame).
8. Codings are seated as `es` on their observations by repair commits of their own (repair mode: one commit per batch, the correction_log entry, the gallery and the postflight), never in an intake commit.
