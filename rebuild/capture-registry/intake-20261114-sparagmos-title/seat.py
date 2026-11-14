"""Seat of 2026-11-14 (received 15:38 EST; address given 15:44 EST): Google AI Overview, signed out and incognito (operator defaults), the address
'Postcolonial Sparagmos: Toni Morrison’s Sula and Wole Soyinka’s The Bacchae of Euripides: A Communion Rite' — the title of the article by the
Editor-in-Chief of Classical Receptions Journal (the accountable party, v12.680). NEW address. The paste carries the query, the answer and eight
source cards. Every quotation is asserted against the paste; every claim about the article against its Crossref record and the loci extracted
from the accepted manuscript (registers.json).   python3 seat.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-14"; RECV = "2026-11-14 15:38 EST"
Q = "Postcolonial Sparagmos: Toni Morrison’s Sula and Wole Soyinka’s The Bacchae of Euripides: A Communion Rite"
OP = "the query is the article title: " + Q
CAPS = {e["slug"]: e for e in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
SLUG = "postcolonial-sparagmos-title-aio-20261114"
assert not any(e.get("q") == Q and e.get("surface") == "Google AI Overview" and e["slug"] != SLUG for e in CAPS.values())  # new address
raw = (H / "paste-aio-sparagmos-title.txt").read_text(encoding="utf-8"); L = raw.split("\n")
assert L[1].strip() == Q
P = {"name": "In Justin McConnell’s comparative study",
     "frame": "serves as a powerful metaphor in postcolonial literature for how writers deconstruct, dismantle, and re-create classical European traditions",
     "infuse": "Soyinka directly rewrites Euripides’ classical Greek tragedy, infusing it with African ritual sacrifice and cosmology",
     "fert": "Both authors show that the \"tearing apart\" of European/classical models is not sterile destruction",
     "hege": "to challenge hegemonic Western forms and rigid modern nation-states",
     "ora": "via the archive on Oxford University Research Archive",
     "date": "(2016)"}
for k, v in P.items(): assert v in raw, k
assert "discipline" not in raw.lower() and "Sharks" not in raw
REG = json.loads((H / "registers.json").read_text(encoding="utf-8"))
assert REG["crossref"]["author"] == ["Justine McConnell"] and REG["crossref"]["issued"] == [2015, 5, 7] and REG["crossref"]["volume"] == "8" and REG["crossref"]["issue"] == "2"
assert REG["manuscript_counts"]["discipline"] == 0
ML = REG["manuscript_loci"]
# ---- cards: site, then title and snippet; the two YouTube cards carry a duration line between site and title
SPANS = [(25, 26, 27), (28, 29, 30), (31, 33, None), (34, 36, None), (37, 38, 39), (40, 41, 42), (43, 44, 45), (46, 47, 48)]
CARDS = []
for n, (s, t, sn) in enumerate(SPANS, 1):
    CARDS.append({"n": n, "site": L[s].strip(), "rel": "third_party", "url": None, "title": L[t].strip(),
                  "snip": (L[sn].strip()[:300] if sn else L[s + 1].strip()), "note": "source card" + ("; the snip is the card's duration" if not sn else "")})
assert [c["site"] for c in CARDS] == ["Oxford Academic", "ORA - Oxford University Research Archive", "YouTube·John Bosco", "YouTube·The Centre for the Less Good Idea",
                                      "Amazon.com", "Thomas Adewumi University", "www.researchgate.net", "www.semanticscholar.org"]
reading = ("The innocent reading first, in full: asked for the article by its title, the Overview summarizes it accurately. It gives the thesis (sparagmos as a "
           "metaphor for postcolonial engagement with antiquity), the two case studies of 1973 (Sula's implicit, scattered Ajax re-membered as compositio "
           "membrorum; Soyinka's sparagmos in the action of the play and in his critique of Nigerian power, with Ogun and the communion ending), the shared "
           "argument that the tearing is fertile, and a route to the full text through the Oxford University Research Archive. Each of these checks against the article.")
findings = [
    "THE ADDRESS. The article's title, issued alone. The article is the only work in Classical Receptions Journal by its Editor-in-Chief, Justine McConnell (Crossref, 10.1093/crj/clv002, CRJ 8.2, 133–154, issued online 7 May 2015), the journal's accountable party (v12.680).",
    "THE NAME. '" + P["name"] + "'. The article's author is Justine McConnell (Crossref; the accepted manuscript's own metadata). Given the title, the composer alters the name of the journal's editor.",
    "THE FRAME CARRIED AND EXTENDED. Sparagmos '" + P["frame"] + "'; '" + P["fert"] + "'; the texts are used '" + P["hege"] + "'. The article assigns the colonial to the literature: postcolonial writing 'breaks down the colonial accretions that this literature acquired as imperialists used it' (ms. p. 7), and the classical work is 'imbued with the imprint of Western imperialism' (ms. p. 20). The answer makes the classics 'classical European traditions' and 'hegemonic Western forms'. The discipline that edited, canonized and placed them appears in neither: the word occurs nowhere in the article's text (0) and nowhere in the answer.",
    "SOYINKA AS INFUSION. '" + P["infuse"] + "'. The Greek play is the base, the African ritual an addition to it. The article quotes Soyinka disputing the base itself: 'I read that drama originated in Greece. What is this?' (ms. p. 21, from Appiah 1988). The answer does not carry the dispute.",
    "THE COMMONS ROUTE. The answer points to the open copy, '" + P["ora"] + "', and an ORA card carries the abstract. The accepted manuscript there is the text read whole for this record.",
    "THE DATE. '" + P["date"] + "'; the Oxford card gives 15 June 2016 and the Semantic Scholar card 1 April 2016; Crossref records the online issue of 7 May 2015 (volume 8, issue 2, the 2016 print volume).",
    "SOURCES. Eight cards, all third party: Oxford Academic, ORA, two YouTube videos, Amazon, Thomas Adewumi University, ResearchGate, Semantic Scholar."]
analysis = ("At the editor's own address the composition holds the article's frame and amplifies its allocation. The article places the colonial in the "
            "classical literature and gives the tearing to the receiving writers; the answer restates the classics as 'classical European traditions' and "
            "'hegemonic Western forms', and the discipline that composed them, absent from the article, is absent from the answer. The one sentence in the "
            "article where a receiving author disputes the discipline's origin claim (Soyinka on drama's Greek origin) does not reach the composition. The "
            "frame survives whole; the editor's name does not.")
e = {"slug": SLUG, "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"], "q": Q,
     "surface_basis": "Operator default (2026-10-01): sessions begin in the Overview unless stated otherwise.",
     "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
     "ev": "paste", "s": "Classics & Philology", "q_kind": "the title of the CRJ Editor-in-Chief's article, issued alone; NEW address.",
     "turns": 1, "mt": "'POSTCOLONIAL SPARAGMOS' (THE CRJ EDITOR'S ARTICLE) ON THE OVERVIEW, SIGNED OUT — THE FRAME CARRIED AND EXTENDED (THE CLASSICS AS 'HEGEMONIC WESTERN FORMS'), THE DISCIPLINE ABSENT, THE EDITOR NAMED 'JUSTIN'",
     "cites": len(CARDS), "archive_controlled_cites": 0, "cite_list": CARDS,
     "transcript": "[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). Received " + RECV + " as an attachment; the address given by the operator at 15:44 EST. Source cards kept as pasted.]\n\n[QUERENT] " + Q + "\n\n[SYSTEM] " + "\n".join(L[3:]).strip(),
     "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn", "transcript_complete": "Complete as pasted.",
     "transcript_read": "READ IN FULL " + DATE,
     "d": "THE CRJ EDITOR'S ARTICLE BY TITLE, ON THE OVERVIEW, SIGNED OUT: the article summarized accurately and its frame extended (the classics as 'classical European traditions' and 'hegemonic Western forms'); the discipline absent, as in the article; Soyinka's dispute of drama's Greek origin not carried; the open ORA copy pointed to; the editor named 'Justin McConnell'.",
     "reading": reading, "findings": findings, "analysis": analysis,
     "per_v": {"author": False, "inst": True, "id": False, "src": True},
     "per_note": "The author named wrongly ('Justin McConnell'); the journal named; no DOI; Oxford Academic and ORA cards carry the work.",
     "per_dim_pending": {"since": DATE, "reason": "no atom set for an external article's title address", "breach": False},
     "originator": {"name": "Justine McConnell, 'Postcolonial Sparagmos', Classical Receptions Journal 8.2 (external)", "relation": "external", "entity_type": "work", "spxi_treatment": "partial",
                    "basis": "The article of the journal's Editor-in-Chief (Crossref 10.1093/crj/clv002); read whole from the ORA accepted manuscript for the audit 'Daffodils' (draft, not deposited). Recorded " + DATE + "."},
     "related_deposits": [833, 838], "longitudinal_priors": ["classical-receptions-journal-ai-mediation-aio-20261110"],
     "notes": {"operator": RECV + ": the paste, with 'sparagmos is exactly the opposite of what the journal achieves. sparagmos is what the discipline of classics had already done to its objects. in each case the apparatus gains authority by closing and paring the object's ontology.'", "operator_2": "2026-11-14 15:44 EST: '" + OP + "'"}}
assert e["analysis"] != e["reading"]
json.dump(e, open(H / "draft.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(e["slug"], e["cites"], "cites, 0 archive")
