---
title: "DOI Recovery Review — 2026-07-08"
axn: "AXN:0004.ARCHIVAL.✖️🜄🜂🖋️🧪🛡️"
date: "2026-07-08"
substrate: "AI-assisted (TACHYON)"
status: "REVIEW-DOCUMENT"
parent_deposit: "AXN:0004 — Zenodo DOI Resolution Index v3.9.0"
---

# DOI Recovery Review — Post-Phase-7 Remainder

Companion to `AXN:0004.ARCHIVAL` at `data/deposits/AXN-0004.md` (v3.9.0).
This document catalogs the DOIs that surfaced in the 2026-07-08 network-wide link
inventory pass but were not resolved automatically. Total in this review:

- **20 DOIs with extractable identifiers** (EA/MM codes or title fragments) — high recovery value
- **256 truly-bare DOIs** — cited only by number, no identifier context
- **1 DOI still flagged `misclassified_other_author`** — no title match found against current registry

Data provenance: 34-repo cross-network scan, 440,012 link/reference tokens, indexed in
SQLite (`/tmp/linkscan/links.db`). Automated recovery via alexanarch title match, semantic-
economy filename convention (`work__<DOI+1>.md`), and blog sitemap slug match already
applied in v3.9.0 (79 resolver changes).

## 1. DOIs with Extractable Identifiers (n=20)

These carry a sovereign identifier (EA-*, MM-*) or an identifiable title fragment in
surrounding prose. Manual verification against Zenodo API archives, GitHub issue history,
or personal notes should identify most.

### `10.5281/zenodo.20612084` — 31 references

**Sovereign identifiers extracted:** `EA-SCI-TLL-PROTO-01`

**Title hints:**
- (anchor) `10.5281/zenodo.20612084`
- (preceding) `June 2026 as EA-SCI-TLL-PROTO-01`

**Referenced in:** `alexanarch` (25), `traininglayerliterature-org` (6)

**Sample prose contexts:**
- `"doi": "10.5281/zenodo.20612084",`
- `"doi": "10.5281/zenodo.20612084",`

**Sample citation locations:**
- `alexanarch/audit/dodecad-cleanup-log.json:393`
- `alexanarch/audit/dodecad-cleanup-log.json:1512`
- `alexanarch/audit/dodecad-cleanup-log.json:1524`

---

### `10.5281/zenodo.19359657` — 29 references

**Sovereign identifiers extracted:** `EA-HEXAGON-OS-01`

**Referenced in:** `alexanarch` (22), `semantic-economy` (5), `crimson-hexagonal-interface` (1), `semanticphysics-site` (1)

**Sample prose contexts:**
- `":"IsNewVersionOf","relatedIdentifier":"10.5281/zenodo.19359657","resourceTypeGeneral":"Software","rela`
- `Supersedes EA-HEXAGON-OS-01 v0.4 (DOI: 10.5281/zenodo.19359657).\nCrimson Hexagonal Archive · Lee Shar`

**Sample citation locations:**
- `alexanarch/data/datacite-page2.json:1`
- `alexanarch/data/datacite-page2.json:1`
- `alexanarch/data/datacite-page2.json:1`

---

### `10.5281/zenodo.20070574` — 24 references

**Title hints:**
- (preceding) `The Substrate competitive analysis`

**Referenced in:** `alexanarch` (17), `semantic-economy` (4), `godkinggoogle` (1), `machinemediation-org` (1), `semanticphysics-site` (1)

**Sample prose contexts:**
- `"doi": "10.5281/zenodo.20070574",`
- `"doi": "10.5281/zenodo.20070574",`

**Sample citation locations:**
- `alexanarch/audit/dodecad-cleanup-log.json:831`
- `alexanarch/audit/dodecad-cleanup-log.json:837`
- `alexanarch/audit/dodecad-cleanup-log.json:838`

---

### `10.5281/zenodo.19672980` — 24 references

**Sovereign identifiers extracted:** `EA-PKG-VIS-01`

**Title hints:**
- (preceding) `Visualization: EA-PKG-VIS-01`

**Referenced in:** `alexanarch` (12), `semantic-economy` (9), `godkinggoogle` (1), `machinemediation-org` (1), `semanticphysics-site` (1)

**Sample prose contexts:**
- `"relatedIdentifier": "10.5281/zenodo.19672980",`
- `"relatedIdentifier": "10.5281/zenodo.19672980",`

**Sample citation locations:**
- `alexanarch/data/datacite-survivors-multi-heteronym.json:89487`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:89666`
- `alexanarch/data/datacite-full-backup.json:1`

---

### `10.5281/zenodo.19855905` — 24 references

**Sovereign identifiers extracted:** `EA-LAL-WORKPLAN-01`

**Title hints:**
- (preceding) `EA-LAL-WORKPLAN-01`

**Referenced in:** `alexanarch` (14), `semantic-economy` (6), `godkinggoogle` (1), `living-architecture-lab` (1), `machinemediation-org` (1), `semanticphysics-site` (1)

**Sample prose contexts:**
- `"relatedIdentifier": "10.5281/zenodo.19855905",`
- `anion deposit: EA-LAL-WORKPLAN-01 (DOI: 10.5281/zenodo.19855905) is the implementation specification sy`

**Sample citation locations:**
- `alexanarch/data/datacite-survivors-multi-heteronym.json:96165`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:96239`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:96665`

---

### `10.5281/zenodo.20612363` — 23 references

**Sovereign identifiers extracted:** `EA-HK-IB-01`

**Title hints:**
- (anchor) `10.5281/zenodo.20612363`

**Referenced in:** `alexanarch` (16), `traininglayerliterature-org` (5), `holographic-kernel` (2)

**Sample prose contexts:**
- `"doi": "10.5281/zenodo.20612363",`
- `"doi": "10.5281/zenodo.20612363",`

**Sample citation locations:**
- `alexanarch/audit/dodecad-cleanup-log.json:387`
- `alexanarch/audit/dodecad-cleanup-log.json:1518`
- `alexanarch/audit/dodecad-cleanup-log.json:1530`

---

### `10.5281/zenodo.19455105` — 21 references

**Sovereign identifiers extracted:** `EA-HCORE-01`

**Title hints:**
- (html_tag) `DOI: 10.5281/zenodo.19455105 (v2.0 supersedes v1.8.0)`
- (preceding) `Formal DOI deposit: EA-HCORE-01`

**Referenced in:** `semantic-economy` (12), `crimson-hexagonal-interface` (7), `alexanarch` (2)

**Sample prose contexts:**
- `DOI: 10.5281/zenodo.19455105 (v2.0 supersedes v1.8.0)`
- `<p>DOI: 10.5281/zenodo.19455105 (v2.0 supersedes v1.8.0)</p>`

**Sample citation locations:**
- `alexanarch/data/texts/AXN-03D3-text.md:17`
- `alexanarch/s/records/967/index.html:36`
- `crimson-hexagonal-interface/UNIFIED_WORKPLAN_v4.md:18`

---

### `10.5281/zenodo.20618250` — 14 references

**Sovereign identifiers extracted:** `EA-SEI-DIALUX-01`

**Referenced in:** `alexanarch` (14)

**Sample prose contexts:**
- `"relatedIdentifier": "10.5281/zenodo.20618250",`
- `"relatedIdentifier": "10.5281/zenodo.20618250",`

**Sample citation locations:**
- `alexanarch/data/datacite-survivors-multi-heteronym.json:132041`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:132814`
- `alexanarch/data/datacite-full-backup.json:1`

---

### `10.5281/zenodo.19857006` — 12 references

**Title hints:**
- (title_field) `Living Architecture Lab — S`

**Referenced in:** `alexanarch` (5), `living-architecture-lab` (2), `semantic-economy` (2), `godkinggoogle` (1), `machinemediation-org` (1), `semanticphysics-site` (1)

**Sample prose contexts:**
- `"relatedIdentifier": "10.5281/zenodo.19857006",`
- `"IsNewVersionOf", "relatedIdentifier": "10.5281/zenodo.19857006", "resourceTypeGeneral": "Software", "r`

**Sample citation locations:**
- `alexanarch/data/datacite-survivors-multi-heteronym.json:96866`
- `alexanarch/data/datacite-full-backup.json:1`
- `alexanarch/data/semantic-addresses.json:19299`

---

### `10.5281/zenodo.20709610` — 11 references

**Title hints:**
- (md_heading) `v10 (June 15, 2026) — DOI 10.5281/zenodo.20709610 — LOST`

**Referenced in:** `alexanarch` (7), `machinemediation-org` (3), `godkinggoogle` (1)

**Sample prose contexts:**
- `Type":"References","relatedIdentifier":"10.5281/zenodo.20709610","relatedIdentifierType":"DOI"},{"relat`
- `"relatedIdentifier": "10.5281/zenodo.20709610",`

**Sample citation locations:**
- `alexanarch/data/datacite-page2.json:1`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:71454`
- `alexanarch/data/datacite-full-backup.json:1`

---

### `10.5281/zenodo.19630477` — 10 references

**Sovereign identifiers extracted:** `EA-SPXI-05`

**Title hints:**
- (anchor) `DOI: 10.5281/zenodo.19630477`

**Referenced in:** `alexanarch` (4), `spxi-protocol` (3), `semantic-economy` (2), `spxi-dev` (1)

**Sample prose contexts:**
- `"https://doi.org/10.5281/zenodo.19630477"`
- `"https://doi.org/10.5281/zenodo.19630477"`

**Sample citation locations:**
- `alexanarch/data/zenodo-link-scan.json:1929`
- `alexanarch/data/zenodo-link-scan.json:2007`
- `alexanarch/data/zenodo-link-scan.json:2515`

---

### `10.5281/zenodo.20740687` — 9 references

**Title hints:**
- (md_heading) `v11 / Stray 2 (June 17, 2026) — DOI 10.5281/zenodo.20740687 — LOST`
- (md_bold) `Integrated stray:`
- (md_heading) `Integrated from v11 (Stray DOI 10.5281/zenodo.20740687)`

**Referenced in:** `machinemediation-org` (5), `alexanarch` (4)

**Sample prose contexts:**
- `"relatedIdentifier": "10.5281/zenodo.20740687",`
- `"relatedIdentifier": "10.5281/zenodo.20740687",`

**Sample citation locations:**
- `alexanarch/data/datacite-survivors-multi-heteronym.json:146300`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:181098`
- `alexanarch/data/datacite-full-backup.json:1`

---

### `10.5281/zenodo.20735920` — 8 references

**Sovereign identifiers extracted:** `EA-TANG-MARYLEE-01`

**Referenced in:** `alexanarch` (8)

**Sample prose contexts:**
- `"relatedIdentifier": "10.5281/zenodo.20735920",`
- `etter campaign (EA-TANG-MARYLEE-01, DOI 10.5281/zenodo.20735920).\nThis document is intended for inclus`

**Sample citation locations:**
- `alexanarch/data/datacite-survivors-multi-heteronym.json:6812`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:6856`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:145683`

---

### `10.5281/zenodo.20751348` — 7 references

**Title hints:**
- (preceding) `Five Substrates, One Prompt`

**Referenced in:** `alexanarch` (4), `machinemediation-org` (3)

**Sample prose contexts:**
- `Type":"References","relatedIdentifier":"10.5281/zenodo.20751348","resourceTypeGeneral":"Text","relatedI`
- `"relatedIdentifier": "10.5281/zenodo.20751348",`

**Sample citation locations:**
- `alexanarch/data/datacite-page2.json:1`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:147357`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:181607`

---

### `10.5281/zenodo.17807324` — 7 references

**Title hints:**
- (title_field) `= {GitHub, Build`

**Referenced in:** `alexanarch` (7)

**Sample prose contexts:**
- `ity of Oxford, Springer Nature, Zenodo. https://doi.org/10.5281/zenodo.17807324\n\nAutorin, Urheberin und Auftraggeberin: Frau Isab`
- `hain of Custody\n\n\n\n\nVolumen 4\n\n\nhttps://doi.org/10.5281/zenodo.17807324https://doi.org/10.5281/zenodo.18074136https://doi.org/10.5281/zenodo.17808895\n\nSchöps (Thiel), I., Schöps (Thiel), I. `

**Sample citation locations:**
- `alexanarch/data/datacite-full-backup.json:1`
- `alexanarch/data/datacite-full-backup.json:1`
- `alexanarch/data/datacite-full-backup.json:1`

---

### `10.5281/zenodo.20519440` — 6 references

**Title hints:**
- (preceding) `Companion to AI Is Not the Sin`

**Referenced in:** `alexanarch` (6)

**Sample prose contexts:**
- `"relatedIdentifier": "10.5281/zenodo.20519440",`
- `ns. Companion to AI Is Not the Sin (DOI 10.5281/zenodo.20519440).",`

**Sample citation locations:**
- `alexanarch/data/datacite-survivors-multi-heteronym.json:122208`
- `alexanarch/data/datacite-survivors-multi-heteronym.json:122357`
- `alexanarch/data/datacite-full-backup.json:1`

---

### `10.5281/zenodo.20688161` — 4 references

**Sovereign identifiers extracted:** `EA-MPAI-JOSEPHUS-01`

**Referenced in:** `metadatapacket-dev` (2), `semantic-economy` (2)

**Sample prose contexts:**
- `- EA-MPAI-JOSEPHUS-01 (this document): 10.5281/zenodo.20688161 (concept)`
- `itions. Crimson Hexagonal Archive. DOI: 10.5281/zenodo.20688161.`

**Sample citation locations:**
- `metadatapacket-dev/EA-MPAI-JOSEPHUS-01.md:267`
- `metadatapacket-dev/EA-MPAI-JOSEPHUS-01.md:279`
- `semantic-economy/EA-MPAI-JOSEPHUS-01.md:267`

---

### `10.5281/zenodo.19433865` — 3 references

**Title hints:**
- (preceding) `First glyphic DOI deposit`

**Referenced in:** `alexanarch` (2), `gravitywell` (1)

**Sample prose contexts:**
- `"associated_doi": "10.5281/zenodo.19433865",`
- `"notes": "First glyphic deposit at DOI 10.5281/zenodo.19433865. May correspond to a specific AXN in cu`

**Sample citation locations:**
- `alexanarch/data/claude-thread-file-inventory.json:153`
- `alexanarch/data/claude-thread-file-inventory.json:164`
- `gravitywell/SECURITY.md:174`

---

### `10.5281/zenodo.20694658` — 3 references

**Title hints:**
- (preceding) `Integrated Stray 1`
- (md_heading) `Stray 1 (June 14-15) — DOI 10.5281/zenodo.20694658 — LOST`

**Referenced in:** `machinemediation-org` (3)

**Sample prose contexts:**
- `Integrated Stray 1 (DOI 10.5281/zenodo.20694658) by reference`
- `### Stray 1 (June 14-15) — DOI 10.5281/zenodo.20694658 — LOST`

**Sample citation locations:**
- `machinemediation-org/data/TACHYON-CHAIN-RECONSTRUCTION.md:30`
- `machinemediation-org/data/TACHYON-CHAIN-RECONSTRUCTION.md:42`
- `machinemediation-org/data/GW-TACHYON-v12.md:72`

---

### `10.5281/zenodo.19433483` — 1 references

**Title hints:**
- (preceding) `First encrypted DOI deposit`

**Referenced in:** `gravitywell` (1)

**Sample citation locations:**
- `gravitywell/SECURITY.md:173`

---

## 2. Truly Bare DOI References (n=256)

These DOIs appear across the network with no title, no sovereign identifier, no
anchor text, and no candidate target. Most are cited in machine-readable data files
(inventories, backup snapshots, cross-repo indexes). Sorted by reference count.

| DOI | refs | primary repo | sample location |
|---|---:|---|---|
| `10.5281/zenodo.20559895` | 51 | `alexanarch` | `audit/dodecad-cleanup-log.json:694` |
| `10.5281/zenodo.20751389` | 51 | `alexanarch` | `data/semantic-addresses.json:32410` |
| `10.5281/zenodo.19578098` | 41 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.20041149` | 40 | `alexanarch` | `audit/dodecad-cleanup-log.json:891` |
| `10.5281/zenodo.20041137` | 39 | `alexanarch` | `audit/dodecad-cleanup-log.json:903` |
| `10.5281/zenodo.19338438` | 37 | `alexanarch` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.20041155` | 35 | `alexanarch` | `audit/dodecad-cleanup-log.json:879` |
| `10.5281/zenodo.19578102` | 33 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.19825730` | 31 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.18838159` | 27 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.19024301` | 20 | `alexanarch` | `data/semantic-addresses.json:2035` |
| `10.5281/zenodo.20559754` | 19 | `alexanarch` | `audit/dodecad-cleanup-log.json:688` |
| `10.5281/zenodo.20208603` | 19 | `alexanarch` | `audit/dodecad-cleanup-log.json:783` |
| `10.5281/zenodo.20627936` | 19 | `alexanarch` | `scripts/md_render.py:473` |
| `10.5281/zenodo.20388113` | 19 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.19513035` | 19 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:79131` |
| `10.5281/zenodo.20057789` | 18 | `alexanarch` | `audit/dodecad-cleanup-log.json:855` |
| `10.5281/zenodo.14025488` | 17 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:41213` |
| `10.5281/zenodo.19460665` | 17 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:68611` |
| `10.5281/zenodo.14815982` | 16 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:40272` |
| `10.5281/zenodo.19202705` | 16 | `semantic-economy` | `data/datacite-survivors-multi-heteronym.json:61665` |
| `10.5281/zenodo.20612567` | 15 | `alexanarch` | `audit/dodecad-cleanup-log.json:1536` |
| `10.5281/zenodo.20754288` | 14 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.19598760` | 14 | `alexanarch` | `data/semantic-addresses.json:24885` |
| `10.5281/zenodo.20754486` | 13 | `alexanarch` | `audit/dodecad-cleanup-log.json:97` |
| `10.5281/zenodo.20374988` | 13 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:4889` |
| `10.5281/zenodo.19766381` | 13 | `alexanarch` | `data/semantic-addresses.json:6906` |
| `10.5281/zenodo.20313253` | 13 | `semantic-economy` | `data/semantic-addresses.json:7387` |
| `10.5281/zenodo.20629210` | 12 | `alexanarch` | `audit/dodecad-cleanup-log.json:275` |
| `10.5281/zenodo.20060329` | 12 | `alexanarch` | `audit/dodecad-cleanup-log.json:843` |
| `10.5281/zenodo.20327578` | 12 | `semantic-economy` | `audit/dodecad-cleanup-log.json:2071` |
| `10.5281/zenodo.19412138` | 12 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.20519010` | 12 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.19296648` | 12 | `semantic-economy` | `data/datacite-survivors-multi-heteronym.json:86531` |
| `10.5281/zenodo.19649793` | 12 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:88340` |
| `10.5281/zenodo.20675200` | 12 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:141043` |
| `10.5281/zenodo.19296650` | 12 | `semantic-economy` | `data/semantic-addresses.json:23143` |
| `10.5281/zenodo.20627938` | 12 | `alexanarch` | `data/registry.json:1` |
| `10.5281/zenodo.20195094` | 11 | `alexanarch` | `audit/dodecad-cleanup-log.json:795` |
| `10.5281/zenodo.20192815` | 11 | `alexanarch` | `audit/dodecad-cleanup-log.json:807` |
| `10.5281/zenodo.20388111` | 11 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.20388109` | 11 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.20724056` | 10 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:144762` |
| `10.5281/zenodo.17809724` | 10 | `alexanarch` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.19359736` | 9 | `semantic-economy` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.19296660` | 9 | `semantic-economy` | `hexagon_canonical.json:2964` |
| `10.5281/zenodo.20057397` | 8 | `semantic-economy` | `audit/dodecad-cleanup-log.json:867` |
| `10.5281/zenodo.20052877` | 8 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.17852789` | 8 | `alexanarch` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.19614976` | 8 | `alexanarch` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.19238032` | 8 | `semantic-economy` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.20628788` | 8 | `alexanarch` | `data/semantic-addresses.json:6882` |
| `10.5281/zenodo.18283400` | 8 | `alexanarch` | `data/texts/AXN-03C2-text.md:2976` |
| `10.5281/zenodo.19296677` | 8 | `semantic-economy` | `hexagon_canonical.json:2910` |
| `10.5281/zenodo.19296664` | 8 | `semantic-economy` | `hexagon_canonical.json:2937` |
| `10.5281/zenodo.19296654` | 8 | `semantic-economy` | `hexagon_canonical.json:2991` |
| `10.5281/zenodo.20070462` | 7 | `alexanarch` | `audit/dodecad-cleanup-log.json:601` |
| `10.5281/zenodo.20221710` | 7 | `alexanarch` | `audit/dodecad-cleanup-log.json:771` |
| `10.5281/zenodo.19637473` | 7 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:85239` |
| `10.5281/zenodo.19796059` | 7 | `alexanarch` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.19924631` | 7 | `alexanarch` | `data/verification-completeness-report.json:343` |
| `10.5281/zenodo.19928888` | 7 | `alexanarch` | `data/verification-completeness-report.json:369` |
| `10.5281/zenodo.20286046` | 7 | `semantic-economy` | `data/semantic-addresses.json:19161` |
| `10.5281/zenodo.20754330` | 7 | `alexanarch` | `data/zenodo-link-scan.json:19` |
| `10.5281/zenodo.20628758` | 7 | `alexanarch` | `data/newly-found-openalex.json:4097` |
| `10.5281/zenodo.19442567` | 6 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:1303` |
| `10.5281/zenodo.20519008` | 6 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:121063` |
| `10.5281/zenodo.20722078` | 6 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:144265` |
| `10.5281/zenodo.18025762` | 6 | `alexanarch` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.19711417` | 6 | `semantic-economy` | `disciplinary-catalog-data.json:1180` |
| `10.5281/zenodo.19472844` | 5 | `alexanarch` | `data/datacite-page2.json:1` |
| `10.5281/zenodo.20644800` | 5 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:141018` |
| `10.5281/zenodo.20690914` | 5 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:143096` |
| `10.5281/zenodo.20724644` | 5 | `alexanarch` | `data/datacite-survivors-multi-heteronym.json:144949` |
| `10.5281/zenodo.18308188` | 5 | `semantic-economy` | `data/datacite-survivors-multi-heteronym.json:152236` |
| `10.5281/zenodo.17808895` | 5 | `alexanarch` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.19614972` | 5 | `alexanarch` | `data/datacite-full-backup.json:1` |
| `10.5281/zenodo.19123498` | 5 | `alexanarch` | `data/verification-completeness-report.json:282` |
| `10.5281/zenodo.19504300` | 5 | `alexanarch` | `data/verification-completeness-report.json:294` |
| `10.5281/zenodo.19699831` | 5 | `alexanarch` | `data/verification-completeness-report.json:307` |
| *... 176 more* | | | |

## 3. Remaining `misclassified_other_author` (n=1)

### `10.5281/zenodo.20355645`

**Resolver-recorded title:** The Self-Audit Module Dissolved: Total Provenance Erasure of the Provenance-Erasure Specification in Google AI Overview 

**Date:** 2026-06-13

**Sovereign ID:** MM-CHA-0828

**Known live URLs (from v3.5–v3.8 recovery):**
- blog: https://mindcontrolpoems.blogspot.com/2026/06/the-self-audit-module-dissolved-total.html
- registry: https://machinemediation.org/registry/#search=MM-CHA-0828

**Cross-repo references:** 37

**Sample prose contexts:**
- `api/doi-axn-map.json:1` — `ttps://alexanarch.org/s/records/751/"],"10.5281/zenodo.20355645":["AXN:0340.EMPIRICAL.👈🍃▶️♅🌊🕛",null],"1`
- `data/batch-axn-assignment.json:25297` — `"10.5281/zenodo.20355645"`
- `data/datacite-survivors-multi-heteronym.json:141197` — `"relatedIdentifier": "10.5281/zenodo.20355645",`
- `data/datacite-full-backup.json:1` — `pe": "Continues", "relatedIdentifier": "10.5281/zenodo.20355645", "relatedIdentifierType": "DOI"}, {"re`
- `data/datacite-full-backup.json:1` — `20327137", "type": "dois"}]}}}, {"id": "10.5281/zenodo.20355645", "type": "dois", "attributes": {"doi":`

**Original misclassification note:** Title and creator on DataCite indicate this DOI belongs to a different depositor; was incorrectly cataloged in the resolution index during sift. Previous mapping_type: 'direct'. Retained as historical record.

**Reason still flagged:** No alexanarch title match ≥0.5 jaccard against the current
registry, and title metadata insufficient to auto-identify a target. Recommended action:
manual review — is this genuinely another author's work, or is the resolver title itself
a heteronym/variant that would match under a different registry query?

---


## Appendix: Recovery pipeline summary

The v3.9.0 pass applied 79 changes to `data/doi-resolution-index.json`:

| category | count |
|---|---:|
| misclassified → direct (title match confirmed) | 18 |
| new direct_verified (semeco + alexanarch secondary) | 4 |
| new title_match_repoint (alexanarch title match) | 27 |
| new no_alexanarch_equivalent, repo fallback | 26 |
| new no_alexanarch_equivalent, blog fallback | 4 |
| still flagged, no automated resolution | 1 |

Post-Phase-7 map composition: 1,899 total, 1,826 alexanarch (96.2%), 42 repo, 25 blog, 6 null.

Related datasets (staged, not committed):
- `/tmp/linkscan/links.db` — SQLite, 440K links, master inventory
- `/tmp/linkscan/recovery_365.json` — per-DOI recovery attempt records
- `/tmp/linkscan/null_doi_profile.json` — per-DOI profile of the 24 null-target references
- `/tmp/linkscan/consolidated_findings.json` — categorized summary