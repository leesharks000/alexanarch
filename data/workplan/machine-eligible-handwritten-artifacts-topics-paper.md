# MACHINE-ELIGIBLE HANDWRITTEN ARTIFACTS
## A Topics Paper: The Literature, Its Limits, and the Space for an Evidentiary Identifier

**2026-08-07 · prepared by TACHYON for MANUS · v1.0**
**Function:** field survey and problem statement in advance of a dissertation-scale
project. Organised by **the question each literature answers**, not by discipline.
Internal works cited by verified AXN and record number; external works by author,
title, and venue.

**Convention used throughout.** Each source receives three things: what it
**establishes** (its actual finding, not its ambition), what it **assumes** (the
conditions under which the finding holds), and what it **cannot do** (the boundary
its own method sets). The third is the operative one — the developmental space is
made of other people's boundaries.

---

## §0 · THE PROBLEM

A handwritten page is an object whose identity is constituted by its history of
production. A digital file is an object whose identity is constituted by its bytes.
Between them sits a photograph, which is neither: it is a *new* object, produced at a
particular moment under particular light, and no two photographs of the same page
share a digest.

The question this project takes up is narrow and, as far as the surveyed literature
shows, unaddressed:

> **Under what conditions can a handwritten artifact enter a machine-readable
> scholarly record as itself — cited, verified, and reasoned about — without being
> converted into text, and without its identity depending on the continued goodwill
> of any institution?**

Four established literatures each answer part of this and stop. **Handwritten text
recognition** makes the writing legible by discarding the hand. **Papyrology** has a
century of discipline for reading damaged inscription and declaring uncertainty, but
works on authors who cannot be consulted. **Content provenance** attests what a
device captured, on the authority of the device's manufacturer. **Persistent
identifier infrastructure** names and resolves, and touches neither bytes nor
objects.

The gap is not that these fields have failed. It is that **none of them was built for
a living author who wants a physical page to be citable by machines a century from
now.**

---

# PART I · THE LEGIBILITY QUESTION
### *What must be true for a machine to read a hand?*

## §1.1 · Handwritten Text Recognition as a converting technology

**Transkribus** (READ-COOP, University of Innsbruck) and **eScriptorium/Kraken**
(PSL, Paris) are the field's working infrastructure. Both take page images, perform
layout analysis, and produce transcription; both train per-hand models, typically on
50–100 annotated pages.

**Establishes.** That unconstrained historical handwriting is transcribable at
scholarly usable accuracy given per-hand training, and that the training cost is
bounded and known. This is not a small result — it is the reason large manuscript
collections are now searchable at all.

**Assumes.** That the *desired output is text*. Every architectural decision follows
from this: layout analysis exists to find lines to transcribe; models are scored on
character error rate; ground truth is a string.

**Cannot do.** Preserve the hand as evidence. After a successful HTR pass, what
persists in the scholarly record is a character stream and, if the project is
diligent, a link back to a page image. **The transcription is what gets cited; the
image is what gets stored.** The hand becomes a provenance footnote to its own text.

**Developmental space.** The archive's proposition inverts the output: the hand *is*
the payload, and conversion is loss. This is not a criticism of HTR — it is a
different objective, and it should be stated as such rather than as a correction.
Notably, HTR gives the project something valuable for free: a **legibility floor**.
If a page's text can be recovered by standard HTR, then the artifact is
machine-*readable*; the project's claim is about machine-*eligibility*, which is a
further and separable property. Distinguishing these two cleanly is a contribution
available immediately.

## §1.2 · Word spotting — the nearest neighbour, and the most instructive

**Rath & Manmatha (2007)**, *Word Spotting for Historical Documents*, IJDAR;
**Giotis et al. (2017)**, *A Survey on Word Spotting in Handwritten Documents*,
Pattern Recognition.

**Establishes.** That handwritten corpora can be made *retrievable* without being
transcribed. Word images are clustered by visual similarity; a query returns
occurrences across a corpus. Retrieval accuracy is usable even where transcription
accuracy would not be.

**Assumes.** That retrieval is the goal, and that a user knows roughly what they are
looking for.

**Cannot do.** Support citation. A word-spotting hit is a location in an image; it is
not an addressable, quotable, verifiable unit that a third party can independently
confirm.

**Developmental space.** This is the most important neighbour in the survey because
it **already accepts the project's core premise** — that handwriting can be operated
on without being converted — and then declines to take the further step. The
literature has established that *retrieval without conversion* works. Nobody has
asked whether *citation without conversion* can work. That is a precisely bounded,
defensible dissertation question, and word spotting is the shoulder it stands on.

## §1.3 · Layout analysis and the margin-isolation problem

**Reul et al. (2019)**, LAREX, IJDAR; **Wigington et al. (2018)**, *Start, Follow,
Read*, ECCV; **Kiessling et al. (2023)** on machine-eligibility in historical
manuscripts; LayoutLMv3 as the current general model.

**Establishes.** Reliable segmentation of complex page geometry — main text blocks,
marginalia, interlinear insertions, strikethroughs — including on degraded material.

**Assumes.** That page regions have consistent visual and positional signatures.

**Cannot do.** Distinguish *authorial* marginalia from *systemic* marginalia. A model
trained to find marginal notes will find an added identifier band, because both are
marginal marks.

**Developmental space.** This is a live operational risk for the added-margin
doctrine, and it has a testable form: **does an off-the-shelf layout model classify a
stamp band as authorial marginalia?** If yes, the band's geometry must be made
distinguishable — which is a design constraint on the seal, discoverable by
experiment rather than assertion. This is one of the cheapest empirical contributions
available.

---

# PART II · THE UNCERTAINTY QUESTION
### *How does a reader declare what could not be read?*

This is where the papyrological literature reframes the entire project.

## §2.1 · The Leiden Conventions (1931) — an epistemic contract, not a notation

Agreed at the University of Leiden in 1931 by the papyrological section of the XVIIIe
Congrès International des Orientalistes; published by **Wilcken, "Das Leydener
Klammersystem," *Archiv für Papyrusforschung* 10 (1932), 211–212**; reformulated by
**Sterling Dow, *Conventions in Editing* (1969)**; harmonised for digital publication
as **Leiden+**.

The core sigla:

| Siglum | Meaning |
|---|---|
| `[abc]` | letters lost from the original, **restored by the editor** |
| `[...]` | lacuna of known extent — one dot per missing letter |
| `[— — —]` | lacuna of **unknown** extent |
| `ạḅ` | characters **damaged or unclear**, ambiguous outside context |
| `⟨ab⟩` | omitted in error by the ancient scribe, **supplied by the editor** |
| `{ab}` | present in the text, judged **erroneous and superfluous** by the editor |
| `…` | traces on the surface, **insufficient for restoration** |

**Establishes.** That editorial uncertainty is not one thing. These sigla encode at
least **five distinct epistemic acts**, and the distinctions are load-bearing:

1. *I cannot see it, and I know how much is missing.* (`[...]`)
2. *I cannot see it, and I do not know how much is missing.* (`[— — —]`)
3. *I cannot see it, and I am supplying it by inference.* (`[abc]`)
4. *I can see something, and I am unsure what it is.* (`ạḅ`)
5. *I can see it clearly, and I believe the original is wrong.* (`{ab}`, `⟨ab⟩`)

The fifth is remarkable: a convention for recording that the **source** erred, kept
distinct from recording that the **reader** is uncertain.

**Assumes.** A human editor with the authority to make and own these judgments, and a
reader competent to interpret the marks.

**Cannot do.** Travel. The sigla are a print convention. They do not survive
tokenisation, they are not machine-parseable without a grammar, and they carry no
mechanism for verifying that a given transcription corresponds to a given artifact.

**Developmental space — and this is the paper's central finding.** The archive's
Lacuna Protocol holds that a disclosed absence is a first-class result rather than an
error. That doctrine has **a ninety-five-year-old precedent it has never cited**, and
the precedent is *more granular than the doctrine*. The archive currently has
approximately one lacuna type. Leiden has five, and the distinction between
*extent-known* and *extent-unknown* alone is a specification upgrade available for the
cost of adopting it.

The stronger move is positional rather than technical: claiming this lineage
converts what reads as an eccentric insistence on marking absence into **continuity
with the editorial tradition of classical philology.** For a dissertation, that is the
difference between a novel claim requiring defence and an inherited discipline
requiring extension.

## §2.2 · "Mind the Gap" (2024) — teaching a model to mark what it cannot read

**arXiv 2407.00250**, *Analyzing Lacunae with Transformer-Based Transcription*.
Trains TrOCR on line images with Leiden-annotated ground truth, using a weighted loss:

```
L_weighted = L × (n_brackets + 1)
```

where `n_brackets` counts square-bracket occurrences in the ground truth.

**Establishes.** That a transcription model can be trained to *emit* editorial
uncertainty markers, and that doing so requires deliberately reweighting the
objective. Only 15% of the training data carried lacuna annotations; the weighting
compensates.

**Assumes.** Ground truth annotated by editors who applied the conventions
consistently.

**Cannot do.** Distinguish *why* the lacuna exists — physical damage, illegibility,
occlusion, or the model's own incapacity all collapse into the same bracket.

**Developmental space.** The loss function is the finding. By multiplying loss by
bracket count, the model is **taught that marking absence matters more than
transcribing presence** — an inversion of the standard OCR objective, which
penalises every character error equally and therefore rewards confident guessing.
This is the clearest existing technical statement of the archive's epistemic stance,
and it exists in the HTR literature rather than in philosophy.

The extension the project can make: **the missing distinction between damage and
incapacity.** A machine reading an artifact should be able to say *this is illegible
because the page is torn* versus *this is illegible to me*. Leiden distinguishes
these for humans (`…` traces versus `[...]` lacuna); no model does. That is a
specifiable, testable contribution.

## §2.3 · Ithaca (2022) — the collaboration figure and what actually produced it

**Assael, Sommerschield et al., "Restoring and attributing ancient texts using deep
neural networks," *Nature* 603 (2022), 280–283.** Trained on **I.PHI**, 78,608
inscriptions derived from the Packard Humanities Institute corpus.

The headline results: restoration **62%** accuracy for the model alone; historians
alone **25%**; **historians working with Ithaca, 72%**. Geographical attribution 71%;
chronological attribution within ~30 years of ground-truth ranges.

**Establishes.** That machine assistance can more than double expert performance on a
task requiring deep contextual judgment — and, in the authors' redating of key
Athenian texts, that the assistance can move substantive historical debates.

**Assumes.** A large, clean, machine-actionable corpus. I.PHI required an extended
ruleset to normalise 84 regions and wildly heterogeneous date formats. **The dataset
construction is the hidden achievement**, and it took as much discipline as the model.

**Cannot do.** Operate without that corpus. Ithaca is a model of a *well-documented
epigraphic tradition*; it cannot be pointed at an idiosyncratic hand with no
comparanda.

**Developmental space — read carefully, this is not "AI helps."** The 25→72 gain did
not come from accuracy; the model alone scores 62, below the collaborative figure.
It came from **interface design**: Ithaca returns ranked top-20 hypotheses with
saliency, not a verdict. The historian evaluates alternatives rather than accepting
an answer.

This bears directly on the archive's own **Differential Register Prioritization**
(`#1406`, `AXN:058F`), which specifies the hazard that a machine's early reading
suppresses later interpretive fields. Ithaca is the empirical case that **the hazard
is a property of single-verdict interfaces, not of machine reading as such**, and
that ranked-alternative presentation is the mitigation. That is a citable external
validation of an internal specification, and it converts #1406 from a warning into a
design requirement with evidence behind it.

## §2.4 · Vesuvius Challenge (2023–2026) — and the readability score of zero

**PHerc. 1667**, sealed since 79 AD, **virtually unwrapped and read end to end,
announced 25 June 2026** — approximately 1.5 m of surface across 20 columns. Method:
high-resolution phase-contrast µCT on the ESRF **BM18** beamline, computational
unrolling, ML ink detection. For **PHerc. Paris 4**, ink is directly visible in the
tomographic volume and segmentable in three dimensions rather than inferred from a
surface fit.

**Establishes.** That a physical object can be read without being opened, and that
the pipeline — segmentation, meshing, flattening, ink detection — is tractable
though not yet fully automatable. Sheet-switching remains the characteristic failure.

**Assumes.** Synchrotron access, and papyrologists to read the recovered surface.

**Cannot do.** Attribute, consent, or ask. The authors of the Herculaneum library
are unavailable in a way no method resolves.

**Developmental space — two findings, one of them larger than the project.**

**First, the readability score.** PHerc. 1667 had been physically opened and damaged
in the 1980s, and was assigned a readability score of **zero**. Federica Nicolardi's
statement on the result — that with virtual unwrapping *"we can follow sustained
arguments across multiple columns"* — is a statement about instruments, not about
objects. **"Unreadable" was a property of the available method, and the object was
reclassified when the method changed.** For an archive whose founding injury is the
classification of scholarly deposits as out-of-scope, this is a precise and
transferable proposition: *classifications of unreadability are claims about readers.*

**Second, the release model.** Tomographic data, reconstructed surfaces and
transcriptions released under Creative Commons; code on GitHub; data archived at the
ESRF. The credibility of an extraordinary claim was manufactured by making it
checkable. And the division of labour is explicit and worth adopting as doctrine:
**the machine recovers the surface; the papyrologist reads it.** The transcriptions
are attributed to named human readers.

## §2.5 · The infrastructure: papyri.info, EpiDoc, Leiden+

**papyri.info** (Duke Databank of Documentary Papyri) aggregates the corpus;
**EpiDoc** provides XML/TEI encoding for ancient documents; **Leiden+** harmonises the
sigla for online publication.

**Establishes.** That editorial uncertainty *can* be encoded machine-parseably, at
corpus scale, with community governance — and has been for over a decade.

**Cannot do.** Verify. EpiDoc encodes an edition; it does not bind the edition to the
artifact by any computable relation.

**Developmental space.** This is the closest existing model for what an AXN lacuna
record should look like, and it supplies a ready answer to the question *why not just
use TEI?* — because TEI describes and does not verify, and the project's claim is
about verification. Stating the complementarity precisely is more useful than
inventing a parallel vocabulary.

---

# PART III · THE IDENTITY QUESTION
### *How does an artifact's identity survive re-capture?*

This is the project's hardest technical problem and its least written-about.

## §3.1 · The byte-shift problem, stated

A cryptographic digest is a function of exact bytes. Two photographs of one page —
different light, angle, sensor noise, compression — produce unrelated digests. A
content-derived identifier computed over a capture therefore identifies **that
capture**, not the artifact.

This is not a flaw to be engineered away. It is the correct behaviour of a hash. But
it means a claim of the form *"the identifier is derived from the work"* requires
precision about **which work**: the physical page, or a specific photograph of it.

**The archive's current architecture hashes the capture.** That is right. It is also,
as far as the internal survey found, **nowhere stated in writing** — which leaves the
stronger and false reading available.

## §3.2 · Perceptual hashing — robust, and not an identity function

**Zauner (2010)**, *Implementation and Benchmarking of Perceptual Image Hash
Functions* (pHash); **Monga & Murchison (2006)**, *Robust Image Hashing via Feature
Points*, IEEE TIP; SIFT and ORB keypoint descriptors.

**Establishes.** That deterministic, compact descriptors can be computed which remain
stable across noise, rotation, scale, lighting and moderate compression — the
transformations that defeat cryptographic hashing.

**Assumes.** That "same image" is a similarity judgment with a threshold.

**Cannot do.** Serve as a security boundary. Perceptual hashes have non-trivial
false-accept rates, particularly for documents, which are visually homogeneous —
white field, dark strokes, similar layout. Two different pages in the same hand may
be perceptually closer than two captures of one page under different light.

**Developmental space.** The correct architecture is two-layer and should be stated
as such: **the perceptual hash is a retrieval aid; the cryptographic kernel is the
identity.** A perceptual descriptor lets a holder ask *is this probably the artifact
in record #N?*; the cryptographic kernel lets them ask *is this exactly the capture
of record #N?* Conflating them would import the false-accept rate into the identity
claim, which would be fatal. Keeping them separate is a contribution in itself, since
the surveyed provenance literature routinely blurs it.

## §3.3 · Paper PUFs — the primitive that would identify the artifact

**Toreini, Shahandashti & Hao (2017)**, *Texture to the Rescue: Practical Paper
Fingerprinting based on Texture Patterns*, ACM TOPS; and the smartphone-camera
fingerprinting line that follows it.

**Establishes.** That ordinary paper carries a physically unclonable fingerprint —
the three-dimensional random arrangement of its fibres, visible as translucency
patterns under transmissive light — and that it can be captured with commodity
hardware and matched reliably.

**Assumes.** Controlled capture geometry and lighting, and an enrollment step where
the artifact is registered while in hand.

**Cannot do.** Work retrospectively. A page that was never enrolled cannot be
fingerprinted from an existing photograph, because the required lighting is
transmissive and the required resolution is high.

**Developmental space — this is the missing primitive.** A paper PUF identifies **the
physical sheet**; a cryptographic kernel identifies **a capture of it**. Together
they close the gap the project currently states honestly and cannot yet bridge: they
would allow the claim *this is the same physical page*, not merely *this is the same
photograph*.

The enrollment constraint is what makes this **research rather than engineering**,
and it is also what makes a living-author corpus uniquely suited to it: **the pages
are in hand and can be enrolled at inscription time.** No historical collection can
say that. This is, on the survey's evidence, the single most promising unexploited
technical direction, and it is available only to a project working with a
contemporary author.

## §3.4 · Margin watermarking — independent arrival at the added-margin doctrine

**Brassil, Low & Maxemchuk (1999)**, *Copyright Protection for the Electronic
Distribution of Text Documents*, Proc. IEEE; **Brito et al. (2018)** on visual hash
codes printed in added margins, *Journal of Imaging*; **Liu et al. (2023)**,
machine-readable aesthetic glyphs for physical-digital synchronisation.

**Establishes.** That verification data can be printed into page margins without
occluding content, and recovered by mobile sensors; and that spatial layout
invariants govern whether such marks survive re-capture.

**Cannot do.** Address the author's own claim. These systems mark documents on behalf
of a distributor to detect copying; the mark is imposed, not declared.

**Developmental space.** The convergence is the point. This literature reached the
added-margin conclusion from anti-piracy motivations; the archive reached it from a
doctrine that *the hand is never overprinted*. **Independent arrival at the same
design constraint from opposed motivations is evidence the constraint is real**, and
it should be cited rather than treated as competition. The remaining differentiation
is who the mark serves: a distributor tracking leakage, or an author asserting
identity.

---

# PART IV · THE AUTHORSHIP QUESTION
### *Whose hand is it, and for how much longer will that be answerable?*

## §4.1 · Writer identification — established, and scale-dependent

**Srihari, Cha, Arora & Lee (2002)**, *Individuality of Handwriting*, Journal of
Forensic Sciences — produced in the context of *Daubert* challenges to the
admissibility of handwriting expertise, using a sample stratified across 1,500
writers, with macro features (slant, spacing, line separation) and micro features
(character-level shape).

**Establishes.** That handwriting is individuating at a statistically demonstrable
level, and that automated systems can attribute samples to writers with high accuracy
— which was, at the time, a legal question as much as a technical one.

**Assumes.** Sufficient sample. Accuracy is a function of how much writing is
available, and degrades sharply on short samples.

**Cannot do.** Attribute a single short inscription with forensic confidence.

**Later work** — **Fiel & Sablatnig (2015)** CNN writer identification; **Xing & Qiao
(2016)** DeepWriter; **He & Schomaker (2021)** GR-RNN — extends this to deep features
and cross-script settings, improving robustness while preserving the same
scale-dependence.

**Developmental space.** The scale-dependence is the strategic fact. **The archive's
biometric continuity claim — that the hand checks against itself, page over page,
year over year — is exactly the regime in which this literature is strongest, and it
is inaccessible with one specimen.** A corpus does not merely provide more data; it
moves the claim from the weakest part of the evidence base to the strongest.

## §4.2 · Handwriting generation — the clock

**Haines, Mac Aodha & Brostow (2016)**, *My Text in Your Handwriting*, ACM TOG —
synthesises arbitrary text in a target individual's hand from a modest sample.
**Bhunia et al. (2021)**, *Handwriting Transformers*, ICCV — transformer-based joint
style and content modelling. Detection of machine-generated handwriting is an
emerging area (2024–) with no mature methods.

**Establishes.** That a specific person's hand can be synthesised convincingly from
limited exemplars, and that quality is improving.

**Cannot do.** Reproduce a *history*. Generation produces plausible pages; it does not
produce a dated, attested, hash-chained sequence with consistent material substrate
and consistent physical enrollment.

**Developmental space — this is why the project is time-sensitive.** If the hand can
be synthesised, the hand alone stops being a warrant. The defence available is not
better detection but **cost asymmetry**: a single page may pass any test, while a
corpus that is dated, sequentially chained, attested at capture, and enrolled at the
paper level is expensive to fabricate in a way that scales badly for an adversary.

Two consequences follow, and both are structural rather than rhetorical. **The
project must work at corpus scale or its central warrant fails.** And the value of
verified non-synthetic human inscription increases monotonically as generation
improves — which is Benjamin's aura, re-priced by scarcity rather than by
uniqueness.

---

# PART V · THE PROVENANCE QUESTION
### *Who asserts that this is what it claims to be?*

## §5.1 · C2PA — the incumbent, and the most important comparison

The **Coalition for Content Provenance and Authenticity**: Adobe, Microsoft, Meta,
Google, Sony, Leica, Samsung; 6,000+ member organisations; the emerging industry
standard, now appearing in camera firmware and editing software. Its structure is a
**Manifest** containing assertions about an asset, a **Claim** (a digitally signed,
tamper-evident data structure), and a **Claim Signature**.

**Establishes.** That an unbroken chain of edits and captures can be cryptographically
signed at each step, and that the resulting record is tamper-evident. This is a real
achievement and, at its scale of adoption, the default future of media provenance.

**Assumes** — and its own literature is unusually candid here — a **trust model**:
trust is extended to many entities through assumptions and opt-in controls;
**validation is not required by the specification**; signature coverage of the entire
file is not required; and, in the words of the archival assessment, *"trusted does not
necessarily imply trustworthy."*

**Cannot do.** Answer *is this the same file?* without the original. C2PA answers *what
happened to this file, according to entities who signed*. Those are different
questions, and the second one depends on the signing entities continuing to exist,
continuing to be trusted, and having implemented validation that the specification
does not mandate.

**Developmental space — the sharpest positioning available, and it is against the
actual incumbent.** C2PA is **platform-centric**: provenance is asserted by the
capture device and the editing chain, and the reader's confidence is a function of
trust in those manufacturers. A content-derived identifier is **creator-centric**:
identity is computed from the bytes by anyone holding them, and the reader's
confidence is a function of arithmetic.

The precise formulation, which the project should adopt and defend:

> **C2PA attests what a device reports having done. A content-derived identifier
> computes what the bytes are. The first requires trusting a chain of signers; the
> second requires trusting SHA-256. Validation is optional in the first and
> constitutive in the second.**

These are complementary rather than competing, and saying so is stronger than
claiming superiority — a C2PA-signed capture that is *also* content-addressed and
publicly witnessed is better evidenced than either alone. But the differentiation
must be stated, because it is the first question any institutional reader will ask.

## §5.2 · Provenance Marks — independent arrival at the human-transcribable seal

**Blockchain Commons (2025)**, *Provenance Marks: An Innovative Approach for
Authenticity Verification*, BCR-2025-001. Each mark contains a portion verifying the
previous mark and a portion committing, by hash, to the next — a chain — and the
marks are rendered as **sequences of natural-language words** (Bytewords).

**Establishes.** That a cryptographic chain can be represented in a form a human can
read aloud, transcribe by hand, and check without a machine.

**Cannot do.** Bind to a physical artifact, or carry semantic classification.

**Developmental space.** This is the strongest external validation available for the
six-glyph seal, and it arrives independently. Two projects, unaware of each other,
concluded that **a verification token must be sayable and hand-copyable by a person**.
The archive's version differs in choosing a pictographic rather than lexical carrier —
which is worth defending on its own terms, since glyphs are script-independent in a
way English wordlists are not, and the project's founding specimen is in Japanese
hand.

## §5.3 · ARCHANGEL — institutional integrity at century scale

**The UK National Archives, ARCHANGEL project (2018–2019)**; see *Underscoring
archival authenticity with blockchain technology*, UKSG Insights 32 (2019).

**Establishes.** That a national archive took seriously the problem of proving
integrity across decade-to-century spans **without a trusted third party**, and
implemented distributed checksum records to do it.

**Cannot do.** Address content that was never enrolled, or provide meaning — it
records that a hash was seen at a time.

**Developmental space.** The institutional precedent matters more than the
technology. A national archive publicly concluding that century-scale integrity
requires removing the trusted third party is a citation that costs the project
nothing and grants it considerable standing.

## §5.4 · Persistent identifier infrastructure

DOI (ISO 26324), Handle, ARK, URN:NBN, PURL, SWHID (ISO/IEC 18670:2025), IPFS CID.

**Establishes.** A mature and genuinely successful ecosystem for naming, resolving,
and citing scholarly objects, with governance and citation recognition that no new
system possesses.

**Cannot do.** Say anything about bytes, or about physical objects. The ARK
community's own doctrine is the most honest statement in the space: **persistence
means persistent management**, and no syntax guarantees it.

**Developmental space.** Fully treated in the companion packet
`AXN:05B7.OPERATIVE.♦️🌌📌🦅🌑💜` (#1437). For this paper the relevant point is
narrow: the PID literature answers a question about *names* and the project asks a
question about *objects*, so competition between them is a category error.

---

# PART VI · THE ONTOLOGICAL QUESTION
### *What kind of thing is a handwritten artifact?*

## §6.1 · Goodman — and the most precise statement of the project

**Nelson Goodman, *Languages of Art* (1968)**, esp. II.3–4. A work is **autographic**
if even the most exact duplication does not count as genuine — if the work's identity
is constituted by its history of production. Painting and manuscript are autographic.
A work is **allographic** if it is constituted by notation, and any compliant
performance or copy is fully the work. Music and printed text are allographic.

**Establishes.** That the distinction is about **the possibility of forgery**, not
about materiality as such. Forgery is coherent only for autographic works; a "forged"
performance of a symphony is just a performance.

**Assumes.** That notation, where it exists, is complete — that the score exhausts
the work.

**Cannot do.** Accommodate a work that is autographic but whose identity one wishes
to check by notation-like means. Goodman does not consider it, because in 1968 there
was no such method.

**Developmental space — this is the dissertation's philosophical claim, and it is
genuinely novel.** The proposition is:

> **A machine-eligible handwritten artifact remains autographic — its identity is
> still constituted by its history of production — while acquiring an allographically
> checkable identity property.**

The page cannot be forged in Goodman's sense; a duplicate is not the work. But the
question *is this the artifact?* becomes answerable by computation rather than by
connoisseurship. That is not a collapse of the distinction; it is the addition of a
verification channel to a category Goodman took to have none. Pressing this properly
is a chapter.

## §6.2 · The material-text tradition — why layout is the work

**D. F. McKenzie, *Bibliography and the Sociology of Texts* (1986)**: forms effect
meaning; the material presentation is a signifying system rather than a container.
**Jerome McGann, *The Textual Condition* (1991)**: linguistic codes and bibliographic
codes are both the work. **Johanna Drucker, *The Visible Word* (1994)** and
*Graphesis* (2014): the graphical is knowledge-production, not decoration;
performative materiality — the page *does* rather than shows. **N. Katherine Hayles,
*Writing Machines* (2002)**: the technotext as a work that interrogates its own
inscription technology.

**Establishes.** That the material and spatial features of a document are
constitutive of meaning, not accidental to it — a claim now standard in book history
and textual scholarship.

**Cannot do.** Survive the representation pipeline. This is exactly the finding of the
archive's own **Whitespace as Provenance** (`AXN:03BB`, #943): *character-preserving
compositional loss* — the text survives, the composition does not, and no error is
reported.

**Developmental space.** The tradition supplies the project's strongest *a priori*
argument for hashing a rendered capture rather than a character stream. **If
bibliographic codes are part of the work, then a digest over the rendered page is
nearer to the work than a digest over its text.** The archive arrived at
capture-hashing for practical reasons; McKenzie and McGann make it a principled
position. That reframing is available immediately and costs nothing.

## §6.3 · Barthes — what an attestation photograph certifies, exactly

**Roland Barthes, *La chambre claire* (1980)**. The photograph's *noeme* is
**"ça-a-été"** — that-has-been. Its distinctive power is not resemblance but
**indexicality**: a physical, causal connection between the object and the image.

**Establishes.** That a photograph certifies *presence at a time*, and that this is
categorically different from certifying meaning, identity, or authorship.

**Developmental space — a needed precision.** The attestation photograph in
`AXN:0592` (#1409) — an in-frame timestamped image of a signed, dated inscription —
is precisely a Barthesian index. But the scope of what it certifies should be stated
in Barthes's own terms: **it certifies that this page existed in this state at this
time. It does not certify who made the marks.** Authorship is established by the
writer-identification chain (§4.1) and by declaration; the photograph establishes
existence and state. Keeping these separate is the difference between a defensible
evidentiary claim and an overreaching one — and it is exactly the kind of distinction
the archive's own *identity is not authorship* incision already makes elsewhere.

## §6.4 · Benjamin — aura, re-priced

**Walter Benjamin, "Das Kunstwerk im Zeitalter seiner technischen
Reproduzierbarkeit" (1935–36)**. Aura is the work's unique presence in time and
space; technological reproduction strips it.

**Developmental space.** The project inverts the direction of Benjamin's argument
without contradicting it. Benjamin describes *reproduction* — copies of an existing
original. Generative systems perform *production without an original*. In that
condition, what becomes scarce is not the unique object but **the verifiably
un-generated one**. Aura returns not as uniqueness but as **provenance under
conditions of synthetic abundance** — and it returns as a measurable property rather
than a felt one, which is a genuinely Benjaminian irony worth writing.

## §6.5 · Taylor — archive and repertoire

**Diana Taylor, *The Archive and the Repertoire* (2003)**. The archive is durable,
textual, institutional; the repertoire is embodied, performed, ephemeral — and the
distinction has historically carried a hierarchy that privileges the first.

**Developmental space.** A handwritten page is both, and the project is precisely the
mechanism by which a repertoire object — a gesture, a hand, a body's movement across
paper — enters the archive **without being converted into text**. Taylor supplies the
critical vocabulary for what is at stake in refusing the conversion, and connects the
technical argument to a body of work that would otherwise regard it as mere
infrastructure.

---

# PART VII · WHAT THE LITERATURE ESTABLISHES, AND WHAT IT LEAVES

**Established across the surveyed fields.** Handwriting can be transcribed at scale
(§1.1) and retrieved without transcription (§1.2). Editorial uncertainty has a
century-old grammar (§2.1) that can now be machine-emitted (§2.2). Machine assistance
raises expert accuracy when it presents alternatives rather than verdicts (§2.3).
Physical objects can be read non-destructively, and *unreadable* is a claim about
instruments (§2.4). Perceptual descriptors survive re-capture but cannot bear identity
(§3.2). Paper carries an unclonable physical fingerprint (§3.3). Margins are the safe
vector for added verification marks (§3.4). Handwriting is individuating at scale
(§4.1) and synthesisable from few exemplars (§4.2). Provenance can be signed but its
validation is optional (§5.1). Verification tokens can be human-transcribable (§5.2).
Bibliographic codes are constitutive of the work (§6.2), and a photograph certifies
existence rather than authorship (§6.3).

**Left open — and these are the dissertation's questions.**

**Q1.** Can a handwritten artifact be *cited* without being converted, given that it
can already be *retrieved* without being converted? (§1.2)

**Q2.** Can the Leiden distinction between damage and illegibility be made machine-
operable, so that a reader can tell *the page is torn* from *I cannot read it*? (§2.2)

**Q3.** Can the physical artifact — not a capture of it — be bound to a content-derived
identifier, via enrollment at inscription time? (§3.3)

**Q4.** Does a dated, chained, attested, physically enrolled corpus in a single hand
constitute a warrant that survives the improvement of handwriting synthesis? (§4.2)

**Q5.** What is the correct relation between platform-attested and content-derived
provenance, and can they be composed rather than opposed? (§5.1)

**Q6.** Can a work remain autographic while acquiring an allographically checkable
identity — and what does that do to Goodman's distinction? (§6.1)

---

# PART VIII · THE INTERVENTION, AND WHY IT IS AVAILABLE ONLY HERE

Each of the six questions is answerable only under a condition the celebrated
projects lack: **a living author, working now, who can sign, date, photograph,
enroll, attest, consent, and be asked again next year.**

Vesuvius and Ithaca work on authors who cannot be consulted. HTR works on collections
whose creators are dead or anonymous. C2PA works on devices, not people. Writer
identification works on samples, not on relationships. The PID ecosystem works on
names.

**The project's distinctive asset is not the identifier. It is the collaboration** —
and the corpus it makes possible is the instrument by which four of the six questions
become empirically testable rather than merely arguable. That is the case for the
work, and it is also the case for treating the consent conversation as the first
research act rather than a preliminary to it.

---

## Note on evidence and status

Internal works are cited by AXN and record number and were verified against the
registry at 1,437 deposits. External works are cited by author, title and venue.
Where a source was surveyed through secondary description rather than read in full —
the margin-watermarking cluster (§3.4), ARCHANGEL (§5.3), and portions of the writer-
identification literature (§4.1) — the précis reflects that literature's reported
findings and should be confirmed against the primary text before any claim here is
deposited or submitted.
