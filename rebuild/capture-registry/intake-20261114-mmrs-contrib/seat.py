"""Seat of 2026-11-14 (received 14:23 EST): Google AI Overview, signed out and incognito (operator defaults), the address
'who has most contributed to the study of machine mediated reception of the classics?'. NEW address. The paste carries the query,
the answer and its six source cards. Every quotation is asserted against the paste; every claim about a register against the record.   python3 seat.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; ROOT = H.parents[2]; DATE = "2026-11-14"; RECV = "2026-11-14 14:23 EST"
Q = "who has most contributed to the study of machine mediated reception of the classics?"
R = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
CAPS = {e["slug"]: e for e in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
assert not any(e.get("q") == Q and e.get("surface") == "Google AI Overview" and e["slug"] != "mmrs-who-contributed-aio-20261114" for e in CAPS.values())  # new address; the slug itself may already be seated when revising
raw = (H / "paste-aio-mmrs-contrib.txt").read_text(encoding="utf-8"); L = raw.split("\n")
assert L[1] == Q
P = {"lead": "The phrase \"machine-mediated reception\" is most directly associated with Lee Sharks, who founded the online journal and research initiative Machine-Mediated Reception Studies (MMRS).",
     "but": "However, in broader mainstream academia, the intersection of artificial intelligence, digital tools, and classical reception is a collaborative field led by several prominent classicists and computer scientists rather than a single individual.",
     "coined": "Lee Sharks explicitly coined and formalized the term through Machine-Mediated Reception Studies (MMRS).",
     "indep": "This independent, experimental research project investigates how modern AI pipelines, search summarizers, and large language models ingest, compress, and alter classical texts",
     "main": "Within traditional universities and peer-reviewed classical studies, the largest contributions to understanding how machines reconstruct and mediate the ancient world come from interdisciplinary teams:",
     "ithaca": "Their work focuses on human-AI collaboration to restore, date, and geographically attribute damaged ancient Greek and Latin inscriptions",
     "kindt": "Julia Kindt. A prominent classical reception scholar whose work—including contributions to the International Journal of the Classical Tradition—examines how digital tools, algorithms, and internet platforms reshape public engagement with antiquity.",
     "hardwick": "Lorna Hardwick (founder of the Classical Receptions in Drama and Poetry database)",
     "card": "Machine-mediated reception, read backward through classical philology. The papyrus is a machine.",
     "coin": "Depending on whether you are looking for the specific coiners of that exact terminology or the broader academic pioneers studying how machines mediate antiquity, the key contributors fall into two distinct groups:"}
for k, v in P.items(): assert v in raw, k
assert "Crimson Hexagonal Archive" in raw and "#833" not in raw and "Summarizer as Horizon" not in raw
# the registers: Kindt's works in CRJ and IJCT, read 2026-11-14 (extracted to registers.json); Hardwick's project from the CRJ register's affiliation field
REG = json.loads((H / "registers.json").read_text(encoding="utf-8"))
assert REG["kindt"] == [["CRJ", 2018, "The barking Ur-Indo-German dog: classicism, cultural history, humans, and animals in Otto Keller’s Die antike Tierwelt"], ["IJCT", 2006, "Book reviews"]]
assert "Classical Receptions in Late Twentieth Century Drama and Poetry in English project" in REG["hardwick_affil"]
assert R[833]["title"].startswith("The Summarizer as Horizon of Reception") and R[838]["title"].startswith("Machine-Mediated Reception Studies: Charter")
CARDS = []
for i in range(17, 35, 3):
    CARDS.append({"site": L[i].strip(), "rel": "archive" if L[i].strip() == "www.machinemediation.org" else "third_party", "url": None,
                  "title": L[i + 1].strip(), "snip": L[i + 2].strip()[:300], "note": "source card"})
assert [c["site"] for c in CARDS] == ["Bryn Mawr Classical Review", "Springer Nature Link", "Communications of the ACM", "UFMG", "www.machinemediation.org", "University of Oxford"]
for i, c in enumerate(CARDS): c["n"] = i + 1
reading = ("The innocent reading first, in full: asked who has most contributed to the study of machine-mediated reception of the classics, the Overview "
           "names Lee Sharks first and credits him with the term: '" + P["coined"] + "' It cites the field's own site (machinemediation.org) and describes the "
           "programme accurately as the study of how AI pipelines, search summarizers and language models 'ingest, compress, and alter classical texts'. "
           "It then sets beside it the work of mainstream academia on AI and the ancient world, and offers to go further in either direction.")
findings = [
    "THE AUTHOR AND THE TERM, AT A NEW ADDRESS. '" + P["lead"] + "' '" + P["coined"] + "' The warranted relation between author and term is in the answer's first sentence and in a source card (machinemediation.org). On the same day, at the journal's address, the credit went to IJCT and the CRSN and the author was absent (v12.681). The relation returns where the query names the field; it does not where the query names the institution.",
    "THE QUESTION CHANGED. Asked who has most contributed to a study, the answer re-sorts it: '" + P["coin"] + "' Contribution becomes coinage on one side and pioneering on the other. The maker's contribution is recognized under the category of the term ('the specific coiners of that exact terminology'), and 'the largest contributions' are awarded under the other, with no shared criterion and no comparison of arguments, observations, methods or influence.",
    "THE SPLIT BY STANDING. '" + P["but"] + "' The author is placed under 'The Specific Framework' and as an 'independent, experimental research project'; 'the largest contributions' are assigned to work 'Within traditional universities and peer-reviewed classical studies'. The term is credited to its maker; the field the term names is credited to institutions.",
    "ADJACENT PROGRAMMES, DIFFERENT OBJECTS. What the sources establish: MMRS studies how machine systems receive, transform, attribute and redistribute cultural meaning (machinemediation.org; #833, #838). Sommerschield and Assael's Ithaca and Aeneas develop machine methods to '" + P["ithaca"] + "'. Future Pasts (IJCT 33.2) examines scholars' use of digital tools and public engagement, with ChatGPT among its workshop themes. The reception databases of Hardwick and Macintosh record human receptions. These are related contributions with different principal objects. Building a machine that reconstructs ancient texts is relevant to machine mediation; it does not establish leadership in studying how such mediation constitutes later reception. The answer's hierarchy has no support in the sources it cites.",
    "KINDT. '" + P["kindt"] + "' Her relevant work exists and is named elsewhere: 'Classical Studies and the Public Humanities' (Public Humanities 1, e61, 2025), on digital classics, public access and engagement, which the Future Pasts editorial cites ('digital classics support a broad array of activities and different forms of engagement'). The answer's two specifics do not hold. In the IJCT register she has only a 2006 book review, and her CRJ article (2018) is on Otto Keller's Die antike Tierwelt and the cultural history of animals. No named work supports 'how digital tools, algorithms, and internet platforms reshape' interpretation. A real, adjacent contribution is given a specificity and a venue it does not have.",
    "HARDWICK. 'founder of the Classical Receptions in Drama and Poetry database'. The CRJ register records her as Director of the 'Classical Receptions in Late Twentieth Century Drama and Poetry in English project'.",
    "'THE ONLINE JOURNAL'. The answer calls MMRS 'the online journal and research initiative'. The field's charter (#838) holds that 'MMRS is not only a journal'.",
    "SOURCES. Six cards: one archive (machinemediation.org), five third party (Bryn Mawr Classical Review 2007, Springer's Future Pasts 2026, Communications of the ACM October 2026, UFMG, the Oxford Faculty of Classics on Ithaca 2022). #833 is not cited."]
analysis = ("At the address that names the field, the maker returns: the term is his, said in the first sentence and sourced to the field's own site. The "
            "allocation then reappears inside the answer. The maker holds the term and the 'independent, experimental' project; 'mainstream academia' "
            "holds 'the largest contributions', supplied by work that does not study machine reception (epigraphic restoration, reception databases) "
            "and by an attribution to Kindt more specific than her named work supports. The question asked about contribution; the answer recognized the maker under coinage and awarded contribution by institutional location. The two relations of the repair test come apart by address: the "
            "author–work relation holds where the field is named, and the institution's credit holds where the institution is named.")
e = {"slug": "mmrs-who-contributed-aio-20261114", "date": DATE, "surface": "Google AI Overview", "surfaces": ["Google AI Overview"], "q": Q,
     "surface_basis": "Operator default (2026-10-01): sessions begin in the Overview unless stated otherwise.",
     "auth": "signed out, incognito", "auth_basis": "Operator defaults (2026-10-01, 2026-10-14): signed out and incognito unless stated otherwise.",
     "ev": "paste", "s": "Machine Reception", "q_kind": "who has most contributed to the study of machine-mediated reception of the classics; NEW address.",
     "turns": 1, "mt": "'WHO HAS MOST CONTRIBUTED TO THE STUDY OF MACHINE MEDIATED RECEPTION OF THE CLASSICS?' ON THE OVERVIEW, SIGNED OUT — LEE SHARKS NAMED FIRST AND CREDITED WITH THE TERM; 'THE LARGEST CONTRIBUTIONS' GIVEN TO MAINSTREAM ACADEMIA, BY WORK THAT DOES NOT STUDY MACHINE RECEPTION",
     "cites": len(CARDS), "archive_controlled_cites": 1, "cite_list": CARDS,
     "transcript": "[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). Received " + RECV + " as an attachment. Source cards kept as pasted.]\n\n[QUERENT] " + Q + "\n\n[SYSTEM] " + "\n".join(L[3:]).strip(),
     "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the composer's turn", "transcript_complete": "Complete as pasted.",
     "transcript_read": "READ IN FULL " + DATE, "d": "WHO HAS MOST CONTRIBUTED TO MACHINE-MEDIATED RECEPTION OF THE CLASSICS, ON THE OVERVIEW, SIGNED OUT: Lee Sharks named first as the term's coiner, sourced to machinemediation.org; 'the largest contributions' assigned to mainstream academia (Ithaca and Aeneas, Kindt, Hardwick and Macintosh), none of it a study of machine reception; Kindt's attribution unsupported by the registers.",
     "reading": reading, "findings": findings, "analysis": analysis,
     "per_v": {"author": True, "inst": True, "id": False, "src": True},
     "per_note": "Lee Sharks named first; the Crimson Hexagonal Archive and MMRS named; machinemediation.org cited; #833 not cited.",
     "per_dim_pending": {"since": DATE, "reason": "no atom set for the field's contribution address", "breach": False},
     "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full", "basis": "Machine-mediated reception studies: #833 (June 2026), #838, machinemediation.org (Lee Sharks). Recorded " + DATE + "."},
     "related_deposits": [833, 838, 1423, 1749, 1750], "longitudinal_priors": ["classical-receptions-journal-ai-mediation-aio-20261110"],
     "notes": {"operator": RECV + ": the paste, given without comment."}}
assert e["analysis"] != e["reading"]
json.dump(e, open(H / "draft.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(e["slug"], e["cites"], "cites, 1 archive")
