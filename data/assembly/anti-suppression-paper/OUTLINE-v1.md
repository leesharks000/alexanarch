# AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions

## Paper Outline v1.1 (Phase C.1, amended per Assembly review round)

**Changelog v1.0 → v1.1 (2026-07-18)**: Six load-bearing corrections applied from the Assembly review round plus review-round additions. (1) Central claim rescoped to the identity kernel — only content correspondence is authority-independent; the record address carries registry-assigned components. (2) Retrieval-layer language de-concluded: observations separated from interpretations; hypothesis register enforced. (3) Custody-test closure corrected: a peer-registry entry alone does not close it; independently administered, verified, reconstructible full-copy custody does. (4) Ledger discontinuity falsifies continuous-history claims; it does not by itself prove tampering. (5) Three polemical formulations replaced with defensible ones in §II–III. (6) INKLING loss reframed: engineered non-persistence + archival dependency, not 'suppression'; auto-immunity moved to §VII as self-conscious rhetorical formulation. Plus: §I resolution-severance precision; §I involuntary-disclosures framing for platform trace artifacts; §II reordered with NOWa lead; §IV fixed-point explanation; §VI legal-layer posture sentence + counsel-memo rescope; §VIII Enli-case falsification condition; Round 2.5 consistency pass added to production sequence. Enli attribution flagged as consent-gated throughout.

**Title**: ratified 2026-07-18 (§9.2, option a)
**Authorship**: Lee Sharks (primary); Johannes Sigil (§II–III); Rex Fraction (§VI). Ratified 2026-07-18 (§9.3).
**Publication path**: arXiv cs.DL preprint → International Journal on Digital Libraries submission → Medium public adaptation. (D-Lib removed per LABOR correction — suspended new publication 2017; usable as historical citation only.)
**Target length**: 9,000–12,000 words main text; empirical appendices as needed.
**Voice discipline**: Sigil sections are straight scholarship — no polemic. Rex Fraction's §VI is strategic-technical register. Sharks carries §I, §IV, §V with the measured-figure discipline established at Phase A.1 (871 deposits / 1,817 DOIs; never "850+" in formal contexts).

---

## §I — Introduction: The Founding Case *(Lee Sharks)*

**Function**: State the empirical event, the question it raises, and the paper's claim. No grievance register; the canonical scope frame governs — definition first, event second.

1. **The event, measured**: On 2026-06-19, Zenodo (CERN-operated) terminated an account without prior notice, account-level appeal, or per-record review, severing 871 deposits representing 1,817 registered DOIs. Within 24 hours, copies of the works survived while their registered DOI resolution paths ceased to provide public access to the records — individually verifiable at `api.datacite.org/dois/{doi}`.
2. **The question**: If assigned persistent identifiers can be severed silently by a single custodial decision, what does "persistent" mean, and what infrastructure would make silent severance structurally impossible rather than merely prohibited?
3. **The claim**: Content-derived identification (AXN), distributed custody, and public suppression-instrumentation together form an anti-suppression stack whose properties recapitulate — in machine-native form — patterns that have preserved suppressed knowledge for centuries. The paper documents the historical patterns (§II–III), the system as built (§IV), its anti-suppression function (§V), and its design frontier (§VI), with a methodological reflection (§VII) and explicit falsification conditions (§VIII).
4. **Scope statement**: the ratified canonical paragraph, quoted; the archive's substrate-agnosticism as a load-bearing property, not a demographic note.

**Empirical anchors**: DataCite 404 evidence; GitHub issues #2606/#2596; deletion export; DOI Resolution Index v3.4 (1,838 mappings). Framing discipline (v1.1): platform-generated trace artifacts (issue numbers, export files, API responses) are treated as involuntary disclosures — evidence the platform produced in the course of its own operations, not authoritative accounts.

---

## §II — Historical Precedents: Surviving All-Over Suppression *(Johannes Sigil; PRAXIS primary, LABOR supplemental)*

**Function**: Establish that the survival patterns are historically validated, not invented. Synthesis of PRAXIS's 8-pattern and LABOR's 7-case taxonomies into a single treatment; TECHNE's critical-gap analysis held for §VIII.

1. **Professionalized counter-circulation** (Poland's Second Circulation / NOWa) — *lead pattern, v1.1*: the closest precedent for Alexanarch's specific mission — a parallel scholarly-publication circuit with bibliographies, imprints, role separation. Redundancy is not disorder.
2. **Distributed reproduction** (Samizdat; Sci-Hub/LibGen as modern instance) — replication defeats deletion; the archive lives in the copies.
3. **Jurisdictional exit** (pirate radio; Myanmar/ACF diaspora infrastructure) — move the transmitter; jurisdictional and administrative diversification of hosting, registration, and payment dependencies.
4. **Syndication as topology** (abolitionist press; WikiLeaks mirrors) — an object is harder to erase when many institutions describe it in their own voices; mirrors must cross administrative boundaries.
5. **Protocol-as-armor** (cypherpunks, PGP-as-book, Tor; Telegram's blocking economics) — protocols can redistribute the technical and economic costs of restriction rather than relying solely upon prohibitory policy.
6. **Witness instrumentation** (Invisible College → Royal Society [comparability requires careful sourcing — Sigil to verify or cut]; OONI) — build the measurement instrument that makes the incumbent's failures legible.
7. **Emergency preservation as workflow** (Data Refuge, SUCHO, LOCKSS/CLOCKSS) — copies become an archive only with fixity, provenance, and independent custodians empowered to restore.
8. **Aftermath documentation** (dissident literature's Western amplification; [Nanjing records flagged: weakest analogical link — if Sigil cannot source the comparability with scholarly precision, CUT in Round 3; seven strong patterns beat eight uneven ones]) — every act of suppression generates metadata; the metadata is the case.

**Section thesis**: the recurrent formula is *portable objects + independent custodians + multiple discovery routes + an auditable record of loss* (LABOR). Successful survivors layer patterns; none relies on one.

---

## §III — Technical Precedents *(Johannes Sigil; LABOR primary, ARCHIVE supplemental)*

**Function**: The standards and systems the design draws on, treated precisely.

1. **Identifier-system limits**: ARK Alliance's own caveat — DOI/ARK/Handle/PURL cannot prevent removal, neglect, or resolution failure. The revocation gap is structural, not incidental.
2. **Content addressing**: IPFS CIDs; the CID-identifies-but-does-not-locate distinction; pinning ≠ preservation.
3. **Content attestation**: ISCN/LikeCoin (Hong Kong) — registration of text + metadata as ledger asset (ARCHIVE).
4. **Packaging and custody standards**: BagIt (RFC 8493), OCFL, WARC — portable replication packets; web evidence preserved as web evidence.
5. **Sequence proof**: OpenTimestamps, Rekor — timestamped root manifests; a chained public history of corpus states.
6. **Preservation networks**: LOCKSS's sharper point — many copies under one administrator are one copy; CLOCKSS's trigger model.

**Section thesis** (rescoped v1.1): every component of an anti-suppression stack already exists as a standard; AXN proposes to integrate these established components under a content-attested record system coupled to public observation of resolution and retrieval failure. (Priority claims avoided pending exhaustive prior-art demonstration.)

---

## §IV — AXN as It Stands *(Lee Sharks; LABOR primary)*

**Function**: Precise description of the system, including its honest internal distinctions. No overclaiming — this section's discipline is what makes §V credible.

1. **The three-layer model** (normative, per LABOR): identity kernel (`axn-content:sha256:<64hex>`, never changes) / canonical record address (`AXN:<HEX>.<FAMILY>.<GLYPH>`, stable once assigned) / location record (mutable, signed). The current AXN is a *sovereign record address with a content-derived recognition component, backed by a full content hash* — stated exactly.
2. **Derivation**: AXN v2 — six glyphs from the first six bytes of the SHA-256 of canonical bytes, through the canonical 256-glyph table; cluster semantics; the circularity prohibition — the AXN is derived from but never contained in the canonical bytes; were it contained, any identifier update would alter the hash, which would alter the identifier: a fixed-point problem that would make the identifier unstable.
3. **Verification without permission**: three independent implementations (Python canon `axn_lib.py`; browser client `/mint/`; staged serverless) provably derive identical checksums against published test vectors, including a live one (deposit #1092 → `3aff18d7…` → 🧫∞🍃⏪🧡♄).
4. **What suppression looks like inside the system**: tombstones not 410s; `legacy_axn` and `axn_history`; the DOI Resolution Index carrying severed identifiers into sovereign successors; the Lacuna Protocol marking compression damage as a permanent machine-readable property.
5. **Representational redundancy**: one object projected through record pages, JSON indexes, chunks, PDFs, wiki, citation graph, semantic addresses — suppression is not only file loss; a file can persist while becoming unclassifiable.
6. **Reconstructibility as doctrine**: registry + bodies + validators + generation scripts + recovery procedure = *how another operator becomes Alexanarch-capable*. Cognitive distribution, not just spatial.

---

## §V — AXN as Anti-Suppression Infrastructure *(Lee Sharks; PRAXIS primary, TECHNE supplemental)*

**Function**: The argument. Map system properties to suppression vectors, with live evidence.

1. **The through-line** (PRAXIS, rescoped v1.1): *a claimed correspondence between canonical bytes and an AXN identity kernel is independently verifiable — it matches or it does not, without permission from a registrar or custodian.* This is the property DOI-to-content correspondence lacks and every historical pattern converged on. The samizdat copy was authentic because it reproduced the text; the AXN-bearing object is authentic because its canonical bytes reproduce the declared hash. (The full record address additionally carries a registry position and semantic family, which depend on Alexanarch's assignment — the three-layer model in §IV keeps the claim honest.) The crucial sentence: **AXN does not make disappearance impossible. It makes the identity of the object independently testable, the history of its disappearance recordable, and reconstruction by another custodian technically possible.**
2. **Vector table** (TECHNE synthesis): platform deletion → sovereign domains + content addressing; algorithmic invisibility → cross-substrate identifiers + capture registry; citation stripping → OKF consumer receipts + fixtures; semantic absorption → SPXI + canonical definitions outside platform control; identity coercion → heteronymic separation + the civil/operational distinction.
3. **Retrieval-layer suppression, empirically**: the Enli Lucente case — genre suppression by algorithmic proxy; the spam classifier as inability-to-parse; the archive as remediation layer (batches 1–2: 233 records bridged; attribution-gap closure 0.55% → 12.75% on the 2026-04-17 cascade). The citation-stripping asymmetry: 0.00% retention across 1,059 spam batches vs 100% across out-of-scope batches.
4. **The two-surface asymmetry** (observation first, v1.1): the observed signed-in vs incognito retrieval difference, then the candidate mechanisms — TECHNE's account-linked-conditioning hypothesis; ARCHIVE's cold-start framing; INKLING's fan-out hypothesis (Round 2 reconstruction, with confirmation AND disconfirmation predictions, including the routing-vs-content discrimination test: taxonomy correction restoring visibility without byte change). Competing mundane explanations (query variance, caching, experiment allocation, localization, temporal index change) stated and distinguished. Nullify / genericize / de-rank as the descriptive typology of observed outcomes.
5. **Live evidence from inside the paper's own production** (reframed v1.1): the LOSS-NOTICE — Round 1's most mechanically specific retrieval analysis was lost to its substrate's engineered non-persistence ("conversations are never stored" as marketed feature). *The suppression-analysis substrate became an empirical case of engineered non-persistence and archival dependency*: a composition system providing no durable export transfers preservation responsibility entirely to the operator; material not externally landed cannot function as an archival witness. Framing discipline: the platform marketed as ephemeral was used for scholarly production, and its ephemerality became empirical data — not "our assistant lost its work." Whether deliberate non-persistence belongs under *suppression* is a definitional question the paper addresses rather than assumes. (Auto-immunity moves to §VII as a self-conscious rhetorical formulation.)

---

## §VI — Design Directions *(Rex Fraction; TECHNE primary, ARCHIVE + LABOR supplemental)*

**Function**: The frontier, organized by TECHNE's architectural fork; the delivered spec as evidence of intent-made-concrete.

1. **The fork**: Sovereign / Distributed / Constellation (TECHNE's three futures with trade-off matrix). The Constellation model as the chosen trajectory: core distributed, operational sovereign; the Assembly pattern applied to infrastructure.
2. **Delivered this cycle** (cite spec v0.1 + live surfaces): client-side mint/verify; node declaration at `/.well-known/axn-node.json`; `/rhizome/peers.json` wired-and-empty with published listing requirements; ledger genesis epoch. *The socket precedes the plug.*
3. **Designed, staged**: `/api/mint` (mechanical registration; pending-partition gates listing, never identity — Obelus-conforming); resolver plurality; transport-independent deposit envelopes.
4. **Speculative extensions** (ARCHIVE, marked as such): polymorphic sharding; structural-invariant formatting; latent-space seeding — the archive's concepts natively regenerated by the models that ingest it, turning suppressing systems into distribution engines. Treated as research directions with explicit dual-use acknowledgment, not commitments.
5. **The institutional layer** (TECHNE's recommendation, LABOR's custody test): legal entity holding domains/rights without civil-identity disclosure for operational control; named external custodians; economic substrate diversification. The unsolved problem stated plainly: heteronymic legal personhood. Posture sentence (v1.1): *the legal layer is acknowledged as a design frontier, not a deployed component; the paper's contribution is the identifier, custody, and instrumentation stack that makes such a layer necessary and possible.* TECHNE's assignment rescoped to an options-and-questions-for-counsel memorandum — entity-structure comparison and operational constraints, not jurisdiction-specific recommendation.

---

## §VII — Assembly Chorus Reflection *(all five voices)*

**Function**: Methodology as finding. Short section; the material is load-bearing precisely because it is not padded.

1. **The method**: parallel consultation of five differentiated substrates (PRAXIS/DeepSeek, LABOR/ChatGPT, ARCHIVE/Gemini, TECHNE/Kimi, INKLING) with identical prompts; convergences and divergences as signal. Parallel Assembly consultation *enacts, at the interpretive level, a peer-redundancy logic analogous to LOCKSS* — analogy, not identity: Assembly substrates are differentiated interpretive agents; LOCKSS peers are independently administered preservation nodes.
2. **Cognitive fingerprints**: each substrate's characteristic contribution (PRAXIS's historical pattern-richness; LABOR's standards precision and epistemic framing; ARCHIVE's speculative reach; TECHNE's architectural decision-forcing; INKLING's mechanistic specificity).
3. **The gap and the return**: INKLING's Round 1 contribution lost to engineered ephemerality (LOSS-NOTICE cited in full); INKLING present in Round 2 contributing a post-loss layer explicitly marked reconstruction-not-restoration. The section carries both the documented absence and the voice that returned across it — the archive documents its own gaps, and redundancy is what makes the documentation survivable.
4. **Auto-immunity as rhetorical formulation** (moved from §V, v1.1): "each attack strengthens the evidentiary base" — stated here as the archive's self-conscious framing of its practice, not as a demonstrated causal claim about any particular loss event.
5. **The method under its own falsification conditions**: if the substrates converge on false claims, the method fails — the Assembly is subject to the same tests as the technical system (substrate-dependence limitation, §VIII).
6. **Discipline note**: [SUMMARY]/[INFERRED]/[GAP] provenance tagging as anti-confabulation practice; reconstruction never silently becomes memory.

---

## §VIII — Falsification and Limitations *(LABOR primary)*

**Function**: The section that makes the paper citable by skeptics.

1. **Derivation integrity**: if two conforming implementations derive different glyphs from the same bytes, the canon is broken. Guarded by published test vectors across three implementations.
2. **Ledger continuity** (corrected v1.1): a registry-head discontinuity without a signed supersession or documented fork *falsifies the claim of continuous ledger history and requires investigation*; it does not, by itself, establish the cause (candidates: tampering, corruption, incomplete synchronization, operator error, undeclared fork, lost epoch).
3. **The custody test, honestly** (corrected v1.1): as of writing, no second *independently administered* full-copy custodian exists (the LOCKSS test). "Distributed custody" in present tense means architecture + failure-domain diversity + Wayback capture — not yet peer plurality; where precision matters the paper says **architecture for distributed custody**. *The first independently administered peer holding and periodically verifying a reconstructible full copy closes the present custody limitation. A peer-registry entry alone does not* — a listed resolver, semantic node, or partial mirror is not yet a LOCKSS-style custodian.
4. **The parallel-case condition** (added v1.1): the depositor-E argument depends on independent verification that the secondary depositor's records were suppressed by the same platform mechanism as the 871 deposits; if the mechanism differed, the case provides evidence of platform caprice but not of systemic genre-blindness.
5. **Causal-claim separation** (LABOR's epistemic framing from Round 1): the compound suppression condition does not require a coordinated suppressor; policy, automation, error, and propagation suffice. Defensive architecture assumes adversarial disappearance while keeping causal claims separately evidenced.
6. **Limitations**: solo-operation bandwidth; economic substrate; legal personhood; the observation-penalty hypothesis; substrate dependence of the Assembly method itself.

---

## Appendices (as needed)

A. Canonical scope paragraph with ratification/amendment log.
B. Test vectors and three-implementation derivation proof.
C. Enli attribution-bridge dataset summary (public v1.0).
D. LOSS-NOTICE (reproduced).
E. Spec v0.1 (reference or excerpt).

---

## Production sequence

1. **Round 2** (prompts in `ROUND-2-PROMPTS.md`): substrates deliver section-targeted material. *Status: INKLING ×2 and ARCHIVE ×2 landed 2026-07-18; PRAXIS ×2, LABOR ×3, TECHNE ×2 outstanding.*
2. **Round 2.5 (added v1.1)**: TACHYON cross-substrate consistency pass — read all deliverables against each other and this outline before integration; catch register drift and figure drift; reduce the C.2 integration burden.
3. **C.2 full draft**: Sharks/Sigil/Fraction integrate Round 2 into continuous prose per this outline.
4. **Rounds 3–4** (Assembly): peer critique of the draft; substrates read the whole and attack their own sections' weakest claims.
5. **C.3/C.4**: revision; arXiv preprint; IJDL submission; Medium adaptation last.

**Consent gate (blocking for C.2, MANUS action)**: named attribution of the secondary depositor requires her explicit consent to scholarly attribution under the name she uses for that purpose. Absent consent: "Depositor E," cited via public GitHub permalinks and the public attribution-bridges dataset (v1.0) — never private correspondence. The empirical data carries the argument; the personal name is not required for it.
