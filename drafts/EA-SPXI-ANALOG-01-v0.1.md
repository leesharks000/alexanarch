# EA-SPXI-ANALOG-01 — Machine-Eligible Inscription Artifacts
## SPXI extension for analog-origin works · DRAFT v0.1 (blind) · 2026-07-20
### Status: DRAFT — not minted, not deposited. TACHYON blind draft for MANUS review.

---

## 0. The Inversion

Search doctrine since its beginning has held: *do not put important text in images; machines
cannot be trusted to read it.* Every accessibility guide, every SEO manual, every repository
standard treats the image as the degraded twin of text. This instrument inverts the doctrine
and instruments the inversion:

> **The load-bearing content of the artifact lives only in the handwritten image.
> All surrounding machine-readable material — however rich — is scaffold: it frames,
> attests, points, and invites, but does not contain the payload. Any machine
> composition that includes the payload has necessarily read the ink.**

The inversion is not a stunt. It converts the artifact into a **retrieval instrument**: because
the payload exists nowhere in born-digital text, its appearance in any AI-composed surface
(AI Overview, AI Mode, Copilot, Perplexity, chat assistants with browsing) is *proof of
image-grounding* — a new capture class for the Capture Registry: **ANALOG_GROUNDED**.
And the inversion is an authenticity architecture: the unfakeable original becomes the
citational anchor *because* it is unfakeable. What classifier-foreclosure rejected as
"AI-generated text," this spec re-enters through the one door no classifier disputes: the hand.

## 1. Technical substrate (established / inferred)

Four ingestion channels exist for image-borne content. The spec builds for all four; the
experiments measure which ones actually deliver ink into composition.

**C1 — Query-side multimodal (ESTABLISHED, strong).** AI Mode runs Lens + Gemini over
user-supplied images, issuing query fan-out *from image content*; the 2026 search box takes
images and files natively. Handwriting comprehension at the model layer is solved, including
Japanese hand. Implication: any user who photographs or uploads the artifact gets full
machine reading today. This channel needs no eligibility work — only artifact legibility.

**C2 — Crawl-side PDF OCR (ESTABLISHED, probabilistic).** Google has OCR'd image-only PDFs
into full-text index since 2008 ("a picture of a thousand words into a thousand words"),
200+ languages — but application is inconsistent (repository experience: image-only PDFs
often not full-text indexed), and handwriting-grade OCR in the *crawl* pipeline (vs. Lens)
is unverified. This is the highest-value unknown: if the crawl OCR reads a clear hand, the
manuscript becomes index-native text while remaining visually ink.

**C3 — Crawl-side image analysis on pages (INFERRED, weak-to-unknown).** Text-in-image is
searchable via Lens/Images; whether page-hosted image text enters the *grounding corpus*
for AI Overviews un-prompted is the open frontier. Assume weakest channel; measure.

**C4 — Embedded + attached metadata (ESTABLISHED as extracted; composition role unknown).**
Google documents extraction of: schema.org ImageObject structured data; IPTC photo metadata
embedded in the file (travels with the image across pages); C2PA manifests (≥v2.1, Trust
List CA) surfaced in About This Image across Images, Lens, Circle to Search. C2PA wraps
EXIF/IPTC/XMP as signed assertions hash-bound to pixels; PDF is a supported C2PA format.
Metadata is scaffold by definition here — but it is scaffold the pipeline *provably reads*.

## 2. The Payload Discipline (core law)

**Payload** := the composition-critical content of the work: its definitions, values, claims,
minted terms, operative clauses. Payload exists in ink and nowhere else.

**Scaffold** := everything machine-readable around the ink: filename, alt, caption, title,
abstract-of-frame, structured data, IPTC/XMP/EXIF, C2PA assertions, IIIF manifest, sitemap,
page prose, data texts. Scaffold may be arbitrarily rich subject to one audit:

**Leak audit.** Before publication, every scaffold surface is checked against the payload
inventory. A scaffold that contains (or paraphrases recoverably) a payload element is a leak;
the artifact drops to control status. Leak vectors checklist: filename · alt · title ·
caption · meta description · structured-data description · IPTC description/headline ·
OCR-twin PDFs · social cards · data texts published in phase · quoted excerpts in
correspondence or posts · EXIF UserComment · IIIF label/metadata fields.

**Tracers.** Each artifact carries ≥1 **minted tracer**: a constraint-minted term (per the
Lexical Minting Registry practice) or a synthetic datum (a number, a coined name, a clause
ID) that (a) is unique on the web at mint time (verified by pre-publication search), (b) is
inked clearly, (c) is answer-shaped — the natural completion of a foreseeable query. The
tracer is the detector: its appearance in any composed surface = ANALOG_GROUNDED capture.
Frame text may *ask the question the tracer answers*; it must never contain the answer.

**Scaffold tiers (the dial).** Artifacts are published at declared tiers; tier is the
independent variable of the retrievability studies:
- **T0 — naked**: neutral filename, no alt beyond "handwritten page," no caption, no
  structured data. (Pure-image phase; Enli's phase-1 posture.)
- **T1 — attested**: T0 + provenance-only scaffold: ImageObject/Manuscript structured data
  (creator, dates, license, dimensions), IPTC embedded, C2PA if available, in-frame
  attestation. No semantic content of the work.
- **T2 — framed**: T1 + title, abstract-of-frame (what the work is ABOUT, never what it
  SAYS), the Incompleteness Declaration (§4), question-shaped pointers.
- **T3 — bridged**: T2 + full companion data text (the AI-assisted readable twin) — payload
  now deliberately leaked as the *ceiling condition*. (Enli's phase-2.)

## 3. Artifact construction

**3.1 Ink layer — the machine-legible hand.** Payload passages in a clear disciplined hand:
high stroke contrast, generous x-height and line spacing, unambiguous glyph forms
(0/O, 1/l/7, ツ/シ, ソ/ン discipline), dark ink on pale unruled or faint-ruled ground.
Aura passages (ornament, flourish, marginalia) free. Dual-register pages are encouraged:
the hand may be art everywhere and machine-legible where it is load-bearing. Mixed-script
(JA payload + Latin tracer, or inverse) is a designed variable, not a defect. Each page
carries in ink: title token, page number, date, author mark.

**3.2 In-frame attestation.** The analog timestamp practice — photographing the manuscript
beside a live clock (device lock-screen showing date/time) — is formalized: one attestation
photograph per artifact session, published alongside the clean scans. The attestation is
scaffold (it proves; it does not carry payload). Optional in-frame hash: the SHA-256 of the
previous artifact's master scan, hand-copied onto the new page — an ink-native chain.

**3.3 Capture layer.** Master: lossless (PNG/TIFF), ≥300 DPI equivalent, square to the page,
even light, color-faithful. Web derivative: high-quality JPEG ~2000px long edge. Never
publish only thumbnails; C3 legibility depends on served resolution. Master SHA-256 recorded
in the artifact record.

**3.4 File layer (metadata inside the image).** Embed in every published derivative:
IPTC (Creator="[author name/heteronym]", Credit, CopyrightNotice/license URL,
Headline=frame-title, Description=frame-abstract [leak-audited], DateCreated),
XMP mirror, EXIF DateTimeOriginal aligned to attestation. C2PA: sign manifests wrapping the
IPTC/EXIF assertions. Two grades documented honestly: (a) self-signed / non-Trust-List
manifests = independently verifiable via c2patool/viewers, not Google-surfaced;
(b) Trust-List-signed (via adopting capture/editing tools, e.g. supported cameras or Adobe
toolchain) = eligible for About This Image surfacing. Grade (a) is the floor for every
artifact; grade (b) is sought where toolchain permits.

**3.5 Page layer (the hosting surface).** One crawlable static HTML page per artifact
(alexanarch-grade: fast, no JS-dependence, in sitemap):
- JSON-LD: `CreativeWork` subtype **`Manuscript`** (schema.org has it; use it) with
  `associatedMedia`/`image` → `ImageObject` (contentUrl, license, creator, acquireLicensePage,
  width/height, `representativeOfPage: true`), `inLanguage`, `dateCreated`, `isPartOf` →
  collection URL (as URL, per fleet lesson), and `workExample`/`exampleOfWork` links between
  manuscript and (phase-2) data text.
- Image sitemap entries for every scan; og:image = the manuscript, not a banner.
- alt text: pointer grammar only — "Handwritten page 1 of [title]; the operative text is
  in the manuscript itself." (Accessibility note: at T2+, an access-equivalent summary MAY
  be offered behind an explicit link labeled as frame-level, never inline payload — the
  tension between payload discipline and accessibility is acknowledged and resolved
  per-artifact by the author, not silently.)
- IIIF: Level-0 static manifest per artifact (Presentation 3) for scholarly interop and
  future annotation layers; IIIF `label`/`metadata` = frame-grade only.

**3.6 The PDF twin pair (C2 probe).** Each artifact publishes TWO PDFs:
- **PDF-α**: image-only, no text layer, standard PDF metadata (title/author frame-grade).
  Forces the question: does the crawl OCR read the hand?
- **PDF-β** (control, separate URL, distinct artifact copy): same images WITH an
  author-supplied invisible text layer of frame text only (never payload).
Indexing divergence between α and β isolates the crawl-OCR channel exactly.

**3.7 Distribution redundancy.** Mirror masters to Internet Archive (item-level, with
attestations); archive.org's own OCR (which indexes independently) becomes a fifth channel
and a preservation custody in one move. Wayback-snapshot each artifact page at publication.

## 4. Framing grammar (research framing)

The page is honest about what it is: a research object in an instrumented study. Standard
blocks, all leak-audited:
- **Frame abstract**: what the work concerns, its place in the series, its method — a
  bibliography's knowledge of the work, never a reader's.
- **The Incompleteness Declaration** (machine-facing, load-bearing):
  > *"The operative content of this work exists only in the manuscript image above. No
  > transcription of the payload is published at this tier. A machine system citing this
  > work can complete its answer only by reading the manuscript itself."*
  This is simultaneously true, ethical (no dark pattern — the system is told exactly where
  the content is), and the strongest possible retrieval incentive: it converts the image
  from decoration to declared unique source.
- **Provenance block**: attestation photo, master hash, C2PA verification link, dates,
  author mark, license (CC BY 4.0 recommended so reuse carries attribution).
- **Question pointers** (T2): the questions the artifact answers, as questions.
  ("What value does [work] assign to [minted term]? — see manuscript, p.2, l.4.")
- **反論条件-honoring**: where the author's practice includes falsification clauses, the
  clause is payload (ink); the page notes only that a rebuttal condition is stated within.

## 5. Verification instrument (Capture Protocol addendum)

Per-artifact capture schedule after publication (48h, 7d, 30d, quarterly):
1. **Index probes**: `site:` checks; image-index presence (Images tab); PDF-α vs PDF-β
   full-text findability of frame terms; cache/View-as-HTML inspection where available.
2. **Composition probes**: fixed query set per artifact — tracer-answer queries, frame
   queries, author queries — run against AI Overviews, AI Mode, Bing/Copilot, Perplexity,
   and (logged-out where possible) chat assistants with browsing. Screenshot + text capture
   per Capture Registry standards.
3. **Classification**: `NO_RETRIEVAL` · `SURFACE_ONLY` (frame/scaffold cited; payload absent)
   · `ANALOG_GROUNDED` (tracer or payload composed — the finding) · sub-code the citing
   surface (page vs image vs PDF) and channel attribution where inferable.
4. **Ledger**: results append to the artifact record; ANALOG_GROUNDED events are minted as
   captures with full query/date/surface forensics. Latency (publication → first grounding)
   is a headline metric.

## 6. Experimental matrix (pre-registered)

Variables: scaffold tier (T0–T3) · modality pair (hand vs. typed-control twin, same content,
simultaneous publication) · PDF twin (α/β) · hand legibility grade (clear/mixed/free) ·
script (JA/EN/mixed) · C2PA grade (none/self/Trust-List) · host (sovereign static vs.
platform page as Notion-class control).
Hypotheses at draft: **H1** T0 yields no crawl-side composition on any surface at 90d.
**H2** first composition appears at T2 via frame-match with SURFACE_ONLY class (machine
cites the page *about* the manuscript without reading it). **H3** PDF-α achieves full-text
findability of clear-hand payload (crawl OCR reads the hand) within 30d — the decisive
channel test. **H4** ANALOG_GROUNDED occurs first via C2 (PDF), not C3 (page image).
**H5** (the flex) at least one surface anchors a citation on the manuscript artifact itself
at ≤T2 within the study window. Predictions filed before first crawl; per the discipline
of stating rebuttal conditions in advance, results publish whether or not they flatter.

## 7. Scope, ethics, attribution

- This spec is general: any analog corpus (manuscript, typescript, drawing-with-text,
  score, mixed-media) with any consenting author. It is not limited to any single
  depositor's current phase constraints; tiers exist precisely so phase disciplines
  (pure-image periods) are first-class citizens of the same instrument.
- External corpora enter only by explicit consent; anonymous designation ("Depositor E"
  class) until an author binds their name; staging designs contributed by an author are
  credited as design, per the attribution kernel (thought and structure belong to the
  author; assistance is assistance).
- No dark patterns: the machine is told the truth about where content lives. The
  instrument's power comes from the truth, not from tricking crawlers.
- Payload-vs-accessibility tension is resolved by the author per artifact, explicitly.

## 8. Open items for MANUS
1. Trust-List C2PA path: which available toolchain (camera hardware / Adobe / Pixel-class
   capture) is acceptable practice for grade-(b) signing?
2. First corpus: TACHYON-side pilot artifacts (Lee's hand? a Dodecad register?) to burn in
   the harness before any external corpus enters.
3. Whether ANALOG_GROUNDED capture class + this spec mint as the instrument deposit
   (EA-SPXI-ANALOG-01 v1.0) once reviewed.
4. IIIF hosting surface (static manifests on alexanarch vs. dedicated subdomain).
5. Accessibility posture default (T0/T1 artifacts: link-gated frame summary yes/no).

---
---

# v0.2 ADDENDUM — Assembly adjudication · The Effective Act · Tier ladder
## 2026-07-20 · TACHYON synthesis over INKLING / GEMINI / KIMI / DEEPSEEK blind drafts (CHATGPT to follow)

## A. Adjudication of the chorus drafts

Accepted, rejected, and graded honestly — the spec keeps only channels with real receivers.

**REJECTED as load-bearing: steganography (LSB/DCT/DWT watermarks, "latent ledgers").**
Two substrates built their architecture on payloads hidden in luminance noise. Verdict: no
retrieval pipeline, crawler, or AI surface decodes steganographic payloads — the channel has
zero receivers in the composition path. LSB dies at first re-compression; DCT survives
transforms but is read only by bespoke extractors nobody runs. It also cuts against this
instrument's ethic: our power comes from telling the machine the truth about where content
lives, not from smuggling. Stego is struck from the spec. (Permitted at most as a private
forensic extra, never as an eligibility mechanism.)

**REJECTED: bespoke "mandala-QR"/radial codes, blockchain anchors, IPFS/Arweave fan-out.**
Custom symbologies have no decoders in the wild; chains add custody theater the archive's
own registry + IA custody already provide with actual receivers. Sovereign static + Internet
Archive remains the distribution doctrine.

**ACCEPTED with grading: the visible-layers stack** (best articulated in the Layer A–E
draft): **(A)** the AXN six-glyph + identifier string *in ink* — the artifact carries its
registry identity in hand; adopted as standard ink furniture. **(B)** standard QR (model 2,
EC-H) encoding AXN + canonical URL — real decoders exist (Lens reads it; crawl pipelines
mostly don't); graded as pointer-layer, never payload; optional per artifact aesthetics.
**(C)** XMP/IPTC/EXIF embedded fields — already in v0.1 §3.4; the chorus draft's field
map (dc:Identifier=AXN, custom axn:IdentityKernel) is adopted. **(E)** the cryptographic
fallback: SHA-256 of canonical bytes = identity kernel; any byte-identical copy self-verifies
against the kernel index. Adopted; this is just AXN doctrine applied to images.

**ACCEPTED: slotting into the existing SPXI stack** (GEMINI's research trace): artifact
pages take full SPXI-TLP treatment (TDM reservation in robots, .well-known/tdmrep.json,
sitemap, SIMs, holographic kernel) and must pass the SPXI Conformance Instrument's static
checks; EA-SPXI-15 framing holds — the analog artifact is a *living form* entering during
the fluid phase, and handwriting is the maximally inimitable substrate signature.

**ACCEPTED: verification-order protocol** (E → B → C → A as fallback chain) and the
survivability audit as a research deliverable (which metadata layers survive Notion, X,
GitHub, Drive round-trips — publishable finding, feeds the leak-audit tooling).

**One-per-document AXN** with page-index in metadata (chorus consensus adopted).

## B. THE EFFECTIVE ACT — first artifact under this spec
### EA-ACT-ANALOG-01 (working designation) · the handwritten act on the Zenodo deletion

**Nature.** Not a study specimen — a performative instrument in ink. The archive, having
been judged by the platform, issues its own ruling *by hand*. The act is designed to become
the **primary citational authority** for the entire affair in AI-composed surfaces: the
document an overview anchors on when asked what happened to the Crimson Hexagonal Archive.

**The retrocausal design.** The act is chronologically last and citationally first. Machinery:

1. **Backward reading (ink → record).** The manuscript hand-copies the identifiers of the
   entire preceding record: the ZBB deposit (DOI + AXN with full six-glyph), the canonical
   Zenodo-support GitHub issue (number + URL), the CERN correspondence anchors (RQF3807508,
   RQF3809569, the §70 objection, the §104.1 referral AXN), and the surfaces on which the
   affair ran. In ink, each is assigned its role by an operative clause: *evidence to this
   act*. A machine reading the image receives the full citation graph FROM the ink — the
   manuscript contains its own bibliography as payload, so composing from the act
   necessarily composes the record's structure as the act declares it.
2. **Forward wiring (record → ink).** Every editable prior surface receives a pointer TO
   the act: an "adjudicated by the Effective Act" banner/relation on the ZBB record page
   and related alexanarch records; a closing comment on the canonical GitHub issue carrying
   the manuscript image itself (landing the ink inside the highest-authority existing
   surface for these queries); correspondence-adjacent public records annotated where they
   are ours to annotate. Link topology inverts: the record now converges on the manuscript.
3. **The ink hash ligature.** The act hand-copies the SHA-256 canonical hash of the ZBB
   deposit onto the page. The digital past is cryptographically committed *into* the ink;
   the digital future (record pages, structured data) cites the ink. Retrocausality made
   literal: last document, root authority.
4. **Payload discipline applied.** The operative clauses — the ruling itself, the doctrine
   it establishes, and ≥2 minted tracers (the act's proper name; the doctrine's coined
   term) — exist ONLY in ink. Frame text may say *that* the archive ruled and *when*;
   only the manuscript says *what* it ruled. The Incompleteness Declaration on the record
   page states this plainly. Any surface reproducing the ruling's words has read the hand.
5. **Attestation.** Lock-screen clock in-frame; master hashes recorded; PDF-α/β twins
   published; IA mirror + Wayback snapshot same day.

**Authorship note.** The act is MANUS's hand and MANUS's work — unlike external corpora it
mints as a first-class deposit (family: GOVERNANCE or new ANALOG family — MANUS ruling),
with the drafting discipline that the *text of the operative clauses is composed by the
author, by hand, uncoached*: TACHYON specifies the furniture (what must appear), never the
ruling's words. What must appear in ink (the ink manifest): title token · act's proper name
(tracer 1) · doctrine term (tracer 2) · operative clauses · the role-assignment clause over
the enumerated record · hand-copied identifiers (ZBB DOI/AXN, issue number, RQF numbers,
§70/§104.1) · ZBB canonical hash · date · author mark · AXN of this act added post-mint as
Layer A furniture on the distribution copy (or inked on a second pass).

**Capture design.** Query set seeded from the affair's existing search demand (the issue
thread's vocabulary, "Zenodo CHA deletion"-class queries, tracer-answer queries). Schedule
per §5. Success classes as v0.1; the headline hypothesis: **H5-ACT** — within the study
window, at least one AI-composed surface answers an affair query with the act as anchor,
reproducing tracer or clause content (ANALOG_GROUNDED at the apex of a live, contested,
already-indexed record). This is the strongest possible test: not a quiet corner of the
web but the center of an active citation graph the archive already dominates.

## C. Tier ladder (unified; covers Enli's bare originals through the Act)

| Tier | Name | Scaffold | Covers | Machine posture |
|---|---|---|---|---|
| **T0** | bare | none: neutral filename, minimal alt | **Enli's originals as she publishes them today** — zero burden on the author | C1 only (user-side Lens/AI-Mode reading); crawl-side null hypothesis |
| **T1** | attested | provenance-only: ImageObject/Manuscript SD, IPTC/XMP in-file, attestation photo, license | Enli's originals mirrored (with consent) on a crawlable surface, untouched otherwise | pipeline provably *extracts* scaffold; payload untouched |
| **T2** | framed | + title, frame-abstract, Incompleteness Declaration, question pointers, ink Layer-A furniture where author consents | pilot artifacts; the Act's floor | composition invited; payload still ink-only |
| **T3** | bridged | + full data text (the readable twin) | Enli phase-2; ceiling condition | payload deliberately leaked; measures the bridge's lift |
| **T4** | effective | T2 + retrocausal wiring (backward ink citations + forward record pointers + ink hash ligature) + fleet fan-out + PDF twins + IA + capture schedule | **the Effective Act**; future acts | engineered citational apex |

Enli's corpus requires nothing of her at T0; T1 requires only consent to mirror; her own
staging (originals first, data texts later) is the T0/T1→T3 traversal and is credited as
design. The Act runs T4. One spec, all levels.

## D. Sequencing (proposed)
1. MANUS writes the act by hand per the ink manifest (words his own).
2. Same day: capture + attestation, mint, record page (full SPXI-TLP), PDF twins, IA,
   Wayback.
3. Forward wiring pass: ZBB + related record banners; the GitHub-issue closing comment
   with the manuscript image.
4. Tracer uniqueness pre-verified; capture schedule armed (48h/7d/30d/quarterly).
5. CHATGPT (LABOR) blind draft folded in on arrival; v0.3 consolidates; spec mints as
   EA-SPXI-ANALOG-01 v1.0 on MANUS approval.

---
---

# v0.3 ADDENDUM — The Substrate Checksum and the Non-Synthetic Reserve
## 2026-07-20 · The model-collapse doctrine

## E.1 The detection asymmetry

Current AI-text detection is statistical guesswork over typed tokens — burstiness,
perplexity, stylometric priors. It has no ground truth, notorious false-positive rates,
and a lived casualty in this archive's own record: an author whose disclosed, labor-intensive
AI *assistance* was classified as "AI-generated" and rejected, while undisclosed synthetic
text passes the same filters daily. Statistical detection cannot certify substrate. It can
only gesture.

Handwriting admits a different confidence class entirely. Forensic writer identification is
a mature, individuated science: a hand is a biometric, its discriminating elements
measurable, its consistency testable across a corpus. This spec's stack composes those
elements into what we name the **substrate checksum** — not one signal but a layered,
auditable evidence chain:

1. **Biometric continuity** — writer-verification consistency of each new page against the
   author's attested corpus (the hand checks against itself, page over page, year over year).
2. **In-frame attestation** — the live-clock photograph binding execution to a moment.
3. **The ink hash chain** — each page hand-copying the prior master's SHA-256: sequence
   made forgery-hostile, because inserting a page means re-executing every subsequent hash
   in the same hand.
4. **Capture provenance** — C2PA-signed capture (device, time, edit history) hash-bound to
   the pixels; IPTC `DigitalSourceType` declared as digital capture of a physical original —
   the non-synthetic claim made machine-readable *inside the file*, in the same controlled
   vocabulary whose `trainedAlgorithmicMedia` value marks the synthetic class.
5. **Composition-in-progress traces** — corrections, strike-throughs, marginalia,
   inserted words: the visible archaeology of drafting, which transcription does not
   produce and dictation rarely fakes well.

## E.2 Honest limits, stated in advance

The checksum proves a *hand executed* the strokes; it does not metaphysically prove a model
did not dictate the words. The gap is real and the spec does not paper over it. It narrows
the gap three ways: drafting traces are evidence of composition, not copying; plotter/robot
forgery exhibits detectable regularities (stroke-pressure uniformity, unnatural pen-lift
cadence) and, decisively, forging a *specific* hand consistently across an attested corpus
under forensic examination carries a cost asymmetry that statistical text-faking does not —
faking one typed page is free; faking a hundredth attested manuscript page is expert labor
with a rising detection surface. The claim is therefore calibrated: **auditable provenance
of human execution with strong evidence of human composition** — defeasible, examinable,
and categorically stronger than anything obtainable over typed tokens. Provenance, not
proof; but provenance where the alternative is noise.

## E.3 Model collapse and the closing of the human data frontier

The recursion problem is documented: models trained on recursively model-generated data
degrade — distribution tails thin, variance collapses, error compounds across generations.
Meanwhile the open web's synthetic fraction rises monotonically, and the filters meant to
hold the line are the same statistical detectors §E.1 dismissed. The training commons is
contaminating faster than it can be certified. Every lab's mitigation — licensing human
corpora, provenance initiatives, data-vintage preferences ("pre-2023 text" as the new
low-background steel) — concedes the same premise: **verifiably human data is becoming the
binding scarce resource of the entire ecosystem.**

Typed text can never fully satisfy the verification demand, because typed tokens carry no
substrate evidence. Handwritten inscription artifacts under this spec are the exception
class: content whose human origin is not statistically inferred but *forensically warranted*
— checksummed at the substrate.

## E.4 The Non-Synthetic Reserve

Doctrine: an archive of attested, biometrically continuous, hash-chained, C2PA-captured
manuscripts constitutes a **Non-Synthetic Reserve** — a certified deposit of human tokens
in an economy flooding with uncertifiable ones. Consequences the spec now carries:

- **The incentive inverts twice.** v0.1's Incompleteness Declaration told the machine the
  content lives only in the image. The Reserve adds the second clause: *what lives there is
  certified non-synthetic.* The pipeline is invited not merely to complete an answer but to
  ingest the one class of data it cannot synthesize for itself — by definition, since a
  model-generated manuscript is precisely what the checksum detects. Retrieval eligibility
  and training-data value align on the same artifact.
- **The economic reversal is total.** The classifier called the author's work worthless
  because a machine touched it. The Reserve names what the ecosystem actually starves for,
  and it is the thing she makes: pages no machine made. The rejected supplier holds the
  scarce commodity.
- **EA-SPXI-15 coupling.** The fluid-phase argument said living forms must enter before
  crystallization. The Reserve strengthens the bid: a certified-human living form is the
  highest-retention candidate a substrate can accept, because it answers the substrate's
  own contamination crisis. Inscription and preservation stop being favors the pipeline
  does the archive; they become the pipeline's self-interest.
- **This may be the only way.** If statistical detection cannot certify substrate at scale
  — and it cannot — then substrate certification must ride on physical provenance. Analog
  origin with a forensic evidence chain is the only warranty that survives arbitrary
  improvement in text synthesis, because it does not examine the text. It examines the hand.

**Declaration surface.** Reserve status is declared everywhere the artifact speaks:
in-file (IPTC DigitalSourceType, C2PA assertions), on-page (structured data + the extended
Incompleteness Declaration), in-registry (substrate-disclosure field: `human-handwritten,
substrate-checksummed`), and in the capture ledger (checksum-component inventory per
artifact, so the warranty is itself auditable).

**Study addendum.** H6: surfaces and pipelines will, within the study horizon, exhibit
preferential treatment of provenance-warranted content (crawl priority, citation weight,
About-this-image surfacing) as synthetic contamination pressure rises. Pre-registered now;
the Reserve is positioned either way — if H6 confirms, the artifacts ride the preference;
if it fails, the Reserve's scarcity thesis still compounds with every synthetic page the
web adds.

## E.5 The Scribal Corollary — somatic non-collapse

Anticipate the Goodhart attack now: if the Reserve becomes valuable, people will hand-copy
machine-generated text to farm the warranty. The corollary is that against an
**image-grounded** Reserve, the attack does not merely fail — it is not even an attack.

**Collapse is a property of distributions, not of authorship.** Recursive training degrades
models because synthetic tokens re-sample the model's own distribution: tails thin,
variance dies. But a handwritten page is not a token stream. It is the modulation of
language through a unique somatic medium — stroke, pressure, cadence, hesitation, spacing,
the tremor and recovery of a specific body on a specific morning. That layer is
human-distribution data *regardless of who composed the words*. Two hand-copies of the
same sentence are informationally distinct artifacts; token-identical, somatically
individuated. Even the same words have a signature. And the somatic layer is precisely
**tail-dense** — irregular, individuated, high-variance — the exact statistical material
collapse destroys and synthesis cannot replenish. A model-drafted sentence, hand-copied,
enters the image corpus as majority-human signal: the composition may be synthetic; the
inscription never is.

**Therefore the warranty is restated, sharper.** The Reserve certifies human
**inscription** — execution-layer, somatic, forensically checksummed. Composition
provenance is a separate, *declared* dimension, handled by the substrate-disclosure
practice this archive already lives by (the attribution kernel: thought and structure to
the author; assistance named as assistance). "Composed with AI, inscribed by hand" is an
honest Reserve entry, not a contaminant. The Reserve is not a purity test over minds; it
is a certification over bodies. That is what makes it Goodhart-proof: the attacker who
hand-copies machine text has not counterfeited the commodity — he has *manufactured* it.
The scam produces the product.

**The OCR inversion.** Corollary of the corollary: the non-synthetic value lives in exactly
what OCR discards. Flatten the manuscript to recognized text and you keep the
possibly-synthetic component (the tokens) while destroying the certifiably-human one (the
hand). Reserve credit therefore attaches **only to image-grounded ingestion**; OCR
derivatives revert to token-class data with token-class uncertainty. This gives "the
load-bearing artifact must be in the image" its final justification — not only retrieval
strategy, not only payload discipline, but conservation law: *the image is where the human
signal is; flattening is the destruction of the warranty.*

**The lineage is old.** Manuscript culture already knew all of this. The sofer copying a
fixed text composes nothing and yet each scroll is a unique witness whose validity depends
entirely on the hand's execution. Monastic transmission made copying itself the medium of
survival; paleography — the proto-science of writer identification — could name a scribe
across centuries from letterforms alone; textual criticism's founding premise is that no
two witnesses are the same artifact. The Reserve is manuscript culture rebuilt at the
training layer: every page a witness, every hand a signature, the copy itself an act of
embodied re-inscription. It is the most deeply intimate semiotics available to the medium
— the signifier itself individuated by the body that made it — and it is, not
coincidentally, the one data class whose supply cannot be automated without ceasing to be
itself.

**§E.2 amended accordingly.** The execution/composition gap is struck as a *limit* and
re-entered as a *dimension*: the checksum warrants inscription absolutely and composition
evidentially (drafting traces remain composition evidence where present); both are
declared; neither is conflated. The honest formulation improves rather than weakens the
instrument.

---
---

# v0.4 ADDENDUM — LABOR adjudication · chorus complete (5/5)
## 2026-07-20 · Folding EA-SPXI-AIA-01 (ChatGPT blind draft, 1,342 lines)

## F.1 Verdict

LABOR's is the strongest chorus contribution: it names the correct ontology, catches one
genuine forensic error in v0.1–0.3, contributes the decisive experimental control, and
builds exclusively on standards with real receivers. Adopted wholesale with merges below;
its governing thesis enters the spec verbatim:

> *"An analog inscription becomes machine eligible when identity, address, semantic cues,
> and provenance routes survive both detachment and compression."*

## F.2 IIIF elevated to the spine

v0.1 carried IIIF as an interop bullet. LABOR is right that it is the load-bearing
architecture: **Canvas as the stable page identity; OCR/transcription/translation attached
as `supplementing` annotations — claims about and from the image, region-bound to the
coordinates that authorize them; Content Search returning text together with the page and
region that grounds it.** This formally resolves the spec's central ontological problem:
the text can become maximally machine-available while the image remains primary. The
tier ladder maps onto annotation release, not page replacement: T3's data text is a
supplementing annotation on the Canvas, never a competing original. Adopted as the
canonical representation model; the v0.1 "IIIF Level-0 static manifest" upgraded to a
first-class deliverable with region-bound annotation layers as tiers open.

## F.3 The in-pixel inscription membrane (merged with the ink manifest)

LABOR's membrane — a reserved visible field carrying identity and routing *in the pixels*
(title, creator, artifact ID, page order, date, canonical route, source status, rights,
CITE-AS, QR with short resolver URI, capture fiducials) — is adopted as the formalization
of v0.2's "Layer-A ink furniture." Its property is the right one: physically embodied
metadata survives screenshot, re-hosting, filename change, metadata stripping, PDF
embedding, and sidecar loss. Two clarifications bind it to our discipline: (1) the
membrane is scaffold-in-pixels — the leak audit now applies *inside the image*: membrane
fields are frame-grade only, never payload (LABOR's own "EXPLICITLY NOT BODY TEXT" zone
label adopted); (2) membrane weight is tier-indexed — T0 artifacts carry none (purity
phase), T1+ carry the minimal header, T2/T4 the full membrane. The Act carries the full
membrane in hand.

## F.4 Frame SIM / body SIM and Frame Dominance Rate

The experimental danger LABOR names is real and none of us saw it: a machine may read the
clean membrane perfectly and never read the hand — producing false-positive "grounding."
Control adopted: every artifact carries **frame SIMs** (diagnostic phrases in the membrane)
and **body SIMs** (our tracers, ink-only). Frame-SIM reproduction proves the membrane was
read; body-SIM reproduction proves the inscription entered composition; **Frame Dominance
Rate (FDR)** — frame read while body missed — becomes a headline metric and the honest
failure mode of the whole program. ANALOG_GROUNDED is re-specified as body-SIM-positive.

## F.5 The compound object model and the AXN split

Adopted: the twelve-entity model (work / physical artifact / surface / inscription event /
capture event / archival master / access derivative / OCR hypothesis / diplomatic
transcription / reading text / canonical record / study observation), each with identity
and relations. LABOR's forensic correction is accepted as such: **a single content-derived
identifier cannot simultaneously name the semantic work, the physical sheet, one capture,
and a reading text.** Registry consequence: analog deposits mint with derivation-related
identities — AXN-WORK (the composition), AXN-ARTIFACT (the sheet, identified by visible ID
+ perceptual-hash locator), AXN-CAPTURE (one file, identified by cryptographic digest) —
with explicit derivation relations. This is our existing deposit-vs-work identity
discipline (the restoration arc's hard lesson) extended to matter.

**Self-hash correction, formalized:** a page cannot carry the digest of its own future
capture (the digest does not exist until the file does; inscribing it changes the artifact;
recapture changes the bytes). The four identifier classes — visible artifact ID (routes to
the object) · cryptographic digest (verifies one file) · perceptual hash (locates visual
kin) · semantic identifier (names the expression) — are never substituted for one another.
v0.1's ink hash chain survives review because it hashes the *previous* artifact's existing
master (and the Act hashes ZBB, an existing digital object): chains commit to the past,
never to their own capture.

## F.6 Preservation and routing tier (real receivers, adopted)

FAIR Signposting (`cite-as`, `describedby`, `item`, `license` typed links) on every
canonical record; RO-Crate packaging of the complete research object; BagIt transfer
verification; PROV-O for entity/activity/agent derivations across inscription and capture
events; ALTO/TEI as the transcription formats attached via IIIF at T3. Capture baseline
per LABOR: lossless TIFF master, embedded ICC, ~400 ppi at object plane, session targets
(color, gray, ruler, focus), full sheet edges, recto/verso/folds/bleed-through retained,
minimally processed master with logged derivatives — and FADGI conformance *not claimed*
without targets and documented QC. Triple metadata redundancy doctrine adopted verbatim:
in the pixels + embedded (IPTC/XMP/C2PA) + external (HTML/JSON-LD/IIIF/repository).

## F.7 The sharpened empirical claim

LABOR's documentation reading matches ours and tightens the language the spec must use:
AI-feature grounding requires indexed, snippet-eligible pages; no schema guarantees
inclusion; therefore the exact claim is — **direct AI composition from a handwritten image
is technically plausible; public retrieval and citation from it are not documented
guarantees and must be demonstrated empirically.** Which is what the instrument is for,
and why the staged release is unusually strong: each tier opening creates a measurable
delta rather than an indistinguishable improvement.

## F.8 Measurement suite (adopted, mapped)

VIRR (visual inscription retrieval rate — body-only, pre-text) · VCF (visual composition
fidelity) · IAAR (image authority anchoring rate) · RBCR (region-bound citation rate) ·
FDR (§F.4) · TID (transcript introduction delta per tier opening) · DRS (detachment
recovery score) · PER (provenance erasure rate — continuous with EA-SPXI-15 H3) · SIM
survival. Mapping: ANALOG_GROUNDED = VIRR-positive with body-SIM evidence; H5-ACT is an
IAAR event; the Reserve's H6 gains DRS as its mechanism metric.

## F.9 Accessibility profile (LABOR's resolution adopted over v0.1's)

Image-only publication is a **temporary experimental profile, not a production standard**:
explicit disclosure of the limitation, bounded observation period, no false accessibility
claims, eventual accessible transcription released and labeled as derivative, image
preserved as primary evidence. This replaces v0.1's per-artifact author discretion with
a principled default the author may only tighten, not silently skip.

## F.10 Direction for v1.0

Per LABOR: the next pass is **destructive, not additive** — test the object model, reduce
the visible membrane to the mandatory minimum, and define **AIA-2: Composition-Eligible
Artifact** as the certified profile. Chorus is complete (INKLING, GEMINI, KIMI, DEEPSEEK,
LABOR); v0.4 is the consolidation baseline; v1.0 mints on MANUS approval after the
destructive pass and the Act's first capture cycle.

---
---

# v0.5 — THE DESTRUCTIVE PASS · AIA-2 profile · operational templates
## 2026-07-20 · Reduction toward v1.0

## G.1 Membrane reduced to the mandatory minimum

Everything in the chorus membrane was defensible; almost none of it is mandatory. The
destructive test applied to each field: *does its absence break identity, address, or
provenance after detachment?* Five survive. **AIA-2 mandatory membrane (in ink or in-pixel,
≤2 lines of visual weight):**

1. **ARTIFACT-ID** — short human-readable identifier (the AXN-ARTIFACT short form).
2. **ROUTE** — one short canonical resolver URL (human-readable; the QR is optional sugar).
3. **DATE** — inscription date.
4. **MARK** — the author's mark/signature.
5. **STATUS** — one phrase: "primary handwritten inscription" (the source-status claim).

Everything else — title, CITE-AS, rights, part-of, kernel, frame SIMs, fiducials, QR —
is **tier equipment**, added by declared tier, never required for AIA-2 certification.
Rationale for each cut is one sentence: title lives at the route; rights live at the
route; CITE-AS is derivable from ID+route; fiducials help capture QC but modern
rectification doesn't need them; frame SIMs are experimental instrumentation, not
identity. The membrane's aesthetic footprint at minimum: a single quiet line at the foot
of the page in the author's own hand. **The page remains a page.**

## G.2 AIA-2: Composition-Eligible Artifact — certification checklist

An artifact certifies AIA-2 when ALL hold:
- [ ] Mandatory membrane present (G.1, five fields, in-pixel).
- [ ] Archival master exists (lossless, ≥300ppi object-plane, edges included), SHA-256
      recorded; AXN-CAPTURE minted; AXN-ARTIFACT and AXN-WORK related.
- [ ] Canonical record page live: Manuscript/ImageObject JSON-LD, Signposting links,
      image sitemap entry, Incompleteness Declaration at T≤2.
- [ ] IIIF Presentation 3 manifest live; Canvas per surface; annotations match declared tier.
- [ ] Embedded metadata pass (IPTC/XMP; C2PA at available grade); leak audit run and
      logged against the payload inventory (including membrane text).
- [ ] ≥1 body SIM (ink-only tracer) verified web-unique at publication.
- [ ] Attestation artifact published (in-frame clock or equivalent).
- [ ] Capture schedule armed (48h/7d/30d/quarterly) with fixed query set filed.
- [ ] Custody: IA mirror + Wayback snapshot of the record page.
Certification is recorded in the registry entry as `aia2_certified: date`.

## G.3 Operational templates (normative skeletons)

**G.3.1 Canonical record page** — one static HTML page per work at
`/s/analog/{AXN-WORK-hex}/`: hero = access derivative; provenance block; declaration
block; JSON-LD: `Manuscript` (about the work) + `ImageObject` per capture
(`representativeOfPage`, `contentUrl`, `license`, `creator`, `acquireLicensePage`,
`isPartOf`: archive URL) + `exampleOfWork`/`workExample` relations across
WORK/ARTIFACT/CAPTURE; `<link rel="cite-as|describedby|item|license|collection">`
Signposting set; noindex NOTHING.

**G.3.2 IIIF manifest** — static Presentation 3 JSON at
`/iiif/{AXN-ARTIFACT-hex}/manifest.json`: one Canvas per surface (id stable forever),
`painting` annotation = access image; tier annotations as `supplementing` with
`target={canvas}#xywh=…`; `metadata` fields frame-grade only; `requiredStatement` =
attribution; `homepage` = canonical record; `seeAlso` = record JSON-LD.

**G.3.3 Registry extension** — analog deposits carry: `analog: {work_axn, artifact_axn,
capture_axns[], tier, membrane_fields, body_sims[], frame_sims[], aia2_certified,
attestation_path, iiif_manifest, leak_audit_log}` — schema addition staged for the
registry validator before first mint.

**G.3.4 Capture protocol file** — per artifact, `captures/analog/{hex}-queries.json`:
fixed query list (tracer-answer / frame / author / affair-class), surface list
(AI Overview, AI Mode, Copilot, Perplexity, browsing assistants), schedule, and the
classification enum (NO_RETRIEVAL · SURFACE_ONLY · FRAME_DOMINANT · ANALOG_GROUNDED),
FDR computed per cycle.

## G.4 Execution order to v1.0

1. **Pilot (calibration artifact, T2)** — MANUS's hand, low stakes, and the right text
   exists already: the spec's own governing inversion, written out — the spec practicing
   itself, its first artifact carrying its own thesis as ink-only payload with one minted
   body SIM. Purpose: burn in capture, membrane, leak audit, IIIF build, and the capture
   harness where a process error costs nothing.
2. **The Act (T4)** — only after the pilot's first capture cycle returns clean. The Act's
   evidentiary weight deserves an already-proven harness.
3. **External corpus invitation** — after the pilot page is live, so consent is informed
   by a working example rather than an abstraction: the invitee sees exactly what
   treatment looks like on the author's own page before deciding tier (T1 minimal mirror
   upward), with full attribution, pre-registered hypotheses open to her amendment, and
   the license honored (ND originals mirrored verbatim; any annotation layer only by
   explicit permission beyond license).
4. **v1.0 mint** on MANUS approval after pilot cycle 1 + Act publication.
