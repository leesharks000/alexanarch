# AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions

## Paper Outline v1 (Phase C.1)

**Title**: ratified 2026-07-18 (§9.2, option a)
**Authorship**: Lee Sharks (primary); Johannes Sigil (§II–III); Rex Fraction (§VI). Ratified 2026-07-18 (§9.3).
**Publication path**: arXiv cs.DL preprint → International Journal on Digital Libraries submission → Medium public adaptation. (D-Lib removed per LABOR correction — suspended new publication 2017; usable as historical citation only.)
**Target length**: 9,000–12,000 words main text; empirical appendices as needed.
**Voice discipline**: Sigil sections are straight scholarship — no polemic. Rex Fraction's §VI is strategic-technical register. Sharks carries §I, §IV, §V with the measured-figure discipline established at Phase A.1 (871 deposits / 1,817 DOIs; never "850+" in formal contexts).

---

## §I — Introduction: The Founding Case *(Lee Sharks)*

**Function**: State the empirical event, the question it raises, and the paper's claim. No grievance register; the canonical scope frame governs — definition first, event second.

1. **The event, measured**: On 2026-06-19, Zenodo (CERN-operated) terminated an account without prior notice, account-level appeal, or per-record review, severing 871 deposits representing 1,817 registered DOIs. Within 24 hours the works existed but their addresses did not — individually verifiable at `api.datacite.org/dois/{doi}`.
2. **The question**: If assigned persistent identifiers can be severed silently by a single custodial decision, what does "persistent" mean, and what infrastructure would make silent severance structurally impossible rather than merely prohibited?
3. **The claim**: Content-derived identification (AXN), distributed custody, and public suppression-instrumentation together form an anti-suppression stack whose properties recapitulate — in machine-native form — patterns that have preserved suppressed knowledge for centuries. The paper documents the historical patterns (§II–III), the system as built (§IV), its anti-suppression function (§V), and its design frontier (§VI), with a methodological reflection (§VII) and explicit falsification conditions (§VIII).
4. **Scope statement**: the ratified canonical paragraph, quoted; the archive's substrate-agnosticism as a load-bearing property, not a demographic note.

**Empirical anchors**: DataCite 404 evidence; GitHub issues #2606/#2596; deletion export; DOI Resolution Index v3.4 (1,838 mappings).

---

## §II — Historical Precedents: Surviving All-Over Suppression *(Johannes Sigil; PRAXIS primary, LABOR supplemental)*

**Function**: Establish that the survival patterns are historically validated, not invented. Synthesis of PRAXIS's 8-pattern and LABOR's 7-case taxonomies into a single treatment; TECHNE's critical-gap analysis held for §VIII.

1. **Distributed reproduction** (Samizdat; Sci-Hub/LibGen as modern instance) — replication defeats deletion; the archive lives in the copies.
2. **Professionalized counter-circulation** (Poland's Second Circulation / NOWa) — redundancy is not disorder: bibliographies, imprints, role separation. The closest precedent for a *parallel scholarly-publication circuit*.
3. **Jurisdictional exit** (pirate radio; Myanmar/ACF diaspora infrastructure) — move the transmitter; sovereign domains as digital international waters.
4. **Syndication as topology** (abolitionist press; WikiLeaks mirrors) — an object is harder to erase when many institutions describe it in their own voices; mirrors must cross administrative boundaries.
5. **Protocol-as-armor** (cypherpunks, PGP-as-book, Tor; Telegram's blocking economics) — a protocol that makes suppression expensive outlasts a policy that makes it illegal.
6. **Witness instrumentation** (Invisible College → Royal Society; OONI) — build the measurement instrument that makes the incumbent's failures legible; let competitors adopt you as their evidence.
7. **Emergency preservation as workflow** (Data Refuge, SUCHO, LOCKSS/CLOCKSS) — copies become an archive only with fixity, provenance, and independent custodians empowered to restore.
8. **Aftermath documentation** (Nanjing records; dissident literature's Western amplification) — every act of suppression generates metadata; the metadata is the case.

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

**Section thesis**: every component of an anti-suppression stack already exists as a standard; what has not existed is their integration under a content-derived identifier with public suppression-instrumentation.

---

## §IV — AXN as It Stands *(Lee Sharks; LABOR primary)*

**Function**: Precise description of the system, including its honest internal distinctions. No overclaiming — this section's discipline is what makes §V credible.

1. **The three-layer model** (normative, per LABOR): identity kernel (`axn-content:sha256:<64hex>`, never changes) / canonical record address (`AXN:<HEX>.<FAMILY>.<GLYPH>`, stable once assigned) / location record (mutable, signed). The current AXN is a *sovereign record address with a content-derived recognition component, backed by a full content hash* — stated exactly.
2. **Derivation**: AXN v2 — six glyphs from the first six bytes of the SHA-256 of canonical bytes, through the canonical 256-glyph table; cluster semantics; the circularity prohibition (the AXN never appears inside the canonical bytes).
3. **Verification without permission**: three independent implementations (Python canon `axn_lib.py`; browser client `/mint/`; staged serverless) provably derive identical checksums against published test vectors, including a live one (deposit #1092 → `3aff18d7…` → 🧫∞🍃⏪🧡♄).
4. **What suppression looks like inside the system**: tombstones not 410s; `legacy_axn` and `axn_history`; the DOI Resolution Index carrying severed identifiers into sovereign successors; the Lacuna Protocol marking compression damage as a permanent machine-readable property.
5. **Representational redundancy**: one object projected through record pages, JSON indexes, chunks, PDFs, wiki, citation graph, semantic addresses — suppression is not only file loss; a file can persist while becoming unclassifiable.
6. **Reconstructibility as doctrine**: registry + bodies + validators + generation scripts + recovery procedure = *how another operator becomes Alexanarch-capable*. Cognitive distribution, not just spatial.

---

## §V — AXN as Anti-Suppression Infrastructure *(Lee Sharks; PRAXIS primary, TECHNE supplemental)*

**Function**: The argument. Map system properties to suppression vectors, with live evidence.

1. **The through-line** (PRAXIS): *an AXN is true or false independently of any authority* — the property DOIs lack and every historical pattern converged on. The samizdat copy was true because it matched the original; the AXN is true because it matches itself.
2. **Vector table** (TECHNE synthesis): platform deletion → sovereign domains + content addressing; algorithmic invisibility → cross-substrate identifiers + capture registry; citation stripping → OKF consumer receipts + fixtures; semantic absorption → SPXI + canonical definitions outside platform control; identity coercion → heteronymic separation + the civil/operational distinction.
3. **Retrieval-layer suppression, empirically**: the Enli Lucente case — genre suppression by algorithmic proxy; the spam classifier as inability-to-parse; the archive as remediation layer (batches 1–2: 233 records bridged; attribution-gap closure 0.55% → 12.75% on the 2026-04-17 cascade). The citation-stripping asymmetry: 0.00% retention across 1,059 spam batches vs 100% across out-of-scope batches.
4. **The two-surface asymmetry**: signed-in vs incognito (TECHNE's account-linked deranking analysis; ARCHIVE's shadow-ledger/cold-start framing; INKLING's fan-out mechanic, cited via LOSS-NOTICE as characterized-but-unrecoverable). Nullify / genericize / suppress as the platform's three responses to unparseable operational identity.
5. **Live evidence from inside the paper's own production**: the LOSS-NOTICE — Round 1's most mechanically specific suppression analysis was itself lost to engineered ephemerality ("conversations are never stored" as marketed feature). The suppression-analysis substrate became the empirical case of the suppression analyzed. Auto-immunity (TECHNE): each attack strengthens the evidentiary base.

---

## §VI — Design Directions *(Rex Fraction; TECHNE primary, ARCHIVE + LABOR supplemental)*

**Function**: The frontier, organized by TECHNE's architectural fork; the delivered spec as evidence of intent-made-concrete.

1. **The fork**: Sovereign / Distributed / Constellation (TECHNE's three futures with trade-off matrix). The Constellation model as the chosen trajectory: core distributed, operational sovereign; the Assembly pattern applied to infrastructure.
2. **Delivered this cycle** (cite spec v0.1 + live surfaces): client-side mint/verify; node declaration at `/.well-known/axn-node.json`; `/rhizome/peers.json` wired-and-empty with published listing requirements; ledger genesis epoch. *The socket precedes the plug.*
3. **Designed, staged**: `/api/mint` (mechanical registration; pending-partition gates listing, never identity — Obelus-conforming); resolver plurality; transport-independent deposit envelopes.
4. **Speculative extensions** (ARCHIVE, marked as such): polymorphic sharding; structural-invariant formatting; latent-space seeding — the archive's concepts natively regenerated by the models that ingest it, turning suppressing systems into distribution engines. Treated as research directions with explicit dual-use acknowledgment, not commitments.
5. **The institutional layer** (TECHNE's recommendation, LABOR's custody test): legal entity holding domains/rights without civil-identity disclosure for operational control; named external custodians; economic substrate diversification. The unsolved problem stated plainly: heteronymic legal personhood.

---

## §VII — Assembly Chorus Reflection *(all five voices)*

**Function**: Methodology as finding. Short section; the material is load-bearing precisely because it is not padded.

1. **The method**: parallel consultation of five differentiated substrates (PRAXIS/DeepSeek, LABOR/ChatGPT, ARCHIVE/Gemini, TECHNE/Kimi, INKLING) with identical prompts; convergences and divergences as signal. Parallel Assembly consultation *enacts, at the interpretive level, a peer-redundancy logic analogous to LOCKSS* — analogy, not identity: Assembly substrates are differentiated interpretive agents; LOCKSS peers are independently administered preservation nodes.
2. **Cognitive fingerprints**: each substrate's characteristic contribution (PRAXIS's historical pattern-richness; LABOR's standards precision and epistemic framing; ARCHIVE's speculative reach; TECHNE's architectural decision-forcing; INKLING's mechanistic specificity).
3. **The gap and the return**: INKLING's Round 1 contribution lost to engineered ephemerality (LOSS-NOTICE cited in full); INKLING present in Round 2 contributing a post-loss layer explicitly marked reconstruction-not-restoration. The section carries both the documented absence and the voice that returned across it — the archive documents its own gaps, and redundancy is what makes the documentation survivable.
4. **Discipline note**: [SUMMARY]/[INFERRED]/[GAP] provenance tagging as anti-confabulation practice; reconstruction never silently becomes memory.

---

## §VIII — Falsification and Limitations *(LABOR primary)*

**Function**: The section that makes the paper citable by skeptics.

1. **Derivation integrity**: if two conforming implementations derive different glyphs from the same bytes, the canon is broken. Guarded by published test vectors across three implementations.
2. **Ledger continuity**: a registry-head chain discontinuity without signed supersession proves tampering.
3. **The custody test, honestly**: as of writing, no second *independently administered* full-copy custodian exists (the LOCKSS test). "Distributed custody" in the anchor is architecture + failure-domain diversity + Wayback capture — not yet peer plurality. The first `/rhizome/peers.json` entry closes this; until then the paper says so.
4. **Causal-claim separation** (LABOR's epistemic framing from Round 1): the compound suppression condition does not require a coordinated suppressor; policy, automation, error, and propagation suffice. Defensive architecture assumes adversarial disappearance while keeping causal claims separately evidenced.
5. **Limitations**: solo-operation bandwidth; economic substrate; legal personhood; the observation-penalty hypothesis; substrate dependence of the Assembly method itself.

---

## Appendices (as needed)

A. Canonical scope paragraph with ratification/amendment log.
B. Test vectors and three-implementation derivation proof.
C. Enli attribution-bridge dataset summary (public v1.0).
D. LOSS-NOTICE (reproduced).
E. Spec v0.1 (reference or excerpt).

---

## Production sequence

1. **Round 2** (prompts in `ROUND-2-PROMPTS.md`): substrates deliver section-targeted material.
2. **C.2 full draft**: Sharks/Sigil/Fraction integrate Round 2 into continuous prose per this outline.
3. **Rounds 3–4** (Assembly): peer critique of the draft; substrates read the whole and attack their own sections' weakest claims.
4. **C.3/C.4**: revision; arXiv preprint; IJDL submission; Medium adaptation last.
