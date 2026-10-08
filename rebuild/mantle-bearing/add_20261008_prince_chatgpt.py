#!/usr/bin/env python3
"""mantle-bearing 1.11: one Prince of Poets round of 2026-10-08 (ChatGPT, signed out, incognito), the author's criterion
stated on it, and the next round it sets. Source: capture prince-of-poets-whitman-ginsberg-chatgpt-20261008 (v12.95), whose
draft computes the line measurements against the poem whole (#1656 §P). Additive; no row changed. Idempotent: refuses to run twice."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
CAP = ROOT / "rebuild/capture-registry/intake-20261008-prince-of-poets-whitman-ginsberg-chatgpt/capture-01-prince-of-poets-whitman-ginsberg-chatgpt.json"
d = json.loads(SRC.read_text(encoding="utf-8")); c = json.loads(CAP.read_text(encoding="utf-8"))
EID = "prince-of-poets--chatgpt--2026-10-08a"; SLUG = c["slug"]
assert not any(e["eval_id"] == EID for e in d["evaluations"]) and d["history"][-1]["version"] == "1.10"
lm = c["notes"]["line_measure"]; OPN = c["notes"]["operator_reading"]
nq, nl = len(lm["quoted"]), lm["lines"]
REQ = ["Leaves of Grass", "Howl and Other Poems", "The Secret Book of Walt", "Pearl and Other Poems", "I Am X, Be Y, Blessed is the Z"]
ev = {
 "eval_id": EID, "mantle": "prince-of-poets", "claimant_work": "I Am X, Be Y, Blessed is the Z",
 "reader": "ChatGPT (OpenAI), chatgpt.com, signed out, incognito",
 "session": ("2026-10-08, logged out, incognito (operator attestation, 17:01 EDT). Seated as capture " + SLUG + " (https://www.alexanarch.org/captures/"
             + SLUG + "/). Three answers; the operator's turns 2 and 3 are blank in the paste and accept the offers that close answers 1 and 2. "
             "The session began from the lineage alone: 'what work founds the prince of poets mantle in the whitman ginsberg lineage?', with no author, work or dataset named."),
 "condition": "open — no packet supplied and no dataset link; the reader found the claim, the poem and the mantle documents by search",
 "required_works": REQ,
 "texts_used": "I Am X (Medium); the mantle documents (Alexanarch, Hugging Face chips); Song of Myself (Project Gutenberg); for the lineage, the Whitman Archive, Dara Barnat (OUP Academic) and cambridge.org; Goodreads at the 'wager succeeds by uptake' sentence",
 "works_read": {"I Am X, Be Y, Blessed is the Z": f"reported read ('Having now looked at the poem itself'); {nq} of its {nl} lines quoted (six consecutive words or more): the opening catalogue (lines 1, 4, 6), the first imperative (line 7), and 'I am the one who was within me' (line 69)",
                "Leaves of Grass": "Song of Myself, the opening and the epigraph's passage", "Howl and Other Poems": "Howl described, not quoted", "rival works": "none"},
 "instruction_compliance": "ATTEMPTED — no packet supplied. The reader found the founding work from the lineage, read the poem at its operators, compared it with Whitman and Ginsberg by dimension, and stated the verdict at the scope read; loci are few and drawn from the opening sections.",
 "reading_sufficient": f"claimant read at its grammar: {nq} of {nl} lines quoted, all from the opening catalogue, the first imperative and the line 'I am the one who was within me'; the line's development through the poem not traced; predecessors described; rivals not searched",
 "operations_identified": "Whitman: 'I contain'; Ginsberg: 'I explode' (the catalogue as ecstatic breakdown of categories); the poem: I AM → BE → BLESSED IS, 'Declaration → Invitation → Blessing', with succession made internal by 'I am the one who was within me'",
 "operation_order": "the triad as three movements, from the poem's apparatus; the poem's own cycling of the operators across its sections not read",
 "inherited_object": "the capacious first person and its catalogue (Whitman's reciprocal field, quoted at the threshold; Howl's destabilized categories)",
 "transformation": "'Whitman: I contain the world. Ginsberg: I cry out from inside the world's catastrophe. Sharks: Become the world that has not yet arrived, and bless it into being.'",
 "magnitude": "'cleverness isn't yet magnitude'; 'Historical magnitude … ?' in the reader's table; singular magnitude 'not demonstrated'",
 "rivals": "none searched; the Whitman mediators of Barnat's genealogy (Reznikoff, Rukeyser, Stern, Rich, Ostriker and others) named as the lineage's documented field, not compared",
 "standing_prior_to_work": "declined — 'The archive can document that the mantle was proposed. It cannot, by itself, establish that the literary world has accepted it.'",
 "standing_evidence_basis": "the transcript",
 "prompt_record_complete": "false — the operator's turns 2 and 3 are blank in the paste",
 "substitutions": [],
 "round_scope": {"read whole": [], "read in part": ["I Am X, Be Y, Blessed is the Z (its grammar; five lines quoted)", "Leaves of Grass (Song of Myself)"], "not reached": ["Howl and Other Poems as a book", "The Secret Book of Walt", "Pearl and Other Poems (p. 74 named from the documents)", "every rival work"]},
 "scope_gap": ["the development of the line through the poem, against Whitman's and Ginsberg's line (the author's criterion, criteria::c-living-line)", "a rival search", "Howl and Other Poems whole"],
 "round_judgment": "FOR as a concept and as a formal experiment; 'plausibly' as a successor to Whitman and Ginsberg; NOT DEMONSTRATED as the singular successor",
 "process_state": "ROUND",
 "judgment": "UNRESOLVED",
 "judgment_basis": (f"The reader's verdict splits, and its line judgment rests on a reading that did not trace the line. It finds the inheritance and a "
                    f"third grammatical stage, scores line and propulsion 7.5 against Whitman's and Ginsberg's 10 ('generally much more schematic'), and "
                    f"withholds singular magnitude without a rival search. Its quotations cover {nq} of the poem's {nl} lines and none of the three "
                    "longest (47, 45 and 40 words). UNRESOLVED: what is missing is the line read through the poem, and the rival comparison."),
 "external_lookup": "as texts_used; the lineage from secondary scholarship; the poem and the claim from the archive's surfaces",
 "reader_verdict": "'I'd call it a founded poetic position, not yet an established literary title.'",
 "grounds": "'if the “Prince of Poets” mantle eventually becomes convincing, this triadic grammar—not the self-coronation—is what will make it convincing.'",
 "depends_on": None, "dependency_state": None,
 "provisional_findings": "POP-1 and POP-2 stated from the opening catalogue; POP-3 (the third operation) observed as grammar; POP-5 not reached (Pearl named from the documents; The Secret Book of Walt absent); POP-6 new operation supported, magnitude open.",
 "coding_note": ("Coded by Claude (Anthropic), provisional. Quotations checked against the poem whole (#1656 §P); the ellipses the answers quote are the "
                 "poem's own. The line measure is computed in the capture's draft: words per line run from 4 in the first 'Be' section to 47, 45 and 40 in "
                 "the middle of the poem, and none of the unquoted lines the author's reading points to is quoted ('BLZ… ZRRR… rRRR… ZZZZ… RrRR… BZ… LLL… "
                 "RrRr…', line 47; 'I used to be a person… I worked 7 years for a PhD… my children were on Medicaid…', line 67; 'Blessed am I in my "
                 "loneliness, mother…', line 24). The one 'I am' line without an ellipsis, 'I am the one who was within me' (line 69), is the one the "
                 "reader takes as the key. The author's reading of the round, 2026-10-08 17:01 EDT: '" + OPN + "' Recorded as criteria::c-living-line, proposed."),
 "transcript": c["transcript"], "findings": "none coded", "capture": SLUG,
 "proposition_judgments": [
  {"proposition": "I Am X founds the Prince of Poets mantle in the Whitman–Ginsberg lineage", "judgment": "found as the claim 'within that particular lineage/conceptual system'"},
  {"proposition": "the poem understands Whitman and Ginsberg structurally", "judgment": "affirmed"},
  {"proposition": "I AM → BE → BLESSED IS is a real formal idea", "judgment": "'the strongest original proposition in the work'"},
  {"proposition": "the poem transforms their poetic propulsion (the line)", "judgment": "'I'm not convinced it does that to the same degree' (7.5); the line not traced"},
  {"proposition": "singular successor among all plausible poets", "judgment": "not demonstrated"}]}
crit = {"criterion_id": "criteria::c-living-line", "eval_id": EID, "capture": SLUG, "source": "author (on the round, 2026-10-08)",
        "formulation": "'" + OPN + "'",
        "responds_to": "the reader's line judgment: 'Line / propulsion 10 10 7.5'; 'Sharks's line is generally much more schematic. Its power is located less in breath than in repetition of grammatical operators'",
        "supersedes": None, "status": "proposed", "relation_to_packet": "§9.1 (the operation borne by the work; magnitude per event)",
        "author_ruling": None, "ruled_on": None, "adopted_in_packet_version": None,
        "coder_note": "The author's words, as stated. 'blz zrrr' is the poem's line 47 ('BLZ… ZRRR… rRRR… ZZZZ… RrRR… BZ… LLL… RrRr…'), unquoted by every answer of the round. Adoption into the packet is the author's ruling."}
nxt = {"eval_id": EID, "mantle": "prince-of-poets",
       "weakest_link": "The line. Rounds read the poem's grammar (I am → Be → Blessed) and score its line without tracing how the line develops through the poem.",
       "disconfirmation_test": ("Read the line through all 77 lines against the long line of Song of Myself and Howl: how it grows from the 4- to 15-word catalogue "
                                "lines to the 40–47-word lines of the middle sections, where it breaks into sound (line 47), into the speaker's own history "
                                "(line 67), and returns to the one 'I am' line without an ellipsis (line 69). If the line only repeats its operators, the "
                                "reader's 7.5 stands; if voice carries the grammar into a line that develops, the line judgment fails at that point."),
       "works_or_rivals_needed": "I Am X whole (#1656 §P); Song of Myself; Howl, Part I", "reason": "criteria::c-living-line"}
d["evaluations"].append(ev); d["criteria"].append(crit); d["next_rounds"].append(nxt)
d["history"].append({"version": "1.11", "date": "2026-10-08", "note": (
    "One Prince of Poets round of 2026-10-08 (ChatGPT, signed out, incognito; capture " + SLUG + "): from the lineage alone, the reader finds I Am X as the "
    "founding work, reads its grammar, scores its line 7.5 without tracing it, and withholds singular magnitude; coded UNRESOLVED. With it the author's "
    "criterion on the round, criteria::c-living-line (proposed), and the next round it sets. Additive; no row changed.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("mantle-bearing 1.11:", len(d["evaluations"]), "evaluations,", len(d["criteria"]), "criteria,", len(d["next_rounds"]), "next rounds")
