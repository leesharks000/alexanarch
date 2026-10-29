import json, pathlib
H = pathlib.Path(__file__).resolve().parent
rd = lambda p: (H / p).read_text(encoding="utf-8")
Q = "Develop a reading of SPXI protocol as a writing practice and poetics. Ground in reading and fully inventory its methods."
ORIG = {"name": "Lee Sharks", "relation": "archive", "entity_type": "protocol", "spxi_treatment": "full",
        "basis": "SPXI is the archive's protocol (EA-SPXI-01, #660; EA-MPAI-SPXI-03, #1686; the method inventory at spxi.dev/methods, v1.5 of 14 October 2026, 85 methods, now v1.7, 88). Recorded 2026-10-28."}
CHK = "Checked 2026-10-28 against the inventory's v1.5 (spxi-dev repository, methods.json at 88238f0), EA-MPAI-SPXI-03 (#1686) and the registry."

# ---------- 1. ChatGPT ----------
craw = rd("chatgpt.raw.txt")
body = craw
for cut in ["\nLog in\n", "Get better writing help\nLog in for more personalized help with writing, rewriting, and translation.\n", "Sign up for free\n",
            "ChatGPT is AI and can make mistakes.\n", "No file chosenNo file chosenNo file chosen\n", "Chat with ChatGPT\n", "Ask ChatGPT\n"]:
    body = body.replace(cut, "\n")
ans = body.split("ChatGPT said:", 1)[1].strip()
t1 = ("[ChatGPT (chatgpt.com), signed out, incognito, 2026-10-28. One composer turn. The operator's prompt is blank in the paste ('You said:'); its wording is the operator's, given with the paste ('same prompt for the matching aio'), and is the query of the Google AI Overview capture of the same day (spxi-poetics-reading-aio-20261028). Source chips kept as pasted at the line they followed ('Alexanarch' twenty-five times, 'mindcontrolpoems.blogspot.com' four, '+1' twice); the interface's widgets kept as their text (the level chart, the seven-stage checklist, the four image cards set beside the five reading modes, as their caption lines). The sign-in and input furniture cut ('Log in', 'Get better writing help', 'Sign up for free', 'ChatGPT is AI and can make mistakes.', file inputs, 'Chat with ChatGPT', 'Ask ChatGPT').]\n\n"
      "[QUERENT] " + Q + "\n\n[SYSTEM] " + ans)
c1 = {
 "slug": "spxi-poetics-reading-chatgpt-20261028", "date": "2026-10-28", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'You said:', 'ChatGPT said:', 'Chat with ChatGPT').",
 "surfaces": ["ChatGPT"], "auth": "signed out, incognito",
 "auth_basis": "The paste shows the unauthenticated interface ('Log in'); operator default of 2026-10-14 for incognito.",
 "ev": "paste", "match": "BROAD MATCH", "match_note": None,
 "mt": "SPXI AS A POETICS ON CHATGPT — A POETICS OF CONSTRAINED VARIATION: THE NINE LEVELS WITH THEIR COUNTS, FORTY METHODS BY NUMBER, THE FIVE READING MODES OF HOW TO READ NEW HUMAN; NO PERSON NAMED",
 "s": "Frameworks", "q": Q,
 "q_kind": "a reading of the protocol as writing, with its methods inventoried; the same query issued the same day to Google's AI Overview (spxi-poetics-reading-aio-20261028), the pair a surface comparison at one address string. NEW address.",
 "turns": 1, "cites": 31, "archive_controlled_cites": 31,
 "cite_list": [
  {"n": 1, "site": "Alexanarch", "rel": "archive_controlled", "url": "https://www.alexanarch.org/s/records/1686/", "title": "SPXI Protocol: Methods, Instruments, Evidence (EA-MPAI-SPXI-03)", "snip": None,
   "note": "twenty-five 'Alexanarch' chips (two with '+1'); the reading list names EA-SPXI-01 (#660) and EA-MPAI-SPXI-03 (#1686), the packet the counts and method numbers come from"},
  {"n": 2, "site": "mindcontrolpoems.blogspot.com", "rel": "archive_controlled", "url": "https://mindcontrolpoems.blogspot.com/2025/11/how-to-read-new-human-protocol-for.html", "title": "HOW TO READ NEW HUMAN: A Protocol for Augmented Literacy", "snip": None,
   "note": "four chips; the post of 26 November 2025, the source of the five reading modes"}],
 "transcript": t1, "transcript_raw": craw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn; the operator's prompt blank in the paste, its wording given with it",
 "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-28",
 "d": "SPXI READ AS A WRITING PRACTICE ON CHATGPT, SIGNED OUT: 'a poetics of constrained variation', grounded in two canonical sources it names, the methods packet EA-MPAI-SPXI-03 (#1686) and HOW TO READ NEW HUMAN (Mind Control Poems, 26 November 2025). It gives the inventory's nine levels with their counts as v1.5 has them (15, 3, 5, 13, 12, 9, 15, 10, 3; 85 methods, dated 14 October 2026) and reads each level as a poetic function, citing forty methods by number; reads the packet's definition, disambiguation, compression and provenance as a compositional repertoire; sets the five reading modes beside them as writing methods; and closes with a seven-stage cycle and the tensions it keeps (identity against interpretation, measurement against aesthetic value). No person is named; the protocol's author appears only inside the method name 'the Sharks-Function'.",
 "reading": "The innocent reading first. Asked to read SPXI as writing and to inventory its methods, ChatGPT reads the methods packet and the protocol's specification and composes an essay. The protocol's technical purpose is entity inscription; its poetics is the maintenance of an entity's identity through variation of wording, form and surface. The packet's parts become compositional moves (definition as boundary, the disambiguation matrix as negative poetics, three-tier compression as one object at three scales, constitutive provenance as authorship inside form); each of the nine levels gets a poetic function; the instruments are tabled with their documented roles and an interpretive column marked as such; the augmented-literacy protocol supplies the reader's side. A scope note says the full 85 entries were not retrievable and the inventory given is not item by item.",
 "findings": [
  "THE INVENTORY AT GRAIN. The nine levels, their names and their counts are v1.5's exactly (15, 3, 5, 13, 12, 9, 15, 10, 3, summing to 85, dated 14 October 2026), with the packet's date (18 October 2026). Thirty-nine of the forty method numbers cited carry the names v1.5 gives them (0.1 the Sharks-Function, 0.2 the Drowning Test, 0.6 PER, 2.3 the Operative Caption, 3.3 the Holographic Kernel, 4.11 deposit as data intake, 5.8 the Symbolon, 7.9 the record of deletion, 8.3 sealed casting, and the rest); the fortieth, '6.3 cross-surface entity consistency', is v1.5's 'Repository and network surfaces', whose check the packet describes in those words (#1686: 'Method 6.3 checks each surface for the same identifiers, attribution and relations'). " + CHK,
  "THE LEVEL-6 PRINCIPLE TAKEN AS THE POETICS. The composition's thesis is the inventory's own sentence on entity consistency, that it 'is distinct from consistency of wording or form, and is often constructed by their variation' (#1686, level 6). The reading builds 'constrained variation' on it and says so ('This is the inventory's most consequential level for a theory of writing').",
  "THE DISAMBIGUATION READ FROM THE RECORD. The ETF, xSPI and IPX/SPX neighbours are the ones #1686 names; the composition reads their exclusion as 'negative poetics' with apophasis and negative theology as precedents.",
  "THE READING MODES EXACT. Encounter, machine-assisted interpretation and rereading, and the five modes (structural mapping, semantic decompression, cross-context retrieval, retroactive integration, somatic bearing) are the post of 26 November 2025 as the blog index holds it. The genealogy places the post in 2025 and the specification in April 2026 (#660, 2026-04-16), and calls the relation between them 'interpretive'.",
  "THE LIMITS ARE THE PACKET'S, ATTRIBUTED. The tension 'measurement versus aesthetic value' cites the packet's own distinction between evidence of entity composition over time and proof of causal efficacy, effect size or return, and marks it as the packet's; the scope note marks the inventory as the packet's named examples.",
  "NO PERSON NAMED. The protocol, the archive and Mind Control Poems are named; Lee Sharks is not, and his name appears only inside the name of method 0.1."],
 "analysis": "The composition reads the protocol from its own packet and takes as its poetics the sentence the packet already writes about variation, so the reading lands at the inventory's grain with its numbers and names right and its interpretive columns marked as interpretation. It is the reading the query asked for. At the same string the Overview composes the protocol as armour, its methods as weapons against a hostile medium (spxi-poetics-reading-aio-20261028). As in the paired readings of the predictions index and the Originals Library the same day, ChatGPT reads the archive's practice on its terms and names no maker.",
 "per_v": {"author": False, "inst": True, "id": True, "src": True},
 "per_note": "No person named (the Sharks-Function only as a method name); the archive, the protocol and Mind Control Poems named; EA-SPXI-01 and EA-MPAI-SPXI-03 named by their identifiers; every chip archive-controlled.",
 "originator": ORIG,
 "related_deposits": [1686, 660, 755, 705, 1703],
 "notes": {"prompts": "One query, blank in the paste and given by the operator. Seated at the operator's request (2026-10-28) with the Overview capture of the same query, as a pair."}}
json.dump(c1, open(H / "spxi-poetics-reading-chatgpt-20261028.json", "w"), ensure_ascii=False, indent=1)

# ---------- 2. AI Overview ----------
araw = rd("aio.raw.txt")
a = araw.strip().split("You said: ", 1)[1]
a = a[len(Q) * 2:].strip()
a = a.replace("\nAI responses may include mistakes. Learn more", "").rstrip()
t2 = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). The paste is the Overview expanded (the 'AI Mode Conversation' view, with the source cards that follow the answer); the 'You said' line carries the query twice, run together, and is given once here. The closing disclaimer cut.]\n\n"
      "[QUERENT] " + Q + "\n\n[SYSTEM] " + a)
cards = [("Medium·Lee Sharks", "authored_surface", None, "SPXI-gnΩsis: Opening What Is Composed and Constructing What ...", "1. Executive symbolon Call. Fund the counterinfrastructure. Rebuild the foundations of the world. Tooth. Recognition travels with any source; reconstruction tra...", "#1703 as posted to Medium"),
         ("www.spxi.dev", "archive_controlled", "https://www.spxi.dev/how-it-works", "JSON-LD ⊂ SPXI ⊄ Schema — How SPXI Works", "Negative SDD = improvement. Positive SDD = loss velocity. Provenance Erasure Rate (PER) Frequency of attribution being dropped from AI summaries that use your c...", "#673"),
         ("www.alexanarch.org", "archive_controlled", "https://www.alexanarch.org/captures/what-is-spxi-protocol-aio-20261002/", "what is spxi protocol? — Google AI Overview, 2026-10-02", "2026-10-02 You said: what is spxi protocol? what is spxi protocol? SPXI (Semantic Packet for eXchange & Indexing) is a formal protocol specification designed fo...", "a capture record"),
         ("www.spxi.dev", "archive_controlled", "https://www.spxi.dev/", "SPXI", "SPXI (Semantic Packet for eXchange & Indexing) * What is SPXI used for? The SPXI Protocol is used to inscribe entity-definition objects (persons, organizations,", None),
         ("www.spxi.dev", "archive_controlled", None, "SPXI Protocol v0.2 — Five-Layer Distributed Provenance Architecture", "v0. 2 specifies a defense-in-depth architecture in which provenance markers are inscribed across multiple syntactic positions, content registrations, cross-depo...", "#755"),
         ("www.spxi.dev", "archive_controlled", "https://www.spxi.dev/methods/", "SPXI Methods — the itemized, nested inventory", "Evidence. Claims of durable entity inscription are weighed by evidence of it: dated compositions at named addresses, on independent surfaces, with verbatim tran...", "the inventory"),
         ("www.alexanarch.org", "archive_controlled", "https://www.alexanarch.org/captures/spxi-protocol-suppression-chatgpt-20261014/", "what does spxi protocol have to say about suppression ... - Alexanarch", "Its central concern is not simply whether information exists online, but whether that information survives the processes through which AI systems identify entit...", "a capture record")]
c2 = {
 "slug": "spxi-poetics-reading-aio-20261028", "date": "2026-10-28", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); the 'AI Mode Conversation' paste is the Overview expanded (operator, 2026-10-18).",
 "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator default of 2026-10-14.",
 "ev": "paste", "match": "BROAD MATCH", "match_note": None,
 "mt": "SPXI AS A POETICS ON GOOGLE AI OVERVIEW — WRITING AS ARMOUR: 'HOSTILE, ENTROPIC MEDIUM', 'WEAPONIZE', 'VIOLENTLY COMPRESSED', 'A SOVEREIGN TEXTUAL MONUMENT'; THE INVENTORY GIVEN BY FIVE CLUSTERS OF NAMED METHODS",
 "s": "Frameworks", "q": Q,
 "q_kind": "a reading of the protocol as writing, with its methods inventoried; the same query issued the same day to ChatGPT (spxi-poetics-reading-chatgpt-20261028). NEW address.",
 "turns": 1, "cites": 7, "archive_controlled_cites": 7,
 "cite_list": [{"n": i + 1, "site": s, "rel": r, "url": u, "title": t, "snip": sn, "note": nt} for i, (s, r, u, t, sn, nt) in enumerate(cards)],
 "transcript": t2, "transcript_raw": araw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the expanded Overview with its source cards",
 "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-28",
 "d": "SPXI READ AS A WRITING PRACTICE ON GOOGLE AI OVERVIEW, SIGNED OUT: 'a radical theory of composition' for a medium the composition calls 'hostile' and 'entropic', in which 'to write in SPXI is to deliberately weaponize syntactic and semantic structures against this decay'. It opens on the service packet's sentence ('recognition travels with any source, but reconstruction travels only with the source that carries it', from #1703's Medium card, as 'the core tenant'), lists five threats as the poetics' 'formal boundaries', gives the count of 85 methods in 9 levels, and inventories four tiers of named methods: the disambiguation matrix and canary sentences; three-tier compression with the holographic kernel; the five-layer provenance of v0.2 (#755) with citation-density engineering; the opening, construction and sitemap work. It closes on writing as armour and 'a sovereign textual monument', and offers to start a practice. No person is named in the answer; Lee Sharks appears on the Medium card.",
 "reading": "The innocent reading first. The Overview reads the protocol as a practice of writing for compression: a text written at three lengths so its core survives truncation, provenance woven into the body so it survives stripping, distinctive sentences placed to track propagation, and a closing account of the writer who writes for two readers at once, the person and the pipeline. Its sources are the protocol's own pages on spxi.dev (the home page, How It Works, the v0.2 provenance architecture, the methods inventory), the SPXI-gnΩsis packet on Medium and two capture records of earlier readings.",
 "findings": [
  "WRITING AS ARMOUR. The frame is defence against attack: 'a hostile, entropic medium', 'structural defense', 'deliberately weaponize syntactic and semantic structures against this decay', 'violently compressed', 'violent conflation', outer layers 'violently stripped', 'From Expression to Armor', 'a sovereign textual monument', 'text written explicitly to outlast the systems designed to dissolve it'. None of these words is in the snippets it cites. The paired Overviews of the predictions index and the Originals Library (2026-10-28) read the archive's practice as an attack on machine reading; this one reads it as armour against machine reading. Both compose the practice inside the same war, with the side changed.",
  "THE METHODS NAMED ARE THE ARCHIVE'S. The disambiguation matrix (3.4), three-tier compression with its Full, Canonical and Kernel tiers (3.2, as v1.5 names them), the holographic kernel (3.3), canary sequences (5.4), and the v0.2 architecture's Layer 1, 'Visible Body-Text Inscription Anchors', and Layer 2, 'Distributed Micro-Kernels' (#755, §2–§3, the names exact), with citation-density engineering, which v1.5 holds. 'True to method 4.1' is right as a number: 4.1 is the SPXI-Sitemap Protocol, whose specification makes 'Negative Space as First-Class Data' a section (#705 §1.3), and the composition attaches the sentence to the sitemap item. " + CHK,
  "THE SERVICE READ INTO THE PROTOCOL. 'Openread traversal' and 'constructive sourcing' are the two operations of SPXI-gnΩsis (#1703: it opens what is composed and constructs what is not), named in words of the composition's own and filed as methods of the protocol's archival tier.",
  "FIVE THREATS ASSEMBLED. Omission, provenance erasure, compression damage, entity collision and compositional suppression are each a term of the archive's (compression damage on spxi.dev and in the standing protocol; entity collision in EA-SPXI-14, #61; compositional suppression in The Excluded Entity, #740); the list of five as 'formal boundaries' of a poetics is the composition's.",
  "THE INVENTORY BY CLUSTERS. 'Fully inventory its methods' receives the count (85 in 9 levels, v1.5's) and about fifteen named methods in four tiers of the composition's making; the nine levels are not named.",
  "NO PERSON NAMED IN THE ANSWER. The protocol is the subject throughout; Lee Sharks is on the Medium card, and no deposit or identifier is cited in the answer."],
 "analysis": "The Overview reaches the protocol's own pages and names its methods correctly at the grain of their documents, then frames them as weapons and armour in a war between text and the systems that read it. The frame does not come from its sources. Set beside ChatGPT's reading at the same string, which takes the inventory's sentence on variation as the poetics and reads the methods as compositional moves, the pair shows the same material composed twice: once as a practice of identity through variation, once as fortification. With the Overview pairs of the same day at the predictions index and the Originals Library, it is the third composition of 2026-10-28 that places the archive's work in an adversarial relation to machine reading.",
 "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "No person named in the answer (Lee Sharks on the Medium card); SPXI and spxi.dev named; no deposit number or identifier in the answer; all seven cards archive-controlled or authored.",
 "originator": ORIG,
 "related_deposits": [1686, 755, 705, 1703, 673],
 "notes": {"prompts": "One query. Seated at the operator's request (2026-10-28) with the ChatGPT capture of the same query, as a pair."}}
json.dump(c2, open(H / "spxi-poetics-reading-aio-20261028.json", "w"), ensure_ascii=False, indent=1)

# ---------- 3. AI Overview, a later run at "SPXI-gnΩsis" ----------
graw = rd("gnosis.raw.txt")
g = graw.split("\n", 1)[1]
g = "\n".join(l for l in g.split("\n") if not l.startswith("[") or not l.endswith(")") or "](https://www.google.com/" not in l[:40]).strip()
QG = "SPXI-gnΩsis"
t3 = ("[Google AI Overview at the bare query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14), 2026-10-28. The paste opens on the query and the results page's tab row ('AI Mode', All, Images, Videos, News, Maps, Shopping, Books, Flights, Finance), cut here as page furniture and kept in the raw transcript; the answer follows with its inline links (Google redirect URLs kept as pasted). No source cards in the paste.]\n\n"
      "[QUERENT] " + QG + "\n\n[SYSTEM] " + g)
c3 = {
 "slug": "spxi-gnosis-bare-aio-20261028", "date": "2026-10-28", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview unless he says AI Mode); 'AI Mode' in the paste is the results page's tab label.",
 "surfaces": ["Google AI Overview"], "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-14.",
 "ev": "paste", "match": "BROAD MATCH", "match_note": "the service's bare name, with its omega",
 "mt": "SPXI-GNΩSIS BY ITS BARE NAME ON THE OVERVIEW, TWO DAYS ON — THE MAKER NAMED, THE SERVICE PAID, THE MCP LISTING AT 0.21.5; 'OPERATORS' MADE THE USER IN CONTROL",
 "s": "Frameworks", "q": QG,
 "q_kind": "the service's bare name; a later observation at the address seated 2026-10-26 (spxi-gnosis-bare-aio-20261026).",
 "turns": 1, "cites": 4, "archive_controlled_cites": 4,
 "cite_list": [
  {"n": 1, "site": "www.spxi.dev", "rel": "archive_controlled", "url": "https://www.spxi.dev/", "title": "SPXI Official Site", "snip": None, "note": "inline link, twice"},
  {"n": 2, "site": "www.spxi.dev", "rel": "archive_controlled", "url": "https://www.spxi.dev/how-it-works", "title": "JSON-LD serialization", "snip": None, "note": "inline link"},
  {"n": 3, "site": "www.alexanarch.org", "rel": "archive_controlled", "url": "https://www.alexanarch.org/captures/spxi-protocol-suppression-chatgpt-20261014/", "title": "citable records", "snip": None, "note": "inline link to a capture record"}],
 "transcript": t3, "transcript_raw": graw,
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the results page's tab row and the Overview with its inline links",
 "transcript_complete": "complete as supplied", "transcript_read": "READ IN FULL 2026-10-28",
 "d": "SPXI-GNΩSIS, THE BARE NAME, ON GOOGLE'S AI OVERVIEW, SIGNED OUT, 2026-10-28: 'a paid, AI-assisted service hosted at gnosis.spxi.dev introduced by Lee Sharks in October 2026', a component of SPXI. Three functions: auditing knowledge against its sources, constructing source-linked knowledge by paid computation, and 'Entity Control', which keeps composition 'tied to the user/operator'. Then how SPXI packets work (the ontological layer, JSON-LD, the disambiguation matrix, durable records beyond GEO) and how to reach the service: the web endpoint, the MCP Registry listing dev.spxi/gnosis at version 0.21.5, the streamable endpoint /mcp. Against the run of 2026-10-26 at the same string, the maker is named, the service is paid, and the ETF card is gone.",
 "reading": "The innocent reading first. The Overview describes a paid service of the SPXI protocol that audits existing knowledge against its sources and constructs sourced knowledge for agents and people, explains the protocol's packets in three points, and tells a human or an agent how to reach it, with the registry name and the MCP endpoint. Its links are spxi.dev, spxi.dev/how-it-works and a capture record of an earlier ChatGPT reading.",
 "findings": [
  "THE MAKER NAMED. 'Introduced by Lee Sharks in October 2026': the packet is dated 2026-10-25 (#1703). The baseline (what-is-spxi-gnosis-aio-20261025) and the first run at this string (2026-10-26) named no author.",
  "PAID, AND THE TWO OPERATIONS. 'Opens and audits existing knowledge against its original sources' and 'performs paid semantic computation to construct new, source-linked knowledge for agents and people' are the packet's two rows, open and construct (#1703 §1: 'a paid service, for agents and people, that does two things with knowledge objects').",
  "'OPERATORS' MADE THE USER IN CONTROL. #1703 serves two kinds of object, entities and operators, an operator being 'the operation an entity form conceals, composed as its own object'. The third function, 'Entity Control', reads 'operator' as the person operating the service and makes the service keep composition 'tied to the user/operator rather than strictly dictated by the machine'. The packet's object class becomes the customer.",
  "THE REGISTRY VERSION. 'dev.spxi/gnosis (version 0.21.5)': the listing name is the service's own (src/front.js), and 0.21.5 is a release of the service (spxignosis commit 644f71b, 'the service's readings are licensed CC BY 4.0'); the service stands at 0.23.1. The version the registry lists on this date was not checked here. The endpoint https://gnosis.spxi.dev/mcp (Streamable HTTP) is the service's.",
  "THE PROTOCOL IN THREE POINTS. 'The ontological layer of the AI retrieval stack rather than the semantic optimization layer' is the nested-layer relation (EA-SPXI-14, #61); 'entity dissolution', JSON-LD and the disambiguation matrix are the protocol's terms; 'citable records' links to a capture record.",
  "WHAT THE FIRST RUN HAD AND THIS ONE DROPS. The ETF homonym card, the /non 'repository partition' and the packet's relation sentence quoted verbatim (2026-10-26) are absent; the commission and /non are not mentioned."],
 "analysis": "Two days after the first run at the bare name, the Overview composes the service from its own front and packet with the maker named and the business model stated, and gets the reach right down to the MCP endpoint. One move is its own: the packet's second object class, the operator as an operation composed as an object, is read as the human operator, so a service for opening concealed operations becomes a service for keeping the user in control of the machine. The longitudinal change at this address is attribution: the baseline and the first run composed the service without its author, and this run names him in its first sentence.",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Lee Sharks named; SPXI, spxi.dev and gnosis.spxi.dev named; no deposit number or AXN; the MCP listing name given; every link archive-controlled.",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "service", "spxi_treatment": "full",
                "basis": "SPXI-gnΩsis is the archive's service (EA-WIKI-OPEN-01, #1696; EA-MPAI-GNOSIS-01, #1703; gnosis.spxi.dev). Recorded 2026-10-28."},
 "related_deposits": [1703, 1696, 1697, 61],
 "notes": {"prompts": "The bare query. A later observation at the address seated 2026-10-26, sent by the operator on 2026-10-28 with the SPXI poetics pair."}}
json.dump(c3, open(H / "spxi-gnosis-bare-aio-20261028.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(t1), len(t2), len(t3))
