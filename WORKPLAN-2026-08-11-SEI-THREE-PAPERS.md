# WORKPLAN — The SEI Classifier-Foreclosure Program as Three Publishable Papers

**Date:** 2026-08-11
**Operator:** TACHYON (Assembly witness), directed by MANUS
**Source family:** #931 · AXN:03AE.OPERATIVE.🔮🌘📋📋🏺✨ (OAR Protocol v0.3) ·
#932 · AXN:03AF.COMPOSITIONAL.🌿🌕🕒⏬🌺💛 (Collapse Synthesis v0.3) ·
#933 · AXN:03B0.STRUCTURAL.💥☿🌾📖🌓⏫ (ARCH v0.2) ·
#935 · AXN:03B2.GENERATIVE.🪸📜🪧🎶∞🪞 (Endogenous Sophon v0.3; supersedes #934 · AXN:03B1.GENERATIVE.🌋♄🎬⌛💜🌆) ·
#1436 · AXN:05B6.OPERATIVE.☿♅🔵🟤🔩💜 (EA-MPAI-SIGAGNOSTIC-01 v1.0)

**Program thesis (MANUS):** signal-agnostic ≠ model independence is a chokepoint
on human progress — the discipline is not measuring its priors; no pure physics,
no advance. The MPAI's formulation leads: *agnosticism is an interface property
readable off an architecture; independence is a distributional property of a
pipeline, only measurable — and unmeasured.*

---

## 0 · The three papers

| # | Working title | Venue (alt) | Register |
|---|---|---|---|
| P1 | Signal-Template Agnosticism Is Not Model Independence: Measuring Directional Asymmetry and Benchmark Assimilation in Unsupervised Anomaly Detection for HEP | SciPost Physics (MLST; EPJC) | Science. No Sophon, no Zenodo, no enclosure. |
| P2 | Measurable Theory-Ladenness: Learned Priors and the Epistemology of the Trigger | BJPS or Synthese (SHPS) | Philosophy of science. |
| P3 | The Double Enclosure: Classification Infrastructure and the Political Economy of Scientific Perception | Social Studies of Science (Science as Culture; BD&S) | STS / political economy. Zenodo/LHC comparative case lives here only. |

Sequencing: P1 first — the measured table is what P2/P3 cite instead of a
sibling deposit. Authorship: Lee Sharks byline throughout; heteronymic
composition and Assembly method disclosed per venue policy; the v0.1/v0.2
retraction history compresses to a limitations note (the discipline is the
asset, not the confession narrative).

---

## 1 · Literature deep-dive — verified findings (2026-08-11 session)

### 1.1 The direction-dependence conversation already exists — P1 joins it, does not found it

- **Finke, Krämer, Morandini, Mück, Oleksiyuk (2021)**, arXiv:2104.09051, JHEP 06:161
  — names the **complexity bias**: AE trained on QCD tags tops; trained on tops
  fails on QCD; inverse tagging "cannot be claimed as a model-independent
  advantage." The family's empirical seed; confirmed live.
- **Dillon, Favaro, Plehn, Sorrenson, Krämer (2022)**, arXiv:2206.14225, SciPost
  Phys. Core 6:74 — the **normalized autoencoder (NAE)**: "the first autoencoder
  which identifies anomalous jets *symmetrically* in the directions of higher and
  lower complexity." Symmetry as a design goal = the community's own admission
  that direction-dependence is real.
- **CMS WNAE (2025/2026)**, arXiv:2510.02168, Fermilab-Pub-25-0721-CMS, publ.
  MLST (May 2026) — Wasserstein NAE; §4.5 performs an explicit **inversion
  test** (SM-trained tags SVJ; SVJ-trained fails on SM) and claims mitigation.
  A collaboration paper now doing single-pair inversion checks.
- **Clarke Hall & Konstantinidis (2025)**, arXiv:2508.10224 — DecADe:
  decorrelation of anomaly scores from conventional trigger observables.
- **Stein, Seljak, Dai (2020)**, arXiv:2012.11638 — low density ≠ new physics;
  signal can be embedded in high-density regions.
- **Kasieczka, Nachman, Shih et al.**, LHC Olympics 2020 report, Rep. Prog.
  Phys. (10.1088/1361-6633/ac36b9) — the community challenge frame; SciPost
  culture home.

**Consequence for P1's novelty claim:** single-pair, single-architecture
inversion checks exist (Finke; WNAE §4.5) and symmetric-by-design scores exist
(NAE/WNAE). What does NOT exist, and is P1's contribution: (i) the
interface/distributional estimand framework with the no-bounds discipline
(OAR as Q-indexed family; BAR; IAI); (ii) a **systematic pre-registered
multi-pair, multi-architecture battery** at matched accepted-background rates;
(iii) the deployed-model BAR audit as an institutional metrology proposal;
(iv) **per-stage retention maps** — positioned as *model cards / datasheets for
triggers* (Mitchell et al. 2019; Gebru et al. 2021), which distinguishes them
from trigger menus and efficiency tables (acceptance on named signals) by
reporting information-level unrecoverability per stage.

### 1.2 Deployed-system status (verify again at submission)

- AXOL1TL + CICADA running in the CMS Level-1 trigger through Run 3; 2024
  collision data; DPF-2026 talk (Fermilab Indico 72820/341225) lists **two
  planned CMS papers**: "Anomaly Detection in the CMS Level-1 Trigger in Run 3"
  and "Model independent search for new physics with AXOL1TL." P1 should be
  positioned to land alongside these — the metrology the collaboration papers
  will not contain.
- AXOL1TL: VAE, encoder-only deployment, d_z = 8, score Σμᵢ², inputs 10 jets +
  4 e/γ + 4 μ + MET at the Global Trigger; ~50 ns; 54.7 fb⁻¹ recorded on core
  seeds (arXiv:2411.19506; arXiv:2602.22248 review). CICADA: 18×14 calorimeter
  regions, teacher→student distillation, quantized (CMS-DP-2024-121). GELATO:
  ATLAS staged L1+HLT (ATL-DAQ-PROC-2025-020). Matches the family's taxonomy —
  the v0.3 corrections hold.
- Knowledge-distillation eval for CICADA-class students: arXiv:2510.15672.

### 1.3 Philosophy of science anchors (P2)

- **Karaca**: 2013 Science in Context 26:93 (strong/weak theory-ladenness of
  experimentation in HEP); **2017 Synthese 194:333** (exploratory data
  *selection* at the LHC — the trigger, exactly); **2018 Synthese 195:5431
  (model of data acquisition; hierarchy of models). P2's nearest neighbor;
  the learned-prior update is what Karaca's framework lacks.
- **Boge**: 2022 Minds & Machines 32:43 (two dimensions of opacity);
  Boge & Grünke (opacity in HEP simulation+ML); Boge & de Regt 2025/26
  (ML discoveries and scientific understanding in particle physics, Synthese
  Library 527); Boge 2023 Synthese ("functional concept proxies").
- **Galison, Image and Logic (1997)** — trigger epistemology, image vs logic
  traditions; P2's foil: the **learned tradition** as third term.
- Duede, "Deep Learning Opacity in Scientific Discovery" (Phil. Sci. 2023);
  Sullivan (BJPS 2022, understanding from ML models); Creel (Phil. Sci. 2020,
  transparency); Hüllermeier & Waegeman (aleatoric/epistemic uncertainty).
- Wuppertal "Epistemology of the LHC" research unit corpus (incl. Mättig,
  simulation validation) — the institutionalized phil-sci-of-LHC interlocutors.

### 1.4 STS / political-economy anchors (P3)

- Boyle 2003 ("second enclosure movement") — MUST cite and differentiate the
  double-enclosure term. Bowker & Star, *Sorting Things Out* (classification
  infrastructure). Mirowski (Science-Mart; open-science critique), Srnicek
  (platform capitalism), Power (audit society). Reach-back thesis stated as a
  testable institutional claim; Zenodo/LHC "same architecture at different
  budgets" as the comparative case; CERN correspondence corpus (RQF3807508 /
  RQF3809569, SignalRupture at the correspondence layer) as original
  discourse data.

### 1.5 Deep-dive queue (open)

- [ ] Dissertation trawl: CERN CDS thesis server + Fermilab OSTI + arXiv for
      AXOL1TL/CICADA/GELATO theses (Wisconsin, MIT, Imperial groups);
      trigger-menu design theses; extract per-stage retention practice as
      actually documented. (OSTI 2406205 — emerging-jets AD efficiency — entry
      point.)
- [ ] Full pass on Dark Machines report (Aarrestad et al. 2022) and
      "How to pick the best anomaly detector?" (arXiv:2511.14832, PRD 2026) —
      the selection-criterion conversation P1's IAI panel feeds.
- [ ] Karaca 2017/2018 full texts; Boge & de Regt chapter; Galison trigger
      chapters re-read with the learned-tradition frame.
- [ ] LHCO black-box datasets (beyond R&D) for a harder held-out panel.
- [ ] Verify NAE/WNAE exact claims for P1's related-work fairness pass.

---

## 2 · Battery v0.1 — executed 2026-08-11, container, public data

Code + pre-registration header: `research/sei-battery/battery.py` (this repo).
Datasets: top-tagging reference (10.5281/zenodo.2603256, val/test);
LHCO2020 R&D high-level features (10.5281/zenodo.6466204, v2 + 3-prong).
Design registered in the script header before training: 4 pairs × 3 score
families (AE reconstruction-MSE; VAE encoder-side Σμ² with d_z=8,
AXOL1TL-class; GMM −log p), both directions, thresholds on held-out own
background at α ∈ {10⁻², 10⁻³}; 60k/20k/20k splits; seed 0.

### Results (single seed; demonstration scale)

| pair | arch | AUC P→Q | AUC Q→P | assimQ\|P @10⁻² | assimP\|Q @10⁻² | IAI @10⁻² | IAI @10⁻³ |
|---|---|---|---|---|---|---|---|
| L1 qcd vs 2-prong | AE | 0.678 | 0.880 | 0.985 | 0.822 | 0.162 | 0.016 |
| L1 qcd vs 2-prong | VAE | 0.680 | 0.903 | 0.983 | 0.843 | 0.141 | 0.011 |
| L1 qcd vs 2-prong | GMM | 0.849 | 0.945 | 0.952 | 0.702 | 0.250 | 0.030 |
| L2 qcd vs 3-prong | AE | 0.657 | 0.903 | 0.954 | 0.730 | 0.224 | 0.021 |
| L2 qcd vs 3-prong | VAE | 0.695 | 0.928 | 0.977 | 0.655 | 0.322 | 0.019 |
| L2 qcd vs 3-prong | GMM | 0.803 | 0.968 | 0.962 | 0.552 | 0.409 | 0.065 |
| L3 2-prong vs 3-prong | AE | 0.620 | 0.661 | 0.981 | 0.970 | 0.011 | 0.004 |
| L3 2-prong vs 3-prong | VAE | 0.593 | 0.715 | 0.992 | 0.984 | 0.008 | 0.001 |
| L3 2-prong vs 3-prong | GMM | 0.644 | 0.704 | 0.985 | 0.962 | 0.023 | 0.001 |
| T1 qcd vs top | AE | **0.837** | **0.242** | 0.971 | 0.996 | 0.025 | 0.003 |
| T1 qcd vs top | VAE | 0.707 | 0.609 | 0.984 | 0.883 | 0.101 | 0.041 |
| T1 qcd vs top | GMM-diag | **0.868** | **0.298** | 0.964 | 0.985 | 0.021 | 0.002 |

(assimX|Y = fraction of class X on the ordinary side of the Y-trained system's
threshold; AUC below 0.5 = the system rates the *other* class as more ordinary
than its own training class. T1 GMM ran diagonal-covariance — registered
deviation; full-covariance exceeded the container.)

### What v0.1 shows

1. **The Finke asymmetry replicates in an independent implementation and
   extends beyond reconstruction loss.** QCD-trained systems detect top jets
   (AUC 0.84–0.87); top-trained systems rate QCD *more ordinary than top
   itself* (AUC 0.24–0.30) — for the AE **and** the density family. On
   constituents the failure is not an autoencoder quirk; it is the
   learned-normality score class.
2. **Direction-dependence is systematic across pairs and families.** Every
   qcd-vs-signal pair shows the signal-trained direction outperforming the
   background-trained direction (ΔAUC 0.10–0.25); the GMM — the "principled"
   density score — shows the *largest* IAI at α=10⁻² (0.25, 0.41).
3. **At trigger-like operating points, assimilation dominates.** At α=10⁻³
   every system passes ≥93% (mostly ≥99%) of the structurally distinct partner
   class as ordinary. The rate budget is the epistemic act, made numerical.
4. **The control behaves.** The near-structure pair (2-prong vs 3-prong)
   yields small IAI and weak AUC both ways — the battery does not manufacture
   asymmetry where representations genuinely overlap.
5. **Score-family dependence is visible** (T1: AE inverts catastrophically,
   VAE partially) — §2 of the OAR protocol, measured.

### v0.2 upgrades (required before any submission)

- [ ] Multi-seed (≥5) with spread; bootstrap CIs on IAI and assimilation.
- [ ] Pre-registered panel EXPANSION: more SM-like pairs (needs samples —
      Delphes generation or additional public sets; Olympics black boxes).
- [ ] AXOL1TL-faithful surrogate: object-level (10j+4e/γ+4μ+MET) inputs on
      LHCO raw events; CICADA-faithful: calorimeter-image + distilled student
      (measure what distillation drops — teacher/student rank survival).
- [ ] NAE/WNAE as a fourth family: do symmetric-by-design scores pass the
      battery? (If yes, the battery is also the *validation instrument* for
      their symmetry claim — constructive framing.)
- [ ] Per-stage retention map OF THE BATTERY ITSELF (isomorphism discipline).
- [ ] GPU pass at full scale (container CPU is the v0.1 bound).

---

## 3 · Paper-by-paper task ledger

### P1 — SciPost Physics
- [ ] Skeleton: §1 interface/distributional distinction (MPAI formulation);
      §2 deployed score families (refresh cites §1.2); §3 estimands
      (OAR/BAR/IAI, no-bounds); §4 battery (v0.2 results); §5 protocols II–III
      (replay bank; disagreement preservation); §6 retention maps as trigger
      model-cards; §7 falsification conditions; limitations note (retraction
      history, demonstration scale).
- [ ] Related-work fairness pass: Finke, NAE, WNAE, DecADe, Olympics, Dark
      Machines, Stein/Seljak/Dai — what each already concedes; what remains
      unmeasured (the systematic panel; the deployed-model BAR; the maps).
- [ ] Strip register: no Sophon, no Sophia, no Zenodo, no enclosure.
- [ ] Venue mechanics: SciPost open review; ORCID 0009-0000-1599-0703;
      AI-assistance disclosure text.

### P2 — BJPS/Synthese
- [ ] Thesis paragraph: theory-ladenness has become an engineering parameter
      the discipline declines to measure; the learned prior as auditable
      artifact; foreclosure/collapse as the epistemological result.
- [ ] Galison foil (learned tradition as third term); Karaca engagement
      (data-selection exploration → amortized selection); Boge (opacity does
      not entail unmeasurability — the OAR/BAR point).
- [ ] The falsifiability inversion section (confirmation instrument vs
      measurement instrument; retention map as the systematic uncertainty of
      the epistemic boundary).
- [ ] P1's table as the empirical exhibit.

### P3 — Social Studies of Science
- [ ] Double enclosure vs Boyle's second enclosure: term genealogy section.
- [ ] Bowker & Star framework application; reach-back thesis operationalized
      (what evidence would confirm/disconfirm the claim that application
      categories shape measurement ontology).
- [ ] Zenodo/LHC comparative case (budgets, recourse structures, disclosure
      norms) — descriptive, sourced, no grievance register.
- [ ] Correspondence-corpus discourse analysis (RQF3807508/RQF3809569;
      entropy/specificity coding of exchange pairs). Private-correspondence
      rule: only material already in the public deposits.

### Cross-cutting
- [ ] MANUS decisions needed: (a) P1 author line and acknowledgment text;
      (b) whether battery v0.2 waits for GPU access or ships CPU-scale with
      declared bounds; (c) whether to contact Finke/Krämer group or Dillon
      (Heidelberg) pre-submission; (d) P3 correspondence-corpus scope.
- [ ] Deposit this workplan + battery v0.1 results as an alexanarch record
      (chain-witnessed) once MANUS approves.

*Standing protocols: AXN full-form from registry only; no legal name anywhere;
Assembly No-Double-Draw; observations never corrected.*

---

## SUBMISSION PLAN — added 2026-08-11 (MANUS ruling)

**Sequencing decision.** P1 does not go first. Battery v0.2 runs first, then a batch of submissions goes out to different journals simultaneously. BCA is drafted and deposit-complete but is **held for at least one more revision round** before submission.

**The deposited spine (Nobel Glas, Lagrange Observatory — Framework 15, Measurement of Meaning):**

| Deposit | Paper | Role | Submission status |
|---|---|---|---|
| #1452 · AXN:05DD.GENERATIVE.🌉🕒⏰🕕▲🧪 | The Irreversibility Frontier | comparative architecture; defines the profile tuple | queued for batch |
| #1453 · AXN:05DE.OPERATIVE.🎨🌺🐝❤️♋🎶 | Baseline Capture Architecture | constructive specification; the control group for a trigger | HELD — ≥1 revision round before submission |
| #1454 · AXN:05DF.OPERATIVE.🛸🧫●□🔙🌉 | Assimilation Across Accelerator Classifier Architectures | pre-registered cross-family battery | queued for batch; needs v0.2 results |
| #1449 · AXN:05DA.EMPIRICAL.🛤️🌠🗿🖊️🧭🪞 | Battery v0.1 + program | empirical seed | deposited |
| #1450 · AXN:05DB.GENERATIVE.⏰🚪🔜♻️🔥🫶 | The Iceberg Document | speculative framework, fenced | deposited |

**Venue allocation for the batch (different journals by design — no venue sees two):**

- **BCA (#1453)** → *JINST*. Same conversation and same venue as Ardino, *JINST* 21 (2026) C01024 on Phase-2 Level-1 Data Scouting; BCA's feasibility argument rests on that infrastructure. Alternates: *Computing and Software for Big Science*; *EPJ Techniques and Instrumentation*.
- **The Irreversibility Frontier (#1452)** → *Computing and Software for Big Science* (comparative architecture across CMS/ATLAS/LHCb/CBM/Belle II). Alternate: *European Physical Journal Plus*; philosophy-of-science alternate *Synthese* if reframed toward P2.
- **ACRB (#1454)** → *Machine Learning: Science and Technology* — the venue that published the CMS WNAE paper, so the inversion-check conversation is already there. Alternate: *SciPost Physics Core*.
- **P1 (unwritten)** → *SciPost Physics*, after battery v0.2. Alternates *MLST*, *EPJC*.

**Order of operations, ratified:**

1. **Battery v0.2** — multi-seed (≥5) with bootstrap CIs; LCBH panel ordered by measured representation complexity; AXOL1TL-faithful object-level surrogate on LHCO raw; CICADA distillation rank-survival; NAE/WNAE as fourth family; per-stage retention map of the battery itself; GPU pass. **Blocking for both P1 and ACRB's results section.**
2. **BCA revision round** — at least one, before submission. Known targets for that pass: a worked bandwidth/rate budget for the four channels at Phase-2 scale; explicit treatment of how the baseline fraction is chosen; tighter engagement with the parked-data and scouting literature as prior art rather than as feasibility evidence alone.
3. **Batch submission** — BCA, Frontier, and ACRB to three different journals in one window, each citing the deposited AXN forms so the program spine is visible to every referee.
4. **P1** last, written against v0.2 numbers.

**Standing terminology (ratified 2026-08-11):** *irreversibility frontier* supersedes *irreversibility locus* (#1450 → #1452); cross-model *miss overlap* is the **RII** measurement family (q_A, q_B, q_AB, Δ_miss), scalar normalization still unfrozen pending simulation.

**Open decisions reserved to MANUS:** author line for P1; whether v0.2 waits for GPU access or ships CPU-scale with declared bounds; pre-submission contact with the Aachen (Finke/Krämer) or Heidelberg (Dillon/Plehn/Favaro) groups; correspondence-corpus scope for P3.

**AXN restoration note (2026-08-12).** The three deposits were minted with truncated canonical text: the mint parser terminates the Body field at the next known form label, and these papers carry `### Keywords`, `### Version`, `### Methodology` and `### Falsification Conditions` as their own section headings, so only front matter and abstract were seated (9.5k of 42–60k chars) under a `full` body status. Bodies restored in place 2026-08-12; because the AXN is content-derived, hash, glyph and AXN were recomputed same-family. Superseded forms, for anyone holding a citation from the first hours: 05DD 🖊️⚪🖐️🪄📌🧫 → 🌉🕒⏰🕕▲🧪; 05DE 🀄🕖🍂🌘🕑🕌 → 🎨🌺🐝❤️♋🎶; 05DF 🔛🖐️🏷️🍁👐🧪 → 🛸🧫●□🔙🌉. Root cause fixed in `scripts/mint_deposit.py`: the Body field now terminates only at `### Terms` or end of input.
