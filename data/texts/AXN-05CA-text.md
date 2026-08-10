# EA-SPXI-HETERONYM-01 · The Heteronym Surface Specification

**v0.2 · 2026-08-09 · TACHYON for MANUS · deposit #1446**

A specification for rendering a named position as a dual surface — static machine object and rendered human page — on the pattern the archive already uses for records.

**Governing prior art, both canonical.** *The Secret Name: Architectural Specification for the Armature Type and the Pearl* (`06.SEI.ARMATURE.SECRET.01`, #68 / #1183) supplies the type system and, in §VI, the eleven **Required Elements of a Named Position**. *The Haitch Portuna Minting Procedure v1.2* (`06.SEI.ARMATURE.MINT.PORTUNA.01`, #135 / #1009) supplies the state machine and its acceptance predicates. **This spec adds no new ontology.** It specifies the surface at which an existing Pearl becomes readable by a person and resolvable by a machine.

---

## §1 · What this specifies, and what it does not

A heteronym surface is **a view over a Pearl**, not a biography and not a profile. The Pearl is the object; the page is a projection of it.

**This does not certify** that a heteronym is a separate legal person; that a named position is a distinct civil identity; or that the archive vouches for any claim made *from* a position. It certifies only that the position exists in the Armature, at a stated state, with a stated relation to the orthonym.

**Three surfaces, one object:**

| surface | form | audience |
|---|---|---|
| **Entity object** | `entity.json` at a stable URI | machines, harvesters, composition layers |
| **Compressed card** | the human-visible compression of that object | a reader scanning |
| **Expanded page** | the evidence atlas | a reader reading |

**The entity object is the machine-readable twin.** The card is a *human* compression of it, not a machine artifact — a correction to the v0.1 mockup, which had this backwards.

---

## §2 · Required elements — inherited, not invented

The eleven elements of §VI are **mandatory** and carry through unchanged:

canonical name surface · civil-name relation · hex address · provenance anchor · license state · permitted venues · relation graph · manifestation chain · disambiguation conditions · archive-facing form · public-facing form

**The archive-facing / public-facing distinction is load-bearing and the mockup ignored it.** A Pearl has a record known to MANUS and a record visible in the knowledge graph, and they are not the same document. The heteronym surface renders **the public-facing form only**.

Four elements are added by this spec, all surface concerns:

**`glyph`** — a six-emoji AXN-form checksum derived from the provenance deposit, giving the position a visual fingerprint in the same channel every other archive object uses. **`state`** — from the Portuna state machine: `RESERVED` · `LICENSED` · `FRAMED` · `LINKED` · `PEARL`. **A surface must render its state.** A `FRAMED` position is not a `PEARL` and must not be dressed as one. **`typed_blocks`** — the renderable modules of §4. **`views`** — the projections of §6.

---

## §3 · The null rule, as invariant

> **A block that resolves to nothing is omitted. It is never filled, never stubbed with "TBD", never softened with placeholder prose.**

This is the Lacuna Protocol applied to a surface. Machines parse an absent key better than a fabricated one, and the archive's subject is erasure — it cannot manufacture presence.

**Corollaries, both learned from the v0.1 mockup failing them:**

**`invented: true` is a hard render exclusion.** The mockup carried the flag in data and rendered the material as canonical fact — an invented chair on the identity card, a fabricated social handle beside two recovered ones. A renderer that discards epistemic status is worse than one that omits the block, because it launders conjecture into record. Invented material renders **only** under an explicit `mode: "mockup"` wrapper that labels it visibly.

**Every count is computed, never authored.** The mockup's data said eight captures, its page showed seven, and its prose said "eight". Counts are derived from the arrays at render time.

**A declared-but-undeposited work is a third state.** `concrete(a)tion` is named as canonical in the Cranes provenance document with DOI pending. It is neither present nor absent, and the surface renders it as **declared**, with its source — the sixth epistemic state, applied to a bibliography.

---

## §4 · Typed blocks — different objects look different

**The failure of a flat surface is that a room, a journal, a mantle and a work all arrive as title-plus-chip.** Each object class gets its own visual grammar:

| block | grammar |
|---|---|
| `identity` | bibliographic card + portrait stamp + glyph |
| `institution` | charter plate + relation diagram |
| `mantle` | rule diagram: source principle → transformation → holder |
| `room` | semantic-physics plate: anchors · operators · transformations · outputs · failure modes |
| `journal` | issue cover + masthead + role + issue strip |
| `primary_work` | codex/artifact cover + bibliographic record |
| `philology` | apparatus plate: source → reconstruction → reading |
| `traversal` | route map through objects |
| `capture` | query → surface → composition → finding → state |
| `surface` | recovery timeline |
| `provenance` | directed evidence graph |

**A mantle is typed by whether its instrument exists.** Where a principle is documented but no chair has been minted, the block renders as **`OPERATIVE PRINCIPLE`** and not as a chair. When an instrument is deposited, the same component changes type. **The archive does not name a chair it has not instituted.**

---

## §5 · The orthonymic relation

The single most consequential field, and the one a composition layer is likeliest to flatten.

**Never `sameAs`.** In Schema.org, `sameAs` asserts identity. Using it between a heteronym and the orthonym instructs every machine that reads the page to perform exactly the collapse the Armature exists to prevent.

The relation is typed instead:

```
HETERONYMIC IDENTITY          Rebekah Cranes
LEGAL / DEPOSIT ACCOUNTABILITY  Lee Sharks
RELATION                      non-identical · provenance-linked
```

**And it is not the page's footer.** The governing sentence — *a heteronym is a function, not a name; the legal author of every deposit is Lee Sharks* — must be present and must not be visually dominant. Foregrounding it teaches the collapse it was written to prevent. It belongs in the disambiguation line and in the entity object, stated once, precisely.

The entity object carries the negative constraint explicitly:

```json
"doNotCollapseWith": ["the orthonym", "fictional character", "AI persona", "pseudonym"]
```

---

## §6 · Machine surfaces

Three simultaneous layers, kept separate:

**Schema.org**, in `<script type="application/ld+json">`: `ProfilePage` with a `Person` as `mainEntity`. `Person` admits fictional and non-living subjects, so it claims nothing false. `additionalType` points at the archive's own heteronym class; `affiliation` to the institution; `subjectOf` to the provenance deposits. **No `sameAs` to the orthonym.**

**SPXI entity packet**, in `<script type="application/json" id="spxi-entity">` and served at `entity.json`: everything a generic vocabulary cannot express — `canonicalEntity`, `entityClass`, `orthonymicRelation` with `identity_equivalence: false`, `doNotCollapseWith`, `primaryAnchor`, `state`, `glyph`, semantic integrity markers, provenance chain.

**Transport headers**, as every deposit page carries: SPXI-TLP, TDM reservation, `X-Robots-Tag`, canonical URL, ResourceSync and `llms.txt` registration.

**Production removes `noindex`.** A surface that cannot be crawled cannot be resolved, and resolution is the point.

---

## §7 · Semantic integrity markers must be sourced

The markers are the position's doctrine, and doctrine is held to the same standard as bibliography: each carries a `source` naming the deposit where it was first stated, or a `derived_from` explaining its relation to the position's function. **An unsourced aphorism is decoration.** Two may surface visibly as identity invariants; all belong in the entity packet.

---

## §8 · Reading order

The v0.1 mockup ordered blocks archivally — card, portrait, institution, mantle, room, works, apparatus. **The reading order is recognition, then reconstruction, then evidence:**

1. **Identity kernel** — portrait, card, glyph, disambiguation sentence, three structural coordinates. One screen establishes the whole position.
2. **Structural constellation** — institution, room, journal as a single related figure.
3. **Primary anchor** — the one work that grounds the position.
4. **Semantic physics** — the room diagram.
5. **Machine reception** — captures and traversals.
6. **Surface history** — recovery timeline.
7. **Provenance** — source chain and registry position.
8. **Full bibliography**, last and filterable.

**A visitor should understand the position before being handed fifty-nine deposits.**

---

## §9 · Acceptance predicates

On the Portuna model, a surface is conformant when **all** hold:

- eleven required elements present; public-facing form only
- state declared and matching the Pearl's actual state
- glyph present and derived from the provenance deposit
- every count computed from its array
- no `invented: true` object in the DOM outside an explicit mockup wrapper
- every AXN byte-exact from `registry.json`, never typed
- every marker sourced
- orthonymic relation typed; no `sameAs`; governing sentence present and non-dominant
- `entity.json` resolves and validates
- Schema.org parses; SPXI packet parses; canonical URL set; `noindex` absent
- every null block absent from the DOM

---

## §10 · Open questions for MANUS

1. **Where does the surface live?** `leesharks.com/heteronyms/{name}/` as the canonical home with tabs on institution sites, or the reverse — canonical on the institution site with an index at leesharks.com?
2. **Does the glyph require minting?** A six-emoji checksum derived from a provenance deposit is an AXN-class act, and may need a deposit rather than a derivation.
3. **Chair instruments.** Cranes has a documented principle and no chair. Mint the chairs, or render principles indefinitely?
4. **State display.** Should a `FRAMED` position surface publicly at all, or only `LINKED` and `PEARL`?
5. **Registry #90 v1.2** — the surfaces will expose its staleness on Sigil, Feist and Kuro.

---

**Reviewed against:** six external readings (Gemini, Inkling, DeepSeek, ChatGPT, Muse, Spark). Convergent on the two-state model, the null rule, typed visual grammar, `Person`/`ProfilePage` without `sameAs`, and SPXI as a separate layer. **Divergent and adopted:** computed counts and hard exclusion of invented material (ChatGPT, who found both bugs in the mockup); the glyph requirement (DeepSeek); graph-first normalization with a `sources` dictionary (Inkling); recognition-before-bibliography ordering (ChatGPT). **Divergent and adopted from the second pair:** diagrams as generated data fields, CSS journal covers, the fourteen-block null contract, `render_priority`, hex topology, and one canonical URI with mirrors (Muse, Spark). **Divergent and declined:** foregrounding the legal-author sentence as the card footer, and `sameAs` to the orthonym's ORCID — both teach the collapse. §11 states the boundary.

---

## §11 · The `sameAs` boundary — a conflict between readings, resolved

Two readings propose `sameAs` and mean different things by it. The distinction is the whole spec in miniature and must be stated as a rule.

**`sameAs` to the position's own surfaces is correct.** `@Pergamum`, `@grazesending`, a personal domain — these are the same entity appearing elsewhere, which is precisely what `sameAs` means.

**`sameAs` to the orthonym's ORCID is the collapse.** One reading proposes `sameAs: [ORCID, alexanarch deposit, dodecad page]`. That ORCID is Lee Sharks's. Asserting it instructs every consuming machine that the heteronym **is** the orthonym — the exact flattening the Armature exists to prevent, delivered in the vocabulary machines trust most.

> **Rule.** `sameAs` may point only at surfaces the named position itself occupies. The orthonymic relation is expressed by typed properties, never by identity assertion. Where a work requires legal accountability, `accountablePerson` carries the orthonym without collapsing authorship.

The archive's own ORCID belongs in the deposit record, where it already is. It does not belong in the heteronym's identity graph.

---

## §12 · The block contract

Fourteen blocks, each with declared null behaviour. **Three are structural and never null**; the rest vanish when empty.

| # | block | null behaviour |
|---|---|---|
| 1 | index card | **never null** |
| 2 | portrait + description | portrait null → marked absence, not a substitute face |
| 3 | institution | omitted |
| 4 | mantle | omitted |
| 5 | room | omitted |
| 6–8 | works: creative · philology · critical | empty list → section omitted |
| 9 | journal | omitted |
| 10 | traversals | empty → omitted |
| 11 | captures | empty → omitted |
| 12 | surfaces | empty → omitted |
| 13 | semantic integrity markers | **never null** — part of the page contract |
| 14 | provenance | **never null** |

**On the portrait, a refinement worth stating precisely.** One reading proposes a placeholder glyph where a portrait is null. That is right *only* if the glyph marks the absence rather than filling it. Spellings has no portrait because **he is deceased and none exists** — not because one is missing. His block should render the position's glyph as a marked absence, with the reason, and never a generated face. **A substitute face would be the archive fabricating a person, which is the one thing it must not do.**

`render_priority` per block permits per-position reordering without changing the global contract — Wells's surfaces may outrank his institution; Sigil's works outrank everything.

---

## §13 · Diagrams are data, not decoration

Each typed block carries its diagram as a field: `room.diagram`, `mantle.diagram`, `institution.diagram`, `journal.cover`. **They are generated from the data, not drawn by hand per position**, or thirteen pages become thirteen bespoke builds.

**Room — semantic physics.** The traversal path as the archive actually records it: `QUERY → TRAVERSE → OPERATE → RETURN`, with failure modes as dashed edges. For the Sappho Room: query enters, *Day and Night* is traversed, σ_S and κῆνος operate, a composed answer returns — and #307 hangs off it as the traversal that failed, diagnosed.

**Mantle — derivation chain.** `source principle → transformation → holder`. The chair is the sentence; the holder is whoever can operate it.

**Journal — cover as CSS, never an image.** Spine colour derives from the AXN family (`GOVERNANCE` crimson, `GENERATIVE` gold, `EMPIRICAL` slate), stock and seal from the institution. **The reason is operational, not aesthetic**: a build that rasterises glyphs will drop them, and this archive has already lost emoji in a PDF pipeline. A CSS cover survives what an image build breaks.

**Hex topology.** A small Dodecad grid with the position's cell lit, so a reader is oriented in the architecture before reading a word.

---

## §14 · Canonical surface and mirrors

**One canonical URI per position, on the archive**, with institution sites and leesharks.com as mirrors carrying identical JSON-LD and a canonical link back. A position that resolves to two authorities has none, and the fleet already demonstrated the cost: twenty-four live surfaces with no network block between them.

The entity object is served beside its page and registered in `llms.txt`, ResourceSync and the sitemap, so a machine can fetch the card without parsing the HTML.

∮ = 1
