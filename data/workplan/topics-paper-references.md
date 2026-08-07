# MACHINE-ELIGIBLE HANDWRITTEN ARTIFACTS — REFERENCES
## Companion apparatus to the topics paper (v2.0)

**2026-08-07 · TACHYON for MANUS**

**Why this exists separately, and why its absence was a real failure.** The topics
paper cited by author, title and venue and supplied **no retrieval path for any
external source**. A paper arguing that citations must resolve, and whose subject is
the erosion of resolvable reference, cannot itself be unretrievable. The research had
been done; the addresses were discarded in the writing. That is the exact failure mode
the archive exists to document, committed internally.

**Read-status is marked on every entry**, because a survey that does not distinguish
what was read from what was described is not a survey:

- **[R]** — read in substance during this pass (full text or substantial extract)
- **[S]** — secondary description only; located and summarised, **primary text not
  read**. Must be confirmed before any claim resting on it is deposited or submitted.
- **[A]** — archive-internal; verified against the registry at 1,437 deposits.

---

## §1 · PAPYROLOGY, EPIGRAPHY, AND EDITORIAL CONVENTION

**[S] Bagnall, Roger S., ed.** *The Oxford Handbook of Papyrology.* Oxford University
Press. — https://academic.oup.com/edited-volume/34530
*Priority read before drafting. The field's standard orientation.*

**[R] Wilcken, Ulrich.** "Das Leydener Klammersystem." *Archiv für Papyrusforschung*
10 (1932), 211–212. — the founding publication of the Leiden Conventions, agreed at
the XVIIIe Congrès International des Orientalistes, Leiden, 7–12 September 1931.

**[S] Dow, Sterling.** *Conventions in Editing: A Suggested Reformulation of the
Leiden System.* Greek, Roman and Byzantine Monographs 2 (1969). —
https://dokumen.pub/conventions-in-editing-a-suggested-reformulation-of-the-leiden-system.html

**[R] Leiden Conventions** — sigla reference and variant practice.
https://en.wikipedia.org/wiki/Leiden_Conventions ·
https://saxa-loquuntur.web.rug.nl/sigla-numerals-abbreviations/ ·
**Leiden+** harmonisation for digital publication:
https://scholarlyeditions.brill.com/sego/standards/

**[S] papyri.info / Duke Databank of Documentary Papyri** — Papyrological Navigator
and Papyrological Editor; the Leiden+ editorial pipeline in production.
https://papyri.info/

**[S] Trismegistos** — interdisciplinary ancient-text metadata platform.
Identifier policy: https://www.trismegistos.org/about_how_to_cite.php ·
Data standards and writing-surface reuse:
https://www.trismegistos.org/about_datastandards.php
*Priority read. The unit-of-identification precedent.*

**[S] EpiDoc** — TEI XML for ancient documents, including physical description.
https://epidoc.stoa.org/

**[S] TEI Guidelines**, `<facsimile>`, `<surface>`, `<zone>`. https://tei-c.org/

**[S] CITE Architecture / Canonical Text Services.**
https://cite-architecture.github.io/ · **Homer Multitext:**
https://www.homermultitext.org/

**[S] Reggiani, Nicola, ed.** *Digital Papyrology III: The Digital Critical Edition of
Greek Papyri.* — located via the digital-papyrology literature.

**[S] HTR-United** — Zenon papyri ground-truth dataset. https://htr-united.github.io/

---

## §2 · MACHINE READING OF ANCIENT AND HISTORICAL TEXT

**[R] Assael, Yannis, Thea Sommerschield, et al.** "Restoring and attributing ancient
texts using deep neural networks." *Nature* 603 (2022), 280–283.
**DOI: 10.1038/s41586-022-04448-z** — https://www.nature.com/articles/s41586-022-04448-z ·
PubMed: https://pubmed.ncbi.nlm.nih.gov/35264762/ ·
PMC: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8907065/ ·
Code: https://github.com/google-deepmind/ithaca · Interface: https://ithaca.deepmind.com
*Restoration 62% model / 25% historians / 72% together; attribution 71%; dating ±30
years. Trained on I.PHI, 78,608 inscriptions.*

**[R] "Mind the Gap: Analyzing Lacunae with Transformer-Based Transcription."**
arXiv:2407.00250. — https://arxiv.org/pdf/2407.00250
*TrOCR trained to emit Leiden Conventions; weighted loss L × (n_brackets + 1).*

**[R] Vesuvius Challenge** — complete virtual unwrapping and reading of PHerc. 1667,
announced 25 June 2026.
Preprint: **arXiv:2606.29085** — https://arxiv.org/html/2606.29085v1 ·
Project: https://scrollprize.org/ · Method: https://scrollprize.org/unwrapping ·
Result: https://scrollprize.org/firstscroll · **Open data:** https://scrollprize.org/data ·
University of Kentucky announcement:
https://uknow.uky.edu/research/day-herculaneum-scrolls-began-speaking-again
*Phase-contrast µCT, ESRF BM18. PHerc. 1667 had a prior readability score of zero.*

**[S] "A computational platform for the virtual unfolding of Herculaneum Papyri."**
*Scientific Reports.* — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7813886/

**[S] "Deciphering scrolls with tomography: A training experiment."**
arXiv:2504.11485 — https://arxiv.org/pdf/2504.11485

---

## §3 · HANDWRITTEN TEXT RECOGNITION AND LAYOUT

**[S] Transkribus** (READ-COOP / University of Innsbruck).
https://www.transkribus.org/ · HTR overview:
https://www.transkribus.org/what-is-handwritten-text-recognition

**[S] eScriptorium / Kraken** (PSL, Paris) — layout analysis and HTR pipeline.

**[S] PAGE XML** and **[S] ALTO** (Library of Congress) — layout-grounded
transcription interchange. https://www.loc.gov/standards/alto/

**[S] Rath, T. M., and R. Manmatha.** "Word spotting for historical documents."
*IJDAR* 9 (2007), 139–152.

**[S] Giotis, Angelos P., et al.** "A survey of document image word spotting
techniques." *Pattern Recognition* 68 (2017), 310–332.

**[S] Reul, Christian, et al.** "LAREX: A semi-automatic open-source tool for layout
analysis and region extraction on early printed books." *IJDAR* (2019).

**[S] Wigington, Curtis, et al.** "Start, Follow, Read: End-to-End Full-Page
Handwriting Recognition." *ECCV* 2018.

**[S] Graves, Alex, et al.** "A Novel Connectionist System for Unconstrained
Handwriting Recognition." *IEEE TPAMI* 31:5 (2009). — the CTC baseline; IAM and RIMES
as standard benchmarks.

---

## §4 · WRITER IDENTIFICATION AND HANDWRITING SYNTHESIS

**[S] Srihari, Sargur N., Sung-Hyuk Cha, Hina Arora, Sangjik Lee.** "Individuality of
Handwriting." *Journal of Forensic Sciences* 47:4 (2002), 856–872.
*1,500-writer stratified sample; macro and micro features; produced amid Daubert
challenges to handwriting expertise.*

**[S] Fiel, Stefan, and Robert Sablatnig.** "Writer Identification and Retrieval Using
a Convolutional Neural Network." *CAIP* 2015.

**[S] Xing, Linjie, and Yu Qiao.** "DeepWriter: A Multi-Stream Deep CNN for
Text-independent Writer Identification." *ICFHR* 2016.

**[S] He, Sheng, and Lambert Schomaker.** "GR-RNN: Global-context residual recurrent
neural networks for writer identification." *Pattern Recognition* 117 (2021).

**[S] Impedovo, Donato, and Giuseppe Pirlo.** "Automatic Signature Verification: The
State of the Art." *IEEE Transactions on Systems, Man, and Cybernetics* 38:5 (2008).

**[S] Haines, Tom S. F., Oisin Mac Aodha, Gabriel J. Brostow.** "My Text in Your
Handwriting." *ACM Transactions on Graphics* 35:3 (2016).

**[S] Bhunia, Ankan Kumar, et al.** "Handwriting Transformers." *ICCV* 2021.

---

## §5 · PHYSICAL IDENTITY, PERCEPTUAL HASHING, WATERMARKING

**[S] Toreini, Ehsan, Siamak F. Shahandashti, Feng Hao.** "Texture to the Rescue:
Practical Paper Fingerprinting based on Texture Patterns." *ACM Transactions on
Privacy and Security* 20:3 (2017). — arXiv: https://arxiv.org/abs/1705.02510
*The paper PUF primitive. Priority read for §4.3 of the paper.*

**[S] Zauner, Christoph.** *Implementation and Benchmarking of Perceptual Image Hash
Functions.* MSc thesis, Upper Austria University of Applied Sciences (2010). — pHash.

**[S] Monga, Vishal, and Brian L. Evans.** "Perceptual Image Hashing Via Feature
Points: Performance Evaluation and Tradeoffs." *IEEE Transactions on Image Processing*
15:11 (2006). *NB — the topics paper v1.0/v2.0 cites this as "Monga & Murchison";
the second author is Evans. **Correct before submission.***

**[S] Brassil, Jack T., Steven Low, Nicholas F. Maxemchuk.** "Copyright Protection for
the Electronic Distribution of Text Documents." *Proceedings of the IEEE* 87:7 (1999).

**[S] Brito, et al.** "Document authenticity verification via visual hash codes printed
in added margins." *Journal of Imaging* (2018). — *citation located through secondary
description; exact author list and volume to confirm.*

**[S] Liu, et al.** "Machine-Readable Aesthetic Glyphs for Physical-Digital
Synchronization." *IEEE T-PAMI* (2023). — *located through secondary description;
confirm before citing.*

---

## §6 · CULTURAL-HERITAGE MODELLING AND DIGITISATION

**[S] CIDOC Conceptual Reference Model.** https://cidoc-crm.org/
**[S] CRMdig** — provenance of digitisation products. https://cidoc-crm.org/crmdig
*Priority read. The capture-as-event ontology.*

**[S] W3C PROV-O: The PROV Ontology.** W3C Recommendation.
https://www.w3.org/TR/prov-o/

**[S] W3C Web Annotation Data Model.** https://www.w3.org/TR/annotation-model/

**[S] IIIF Presentation API** and **Image API.** https://iiif.io/api/

**[S] METS** (Metadata Encoding and Transmission Standard), Library of Congress.
https://www.loc.gov/standards/mets/

**[S] PREMIS** preservation metadata, Library of Congress.
https://www.loc.gov/standards/premis/

**[S] IFLA Library Reference Model** and **ISBD for Manifestation.**

**[S] Centre for Manuscript Genetics**, University of Antwerp — *critique génétique*
and the *avant-texte*.

**[S] FADGI**, *Technical Guidelines for Digitizing Cultural Heritage Materials*, 3rd
ed. (2023). https://www.digitizationguidelines.gov/

**[S] OAIS** — Reference Model for an Open Archival Information System, ISO 14721.

---

## §7 · ARCHIVAL AUTHENTICITY AND TIMESTAMPING

**[S] InterPARES.** https://www.interpares.org/ ·
InterPARES 1: https://www.interpares.org/ip1/ip1_index ·
**Authenticity Task Force documents:** https://www.interpares.org/ip1/ip1_documents/atf
*Priority read. Source of the verifiable-exact-capture / authenticity distinction
adopted throughout the paper.*

**[R] RFC 3161** — Internet X.509 PKI Time-Stamp Protocol (TSP).
https://www.rfc-editor.org/rfc/rfc3161

**[S] ARCHANGEL** — "Underscoring archival authenticity with blockchain technology."
*UKSG Insights* 32 (2019). — https://insights.uksg.org/articles/10.1629/uksg.470

**[S] Duranti, Luciana**, and the diplomatics lineage from Mabillon, *De re
diplomatica* (1681).

---

## §8 · CONTENT PROVENANCE AND HUMAN-CHECKABLE FINGERPRINTS

**[S] C2PA** — Coalition for Content Provenance and Authenticity. https://c2pa.org/
**[S]** "Cryptographic Provenance and AI-generated Images." AI Collaboratory (2025). —
https://ai-collaboratory.net/wp-content/uploads/2025/11/S13212_7356.pdf
*Source of the trust-model limitations quoted in §6.1: validation not required by the
specification; signature coverage of the entire file not required; "trusted does not
necessarily imply trustworthy."*

**[S] Azimpourkivi, Mozhgan, et al.** — visual key fingerprints and the limits of human
visual discrimination. *USENIX Security* 2020. —
https://www.usenix.org/conference/usenixsecurity20/presentation/azimpourkivi
*Priority read. Prescribes the empirical programme for the glyph seal.*

**[S] OpenSSH randomart** — `ssh-keygen(1)`. https://man.openbsd.org/ssh-keygen

**[R] RFC 2289** — A One-Time Password System (word-based short authentication
strings). https://www.rfc-editor.org/rfc/rfc2289

**[S] Blockchain Commons.** "Provenance Marks: An Innovative Approach for Authenticity
Verification." BCR-2025-001. —
https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2025-001-provenance-mark.md

**[S] Dual-Fingerprint Identity Primitive (DFIP)**, Artifact Virtual (2026). —
https://huggingface.co/amuzetnoM/project-emergent/blob/main/papers/biometric-blockchain-provenance.md

---

## §9 · UNICODE AND TRANSMISSION INTEGRITY

**[R] Unicode Standard Annex #15** — Unicode Normalization Forms.
https://www.unicode.org/reports/tr15/

**[R] Unicode Technical Standard #51** — Unicode Emoji (presentation sequences,
variation selectors, ZWJ). https://www.unicode.org/reports/tr51/

*Together these establish the seal-transmission risk in §6.3: compatibility
normalisation can erase distinctions, and emoji presentation depends on variation
selectors and platform font coverage.*

---

## §10 · PERSISTENT IDENTIFIERS

**[R] DOI Handbook.** https://www.doi.org/doi-handbook/html/ · ISO 26324.
**[R] ARK Alliance** — ARK overview. https://arks.org/about/ark-overview/
**[R] RFC 8141** — Uniform Resource Names (URN).
https://www.rfc-editor.org/rfc/rfc8141.html
**[R] SWHID** — specification and ISO/IEC 18670:2025.
https://www.swhid.org/specification/v1.0/1.Scope/ · https://www.swhid.org/publications/
**[R] IPFS Content Identifiers.** https://docs.ipfs.tech/concepts/content-addressing/
**[S] PURL**, OCLC. https://www.oclc.org/research/areas/data-science/purl.html
**[S] Klein, Martin, et al.** "Scholarly Context Not Found: One in Five Articles
Suffers from Reference Rot." *PLOS ONE* 9:12 (2014). **DOI: 10.1371/journal.pone.0115253**
**[R] RFC 8493** — BagIt File Packaging Format.
https://www.rfc-editor.org/rfc/rfc8493 · **[S] RO-Crate** https://www.researchobject.org/ro-crate/ ·
**[S] Oxford Common File Layout** https://ocfl.io/ ·
**[S] ResourceSync** ANSI/NISO Z39.99-2017 ·
**[S] FAIR Signposting** https://signposting.org/ ·
**[R] RFC 7089** — Memento. https://www.rfc-editor.org/info/rfc7089/

---

## §11 · THEORY AND CRITICISM

**[S] Goodman, Nelson.** *Languages of Art: An Approach to a Theory of Symbols.*
Bobbs-Merrill, 1968. — esp. II.3–4, autographic/allographic.
**[S] McKenzie, D. F.** *Bibliography and the Sociology of Texts.* Panizzi Lectures
1985; Cambridge UP, 1986/1999.
**[S] McGann, Jerome.** *The Textual Condition.* Princeton UP, 1991.
**[S] Drucker, Johanna.** *The Visible Word: Experimental Typography and Modern Art,
1909–1923.* Chicago, 1994. · *Graphesis: Visual Forms of Knowledge Production.*
Harvard, 2014.
**[S] Hayles, N. Katherine.** *Writing Machines.* MIT Press, 2002.
**[S] Barthes, Roland.** *La chambre claire: Note sur la photographie.* Gallimard,
1980. (*Camera Lucida*, trans. Howard, 1981.)
**[S] Benjamin, Walter.** "Das Kunstwerk im Zeitalter seiner technischen
Reproduzierbarkeit" (1935–36).
**[S] Taylor, Diana.** *The Archive and the Repertoire: Performing Cultural Memory in
the Americas.* Duke UP, 2003.
**[S] Sellen, Abigail J., and Richard H. R. Harper.** *The Myth of the Paperless
Office.* MIT Press, 2002.

---

## §12 · ARCHIVE-INTERNAL SOURCES

All **[A]**; verified against the registry at 1,437 deposits. Records resolve at
`https://www.alexanarch.org/s/records/{n}/`

| # | AXN | Short title |
|---|---|---|
| 1409 | `AXN:0592.UNCLASSIFIED.👈△🥁🪸🧪🎺` | EA-SPXI-ANALOG-01 — Machine-Eligible Handwritten Artifacts |
| 1406 | `AXN:058F.OPERATIVE.🧲🎶♉♾️👋🙏` | Differential Register Prioritization |
| 1432 | `AXN:05A9.OPERATIVE.🐚🌪️🕖🫵⏩○` | AXN-SYMBOLON-SPEC v0.2 |
| 1077 | `AXN:0446.OPERATIVE.🏛️🛡️🌅🎆📏🔎` | EA-APPARATUS-01 — The Apparatus Grammar |
| 1404 | `AXN:058D.UNCLASSIFIED.📐🛸△👐♉🧫` | The Feist Source — critical edition |
| 943 | `AXN:03BB.GENERATIVE.🐚💎🪄💡🌙🚪` | Whitespace as Provenance |
| 942 | `AXN:03BA.OPERATIVE.♅🛤️🕗🧊🍃☉` | EA-PROVENANCE-METADATA-01 v0.2 |
| 941 | `AXN:03B9.OPERATIVE.👇🍄🏰⊗🌕💚` | EA-PROVENANCE-METADATA-01 v0.1 |
| 944 | `AXN:03BC.OPERATIVE.🕙🕚🌆🀄🔺♦️` | EA-MANDALA-INSCRIPTION-01 |
| 548 | `AXN:0179.ARCHIVAL.🔽🟠🌺🗿🎲📦` | EA-ARK-01 · ASCII Spatial Transform v0.2 |
| 1333 | `AXN:0546.UNCLASSIFIED.⏏️🍂↘️⭕🌾🔵` | EA-ARK-ASCII-01 — Space Ark |
| 29 | `AXN:0191.GOVERNANCE.🐚🟣○🌪️🎲🔀` | The Inaugural Ark — Visual Compression |
| 1330 | `AXN:0543.UNCLASSIFIED.↘️🔗🌈📝🎬♅` | EA-ARK-EMOJI-01 — Glyphic Checksum / Emoji Transform |
| 1331 | `AXN:0544.UNCLASSIFIED.⏰🖐️👐♉⚫□` | The Lunar Arm — operator/shadow transform |
| 1332 | `AXN:0545.UNCLASSIFIED.🌋👋🌈↙️👁️🍃` | The Lunar Arm (Crimson Hexagon) |
| 215 | `AXN:000F.EMPIRICAL.🏠🌳🌉⭐▲🎲` | Material Symbol — The Untethered Tag |
| 504 | `AXN:0147.GOVERNANCE.🔐🔃🔃🤲➗♅` | Visual Schema — MSMRM |
| 127 | `AXN:02B2.GOVERNANCE.🎶🔀🧪🧲⚙️🔴` | Inscriptions That Survive the Tokenizer — SPXI-TLP v2.2 |
| 186 | `AXN:032C.GOVERNANCE.⊗🫵🏔️❌▽🚨` | Who Is Writing for the Machines? |
| 89 | `AXN:0260.GOVERNANCE.🌲🕙☁️🕔●🔜` | Crystallization of Substrate |
| 1367 | `AXN:0568.UNCLASSIFIED.🎨↙️🌹👈🔐🏁` | Crystallization of Substrate — structural integration |
| 616 | `AXN:01D1.GOVERNANCE.⊗🖐️↙️♌⚪🗿` | Steganographic Channels |
| 185 | `AXN:032B.EMPIRICAL.✋🤝☀️🌠🛤️🔼` | The Steganographic Bracket |
| 1422 | `AXN:059F.GENERATIVE.🗝️🤝🚨⏰∮🔧` | After the Obelus |
| 339 | `AXN:008F.GENERATIVE.☿💜⚙️🫵🤲❤️` | The Resonance Engine — Total Connecting Machine |
| 863 | `AXN:036C.STRUCTURAL.📦⊕🎪⛵🌀↖` | The Minimum Viable Archive |
| 1407 | `AXN:0590.GOVERNANCE.💜🗡️🔃🔓🪄` | EA-ACT-ANALOG-01 — The Effective Act |
| 1437 | `AXN:05B7.OPERATIVE.♦️🌌📌🦅🌑💜` | DOI Alternatives Are Complementary Infrastructures |
| 1436 | `AXN:05B6.OPERATIVE.☿♅🔵🟤🔩💜` | Signal-Template Agnosticism Is Not Model Independence |

**Referenced in the internal passes, not located as deposits — TO RESOLVE:**
*"The Hand and the Act"* · *"Five Ways a Citation Fails"* · **UMBML v0.5, hex
`02.UMB.CHECKSUM`, DOI `10.5281/zenodo.18452132`** (severed; body recoverable from
mindcontrolpoems.blogspot.com).

---

## §13 · STATUS SUMMARY AND WHAT THIS MEANS FOR THE PAPER

**Read in substance [R]:** 17 · **Secondary description only [S]:** 58 ·
**Archive-internal, verified [A]:** 29.

**The honest reading of that ratio.** Roughly three-quarters of the external
literature has been *located and characterised*, not *read*. The topics paper is
therefore a **survey of the field's shape**, and its per-source analyses of what each
work establishes, assumes and cannot do are — for the [S] entries — inferences from
abstracts, documentation, and secondary description.

That is a legitimate stage. It is not a literature review, and the paper should not
be presented as one until the priority reads are done.

**Priority reads before drafting**, in order: Trismegistos identifier policy · CRMdig ·
InterPARES Authenticity Task Force · the USENIX visual-fingerprint study · UAX #15 and
UTS #51 · Toreini et al. on paper PUFs · Bagnall's *Handbook*.

**Known citation defect to fix before submission:** Monga & **Evans**, not Monga &
Murchison (§5).
