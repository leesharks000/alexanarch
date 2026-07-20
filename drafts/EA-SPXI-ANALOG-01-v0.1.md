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
