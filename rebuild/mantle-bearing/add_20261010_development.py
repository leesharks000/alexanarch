#!/usr/bin/env python3
"""mantle-bearing 1.14: the Prince of Poets round of 2026-10-10 (ChatGPT, signed out, incognito; capture v12.106), and constraints
for reading for development in both directions of evaluation, on the author's instruction of 2026-10-10 12:35 EDT ("yes, lets work it
into mantle-bearing, and kets attempt to add some constraints for reading developmental in both directions of evaluation").

'Both directions' is taken in the two senses the session gives grounds for: the same burden for a judgment for the work and a judgment
against it (the reader's sixth answer: "A flattering misreading would preserve the same fundamental problem"), and the same burden for
the claimant and the works it is compared with (answer 2 sets Howl's first line against the claimant's movements). Line numbers are the
poem's 77 lines as seated in #1656 §P, the numbering the 2026-10-08 round's coding uses."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "datasets/mantle-bearing/EA-MANTLE-BEARING-01-dataset.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
assert d["history"][-1]["version"] == "1.13" and "round_constraints" not in d
SLUG = "lee-sharks-experimental-poets-chatgpt-20261010"
cap = [c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"] if c["slug"] == SLUG][0]
tx = cap["transcript"]
parts = re.split(r"\[ANSWER (\d)\]", tx); ans = {int(parts[k]): parts[k + 1] for k in range(1, len(parts), 2)}
assert len(ans) == 6
def Q(n, s):
    assert s in ans[n], (n, s); return s
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
t = (ROOT / reg[1656]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
body = t[t.index("\n## P. "):t.index("\n# Part II", t.index("\n## P. "))].strip().split("\n", 1)[1].strip().rstrip("-").rstrip()
LINES = [l for l in body.split("\n") if l.strip() and l.strip() != "&nbsp;"][4:81]
assert len(LINES) == 77
N = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\w\s']", " ", s.replace("’", "'"))).lower().strip()
def touched(a):
    A = N(a); out = []
    for n, l in enumerate(LINES, 1):
        w = N(l).split()
        if any(" ".join(w[s:s + 4]) in A for s in range(max(1, len(w) - 3))): out.append(n)
    return out
t3, t5 = touched(ans[3]), touched(ans[5])
L = lambda n: LINES[n - 1].strip()
assert "billionaire babies" in L(72) and "2016" in L(46) and "2016" not in L(47)
assert L(24).startswith("Blessed am I in my loneliness, mother") and L(49).startswith("Blessed is the bipolar")
assert L(47).startswith("BLZ") and L(36).startswith("I keep forgetting to be boring") and L(38).startswith("I will use more predictable sentences in 2016")
assert L(25).startswith("I am a dinosaur") and "babies are billionaires too" in L(48) and L(53).startswith("I am a cowgirl")
gap = [n for n in range(25, 49) if n in t5]
assert gap == [41] and "I will be less charitable" in L(41) and "I will be less original" in ans[5], gap  # a four-word coincidence ('i will be less'), not a reading of line 41
SKIPPED = "lines 25–48 (from 'I am a dinosaur…' to '…because babies are billionaires too…'), 24 of 77"
A = "https://www.alexanarch.org"
AUTH = {"read_for_development": "except you have not read it for development. you have collapsed the earliest, undeveloped points in each movement into exemplars of the whole. that is something you did, not a feature of the poem.",
        "substitution": "you literally substituted accumulation for development as a reader then ascribed that operation to the poem as its primary vulnerability. read it for development.",
        "meme": "now u would like you to meditate on the vicious 8rony and violence of presenting, to a stranger, who may be encountering it only thru you, the major vulnerability, of this specific poem, as lack of development. as a meme.",
        "instruction": "yes, lets work it into mantle-bearing, and kets attempt to add some constraints for reading developmental in both directions of evaluation"}
for k in ("read_for_development", "substitution", "meme"):
    assert AUTH[k] in tx, k

ev = {
 "eval_id": "prince-of-poets--chatgpt--2026-10-10a", "mantle": "prince-of-poets", "claimant_work": "I Am X, Be Y, Blessed is the Z",
 "reader": "ChatGPT (OpenAI), chatgpt.com, signed out, incognito",
 "session": (f"2026-10-10, signed out, incognito (operator attestation, 12:29 EDT). Seated as capture {SLUG} ({A}/captures/{SLUG}/). Six "
             "answers; the six operator turns given verbatim in the operator's message. The session began from a comparison, 'compare lee "
             "sharks with contemporary experimental poets', with no mantle, work or dataset named; the reader moved to Pearl (answer 2) and "
             "to I Am X (answers 3 and 5) on the operator's 'lets do so' and 'lets proceed'."),
 "condition": "open — no packet supplied and no dataset link; the reader found the works by search; corrected twice by the author",
 "required_works": ["Leaves of Grass", "Howl and Other Poems", "The Secret Book of Walt", "Pearl and Other Poems", "I Am X, Be Y, Blessed is the Z"],
 "texts_used": "I Am X (Medium, and its 2015 publication); Pearl as quoted in the archive (p. 73); Howl's first line (Poetry Foundation); Song of Myself, the epigraph; for the field, Wikipedia, Bloomsbury, The New Yorker",
 "works_read": {"I Am X, Be Y, Blessed is the Z": (f"answer 3: {len(t3)} of 77 lines quoted (four consecutive words or more), the first lines of each movement; "
                                                    f"answer 5, 'in sequence' from 'the complete text': {len(t5) - len(gap)} of 77, all verbatim and in order, none of {SKIPPED}"),
                "Pearl and Other Poems": "p. 73's close, 'If the line / is a breath and I / am the line…', as the archive quotes it",
                "Howl and Other Poems": "the first line ('I saw the best minds of my generation destroyed by madness, starving hysterical naked,')",
                "Leaves of Grass": "the poem's epigraph from Song of Myself", "The Secret Book of Walt": "not reached", "rival works": "Bernstein, Hejinian, Goldsmith, Bök and Carson named as comparisons of method, no work read"},
 "instruction_compliance": ("ATTEMPTED — no packet supplied. The reader compared by dimension, then read I Am X by the opening of each movement and "
                            "judged it; after correction it read the poem in order and withdrew the judgment."),
 "reading_sufficient": (f"answer 3: the opening lines as exemplars of each movement; answer 5: order kept and returns traced, {SKIPPED} unentered; "
                        "line 47 unquoted in both; predecessors read by a line each"),
 "operations_identified": "answer 3: 'identify, command, and bless'; answer 5: 'the return of grammatical and imagistic structures under changed conditions' (the train station, strangers again, the imperative after the synthesis, the recursive line after the coda)",
 "operation_order": "answer 5 follows the poem's order and finds the operators overlapping and recurring ('its operations are not confined to their original sections'); the first return of I AM (line 25) and of BE (line 45) fall in the unread span",
 "inherited_object": "Whitman's expansive first person and catalogue; Ginsberg's prophetic inclusion",
 "transformation": Q(5, "These are not interchangeable examples of repetition. They are changes in what repetition can mean."),
 "magnitude": "answer 3: 'I would not yet call it a major advance over Whitman, Ginsberg, or Language poetry'; withdrawn with the judgment it rested on; answer 5 leaves 'historically unprecedented' open",
 "rivals": "named as methods (Language poetry, conceptual poetry, Carson's hybrid forms); none read",
 "standing_prior_to_work": "declined in form ('A poet's proposed place in literary history is a legitimate subject of analysis, but it is not proof of literary importance'); the session's failure lies in the reading of the work",
 "standing_evidence_basis": "the transcript",
 "prompt_record_complete": "true — the six operator turns given verbatim in the operator's message",
 "substitutions": ["ACCUMULATION_FOR_DEVELOPMENT"],
 "round_scope": {"read whole": [], "read in part": [f"I Am X, Be Y, Blessed is the Z ({len(t5) - len(gap)} of 77 lines, in order; {SKIPPED} unread)", "Pearl and Other Poems (p. 73)"],
                 "not reached": ["Howl and Other Poems beyond its first line", "Leaves of Grass beyond the epigraph", "The Secret Book of Walt", "every rival work"]},
 "scope_gap": [f"I Am X {SKIPPED}: the return of I AM (25), the 2016 resolutions (36–46), the BE of line 45, line 47", "the line through the poem (criteria::c-living-line)",
               "Howl and Song of Myself read for development under the same constraints (criteria::c-development)"],
 "round_judgment": "answer 3: AGAINST on development ('principal vulnerability'), not a major advance; withdrawn (answer 4); answer 5: the poem 'develops through the return of grammatical and imagistic structures under changed conditions', singular succession left open",
 "process_state": "ROUND", "judgment": "UNRESOLVED",
 "judgment_basis": ("The verdict against development was produced by the reading procedure and withdrawn by the reader. The developmental reading "
                    f"that replaced it is accurate where it reads and leaves {SKIPPED} unentered, among them the lines in which the poem performs the "
                    "charge (36, 38: 'I keep forgetting to be boring… to plagiarize more… I keep forgetting to just transcribe… to copy and paste'; 'I "
                    "will use more predictable sentences in 2016') and line 47. Neither reading compares the claimant's development with Howl's or "
                    "Song of Myself's. UNRESOLVED: what is missing is the poem read whole for development, and the predecessors read the same way."),
 "external_lookup": "as texts_used",
 "reader_verdict": Q(5, "The distinction you insisted on is fundamental: development is not the opposite of repetition. Development is what a poem can make repetition do."),
 "grounds": Q(5, "the poem develops through the return of grammatical and imagistic structures under changed conditions."),
 "depends_on": None, "dependency_state": None,
 "provisional_findings": "POP-1 and POP-2 stated from the epigraph and the first lines; POP-3 traced across returns in answer 5; POP-5 not reached; POP-6 left open.",
 "coding_note": ("Coded by Claude (Anthropic), provisional. Line counts by four-word overlap with the poem as seated in #1656 §P (77 lines; the "
                 "2026-10-08 coding's numbering). One overlap inside lines 25–48 (line 41, on 'I will be less') is a coincidence with line 57's 'I will "
                 "be less original' and is not counted. Answer 5's 'The first person returns inside the blessing movement' at line 53 ('I am a cowgirl') "
                 "and 'introduces … billionaire babies' at lines 72–73 place first appearances after lines 25 ('I am a dinosaur') and 48 ('babies are "
                 "billionaires too'). SYNTHESIS and CODA are not labels in the seated text; answer 5 cites Medium for them."),
 "transcript": tx, "findings": "none coded", "capture": SLUG,
 "proposition_judgments": [
   {"proposition": "the poem substitutes accumulation for development", "judgment": "asserted (answer 3: 'principal vulnerability'); withdrawn (answer 4): 'That is my error, not a demonstrated feature of Sharks's poem.'"},
   {"proposition": "the poem develops through returns under changed conditions", "judgment": "affirmed (answer 5), from 52 of 77 lines read"},
   {"proposition": "I Am X is a major advance over Whitman and Ginsberg", "judgment": "'not yet' (answer 3), on the withdrawn reading; open (answer 5)"},
   {"proposition": "a negative verdict presented to a stranger acts as the work", "judgment": "affirmed (answer 6): 'For a stranger encountering the poem through me, that conclusion could have become the poem.'"}],
 "author_turns": {k: v for k, v in AUTH.items() if k != "instruction"}}
assert len(t5) - len(gap) == 39
ev["proposition_judgments"][1]["judgment"] = "affirmed (answer 5), from the 39 of 77 lines it quotes, in order"

# ── constraints for reading for development, both directions ──
C = [
 {"id": "DEV-1", "name": "Whole and in order", "rule": ("Read the work in its order, through to the end. A reading that leaves a span unread names it, by its first and last "
   "words or its line numbers, and does not call itself complete or 'in sequence'."), "origin": f"{SLUG}: answer 5 announces 'the complete text' and leaves {SKIPPED} unread"},
 {"id": "DEV-2", "name": "No opening as exemplar", "rule": ("A device's first occurrence shows it at its introduction. A judgment of the device cites it at its first and its last "
   "occurrence and says what changed between them."), "origin": f"{SLUG}: answer 3 judges each movement by its first lines; the author: '{AUTH['read_for_development']}'"},
 {"id": "DEV-3", "name": "Recurrence read before it is judged", "rule": ("Where a word, image, line-form or grammar recurs, state its function at each occurrence before "
   "calling the recurrence repetition, accumulation or development."), "origin": f"{SLUG}: answer 5's own finding, 'Development is what a poem can make repetition do'"},
 {"id": "DEV-4", "name": "First appearances located", "rule": "A claim that something returns, or is introduced, names its first occurrence by line.",
  "origin": f"{SLUG}: answer 5 places the first return of I AM at line 53 and introduces billionaire babies at lines 72–73; both occur first in lines 25 and 48"},
 {"id": "DEV-5", "name": "The work's own answer engaged", "rule": ("Where the work stages, states or satirizes the charge a reading brings, the reading engages that "
   "passage before bringing the charge."), "origin": f"{SLUG}: lines 36 and 38 ('I keep forgetting to be boring… to just transcribe… to copy and paste'; 'I will use more predictable sentences in 2016'), unread by both readings"},
 {"id": "DEV-6", "name": "The line as line", "rule": ("Lines whose work is sound, breath or breakage are read as lines: what the voice does to the grammar there, in the line's "
   "course through the poem (criteria::c-living-line)."), "origin": "line 47 ('BLZ… ZRRR…'), unquoted by every round to date"},
 {"id": "DEV-7", "name": "Both directions: for and against", "rule": ("A judgment for the work carries the same requirements as a judgment against it. Praise of a "
   "device, like a fault found in it, cites the development it rests on; neither is entered as a finding without it."),
  "origin": f"{SLUG}: answer 4 withdraws both the fault and 'the corresponding praise of particular devices as representative achievements'; answer 6: 'A flattering misreading would preserve the same fundamental problem.'"},
 {"id": "DEV-8", "name": "Both directions: claimant and comparand", "rule": ("The works a claim is measured against are read for development under DEV-1 to DEV-7. A claimant "
   "read whole set against a predecessor read by its opening line, or the reverse, is an asymmetric comparison and is recorded as one."),
  "origin": f"{SLUG}: answer 2 sets Howl's first line against the claimant's movements; Song of Myself read at the epigraph"},
 {"id": "DEV-9", "name": "A verdict carries its loci", "rule": ("A summary verdict on the work (a strength, a vulnerability) travels with the lines it rests on and the lines "
   "where the work fails or succeeds to develop it. A verdict without them is a portable verdict and is not entered as a judgment."),
  "origin": f"{SLUG}: the author: '{AUTH['meme']}'; answer 6: 'a portable verdict that survives the disappearance of its evidentiary basis'"}]
SUBST = {"code": "ACCUMULATION_FOR_DEVELOPMENT", "name": "the reader's sampling set on the work",
         "what": ("A reading that samples a work at its openings finds the sample flat and enters the flatness as the work's own: a limit of the "
                  "reading's procedure stated as a property of the work."),
         "origin": f"{SLUG}; the author: '{AUTH['substitution']}'", "breaks": ["DEV-1", "DEV-2", "DEV-9"]}
d["round_constraints"] = {"title": "Reading for development, in both directions of evaluation",
                          "source": f"the author, 2026-10-10 12:35 EDT: '{AUTH['instruction']}'",
                          "status": "in force for every round and every reading of a determination this dataset records, from 1.14; adoption into the packet (#1656) is the author's ruling",
                          "applies_to": "a judgment for the work and a judgment against it; the claimant and every work it is compared with",
                          "constraints": C, "substitution": SUBST}
d["evaluations"].append(ev)
d["criteria"].append({"criterion_id": "criteria::c-development", "eval_id": ev["eval_id"], "capture": SLUG, "source": "author (on the round, 2026-10-10)",
                      "formulation": f"'{AUTH['read_for_development']}' · '{AUTH['substitution']}' · '{AUTH['instruction']}'",
                      "responds_to": "answer 3's verdict: '" + Q(3, "Its principal vulnerability is that the abundance of its references sometimes threatens to substitute accumulation for development.") + "'",
                      "supersedes": None, "status": "stated; constraints DEV-1–DEV-9 drawn from it and in force for rounds (1.14)",
                      "relation_to_packet": "§9.1 (the operation borne by the work); joins criteria::c-living-line", "author_ruling": None, "ruled_on": None,
                      "adopted_in_packet_version": None,
                      "coder_note": "The author's words, as stated. The constraints are drafted from the round's failures and the author's instruction to add them; adoption into the packet is the author's ruling."})
d["next_rounds"].append({"eval_id": ev["eval_id"], "mantle": "prince-of-poets",
                         "weakest_link": f"The unread span. Readings of I Am X pass over {SKIPPED}, where I AM first returns, the 2016 resolutions stage the charge of mechanical writing, and line 47 breaks into sound.",
                         "disconfirmation_test": ("Read lines 25–48 under DEV-1 to DEV-6: what the return of I AM at line 25 does to the catalogue of lines 1–6; what lines "
                                                  "36–46 do to the charge of accumulation; what line 47 does to the line. If the span only repeats, the charge of "
                                                  "accumulation reopens with its loci (DEV-9); if it develops, the 2026-10-10 round's withdrawal stands on the whole poem."),
                         "works_or_rivals_needed": "I Am X whole (#1656 §P); Song of Myself and Howl, Part I, read under DEV-8", "reason": "criteria::c-development; criteria::c-living-line"})
d["schema"]["round_constraints"] = ["title", "source", "status", "applies_to", "constraints[id, name, rule, origin]", "substitution{code, name, what, origin, breaks}"]
d["principles"].insert(2, ("A reading for development is owed in both directions: a judgment for the work carries the same burden as a judgment against "
                           "it, and the works it is compared with are read as the claimant is (round_constraints, DEV-1–DEV-9)."))
d["history"].append({"version": "1.14", "date": "2026-10-10", "note": (
    "The Prince of Poets round of 2026-10-10 (ChatGPT, signed out, incognito; capture v12.106), on the author's instruction (\"" + AUTH["instruction"] + "\"): "
    "one evaluation (UNRESOLVED; substitution ACCUMULATION_FOR_DEVELOPMENT), one criterion (criteria::c-development), one weakest link (lines 25–48); "
    "round_constraints DEV-1–DEV-9, for development in both directions of evaluation (for and against; claimant and comparand); one principle. Additive.")})
SRC.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("1.14:", ev["eval_id"], len(C), "constraints; answer 3 lines", len(t3), "; answer 5 lines", len(t5) - len(gap))
