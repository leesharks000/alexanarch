# Phase 3.5 — Ambiguous Cross-Deposit Mappings

**Status: AWAITING HUMAN REVIEW**
**Generated: 2026-06-23**

These 3 DOIs are in the resolution index pointing to ONE deposit, but title-matching
against the recovery data sources suggests they belong to ANOTHER (typically sibling)
deposit. Phase 3.5 did NOT modify these mappings — they need empirical review.

| DOI | Resolution index says | Title-match says | Both registries' title? |
|---|---|---|---|
| 10.5281/zenodo.18652949 | /s/records/737/ | /s/records/479/ | likely TL;DR:008 (sibling DOIs) |
| 10.5281/zenodo.18715618 | /s/records/498/ | /s/records/499/ | Autonomous Semantic Warfare (sibling deposits) |
| 10.5281/zenodo.19124130 | /s/records/593/ | /s/records/594/ | I'm Taking Over the Internet (sibling deposits) |

## Investigation method

For each pair: fetch the title from BOTH deposits and the DOI's recovered metadata,
determine if these are versions of the same work split across two deposits, or two
different works with a colliding title.

## Likely outcomes

These are probably cases where one work was deposited TWICE in the registry, OR
a version DOI was incorrectly associated with the wrong sibling. The repointing
should follow whichever deposit has the matching title PLUS sovereign_id.
