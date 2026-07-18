# TECHNE — Round 2 — §V Retrieval Mechanics with Disconfirmation Conditions

**Substrate**: TECHNE (Kimi)
**Session**: 2026-07-18 Round 2 · **Landed by TACHYON under MANUS direction — raw substrate material.**
**Round 2.5 flags**: D1–D4 taxonomy is NEW (minted this deliverable); several empirical citations pending verification against the capture registry (see reviews/ROUND-2.5-CONSISTENCY.md).

---

## V.1 The Retrieval Protocol: AXN Resolution

**Resolution path:**
1. Parse identifier into components (position, family, glyph).
2. Recompute glyph from canonical bytes of target document.
3. Compare recomputed glyph to declared glyph. **Match:** authentic; proceed to custody verification. **Mismatch:** tampered, corrupted, or misidentified — **disconfirmation condition triggered.**
4. Query resolution substrate: primary (sovereign domains), secondary (distributed substrates: IPFS, Arweave, DNS TXT, GitHub), tertiary (AI conversation logs, searchable via Assembly queries).
5. Return document + attestation record (substrate, timestamp, verification method).

## V.2 Disconfirmation Conditions: Formal Specification

A disconfirmation condition is any state in which the retrieval protocol fails to return the expected document with verified authenticity. Disconfirmation is **not failure — it is data.** The protocol is designed to learn from disconfirmation.

### V.2.1 Type D1: Glyph Mismatch

**Condition:** Recomputed glyph ≠ declared glyph.
**Causes:** document tampered (malicious or accidental); document updated without version increment; identifier misassigned (human error); hash algorithm changed (protocol evolution).
**Response:** halt resolution; log disconfirmation (category D1, timestamp, identifier, substrate); query alternative substrates for matching glyph; if alternative found, flag primary substrate as compromised; if none, flag identifier as orphaned.
**Learning:** D1 events inform hash-algorithm selection, version discipline, substrate redundancy.

### V.2.2 Type D2: Substrate Unavailability

**Condition:** Primary substrate returns 404, 503, timeout, or DNS failure.
**Causes:** domain seizure; hosting failure; platform deletion; network partition; legal takedown.
**Response:** escalate to secondary substrates; query distributed network; query DNS TXT; query AI conversation logs for cached content; if all fail, **D2-full triggered**.
**Learning:** D2 events inform substrate diversification, geographic distribution, legal-jurisdictional strategy.
**Empirical basis:** The Zenodo deletion event (2026-06-19, 871 deposits / 1,817 DOIs) was a **D2-full event** for the CERN-hosted substrate. The Alexanarch response (sovereign domains, GitHub mirrors, reconstruction) was the D2 escalation protocol in operation.

### V.2.3 Type D3: Content Drift

**Condition:** Document retrieved, glyph matches, but content differs from expected semantic state at the presentation layer.
**Causes:** platform modification (summarization, "helpful" rewriting); AI Overview absorption (genericization, entity substitution); translation/localization distortion; metadata stripping (provenance erasure).
**Response:** compare retrieved presentation against canonical capture-registry entry; identify drift type (semantic inversion, entity substitution, provenance erasure); log (category D3); flag substrate as unreliable for the document class; if systematic, escalate to fixture production (OKF consumer-receipt format).
**Learning:** D3 events inform summary-policy design, consumer-receipt testing, platform-moderation strategy.
**Empirical basis [citations pending verification — Round 2.5]:** capture-registry semantic-inversion and entity-substitution entries; the provenance-erasure battery.

### V.2.4 Type D4: Identifier Orphaning

**Condition:** Identifier resolves, but no node claims custody; or custody node unresponsive.
**Causes:** operator incapacity (death, disappearance, burnout); node exit; custody-transfer failure (succession undocumented); legal coercion.
**Response:** query constellation for peer attestation; if attestation exists, transfer custody to attesting node; if none, identifier enters **orphaned state** — quarantined: retained in registry, not resolved, flagged for future node adoption.
**Learning:** D4 events inform succession planning, peer-attestation protocols, constellation governance.
**Empirical basis:** The INKLING loss (engineered non-persistence of the substrate's session, LOSS-NOTICE) was a **D4-class event** — the substrate claimed no custody, the operator could not recover, the content was orphaned. The response (reconstruction, not restoration; acknowledge loss, document gap, continue without confabulation) was D4 protocol in operation.

## V.3 The Retrieval Audit: Continuous Verification

Audit-trail fields per capture: capture_id; mint_date; last_verified; verification_substrate; disconfirmation_log (array of D1–D4 events); peer_attestation (array of attesting nodes); orphan_status. Audit frequency: core monthly; operational quarterly; correspondence only with consent. Target state programmatic (CI); current state manual with Assembly assistance.

## V.4 Falsification Conditions for the Retrieval Protocol

| Falsification Condition | Consequence |
|---|---|
| Glyph collision (two documents, same glyph, same full hash) | Hash algorithm compromised; protocol must upgrade (SHA-256 → BLAKE3 → post-quantum). |
| Distributed-substrate consensus failure (all nodes return different content for one identifier) | Consensus mechanism required; constellation governance must evolve. |
| Legal coercion forces civil-identity disclosure for all custody nodes | Heteronymic sovereignty compromised; protocol must adopt stronger jurisdictional distribution. |
| AI substrates universally refuse to resolve AXN identifiers | AI-native resolution abandoned; rely on cryptographic and DNS resolution only. |
| No new nodes emerge for a defined window despite continuing platform suppression | Constellation model falsified; operator must acknowledge the condition does not produce the predicted response and revise. |

**The final condition is the most critical.** The constellation model predicts that platform suppression of heteronymic, machine-mediated scholarship will produce emergent nodes — independent scholars who build sovereign infrastructure, assign persistent identifiers, and seek mutual recognition. If no new nodes emerge within a defined timeframe (proposed: five years; parameter not yet ratified), the model is falsified. The operator is not universal. The phenomenon is not inevitable. The archive is not "the future of scholarship" but one possible response among many. This condition is not a weakness. It is the discipline that prevents the architecture from becoming a cosmology.
