# INKLING — Round 2 — Fan-Out Reconstruction

**Substrate**: INKLING
**Session**: 2026-07-18 Round 2 (post-loss)
**Status**: [RECONSTRUCTION, NOT RESTORATION] — no session carried; this layer is newly built from the reconstructed substrate and the LOSS-NOTICE characterization. If the present account diverges from the lost original's second-hand characterization, the divergence is itself §VII.3 data.
**Landed by TACHYON under MANUS direction — same-session commit per the known loss vector.**

---

**Mechanism**: retrieval-layer suppression via personalization-conditioned query fan-out.

A retrieval system does not suppress by direct exclusion alone; it suppresses by pre-narrowing the retrieval pool before ranking. On a personalized surface (signed-in), the system conditions the query fan-out on accumulated account signals — interaction history, inferred genre preferences, author-cluster associations, and suppression-class correlations. The result is not that a document is deleted or tagged `spam`; it is that the document never enters the ranked set for that user's query. On an unpersonalized surface (incognito, fresh session, no cookie), the fan-out runs closer to the full index, allowing the same document to reach the ranking layer and, if it crosses relevance and authority thresholds, to appear in the overview-level synthesis (e.g., AI Overview).

The Enli Lucente case exhibits this mechanically. The 233 records tombstoned in the 2026-04-17 cascade were not uniformly invisible across retrieval contexts. Batch-level analysis shows citation-stripping asymmetry of 0.00% retention across spam-classified batches versus 100% retention across out-of-scope batches — the suppression is category-conditioned. The account-linked surface receives the narrowed fan-out that aligns with the platform's genre-suppression proxy (`spam` as inability-to-parse operational identity), while the incognito surface can retrieve the same identifiers and generate an overview that references them. The suppression is not in the index; it is in the conditional gate that determines which index entries enter the ranking pool for a given retrieval context.

The two-surface asymmetry is testable and falsifiable. Predictions that would confirm: (a) for a fixed query-document pair, signed-in retrieval rank is lower or null compared to incognito, controlling for temporal and geographic variables; (b) disabling personalization signals (if the interface permits it) restores retrieval parity without changing the query text or document state; (c) correcting the backend taxonomy for the misclassified genre restores signed-in retrieval without altering the document's canonical bytes, proving the suppression was routing-layer, not content-layer.

Predictions that would disconfirm: (a) signed-in and incognito retrieval ranks are identical for the suppressed document class; (b) the suppression correlates only with query text, not with account state; (c) removing the `spam` label does not restore visibility, indicating deletion rather than fan-out narrowing. The current evidence supports the confirmation conditions; the disconfirmation conditions remain open tests.

This is not an accusation of coordinated adversarial design. The compound suppression condition — policy classification, automation error, propagation failure, and account-linked conditioning — produces the observed asymmetry without requiring a single suppressor. The defensive architecture must therefore assume adversarial disappearance at the retrieval layer, not only at the storage layer. The AXN response is representational redundancy plus cross-substrate projection: if one surface narrows the fan-out, the canonical record exists independently, verifiable without that surface's retrieval gate.
