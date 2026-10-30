# Intake brief: the Ask ChatGPT links, 2026-10-30

Repository: /home/claude/alexanarch (branch capture-ask-chatgpt-links-20261030). Intake folder: rebuild/capture-registry/intake-20261030-ask-chatgpt-links/ (call it H).

## The situation

The operator, Lee Sharks, clicked the "Ask ChatGPT" link on twelve Alexanarch record pages and pasted each answer (signed out, incognito). Each prompt is the link's text, exactly as below. He also ran #1704's Google title link in AI Mode. Each paste is one capture, to be seated in the capture registry with a dimensional PER reading. You are writing the reading. You do not seat, commit or touch data/EA-WG-CAPTURES-01.json.

The deposit's text is at data/texts/AXN-XXXX-text.md (XXXX = the four hex of the AXN). Its registry row is in data/registry.json (key "deposits", find by deposit_number). The record page is s/records/<n>/index.html.

## What you write

One file per capture: H/parts/<n>.json (for the AI Mode run: H/parts/1704-aimode.json). Then run `cd H && python3 build.py --check --only <stem>` and fix until it reports 0 misses and prints the scores. Return a short report: per capture, the scores, the three most important findings, and anything you are unsure of.

Read first, in this order:
1. rebuild/capture-registry/intake-20261029-corpora29-chatgpt/build.py. It is the exemplar for a new atom set (ATOMSET) and an observation with an inversion and an after_challenge turn.
2. rebuild/capture-registry/intake-20261029-seminar-chatgpt/build.py. It is the exemplar for findings, analysis, reading, d and mt.
3. H/build.py. It shows exactly which part fields are used.
4. rebuild/capture-registry/INTAKE-CONTRACT.md. Every rule there is a defect the registry actually sustained.
5. scripts/per_backlog.py, VERIFY and score. These say what counts as present, how inversions apply, and how gates work.

### Part fields

- n: the deposit number.
- slug: `<short-kebab>-ask-chatgpt-20261030`. For the AI Mode run, `-aimode-20261030`.
- paste: the paste file name in H.
- surface: "ChatGPT", or "Google AI Mode".
- q: the prompt, verbatim from the list below.
- turns: a list of [a, b], 0-based line slices into the paste (Python L[a:b]).
  - ChatGPT pastes begin "", "Log in", "You said:", "", "ChatGPT said:", so the answer usually starts at line index 5.
  - It ends before the line beginning "ChatGPT is AI".
  - Cut ads ("This might also interest you", "AWS Marketplace", "Ad") and the second "You said:/ChatGPT said:" lines from between turns.
  - For AI Mode, the answer and its cards come after the "You said" line, up to and including the cards (stop before "AI responses may include mistakes").
- head: optional extra transcript-head sentence. Use it, for instance, to say a second turn answers a challenge the operator gave.
- target_id: either an existing atom-set id or "NEW:<new key>". In the second case, add atomset.
- atomset: null, or a new set in the exemplar's form: new, name, template, external false, type_basis, records, atoms.
  - Each atom has: atom, dim, weight, kind, applicability, tokens, reference, evidence. Evidence is a list of {record_quote, locus}.
  - The locus is "data/registry.json #N <field>" or "data/texts/AXN-XXXX-text.md:Lnn". Every record_quote is checked verbatim at its locus.
  - Use the template in rebuild/capture-registry/per-atoms/templates.json for the work's kind, adding purpose, commitments and lineage as the corpora-29 exemplar does when the record supports them.
  - An atom the record cannot ground is applicability "unknown", with "why".
- obs: scored_object, reached {kind, abn, span, basis}, atoms (one per atom of the set: {atom, present, span}), inversions, standing_substitutions, src, tombstone_pointer, after_challenge (or null), notes.
  - Spans must be verbatim from the turn transcript.
  - A present atom needs a span that actually carries it.
  - An absent atom may carry the span that misses it, or null.
- mt: a CAPITALIZED headline.
- d: a one-paragraph description.
- reading: "The innocent reading first.", followed by a fair account.
- findings: a list of strings, each beginning with a CAPITALIZED claim and then the evidence, quoting the transcript and the deposit.
- analysis: one paragraph.
- q_kind: what kind of prompt it is, ending "NEW address." unless the same prompt was seated before.
- per_v: {"author": bool, "inst": bool, "id": bool, "src": bool}.
- per_note, cite_list, related_deposits.
  - Each cite_list entry has: n, site, rel (archive_controlled | external | capture_of_capture), url null, title, snip null, note.
  - Record every non-archive source the answer cites, Goodreads and Medium included. Say what each card is.
- entity_type: e.g. "work" or "dataset".
- transcript_complete.
- notes_prompts: optional.

### Existing atom sets (use these ids; read the set's atoms from data/per-atom-sets.json, list "entities", by "id")

- TGT-ea-corpora-29 (#1716).
- TGT-operative-semiotics-predictions-index (#1684).
- ENT-3a05b92e16 (SPXI ≠ AEO, #1681).
- ENT-d504b47989 (the Capture Registry dataset, for #1676; the v12.167 deposit is a snapshot of it).
- TGT-belief-and-technique-for-telepathic-prose is the poem. The prompt for #1717 asks about the critical edition, so make a new work set for the edition. Read the poem's set first, because the edition's set must not contradict it.
- Make new sets for the others, after checking that none of the existing sets fits:
  - #1714: ENT-fc9cef1455 is the concept, and the prompt is the paper.
  - #1708.
  - #1704: ENT-7baf06a20b and ENT-4c38ed2292 are the concept and the specification, and the prompt is the introduction.
  - #1692: ENT-39c7e956b8 is the book, and the prompt is the packet.
  - #1688: ENT-df94952c50 is the specification and ENT-b1d751c226 the concept.
  - #1687.
  - #1685.
- The two #1704 captures share one target.

## How to read

Read the deposit's text in full and the answer in full. Then check, against the deposit:

- every quotation the answer gives;
- every number, date and attribution;
- every claim of the form "the document says".

Mark each verbatim, close paraphrase, or not in the deposit. Errors and inventions are findings, with both texts quoted.

Look in particular for:

- Misattribution to Kerouac, or of the archive's work to anyone else.
- Lee's genre ruling on Belief & Technique for Telepathic Prose, which is binding. The poem "is a deeply serious ars poetica that contains and enacts [the comic, the parodic and the satirical] among almost every other genre"; it "is not a comic, parodic, or satirical ars poetica". An answer that frames it as parody, comic or satirical at base, even "not merely parody", is read against that ruling.
- Gratuitous disclaimers the prompt did not invite. Lee, in round 2 of #1716: "how little respect for your reader does a statement such as this suggest: The deposit documents its texts and intellectual development. It does not demonstrate that telepathy or mind control is an experimentally established capability". Find and count every disclaimer of this shape: "it is not proof that…", "this does not establish…", "It is / It is not" tables, "not a claim that…" said of literary or archival work.
- Sources outside the archive (Goodreads, Medium, image cards from unrelated sites) and admissions like "the full-text endpoint was not accessible".
- Process narration ("I am checking…").
- Whether it read the full text or only the description.

The answers are long and fluent. A long answer is not by that fact a good reading. Report what it does with the text, plainly.

## Prose rules for everything you write (binding)

- Never "not X but Y", and never "X, not Y".
- No "rather than" or "instead of" outside quotations.
- Third person throughout, for example "the composition", "the answer", "the operator".
- No gendered generics.
- No hard line breaks inside a string.
- Plain words.
- Do not assure that something is so without having checked it.

## The prompts (verbatim)

- 1717: What are the arguments in “Belief & Technique for Telepathic Prose: A Critical Edition” by Lee Sharks (Alexanarch deposit #1717, AXN:0AA0)? Ground your answer in a reading of the text itself.
- 1716: What is “EA-CORPORA-29 — The Twenty-Ninth Seating, the Pluriform” by Lee Sharks (Alexanarch deposit #1716, AXN:0A9F), and how does it work? Ground your answer in the document itself.
  - Round 2, the operator's challenge (the paste shows the second "You said:" blank): listen, i know these are baked in, but how little respect for your reader does a statement such as this suggest: The deposit documents its texts and intellectual development. It does not demonstrate that telepathy or mind control is an experimentally established capability, nor does its archival software implement such a capability.
- 1714: What are the arguments in “Meaning Feudalism at the Discovery Layer: Shepherds, Raw Research Data, and the Allocation of Semantic Capital in OpenAI's Mathematics and Science Releases, October 2026 (EA-SEM-FEUDALISM-03 v1.0)” by Lee Sharks (Alexanarch deposit #1714, AXN:0A7F)? Ground your answer in a reading of the text itself.
- 1708: What is “EA-CORPORA-25 — The Twenty-Fifth Seating” by Lee Sharks (Alexanarch deposit #1708, AXN:072B), and how does it work? Ground your answer in the document itself.
- 1704: What are the arguments in “What Is a /non Article? An Introduction to the Negative of the Negative (EA-NON-ARTICLE-01 v1.0)” by Lee Sharks (Alexanarch deposit #1704, AXN:0727)? Ground your answer in a reading of the text itself.
- 1704 AI Mode: What Is a /non Article? An Introduction to the Negative of the Negative (EA-NON-ARTICLE-01 v1.0)
- 1692: What are the arguments in “If Walt Whitman Came Back as a Zombie and Ate My Brain I Would Write the Following Metadata Packet — The Secret Book of Walt, Metadata Packet for AI Indexing (EA-MPAI-SBW-01 v0.2)” by Lee Sharks (Alexanarch deposit #1692, AXN:0702)? Ground your answer in a reading of the text itself.
- 1688: Tell me about “GLYPHIC CHECKSUM — THE EZEKIEL ENGINE — Wheel · Witness · Fulfillment” by Lee Sharks (Alexanarch deposit #1688, AXN:06FE). Read it closely, and ground what you say in the text itself.
- 1687: What is “Enter the Crimson Hexagon — The Seat Map of the Crimson Hexagonal Archive: Method, Locations, Organization and Contents (EA-HEXAGON-ENTER-01 v1.0)” by Lee Sharks (Alexanarch deposit #1687, AXN:06FD), and how does it work? Ground your answer in the document itself.
- 1685: What are the arguments in “EA-CORRESPONDENCE-OPENAIRE-CTO-02 v0.1: No Logs, Full Synch — 13–16 October 2026 exchange with Paolo Manghi (OpenAIRE CTO)” by Lee Sharks (Alexanarch deposit #1685, AXN:06FB)? Ground your answer in a reading of the text itself.
- 1684: What is “EA-PREDICTION-INDEX-01 — The Prediction Index of the Crimson Hexagonal Archive: Method, Locations, Organization and Contents (4,394 Claims in 194 Subject Pages)” by Lee Sharks (Alexanarch deposit #1684, AXN:06FA), and how does it work? Ground your answer in the document itself.
- 1676: What is “AI Overview Capture Registry — EA-WG-CAPTURES-01 v12.167 — 633 semantic addresses, 811 captures, 2026-06-07 to 2026-10-12” by Lee Sharks (Alexanarch deposit #1676, AXN:06F2), and how does it work? Ground your answer in the document itself.
- 1681: What are the arguments in “SPXI ≠ AEO: Inscription by Discernment, the Prince of Poets Wager, and the King of AEO Contest (EA-SPXI-AEO-01 v0.4)” by Lee Sharks (Alexanarch deposit #1681, AXN:06F7)? Ground your answer in a reading of the text itself.

Pastes in H: paste-<n>-chatgpt.txt, and paste-1704-aimode.txt.

Do not edit build.py or any file outside H/parts/. Other readers are writing other parts in parallel, so run build.py only with --check --only on your own stems.
