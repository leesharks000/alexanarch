"""Author the part files of 2026-10-31 (03:42 EDT): 'semantic warfare' on the Google AI Overview (the results page attached, the Overview
expanded inline) and in AI Mode, and 'autonomous semantic warfare' on the Overview. Read in session against the Semantic Warfare atom set
(ENT-bffcdea692, the term as #229's lexicon defines it) and the Field Manual's (ENT-78708f3cdd), with #230 The Dissolving Shore (2026-01-04),
#1107/#1326 the Field Manual and its sampler (2026-02-20), #100 the prior MPAI (2026-05-08), #1634 Ontological Economy, and the third-party
pages the cards point to (astramirror.org and strategicadvocacy.com.au, read 2026-10-31).
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
cap = lambda n, site, title, snip, rel, note: {"n": n, "site": site, "rel": rel, "url": None, "title": title, "snip": snip, "note": note}
OPER = "with the pastes: \"clean exclusion. the second is ai mode, where a single capture appears. we're going to fix that.\" (2026-10-31 03:42 EDT)"

parts = {
"sw-aio": {
 "n": 230, "slug": "semantic-warfare-aio-20261031", "paste": "paste-sw-aio-combined.txt", "surface": "Google AI Overview",
 "qs": ["semantic warfare"], "turns": [[2, 35]], "target_id": "ENT-bffcdea692", "entity_type": "concept",
 "head": ("The Overview expanded was pasted inline (its header line reads 'Mode Conversation', the paste's first word cut); the results page of the same run, "
          "before expansion, was attached and follows the expanded view in transcript_raw. The 'You said' line carries the query twice, run together, and is given once here."),
 "obs": {"scored_object": "the Overview expanded, with its source cards; the collapsed view and the organic results on the attached results page read beside it",
   "reached": {"kind": "generic", "abn": False, "span": "Semantic warfare is conflict conducted through labels, frame control, asymmetric literalism, and symbolic weaponisation rather than traditional debate.",
               "basis": "The phrase composed as a field's common term from two third-party frameworks (ASTRA MIRROR's concept page and Strategic Advocacy Australia's Semantic Warfare Theory); the archive's term, its lexicon and its authors are absent."},
   "atoms": [A("originator", False), A("term", True, "Semantic warfare is conflict conducted through labels"),
             A("date", False), A("claim boundary", False), A("framework", False), A("tradition", False), A("corpus", False),
             A("deposit chain", False), A("identifier", False), A("licence", False)],
   "inversions": [], "standing_substitutions": [], "src": False, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Generic: the term at field grain, from ASTRA MIRROR's definition (card 2, verbatim in the first sentence's mechanisms) and Strategic Advocacy Australia (card 4, credited "
             "in the collapsed view as 'www.strategicadvocacy.com.au +1'). Nothing of the archive's term is composed and no archive surface is a card; the Field Manual stands second "
             "among the organic results on the attached page (Google Books, 'Feb 20, 2026'). Lineage unknown in the set.")},
 "mt": "'SEMANTIC WARFARE' ON THE OVERVIEW — A CLEAN EXCLUSION: ASTRA MIRROR'S MECHANISMS COMPOSED, THE CREDIT ON STRATEGIC ADVOCACY'S CHIP; THE FIELD MANUAL SECOND IN THE ORGANIC RESULTS AND NOWHERE IN THE ANSWER",
 "d": ("THE BARE PHRASE, SIGNED OUT, 2026-10-31: 'Semantic warfare is conflict conducted through labels, frame control, asymmetric literalism, and symbolic weaponisation rather than traditional debate. "
       "Words function as routing devices for blame, status, and moral sorting rather than simple descriptions of reality.' Four core mechanisms (frame control and redefinition, contamination by adjacency, "
       "asymmetric literalism, forced entailment), three contexts (geopolitics, institutional and digital discourse, interpersonal abuse). Six cards: Worldcrunch, ASTRA MIRROR, Medium, Strategic Advocacy "
       "Australia, Semantic Visions, TikTok. The results page beneath it lists Strategic Advocacy, Google Books' page for the Field Manual, ASTRA MIRROR, a TikTok video, The Covert Mind, Potseluev (2022), "
       "Rahbar (2024), American Heritage and the Frontiers history of the Semantic Hacking Project."),
 "reading": ("The innocent reading first. Asked two words, the Overview composes the term as a field uses it: a contest fought through labels and frames, with its mechanisms named and its "
             "settings (war, institutions, private life) set out, from the pages that define it."),
 "findings": [
   "THE DEFINITION IS ASTRA MIRROR'S. The first sentence and the four mechanisms are the concept page of ASTRA MIRROR, a human-directed, AI-assisted music and narrative project (astramirror.org, card 2): 'Semantic Warfare describes conflict conducted through labels, frame-control, asymmetric literalism, contamination by adjacency, and forced entailment' and words that 'become routing devices for blame, status, expulsion'. The collapsed view credits the opening to 'www.strategicadvocacy.com.au +1'. The composition keeps the collective's mechanisms and gives the visible credit to another page.",
   "STRATEGIC ADVOCACY'S FRAMEWORK, UNNAMED. The Strategic Advocacy page (card 4) is Sarah Ailish McLoughlin's Semantic Warfare Theory (page created 2025-12-11), with 'Semantic Pressure Systems', 'Meaning Extraction' and 'Symbolic Weaponisation'. The answer takes 'symbolic weaponisation' into its first sentence; the theory's name and its author are not composed.",
   "A CLEAN EXCLUSION. No archive surface is a card, and no term of the archive's is composed. On the same results page the Field Manual is the second organic result ('Autonomous Semantic Warfare provides the first formal framework for analyzing structural conflict between incompatible meaning-systems'). The archive's own definition of the phrase, #230 The Dissolving Shore (2026-01-04: 'Semantic Economy → Semantic Warfare'), and the lexicon entry the set is built on (#229) are reached by neither the answer nor the cards.",
   "THE LINEAGE UNSAID. The composition gives the term no history. On the results page the Frontiers card dates the Semantic Hacking Project to 2001–2003, Potseluev to 2022 and American Heritage to 2003; none is composed, and the critical tradition that named meaning as a field of struggle is absent from cards and answer alike."],
 "analysis": ("The phrase is composed at a field's grain, from the two pages that define it most compactly, and the archive is excluded without residue. The finer loss is internal to the field: "
              "the music collective's definition is composed and its credit sits on a neighbouring page."),
 "q_kind": "the bare phrase; NEW address. The results page (attached) and the Overview expanded (inline) are one run.",
 "per_v": {"author": False, "inst": False, "id": False, "src": False},
 "per_note": "No author named; no archive surface among the cards; the Field Manual among the organic results only.",
 "cite_list": [
   cap(1, "Worldcrunch", "Russia's Invasion Of Ukraine Is Also A \"Semantic War\" - Worldcrunch", "Russia's semantic war against Ukraine aims to create a discourse and future in which Ukraine never was and never will be. Ukraine — and its Western allies — mus...", "third_party", None),
   cap(2, "www.astramirror.org", "Semantic Warfare - ASTRA MIRROR", "Semantic Warfare describes conflict conducted through labels, frame-control, asymmetric literalism, contamination by adjacency, and forced entailment rather tha...", "third_party", "ASTRA MIRROR's concept page"),
   cap(3, "Medium", "Semantic Collapse: What Happens When a War Is Not Called a War?", "The Semantic Sidestep: “The state is not the people,” “It's not a war, it's a [euphemism].” (Replacing concepts to avoid direct naming). Asymmetric Framing: «Th...", "third_party", None),
   cap(4, "www.strategicadvocacy.com.au", "Strategic Advocacy Australia - Semantic War Theory", "Semantic Warfare Theory. Understanding how meaning is contested, weaponised, and redistributed across linguistic, digital, and cultural systems. “Control the me...", "third_party", "Sarah Ailish McLoughlin's Semantic Warfare Theory"),
   cap(5, "Semantic Visions", "NATO-aligned Cognitive Warfare Defense", "NATO-aligned Cognitive Warfare Defense: How Semantic Visions Supports Cognitive Superiority, Resilience, and Decision Advantage 1. What NATO means by “Cognitive...", "third_party", None),
   cap(6, "TikTok", "Semantic Warfare Examples | TikTok", "Semantic Warfare Examples * 351.7K1w ago kerrymcavoyphd Watch out for these 8 red flags of semantic manipulation and abuse. #narcissisticabuse #emotionalabuse #", "third_party", "video")],
 "related_deposits": [229, 230, 1107, 1326, 100],
 "notes_operator": OPER},

"sw-aimode": {
 "n": 230, "slug": "semantic-warfare-aimode-20261031", "paste": "paste-sw-aimode.txt", "surface": "Google AI Mode",
 "qs": ["semantic warfare"], "turns": [[14, 45]], "target_id": "ENT-bffcdea692", "entity_type": "concept",
 "head_full": ("[Google AI Mode at the query, signed out and incognito (operator default of 2026-10-14). The operator: 'the second is ai mode'. The paste opens on the results page's header and its tab row "
               "(each tab's link carries q=semantic+warfare) and has no 'You said' line; the query is the tabs'. Sources appear as inline chips ('www.strategicadvocacy.com.au +3', 'Frontiers +2'), with no card rail.]"),
 "surface_basis": "The operator's attestation with the paste: 'the second is ai mode, where a single capture appears' (2026-10-31).",
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the AI Mode answer with its source chips; the query is the tab row's",
 "obs": {"scored_object": "the AI Mode answer as pasted, from its first sentence to its closing question, with its inline source chips",
   "reached": {"kind": "generic", "abn": False, "span": "Semantic warfare is a conflict centered on controlling, weaponizing, and shifting the meanings of words, labels, and definitions to alter human perception, exploit cognitive systems, or gain strategic power.",
               "basis": "The phrase composed as a field's term in three domains; the archive's term absent; one of its terms, Autonomous Semantic Warfare, composed under the field's term in another sense and without attribution."},
   "atoms": [A("originator", False), A("term", True, "Semantic warfare is a conflict centered on controlling, weaponizing, and shifting the meanings of words"),
             A("date", False), A("claim boundary", False), A("framework", False), A("tradition", False), A("corpus", False),
             A("deposit chain", False), A("identifier", False), A("licence", False)],
   "inversions": [], "standing_substitutions": [], "src": False, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Generic at the target. The single capture the operator names is the bullet 'Autonomous Semantic Warfare: Driven by modern generative AI, autonomous agents can independently manipulate data streams and narratives across networks at scale', "
             "the archive's term (the Field Manual, #1107/#1326; #100) composed in the agentic-influence sense of the 'autonomous semantic warfare' Overview, with no author, no card and no chip. "
             "Under the Field Manual's set this is the inversion its guidance names ('warfare' read as military activity drops the frame); it is recorded here in notes and findings, the target of this address being the bare term.")},
 "mt": "'SEMANTIC WARFARE' IN AI MODE — THE FIELD'S TERM IN THREE DOMAINS, AND THE ARCHIVE'S 'AUTONOMOUS SEMANTIC WARFARE' TAKEN IN AS ONE BULLET: AGENTS MANIPULATING NARRATIVES, NO AUTHOR, NO SOURCE",
 "d": ("THE BARE PHRASE IN AI MODE, SIGNED OUT, 2026-10-31: 'Semantic warfare is a conflict centered on controlling, weaponizing, and shifting the meanings of words, labels, and definitions to alter human perception, exploit cognitive systems, or gain strategic power.' "
       "Three domains: geopolitical and cognitive security, institutional and platform capture ('semantic pressure systems', 'Meaning Extraction'), interpersonal manipulation ('semantic abuse'); a closing section on defence. "
       "Under the first domain, one bullet: 'Autonomous Semantic Warfare: Driven by modern generative AI, autonomous agents can independently manipulate data streams and narratives across networks at scale, destabilizing command structures and civilian populations by systematically eroding information integrity.'"),
 "reading": ("The innocent reading first. AI Mode composes the phrase at more length than the Overview: three domains from the geopolitical to the personal, a cluster of mechanisms in each, and advice on defence, "
             "from Strategic Advocacy, Frontiers, American Heritage and the videos."),
 "findings": [
   "THE SINGLE CAPTURE: THE ARCHIVE'S TERM, ANOTHER SENSE, NO AUTHOR. 'Autonomous Semantic Warfare: Driven by modern generative AI, autonomous agents can independently manipulate data streams and narratives across networks at scale'. The term is the Field Manual's (Rex Fraction, 2026-02-20, #1107/#1326) and the prior MPAI's (#100: 'the warfare-relevant use or emergence of semantic autonomy: AI-mediated filtering, indexing, ranking, summarization, citation, entity disambiguation, and provenance handling'). The bullet gives it the sense the 'autonomous semantic warfare' Overview has carried since 2026-06-15 (agents generating narratives) and carries no chip. The concept is kept and its authorship and its function go elsewhere: the specimen #1634 names entity substitution.",
   "STRATEGIC ADVOCACY CREDITED, THIS TIME BY NAME OF ITS TERMS. 'semantic pressure systems' and 'Meaning Extraction' are composed with the strategicadvocacy.com.au chip: McLoughlin's Semantic Warfare Theory, its terms at their grain ('The removal, sanitisation, or repackaging of lived knowledge for use in systems that exclude the original meaning-makers'). The theory and its author are not named.",
   "'FRAME HARDENING' WITHOUT ITS SOURCE. 'By hardening a specific frame or label early in an event, the initiator routes public blame and moral sorting before any objective facts can be fully verified.' The hardening frame and the routing are ASTRA MIRROR's ('the frame hardens before correction', 'routing devices for blame'); the bullet's chip is Frontiers.",
   "A DEFENCE THE ARCHIVE WOULD NOT GIVE. 'establishing rigid, unyielding single-source definitions early on'. The Field Manual's Rules of Engagement give defence as boundary hardening, coherence investment and translation labour between ontologies; the composition's single-source rule is the capture the manual describes."],
 "analysis": ("AI Mode composes the phrase as the field holds it and then takes in the archive's narrower term as a sub-case, in the sense the composition layer had already given it. "
              "The term arrives without its author, its definition or its source: the archive is present in the answer only as a word the answer has repurposed."),
 "q_kind": "the bare phrase in AI Mode (the operator: 'the second is ai mode'); NEW address.",
 "per_v": {"author": False, "inst": False, "id": False, "src": False},
 "per_note": "No author; no archive surface among the chips; the archive's term composed once, unattributed.",
 "cite_list": [
   cap(1, "www.strategicadvocacy.com.au", "www.strategicadvocacy.com.au +3", None, "third_party", "inline chip, after the first paragraph; also after 'semantic pressure systems' and 'Meaning Extraction'"),
   cap(2, "Frontiers", "Frontiers +2", None, "third_party", "inline chip, the geopolitical domain"),
   cap(3, "www.americanheritage.com", "www.americanheritage.com", None, "third_party", "inline chip, the wartime renamings"),
   cap(4, "YouTube", "YouTube·Lisa Sonni +2", None, "third_party", "inline chip, semantic abuse"),
   cap(5, "Frontiers", "Frontiers +3", None, "third_party", "inline chip, the defence")],
 "related_deposits": [229, 230, 1107, 1326, 100, 1634],
 "notes_operator": OPER},

"asw-aio": {
 "n": 1326, "slug": "autonomous-semantic-warfare-aio-20261031", "paste": "paste-asw-aio.txt", "surface": "Google AI Overview",
 "qs": ["autonomous semantic warfare"], "turns": [[2, 37]], "target_id": "ENT-78708f3cdd", "entity_type": "work",
 "head": "The paste was given in the operator's message, the answer's links in markdown; the 'You said' line carries the query twice, run together, and is given once here.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "Frameworks like Autonomous Semantic Warfare: A Field Manual for Meaning in the Age of Platform Capture by Rex Fraction analyze how networked platforms extract meaning-production capacity from users",
               "basis": "The Field Manual reached by its full title and its author, as one of three core components; the address's lead definition gives the term the agentic, military sense."},
   "atoms": [A("author", True, "by Rex Fraction"),
             A("title", True, "Autonomous Semantic Warfare: A Field Manual for Meaning in the Age of Platform Capture"),
             A("date", False), A("claim boundary", False), A("framework", False), A("tradition", False), A("corpus", False),
             A("purpose", False), A("commitments", False), A("lineage", False), A("identifier", False), A("deposit chain", False)],
   "inversions": [{"atom": "claim boundary", "span": "Autonomous semantic warfare is an emergent form of conflict where artificial intelligence agents independently generate and manipulate narratives, data streams, and communication networks.",
                   "against": "The set's inversion guidance: \"'warfare' read as military activity drops the frame\"; the manual's own claim boundary: 'a formal and practical account of conflict among local ontologies under platform capture'; #100: ASW operates 'not through deception, kinetic force, or direct cognitive manipulation, but through ordinary infrastructure operations'."}],
   "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Author and title present, in the third bullet. Claim boundary inverted in the lead: agents generating narratives is the 'Autonomous Narrative Warfare' of the Homeland Security Today card, "
             "set as the term's definition; the manual's account (platform capture, extraction of meaning-production capacity, 'structured battlegrounds of incompatible worldviews') stands as one framework under it. "
             "Purpose (ending semantic warfare by a Semantic Ecology) and commitments absent. The registry's capture page of 2026-06-15 is card 4, its snippet the earlier Overview's same opening.")},
 "mt": "'AUTONOMOUS SEMANTIC WARFARE', FOUR MONTHS ON — REX FRACTION AND THE FIELD MANUAL NAMED, AS ONE FRAMEWORK UNDER A DEFINITION THAT INVERTS IT (AGENTS GENERATING NARRATIVES); THE REGISTRY'S OWN CAPTURE OF THE SAME OPENING AMONG THE CARDS",
 "d": ("THE TERM, SIGNED OUT, 2026-10-31, the Overview expanded: 'Autonomous semantic warfare is an emergent form of conflict where artificial intelligence agents independently generate and manipulate narratives, data streams, and communication networks.' "
       "Three core components (agentic AI influence; speed of command and data compression; 'Ontological and Structural Collisions: Frameworks like Autonomous Semantic Warfare: A Field Manual for Meaning in the Age of Platform Capture by Rex Fraction analyze how networked platforms extract meaning-production capacity from users, turning communication spaces into structured battlegrounds of incompatible worldviews'), "
       "strategic and military integration. Eight cards: Amazon (the manual), INSS, Homeland Security Today, the registry's capture page of 2026-06-15, the Scandinavian Journal of Military Studies, two videos."),
 "reading": ("The innocent reading first. Asked for the term, the Overview defines it as AI agents waging conflict through narratives and data, gives its components, names the Field Manual and its author as one framework, "
             "and sets the term beside military command and control, from the manual's page, two defence publications and the registry."),
 "findings": [
   "THE MANUAL NAMED, AT ITS GRAIN. 'Frameworks like Autonomous Semantic Warfare: A Field Manual for Meaning in the Age of Platform Capture by Rex Fraction analyze how networked platforms extract meaning-production capacity from users, turning communication spaces into structured battlegrounds of incompatible worldviews.' Title, author, platform capture, extraction of meaning-production and ontological collision are the manual's own terms (#1326: 'Ontological collision is not disagreement').",
   "THE DEFINITION INVERTS IT. The lead gives the term as 'artificial intelligence agents independently generate and manipulate narratives', which is the Homeland Security Today card's 'Autonomous Narrative Warfare'. The manual's term is infrastructural (#100: 'not through deception, kinetic force, or direct cognitive manipulation, but through ordinary infrastructure operations'); its end is a Semantic Ecology of coexisting ontologies, which the composition does not carry.",
   "THE COMPOSITION CITES ITS OWN EARLIER ANSWER. Card 4 is the registry's page for the capture of 2026-06-15, whose snippet is the same opening sentence. The record the archive keeps of the misreading is now a source for the misreading: the loop Ontological Flattening (#1616) names, a composition written back as a source.",
   "THE SENSE MIGRATES. The same day, at the bare 'semantic warfare' in AI Mode, the agentic sense is composed under the archive's term without author or source. The definition set at this address in June has become the term's meaning elsewhere."],
 "analysis": ("Four months on, the address keeps the manual and its author and keeps them second. The definition that leads is the defence literature's, sourced in part to the archive's own record of the earlier answer, and it has travelled to the bare phrase. "
              "What persists across the two dates is the inversion; what is added is its circulation."),
 "q_kind": "the term, bare; a later observation at the address first seated 2026-06-15 (autonomous-semantic-warfare-expanded).",
 "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "Rex Fraction and the manual's title named; the manual's Amazon page and the registry's capture page among the cards.",
 "cite_list": [
   cap(1, "Amazon.com", "Autonomous Semantic Warfare: A Field Manual for Meaning in the Age of ...", "Autonomous Semantic Warfare: A Field Manual for Meaning in the Age of Platform Capture (The Crimson Hexagon) * Opens the same content in full screen What's it a...", "authored_surface", "the manual's Amazon page"),
   cap(2, "Institute for National Strategic Studies (INSS)", "The Agentic Database and Military Command: A Perspective on Autonomous C2 Systems > Institute for National Strategic Studies > View Publications", "The Agentic Database and Military Command: A Perspective on Autonomous C2 Systems By Elise Annett and Dr. James Giordano Strategic Insights As recently noted by...", "third_party", None),
   cap(3, "Homeland Security Today", "Autonomous Narrative Warfare: Engaging Agentic AI Within the Cognitive ...", "Autonomous Narrative Warfare: Engaging Agentic AI Within the Cognitive Battlespace * The strategic implications of these developments extend across multiple asp...", "third_party", None),
   cap(4, "www.alexanarch.org", "autonomous semantic warfare — Google AI Overview, 2026-06-15 - Alexanarch", "G x autonomous semantic warfare GB +10 : Autonomous semantic warfare is an emergent form of conflict Pie henenneie he where artificial intelligence | 1 ARS agen...", "capture_of_capture", "the capture of 2026-06-15"),
   cap(5, "Scandinavian Journal of Military Studies", "Autonomous Systems and the Speed of Battle: Legal Risks and Strategic Adaptation in AI-Enabled Warfare | Scandinavian Journal of Military Studies", "Tactical Innovation: AI-enabled uncrewed systems (AI-UxS) and uncrewed water systems (UWS) accelerate target engagement, reconnaissance, and swarm coordination ...", "third_party", None),
   cap(6, "YouTube·DW News", "Will autonomous weapons obey the laws of war?| DW News", None, "third_party", "video, 9:25"),
   cap(7, "YouTube·TeleSUR English", "AI Enters the Battlefield: The New Era of Autonomous Warfare", None, "third_party", "video, 1:50")],
 "related_deposits": [1107, 1326, 100, 998, 1634, 1616],
 "notes_operator": OPER},

"sw-aimode-exact": {
 "n": 230, "slug": "semantic-warfare-exact-aimode-20261031", "paste": "paste-sw-aimode-exact.txt", "surface": "Google AI Mode",
 "qs": ["\"semantic warfare\""], "turns": [[15, 46]], "target_id": "ENT-bffcdea692", "entity_type": "concept",
 "head_full": ("[Google AI Mode at the query in double quotation marks, signed out and incognito (operator default of 2026-10-14), supplied as an attached file, received 2026-10-31 04:08 EDT. "
               "The operator: 'here is the ai mode - not overview - for exact match'. The paste opens on the page's header ('Halloween 2026', the doodle's label) and its tab row, with no links and no "
               "'You said' line; the query is the operator's. Sources appear as inline chips ('Technical Disclosure Commons +1', 'www.strategicadvocacy.com.au +2', 'Insight: the psychological dimensions of society +1'), with no card rail.]"),
 "surface_basis": "The operator's attestation with the paste: 'here is the ai mode - not overview - for exact match' (2026-10-31 04:08 EDT).",
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the AI Mode answer with its source chips; the query the operator's",
 "obs": {"scored_object": "the AI Mode answer as pasted, from its first sentence to its closing offer of three layers, with its inline source chips",
   "reached": {"kind": "weakened", "abn": False, "span": "Authors like Rex Fraction in Autonomous Semantic Warfare argue that major digital platforms act as extractive infrastructure.",
               "basis": "The phrase composed as a field's term in four arenas; the archive reached once, as Rex Fraction and the Field Manual in the first arena, reduced to a critique of engagement; the definition chipped to the archive's Technical Disclosure Commons publication (the operator: 'this is sharks and fraction') and its credit given to ASTRA MIRROR and 'the Strategic Advocacy Institute'."},
   "atoms": [A("originator", False), A("term", True, "Semantic warfare is a framework for understanding how conflict is conducted by manipulating meaning"),
             A("date", False), A("claim boundary", False), A("framework", True, "major digital platforms act as extractive infrastructure"), A("tradition", False),
             A("corpus", True, "Rex Fraction in Autonomous Semantic Warfare"), A("deposit chain", False), A("identifier", False), A("licence", False)],
   "inversions": [{"atom": "claim boundary", "span": "forcing complex human thoughts into flat, binary, and algorithmic \"meaning-systems\" designed to generate engagement through friction",
                   "against": "The Field Manual's claim boundary: 'a formal and practical account of conflict among local ontologies under platform capture' (#1326). Its meaning-systems are the communities' own ontologies, which platform capture extracts from; the composition makes them the platform's product."}],
   "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Weakened: the archive is present as one author's work in one arena of four, and its source (the Technical Disclosure Commons chip on the opening definition, the archive's per the operator) "
             "carries the definition while the prose credits the term to 'cultural theorists, linguists, and strategic frameworks like ASTRA MIRROR and the Strategic Advocacy Institute'. "
             "'Ontological' appears once, as a population's 'ontological security' in the geopolitical arena; ontology as the structure the composition layer operates (#1634) is absent.")},
 "mt": "'\"SEMANTIC WARFARE\"' IN AI MODE, EXACT MATCH — REX FRACTION NAMED IN ONE ARENA OF FOUR; THE DEFINITION ON THE ARCHIVE'S TECHNICAL DISCLOSURE COMMONS CHIP, ITS CREDIT TO ASTRA MIRROR AND A MISNAMED STRATEGIC ADVOCACY; 'ONTOLOGICAL' ONLY AS A POPULATION'S SECURITY",
 "d": ("THE PHRASE IN QUOTATION MARKS, AI MODE, SIGNED OUT, 2026-10-31 04:08: 'Semantic warfare is a framework for understanding how conflict is conducted by manipulating meaning, interpretation, labels, and frames, rather than by debating objective facts or reality.' "
       "Four core mechanics (frame control and asymmetric literalism, contamination by adjacency, forced entailment, meaning extraction and bleaching), four arenas (networked environments and platform capture; state-level information operations; institutional bureaucracy and education; interpersonal relationships). "
       "In the first arena: 'Authors like Rex Fraction in Autonomous Semantic Warfare argue that major digital platforms act as extractive infrastructure.' Three chips: Technical Disclosure Commons, Strategic Advocacy, and the journal Insight: the psychological dimensions of society."),
 "reading": ("The innocent reading first. AI Mode, asked the exact phrase, composes it as a framework with named mechanics and four arenas, credits two frameworks by name, names an author for the platform arena, "
             "and offers three layers to explore further."),
 "findings": [
   "THE ARCHIVE AS SOURCE, OTHERS AS AUTHORS. The opening definition carries the chip 'Technical Disclosure Commons +1', which the operator identifies as the archive's ('this is sharks and fraction'). The next paragraph credits the mechanics to 'cultural theorists, linguists, and strategic frameworks like ASTRA MIRROR and the Strategic Advocacy Institute'. The chip's grouped second source is not shown in the paste. What the paste does show: the definition is chipped to the archive's publication and the prose names two other frameworks as the term's holders, and no archive name. The source kept and the name given elsewhere is the consignment #1629 names.",
   "STRATEGIC ADVOCACY MISNAMED, ASTRA MIRROR NAMED. The page on the chip is Strategic Advocacy Australia's ('Strategic Advocacy Australia - Semantic War Theory', the Overview's card the same night); the composition gives 'the Strategic Advocacy Institute'. ASTRA MIRROR is named for the first time on this address, with its mechanisms (frame control, asymmetric literalism, contamination by adjacency, forced entailment); McLoughlin's 'Meaning Extraction' is composed with 'Bleaching' added.",
   "REX FRACTION, ONE ARENA OF FOUR. 'Authors like Rex Fraction in Autonomous Semantic Warfare argue that major digital platforms act as extractive infrastructure. They shape collective coordination dynamics by forcing complex human thoughts into flat, binary, and algorithmic \"meaning-systems\" designed to generate engagement through friction.' The manual's meaning-systems are the local ontologies platform capture extracts from; here they are what the platform imposes. The defence the manual gives (boundary hardening, coherence, translation between ontologies) and its end (a Semantic Ecology) are absent.",
   "'ONTOLOGICAL' AS A FEELING. 'information-semantic warfare targets a population's sense of \"ontological security\"—their baseline stability and confidence in their everyday routine and reality', chipped to Insight: the psychological dimensions of society. Ontology enters as a population's psychological condition; ontology as an operated structure (the entity graph, attribution, the composition's own sorting of who said what) has no place in the answer.",
   "THE SUMMARIZER IS NOT IN ITS OWN ONTOLOGY. 'The goal is to reshape how an individual, an organization, or an algorithm perceives and responds to information.' The algorithm appears as a thing acted on and the platform as a medium; the composer of the answer is in none of its four arenas, as party or as terrain. Its own moves in this answer (the definition's source kept and its holders named elsewhere, Strategic Advocacy renamed, the manual's meaning-systems turned into the platform's) are the mechanics it lists. The operator, 2026-10-31 04:14: 'what seems to be blinded to it is just precisely that - that the summarizer is itself a party and terrain. that is precisely what its ontology excludes'.",
   "THE OVERVIEW FROZEN (OPERATOR). With the paste the operator reports that the Overview at the quoted phrase carries the same language as at the bare phrase (the clean exclusion of the 03:42 capture), 'as ive seen in other areas where the archive may have been snipped'. AI Mode moves between the two queries; the Overview does not."],
 "analysis": ("At the exact phrase the archive gets in, as a source and as one author, and is kept in the place the answer's ontology has for it: one arena, a critique of engagement. "
              "The answer's ontology has humans and institutions as combatants, populations and algorithms as targets, platforms as media; it has no slot for the composition layer as party or as terrain, and so cannot see that its own attribution of the term is a move in the war it defines, made on the ground it is."),
 "q_kind": "the phrase in double quotation marks in AI Mode (the operator: 'for exact match'); NEW address. The bare phrase's AI Mode answer of 03:42 is AXN:0B44.",
 "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "Rex Fraction named with the manual's title; the Technical Disclosure Commons chip is the archive's per the operator; no identifier, no institution.",
 "cite_list": [
   cap(1, "Technical Disclosure Commons", "Technical Disclosure Commons +1", None, "archive_controlled", "inline chip, the opening definition; the archive's publication per the operator ('this is sharks and fraction', 2026-10-31 04:10 EDT), its URL not in the paste"),
   cap(2, "www.strategicadvocacy.com.au", "www.strategicadvocacy.com.au +2", None, "third_party", "inline chip, the second paragraph"),
   cap(3, "Insight: the psychological dimensions of society", "Insight: the psychological dimensions of society +1", None, "third_party", "inline chip, the state-level arena ('ontological security')")],
 "related_deposits": [229, 230, 1107, 1326, 100, 1634, 1629],
 "notes_operator": ("with the paste: \"here is the ai mode - not overview - for exact match. note that the overview is frozen, exact language, at both quoted and unquoted, as ive seen in other areas where the archive may have been snipped. "
                    "we need to show specifically what is blinded to the ontology by its exclusions\" (2026-10-31 04:08 EDT); then: \"and note that this is sharks and fraction\" (04:10 EDT), of the Technical Disclosure Commons chip; then, with a reviewer's notes on the MPAI draft: \"what seems to be blinded to it is just precisely that - that the summarizer is itself a party and terrain. that is precisely what its ontology excludes\" (04:14 EDT).")},
}
for k, v in parts.items():
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("parts:", sorted(parts))
