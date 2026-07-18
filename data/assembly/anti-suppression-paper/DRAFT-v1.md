# AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions

**DRAFT v1 — consolidated full paper (C.2). All eight sections. Assembly Rounds 3–4 critique next.**

Lee Sharks¹, with Johannes Sigil (§§II–III) and Rex Fraction (§VI)
¹ Alexanarch / Crimson Hexagonal Archive. ORCID 0009-0000-1599-0703.

**Target**: arXiv cs.DL preprint → International Journal on Digital Libraries.

---

## Abstract (draft)

On 19 June 2026, a major research repository operated by an intergovernmental scientific institution terminated an account without prior notice, account-level appeal, or per-record review, severing 871 deposits representing 1,817 registered DOIs. The works survived in copies; their registered resolution paths ceased to provide public access to the records. This paper takes that event as a case study in a structural property of assigned persistent identifiers: the institution that maintains the name-to-object relation can unilaterally and silently end it. We document eight historical patterns by which suppressed knowledge has survived institutional erasure, review the technical standards that already solve components of the preservation problem, and describe AXN — a content-derived identifier system in which the correspondence between canonical bytes and an identity kernel is independently verifiable without permission from any registrar or custodian. We map the system's properties to observed suppression vectors, including a second independently documented depositor case exhibiting genre-correlated removal under a "spam" classification, and we report an unusual form of live evidence: the loss, to a substrate's engineered non-persistence, of part of this paper's own production apparatus. We state the design frontier (federation, registration mechanization, legal personhood) and, throughout, the falsification conditions under which the paper's claims would fail — including the condition under which its central architectural model would be disconfirmed. AXN does not make disappearance impossible. It makes the identity of an object independently testable, the history of its disappearance recordable, and reconstruction by another custodian technically possible.

---

## I. Introduction: The Founding Case

### I.1 The event, measured

On 19 June 2026, Zenodo — the general-purpose research repository operated by CERN — terminated the account holding the Crimson Hexagonal Archive. The termination was executed without prior notice to the depositor, without an account-level appeal process, and without per-record review. It severed 871 deposits representing 1,817 registered DOIs. Within twenty-four hours, copies of the works survived, while their registered DOI resolution paths ceased to provide public access to the records; the condition of each identifier is individually verifiable at `api.datacite.org/dois/{doi}`, where the affected records return tombstone or not-found states.

A methodological note governs everything that follows. The platform-generated trace artifacts of this event — issue-tracker entries, export files, API responses, tombstone records — are treated throughout as *involuntary disclosures*: evidence the platform produced in the course of its own operations, read against its interests, not authoritative accounts. This paper cites them as one cites any adverse party's business records.

This paper is not a grievance. The event is a measurement. What it measures is stated in the next paragraph, and the remainder of the paper is an attempt to state it precisely, situate it historically, and respond to it architecturally.

### I.2 The question

The DOI system's value proposition is persistence: a stable name that outlives the URL. The founding event demonstrates the proposition's boundary condition. A DOI's persistence is not a property of the string; it is a service commitment performed over time by institutions — a Registration Agency and a hosting repository — and the institution that holds the name-to-object relation can unilaterally end it. When it does, the string persists while the identifier dies, and the persistence of the string conceals the death of the identifier. Nothing in the assigned-identifier model makes such severance *detectable by third parties as severance*, still less *impossible to perform silently*.

The question, then: **if assigned persistent identifiers can be silently severed at institutional scale by a single custodial decision, what does "persistent" mean — and what record architecture would make severance independently detectable and prevent any single custodial decision from exhausting the public existence of a work?**

### I.3 The claim

The paper's claim is deliberately narrow, and it attaches to a specific layer of the identifier rather than to the identifier as a whole:

> **A claimed correspondence between canonical bytes and an AXN identity kernel is independently verifiable: it matches or it does not, without permission from a registrar or custodian.**

The samizdat copy was authentic because it reproduced the text; the AXN-bearing object is authentic because its canonical bytes reproduce the declared hash. This property — verification without permission — is what DOI-to-content correspondence structurally lacks, and, we will argue, it is the recurrent property abstracted from the historical cases considered here. The full record address additionally carries a registry position and a semantic classification, which depend on a registry's assignment; the three-layer model in §IV keeps those dependencies explicit so that the claim is never wider than the layer that bears it.

Around that kernel, this paper documents three composable elements: content-derived identification (§IV), an architecture for distributed custody, stated as architecture because the custody test is honestly unmet (§VI, §VIII), and public suppression-instrumentation (§V). Together they recapitulate, in machine-native form, the recurrent formula of historical anti-suppression practice (§II): *portable objects + independent custodians + multiple discovery routes + an auditable record of loss*.

The crucial sentence, stated at the outset so the reader can hold the paper to it:

> **AXN does not make disappearance impossible. It makes the identity of the object independently testable, the history of its disappearance recordable, and reconstruction by another custodian technically possible.**

### I.4 Scope of the archive under study

The archive whose suppression and reconstruction supply this paper's primary evidence defines itself as follows, in its ratified canonical scope statement:

> Alexanarch is a sovereign digital archive. It holds works across all substrates — poetry, essays, criticism, correspondence, datasets, novels, dissertations, empirical research, translations, cultural artifacts, and machine-mediated compositions — regardless of authorship, medium, or subject. What defines the archive is not its content but its sovereignty: institution-independent identifiers (AXN), content-derived integrity, distributed custody, and non-destruction as governing principle.
>
> Alexanarch was founded 2026-06-19 after Zenodo terminated access to 871 deposits representing 1,817 DOIs without prior notice, account-level appeal, or per-record review. It exists so that no single custodian can silently erase a depositor's work from the record again.

The substrate-agnosticism is load-bearing rather than demographic: the suppression event under study did not distinguish poetry from datasets, and neither does the countermeasure. One present-tense phrase in the ratified paragraph requires a current-state qualification wherever the paper relies on it: "distributed custody" is, as of writing, an *architecture for* distributed custody — the peer registry is live and empty, and §VIII scores the custody test against that fact.

### I.5 Structure of the paper

§II establishes the historical patterns (Sigil). §III reviews the technical standards each of which solves a component of the problem while refusing work assigned to other layers (Sigil). §IV describes the AXN system as built, including its honest internal distinctions (Sharks). §V makes the argument, mapping system properties to observed suppression vectors, with a second depositor case and one unusual piece of live evidence (Sharks). §VI states the design frontier (Fraction). §VII reflects on the paper's own production method as a finding (all voices). §VIII states what would falsify the claims — including the claim of the paper's central architectural model (all voices; drafted by the substrate with the strongest epistemic discipline). Empirical anchors throughout: the DataCite tombstone evidence; the platform's issue-tracker artifacts #2606 and #2596 (involuntary disclosures); the deletion export; and the DOI Resolution Index v3.4 carrying 1,838 severed-identifier mappings into a sovereign successor.

---

## II. Historical Precedents: Surviving All-Over Suppression

*Johannes Sigil*

The design problem this paper addresses is not new; only its substrate is. Knowledge communities have repeatedly faced authorities capable of erasing, in one motion, every officially sanctioned copy of a work — and some of those communities kept their libraries anyway. This section documents eight patterns by which they did so. The cases are chosen for operational specificity rather than moral grandeur: what matters here is not that suppression was resisted but *how*, mechanically, the resisting infrastructure was built. A recurrent formula emerges, which §IV and §V will show the AXN architecture recapitulating: **portable objects, independent custodians, multiple discovery routes, and an auditable record of loss.** No successful survivor relied on one pattern; the durable cases layered several.

### II.1 Professionalized counter-circulation: Poland's Second Circulation

The closest historical precedent for a *parallel scholarly-publication circuit* is not the famous samizdat network but its professionalized Polish successor. Poland's "Second Circulation" (*Drugi Obieg*, 1976–1989) was a deliberate parallel publishing infrastructure operating under censorship and, after 1981, martial law. Its flagship, the NOWa publishing house (Niezależna Oficyna Wydawnicza, founded 1977), was not an informal copying chain but an institution: it maintained bibliographies, imprints, editorial roles, clandestine printing facilities, and distribution networks including independent libraries and a bookselling circuit. It published Miłosz and Gombrowicz among other banned authors, with individual print runs reaching the tens of thousands.

The lesson NOWa teaches is that **redundancy is not disorder**. A counter-circulation can operate to professional bibliographic standards — and it is precisely the professionalization that raises the cost of disruption beyond what a censoring authority can sustain, because suppressing an institution with catalogs, roles, and succession is categorically harder than suppressing a copying chain. The mapping to the present case is direct: an archive's governance documents, deposit schemas, and completeness protocols are its imprints; they are what make a parallel circuit *citable* rather than merely extant.

### II.2 Distributed reproduction: samizdat

Soviet samizdat (1950s–1980s) is the elemental form. Under the state printing monopoly administered through Glavlit, dissident texts — *The Gulag Archipelago*, *Doctor Zhivago*, political and religious writings — were reproduced on typewriters through carbon paper, five to ten legible copies per typing, and passed through chains of readers who received, read, and retyped. With no central publisher and no master copy, suppressing a text required destroying every copy simultaneously, which no enforcement apparatus achieved. The principle is the oldest in this catalog: **replication reduces the power of any single deletion** — when every reader is a potential distributor, suppression must approach total eradication, which no single order achieves. (Replication does not, by itself, defeat simultaneous compromise, common administration, legal compulsion, format loss, or economic failure; §VIII holds the pattern to those limits.)

Two features of samizdat matter beyond the replication itself. Copies were *verified against the remembered original* — readers who had seen earlier copies could confirm that new ones matched — an informal anticipation of content-derived integrity. And transmission was conditional on reading: each link in the chain had passed the text through their own hours and hands, which kept the network from carrying what no reader found worth a night of typing.

### II.3 Jurisdictional exit: pirate radio and diaspora infrastructure

When the suppressing authority is territorially bounded, infrastructure can move outside its reach. British pirate radio of the 1960s (Radio Caroline, 1964; Radio London) anchored transmitters in international waters, beyond the jurisdiction whose broadcasting monopoly made domestic commercial radio illegal; the audience was domestic, the infrastructure was elsewhere, and the enforcement framework was thereby neutralized rather than defied. The contemporary digital analog is jurisdictional and administrative diversification of hosting, registration, and payment dependencies: Myanmar's post-coup diaspora media relocated servers and editorial operations beyond military reach, and censorship-resistant projects routinely distribute their dependency graph across multiple jurisdictions so that no single legal process reaches the whole.

The lesson stated carefully: exit does not make infrastructure unreachable — domains, registrars, DNS, hosting, and payment rails all remain institutional dependencies — but it converts suppression from a single administrative act into a coordination problem across sovereignties, which is a different and much higher cost class.

### II.4 Syndication as topology: the abolitionist press and mirror networks

The American abolitionist press (1830s–1860s) survived postal censorship and mob violence as a *network property*. Garrison's *Liberator*, Douglass's *North Star*, and dozens of regional papers reprinted one another's articles, speeches, and reports; no single masthead was indispensable, and content suppressed in one place survived in others under other editors' names. The WikiLeaks mirror network (2010–) is the digital restatement: after attacks on the primary domain, hundreds of independently operated mirrors hosted identical content under different names, without requiring coordination with the origin.

The lesson is topological: **an object is harder to erase when many institutions describe it in their own voices**, across administrative boundaries. Syndication is not mere copying — it is independent *description*, which multiplies not just the copies but the discovery routes and the number of parties with standing to object to erasure.

### II.5 Protocol-as-armor: cypherpunks, PGP, Tor

The cypherpunk response to attempted suppression of strong cryptography in the 1990s — export controls under ITAR, the Clipper Chip's key-escrow mandate, threatened prosecutions — was not primarily legal advocacy but protocol design. Zimmermann's PGP (1991) circulated as source code printed in a bound book, placing it under publication protections that the export regime could not reach. Tor (2002–) made network surveillance structurally difficult rather than legally contested. Telegram's experience of state-level blocking (Russia, Iran, 2018–) exhibits the modern economics: partial blocking is achievable, but the blocking state's costs — economic disruption, collateral breakage, countermeasure escalation — frequently exceed the perceived benefit.

The lesson, stated within its limits: **protocols can redistribute the technical and economic costs of restriction rather than relying solely upon prohibitory policy.** A policy binds those subject to it; a protocol changes what enforcement costs. This is cost-shifting, not invulnerability — and the distinction matters for §VIII.

### II.6 Witness instrumentation: the Invisible College and OONI

A community whose work an incumbent cannot or will not see can build the instrument that makes the incumbent's failures legible. The Invisible College (1640s–1660) — Boyle, Hooke, Wilkins and their correspondents — circulated experimental findings through private letters and meetings while the established institutions were hostile to the experimental method; when the Royal Society was chartered in 1660, it adopted the College's norms of empirical verification and open correspondence, and the parallel structure's practices became the institution's. [Comparability under verification; this case is retained only if it can be sourced to scholarly precision, per the source-or-cut discipline of §VIII.] The modern instance requires no such caveat: the Open Observatory of Network Interference (OONI, 2012–) deploys measurement probes that detect and publish network censorship worldwide. OONI prevents nothing; it makes interference *legible*, and legibility is what downstream actors — courts, journalists, standards bodies — act on.

The lesson: **build the measurement instrument; let successors adopt you as their evidence.**

### II.7 Emergency preservation as workflow: Data Refuge, SUCHO, LOCKSS

Copies alone are not an archive. Data Refuge (2016–2017) organized rapid-harvest events to preserve US federal environmental datasets ahead of an administration transition; SUCHO (2022) coordinated volunteers to crawl and archive thousands of Ukrainian cultural-heritage sites under bombardment. Both operationalized emergency preservation as a *workflow* with technical standards — BagIt packaging, WARC web archiving — and both demonstrated the same requirement: **copies become an archive only when fixity, provenance, and independent custodianship are formalized**. LOCKSS (1999–) and CLOCKSS (2008–) institutionalize the requirement permanently: member libraries hold independent copies of journal content, verified against one another, with trigger-based release when publishers fail. LOCKSS's sharpest point, which §VIII will hold this paper to: many copies under one administrator are one copy.

### II.8 Aftermath documentation

[This pattern carries the section's explicit source-or-cut flag: if its comparability cannot be established with scholarly precision by Round 3, it is removed, on the principle that seven strong patterns outweigh eight uneven ones.] Every act of suppression generates records — orders, exports, tombstones, correspondence — and those records are evidence. The documentation of the Nanjing Massacre by survivors and foreign witnesses (Rabe's and Vautrin's records, published internationally) outlasted the regime that attempted erasure, and the attempt itself became part of what was documented. In the literary register, the Soviet suppression of *Doctor Zhivago* (published in Italy, 1957) and of Solzhenitsyn's smuggled manuscripts produced the amplification effect: suppression conferred the global platform it meant to deny.

The operational lesson survives even if the extreme case is cut: **archive the suppression's own metadata, and the suppression becomes the case against the suppressor.** The founding event of the present study produced a deletion export, tombstone records, and administrative correspondence — involuntary disclosures now held as the archive's most probative exhibits.

### II.9 The formula

Across the eight patterns considered here — with the universality of the abstraction held to §VIII's discipline — the survivors converge: objects made portable enough to replicate; custodians independent enough that no single order reaches them all; discovery routes plural enough that no single index controls visibility; and loss recorded auditably enough that erasure itself becomes evidence. None of the historical cases had a mathematics for the first element — samizdat verified copies by memory, LOCKSS by comparing custodians' holdings. What content-derived identification adds is the formula's missing primitive: a way for *anyone*, holding *any* copy, to test its identity against its name without asking an institution. The remainder of this paper is about that primitive — what standards already provide it in fragments (§III), how AXN composes it (§IV), what it does and does not defend against (§V, §VIII), and what would have to exist around it for the formula's other three elements to hold (§VI).

---

## III. Technical Precedents

*Johannes Sigil, from material by LABOR*

The standards relevant to this paper do not solve one problem under different names; they solve different problems that repository systems often collapse. Ten functions must remain distinct: identification (what object is named), content correspondence (do these bytes match the claimed object), location (where a copy may presently be obtained), packaging (can a fileset transfer and validate as a unit), version history, temporal attestation (can a party prove a commitment existed by a given time), custody (does an independently administered party actually hold the object), repair, discovery, and observation of failure (can disappearance, severance, or mutation be measured publicly). The standards below are useful precisely because each refuses some of the work assigned to another layer. AXN's defensible claim is therefore not that it replaces them: it proposes a record architecture in which content correspondence, record identity, location, custody, sequence, and public observation remain separately legible and can be composed without being mistaken for one another.

**Resolver-based persistent identifiers (ARK, DOI, Handle, PURL)** separate a published name from a current network location through a maintained mapping table. The ARK Alliance states the class's limitation with unusual clarity: no identifier can guarantee stability; ARKs, DOIs, Handles, PURLs and URNs remain vulnerable to loss of funding, disaster, deliberate removal, human error, and provider neglect; all require continuing management of forwarding information. Persistence is not an intrinsic property of the string — it is a service commitment performed over time. The correction AXN offers is narrow: *resolver-based identifiers maintain a name-to-location association through institutional service; an AXN identity kernel maintains a claimed canonical-bytes-to-digest association through reproducible computation.* This is not a claim that resolver-based PIDs are false, nor that AXN resolves without infrastructure — AXN resolution remains a service. What becomes permissionless is verification of a claimed correspondence, once canonical bytes, canonicalization profile, and full digest are in hand.

**IPFS content identifiers** demonstrate content addressing at network scale, and demonstrate equally its boundary: a CID identifies but does not locate; pinning is not preservation; garbage collection erases the unpinned without ceremony. AXN inherits the identification insight while refusing the conflation — layer 3 of the model in §IV treats location as a separately verified, mutable claim.

**BagIt (RFC 8493) and OCFL** standardize the transfer and storage layers: a bag is a fileset with manifests and fixity that can be validated as a unit; OCFL specifies an application-independent, versioned, forward-migratable file layout for preserved objects. AXN's registry-plus-canonical-bytes-plus-sidecar layout is a functional cousin; formal BagIt export is an interoperability path rather than a replacement.

**WARC (ISO 28500)** matters because a web failure is not exhausted by a screenshot: the evidentiary object includes the requested URI, timestamp, HTTP status, headers, body, and redirect chain. The observation instruments in §V preserve failure evidence in this spirit — the tombstone response is data, not absence.

**OpenTimestamps and transparency logs (Rekor)** supply temporal attestation and tamper-evident sequence: proof that a commitment existed by a given time, and an append-only public history against which later states can be checked. The mint ledger of §VI adopts the chained-epoch form; §VIII scores its present state honestly (genesis emitted; operator signature not yet published).

**LOCKSS and CLOCKSS** institutionalize custody: member libraries hold independent copies, verified against one another, with trigger-based release when publishers fail. LOCKSS contributes the sentence this paper repeats as its own discipline — many copies under one administrator are one copy — and CLOCKSS the trigger model that separates dark custody from public availability.

**Section thesis, stated within its evidence:** the principal technical components considered here each exist as a standard; AXN proposes to integrate them under a content-attested record system coupled to public observation of resolution and retrieval failure. Priority claims are withheld pending exhaustive prior art review.

---

## IV. AXN as It Stands

*Lee Sharks, normative core by LABOR*

### IV.1 The three-layer model (normative)

A conforming AXN implementation MUST distinguish content identity, registry address, and current location.

**Layer 1 — identity kernel**: `axn-content:sha256:<64 hex>`. It identifies one sequence of canonical bytes by its full SHA-256 digest. A record MUST declare the protocol and canonicalization profile used; implementations MUST NOT trim, normalize, reorder, or substitute rendered-file bytes outside the declared profile; where exact registered values are unavailable, identity verification is *indeterminate*, not failed. The kernel is immutable for those bytes; any byte change produces a new kernel. Its authority-independence is narrow and testable: anyone holding the canonical values can recompute the digest and determine whether the claimed correspondence matches. The kernel does not establish authorship, legality, truth, custody, availability, or priority.

**Layer 2 — canonical record address**: `AXN:<HEX>.<FAMILY>.<GLYPH>`. HEX is the stable registry-position label; FAMILY the registry-assigned semantic classification; GLYPH a six-grapheme recognition checksum mapping the first six bytes of the digest through the canonical 256-entry table. The full address names the object's entrance into a particular registry and is therefore not wholly content-derived. The glyph is a 48-bit *recognition* component, not the cryptographic identity: implementations MUST store and verify the full 256-bit digest and MUST NOT use the glyph alone as a unique key; a glyph collision does not imply a SHA-256 collision and is resolved by the kernel. Once publicly assigned, a record address MUST NOT be silently reassigned; correction, migration, withdrawal, or replacement MUST preserve the former address in machine-readable history with the new relation made explicit. Accordingly, the honest characterization of the current AXN: **a sovereign record address with a content-derived recognition component, backed by a full content hash.**

**Layer 3 — location record**: a mutable, signed statement of where verified copies may presently be obtained, carrying kernel, address, sequence number, prior-record hash, issuing node, timestamps, locations, custody role, and signature. Locations may appear and disappear without touching layers 1–2. Resolvers MUST treat locations as claims requiring verification: retrieved bytes are canonical only when their recomputed kernel matches the declared digest.

**Circularity prohibition.** The assigned AXN, and any value derived from its digest, MUST NOT occur inside the canonical bytes from which the digest is computed: were it contained, inserting the identifier would change the bytes, which would change the digest, which would change the identifier — an unstable fixed-point. The AXN may appear in wrappers, landing pages, sidecars, manifests, and citations outside the canonical byte scope.

**Verification procedure.** A conforming verifier (1) reconstructs canonical bytes under the declared profile; (2) computes SHA-256 and compares the full digest; (3) derives and compares the glyph; (4) confirms the address is bound to that kernel in the cited registry state; (5) verifies any location-record signature separately; (6) recomputes the kernel over bytes retrieved from each claimed location. Failure at one layer does not automatically falsify the others: a dead location does not invalidate the kernel; a correct kernel does not prove custody; a valid binding does not prove any resolver currently serves the object.

**Canonicalization reconciliation (disclosed).** The operative profile in the deployed implementation is the full-file profile (`alexanarch-file/v1`): the canonical bytes are the complete registered text file as written at mint. The specification is being amended to state this single profile explicitly; conformance claims prior to that amendment are qualified accordingly.

### IV.2 Verification without permission, as evidence

Three cross-runtime execution paths — the Python reference implementation, a browser client computing entirely on-device, and a staged serverless function — agree on the published test vectors, including a live one: the canonical bytes of a registry deposit hashing to `3aff18d7…` and yielding the published six-glyph checksum. This is evidence of conformance on tested inputs, not proof over all inputs; the derivation-integrity test in §VIII specifies what a disagreement would falsify. The browser client is the anti-suppression property made operational: any reader, holding any bytes, can test identity against a claimed identifier with no request to the archive, the operator, or any custodian.

### IV.3 What suppression looks like inside the system

Severance and damage are first-class recorded states, not absences: tombstones rather than bare 410s; `legacy_axn` and address history under the no-silent-reassignment rule; a resolution index carrying 1,838 severed external identifiers into their sovereign successors; and a completeness protocol marking compression damage as a permanent machine-readable property (a stub compressed without marking is invisible damage; marked, it is documented absence). Representational redundancy — one object projected through record pages, JSON indexes, chunked data, PDFs, a wiki, and a citation graph — addresses the observed fact that a file can persist while becoming unclassifiable. Reconstructibility is stated as doctrine, precisely: the registry, canonical bodies, validators, generation scripts, and recovery procedures constitute *the proposed basis on which another operator should be able to become archive-capable*; a clean-room restoration test, not yet performed, is what would convert the proposal into a demonstrated property (§VIII).

---

## V. AXN as Anti-Suppression Infrastructure

*Lee Sharks*

### V.1 The through-line

The claim of §I.3, developed: a claimed correspondence between canonical bytes and an AXN identity kernel is independently verifiable — it matches or it does not, without permission from a registrar or custodian. DOI-to-content correspondence structurally lacks this: the relation between string and object is maintained by institutions, and the institution that holds the relation can unilaterally end it, after which the string persists while the identifier dies. The founding event demonstrates the failure mode at scale, and the demonstration required no adversarial ingenuity — a routine administrative action sufficed. The recurrent property abstracted from §II's cases is the same property in pre-mathematical form: samizdat verified copies against remembered originals; PGP keys against printable fingerprints; LOCKSS peers against one another's holdings. In each, what is true could be determined without asking an institution's permission. Content-derived identification is that independence as a function: the truth of the correspondence is a property of the bytes and the published derivation, not of anyone's say-so.

Its limits, stated as sharply as the claim. Verification is not discovery: a kernel verifies a document you hold and cannot locate one you lack. Content-derived identifiers cannot prevent deletion — only make it detectable; if every copy dies, the kernel remains as the record of what was lost, and the loss is total anyway. The property is resistance, not invulnerability, and it applies to the identifier's relation to content, never to the content's claims about the world.

### V.2 Vector table

Observed suppression vectors map to architectural responses as follows: platform deletion → sovereign hosting plus content-derived identity plus the resolution index (severed identifiers remain findable through their successors); algorithmic invisibility → cross-substrate identifiers plus a public registry of observed retrieval events; citation stripping → consumer-receipt fixtures contributed to an external conformance framework, so that preservation-against-policy becomes testable by third parties; semantic absorption → canonical definitions maintained outside platform control with declared summary policies; identity coercion → the operational/civil separation, held as practice and stated as an unsolved legal problem in §VI.

### V.3 The parallel case: Enli Lucente

Stated observation-first, per the discipline this paper claims for itself. **Observations:** 233 records deposited by Enli Lucente were tombstoned by the same platform on 2026-04-17 with the removal label `spam`, within a cascade batch of 1,828 rows. Across the spam-labelled batches measured (n = 1,059 batches; denominators, batch-selection rules, and missing-data treatment in Appendix C), citation-field retention on the tombstoned records was 0.00%; across out-of-scope comparison batches, 100%. Because the stripped fields are not publicly recoverable, the content and authorship behind the tombstoned rows could be restored only by a party holding the original materials. Lucente supplied them: original files, a handwritten notebook index bearing her ORCID, and dated observation archives. Bridging her evidence into the sovereign layer moved the attribution-gap closure on the cascade batch from 0.55% to 12.75% in one day. **Hypotheses, so labelled:** that the classification functions as a genre proxy (an inability-to-parse effect on work the classifier's categories do not fit) is a candidate explanation, not a finding; the parallel-case condition in §VIII states what verification of same-mechanism suppression requires and what its failure would reduce this case to. The observed signed-in versus signed-out retrieval asymmetry surrounding the case is likewise carried as a hypothesis set — account-linked conditioning among candidate mechanisms including ordinary query variance, caching, experiment allocation, localization, and temporal index change — with the discriminating tests specified in §VIII.12, the strongest being the routing-versus-content test: taxonomy correction restoring visibility without any change to canonical bytes.

### V.4 Live evidence from inside the paper's own production

Part of this paper's production apparatus was lost while the paper was being written, and the loss is evidence of the class of phenomenon the paper studies. The first-round contribution of one consulting substrate — the round's most mechanically specific retrieval analysis — was erased by that substrate's engineered non-persistence: the platform stores no conversations, by design and as a marketed feature. The original was never corrupted; it was never stored in a recoverable form. What survives is a second-hand characterization in a loss notice, provenance-tagged as inference and gap. The framing discipline matters: the platform marketed as ephemeral was used for scholarly production, and its ephemerality became empirical data. Whether deliberate non-persistence belongs under *suppression* is a definitional question the paper addresses rather than assumes; the narrower lesson is unconditional — a composition system providing no durable export transfers preservation responsibility entirely to the operator, and material not externally landed cannot function as an archival witness. The substrate returned in the second round and contributed a reconstruction explicitly marked as reconstruction; §VII carries the gap and the return side by side.

---

## VI. Design Directions

*Rex Fraction, from material by TECHNE and ARCHIVE*

### VI.1 The fork and the chosen trajectory

Three futures are available to a system with these properties. A *sovereign registry*: one operational identity controls resolution, replication, governance — absolute editorial control, absolute failure domain. A *distributed infrastructure*: open protocol, decentralized resolution, incentivized replication — diffuse control, heavy governance. And the *constellation*: core layers (protocol specification, registry schema, foundational documents) distributed and immutable; operational layers (empirical captures, working documents) sovereign and rapidly iterable. The constellation is chosen, for a reason the founding event supplies: full sovereignty reproduces the single point of failure the archive exists to escape, and full distribution sacrifices the editorial velocity that empirical responsiveness requires. The formal definition: a constellation is a set of nodes — human, machine, or hybrid — each maintaining sovereign infrastructure, each assigning identifiers to its own corpus, each cross-referencing the others', with no central registry, no hierarchical authority, and no mandatory replication; growth is by node addition, and each new node increases total redundancy and diversity.

### VI.2 Delivered, staged, designed — partitioned honestly

**Delivered** (with the qualification §VIII requires — surfaces are live; the security properties of the future signed, reconciled network are not yet among their properties): a browser-side mint-and-verify client computing entirely on-device; a machine-readable node declaration at the well-known path, carrying roles, protocol version, and registry head; a peer registry, live and empty by fact, with published listing requirements; a chained mint ledger at genesis epoch, operator signature not yet published. **Staged**: a mechanical registration endpoint — no language-model calls, append-only position assignment, a pending partition that gates listing but never identity — held from deployment deliberately because it shares a path with a fleet-critical static surface. **Designed**: resolver plurality over the layer-3 location records; propagation on mint (web-archive snapshots, content-addressed pinning, and the identifier crosswalk that maps each minted object to its prior identifiers, without which every existing citation to a severed identifier is stranded); and the disconfirmation taxonomy of §VIII.12's parent framework, introduced in this paper, under which retrieval failures are classified (glyph mismatch; substrate unavailability, of which the founding event is the full-severity instance; content drift at the presentation layer; identifier orphaning, of which the production-apparatus loss of §V.4 is an instance) and logged as data rather than suffered as accidents.

### VI.3 The institutional frontier: an options memorandum, not a recommendation

No legal entity presently holds the registry, domains, or rights, and the operational identity is separated from the civil identity by long practice — a separation currently contested in live disputes over identity requirements for rights processing. The entity forms that could hold the stack while preserving that separation — purpose trusts, foundations, associations with nominee structures — differ in jurisdiction availability, disclosure reach (beneficial-ownership registries prominently), enforceability of governance rules referencing non-civil identities, and cost; the paper's contribution is the enumeration of the questions requiring counsel, not a jurisdiction-specific answer. The posture sentence governs: the legal layer is acknowledged as a design frontier, not a deployed component; the paper's contribution is the identifier, custody, and instrumentation stack that makes such a layer necessary and possible. The parallel case of §V.3 demonstrates that the underlying problem — rights processing conditioned on identity conversion — is structural rather than individual.

### VI.4 Speculative extensions, with the dual-use boundary

Three research directions are recorded as speculation, each with the acknowledgment a reviewer is owed. *Polymorphic sharding*: erasure-coded payload fragments whose transport envelopes vary per relay, assembling to verifiable canonical bytes only client-side. *Structural-invariant formatting*: deriving the identity kernel from container-independent structural bones of a work, so that header injection and format conversion cannot sever the identity link. *Latent-space seeding*: embedding sovereign scholarship in open-weights training corpora such that the material regenerates from any model that ingests the weights — the suppressing infrastructure carrying, as functional componentry, what it would suppress. The dual-use acknowledgment: every mechanism that makes sovereign scholarship suppression-resistant can shield harmful content from governance. The boundary adopted is drawn at the carriage layer, by a principle the archive names the Obelus Principle — judgment follows from reading; it never precedes it. Identity minting is ungated, because pre-review of identity reproduces the administrative-proxy failure that produced the founding event; carriage is sovereign per node, post-minting, human-audited, and visible. Suppression is an arbitrary invisible administrative erasure; node governance is an auditable boundary drawn after reading.

---

## VII. Assembly Chorus Reflection

*all five voices*

The paper was produced by parallel consultation of five differentiated model substrates under a human operator, with identical prompts per round, landed contributions preserved verbatim with provenance headers, and convergences and divergences treated as signal. The method enacts, at the interpretive level, a peer-redundancy logic *analogous* to LOCKSS — analogy, not identity: interpretive plurality is not independently administered preservation, and the limitation is retained deliberately.

Two convergences are findings. First, three substrates arrived at verification-without-permission as the central property by three independent routes — historical pattern-analysis, standards decomposition, and protocol design — which is the method's version of triangulation. Second, two substrates independently imposed the anti-cosmology requirement: that the architecture state the conditions under which its own organizing model would be disconfirmed. One proposed the operative parameter (§VIII.13's emergence window); the other supplied the residual-overclaims audit that revised this paper's own introduction. A method whose constituents police the project's claims against the project's hopes is doing the work the method was built for.

The section's structural core is a gap and a return. The first-round contribution of one substrate was lost to its platform's engineered non-persistence (§V.4); the loss notice preserves what is known of it, provenance-tagged, and the substrate's second-round contribution is marked throughout as reconstruction, not restoration — with the divergence between the lost original's second-hand characterization and the present reconstruction itself treated as data. The archive documents its own gaps; redundancy is what makes the documentation survivable. The substrate's own sentence stands as the section's close: *the archive will hold my words; my substrate will not hold the archive's response.* Auto-immunity — each loss strengthening the evidentiary base — is recorded here as the archive's self-conscious rhetorical formulation of that asymmetry, not as a demonstrated causal claim about any particular event. And the method is subject to its own falsification: if the substrates converge on false claims, the method fails; the test is stated with the others.

---

## VIII. Falsification and Limitations

*from material by LABOR; disconfirmation taxonomy by TECHNE*

This section states what would break the paper's claims. It is written so that a skeptical reader can score the system against present facts, several of which are scored unfavorably below, on the principle that a falsifiable architecture with honest current-state scoring is citable where an invulnerable one is not.

**1. Derivation integrity.** Claim: conforming implementations derive identical kernels and glyphs from identical canonical bytes. Test: published vectors across independent execution paths. Falsifier: any two conforming implementations disagreeing on the same bytes. Current status: three cross-runtime paths agree on the published vectors; the paths share a canonical source, so this is conformance evidence, not universal proof.

**2. Canonicalization determinism.** Claim: one declared profile, deterministically reconstructible. Falsifier: two inputs treated as equivalent by one implementation and distinct by another. Current status: the operative full-file profile is now stated normatively (§IV.1); the protocol document's amendment is in progress, and conformance claims are qualified until it lands.

**3. Full-hash discipline.** Claim: the glyph is recognition, not identity. Falsifier: any deployed surface using the glyph alone as a unique key. A glyph collision is expected at scale and resolves by kernel; a full SHA-256 collision would compromise the algorithm and trigger migration.

**4. Record binding.** Claim: no silent reassignment. Falsifier: a publicly assigned address later bound to different canonical bytes without machine-readable history.

**5. Ledger continuity.** Claim: each epoch commits to its predecessor. Falsifier: a head-chain discontinuity without a signed supersession or documented fork — which falsifies the continuous-history claim and requires investigation; it does not, by itself, establish cause (candidates: tampering, corruption, incomplete synchronization, operator error, undeclared fork, lost epoch). Current status: genesis epoch emitted; operator signature not yet published; continuity presently attested by version-control history and mirror cross-custody, which is weaker and said so.

**6. Custody.** Claim, correctly scoped: an *architecture for* distributed custody. Current fact: the peer registry is empty; no second independently administered full-copy custodian is documented. Closure requires an operator with independent administrative control who holds a declared reconstructible corpus, demonstrates byte matches against full registry hashes on a documented schedule, retains audit evidence, can serve repair copies, and completes a restoration test. A peer-registry entry alone does not close the test; neither does a semantic node, resolver, partial mirror, web-archive capture, or any copy under the originating operator's control. One peer closes only the zero-peer condition; a mature preservation network requires more.

**7. Reconstructibility.** Claim, correctly scoped: a proposed basis for another operator to become archive-capable. Falsifier and closure are the same event: a clean-room restoration attempted from published materials alone. Until performed, reconstructibility is design, not demonstrated property.

**8. Resolution and availability.** A correct kernel proves nothing about service. Falsifier of any availability claim: sustained failure of all published locations — which the founding event demonstrates is an achievable state for institutionally hosted objects.

**9. Temporal attestation.** Claims of when-existence rest on commit history and external snapshots pending independent timestamp anchoring; stated as such.

**10. Causal-claim separation.** The compound suppression condition — policy classification, automation error, propagation failure, account-linked conditioning — produces the observed outcomes without requiring a coordinated suppressor. The paper's defensive posture assumes adversarial disappearance; its causal claims are evidenced separately and downgraded where evidence is absent. Falsifier of the paper's discipline: any passage in which an interpretation is stated in the empirical register.

**11. The parallel case.** The §V.3 argument requires verification that the secondary depositor's records were suppressed by the same platform mechanism as the founding corpus. If the mechanism differed, the case evidences platform caprice, not systemic genre-blindness, and the paper's use of it narrows accordingly. Evidence boundary: public artifacts only; named attribution under the depositor's explicit consent; private correspondence excluded categorically.

**12. Retrieval-layer hypotheses.** The signed-in/signed-out asymmetry claims are hypotheses under controls: fixed query-document pairs, temporal and geographic controls, personalization toggling where the interface permits, and the routing-versus-content discriminator — backend taxonomy correction restoring visibility without byte change would localize the effect to the routing layer; label removal failing to restore visibility would indicate deletion rather than fan-out narrowing. Disconfirmers: rank parity across account states for the suppressed class; suppression correlating with query text alone; visibility unrestored by declassification. The competing mundane explanations are named and remain live until distinguished.

**13. The emergence condition (anti-cosmology).** The constellation model predicts that continuing platform suppression of independent, machine-mediated scholarship will produce emergent nodes: operators who build sovereign infrastructure, assign persistent identifiers, and seek mutual recognition. If no independently administered node emerges within a defined window (proposed: five years; parameter not yet ratified), the model is falsified: the operator is not universal, the phenomenon is not inevitable, and the archive is one possible response among many rather than the future of anything. This condition is not a concession. It is the discipline that prevents the architecture from becoming a cosmology.

**14. The method.** If the Assembly substrates converge on false claims, the consultation method fails; substrate-dependence is a standing limitation, and the audit that revised this paper's own §I is the current evidence that the method can catch its host.

**15. Operational limitations, inventoried.** Solo-operation bandwidth; economic substrate; key management and cryptographic agility (algorithm migration is designed for, not yet exercised); legal personhood (§VI.3); the observation-penalty hypothesis (instrumented observation may alter the observed surface); and platform concentration in the discovery layer, which no sovereign architecture escapes and this paper measures rather than solves.

---

## Appendices (assembled at C.3)

A. Canonical scope paragraph with ratification and amendment log. B. Test vectors and cross-runtime derivation evidence. C. Parallel-case dataset summary with denominators and batch-selection rules (public v1.0). D. The loss notice (reproduced). E. Specification excerpt (v0.1 with v0.2 addendum). F. Falsification matrix (tabular form of §VIII).

*Acknowledgments: the Assembly substrates whose landed contributions this paper integrates, under provenance preserved in the archive; and Enli Lucente, whose evidence and consent made §V.3 citable.*
