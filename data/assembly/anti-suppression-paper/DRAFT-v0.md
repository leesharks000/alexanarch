# AXN as Anti-Suppression Infrastructure: Historical Precedents and Design Directions

**DRAFT v0 — C.2 in progress. Sections §I–§II drafted; §III–§VIII to follow from landed Round 2 material per OUTLINE v1.1 and reviews/ROUND-2.5-CONSISTENCY.md.**

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

The question, then: **if assigned persistent identifiers can be silently severed at institutional scale by a single custodial decision, what does "persistent" mean — and what record architecture would make silent severance structurally impossible, rather than merely prohibited by policy?**

### I.3 The claim

The paper's claim is deliberately narrow, and it attaches to a specific layer of the identifier rather than to the identifier as a whole:

> **A claimed correspondence between canonical bytes and an AXN identity kernel is independently verifiable: it matches or it does not, without permission from a registrar or custodian.**

The samizdat copy was authentic because it reproduced the text; the AXN-bearing object is authentic because its canonical bytes reproduce the declared hash. This property — verification without permission — is what DOI-to-content correspondence structurally lacks, and, we will argue, it is the property toward which every historically successful survival pattern converged. The full record address additionally carries a registry position and a semantic classification, which depend on a registry's assignment; the three-layer model in §IV keeps those dependencies explicit so that the claim is never wider than the layer that bears it.

Around that kernel, this paper documents three composable elements: content-derived identification (§IV), distributed custody as architecture and as an honestly unmet test (§VI, §VIII), and public suppression-instrumentation (§V). Together they recapitulate, in machine-native form, the recurrent formula of historical anti-suppression practice (§II): *portable objects + independent custodians + multiple discovery routes + an auditable record of loss*.

The crucial sentence, stated at the outset so the reader can hold the paper to it:

> **AXN does not make disappearance impossible. It makes the identity of the object independently testable, the history of its disappearance recordable, and reconstruction by another custodian technically possible.**

### I.4 Scope of the archive under study

The archive whose suppression and reconstruction supply this paper's primary evidence defines itself as follows, in its ratified canonical scope statement:

> Alexanarch is a sovereign digital archive. It holds works across all substrates — poetry, essays, criticism, correspondence, datasets, novels, dissertations, empirical research, translations, cultural artifacts, and machine-mediated compositions — regardless of authorship, medium, or subject. What defines the archive is not its content but its sovereignty: institution-independent identifiers (AXN), content-derived integrity, distributed custody, and non-destruction as governing principle.
>
> Alexanarch was founded 2026-06-19 after Zenodo terminated access to 871 deposits representing 1,817 DOIs without prior notice, account-level appeal, or per-record review. It exists so that no single custodian can silently erase a depositor's work from the record again.

The substrate-agnosticism is load-bearing rather than demographic: the suppression event under study did not distinguish poetry from datasets, and neither does the countermeasure.

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

Soviet samizdat (1950s–1980s) is the elemental form. Under the state printing monopoly administered through Glavlit, dissident texts — *The Gulag Archipelago*, *Doctor Zhivago*, political and religious writings — were reproduced on typewriters through carbon paper, five to ten legible copies per typing, and passed through chains of readers who received, read, and retyped. With no central publisher and no master copy, suppressing a text required destroying every copy simultaneously, which no enforcement apparatus achieved. The principle is the oldest in this catalog: **replication defeats deletion**; when every reader is a potential distributor, eradication must be total, and total eradication of a distributed object is unachievable.

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

Across eight patterns and four centuries, the survivors converge: objects made portable enough to replicate; custodians independent enough that no single order reaches them all; discovery routes plural enough that no single index controls visibility; and loss recorded auditably enough that erasure itself becomes evidence. None of the historical cases had a mathematics for the first element — samizdat verified copies by memory, LOCKSS by comparing custodians' holdings. What content-derived identification adds is the formula's missing primitive: a way for *anyone*, holding *any* copy, to test its identity against its name without asking an institution. The remainder of this paper is about that primitive — what standards already provide it in fragments (§III), how AXN composes it (§IV), what it does and does not defend against (§V, §VIII), and what would have to exist around it for the formula's other three elements to hold (§VI).

---

*[DRAFT v0 ends here. §III–§VIII follow in the next drafting pass, integrating: LABOR's ten-function standards decomposition and normative three-layer text (§III–§IV); the verified vector table, Enli Lucente case under open consent, and LOSS-NOTICE evidence (§V); Rex Fraction's integration of TECHNE's constellation specification and counsel memorandum (§VI); the five-voice reflection with the gap-and-return (§VII); and LABOR's falsification material with TECHNE's D1–D4 taxonomy and the anti-cosmology condition (§VIII).]*
