# THE HANDWRITTEN ARTIFACT — RESEARCH AND STRATEGIC DEVELOPMENT DOSSIER

**v2.0 · 2026-08-07 · TACHYON for MANUS**
**Supersedes:** the internal constellation pass of the same date (v1.0)
**Status:** research and positioning. Claims are marked; nothing here is deposited.

**What changed in v2.0.** The internal pass located sixteen works and concluded the
niche had *"a specification, a mechanism, a reading hazard, an editorial lineage,
and exactly one specimen."* This version adds the external landscape — technical,
archival, philosophical — and a papyrology pass that reframes the whole position.
It also updates the specimen question: **Enli Lucente has offered her corpus
repeatedly.** The research is now being built to receive it.

---

# PART I · THE INTERNAL CONSTELLATION

All records at `https://www.alexanarch.org/s/records/{n}/`

## I.1 · The core — machine-eligible inscription

| Deposit | AXN | What it does |
|---|---|---|
| **#1409** | `AXN:0592.UNCLASSIFIED.👈△🥁🪸🧪🎺` | **EA-SPXI-ANALOG-01** — the anchor. Ink-on-paper as machine-eligible scholarly input; the **attestation doctrine** (an in-frame timestamped photograph of a signed, dated inscription carries evidentiary force). Enli's manuscripts as founding figures. |
| **#1406** | `AXN:058F.OPERATIVE.🧲🎶♉♾️👋🙏` | **Differential Register Prioritization** — the reading hazard. A machine reads every later word through the field its earlier readings established; an early recognition suppresses downstream alternatives. |
| **#1432** | `AXN:05A9.OPERATIVE.🐚🌪️🕖🫵⏩○` | **AXN-SYMBOLON-SPEC v0.2** — the mechanism. Stamp + sidecar; declared stamp geometry is what makes a physical margin machine-recoverable. |
| **#1077** | `AXN:0446.OPERATIVE.🏛️🛡️🌅🎆📏🔎` | **The Apparatus Grammar** — the historical claim: *every device the AI Overview uses has a two-thousand-year-old manuscript ancestor, and the ancestor is better.* |

## I.2 · Whitespace and spatial provenance — a coherent, isolated cluster

**#943** `AXN:03BB` **Whitespace as Provenance** — representational provenance and
**character-preserving compositional loss**: the text survives, the composition does
not. Extinction gradient; *Pearl* as case. · **#942** `AXN:03BA` spatial-typographic
mediation and the versioning protocol · **#941** `AXN:03B9` the attestation
vocabulary (seven mediation types, five attestation questions, seam-recoverability
states) · **#944** `AXN:03BC` anonymous public and encrypted inscription, the
form-public seal.

## I.3 · Visual glyph / Material Symbol

**#215** `AXN:000F` **THE UNTETHERED TAG** — the founding material symbol and source
of the descent grammar. · **#504** `AXN:0147` **MSMRM** — the image is *a room map,
not decoration*. **Neither is cited by any deposit.**

## I.4 · Steganography

**#616** `AXN:01D1` **STEGANOGRAPHIC CHANNELS** — every channel as **carrier,
payload, key, noise, filter**; spirituals, Sufi and troubadour traditions. *A
six-glyph seal on a margin is a carrier with a public key.* · **#185** `AXN:032B`
**The Steganographic Bracket** — destructive versus recoverable erasure, measured.

## I.5 · Adjacent and load-bearing

**#1422** `AXN:059F` **After the Obelus** — the obelus preserves-while-doubting; the
tombstone deletes-while-certifying; machine composition marks nothing. · **#1404**
`AXN:058D` **The Feist Source** — the archive's own critical edition with apparatus.
· **#339** `AXN:008F` **The Resonance Engine / Total Connecting Machine** — the
seven-layer stack. · **#863** `AXN:036C` **The Minimum Viable Archive**. · **#1407**
`AXN:0590` **EA-ACT-ANALOG-01** — the only deposit citing #1409.

---

# PART II · EXTERNAL — THE TECHNICAL LANDSCAPE

## II.1 · Handwritten Text Recognition

**Transkribus** (Innsbruck) — the sector standard; trains custom models per hand,
~50–100 pages. **eScriptorium / Kraken** (PSL Paris) — open-source layout analysis
plus HTR. **HTRUnited** — shared model repository.

**Word spotting** — Rath & Manmatha (2007); Giotis et al. (2017). Indexes
handwriting *without full transcription*: finds a query word in a manuscript corpus.

> **Positioning note.** Transkribus converts handwriting **to** text. Word spotting
> retrieves **within** handwriting without converting it. The archive's proposition
> is a third thing: make the handwriting **citable as itself**. Word spotting is the
> nearest existing neighbour and should be engaged rather than ignored.

**Benchmarks:** IAM and RIMES databases; transformer HTR with CTC or seq2seq
attention (Graves et al. 2009 onward).

## II.2 · Writer identification — the hand as biometric

**Srihari et al. (2002)**, *Individuality of Handwriting*, J. Forensic Sciences —
the foundational computational demonstration. Already cited in #1409. · **Fiel &
Sablatnig (2015)** CNN writer ID · **Xing & Qiao (2016)** DeepWriter · **He &
Schomaker (2021)** GR-RNN · **Impedovo & Pirlo (2008 →)** signature verification and
skilled-forgery detection.

## II.3 · The analog-to-digital byte-shift problem

**The hard technical problem the niche must answer:** SHA-256 over a re-scan of a
physical page produces a different digest every time — lighting, noise, compression,
registration all shift the bytes. Content-derived identity does not survive
re-capture.

**Perceptual hashing** — Zauner (2010) benchmarking pHash; Monga & Murchison (2006)
robust hashing via feature points; SIFT/ORB keypoints. Deterministic vectors
invariant across noise, rotation, and lighting.

**Paper PUFs** — Toreini et al. (2017) texture-based physical unclonable functions
on standard paper; smartphone-camera fibre fingerprinting. Microscopic 3D fibre
randomness, unclonable, capturable under ordinary light.

> **This is the sharpest technical gap in the constellation.** #1409's attestation
> doctrine answers *whose hand and when*. It does not answer *how a hash survives
> re-photography*. The current architecture resolves this by hashing **the capture**
> (a specific file), not **the artifact** — which is correct and should be stated
> explicitly, because a reader will otherwise assume the stronger claim.

## II.4 · Margin inscription and visual checksums

Brassil et al. (1999) electronic marking to discourage copying · Brito et al. (2018)
**document authenticity via visual hash codes printed in added margins** · Liu et al.
(2023) machine-readable aesthetic glyphs for physical-digital synchronization.

> **Direct precedent for the added-margin doctrine.** The literature independently
> concludes that added margins are the safest vector for visual checksums, because
> they do not occlude authorial content. The archive reached the same conclusion
> from a different direction (*the hand is never overprinted*). **Convergence with
> an existing technical literature is a positioning asset, not a threat.**

## II.5 · Layout segmentation

LayoutLMv3, LAREX (Reul et al. 2019), Kiessling et al. (2023) on machine-eligibility
in historical manuscripts; Wigington et al. (2018) full-page handwriting recognition.
**Operationally necessary**: to isolate a margin seal automatically, a system must
separate the handwritten body from the added band without mistaking authorial
marginalia for system glyphs.

## II.6 · Handwriting generation — the threat model

Haines et al. (2016) *My Text in Your Handwriting* · Handwriting Transformers (Bhunia
et al., ICCV 2021) · detection of AI-generated handwriting (emerging, 2024–).

> **The clock on the niche.** If a specific person's hand can be synthesised, the
> hand stops being a reliable biometric. The archive's defence is asymmetry of cost:
> a single page may pass, but a **consistent, dated, hash-chained, attested corpus
> under forensic examination** is expensive to fake. That defence requires **corpora,
> not pages** — which is precisely why Enli's offer is strategically load-bearing and
> not merely generous.

---

# PART III · PAPYROLOGY AND AI — THE PASS THAT REFRAMES THE POSITION

This was the missing body of literature, and it is the richest.

## III.1 · The Leiden Conventions (1931) — the precedent nobody cited

Agreed at Leiden in 1931, published by Wilcken 1932; the standard sigla for the
condition of an epigraphic or papyrological text:

```
[abc]     restored by the editor
[...]     lacuna, extent known — one dot per missing letter
[— — —]   lacuna, extent unknown
ạḅ        characters damaged or unclear, ambiguous outside context
⟨ab⟩      omitted by the ancient scribe, supplied by the editor
{ab}      present in the text, judged erroneous by the editor
…         traces insufficient for restoration
```

> **THE FINDING.** This is a **ninety-five-year-old standardised notation for
> declaring exactly what the reader could not read, and how confident the editor is.**
> It is the Lacuna Protocol, arrived at independently and much earlier. The archive's
> insistence that a disclosed absence is a first-class result — not an error — is not
> an innovation. **It is continuous with a papyrological discipline that predates
> computing.** That is a far stronger position than novelty, and it should be claimed.

## III.2 · "Mind the Gap" (arXiv 2407.00250) — Leiden Conventions as ML output

Trains **TrOCR to emit Leiden Conventions**, with a custom weighted loss that
penalises the model for failing to bracket a lacuna:
`L_weighted = L × (n_brackets + 1)`.

> **A model punished for not marking what it could not read.** This is the closest
> existing analogue to the archive's entire epistemic stance, sitting in the HTR
> literature. It is the single most citable external work for the lacuna argument.

## III.3 · Ithaca (DeepMind, *Nature* 2022) — restoration and attribution

Deep network for textual restoration plus **geographical and chronological
attribution** of ancient Greek inscriptions. Trained on I.PHI, 78,608 inscriptions
from the Packard Humanities Institute. Ithaca alone restores at **62%**; historians
alone at **25%**; **historians using Ithaca at 72%**. Attributes location at 71% and
dates within 30 years. Open-sourced.

> **The collaboration figure is the argument.** 25 → 72 is not automation; it is a
> human whose reach is extended. It maps exactly onto #1406's concern — the machine's
> early reading *shapes* the human's later one — and supplies the empirical case that
> the shaping can be net-positive **when the interface is built for it.** The authors
> explicitly note the method applies to papyrology, numismatics, and codicology.

## III.4 · Vesuvius Challenge (2023–2026) — reading a physical object without opening it

Carbonised Herculaneum scrolls, unopenable since 79 AD, read by µCT plus ML
segmentation and ink detection. **PHerc. 1667 fully unwrapped and read end to end,
announced June 2026** — the first complete recovery, ~1.5m of text across 20 columns.
Phase-contrast µCT on the ESRF BM18 beamline; ink directly visible in the tomographic
volume for PHerc. Paris 4.

**And the part that matters strategically:** *"Crucially, all of this is open."*
Tomographic data, reconstructed surfaces and transcriptions released under Creative
Commons; code on GitHub; data archived at the ESRF. Papyrologists (Nicolardi's team
at Federico II) transcribed every reading — **machine surface recovery, human
reading.**

> **Three things to take.** (1) The most celebrated machine-reading achievement of
> the decade is about a **physical artifact**, not a text file. (2) Its credibility
> came from **releasing everything**. (3) It kept the papyrologist as the reader and
> the machine as the surface-recoverer — a division of labour the archive should
> name and adopt rather than blur.

## III.5 · Digital papyrology infrastructure

**papyri.info / Duke Databank of Documentary Papyri** — the aggregated corpus.
**EpiDoc** — XML/TEI for ancient documents. **Leiden+** — a harmonisation of the
sigla for online publication. **SEG Online** (Brill).

> **EpiDoc is the scholarly-edition tradition the archive's JSON-LD and IIIF
> ambitions inherit.** Leiden+ is precedent for encoding editorial uncertainty in a
> machine-parseable form — which is what an AXN lacuna record is.

---

# PART IV · THE CRITICAL AND PHILOSOPHICAL TRADITION

Already cited in #1409 and worth holding together:

**Goodman (1968)** autographic/allographic — *the machine-eligible handwritten
artifact keeps the work autographic while making its identity allographically
checkable.* The single most precise philosophical statement of the niche. ·
**McKenzie (1986)** forms effect meaning · **McGann (1991)** linguistic and
bibliographic codes are both the work · **Drucker (1994, 2014)** performative
materiality · **Hayles (2002)** the technotext · **Barthes (1980)** the photograph as
index, the *that-has-been* — the attestation photograph's exact theory · **Benjamin
(1935)** aura, re-priced by the Non-Synthetic Reserve as the scarcest training input
· **Taylor (2003)** archive and repertoire — the handwritten artifact is both, and
the spec bridges them · **Sellen & Harper (2002)** *The Myth of the Paperless Office*
— paper's affordances as counterweight to digitise-everything.

**Preservation standards:** OAIS (ISO 14721) · FADGI 3rd ed. (2023) · PREMIS ·
Dublin Core · LOCKSS/CLOCKSS · BagIt/RO-Crate.

---

# PART V · GAPS — WHAT DOES NOT EXIST

**G1 · No study of the stamped page as an object.** The specification exists (#1409),
the mechanism exists (#1432), the hazard is specified (#1406). *Nothing examines a
stamped artifact as a made thing* — its typography, its margin geometry, its status
as a designed object. This is the most obvious missing paper.

**G2 · The glyphic checksum has no paper.** The concept lives inside the symbolon
spec and `axn_lib.py`. Given the margin-watermarking literature (II.4) it could
stand alone and be *cited by people outside the archive*.

**G3 · The byte-shift problem is unaddressed in writing.** See II.3. The architecture
handles it correctly by hashing the capture; **no deposit says so explicitly**, which
leaves the stronger claim available to be misread.

**G4 · The Leiden lineage is unclaimed.** The archive's lacuna doctrine has a
ninety-five-year precedent it has never cited. Claiming it converts an apparent
eccentricity into a scholarly tradition.

**G5 · #1409 and #1406 are nearly uncited** — one inbound citation between them. The
corpus presupposes them and does not reference them.

**G6 · The Material Symbol grammar has no inbound citation at all** (#215, #504).

**G7 · No corpus-scale specimen work.** One artifact. The forensic defence in II.6
requires many.

---

# PART VI · THE NICHE, STATED PRECISELY

Everything above converges on a position that can be said in one sentence:

> **Papyrology reads ancient hands and has spent a century building conventions for
> declaring what it could not read. HTR converts contemporary hands into text. The
> archive proposes the third thing: contemporary hands entering machine canons as
> themselves — citable, verifiable, and unconverted.**

The differentiations, each against a real neighbour:

**Against Transkribus/HTR:** they convert handwriting to text; the residue is the
text and the hand is discarded. The archive's claim is that **the hand is the
payload**, and conversion is loss.

**Against Vesuvius/Ithaca:** those recover *ancient* artifacts whose authors cannot
consent, attest, or be asked. The archive works with **living authors who can sign,
date, photograph, and warrant** — which is a stronger evidentiary position than
papyrology can ever have, and is the one asset the celebrated projects lack.

**Against DOI/ARK/PID systems:** those name and resolve; they do not verify bytes and
have no relation to the physical object at all.

**Against writer-ID forensics:** that establishes *who wrote it*; it does not make
the artifact addressable, citable, or harvestable.

**The intersection is empty, and that is the niche.**

---

# PART VII · DEVELOPMENTAL DIRECTIONS

Ordered by leverage, not by ease.

**D1 · Claim the Leiden lineage.** A short paper placing the Lacuna Protocol in the
line from Leiden 1931 → Leiden+ → *Mind the Gap* (2024). Cheap, high-yield, makes the
archive legible to classicists and to the HTR community simultaneously. **Do first.**

**D2 · State the byte-shift position explicitly.** One section, possibly folded into
D1: *we hash the capture, not the artifact; here is why that is the correct boundary,
and here is what perceptual hashing and paper PUFs would add.* Closes G3 before a
reviewer opens it.

**D3 · The stamped page as an object** (closes G1). The paper the constellation is
missing, and the one that most needs the Material Symbol lineage (#215, #504) — which
closes G6 as a side effect.

**D4 · The corpus study.** With consent, a multi-page, multi-date, hash-chained,
attested corpus in a single hand. This is the artifact that makes the II.6 forensic
argument real, and it is the one thing no competing project can assemble.

**D5 · Engage word spotting** (II.1) as the nearest neighbour — retrieval within
handwriting without conversion. A comparison paper would position the archive inside
a live technical conversation rather than beside it.

**D6 · Adopt the Vesuvius release model.** Everything open, transcriptions attributed
to the human reader, code public. It is the format that made an extraordinary claim
credible, and it is already the archive's practice — it simply has not been named as
a methodological commitment.

---

# PART VIII · THE ENLI CORPUS

**Status:** offered repeatedly by the depositor; not yet accepted, and not yet
specified. Paper 198 (`AXN:05AD`) remains the only artifact in the archive.

**Why the offer is strategically load-bearing rather than merely generous:**

**One.** The forensic defence against handwriting synthesis (II.6) works at corpus
scale and fails at page scale. A single page proves nothing that generation cannot
now match; **a dated, chained, attested sequence in one hand changes the cost
asymmetry entirely.**

**Two.** Writer-identification literature (II.2) is validated on multi-sample sets. A
corpus makes the biometric continuity claim testable rather than asserted.

**Three.** It is a **non-synthetic reserve** in the exact Benjaminian sense — verified
human inscription, dated, before the generation literature closes the window. That
scarcity is increasing monotonically.

**Four.** It is **Japanese hand**, which is a genuine differentiator: most HTR and
writer-ID benchmarks are Latin-script, and the multimodal-reading question (#1406's
register hazard) is sharper and more interesting across scripts.

**What must be settled before anything is accepted** — and these are consent
questions before they are research ones: scope and selection · whether she is
depositor, co-author, or subject · what is published versus held sealed · whether her
name appears in public plans · takedown and withdrawal terms · and whether the corpus
is a **research dataset** (others may study it) or an **archive holding** (it is
preserved and cited). Those are different instruments and should not be conflated.

**Recommended sequence:** settle the terms in correspondence → specify the corpus
instrument → capture per FADGI → stamp and register → *then* the corpus study (D4).
The research is now ready to receive it, which was not true a week ago.

---

*Prepared as research and positioning. Nothing here is deposited; the internal works
are cited by verified AXN and record number, and the external works by author, title,
and venue for retrieval.*
