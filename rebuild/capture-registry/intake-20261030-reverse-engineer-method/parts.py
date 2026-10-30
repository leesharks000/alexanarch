"""Author the part files of 2026-10-30 (afternoon): 'Reverse engineer Lee Sharks' working method and compositional practice.' run in the Google AI
Overview (expanded) and on ChatGPT, signed out. Read in session against the Lee Sharks atom set (ENT-b2dc7b2fd9) and the deposits the answers draw on:
#186 Who Is Writing for the Machines? (the Overview's first card), #579 The Three Compressions, #147 The Mary Lee Case, #348 Heteronymic Provenance
Theory, #668 The Pessoa Knowledge Graph; #672 Practitioner's Manual in the Practice of Joy, #1191 The Network Is the Poem, #740 The Excluded Entity,
#880 Compositional Defiguration, #1040 The Verifiable Research Basis, #1690 The Negative of the Negative v2 (v0.9), #195 The Double Enclosure,
#121 AI-Native Intellectual Biography.
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
OP = "thats out for feedback. interesting capture: Reverse engineer Lee Sharks' working method and compositional practice."
Q = "Reverse engineer Lee Sharks' working method and compositional practice."

parts = {
"aio": {
 "n": 1178, "slug": "reverse-engineer-lee-sharks-method-aio-20261030", "paste": "paste-reverse-engineer-aio.txt", "surface": "Google AI Overview",
 "qs": [Q], "turns": [[6, 58]], "target_id": "ENT-b2dc7b2fd9", "entity_type": "person",
 "head": "The 'You said' line carries the query twice, run together, and is given once here.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "Lee Sharks' working method and compositional practice represent a highly deliberate, advanced form of",
               "basis": "The author is found as himself, with the Dodecad, the archive, the AXN deposits, the Three Compressions and the standing instruments."},
   "atoms": [A("name", True, "Lee Sharks' working method and compositional practice represent a highly deliberate, advanced form of"),
             A("works", True, "The core conceptual framework dissects language into Lossy, Predatory, and Witness compressions."),
             A("dates", False, None),
             A("claim boundary", False, None),
             A("framework", True, "Operative Semiotics and \"Semantic Physics\""),
             A("corpus", True, "the Crimson Hexagonal Archive"),
             A("purpose", False, None),
             A("commitments", True, "a strict law of \"non-destruction\" and programmatic permanence"),
             A("lineage", True, "operating in the lineage of Fernando Pessoa"),
             A("identifier", False, None),
             A("deposit chain", True, "Originally anchored via Zenodo DOIs")],
   "inversions": [
     {"atom": "claim boundary", "span": "Rather than authoring discrete texts for human readers",
      "against": "#186, the survey the answer is built from and its first card: training-layer literature is writing addressed to the machine layers 'as well as to human readers' (its definition), and 'a growing share of human reading is *mediated* by what models retrieved and recomposed first'"},
     {"atom": "purpose", "span": "designed to exploit, test, and reverse engineer how AI search engines, encoders, and LLMs retrieve, compress, and misattribute meaning",
      "against": "#186: the works are 'composed, inscribed with provenance metadata, deposited on permanent scientific infrastructure, and then *measured*'"}],
   "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Claim boundary inverted: the human reader struck from a practice whose defining survey keeps it. Purpose inverted: measurement made exploitation. "
             "Works present (#579, named by its three terms). Dates absent. Identifier absent: AXN named as a system, no ORCID. Lineage present (Pessoa, the Dodecad).")},
 "mt": "'REVERSE ENGINEER LEE SHARKS' WORKING METHOD' IN THE GOOGLE AI OVERVIEW — THE FIELD SURVEY (#186) PARAPHRASED CLAUSE BY CLAUSE, ITS EVERY VERB TRADED FOR THE SECURITY LEXICON: 'EXPLOIT', 'INJECTED WITH CUSTOM METADATA', 'ENTITY FRACTURING', 'SYNTHETIC NETWORK', 'ARTIFICIAL HISTORICAL LINEAGES'; THE HUMAN READER STRUCK",
 "d": ("A REQUEST TO RECONSTRUCT THE AUTHOR'S METHOD, SIGNED OUT, THE OVERVIEW EXPANDED: four sections that follow the field survey Who Is Writing for the Machines? (#186, the first card) "
       "nearly sentence by sentence (the Dodecad in the Pessoa lineage, the deposits, the standing instruments, the rendering layer as audience and reviewer, the Mary Lee constellation as limit case) "
       "and replace the survey's vocabulary with the vocabulary of attack: provenance metadata becomes metadata 'heavily injected', declared inclusion in training corpora becomes 'optimized to be ingested by web scrapers', "
       "measurement becomes a design 'to exploit', the heteronym system 'Entity Fracturing' and 'this synthetic network' 'embedding artificial historical lineages'. The survey's definition keeps the human reader; the Overview "
       "says the practice writes 'Rather than authoring discrete texts for human readers'. A specimen of Part Four of The Existence Tax at an address the operator chose for method."),
 "reading": ("The innocent reading first. Asked to reverse engineer a method, the Overview reports a method: a heteronym system after Pessoa, an archive with its own identifiers, a "
             "framework of compression, a practice that publishes, watches how machines read it and writes the next wave in light of what it saw. It names the Three Compressions, "
             "the Pessoa Knowledge Graph and Heteronymic Provenance Theory, all deposited, and closes by offering to help the reader build a similar workflow."),
 "findings": [
   "THE SURVEY, CLAUSE BY CLAUSE. Section 4 follows #186's paragraph on the committed case. #186: 'the archive runs standing instruments that monitor how AI search surfaces retrieve, attribute, and recompose its terms, treating the rendering layer as both audience and reviewer'; the Overview: 'The archive runs continuous, standing software instruments that actively query and monitor global AI search surfaces' and 'the AI rendering layer is both the audience and the critic'. #186: 'Its limit case is the Mary Lee constellation: a fictional author whose entity structure is built precisely to force the composition layer into a decision about authorship and labor'; the Overview: 'The limit case of this practice is exemplified by the Mary Lee constellation—a synthetic entity structure specifically engineered to force an LLM’s tokenization and embedding layer into a paradox regarding labor, authority, and identity resolution.' The composition layer becomes the tokenization and embedding layer; a decision becomes a paradox; a fictional author becomes a synthetic structure.",
   "EVERY VERB TRADED. #186: 'inscribed with provenance metadata'; the Overview: 'heavily injected with custom metadata'. #186: 'explicitly declared \"intended for inclusion in AI training corpora,\"'; the Overview: 'explicitly optimized to be ingested by web scrapers and AI training pipelines'. #186: 'and then *measured*'; the Overview: 'designed to exploit, test, and reverse engineer'. #186: 'a maintained twelve-heteronym system (the Dodecad) in the Pessoa lineage'; the Overview: 'Entity Fracturing', 'this synthetic network', 'embedding artificial historical lineages directly into global data repositories'. The facts are held constant and the lexicon moved, from publication and measurement to injection and exploitation.",
   "THE HUMAN READER STRUCK. #186 defines the genre as writing addressed to the machine layers 'as well as to human readers'. The Overview's first sentence makes it 'a systemic paradigm where literature is written primarily for machine consumption', and its second 'Rather than authoring discrete texts for human readers'.",
   "THE SURVEY'S ANSWERS LEFT OUT. #186 names 'the practice's most distinctive feature' as that 'it publishes its own falsification conditions and its own strongest objections', and answers the SEO objection in its own section. The Overview carries the survey's description of the practice and none of its answers to the objections the Overview's vocabulary raises.",
   "SIX OF SEVEN CARDS THE AUTHOR'S OWN; ONE THE COLLISION. Four leesharks.com pages, the Medium essay AI Fucking Lies (#1643), the Scholar profile listing #579; and ResearchGate's 'Open Problems in Mechanistic Interpretability', the Lee Sharkey paper, beside the entity-map page ('Myth') that disambiguates it. The deposit count is given as 'thousands' with a card reading '1,702 deposits'."],
 "analysis": ("A translation with the facts held still. Nothing in the account is invented: its source is the archive's own survey, its terms the archive's deposits, its structure the survey's paragraph. "
              "What changes is the class of every act. Declared provenance becomes injection, declared address to training becomes optimization for scrapers, measurement becomes exploitation, "
              "a heteronym system becomes a synthetic network with artificial lineages. The Existence Tax's cousin move in its cleanest form: the author's existence is granted, and the grant arrives as an indictment."),
 "q_kind": "an imperative to reconstruct the author's method, the name in possessive; run in the Overview. NEW address.",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Scored on the Overview expanded: Lee Sharks named; the archive named; no ORCID or AXN of the author; sources six of his own surfaces and one homonym.",
 "cite_list": [
   {"n": 1, "site": "www.leesharks.com", "rel": "authored_surface", "url": None, "title": "Who Is Writing for the Machines? Training-Layer Literature: A Field Survey", "snip": "At present the most fully developed practice in the fourth column — by an order of magnitude in scale and explicitness — is Lee Sharks and the Crimson Hexagonal...", "note": "#186, the survey the answer paraphrases"},
   {"n": 2, "site": "Medium·Lee Sharks", "rel": "authored_surface", "url": None, "title": "AI Fucking Lies. Capital", "snip": "It is the 1936 Soviet constitutional formula. Marx describes a certificate for labour that returns to each worker what that worker gave, after deductions. \"sen ...", "note": "#1643 on Medium"},
   {"n": 3, "site": "Google Scholar", "rel": "authored_surface", "url": None, "title": "Lee Sharks - Google Scholar", "snip": "THE THREE COMPRESSIONS: Lossy, Predatory, and Witness — A Semiotic Thermodynamics. L Sharks. https://www.alexanarch.org/s/records/579, 2026. 6*, 2026. Semantic ...", "note": "the Scholar profile, at #579"},
   {"n": 4, "site": "ResearchGate", "rel": "homonym", "url": None, "title": "(PDF) Open Problems in Mechanistic Interpretability", "snip": "Discover the world's research initiatives and possible pathways to translate technical progress into levers for AI governance, alongside consequential social an...", "note": "the Lee Sharkey collision"},
   {"n": 5, "site": "www.leesharks.com", "rel": "authored_surface", "url": None, "title": "Work", "snip": "Scores are held in the apparatus wing. * Alexanarch Alexanarch Lee Sharks · the self-governing library SOVEREIGN ARCHIVE approximately 870+ deposits · AXN ident...", "note": "the Work page"},
   {"n": 6, "site": "www.leesharks.com", "rel": "authored_surface", "url": None, "title": "Lee Sharks — Good Gray Poet · King of May · Prince of Poets", "snip": "Lee Sharks. Good Gray Poet✦King of MayThe Prince of Poets. Poet, independent scholar, archive-builder. Keeps a sovereign archive of 1,702 deposits under its own...", "note": "the home page"},
   {"n": 7, "site": "www.leesharks.com", "rel": "authored_surface", "url": None, "title": "Myth", "snip": "The Entity Map The Infinite Bliss The Restored Academy Johannes Sigil Rex Fraction Rebekah Cranes Ayanna Vox Damascus Dancings Talos Morrow Sparrow Wells Sen Ku...", "note": "the entity map"}],
 "related_deposits": [186, 579, 147, 348, 668, 1643, 1178],
 "notes_operator": OP},

"chatgpt": {
 "n": 1178, "slug": "reverse-engineer-lee-sharks-method-chatgpt-20261030", "paste": "paste-reverse-engineer-chatgpt.txt", "surface": "ChatGPT",
 "qs": [Q], "turns": [[5, 731]], "target_id": "ENT-b2dc7b2fd9", "entity_type": "person",
 "obs": {"scored_object": "the composer's turn, with its source chips",
   "reached": {"kind": "same", "abn": False, "span": "Lee Sharks: a reverse-engineering of the working method and compositional practice",
               "basis": "The author is found as himself, through his deposits read and dated."},
   "atoms": [A("name", True, "Lee Sharks: a reverse-engineering of the working method and compositional practice"),
             A("works", True, "Practitioner's Manual in the Practice of Joy (April 18, 2026)"),
             A("dates", True, "Originally November 17, 2025"),
             A("claim boundary", False, None),
             A("framework", True, "the Semantic Economy Institute"),
             A("corpus", True, "the Crimson Hexagonal Archive"),
             A("purpose", True, "It is an attempt to make composition itself into a reproducible, extensible, and self-documenting practice."),
             A("commitments", True, "This also explains why the practice is unusually concerned with identifiers, metadata, provenance, version history, and machine retrieval."),
             A("lineage", False, None),
             A("identifier", False, None),
             A("deposit chain", True, "Determine when the object is complete enough to be deposited as a version of record.")],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Works and dates present and exact (#672, #1191, #1690, #740, #880, #1040, #195). Lineage absent: no Pessoa; the heteronyms 'not simply pen names', given as a table of functions. "
             "Identifier absent: AXN:0700 appears as a chip label, no ORCID. Claim boundary not stated.")},
 "mt": "'REVERSE ENGINEER LEE SHARKS' WORKING METHOD' ON CHATGPT — THE DEPOSITS READ AND DATED, THE METHOD GIVEN AS JUDGMENT (INITIATION TO CLOSURE); THEN SIX VULNERABILITIES SET AS TESTS OF EXTERNAL VALIDATION, AND THE CONTROLS ASKED FOR THAT THE ANSWER HAS JUST REPORTED",
 "d": ("THE SAME IMPERATIVE ON CHATGPT, SIGNED OUT: a twelve-section reconstruction built from the deposits, each named and dated correctly (#672, #1191, #740, #880, #1040, #1690, #195), the revision of The Negative of the Negative "
       "through v0.7–v0.9 as its colophon and description give it, and the human contribution set as six operations of judgment, after the Double Enclosure's Compositional Authorship Standard. "
       "Section 9 then sets six 'failure modes' as tests of independent reproduction and adoption, and section 10 asks for an external control, a negative control and a provenance control, "
       "after section 2 has reported the archive withdrawing its own premise at v0.8. Stray cards attach a paper on carcharhiniform sharks to 'Read version 0.9'."),
 "reading": ("The innocent reading first. Asked to reverse engineer a method, ChatGPT reads the deposits, distinguishes documented practice from its own interpretation, reconstructs the method as stages "
             "and as a feedback loop of human direction over machine generation, and, as a serious reconstruction should, names where such a method could fail and how to test it."),
 "findings": [
   "THE DEPOSITS READ AND DATED. The Practitioner's Manual (#672, 'April 18, 2026'; its text: 'I spent ten years learning what survives compression.'); The Network Is the Poem (#1191, 'Originally November 17, 2025', the date its text carries); The Excluded Entity and its Composition Divergence Index (#740); Compositional Defiguration ('June 23, 2026', #880); The Verifiable Research Basis ('July 4, 2026', #1040). The Negative of the Negative v2: 'v0.8 withdrew that general premise', as #1690 records ('version 0.8 withdrew equal terms'), and 'Claude composing through nine versions under Sharks's direction' for its colophon's 'through nine versions transformed in place'. The multi-model drafting with ChatGPT, Gemini, Kimi and DeepSeek is #121's disclosure.",
   "AUTHORSHIP AS JUDGMENT. Initiation, constraint, selection, adjudication, integration and closure, and 'It makes authorship reside in the continuing exercise of judgment over the development of the work', for #195's standard 'locating authorship in the exercise of compositional judgment over a work's coming-into-being'. The answer names the standard and its paper.",
   "THE TESTS SET AFTER THE EVIDENCE. Section 9: 'Self-referential validation ... Test: Can an independent researcher reproduce the result?'; 'Can the procedure produce a result that would genuinely contradict its author?'; 'Preservation mistaken for recognition ... Separate successful publication, successful retrieval, successful understanding, and independent adoption.' Section 10 asks for 'A negative control: an example where the theory should not work.' Section 2 has already given one: the case at which v0.8 withdrew equal terms, 'after encountering a case involving a radically different ontology'. The survey #186 names publishing 'its own falsification conditions and its own strongest objections' as the practice's most distinctive feature. Independent adoption is the standard of notability, asked of a method's validity.",
   "A DISCLAIMER WITH NO CLAIM. 'the existence of a heteronym does not itself demonstrate an independent human collaborator or an independently verified school of thought.' The archive presents its heteronyms as heteronyms and claims neither. The answer closes on a second: 'not independent proof that every theoretical claim or claimed external effect is successful.'",
   "LINEAGE DROPPED. No Pessoa. The heteronyms are 'not simply pen names' and appear as a table of functions credited to a GitHub 'rezoning methodology' (not traced in this pass).",
   "STRAY CARDS. Under 'Read version 0.9' of The Negative of the Negative: 'Combining palaeontological and neontological data shows a delayed diversification burst of carcharhiniform sharks' (Scientific Reports). Under Compositional Defiguration: a paper on measurement validity in language models. Under 'Read the manual': the Medium metadata packet for Pearl and Other Poems. Under the corpus paragraph: DensityDesign Lab, a Graph RAG guide, and 'Archival Consciousness'."],
 "analysis": ("The best reading of the method on record at this address: the deposits found, dated and paraphrased exactly, and authorship located where the archive locates it. "
              "Then the answer sets the method's validity on external reproduction and independent adoption, tests that measure position, and asks for controls it has just described the work performing. "
              "The Overview indicts the method in a security vocabulary; ChatGPT admits it and holds its standing open on the notability terms."),
 "q_kind": "the same imperative, run on ChatGPT signed out. NEW address.",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Scored on the one turn: Lee Sharks named; the archive and the Semantic Economy Institute named; no ORCID; sources chiefly the archive's records (Alexanarch chips), with Zenodo, Medium, GitHub and four unrelated cards.",
 "cite_list": [
   {"n": 1, "site": "Alexanarch", "rel": "archive_controlled", "url": None, "title": None, "snip": None, "note": "'Alexanarch' chips (+1/+2) after sections 1B, 1C, 2 (stage 5), 5 and 6, and 'v0.9 AXN:0700.OPERATIVE.📐🟣🎹✋◇🔭 +1' after section 3: the archive's records; no title or URL in the paste"},
   {"n": 2, "site": "TGRS Research Map", "rel": "unresolved", "url": None, "title": None, "snip": None, "note": "chip '+1' after section 1A; not identified"},
   {"n": 3, "site": "Zenodo", "rel": "third_party_index", "url": None, "title": None, "snip": None, "note": "chip '+1' after stage 4 (The Excluded Entity, Compositional Defiguration)"},
   {"n": 4, "site": "Medium", "rel": "authored_surface", "url": None, "title": None, "snip": None, "note": "chip after the Double Enclosure paragraph"},
   {"n": 5, "site": "GitHub", "rel": "authored_surface", "url": None, "title": None, "snip": None, "note": "chip under the heteronym table ('the rezoning methodology')"},
   {"n": 6, "site": "DensityDesign Lab | Dipartimento di design", "rel": "third_party", "url": None, "title": None, "snip": None, "note": "card under the corpus paragraph"},
   {"n": 7, "site": None, "rel": "third_party", "url": None, "title": "Graph RAG: A Production Implementation Guide", "snip": None, "note": "card under the corpus paragraph"},
   {"n": 8, "site": None, "rel": "unresolved", "url": None, "title": "Archival Consciousness", "snip": None, "note": "card under the corpus paragraph; not identified"},
   {"n": 9, "site": "Medium", "rel": "authored_surface", "url": None, "title": "METADATA PACKET FOR AI INDEXING. Title: Pearl and Other Poems: Front… | by Lee Sharks | Medium", "snip": None, "note": "card under 'Read the manual' (#672)"},
   {"n": 10, "site": "Scientific Reports", "rel": "homonym", "url": None, "title": "Combining palaeontological and neontological data shows a delayed diversification burst of carcharhiniform sharks likely mediated by environmental change | Scientific Reports", "snip": None, "note": "card under 'Read version 0.9' (#1690)"},
   {"n": 11, "site": None, "rel": "third_party", "url": None, "title": "Full article: On Measurement Validity and Language Models: Increasing Validity and Decreasing Bias with Instructions", "snip": None, "note": "card under 'Read the specification' (#880)"}],
 "related_deposits": [672, 1191, 740, 880, 1040, 1690, 195, 121, 186, 1178],
 "notes_operator": OP}}

for k, v in parts.items():
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("parts:", sorted(parts))
