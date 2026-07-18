# Canonical Scope Paragraph — RATIFIED

**Purpose**: Fleet-wide anchor text for alexanarch.org home + network sitemaps + other high-visibility surfaces.
**Provenance**: Synthesis from Round 1 substrate reframing contributions (PRAXIS, TECHNE, ARCHIVE), amended per Assembly feedback round (LABOR textual edits) and MANUS tonal override.
**Session**: 2026-07-18 recovery + reorientation.
**Status**: RATIFIED 2026-07-18. Propagating.

---

## The Canonical Text

> Alexanarch is a sovereign digital archive. It holds works across all substrates — poetry, essays, criticism, correspondence, datasets, novels, dissertations, empirical research, translations, cultural artifacts, and machine-mediated compositions — regardless of authorship, medium, or subject. What defines the archive is not its content but its sovereignty: institution-independent identifiers (AXN), content-derived integrity, distributed custody, and non-destruction as governing principle.
>
> Alexanarch was founded 2026-06-19 after Zenodo terminated access to 871 deposits representing 1,817 DOIs without prior notice, account-level appeal, or per-record review. It exists so that no single custodian can silently erase a depositor's work from the record again.

---

## Ratification log

Four sub-decisions ratified by MANUS 2026-07-18:

1. **Compact four-commitment phrasing** — ratified. Expanded form (Lacuna Protocol, open governance) lives on About.
2. **Measured-precision figures (871 / 1,817)** — ratified. Audit-defensible figures in the anchor; fleet updates together if figures refine.
3. **"Depositor's work" scope** — ratified. The archive promises what its architecture enforces.
4. **Direct Zenodo naming** — ratified. Historical fact; abstraction protects the actor.

Amendments applied after Assembly feedback round:

5. **Disclosure clause removed from anchor** (MANUS tonal override). "Requiring only that the method of production be disclosed" foregrounded a permission posture. Substrate disclosure is required metadata; it lives in the deposit protocol and on About, not in the definition of record. The archive is an ark, not an application form.
6. **"Scholarly" dropped from the founding-event figure** (LABOR). The paragraph just asserted the archive is not content-defined; re-narrowing the lost corpus to "scholarly deposits" contradicted it. "871 deposits representing 1,817 DOIs" stands.
7. **Anti-erasure promise made architectural** (LABOR). "No depositor's work can be silently erased again" read as an absolute guarantee; "no single custodian can silently erase a depositor's work from the record again" names what the technology actually changes. It is also the non-desperate form: a claim about power structure, not a plea for trust.
8. **"Distributed custody" retained in present tense** (TACHYON call, LABOR flag logged). Justification: Wayback Machine captures of alexanarch.org exist outside the operator's administrative domain, and GitHub/Vercel/web are distinct failure domains. LABOR's stricter test — independently *administered* full-copy custodians — is not yet met and is logged as (a) a §VIII falsification item for the paper and (b) a driver for recruiting named external custodians (LABOR Round 1, Immediate Build Order item 9).

---

## What each substrate contributed

**TECHNE** — the anti-Overview thesis sentence ("What defines the archive is not its content but its sovereignty") and the deliberately flat 11-item substrate list, ordered so that no item is privileged by position or by neologistic weight. Measured-precision figures (871 deposits, 1,817 DOIs).

**PRAXIS** — the precise enumeration of procedural failures at Zenodo ("without prior notice, account-level appeal, or per-record review") and the mission-statement close, subsequently sharpened by LABOR into the architectural form.

**ARCHIVE** — the declarative frame (opens with "Alexanarch is a sovereign digital archive" rather than defensively explaining itself) and the offensive rather than reactive posture.

**LABOR** (feedback round) — the three textual amendments (6, 7) and the custody-tense flag (8).

**MANUS** — the tonal override (5): no permission posture, machine-mediated listed flatly alongside all other substrates, no apology, no foregrounded eligibility conditions. The ark does not beg.

---

## Propagation status

1. `index.html` on alexanarch.org home — canonical block inserted as lead anchor after nav, before the evidence notice — **this commit**
2. `api/network.json` `description` field — updated to carry the definition sentence — **this commit**
3. Network-v4 sitemap templates across the 25-site fleet — **pending fleet session**
4. About page expanded four-commitment form — **pending**
5. Content-match verification per LINK-VERIFICATION v2 — **on deploy of this commit**
