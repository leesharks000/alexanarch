# Brief 2: one full /non entry, end to end (EA-NEGONT-02 v0.7), at the grain of the worked examples

You build ONE entity's full entry: field ledger, archive reading and ledger, and the composition. First read BRIEF.md in this folder (extraction rules and ledger formats; they still hold). Then study the finished examples, which are your model:
- /home/claude/alexanarch/datasets/negative-of-the-negative/v2/rows/model-collapse.json (the original worked example) and rows/howl.json, rows/theophrastus.json, rows/the-socratic-problem.json (composed today).
- The composition scripts that produced the last three: entries/compose_howl.py, compose_theophrastus.py, compose_socratic.py, and the shared writer entries/compose_common.py (call write_row; it checks every claim id and writes ledgers/<entity>/, traversal/<entity>/reading.json and rows/<entity>.json into the repo).

Python: export PATH=/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/py312:$PATH
Work files go under entries/<entity>/ (scratchpad). Your compose script is entries/compose_<entity>.py; running it is the only thing that writes into the repo, and it may write only that entity's files. Do not git commit; do not touch other entities' files.

## Steps
1. FIELD (entries/<entity>/field.json): the cards in the transcript (given in your task) are the field B. WebFetch each card's page and extract claims with VERBATIM quotes (ask WebFetch for exact quotations). YouTube/Reddit: title only. A blocked page: card snippet as its only quote, fetched: "not fetchable: <reason>". Aim 20–40 field claims.
2. READING (entries/<entity>/reading.json, same format as traversal/howl/reading.json): the D/R/O string pass is done at datasets/negative-of-the-negative/v2/traversal/<entity>/candidates-{D,R,O}.jsonl. Admit by reading only (spec §3.4): a claim of the stratum's kind about the entity; naming it is not enough. Volume is never a ground for removal, but most string hits will not bear; group bulk non-admissions with a shared reason. Read the defining deposits whole where the archive has a line on the entity.
3. ARCHIVE LEDGER (entries/<entity>/ledger.json): claims from admitted deposits, ids <P><dep>-<nn> with the prefix given in your task; verify every quote verbatim (whitespace-normalised) against the deposit text and reach 100%.
4. COMPOSE (entries/compose_<entity>.py → run it): objects T, KO (expansion, 14–22 sentences), P (compression: lede, 5–7 headed sections, rail of lineages), P_B and KO_B (the field alone, same plan), delta (T_vs_LB and LB_vs_LBA), kernel (about 11 K entries), status, spec. Follow the pattern of the three compose scripts exactly. The conventional reading leads, in full; archive material follows at its grade.

## Composition rules (an independent checker will audit every sentence against the QUOTES it cites; these are the failures it found last time)
- Every factual element of a sentence (date, number, name, attribute) must be supported by the QUOTE of at least one cited claim, not only by the ledger's paraphrase. If only the paraphrase has it, cut it or cite a claim whose quote does.
- Archive claims whose modality is interpretation, hypothesis or stipulation carry their grade in grammar: "is read as", "is held", "is defined as", "is specified as", "is stated as a hypothesis". Never plain fact. Documented archive findings may be stated as findings ("a measure finds…").
- Field claims marked attributed keep attribution ("is said", "reputedly", "X argues", "by Y's account"). Keep hedges the source has ("ideally", "it is widely believed", "helped").
- Do not overstate limits, falsifiers or withdrawals: a "would weaken" is not "would falsify"; an "open item" is not a falsifier; "found unremarkable" is not "withdrawn".
- Where the archive disagrees with itself, carry it as contested, naming the positions.
- No "not X but Y", "not X, but Y", "rather than", or "not X, only Y" constructions in your own prose (inside quoted field text is fine). State Y directly.
- No dates or numbers the cited quotes do not give.
- Private individuals by initial only.

Final message: counts (field claims, admitted/not-admitted deposits, archive claims, quote pass rate, KO sentences, kernel entries), the files written, what you could not do, and 6–10 lines on what admission adds to the entity.
