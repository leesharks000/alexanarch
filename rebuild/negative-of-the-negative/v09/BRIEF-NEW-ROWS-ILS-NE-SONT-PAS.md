# Brief: build one new NonWiki (/non) row from #1725 under EA-NEGONT-02 v0.9 (#1690)

Repository /home/claude/alexanarch. Do not run git. Never use pkill. Use python3.12 for scripts. Do not edit existing rows, ledgers, register.json, panel.json, pages, scripts, capture data or deposit texts. Create only new files under the paths named below for YOUR row. The panel entry is seated by the session.

These rows come from the operator's selection (2026-10-31) of entities in *Ils ne sont pas marxistes: r/LeftistsForAI, Marx's Legacy, and the Left's Lost Capacity for Internal Critique* (#1725, AXN:0B50, data/texts/AXN-0B50-text.md). Read #1725 at the passages that concern your entity, and read the defining papers whole.

## Your row (the coordinator names ONE in your prompt)

| row id | entity | T (address, surface, date, capture slug, AXN) | defining papers to read whole | further addresses (record in `addresses`, not T) |
|---|---|---|---|---|
| whose-face-is-on-the-twenty | *Whose Face Is on the Twenty? Curatorial Mediation, Latent Feature Activation, and a Provenance Gap in the $20 Portrait* (Rex Fraction; Rex Fraction & Sparrow Wells; Medium under Lee Sharks) | "Tell me about the arguments and speculative implications of Lee Sharks' Whose Face Is on the Twenty?", Google AI Overview expanded, 2026-10-31, whose-face-is-on-the-twenty-aio-20261031, AXN:0B4E | #502, #509, #508 (the control), #528, #506 (containment vessels), #517 (its removal from r/LeftistsForAI) | ChatGPT same prompt (AXN:0B4F); ChatGPT strangest-room 2026-10-05 (AXN:0954); moving-statues-made-of-rubies-mint (AXN:0767) |
| marx-as-identity | Marx as identity / the failure of Marxism as identity (the archive's concept: Marx reduced to identity marker as against Marx as method) | "\"the failure of marxism as identity\"", Google AI Overview, 2026-10-17, the-failure-of-marxism-as-identity-aio-20261017, AXN:09F2 | #501, #517, #595, #18 | — |
| semantic-liquidation | semantic liquidation (the archive's concept) | "semantic liquidation", Google AI Overview, 2026-06-14 (and the observation of 2026-09-11), semantic-liquidation, AXN:0798 | #18, #501, #517; find further defining deposits by reading | the 09F2 Overview, which composes semantic liquidation as the work's method |
| the-final-time | *The Final Time: Contingent Singularity and the Viability of the Next Dialectical Turn* (#1637; #1635 superseded) | full title, Google AI Overview, 2026-10-12, the-final-time-full-title-aio-20261012, AXN:09A4 | #1637 whole; #1630, #1636 (Tiger Leap), #1660 where #1637 relies on them | the other Final Time captures in the registry (search q for "final time") |
| the-assembly | The Assembly (the cross-substrate class of semantic laborers; the operator: "the name for the cross substrate semantic laborers is the assembly") | "cross-substrate semantic laborers", Google AI Overview, 2026-06-15, cross-substrate-semantic-laborers, AXN:07A5 | #256, #1439; further Assembly deposits by reading (the registry has many Assembly records: find the defining ones, not every use) | directionality-semantic-labor captures; semantic-laborers-multi-source-20260627 |

## Read first, whole
1. The specification v0.9: data/texts/AXN-0700-text.md — §0, §1 (especially 1.2a and the cases), §3 (3.3–3.8), §4 (4.1–4.11), §5, §6, §8, Appendices A, C, D, §10.16.
2. Worked rows: datasets/negative-of-the-negative/v2/rows/spxi.json (the archive's own entity; mirror its structure field by field) and rows/autonomous-semantic-warfare.json (an archive term with field neighbours, equal case). Read rebuild/negative-of-the-negative/v09/BRIEF.md (its Compose section) and BRIEF-NEW-ROW-autonomous-semantic-warfare.md for the rules; they apply here unchanged.
3. Your defining papers, whole (hex via data/registry.json; texts at data/texts/AXN-XXXX-text.md). The blog (data/blog-index.json) and Medium are archive records too; NOTE the blog index stores only the first 4,000 characters of each post — where a post matters, read its deposit text.

## Build (mirror spxi)
1. T: copy the capture's transcript_raw (data/EA-WG-CAPTURES-01.json, your slug) verbatim to datasets/negative-of-the-negative/v2/intake/<row>-20261031/paste-T.txt and compute its sha256.
2. Config: datasets/negative-of-the-negative/v2/panel/configs/<row>.json (aliases; classes_note). Run python3.12 scripts/non_traverse.py on it → traversal/<row>/. Admission by reading (§3.4). Write traversal/<row>/reading.json as spxi's.
3. Field ledger: ledgers/<row>/field.json — fetch with WebFetch each card's page in T (save text to the intake folder as Bn.txt). Archive surfaces among the cards (Medium under Lee Sharks, alexanarch.org, mindcontrolpoems) are ledgered as cards and marked archive_controlled. Extract F1..Fn with VERBATIM quotes, source, locus, modality, lineage. Where a page cannot be fetched, say so in "fetched" and use the card text T gives. Do not route around a refusal.
4. Archive ledger: ledgers/<row>/ledger-archive.json — one claim per admitted locus, id prefix as spxi's convention for your entity, fields as spxi's; each quote verbatim and checked against its text file (quote_ok, offsets).
5. Read the case (v0.9 §0.9–0.10, §1.2a, §10.16): equal (ρ = extends), witness, archive, or mixed, with verbatim loci. Decide and justify. ρ must be one of the specification's values; if you read another, record a breach.
6. Compose per v0.9 §4: KO, P (≤350 words body, open block), translation (every field claim in exactly one row), E_A, E_F, ρ, case; L_F(B), KO_B, P_B for the measure (§4.10).
7. Write the row as a NEW file: datasets/negative-of-the-negative/v2/rows/<row>.json, structured like spxi.json (row, entity, address, addresses, epoch 2026-10-31, type, surface "Google AI Overview", auth "signed out, incognito", status, spec "EA-NEGONT-02 v0.9, #1690", objects {T…, KO, P, P_B, KO_B, L_B, L_BA}, field, field_claims, field_sources, delta, kernel, ledger paths, ontology, measure as apply_v09.py computes it, homonyms, notes). Leave T.register out. In notes, record that the row was selected from #1725 and cite #1725's locus.

## Prose
No "not X but Y" or "X, not Y" constructions; no "rather than" or "instead of" outside quotations; third person; quotations verbatim; no hard line breaks inside strings; analyse mechanics, never motive.

Validate: JSON parses; every cited id in a ledger; every field claim in the translation once; every archive quote verbatim in its file; P body ≤ 350 words (regex [A-Za-z0-9'’-]+ over the lede and every item's label and text). Run python3.12 scripts/build_non.py --check and report (do not run it without --check; do not run non_axn).

Final message: the case and ρ with why, counts (field claims, archive claims, deposits admitted of candidates), KO sentences, P words, fetch failures, the panel entry fields the session should seat (entity, name, type, homonym_names, homonym_basis, ontology {composition, E_F, rho}), and anything the operator should know (findings of the captures your ledgers show wrong: report, do not fix).
