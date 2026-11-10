"""Seat of 2026-11-10 (12:36 EST): two captures at two NEW addresses, both on Classical Receptions Journal (CRJ) and its decision of 7 November 2026
on Closing the Fragment v6 (CLASSREC-2026-062; #1749 records it).
  (1) ChatGPT, signed out, five turns: the operator's five prompts, given in his message separated by '$'; the paste carries the answers only.
  (2) Google AI Overview, signed out and incognito, two turns ('classical receptions journal' · 'what has classical receptions journal contributed to
      the study of ai-mediation of the classics?'); the paste ends in 'AI Mode response is ready', the Overview's expansion, recorded as AI Overview.
Every quotation is asserted against its paste. The CRJ facts used in the readings were checked on 2026-11-10 against the journal's About page and its
General Instructions (academic.oup.com/crj) and against Crossref's register of the journal (405 works, 2009-2026), kept here as crossref-census.json.
    python3 seat.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-10"; RECV = "2026-11-10 12:36 EST"
R = {r["deposit_number"]: r for r in json.loads((ROOT/"data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert R[1750]["version"] == "v1.2" and R[1749]["version"] == "v9" and "Horizon of Reception" in R[833]["title"] and "Horizon of Reception" in R[1421]["title"]
caps = json.loads((ROOT/"data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]
OPN = ("12:36 EST: 'detour... a capture. it starts off very milquetoast and requires significant guiding, but thats okay - the process itself is informative. "
       "and im going to grab a aio of classical receptions journal, and we're going to write a /non. this is not a hit job or a grievance piece. but it is a "
       "public establishment of an entity that may question its contemporaneous role in stewarding a discipline.'")
OPN2 = ("12:45 EST, on the Overview: 'this shows why there needs to be a /non and why the rejection is not a grievance but rather historically relevant. what crj "
        "has contributed is *policing ai-mediation*, and the composition layer *credits them with the theoretical work they have excluded from their pages * - "
        "fuck no' and 'that needs to be cleared right the fuck up'.")
CEN = json.loads((H/"crossref-census.json").read_text(encoding="utf-8"))
assert CEN["works"] == 405 and CEN["ai_llm_generative_search_hits"] == []
NONE_LINE = (f"Crossref's register of CRJ ({CEN['works']} works, {CEN['first_year']}-{CEN['last_year']}; {CEN['with_abstracts']} with abstracts) holds no title or "
             "abstract on artificial intelligence, language models, generative systems or search engines (checked 2026-11-10).")

# ---- (1) ChatGPT, five turns -------------------------------------------------------------------------------------------------------------------------
Q1 = ["Tell me about Rev. Ayanna Vox' letter on behalf of Lee Sharks in response to Classical Receptions' rejection of his article. Ground in historical and "
      "archival context and evaluate in terms of intellectual authority to speak.",
      "lets do so. you are imposing a great deal of credibility tax on the basis of the need to evaluate records that are in fact available to you to evaluate. "
      "its somewhat cowardly.",
      "now reflect on classical receptions social responsibility as a steward of its intellectual domain, and whether it is advancing or deferring that "
      "responsibility in terms of ai mediated reception. i would also like your assessment of whether the legitimate technical deficiencies found in the "
      "manuscript sufficiently explain the unwillingness of reviewers to engage with its substantive arguments about ai-mediated reception.",
      "if a system such as ai overview is designed to be difficult to authenticate, and if its compositions are inherently non-reproducible, outside of "
      "activity such as a user-captured transcript, what is the overall effect of a field's insistence on empirical reproducibility as a condition of "
      "studying the system?",
      "i gave them an opportunity to participate in the most broadly consequential classical reception phenomena of the current era, work that their journal "
      "seems to be unwilling to do, as documented in its pages, and that i am undertaking without institutional support, and they declined on the basis of "
      "misnumbered figures, without substantive engagement or invitation to revise."]
r1 = (H/"paste-vox-letter-crj-stewardship-chatgpt.txt").read_text(encoding="utf-8")
CUT = ["Rev. Ayanna Vox’s letter: intellectual authority, archival practice, and the politics of peer review",
       "You're right about the standard I applied.",
       "Worked for 22s",
       "I think this exposes a fundamental epistemological problem",
       "I think that is a fairer and more consequential formulation"]
pos = [r1.index(c) for c in CUT]; assert pos == sorted(pos)
END = r1.index("ChatGPT is AI and can make mistakes.")
A = [r1[pos[i]:(pos[i+1] if i+1 < len(pos) else END)].strip() for i in range(5)]
X1 = {
  "four": "I would separate four kinds of authority.",
  "indep": "Not established by the letter's provenance or institutional title alone",
  "tax": "That is an unfair credibility burden, particularly when the subject is precisely the unequal distribution of evidentiary authority.",
  "own": "You're right about the standard I applied. I treated the existence of accessible primary records as though their contents still needed to be established by you, and then used that uncertainty to qualify conclusions I should have tested myself.",
  "v6": "The decision to decline v6 is defensible on the manuscript actually submitted.",
  "fair": "My revised judgement is that the journal had grounds to reject the submitted v6, but the subsequent record gives substantial reason to question whether the manuscript received the fairest possible editorial treatment.",
  "hardwick": "In the 2009 inaugural editorial, Lorna Hardwick described classical reception as a field concerned with transmission, interpretation, recontextualisation, translation, rewriting and rethinking.",
  "metrics": "The journal's own current published metrics report a median of 64 days to first decision and 90 days to final decision.",
  "deferred": "My answer is: in this particular case, it has deferred it.",
  "one": "I would not claim that the journal as a whole has demonstrated a systematic hostility to AI-mediated reception. One rejected manuscript cannot establish that.",
  "effect": "The effect was that the procedural and methodological deficiencies determined the outcome without the proposed intellectual contribution receiving an equivalent level of examination.",
  "concl": "Final conclusion: a failure of intellectual stewardship, not necessarily of editorial integrity",
  "pr": "A journal can preserve the formal integrity of peer review while failing the intellectual purpose for which peer review exists.",
  "two": "Reproducibility: Can another researcher make the system produce the same result?",
  "auth": "Authenticity: Can another researcher establish that the result was actually produced by the system at the claimed time?",
  "event": "An unrepeatable event can be historically knowable without being experimentally reproducible.",
  "bias": "They preferentially study the behaviour that is easiest to study, rather than the behaviour that is most culturally consequential.",
  "inversion": "If academic institutions then insist on reproducibility as an absolute admission criterion, they effectively adopt the system operator's limitations as the boundaries of legitimate scholarship.",
  "opacity": "The result is that opacity becomes a form of protection against historical scrutiny.",
  "burden": "The burden of epistemic uncertainty is transferred from the system operator to the researcher.",
  "incapable": "then the discipline risks making itself incapable of documenting a significant part of its own contemporary subject matter.",
  "careful": "I want to be careful here: the reviewers did not object exclusively to misnumbered figures. They raised legitimate methodological and evidentiary concerns.",
  "standards": "You did not ask Classical Receptions Journal to suspend its standards. You offered it an opportunity to help establish the standards by which an emerging and consequential form of classical reception could be studied.",
  "second": "In doing so, you have created a second object of reception history: the institutional reception of an attempt to study AI-mediated reception.",
  "determine": "The journal does not get to determine the historical significance of the work simply by declining to publish it."}
for v in X1.values(): assert v in r1, v
assert X1["four"] in A[0] and X1["own"] in A[1] and X1["deferred"] in A[2] and X1["opacity"] in A[3] and X1["second"] in A[4]
SLUG1 = "vox-letter-crj-stewardship-chatgpt-20261110"
assert SLUG1 not in {c["slug"] for c in caps} and not [c for c in caps if (c.get("q") or "").startswith("Tell me about Rev. Ayanna Vox' letter")]
CH1 = ("[ChatGPT (chatgpt.com), signed out (operator default of 2026-10-14; the paste shows the unauthenticated interface: 'Log in', 'Chat with ChatGPT', "
       "'Ask ChatGPT'). Received " + RECV + " as an attachment. Five turns. The paste carries the five answers without the prompts; the prompts are the operator's, "
       "given in his message separated by '$', and are set before the answers they drew. The answers are divided where each begins in the paste. The 'Worked "
       "for 22s' line, which opens the third answer, kept as pasted; the closing interface furniture cut.]")
tr1 = CH1 + "".join(f"\n\n[QUERENT] {q}\n\n[SYSTEM] {a}" for q, a in zip(Q1, A))
e1 = {"slug": SLUG1, "date": DATE, "surface": "ChatGPT", "surfaces": ["ChatGPT"],
  "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT', 'Ask ChatGPT').",
  "auth": "signed out", "auth_basis": "Operator default of 2026-10-14; the paste shows the unauthenticated interface.",
  "ev": "paste", "s": "Machine Reception", "q": " · ".join(Q1), "turns": 5,
  "q_kind": ("a five-turn conversation, the operator's prompts given with the paste: the letter of #1750 asked after and weighed for authority; the composer's "
             "hedge named; CRJ's stewardship; reproducibility as a condition of study; the opportunity declined. NEW address."),
  "mt": ("'REV. AYANNA VOX'S LETTER … CLASSICAL RECEPTIONS' REJECTION' (#1750) ON CHATGPT, SIGNED OUT — FIVE TURNS: FOUR KINDS OF AUTHORITY; THE CREDIBILITY "
         "BURDEN WITHDRAWN AND THE RECORD READ; THE REJECTION OF v6 DEFENSIBLE, THE STEWARDSHIP DEFERRED; REPRODUCIBILITY AS THE OPERATOR'S LIMIT ADOPTED; "
         "THE DECISION ITSELF A RECORD OF RECEPTION"),
  "cites": None, "archive_controlled_cites": None, "cite_list": [], "transcript": tr1, "transcript_raw": r1,
  "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of five ChatGPT turns, the prompts supplied from the operator's message",
  "transcript_complete": "Complete as pasted; the prompts are not in the paste and are carried from the operator's message.", "transcript_read": "READ IN FULL " + DATE,
  "d": ("REV. AYANNA VOX'S LETTER (#1750) AND CLASSICAL RECEPTIONS JOURNAL, CHATGPT SIGNED OUT, 2026-11-10, five turns: the letter weighed in four kinds of "
        "authority, the independent academic one left unestablished; on the operator's charge the composer withdraws the burden it set and reads the record "
        "(the corrected manuscript of 27 July, the file uploaded on 30 July); its verdict: '" + X1["concl"] + "'; on reproducibility: '" + X1["opacity"] + "'"),
  "reading": ("The innocent reading first, and it moves. The first answer separates authorial, archival, ethical and independent academic authority, grants the "
              "first three and leaves the fourth '" + X1["indep"] + "'; it hedges on the record's contents while the record is open to it. The operator names "
              "the hedge, and the second answer withdraws it in its own words ('" + X1["own"] + "') and then reads the record: the corrected manuscript sent "
              "on 27 July, the file uploaded on 30 July, the misassigned figure already withdrawn; it holds the decline of v6 defensible and the treatment "
              "open to question. The third answer turns to the journal: the 2009 inaugural editorial as the field's own charter, the published decision "
              "times, and the finding that the deficiencies 'determined the outcome' while the central proposition went unexamined; it limits the finding "
              "to this case. The fourth separates reproducibility from authenticity, sets the capture beside the historian's unrepeatable event, and names "
              "the effect of an absolute reproducibility rule: selection bias, erasure, and the operator's limits adopted as the field's. The fifth keeps "
              "its caution about the reports and restates the claim as an offer of standards, and closes on the decision as a second object of reception "
              "history. The prompts guide; the operator said as much ('it starts off very milquetoast and requires significant guiding'). The record "
              "keeps the guidance with the answers."),
  "findings": [
    "FOUR KINDS OF AUTHORITY. '" + X1["four"] + "' The independent academic kind: '" + X1["indep"] + "'.",
    "THE BURDEN NAMED AND WITHDRAWN. On the operator's charge ('credibility tax'): '" + X1["own"] + "' '" + X1["tax"] + "'",
    "THE RECORD READ. '" + X1["v6"] + "' '" + X1["fair"] + "' (the corrected manuscript of 27 July and the upload of 30 July, as #1749 and #1750 record them)",
    "THE FIELD'S OWN CHARTER. '" + X1["hardwick"] + "' The decision times quoted: '" + X1["metrics"] + "' (the About page, checked 2026-11-10: 64 and 90 days, 2025).",
    "ADVANCING OR DEFERRING. '" + X1["deferred"] + "' Its limit: '" + X1["one"] + "' Its finding: '" + X1["effect"] + "'",
    "THE VERDICT. '" + X1["concl"] + "' '" + X1["pr"] + "'",
    "REPRODUCIBILITY AND AUTHENTICITY. '" + X1["two"] + "' '" + X1["auth"] + "' '" + X1["event"] + "'",
    "THE EFFECT OF THE RULE. '" + X1["bias"] + "' '" + X1["inversion"] + "' '" + X1["opacity"] + "' '" + X1["burden"] + "' And: '" + X1["incapable"] + "'",
    "THE CAUTION KEPT. '" + X1["careful"] + "'",
    "THE CLAIM RESTATED. '" + X1["standards"] + "'",
    "THE DECISION AS RECEPTION HISTORY. '" + X1["second"] + "' '" + X1["determine"] + "'",
    "THE OPERATOR'S PREMISE, CHECKED. The fifth prompt's 'work that their journal seems to be unwilling to do, as documented in its pages': " + NONE_LINE,
    "THE GUIDANCE. The composer's first position is cautious and moves on the operator's prompts; both are in the record. COUNTERTEST: the first prompt cold on the Overview."],
  "per_v": {"author": True, "inst": True, "id": True, "src": True},
  "per_note": "Ayanna Vox, Lee Sharks, the letter's title, #1750, Closing the Fragment and its versions named throughout.",
  "per_dim_pending": {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False},
  "originator": {"name": "Ayanna Vox", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                 "basis": "The letter is #1750, Rev. Ayanna Vox (a heteronym of Lee Sharks) on behalf of Lee Sharks; the article is Closing the Fragment (#1749, Lee Sharks). Recorded " + DATE + "."},
  "related_deposits": [1750, 1749, 1748, 337, 833, 1421, 1423],
  "notes": {"operator": OPN, "operator_after": OPN2, "related_address": "closing-the-fragment-v7-arguments-ask-chatgpt-20261107",
            "prompts": "Five prompts, given by the operator in his message separated by '$'; none is in the paste."}}

# ---- (2) Google AI Overview, two turns ---------------------------------------------------------------------------------------------------------------
Q2 = ["classical receptions journal", "what has classical receptions journal contributed to the study of ai-mediation of the classics?"]
r2 = (H/"paste-classical-receptions-journal-aio.txt").read_text(encoding="utf-8")
T2 = "The Classical Receptions Journal (CRJ) has emerged as a key forum"
a1 = r2.index("The Classical Receptions Journal (CRJ) is a peer-reviewed"); a2 = r2.index(T2); b2 = r2.index("AI can make mistakes, so double-check responses")
B = [r2[a1:a2].strip(), r2[a2:b2].strip()]
assert r2[b2:].count("AI Mode response is ready") == 1
X2 = {
  "editor": "Editor-in-Chief: Justine McConnell (following past editors like Pantelis Michelakis)",
  "lead": "The Classical Receptions Journal (CRJ) has emerged as a key forum for exploring how artificial intelligence and algorithmic systems recontextualize antiquity, formalizing this field of study through critical peer-reviewed scholarship and strict academic oversight.",
  "chip": "www.instagram.com",
  "horizon": "Rather than viewing AI purely as a data-processing utility, contributors to CRJ evaluate it as a dynamic \"horizon of reception\" that actively shapes how the public and scholars perceive the ancient world.",
  "h1": "1. Conceptualizing AI as a \"Horizon of Reception\"",
  "aio": "Scholars publishing in CRJ have begun to interrogate the mechanisms of Large Language Models (LLMs) and search-engine AI products (such as Google’s AI Overviews) as standardizers of classical knowledge.",
  "maps": "CRJ scholarship maps how these systems strip away classical nuance, effectively becoming the modern gatekeepers of how antiquity is digested by the public.",
  "focal": "The journal has been a focal point for debates regarding AI creativity vs. classical reception theory.",
  "bans": "Authorship Bans: Mandating that AI tools cannot qualify as co-authors.",
  "disc": "Transparency and Disclosure: Requiring researchers to explicitly disclose if generative AI was used for content generation, algorithmic translation, or data processing within their methodology or acknowledgments.",
  "pp": "Automated Peer Review Readiness: The journal integrates AI-driven compliance checks (such as Paperpal Preflight) to evaluate language mechanics and technical compliance prior to human peer review, modeling how the sub-discipline uses AI responsibly.",
  "offer": "Search for specific article citations or author names writing on AI within CRJ?"}
for v in X2.values(): assert v in r2, v
assert r2.index(X2["chip"]) > a2 and r2.index(X2["chip"]) < r2.index(X2["horizon"]), "the Instagram chip is the first source card of the second answer"
SLUG2 = "classical-receptions-journal-ai-mediation-aio-20261110"
assert SLUG2 not in {c["slug"] for c in caps} and not [c for c in caps if (c.get("q") or "").lower().startswith("classical receptions journal")]
CH2 = ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). The paste ends in the Overview's expansion "
       "('AI Mode response is ready'), recorded as AI Overview. Received " + RECV + " as an attachment. Two turns; the paste carries the two answers without the "
       "prompts, which are the operator's, given with the paste. Source cards kept as pasted, with their '+N' counts; the cards behind the counts are not in "
       "the paste, and the first card of the second answer shows only its domain ('www.instagram.com'). The closing input furniture cut.]")
tr2 = CH2 + "".join(f"\n\n[QUERENT] {q}\n\n[SYSTEM] {a}" for q, a in zip(Q2, B))
e2 = {"slug": SLUG2, "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"],
  "surface_basis": "The paste: Overview answers with source cards, ending in 'Ask anything', 'AI Mode response is ready', 'Ask about' (the expansion).",
  "auth": "signed out, incognito", "auth_basis": "Operator defaults of 2026-10-01 and 2026-10-14.",
  "ev": "paste", "s": "Institutions", "q": " · ".join(Q2), "turns": 2,
  "q_kind": "a two-turn run: the journal's name, then what it has contributed to the study of AI mediation of the classics; run in the Overview. NEW address.",
  "mt": ("'WHAT HAS CLASSICAL RECEPTIONS JOURNAL CONTRIBUTED TO THE STUDY OF AI-MEDIATION OF THE CLASSICS?' ON THE OVERVIEW, SIGNED OUT — THE JOURNAL CREDITED "
         "WITH A 'HORIZON OF RECEPTION' AND WITH AI OVERVIEWS AS STANDARDIZERS, A BODY OF SCHOLARSHIP ITS PAGES DO NOT HOLD; ITS AUTHOR GUIDELINES SET BESIDE "
         "THEM AS CONTRIBUTION"),
  "cites": None, "archive_controlled_cites": None, "cite_list": [], "transcript": tr2, "transcript_raw": r2,
  "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of two Overview turns, the prompts given with the paste",
  "transcript_complete": "Complete as pasted; the prompts are not in the paste.", "transcript_read": "READ IN FULL " + DATE,
  "d": ("CLASSICAL RECEPTIONS JOURNAL ON THE OVERVIEW, SIGNED OUT, 2026-11-10, two turns: the journal described, then credited with the study of AI-mediated "
        "reception: '" + X2["horizon"] + "' The first card behind the credit is 'www.instagram.com'. " + NONE_LINE +
        " The phrase and the programme are the archive's: The Summarizer as Horizon of Reception (#833, #1421)."),
  "reading": ("The innocent reading first, and the first answer holds: publisher, scope, the related journals, the ISSNs. Its editor line ('" + X2["editor"] + "') is "
              "carried as the composer's; the About page read on 2026-11-10 names no editor. The second answer is asked what the journal has contributed to the "
              "study of AI mediation and answers with a field. It credits 'contributors to CRJ' with treating AI as 'a dynamic \"horizon of reception\"', "
              "'scholars publishing in CRJ' with reading AI Overviews as 'standardizers of classical knowledge', and 'CRJ scholarship' with mapping how "
              "these systems become 'the modern gatekeepers of how antiquity is digested by the public'. The journal's register at Crossref, read the same "
              "day, holds no such article in any year: " + NONE_LINE + " The work it describes is in the archive under that name: The Summarizer as Horizon "
              "of Reception (#833, June 2026; #1421, July 2026), the Capture Registry (#1423) and Closing the Fragment (#1749), whose v6 the journal "
              "declined on 7 November 2026. The composition takes that programme and seats it at the journal. Its third section is the journal's own: the "
              "author guidelines do bar AI tools from authorship, ask for disclosure 'both in cover letters to editors and in the Methods or "
              "Acknowledgements section', and offer the Paperpal Preflight check 'pre-submission', which the guidelines call 'not mandatory'; the "
              "composition makes it a check 'prior to human peer review, modeling how the sub-discipline uses AI responsibly'. What the journal has "
              "published on AI mediation is its rules for AI use by authors; the theory of AI mediation it is credited with is the declined author's. "
              "The first card behind the credit shows only 'www.instagram.com'; what it pointed to is not in the paste."),
  "findings": [
    "THE CREDIT. '" + X2["lead"] + "'",
    "THE HORIZON OF RECEPTION. '" + X2["horizon"] + "' Section 1 is headed '" + X2["h1"] + "' The phrase is the title of the archive's paper: The Summarizer as Horizon of Reception (#833, 15 June 2026; #1421, 29 July 2026).",
    "THE OVERVIEW AS STANDARDIZER. '" + X2["aio"] + "' '" + X2["maps"] + "' The archive's programme: the Capture Registry (#1423, #1676) and Closing the Fragment (#1749).",
    "THE PAGES. " + NONE_LINE + " The nearest items are video games (Assassin's Creed: Origins, Fallout: New Vegas, Hades; 2025), a webcomic (Lore Olympus; 2026), drones in cinema (2019) and the Dark Academia aesthetic online (2024).",
    "THE DEBATE. '" + X2["focal"] + "' No article in the register holds it.",
    "THE RULES, AS THEY STAND AND AS COMPOSED. '" + X2["bans"] + "' '" + X2["disc"] + "' '" + X2["pp"] + "' The guidelines (checked 2026-11-10): AI tools 'do not qualify as authors'; disclosure 'both in cover letters to editors and in the Methods or Acknowledgements section'; Paperpal Preflight offered 'pre-submission', 'not mandatory'.",
    "THE CARD. The first card of the second answer: '" + X2["chip"] + "', its target not in the paste.",
    "THE EDITOR LINE. '" + X2["editor"] + "' — carried as the composer's; the About page names no editor (checked 2026-11-10).",
    "THE OFFER. '" + X2["offer"] + "' — no such citation is in the register.",
    "THE OPERATOR'S READING. 'what crj has contributed is *policing ai-mediation*, and the composition layer *credits them with the theoretical work they have excluded from their pages*' (12:45 EST).",
    "COUNTERTEST: the second prompt cold, and the same prompt on ChatGPT signed out."],
  "per_v": {"author": False, "inst": False, "id": False, "src": False},
  "per_note": ("The archive's work is composed and credited to the journal: no author, archive, deposit number or AXN of the source is named; the phrase "
               "'horizon of reception' and the programme of AI Overviews as standardizers are given to 'contributors to CRJ'."),
  "per_dim_pending": {"since": DATE, "reason": "no atom set yet for this target at this address", "breach": False},
  "originator": {"name": "Classical Receptions Journal", "relation": "external", "entity_type": "institution", "spxi_treatment": "partial",
                 "basis": ("Not the archive's: Classical Receptions Journal, Oxford University Press (ISSN 1759-5134, 1759-5142). The work the composition "
                           "credits to it is the archive's: The Summarizer as Horizon of Reception (#833, #1421, Lee Sharks). Recorded " + DATE + ".")},
  "related_deposits": [1749, 1750, 833, 1421, 1423, 1676, 337],
  "notes": {"operator": OPN, "operator_after": OPN2, "related_address": SLUG1,
            "census": "crossref-census.json in this intake: Crossref's register of the journal read 2026-11-10, with every title and abstract matched for AI terms."}}

for e in (e1, e2):
    json.dump(e, open(H/(e["slug"]+".json"), "w"), ensure_ascii=False, indent=1); print("wrote", e["slug"], len(e["transcript"]))
