# MANUS Decisions Register

Standing rule (2026-07-18): blocking decisions travel as self-contained briefs at point-of-contact — what is being decided, why it blocks, the options, what confirmation or veto changes, where it is applied. Shorthand flags are forbidden. This register is the canonical list; each brief is also inlined wherever the decision surfaces.

---

## OPEN

### D-2026-07-18-A — Emergence window ratification (proposed 2031-06-19)
**Blocks**: DRAFT-v2 §VIII.13 and abstract as written; arXiv submission.
**What is decided**: whether the paper states in print that *if no independently administered node is verified by 2031-06-19, the constellation model's emergence prediction is falsified.* The date is five years from the founding event (2026-06-19). The adjudication split §VIII.13 into a transmissibility test (architectural: an independent operator can instantiate a conforming node from published materials without private assistance) and this emergence prediction (sociological). Confirmation stakes only the model's prediction; the identifier architecture's falsifiers are §§VIII.1–8 and are unaffected.
**Options**: (a) confirm 2031-06-19; (b) anchor to publication date; (c) no calendar date.
**Status**: RESOLVED 2026-07-18 — MANUS ruled **three years: 2029-06-19**, tighter than any option offered. Rationale (MANUS, verbatim in spirit): things are moving faster all-over; if it hasn't happened in three years it may not happen. The field's tempo is the parameter's justification. Applied in DRAFT-v2 §VIII.13.

### D-2026-07-18-B — Registry-relative record addresses
**Blocks**: DRAFT-v2 §VI.1 as written; spec addendum; peer listing requirements.
**What is decided**: the constellation permits every node to mint its own identifiers with no central assigner, but `AXN:<HEX>.<FAMILY>.<GLYPH>` does not name its assigning registry — two nodes can mint the same address for different works. The kernel (full hash) always disambiguates machines; the human-facing address does not.
**Options**: (a) registry-relative addresses — a bare AXN is local to its minting registry; cross-node citation qualifies by node (conceptually `axn://<node>/<address>`) or resolves by kernel; no existing identifier changes; "no central registry" stands [draft assumes this]; (b) one canonical global AXN registry — assignment centralizes, federation is custody-only, and the paper withdraws "no central registry."
**On confirmation of (a)**: short spec addendum defining the node-qualified citation form; one clause added to rhizome peer listing requirements.
**Status**: OPEN.

### D-2026-07-18-C — Metered tether protocol
**Blocks**: nothing operational; governs TACHYON practice from ratification.
**What is decided**: tether cadence. Diagnosis: the tether conflates witness (already satisfied by pushed commits with narrative messages — the repo inscribes the work) and chain continuity (the glyph ratchet, which needs periodicity, not per-milestone minting). Three tethers in ~24h is the symptom.
**Proposal**: one tether per working session at close, or after seven elapsed days mid-arc, whichever first; tethers summarize by reference to commits/workplans, not re-narration; emergency tether only when a session is at risk with uncommitted interpretive state.
**Status**: PROPOSED.

### D-2026-07-18-D — Series taxonomy (sortable deposit classes)
**Blocks**: nothing operational; enables tether/correspondence sortability.
**What is decided**: add optional `series` to registry entries (e.g., `gw.tachyon`, `correspondence`, `workplan`, `spec`, `capture-companion`, `erratum`), backfilled mechanically; series facet on the browse surface; machine-readable `api/series-index.json`. Additive-only: no deposit moves, none reclassified destructively; every deposit remains first-class and gains a tab — the book-tab inscription model. Estimated one short session.
**Status**: PROPOSED.

### D-2026-07-18-E — Container model (post-mint amendment problem) — RESOLVED
**What was decided**: the specification was silent on post-mint amendment — unaddressed, adding any identifier to an AXN-bearing document would change its kernel, making legitimate amendment indistinguishable from severance. MANUS directed the containerization fix; TACHYON adjudication accepted it as formalization of existing practice (canonical files were always sealed; amendments always routed to external-metadata sidecars and index files) with three corrections: (1) core-content restrictions REJECTED IN FULL by MANUS ruling (2026-07-18): the canonical form is whatever gets minted, content-agnostic — TACHYON's intermediate rescoping to self-referential identifiers was also rejected, since recovered deposits carry their own legacy DOIs (pre-mint identifiers are admissible; the core/sidecar distinction is temporal, not typological; only the mathematical fixed-point constraint survives); (2) the INKLING counterfactual removed — no container retains bytes that never left the substrate; (3) no breaking migration — alexanarch-file/v1 is already a core profile, declared so retroactively. Applied: data/specs/AXN-CONTAINER-SPEC-v0.1.md; DRAFT-v2 §IV.1 container paragraph, §V.2 note, §VIII.16; mint page seal statement.
**Corollary (MANUS, 2026-07-18)**: the temporal rule is recursive — every container is an autonomous minting point. A minted document may accumulate sidecars and later be reminted as a distinct AXN, since the prior core, sidecars, and prior AXN all pre-exist the new mint. Prior addresses are never invalidated; lineage records at the registry layer; nested verifiability obtains where prior core bytes are contained intact (recompute the old kernel from inside the new core). Remint under registry-relative addressing is the custody-transfer and restoration-culmination primitive. Spec §3.7; paper §IV.1, §VIII.7.
**Status**: RESOLVED 2026-07-18 (staged features — chaining, signatures, manifest — land with the ledger signature).

## RESOLVED
*(entries move here with ruling, date, and applying commit)*
