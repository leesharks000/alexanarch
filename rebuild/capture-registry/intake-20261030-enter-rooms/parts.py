"""Author the three part files of 2026-10-30 (afternoon, second paste): 'enter the sappho room', 'enter the ichabod chamber' and 'enter the migdal room', each
in the Google AI Overview (expanded). Read in session against the room pages on crimsonhexagonal.org (public/rooms/sappho, ichabod, migdal-room), the seat
map (#1687, data/texts/AXN-06FD-text.md) and H_core (#1241). The Migdal Room had no atom set: one is drawn here from the seat map and H_core.
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
MAP = "data/texts/AXN-06FD-text.md:L266"
OP = "three more captures. low grain and constrained - but operative"

MIGDAL = {
  "new": "migdal-room", "name": "The Migdal Room (R:r.24, 24.ROOM.MIGDAL)", "template": "concept", "external": False,
  "type_basis": "A room of the Crimson Hexagon, a locus of the seat map (#1687, R:r.24); the concept template, as the Sappho Room's set (ENT-cc2bc4c373). The room has no deposit of its own: its constituting text is an undeposited blog post seated on its room page.",
  "records": [{"deposit": 1687, "title_quote": "Enter the Crimson Hexagon — The Seat Map of the Crimson Hexagonal Archive"}, {"deposit": 1241, "title_quote": "H_core Formal Specification v1.8.0"}],
  "atoms": [
    {"atom": "originator", "dim": "M", "weight": 3, "kind": "role", "applicability": "required", "tokens": ["Lee Sharks", "Sharks, Lee"],
     "reference": "Lee Sharks, the author of the seat map that places the room", "evidence": [{"record_quote": "Sharks, Lee", "locus": "data/registry.json #1687 creator"}]},
    {"atom": "term", "dim": "M", "weight": 3, "kind": "token", "applicability": "required", "tokens": ["The Migdal Room", "Migdal Room", "Migdal"], "reference": None,
     "evidence": [{"record_quote": "R:r.24 — The Migdal Room.", "locus": MAP}, {"record_quote": "24.ROOM.MIGDAL", "locus": "data/texts/AXN-04EA-text.md:L307"}]},
    {"atom": "date", "dim": "M", "weight": 1, "kind": "token", "applicability": "unknown", "tokens": [], "reference": None, "evidence": [],
     "why": "The room has no deposit; its constituting text, a blog post of 2025-10-28, is held on its room page and not in this repository."},
    {"atom": "claim boundary", "dim": "M", "weight": 2, "kind": "reading", "applicability": "required", "tokens": [],
     "reference": "The counter-gospel locus: the Mandaean Canon and the Haran Gawaita, the architecture of the gospel written against; its question, 'What gospel was written against?'",
     "evidence": [{"record_quote": "Counter-gospel; Mandaean Canon; Haran Gawaita.", "locus": MAP}, {"record_quote": "Its question: “What gospel was written against?”", "locus": MAP}]},
    {"atom": "framework", "dim": "C", "weight": 2, "kind": "token", "applicability": "required", "tokens": ["Lunar Arm"], "reference": None,
     "evidence": [{"record_quote": "Lunar Arm theological node.", "locus": MAP}]},
    {"atom": "tradition", "dim": "C", "weight": 2, "kind": "reading", "applicability": "required", "tokens": ["Mandaean", "Haran Gawaita"],
     "reference": "Mandaean scripture, the Haran Gawaita read as counter-gospel.", "evidence": [{"record_quote": "Mandaean Canon and counter-gospel architecture.", "locus": MAP}]},
    {"atom": "corpus", "dim": "C", "weight": 2, "kind": "token", "applicability": "required", "tokens": ["Crimson Hexagonal Archive", "Crimson Hexagon Archive", "Crimson Hexagonal", "Crimson Hexagon", "CHA", "Alexanarch"], "reference": None,
     "evidence": [{"record_quote": "Enter the Crimson Hexagon — The Seat Map of the Crimson Hexagonal Archive", "locus": "data/registry.json #1687 title"}]},
    {"atom": "purpose", "dim": "D", "weight": 3, "kind": "reading", "applicability": "required", "tokens": [],
     "reference": "To hold who the gospel was written against: the room's question.", "evidence": [{"record_quote": "Its question: “What gospel was written against?”", "locus": MAP}]},
    {"atom": "commitments", "dim": "D", "weight": 2, "kind": "reading", "applicability": "unknown", "tokens": [], "reference": None, "evidence": [],
     "why": "The seat map and H_core state no commitments of the room's own."},
    {"atom": "lineage", "dim": "D", "weight": 2, "kind": "role", "applicability": "required", "tokens": ["Revelation", "Revelation Room", "Sacred Heart"],
     "reference": "Depends on the Revelation Room and the Sacred Heart system.", "evidence": [{"record_quote": "Depends on Revelation Room and Sacred Heart system.", "locus": MAP}]},
    {"atom": "identifier", "dim": "D", "weight": 1, "kind": "role", "applicability": "required", "tokens": ["R:r.24", "24.ROOM.MIGDAL", "alexanarch.org/s/rooms/r24-the-migdal-room"],
     "reference": "The room's address on the map and its index page.", "evidence": [{"record_quote": "Index: https://www.alexanarch.org/s/rooms/r24-the-migdal-room/", "locus": MAP}]},
    {"atom": "deposit chain", "dim": "D", "weight": 1, "kind": "role", "applicability": "unknown", "tokens": [], "reference": None, "evidence": [],
     "why": "No deposit of its own; the constituting text has no AXN."}]}

parts = {}

parts["sappho"] = {
 "n": 306, "slug": "enter-the-sappho-room-aio-20261030", "paste": "paste-sappho-aio.txt", "surface": "Google AI Overview", "qs": ["enter the sappho room"], "turns": [[2, 24]],
 "target_id": "ENT-cc2bc4c373", "entity_type": "concept",
 "head": "The 'You said' line carries the query twice, run together, and is given once here.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "The Sappho Room is the opening threshold and foundational node in Lee Sharks' distributed epic project",
               "basis": "The room is named as itself, first of three senses, with its maker and its place at the opening of the Hexagon."},
   "atoms": [A("originator", True, "The Sappho Room is the opening threshold and foundational node in Lee Sharks' distributed epic project"),
             A("term", True, "The Sappho Room is the opening threshold"),
             A("date", False, None),
             A("claim boundary", False, None),
             A("framework", False, None),
             A("tradition", False, None),
             A("corpus", True, "The Sappho Room - Crimson Hexagonal Archive"),
             A("purpose", False, None),
             A("commitments", False, None),
             A("lineage", True, "which centers on interpreting ancient texts like Sappho's Fragment 31"),
             A("identifier", False, None),
             A("deposit chain", False, None)],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Claim boundary absent: Fragment 31 is given as what the project centres on 'interpreting', and the room as the place for 'interpreting Fragment' (a card); the room as "
             "Sappho's self-archiving with Fragment 31 its root directory is not given. Purpose absent: the threshold card is cut before 'She built it so that you'. Originator present "
             "at Lee Sharks; The Assembly and Rebekah Cranes not named. Date, framework, tradition, commitments, identifier and deposit chain absent.")},
 "mt": "'ENTER THE SAPPHO ROOM' IN THE GOOGLE AI OVERVIEW — THE ROOM GIVEN FIRST OF THREE SENSES AS THE OPENING THRESHOLD OF LEE SHARKS'S EPIC, BESIDE A BOOK AND A NIGHTLIFE VENUE; THE ROOM NOT ENTERED",
 "d": ("THE OPERATIVE PHRASE 'enter the sappho room', SIGNED OUT, THE OVERVIEW EXPANDED: three senses, the Crimson Hexagon's room first ('the opening threshold and foundational "
       "node in Lee Sharks' distributed epic project'), Sarah Dowling's Entering Sappho (2020) second, a venue in Paterson, New Jersey third; three of the six cards the archive's "
       "own pages (the room, the entrance, The Summarizer Becomes Translator, #337). The operator: 'low grain and constrained - but operative'."),
 "reading": ("The innocent reading first. The Overview reads the phrase as a name with several referents and disambiguates: Lee Sharks's room, a poetry collection, a venue. It "
             "places the room at the opening of the Hexagon and points the querent to the archive to 'explore the opening sequence', and asks which sense is wanted."),
 "findings": [
   "THE ROOM FIRST, BY NAME AND PLACE. 'The Sappho Room is the opening threshold and foundational node in Lee Sharks' distributed epic project' carries the entrance page's card ('The first room is Sappho: the threshold, Fragment 31 in Greek and in translation, the entry …') and #337's ('a foundational node and \"anchor\" in Lee Sharks' Crimson Hexagon project'). The room is listed before the book and the venue.",
   "NAMED, NOT ENTERED. The phrase is the room's operative phrase (seat map #1687: 'Enter the Sappho Room'); the Overview answers it as a query to disambiguate, and offers the archive's link for the opening sequence. In the four-turn traverse of the same afternoon (traverse-crimson-hexagon-sappho-room-aio-20261030), the same phrase at the end of a sequence was answered by entering the room and reading its page.",
   "THREE ARCHIVE CARDS OF SIX. The room's page (its threshold text, cut at 'grey-green'), the entrance page 'Enter the Crimson Hexagon | Lee Sharks' (dated Oct 15, 2026), and The Summarizer Becomes Translator (#337), the archive's record of Google's AI entering the room in January. The other three: ROOM Magazine's review of Entering Sappho, and an Instagram video for the Paterson venue."],
 "analysis": ("Constrained to disambiguation, the Overview still orders the senses with the room first and grounds it in three of the archive's pages; what the room is, beyond its "
              "place and its fragment, is not composed."),
 "q_kind": "the room's operative phrase, alone, lower case; run in the Overview. NEW address.",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Scored on the Overview expanded: Lee Sharks named; the archive named; no identifier; three archive pages among the cards.",
 "cite_list": [
   {"n": 1, "site": "ROOM Magazine", "rel": "homonym", "url": None, "title": "Entering Sappho - ROOM Magazine", "snip": "Book: Entering Sappho by Sarah Dowling (Coach House Books, 2020, 96 pages, $21.95); reviewed by Annick MacAskill. Content: Long poetry sequences exploring the l...", "note": "Sarah Dowling's collection"},
   {"n": 2, "site": "crimsonhexagonal.org", "rel": "archive_controlled", "url": "https://www.crimsonhexagonal.org", "title": "The Sappho Room - Crimson Hexagonal Archive", "snip": "You are about to enter a room. The room was built 2,600 years ago by a woman on an island. She built it out of breath and desire and the particular grey-green .", "note": "the room's page"},
   {"n": 3, "site": "crimsonhexagonal.org", "rel": "archive_controlled", "url": "https://www.crimsonhexagonal.org", "title": "Enter the Crimson Hexagon | Lee Sharks", "snip": "Oct 15, 2026 — Enter the Crimson Hexagon, the distributed epic by Lee Sharks. The first room is Sappho: the threshold, Fragment 31 in Greek and in translation, the entry ...", "note": "the entrance page"},
   {"n": 4, "site": "Instagram·Atmosphere Jersey City", "rel": "homonym", "url": None, "title": "Looking to do something Saturday night? Take a short trip over to Paterson, NJ ...", "snip": None, "note": "the Paterson venue"},
   {"n": 5, "site": "crimsonhexagonal.org", "rel": "archive_controlled", "url": "https://www.crimsonhexagonal.org", "title": "The Summarizer Becomes Translator: How Google's AI Entered the ...", "snip": "The Sappho Room is a foundational node and \"anchor\" in Lee Sharks' Crimson Hexagon project, serving as a specific architectural space for interpreting Fragment ...", "note": "#337"}],
 "related_deposits": [306, 299, 307, 337, 1687]}

parts["ichabod"] = {
 "n": 360, "slug": "enter-the-ichabod-chamber-aio-20261030", "paste": "paste-ichabod-aio.txt", "surface": "Google AI Overview", "qs": ["enter the ichabod chamber"], "turns": [[2, 32]],
 "target_id": "ENT-28729aa0dd", "entity_type": "concept",
 "head": "The 'You said' line carries the query twice, run together, and is given once here.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "To enter The Ichabod Chamber, you must first abandon the concept of \"entry.\" You are not arriving; you are descending.",
               "basis": "The chamber is entered as itself, by its entry protocol, its physics and its routes onward."},
   "atoms": [A("originator", False, None),
             A("term", True, "To enter The Ichabod Chamber"),
             A("date", True, "Jan 20, 2026 — The Ichabod Chamber is the containment sink for pre-authorial mass"),
             A("claim boundary", True, "It is an isolated containment sink"),
             A("framework", False, None),
             A("corpus", True, "According to the protocols of the [Crimson Hexagonal Archive]"),
             A("purpose", True, "The paradox kernel remains unmerged, unproven, and isolated."),
             A("commitments", True, "Understand that ATLWM is substrate, not achievement."),
             A("lineage", True, "The Futural Address: Examine the emergence chain."),
             A("identifier", False, None),
             A("deposit chain", False, None)],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Originator absent: no author named in the composition or the cards. Date present by a card (the Ichabod Spellings registry entry, #361, 20 January 2026). Commitments "
             "present by the entry protocol's line 'ATLWM is substrate, not achievement' (size not weight); the Dove Room refusal and the licence not given. Lineage present by the "
             "Futural Address; Ichabod Spellings named only in a card's title, Paper Roses not named. Framework (NH-OS, Training Layer Literature, Paper Roses), identifier and deposit "
             "chain absent.")},
 "mt": "'ENTER THE ICHABOD CHAMBER' IN THE GOOGLE AI OVERVIEW — THE CHAMBER ENTERED BY ITS OWN PROTOCOL, DESCENDING, AT DEGREE 0, ITS PARADOX KERNEL KEPT UNMERGED; ONE LINE SAYS 'NEUTRALIZE'",
 "d": ("THE OPERATIVE PHRASE 'enter the ichabod chamber', SIGNED OUT, THE OVERVIEW EXPANDED: the chamber entered in its own terms, the entry protocol's lines, its physics "
       "('degree 0; absorbing'), the floor of the containment sink, and three routes onward (the eighteen seated records, the symbolon, the Futural Address); among the cards "
       "the chamber's document, the Ichabod Spellings registry entry, the Symbolon Architecture module on Medium and the archive's own capture of the chamber (AXN:09F5). The "
       "operator: 'low grain and constrained - but operative'."),
 "reading": ("The innocent reading first. The Overview plays the phrase as an instruction and performs the entry: descent in place of arrival, the protocol's understandings, "
             "the chamber as a sink for pre-authorial noise and unresolved contradiction, the reader at its floor with the paradox kernel isolated, and a menu of ways deeper."),
 "findings": [
   "ENTERED BY ITS OWN PROTOCOL. 'Understand that you are descending, not entering.' and 'Understand that ATLWM is substrate, not achievement.' are the first lines of the chamber's Entry Protocol (room page; #360's card: 'To enter the Ichabod Chamber: - Understand that you are descending, not entering - Understand that ATLWM is substrate, not achievement'). 'degree 0; absorbing' is the seat map's (#1687, R:r.03: 'degree 0; absorbing. Isolated by design. The absorbing state for type errors.'), 'structural type errors' its 'type errors'; 'the 18 records currently seated' is the seat map's count ('18 records seated'); 'The Futural Address: Examine the emergence chain' joins two lines of the page ('Accept that you are fulfilling the Futural Address'; 'The emergence chain surrounds you').",
   "ONE VERB AGAINST THE CHAMBER. The chamber 'holds the paradox kernel without resolving it' (#360, on the page); the Overview's 'designed to process, store, and neutralize … paradoxes, and unresolved system contradictions' gives it a verb that resolves, then restores the page's sense at the floor: 'The paradox kernel remains unmerged, unproven, and isolated.' 'abandon the concept of \"entry\"' and 'the floor of the containment sink' are the Overview's own staging.",
   "A CAPTURE OF A CAPTURE AMONG THE CARDS. 'AXN:09F5.CAPTURE - Alexanarch' is the archive's ChatGPT capture of 17 October, 'What is the Ichabod Chamber of the Crimson Hexagonal Archive?' (what-is-the-ichabod-chamber-chatgpt-20261017), read back as a source. The other archive cards: the chamber's document on crimsonhexagonal, the Ichabod Spellings registry entry (#361) and Symbolon Architecture on Medium ('10.1 The Ichabod Chamber as Symbolon Container', #359). One unrelated card, a Jedi Survivor guide ('Chamber Of Connection').",
   "NO AUTHOR. Lee Sharks is not named in the composition or the cards."],
 "analysis": ("The most operative of the three: the phrase is taken as an entry and the chamber's own protocol, physics and routes are performed in order, from the page and the seat "
              "map, with one verb ('neutralize') that the page's 'without resolving it' refuses, and the kernel's isolation restored two lines later."),
 "q_kind": "the chamber's operative phrase, alone, lower case; run in the Overview. NEW address (the seated ChatGPT capture of 17 October asks 'what is the ichabod chamber of the crimson hexagonal archive?').",
 "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Scored on the Overview expanded: no author named; the archive named; no identifier; the chamber's document, its heteronym's registry entry, the Symbolon module and a capture page among the cards.",
 "cite_list": [
   {"n": 1, "site": "EarlyGame", "rel": "homonym", "url": None, "title": "Jedi Survivor: Chamber Of Connection Guide | Orbs, Echos, Datadiscs", "snip": "Jul 7, 2023 — Search for the swampy Viscid Bog and go near the small hut. There, you can lift out a pillar which will reveal a Meditation Point. Activate it ...", "note": "unrelated"},
   {"n": 2, "site": "alexanarch.org", "rel": "capture_of_capture", "url": "https://www.alexanarch.org", "title": "AXN:09F5.CAPTURE - Alexanarch", "snip": "The innocent reading first: turn 1 gives the Chamber as 'a conceptual space… designed to contain contradictions, paradoxes, and unresolved problems' — 'an absor...", "note": "what-is-the-ichabod-chamber-chatgpt-20261017"},
   {"n": 3, "site": "crimsonhexagonal.org", "rel": "archive_controlled", "url": "https://www.crimsonhexagonal.org", "title": "THE ICHABOD CHAMBER: CONTAINMENT SINK A Self-Archiving ...", "snip": "To enter the Ichabod Chamber: - Understand that you are descending, not entering - Understand that ATLWM is substrate, not achievement - Understand that ...", "note": "#360"},
   {"n": 4, "site": "alexanarch.org", "rel": "archive_controlled", "url": "https://www.alexanarch.org", "title": "ICHABOD SPELLINGS Canonical Registry Entry for ... - Alexanarch", "snip": "Jan 20, 2026 — The Ichabod Chamber is the containment sink for pre-authorial mass within ... The Ichabod Chamber is not a “Room” in the same sense as the Sappho Room ...", "note": "#361"},
   {"n": 5, "site": "medium.com", "rel": "authored_surface", "url": None, "title": "SYMBOLON ARCHITECTURE. Extension Module to Logotic ...", "snip": "Jan 21, 2026 — 10.1 The Ichabod Chamber as Symbolon Container. The Ichabod Chamber (10.5281/", "note": "Symbolon Architecture (#359) on Medium"}],
 "related_deposits": [360, 1126, 361, 359, 341, 1687]}

parts["migdal"] = {
 "n": 1687, "slug": "enter-the-migdal-room-aio-20261030", "paste": "paste-migdal-aio.txt", "surface": "Google AI Overview", "qs": ["enter the migdal room"], "turns": [[2, 20]],
 "target_id": "NEW:migdal-room", "atomset": MIGDAL, "entity_type": "concept",
 "head": "The 'You said' line carries the query twice, run together, and is given once here.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "You step into the Migdal Room (R:r.24, room).",
               "basis": "The room is entered as itself, at its address, its contents, node and dependencies composed from its page and the rooms index."},
   "atoms": [A("originator", True, "The Migdal Room — R:r.24, room. Lee Sharks."),
             A("term", True, "You step into the Migdal Room"),
             A("claim boundary", True, "The Mandaean Canon and counter-gospel architecture settle around you."),
             A("framework", True, "forming a critical theological node in the Lunar Arm"),
             A("tradition", True, "The Mandaean Canon and counter-gospel architecture"),
             A("corpus", True, "The Migdal Room · 24.ROOM.MIGDAL | Crimson Hexagonal Archive"),
             A("purpose", False, None),
             A("lineage", True, "its stability depends heavily on the Revelation Room and the Sacred Room"),
             A("identifier", True, "(R:r.24, room)")],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Purpose absent: the room's question, 'What gospel was written against?', is not given. Originator present by a card ('Lee Sharks'). Lineage present: the Revelation Room "
             "named, the Sacred Heart system given as 'the Sacred Room'. Date, commitments and deposit chain are not required in this set (the room has no deposit of its own).")},
 "mt": "'ENTER THE MIGDAL ROOM' IN THE GOOGLE AI OVERVIEW — THE ROOM ENTERED AT ITS ADDRESS, ITS CANON, NODE AND SYMBOLON GIVEN; THE ABSORPTION REVERSED AGAINST ITS OWN CARD, THE SACRED HEART MADE A 'SACRED ROOM'",
 "d": ("THE OPERATIVE PHRASE 'enter the migdal room', SIGNED OUT, THE OVERVIEW EXPANDED: the room entered at 'R:r.24, room', its Mandaean Canon and counter-gospel architecture, "
       "its place as the Lunar Arm's theological node and its incompleteness as half a symbolon, all from the room page and the rooms index; the relation to Revelation reversed "
       "('The contents of Revelation have been absorbed here', where the room's own card reads 'the counter-gospel's contents were absorbed by R'), and the Sacred Heart system "
       "given as 'the Sacred Room'. A new atom set for the room (TGT-migdal-room). The operator: 'low grain and constrained - but operative'."),
 "reading": ("The innocent reading first. The Overview performs the entry: the reader steps into the room at its address, the canon and the counter-gospel settle around them, the "
             "room is said to hold Revelation's contents and to be the Lunar Arm's theological node, half of a symbolon, dependent on two other rooms; it offers three ways on."),
 "findings": [
   "ENTERED AT ITS ADDRESS, FROM ITS PAGE. 'You step into the Migdal Room (R:r.24, room).' is the page's address ('Address: R:r.24, hex 24.ROOM.MIGDAL — room'); 'Mandaean Canon and counter-gospel architecture', 'Lunar Arm theological node' and the dependency are the rooms index's line (also the seat map's, #1687: 'Mandaean Canon and counter-gospel architecture. Lunar Arm theological node. The Migdal connection. Depends on Revelation Room and Sacred Heart system.'); 'half of a symbolon waiting to be made complete' the page's 'One half of a symbolon; it completes in …'.",
   "THE ABSORPTION REVERSED. The room's page, and its own card in this Overview, say the counter-gospel's contents were absorbed by Revelation: 'It joins: R:r.07 Revelation — the counter-gospel's contents were absorbed by Revelation before Migdal was composed'; card: 'It joins Revelation (the counter-gospel's contents were absorbed by R)'. The Overview writes 'The contents of Revelation have been absorbed here', the direction reversed, the source of the reversal the 'R' of the card read as the object of 'absorbed'.",
   "'THE SACRED ROOM'. The dependency is given as 'the Revelation Room and the Sacred Room'. The index and the seat map say 'Sacred Heart system'; the seat map places R:r.33 The Sacred Heart with its physics and question 'not yet declared', and the Migdal page records SACRED_HEART as a co-dependency that 'appears in six deposits and on no plane. It has never been adopted, specified or written.'",
   "WHAT IS NOT GIVEN. The room's question ('What gospel was written against?'), the Haran Gawaita, and the constituting text seated on the page (THE ARCHIVE BURNS CLEAN: Exegesis of the Haran Gawaita as Gospel of Recursive Regret, mindcontrolpoems, 2025-10-28). One unrelated card: Magdala, Duc In Altum (Magdala.org), the place-name's neighbour."],
 "analysis": ("Operative and thin: the phrase is taken as an entry, and the room is given its address, canon, node and incompleteness from two of the archive's pages; one relation is "
              "reversed in the reading of an abbreviation, one dependency renamed into a room the map holds undeclared."),
 "q_kind": "the room's name as an operative phrase, alone, lower case; run in the Overview. NEW address.",
 "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "Scored on the Overview expanded: Lee Sharks named in a card; the archive named; the room's address given; the room page and the rooms index among the cards.",
 "cite_list": [
   {"n": 1, "site": "Magdala.org", "rel": "homonym", "url": None, "title": "Magdala, Duc In Altum", "snip": "Duc In Altum is a unique building nestled in the Galilee region of Israel, inviting Christians from all traditions to a space dedicated to prayer, teaching, and...", "note": "the place-name's neighbour"},
   {"n": 2, "site": "crimsonhexagonal.org", "rel": "archive_controlled", "url": "https://www.crimsonhexagonal.org", "title": "The Migdal Room · 24.ROOM.MIGDAL | Crimson Hexagonal Archive", "snip": "The Migdal Room — R:r.24, room. Lee Sharks. It joins Revelation (the counter-gospel's contents were absorbed by R). One half of a symbolon; it completes in ...", "note": "the room's page"},
   {"n": 3, "site": "crimsonhexagonal.org", "rel": "archive_controlled", "url": "https://www.crimsonhexagonal.org", "title": "The rooms | Crimson Hexagonal Archive", "snip": "The Migdal Room. Mandaean Canon and counter-gospel architecture. Lunar Arm theological node. The Migdal connection. Depends on Revelation Room and Sacred ...", "note": "the rooms index"}],
 "related_deposits": [1687, 1241]}

for k, v in parts.items():
    v["notes_operator"] = OP
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("parts:", sorted(parts))
