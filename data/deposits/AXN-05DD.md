---
deposit_number: 1452
hex: 05DD
title: "The Irreversibility Frontier: Comparative Architectures of Online Selection in Accelerator Science (EA-SEI-IRREVERSIBILITY-FRONTIER-01 v1.0)"
creator: Nobel Glas
orcid: 0009-0000-1599-0703
date: 2026-08-11
content_type: Theoretical paper; comparative architecture analysis and selection metrology
license: CC-BY-4.0
substrate: AI-assisted (substrate) — drafted through the Assembly under MANUS (Lee Sharks) editorial governance; deposited under the Nobel Glas heteronym, Director of Lagrange Observatory, whose function is the Measurement of Meaning (Framework 15). Transport D, No-Double-Draw.
version: v1.0
related_ids: "AXN:05DA.EMPIRICAL.🛤️🌠🗿🖊️🧭🪞 (#1449, the battery); AXN:05DB.GENERATIVE.⏰🚪🔜♻️🔥🫶 (#1450, the Iceberg Document); companion specifications EA-SEI-BCA-01 and EA-SEI-ACRB-01"
axn_schema_version: v2
protocol_version: alexanarch-deposit-protocol/v1
keywords:
  - irreversibility frontier
  - Irreversibility Profile
  - fidelity locus
  - replay horizon
  - bypass channel
  - semantic selection
  - representational irreversibility
  - retention irreversibility
  - CMS
  - ATLAS
  - LHCb
  - CBM
  - Belle II
  - free streaming
  - Zero Bias
  - Level-1 Data Scouting
  - No-Retention-Bound
---

# The Irreversibility Frontier: Comparative Architectures of Online Selection in Accelerator Science (EA-SEI-IRREVERSIBILITY-FRONTIER-01 v1.0)

## Description

Defines the irreversibility frontier: for a specified scientific question and fidelity hierarchy, the earliest stage at which an event-content-dependent transformation or gate can permanently eliminate a scientifically relevant distinction without a sufficiently independent durable record from which that loss can later be audited. A detector may have several frontiers at different fidelity levels, so an architecture is described by an Irreversibility Profile — the tuple (fidelity locus, entering rate, surviving fraction, replay horizon, bypass channels, selector class) — rather than by a scalar score, which would imply comparability the present evidence does not justify. The scientifically decisive variables are the locus and the bypass.

The paper distinguishes representational from retention irreversibility, separates semantic depth from physical depth, and applies the profile comparatively across CMS (early irreversible selection with emerging side channels: Zero Bias, Global Trigger shadow deployment, Level-1 Data Scouting), ATLAS (a comparable early frontier with multi-level learned anomaly selection), LHCb (physics selection moved downstream of full-detector readout), CBM (free streaming before event ontology), and Belle II. It closes by connecting the frontier to the No-Retention-Bound observation: validation of individual stages on their design support establishes no nontrivial lower bound on end-to-end retention for a novelty distribution outside that characterized support. This paper supersedes the term irreversibility locus introduced in EA-SEI-ICEBERG-01.

## Methodology

Comparative and specification work built on published accelerator-trigger documentation (CMS Level-1 Data Scouting, Global Trigger, AXOL1TL, CICADA; ATLAS GELATO; LHCb, CBM, Belle II) and on the anomaly-detection methods literature; claim boundaries stated explicitly in the paper; SPXI packet subordinated to the prose. Terminology reconciled at mint: the irreversibility frontier supersedes the irreversibility locus of #1450, and cross-model miss overlap is unified with the Representational Independence Index family of #1450.

## Falsification Conditions

The comparative claim fails if the profile components cannot be assigned consistently to the named experiments from published documentation, or if experiments with materially different profiles show no corresponding difference in auditability of what their selection discards. The framework makes no claim about which architecture is scientifically superior; it claims only that locus and bypass are the decisive comparative variables.

## Files

Canonical text below (Body). Source: https://github.com/leesharks000/alexanarch/tree/main/research/sei-papers

---
document_id: EA-SEI-IRREVERSIBILITY-FRONTIER-01
title: "The Irreversibility Frontier"
subtitle: "Comparative Architectures of Online Selection in Accelerator Science"
short_title: "The Irreversibility Frontier"
version: "1.0"
date: "2026-08-11"
status: "DEPOSITED v1.0"
document_class: "comparative accelerator-systems and scientific-metrology paper"
program: "Semantic Economy Institute — accelerator selection metrology"
creator: "Nobel Glas"
persistent_identifier: "pending"
keywords:
  - irreversibility frontier
  - accelerator trigger architecture
  - selection metrology
  - representational irreversibility
  - retention irreversibility
  - recoverability envelope
  - online reconstruction
  - triggerless readout
  - data scouting
  - shadow deployment
  - scientific observability
companion_works:
  - EA-SEI-ACRB-01 — Assimilation Across Accelerator Classifier Architectures
  - EA-SEI-BCA-01 — Baseline Capture Architecture for Learned Scientific Triggers
---

# The Irreversibility Frontier
## Comparative Architectures of Online Selection in Accelerator Science

**EA-SEI-IRREVERSIBILITY-FRONTIER-01 · v1.0 · 2026-08-11 · v1.0 · Nobel Glas**

**Document class:** comparative accelerator-systems and scientific-metrology paper  
**Program:** Semantic Economy Institute — accelerator selection metrology  
**Persistent identifier:** pending at mint  
**Citation status:** provisional; use the suggested citation below only for circulation of this draft.

### Abstract

High-rate accelerator experiments necessarily discard data. The scientific question is therefore not whether selection occurs, but **where selection becomes irreversible relative to sensing, representation, reconstruction, and durable preservation**. This variable is rarely treated as a comparative property of experimental architecture. Trigger papers conventionally report rates, latency, efficiencies, resource utilization, and benchmark sensitivity. These quantities describe how a selector performs on events whose relevance is already specified. They do not by themselves describe how much evidence survives from which the selector's blind spots could later be discovered.

This paper introduces the **irreversibility frontier** as a metrological description of online scientific selection. We distinguish two forms of irreversible loss: **representational irreversibility**, in which information is removed by a non-invertible transformation without a surviving upstream copy, and **retention irreversibility**, in which an event-content-dependent decision permanently prevents an event from entering durable scientific memory. We then define an **Irreversibility Profile** that records the fidelity locus of the first consequential gate, its input rate and retention fraction, the selector class operating there, the existence and fidelity of independent bypass channels, and the time horizon over which predecision data remain replayable.

The comparison is developed across several current accelerator architectures. CMS and ATLAS retain conventional early hardware-trigger frontiers at the 40 MHz LHC bunch-crossing rate, while now placing learned anomaly detection inside those trigger systems. CMS simultaneously demonstrates partial counterarchitectures through Zero Bias sampling, Level-1 Data Scouting at 40 MHz, and a Global Trigger test crate that receives live production inputs without controlling detector readout. LHCb moves the first major physics selection downstream of full-detector readout, reconstructing the 30 MHz collision stream in an all-software trigger whose first stage runs on GPUs. CBM pushes the distinction further: its self-triggered detectors produce a free-streaming input in which events are not predefined and full online event reconstruction occurs inside the First-level Event Selector. Belle II demonstrates that sophisticated learned reconstruction, including a deployed graph neural network, can itself be placed in the first-level hardware trigger path. Current sPHENIX/EIC R&D provides a prospective case in which streaming readout and learned online selection are still being co-designed.

The comparison does not establish that later selection is automatically more sensitive to unknown physics, nor that machine learning uniquely creates irreversible bias. The irreversibility frontier predates machine learning. The methodological claim is narrower: **when ontology-bearing or learned selection occurs before an independent durable record is made, a class rejected by the selector may also lose the evidentiary channel through which the rejection could later be measured.** Moving the frontier downstream, widening content-independent bypasses, or preserving predecision representations enlarges the set of novelty classes for which retention remains retrospectively auditable.

The paper concludes by proposing an **Irreversibility Statement** as a standard component of documentation for learned and high-rate scientific selectors. The companion Accelerator Classifier Retention Battery specifies what retention behavior should be measured; the companion Baseline Capture Architecture specifies how to preserve an independent control plane from which it can be measured. The present paper identifies the architectural variable that determines whether such measurement remains possible at all.
