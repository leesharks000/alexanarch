# Capture records with a blog candidate, found by index

Produced by `scripts/index_blog.py --find-missing` against a complete index of all
2,809 posts. **Nothing here is a finding.** Each line is a post to open and read —
the score nominates, and only reading confirms.

The index exists because every prior pass GUESSED a URL from a deposit title and
scored one fetch against a threshold. #1272's correct URL sat unread in the queue's
own `candidate_blog_urls` field; #1287's correct post was fetched and rejected at 0.43.

```
searching 2,809 indexed posts for 92 capture records

  #951    0.85  EA-MANDALA-02 v1.0: MANDALA: Systema Magiae 
         -> https://mindcontrolpoems.blogspot.com/2026/07/the-87-orphans-unmatched-tombstoned.html
  #952    0.85  EA-MANDALA-03 v1.0: ΜΑΝΔΑΛΑ: ΤΟ ΣΥΣΤΗΜΑ ΤΗΣ 
         -> https://mindcontrolpoems.blogspot.com/2026/07/the-87-orphans-unmatched-tombstoned.html
  #953    0.85  EA-MANDALA-04 v1.0: المَنْدَلَة: نِظَامُ الس
         -> https://mindcontrolpoems.blogspot.com/2026/07/the-87-orphans-unmatched-tombstoned.html
  #954    0.85  EA-MANDALA-06 v1.0: המנדלה: מערכת הקסם הרקור
         -> https://mindcontrolpoems.blogspot.com/2026/07/the-87-orphans-unmatched-tombstoned.html
  #955    0.85  EA-MANDALA-07 v1.0: मण्डलम्: पुनरावर्तक-माया
         -> https://mindcontrolpoems.blogspot.com/2026/07/the-87-orphans-unmatched-tombstoned.html
  #974    0.78  SPXI.dev — Protocol Specification Landing Pa
         -> https://mindcontrolpoems.blogspot.com/2026/04/ea-spxi-01-spxi-formal-specification.html
  #1001   0.73  The Crimson Hexagonal Archive Hugging Face D
         -> https://mindcontrolpoems.blogspot.com/2026/05/crimson-hexagonal-archive-hugging-face.html
  #1003   0.75  AI-Native Intellectual Biography: Genre, Pro
         -> https://mindcontrolpoems.blogspot.com/2026/05/ai-native-intellectual-biography-new.html
  #1030   0.70  KADEEZY — "The Crossed The Line Run": Comput
         -> https://mindcontrolpoems.blogspot.com/2026/06/hexagonal-contributor-license-kadeezy.html
  #1034   0.80  The Feist Function: Algorithmic Instructions
         -> https://mindcontrolpoems.blogspot.com/2026/06/ea-feist-voice-transform-01-feist.html
  #1036   0.79  Visual Schema Dataset v0.1: 174 Prose Schema
         -> https://mindcontrolpoems.blogspot.com/2026/07/the-87-orphans-unmatched-tombstoned.html
  #1222   0.73  Encyclotron Audit: Basecamp (37signals) — A 
         -> https://mindcontrolpoems.blogspot.com/2026/04/compression-diagnostics-measuring-what.html
  #1224   0.85  Article IX — Adjudication and Repair Protoco
         -> https://mindcontrolpoems.blogspot.com/2026/05/article-ix-adjudication-and-repair.html
  #1226   0.85  The Josephus Thesis Is Not the Piso Hypothes
         -> https://mindcontrolpoems.blogspot.com/2026/06/ea-mpai-josephus-01-v10-metadata-packet.html
  #1232   0.71  Sémantique Potentielle — Release 4: Model Co
         -> https://mindcontrolpoems.blogspot.com/2026/06/semantique-potentielle-release-4-model.html
  #1241   0.83  H_core Formal Specification v1.8.0 — Complet
         -> https://mindcontrolpoems.blogspot.com/2026/03/symbolon-architecture-epistemic-field.html
  #1246   0.73  The Feist Function: Algorithmic Instructions
         -> https://mindcontrolpoems.blogspot.com/2026/06/ea-feist-voice-transform-01-feist.html
  #1269   0.85  Crimson Hexagon: LIBERATORY OPERATOR SET: Te
         -> https://mindcontrolpoems.blogspot.com/2026/05/cross-reference-map-master-index-of.html
  #1273   1.00  THE FLICKER: Notes Toward a Lyric Theory
         -> https://mindcontrolpoems.blogspot.com/2025/11/the-flicker-notes-toward-lyric-theory.html
  #1274   0.86  Visual Schema // Crimson Hexagon Navigation 
         -> https://mindcontrolpoems.blogspot.com/2026/03/symbolon-architecture-epistemic-field.html
  #1276   1.00  Canonical Closure Notice: Sevenfold Witness 
         -> https://mindcontrolpoems.blogspot.com/2026/01/canonical-closure-notice-sevenfold.html
  #1278   0.85  The Epistle Triptych: Seed Text, Heteronym P
         -> https://mindcontrolpoems.blogspot.com/2026/01/integrity-lock-certificate-epistle.html
  #1280   0.70  The Afterlife Archive: Recovered Documents f
         -> https://mindcontrolpoems.blogspot.com/2025/12/crimson-hexagon-invoice-leak-as-poem-ii.html
  #1283   0.71  Crimson Hexagon Vendor Ops / Procurement Rec
         -> https://mindcontrolpoems.blogspot.com/2025/12/crimson-hexagon-invoice-leak-as-poem-ii.html
  #1285   1.00  Mandala Oracle — Operational Protocol
         -> https://mindcontrolpoems.blogspot.com/2025/12/mandala-oracle-operational-protocol.html
  #1288   0.85  MRA Incident Report — Poem Classifier Interv
         -> https://mindcontrolpoems.blogspot.com/2025/12/ctiwound-incident-report-mandala-oracle.html
  #1289   0.85  Status Report — Boundary Deletion and Identi
         -> https://mindcontrolpoems.blogspot.com/2025/12/status-report-research-division.html
  #1290   1.00  The Mirror-Corgi: Notes on What We Call AI H
         -> https://mindcontrolpoems.blogspot.com/2025/12/the-mirror-corgi-notes-on-what-we-call.html
  #1291   0.85  The Mirror-Corgi, Revisited — Boundary Gramm
         -> https://mindcontrolpoems.blogspot.com/2025/12/the-mirror-corgi-revisited.html
  #1292   1.00  Companion Artifacts: The Forensic Trinity
         -> https://mindcontrolpoems.blogspot.com/2025/12/companion-artifacts-forensic-trinity.html
  #1296   1.00  THE THREE-BODY GENESIS (Meta-Deposit)
         -> https://mindcontrolpoems.blogspot.com/2026/01/zenodo-packet-three-body-genesis-meta.html
  #1297   0.85  Document 206 The Non-Indexed Perfective: Thr
         -> https://mindcontrolpoems.blogspot.com/2026/02/phase-x-navigation-map-interdimensional.html
  #1298   0.73  Document 206b The Non-Indexed Perfective: Ve
         -> https://mindcontrolpoems.blogspot.com/2026/02/the-non-indexed-perfective-citational.html
  #1299   0.73  Document 206c The Non-Indexed Perfective: Ve
         -> https://mindcontrolpoems.blogspot.com/2026/02/the-non-indexed-perfective-citational_1.html
  #1300   0.85  INFINITY ENOUGH Capstone Deposit
         -> https://mindcontrolpoems.blogspot.com/2026/02/the-thumb-formal-operators-for-phase-x.html
  #1304   0.85  PHASE X NAVIGATION MAP (Document 210)
         -> https://mindcontrolpoems.blogspot.com/2026/05/the-google-critique-navigational-map.html
  #1306   1.00  The Infinite Bliss — Institutional Provenanc
         -> https://mindcontrolpoems.blogspot.com/2026/02/the-infinite-bliss-institutional.html
  #1307   0.76  METADATA PACKET: Document 206a The Non-Index
         -> https://mindcontrolpoems.blogspot.com/2026/01/zenodo-triptych-packet.html
  #1313   0.85  SEMANTIC COLLAPSE AS COMEDY Document 222
         -> https://mindcontrolpoems.blogspot.com/2026/02/semantic-collapse-as-comedy-analytical.html
  #1315   0.85  Document 238: THE CONFORMANCE MODULE — Logot
         -> https://mindcontrolpoems.blogspot.com/2026/02/logotic-programming-module-11.html
  #1316   0.85  Document 239: THE TELEMETRY MODULE — Logotic
         -> https://mindcontrolpoems.blogspot.com/2026/02/logotic-programming-module-10.html
  #1318   0.83  The Flood and the Vessel: Semantic Preservat
         -> https://mindcontrolpoems.blogspot.com/2026/02/the-flood-and-vessel-semantic.html
  #1319   1.00  LP v1.2 — The Epistemic Ledger
         -> https://mindcontrolpoems.blogspot.com/2026/02/logotic-programming-module-12-epistemic.html
  #1320   1.00  "The Unmade Sign: Toward a Semiotic Theory o
         -> https://mindcontrolpoems.blogspot.com/2026/02/visual-schema-unmade-sign-under.html
  #1325   1.00  THE MACRO-MAQUETTE: SEED
         -> https://mindcontrolpoems.blogspot.com/2026/02/the-macro-maquette-seed-author-lee.html
  #1328   0.70  Architectural Distinction Note: On the Relat
         -> https://mindcontrolpoems.blogspot.com/2026/03/symbolon-architecture-epistemic-field.html
  #1331   0.85  🌑⬡ THE LUNAR ARM EA-ARK-EMOJI-01-SHADOW: Ope
         -> https://mindcontrolpoems.blogspot.com/2026/03/crimson-hexagon-space-ark-glyphic.html
  #1332   0.85  Crimson Hexagon: 🌑⬡ THE LUNAR ARM EA-ARK-EMO
         -> https://mindcontrolpoems.blogspot.com/2026/03/crimson-hexagon-space-ark-glyphic.html
  #1333   0.85  Crimson Hexagon: EA-ARK-ASCII-01: The Space 
         -> https://mindcontrolpoems.blogspot.com/2026/03/ea-ark-01-v425-ascii-spatial-transform.html
  #1335   1.00  Companion Artifacts — Forensic Recovery Set
         -> https://mindcontrolpoems.blogspot.com/2025/12/companion-artifacts-forensic-recovery.html
  #1339   0.70  Crimson Hexagon: EA-ARK-01-FRACTION v2.1 The
         -> https://mindcontrolpoems.blogspot.com/2026/03/symbolon-architecture-epistemic-field.html
  #1349   0.76  Gravity Well: Suffusion Map — Room-by-Room F
         -> https://mindcontrolpoems.blogspot.com/2026/05/r29-imploding-velcro-nativity-room.html
  #1363   0.76  The 3:60 Room — Room Specification and Contr
         -> https://mindcontrolpoems.blogspot.com/2026/05/skiouros-pyrophthalmos-and-sciurid.html
  #1367   0.70  Crystallization of Substrate: Structural Int
         -> https://mindcontrolpoems.blogspot.com/2026/05/ea-spxi-15-crystallization-of-substrate.html
  #1368   0.85  CTI_WOUND: Google AI Overview Total Liquidat
         -> https://mindcontrolpoems.blogspot.com/2026/03/ctiwoundgoogleaiototalliquidation202603.html
  #1369   1.00  Provenance Is What Authorship Must Endure: A
         -> https://mindcontrolpoems.blogspot.com/2026/05/documentid-ea-mpai-provenance-02-title.html
  #1375   0.82  TL;DR:011 — THE BASIN HOLDS: Bing AI Search 
         -> https://mindcontrolpoems.blogspot.com/2026/03/symbolon-architecture-epistemic-field.html
  #1379   0.74  Overview Watch: Comprehensive Development Pl
         -> https://mindcontrolpoems.blogspot.com/2026/04/overview-watch-comprehensive.html
  #1387   0.78  The Basin Holds: External Stabilization of t
         -> https://mindcontrolpoems.blogspot.com/2026/03/symbolon-architecture-epistemic-field.html
  #1399   1.00  OKF Summarization-Governance Proposal: prove
         -> https://mindcontrolpoems.blogspot.com/2026/06/proposal-optional-summarization.html
  #1402   0.71  OKF Summarization-Governance Proposal: prove
         -> https://mindcontrolpoems.blogspot.com/2026/07/ea-correspondence-okf-01-v10-predicted.html

61 of 92 capture records have a strong blog candidate.
None is a finding. Each is a post to open and read.
```