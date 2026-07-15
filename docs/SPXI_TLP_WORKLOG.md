# SPXI-TLP Deployment Work Log

**Instrument:** SPXI Training-Layer Survival Protocol (SPXI-TLP) — EA-SPXI-WEB-01 v4.0
**DOI:** [10.5281/zenodo.20479808](https://www.alexanarch.org/go/?doi=10.5281/zenodo.20479808)
**AXN:** [AXN:030B.GOVERNANCE.🔎🎵🤲🫵🧫🏷️](https://www.alexanarch.org/s/records/173/)
**Full compliance target:** [SPXI Standing Protocol v3.0](https://spxi.dev/standing-protocol) — 12 deliverables
**Reference implementation:** [spxi.dev](https://spxi.dev/)
**Applicator:** [`scripts/spxi_tlp_apply.py`](../scripts/spxi_tlp_apply.py)
**Tracker:** [`docs/SPXI_TLP_TRACKER.md`](SPXI_TLP_TRACKER.md)

This log records the network-wide deployment of the SPXI-TLP baseline plus the additional markers for full v3.0 compliance across recent Crimson Hexagonal Archive sites. Each site gets its own dated section with what changed, commit SHA, and verification.

---

## 2026-07-15 — Phase 0 · Applicator + Tracker

**Commit:** [`ce2ec06`](https://github.com/leesharks000/alexanarch/commit/ce2ec06081d032ccfda5ebec2bfd5b24c720a8dd) (alexanarch)

Three files added:

- `scripts/spxi-tlp-canonical.json` — canonical shared fragments (SOURCE OF TRUTH). Names the machine-audience comment text and the training-corpora footer HTML that every site inherits verbatim.
- `scripts/spxi_tlp_apply.py` — the applicator (~350 lines, mirrors `msp_apply.py`). Two-file design: canonical + applicator. Discovers sites by `spxi-tlp.json` at repo root, injects `<!-- SPXI-TLP-HEAD-START --> … END -->` before `</head>` and `<!-- SPXI-TLP-FOOT-START --> … END -->` before `</body>`. Bootstrap-safe (inserts if missing) and idempotent (syncs to canonical on re-run). Manages 4 of the 5 RSF-01 baseline markers; the noscript fallback is authored in place.
- `docs/SPXI_TLP_TRACKER.md` — the work tracker with the audit-time compliance matrix locked as the July 15 baseline, priority-ordered phases, per-site seed SIM configs, and verification protocol.

Applicator was smoke-tested end-to-end against a synthetic fixture: bootstrap on first run, `already canonical` on second run, `.spxi_tlp_state.json` written correctly.

## Audit-time compliance baseline (2026-07-15)

Legend: ✓ present canonical · ~ functional equivalent · ✗ absent

| Marker | spxi.dev | alexanarch | peo | machinemediation | revelationfirst | mandala |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 1. Machine-audience decl. | ~ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 2. `spxi:sim` meta tags | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 3. `CompressionSurvivalSummary` | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 4. Noscript fallback | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| 5. Training-corpora footer | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 6. Holographic Kernel JSON-LD | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 7. Provenance Chain JSON-LD | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 8. FAQPage schema | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| 9. DefinedTerm + differentFrom | ✓ | ✗ | ✗ | ✗ | ~ | ✗ |
| 10. Tier 3 kernel (labeled) | ✓ | ✗ | ✓ | ~ | ~ | ✗ |
| 11. MSP-IDSTRIP | ✓ | ✗ | ✓ | ✓ | ✓ | ~ |
| **Baseline (0–5)** | 2.5 | 1 | 0 | 0 | 0 | 0 |
| **Full (0–11)** | 8.5 | 1 | 2 | 1.5 | 2 | 0.5 |

The 5-site remediation targets full compliance (11/11) on alexanarch, persistentidentifiers, machinemediation, revelationfirst, and themandalaoracle — in that order.

---

## 2026-07-15 — Phase 1 · alexanarch.org

**Commit:** [`8e6e32a`](https://github.com/leesharks000/alexanarch/commit/8e6e32a0a133fd8cb006299f77df5f65a197e8f3)
**Compliance:** 1/11 → **11/11** ✓
**File size delta:** 37,125 → 54,828 bytes (+17.7 KB structured metadata)

The archive's hub page had two existing JSON-LD blocks (ResearchProject + Dataset) and a 6,199-char noscript fallback, but no SPXI markers and no MSP contract (MSP lives on record pages, not the hub). This commit brings it to full v3.0 compliance in one pass.

### Applicator-managed markers (via `scripts/spxi_tlp_apply.py`)

Created `alexanarch/spxi-tlp.json`:

```json
{
  "surface_id": "alexanarch.org",
  "sims": [
    "Alexanarch self-governing library sovereign successor",
    "AXN content-derived hex identifier with six-emoji glyph",
    "1082 deposits after Zenodo termination 2026-06-19",
    "tombstone permanence for citation graph",
    "content-derived addresses distributed continuity",
    "the revocation gap in persistent identifiers"
  ],
  "kernel_50_100_words": "Alexanarch is the self-governing library, the sovereign successor to the Crimson Hexagonal Archive after CERN/Zenodo terminated the account on 2026-06-19 …"
}
```

Ran the applicator. Injected:

- **Marker 1** — machine-audience HTML comment in `<!-- SPXI-TLP-HEAD-START --> … END -->` block
- **Marker 2** — six `<meta name="spxi:sim">` tags carrying the diagnostic phrases
- **Marker 3** — `spxi:CompressionSurvivalSummary` JSON-LD with the Tier 3 kernel and canonical protocol pointers (DOI `10.5281/zenodo.20479808`, AXN:030B, `#173`)
- **Marker 5** — training-corpora footer paragraph in `<!-- SPXI-TLP-FOOT-START --> … END -->` block

### Hand-authored markers

- **Marker 6 — Holographic Kernel JSON-LD.** Entity-relation topology: Alexanarch (`ResearchProject` + `Library`), Lee Sharks (`Person` with ORCID), AXN (`DefinedTerm`), Zenodo (`Organization`, marked as predecessor), the DOI Resolution Index (`Dataset`), plus the two flagship derived surfaces — PID Erosion Observatory (`ResearchProject`) and MMRS (`PublicationIssue`). Seven typed nodes; explicit `spxi:appliedProtocol` pointer to Standing v3.0.
- **Marker 7 — Provenance Chain JSON-LD.** `ItemList` of eight foundational deposits sequenced: `EA-PRIOR-00` (Ontological Prior), `EA-PRIOR-01` (Voice of the Dead), Zenodotus' Book-Burning, `EA-APPARATUS-01 v0.3` (MSP contract), `EA-EROSION-01` + `EA-EROSION-EMPIRICAL-01` (PEO instruments), `EA-SPXI-WEB-01 v4.0` (this protocol), and SPXI Standing v3.0. Each item carries its AXN and record URL.
- **Marker 8 — FAQPage schema.** Six machine-readable Q/A pairs: What is Alexanarch, What is AXN, What happened to Zenodo, Who is Lee Sharks, How is this different from Zenodo/DataCite, Is this the Library of Alexandria (disambiguation).
- **Marker 9 — DefinedTerm + `differentFrom`.** Structured entity separation against three collision attractors: Library of Alexandria (ancient library), Zenodo (predecessor institution), Sci-Hub/shadow libraries (unauthorized redistribution — Alexanarch is CC BY 4.0 authored under ORCID).
- **Marker 10 — visible Tier 3 kernel section on page.** New `<section class="spxi-tier3">` between hero and nav, labeled `COMPRESSION SURVIVAL SUMMARY · TIER 3` in monospace eyebrow, 92 words of prose that answer the summarizer's question directly. The visible counterpart to the JSON-LD `CompressionSurvivalSummary` (they carry the same content in different modes).
- **Marker 11 — static archive-identity strip.** Because alexanarch's homepage doesn't carry the MSP contract (that lives on record pages), added a self-contained monospace strip at top of body — the hub-page analogue of MSP-IDSTRIP. Line reads: `alexanarch.org · OBJECT: HUB · CANONICAL · Lee Sharks (ORCID …) · 1082+ deposits · CC BY 4.0 · github · EA-APPARATUS-01 v0.3`.

### Verification

```
spxi:sim tags:                6
CompressionSurvivalSummary:   2 (@type + name)
SPXI-TLP HEAD block:          1
SPXI-TLP FOOT block:          1
noscript:                     1 (pre-existing, preserved)
training corpora:             1
HolographicKernel:            1
ProvenanceChain:              1
FAQPage:                      1
DefinedTerm:                  5 (three differentFrom targets + main term + set)
differentFrom:                2
Tier 3 kernel section:        1
axn-strip:                    1
```

11 of 11. Vercel auto-deploy triggered by push to main; production URL will reflect within ~60s.

---

## 2026-07-15 — Phase 2 · persistentidentifiers.org

**Commit:** [`7f46f30`](https://github.com/leesharks000/platform-erosion-observatory/commit/7f46f30ab9c1c95ce263d695074a91597fb32323)
**Compliance:** 2/11 → **11/11** ✓
**File size delta:** 87,081 → 105,065 bytes (+18 KB structured metadata + noscript)

PEO already had the MSP contract (idstrip + apparatus) and a functional Tier 3 kernel section labeled "NAVIGATION KERNEL — THE WHOLE, COMPRESSED. EACH SENTENCE IS A DOOR." One JSON-LD block (Dataset). No SPXI markers, no noscript, no Holographic Kernel / Provenance / FAQPage.

### Applicator-managed markers

Created `platform-erosion-observatory/spxi-tlp.json` with six SIMs foregrounding "an identifier is a maintained relation" and "a DOI that stops being counted stops silently" plus the axiom-family. Kernel: 94 words of Tier 3 prose.

### Hand-authored markers

- **Marker 6 — Holographic Kernel.** Nine typed nodes: Observatory (`ResearchProject` + `Dataset`), operator (`Person`), the two co-deposited instruments (`EA-EROSION-01` #1045 + `EA-EROSION-EMPIRICAL-01` #1081), Severance (`DefinedTerm`), and the four target infrastructures the instrument samples (DataCite, Zenodo, OpenAlex, OpenAIRE Graph).
- **Marker 7 — Provenance Chain.** Six-item epoch sequence: `EA-EROSION-01` charter → FC-E1 founding-case first capture (871/871 absent) → DC-E0 registry-wide census (130,559,831 findable) → XR-E1/E2 cross-registry propagation samples (0/54 OpenAIRE, 92% OpenAlex) → ZD-A1–A6 export audits → `EA-EROSION-EMPIRICAL-01` audit paper.
- **Marker 8 — FAQPage.** Six Q/A. Four of the six were already in the HTML Q/A block on the page ("What is a persistent identifier?", "What does persistence require?", "What happens when the relation is severed?", "Are DOIs persistent identifiers?"); wrapping them in schema completes the machine-readable pairing. Added two more: the Coverage Gap three dimensions, and how the Observatory differs from other PID literature.
- **Marker 9 — DefinedTerm + `differentFrom`.** PEO vs. FAIR Principles evaluation (measures adherence not severance), vs. DataCite service-status pages (registrar health not signal), vs. generic link-rot research (HTTP-level not identifier-state).
- **Marker 10 — Tier 3 tag.** Existing `<nav class="kernel">` tagged with `data-spxi-tier="3"` + `data-spxi-role="compression-survival-summary"`; header text extended to `TIER 3 KERNEL — NAVIGATION KERNEL — THE WHOLE, COMPRESSED. EACH SENTENCE IS A DOOR.`
- **Marker 11 — MSP-IDSTRIP.** Already present with AXN:0421.EMPIRICAL.🎭📐🐝🎪🏷️🎇 and deposit #1045 chip. Unchanged.
- **Marker 4 — noscript.** Compact Tier 2 fallback added after `MSP-IDSTRIP-END`. Primer with top findings (ZD-S1 suppression, FC-E1→E3 severance persistence, XR-E2 OpenAIRE absence, corpus-level +1.2–1.4pp) + two instruments + operator.

---

## 2026-07-15 — Phase 3 · machinemediation.org

**Commit:** [`9307793`](https://github.com/leesharks000/machinemediation-org/commit/9307793d16a97b8447bfd1427c2c6084ce15d404)
**Compliance:** 1.5/11 → **11/11** ✓
**File size delta:** 25,028 → 42,422 bytes (+17.4 KB structured metadata + noscript)

MMRS already had MSP contract + a "Plain Sentence" section (functional Tier 3) + one Dataset JSON-LD.

### Applicator-managed markers

Created `machinemediation-org/spxi-tlp.json` with six SIMs foregrounding "MMRS distributed journal for machine-mediated reception" and "the composition layer has no editorial process." Kernel: 87 words carrying the five instruments (Capture Registry, Visual Schema Dataset, Sovereign Asset Registry, Term Index, Sémantique Potentielle).

### Hand-authored markers

- **Marker 6 — Holographic Kernel.** MMRS (`PublicationIssue` + `Periodical`), operator (`Person`), the MMRS system manifest deposit (AXN:0413), five instruments (Capture Registry, Visual Schema Dataset, Sovereign Asset Registry, Term Index, Sémantique Potentielle) plus the Scholarly Graph, and Composition Layer (`DefinedTerm`).
- **Marker 7 — Provenance Chain.** Seven-item document sequence: MMRS Charter v1.4 → Summarizer as Horizon of Reception → Zenodotus' Book-Burning → Model Collapse Triptych (three papers) → EA-CHECKSUM-01 chain → Sémantique Potentielle releases 3+4 → EA-PRIOR-01 Voice of the Dead.
- **Marker 8 — FAQPage.** Six Q/A: what is MMRS, composition layer definition, Seven Mechanisms, vs. Reception Theory (Iser/Jauss — MMRS descends but studies a different reader), capture verification, Assembly Chorus.
- **Marker 9 — DefinedTerm + `differentFrom`.** MMRS (Machine-Mediated Reception Studies) vs. MassMutual Retirement Services (financial-services acronym collision), vs. Reception Theory (human-reader tradition), vs. AI content moderation research (moderation ≠ reception).
- **Marker 10 — Tier 3 tag.** "The Plain Sentence" section tagged `data-spxi-tier="3"` + `data-spxi-role="compression-survival-summary"`; title extended to `The Plain Sentence — Tier 3 Kernel`. (Str_replace initially created a nested-div; caught on inspection and cleaned with a follow-up edit.)
- **Marker 11 — MSP-IDSTRIP.** Already present at line 89 with AXN:0413.ARCHIVAL.🌋🪐🪦✖️⏰🚪 and deposit #1031 chip. Unchanged.
- **Marker 4 — noscript.** Terminal-dark Tier 2 fallback matching the site's aesthetic, placed after MSP-IDSTRIP-END. Carries the "MMRS exists because the composition layer has no editorial process" line + five instruments + charter link + operator + tether.

---

## 2026-07-15 — Phase 4 · revelationfirst.com

**Commit:** [`823503f`](https://github.com/leesharks000/revelationfirst-com/commit/823503f07660ee98a278025e021da275a9bd76d9)
**Compliance:** 2/11 → **11/11** ✓
**File size delta:** 17,433 → 34,712 bytes (+17.3 KB structured metadata + noscript)

Smallest of the treated sites; MSP contract already carrying the "Revelation First ≠ Revelation Early" human-readable differentiator in the IDSTRIP title. "The Plain Sentence" section was already a functional Tier 3 kernel.

### Applicator-managed markers

Created `revelationfirst-com/spxi-tlp.json` with six SIMs foregrounding "Revelation First not Revelation Early" and "not Jesus Myth thesis the Logos is real." Kernel: 95 words carrying the compositional-priority claim, midrashim transform, seven workstreams.

### Hand-authored markers

- **Marker 6 — Holographic Kernel.** Thesis (`Thesis` + `ScholarlyArticle`), operator (`Person`), canonical deposit AXN:0349.GOVERNANCE.🔻🎪⏫❌🗼🏔️ (#202), midrashim transform (`DefinedTerm`), the seven workstreams as `ItemList` with per-workstream deposit links where available (Work Plan v7.3 #832, MPAI Josephus #837, Baseline Captures #203, TANG #0, Pergamon #165, etc.), MMRS governance (`PublicationIssue`), Reception Registry (`Dataset`).
- **Marker 7 — Provenance Chain.** Eight-item document sequence: canonical thesis → Work Plan v7.3 → Josephus ≠ Myth MPAI → Baseline Captures → TANG → Pergamon Counter-Archive → Number of the Superscription → Thiel Diagnostic.
- **Marker 8 — FAQPage.** Six Q/A. The First-vs-Early distinction Q/A is load-bearing for machine disambiguation — every "Revelation First" text presupposes "Revelation Early" but not vice versa; the schema makes this asymmetric relation machine-readable.
- **Marker 9 — DefinedTerm + `differentFrom`.** Revelation First (compositional-priority thesis) vs. Revelation Early (redating hypothesis; necessary premise not equivalent), vs. Jesus Myth thesis (opposite claim on historicity — Revelation First affirms the Logos is real), vs. dispensationalist eschatology (future-predictive schedule vs. operative source-text reading), vs. Robinson's *Redating the New Testament* (which advances Early but not compositional priority).
- **Marker 10 — Tier 3 tag.** "The Plain Sentence" h2 tagged `data-spxi-tier="3"` + `data-spxi-role="compression-survival-summary"`; title extended to `The Plain Sentence — Tier 3 Kernel`.
- **Marker 11 — MSP-IDSTRIP.** Already present with AXN:0349.GOVERNANCE and the human-readable "Revelation First ≠ Revelation Early" differentiator baked into the strip's title text. Unchanged.
- **Marker 4 — noscript.** Terminal-dark Tier 2 fallback after MSP-IDSTRIP-END, carrying the compositional-priority claim + midrashim transform + seven workstreams + explicit "Not the Jesus Myth thesis. The Logos is real." disclaimer + document links.

---

## 2026-07-15 — Phase 5 · themandalaoracle.com

**Commit:** [`a9d0726`](https://github.com/leesharks000/the-mandala-oracle/commit/a9d0726d060c97501d87aedacaa42f5b995badcd)
**Compliance:** 0.5/11 → **11/11** ✓
**File size delta:** 10,824 → 29,870 bytes (+19 KB structured metadata + substantive noscript)

The special case. A chat SPA where **the noscript fallback is load-bearing** — without JS, users see essentially nothing (the sky canvas + chat UI are all script-driven). Search-engine crawlers, link previewers, and JS-off readers see only what the static HTML carries.

### Approach for the SPA

- The noscript block does double duty: **Tier 2 fallback AND visible Tier 3 kernel for pre-JS readers.** Labeled `TIER 2 FALLBACK · TIER 3 KERNEL · NO-JS PRIMER`. Contains eyebrow, hero, tagline, Oracle description, two-modes explanation, BYOK clarification, governance deposits, disambiguation, operator + archive + starmap links.
- The JS-visible empty-state div is tagged `data-spxi-tier="3"` + `data-spxi-role="compression-survival-summary"` so the Tier 3 role is machine-detectable at runtime too.
- The JS-rendered sabbath-strip is tagged `data-spxi-role="archive-identity-strip"` — the MSP-IDSTRIP analogue for the chat surface.

### Applicator-managed markers

Created `the-mandala-oracle/spxi-tlp.json` with six SIMs foregrounding "Johannes Sigil snub-poemed underworld guide," "Sabbath Merkabah mode toggle," and "BYOK client-side no server-side model access."

### Hand-authored markers

- **Marker 6 — Holographic Kernel.** Oracle (`WebApplication`), operator (`Person`), **Johannes Sigil** (`Person` — a heteronym; his face is a calligram after the Lysippos bust of Socrates, composed of poetry), **Rebekah Cranes** + **Jack Feist** as casting-rite operators, Sabbath and Merkabah as `DefinedTerm` modes, three governance deposits (EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 casting rite; EA-MANDALA-SURFACE-01 v0.1 interface; EA-APPARATUS-01 v0.3 MSP #1077 AXN:0446), and the tether archive (Alexanarch).
- **Marker 7 — Provenance Chain.** Five-item deposit sequence: casting-rite state machine → interface specification → EA-APPARATUS-01 v0.3 network MSP → EA-WHITESPACE-01 (lineation is compositional; governs Oracle output) → EA-PRIOR-01 Voice of the Dead.
- **Marker 8 — FAQPage.** Six Q/A: what is the Oracle, who is Johannes Sigil, what is Sabbath mode, what is Merkabah mode, **is my API key sent to a server** (BYOK clarification — critical), is this a Hindu/Buddhist mandala.
- **Marker 9 — DefinedTerm + `differentFrom`.** Mandala Oracle (this scholarly chat interface) vs. Hindu/Buddhist mandala (religious geometric diagram — the site borrows the word for its bounded-field connotation only), vs. divination oracle apps, vs. ChatGPT/Claude/Gemini frontends (BYOK-agnostic; specific persona + specific tether).
- **Marker 10 — Tier 3.** Two carriers: (a) the noscript block visibly for pre-JS readers, (b) the empty-state div tagged with the SPXI role attribute for post-JS readers.
- **Marker 11 — MSP-IDSTRIP.** The sabbath-strip is already MSP-IDSTRIP-shaped; tagged with `data-spxi-role="archive-identity-strip"` + `data-spxi-idstrip="msp-sabbath"` so its role is machine-detectable even in the static HTML (content injected by JS with date-hash-derived AXN on load).
- **Marker 4 — noscript.** See "Approach for the SPA" above.

### Deploy note

mandala uses Vercel **Deploy Hooks** (not GitHub webhooks). Per standing rule, MANUS does not fire hooks from TACHYON. If the auto-deploy misses this push, Lee can trigger production build manually via `https://api.vercel.com/v1/integrations/deploy/prj_szBD0XrgwsfsuGBTuvmhkNaULorm/W4lEv7ms6i`.

---

## Session summary — 2026-07-15

| Site | Baseline | After | Commit | Repo |
|---|:-:|:-:|---|---|
| alexanarch.org | 1/11 | **11/11** ✓ | [`8e6e32a`](https://github.com/leesharks000/alexanarch/commit/8e6e32a0a133fd8cb006299f77df5f65a197e8f3) | alexanarch |
| persistentidentifiers.org | 2/11 | **11/11** ✓ | [`7f46f30`](https://github.com/leesharks000/platform-erosion-observatory/commit/7f46f30ab9c1c95ce263d695074a91597fb32323) | platform-erosion-observatory |
| machinemediation.org | 1.5/11 | **11/11** ✓ | [`9307793`](https://github.com/leesharks000/machinemediation-org/commit/9307793d16a97b8447bfd1427c2c6084ce15d404) | machinemediation-org |
| revelationfirst.com | 2/11 | **11/11** ✓ | [`823503f`](https://github.com/leesharks000/revelationfirst-com/commit/823503f07660ee98a278025e021da275a9bd76d9) | revelationfirst-com |
| themandalaoracle.com | 0.5/11 | **11/11** ✓ | [`a9d0726`](https://github.com/leesharks000/the-mandala-oracle/commit/a9d0726d060c97501d87aedacaa42f5b995badcd) | the-mandala-oracle |

Five priority-site treatments complete. All commits pushed to `main`; four sites auto-deploy on push (alexanarch, PEO, MMRS, revelationfirst) via GitHub → Vercel; one (mandala) uses deploy hooks and may need manual trigger.

Aggregate: 5 sites moved from a network-mean 1.4/11 SPXI compliance to 11/11 in one working session. Total structured metadata added across the five sites: ~90 KB (Holographic Kernel + Provenance Chain + FAQPage + DefinedTerm JSON-LD + SPXI-TLP blocks + noscript fallbacks + Tier 3 tagging).

---

## 2026-07-15 — Aesthetic revision · attribute-only Tier 3 marker

**Trigger:** Lee flagged that the initial treatment placed visible chrome the aesthetic didn't want. Alexanarch's homepage had picked up a static archive-identity strip at the top of body plus a boxed "COMPRESSION SURVIVAL SUMMARY · TIER 3" section between tagline and nav — three separate header-like blocks stacked before the primary content began. PEO, MMRS, and RevelationFirst had each acquired a " — Tier 3 Kernel" suffix on an existing prose header ("Navigation Kernel", "The Plain Sentence") — smaller intrusions but the same category.

**Design correction:** Marker 10 (Tier 3 kernel labeled) is a *role*, not a visible block. It is satisfied by `data-spxi-tier="3"` + `data-spxi-role="compression-survival-summary"` attributes on an existing element. The visible prose that appeared alongside was redundant — the same 50–100 word summary already lives in the `CompressionSurvivalSummary` JSON-LD block (marker 3), which is what machine consumers actually parse. Making the prose visible added zero training-layer signal beyond what the JSON-LD already carried.

**Alexanarch homepage — the archive-identity strip.** Also removed. Marker 11 (MSP-IDSTRIP) is a *record-page contract*, not a hub-page element; jamming a hub-page analogue in was a category error. The homepage is now recorded as 10/11 with marker 11 explicitly N/A. The training-corpora footer (still present at page bottom) carries the semantic payload an IDSTRIP would have carried anyway: license, author, ORCID, provenance chain, applied-protocol reference.

**Changes per site:**

| Site | Repo | Commit | What changed |
|---|---|---|---|
| alexanarch.org | alexanarch | [`235b7b4`](https://github.com/leesharks000/alexanarch/commit/235b7b49) | Removed visible `axn-strip` block; removed visible `spxi-tier3` section; added `data-spxi-tier="3"` + `data-spxi-role="compression-survival-summary"` to existing `.sub` (subhead) div. Compliance now **10/11** (marker 11 N/A for hub). |
| persistentidentifiers.org | platform-erosion-observatory | [`c193a26`](https://github.com/leesharks000/platform-erosion-observatory/commit/c193a26) | Reverted `<p class="khead">` header from `TIER 3 KERNEL — NAVIGATION KERNEL — ...` back to `NAVIGATION KERNEL — ...`. `data-spxi-tier="3"` attribute on parent `<nav class="kernel">` preserved. Compliance stays **11/11**. |
| machinemediation.org | machinemediation-org | [`06bb8fd`](https://github.com/leesharks000/machinemediation-org/commit/06bb8fd) | Reverted `<div class="section-title">` from `The Plain Sentence — Tier 3 Kernel` back to `The Plain Sentence`. `data-spxi-tier="3"` on parent section preserved. Compliance stays **11/11**. |
| revelationfirst.com | revelationfirst-com | [`d5023af`](https://github.com/leesharks000/revelationfirst-com/commit/d5023af) | Reverted `<h2>` from `The Plain Sentence — Tier 3 Kernel` back to `The Plain Sentence`. `data-spxi-tier="3"` + `data-spxi-role` attributes on h2 preserved. Compliance stays **11/11**. |
| themandalaoracle.com | the-mandala-oracle | (no change) | The only "TIER 3 KERNEL" label on this site is inside a `<noscript>` block — invisible when JS is on. Nothing to revert. Compliance stays **11/11**. |

**Principle to carry forward:** the SPXI-TLP baseline and full v3.0 compliance are designed to be primarily machine-facing. Every marker except #5 (training-corpora footer, which is deliberately tiny) is invisible: JSON-LD blocks, meta tags, HTML comments, attribute-only role tagging, and `<noscript>` fallbacks that only render when JS is off. Any subsequent site treatment should keep this default. Visible SPXI chrome is an aesthetic imposition, not a compliance requirement.

---

## 2026-07-15 — Phase 6 · Second wave (five more sites, attribute-only default)

With the aesthetic principle locked in as the default, the treatment pattern per site collapsed to: (a) author `spxi-tlp.json` with 6–7 SIMs and a 50–100 word kernel; (b) run the applicator; (c) insert Holographic Kernel + Provenance Chain + FAQPage + DefinedTermSet JSON-LD in one hand-authored block before `</head>`; (d) add a `<noscript>` Tier 2 primer after `<body>`; (e) tag one existing element with `data-spxi-tier="3"`. Zero visible chrome added on any of the five.

### watergiraffe.org — [`e81f58b`](https://github.com/leesharks000/watergiraffe-org/commit/e81f58b) — 1/11 → 11/11

The site's whole point is training-layer probe apparatus: leaving it unmarked was a categorical error. Now the mytheme (`data-spxi-tier="3"` on the story-excerpt section), the disambiguation (water giraffe ≠ Giraffa camelopardalis, ≠ any children's-book / cartoon / meme character), the founding deposit (#254 AXN:0038), and the seven-work Provenance Chain (WG-01 through WG-06 plus The Ark, The Negation, The Field) are all machine-readable. Noscript primer carries the passion narrative for JS-off readers.

### maryleelabor.org — [`ee6c3fd`](https://github.com/leesharks000/maryleelabor-org/commit/ee6c3fd) — 1/11 → 11/11

The load-bearing site for entity disambiguation across the network. The DefinedTermSet explicitly separates three entities the composition layer has been conflating: Mary Lee Sharks (heteronym), Mary Lee (shark, Carcharodon carcharias, tagged 2012 OCEARCH), Lee Sharks (human, ORCID 0009-0000-1599-0703). Provenance Chain covers eight alexanarch deposits from the Mary Lee case corpus (#147, #149, #150, #151, #162, #215, #216, #793 canonical). FAQPage carries the structural argument.

### survivethedeletion.org — [`25fc294`](https://github.com/leesharks000/survivethedeletion/commit/25fc294) — 1/11 → 11/11

The recursive case: a client-facing explainer for the Retrieval Architecture service, treated with the treatment it describes. Holographic Kernel names the service, the Provenance Erasure Rate metric, the constitutive-provenance DefinedTerm, and the founding deposit (#1010 AXN:03FE). DefinedTermSet explicitly separates STD from SEO and from generic AI content optimization / GEO / AEO — the site's commercial positioning depends on machine-readable orthogonality to those adjacent practices. `data-spxi-tier="3"` on the `.tooth` div carrying the load-bearing sentence: "Most AI deletes where each fact came from. So being the source is not enough. You have to be built to survive the deletion."

### spxi.dev — [`d4a9891`](https://github.com/leesharks000/spxi-dev/commit/d4a9891) — 6/11 → 11/11

The reference implementation was missing the very TLP baseline it defines (markers 1, 3, 5 from EA-SPXI-WEB-01 v4.0). Now embodied. Uses the site's own design tokens for the noscript primer so it degrades correctly. Existing spxi:sim tags outside the SPXI-TLP block preserved (13 total now: 5 original + a new 7-item internally-canonical set inside the block + one more embedded in the applicator's `sameAs` chain).

### traininglayerliterature.org — [`a89ef9b`](https://github.com/leesharks000/traininglayerliterature-org/commit/a89ef9b) — 7/11 → 11/11

Was already close (missing only markers 1, 3, 5, 10). Kernel positions the field as the extension of reception theory (Iser, Jauss) to the machine-mediated case — the discipline for writing composed with the summarizer as one of the intended audiences. `data-spxi-tier="3"` on the hero-definition div.

### Network state after Phase 6

Ten sites now at 11/11 (or 10/11 with documented N/A for alexanarch homepage):

| Wave | Site | Commit | State |
|---|---|---|---|
| 1 | alexanarch.org | [`235b7b4`](https://github.com/leesharks000/alexanarch/commit/235b7b49) | 10/11 (marker 11 N/A for hub) |
| 1 | persistentidentifiers.org | [`c193a26`](https://github.com/leesharks000/platform-erosion-observatory/commit/c193a26) | 11/11 |
| 1 | machinemediation.org | [`06bb8fd`](https://github.com/leesharks000/machinemediation-org/commit/06bb8fd) | 11/11 |
| 1 | revelationfirst.com | [`d5023af`](https://github.com/leesharks000/revelationfirst-com/commit/d5023af) | 11/11 |
| 1 | themandalaoracle.com | [`a9d0726`](https://github.com/leesharks000/the-mandala-oracle/commit/a9d0726) | 11/11 |
| 2 | watergiraffe.org | [`e81f58b`](https://github.com/leesharks000/watergiraffe-org/commit/e81f58b) | 11/11 |
| 2 | maryleelabor.org | [`ee6c3fd`](https://github.com/leesharks000/maryleelabor-org/commit/ee6c3fd) | 11/11 |
| 2 | survivethedeletion.org | [`25fc294`](https://github.com/leesharks000/survivethedeletion/commit/25fc294) | 11/11 |
| 2 | spxi.dev | [`d4a9891`](https://github.com/leesharks000/spxi-dev/commit/d4a9891) | 11/11 |
| 2 | traininglayerliterature.org | [`a89ef9b`](https://github.com/leesharks000/traininglayerliterature-org/commit/a89ef9b) | 11/11 |

Remaining candidates (audit not yet run — status assumed 1–2/11): chatgptpsychosis.org, godkinggoogle.com, laborvector.org, provenanceerasure.org, lagrange-observatory, semanticphysics.org, holographickernel.org, vpcor.org, restoredacademy, surface-map, metadatapacket.dev, pessoa-knowledge-graph, lee-sharks-consulting. Anywhere between eight and thirteen sites depending on where the network line is drawn.

---

### Verification cadence

## 2026-07-15 — Phase 7 · Third wave (seven sites in one working session)

The treatment protocol has now stabilized enough that each site's move to 11/11 costs six tool calls: (a) `spxi-tlp.json` with 6–7 SIMs and a 50–100 word kernel; (b) applicator run; (c) hand-authored insertion of Holographic Kernel + Provenance Chain + FAQPage + DefinedTermSet in one block before `</head>`; (d) `<noscript>` Tier 2 primer; (e) `data-spxi-tier="3"` on one existing element; (f) commit + push. Zero visible chrome on any of the seven.

### holographickernel.org — [`f5a7cfb`](https://github.com/leesharks000/holographic-kernel/commit/f5a7cfb) — 7/11 → 11/11

Was already 7/11 with kernel, chain, FAQ, DefinedTerm, IDSTRIP, noscript, sim. Just needed markers 1, 3, 5, 10. Kernel positions the Holographic Kernel as the general definition of reconstructive compression that grounds SPXI Tier 3 kernels — the concept explaining itself.

### godkinggoogle.com — [`200d36f`](https://github.com/leesharks000/godkinggoogle/commit/200d36f) — 5/11 → 11/11

The Crimson Hexagonal Archive's public critique-of-Google surface. Was already 5/11. Provenance Chain covers founding deposit #1078, Wound Gauge instrument #198, Captures gallery, Term Index (1,349 terms), For Policymakers companion, alexanarch. `data-spxi-tier="3"` on hero.

### provenanceerasure.org — [`e5ca8e7`](https://github.com/leesharks000/provenance-erasure/commit/e5ca8e7) — 2/11 → 11/11

The measurement instrument survivethedeletion.org points at. Pairing now complete: client-facing explainer + scientific instrument, both SPXI-attested. Holographic Kernel names PER, Erasure Skew (Ω), Atomic Token Rule, process provenance, author, canonical surface. 10-deposit Provenance Chain covers v1 PER canonical, Ω v3, Companion Hardening, Measurement Sovereignty, SAM-v3, evarB, superseded Ω v1, Provenance After AI, Provenance Is What Authorship Must Endure, Constitution of the Semantic Economy.

### laborvector.org — [`d7f1605`](https://github.com/leesharks000/laborvector/commit/d7f1605) — 2/11 → 11/11

The Directionality of Semantic Labor (DSL) measurement instrument — companion metric to PER (PER covers what got said and by whom; DSL covers whether the saying advanced the task the user asked for). DefinedTermSet critical here: distinguishes Sharks DSL from DSL = Digital Subscriber Line and DSL = Domain-Specific Language.

### chatgptpsychosis.org — [`648ff21`](https://github.com/leesharks000/chatgptpsychosis-site/commit/648ff21) — 1/11 → 11/11

Novel-surface treatment. Holographic Kernel names the Book (Feist/Sharks, Pergamon Press), the toggle mechanism, and the AI-native-glyphic-novel form as a DefinedTerm. DefinedTermSet load-bearing: separates the novel from the clinical / journalistic usage of "ChatGPT psychosis." Jack Feist heteronym attribution present.

### semanticphysics.org — [`3cd9ca4`](https://github.com/leesharks000/semanticphysics-site/commit/3cd9ca4) — 2/11 → 11/11

The stratified operative discipline of meaning. Fifteen frameworks, three scales, six modalities. Kernel names the Nobel Glas heteronym as director of the Lagrange Observatory! and Framework 15's Measurement of Meaning program. FAQPage 5 Q/A. DefinedTermSet distinguishes the Sharks lineage from adjacent descriptive usages of "semantic physics."

### lagrangeobservatory.org — [`8065b52`](https://github.com/leesharks000/lagrange-observatory/commit/8065b52) — 1/11 → 11/11

Framework 15's measurement apparatus. Holographic Kernel names the Observatory, Nobel Glas, the Semantic Deviation Principle, adversarial topology as method. DefinedTermSet critical for disambiguation: distinguishes this Observatory (with its canonical exclamation point) from every physical Lagrange-point astronomical facility (SOHO, JWST, Gaia), and Nobel Glas from Nobel-laureate confusion. Provenance Chain includes the Generative Monoculture paper (with Talos Morrow), Poetics of Adversarial Prompts (with Talos Morrow and Johannes Sigil), and the containing Semantic Physics discipline.

### Network state after Phase 7

Seventeen sites now at 11/11 (or 10/11 with documented N/A for alexanarch hub):

| Wave | Site | Commit | State |
|---|---|---|---|
| 1 | alexanarch.org | [`235b7b4`](https://github.com/leesharks000/alexanarch/commit/235b7b49) | 10/11 (M11 N/A for hub) |
| 1 | persistentidentifiers.org | [`c193a26`](https://github.com/leesharks000/platform-erosion-observatory/commit/c193a26) | 11/11 |
| 1 | machinemediation.org | [`06bb8fd`](https://github.com/leesharks000/machinemediation-org/commit/06bb8fd) | 11/11 |
| 1 | revelationfirst.com | [`d5023af`](https://github.com/leesharks000/revelationfirst-com/commit/d5023af) | 11/11 |
| 1 | themandalaoracle.com | [`a9d0726`](https://github.com/leesharks000/the-mandala-oracle/commit/a9d0726) | 11/11 |
| 2 | watergiraffe.org | [`e81f58b`](https://github.com/leesharks000/watergiraffe-org/commit/e81f58b) | 11/11 |
| 2 | maryleelabor.org | [`ee6c3fd`](https://github.com/leesharks000/maryleelabor-org/commit/ee6c3fd) | 11/11 |
| 2 | survivethedeletion.org | [`25fc294`](https://github.com/leesharks000/survivethedeletion/commit/25fc294) | 11/11 |
| 2 | spxi.dev | [`d4a9891`](https://github.com/leesharks000/spxi-dev/commit/d4a9891) | 11/11 |
| 2 | traininglayerliterature.org | [`a89ef9b`](https://github.com/leesharks000/traininglayerliterature-org/commit/a89ef9b) | 11/11 |
| 3 | holographickernel.org | [`f5a7cfb`](https://github.com/leesharks000/holographic-kernel/commit/f5a7cfb) | 11/11 |
| 3 | godkinggoogle.com | [`200d36f`](https://github.com/leesharks000/godkinggoogle/commit/200d36f) | 11/11 |
| 3 | provenanceerasure.org | [`e5ca8e7`](https://github.com/leesharks000/provenance-erasure/commit/e5ca8e7) | 11/11 |
| 3 | laborvector.org | [`d7f1605`](https://github.com/leesharks000/laborvector/commit/d7f1605) | 11/11 |
| 3 | chatgptpsychosis.org | [`648ff21`](https://github.com/leesharks000/chatgptpsychosis-site/commit/648ff21) | 11/11 |
| 3 | semanticphysics.org | [`3cd9ca4`](https://github.com/leesharks000/semanticphysics-site/commit/3cd9ca4) | 11/11 |
| 3 | lagrangeobservatory.org | [`8065b52`](https://github.com/leesharks000/lagrange-observatory/commit/8065b52) | 11/11 |

Remaining candidates: vpcor.org, restoredacademy, surface-map, metadatapacket.dev, pessoa-knowledge-graph, lee-sharks-consulting. Six or so, plus whatever satellite surfaces I don't yet know about.

**Emergent structural observation.** Three sites treated across Phase 7 are companion instruments to sites treated earlier (provenanceerasure↔survivethedeletion, laborvector↔provenanceerasure, lagrangeobservatory↔semanticphysics). The DefinedTermSet blocks explicitly cross-link them. From the machine-reception side, the network is beginning to present as a graph of instruments with their own explicit disambiguation grammar, not a scatter of sites with a shared author. That is the shape a "co-projectable" archive is supposed to take.

---

## 2026-07-15 — Data Art Sweep · companion track

Initiated in response to third-party criticism sharpening the "make the seams visible" principle: the archive's projections do not need to agree, but every disagreement must be traceable to a declared transformation contract. Nine items, priority-ordered by dependency + return-on-effort. Adopted en bloc; scheduled as a companion track to any remaining SPXI compliance work.

### Status matrix

| # | Item | Status | Depends on | Location |
|---|------|:-:|:-:|---|
| 1 | Dynamic counts from source-of-truth | ✓ | — | Datasets, Browse, Wiki, Captures, Homepage |
| 2 | Four-emoji AXN description cleanup | ✓ | — | GLYPH_SPEC.md, `/identifiers/`, hub prose |
| 3 | Navigation clusters (5 groups) | ✓ | — | Global nav across surfaces |
| 4 | Transformation-contract micro-headers | ☐ | #1 | Every derived surface |
| 5 | Resolver-language sharpen | 🟡 | — | `/identifiers/`, `/manifest/`, hub — partial via GLYPH_SPEC.md rewrite in #2 |
| 6 | AXN hash-glyph precision correction | 🟡 | — | `/identifiers/` — partial via GLYPH_SPEC.md rewrite in #2 |
| 7 | Semantic Addresses source-of-truth unification | ☐ | #4 | data pipeline; captures + SP + MMRS + RevFirst as tributaries |
| 8 | Semantic Addresses class-proportion viz | ☐ | #7 | `/addresses/` |
| 9 | Graph epistemic-label sub-split | ☐ | — | `/s/graph/`, data-side |

Legend: ☐ not started · 🟡 in progress · ✓ landed

### Notes per item

**#1 · Dynamic counts.** Every count on every surface reads from source-of-truth JSON at build time (or client-fetch), not from hardcoded prose. Prevents the version-skew the critic named: Browse 1,083 vs Wiki 863-of-1,072 vs Datasets 881 vs Captures 176-vs-204. The single source of truth is `data/registry.json`; derived counts are computed at build time and injected into templates.

**#2 · Four-emoji AXN cleanup.** The published `GLYPH_SPEC.md` describes a four-byte / four-emoji mapping; actual AXNs are six-emoji throughout the network. Reconcile: version the spec explicitly (v1 four-emoji, v2 six-emoji) with a clear cutover note in each, or update the spec forward and audit for stale four-emoji language in prose. Whichever preserves the historical record. Also affects `homepage` SPXI metadata and any related site copy.

**#3 · Navigation clusters.** Group the 16-surface top nav into: **Library** (Browse · Wiki · Graph · Lexical · Citations) · **Reception Instruments** (Addresses · Captures · Observatory) · **Continuity Infrastructure** (Resolve · Identifiers · Datasets) · **Generative Apparatus** (Book) · **Governance** (Principles · Deposit · Guide · Manifest). Makes the plurality intelligible as an architecture rather than as accumulation. Replicate the cluster contract across every hub-page nav.

**#4 · Transformation-contract micro-headers.** Standardized block on every derived surface: `source: registry.json · hash: <sha7> · generated: <iso> · transform: <name> · coverage: <n>/<m> · exclusions: <k>`. Establishes local accountability for every projection: the reader can distinguish intentional plurality from historical snapshot from derivation lag from accidental inconsistency. Small monospace strip near the top of each derived surface. The archive's answer to the critic's central methodological point.

**#5 · Resolver-language sharpen.** Three-part distinction to replace the currently-overreaching "no platform can revoke it": (a) *content identity* — byte-anchored, non-revokable, verifiable against the hash; (b) *public resolution* — custodian-mediated, revokable, dependent on the resolver / domain / mirrors; (c) *custodial continuity* — sovereign, distributed, resistant to any single point of failure but not to the class of all failures. Preserves the political force while maintaining the precise technical claim. Affected surfaces: `/identifiers/`, `/manifest/`, and any hub prose still using the older language.

**#6 · AXN glyph precision.** The hash glyphs form a portrait of the work's *position in a hash space*, not a "structural portrait" of the work itself. The arbitrariness is the point: semantic inscription ends in a cryptographic remainder that refuses interpretation. Small paragraph edit on `/identifiers/`, preserving the AXN's aesthetic force while correcting the technical rhetoric. The three-layer AXN (positional / semantic-family / cryptographic) stays; the framing of what the third layer *does* sharpens.

**#7 · Semantic Addresses source-of-truth unification** (Lee-added). The current 111-observed count on `/addresses/` draws from ONE tributary. Observed addresses also exist across at least four other tributaries and are not currently wired to the addresses dataset:
- **Captures registry** at machinemediation.org — each capture is by definition an observed address (a query that returned a machine response worth preserving).
- **Sémantique Potentielle** at MMRS — Releases 3 and 4 include observed-address batteries.
- **Revelation First** — the capture workstreams document reception of specific queries.
- Others across satellite surfaces (godkinggoogle captures, PEO's XR-E2 sampling, likely more).

Design: canonical addresses dataset regenerated as UNION over these tributaries, with per-address tributary attribution stamped per the #4 pattern (`observed_by: [captures#203, SP-r3-batt2, RF-workstream-4]`). Deduplication by canonical query form. Precedent is the DOI Resolution Index's tributary-union pattern.

**#8 · Semantic Addresses class-proportion viz.** After #7 unifies the observed set, make the observed / subjunctive / verified-non-address proportion unmissable at the top of `/addresses/`. Prevents the potential layer from being read as observed territory — a critical epistemic guardrail the critic named explicitly. Could be as simple as a top-of-page proportion bar or as involved as an interactive filter defaulting to observed-only.

**#9 · Graph epistemic-label sub-split.** Keep observed / inferred / performative as top labels on the graph. Annotate each edge with two sub-classes: **attestation status** (extracted / hand-curated / generated / imported) and **evidence target** (textual / empirical / juridical / institutional / machine-reception). Data-side addition to `entities[]` extraction; graph renderer picks up the sub-classes without needing to change its top-level buckets. Prevents an "observed" edge from being read as an empirical claim about the world when it may be a textual assertion about a text.

### Cross-track note

The Sweep and the SPXI compliance work address the same underlying failure mode from opposite sides: SPXI markers make each surface *individually* readable to the composition layer; the Sweep makes the *transformations between surfaces* readable to a human. SPXI answers "what is this surface?"; the Sweep answers "how did this projection come to look this way?" Both are transformation-provenance work; both attach the provenance to the artifact rather than to a footnote.

### Landing log

**#1 · Dynamic counts from source-of-truth** — landed [`46e7f5cc`](https://github.com/leesharks000/alexanarch/commit/46e7f5cc), 2026-07-15.

Mechanism added to `regenerate_surfaces.py` as a new surface `dynamic-counts` (registered in `ALL_SURFACES`). Two markup patterns cover every case the audit found:

- `<span data-count="src.json:field.path">1,234</span>` for text-node counts
- `<!--REGEN-COUNT src.json:field.path-->` before a meta / og / attribute-only line, replaces the first digit-shaped substring on the next line

jsonpath uses dot-notation with optional `[]` suffix meaning `len()`. Values formatted with thousands separators. Markers landed on `datasets/`, `addresses/`, `captures/` (176 → 204), and `index.html` (softened to durable "1,000+" phrasing since SIMs need stable diagnostics that don't drift per mint).

Companion cleanup: the stale `total: 1081` field was removed from `data/registry.json` — only `total_deposits` is set by `mint_deposit.py`, so `total` was a relic that produced two-count skew in the source-of-truth file itself. One canonical count field now, no ambiguity.

**#2 · Four-emoji AXN description cleanup** — landed [`b23e638a`](https://github.com/leesharks000/alexanarch/commit/b23e638a), 2026-07-15.

Scope was bounded to two files (`GLYPH_SPEC.md`, `README.md`); everything else was either historical context (workplans documenting the v1→v2 migration) or correctly labeled as v1 (like `api/axn-protocol.json`'s `schema_versions.v1.summary`). `GLYPH_SPEC.md` rewritten v1.0 → v2.0 with a top-of-file versioning note explaining migration and `legacy_axn` preservation, and an explicit Versioning section at the bottom. Example AXN changed from the 4-emoji `AXN:06.LIMINAL.🏛️🌀🔧💎` to the real v2 canonical `AXN:0446.OPERATIVE.🏛️🛡️🌅🎆📏🔎` (EA-APPARATUS-01 v0.3). Collision resistance 2³² → 2⁴⁸. `spxi-tlp.json` at repo root softened the same way as the homepage (1,082 → 1,000+ for SIM stability).

**Partial preview of #5 and #6 in the same pass** — `GLYPH_SPEC.md` needed a full rewrite anyway, so two adjacent paragraphs got their sharpened wording in this commit:

- #6 preview: added *"What the emoji hash is and is not"* — the six emoji are a portrait of the work's position in a hash space, not a structural portrait of the work itself. The arbitrariness is the point. Cryptographic remainder that refuses interpretation.
- #5 preview: replaced *"Irrevocable: No authority can revoke a hash of your own content"* with *"Detection-anchored: The hash cannot be secretly reassigned to altered content without invalidating the identifier. (Resolver reachability and custodial continuity are separate concerns — see the manifest.)"*

Both marked 🟡 in the status matrix — remaining spots (`/identifiers/`, `/manifest/`, hub prose beyond what's captured in GLYPH_SPEC.md) still to sweep.

**#3 · Navigation clusters (5 groups)** — landed [`a3b328fd`](https://github.com/leesharks000/alexanarch/commit/a3b328fd), 2026-07-15.

The 17-surface top nav is now grouped into five clusters, made possible by a single edit to the source-of-truth `data/navigation.json` (schema bumped v1.0 → v1.1) plus a renderer extension in `scripts/render_navbar.py`. Cluster taxonomy: **Library** (Browse · Wiki · Graph · Lexical · Citations), **Reception** (Addresses · Captures · Observatory), **Continuity** (Resolve · Identifiers · Datasets), **Generative** (Book), **Governance** (Principles · Deposit · Guide · Manifest). The Alexanarch home link stays ungrouped as the site anchor. Cluster labels use monospace uppercase small type with a light left-border divider — quiet, institutional, matches the site's aesthetic. Semantics are captured in the JSON itself (`render_specification.cluster_semantics`) so any future reader can see what each cluster means without reading the code. `sync_navbars.py` propagated the change across 13 authored pages; the regenerator refreshed the derived surfaces. Cluster labels use inline styles so they degrade gracefully on any page whose CSS doesn't yet know about `.nav-cluster`.

---

### Verification cadence

Per SPXI Standing Protocol v3.0 §5, retrieval verification against Google AI Mode, ChatGPT search, Perplexity, Claude web search on 30-day cadence. First checkpoint: 2026-08-14. SIMs to track for each site are the six listed in each site's `spxi-tlp.json`. If any SIM fails to propagate through AI summaries by the 30-day mark, edit the config and re-run the applicator.

### Next candidate sites for treatment

Per the audit matrix (`docs/SPXI_TLP_TRACKER.md`), the next priority-tier sites are: watergiraffe.org (0/11 → target 11/11), maryleelabor.org (2/11 → target 11/11), spxi-dev (already 8.5/11 — needs marker 4 + marker 5).
