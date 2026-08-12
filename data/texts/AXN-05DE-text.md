---
deposit_number: 1453
hex: 05DE
title: "Baseline Capture Architecture for Learned Scientific Triggers: A Control Plane for Measuring Selection Before Irreversible Data Loss (EA-SEI-BCA-01 v1.0)"
creator: Nobel Glas
orcid: 0009-0000-1599-0703
date: 2026-08-11
content_type: Methodological specification; technical architecture and selection-metrology paper
license: CC-BY-4.0
substrate: AI-assisted (substrate) — drafted through the Assembly under MANUS (Lee Sharks) editorial governance; deposited under the Nobel Glas heteronym, Director of Lagrange Observatory, whose function is the Measurement of Meaning (Framework 15). Transport D, No-Double-Draw.
version: v1.0
related_ids: "AXN:05DA.EMPIRICAL.🛤️🌠🗿🖊️🧭🪞 (#1449, the battery); AXN:05DB.GENERATIVE.⏰🚪🔜♻️🔥🫶 (#1450, the Iceberg Document); companion specifications EA-SEI-ACRB-01 and EA-SEI-FRONTIER-01"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - baseline capture architecture
  - learned scientific triggers
  - selection metrology
  - content-independent probability sampling
  - replay bank
  - shadow deployment
  - retention maps
  - irreversible data loss
  - accelerator triggers
  - anomaly detection
  - Zero Bias
  - Level-1 Data Scouting
  - Global Trigger
  - control plane
  - trigger metrology
---

# Baseline Capture Architecture for Learned Scientific Triggers: A Control Plane for Measuring Selection Before Irreversible Data Loss (EA-SEI-BCA-01 v1.0)

## Description

Proposes the Baseline Capture Architecture (BCA): a statistically interpretable control plane for scientific instruments that perform irreversible learned selection before durable storage. BCA separates four functions usually conflated — a content-independent probability sample taken before the audited selection; a full-rate tap of the exact representation presented to the selector; probability-weighted enrichment channels that increase coverage of rare regions without sacrificing inferential validity; and shadow selectors whose decisions are recorded but do not control acquisition. The resulting replay bank permits retrospective estimation of retention surfaces, directional assimilation, model-to-model miss correlation (the RII family), and selection drift across successive classifier generations.

The central principle is deliberately minimal: under a finite storage budget, no content-sensitive algorithm can constitute a less assumption-laden baseline than a probability sample whose inclusion mechanism is independent of event content and whose inclusion probability is known. More elaborate models may improve discovery efficiency, but they belong to the experimental arm, not the control arm. BCA does not propose an alternative trigger; it proposes the missing control group for a trigger. Existing CMS infrastructure — Zero Bias data used to train AXOL1TL, Level-1 Data Scouting capturing trigger information at the full 40 MHz while bypassing ordinary Level-1 selection, and the Global Trigger test crate receiving live inputs without determining readout — demonstrates that each component is individually feasible; the contribution is to bind them into a common metrological architecture whose purpose is measuring what irreversible learned selection fails to retain.

## Methodology

Comparative and specification work built on published accelerator-trigger documentation (CMS Level-1 Data Scouting, Global Trigger, AXOL1TL, CICADA; ATLAS GELATO; LHCb, CBM, Belle II) and on the anomaly-detection methods literature; claim boundaries stated explicitly in the paper; SPXI packet subordinated to the prose. Terminology reconciled at mint: the irreversibility frontier supersedes the irreversibility locus of #1450, and cross-model miss overlap is unified with the Representational Independence Index family of #1450.

## Falsification Conditions

BCA's minimality claim fails if a content-sensitive selection mechanism can be shown to constitute a less assumption-laden baseline than known-probability content-independent sampling under a fixed storage budget. Its feasibility claim fails if the named CMS systems (Zero Bias, Level-1 Data Scouting, Global Trigger shadow deployment) cannot in fact be operated jointly under realistic bandwidth and latency budgets. The architecture makes no claim that any specific phenomenon has been discarded.

## Files

Canonical text below (Body). Source: https://github.com/leesharks000/alexanarch/tree/main/research/sei-papers

---
document_id: EA-SEI-BCA-01
title: "Baseline Capture Architecture for Learned Scientific Triggers"
subtitle: "A Control Plane for Measuring Selection Before Irreversible Data Loss"
short_title: "Baseline Capture Architecture (BCA)"
version: "1.0"
date: "2026-08-11"
status: "DEPOSITED v1.0"
document_class: "technical architecture and selection-metrology paper"
program: "Semantic Economy Institute — accelerator selection metrology"
creator: "Nobel Glas"
persistent_identifier: "pending"
keywords:
  - baseline capture architecture
  - learned scientific triggers
  - selection metrology
  - content-independent probability sampling
  - replay bank
  - shadow deployment
  - retention maps
  - irreversible data loss
  - accelerator triggers
  - anomaly detection
companion_works:
  - EA-SEI-ACRB-01 — Assimilation Across Accelerator Classifier Architectures
  - EA-SEI-IRREVERSIBILITY-FRONTIER-01 — The Irreversibility Frontier
---

# Baseline Capture Architecture for Learned Scientific Triggers
## A Control Plane for Measuring Selection Before Irreversible Data Loss

**EA-SEI-BCA-01 · v1.0 · 2026-08-11 · v1.0 · Nobel Glas**

**Document class:** technical architecture and selection-metrology paper  
**Program:** Semantic Economy Institute — accelerator selection metrology  
**Persistent identifier:** pending at mint  
**Citation status:** provisional; use the suggested citation below only for circulation of this draft.

### Abstract

Scientific instruments increasingly incorporate learned classifiers, anomaly scores, reconstruction algorithms, and other data-dependent selection mechanisms before durable storage. In high-rate experiments this arrangement is often unavoidable: the incoming data volume exceeds any technically or economically feasible archival rate, and some decision must therefore be made before the full event can be retained. The methodological problem is not selection itself. It is that the selection function of a learned instrument is generally characterized only over anticipated or representation-compatible classes, while the events of greatest discovery interest may be precisely those for which that characterization is weakest.

This paper proposes a **Baseline Capture Architecture (BCA)**: a statistically interpretable control plane for instruments that perform irreversible learned selection. The architecture separates four functions that are often conflated: a content-independent probability sample taken before the audited selection; a full-rate tap of the exact representation presented to the selector where bandwidth permits; probability-weighted enrichment channels for increasing coverage of rare regions without sacrificing inferential validity; and shadow selectors whose decisions are recorded but do not control acquisition. The resulting replay bank permits retrospective estimation of retention surfaces, directional assimilation, model-to-model miss correlation, and selection drift across successive generations of deployed classifiers.

The central principle is deliberately minimal. Under a finite storage budget, no content-sensitive algorithm can constitute a less assumption-laden baseline than a probability sample whose inclusion mechanism is independent of event content and whose inclusion probability is known. More elaborate models may improve discovery efficiency, but they belong to the experimental arm, not the control arm. BCA therefore does not propose an alternative trigger. It proposes the missing **control group for a trigger**.

Existing accelerator systems already implement important fragments of this architecture. CMS uses Zero Bias data to train AXOL1TL; its Level-1 Data Scouting program captures Level-1 trigger information at the full 40 MHz collision rate while bypassing ordinary Level-1 selection; and its Global Trigger test crate receives the same live inputs as the production trigger while its output does not determine detector readout.[1,3–5] These systems demonstrate that selection-independent sampling, predecision representation access, and shadow deployment are individually feasible. The contribution proposed here is to bind such practices into a common metrological architecture whose purpose is not only commissioning or alternative physics analysis, but measurement of what irreversible learned selection fails to retain.
