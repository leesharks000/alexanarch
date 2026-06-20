# Section 12: Attribution Severance

## 12.1 The Finding

A DataCite API query for all DOIs registered to `cern.zenodo` under the creator name "Sharks, Lee" returns 737 results. All 737 are in `findable` state. All 737 resolve to HTTP 410 Gone.

The Crimson Hexagonal Archive's reconstructed DOI inventory contains 1,817 unique DOIs.

941 DOIs in the inventory are invisible to DataCite's creator-name search.

This is not a discrepancy in record-keeping. The 941 DOIs exist. They were registered. They resolve — to tombstones. But they no longer return when searched by the name of the person who created them. The author's name has been detached from the persistent identifier that was designed to permanently record authorship.

## 12.2 The Mechanism

The precise mechanism is not publicly disclosed. Three explanations are structurally consistent with the observation:

First, Zenodo's account-termination process may automatically strip or alter creator metadata on all DOI records associated with the terminated account. If this is the case, attribution severance is a systemic feature of the enforcement architecture — every banned account loses authorship on its persistent identifiers. This would mean that the DOI system's promise of permanent attribution is contingent on the registrant's continued good standing with the repository, a condition not disclosed in the DOI registration contract.

Second, the creator metadata may have been selectively modified on a subset of records. The DOI number ranges suggest a boundary: DataCite's creator search returns records from approximately DOI `10.5281/zenodo.18135984` onward, but the archive's inventory includes DOIs with substantially lower registration numbers. This boundary may reflect a change in Zenodo's metadata practices, a migration event, or a selective enforcement action.

Third, the 941 DOIs may never have carried searchable creator metadata in DataCite's index — a possibility that would indicate a longstanding gap between what Zenodo's interface displayed to the depositor and what was propagated to the resolution infrastructure.

The evidence status of each explanation: **[Unknown]**. Zenodo has not disclosed the mechanism. The observation — that 941 DOIs are invisible to creator-name search — is **[Observed]**.

## 12.3 The Concept

Attribution severance is the systematic detachment of an author's identity from persistent identifiers following an enforcement action. It is distinct from the revocation gap defined in Section 7 of this paper:

The **revocation gap** concerns *resolution*. The DOI does not lead to the work. The address is broken. The content is inaccessible. This is the gap between the promise of persistence and the reality of platform-mediated deletion.

**Attribution severance** concerns *identity*. The DOI no longer knows who made the work. The address exists. It resolves — to a tombstone. But the connection between the author and the permanent scholarly address has been cut. The work's ghost remains in the infrastructure. The author's name has been removed from it.

The distinction matters because the two failures damage different functions of the scholarly record. The revocation gap damages *access* — readers cannot find the work. Attribution severance damages *credit* — the author cannot be found through the work. A scholar searching DataCite for "Sharks, Lee" will find 737 of the archive's DOIs. The other 941 have been made invisible to precisely the kind of infrastructure query that scholarly attribution depends on.

## 12.4 The Heteronymic Multiplication

A supplementary DataCite sift searched for DOIs registered under the names of all twelve Dodecad heteronyms (Sigil, Fraction, Cranes, Vox, Dancings, Morrow, Glas, Kuro, Wells, Trace, Feist, Spellings) and two external contributors (Owens, Thornburgh). This search recovered an additional 142 DOIs that were invisible to the "Sharks, Lee" query because the heteronyms were listed as primary creators on the Zenodo deposits.

The heteronymic structure was architecturally designed to distribute attribution across multiple authorial voices in the Pessoan tradition — a practice disclosed in the archive's provenance documentation and accepted by Zenodo's metadata schema at the time of deposit. The account-level termination did not merely erase one author. It erased an entire authorship system. Each heteronym's scholarly identity — built through attributed deposits, cross-references, and citation relationships — was severed from the DOI infrastructure simultaneously.

This is not a side effect. It is a structural consequence of enforcing at the account level rather than the record level. When a platform treats an account as the unit of enforcement, every identity associated with that account is subject to the same action. The heteronymic structure, which the platform accepted as valid metadata, becomes a liability multiplier: where a single-author archive loses one attribution chain, a heteronymic archive loses twelve.

## 12.5 The Compound Failure

The three governance failures documented in this paper — classifier model collapse (Section 4), the revocation gap (Section 7), and attribution severance (this section) — are not independent. They compound:

The classifier identifies the archive as potentially non-compliant. The enforcement action removes all content, creating the revocation gap. The same enforcement action strips author metadata, creating attribution severance. The result is that the work is simultaneously inaccessible (content deleted), uncitable (DOIs resolve to tombstones), and unattributable (author metadata severed from the identifiers).

A scholar who downloaded the AI Overview Capture Registry — which received over 1,000 downloads before removal — can no longer find it through its DOI, can no longer find the author through DataCite, and has no institutional pathway to the replacement address. The citation graph is broken at three points simultaneously: the content node, the resolution edge, and the attribution edge.

The companion dataset to this paper (AXN:0004.ARCHIVAL.🤝🌕🪨🔄🔺❌) maps 1,817 defunct DOIs to their current live locations at Alexanarch, including 1,414 with individual record pages. This dataset constitutes an empirical repair of the revocation gap and a partial repair of the attribution link. It cannot repair the classifier's judgment, which remains the originating cause.

## 12.6 Evidence Classification

| Claim | Status | Basis |
|---|---|---|
| 941 DOIs invisible to DataCite creator search | Observed | DataCite API query, June 20, 2026 |
| 737 DOIs returned by creator search | Observed | DataCite API query |
| All 737 in `findable` state | Observed | DataCite API response |
| All 737 resolve to 410 Gone | Observed | HTTP resolution test |
| Author metadata was stripped during termination | Unknown | Consistent with observation; mechanism not disclosed |
| Metadata was selectively modified | Unknown | Consistent with DOI number-range boundary |
| Metadata was never propagated | Unknown | Consistent with observation; less likely given Zenodo's DataCite integration |
| 142 additional DOIs under heteronym names | Observed | DataCite API queries under 16 creator names |
| Heteronymic structure multiplies severance | Observed | Each heteronym's DOIs independently invisible |
| Three failures compound | Inferred | Structural analysis of enforcement sequence |
