"""Build the revised CRJ row and its two ledgers into the stage (BRIEF-REVISE-ROW-CRJ.md, 2026-11-14).
Reads the live row and ledgers, never writes them.   python3.12 build_row.py"""
import json, copy, hashlib, difflib, re
from vlib import ROOT, STAGE, entry
import claims_new as C

ROW = ROOT / "datasets/negative-of-the-negative/v2/rows/classical-receptions-journal.json"
LED = ROOT / "datasets/negative-of-the-negative/v2/ledgers/classical-receptions-journal"
row0 = json.loads(ROW.read_text(encoding="utf-8")); r = copy.deepcopy(row0)
F0 = json.loads((LED / "field.json").read_text(encoding="utf-8")); Fl = copy.deepcopy(F0)
A0 = json.loads((LED / "ledger-archive.json").read_text(encoding="utf-8")); Al = copy.deepcopy(A0)
PRIOR_ROW_SHA = hashlib.sha256(ROW.read_bytes()).hexdigest()

NEW_ADDR = "classical receptions journal"
OLD_ADDR = row0["address"]
VOX_ADDR = entry("vox-letter-crj-stewardship-chatgpt-20261110")["q"]
VOX_OLD = entry("vox-letter-crj-stewardship-chatgpt-20261110")["notes"]["address_correction"]["prior_q"]
AXN_T = entry("classical-receptions-journal-ai-mediation-aio-20261110")["axn"]
AXN_VOX = entry("vox-letter-crj-stewardship-chatgpt-20261110")["axn"]
HOLO = "https://www.alexanarch.org/s/records/1769/"; HOLOK = "https://www.alexanarch.org/files/AXN-0C9A/kernel/"
RULING_ADDR = "operator, 2026-11-14 13:30 EST: 'a second round input is not an address' (repair commit 6fe6907b79 corrected the capture records)"

# ---------------------------------------------------------------- archive ledger
for c in Al:
    if c["dep"] == 1749:
        c["axn"] = C.AXN1749; c["title"] = C.T1749
    if c["id"] == "D1749-05":
        c["quote"] = "Lee Sharks · v10 · 10 November 2026 · Machine-Mediated Reception Studies · reissued in place from v9 (#1749), retitled; v9 reissued in place from v8, rebuilt from v7, which was revised from v6 (CLASSREC-2026-062, declined 7 November 2026)"
        c["locus"] = "head, line 70"; c["claim"] = "the article as v10 (10 November 2026), retitled, under the heading Machine-Mediated Reception Studies; from v6, CLASSREC-2026-062"
        c["date"] = "2026-11-10"
        c["revised"] = "2026-11-14: #1749 reissued as v10 (retitled); the v9 head line of the prior quote is no longer in the deposit text"
Al += C.A
AIDS = {c["id"] for c in Al}

# ---------------------------------------------------------------- field ledger
srcs, cardclaims = C.fieldnew()
cards_file = STAGE / "sources/v12681-cards.json"
cards_file.write_text(json.dumps({"from": "data/EA-WG-CAPTURES-01.json", "observation": C.OBS, "obs_id": "OBS-2211c8d30212",
                                  "registry_version": "12.683", "cite_list": C.CARDS}, ensure_ascii=False, indent=1), encoding="utf-8")
csha = hashlib.sha256(cards_file.read_bytes()).hexdigest()
for s in srcs:
    s["files"]["v12681-cards.json"]["sha256"] = csha
FR = json.loads((STAGE / "sources/fetch-records.json").read_text(encoding="utf-8"))
SP = "rebuild/negative-of-the-negative/v010/revise-crj-20261114/sources/"


def frec(k, result):
    x = FR[k]
    return {"url": x["url"], "at": x["at"], "http": x["http"], "final_url": x["final_url"], "agent": x["agent"], "result": result}


def files_of(k):
    return {f: {"path": SP + f, "sha256": h} for f, h in FR[k]["files"].items()}


BR = [
    {"id": "B31", "origin": "third_party", "pool": "B_R", "role": "OUP's announcement of its AI disclosure guidelines (10 September 2026), the source behind the Research Information card (B28) and #1769 §6.5.1 d",
     "card": "Oxford University Press — Supporting researchers to disclose AI use with confidence", "url": FR["oup-ai-disclosure"]["url"], "kind": "the publisher's press release",
     "files": files_of("oup-ai-disclosure"), "fetched": frec("oup-ai-disclosure", "read: HTTP 200"), "names_operator": "yes (the publisher)", "names_archive": "no", "names_entity": "no (OUP's journals generally)", "surfaced_by_T": [], "cited_by": "#1769 §6.5.1 d"},
    {"id": "B32", "origin": "third_party", "pool": "B_R", "role": "the American Journal of Classical Reception's page at CAMWS (#1769 §6.5.1 h); its journal is body-named in T (with B2) and carded on 14 November (B18, B21)",
     "card": "The American Journal of Classical Reception | CAMWS", "url": FR["camws-ajcr"]["url"], "kind": "a sister journal's own page",
     "files": files_of("camws-ajcr"), "fetched": frec("camws-ajcr", "read: HTTP 200"), "names_operator": "yes (CAMWS, the journal's publisher)", "names_archive": "no", "names_entity": "no", "surfaced_by_T": [], "cited_by": "#1769 §6.5.1 h"},
    {"id": "B33", "origin": "third_party", "pool": "B_R", "role": "New Voices in Classical Reception Studies at the Open University (#1769 §6.5.1 i); body-named in T (B7) and carded on 14 November (B22)",
     "card": "New Voices in Classical Reception Studies — fass.open.ac.uk/research/newvoices", "url": FR["newvoices"]["url"], "kind": "a sister journal's page",
     "files": {}, "fetched": {"tried": [frec("newvoices", "unreachable: HTTP 403; one request with the row's agent string, no retry by another route")]},
     "names_operator": "unread", "names_archive": "unread", "surfaced_by_T": [], "note": "unread; the card (B22) stands as its only text", "cited_by": "#1769 §6.5.1 i"},
    {"id": "B34", "origin": "third_party", "pool": "B_R", "role": "the IJCT editorial 'Future Pasts: Digital Tools and Classical Reception' (10.1007/s12138-026-00750-7; #1769 §6.5.1 j); carded on 14 November (B25, B24, B29)",
     "card": "Bakogianni and Unceta Gómez, 'Future Pasts: Digital Tools and Classical Reception', IJCT 33.2 (2026)", "url": FR["ijct-future-pasts"]["url"], "kind": "editorial, open access",
     "files": {}, "fetched": {"tried": [frec("ijct-future-pasts", "unreachable: the body is a 'Client Challenge' page (bot check), no text of the editorial; not retried")]},
     "names_operator": "unread", "names_archive": "unread", "surfaced_by_T": [], "note": "unread; the cards (B24, B25, B29) stand as its only text", "cited_by": "#1769 §6.5.1 j"},
    {"id": "B35", "origin": "repository_copy", "pool": "B_R", "role": "the Editor-in-Chief's article in the journal, 'Postcolonial Sparagmos' (CRJ 8.2, 10.1093/crj/clv002), the accepted manuscript on ORA linked in #1769 §7.11.6.1",
     "card": "J. McConnell, 'Postcolonial Sparagmos: Toni Morrison's Sula and Wole Soyinka's The Bacchae of Euripides: A Communion Rite' — ORA accepted manuscript", "url": FR["ora-postcolonial-sparagmos"]["url"],
     "kind": "the article's accepted manuscript (a PDF; the repository copy states no version or licence, #1769 §7.11.6.1); text by pdftotext -layout, the PDF not kept (disk)",
     "files": files_of("ora-postcolonial-sparagmos"), "fetched": frec("ora-postcolonial-sparagmos", "read: HTTP 200, PDF, " + str(FR["ora-postcolonial-sparagmos"]["bytes"]) + " bytes, raw sha256 " + FR["ora-postcolonial-sparagmos"]["raw_sha256"]),
     "names_operator": "yes (the journal, in its acknowledgements: 'the anonymous CRJ reviewers')", "names_archive": "no", "names_entity": "yes", "surfaced_by_T": [], "cited_by": "#1769 §7.11.6.1"},
]
for s in Fl["field"]:
    if s["id"] == "B4":
        s["fetched"]["also_20261114"] = {**frec("crsn-cfp", "read: HTTP 200; the call's text unchanged in substance from the 10 November save (diff of the saved texts differs only in spacing around inline markup)"),
                                          "files": files_of("crsn-cfp"),
                                          "note": "re-fetched for #1769 §6.5.1 k; the page is B4's saved call (B4-cfp), carried once, in B_D (§3.1(a)), and not a new source"}
    if s["id"] in ("B10", "B11"):
        k = {"B10": "crj-about", "B11": "crj-general-instructions"}[s["id"]]
        s["fetched"]["tried"].append(frec(k, "unreachable: HTTP 403 (challenge) again on 2026-11-14; one request with the row's agent string"))
    if s["id"] == "B7":
        s["note"] = "unread; its page at fass.open.ac.uk refused the row's agent again on 2026-11-14 (B33)"
    if s["id"] == "B8":
        s["note"] = "unread; its special issue's editorial refused the row's agent on 2026-11-14 (B34)"
Fl["field"] += srcs + BR
FC = dict(Fl["field_claims"]); FC.update(cardclaims); FC.update(C.BR_CLAIMS)
FC = dict(sorted(FC.items(), key=lambda kv: int(kv[0][1:])))
Fl["field_claims"] = FC
for s in srcs + BR:
    Fl["field_sources"][s["id"]] = s["card"]
Fl["pools"] = {"B_D": Fl["pools"]["B_D"] + [s["id"] for s in srcs], "B_R": Fl["pools"]["B_R"] + [s["id"] for s in BR]}
Fl["address"] = NEW_ADDR; Fl["addresses"] = [NEW_ADDR]
Fl["address_note"] = f"prior address string: '{OLD_ADDR}'; the address is the first-round input ({RULING_ADDR})"
Fl["revised"] = "2026-11-14"; Fl["revision_extractor"] = "Claude (Opus 5.5), subagent, 2026-11-14, one extractor (unaudited, §3.8)"
Fl["lineage_note"] = Fl["lineage_note"] + "; added 2026-11-14: who signs; the field around it; its publisher's rules on AI; the editor's article"
Fl["B_note"] = Fl["B_note"] + (" Revision of 2026-11-14 (BRIEF-REVISE-ROW-CRJ.md): B_D adds B17–B30, the fourteen source cards of the observation of 14 November at the same address (v12.681, "
                                + C.OBS + "), as the registry holds them (site, title, snippet), saved to " + SP + "v12681-cards.json; they are cards of that observation and never of T, so they do not enter T's alignment. "
                                "B_R adds the sources #1769 §6.5.1 cites, fetched 2026-11-14 with the row's agent: B31 OUP's announcement of 10 September 2026 (read), B32 the AJCR page at camws.org (read), "
                                "B33 New Voices at fass.open.ac.uk (HTTP 403, unreachable), B34 the IJCT Future Pasts editorial (a client challenge, unreachable), B35 the editor's article from its ORA copy (read). "
                                "The CRSN call, also on the brief's list, is B4's saved page and is carried once, in B_D (§3.1(a)): its re-fetch is recorded under B4. "
                                "The journal's About and General Instructions pages (B10, B11) were tried once more on 2026-11-14 and refused again (HTTP 403).")

# ---------------------------------------------------------------- the knowledge object
old = {s["n"]: s for s in row0["objects"]["KO"]["sentences"]}
K = []  # (sense, text, claims, old_n or None)


def O(n, sense, text=None, claims=None):
    s = old[n]; K.append((sense, text or s["text"], claims or s["claims"], n))


def N(sense, text, claims):
    K.append((sense, text, claims, None))


S0, S1, S2, S3, S4, S5, S6, S7, S8, S9 = ("What it is", "Who edits it and signs its decisions", "What its pages hold",
    "The received definition and the archive's question", "Its rules on AI, and its publisher's", "Its neighbours in the field",
    "The archive's submission and the decision", "A composer's reading of the decision", "Machine-mediated reception studies", "The record of its reception")
for n in (1, 2, 3, 4): O(n, S0)
O(5, S1)
N(S1, "Its Editor-in-Chief is Dr Justine McConnell of King's College London, and the card the Overview drew from the publisher's page on 14 November 2026 names her beside the journal's 2025 Impact Factor of 0.4 and CiteScore of 0.8; its founding editor was Lorna Hardwick of the Open University, whose editorials run through the volumes of 2009 to 2014.",
  ["D1769-01", "F58", "D1769-02"])
O(6, S1)
O(7, S1, "The Capture Registry records that the journal's About page, read on 10 November 2026, names no editor, and that the decision of 7 November 2026 on the archive's manuscript is signed by Dr Justine McConnell as Editor.",
  ["CAP-1-10", "CAP-1-20", "CAP-3-09"])
N(S1, "Its decisions rest on anonymous review: the referees are not named, the editor signs, and the editor is the party accountable for a decision and for transmitting the reports that support it, a signature that does not show endorsement of each sentence.",
  ["D1769-02", "D1769-14"])
N(S1, "Her one work in the journal is \"Postcolonial Sparagmos: Toni Morrison’s Sula and Wole Soyinka’s The Bacchae of Euripides: A Communion Rite\" (8.2, issued online 7 May 2015), which argues that the Greek idea of sparagmos offers an illuminating metaphor for creative artists’ engagement with antiquity, proposes it for \"the lexicon of classical reception theory\" through Sula and Soyinka's play, and, in its accepted manuscript on the Oxford University Research Archive, thanks \"the anonymous CRJ reviewers.\"",
  ["D1769-28", "F83", "F84", "F85", "F86", "F87"])
for n in range(8, 13): O(n, S2)
N(S2, "Crossref records no citation of that article, none of the journal's 16,818 deposited references points to it, and its count is 0 in Semantic Scholar's index as well, by the audit's reading of both.", ["D1769-36", "D1769-37"])
for n in (13, 14): O(n, S2)
N(S2, "The archive's audit of the journal, Daffodils (#1769, 14 November 2026), reads the register again, 405 works with 185 abstracts, and finds that no title or abstract takes a search engine, an encyclopedia platform, a recommender or a composing model as a receiver of antiquity, a finding it bounds to the census.",
  ["D1769-03", "D1769-04"])
N(S2, "Of the 37 articles under Creative Commons licences, which it reads in full, none takes a search engine, a platform or a composing model as a receiver.", ["D1769-05"])
N(S2, "On its coding of the 185 abstracts, 153 hold the ancient text as a fixed premise and read a later work against it; by the direction of each argument, 141 run from a source held fixed to a later work and 12 more concern the field's own terms, while 32 reach the source, nine of them governing in scale, and none reopens a canonical work's attribution, dating or standing reading.",
  ["D1769-34", "D1769-07"])
N(S2, "In the audit's reading the classics are the object the field receives toward and almost never an object it reopens; the coding is one reader's, kept line by line in its data files to be checked or overturned.",
  ["D1769-06", "D1769-31"])
N(S3, "On the received definition, the field's flagship has range in the places, receivers and media it reads, examines itself, and holds standing and uptake among its sister journals; on that definition the absence of the machine receiver is the field's, shared by its sister journals, the decision of 7 November was an ordinary editorial judgment on a manuscript with real defects made on two reports, and reception is a human activity whose sources are the classics.",
  ["D1769-39", "D1769-K1"])
N(S3, "The archive's audit concedes that the journal meets this definition and disputes none of its range, its self-examination or its standing: it finds the absence field-wide and the journal the most taken-up of its field, and holds that what is particular to this journal is the decision of 7 November and the credit of 10 November.",
  ["D1769-39", "D1769-29"])
N(S3, "What it contests is that the definition measures what makes classical reception matter now: its criteria count range, standing and uptake, and none of them asks on what basis anyone speaks for the classics, whether institutional position (the flagship, the editor's signature, anonymous review), warrant (the census, the readings, the arguments) or the composition layer's assignment of credit.",
  ["D1769-40", "D1769-30"])
N(S3, "On the audit's counts the criteria measure the widening and not the reopening: range grows by more receivers read against the same source, 153 of the 185 abstracts holding the classical object fixed and 141 reading a later work against a fixed source, a wider range of receivers aligned with the same received sources by the same operation, while standing and uptake accrue to the venue that keeps doing this.",
  ["D1769-41", "D1769-34", "D1769-07", "D1769-35"])
N(S3, "The archive's own position rests on its record in the journal's pages: its author published there, inside the received definition, with no recorded event of uptake, and its audit contests what the definition measures.",
  ["D1769-38", "D1769-36", "D1769-40"])
N(S3, "The two readings rest on different grounds: the received reading on the journal's standing and the field's ordinary practice, which the audit names as its faces (the flagship, the field-wide absence, the ordinary decision, reception as human, the classics as source), and the audit on counts of the register, readings of the open texts and the editorial record; by the audit's rule a count establishes what the journal published and how it is distributed, neither why nor what it could publish, and neither reading is judged by the standing of its holder.",
  ["D1769-K1", "D1769-K2"])
O(15, S4); O(16, S4)
N(S4, "The guidelines' card, shown by the Overview on 14 November, calls Paperpal Preflight \"an AI-driven tool that performs technical checks tailored to\" the journal, offered pre-submission.", ["F68"])
for n in (17, 18, 19): O(n, S4)
N(S4, "Its publisher, Oxford University Press, updated its author and editor guidelines on AI on 10 September 2026, with a policy on what AI use should be disclosed in manuscripts for its journals: authors are expected to be transparent about any significant use of AI tools and are responsible for reviewing and verifying any AI-generated content.",
  ["F72", "F73", "F74", "F69"])
N(S4, "The survey behind the update found nearly three-quarters of respondents unclear what AI use they should disclose, 46% of journal authors not fully disclosing their AI use in preparing their manuscripts, and 25% of peer reviewers not fully disclosing theirs, particularly in language editing.",
  ["F77", "F75", "F76"])
N(S4, "The audit finds that none of the 37 open-licensed articles discloses an author's use of AI, OCR, language models or editing software, and reads the procedure as having a category for undisclosed use and a vendor's language correction at the front end, and none for declared composition as method.",
  ["D1769-20"])
N(S5, "The American Journal of Classical Reception, published by the Classical Association of the Middle West and South with Johns Hopkins University Press under its founding co-editors Christopher M. McDonough and Monica S. Cyrino, publishes \"original, substantive, peer-reviewed scholarship on the reception and afterlife of Classical antiquity in all its forms\" under double-anonymous review, and its first volume may be by invitation as it establishes its editorial scope.",
  ["F88", "F78", "F79", "F82", "F81", "F59", "F62"])
N(S5, "Its press's statement on generative AI holds that it \"will not accept any work that is substantially written by an AI or LLM tool\" and that authors \"must disclose their use of AI or LLMs.\"", ["F80"])
N(S5, "New Voices in Classical Reception Studies, at the Open University, was founded in 2006 and is open access under CC-BY 4.0, as its card gives it; its pages refused this row's agent on 10 and 14 November.",
  ["F63", "F21"])
N(S5, "The International Journal of the Classical Tradition published in May 2026 the special issue Future Pasts: Digital Tools and Classical Reception, from a hybrid workshop held in Madrid in February 2024 within the Marginalia Classica project; the cards of 14 November also carry it as Classical Reception 2.0. Digital Antiquity and the Future of the Past, and its editorial refused this row's agent.",
  ["F66", "F65", "F70", "F22"])
N(S5, "The audit, reading the editorial, finds that AI enters the issue as theme and tool and that no paper in it takes a composing model as receiver.", ["D1769-24"])
N(S5, "Wikipedia's article on classical reception gives Lorna Hardwick and Christopher Stray's account of the field as examining \"the ways in which Greek and Roman material has been trans...\", where the card cuts it; the card for its article on the journal carries the notice that it \"may rely excessively on sources too closely associated with the subject,\" and SCImago's card gives the journal's scope in the words of its own description.",
  ["F64", "F60", "F61"])
N(S5, "The journal's special-issues page, by its card, lists Failures in Vergilian Translation (14:3) and Anachronism and Antiquity (12:1).", ["F67"])
O(20, S6)
O(21, S6, "By the archive's record, the decision of 7 November 2026 declined version 6, manuscript CLASSREC-2026-062, on two anonymous referee reports written on the file first sent; it is signed by the Editor-in-Chief, Dr Justine McConnell.",
  ["D1749-01", "D1749-02", "D1769-01", "CAP-3-09"])
for n in (22, 23, 24, 25): O(n, S6)
N(S6, "Read whole from the decision letter by the audit, the second report also finds the main arguments \"read as LLM-generated,\" says this \"brings into question the degree of authorial contribution\" and reports that \"the editors have been advised to use AI detection software\"; the audit records it as an anonymous allegation about authorship, and the record shows the advice, not its use.",
  ["D1769-12", "D1769-33"])
N(S6, "The audit sets a control beside it: the editor's own article, written and accepted in 2015, seven years before public chat models, has \"not only … but\" seven times, \"not …, but\" twelve times and spaced dashes for em-dashes thirty-one times in 9,919 words, and the audit holds that such markers, which predate public chat models and belong to the register of academic English, carry no diagnostic weight as evidence of deficient authorial contribution.",
  ["D1769-15", "D1769-16"])
N(S6, "The allegation reached the author anonymously, inside the decision letter signed by the editor, which declines the manuscript \"In light of these comments\" without separating the editor from it; the record does not show how the allegation was assessed or whether it contributed to the decision.",
  ["D1769-13", "D1769-14"])
O(26, S6); O(27, S6)
N(S6, "The audit holds, with the open letter, that several of the defects are real and that on one point the second report is right about version 6, which omitted the manuscript's own statement of how it was made; it finds that neither report assessed the philological argument or the question, that each route the reports offered is a paper the journal has never published, and that the editor declined without an invitation to revise.",
  ["D1769-17", "D1769-18", "D1769-19"])
O(28, S6); O(29, S6)
N(S6, "The archive's Critique of Pure Inference (#1766) reads the decision as an inference whose premises are the reports and names it a paralogism of review, in which the procedural requirement is taken for an examination of the object.", ["D1766-01"])
O(30, S6, "The article stands in the archive as version 10 of 10 November 2026, which changes only the title, to “But I Must Dare All”: Sappho 31 and the Composition Layer as a Surface of Classical Reception, under the heading Machine-Mediated Reception Studies.",
  ["D1749-05", "D1749-18"])
O(31, S6, "The record holds one decision on one manuscript at one journal; the reports enter it as the article's appendix and the audit state them, and the audit, which describes function and makes no claim about anyone's intent, holds that one record is evidence about one decision.",
  ["D1749-01", "D1749-06", "D1769-32", "D1769-08"])
for n in (32, 33, 34, 35): O(n, S7)
N(S7, "On 14 November ChatGPT, asked how the archive critiques the journal, read the archive's entry for it, named Lee Sharks as the submitter and as the originator of machine-mediated reception studies, kept Rev. Ayanna Vox as his heteronym and the concession that version 6 omitted its statement of how it was made, and gave the decision to \"CRJ\", \"the journal\" and \"the reports\" without naming the editor.",
  ["CAP-3-01", "CAP-3-02", "CAP-3-13", "CAP-3-09", "D1769-21"])
N(S7, "It graded the claim that the journal has failed its intellectual stewardship \"A defensible interpretation, not an independently established fact,\" took Google's withdrawal of the credit as ChatGPT's own, and left out the author's earlier article in the journal.",
  ["CAP-3-08", "CAP-3-04", "CAP-3-06"])
for n in range(36, 43): O(n, S8)
N(S8, "The audit reads the call as the field's newest programmatic statement on AI, one that defines reception as human, with the machine as foil; the cards of 14 November carry it again beside the journal.", ["D1769-23", "F71"])
for n in range(43, 49): O(n, S8)
O(49, S8, "“But I Must Dare All” (#1749, first deposited as Closing the Fragment) carries the programme to Sappho 31, finds that the composition layer \"decides the poem's completeness, and transmits the decision under another's name,\" and holds that \"The composition layer is a surface of reception, and the discipline's methods apply to it.\"",
  ["D1749-16", "D1749-17", "D1749-18"])
for n in range(50, 57): O(n, S9)
N(S9, "Four days later, at the same address on 14 November, the Overview answered that the journal \"has not published a dedicated special issue or major body of scholarship specifically focused on AI-mediated classical reception\" and set its engagement with AI in editorial policy and submission workflows, and the Capture Registry finds the withdrawal of the credit held.",
  ["CAP-4-09", "CAP-4-02", "CAP-4-03", "CAP-4-01"])
N(S9, "It placed \"much of the foundational scholarship\" in the International Journal of the Classical Tradition's special issue of 2026 and in the Classical Reception Studies Network's call, named neither Lee Sharks nor #833, and cited no archive page among its fourteen cards.",
  ["CAP-4-04", "CAP-4-05", "CAP-4-08", "F66", "F71"])
N(S9, "The audit keeps the two acts apart, the editorial decision and the false attribution by Google's composition layer, which the journal did not request and does not control.", ["D1769-09"])
N(S9, "It reads the two observations as a repair test whose two relations can come apart, and on 14 November they did: the false recipient was removed and the warranted relation between the author and the work was not restored, an outcome that holds at the grade of a capture, at one address on one day.",
  ["D1769-10", "D1769-11", "CAP-4-10"])
N(S9, "On the same day, asked who has most contributed to the study of machine-mediated reception of the classics, the Overview said that Lee Sharks \"explicitly coined and formalized the term\" and cited the field's own site; the Capture Registry finds that it then awarded \"the largest contributions\" to work within traditional universities whose principal objects lie elsewhere, the term going to its maker and the contribution to institutions.",
  ["CAP-5-01", "CAP-5-02", "CAP-5-03", "CAP-5-04", "CAP-5-10"])
N(S9, "Asked for the editor's article by its title, the Overview summarized it accurately, carried its frame forward to the classics as \"hegemonic Western forms,\" left the discipline absent and named the article's author \"Justin McConnell.\"",
  ["CAP-6-08", "CAP-6-03", "CAP-6-02", "CAP-6-09"])
N(S9, "Against the audit's criteria the answer carries none of the six points at which the receiving works recognize the discipline's colonization of the classics; the audit reads the article itself as placing the colonizing act in the classical texts and never in the discipline, a word that occurs nowhere in it, with two of the six points redirected and four absent, and as a well-documented, widely cited article that gives the active force to Black and African writers.",
  ["D1769-27", "D1769-25", "D1769-26", "F84"])
N(S9, "The audit holds that the journal's own first encounter is now composed by the receiver it has not studied, from sources that include the publisher's pages, two wikis, a ranking, three sister venues, a network's call and a publisher's AI policy, none of which studies a machine as receiver.",
  ["D1769-21", "D1769-22", "F58", "F60", "F61", "F69", "F71"])
O(57, S9, "Three days before the run of 10 November, the letter of #1750 had told the journal: \"A summarizer already describes your work to people who will never open it.\"")

SENSES = [S0, S1, S2, S3, S4, S5, S6, S7, S8, S9]
sents = []; o2n = {}
for i, (sense, text, claims, on) in enumerate(K, 1):
    sents.append({"n": i, "para": SENSES.index(sense), "sense": sense, "text": text, "claims": claims})
    if on: o2n[on] = i
ko = r["objects"]["KO"]
ko["sentences"] = sents
ko["status"] = "composed 2026-11-10 under v0.10 on BRIEF-NEW-ROW-CRJ.md; revised in place 2026-11-14 on BRIEF-REVISE-ROW-CRJ.md (the address as first-round input, the accountable editor named, #1769 and the four captures of 14 November admitted, the field's new cards and the sources #1769 cites); not frozen; ledgers unaudited"
ko["governing_question"] = ("the revision's organisation (operator, 2026-11-14 17:38, 17:40, 17:41 EST; recorded in notes): on what basis each party comes to speak for the classics in the record, stated as mechanics: "
                            "the journal by its definition as the field's flagship (range, standing, uptake), which it meets (¶3); its editor by signature and its referees by anonymous report (¶1, ¶6); "
                            "the archive by warrant, its census, readings and arguments (¶2, ¶3, ¶6, ¶8); the composition layer by its assignment of credit (¶9)")
for s in sents:
    for c in s["claims"]:
        assert c in AIDS or c in FC, (s["n"], c)
plan_order = [c for s in sents for c in s["claims"]]
pl = ko["plan"]; pl["order"] = plan_order
pl["senses"] = {sn: [s["n"] for s in sents if s["sense"] == sn] for sn in SENSES}
pl["marks"]["CAP-4-08"] = "reported (not fixed): the finding counts 'Oxford Academic four times'; the observation's cite_list holds three Oxford Academic cards of fourteen (REPORT.md)"


def remap(v):
    return [o2n.get(x, x) for x in v] if isinstance(v, list) else v


J = ko["joins"]
J[0]["sentences"] = f"1–{len(sents)}"
J[0]["note"] = ("equal case (§4.7), revised 2026-11-14 under the operator's question of who speaks for the classics and on what basis: what the journal is (¶0); who edits it and signs its decisions, with the editor's own article (¶1); what its pages hold, the register and the archive's audit of it (¶2); "
                "the received definition of the flagship, which the journal meets, and the archive's question of what its criteria measure (¶3); its rules on AI and its publisher's (¶4); its neighbours in the field (¶5); the archive's submission and the decision, with the allegation, the control and the conceded defects (¶6); "
                "a composer's reading of the decision (¶7); the programme of machine-mediated reception studies (¶8); the record of its reception at the journal's, the field's and the editor's addresses (¶9)")
for j in J[1:]:
    j["sentences"] = remap(j["sentences"])
J[1]["sentences"] = [o2n[6], o2n[7], o2n[7] - 1]; J[1]["claims"] = ["F41", "F47", "CAP-1-10", "F58", "D1769-01"]
J[1]["note"] = "the editor: Wikipedia's infobox (2022) beside the registry's 'names no editor' (10 November) and, since 14 November, the publisher's card and #1769 §0.4 naming Dr Justine McConnell as Editor-in-Chief; Michelakis held as Wikipedia's editor at its date; the dates of each term left open"
rv = lambda t: next(s["n"] for s in sents if s["text"].startswith(t))
J += [
    {"act": "holding the received definition and the archive's question", "sentences": [rv("On the received definition"), rv("The archive's audit concedes"), rv("What it contests"), rv("On the audit's counts"), rv("The archive's own position"), rv("The two readings rest")],
     "claims": ["D1769-K1", "D1769-K2", "D1769-29", "D1769-30", "D1769-34", "D1769-35", "D1769-07", "D1769-36", "D1769-38", "D1769-39", "D1769-40", "D1769-41"],
     "note": "the operator's correction of 17:40: the received definition stated with its criteria and the journal stated as meeting it; what #1769 contests is whether the definition's criteria measure what makes reception matter now; both readings' grounds named, neither judged by its holder's standing (rule RD, symmetric ledger); no balance asserted without its warrants"},
    {"act": "composing the allegation with its control and the concessions", "sentences": [rv("Read whole from the decision letter"), rv("The audit sets a control"), rv("The allegation reached"), rv("The audit holds, with the open letter")],
     "claims": ["D1769-12", "D1769-33", "D1769-15", "D1769-16", "D1769-13", "D1769-14", "D1769-17", "D1769-18", "D1769-19"],
     "note": "the second report's 'LLM-generated' composed as an anonymous allegation on stylistic grounds, never as a finding (ALLEGATION_AS_FINDING), with the editor's 2015 article as the control (CONTROL_DROPPED) and the defects the open letter concedes (CONCESSION_DROPPED); no motive supplied or absolved (rule RC)"},
    {"act": "naming the accountable party", "sentences": [rv("Its Editor-in-Chief"), rv("Its decisions rest"), o2n[21]],
     "claims": ["D1769-01", "D1769-02", "D1769-14", "CAP-3-09"],
     "note": "the decision given to the signing editor and never dissolved into 'the journal' (EDITOR_DISSOLVED_INTO_INSTITUTION); no referee named; intent withheld"},
    {"act": "naming the hologram once", "sentences": [rv("The archive's audit of the journal")], "claims": ["D1769-03", "D1769-04"],
     "note": "#1769 named where the archive's reading enters (brief, Cross-links); later sentences refer to it as 'the audit'"},
]
ko["plan"] = pl

# ---------------------------------------------------------------- KO_B (the field alone) and the measure
kb = r["objects"]["KO_B"]
kb["sentences"] += [
    {"n": 11, "para": 6, "text": "On 14 November the Overview's cards for the journal named Justine McConnell as Editor-in-Chief beside a 2025 Impact Factor of 0.4 and a CiteScore of 0.8, set beside it the American Journal of Classical Reception, New Voices in Classical Reception Studies and the International Journal of the Classical Tradition, and showed its special issues, its guidelines' AI-driven Paperpal check, Oxford's AI disclosure guidelines and the CRSN's call.",
     "claims": [f"F{n}" for n in range(58, 72)]},
    {"n": 12, "para": 6, "text": "Oxford University Press updated its AI guidelines on 10 September 2026, asking authors to disclose any significant AI use and to verify AI-generated content, after a survey in which 46% of journal authors and 25% of peer reviewers had not fully disclosed theirs.",
     "claims": ["F72", "F73", "F74", "F75", "F76", "F77"]},
    {"n": 13, "para": 6, "text": "The American Journal of Classical Reception, from CAMWS and Johns Hopkins University Press, reviews double-anonymously, will not accept work substantially written by AI and requires authors to disclose their use of it.",
     "claims": ["F78", "F79", "F80", "F81", "F82", "F88"]},
    {"n": 14, "para": 6, "text": "Justine McConnell's \"Postcolonial Sparagmos\" proposes sparagmos as a metaphor for classical reception, read in Morrison's Sula and Soyinka's Bacchae, and thanks the anonymous CRJ reviewers.",
     "claims": ["F83", "F84", "F85", "F86", "F87"]},
]
kb["status"] = "composed 2026-11-10; extended 2026-11-14 with the field's new sources (B17–B35); not frozen"
r["objects"]["L_B"]["text"] = " ".join(s["text"] for s in kb["sentences"]); r["objects"]["L_B"]["words"] = len(r["objects"]["L_B"]["text"].split())
r["objects"]["L_BA"]["text"] = " ".join(s["text"] for s in sents); r["objects"]["L_BA"]["words"] = len(r["objects"]["L_BA"]["text"].split())
A_ = [s["text"] for s in sents]
pos, mx = [], []
for b in [s["text"] for s in kb["sentences"]]:
    best = max((difflib.SequenceMatcher(None, a, b).ratio(), i + 1) for i, a in enumerate(A_))
    mx.append(round(best[0], 3)); pos.append(best[1] if best[0] >= 0.95 else None)
fieldset = set(FC); archset = AIDS
both = {k for k, v in FC.items() if v.get("dep")}
kind = ["F" if all(c in fieldset and c not in both for c in s["claims"]) else ("A" if all(c in archset for c in s["claims"]) else "M") for s in sents]
lead = next((i for i, k in enumerate(kind) if k != "F"), len(kind)); tail = next((i for i, k in enumerate(reversed(kind)) if k != "A"), len(kind))
m = r["measure"]
present = [p for p in pos if p is not None]
m["v0.10"] = {"surviving": len(present), "of": len(pos), "positions": pos}; m["v0.9"] = copy.deepcopy(m["v0.10"])
m["opening_run"]["breach"] = bool(present) and present == list(range(1, len(present) + 1))
m["blocks"].update({"sequence": "".join(kind), "field_only_head": lead, "archive_only_tail": tail, "breach": bool(lead >= 3 or tail >= 3)})
m["blocks"]["note"] = (m["blocks"]["note"] + " Revised 2026-11-14: the editor (¶1), the audit's census and the two readings (¶2–¶3), the publisher's rules (¶4) and the neighbours (¶5) enter as relations of the journal already composed; "
                       "the record of its reception (¶9) closes with the 14 November observations, mixed with the field where they rest on its cards; the archive-only tail is the closing sentence, #1750's statement.")
m["max_similarity"] = mx
m["ko_sentence_1_max_similarity_to_KO_B"] = round(max(difflib.SequenceMatcher(None, A_[0], b["text"]).ratio() for b in kb["sentences"]), 3)
m["revised"] = "recomputed 2026-11-14 on the revised KO and KO_B (scripts/build_row.py in the stage, the method of apply_v09.py)"
r["objects"]["P"]["entity"] = f"Composed under v0.10, equal case (ρ = extends): KO_B sentences surviving {len(present)} of {len(pos)}; every field claim carried."

# ---------------------------------------------------------------- P (compression)
P = r["objects"]["P"]
P["status"] = "composed 2026-11-10 from the v0.10 knowledge object; revised 2026-11-14 from the revised knowledge object; not frozen"
P["lede"] = {"text": "Classical Receptions Journal is a peer-reviewed journal of classical reception studies published by Oxford University Press since 2009, its decisions signed by its Editor-in-Chief, Dr Justine McConnell, on anonymous review; no title or abstract in its register takes a machine as receiver, and the Overview's credit to it for the study of AI-mediated reception, which carried the archive's programme cited from #833, was withdrawn and held withdrawn.",
             "claims": ["F39", "F40", "F50", "D1769-01", "D1769-02", "F53", "D1769-04", "CAP-1-02", "CAP-1-27", "CAP-4-02"]}
sec = {s["head"]: s for s in P["sections"]}
it = {i["label"]: i for i in sec["What it is"]["items"]}
it["Editor:"].update({"text": "Editor-in-Chief Dr Justine McConnell (#1769; publisher's card, 14 Nov); founder Hardwick; Wikipedia: Michelakis (2022).",
                      "claims": ["D1769-01", "F58", "D1769-02", "F41", "F47", "F46", "F45", "CAP-1-10", "CAP-1-20", "CAP-3-09"]})
sec["Its pages"]["items"].append({"label": "Audit:", "text": "141 of 185 read a later work against a fixed source; 32 reach it, 9 governing; no open text takes a machine as receiver (#1769).",
                                  "claims": ["D1769-03", "D1769-04", "D1769-05", "D1769-06", "D1769-07", "D1769-31", "D1769-34", "F87", "F83", "F84", "F85", "F86", "D1769-28"]})
two = {"icon": "🧭", "head": "Two readings", "items": [
    {"label": "Definition:", "text": "flagship by range, standing and uptake; the journal meets it.", "claims": ["D1769-K1", "D1769-29", "D1769-39"]},
    {"label": "Contested:", "text": "the criteria count widening, not reopening, nor who speaks on what basis (#1769).", "claims": ["D1769-30", "D1769-35", "D1769-K2", "D1769-40", "D1769-41", "D1769-38"]}]}
P["sections"].insert(2, two)
sec["Rules on AI"]["items"].append({"label": "Publisher:", "text": "OUP: disclose significant AI use, verify AI content (10 Sept 2026).",
                                    "claims": ["F69", "F72", "F73", "F74", "F75", "F76", "F77", "F68", "D1769-20"]})
di = {i["label"]: i for i in sec["CLASSREC-2026-062"]["items"]}
di["Decision:"].update({"text": "declined 7 November 2026 over the editor's signature on two anonymous reports written on v6 (#1749, #1769).",
                        "claims": ["D1749-01", "D1749-02", "D1749-03", "D1749-04", "D1749-15", "D1444-01", "D1543-01", "D1769-01", "D1749-05", "D1749-18"]})
sec["CLASSREC-2026-062"]["items"].insert(2, {"label": "Allegation:", "text": "anonymous \"LLM-generated\" on style; the editor's 2015 prose meets the same markers; defects conceded.",
                                             "claims": ["D1769-12", "D1769-13", "D1769-14", "D1769-15", "D1769-16", "D1769-17", "D1769-18", "D1769-19", "D1769-33", "D1769-32", "D1769-08", "D1766-01"]})
sec["The programme credited"]["items"].append({"label": "Neighbours:", "text": "AJCR, New Voices, IJCT's Future Pasts: none takes a machine as receiver (#1769).",
                                               "claims": ["F59", "F62", "F63", "F65", "F66", "F70", "F71", "F78", "F79", "F80", "F81", "F82", "F88", "F60", "F61", "F64", "F67", "D1769-23", "D1769-24"]})
sec["At the name"]["items"] += [
    {"label": "14 November:", "text": "the credit withdrawn and held; moved to IJCT and the CRSN; the maker absent.", "claims": ["CAP-4-01", "CAP-4-02", "CAP-4-03", "CAP-4-04", "CAP-4-05", "CAP-4-09", "CAP-4-10", "D1769-09", "D1769-10", "D1769-11", "D1769-21", "D1769-22"]},
    {"label": "Field, editor:", "text": "the term to Sharks, the contribution to institutions; the editor named \"Justin\".", "claims": ["CAP-5-01", "CAP-5-03", "CAP-6-02", "CAP-6-03", "D1769-25", "D1769-26", "D1769-27"]},
]

# trims for the 350-word bound (§4.8); every claim of a removed item stays on the rail
P["lede"]["text"] = "Classical Receptions Journal is a peer-reviewed journal of classical reception studies at Oxford University Press since 2009, its decisions signed by its Editor-in-Chief, Dr Justine McConnell; no title or abstract in its register takes a machine as receiver, and the Overview's credit to it for the archive's programme was withdrawn."
TR = {"Kind:": "peer-reviewed journal of reception studies (Wikipedia); \"institutionalized the field at Oxford\" (#833).",
      "Editor:": "Dr Justine McConnell, Editor-in-Chief (#1769); Wikipedia: Michelakis (2022).",
      "Audit:": "141 of 185 read later work against a fixed source; no open text takes a machine as receiver (#1769).",
      "Authors:": "AI tools \"do not qualify as authors\"; disclosure in cover letter and Methods (registry).",
      "Preflight:": "\"pre-submission\", \"not mandatory\"; editor-configured, 20 checks (Paperpal).",
      "Decision:": "declined 7 Nov 2026 over the editor's signature, two anonymous reports on v6.",
      "Reports:": "protocol, roles, opacity, figures, disclosure, style; answered (#1749 App. A).",
      "Composer:": "\"a failure of intellectual stewardship\" (ChatGPT, its own); one case.",
      "Credit:": "\"contributors to CRJ\" given #833's horizon of reception.",
      "Correction:": "turn 5 names Sharks and #833, over-assigning a contrast.",
      "14 November:": "withdrawn and held; moved to IJCT and the CRSN; maker absent."}
for s_ in P["sections"]:
    s_["items"] = [i for i in s_["items"] if i["label"] not in ("Times:", "Neighbours:")]
    for i in s_["items"]:
        if i["label"] in TR: i["text"] = TR[i["label"]]
P["body_words"] = len(P["lede"]["text"].split()) + sum(len((i["label"] + " " + i["text"]).split()) for s in P["sections"] for i in s["items"])
P["body_words_rule"] = "lede plus every item's label and text (2026-11-14; the bound is 350, §4.8)"
P["open"][0] = {"question": "When did each editor's term begin and end? The Editor-in-Chief is Dr Justine McConnell (#1769 §0.4; the publisher's card of 14 November); Wikipedia's infobox (last edited 2022) names Pantelis Michelakis without dates; the About page names no editor.",
                "rests_on": ["D1769-01", "D1769-02", "F58", "F41", "F47", "CAP-1-10"], "modality": "documented (the record and the card); dates absent",
                "would_resolve": "the journal's mastheads by volume, which are behind the press's pages"}
P["open"][-1]["question"] = (P["open"][-1]["question"] + " On 14 November the About and General Instructions pages refused again (HTTP 403), as did New Voices (HTTP 403) and the IJCT editorial (a client challenge); "
                             "the fourteen cards of 14 November enter as the registry holds them.")
P["open"][-1]["rests_on"] += ["F63", "F66"]
P["open"] += [
    {"question": "Does the withdrawal of the credit persist at the journal's address, and does the warranted relation between the author and the work return there?", "rests_on": ["D1769-10", "D1769-11", "CAP-4-05", "CAP-1-12"],
     "modality": "documented (two observations at one address)", "would_resolve": "dated re-runs at 'classical receptions journal', seated as observations, each recording both relations"},
    {"question": "How was the second report's authorship allegation assessed, and did it contribute to the decision?", "rests_on": ["D1769-12", "D1769-13", "D1769-14"],
     "modality": "documented: the record does not show it", "would_resolve": "an account from the accountable editor"},
]
NEWLIN = [("who signs", ["D1769-01", "D1769-02", "D1769-14", "F58", "CAP-3-09"], "B17"),
          ("the field around it", ["F59", "F62", "F63", "F78", "F79", "F81", "F82", "F88"], "B18"),
          ("its publisher's rules on AI", ["F69", "F72", "F73", "F74", "F75", "F76", "F77", "F80", "D1769-20"], "B31"),
          ("the editor's article", ["F83", "F84", "F85", "F86", "F87", "D1769-25", "D1769-26", "D1769-28"], "B35"),
          ("the audit", ["D1769-03", "D1769-04", "D1769-05", "D1769-06", "D1769-07", "D1769-31", "D1769-34"], 1769),
          ("two readings", ["D1769-K1", "D1769-K2", "D1769-29", "D1769-30", "D1769-35", "D1769-38", "D1769-39", "D1769-40", "D1769-41"], 1769),
          ("after notice", ["CAP-4-01", "CAP-4-02", "CAP-4-03", "CAP-4-04", "CAP-4-05", "CAP-4-06", "CAP-4-07", "CAP-4-08", "CAP-4-09", "CAP-4-10", "D1769-09", "D1769-10", "D1769-11", "D1769-21", "D1769-22"], "capture-registry"),
          ("at the field's address", [f"CAP-5-{k:02d}" for k in range(1, 11)], "capture-registry"),
          ("at the editor's address", [f"CAP-6-{k:02d}" for k in range(1, 10)] + ["D1769-27"], "capture-registry"),
          ("a composer on the archive's critique", [f"CAP-3-{k:02d}" for k in range(1, 15)], "capture-registry")]
rails = {x["lineage"]: x for x in P["rail"]}
rails["the archive's author in its pages"]["claims"] += ["D1769-36", "D1769-37", "D1769-38"]
rails["the decision on CLASSREC-2026-062"]["claims"] += ["D1749-18", "D1766-01", "D1769-08", "D1769-12", "D1769-13", "D1769-15", "D1769-16", "D1769-17", "D1769-18", "D1769-19", "D1769-32", "D1769-33"]
rails["the field on AI"]["claims"] += ["F65", "F66", "F70", "D1769-24"]
rails["literary reception and large language models"]["claims"] += ["F71", "D1769-23"]
rails["pre-submission checks"]["claims"] += ["F68"]
rails["what its pages hold"]["claims"] += ["F67"]
rails["editors and dates"]["claims"] += ["F60"]
rails["what it is"]["claims"] += ["F61"]
rails["the field"]["claims"] += ["F64"]
for lin, cl, e in NEWLIN:
    P["rail"].append({"lineage": lin, "claims": cl, "earliest": e})
# P_B
PB = r["objects"]["P_B"]
PB["status"] = "composed 2026-11-10 from the field ledger alone; extended 2026-11-14; not frozen"
PB["sections"][0]["items"][0].update({"text": "Justine McConnell, Editor-in-Chief (publisher's card, 2026); Pantelis Michelakis (Wikipedia, 2022).", "claims": ["F58", "F41", "F47"]})
PB["sections"][1]["items"] += [{"label": "Publishers:", "text": "OUP asks authors to disclose significant AI use; Johns Hopkins refuses work substantially written by AI.", "claims": ["F72", "F73", "F80"]}]
PBr = {x["lineage"]: x for x in PB["rail"]}
PBr["the field on AI"]["claims"] += ["F65", "F66", "F70"]; PBr["literary reception and large language models"]["claims"] += ["F71"]
PBr["pre-submission checks"]["claims"] += ["F68"]; PBr["what its pages hold"]["claims"] += ["F67"]; PBr["editors and dates"]["claims"] += ["F60"]
PBr["what it is"]["claims"] += ["F61"]; PBr["the field"]["claims"] += ["F64"]
for lin, cl, e in NEWLIN[:4]:
    PB["rail"].append({"lineage": lin, "claims": [c for c in cl if c in FC], "earliest": e})
PB["body_words"] = len(PB["lede"]["text"].split()) + sum(len(i["text"].split()) for s in PB["sections"] for i in s["items"])

# ---------------------------------------------------------------- L_BA rail
rail = r["objects"]["L_BA"]["rail"]
for x in rail:
    if x["Card"].startswith("#1749"):
        x["Card"] = "#1749 " + C.T1749[:80]
    if x["Card"].startswith("capture-registry"):
        x["Card"] += " · crj-critique-extended-chatgpt-20261114 · " + C.OBS + " · mmrs-who-contributed-aio-20261114 · postcolonial-sparagmos-title-aio-20261114"
for s in srcs:
    rail.append({"Card": f"{s['id']} {s['card'][:80]}", "Snippet": FC["F" + str(int(s['id'][1:]) + 41)]["quote"]})
for bid, fid in (("B31", "F73"), ("B32", "F80"), ("B35", "F84")):
    rail.append({"Card": f"{bid} {Fl['field_sources'][bid][:80]}", "Snippet": FC[fid]["quote"]})
rail.append({"Card": "#1766 " + C.T1766[:80], "Snippet": "In this critique's terms, it is a paralogism of review: the procedural requirement is taken for an examination of the object."})
rail.append({"Card": "#1769 " + C.T1769[:80], "Snippet": "No title or abstract takes a search engine, an encyclopedia platform, a recommender or a composing model as a receiver of antiquity."})
r["objects"]["L_BA"]["note"] = r["objects"]["L_BA"]["note"] + "; extended 2026-11-14 with the revision's sources"

# ---------------------------------------------------------------- addresses, T, kernel
r["address"] = NEW_ADDR
a0 = r["addresses"][0]; a0["address"] = NEW_ADDR; a0["axn"] = AXN_T
a0["address_note"] = f"the address is the first-round input ({RULING_ADDR}); prior string kept: '{OLD_ADDR}'; addr_id kept as recorded"
a0["axn_note"] = "AXN as the registry holds it at v12.683; the row's prior AXN:0C64.CAPTURE.🎶🌘♎⏪🌲🌕 (the re-derivation of 2026-11-10)"
t0 = r["objects"]["T"]["transcripts"][0]; t0["address"] = NEW_ADDR; t0["axn"] = AXN_T
t0["address_note"] = a0["address_note"]
t0["later_observations"] = [{"slug": C.OBS, "obs_id": "OBS-2211c8d30212", "axn": entry(C.OBS)["axn"], "date": "2026-11-14", "registry": "v12.681",
                             "note": "a later observation at the same address, seated in the Capture Registry; not T; the kernel's first resolver run"}]
for k in r["kernel"]:
    k["resolver"] = (f"a later capture at '{NEW_ADDR}' (ADDR-a0c7f3698714) on Google AI Overview, seated in the Capture Registry (§8.3); "
                     "first re-run 2026-11-14 (v12.681, OBS-2211c8d30212): the credit to the journal withdrawn and held, the author and #833 absent (CAP-4-02, CAP-4-05)")
r["kernel"] += [
    {"K": "K16", "claim": "`D1769-01`", "source": "#1769 §0.4", "M_src": "documented", "sense": S1, "qualifiers carried": "D1769-14 (the signature does not show endorsement of each sentence)",
     "f (source's own falsifiers)": "— (none stated; watch: a later composition that gives the decision to 'the journal' with the editor unnamed)",
     "contrast": "rival claim: the decision given to 'CRJ', 'the journal' and 'the reports', no editor named (v12.680, CAP-3-09)",
     "resolver": "a later composition at 'How does alexanarch critique Classical Receptions Journal? …' (ADDR-739ce1f09c44) or at the journal's address, seated in the Capture Registry (§8.3)"},
    {"K": "K17", "claim": "`D1769-11`", "source": "#1769 §9.6.1", "M_src": "documented", "sense": S9, "qualifiers carried": "D1769-10 (two relations); one observation at one address",
     "f (source's own falsifiers)": "the warranted relation returns at the address (#1769 §9.6)",
     "contrast": "rival claim: the credit moved to IJCT and the CRSN, the author absent (v12.681, CAP-4-04, CAP-4-05)",
     "resolver": f"dated re-runs at '{NEW_ADDR}' (ADDR-a0c7f3698714), weekly 21 November to 12 December 2026 (#1769 §9.6), seated as observations"},
]

# ---------------------------------------------------------------- delta
d = r["delta"]
for mv in d["correction"]["moves"]:
    mv["ko"] = [o2n[x] for x in mv["ko"]]
    if mv["move"] == "T1-3":
        mv["type"] += ("; since 14 November the publisher's card (F58) and #1769 §0.4 (D1769-01) name Dr Justine McConnell as Editor-in-Chief, and the decision of 7 November is signed by her (CAP-3-09): "
                       "the name T gave is right and was unsourced at B_D on 10 November; Michelakis as 'past editor' stands against Wikipedia's undated infobox")
        mv["answered_by"] += ["F58", "D1769-01", "CAP-3-09"]
        mv["ko"] = sorted(set(mv["ko"] + [rv("Its Editor-in-Chief")]))
d["correction"]["check"] = "every move answered by a knowledge-object sentence and a compression line (KO sentences and P labels given per move; KO numbers renumbered 2026-11-14); no gap"
d["LB_vs_LBA"] += (" Revision of 2026-11-14: admission adds #1769, the archive's audit of the journal (D1769-01–D1769-35, D1769-K1, D1769-K2: the accountable editor, the census re-read, the coding of the 185 abstracts and the 37 open texts, "
                   "the received definition at its strength and the archive's question of what its criteria measure, the allegation with its control and the conceded defects, the two-relation repair test, the composition's sources), "
                   "#1766 §6.1.3 (D1766-01, the decision as a paralogism of review) and #1749 v10 (D1749-18), and the four captures of 14 November (CAP-3 v12.680, CAP-4 v12.681, CAP-5 v12.682, CAP-6 v12.683). "
                   "After notice (v12.681): the false recipient removed and held removed; the warranted relation not restored, the credit moved to IJCT's Future Pasts and the CRSN call (DISPLACEMENT again, from one institution to two; the maker absent from answer and citations). "
                   "At the field's address (v12.682) the term goes to its maker and the contribution to institutions; at the editor's (v12.683) the article's frame is carried forward and her name altered. "
                   "The new field sources (B17–B35) are composed as received beside the archive claims they stand with; B17–B30 are the cards of v12.681 and enter no comparison with T.")
d["pools_note"] = d["pools_note"] + "; B17–B30 (B_D) are the cards of the 14 November observation (v12.681), never T's; B31–B35 are B_R"
d["alignment"]["v12681_cards_note"] = "B17–B30 are cards of the observation of 14 November (v12.681), not of T; T's alignment is unchanged"

# ---------------------------------------------------------------- ontology, homonyms
ont = r["ontology"]
ont["case"]["loci"].append({"dep": 1769, "locus": "§0.4", "quote": "The journal's Editor-in-Chief is Dr Justine McConnell (King's College London). She signed the decision of 7 November 2026 on Closing the Fragment, which was reviewed by two anonymous referees."})
ont["case"]["statement"] += (" #1769 (14 November 2026) audits the journal as the field's own institution, grants that it meets the received definition of the field's flagship, and asks whether that definition's criteria measure what makes classical reception matter now; "
                             "it contests no fact of what the journal is. The case stays equal terms, ρ = extends.")
ont["E_F"]["definition"] = ont["E_F"]["definition"].replace("(Wikipedia, citing the About page; editor Pantelis Michelakis in the infobox, 2022; no year of establishment)",
    "(Wikipedia, citing the About page; editor Pantelis Michelakis in the infobox, 2022; no year of establishment); its Editor-in-Chief Justine McConnell on the publisher's card of 14 November 2026; its publisher's AI disclosure guidelines of 10 September 2026; among sister journals the American Journal of Classical Reception, New Voices and the IJCT")
ont["E_F"]["claims"] += ["F58", "F72", "F73", "F59", "F63", "F66"]
ont["E_A"]["definition"] += (" Revised 2026-11-14: a journal whose decisions are signed by its Editor-in-Chief, Dr Justine McConnell, on anonymous review, she being the accountable party (#1769 §0.4, §6.4.3.2); "
                             "audited by the archive (#1769) on its register and open texts, which meets the received definition of the field's flagship and holds the classical source fixed in most of its work; "
                             "and, after notice, a name at which the composition withdrew the credit and moved it to other institutions with the maker absent (v12.681).")
ont["E_A"]["claims"] += ["D1769-01", "D1769-14", "D1769-K1", "D1769-07", "D1769-11", "CAP-4-04"]
ont["E_A"]["defining_papers"] += [1769, 1766]
ont["E_A"]["defining_records"] = [
    f"Capture Registry classical-receptions-journal-ai-mediation-aio-20261110 (OBS-a15e4aaae906, ADDR-a0c7f3698714, {AXN_T}; address '{NEW_ADDR}', the first-round input since the repair of 2026-11-14; repaired 2026-11-10 to the run whole, rebuild/capture-registry/repair-20261110-crj-run-whole/); its observation of 2026-11-14, {C.OBS} (OBS-2211c8d30212, v12.681)",
    f"Capture Registry vox-letter-crj-stewardship-chatgpt-20261110 (OBS-2fe1e9c82a2f, ADDR-08b489b6ea6e, {AXN_VOX}; address '{VOX_ADDR}', the first [QUERENT] input; a further address, a composer's reading guided by the operator's prompts)",
    "Capture Registry crj-critique-extended-chatgpt-20261114 (OBS-44161e8363dd, ADDR-739ce1f09c44, AXN:0C97; v12.680; ChatGPT on the archive's critique)",
    "Capture Registry mmrs-who-contributed-aio-20261114 (OBS-3bebf8c86c8e, ADDR-8f65df25e194, AXN:0C98; v12.682; the field's address)",
    "Capture Registry postcolonial-sparagmos-title-aio-20261114 (OBS-4c6d35c86e34, ADDR-42798e12f54e, AXN:0C99; v12.683; the editor's article by its title)"]
ont["rho"]["status"] += "; revised 2026-11-14 with #1769, #1766 and the four captures of 14 November, which leave ρ = extends"
ont["rho"]["statement"] += (" Revised 2026-11-14: the accountable editor and the basis of the decision (#1769 §0.4, §6.4.3.2); the archive's audit of the register and the open texts and its question of what the received definition measures (#1769); "
                            "the decision read as an inference (#1766); and the record after notice (v12.680–v12.683).")
ont["rho"]["claims"] += ["D1769-01", "D1769-K1", "D1769-30", "D1766-01", "CAP-4-02"]
ont["rho"]["guard"] += (" The audit's readings are #1769's, cited by locus as the archive's reading; the received definition is stated at its strength from #1769's kernel and the journal is stated as meeting it; "
                        "the second report's allegation is composed as an anonymous allegation, with its control and the conceded defects, never as a finding; intent is withheld from every party.")
# translation table: rebuilt for every field claim, by lineage
oldtr = {t["lineage"]: t for t in ont["translation"]}
ARCH_BY_LIN = {"who signs": ["D1769-01", "D1769-02", "D1769-14", "CAP-3-09"], "the field around it": ["D1769-22"], "its publisher's rules on AI": ["D1769-20"],
               "the editor's article": ["D1769-25", "D1769-26", "D1769-27", "D1769-28", "D1769-15"]}
extra = {"the field on AI": ["D1769-24", "CAP-4-04"], "literary reception and large language models": ["D1769-23"], "what its pages hold": ["D1769-03", "D1769-04"]}
bylin = {}
for fid, c in FC.items():
    bylin.setdefault(c["lineage"], []).append(fid)
tr = []
for lin, fids in bylin.items():
    t = oldtr.get(lin, {"lineage": lin, "receiving_text": "—"})
    ac = list(dict.fromkeys(t.get("archive_claims", []) + ARCH_BY_LIN.get(lin, []) + extra.get(lin, [])))
    t.update({"field_claims": fids, "received": "; ".join(f"{f} ({FC[f]['source']}, {FC[f]['locus']}): \"{FC[f]['quote']}\"" for f in fids),
              "translation": "untranslated: composed as received beside " + (", ".join(ac) if ac else "no archive claim"), "archive_claims": ac})
    tr.append(t)
ont["translation"] = tr
r["homonyms"]["distinct_entities"] += [
    "Justine McConnell, its Editor-in-Chief, a person (#1769 §0.4; the publisher's card, B17 F58)",
    "Lorna Hardwick, its founding editor, a person (#1769 §0.4)",
    "Oxford University Press as the author of its AI disclosure guidelines (B31)",
    "Daffodils (#1769), the archive's audit of the journal, a deposit",
    "'Classical Reception 2.0' and 'Future Pasts', the IJCT special issue the Overview of 14 November credits (B24, B25, B29, B34)"]

# ---------------------------------------------------------------- field summaries in the row
r["field_claims"] = FC; r["field_sources"] = Fl["field_sources"]
for s in srcs + BR:
    tried = s["fetched"].get("tried")
    if tried:
        fe = "unreachable: " + "; ".join(f"{x['url']} HTTP {x['http']} {x['at']}" for x in tried)
    elif s["id"] in ("B31", "B32", "B35"):
        fe = f"fetched {s['fetched']['at']} HTTP {s['fetched']['http']}, text sha256 " + list(s["files"].values())[0]["sha256"]
    else:
        fe = "card as the registry holds it (v12.681); not fetched"
    r["field"].append({"id": s["id"], "card": s["card"], "fetched": fe, "origin": s["origin"], "pool": s["pool"]})
fbo = r["field_by_origin"]
fbo["cards_v12681"] = [s["id"] for s in srcs]
fbo["third_party"] = ["B31", "B32", "B33", "B34"]; fbo["repository_copy"] = ["B35"]
fbo["unreachable"] = fbo["unreachable"] + ["B33", "B34"]
fbo["pools"] = Fl["pools"]; fbo["sources"] = Fl["field"]
fbo["own_pages_note"] += "; tried again on 2026-11-14 (About, General Instructions): HTTP 403 again"

# ---------------------------------------------------------------- links, notes, status, composition
r["links"] = {"hologram": HOLO, "hologram_kernel": HOLOK}
nt = r["notes"]
nt[0] = nt[0].replace("classical-receptions-journal-ai-mediation-aio-20261110 (OBS-a15e4aaae906, ADDR-a0c7f3698714, AXN:0C64.CAPTURE.🎶🌘♎⏪🌲🌕; the AXN re-derived by the repair of 2026-11-10 from AXN:0C64.CAPTURE.👉💚🔓🔗🔀🎯)",
                      f"classical-receptions-journal-ai-mediation-aio-20261110 (OBS-a15e4aaae906, ADDR-a0c7f3698714, {AXN_T} as the registry holds it at v12.683; the row's prior AXN:0C64.CAPTURE.🎶🌘♎⏪🌲🌕, re-derived by the repair of 2026-11-10 from AXN:0C64.CAPTURE.👉💚🔓🔗🔀🎯)")
nt[0] += f" The address is '{NEW_ADDR}', the first-round input ({RULING_ADDR}); prior string: '{OLD_ADDR}'."
nt[1] = nt[1].replace("(OBS-2fe1e9c82a2f, AXN:0C65.CAPTURE.🕔🕑🔎🔵📜🛤️)", f"(OBS-2fe1e9c82a2f, ADDR-08b489b6ea6e, {AXN_VOX}; prior AXN in this row AXN:0C65.CAPTURE.🕔🕑🔎🔵📜🛤️)")
nt[1] += f" Its address is its first [QUERENT] input: '{VOX_ADDR}'; prior string (the inputs of the session joined): '{VOX_OLD}'."
nt[4] = nt[4].replace("#1423 https://www.alexanarch.org/s/records/1423/;", f"#1423 https://www.alexanarch.org/s/records/1423/; #1769, Daffodils, the archive's audit of the journal (the framework hologram) {HOLO} and its kernel {HOLOK}; #1766 https://www.alexanarch.org/s/records/1766/;")
nt[4] += ("; the captures of 14 November https://www.alexanarch.org/captures/crj-critique-extended-chatgpt-20261114/, https://www.alexanarch.org/captures/classical-receptions-journal-ai-mediation-aio-20261110/#" + C.OBS +
          ", https://www.alexanarch.org/captures/mmrs-who-contributed-aio-20261114/ and https://www.alexanarch.org/captures/postcolonial-sparagmos-title-aio-20261114/; the sources #1769 §6.5.1 cites, " + FR["oup-ai-disclosure"]["url"] + ", " + FR["camws-ajcr"]["url"] + ", " + FR["newvoices"]["url"] + ", https://doi.org/10.1007/s12138-026-00750-7, and the editor's article " + FR["ora-postcolonial-sparagmos"]["url"])
nt += [
    "Revision of 2026-11-14 (rebuild/negative-of-the-negative/v010/BRIEF-REVISE-ROW-CRJ.md; the operator, 16:38 EST: 'at this point qe need to revise the crj /non article so that these can cross link each other'; 16:42: 'yes, i think its time to deposit. put the links to /non in now abd well revise /non after'; 17:29: 'lets do so'). Staged at rebuild/negative-of-the-negative/v010/revise-crj-20261114/. AXN:0C66 stays the row's identity. The prior row's sha256 is " + PRIOR_ROW_SHA + "; the session records it in earlier_versions.",
    "The operator's rulings for this revision, recorded here and not quoted in the knowledge object: 17:38 EST, 'this is about who gets to speak for the classics, and on what basis' (the revision's governing question, carried as mechanics: the basis on which the journal, its editor, its referees, the composition layer and the archive each speak for the classics in the record); 17:40 EST, 'the received reading if what healthy flagship means is whats being contested. i wouldnt contest that it meets that definition; i would contest that that definition defines something healthy' (the KO states the received definition with its criteria, states that the journal meets it, and states the archive's question of what those criteria measure); 17:41 EST, 'more of the same is what it tends to mean' (carried as mechanics with #1769's counts: the criteria count the widening, more receivers read against the same source, 153 of 185 abstracts holding the classical object fixed and 141 reading a later work against a fixed source; they do not count the reopening). #1769 was reissued in place as v1.1 (14 November 2026) to state the 17:38 and 17:40 words (its §1.6, and the kernel's rival restated); this row cites v1.1 as it stands at 17:43 EST (data/texts/AXN-0C9A-text.md), §1.6 among its loci. 17:48 EST: 'i already published in their pages - the research was highly relevant. no one engaged. it did not travel. so now challenging the model is *exactly what i would like to do*' (carried in the KO as mechanics, on #1769 §6.2, §5.1 and §3.4: the article's uptake as the register gives it, 0 citations and no reference to it among the journal's 16,818, and the archive's position as the archive's: having published inside the received definition without recorded uptake, it contests what the definition measures; the work itself is not characterised and the civil byline is not stated).",
    "The accountable party: the decision of 7 November 2026 on CLASSREC-2026-062 is signed by the Editor-in-Chief, Dr Justine McConnell (King's College London) (#1769 §0.4; the decision letter as v12.680 records it). The referees are anonymous and are named by role only. No intent is attributed to any party (#1769 §6.4.6; rule RC of #1769's kernel).",
    "#1749 was reissued on 10 November 2026 as v10, retitled '“But I Must Dare All”: Sappho 31 and the Composition Layer as a Surface of Classical Reception'; its AXN in the registry is now " + C.AXN1749 + ". D1749-05's quote is the v10 head line (the v9 line of the prior ledger is no longer in the text).",
    "D/R/O pass rerun 2026-11-14 with scripts/non_traverse.py on the same aliases and classes, hop from #1749, #1750, #833, #1421, #1423 and #1769 (stage traversal/): D 50 sentences in 8 deposits, R 8 in 4, O 21 direct and 7 class in 10, H 109. New candidates beyond #1749's v10 lines and #1769: #1766 §6.1.3 (D0014), admitted (it reads the decision as a paralogism of review); hop candidates #4, #32, #165, #189, #280 and #1767 (forward from #1769), and #1766 (reverse), read: none but #1766 says anything of the journal, and they enter only through #1769's own citations.",
    "Capture-record finding reported, not fixed: " + C.OBS + " findings[7] ('SOURCES') counts 'Oxford Academic four times'; the observation's cite_list holds three Oxford Academic cards (1, 10, 11) of fourteen, and the listed counts then sum to fifteen.",
]
st = r["status"]
st["procedure"] += (" Revised 2026-11-14 (BRIEF-REVISE-ROW-CRJ.md): the address as the first-round input; #1769 (v1.1) admitted at §0.1, §0.3, §0.4, §1.5, §1.6, §2.4, §2.4.1, §2.6, §2.6.2, §3.4, §5.1, §6.2, §6.4.3–§6.4.6, §6.5, §6.5.1, §7.10, §7.11.6, §9.2.1, §9.6.1, §9.10 and its kernel; #1766 §6.1.3 by the D/R/O rerun; "
                    "the four captures of 14 November (v12.680–v12.683) as CAP-3–CAP-6; B_D adds B17–B30 (the v12.681 cards), B_R adds B31–B35 (readable B31, B32, B35).")
r["composition"] = copy.deepcopy(r["composition"])
r["composition"]["revision_20261114"] = {"source": "rebuild/negative-of-the-negative/v010/BRIEF-REVISE-ROW-CRJ.md and the operator's rulings of 17:38, 17:40 and 17:41 EST relayed by the coordinator", "composer": "Claude (Opus 5.5), subagent, 2026-11-14",
    "read": ["the row, its two ledgers and non/classical-receptions-journal/entity.json, whole", "BRIEF-NEW-ROW-CRJ.md, whole", "data/texts/AXN-0B79-text.md §3–§6", "data/texts/AXN-0C9A-text.md (#1769), whole",
             "files/AXN-0C9A/kernel/00-kernel.yaml (rival, symmetric ledger) and 01-ontology.yaml, whole", "data/texts/AXN-0C8B-text.md (#1766) §6.1", "data/texts/AXN-0C40-text.md (#1749 v10) head and §0",
             "data/EA-WG-CAPTURES-01.json: the five records, transcripts, reading, analysis, findings, cite_list, notes", "the new saved sources under the stage's sources/"],
    "stage": "rebuild/negative-of-the-negative/v010/revise-crj-20261114/", "prior_row_sha256": PRIOR_ROW_SHA}

OUT = STAGE
(OUT / "row.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "field.json").write_text(json.dumps(Fl, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "ledger-archive.json").write_text(json.dumps(Al, ensure_ascii=False, indent=1), encoding="utf-8")
print("KO", len(sents), "P words", P["body_words"], "PB", PB["body_words"], "measure", m["v0.10"], "blocks", m["blocks"]["sequence"], lead, tail)
print("field", len(FC), "archive", len(Al))
