# MACHINE-ELIGIBLE HANDWRITTEN ARTIFACTS
## A Topics Paper: The Literature, Its Limits, and the Space for an Evidentiary Identifier

**v2.0 · 2026-08-07 · TACHYON for MANUS**
**Integrates:** three internal archival passes, four external research passes
(including the Assembly external constellation v0.1), and a papyrology/AI sweep.
**Status:** field survey and problem statement in advance of a dissertation-scale
project. **For review.**

**Convention.** Each source receives what it **establishes** (its finding, not its
ambition), what it **assumes** (the conditions under which the finding holds), and
what it **cannot do** (the boundary its own method sets). The third is operative: the
developmental space is made of other people's boundaries.

**A terminological discipline adopted in this version.** Following InterPARES (§5.5),
this paper distinguishes **verifiable exact capture** — what a digest establishes —
from **authenticity**, which is a broader judgment requiring identity, integrity,
transmission context, custody, documentary form, and procedure. v1.0 used
"verification" loosely across both. The correction is load-bearing and is applied
throughout.

---

## §0 · THE PROBLEM

A handwritten page is an object whose identity is constituted by its history of
production. A digital file is an object whose identity is constituted by its bytes.
Between them sits a photograph, which is neither: a *new* object made at a particular
moment under particular light, and no two photographs of one page share a digest.

> **Under what conditions can a handwritten artifact enter a machine-readable
> scholarly record as itself — cited, verifiably captured, and reasoned about —
> without being converted into text, and without its identity depending on the
> continued goodwill of any institution?**

Five established literatures each answer part of this and stop. **Handwritten text
recognition** makes writing legible by discarding the hand. **Papyrology and its
digital infrastructure** have a century of discipline for reading damaged inscription,
declaring uncertainty, and modelling the artifact/text distinction — but work on
authors who cannot be consulted. **Cultural-heritage modelling** describes objects and
digitisation events precisely and verifies nothing. **Content provenance** attests
what a device reports, on the authority of its manufacturer. **Persistent identifier
infrastructure** names and resolves, and touches neither bytes nor objects.

The gap is not that these fields have failed. **None was built for a living author who
wants a physical page to be citable by machines a century from now.**

---

# PART I · THE LEGIBILITY QUESTION
### *What must be true for a machine to read a hand?*

## §1.1 · HTR as a converting technology

**Transkribus** (READ-COOP / Innsbruck) and **eScriptorium/Kraken** (PSL) perform
layout analysis and transcription, training per-hand models on typically 50–100
annotated pages.

**Establishes.** Unconstrained historical handwriting is transcribable at scholarly
accuracy given per-hand training, at bounded and known cost.

**Assumes.** *The desired output is text.* Every architectural decision follows:
layout analysis finds lines to transcribe; models are scored on character error rate;
ground truth is a string.

**Cannot do.** Preserve the hand as evidence. After a successful pass, what enters the
scholarly record is a character stream with, at best, a link back to an image. **The
transcription is cited; the image is stored.** The hand becomes a provenance footnote
to its own text.

**Developmental space.** The project inverts the output: the hand is the payload,
conversion is loss. Not a criticism of HTR — a different objective. HTR also supplies
something valuable for free: a **legibility floor**. If standard HTR recovers a page's
text, the artifact is machine-*readable*; machine-*eligibility* is a further and
separable property. Distinguishing the two cleanly is available immediately.

## §1.2 · Word spotting — the nearest neighbour

**Rath & Manmatha (2007)**, IJDAR; **Giotis et al. (2017)**, *A Survey on Word
Spotting in Handwritten Documents*, Pattern Recognition.

**Establishes.** Handwritten corpora can be made *retrievable* without transcription.
Retrieval accuracy is usable where transcription accuracy would not be.

**Cannot do.** Support citation. A hit is a location in an image, not an addressable,
quotable unit a third party can independently confirm.

**Developmental space.** The most instructive neighbour, because it **already accepts
the core premise** — handwriting can be operated on without conversion — and declines
the further step. *Retrieval without conversion* is established. **Nobody has asked
whether citation without conversion can work.** That is the dissertation question, and
word spotting is its shoulder.

## §1.3 · Layout analysis and the margin-isolation problem

**Reul et al. (2019)** LAREX, IJDAR; **Wigington et al. (2018)** ECCV; **Transkribus
layout recognition**; **PAGE XML** and **ALTO** as the interchange formats;
LayoutLMv3 as the current general model.

**Establishes.** Reliable segmentation of complex page geometry — text blocks,
marginalia, interlinear insertion, strikethrough — including on degraded material,
with standardised layout-grounded transcription formats (PAGE, ALTO) that bind text
to coordinates.

**Cannot do.** Distinguish *authorial* marginalia from *systemic* marginalia. A model
trained to find marginal notes will find an added identifier band; both are marginal
marks.

**Developmental space.** A live operational risk with a testable form: **does an
off-the-shelf layout model classify a stamp band as authorial marginalia?** If yes,
the band's geometry is a design constraint discoverable by experiment. Among the
cheapest empirical contributions available. **ALTO/PAGE are also the correct
interchange target** — the project should emit them rather than invent a coordinate
vocabulary.

## §1.4 · Ground truth for the ancient hand

**HTR-United** — Zenon papyri ground-truth dataset; **Transkribus** public models.

**Establishes.** Community-governed, versioned ground truth for papyrological hands
exists and is shared.

**Developmental space.** A contemporary corpus with attested provenance, dated
inscription events, and consent is **a ground-truth resource of a kind the field does
not have** — every existing set is retrospective and its provenance reconstructed.
This is a contribution to HTR, not merely a use of it.

---

# PART II · THE UNCERTAINTY QUESTION
### *How does a reader declare what could not be read?*

## §2.1 · The Leiden Conventions (1931) — an epistemic contract

Agreed at Leiden, 1931; published by **Wilcken, "Das Leydener Klammersystem,"
*Archiv für Papyrusforschung* 10 (1932), 211–212**; reformulated by **Sterling Dow,
*Conventions in Editing* (1969)**; harmonised for digital publication as **Leiden+**;
implemented in the **papyri.info / DDbDP** editorial pipeline.

| Siglum | Meaning |
|---|---|
| `[abc]` | lost from the original, **restored by the editor** |
| `[...]` | lacuna of **known** extent — one dot per missing letter |
| `[— — —]` | lacuna of **unknown** extent |
| `ạḅ` | characters **damaged or unclear**, ambiguous outside context |
| `⟨ab⟩` | omitted in error by the **ancient scribe**, supplied by the editor |
| `{ab}` | present but judged **erroneous and superfluous** by the editor |
| `…` | traces **insufficient for restoration** |

**Establishes.** Editorial uncertainty is not one thing. These encode at least **five
distinct epistemic acts**:

1. *I cannot see it, and I know how much is missing.*
2. *I cannot see it, and I do not know how much is missing.*
3. *I cannot see it, and I am supplying it by inference.*
4. *I can see something and am unsure what it is.*
5. *I can see it clearly and believe the original is wrong.*

The fifth is remarkable: a convention for recording that the **source** erred, kept
distinct from recording that the **reader** is uncertain.

**Cannot do.** Travel. A print convention: not tokenisation-stable, not
machine-parseable without a grammar, and carrying no mechanism binding a transcription
to an artifact.

**Developmental space — the paper's central positioning finding.** The archive's
Lacuna Protocol holds that a disclosed absence is a first-class result. That doctrine
has **a ninety-five-year precedent it has never cited, and the precedent is more
granular than the doctrine.** One lacuna type where papyrology has five; the
extent-known/extent-unknown distinction alone is a specification upgrade available for
the cost of adopting it.

The stronger move is positional: claiming this lineage converts an apparently eccentric
insistence on marking absence into **continuity with the editorial tradition of
classical philology** — the difference between a novel claim requiring defence and an
inherited discipline requiring extension.

## §2.2 · "Mind the Gap" (2024) — teaching a model to mark what it cannot read

**arXiv 2407.00250.** TrOCR trained on Leiden-annotated ground truth with weighted
loss `L_weighted = L × (n_brackets + 1)`; only 15% of training lines carried lacuna
annotation, which the weighting compensates.

**Establishes.** A transcription model can be trained to *emit* editorial uncertainty
markers, and doing so requires deliberately reweighting the objective.

**Cannot do.** Distinguish *why* a lacuna exists — damage, illegibility, occlusion, or
the model's own incapacity all collapse into one bracket.

**Developmental space.** The loss function is the finding: multiplying loss by bracket
count **teaches the model that marking absence matters more than transcribing
presence** — an inversion of standard OCR objectives, which penalise all character
errors equally and therefore reward confident guessing. The extension available is
Leiden's own distinction: `…` (traces, physically insufficient) versus `[...]`
(lacuna). **A machine should be able to say *the page is torn* rather than *I cannot
read it*.** Specifiable and testable.

## §2.3 · Ithaca (2022) — the collaboration figure, and what produced it

**Assael, Sommerschield et al., *Nature* 603 (2022), 280–283.** Trained on **I.PHI**,
78,608 inscriptions from the Packard Humanities Institute. Restoration: model **62%**;
historians **25%**; **historians with Ithaca 72%**. Geographic attribution 71%; dating
within ~30 years.

**Assumes.** A large, clean, machine-actionable corpus. I.PHI required an extended
ruleset to normalise 84 regions and heterogeneous date formats. **The dataset
construction is the hidden achievement.**

**Developmental space — this is not "AI helps."** The 25→72 gain cannot come from
accuracy: the model alone scores 62, *below* the collaborative figure. It comes from
**interface design** — ranked top-20 hypotheses with saliency, not a verdict; the
historian evaluates alternatives rather than accepting an answer.

This bears directly on the archive's **Differential Register Prioritization**
(`AXN:058F`, #1406), which specifies the hazard that a machine's early reading
suppresses later interpretive fields. Ithaca is empirical evidence that **the hazard is
a property of single-verdict interfaces, not of machine reading as such**, and that
ranked-alternative presentation is the mitigation. That converts an internal warning
into a design requirement with external validation.

## §2.4 · Vesuvius Challenge (2023–2026) — and the readability score of zero

**PHerc. 1667** virtually unwrapped and read end to end, announced **25 June 2026**;
~1.5 m across 20 columns; phase-contrast µCT on the ESRF **BM18** beamline. For
**PHerc. Paris 4**, ink is directly visible in the tomographic volume and segmentable
in three dimensions rather than inferred from a surface fit.

**Cannot do.** Attribute, consent, or ask.

**Developmental space — two findings, one larger than the project.**

**The readability score.** PHerc. 1667 was physically opened and damaged in the 1980s
and assigned a readability score of **zero**. Nicolardi's statement on the result —
that *"we can follow sustained arguments across multiple columns"* — is a claim about
instruments, not objects. **"Unreadable" was a property of the available method, and
the object was reclassified when the method changed.** For an archive whose founding
injury is classification as out-of-scope, that proposition transfers exactly:
*classifications of unreadability are claims about readers.*

**The release model.** Tomographic data, surfaces and transcriptions under Creative
Commons; code on GitHub; data at the ESRF. Credibility for an extraordinary claim was
manufactured by making it checkable. And the division of labour is explicit: **the
machine recovers the surface; the papyrologist reads it**, with transcriptions
attributed to named human readers.

---

# PART III · THE MODELLING QUESTION *(new in v2.0)*
### *What is the identified unit, and how is a capture represented?*

This part was absent from v1.0 and is where the external constellation is strongest.
**Most of what the project needs to say about objects has already been modelled.**

## §3.1 · Trismegistos — the unit-of-identification problem, already solved

**trismegistos.org**; identifier policy at `about_how_to_cite.php`; data standards at
`about_datastandards.php`.

**Establishes.** A working policy for what receives a stable number across an
interdisciplinary ancient-text corpus. Trismegistos prioritises **material aspects**:
multiple texts on what was a single ancient writing surface generally belong to one
*document* record, unless the shared surface is merely accidental. It models reuse
explicitly — blank-side reuse, reuse of blank space, palimpsest old/new relations,
multiple texts on one papyrus. And it **preserves superseded identifiers and
redirects** after records are joined or corrected.

**Cannot do.** Verify. It is a naming and disambiguation authority for a scholarly
community.

**Developmental space — the closest precedent for a question the project has not
answered.** What exactly is the identified unit?

```
one artifact may bear several texts
one work may span several artifacts
one artifact may be reused for an unrelated work
one capture may represent part of one artifact
one derivative may combine several captures
```

Contemporary sheets are equally complex: recto/verso, layered, corrected,
overwritten, collaged, continued later, **stamped after inscription**. Trismegistos's
rule — that added marks and later witness events should be represented **as events and
zones rather than as co-original with the handwriting** — is precisely the discipline
an added-margin doctrine requires. And its identifier policy (preserve superseded
numbers, redirect, never silently merge) is a direct model for AXN's own
non-destruction commitment.

## §3.2 · CIDOC CRM and CRMdig — the missing ontology between page and hash

**cidoc-crm.org**; **CRMdig** extension.

**Establishes.** CRM models cultural-heritage objects, actors and events; **CRMdig
extends it to describe methods, steps, equipment, parameters and physical measurement
processes that produce digital representations.**

**Developmental space — this is the answer to the byte-shift problem's *modelling*
half.** CRMdig represents **capture as an event produced by a device and a process,
not as a transparent copy.** That is exactly the relation the project needs between
physical page and capture hash, and it exists, is maintained, and is used by museums.

**Recommendation, adopted:** build the analog profile as a **constrained mapping to
CRMdig** before inventing capture-event properties. Inventing a parallel vocabulary
here would be the clearest possible sign of not having read the field.

## §3.3 · PROV-O, Web Annotation, IIIF

**W3C PROV-O** — the interoperable provenance projection (entities, activities,
agents). **W3C Web Annotation Data Model** — annotations with targets and selectors,
including image regions. **IIIF Presentation API** and **Image API** — canvases,
annotations, and arbitrary-region image requests.

**Establishes.** That **images, passages, and image regions are already citable** at
web scale, with mature standards and broad institutional adoption. A IIIF canvas plus
a Web Annotation selector addresses a rectangle of a manuscript page as a first-class
resource.

**Developmental space — and a claim the project must not make.** *"No prior system
makes image regions citable"* is **false**, and asserting it would be immediately
disqualifying to any digital-humanities reader. What IIIF does not supply is
**content-verifiable identity**: a canvas is a URI served by an institution, and if
the institution stops serving it, the citation fails in exactly the way the project
exists to address. **The differentiation is verification and custody, not
addressability.**

## §3.4 · EpiDoc, TEI facsimile, CITE/CTS, METS, PREMIS

**EpiDoc** (TEI XML for ancient documents, including physical description);
**TEI `<facsimile>`/`<surface>`/`<zone>`** binding text to image coordinates; **CITE
Architecture / Canonical Text Services** and the **Homer Multitext** for canonical
citation of texts and image regions; **METS** for packaging physical and logical
structure; **PREMIS** for preservation metadata.

**Establishes.** A complete, mature stack for describing, structuring, packaging and
preserving manuscript material — including the artifact/text distinction the project
treats as central.

**Developmental space.** Two consequences. First, another **claim to avoid**: the
project did not invent the text/artifact distinction; TEI, EpiDoc and CITE have
encoded it for decades. Second, **these are emission targets, not competitors.** An
analog profile that emits EpiDoc-compatible physical description and TEI zones would
be legible to the exact scholarly community whose practice it inherits.

## §3.5 · Genetic criticism, IFLA LRM

**Centre for Manuscript Genetics** (Antwerp); *critique génétique* and the
*avant-texte*. **IFLA Library Reference Model** and **ISBD for Manifestation**.

**Establishes.** Genetic criticism treats the manuscript record of composition — drafts,
corrections, layers — as a scholarly object in its own right. IFLA LRM supplies the
work/expression/manifestation/item hierarchy that library cataloguing rests on.

**Developmental space.** Genetic criticism is the humanities discipline most invested
in *the page as process*, and it has never had a verification layer. IFLA LRM supplies
the vocabulary for saying precisely which level an identifier addresses — **and the
project's answer is unusual: the AXN kernel addresses an *item*, while the record
addresses a *manifestation*.** Stating that in LRM terms would make the system legible
to cataloguers instantly.

---

# PART IV · THE IDENTITY QUESTION
### *How does an artifact's identity survive re-capture?*

## §4.1 · The byte-shift problem, stated

A digest is a function of exact bytes. Two photographs of one page — different light,
angle, sensor noise, compression — produce unrelated digests. A content-derived
identifier computed over a capture identifies **that capture**, not the artifact.

This is correct hash behaviour, not a flaw. But *"the identifier is derived from the
work"* requires precision about **which work**: the page, or a photograph of it.

**The archive hashes the capture.** That is right; it is also, per the internal
survey, **nowhere stated in writing** — leaving the stronger and false reading
available. §3.2 supplies the modelling vocabulary (CRMdig); §4.3 supplies the physical
primitive that would close the remaining gap.

## §4.2 · Perceptual hashing — robust, not an identity function

**Zauner (2010)** pHash benchmarking; **Monga & Murchison (2006)**, IEEE TIP; SIFT/ORB
descriptors.

**Establishes.** Deterministic compact descriptors stable across noise, rotation,
scale, lighting and moderate compression — the transformations that defeat
cryptographic hashing.

**Cannot do.** Serve as a security boundary. Non-trivial false-accept rates,
especially for documents, which are visually homogeneous: two different pages in one
hand may be perceptually closer than two captures of one page.

**Developmental space.** A two-layer architecture, stated explicitly: **perceptual
hash as retrieval aid, cryptographic kernel as identity.** Conflating them would
import the false-accept rate into the identity claim. Keeping them separate is itself
a contribution, since the surveyed provenance literature routinely blurs it.

## §4.3 · Paper PUFs — the primitive that would identify the artifact

**Toreini, Shahandashti & Hao (2017)**, *Texture to the Rescue: Practical Paper
Fingerprinting based on Texture Patterns*, ACM TOPS, and the smartphone-capture line
following it.

**Establishes.** Ordinary paper carries a physically unclonable fingerprint — the
three-dimensional random arrangement of its fibres, visible as translucency under
transmissive light — capturable with commodity hardware and reliably matchable.

**Cannot do.** Work retrospectively. A page never enrolled cannot be fingerprinted
from an existing photograph; the required lighting is transmissive and the resolution
high.

**Developmental space — the missing primitive.** A paper PUF identifies **the physical
sheet**; a kernel identifies **a capture**. Together they would support *this is the
same physical page*, not merely *this is the same photograph*.

**The enrollment constraint is what makes this research rather than engineering, and
it is available only to a project working with a living author** — the pages are in
hand and can be enrolled at inscription time. No historical collection can say that.
On the survey's evidence this is the single most promising unexploited technical
direction.

## §4.4 · Margin watermarking — independent convergence

**Brassil, Low & Maxemchuk (1999)**, Proc. IEEE; **Brito et al. (2018)**, *Journal of
Imaging*; **Liu et al. (2023)** machine-readable aesthetic glyphs.

**Establishes.** Verification data can be printed into margins without occluding
content and recovered by mobile sensors; spatial layout invariants govern survival
across re-capture.

**Cannot do.** Serve the author. These systems mark documents on a distributor's
behalf to detect copying; the mark is imposed, not declared.

**Developmental space.** The convergence is the point: this literature reached the
added-margin conclusion from anti-piracy motives, the archive from a doctrine that
*the hand is never overprinted*. **Independent arrival at one constraint from opposed
motivations is evidence the constraint is real.** The remaining differentiation is
whom the mark serves.

---

# PART V · THE AUTHORSHIP AND AUTHENTICITY QUESTIONS

## §5.1 · Writer identification — established, and scale-dependent

**Srihari, Cha, Arora & Lee (2002)**, *Individuality of Handwriting*, J. Forensic Sci.
— produced amid *Daubert* challenges to handwriting expertise; 1,500-writer stratified
sample; macro features (slant, spacing, line separation) and micro features (character
shape). Extended by **Fiel & Sablatnig (2015)**, **Xing & Qiao (2016)** DeepWriter,
**He & Schomaker (2021)** GR-RNN, and papyrus-specific preprocessing work.

**Establishes.** Handwriting is individuating at a statistically demonstrable level;
automated attribution is accurate given sufficient sample — a legal question as much
as a technical one at the time.

**Cannot do.** Attribute a single short inscription with forensic confidence.
Accuracy degrades sharply on short samples.

**Developmental space.** The scale-dependence is strategic. **The biometric continuity
claim — the hand checks against itself, page over page, year over year — is exactly
the regime where this literature is strongest, and it is inaccessible with one
specimen.** A corpus moves the claim from the weakest part of the evidence base to the
strongest.

## §5.2 · Handwriting generation — the clock

**Haines, Mac Aodha & Brostow (2016)**, *My Text in Your Handwriting*, ACM TOG;
**Bhunia et al. (2021)**, *Handwriting Transformers*, ICCV; detection of
machine-generated handwriting emerging 2024–, with no mature methods.

**Cannot do.** Reproduce a *history*. Generation produces plausible pages, not a
dated, attested, chained sequence with consistent substrate and physical enrollment.

**Developmental space — why the project is time-sensitive.** The defence is not better
detection but **cost asymmetry**: a single page may pass any test; a corpus that is
dated, sequentially chained, attested at capture and enrolled at the paper level
scales badly for an adversary. Two structural consequences: **the project must work at
corpus scale or its central warrant fails**, and the value of verified non-synthetic
inscription rises monotonically as generation improves.

## §5.3 · InterPARES and diplomatics — the correction this paper adopts

**InterPARES** (interpares.org; Authenticity Task Force documents); diplomatics from
Mabillon (1681) onward as the analytic lineage.

**Establishes.** How authentic digital records are identified, assessed and preserved,
drawing on archival science and diplomatics: authenticity depends on **identity,
integrity, creation and transmission context, custody, documentary form, procedure,
preservation controls, and evidence of alteration.**

**Cannot do.** Be reduced to a checksum.

**Developmental space — a terminological discipline, adopted throughout v2.0.** A hash
verifies bytes. **It does not establish record authenticity.** The correct usage is:

> **"Verifiable exact capture" for what a digest establishes. "Authentic" reserved for
> a broader, explicitly evidenced judgment.**

Diplomatics further disciplines the *stamp* and *witness* vocabulary: the project
records an event and supplies evidence; it **does not confer legal authenticity,
ownership, notarisation, or authority.** This aligns with the archive's own
*witnessing ≠ notarization* incision and gives it a scholarly lineage.

## §5.4 · RFC 3161 — what a timestamp is and is not

**RFC 3161**, Time-Stamp Protocol: a Time-Stamp Authority attests that a datum existed
at a time.

**Developmental space.** An attestation timestamp is **not** an RFC 3161 trusted
timestamp and must not be described as one unless a TSA is actually used. An RFC 3161
token would be a sound **optional external witness** — never the sole authority, which
would reintroduce the trusted third party the architecture exists to remove.

---

# PART VI · THE PROVENANCE QUESTION
### *Who asserts that this is what it claims to be?*

## §6.1 · C2PA — the incumbent, and the essential comparison

**Coalition for Content Provenance and Authenticity**: Adobe, Microsoft, Meta, Google,
Sony, Leica, Samsung; 6,000+ members; appearing in camera firmware and editing
software. Structure: a **Manifest** of assertions, a **Claim** (signed, tamper-evident),
and a **Claim Signature**.

**Assumes** — and its literature is candid — a trust model in which trust is extended
to many entities by assumption and opt-in; **validation is not required by the
specification**; signature coverage of the entire file is not required; and *"trusted
does not necessarily imply trustworthy."*

**Cannot do.** Answer *is this the same file?* without the original, or establish the
truth of depicted content.

**Developmental space — the sharpest positioning, against the actual incumbent.**

> **C2PA attests what a device reports having done. A content-derived identifier
> computes what the bytes are. The first requires trusting a chain of signers; the
> second requires trusting SHA-256. Validation is optional in the first and
> constitutive in the second.**

Platform-centric versus creator-centric. These are **complementary rather than
competing**, and saying so is stronger than claiming superiority: a C2PA-signed
capture that is *also* content-addressed and publicly witnessed is better evidenced
than either alone.

## §6.2 · Human-checkable fingerprints — the glyph seal's real literature

**Azimpourkivi et al., visual key fingerprints (USENIX Security 2020)** — maps keys to
images for human comparison, **explicitly modelling the limits of human visual
discrimination and measuring attack success.** **OpenSSH randomart**
(`ssh-keygen -lv`) — a mnemonic visual surface derived from a stronger fingerprint.
**RFC 2289** — conversion of a short binary value into human-readable words for manual
entry. **Blockchain Commons Provenance Marks (2025)** — a hash chain rendered as
natural-language Bytewords.

**Establishes.** A long-standing, well-studied design pattern: **keep a strong machine
representation and offer a bounded human-transcription layer.** And critically —
**human distinguishability must be measured, not assumed.**

**Cannot do.** Bear identity. Every source in this cluster states the same caution:
short human surfaces necessarily reduce collision resistance and are **recognition
aids, not substitutes for comparing the full fingerprint.**

**Developmental space — this converts an aesthetic decision into an empirical
programme.** The six-glyph seal has a real literature it has never engaged, and that
literature prescribes the tests: **confusion rates, recall, transcription accuracy,
cross-device rendering, low-resolution and grayscale legibility, missing-glyph
behaviour, sequence-order errors, and accessibility.** None has been run. Running them
is a paper, and the honest possible outcome — that six glyphs discriminate less well
than assumed — is publishable either way.

The archive's own scope discipline (*the glyphs are a 48-bit recognition checksum; the
full digest is the security boundary*) is exactly the caution this literature demands,
arrived at independently. That should be cited, not merely asserted.

## §6.3 · Unicode — a threat to the seal not previously considered

**UAX #15** (Normalization Forms); **UTS #51** (Unicode Emoji), presentation sequences
and variation selectors.

**Establishes.** Canonical and compatibility normalisation define equivalence classes,
and **compatibility normalisation can deliberately erase distinctions.** Emoji
rendering depends on presentation sequences, variation selectors, platform font
coverage, and ZWJ sequence support.

**Developmental space — a live risk.** A glyph seal transmitted through a system that
applies compatibility normalisation, strips variation selectors, or lacks a font may
arrive **altered or invisible** — silently. The project must specify the seal's
**normalisation form, code points including any variation selectors, and expected
fallback behaviour**, and should test transmission through the pipelines it cares
about most: search indexing, PDF text layers, email, and the composition layers it
measures. This is the seal's equivalent of the byte-shift problem, and it is currently
unaddressed.

## §6.4 · ARCHANGEL and the PID ecosystem

**ARCHANGEL** (UK National Archives, 2018–19; UKSG *Insights* 32) — distributed
checksum records for decade-to-century integrity **without a trusted third party**.
Institutional precedent worth more than the technology.

**DOI (ISO 26324), Handle, ARK, URN:NBN, PURL, SWHID (ISO/IEC 18670:2025), CID** —
mature naming and resolution with governance and citation recognition no new system
possesses; treated fully in the companion packet `AXN:05B7.OPERATIVE.♦️🌌📌🦅🌑💜`
(#1437). The ARK community's doctrine is the honest statement in the space:
**persistence means persistent management.**

## §6.5 · Preservation packaging

**RO-Crate**, **BagIt (RFC 8493)**, **Oxford Common File Layout**, **ResourceSync**,
**OAI-PMH**, **FAIR Signposting**, **Memento (RFC 7089)**.

**Establishes.** Complete, adopted machinery for packaging, harvesting, discovering and
time-travelling scholarly objects.

**Developmental space.** These are emission targets and several are already
implemented in the archive. The relevant discipline is a **claim to avoid**: one
registry and one website are not distribution, whatever the packaging.

---

# PART VII · THE ONTOLOGICAL QUESTION

## §7.1 · Goodman — the project's philosophical claim

**Nelson Goodman, *Languages of Art* (1968)**, II.3–4. A work is **autographic** if
even the most exact duplication does not count as genuine — identity constituted by
history of production. **Allographic** if constituted by notation, where any compliant
copy is fully the work.

**Establishes.** The distinction is about **the possibility of forgery**, not
materiality as such. Forgery is coherent only for autographic works.

**Cannot do.** Accommodate a work that is autographic but whose identity one wishes to
check by notation-like means. Goodman does not consider it; in 1968 there was no such
method.

**Developmental space — the dissertation's philosophical claim, and it is novel:**

> **A machine-eligible handwritten artifact remains autographic — its identity still
> constituted by its history of production — while acquiring an allographically
> checkable identity property.**

The page cannot be forged in Goodman's sense; a duplicate is not the work. But *is
this the artifact?* becomes answerable by computation rather than connoisseurship. Not
a collapse of the distinction but **a verification channel added to a category Goodman
took to have none.** A chapter.

## §7.2 · The material-text tradition — why layout is the work

**McKenzie (1986)** forms effect meaning; **McGann (1991)** linguistic and
bibliographic codes are both the work; **Drucker (1994, 2014)** performative
materiality; **Hayles (2002)** the technotext.

**Cannot do.** Survive the representation pipeline — which is the archive's own
finding in **Whitespace as Provenance** (`AXN:03BB`, #943): *character-preserving
compositional loss*, the text surviving while the composition does not, with no error
reported.

**Developmental space.** The tradition supplies the strongest *a priori* argument for
hashing a rendered capture rather than a character stream: **if bibliographic codes are
part of the work, a digest over the rendered page is nearer to the work than a digest
over its text.** The archive arrived at capture-hashing for practical reasons;
McKenzie and McGann make it principled.

## §7.3 · Barthes — what the attestation photograph certifies

**Barthes, *La chambre claire* (1980).** The photograph's *noeme* is **"ça-a-été"** —
that-has-been; its power is **indexicality**, a physical causal connection between
object and image.

**Developmental space — a needed precision.** The attestation photograph in
`AXN:0592` (#1409) is exactly a Barthesian index, and its scope should be stated in
those terms: **it certifies that this page existed in this state at this time. It does
not certify who made the marks.** Authorship comes from the writer-identification
chain (§5.1) and declaration. This is the same discipline as the archive's *identity is
not authorship* incision, and the same discipline InterPARES demands (§5.3).

## §7.4 · Benjamin and Taylor

**Benjamin (1935–36)** — aura as unique presence, stripped by reproduction. The
project inverts the direction without contradiction: Benjamin describes *reproduction*
of an existing original; generative systems perform *production without an original*.
What becomes scarce is not the unique object but **the verifiably un-generated one** —
aura returning as provenance under synthetic abundance, and as a measurable rather
than felt property.

**Taylor (2003)** — archive and repertoire. A handwritten page is both, and the project
is the mechanism by which a repertoire object — a gesture, a hand, a body's movement
across paper — enters the archive **without conversion to text.**

---

# PART VIII · WHAT THE LITERATURE ESTABLISHES, AND WHAT IT LEAVES

**Established.** Handwriting is transcribable at scale (§1.1) and retrievable without
transcription (§1.2), with standardised layout formats (§1.3). Editorial uncertainty
has a century-old five-part grammar (§2.1), now machine-emittable (§2.2). Machine
assistance raises expert accuracy when it offers alternatives rather than verdicts
(§2.3). Physical objects can be read non-destructively, and *unreadable* is a claim
about instruments (§2.4). The unit-of-identification problem has a working policy
(§3.1) and capture is already modelled as a device-and-process event (§3.2). Images and
image regions are already citable (§3.3), and the artifact/text distinction has been
encoded for decades (§3.4). Perceptual descriptors survive re-capture but cannot bear
identity (§4.2). Paper carries an unclonable fingerprint (§4.3). Margins are the safe
vector for added marks (§4.4). Handwriting is individuating at scale (§5.1) and
synthesisable from few exemplars (§5.2). Authenticity is broader than integrity (§5.3).
Human-checkable fingerprints are a studied pattern whose discriminability must be
measured (§6.2). Bibliographic codes are constitutive (§7.2); a photograph certifies
existence, not authorship (§7.3).

**Left open — the dissertation's questions.**

**Q1.** Can a handwritten artifact be **cited** without conversion, given that it can
already be **retrieved** without conversion? (§1.2)

**Q2.** Can Leiden's distinction between *physical damage* and *reader incapacity* be
made machine-operable? (§2.1–2.2)

**Q3.** Can the **physical artifact** be bound to a content-derived identifier via
enrollment at inscription time — and can the resulting compound object be expressed as
a constrained CRMdig profile? (§3.2, §4.3)

**Q4.** Does a dated, chained, attested, physically enrolled corpus in a single hand
constitute a warrant that survives improving handwriting synthesis? (§5.2)

**Q5.** How should platform-attested and content-derived provenance be **composed**
rather than opposed? (§6.1)

**Q6.** How discriminable is a six-glyph seal to human readers under the conditions the
visual-fingerprint literature specifies — and does it survive Unicode normalisation
and platform rendering? (§6.2–6.3)

**Q7.** Can a work remain autographic while acquiring an allographically checkable
identity, and what does that do to Goodman's distinction? (§7.1)

---

# PART IX · CLAIMS TO AVOID

Recorded as scholarly discipline, because each is available to a careless draft and
each would be disqualifying to the readers the project most needs.

**Do not claim** that the project invented the text/artifact distinction (§3.4); that
no prior system identifies writing surfaces (§3.1); that no prior system makes images,
passages or image regions citable (§3.3); that a hash establishes authorship (§7.3) or
archival authenticity (§5.3); that the glyph sequence is the cryptographic security
boundary (§6.2); that OCR or HTR preserves the artifact (§1.1); that a transcription is
an equivalent copy; that an attestation timestamp is an RFC 3161 trusted timestamp
(§5.4); that C2PA proves the truth of depicted content (§6.1); that one registry and
one website constitute distribution (§6.5); that a handwritten original is
self-interpreting; that all blank space is semantically significant; or that papyrology
reduces to *preserving handwriting* (§2).

---

# PART X · THE INTERVENTION

**The credible originality claim** is not any single property. It is that no located
system combines, in one lightweight public instrument for **contemporary** handwritten
artifacts:

```
full exact-capture digest
+ visible hand-copyable recognition seal
+ public witness position
+ non-destructive event history
+ explicit work / artifact / capture distinction
+ machine-readable provenance and reading instructions
+ open registry export
+ composition-layer measurement
+ plural custody and resolution
```

Stated as a sentence:

> **A public, content-verifiable witness protocol that lets a contemporary handwritten
> artifact carry a visible machine address while preserving the artifact, the capture,
> the transcription, and the interpretation as distinct objects.**

The glyphs matter because they make the relation perceptible at the artifact surface.
The full digest matters because perception is not proof. The public witness matters
because a bare hash has no history. The facsimile and annotation layers matter because
a digest cannot teach a machine how a page is organised. Plural custody matters because
**no identifier stores the object.**

**And the enabling condition is not technical.** Each of Q1–Q7 is answerable only where
there is **a living author who can sign, date, photograph, enroll, attest, consent, and
be asked again next year.** Vesuvius and Ithaca work on authors who cannot be consulted;
HTR on collections whose creators are anonymous; C2PA on devices; writer identification
on samples; the PID ecosystem on names.

The project's distinctive asset is not the identifier. **It is the collaboration** —
which makes the consent conversation the first research act rather than a preliminary
to one.

---

## Note on evidence and status

Internal works cited by AXN and record number, verified against the registry at 1,437
deposits. External works cited by author, title and venue. Sources surveyed through
secondary description rather than read in full — the margin-watermarking cluster
(§4.4), ARCHANGEL (§6.4), portions of the writer-identification literature (§5.1), and
the visual-fingerprint cluster (§6.2) — are marked as such and require confirmation
against the primary text before any claim here is deposited or submitted.

**Priority reads before drafting:** Bagnall, *Oxford Handbook of Papyrology*;
Trismegistos identifier policy; CRMdig; InterPARES Authenticity Task Force; the USENIX
visual-fingerprint study; UAX #15 and UTS #51.
