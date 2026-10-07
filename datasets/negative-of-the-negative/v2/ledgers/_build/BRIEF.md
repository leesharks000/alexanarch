# Brief: ledgers for three /non entities (EA-NEGONT-02 v0.7)

Repo: /home/claude/alexanarch (read only for you; write ONLY under /tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/entries/<entity>/).
Python: `export PATH=/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/py312:$PATH` (python3.12).

The dataset composes public knowledge of an entity three ways: T (what Google's composition layer gave), L(B) (recomposed from the full texts of the sources the layer itself surfaced, "the field"), and L(B ∪ A) (the same algorithm with the archive's subset A admitted on equal terms). You build LEDGERS — claim lists — not prose. Someone else composes.

Spec: data/texts/AXN-06E7-text.md (§3.3 modalities, §3.4 D/R/O selection, §3.5 extraction and kernels, §3.6 lineages, §4.2 stipulation rule). Read those sections first.
Worked example to imitate: datasets/negative-of-the-negative/v2/rows/model-collapse.json (field_claims F1–F18) and datasets/negative-of-the-negative/worked-example/ledger-archive.json (archive claims).

## Extraction rules (source-neutral; the same for field and archive)
- From each source take: the claims in its abstract/opening, its defined terms, its headline findings, its stated limits, its falsifiers. Nothing chosen by how it reads.
- Every claim carries a VERBATIM quote from the source text (copy exactly; never paraphrase inside "quote") and a locus (section heading, paragraph, or page part).
- Modality (M_src, the source's own): documented | attributed | stipulation | self-description | interpretation | hypothesis | contested. A source defining its own term or subject is **stipulation** (field or archive alike, §4.2). Self-description only where a source assesses itself.
- kernel: per source, its central claim and governing limit — 2 claims, at most 3. Mark with "kernel": true.
- const (constitutive): rare — a claim whose removal changes the identity of the entity. Mark sparingly.
- lineage: a short name grouping instances that state one substantive claim; the earliest instance is the lineage's earliest. Two instances are the same claim only if subject, predicate, object, qualifier and modality all match.
- Private individuals appear by initial only. Do not write the given names of private people (cited scholars and public figures are fine).

## Field claim format (field.json)
{"field": [{"id": "B1", "card": "<site — title as on the card>", "url": "...", "fetched": "<how: WebFetch verbatim excerpts YYYY-MM-DD | not fetchable: reason>"}...],
 "field_claims": {"F1": {"source": "B1", "locus": "...", "quote": "\"...verbatim...\"", "claim": "<one-line paraphrase>", "modality": "...", "kernel": true|false, "const": true|false, "lineage": "..."}, ...}}

## Archive claim format (ledger.json): a JSON list
[{"id": "<P><dep>-<nn>", "dep": <deposit number>, "claim": "<one-line paraphrase>", "kind": "definition|claim|limit|finding|falsifier|relation|...", "modality": "...", "strata": ["D"|"R"|"O"], "locus": "...", "quote": "<verbatim from the deposit text>", "kernel": bool, "const": bool, "lineage": "...", "date": "<deposit date>"}]
Prefix <P>: H for Howl, T for Theophrastus, S for the Socratic problem.
Deposit texts: data/registry.json → deposits[*].full_text_path (e.g. /data/texts/AXN-06E7-text.md), date, title, creator.
Verify every quote: after writing, run a check that each quote occurs verbatim (whitespace-normalised) in its deposit text; report the pass rate and fix failures.

Report back (final message): counts (sources, claims, kernels, lineages), files written, anything you could not do, and 5–10 lines on what the archive (or field) says about the entity that the others do not.
