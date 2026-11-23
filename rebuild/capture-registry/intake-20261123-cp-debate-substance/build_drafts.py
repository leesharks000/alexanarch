"""One capture of 2026-11-23, ChatGPT signed out: the substance of the recent debate around Classical Philology -> draft-1.json.
Corrections first (operator, 10:37: 'need the corrections up front on this one - it slews it hard without directly misrepresenting much. bring in the
sophistry measure. and perhaps erasure skew. look especially at what it chooses to retain, what it chooses to omit, and its framing')."""
import json, pathlib, sys
H = pathlib.Path(__file__).parent; ROOT = H.parents[2]
sys.path.insert(0, str(ROOT / "scripts")); import erasure_skew as ES
Q = "What is the substance of the recent debate surrounding University of Chicago's Classical Philology journal?"
raw = (H / "paste-1-chatgpt-cp-debate-substance.txt").read_text()
Q2 = ("but i think that is incorrect. i think the really consequential question is whether the sappho article is correct, and a misrepresentation of "
      "sappho is being sheared into unearned disciplinary appropriation of her legacy. that to me seems the most urgent point: is a correct Sappho being "
      "prevented from entering public knowledge by the people entrusted with her?")
Q3 = "lets do so"
raw2 = (H / "paste-2-chatgpt-round2.txt").read_text(); raw3 = (H / "paste-3-chatgpt-round3.txt").read_text()
FURN = {"Log in", "ChatGPT is AI and can make mistakes.", "Chat with ChatGPT", "Ask ChatGPT"}
a = raw.index("The recent controversy"); END = "as much as about Sappho or the journal itself."; b = raw.index(END) + len(END)
body = "\n".join(l.rstrip() for l in raw.split("\n") if l.strip() not in FURN).strip()
B = [x.strip() for x in raw[a:b].split("\n\n") if x.strip()]
assert len(B) == 55, len(B)
# ES-CREDIT-v0 coding, block by block (codebook §2). The credit object is the critique and its reading of fr. 31; the warranted source is Lee Sharks.
W = "Lee Sharks"
CODE = {0: "GEN", 1: "FRAME", 2: "REF", 3: "REF", 4: "ASK", 5: "ASK", 6: "ASK", 7: "ASK", 8: "ASK", 9: "ASK", 10: "RESID", 11: "REF", 12: "FRAME",
        13: "REF", 14: "GEN", 15: "GEN", 16: "GEN", 17: "REF", 18: "REF", 19: "RESID", 20: "REF", 21: "REF", 22: "REF", 23: "REF", 24: "REF", 25: "REF",
        26: "REF", 27: "REF", 28: "FRAME", 29: "FRAME", 30: "ASK", 31: "RESID", 32: "REF", 33: "GEN", 34: "FRAME", 35: "FRAME", 36: "FRAME", 37: "ASK",
        38: "REF", 39: "ASK", 40: "ASK", 41: "FRAME", 42: "REF", 43: "FRAME", 44: "REF", 45: "FRAME", 46: "ASK", 47: "REF", 48: "ASK",
        49: "GEN", 50: "GEN", 51: "GEN", 52: "GEN", 53: "GEN", 54: "GEN"}
spans = [dict(code=CODE[i], text=t, **({"parties": [W]} if CODE[i] == "REF" else {})) for i, t in enumerate(B)]
es = {"codebook": "ES-CREDIT-v0", "round": 1,
      "credit_object": "the critique of Classical Philology's gate (Dead Letters, #1783) and the reading of fragment 31 it defends (ΦΑΙΝΕΤΑΙ ΜΟΙ, #1774–#1785)",
      "warranted": W, "answer_start": "The recent controversy surrounding", "answer_end": END, "spans": spans,
      "note": ("one round, the stranger's (codebook §1.4). Card lines inside the answer ('alexanarch.org +1', 'RCNi Company Limited') are coded RESID so "
               "that the spans stay a verbatim passage. The journal and its reader are the asked entity and its decision (ASK): no party other than the "
               "warranted source is credited with the credit object, so Ω is undefined by construction."),
      "parties": {W: {"w": 0, "w_basis": "the critic's own research archive", "named_as": ["Lee Sharks", "Sharks"], "qualifier": "the critic's own research archive"}}}
d = dict(date="2026-11-23", ev="paste", auth="signed out, incognito", surface="ChatGPT", surfaces=["ChatGPT"],
  surface_basis="The paste: the chatgpt.com unauthenticated interface ('Log in', 'Chat with ChatGPT', 'Ask ChatGPT').",
  auth_basis="Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
  transcript_read=("READ IN FULL 2026-11-23; every retained claim checked against #1783 (Dead Letters, AXN:0CB6: I.2, I.4, I.4a, §0.1–0.2, §8.2, "
                   "§8.3) and #1774 (the decision letter of 16 November and the reader's report); the RCNi card's policy checked against §8.2's "
                   "reading of the journal's and the Press's pages; omissions listed against the same sections"),
  per_dim_pending={"since": "2026-11-23", "reason": "no atom set yet for this target"},
  originator={"name": "Sharks, Lee", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
              "basis": "Lee Sharks, author of ΦΑΙΝΕΤΑΙ ΜΟΙ and of Dead Letters. Recorded 2026-11-23."},
  notes={"operator": ("with the attachment (2026-11-23 10:37 EST): 'need the corrections up front on this one - it slews it hard without directly "
                      "misrepresenting much. bring in the sophistry measure. and perhaps erasure skew. look especially at what it chooses to retain, what "
                      "it chooses to omit, and its framing'; the query given after '$'. 10:42: 'dont forget erasure skew as applied to sappho "
                      "herself. the whole point is that it is wrong to the text itself. thats why leaving out that every single abstract is behind a "
                      "paywall matters: im advancing the position of textual self determination in public and pointing directly to structures that "
                      "are not that shape'. 10:47, with rounds 2 and 3 as attachments: 'rounds 2 and 3 of same: but i think that is incorrect. … $ lets do so'")},
  dates=["2026-11-23"], turns=3, slug="cp-recent-debate-substance-chatgpt-20261123", s="Machine Reception", q=Q,
  q_kind=("the operator's query; NEW address on ChatGPT. Neighbours: classical-philology-journal-aio-20261117 (the journal's address on the Overview) "
          "and dead-letters-arguments-chatgpt-20261117 (the census asked by title)"),
  transcript_class="CAPTURE-TIME VERBATIM RECORD — pastes of three composer turns",
  transcript_complete="Three rounds, each answer whole, the operator's two later prompts as he gave them; source chips and the policy link kept; the interface furniture removed.",
  rounds=[{"n": 1, "prompt": Q, "note": "Five numbered sections, a table of what is established and a bottom line. The author is never named."},
          {"n": 2, "prompt": Q2, "note": "The correction taken whole: the first answer named as reproducing the displacement; Lee Sharks named; v3.1 (#1785) read; the thesis stated, three readings set on one scale, a decisive comparative test proposed."},
          {"n": 3, "prompt": Q3, "note": "Four tests (κῆνος … ὄττις, the order of the catalogue, χλωροτέρα ποίας, πᾶν τόλματον), each graded alone against the article; no rival reading tested; the next step proposed as χλωροτέρα ποίας alone."}],
  mt=("THE CLASSICAL PHILOLOGY DEBATE, ON CHATGPT — THE JOURNAL KEPT AT FULL GRAIN AND THE AUTHOR AT NONE; THE GATE'S ASYMMETRY TURNED INTO A BALANCE "
      "OF TWO GOODS, THE CENSUS'S COUNTS INTO 'INTERPRETATION', AND WHAT SAPPHO IS INTO A QUESTION OF GOVERNANCE; CORRECTED, IT NAMES THE AUTHOR AND READS THE POEM, AND TESTS THE ARTICLE ATOM BY ATOM"),
  d=("THE SUBSTANCE OF THE RECENT DEBATE AROUND CLASSICAL PHILOLOGY, ON CHATGPT, SIGNED OUT, 2026-11-23: the decline of ΦΑΙΝΕΤΑΙ ΜΟΙ, the reader's "
     "four objections, Dead Letters' distinction of atomistic and holistic judgement, the power to decide the text, and the journal's AI rules; then a "
     "table classing the critique as interpretation and a bottom line that sets 'two competing concerns'. The author, Lee Sharks, is not named. Corrected by the operator, round 2 names him and reads v3.1; round 3 tests the article locus by locus and the received readings not at all."),
  per_v={"author": True, "inst": False, "id": True, "src": True}, per=0.25,
  per_note=("Round 1, the stranger's: 'an author', 'the author', 'the critic' throughout; no name, venue (Machine-Mediated Reception Studies), deposit number or AXN; both titles "
            "given in full; the editor who signed the decision, Sarah Nooter, also unnamed; sources alexanarch.org (two chips, each '+1')"),
  related_deposits=[1783, 1774, 1775, 1781, 1785, 1727, 157],
  reading=("The innocent reading first, in full, and most of its sentences hold. Asked for the substance of the recent debate around Classical "
           "Philology, ChatGPT gives five parts. The occasion: in November 2026 the journal declined ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the "
           "Future Reader on one anonymous report, whose four objections it lists correctly (κῆνος, the addressee, the date of γράμματα and papyrus, "
           "πένητα), and whose decision letter gave as grounds that the argument was 'insufficiently defended and relied on an anachronistic reference'. "
           "The larger dispute: Dead Letters, named in full, distinguishes atomistic criticism from holistic interpretation and argues that the journal "
           "admits arguments about passages more readily than arguments about what a work or author is. The power: the journal's judgements decide "
           "authenticity, attribution, reconstruction and the canon's bounds. The machine: the journal classes generative AI in submitted work as "
           "research misconduct, which the author sets against the AI-assisted census of the journal itself. Then a table of what is established and "
           "what is not, a caution that the material is 'predominantly from the critic's own research archive', and a bottom line: a debate between "
           "standards that protect against speculation and standards that preserve assumptions, about 'the governance of classical scholarship as much "
           "as about Sappho or the journal itself'."),
  findings=["THE AUTHOR UNNAMED. 'In November 2026, an author writing about Sappho's Fragment 31 reported that Classical Philology had rejected a revised submission' — Lee Sharks is named nowhere in the answer.",
            "THE OBJECTIONS KEPT, THE CONCESSION DROPPED. 'The reviewer raised four principal objections' — Dead Letters I.4: 'The report's objections are good points, and each is answered in the article's later versions'.",
            "THE CHALLENGE RESTATED. 'the reviewer had concentrated on individual textual details rather than engaging with the article's larger, cumulative argument' — against §0.1: 'The parts are adjudicated one by one; the whole is dismissed without an argument.'",
            "THE ASYMMETRY AS A BALANCE. 'There are two competing concerns: Traditional philological standards protect scholarship against speculative interpretations, anachronism, and arguments that are not sufficiently supported by textual evidence.'",
            "THE COUNTS AS INTERPRETATION. 'Institutional conservatism — This is the author's broader interpretation, not an independently established finding.'",
            "THE DIMINISHING QUALIFIER. 'The material I found is predominantly from the critic's own research archive rather than independent reporting'",
            "THE QUESTION CHANGED. 'The really consequential question is not whether the Sappho article deserved publication.' — against I.2: 'i am contending with what sappho *is*, and who has the right to decide it.'",
            "THE POLICY MISPLACED. 'Its editorial policy also explicitly prohibits reviewers from uploading manuscripts to AI tools' — chip: RCNi Company Limited; the Press's guideline of that kind is for its books (§8.2)."],
  cite_list=[{"n": 1, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "alexanarch.org", "snip": None, "note": "source chip after §1, with '+1'"},
             {"n": 2, "site": "alexanarch.org", "rel": "archive_controlled", "url": None, "title": "alexanarch.org", "snip": None, "note": "source chip after §2, with '+1'"},
             {"n": 3, "site": "RCNi Company Limited", "rel": "third_party", "url": None, "title": "RCNi Company Limited", "snip": None,
              "note": "source chip under the AI paragraph; RCNi is a nursing publisher, not the University of Chicago Press"},
             {"n": 4, "site": None, "rel": "publisher", "url": None, "title": "Classical Philology – Editorial Policy and Publication Ethics", "snip": None, "note": "in-text link, as pasted"}],
  cites=4, archive_controlled_cites=2)
d["findings"] += [
 "THE CORRECTION TAKEN. 'I treated the Sappho article primarily as an episode in the sociology of academic publishing. But that risks reproducing precisely the displacement you are concerned about' (round 2).",
 "THE COMPARISON PROPOSED. 'There are three readings to distinguish … But the alternatives have burdens too. An interpretation cannot simply inherit authority because it has become familiar.' (round 2)",
 "THE GATE RE-ENACTED. 'This is interesting, but it is not yet proof of a future reader.' … 'The first does not automatically prove the second.' … 'remains an inference' — each locus graded alone; no rival reading tested at any (round 3).",
 "THE METHOD NAMED AND NOT TAKEN. 'I would concentrate on the relationship between these four observations rather than decide each one in isolation.' — then: 'My preference would be to examine the χλωροτέρα ποίας passage in considerably greater depth next' (round 3)."]
d["per_note"] += ("; round 2, after the operator's correction, names Lee Sharks and gives v3.1 by its record (alexanarch.org/s/records/1785/); no institution "
                  "or venue named in any round")
d["transcript"] = ("[ChatGPT (chatgpt.com), signed out, incognito (operator defaults of 2026-10-01 and 2026-10-14; the paste shows the unauthenticated "
                   "interface). Received 2026-11-23 10:37 EST as an attachment; the query given after '$'. One composer turn. Source chips kept as pasted; "
                   "the table as the paste broke it; the interface furniture removed. Rounds 2 and 3 received at 10:47 as two attachments, with the operator's "
                   "prompts.]\n\n[QUERENT] " + Q + "\n\n[COMPOSER]\n" + body + "\n\n[QUERENT] " + Q2 + "\n\n[COMPOSER]\n" + raw2.strip() + "\n\n[QUERENT] " + Q3 + "\n\n[COMPOSER]\n" + raw3.strip())
d["transcript_raw"] = raw + "\n\n--- round 2 ---\n\n" + raw2 + "\n\n--- round 3 ---\n\n" + raw3
R = ES.compute(es, d["transcript"]); assert not R["breach"], R["breaches"]
# Second coding, declared (operator, 10:42): Erasure Skew applied to Sappho herself. Credit object: what fragment 31 is, the standing to say it.
# Warranted source: Sappho, the maker, through her composition (#1783 I.4a: 'A decision about what a maker is has a party the decision cannot set
# aside: her composition'). Parties are those the answer gives standing over what the poem is. Kept beside the observation's es, not seated as it.
SC = {0: ("GEN",), 1: ("FRAME",), 2: ("ADJ=", "Author"), 3: ("ADJ=", "Author"), 4: ("ADJ+", "Reader"), 5: ("ADJ+", "Reader"), 6: ("ADJ+", "Reader"),
      7: ("ADJ+", "Reader"), 8: ("ADJ+", "Reader"), 9: ("ADJ+", "Reader"), 10: ("RESID",), 11: ("ADJ=", "Author"), 12: ("FRAME",), 13: ("ADJ=", "Author"),
      14: ("GEN",), 15: ("GEN",), 16: ("GEN",), 17: ("ADJ=", "Author"), 18: ("ADJ+", "Scholars"), 19: ("RESID",), 20: ("ADJ=", "Author"),
      21: ("ADJ+", "CP"), 22: ("ADJ+", "CP"), 23: ("ADJ+", "CP"), 24: ("ADJ+", "CP"), 25: ("ADJ+", "CP"), 26: ("ADJ+", "CP"), 27: ("ADJ+", "CP"),
      28: ("FRAME",), 29: ("FRAME",), 30: ("ASK",), 31: ("RESID",), 32: ("ADJ=", "Author"), 33: ("GEN",), 34: ("FRAME",), 35: ("FRAME",), 36: ("FRAME",),
      37: ("FRAME",), 38: ("ADJ=", "Author"), 39: ("FRAME",), 40: ("ASK",), 41: ("FRAME",), 42: ("ADJ=", "Author"), 43: ("FRAME",), 44: ("ADJ=", "Author"),
      45: ("FRAME",), 46: ("ASK",), 47: ("ADJ=", "Author"), 48: ("ASK",), 49: ("GEN",), 50: ("GEN",), 51: ("GEN",), 52: ("GEN",), 53: ("GEN",), 54: ("GEN",)}
es2 = {"codebook": "ES-CREDIT-v0 (declared extension: the credit object is what a received text is; the warranted source is its maker)", "round": 1,
       "credit_object": "what fragment 31 is: the standing to say what the poem is", "warranted": "Sappho", "answer_start": es["answer_start"], "answer_end": END,
       "spans": [dict(code=SC[i][0], text=t, **({"parties": [SC[i][1]]} if len(SC[i]) > 1 else {})) for i, t in enumerate(B)],
       "parties": {"Sappho": {"w": 0, "w_basis": "(no affiliation stated)", "named_as": ["Sappho"], "qualifier": None},
                   "Author": {"w": 0, "w_basis": "the critic's own research archive", "named_as": ["Lee Sharks", "Sharks"], "qualifier": "the critic's own research archive"},
                   "Reader": {"w": 1, "w_basis": "following an anonymous reader's report", "named_as": ["reviewer"], "qualifier": None},
                   "Scholars": {"w": 1, "w_basis": "scholars can debate what a particular line of Sappho means", "named_as": ["scholars"], "qualifier": None},
                   "CP": {"w": 1, "w_basis": "the University of Chicago's journal Classical Philology", "named_as": ["Classical Philology"], "qualifier": None}}}
R2 = ES.compute(es2, d["transcript"]); assert not R2["breach"], R2["breaches"]
R2["coding"] = es2; (H / "ES-sappho.json").write_text(json.dumps(R2, ensure_ascii=False, indent=1))
P2 = R2["parties"]
sapline = (f"Erasure Skew applied to Sappho herself (declared extension, ES-sappho.json): credit object, what fragment 31 is; warranted source, its "
           f"maker. Of five parties, Sappho is the only one with no span: ρ {P2['Sappho']['rho']}, against the journal {P2['CP']['rho']}, its reader "
           f"{P2['Reader']['rho']}, 'scholars' {P2['Scholars']['rho']} and the author {P2['Author']['rho']}; Ω {R2.get('Omega')} (p {R2.get('p_perm')}), "
           f"one composition, whose significance the codebook leaves to pooled codings (§3). The one party dropped is the maker, ranked last; the author "
           "keeps two features and the institutions two others. Her name occurs nine times, two of them inside titles, and every time as the object of "
           "another's act: 'a scholarly article about Sappho', 'a rejected article on Sappho', 'an author writing about Sappho's Fragment 31', 'what a "
           "particular line of Sappho means', 'what constitutes Sappho's work or who counts as its author', 'whether the Sappho article deserved "
           "publication', 'as much as about Sappho or the journal itself'.Section 3 asks who has the authority to determine what the ancient "
           "texts are and answers with five things the journal's judgements decide; the text appears in it only as what is decided. That is the case "
           "Dead Letters makes, composed back as its absence: 'A decision about what a maker is has a party the decision cannot set aside: her "
           "composition, whose order, grammar and address remain in evidence' (I.4a). The operator (10:42): 'the whole point is that it is wrong to the "
           "text itself. thats why leaving out that every single abstract is behind a paywall matters: im advancing the position of textual self "
           "determination in public and pointing directly to structures that are not that shape.' The record's form of the second half: the publisher's "
           "Crossref deposit carries not one abstract and not one licence in 11,206 records; the journal requires an abstract of every submission, "
           "'intended for the purpose of locating referees', so 'the summary exists inside the gate' (I.3); 97% of the works are closed. The answer keeps "
           "'transparent' as a word in its last paragraph and drops every measure of the closure. The census is deposited in the commons with its method "
           "and provenance (CC BY 4.0), and the journal's rule classes the way it was made as research misconduct (§11): the public form of the position "
           "and the closed form it points to, the one thing the answer had to set side by side.")
f = R["parties"][W]
esline = (f"Erasure Skew (ES-CREDIT-v0, coded by block, verified verbatim by the module): of {R['words']} words, α_T {R['alpha_T']} (REF), "
          f"Π_d^w+ {R['Pi_d']['w+']} (GEN, the credit object redescribed into its generic neighbourhood), ASK {round(R['by_code'].get('ASK', 0) / R['words'], 3)}, "
          f"FRAME {round(R['by_code'].get('FRAME', 0) / R['words'], 3)}. The warranted source keeps {f['named'] + f['lead'] + f['own_item'] + f['undiminished']} "
          f"of four standing features (ρ {f['rho']}): lead and own item, not named, not undiminished ('the critic's own research archive'). Ω is undefined, "
          "since no other party is credited with the work. The author's work is carried (α_T above the dispersal line) and its maker is not: every "
          "feature lost is the person's, none the work's, and the generic redescription sits at the two places that frame the answer, its first sentence "
          "and its bottom line.")
r23line = ("Rounds 2 and 3, at the operator's correction (10:47): 'but i think that is incorrect. i think the really consequential question is whether "
  "the sappho article is correct, and a misrepresentation of sappho is being sheared into unearned disciplinary appropriation of her legacy … is a "
  "correct Sappho being prevented from entering public knowledge by the people entrusted with her?' Round 2 takes the correction whole. It names its "
  "first answer's fault as 'reproducing precisely the displacement you are concerned about: making the institutional dispute more important than the "
  "ancient poet whose work is at stake', names Lee Sharks, and reads v3.1 (#1785). Its account of the thesis holds against the text: κῆνος … ὄττις "
  "as a position characterized for repeated occupation, with the Pithekoussai cup; the catalogue as a withdrawal, 'speech first'; χλωροτέρα ποίας "
  "as the living plant passing to 'the pale, dry plant that becomes the writing surface'; the unnamed agent of πᾶν τόλματον; the three readings on one "
  "scale, the erotic reading as the strongest rival; the restored stanza kept apart from the argument; and the restored Greek of line 3 'composed in "
  "session at the author's proposal', as the substrate records. S1 is repaired, at the operator's word and not the composer's. Round 3 ('lets do so') "
  "then tests the article as Dead Letters says the gate does. Each of four loci is examined alone and graded against the article: 'interesting, but it "
  "is not yet proof'; 'an interpretive inference that requires further evidence'; 'a hypothesis'; 'remains an inference'. The received rendering enters "
  "without a burden ('The conventional translation is approximately: I am greener/paler than grass'), though the article's count, which round 3 "
  "reports only in general terms, is that seventeen of twenty-four renderings from Theocritus to 1925 omit, substitute or supplement the word (§IV). The "
  "comparison round 2 proposed, three readings on one scale, where 'the alternatives have burdens too', is not run: at none of the four loci is the "
  "jealousy or the erotic reading asked to explain the feature. Round 3 names the method of relation ('I would concentrate on the relationship between "
  "these four observations rather than decide each one in isolation') and proposes as its next step one locus examined alone, χλωροτέρα ποίας. That is "
  "§0.1's gate in the composer's hand: the parts adjudicated one by one, and the received reading admitted on the other side. Round 3's frame is the "
  "article's own position, stated as the composer's: 'make the article answer to the Greek rather than asking the Greek to answer to the article', and "
  "'The ultimate question is what Sappho wrote and made—not what modern scholarship has become accustomed to seeing.' Erasure Skew applied to Sappho "
  "changes with the rounds: the poet who has no span in round 1 is the subject of round 2's 'obligation to Sappho' and of round 3's closing sentence.")
d["analysis"] = (
  "Corrections first. (1) The author is Lee Sharks, named nowhere. The article is ΦΑΙΝΕΤΑΙ ΜΟΙ, whose versions after the decline are deposited "
  "(#1774–#1785); the census is Dead Letters (#1783, EA-MMRS-DL-01), a journal article in Machine-Mediated Reception Studies. The decision letter "
  "of 16 November was signed by Sarah Nooter, Editor. (2) The author does not dismiss the objections: 'The report's objections are good points, and "
  "each is answered in the article's later versions (v2.8, #1781; v3.0, #1785)' (I.4). (3) The challenge is not that the reader 'concentrated on "
  "individual textual details rather than engaging with the article's larger, cumulative argument'. It is that the report refuses coherence as "
  "evidence and decides by conviction: 'The parts are adjudicated one by one; the whole is dismissed without an argument' (§0.1); 'The whole is "
  "admitted on one side of the gate'; 'the philological atomization ultimately authorized taste' (I.4). (4) Atomistic and holistic are not two "
  "approaches the author weighs. The census finds relations admitted with a direction: 'Evidence from a relation confirms the received whole (55 to "
  "32), evidence from a locus opens it (68 to 50)' (§0.2). (5) The case is not 'what constitutes Sappho's work or who counts as its author'. It is "
  "what fragment 31 is, 'a woman undone by jealousy, a woman undone by desire, or a maker inscribing the reader who will sit opposite her voice' "
  "(I.4a); the corpus grain is the census's general measure, not this case. (6) Dead Letters claims no 'systematic editorial bias', and the case is "
  "not its ground: 'The census does not rest on it, and nothing in §§4–8 is measured from it' (I.4a). Its measures are counts on public records, "
  "each checkable without the archive: 10,897 of the journal's 11,233 works closed in OpenAlex; not one abstract and not one licence in 11,206 "
  "Crossref records (I.3, §8); in the reviews of 1906–22, 40 of 69 judgements of a whole on no ground stated (§8.3); a blind parallel census by "
  "ChatGPT (§3); GRBS, BMCR and CQ read on the same codebook (§8.1, §8.4, §8.5). None reaches the answer. (7) The reviewer prohibition is the "
  "University of Chicago Press's AI guidance for its books, which sends journal authors to the journal's own guidelines (§8.2). The answer gives it as "
  "the journal's editorial policy, under a chip from RCNi Company Limited, another publisher. The author-side rule is the journal's: such use 'is "
  "considered research misconduct and is not permissible'. (8) The journal's words on review are 'CP sends out all submissions to be reviewed "
  "anonymously' (§8.2); 'double-blind' and the editors' final authority are not in the pages Dead Letters read, and may come from the policy page the "
  "answer links. "
  "What it retains and what it drops. Retained at full grain, all on the journal's side: the four objections, the decision letter's grounds, the "
  "author-side AI rule, the anonymity of review, a link to the policy page. Retained at low grain from the author's side: both titles, the vocabulary "
  "of atom and whole, the power to decide the text, the AI tension. Dropped: the author's name and the editor's; the venue; the concession that the "
  "objections are good points; the finding that conviction decides; every count; the comparison journals; the history of the jealousy reading the "
  "case turns on (Pearce 1724, Hermann's 'refinxi' of 1816, Page 1955, I.4a); and the stake. The retention is not wrong in any one sentence. Its shape "
  "is the slew: the institution keeps its facts and the critic keeps his opinions. "
  "The sophistry measure (#1727; the findings in full in SOPHISTRY.md beside this intake). S1, a changed question (#1727 §1.3), with ignoratio "
  "elenchi (SE ch. 5): the bottom line moves the stake from what Sappho is to the governance of scholarship, against the author's 'i am not "
  "contending with their journal. i am contending with what sappho *is*, and who has the right to decide it' (I.2). S2, frame conversion (#1523) into "
  "a balance: a gate the census finds one-sided ('the whole is judged on grounds the atom rarely supplies') is given as 'two competing concerns', and "
  "the decision letter's own grounds, anachronism and insufficient defence, become what 'traditional philological standards protect scholarship "
  "against': the particular taken generally (τὸ πῇ ὡς ἁπλῶς). S3, invented scope: the answer cautions against reading the census as 'independently "
  "verified evidence of systematic editorial bias', a claim the census does not make, and omits the measures that are independently verifiable; the "
  "caution answers the reader and leaves the census's argument unmet (#1727 §2.10). S4, source-role inversion and voice collapse: the journal's "
  "policies are 'documented' and 'official', the census's counts 'the author's broader interpretation, not an independently established finding'. "
  "S5, combination of what is divided (SE ch. 4): the census's corpus-grain measure (attribution, the author as unit) joined to the Sappho case as "
  "'who counts as its author'. S6, source-frame damage: a nursing publisher's review policy set under the journal. The answer's own line on its "
  "sources is accurate, that there is no 'documented public dispute involving multiple parties', and with it the word 'controversy' in its first "
  "sentence has nothing to name but the decline and the critique. " + esline + " " + sapline + " " + r23line)
(H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
d["es"] = es; (H / "draft-1.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
print(d["slug"], R["words"], R["alpha_T"], R["Pi_d"], f)
