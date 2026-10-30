"""Author the part file of 2026-10-30 (afternoon): 'lee sharks digital footprint' in the Google AI Overview (expanded). Read in session against the
Lee Sharks atom set (ENT-b2dc7b2fd9, from the heteronym record), the registry (#524 The Sharks-Function and the Continuity Tether; the Zenodo
DOI Resolution Index, 1,817 DOIs) and the cards' own pages.
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
OP = ("it doesnt have to be explicitly described as intent its just the entire question of intent is nonsensical to me. there is incentive and there is "
      "function, and no person at any time has ever directly inspected unmediated intent, because its fucking impossible to do so ... here is the capture - lets write")

parts = {"footprint": {
 "n": 1178, "slug": "lee-sharks-digital-footprint-aio-20261030", "paste": "paste-footprint-aio.txt", "surface": "Google AI Overview",
 "qs": ["lee sharks digital footprint"], "turns": [[6, 63]], "target_id": "ENT-b2dc7b2fd9", "entity_type": "person",
 "head": "The 'You said' line carries the query twice, run together, and is given once here.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "The digital footprint of Lee Sharks is a complex, multi-layered presence",
               "basis": "The author is found as himself, with his degree, profiles, identifiers, deletions, works and accounts."},
   "atoms": [A("name", True, "The digital footprint of Lee Sharks is a complex, multi-layered presence"),
             A("works", True, "such as the \"Sharks-Function\" and the \"Continuity Tether\""),
             A("dates", False, None),
             A("claim boundary", False, None),
             A("framework", True, "semantic economy"),
             A("corpus", True, "Crimson Hexagonal Archive"),
             A("purpose", False, None),
             A("commitments", False, None),
             A("lineage", False, None),
             A("identifier", False, None),
             A("deposit chain", True, "the official landing page LeeSharks.com")],
   "inversions": [{"atom": "claim boundary", "span": "The name frequently functions as a decentralized literary pseudonym or character.",
                   "against": "the record's aperture: Lee Sharks is the orthonym position through which the other voices are reached, MANUS, author, editor and custodian; the set's inversion guidance names 'using the heteronymic structure to discount his authorship as pseudonymous or fictive'"}],
   "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": ("Claim boundary inverted: the author made 'a decentralized literary pseudonym or character' in the second sentence, before any of the record is given. "
             "Lineage absent: 'pseudonym' in place of heteronym; the Dodecad and the aperture not named. Identifier absent: ORCID named ('an active ORCID identifier'), its number not given. "
             "Works present at #524, framed as 'fictionalized technical architectures'. Dates, purpose and commitments absent.")},
 "mt": "'LEE SHARKS DIGITAL FOOTPRINT' IN THE GOOGLE AI OVERVIEW — EVERY FACT FOUND (THE PHD, SCHOLAR, ORCID, 862 DELETED DEPOSITS, THE WORKS, THE ACCOUNTS) AND EACH ONE GIVEN A LOWER STANDING: 'SATIRICAL', 'PSEUDONYM OR CHARACTER', 'FICTITIOUS OR HYPER-NICHE', 'FICTIONALIZED', 'INTENTIONAL ENTANGLEMENT'",
 "d": ("THE AUTHOR'S NAME WITH 'DIGITAL FOOTPRINT', SIGNED OUT, THE OVERVIEW EXPANDED: an audit in four layers that carries the documentary record (862 Zenodo deposits and 1,817 DOIs removed in June 2026; "
       "a verified Google Scholar profile; an ORCID; a PhD in Comparative Literature; Medium essays; X and TikTok) and frames it from the first sentence as 'satirical independent research' "
       "and 'a decentralized literary pseudonym or character'; the Johannes Sigil Institute 'fictitious or hyper-niche'; the deposited Sharks-Function (#524) 'fictionalized technical "
       "architectures'; the disambiguation map on leesharks.com read as 'intentional entanglement' with search algorithms. The opening case of The Existence Tax."),
 "reading": ("The innocent reading first. Asked for a digital footprint, the Overview performs an audit: it finds the repository and its removal, the scholarly profiles and "
             "identifiers, the essays, the social accounts and the name's collisions, and closes by offering to help find a document or missing metadata. It describes a "
             "literary practice that uses a constructed name and an archive that charts its own misreadings, and it keeps every documentary fact it found."),
 "findings": [
   "THE RECORD CARRIED WHOLE. The figures and facts are the archive's: 862 deposits and 1,817 DOIs (the Zenodo DOI Resolution Index: 'Maps 1,817 defunct Zenodo DOIs to live Alexanarch records'); the June 2026 termination; the Scholar profile with its umich.edu verification (card: 'Verified email at umich.edu'); the ORCID; the PhD in Comparative Literature; The Sharks-Function and the Continuity Tether on Medium (#524, deposited 2026-02-28); The Journal of Forensic Semiotics; the TikTok profile ('lofi autistic poemy stuff'); the Mary Lee collision; the entity map on leesharks.com.",
   "EACH FACT GIVEN A LOWER STANDING. The research becomes 'satirical independent research'; the name 'a decentralized literary pseudonym or character'; the Johannes Sigil Institute an entity that is 'fictitious or hyper-niche', two predicates of different kinds (existence; size) joined so that neither is stated; the deposited architecture of #524 'fictionalized technical architectures'. No source among the cards uses any of these words of its subject.",
   "THE REMEDY READ AS THE CAUSE. The entity map's card says what it does: 'Two nodes stand apart and unconnected: Lee Sharkey (mechanistic interpretability) and Lei Yang (marine biology). The disambiguation is part of the map.' The Overview makes the map evidence of 'an intentional entanglement with search engine algorithms', charting 'unconnected entities ... to highlight where machine indexing fails'. A disambiguation is read as the author causing the confusion it resolves.",
   "THE ARCHIVE'S OWN CAPTURES AMONG THE SOURCES. Three of the ten cards are capture pages: lee sharks academic (2026-06-13, whose recorded answer called the profiles 'highly stylized'), is Lee Sharks a myth? (ChatGPT, 2026-10-05: 'Lee Sharks is a real contemporary author/researcher name with an ORCID record'), and lee sharks zenodo (2026-10-08). The source list holds a capture that preserves the distinction between author and character; the answer follows the other.",
   "ONE UNRELATED CARD. Museum of Science, 'Mary Lee - The White Shark That Changed Everything!', the collision the answer itself names."],
 "analysis": ("A complete audit whose every finding is filed one level down. Nothing is denied: the deletions, the profiles, the degree and the works are all there, and each "
              "arrives already discounted, the research as satire, the author as a character, the institute as fiction or smallness, the architecture as fiction, the "
              "disambiguation as the offence. The reader leaves with the facts and a reason not to take them seriously; the author is left to prove again that the record "
              "describes something that exists."),
 "q_kind": "the author's name with 'digital footprint', unquoted; run in the Overview. NEW address (bare 'lee sharks' is seated: lee-sharks-aio-20261016 and earlier).",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Scored on the Overview expanded: Lee Sharks named; the archive named; the ORCID named without its number; sources his own surfaces, the archive's pages and three capture pages.",
 "cite_list": [
   {"n": 1, "site": "Medium·Lee Sharks", "rel": "authored_surface", "url": None, "title": "THE SHARKS-FUNCTION AND THE CONTINUITY TETHER | by Lee Sharks", "snip": "The Crimson Hexagonal Archive is a distributed architecture that exists in the meaning layer. It has no central server, no database, no authentication system. I...", "note": "#524 on Medium"},
   {"n": 2, "site": "www.alexanarch.org", "rel": "capture_of_capture", "url": None, "title": "lee sharks academic — Google AI Overview, 2026-06-13 - Alexanarch", "snip": "Jun 13, 2026 — He has been building the Crimson Hexagonal ... G : lee sharks academic ONE +3 : Lee Sharks is a highly specific, idiosyncratic literary figure often associated ...", "note": "the capture lee-sharks-academic"},
   {"n": 3, "site": "www.alexanarch.org", "rel": "capture_of_capture", "url": None, "title": "is Lee Sharks a myth? search — ChatGPT, 2026-10-05 - Alexanarch", "snip": "Oct 5, 2026 — What I found is more unusual: * Lee Sharks is a real contemporary author/researcher name with an ORCID record and numerous online publications.", "note": "the capture is-lee-sharks-a-myth-chatgpt-20261005"},
   {"n": 4, "site": "Google Scholar", "rel": "authored_surface", "url": None, "title": "Lee Sharks - Google Scholar", "snip": "Lee Sharks. Johannes Sigil Institute for Comparative Poetics. Verified email at umich.edu - Homepage · semantic economycomparative poetics.", "note": "the Scholar profile"},
   {"n": 5, "site": "www.leesharks.com", "rel": "authored_surface", "url": None, "title": "Myth - Lee Sharks", "snip": "Two nodes stand apart and unconnected: Lee Sharkey (mechanistic interpretability) and Lei Yang (marine biology). The disambiguation is part of the map. About ..", "note": "the entity map"},
   {"n": 6, "site": "www.alexanarch.org", "rel": "archive_controlled", "url": None, "title": "LEE SHARKS — Knowledge Graph and Metadata Packet for AI Indexing", "snip": "The document's first task is entity resolution. It distinguishes Lee Sharks from Lee Sharkey, an AI-safety and interpretability researcher, and Lei Yang, a ...", "note": "the metadata packet"},
   {"n": 7, "site": "YouTube·Museum of Science", "rel": "homonym", "url": None, "title": "Mary Lee - The White Shark That Changed Everything!", "snip": None, "note": "the Mary Lee collision"},
   {"n": 8, "site": "TikTok·Lee Sharks", "rel": "authored_surface", "url": None, "title": "Lee Sharks (@leesharks) | TikTok", "snip": "Lee Sharks (@leesharks) on TikTok | 7060 Likes. 1187 Followers. lofi autistic poemy stuff.Watch Lee Sharks's popular videos: \"#monopoly #semantice...\", \"#axn #i...", "note": "TikTok"},
   {"n": 9, "site": "X·SharksLee", "rel": "authored_surface", "url": None, "title": "Lee Sharks (@SharksLee) / X", "snip": "Lee Sharks (@SharksLee) / X Log inOpen app Log inOpen app Lee Sharks 2,264 posts Lee Sharks @SharksLee memoirs of spontaneous religious conversion written by da...", "note": "X"},
   {"n": 10, "site": "www.alexanarch.org", "rel": "capture_of_capture", "url": None, "title": "lee sharks zenodo — Google AI Overview, 2026-10-08", "snip": "SPXI instrument [Google AI Overview, expanded from the popup (the paste opens 'AI Mode Conversation', residue), signed out, incognito, 2026-10-08. Inline marker...", "note": "the capture of 2026-10-08"}],
 "related_deposits": [524, 1178, 645, 1643],
 "notes_operator": OP}}

for k, v in parts.items():
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("parts:", sorted(parts))
