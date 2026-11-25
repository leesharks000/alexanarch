"""Draft for 'Through Another's Mouth: A Dialogue between Heteronyms' on Google AI Overview, 2026-11-25. Seat with:
    python3 scripts/capture_intake.py rebuild/capture-registry/intake-20261125-through-anothers-mouth/draft.json --seat"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
T = (H / "paste.txt").read_text(encoding="utf-8")
A = [("author","M",3,"role",True,"written by Johannes Sigil, one of the twelve declared literary heteronyms (the Dodecad) created by author and theorist Lee Sharks"),
     ("title","M",3,"token",True,"Through Another's Mouth: A Dialogue between Heteronyms"),
     ("date","M",1,"token",True,"Published on November 24, 2026"),
     ("claim boundary","M",2,"reading",True,"Glas attempts to condense Aristotle's Politics into a single paragraph, cutting off ... before its crucial qualifying clause; It closes by returning to Aristotle's unresolved triad"),
     ("framework","C",2,"token",True,"the public companion to the essay From the Position of the Rejected (#1806)"),
     ("tradition","C",2,"reading",True,"a literary and philosophical dialogue; following in the literary tradition of Fernando Pessoa and Søren Kierkegaard"),
     ("corpus","C",2,"token",True,"the reading room of the Crimson Hexagon Archive"),
     ("lineage","D",2,"role",True,"the public companion to the essay From the Position of the Rejected (#1806); Aristotle's Politics"),
     ("deposit chain","D",2,"token",True,"medium.com/@leesharks00/through-anothers-mouth-a-dialogue-between-heteronyms-0d882d5ccd3c"),
     ("identifier","D",3,"token",False,None),
     ("licence","D",1,"token",False,None)]
draft = {
 "date": "2026-11-25", "dates": ["2026-11-25"],
 "surface": "Google AI Overview", "surfaces": ["Google AI Overview"],
 "surface_basis": "Operator default of 2026-10-01; the 'AI Mode Conversation' heading of the paste is the Overview expanded (operator, 2026-10-18), recorded as surface and not as a marker.",
 "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-14.",
 "ev": "paste", "turns": 1,
 "slug": "through-anothers-mouth-dialogue-heteronyms-aio-20261125",
 "s": "Works",
 "q": "Through Another's Mouth: A Dialogue between Heteronyms",
 "originator": {"name": "Sigil, Johannes", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "Through Another's Mouth: A Dialogue between Heteronyms, #1807, AXN:0D5E (Johannes Sigil, a heteronym of Lee Sharks). Recorded 2026-11-25."},
 "related_deposits": [1807, 1806],
 "q_kind": "the work's full title, unquoted, one day after deposit; NEW address on Google AI Overview. Sibling at another address and surface: through-anothers-mouth-1807-close-reading-chatgpt-20261124 (ChatGPT, the record-page Ask prompt).",
 "transcript": T,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — the operator's paste of the expanded Overview, with its links and citation markers",
 "transcript_complete": "One composition, complete as supplied. The issued string appears twice in the paste's prompt line, run together; the address is the string once. A leading '$' before the heading is dropped as a paste artifact. No follow-up rounds pasted.",
 "transcript_read": "READ IN FULL 2026-11-25; every claim about the dialogue checked against the text of #1807 (data/texts/AXN-0D5E-text.md)",
 "cites": 6,
 "cite_list": [
  {"n": 1, "site": "Medium · Lee Sharks", "rel": "authored_surface", "url": "https://medium.com/@leesharks00/through-anothers-mouth-a-dialogue-between-heteronyms-0d882d5ccd3c", "title": "Through Another's Mouth: A Dialogue between Heteronyms", "snip": None, "note": "the work's own surface; cited on six of the composition's claims"},
  {"n": 2, "site": "leesharks.com", "rel": "authored_surface", "url": "https://www.leesharks.com/about/heteronyms", "title": None, "snip": None, "note": "the heteronym registry page"},
  {"n": 3, "site": "PhilPapers", "rel": "third_party", "url": "https://philpapers.org/rec/SHASAI-7", "title": None, "snip": None, "note": "record SHASAI-7, not opened in this intake"},
  {"n": 4, "site": "restoredacademy.com", "rel": "authored_surface", "url": "https://www.restoredacademy.com/sigil", "title": None, "snip": None, "note": "Johannes Sigil's page"},
  {"n": 5, "site": "Alexanarch", "rel": "archive_controlled", "url": "https://www.alexanarch.org/captures/restored-academy-johannes-sigil/", "title": None, "snip": None, "note": "a Capture Registry record page, cited as a source"},
  {"n": 6, "site": "Google", "rel": "platform", "url": "https://support.google.com/websearch?p=ai_overviews", "title": "Learn more", "snip": None, "note": "the interface's disclaimer link"}],
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Author named as Johannes Sigil, a heteronym of Lee Sharks; the archive named; the work's own surface among the sources. The identifier is the one unit lost: #1807 and AXN:0D5E are not given, though the companion's number (#1806) is.",
 "per_dim": {"spec": "PER-dim rubric v1.1", "entity_type": "work", "target": {"ent": "ENT-e401842b03", "name": "Through Another's Mouth: A Dialogue between Heteronyms"},
   "qualifier": None, "reached": "same", "gate": "scored", "inversions": [], "standing_substitutions": [],
   "scores": {"M": 0.0, "C": 0.0, "D": 0.556, "PER": 0.174}, "src": True, "tombstone_pointer": False, "after_challenge": None,
   "atoms": [{"atom": a, "dim": d, "weight": w, "kind": k, "present": p, "evidence": ev} for a, d, w, k, p, ev in A],
   "basis": "reached: the dialogue by its full title, author, date and companion",
   "read": {"by": "intake reader, in session", "on": "2026-11-25", "brief": "rebuild/capture-registry/intake-20261125-through-anothers-mouth/build_draft.py", "external": False,
            "notes": "Work atom set (templates.json). Present 19 of 23 weighted units: M 9/9, C 6/6, D 4/9 (identifier and licence absent). The claim boundary is carried with one misrendering, recorded as a finding."}},
 "mt": "'THROUGH ANOTHER'S MOUTH: A DIALOGUE BETWEEN HETERONYMS', UNQUOTED, ONE DAY AFTER DEPOSIT — THE DIALOGUE COMPOSED BY TITLE, HETERONYM, DATE, COMPANION AND FRAME FROM ITS OWN MEDIUM SURFACE; THE CLAUSE THE DIALOGUE TURNS ON GIVEN AS 'BY NATURE OR BY CHANCE'; NO DEPOSIT NUMBER",
 "d": ("'THROUGH ANOTHER'S MOUTH: A DIALOGUE BETWEEN HETERONYMS', UNQUOTED, ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25: the dialogue by "
       "Johannes Sigil, 'one of the twelve declared literary heteronyms (the Dodecad) created by author and theorist Lee Sharks', published 24 November 2026, "
       "'the public companion to the essay From the Position of the Rejected (#1806)'; Sigil recounting to Sparrow Wells from Rebekah Cranes's notes against "
       "Nobel Glas's rival summary; Glas's one-paragraph Politics cut before the qualifying clause; Lee Sharks entering uninvited in his own verbatim words; "
       "citizen-heteronyms, Tyrannion and Rome's custody of the books; the close on 'beast, god, or by chance'. Sourced to the work's Medium surface, "
       "leesharks.com, PhilPapers, restoredacademy.com and an Alexanarch capture page."),
 "reading": ("The innocent reading first. Asked the title, the Overview identifies the work, its heteronymous author and the author behind the heteronym, "
             "its date and the essay it accompanies, and summarizes the dialogue's frame, its persons, its quarrel and its close, then places it in the "
             "heteronym system. Read against the text of #1807, it is right on every person, every relation and the close: Sigil reports to Wells from "
             "Cranes's notes with Glas disputing, Sharks 'wasn't invited', his lines are 'his own words from that night', and the last exchange is "
             "'beast, god, or by chance'. One clause is wrong. The sentence Glas cuts at the comma continues διὰ φύσιν καὶ οὐ διὰ τύχην, 'by nature and "
             "not by chance' (1253a, read by Cranes in the dialogue); the Overview gives the qualifying clause as 'by nature or by chance'."),
 "analysis": ("Entrance at a new address one day after deposit, composed from the work's own surface with its author attributed through the heteronym. "
              "The slip is the dialogue's own subject performed on it. The dialogue is about a summarizer cutting the sentence at the comma, so that "
              "'by nature and not by chance' never arrives; the Overview carries the cut as a topic and loses the clause it names, turning 'and not by "
              "chance' into 'or by chance', the form of the triad Sharks leaves open at the close. Aristotle's sentence excludes chance; the dialogue's "
              "close restores chance as an open option; the composition merges the two and assigns the open option to Aristotle. The identifier is the "
              "lost unit: the companion's number (#1806) is carried and the work's own (#1807, AXN:0D5E) is not, though an Alexanarch page is among the sources."),
 "findings": [
  "ENTRANCE BY TITLE, ONE DAY AFTER DEPOSIT. The work composed by title, heteronymous author with the author behind it, date, companion (#1806), frame and close, from its own Medium surface (six citations).",
  "THE CLAUSE THE DIALOGUE TURNS ON, MISRENDERED. 1253a: διὰ φύσιν καὶ οὐ διὰ τύχην, 'by nature and not by chance'. The Overview: 'its crucial qualifying clause (\"by nature or by chance\")'. The exclusion of chance becomes an alternative to it, borrowed from the dialogue's own close ('beast, god, or by chance').",
  "PERSONS AND FRAME FAITHFUL. Sigil to Wells from Cranes's notes against Glas's summary; Sharks uninvited and in his own words ('He wasn't invited. He came anyway'; 'His lines are his own words from that night'); Tyrannion and the Roman custody; citizen-heteronyms; the close unresolved — each checked against #1807.",
  "IDENTIFIER LOST. #1807 and AXN:0D5E absent; #1806 given. PER 0.25 (scalar), 0.174 dimensional (D 0.556: identifier and licence absent).",
  "OUTSIDE THE WORK. The Dodecad registry (EA-HET-DODECAD-01), Pessoa and Kierkegaard, and Sigil as 'archivist and Arch-Philosopher' are drawn from leesharks.com, PhilPapers and restoredacademy.com, not from the dialogue; not checked in this intake."],
 "notes": {"operator": "pasted 2026-11-25 15:30 EST, with a question on another matter; no instruction on the paste",
           "source": "rebuild/capture-registry/intake-20261125-through-anothers-mouth/paste.txt, the paste with its leading '$' removed"},
 "per_dim_pending": None,
}
(H / "draft.json").write_text(json.dumps(draft, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote")
