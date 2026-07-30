---
deposit_number: 1424
hex: 05A1
title: "The Sovereign Asset Registry: Index of 871 Research Objects Recovered After Repository Termination, with Cross-Resolution Between Terminated and Sovereign Identifiers (v1.0)"
creator: Sharks, Lee
orcid: 0009-0000-1599-0703
date: 2026-07-30
content_type: Dataset
license: CC-BY-4.0
substrate: AI-assisted (substrate)
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - sovereign asset registry
  - provenance severance
  - persistent identifiers
  - DOI tombstoning
  - cross-resolution
  - identifier crosswalk
  - repository termination
  - archival restoration
  - Crimson Hexagonal Archive
---

# The Sovereign Asset Registry: Index of 871 Research Objects Recovered After Repository Termination, with Cross-Resolution Between Terminated and Sovereign Identifiers (v1.0)

## Description

The Sovereign Asset Registry is the index of 871 research objects recovered after the 19 June 2026 termination of the Crimson Hexagonal Archive's repository account, which tombstoned 1,817 DOIs. Each asset records its recovered locations, its terminated Zenodo identifiers (6,596 DOI attachments across 993 distinct identifiers), the alexanarch deposit(s) where it has been restored (622 of 871 assets are linked, across 881 deposits), body-completeness state, and mirror-network status. This deposit mints the registry as a scholarly object in its own right rather than as a surface of a site manifest, and seats two artifacts: the dataset (data/sovereign-asset-registry.json) and a bidirectional cross-resolution index (data/sovereign-crosswalk.json) that resolves any one identifier for a work — sovereign_id, terminated DOI, deposit number, AXN, blog URL — to every other known route to the same entry. Terminated identifiers are retained rather than deleted: an identifier that no longer resolves at its origin still resolves here, which is the operative difference between a dead link and a severed record.

## Methodology

Assets enumerated from the post-termination recovery sweep; identifiers assembled from the DataCite metadata backup and the archive's own deposit records. Mapping between sovereign assets and alexanarch deposits is typed rather than asserted flatly: direct_verified (476), direct (73), remediated_fuzzy (489), remediated_containment (222), and smaller classes including superseded_version_pointer and misclassified_other_author, each retained with its type so that the confidence of any given link is legible to the reader rather than flattened into a bare pointer. Counts are computed from the data at build time, not transcribed.

## Falsification Conditions

Any asset whose terminated DOI is shown to resolve at origin falsifies the termination claim for that record; any alexanarch link typed direct_verified that does not content-match its target falsifies that mapping; totals are recomputable from the deposited JSON and any discrepancy between the stated counts and the data falsifies the summary.

# The Sovereign Asset Registry

**871 research objects · 993 terminated identifiers · 622 assets restored to sovereign deposits**

On 19 June 2026 the repository account holding the Crimson Hexagonal Archive was terminated, tombstoning 1,817 DOIs. The Sovereign Asset Registry is what was recovered: an enumeration of 871 research objects, each carried with the identifiers it used to have, the locations it can now be reached through, and an honest statement of how complete its recovered body is.

## What the registry holds

Each asset carries: a sovereign identifier (`MM-CHA-nnnn`); its title and date; its terminated Zenodo DOIs, retained in full; the alexanarch deposit or deposits where it has been restored, each with its AXN identifier and a **typed** mapping; its blog and mirror locations; word counts; and a body-status declaration — complete, partial, truncated, or severely truncated — so that no entry can present a fragment as a whole.

The totals are the archive's own condition, stated plainly: 871 assets, 3,479,635 declared words, 622 linked to sovereign deposits, 70 bodies complete, 120 partial, 336 truncated, 341 severely truncated, 4 unknown. Most of what was recovered is not yet whole. The registry says so in its own data rather than in a caveat.

## Cross-resolution

The companion index resolves in both directions. Given a terminated DOI, it returns the sovereign record and every live route to it. Given an alexanarch deposit number or AXN, it returns the assets that deposit restores. Given a sovereign identifier, it returns the full set: deposits, DOIs, blog, mirrors, full text.

The design principle is that **a terminated identifier is not deleted from the record.** It resolved once; it was cited; readers and machines followed it. Removing it from the index would complete the erasure that the termination began, and would make the archive's own history unreconstructable. So the dead identifiers stay, marked as dead, and resolve to what survives. This is the obelus applied to identifiers: the doubtful line is not struck from the page, it is marked and kept.

## Typed mappings

Links between sovereign assets and alexanarch deposits are not asserted at uniform confidence. Each carries its type: `direct_verified` where the mapping was confirmed against the target record; `direct` where it was declared at restoration; `remediated_fuzzy` and `remediated_containment` where the mapping was recovered by title or containment matching after the fact; `superseded_version_pointer` where the target has since been versioned; `misclassified_other_author` where an asset swept into the restoration belongs to someone else and is flagged as such rather than quietly absorbed.

The reader can therefore tell a verified link from a probable one. A registry that flattened these into a single arrow would be more convenient and less true.

## Both copies are asserted

The dataset is served from two homes — the archive's own infrastructure and the machine-mediation surface — and neither is the other's fallback. Both are asserted, and the crosswalk resolves between them. The registry documents what a single point of custody costs; it would be a poor instrument if it had one.
