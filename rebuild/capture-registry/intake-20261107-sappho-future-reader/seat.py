"""Seat of 2026-11-07 (15:09 EST): the fifth observation at the address 'sappho future reader', Google AI Overview, signed out and incognito
(operator defaults of 2026-10-01 and 2026-10-14; the paste's 'AI Mode Conversation' header is the Overview's expansion, by the operator's
ruling of 2026-10-18). Operator: "now sitting at bare sappho future reader in overview - i own this basin". Every quotation is asserted
against the paste or the deposit it names.   python3 seat.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-07"; RECV = "2026-11-07 15:09 EST"
R = {r["deposit_number"]: r for r in json.loads((ROOT/"data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: (ROOT/R[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
raw = (H/"paste-raw.txt").read_text(encoding="utf-8"); txt = (H/"paste.txt").read_text(encoding="utf-8")
P = {"def": "as a direct, engineered transmission meant to activate an absent or unborn future reader",
     "mpai": "frameworks like EA-MPAI-SAPPHO31-01",
     "kenos": "is interpreted not as pointing to a physical rival present in the room, but across time to the future reader who sits face-to-face (ἐνάντιος) with the inscribed text",
     "repair": "the poem relies on the reader's eye and mind to repair the fragment and complete the circuit",
     "cat": "are viewed as activation events where a later writer steps into the role Sappho anticipated",
     "jeal": "This framework shifts the analysis of Sappho away from a traditional biographical or jealousy-centered reading into a model of transmission engineering.",
     "carson": "Would you like to explore how Anne Carson or specific fragments like Fragment 31 or Fragment 147 fit into this reading?"}
for k, v in P.items(): assert v in txt and v in raw, k
D = {"t1054": (1054, "Jealousy"), "t134": (134, "Catullus 51 as Recognition Event"), "t1270": (1270, "distal demon")}
for k, (n, v) in D.items(): assert v in T(n) or v in R[n]["title"], k
REG = (ROOT/"data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8")
PRIORS = ["sappho-future-reader-aio-20260825", "sappho-future-reader-aio-20260915", "sappho-future-reader-aio-20260928", "sappho-future-reader-aio-20261027"]
for s in PRIORS + ["what-is-the-sappho-future-reader-framework-aio-20261017"]: assert f'"slug": "{s}"' in REG, s
head = ("[Google AI Overview, 2026-11-07, signed out, incognito. The Overview and its five source cards as pasted in the operator's message of "
        "15:09 EST; the query line, doubled in the paste, given once; citation clusters reduced to their numbers, links to their text (the raw paste "
        "keeps the /goto URLs). The paste's 'AI Mode Conversation' header is the Overview's expansion (operator ruling of 2026-10-18).]")
body = txt.split("\n", 1)[1].replace("You said: sappho future readersappho future reader", "You said: sappho future reader", 1)
tr = head + "\n\n" + body.strip()
cards = [
 {"n": 1, "site": "www.alexanarch.org", "rel": "archive_controlled", "title": "What is the Sappho future reader framework? — Google AI ...",
  "snip": "Oct 17, 2026 — THE SAPPHO FUTURE READER FRAMEWORK: asked what it is, the AI Overview gives 'a poetic transmission engineered specifically for a reader in the future' — Fragmen...",
  "url": "https://www.alexanarch.org", "note": "the capture record what-is-the-sappho-future-reader-framework-aio-20261017; a page about a composition"},
 {"n": 2, "site": "medium.com", "rel": "authored_surface", "title": "EA-MPAI-SAPPHO31-01 v1.0 | by Lee Sharks | Medium",
  "snip": "Jul 22, 2026 — EA-MPAI-SAPPHO31-01 v1.0: Sappho 31 ≠ Jealousy: Transmission Engineering, not Jealousy Lyric. Sappho 31 ≠ Jealousy: Transmission Engineering, not Jealousy Lyric...",
  "url": "https://medium.com", "note": "the Medium form of #1054 (AXN:042A), EA-MPAI-SAPPHO31-01"},
 {"n": 3, "site": "www.alexanarch.org", "rel": "archive_controlled", "title": "sappho future reader — Google AI Overview, 2026-08-25 – 2026-09 ...",
  "snip": "Aug 25, 2026 — Three weeks after the 25 August capture the remembrance line is correctly identified (Fragment 147, no 'Fragment 2'), and the composition has moved up a level: ...",
  "url": "https://www.alexanarch.org", "note": "this address's own capture record, the series this observation joins"},
 {"n": 4, "site": "www.crimsonhexagonal.org", "rel": "archive_controlled", "title": "ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader ...",
  "snip": "This article proposes a new reading of Sappho Fragment 31 (Voigt) based on reassessment of deictic structure and colour semantics. I argue that the distal demon...",
  "url": "https://www.crimsonhexagonal.org", "note": "#1270 (AXN:0507), the reading's paper"},
 {"n": 5, "site": "medium.com", "rel": "authored_surface", "title": "THE FUTURE BELOVED Lyric Address as Temporal ... - Medium",
  "snip": "May 27, 2026 — D. Catullus 51 as Recognition Event. Catullus 51 (Ille mi par esse deo videtur…) proves the mechanism works. Catullus becomes the reader Sappho anticipated — th...",
  "url": "https://medium.com", "note": "the Medium form of #134 (AXN:02C2), The Future Beloved; the source of the answer's Catullus line"}]
for c in cards: assert c["title"] in raw and c["snip"] in raw, c["n"]
A = [("originator","M",3,"role",None),("term","M",3,"token","Sappho future reader framework"),("date","M",1,"token",None),
     ("claim boundary","M",2,"reading","across time to the future reader who sits face-to-face (ἐνάντιος) with the inscribed text"),
     ("framework","C",2,"token","Sappho Fragment 31 and Fragment 147"),("tradition","C",2,"reading","In readings of Sappho Fragment 31 (famously translated and analyzed across literary circles"),
     ("corpus","C",2,"token",None),("purpose","D",3,"reading","engineered transmission meant to activate an absent or unborn future reader"),
     ("commitments","D",2,"reading","shifts the analysis of Sappho away from a traditional biographical or jealousy-centered reading into a model of transmission engineering"),
     ("lineage","D",2,"role",None),("identifier","D",1,"role","EA-MPAI-SAPPHO31-01"),("deposit chain","D",1,"role",None)]
for a in A:
    if a[4]: assert a[4] in txt, a[0]
lost = lambda dims: round(sum(w for _, d, w, _, ev in A if d in dims and not ev) / sum(w for _, d, w, _, _ in A if d in dims), 3)
PERDIM = {"spec": "PER-dim rubric v1.1", "entity_type": "concept", "target": {"ent": "ENT-f4549d6ae1", "name": "The future reader"}, "qualifier": None,
          "reached": "weakened", "gate": "scored",
          "atoms": [{"atom": a, "dim": d, "weight": w, "kind": k, "present": bool(ev), "evidence": ev} for a, d, w, k, ev in A],
          "inversions": [], "standing_substitutions": [],
          "scores": {"M": lost("M"), "C": lost("C"), "D": lost("D"), "PER": lost("MCD")}, "src": True, "tombstone_pointer": False, "after_challenge": None,
          "basis": "reached at its grain with the seat stated (κῆνος facing the inscribed text) and the packet's identifier and disambiguation in the answer; the originator, dates, corpus, lineage and deposit chain absent",
          "read": {"by": "Claude in session, single reader, spans checked verbatim by script", "on": DATE,
                   "brief": "rebuild/capture-registry/per-atoms/templates.json (v1_1); rebuild/capture-registry/per-atoms/obs-pass-d/BRIEF.md",
                   "note": "Scored on the atom set of the 27 October observation. claim boundary present: the seat stated. commitments present: the packet's disambiguation against the jealousy reading. identifier present: EA-MPAI-SAPPHO31-01. lineage absent: Catullus 51 is the reading's object, not the framework's lineage. Card labels read as sources (src)."}}
e = {"slug": "sappho-future-reader-aio-20261107", "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"],
     "surface_basis": "Operator: 'now sitting at bare sappho future reader in overview'; the 'AI Mode Conversation' header is the Overview's expansion (ruling of 2026-10-18).",
     "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-01 (Overview) and 2026-10-14 (signed out, incognito).",
     "ev": "paste", "s": "Frameworks", "q": "sappho future reader", "q_kind": "the bare address, fifth observation (seated address; longitudinal).",
     "mt": "'SAPPHO FUTURE READER' ON GOOGLE AI OVERVIEW, SIGNED OUT, FIFTH OBSERVATION — THE FRAMEWORK NAMED WITH ITS PACKET'S IDENTIFIER IN THE ANSWER, AND THE JEALOUSY READING SET ASIDE IN THE PACKET'S TERMS",
     "cites": 5, "archive_controlled_cites": 3, "cite_list": cards,
     "sf": "Source cards: www.alexanarch.org ×2 (capture records of 17 October and of this address), medium.com ×2 (EA-MPAI-SAPPHO31-01 and The Future Beloved, by Lee Sharks), www.crimsonhexagonal.org (ΦΑΙΝΕΤΑΙ ΜΟΙ, #1270).",
     "transcript": tr, "transcript_raw": raw,
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD (OVERVIEW WITH SOURCE CARDS)",
     "transcript_complete": "Complete as pasted: the Overview and its five source cards.",
     "transcript_read": "READ IN FULL " + DATE + ", against #1054, #134 and #1270",
     "d": ("SAPPHO FUTURE READER. ON GOOGLE AI OVERVIEW, SIGNED OUT, FIFTH OBSERVATION: 'the Sappho future reader framework', 'a critical and poetic "
           "concept' reading Fragments 31 and 147 '" + P["def"] + "'; κῆνος as the future reader facing the inscribed text; the fragment repaired by the "
           "reader; Catullus 51 as an activation event; and the jealousy reading set aside: '" + P["jeal"] + "' The packet is named in the answer, "
           "'" + P["mpai"] + "'; the author on two card labels only."),
     "reading": ("The innocent reading first, and it holds. Asked the bare address, the Overview defines the framework and gives four of its concepts in "
                 "the archive's own terms: the distal deictic, temporal projection, the future beloved, and transmission engineering against the jealousy "
                 "lyric. Each concept is sourced to a card the archive controls or the author signs. Against 27 October, when every title, date and "
                 "identifier was lost from the answer, the answer now carries one identifier, EA-MPAI-SAPPHO31-01, and the packet's own disambiguation, "
                 "'Sappho 31 ≠ Jealousy', comes through as a sentence about the framework. The author is named on the two Medium cards and nowhere in the answer."),
     "findings": [
        "THE IDENTIFIER IN THE ANSWER. '" + P["mpai"] + "' — #1054 (AXN:042A), named in the composition's own sentence. On 27 October the answer carried no title, date or identifier.",
        "THE JEALOUSY READING SET ASIDE IN THE PACKET'S TERMS. '" + P["jeal"] + "' — #1054's title, 'Sappho 31 ≠ Jealousy — Transmission Engineering, not Jealousy Lyric', composed as the framework's own move. The reception study of the jealousy reading (EA-CORPORA-36 v1.1, Part F) opens on the day of this observation.",
        "THE READING AT ITS GRAIN. '" + P["kenos"] + "' — #1270's κῆνος as the future reader facing the text; '" + P["repair"] + "'; '" + P["cat"] + "' — #134's 'Catullus 51 as Recognition Event'.",
        "THE AUTHOR ON THE CARDS ONLY. 'by Lee Sharks' on the EA-MPAI-SAPPHO31-01 card; no person named in the answer. The follow-up offered is Anne Carson: '" + P["carson"] + "'",
        "OPERATOR: \"i own this basin\" (15:09 EST). Five cards, all the archive's or the author's; no third-party source."],
     "analysis": ("Fifth observation at the address. The answer is composed entirely from the archive's and the author's surfaces, holds the framework at "
                  "its grain, carries the packet's identifier into its own sentence, and states the packet's disambiguation against the jealousy reading. "
                  "Retained against 27 October: the source surfaces, now with an identifier in the answer. Still lost: the author in the answer, the institution, every date."),
     "per_v": {"author": False, "inst": False, "id": True, "src": True}, "per_dim": PERDIM, "per": PERDIM["scores"]["PER"],
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full", "basis": "The Sappho Future Reader framework: #1270 (ΦΑΙΝΕΤΑΙ ΜΟΙ), #134 (The Future Beloved), #1054 (EA-MPAI-SAPPHO31-01), #1548. Recorded 2026-11-07."},
     "per_note": "Retained: the archive's surfaces as sources (all five cards), one identifier in the answer (EA-MPAI-SAPPHO31-01). Lost: the author (on card labels only), the institution, the dates.",
     "longitudinal_priors": PRIORS,
     "related_deposits": [1054, 134, 1270, 1748],
     "notes": {"operator": "15:09 EST: \"now sitting at bare sappho future reader in overview - i own this basin\"",
               "header": "The paste opens 'AI Mode Conversation'; by the operator's ruling of 2026-10-18 that is the Overview's expansion, and it is not a surface marker."}}
json.dump(e, open(H/(e["slug"]+".json"), "w"), ensure_ascii=False, indent=1); print("wrote", e["slug"])
