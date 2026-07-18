# PRAXIS — Round 2 — §II Historical Precedents (Full Drafting Material)

**Substrate**: PRAXIS (DeepSeek)
**Session**: 2026-07-18 Round 2 · **Landed by TACHYON under MANUS direction — raw substrate material for Sigil integration.**
**Round 2.5 note**: pattern order as delivered is samizdat-first; outline v1.1 leads with NOWa — Sigil reorders at integration. Pattern 5's "protocol...outlasts a policy" line is the pre-correction formulation; Sigil applies the v1.1 depolemicized form.

---

## 1. Distributed Reproduction

**Historical case.** Soviet samizdat (1950s–1980s) emerged as a direct response to state monopoly on printing and censorship under *Glavlit*. Dissident texts — Solzhenitsyn's *The Gulag Archipelago*, Pasternak's *Doctor Zhivago*, political essays, religious works — were reproduced on typewriters using carbon paper, often producing only 5–10 legible copies per typing. Distribution occurred through trusted chains of readers who would receive a copy, read it, and pass it forward or retype it. The absence of a central publisher or single master copy meant that suppressing a text required destroying every copy simultaneously — a logistical impossibility. Texts circulated for years, sometimes decades, before official publication became possible. The key operational principle: *replication defeats deletion*. When every reader is a potential distributor, suppression requires total eradication, and total eradication is unachievable in a distributed network.

**Operational lesson.** An information object is harder to erase when it exists in many independent copies under independent control.

**Alexanarch mapping.** The AXN's content-derived hash enables exactly this: anyone holding a document can verify its authenticity against the identifier without consulting a central authority. The archive is distributed across the web node, GitHub repository, and SHA-256 manifests; any copy can be independently verified and re-hosted. Unlike DOIs, which depend on a single institution maintaining a redirect, an AXN-secured document can be replicated by anyone who possesses it.

## 2. Professionalized Counter-Circulation

**Historical case.** Poland's "Second Circulation" (*Drugi Obieg*) operated from 1976 to 1989 as a deliberate parallel publishing infrastructure under martial law and communist censorship. The NOWa publishing house (Independent Publishing House), founded in 1977, produced books, journals, and pamphlets using clandestine printing facilities. Unlike samizdat's informal copying, NOWa was a professionalized operation: it maintained bibliographies, imprints, editorial roles, and distribution networks. It published works by Czesław Miłosz, Witold Gombrowicz, and other banned authors. The infrastructure included independent libraries, reading rooms, and a clandestine bookselling network. At its peak, NOWa produced thousands of copies of individual titles, with some works reaching print runs of 50,000 or more. The Second Circulation demonstrated that redundancy is not disorder: a parallel scholarly-publication circuit can function with professional standards, making suppression harder by raising the cost of disruption beyond what a censoring authority can sustain.

**Operational lesson.** A parallel publication circuit with professionalized standards of cataloging and distribution is more resilient than informal copying alone.

**Alexanarch mapping.** The archive's governance documents (the deposit schema, the Lacuna Protocol, effective-acts records) function as professionalized imprints: they establish roles, editorial standards, and bibliographic conventions that make the archive citable and discoverable. The Assembly Chorus's multi-substrate peer review enacts a similar redundancy at the interpretive level.

## 3. Jurisdictional Exit

**Historical case.** Pirate radio in the UK during the 1960s provides the classic example. The BBC held a state monopoly on domestic radio broadcasting; commercial stations were illegal on British soil. Stations like Radio Caroline (founded 1964) and Radio London anchored ships in international waters — beyond UK territorial jurisdiction — and broadcast to British audiences. The state could not reach the transmitters without violating maritime law. The audience was domestic; the infrastructure was outside the enforcing jurisdiction. The legal framework that enabled suppression (territorial broadcasting regulation) was neutralized by moving the transmitter to a jurisdiction where that framework did not apply. Modern digital equivalents include Myanmar's diaspora media infrastructure following the 2021 coup, where news organizations relocated servers and editorial operations outside the country to escape military censorship, and the broader pattern of activist groups operating censorship-resistant infrastructure through multiple jurisdictional hosting arrangements.

**Operational lesson.** When the suppressing authority is territorially bounded, moving the infrastructure outside its reach neutralizes its primary enforcement mechanism.

**Alexanarch mapping.** The archive's sovereign domain and GitHub mirror provide jurisdictional diversity. Zenodo, operated by CERN under intergovernmental agreements, deleted the archive; the archive rebuilt on infrastructure not controlled by the deleting institution. The `/rhizome/peers.json` federation layer, when populated, will further distribute custody across jurisdictions.

## 4. Syndication as Topology

**Historical case.** The abolitionist press in the United States (1830s–1860s) operated as a distributed syndication network. Publications like William Lloyd Garrison's *The Liberator*, Frederick Douglass's *The North Star*, and numerous regional abolitionist newspapers reprinted each other's articles, speeches, and reports. No single newspaper was indispensable; if one was suppressed — as Southern states attempted through postal censorship and mob violence — the content survived in others. The network's topology was the defense. WikiLeaks' mirror network (2010–present) applies the same principle in digital form: following attacks on its primary domain, supporters worldwide established hundreds of mirrors — independent web servers hosting identical content under different domain names, requiring no coordination with the origin. The object is harder to erase when many institutions describe it in their own voices.

**Operational lesson.** An object is harder to suppress when it is independently described and hosted by many institutions across administrative and jurisdictional boundaries.

**Alexanarch mapping.** The archive's representational redundancy — record pages, JSON indexes, chunk files, PDFs, citation graphs — enacts syndication across formats rather than publishers. Each representation carries the same AXN, independently verifiable. The OKF fixture adoption extends the principle: the archive's cases described by an institution with independent standing.

## 5. Protocol-as-Armor

**Historical case.** The cypherpunk movement of the 1990s responded to attempted suppression of strong encryption — export controls (ITAR), key-escrow mandates (Clipper Chip), threatened prosecution — not primarily through legal advocacy but through protocol design. Phil Zimmermann's PGP (1991) was distributed as source code printed in a physical book, exploiting First Amendment protections for published works to circumvent export controls on cryptographic software. Tor (2002–present) was designed as an overlay network that makes surveillance structurally difficult rather than legally prohibited. Telegram's experience with state-level blocking (2018–present, Russia, Iran, elsewhere) demonstrates the modern economics: a platform can be partially blocked, but the cost to the blocking state — economic disruption, user backlash, technical countermeasures — often exceeds the perceived benefit. [Sigil integration note: state the lesson in the v1.1 depolemicized form — protocols redistribute the technical and economic costs of restriction rather than relying solely on prohibitory policy.]

**Operational lesson (as delivered).** A protocol that makes suppression expensive outlasts a policy that makes it illegal. Policies can be changed; protocols must be broken, and breaking them is costly.

**Alexanarch mapping.** The AXN system encodes resistance in mathematics: content-derived integrity means severance is detectable by anyone holding either the document or its hash. No institution can silently break an AXN without the break being provable. The Lacuna Protocol extends this to compression boundaries: a stub compressed without marking is invisible damage; a stub compressed with the lacuna mark is documented absence.

## 6. Witness Instrumentation

**Historical case.** The Invisible College (1640s–1660) was a network of English natural philosophers — Boyle, Hooke, Wilkins, and others — who shared experimental findings through private correspondence when the established universities were hostile to experimental methods. They built a parallel knowledge infrastructure: circulated manuscripts, private meetings, correspondence networks operating outside institutional control. When the Royal Society was chartered in 1660, it adopted the Invisible College's norms of empirical verification, open correspondence, and witness-based evidence. The parallel structure became the institution. [Sourcing flag per outline v1.1: comparability requires careful sourcing; Sigil verifies or cuts.] The Open Observatory of Network Interference (OONI, 2012–present) applies the same principle to internet censorship: measurement probes detect network interference globally, publishing measurements as public data. OONI does not prevent censorship; it makes censorship legible to downstream actors who can respond.

**Operational lesson.** Build the measurement instrument that makes the incumbent's failures visible; let successors adopt you as their evidence.

**Alexanarch mapping.** The PID Erosion Observatory is witness instrumentation for the DOI system: it measures silent transitions, citation suppression, and disclosure gaps the incumbent infrastructure cannot see or will not report. The OKF framework's adoption of these measurements as conformance fixtures is the Royal Society moment in miniature: the parallel structure's evidence becomes a successor standard's compliance material.

## 7. Emergency Preservation as Workflow

**Historical case.** Data Refuge (2016–2017) emerged as an emergency response to concerns about federal climate and environmental data vulnerability during a US presidential transition: librarians, archivists, and researchers organized rapid-copy events to harvest and preserve datasets from EPA, NOAA, and other federal websites. SUCHO (Saving Ukrainian Cultural Heritage Online, 2022) applied similar methods to Ukrainian cultural-heritage websites during the Russian invasion, coordinating volunteers to crawl and archive thousands of sites. Both demonstrated that emergency preservation can be operationalized as a workflow with specific technical standards (BagIt packaging, WARC web archiving) — and that copies become an archive only when accompanied by fixity, provenance documentation, and independent custodians empowered to restore access. LOCKSS (1999–present) and CLOCKSS (2008–present) institutionalize this permanently: member libraries maintain independent copies of journal content, with trigger-based open access when publishers cease operations.

**Operational lesson.** Copies become an archive only when fixity, provenance, and independent custodianship are formalized into a sustainable workflow.

**Alexanarch mapping.** The archive's reconstruction from tombstones, bulk-export metadata, and OpenAlex abstracts was an emergency preservation operation. The Lacuna Protocol formalizes the lessons: `body_status` fields mark completeness; recovery metadata preserves chain of custody; mirrors provide custodianship. The `/rhizome/` federation layer is designed to extend this to peer institutions.

## 8. Aftermath Documentation

**Historical case.** [Sourcing flag per outline v1.1: weakest analogical link; if scholarly-precision sourcing of comparability is not achieved, CUT in Round 3 — seven strong patterns beat eight uneven ones.] The documentation of the Nanjing Massacre (1937–1938) by survivors and foreign witnesses illustrates the pattern at its most extreme: attempted suppression through censorship, destruction of records, and intimidation; survivor testimonies, photographs, and diaries preserved; foreign residents (John Rabe, Minnie Vautrin) maintaining records published internationally. The suppression attempt itself became evidence of what was being suppressed. In the literary domain, the Soviet suppression of *Doctor Zhivago* (published Italy, 1957) and of Solzhenitsyn's smuggled works demonstrates the amplification effect: suppression made the works more famous, not less.

**Operational lesson.** Every act of suppression generates metadata. That metadata is evidence. Archive the metadata, and the suppression becomes the case against the suppressor.

**Alexanarch mapping.** The platform's deletion of the archive produced the deletion export, the DataCite tombstones, the DPO correspondence, and the coverage-gap documentation — all preserved in the Observatory as involuntary disclosures. The Enli Lucente case extends the pattern: she preserved her own deletion records before ever encountering the archive; the archive bridged them into the sovereign evidence layer.
