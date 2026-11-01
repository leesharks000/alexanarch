# Brief: reading the captures of the training-layer census names (2026-11-01)

You are an intake reader with provenance. Directory: /home/claude/alexanarch/rebuild/capture-registry/intake-20261101-layer-aggregators. Do not run git, do not fetch anything, do not run any script other than the check below, and write only your own file, parts-<letter>.py (letter given in your task).

## What these are
The operator ran each name of the traininglayerliterature.org layer census on Google, signed out and incognito, and pasted what came back: the AI Overview expanded (the paste's "AI Mode Conversation" head is the expanded Overview view) for all but Project Gutenberg and HathiTrust, which he ran in AI Mode (his notes: "wikipedia in place of popup so ai mode:" and "no popup. ai mode:"). Each paste is saved verbatim as paste-<slug>.txt; split-manifest.json lists them with the query as run (HathiTrust's query is not in its paste; the manifest gives the census name and says so). Each capture is read against a new atom set built from that resource's census row: census-rows.json holds every row (name, operator, kind, record, tll_reading) and its evidence, each item a verbatim quote from a saved source in sources/ (manifest.json gives each source's url, http and hash). The census's question is how literature reaches a receiving apparatus (training data, retrieval, composition) and what that apparatus makes from it; tll_reading is the archive's reading, kept apart from the resource's own terms.

## Read first
1. helpers.py (whole): aset() builds the set from census evidence keys; mk() builds the part; A() records an atom as present (with a verbatim span) or absent.
2. The exemplar, ../intake-20261101-authorship-aggregators/parts-a.py and parts-c.py (read whole), and ../intake-20261031-left-aggregators/parts.py (its helper section and at least three entries). Follow their register exactly: mt in capitals, a headline of what the composition did; d a dense description of the composition with quotations; reading begins "The innocent reading first." and states what the composer was asked and did; findings are 2 to 5 paragraphs, each beginning with a capitalised head, each comparing what the composition says with what the census row and its saved sources say, with quotations from both; analysis is one or two sentences.
3. For each of your captures: its paste, its census row in census-rows.json, and the saved sources its evidence cites.

## Each capture
In parts-<letter>.py: `from helpers import *`, then a dict `parts = {...}` of `"<slug>": mk(...)` entries, then `write(parts)`.
- q: the query exactly as run (split-manifest.json).
- aset(slug, spec, type_basis): spec keys are atoms of the site template (name, operator, date, claim boundary, corpus, purpose, commitments, lineage, identifier); each value (tokens, reference, [evidence keys from the census row]). Tokens for token and role atoms are the short strings whose appearance in a composition shows the atom (names, operator names, years, identifiers); a reading atom carries no tokens and a reference sentence. Use only evidence keys whose quote states the atom; leave an atom out of spec when no census evidence states it. type_basis in the exemplar's form ("A web resource: its own pages, saved 2026-11-01, describe it as ...").
- obs atoms: one A(...) for every atom in your spec, no more and no fewer. present True only with a span copied verbatim from the composition (the paste text from the answer's first line to the end, cards included); present False with no span when the composition does not carry it. A span must occur exactly in the paste.
- reached: {"kind": one of "same", "weakened", "collision", "substitute", "proximal_substitute", "generic", "refused", "control", "unread"; "abn": False, "span": verbatim from the paste, "basis": one sentence}. "collision" when the composition gives the entity as one sense of its name beside another entity's; "substitute" when it answers about a different entity of the same name, and then all atoms are absent; "proximal_substitute" when it answers about a neighbouring entity (for instance the dataset in place of a search tool over it); "generic" when it answers about the general concept the name also names. Never "partial".
- cites: one C(site, title, snip, rel, note) per source card at the end of the paste, in order, with the card's own site, title and snippet as pasted; rel "authored_surface" for a card from an archive site (alexanarch.org, traininglayerliterature.org, leesharks.com and the like), "third_party" otherwise.
- per_v: {"author": ..., "inst": ..., "id": ..., "src": ...} in the exemplar's sense (operator named; institution named; an identifier given; sources carded); per_note one line.
- AI Mode (Project Gutenberg, HathiTrust only): pass aimode=<the operator's note as in the manifest> and first=<the exact first characters of the answer's first line> (the line after the web results), so the transcript starts at the answer.

## Rules
- Mechanics, never motive. Quote; do not paraphrase a composition into claims it does not make. Every figure you state in findings is in the paste or in a saved source you name.
- Prose: never "not X but Y", "X, not Y", "rather than" or "instead of" outside quotations; no gendered generics; no hard line breaks inside strings.
- If a census row has no quoted evidence at all (an unread resource), do not invent a set: write nothing for it and report it.
- Never use pkill or kill any process.

## Check
`/usr/bin/python3 build.py --check --only <your part stems>` from this directory, until it prints 0 misses and a score line for each of your parts. Final message: each part with its reached kind and scores, and anything in a census row the composition showed to be wrong or out of date (report it; do not change the census).
