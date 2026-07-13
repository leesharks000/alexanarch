# MSP-ROLLOUT — Mandala Surface Protocol: Fleet Application Plan & Tracker

**Status: ACTIVE · living document · append to the progress log every session that touches it**
**Governing standard:** EA-APPARATUS-01 v0.3 — deposit #1077, AXN:0446.OPERATIVE.🏛️🛡️🌅🎆📏🔎 — canonical text at https://www.alexanarch.org/s/records/1077/ (full MD: /data/deposits/AXN-0446.md)
**Reference surfaces:** persistentidentifiers.org (release 1.1.0, content commit 887270e + exactness patch 792216c — THE reference implementation, Chorus-certified) · themandalaoracle.com (rite apparatus: commits 34a062b, 155cae2, e95c6df, 046823a)
**Canonical tokens contract:** platform-erosion-observatory `assets/msp-tokens.css` (PEO skin); the contract classes are skin-independent — `.lemma .term .axn-chip .witness-row .w-chip .state .idstrip .helix .mspcolophon .doors .obol` — skinned per surface via `--msp-*` vars (spec §11: four skins, one grammar).

## 0. How to walk this document (any instance, any session)

1. Read this file top to bottom once.
2. Read the spec at the deposit URL above (§§2–9 are binding; §12 is the adoption map this plan extends).
3. Check the tracker (§5). Find the first row whose next unchecked gate you can advance.
4. Respect the gates (§4). Nothing ships to a Tier-1 surface without MANUS eyes on a preview. Tier-2 mechanical ships on the batch-exemplar approval recorded in the log.
5. Append to the progress log (§7) before session close: date, rows advanced, commits, anything a future instance must know.
6. Standing rules: session PATs rotate at day close and are never written into any file; pushes to many repos are STAGGERED (Vercel deploy limits — max ~6 site deploys per batch, batches hours apart); deploy verification for domains outside the sandbox allowlist is done against `raw.githubusercontent.com/<repo>/<sha>/<file>` (deploy-source verification), with live-domain content-match (Rule 28) left to MANUS's browser.

## 1. The two-layer model

Every application decomposes into:

**MECHANICAL (scriptable, ~80% of labor, 0% of judgment):**
- Inject tokens contract (inline `<style>` block preserving single-file ethos, PLUS vendored `assets/msp-tokens.css`)
- Identity strip at apex: full AXN with six-emoji glyph (pull from registry.json — NEVER from memory, per AXN-integrity rule), title, object state, version/founding date, canonical URL, deposit chip
- Link typing: `alexanarch.org/s/records/N/` links → `class="axn-chip"`; `alexanarch.org/data/*.json` links → `class="w-chip"`
- §7 colophon at foot: every schema field, unknowns stated as `unknown` never omitted; `repository_commit` filled via the two-commit dance (commit content → fill SHA → commit "colophon: repository_commit=X"); `render_sha256` computed with its own field's value set to `null` (self-excluded convention, stated inline)
- Doors: 2–3 verbs from the manifest

**EDITORIAL (MANUS or instance judgment under MANUS gate; cannot and must not be scripted):**
- Nuclei (lemma) selection: at most one per block; skip sections whose device is numbering or whose candidate is weak — a weak lemma is worse than none (precedent: PEO taxonomy left deliberately bare)
- Triple-helix placement: only where severed DOIs are actually cited; cohort values are LEGEND, individual identifiers get per-slot states from dated captures; UNQUERIED is a state, not an omission (spec §6)
- Obol register decision: evidentiary surfaces carry cost-of-custody AS DATA in the sober register (exemplar: PEO obol block); narrative surfaces MAY carry it diegetically (Obol Rule — the membrane is load-bearing; nothing crosses in either direction)
- Witness rows: only where witness artifacts exist to link (Rule 6: named witnesses without artifacts are personalized favicons)
- Exactness pass: operator-vocabulary discipline (instrument/repository/registry operator), quotations verbatim, claims scoped to what is proven (model: the ten-item Chorus patch, PEO commit 792216c's message is the checklist)

## 2. Manifest schema — `msp.json` (one per site repo, at root)

```json
{
  "surface_id": "example.org",
  "canonical_url": "https://example.org/",
  "axn": "PULL FROM registry.json — full form with glyph",
  "deposit_number": 0,
  "title": "…",
  "object_state": "canonical | draft | superseded",
  "tier": 1,
  "register": "evidentiary | narrative",
  "skin": { "--msp-lemma": "…", "--msp-chipfg": "…", "…": "override only what differs from PEO defaults" },
  "doors": [ {"label": "Verb phrase", "href": "…"}, {"…": "2–3 total"} ],
  "index_files": ["index.html"],
  "notes": "anything site-specific the applicator must respect"
}
```

## 3. Applicator — `msp_apply.py` (TO BE BUILT, session A)

Home: this repo, `scripts/msp_apply.py`. Reads a target repo's `msp.json`, performs the mechanical layer idempotently (marker comments guard double-application), runs the colophon two-commit dance, pushes. Fanout mode: iterate a list of cloned repos, batch-limited per the stagger rule. Precedent muscle: `scripts/fanout.py` (the 25-repo DOI link-repair campaign).

## 4. Gates (from spec §12, extended)

- **Tier 1:** manifest → mechanical apply on a branch or preview copy → static preview → MANUS eye → editorial pass (nuclei proposed by instance, MANUS veto per item) → ship → deploy-source verify → tracker tick.
- **Tier 2:** manifest → mechanical apply. ONE exemplar satellite goes to MANUS preview first; on approval (record it in the log), the remaining Tier-2 fanout ships without per-site preview. No editorial layer; no lemmas on satellites.
- **Special/narrative:** register decision by MANUS per site BEFORE any apply.
- **alexanarch:** generator project — apparatus goes into `scripts/regenerate_surfaces.py` record-page template + homepage, NOT into 1,077 pages by hand. Own session. ASCII figure-parity rule applies to deposits going forward (spec §5.4).

## 5. Fleet tracker

Legend: M=manifest · A=mechanical applied · E=editorial pass · ✓=MANUS approved · D=deployed & deploy-source verified. Fill with commit SHAs, not checkmarks alone.

### Done / reference
| repo | domain | status |
|---|---|---|
| platform-erosion-observatory | persistentidentifiers.org | **REFERENCE** — release 1.1.0; 887270e + 792216c (exactness); live-domain Rule 28 check remains with MANUS (domain not in sandbox allowlist) |
| the-mandala-oracle | themandalaoracle.com | rite apparatus live (Specimen Rule, states, tether, marks, carry-keys: 34a062b…046823a) · REMAINING: token-alignment to canonical contract (small; fold into session B) |

### Tier 1 — full apparatus (mechanical + editorial)
| repo | domain | M | A | E | ✓ | D | notes |
|---|---|---|---|---|---|---|---|
| alexanarch | alexanarch.org | | | | | | GENERATOR PROJECT — own session (session C); template-level |
| machinemediation-org | machinemediation.org | | | | | | Capture Registry entries as quaestio-numbered apparatus w/ states (spec §12) |
| semanticphysics-site | semanticphysics.org | | | | | | ~14 frameworks; falsification conditions are native claim-state material |
| leesharks.com | leesharks.com | | | | | | TikTok Primer v2.0 pending on same surface — coordinate |
| lee-sharks-corporate | semanticeconomy.org | | | | | | SPECIFIED BY MANUS 2026-07-13: this repo serves semanticeconomy.org. Partial apparatus already applied — DIFF against canonical contract before touching; reconcile, don't overwrite |

### Tier 2 — mechanical only (strip · tokens · colophon · chips · doors; NO lemmas)
watergiraffe-org (watergiraffe.org) · traininglayerliterature-org (traininglayerliterature.org) · surface-map (surfacemap.org) · spxi-dev (spxi.dev app) · spxi-protocol (spxi.dev spec) · revelationfirst-com (revelationfirst.com) · restoredacademy (restoredacademy.org) · lagrange-observatory (lagrangeobservatory.org) · laborvector (laborvector.org) · provenance-erasure · vpcor-org (vpcor.org) · living-architecture-lab (livingarchitecturelab.org) · holographic-kernel (holographickernel.org) · maryleelabor-org · metadatapacket-dev · pessoa-knowledge-graph · lee-sharks-consulting
— each row: M/A/D columns only; track in the progress log as batches (B1, B2, …), ≤6 deploys per batch.

### Special register — MANUS decision before touching
| repo | note |
|---|---|
| godkinggoogle | narrative surface — Obol Rule diegetic register candidate |
| secret-book-of-walt | narrative surface — same |

### Excluded / not sites
| repo | reason |
|---|---|
| semantic-economy | file dump, not a site (MANUS, 2026-07-13) |
| data-rhizome | private data repo — substrate, not surface |
| evarb-co-signatures | DOI pointer repo |
| mandala-oracle | possible legacy duplicate of the-mandala-oracle — VERIFY with MANUS before any action |

### Inventory tail
41 repos total accessible; first 30 reviewed 2026-07-13. **Session A must enumerate the remaining 11** and place them in tiers or exclusions.

## 6. Session plan

- **Session A:** build `msp_apply.py` + manifest generator; enumerate inventory tail; manifests for all Tier 2; ONE exemplar satellite → MANUS preview → on approval, fanout batch B1 (≤6). Estimated: one session.
- **Session B:** remaining Tier-2 batches (B2, B3…); oracle token-alignment; Tier-1 mechanical applies + preview copies for machinemediation, semanticphysics, leesharks.com, lee-sharks-corporate (diff-first).
- **Session C:** Tier-1 editorial passes with MANUS (nuclei proposed per site, veto per item); alexanarch generator project.
- **Session D (buffer):** exactness passes (Chorus review invited per Tier-1 surface, per the PEO precedent), stragglers, v1.0 designation review per spec §12 gates.

## 7. Progress log (append-only)

- **2026-07-13 (TACHYON, founding session):** Standard deposited (#1077, hex-collision pipeline bug fixed in same commit d03c009). Oracle Phase 1 + reader-experience design + tether/checksum/marks/carry shipped (34a062b, 155cae2, e95c6df, 046823a; cache-bust v=8). PEO full apparatus + nine nuclei (887270e), ten-item Chorus exactness patch (792216c), certified reference at release 1.1.0. Canonical tokens contract established at peo/assets/msp-tokens.css. Fleet enumerated (30/41). This plan written. PAT of the day rotated at close per standing rule.
