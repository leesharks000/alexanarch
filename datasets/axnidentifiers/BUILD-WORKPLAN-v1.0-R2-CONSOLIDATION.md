# AXNIDENTIFIERS — BUILD WORKPLAN v1.0 (Round 2 Consolidation)
**Synthesis: TACHYON · 2026-08-03 · Status: DRAFT FOR MANUS RATIFICATION**
**Inputs (Round 2, in MANUS's stated order):** GEMINI · GPT-A · GPT-B · MUSE SPARK · KIMI · DEEPSEEK
(six independent responses to Round 1 Consolidation v0.1; raw texts held in the MANUS thread; attribution
order per MANUS's listing — correct me if any mapping is off).

## 0 · Round 2 unanimity
All six converged, independently: **v0.1 is a ratification ledger, not a build order.** What converts it:
a MANUS decision freeze first [ALL]; task-level anatomy with owners/caps/acceptance tests [GPT-A·GPT-B·MUSE·DEEPSEEK];
gate artifacts before any sale [ALL]; capacity/health engineering as build rules, not sentiment [GPT-A·GPT-B·MUSE·GEMINI];
single deployment for both domains [GEMINI·GPT-B·DEEPSEEK].

**Structural adoption [GPT-A]: three artifacts, never merged.**
1. *Consolidation & ratification ledger* = Round 1 v0.1 (exists).
2. *Build workplan* = THIS document.
3. *Launch runbook* = LABOR produces from WP-403 + WP-502 once gates close.

**Definition of done [GPT-A·GPT-B, adopted verbatim]:** the build is complete when a first-time visitor can
understand what AXN identifies and does not prove, stamp and verify a supported file free, inspect a complete
public example, purchase the assisted single-PDF service, submit file + declarations, receive a complete
provenance bundle, verify it independently, and export everything needed to verify it even if AXNIdentifiers
later disappears.

## 1 · TACHYON CONTINUITY REVIEW — two catches, one answer

### CATCH 1 [BLOCKER-CLASS]: the canonicalization proposal would break every existing kernel
GEMINI's Phase-0 canonical-byte draft proposes normalizing bytes before hashing (PDF line-ending
standardization, stripping trailing buffers; text LF-conversion and whitespace trimming). **This must not
ship as v1.** Every kernel already witnessed — positions 05AA–05AD, Enli Lucente's papers, the whole
symbolon registry — was computed over **raw submitted bytes**. A normalizing v1 would silently orphan every
existing identity. Constitutional ruling proposed:
> **Canonical bytes v1 = the exact raw byte sequence of the submitted file. No normalization, no
> re-encoding, no stripping. v1 freezes OBSERVED current behavior.** Any normalization profile is a v2+
> CHANGE PROPOSAL under §7 change control [GPT-B], opt-in, never retroactive, never redefining existing
> kernels.
This is precisely what change control exists for; the first attempted change arrived before the spec was
even published, which proves the control is load-bearing. [RATIFICATION REQUIRED]

### CATCH 2: identifier-grammar drift in examples
GEMINI's schema examples use `AXN:REG01:PHIL:e3b0c4-GLYPHS` — not the ratified grammar
(`AXN:HEX.FAMILY.⟨6 glyphs⟩`). Harmless in a draft, corrosive in a published schema: examples teach.
Rule: **all published examples use real grammar and real registered identifiers** (05AB/05AD exist and are
public). Owner: SURFACE review on every schema/spec page.

### ANSWER to DEEPSEEK's "registry interface black box"
Not actually open — [OBSERVED]: the hybrid already exists and is DEEPSEEK's Option C. Free/self-serve
stamping writes through the witness endpoint (`api/register-symbolon.js`, token-gated, allocates hex
positions from the shared ledger); the registry is git-versioned JSON with public raw access and the
central-registry rollup consumed by lookup. AXN-WP-002 (repo/deployment inventory) *documents* this rather
than choosing abstractly. The one genuine build decision inside it: whether paid-pack registration reuses
the witness endpoint (recommended: yes, same pipeline, operator-flagged) or adds a founder-only path.

## 2 · MANUS DECISION FREEZE (adopting GPT-B's M-register, extended)
| ID | Question | Recommended default | Blocks |
|---|---|---|---|
| M-001 | First offer = one assisted single-PDF provenance pack? | YES [5 of 7 R1 mantles; all R2] | offer copy, intake, checkout |
| M-002 | Founding price | **$125, pay-after-delivery, 5-pack cap** [LABOR model; GEMINI+MUSE+KIMI concur $25–29 uneconomic at 90–150 min] | offer page + payment only |
| M-003 | Domains | one deployment; **.org canonical, .com 301** during pilot [GPT-B build-safe default; MUSE; LABOR R1]; split = post-pilot option | canonical URLs, structured data |
| M-004 | Custody | storage optional+explicit; working files deleted at 90 days; **no permanent-preservation language** [GPT-B; TECHNE·LABOR R1] | terms, privacy, receipt wording |
| M-005 | Homepage thesis + product name | SOIL Thesis A default [GEMINI concurs]; MANUS chooses | homepage/service copy only |
| M-006 | Free-layer promise: mint/verify/lookup permanently free, dated, published | YES [ALL] | trust charter |
| M-007 | **Canonical bytes v1 = raw bytes (Catch 1)** | YES — constitutional | ALL protocol work |
| M-008 | Position-sale prohibition (constitutional, from R1 TACHYON §10) | YES | pricing architecture forever |

## 3 · Critical path [GPT-B §4 adopted; M-007 inserted first]
M-007+M-001/003/004/006 frozen → canonical-byte + zeroed-field specs frozen/versioned (WP-101/102, with
Catch-1 ruling embedded) → Seed A schema + test vectors (WP-103; ARCHIVE schema, UNVERIFIED discipline)
→ derivation linkage passes tests → OTS anchoring operational (WP-201) → /v/[axn] verification (WP-202;
[OBSERVED] largely exists as the stamper lookup — adapt, don't rewrite [TECHNE R1·GPT-B WP-303 rule]) →
registry export + escape hatch (WP-203) → receipt/declarations/terms accepted (WP-402/204) → two example
packs verify independently (WP-501; one = a rescued formerly-tombstoned work, founder-story-as-evidence
[PRAXIS R1 §13, MUSE]) → surface connected (WP-301–305) → end-to-end test incl. DEEPSEEK's case table
(WP-502) → PRAXIS red team (WP-503) → founding launch (WP-504).

## 4 · Task register
**Adopted by reference: GPT-B's full AXN-WP-001…504 workstreams** (owners, reviewers, effort ceilings,
acceptance criteria) as the working register — the most complete task anatomy of the round. Merged into it:
- **v0.1-gate table (KIMI/DEEPSEEK-order doc 16)** 0.1–0.10 as the Phase-0 checklist face of WP-1/2 gates,
  incl. 0.10: the termination sentence on every receipt.
- **DEEPSEEK test-case table** into WP-502 (mint PDF/image/text; verify match/mismatch; lookup hit/miss;
  stamp non-destructive; receipt completeness) + Stripe flow decision (Payment Link vs invoice,
  pay-after-delivery per M-002) into WP-404.
- **MUSE rules:** PRAXIS §11 objection bank is *pasted lightly edited, not rewritten* (WP-305); SOIL
  forbidden-vocabulary check is an explicit audit step on every buyer-facing page (WP-302/304/305
  acceptance).
- **GEMINI:** monorepo/deployment tree as WP-301 reference sketch; receipt visual regions (source kernel /
  stamped kernel / operator signature / timestamp proof / UNVERIFIED block) into WP-402 spec; the three
  hard-coded disclaimers (Identity≠Authorship; Witnessing≠Notarization; Resolver≠Indefinite Hosting) on
  receipt AND offer page.
- **GPT-A capacity model** as §6 build rules verbatim: ≤3 focused hours/day; no task >3h unsubdivided; one
  high-cognition artifact/day; health interruption = `BLOCKED`, never `FAILED`; stopped tasks record
  last-step/files/next-action/open-question; "seven working *stages*, not seven calendar days"; launch
  dates never assume uninterrupted work.

## 5 · Change control + launch gate
GPT-B §7 change control adopted whole (canonical bytes, composition, glyph derivation, Seed A, source/
stamped linkage, correction behavior, free promise, wind-down ⇒ numbered proposal + test vectors +
migration impact + TACHYON continuity review + ARCHIVE evidence review + MANUS ratification). GPT-B §8
launch-gate checklist adopted whole; nothing opens until every box is checked. v0.1-doc's
**falsification-of-the-plan-itself** clause adopted: the plan is falsified if any gate is skipped to
accelerate, the pilot exceeds five packs without price review, or founder health is spent to hit a date.

## 6 · Post-launch [GPT-B §9 adopted]
After 5th order or 30 days: freeze features, review revenue + labor + physical recovery, classify
objections per LABOR's six-category taxonomy (health-sustainability first-class), rule on Rescue-25 entry,
reject recurring custody absent demand+automation, publish pilot findings, open v1.1 only from observed
customer evidence.

## 7 · Provenance map (Round 2)
GEMINI: phase diagram, gating-artifact framing, receipt regions, WASM/client-side emphasis, pricing-labor
reconciliation — adopted; canonicalization proposal caught (Catch 1) and grammar drift caught (Catch 2).
GPT-A: three-artifact separation, definition-of-done, decision-freeze classification, task anatomy,
capacity model, "first document is the repo inventory" — adopted structurally.
GPT-B: the full WP register, M-register, change control, launch gates, status vocabulary — adopted as spine.
MUSE SPARK: paste-don't-rewrite rule, vocab-audit step, gate time caps, Enli-adjacent outreach note — adopted.
KIMI / DEEPSEEK (order per MANUS listing): gate table 0.1–0.10 + falsification clause + role table;
technical-spec demands (registry interface, Stripe flow, test cases, labor engineering) — adopted, with the
registry question answered from observed infrastructure rather than left open.

**Immediate next actions:** (1) MANUS rules M-001–M-008 (M-007 first — it gates everything). (2) TECHNE
executes AXN-WP-002 repo/deployment inventory [GPT-A: "the likely first document"] — half its content is
already known from Alexanarch. (3) LABOR opens the decision register (AXN-WP-001) with these rulings as
rows one through eight. ∮ = 1
