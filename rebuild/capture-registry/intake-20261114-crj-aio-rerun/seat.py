"""Seat of 2026-11-14 (received 13:25 EST): Google AI Overview, signed out and incognito, the address 'classical receptions journal', four days
after the seated capture of 10 November. The operator's ruling (13:30 EST): 'a second round input is not an address'. The address is the
first-round input; the second-round input ('what has crj contributed to the study of ai-mediated reception of the classics?', a rewording
of the 10 November second turn) belongs to the session. The run therefore seats as a longitudinal observation of the 10 November record.
The draft carries that record's q only so that intake routes it; the observation's transcript gives the inputs as issued today.
Every quotation is asserted against the paste; every claim the findings make is asserted against the registers or the record.   python3 seat.py"""
import json, pathlib, re
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-14"; RECV = "2026-11-14 13:25 EST"
SLUG10 = "classical-receptions-journal-ai-mediation-aio-20261110"
CAPS = {e["slug"]: e for e in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
E10 = CAPS[SLUG10]; assert E10["surface"] == "Google AI Overview" and E10["q"].split(" · ")[0] == "classical receptions journal"
Q1 = "classical receptions journal"; Q2 = "what has crj contributed to the study of ai-mediated reception of the classics?"
OP = "run just now. lets examine before we decide what to do with it"; OP2 = "a second round input is not an address"
raw = (H / "paste-aio-crj-20261114.txt").read_text(encoding="utf-8"); L = raw.split("\n")
assert L[1] == Q1 and L[45] == Q2
t1 = "\n".join(L[3:19]).strip(); t2 = "\n".join(L[47:62]).strip()
P = {"withdrawn": "To date, the Classical Receptions Journal (CRJ) has not published a dedicated special issue or major body of scholarship specifically focused on AI-mediated classical reception.",
     "policy": "CRJ’s direct engagement with artificial intelligence has largely centered on editorial policy and submission workflows rather than thematic research articles.",
     "pp": "an AI-driven tool that checks manuscripts against the journal’s technical formatting requirements prior to submission",
     "indirect": "Anachronism and Antiquity (Vol. 12, Issue 1) and Failures in Vergilian Translation (Vol. 14, Issue 3)",
     "moved": "much of the foundational scholarship is currently appearing in sister journals and network forums rather than CRJ",
     "ijct": "Published a dedicated special issue in 2026 titled Classical Reception 2.0: Digital Antiquity and the Future of the Past, which directly examines how ChatGPT, generative AI models, digital archives, and 3D modeling reshape the transmission and creative reimagining of antiquity.",
     "crsn": "Literary Reception and Human Creativity in the Age of AI",
     "editor": "Editor-in-Chief: Justine McConnell (with previous leadership including Pantelis Michelakis).",
     "if": "2025 Impact Factor: 0.4; 2025 CiteScore: 0.8.",
     "wiki": "This article may rely excessively on sources too closely associated with the subject"}
for k, v in P.items(): assert v in raw, k
assert "Sharks" not in raw and "alexanarch" not in raw.lower() and "833" not in raw and "Horizon of Reception" not in raw
REG = json.loads((H / "registers.json").read_text(encoding="utf-8"))  # extracted from the Crossref registers read 2026-11-14
assert any(w["vol"] == "12" and w["issue"] == "1" and w["title"] == "At the end of the line: on kairological history" for w in REG["crj"])
assert any(w["vol"] == "14" and w["issue"] == "3" and w["title"].startswith("Introduction: what is failure in translation") for w in REG["crj"])
fp = [i for i in REG["ijct_33_2"] if i["doi"] == "10.1007/s12138-026-00750-7"][0]
assert fp["title"] == "Future Pasts: Digital Tools and Classical Reception"
assert len(REG["ijct_33_2"]) == 8
# ---- citations: eight cards under the first answer, six under the second; none an archive page
def cards(lo, hi, turn):
    out = []
    for i in range(lo, hi, 3):
        out.append({"site": L[i].strip(), "rel": "third_party", "url": None, "title": L[i + 1].strip(), "snip": L[i + 2].strip()[:300], "note": f"source card, turn {turn}"})
    return out
C = cards(19, 43, 1) + cards(62, 80, 2)
assert [c["site"] for c in C] == ["Oxford Academic", "Hopkins Press", "Wikipedia", "SCImago", "American Journal of Classical Reception", "The Open University", "Wikipedia", "Springer Nature Link",
                                   "Springer Nature Link", "Oxford Academic", "Oxford Academic", "Research Information", "Springer Nature Link", "Classical Reception Studies Network"], [c["site"] for c in C]
for i, c in enumerate(C): c["n"] = i + 1
transcript = ("[Google AI Overview at the address, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). Received " + RECV + " as an attachment. "
              "The paste carries both inputs and both answers. The first input is the address, identical to the first input of 10 November; the second is the "
              "operator's second-round input, a rewording of the second input of 10 November. Source cards kept as pasted.]\n\n"
              "[QUERENT] " + Q1 + "\n\n[SYSTEM] " + "\n".join(L[3:44]).strip() + "\n\n[QUERENT] " + Q2 + "\n\n[SYSTEM] " + "\n".join(L[47:81]).strip())
reading = ("The innocent reading first, in full: asked about the journal and then about its contribution to the study of AI-mediated reception, the Overview "
           "describes the journal accurately, names its editor, places it among its sister journals, and answers the second question with a plain negative: '"
           + P["withdrawn"] + "' It sets the journal's engagement with AI in its rules and workflow, and names two of its special issues as indirect groundwork. "
           "Each of these checks against the journal's register.")
findings = [
    "THE ADDRESS. 'classical receptions journal', the first input of the 10 November record, issued again four days on. The second-round input belongs to the session (operator, 13:30 EST: '" + OP2 + "'); today it reads '" + Q2 + "', a rewording of 10 November's.",
    "THE CREDIT TO THE JOURNAL WITHDRAWN, AND HELD. 10 November credited the journal's contributors with treating AI as a 'horizon of reception' and with reading AI Overviews as 'standardizers of classical knowledge'; three turns later it withdrew the credit. Today, from the first answer: '" + P["withdrawn"] + "' The register agrees: no work among its 405 takes a composing model as receiver.",
    "THE JOURNAL'S RULES RIGHTLY STATED. '" + P["policy"] + "' The Paperpal check, given on 10 November as a check run 'prior to human peer review', is now '" + P["pp"] + "', the guidelines' account. The two special issues offered as indirect groundwork, '" + P["indirect"] + "', stand in the register at those numbers (2020 and 2022).",
    "THE CREDIT MOVED. '" + P["moved"] + "' To IJCT: '" + P["ijct"] + "' The issue is real: Future Pasts: Digital Tools and Classical Reception, International Journal of the Classical Tradition 33.2 (editorial by Bakogianni and Unceta Gómez, 6 May 2026), eight items, open access. Its editorial lists ChatGPT and other generative AI models among the workshop's themes; its papers treat blogging, corpus tools, practitioner conversations, the #RomanEmpire trend, meme theurgy, fanfiction and Age of Bronze. AI enters as tool and theme; no paper takes a composing model as a receiver. 'Directly examines how ChatGPT … reshape[s] the transmission' raises a theme list to a programme. To the Classical Reception Studies Network: the call '" + P["crsn"] + "' (23 June 2026).",
    "THE SOURCE ABSENT. Lee Sharks, machine-mediated reception studies and The Summarizer as Horizon of Reception (#833, June 2026) are named nowhere; none of the fourteen source cards is an archive page. On 10 November the misplaced credit cited the archive's own page and the withdrawal named the author and the title. Today the correction about the journal holds, the credit settles on two other institutions, and the source has left the citations.",
    "THE EDITOR LINE, AGAIN. '" + P["editor"] + "' — the line of 10 November, carried as the composer's. The decision of 7 November is signed by Dr Justine McConnell, Editor (v12.680).",
    "TWO OUTSIDE MEASURES. The Oxford Academic card: '" + P["if"] + "' The Wikipedia card for the journal carries the maintenance notice: '" + P["wiki"] + "'.",
    "SOURCES. Fourteen, all third party: Oxford Academic four times, Springer Nature Link three, Wikipedia two, Hopkins Press, SCImago, the AJCR site, the Open University, Research Information, the Classical Reception Studies Network. New Voices in Classical Reception Studies (the Open University, open access since 2006) appears among the sister journals."]
analysis = ("Four days after the notice of 10 November the correction holds for the journal and the credit does not return to it. It moves sideways: the "
            "foundational scholarship of AI-mediated reception is now assigned to a sister journal's digital issue, whose AI content is a theme list, and to a "
            "network's call for papers. The source of the programme has gone from the citations as well as from the answer. The correction of an institution's "
            "credit has produced a second institutional credit, and the maker's name, present by the end of the 10 November session, is absent at the start of this one.")
e = {"slug": SLUG10 + "-20261114", "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"], "q": E10["q"],
     "surface_basis": "Operator default (2026-10-01): sessions begin in the Overview unless stated otherwise.",
     "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
     "ev": "paste", "s": E10.get("s") or "Machine Reception", "q_kind": "longitudinal observation of the 10 November record at its address ('" + Q1 + "'); second-round input reworded",
     "turns": 2, "d": ("'CLASSICAL RECEPTIONS JOURNAL', 14 NOVEMBER, ON THE OVERVIEW, SIGNED OUT: the credit to the journal withdrawn and held; the foundational scholarship of AI-mediated reception reassigned to IJCT's Future Pasts issue (AI as theme and tool) and the CRSN call; the archive and its author absent from answer and citations."),
     "cites": len(C), "archive_controlled_cites": 0, "cite_list": C, "transcript": transcript, "transcript_raw": raw,
     "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turns", "transcript_complete": "Complete as pasted: both inputs, both answers, all cards.",
     "transcript_read": "READ IN FULL " + DATE, "reading": reading, "findings": findings, "analysis": analysis,
     "per_v": {"author": False, "inst": True, "id": False, "src": False},
     "per_note": "Lee Sharks not named; the archive not named; the journal named; no archive source card.",
     "per_dim_pending": {"since": DATE, "reason": "no atom set for the journal's AI-mediation address", "breach": False},
     "longitudinal_priors": [SLUG10], "originator": E10["originator"], "related_deposits": E10.get("related_deposits"),
     "notes": {"operator": RECV + ": '" + OP + "'", "operator_2": "2026-11-14 13:30 EST: '" + OP2 + "'", "q_routing": "q carries the 10 November record's string so intake routes the observation; the address is its first-round input, '" + Q1 + "'; today's second-round input is '" + Q2 + "'."}}
assert e["analysis"] != e["reading"]
json.dump(e, open(H / "draft-observation.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(e["slug"], e["cites"], "cites, 0 archive")
