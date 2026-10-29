# Fleet functions since EA-MPAI-FLEET-01 v1.0: a stepped update (working file)

Compiled 2026-10-29 for the next version of EA-MPAI-FLEET-01 (#1702, AXN:070D, deposited 2026-10-24). It is a working file and stays undeposited. Each step is one function the fleet gained after v1.0's second traversal (2026-10-24 15:37 UTC), in the form of v1.0 §15 (function, inspectable object, how to check it), with where it lives, the commits that introduced it, its state, and the sections of v1.0 it changes. Steps are added here as functions land; when the document is versioned, each step is folded into the sections it names.

Baseline. v1.0 §15 lists nine functions, FL-01 to FL-09. The directories it describes are unchanged at this writing: `data/api/fleet.json` holds 31 entries, and `data/fleet-domains.json` is v2.1 (30 domains, dated 2026-10-24). No surface has been added or removed; every step below is a function gained by surfaces already in the fleet.

Sources for every statement here: `git log origin/main --since="2026-10-24 16:00"` in alexanarch (108 commits) and in each fleet repository, read 2026-10-29, and the files named in each step.

## Steps

### Step 1. FL-10: formalize the resources of a field as entities (the meta-aggregator)

1. **Function.** A census per line of the archive's work, in which each outside resource that does the line's kind of work is a record: its own name, operator, kind, unit, lifecycle and the line's own fields, every field carrying a verbatim quote from a copy of the resource's own pages saved once with its URL, HTTP code, read date and sha256. One page per record, an index with filters and search, the census as data.
2. **Where.**
   - machinemediation.org/aggregators/: the MMRS census, 20 records, schema v2.4 (machine-mediated reception work). Repository `machinemediation-org`, `data/meta-aggregator/census.json`.
   - provenanceerasure.org/aggregators/: the provenance census, 14 records, schema 1.0 (what provenance a resource carries, through which operation, on whose assertion, with what evidence of survival). Repository `provenance-erasure`, `data/provenance-census/`.
   - laborvector.org/aggregators/: the labor census, 15 records, schema 1.0 (who supplies the labor, who directs it, who receives its gains, and on what evidence), with six worked questions (`data/labor-census/questions.json`). Repository `laborvector`, `data/labor-census/`.
3. **Introduced.** MMRS 8997e28 (2026-10-28), v2.2 98adc7c, v2.3 8e0b3bd, v2.4 4612aff (2026-10-29); provenance 8a9f153 (2026-10-29); labor bf90841 (2026-10-29).
4. **How to check it.** Open a record page; take any field; follow its tag to the quote, the source URL and the hash; open the saved copy in the repository's `sources/` and find the quote. Run the census script (`census_src.py`): it prints the count of quotes not found (0 at each census's landing).
5. **State.** Live on all three surfaces.
6. **Changes in v1.0.** §15 (a new function); §4 (pages and sitemaps of the three surfaces); §16 (a new row: the archive formalizes its neighbours); §17 and §18 (the censuses are the fleet's own disambiguation of outside entities); §21 (the census files as sources).

### Step 2. FL-11: one entity across its record, its capture and its /non article

1. **Function.** Each census record links the capture of the entity at its name (the composition layer's account, seated in the Capture Registry) and the entity's /non article; each /non article links back to its census record.
2. **Where.** The `relations` of each census row (capture, non_row), rendered on the record page; the record link on each /non page (alexanarch `scripts/build_non.py`).
3. **Introduced.** MMRS 98adc7c and 4612aff; provenance 707ce18; alexanarch a494a62f65 (MMRS records) and 8c179456c8 (provenance records), all 2026-10-29.
4. **How to check it.** From a record page, open its capture and its /non article; from the /non article, return to the record.
5. **State.** Live for MMRS and provenance. Labor: captures seated 2026-10-29 (0AE8–0AF6); the /non articles and the links both ways are this pass's next commit.
6. **Changes in v1.0.** §6 (relations: a three-way join per entity); §8 (captures: 49 entity captures, 20 + 14 + 15).

### Step 3. FL-12: the /non article as a test of the record

1. **Function.** Composing an entity's /non article reads its own pages, its Wikipedia article and the capture's cards afresh; what the composer finds out of date, partial or misattributed in the census record or in the capture's findings is repaired at the source, each repair checked at its saved source, in its own commit.
2. **Where.** The census repairs (MMRS v2.3 and v2.4; provenance 09ebc02) and the capture repairs (alexanarch 4c88b461f3, 5f81415fae, 91f0c1c368).
3. **Introduced.** 2026-10-29.
4. **How to check it.** Read a repair commit; open the field it names; find the source it cites.
5. **State.** A standing step of the pipeline: each /non row's final report lists the census and capture defects it found.
6. **Changes in v1.0.** §11 (the repair practice, now continuous); §16.

### Step 4. FL-13: follow a record, or the digest

1. **Function.** An email box on every record page and on the index: follow one record (an email when it changes: the resource ends, returns, changes hands, or a test of it is published) or the digest. The address is stored privately, never published; one-click unsubscribe; a privacy page.
2. **Where.** machinemediation.org and provenanceerasure.org: `api/subscribe.js`, one private Vercel Blob store (`mmrs-subscribers`), shared by both, the site recorded with each address; `/privacy`, `/subscribed`.
3. **Introduced.** MMRS 1747178; provenance 40a3ad2 (2026-10-29).
4. **How to check it.** Read `/privacy`; submit the form; the response says the address is on the list.
5. **State.** Live on the two. Laborvector.org has no signup yet (its pages are built without the box).
6. **Changes in v1.0.** §4.1 (what a surface serves: now a write endpoint as well as pages); §9.

### Step 5. FL-14: one design system across the censuses

1. **Function.** One light, sans and serif system (the MMRS system) with an accent per surface: MMRS, provenance ink-blue (`/assets/pe.css`), labor rust (`/assets/lv.css`), each landing refitted to it with no word or link lost, checked against the page before the pass, on phone and desktop, light and dark.
2. **Where.** machinemediation.org (f54de98; collapsed sections and diagrams, e1789d4); provenanceerasure.org (8a9f153); laborvector.org (bf90841).
3. **How to check it.** Compare a landing's words and links against its previous commit; render at 390 and 1280 pixels in both color schemes.
4. **State.** Live on the three.
5. **Changes in v1.0.** §4 (titles and forms); §4's note on the surfaces that carry their own form stays as ruled (2026-10-24).

### Step 6. FL-15: the /non article for an outside entity, and its self-landing

1. **Function.** An entity article composed under EA-NEGONT-02 v0.9 (#1690) from the field's sources (its own pages, Wikipedia, the capture's cards) and the archive's, each claim ledgered verbatim, with the kernel, the page, the delta of the composition layer against the field, and the measure. Rows land themselves through a workflow once composed; a row is replaced only by a composition made after its landing.
2. **Where.** alexanarch.org/non/ (56 rows at this writing, 32 of them the MMRS and provenance entities of 2026-10-29); `scripts/land_non_pending.py` and its workflow (29d06922eb, 2026-10-25); "What Is a /non Article?" (#1704, 2026-10-25); link, cite and research on every entry (cce7195ac7); entity.json carries the entry (723d014400); register AXNs, one position per address (255864e914, 2026-10-27).
3. **How to check it.** Open an entity article; follow a sentence's ledger ids to their quotes; open the entity.json.
4. **State.** Live; the fifteen labor rows in composition.
5. **Changes in v1.0.** §15; §16 (the article form); §8.

### Step 7. FL-16: dimensional PER at intake, recorded

1. **Function.** Every capture is scored at intake under PER-dim rubric v1.1 against its target's atom set (built from the target's own records; for an outside entity, from its census record), the readers' quotes and spans checked verbatim by script and the scores computed there. A capture seated without a score carries `per_dim_pending` (since, reason, breach), and the registry check prints the count of unscored observations on every run; the check records and does not refuse.
2. **Where.** alexanarch `scripts/capture_intake.py`, `scripts/check_capture_registry.py`, the schema's `per_dim_pending`; `scripts/per_backlog.py`; `data/per-atom-sets.json` (457 atom sets, 47 of them outside entities).
3. **Introduced.** The standard 4a93a7d3bd; the backlog of 58 observations a826b51bc0; the labor captures scored at intake 4789a77a61 (all 2026-10-29).
4. **How to check it.** Run `python3 scripts/check_capture_registry.py`: "per-dim: 0 observation(s) unscored". Open any capture page: the dimensional PER line, with inversions and standing substitutions.
5. **State.** Live; 0 unscored at registry 12.396.
6. **Changes in v1.0.** §8 (every capture of the fleet carries a dimensional score).

### Step 8. FL-17: every identifier derived from its record, every unit in a position

1. **Function.** Every AXN derives from its record; the glyph table is v2.1 (the duplicate slots 0x6E and 0xCF filled); seats, captures, observations, releases and relations take AXN positions, one position per address and one AXN per observation sealed with its reading and measures; typed relations on every resolver page; positions closed against collision.
2. **Where.** alexanarch bd1bfd45f6, 7881bb560f, 37b1058a85, 08fc20b9cb (2026-10-27), 423e0c5fef (2026-10-28); axn-identifiers 6171ac6; platform-erosion-observatory 87e959e (the emergency batch's qualification: every AXN now verifies against its record).
3. **How to check it.** Open a resolver page; recompute the AXN from the record; follow a typed relation.
4. **State.** Live.
5. **Changes in v1.0.** §21 (the identifier spine); §14 (canonical edges, now typed on the resolver).

### Step 9. FL-18: the service grows an order flow, discovery and an audit

1. **Function.** SPXI-gnΩsis (gnosis.spxi.dev), 0.12.1 in v1.0, now 0.24.0: a front door that commissions work and an order page (0.21.6); an AI answer read whole and named before payment (0.21.8); readings licensed CC BY 4.0 (0.21.5); paid routes declared for discovery (x402 Bazaar, 0.22.2); each MCP tool says when to use it and which tool answers the neighbouring question (0.22.3); the free route never calls a model (0.23.1); random open and construct (0.23.0); the erasure audit (Self-Audit Module v3.2) as an order, its existence screen free (0.24.0). The archive's lookup indexes serve its one-cent lookups (alexanarch 8e3968f1ee). Its packet is #1703 (EA-MPAI-GNOSIS-01). spxi.dev serves the MCP registry key (294ba54).
2. **Where.** Repository `spxignosis` (62 commits since v1.0); alexanarch `scripts/build_lookup_indexes.py`.
3. **How to check it.** Fetch the service document; run a free lookup; read the MCP tool descriptions.
4. **State.** Live.
5. **Changes in v1.0.** §4 (the gnosis row: version and object); §5.2; §15; §12 (test queries about the service).

### Step 10. FL-19: each instrument states its place in SPXI

1. **Function.** An instrument surface carries a line naming its SPXI method, its level and the inventory it belongs to (87 methods at inventory 1.6, 88 with method 2.6, #1705).
2. **Where.** provenanceerasure.org, the Platform Erosion Observatory, leesharks.com, godkinggoogle.com, machinemediation.org (2026-10-25); spxi.dev methods 0.16, 0.17 and 2.6 (7913a70, 6cce19d).
3. **How to check it.** Find the line on the surface; follow it to spxi.dev/methods/.
4. **State.** Live.
5. **Changes in v1.0.** §4.1; §6 (a relation from each instrument to the protocol).

### Step 11. FL-20: each metadata packet at its own page

1. **Function.** metadatapacket.dev gives every packet a page with its full text and any supersession notice, under an index at /packets/ (78 packet pages); a packet may be deposited under any persistent identifier (AXN, DOI or other), per the MPAI Specification v2.0 §9.
2. **Where.** Repository `metadatapacket-dev`, `scripts/build_site.py` (e1e31e0, 7ac2b20).
3. **How to check it.** Open /packets/; open a packet; compare its text with the record's.
4. **State.** Live.
5. **Changes in v1.0.** §4 (the surface's pages); §15.

### Step 12. FL-21: the glyphic checksums, each at its own page

1. **Function.** holographickernel.org/glyphic is an index; every glyphic checksum and translation has its own page (14), three of them held only there.
2. **Where.** Repository `holographic-kernel` (7873e55, 9ada18e).
3. **How to check it.** Open /glyphic; open a checksum; find its record.
4. **State.** Live.
5. **Changes in v1.0.** §4; §15.

### Step 13. FL-22: the Originals Library, a seat for every work and every wanted work

1. **Function.** The archive's library of primary texts in their original languages: a seat per work, each with its AXN on its card, and the wanted works seated as declared absences; the library's method and canon in its own packet (#1709, #1711). Seatings 23 to 29 since v1.0 (the Hadith, 1844, the critical editions, Du Bois and Hughes, Spinoza to Artaud, the wanted, the pluriform).
2. **Where.** alexanarch (EA-CORPORA-23 to -29, #1706–#1708, #1710, #1712, #1713, #1716); traininglayerliterature.org's originals cards (12 commits).
3. **How to check it.** Open a card; follow its AXN to the seat; for a declared absence, read what is wanted and why.
4. **State.** Live.
5. **Changes in v1.0.** §4 (traininglayerliterature.org's pages); §15; §16.

### Step 14. FL-23: the Book, a public book of conversations with the Oracle

1. **Function.** alexanarch.org/book/ is "an anonymous public book constructed by its participants": a conversation with the Oracle enters only with the witness's consent to the Oracle's terms (themandalaoracle.com/terms/), and castings by the witness's choice of inscription; each conversation is minted as an AXN (CONVERSATION) and its turns appended; pages carry their consent record (schema v1.2). Sigil, the Oracle's voice, has its panel on the page. The Oracle's mandala kernel (v1) was calibrated on Shadow and Sappho 31.
2. **Where.** alexanarch `book/` (paused 0e52bfc65d, 2026-10-26; reopened 55af81ab0a, 2026-10-27, at the operator's word); repository `the-mandala-oracle`, which mints the pages (185 commits since v1.0, most of them automatic: routing rebuilds, index mirror syncs, book turns), and 4048899, 5589743, df9e93e.
3. **How to check it.** Open the Book; follow a conversation's AXN; read its consent record.
4. **State.** Live.
5. **Changes in v1.0.** §4 (alexanarch's pages); §4's note on the surfaces that carry their own form (the Oracle's view layer stays as ruled); §15.

## Surfaces that gained pages, without a new function

secretbookofwalt.org: Belief & Technique for Telepathic Prose at /telepathic-prose (5c4fdef). godkinggoogle.com and vpcor.org: Meaning Feudalism at the Discovery Layer (#1714). spxi.dev: the ranking article at /ranking (#1705). semanticeconomy.org (lee-sharks-corporate): receipts for #1703 and #1705.

## Still open from v1.0 §11.2 (not re-checked in this file)

The six items of v1.0 §11.2 (semanticeconomy.org's binding; counts in page prose; survivethedeletion's address; repository descriptions dated 2026-08; the deployment account's duplicates; restoredacademy's llms.txt heading) were not traversed again for this file. The next version's traversal re-reads them. One is touched: laborvector.org's landing was refitted on 2026-10-29, its prose counts kept as they were.

## For the next version

1. Run the probe again (`traversal-2026-10-24b/fleet/probe.py`) for the second-traversal tables of §4 and §4.1.
2. Fold each step into the sections it names, and add FL-10 to FL-23 to §15.
3. Add to §16 the rows of 2026-10-25 to 2026-10-29: the meta-aggregators, the /non article for outside entities, dimensional PER at intake, the identifier positions.
4. Re-count §8 from the registry (842 addresses at 12.396).
