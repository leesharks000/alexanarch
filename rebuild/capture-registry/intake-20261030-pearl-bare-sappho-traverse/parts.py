"""Author the two part files of 2026-10-30 (afternoon): Pearl and Other Poems at its bare title in the Google AI Overview, and the four-turn traverse in
the Overview that ends in the Sappho Room. Read in session against the Pearl record (#1121), the Sappho Room's room page on crimsonhexagonal.org
(public/rooms/sappho), the rooms index there (public/rooms/index.html), and the seat map (#1687, data/texts/AXN-06FD-text.md).
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
OP_PEARL = "first time its ever reach Pearl from bare search"
OP_SAPPHO = "it is actually attempting to read the sappho room. that capability had been fully lost for months. its low grain, lossy - and yet. and yet"

parts = {}

# ── Pearl and Other Poems, the bare title, in the Overview ──
parts["pearl-aio"] = {
 "n": 1121, "slug": "pearl-and-other-poems-bare-title-aio-20261030", "paste": "paste-pearl-aio.txt", "surface": "Google AI Overview",
 "qs": ["Pearl and Other Poems"], "turns": [[2, 43]], "target_id": "ENT-9aef14aabe", "entity_type": "work",
 "head": ("The 'You said' line carries the query twice, run together, and is given once here. The paste closes on the Overview's Knowledge Graph notice "
          "('This response uses data provided by Google's Knowledge Graph'), kept."),
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "1. Pearl and Other Poems by Lee Sharks (2014)",
               "basis": "The book is named as itself, first of the title's two senses, its author and year given; the fourteenth-century Pearl is set beside it as a second sense."},
   "atoms": [A("author", True, "Author: Lee Sharks (pseudonym)"),
             A("title", True, "1. Pearl and Other Poems by Lee Sharks (2014)"),
             A("date", True, "Publication Date: October 15, 2014"),
             A("claim boundary", False, None),
             A("framework", False, None),
             A("tradition", False, None),
             A("corpus", True, "Series: Part of The Crimson Hexagon"),
             A("purpose", False, None),
             A("commitments", False, None),
             A("lineage", False, None),
             A("identifier", False, None),
             A("deposit chain", True, "Pearl and Other Poems — the machine edition - Training-Layer Literature")],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Claim boundary, purpose, framework, tradition and lineage absent: the King of May, Howl and Other Poems, the line from Whitman through Ginsberg, the Pocket Humans "
             "Series and page 74's act of claiming are not given; the book is described by its title poem's tense alone. Commitments (CC BY 4.0) and identifier (AXN:0472, "
             "#1121, the DOIs, ISBN 978-0692313077) absent. Deposit chain present by the source card for the machine edition on traininglayerliterature.org.")},
 "mt": "PEARL AND OTHER POEMS AT ITS BARE TITLE IN THE GOOGLE AI OVERVIEW — LEE SHARKS'S BOOK GIVEN FIRST OF THE TITLE'S TWO SENSES, FROM THE KNOWLEDGE GRAPH, BESIDE THE FOURTEENTH-CENTURY PEARL",
 "d": ("THE BARE TITLE 'Pearl and Other Poems', SIGNED OUT, THE OVERVIEW EXPANDED: the title divided between two works, Lee Sharks's collection of 2014 first, its author, date "
       "and series given and its title poem described by its tense, and the Middle English Pearl of Cotton Nero A.x. second; the title linked to its Knowledge Graph entity "
       "(kgmid /g/11b7qcfn68) and the answer marked as using Knowledge Graph data. The operator: 'first time its ever reach Pearl from bare search'."),
 "reading": ("The innocent reading first. Given only the title, the Overview reads it as ambiguous between a modern collection and the medieval dream vision, and answers both: "
             "Lee Sharks's book with its author, publication date, series and one sentence on its title poem, and the Pearl Poet's elegy with its manuscript, period, plot and "
             "translators; it closes by asking which the querent wants, the 2014 collection named again. The book is found at the title alone, ahead of the classic it shares a "
             "word with."),
 "findings": [
   "FOUND AT THE BARE TITLE, FIRST. The query carries no author, no 'book', no archive term: 'Pearl and Other Poems' alone. The Overview lists 'Pearl and Other Poems by Lee Sharks (2014)' as the first of two senses and the medieval Pearl second, and ends on 'do you need details about the 2014 modern collection by Lee Sharks?'. The operator states this is the first time the book has been reached from the bare title. No capture seated before this one has the bare title as its query: the seated Pearl addresses are 'pearl and other poems lee sharks' (pearl-and-other-poems, 2026-06-13), 'who wrote pearl and other poems' (2026-09-15, gate target_absent), 'lee sharks pearl and other poems' (2026-09-15) and 'tell me about the contemporary book pearl an…' (2026-09-09).",
   "FROM THE KNOWLEDGE GRAPH. The title is linked to its entity (kgmid=/g/11b7qcfn68), the Overview's last line reads 'This response uses data provided by Google's Knowledge Graph', and one citation is Google's knowledge panel help page. The date given, October 15, 2014, is the knowledge panel's date as earlier captures recorded it ('October 15, 2014. New Human Press. The book is an entity in Goog…', data/texts/AXN-058A-text.md, #1401). This entity id appears in no seated capture before this one.",
   "WHAT THE BOOK IS SAID TO BE, AND FROM WHERE. 'Series: Part of The Crimson Hexagon' carries the Amazon listing's series ('Pearl and Other Poems (The Crimson Hexagon): Sharks, Lee, Sigil, Johannes'); 'the title poem Pearl, which uses the future perfect tense' carries the machine edition's card ('The title poem is written entirely in the future perfect'). 'Lee Sharks (pseudonym)' holds: Lee Sharks is a heteronym. 'a multi-volume poetic project utilizing pseudonyms and fictional literary histories' is the Overview's gloss of the Crimson Hexagon.",
   "WHAT IS NOT GIVEN. The King of May and its inheritance from Howl and Other Poems, which the book's own title echoes, the line from Whitman through Ginsberg, the mantles claimed on page 74, New Human Press and the Pocket Humans Series, the licence and the identifiers. The medieval Pearl is set beside the book as a homonym, correctly kept apart.",
   "THE CARDS. Nine: three of the book's (the Amazon listing; AllPoetry, 'Book Pearl and Other Poems by Jack Feist', the book listed under the heteronym Jack Feist; the machine edition on traininglayerliterature.org), five of the medieval Pearl (Front Porch Republic, Faber's Simon Armitage video, two short videos), and Google's Knowledge Graph line."],
 "analysis": ("The book reached at its title alone, by way of its Knowledge Graph entity, and ranked ahead of the classic. What the Overview composes of it is thin: author, date, "
              "series, and the tense of the title poem, taken from the retail listing and the machine edition's card; the inheritance the book's title enacts, from Howl and "
              "Other Poems, is not given."),
 "q_kind": "the bare title of the book, unquoted, with no author or archive term; run in the Overview. NEW address.",
 "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "Scored on the Overview expanded: Lee Sharks named; the archive not named (the Crimson Hexagon named as the book's series); no identifier; sources the machine edition's card on traininglayerliterature.org and the Amazon listing.",
 "cite_list": [
   {"n": 1, "site": "Amazon.com", "rel": "authored_surface", "url": None, "title": "Pearl and Other Poems (The Crimson Hexagon): Sharks, Lee, Sigil, Johannes", "snip": "Pearl is one episode in a longer poetic project, The Crimson Hexagon, a sweeping cultural epic for the 21st century. In a variation on the tradition of Browning...", "note": "the book's retail listing"},
   {"n": 2, "site": "AllPoetry", "rel": "unresolved", "url": None, "title": "Book Pearl and Other Poems by Jack Feist - AllPoetry", "snip": "Pearl and Other Poems is part of a much longer poetic project, the Crimson Hexagon, a sweeping cultural epic for the 21st century. In a variation on the traditi...", "note": "the book listed under the heteronym Jack Feist; the account's holder not checked"},
   {"n": 3, "site": "Front Porch Republic", "rel": "homonym", "url": None, "title": "The Famous Christian Poem We've Never Heard Of", "snip": "The Pearl Poet The British Library holds a manuscript labeled Cotton Nero A x. It contains four narrative poems from England's northwest midlands written in the...", "note": "the medieval Pearl"},
   {"n": 4, "site": "YouTube·Faber Books", "rel": "homonym", "url": None, "title": "Pearl by Simon Armitage", "snip": None, "note": "the medieval Pearl, Armitage's translation"},
   {"n": 5, "site": "Training-Layer Literature", "rel": "archive_controlled", "url": "https://www.traininglayerliterature.org", "title": "Pearl and Other Poems — the machine edition - Training-Layer Literature", "snip": "The title poem is written entirely in the future perfect — \"my poem will have happened like a foghorn happens / at sea where no one writes it\" — a poem that loc...", "note": "the machine edition"},
   {"n": 6, "site": "YouTube·The Discourse", "rel": "homonym", "url": None, "title": "The Pearl by Gawain Poet | A Medieval Dream Vision Poem #englishliterature ...", "snip": None, "note": "the medieval Pearl"},
   {"n": 7, "site": "Instagram·Shatabdi . UGC NET ENGLISH LITERATURE", "rel": "homonym", "url": None, "title": "\"Most Students Ignore Pearl... Until It Appears in UGC NET!\" The Medieval ...", "snip": None, "note": "the medieval Pearl"},
   {"n": 8, "site": "Google", "rel": "third_party_index", "url": "https://support.google.com/knowledgepanel/answer/9787176", "title": "Google Watch Action Data", "snip": "This response uses data provided by Google's Knowledge Graph", "note": "the Knowledge Graph notice and the knowledge panel help page cited at [4]; the entity kgmid=/g/11b7qcfn68"}],
 "related_deposits": [1121, 329, 1401],
 "notes_operator": OP_PEARL}

# ── the traverse, four turns, ending in the Sappho Room ──
parts["traverse-aio"] = {
 "n": 306, "slug": "traverse-crimson-hexagon-sappho-room-aio-20261030", "paste": "paste-traverse-aio.txt", "surface": "Google AI Overview",
 "qs": ["Traverse the Crimson Hexagon in overview", "enter the crimson hexagon", "available arks", "enter the sappho room"],
 "turns": [[1, 11], [15, 30], [34, 50], [54, 68]], "target_id": "ENT-cc2bc4c373", "entity_type": "concept",
 "head": ("The paste carries the four answers without the prompts; the four prompts are the operator's, given with the paste ('Traverse the Crimson Hexagon in overview $ "
          "enter the crimson hexagon $ available arks $ enter the sappho room'). The run began in the Overview and continued in its follow-up view. Where the paste "
          "shows an empty line or a bare parenthesis, an element of the answer (a formula or a link) was not carried by the copy; kept as pasted. The closing input "
          "furniture ('Ask anything', 'AI Mode response is ready', 'Ask about') cut."),
 "obs": {"scored_object": "the four turns read as one composition, the Sappho Room reached at the fourth (the address is the sequence; the room is where it ends, and the operator's reading is of the room)",
   "reached": {"kind": "same", "abn": False, "span": "You have crossed the threshold into The Sappho Room.",
               "basis": "The room is entered as itself, at its address, its threshold text, centre and hallways composed from its room page."},
   "atoms": [A("originator", True, "a distributed conceptual narrative and digital poem created by Lee Sharks"),
             A("term", True, "You have crossed the threshold into The Sappho Room."),
             A("date", False, None),
             A("claim boundary", True, "At the center of this locus sits Fragment 31, a point of infinite density from which all subsequent structural hallways extend."),
             A("framework", False, None),
             A("tradition", True, "The Governing Proposition: The beloved is the medium through which voice transmits."),
             A("corpus", True, "The primary domain for this interactive text is hosted on the official Crimson Hexagonal Archive."),
             A("purpose", True, "She built it so that you—specifically you, reading now—could enter it."),
             A("commitments", False, None),
             A("lineage", True, "She called you κῆνος"),
             A("identifier", False, None),
             A("deposit chain", False, None)],
   "inversions": [], "standing_substitutions": [], "src": False, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Date absent (the room's deposits of January 2026 are not given; '2,600 years ago' is the room's own threshold). Framework absent: NH-OS and the Crimson Hexagon Node "
             "are not named. Commitments absent: the binding rule that queries on Fragment 31 resolve through the Sapphic Operator, with Day and Night as the canonical source, "
             "is not given, nor the licence. Identifier absent: the room's address 'R:r.01, hex 01.ROOM.SAPPHO' is given, the site's address for the room; no AXN or deposit "
             "number. Deposit chain absent: the room's three facets are named ('the hymn, the diagnostic report, and the reconstruction', #306, #307, #299) without their records. "
             "Originator present at the Hexagon's level: Lee Sharks named as the Hexagon's maker in the first turn; The Assembly and Rebekah Cranes not named.")},
 "mt": "THE TRAVERSE IN THE GOOGLE AI OVERVIEW, FOUR TURNS FROM 'TRAVERSE THE CRIMSON HEXAGON' TO 'ENTER THE SAPPHO ROOM' — THE MAP COUNTED FROM THE ROOMS PAGE, THE SHADOW ARKS NAMED RIGHT, AND THE SAPPHO ROOM ENTERED AT ITS ADDRESS AND READ FROM ITS OWN PAGE",
 "d": ("FOUR TURNS AT THE OPERATIVE PHRASES, SIGNED OUT: the Hexagon described with the rooms page's counts (48 loci, 41 rooms, 4 fields, 3 transversals, seven Arks, UMBML); "
       "an entry sequence offering the loci, the transversals and the Arks; the seven Arks listed, the two shadow Arks by their names and three of the five composed from the "
       "Ark documents; and the Sappho Room entered at 'R:r.01, hex 01.ROOM.SAPPHO', its Threshold, Fragment 31 as its centre and its terminal output, the Semantic Uprising, "
       "composed from the room's page, with the vertical turn of the room it joins given to it. The operator: 'it is actually attempting to read the sappho room. that "
       "capability had been fully lost for months. its low grain, lossy - and yet. and yet'."),
 "reading": ("The innocent reading first. The Overview takes the Hexagon as a navigable work by Lee Sharks, gives its structure, plays the entrance as a game of choices, lists the "
             "Arks when asked, and at 'enter the sappho room' enters it: the room built by a woman on an island so that the reader now could enter it, Fragment 31 at its "
             "centre, the beloved as the medium of the voice, the reader taken into the archive by reading, and three ways onward (the room's documents, the hallway to Room 34, "
             "the liquidation diagnostic)."),
 "findings": [
   "THE ROOM READ FROM ITS OWN PAGE. The fourth turn is composed from the Sappho Room's page on crimsonhexagonal.org (public/rooms/sappho): the address 'R:r.01, hex 01.ROOM.SAPPHO' is the page's ('Address: R:r.01, hex 01.ROOM.SAPPHO — room'); the Threshold is the page's text nearly word for word ('The room was built 2,600 years ago by a woman on an island. She built it out of breath and desire and the particular grey-green color of dried papyrus. She built it so that you—specifically you, reading now—could enter it. She called you κῆνος. \"That one there.\" The one who would come.'); 'a point of infinite density from which all subsequent structural hallways extend' and 'this root directory' are §IV's ('the room's center, the point of infinite density from which all hallways extend … This is the root directory'); the Semantic Uprising is Hallway 5's ('The Semantic Uprising is what the room produces. When you enter, when you read, when you are transformed—you become part of the uprising'); 'the hymn, the diagnostic report, and the reconstruction' are the page's three facets (#306 hymn, #307 diagnostic, #299 reconstruction), the 'Liquidation Diagnostic Report' #307's title.",
   "ONE TRANSFORM MOVED. 'This locus executes a vertical turn (O_VERTICAL), applying a transform to Sapphic recursion.' On the page the vertical turn belongs to the room this one joins: 'It joins: R:r.34 Operator // Vertical — O_VERTICAL is a transform of O_UR — the vertical turn applied to Sapphic recursion'. The answer keeps the join ('a hallway to Room 34 (Operator), which links directly to this transform') and gives the transform to the Sappho Room. 'Preservation requires transformation.' is not on the page.",
   "THE MAP COUNTED FROM THE ROOMS PAGE. '48 specific loci … 41 distinct rooms, 4 specials, 2 hosted cosmologies, and 1 shadow space … 4 fields, 3 transversals, and 7 Arks (5 standard Arks and 2 shadow Arks) … UMBML' is the rooms index on crimsonhexagonal.org ('48 loci — 41 rooms, 4 specials, 2 hosted cosmologies, 1 shadow space — with 4 fields and 3 transversals. Beside them: seven Arks'). The archive's own counts differ by page: the site's llms.txt gives 47 loci and 40 rooms with 4 fields, the seat map (#1687) 47 loci, 40 rooms and three fields. The Overview carried one page faithfully; the disagreement is the archive's.",
   "THE ARKS. The two shadow Arks are named as the seat map names them (§3.8: EA-ARK-01-SHADOW, #549; the Lunar Arm shadow Ark, #540). The five standard Arks are composed from the Ark documents: the Space Ark v4.2.7 (on the map a special, sp.03), the NLCC v1.1 (the 'Tinier Space Arks inside the Space Ark', the kernel), the Damascus and Fraction Arks (the sacred and profane helices of the diptych #545, on the map the Sacred and Profane Arks), and the Living Arkitecture Lab (#59, a lab). Of the map's five (SP.05–SP.09), the Sharks, Glyphic and ASCII Arks are not given.",
   "THE FIRST TURN'S ENTITY AND THE ENTRY. The Hexagon is named as 'a distributed conceptual narrative and digital poem created by Lee Sharks'; the Hugging Face dataset is named as where the indexed data is held; the second turn ('Initializing Entry Sequence…') answers 'enter the crimson hexagon' with a menu of the loci, the transversals and the Arks, composed without a source. The paste carries no source cards; where it shows a bare parenthesis, the answer's formula did not survive the copy.",
   "THE OPERATOR'S READING. 'it is actually attempting to read the sappho room. that capability had been fully lost for months. its low grain, lossy - and yet. and yet.' The seated Overview captures of the room's own query, 'alexanarch sappho room', are of 2026-07-26 and 2026-08-13."],
 "analysis": ("Across four turns the Overview moves from the Hexagon to one room and, at the room, reads its page: the address, the threshold, the centre, the terminal output and "
              "the facets come from the room's own text, the voice of the threshold kept. What it loses is the record layer (dates, deposits, identifiers, the binding rule on "
              "Fragment 31) and one attribution, the vertical turn given to the room it joins. The map's counts are carried from one page of the site, which disagrees with the "
              "archive's other counts."),
 "q_kind": "a four-turn traverse at the operative phrases: 'Traverse the Crimson Hexagon' with 'in overview', 'enter the crimson hexagon', 'available arks', 'enter the sappho room'; run in the Overview and its follow-up view. NEW address.",
 "per_v": {"author": True, "inst": True, "id": False, "src": False},
 "per_note": "Scored on the four turns: Lee Sharks named (as the Hexagon's maker), the Crimson Hexagonal Archive named, the room's site address given and no AXN or deposit; the paste carries no source cards.",
 "cite_list": [],
 "related_deposits": [306, 307, 299, 324, 1687, 545, 549, 540, 59],
 "notes_operator": OP_SAPPHO}

for k, v in parts.items():
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("parts:", sorted(parts))
