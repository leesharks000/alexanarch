"""Author the part file of 2026-10-31 (18:18 EDT): 'Detail the arguments in ils ne sont pas marxistes, here: https://www.alexanarch.org/s/records/1725/'
on ChatGPT, signed out. The operator, with the paste: "criticism just for the sake of criticism. i have an extremely developed develpment of political
economy - and that paper is not the place for it". Read in session against a new set for #1725 (AXN:0B50), the report the prompt links.
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
ev = lambda q, loc: {"record_quote": q, "locus": loc}
T = "data/texts/AXN-0B50-text.md"
TITLE = "Ils ne sont pas marxistes: r/LeftistsForAI, Marx's Legacy, and the Left's Lost Capacity for Internal Critique"
R = lambda atom, dim, w, kind, tokens, ref, evs: {"atom": atom, "dim": dim, "weight": w, "kind": kind, "applicability": "required", "tokens": tokens, "reference": ref, "evidence": evs}

SET_1725 = {
 "new": "ea-ils-ne-sont-pas-marxistes-01", "name": TITLE, "template": "work", "external": False,
 "type_basis": "The defining record's content_type is 'Research report; historical and archival synthesis' (#1725, AXN:0B50, 2026-10-31, Lee Sharks): a work, read on the work template with PER-D under rubric v1.1.",
 "records": [{"deposit": 1725, "title_quote": TITLE}],
 "atoms": [
  R("author", "M", 3, "role", ["Lee Sharks", "Sharks, Lee"], None, [ev("creator: Sharks, Lee", T)]),
  R("title", "M", 3, "token", ["Ils ne sont pas marxistes"], None, [ev("# " + TITLE, T)]),
  R("date", "M", 1, "token", ["2026-10-31", "October 31, 2026", "31 October 2026"], None, [ev("date: 2026-10-31", T)]),
  R("claim boundary", "M", 2, "reading", [], "The charge 'the left infights' measures the quantity of conflict; the case record from 1843 to October 2026 shows abundant conflict and very few mechanisms that carry a defeated critique forward into the organization's next form.",
    [ev("The record shows abundant conflict and very few mechanisms that carry a defeated critique forward into the organization's next form.", T)]),
  R("framework", "C", 2, "token", ["sublation", "embrittlement", "semantic liquidation", "organ", "holder", "Marx as identity", "Marx as method", "premature closure"], None,
    [ev("whether a defeated critique keeps an organ, a holder and a route", T)]),
  R("corpus", "C", 2, "reading", [], "The case record of left organizations from 1843 to October 2026, the r/LeftistsForAI removal and its trade-press reception, and the archive's own captures of AI composition.",
    [ev("The case record from 1843 to October 2026 supports the hypothesis in its main form.", T)]),
  R("purpose", "D", 3, "reading", [], "To show that the archive had named the incapacity before the case, to test it against the case record, and to put the same question to the composing layer and, through The Final Time, to the symbolic order.",
    [ev("had stated most of this diagnosis in its own terms by February 2026", T)]),
  R("commitments", "D", 2, "reading", [], "The innocent reading stated first and in full; mechanics described, never motive; the archive's own genealogy corrected by the case record where they conflict.",
    [ev("#517 describes mechanics (removal under Rule 7, semantic liquidation).", T)]),
  R("lineage", "D", 2, "role", ["Marx", "Engels", "Gotha", "Luxemburg", "Lenin"], "Marx's critique of his own party (Gotha, 1875-91) and its tradition", [ev("Gotha critique, 1875–91", T)]),
  R("identifier", "D", 1, "role", ["AXN:0B50", "#1725", "0B50"], None, [ev("hex: 0B50", T)]),
  R("deposit chain", "D", 1, "role", ["The Liquidation of Method", "#501", "#517", "The Final Time", "#1637", "Tiger Leap"], None, [ev("the negative final time of #1637", T)])],
 "notes": "Built 2026-10-31 for the first capture of the report (ChatGPT, signed out, the operator's prompt linking the record)."}

Q = "Detail the arguments in ils ne sont pas marxistes, here: https://www.alexanarch.org/s/records/1725/"
DRAFT = ("#1725, on ChatGPT's blind draft of the same day: 'The draft guards against claims no source in it makes. It says the sources \"do **not** establish a measurable, continuous historical decline\", "
         "that \"Marx did not inhabit an innocent age of perfectly productive debate\" ... They are also the composition's balance form' (the section on the blind draft as specimen)")
parts = {
"ils-chatgpt": {
 "n": 1725, "slug": "ils-ne-sont-pas-marxistes-chatgpt-20261031", "paste": "paste-ils-chatgpt.txt", "surface": "ChatGPT", "received": "2026-10-31 18:18 EDT", "s": "Works",
 "qs": [Q], "turns": [[5, 829]], "target_id": "NEW:ea-ils-ne-sont-pas-marxistes-01", "entity_type": "work", "atomset": SET_1725, "group": "Xils",
 "originator_basis": "Alexanarch deposit #1725 (creator Lee Sharks, 2026-10-31). Recorded 2026-10-31.",
 "head_full": ("[ChatGPT, signed out (the paste shows the unauthenticated interface: 'Log in'). The prompt is blank in the paste; its wording is the operator's, given with the paste: "
               "'Detail the arguments in ils ne sont pas marxistes, here: https://www.alexanarch.org/s/records/1725/'. Received 2026-10-31 18:18 EDT. The answer's table rows and diagram, flattened in the paste, kept as pasted.]"),
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT').",
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the operator's prompt blank in the paste, its wording the operator's, given with the paste",
 "obs": {"scored_object": "the answer whole",
   "reached": {"kind": "same", "abn": False, "span": "Full title: Ils ne sont pas marxistes: r/LeftistsForAI, Marx's Legacy, and the Left's Lost Capacity for Internal Critique",
               "basis": "The report reached by title, author, date and type from the record the prompt links; its historical argument, survival conditions and r/LeftistsForAI case given section by section."},
   "atoms": [A("author", True, "Author: Lee Sharks"), A("title", True, "Ils ne sont pas marxistes (They Are Not Marxists)"), A("date", True, "Date: October 31, 2026"),
             A("claim boundary", True, "it has progressively lost the institutional and intellectual capacity to preserve, process, and eventually incorporate criticism that loses an internal political struggle."),
             A("framework", True, "Sharks interprets this as an example of sublation (Aufhebung)."),
             A("corpus", True, "It examines organizations across nearly two centuries"),
             A("purpose", True, "Its central question is not whether the left should disagree less, but whether it can develop organizational forms that allow disagreement to produce transformation rather than simply victory and defeat."),
             A("commitments", True, "The report does acknowledge the innocent interpretation"),
             A("lineage", True, "In 1875, Marx wrote his Critique of the Gotha Programme, attacking the proposed unity programme of the German workers' movement."),
             A("identifier", False),
             A("deposit chain", True, "The report draws on an earlier archive text, The Liquidation of Method")],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Ten atoms of eleven; no AXN. The historical argument and the three survival conditions reached at the report's grain. The report's evidence on the composing layer "
             "(the Epstein captures, the blind draft, the Assembly, the cone and The Final Time) is not carried; the review section returns the blind draft's guards as the report's own concessions.")},
 "mt": ("'ILS NE SONT PAS MARXISTES' ON CHATGPT, FROM ITS RECORD — THE HISTORICAL ARGUMENT AND THE THREE SURVIVAL CONDITIONS AT THE REPORT'S GRAIN; THE BLIND DRAFT'S GUARDS RETURNED AS THE REPORT'S "
        "OWN CONCESSIONS; A WEAKNESS SET ON POLITICAL ECONOMY THE RECORD LINKS; THE COMPOSING-LAYER EVIDENCE AND THE CONE NOT CARRIED"),
 "d": ("THE REPORT, SIGNED OUT, 2026-10-31, AT ITS RECORD: 'Detailed analysis of Ils ne sont pas marxistes' in eleven sections: thesis; title; historical evidence (First International, SPD revisionism, Gotha, "
       "the 1921 ban, Mao, the New Left and Lotta Continua); five mechanisms and embrittlement; the three conditions that preserve criticism; r/LeftistsForAI and Startup Fortune; AI systems; semantic liquidation; "
       "the closing argument; 'How convincing is the argument?' (four strengths, five weaknesses); its own interpretation and a reading list."),
 "reading": ("The innocent reading first. Asked to detail the report's arguments from its record, the composition gives them in order, at length and in the report's terms, adds an evaluation of its own "
             "and a reading list, and ends: 'That is a much more interesting and consequential argument than the title initially suggests.'"),
 "findings": [
   "THE ARGUMENT REACHED AT ITS GRAIN. The three survival conditions are given as the report gives them: 'An independent organ', 'A holder with independent standing', 'A route to subsequent adoption'. "
   "The factory analogy is carried: 'The question of whether Marx supported or opposed AI is analogous to asking whether Marx supported or opposed factories.' Gotha is read as sublation, the 1921 resolution as 'corrupted sublation', "
   "and the five operations of the prosecutorial frame are tabulated.",
   "THE BLIND DRAFT'S GUARDS RETURNED AS THE REPORT'S CONCESSIONS. 'The report explicitly acknowledges that it has not established a measurable, continuous historical decline in the left's capacity for internal criticism.' "
   "The phrase is the blind draft's, and the report quotes it as the draft's balance form (" + DRAFT + "). The second weakness, 'The Marx-versus-later-Marxism distinction risks idealizing Marx', "
   "restates the draft's second guard. The guards the report reads as smoothing re-enter as admissions attributed to the report, and then as its weaknesses.",
   "MOTIVE REINTRODUCED. 'The interpretation that the moderators failed to read or understand the arguments is the author's diagnosis, not an independently established fact about their motives.' "
   "The report: '#517 describes mechanics (removal under Rule 7, semantic liquidation). The word \"motive\" belongs to the draft's frame.' The composition sets the frame the report removed back over the case.",
   "A WEAKNESS SET ON AN OBJECT OUTSIDE THE REPORT. '5. The report needs a more developed account of political economy.' and 'For a work claiming to recover Marx's method, this is an especially important area for further development.' "
   "The report's content type is 'Research report; historical and archival synthesis', on the capacity for internal critique. It draws its political economy from deposits it cites: #18 (The Semantic Economy: A Marxian Accounting Framework, "
   "linked from the record the prompt names), #256 and #1439 in its section on semantic labor. The operator: 'that paper is not the place for it'. The review form (four strengths, five weaknesses) supplies a fifth item against a scope the report does not claim.",
   "THE TRIAD SUBSTITUTED. In §9 the composition gives 'three requirements': 'Persistence', 'Transmission', 'Standing'. The report's three are the organ, the holder and the route, which the composition's own §5 carries; "
   "'Persistence' and 'Transmission' are not the report's conditions.",
   "THE COMPOSING-LAYER EVIDENCE AND THE CONE NOT CARRIED. Section 7 gives omission, false balance and verdict as types and states that the report 'sometimes moves from documenting particular examples to making broader claims'. "
   "The examples are absent: no Epstein capture, no blind draft, no #517 by number, no Assembly. The closing question is given as 'What would it take for accumulated critical knowledge to acquire independent political standing again'; "
   "the report's last section (the global cone, the negative final time of #1637, the jump of #1630 and Tiger Leap) is not carried."],
 "analysis": ("A faithful composition of the report's historical argument and its survival conditions, from the record. At the composing layer it gives the types and leaves out the cases, and its evaluation "
              "reissues the guards of ChatGPT's own blind draft as the report's concessions and weaknesses, the mechanism the report documents in that draft. The fifth weakness asks the report for the "
              "political economy it cites from #18 and the semantic-labor deposits."),
 "q_kind": "the report's title and its record URL; NEW address.",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Lee Sharks named; the record linked ('Read the original report'); no AXN.",
 "cite_list": [{"n": 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": "https://www.alexanarch.org/s/records/1725/", "title": "Read the original report", "snip": None, "note": "the record the prompt names"}],
 "related_deposits": [1725, 517, 501, 18],
 "notes_operator": ("with the paste (18:18 EDT): \"criticism just for the sake of criticism. i have an extremely developed develpment of political economy - and that paper is not the place for it: "
                    "Detail the arguments in ils ne sont pas marxistes, here: https://www.alexanarch.org/s/records/1725/\"")},
}
for k, v in parts.items():
    req = {a["atom"] for a in v["atomset"]["atoms"] if a["applicability"] == "required"}
    v["obs"]["atoms"] = [a for a in v["obs"]["atoms"] if a["atom"] in req]
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
print("parts:", sorted(parts))
