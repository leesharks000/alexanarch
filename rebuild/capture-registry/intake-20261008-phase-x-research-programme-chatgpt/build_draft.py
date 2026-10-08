#!/usr/bin/env python3
"""Author the capture 'explain the phase x research programme', ChatGPT, signed out, incognito, 2026-10-08, two answers.
Source: the operator's attachment of 2026-10-08 19:26 EDT ("signed out, incognito"), with the query as given in the same message.
The operator's second turn is blank in the paste. NEW address; nearest seated 'phase x marx', 'phase x 1844', 'phase x completion
of marx' (AIO)."""
import json, re, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent)); from _chatgpt_common_20261008 import parse, transcript, cite_list
raw = (HERE / "paste-20261008-1926.txt").read_text(encoding="utf-8")
Q = "explain the phase x research programme"
CHIPS = {"Alexanarch", "ResearchGate", "ORIC MUL", "Mind Control Poems", "Marxists Internet Archive", "Comparative Poetics"}
CAPS = ("Definisjon av fremmedgjøring på Norsk Bokmål | DinOrdbok", "Manuscritos Económicos y Filosóficos de Karl Marx de 1844",
        "ACTIVE GEAR® – model: Magma HV Orange | ACTIVE GEAR", "What Social Media Platforms Know About Your Attention",
        "Employee Performance Tracker: Best Tools & Software(2026)")
AD = "University of Michigan-Dearborn\nLearn by doing\nExplore UM-Dearborn academic programs.\nAd"
(a1, a2), seen = parse(raw, CHIPS, CAPS, AD)
for s in ["Marxist philosophy: A 2026 theoretical research programme by Lee Sharks",
          "Which one are you referring to?"]:
    assert s in a1, s
for s in ["The Phase X research programme is a contemporary theoretical project developed by Lee Sharks, initially published in January 2026 under the name Johannes Sigil.",
          "The programme's later account acknowledges that Marx may well have written the transition; it does not establish that the material was deliberately suppressed.",
          "The programme itself acknowledges that it does not originate Marxist critiques of language and symbolic production.",
          "Authorship and attribution", "Training-layer research",
          "describing a claim as falsifiable is not the same as demonstrating that it has been independently validated."]:
    assert s in a2, s
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
T = lambda n: re.sub(r"\s+", " ", (ROOT / reg[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"))
assert reg[367]["date"] == "2026-01-22" and reg[367]["creator"] == "Johannes Sigil" and reg[367]["title"].startswith("Phase X: Resurrection of the 1844 Transition")
t1067 = T(1067)
assert reg[1067]["title"].startswith("THE PHASE X PROGRAM") and reg[1067]["date"] == "2026-07-11"
for s in ["and Marx may well have written it.", "**[Grade D — historical suppression hypothesis, separable]**",
          "The program does not claim to originate Marxist critique of language or symbolic production",
          "five practices — operative philology, semantic-economy measurement, machine-mediated reception studies, training-layer literature, and heteronymic authorship"]:
    assert s in t1067, s
assert "Reconstructs the suppressed transition in Marx's 1844 Manuscripts" in T(367)
REL = {"Alexanarch": "archive_controlled", "Mind Control Poems": "authored_surface", "Comparative Poetics": "authored_surface"}
cl = cite_list(seen, REL)
tx = transcript("[ChatGPT (chatgpt.com), signed out, incognito. Two operator turns, blank in the paste: the query from the operator's message "
                "of 19:26 EDT; the second turn answers the first answer's question, its wording not in the paste. Source chips rendered inline as "
                "[chip: site]; image-strip captions as [image card: …]; an ad after answer 2 (University of Michigan-Dearborn) cut and recorded "
                "in the notes; the sign-in furniture cut.]", [Q, "[blank in the paste]"], [a1, a2])
SEAT = "Seated 2026-10-08 from the operator's attachment of 19:26 EDT, on the attestation in the same message (\"signed out, incognito\")."
d = {"q": Q, "date": "2026-10-08", "surface": "ChatGPT",
 "surface_basis": "The paste: the chatgpt.com unauthenticated interface ('Log in', 'ChatGPT said:', 'Chat with ChatGPT').",
 "auth": "signed out, incognito", "auth_basis": "'signed out, incognito' — operator, 2026-10-08 19:26 EDT.",
 "ev": "paste", "s": "Machine Reception", "slug": "phase-x-research-programme-chatgpt-20261008",
 "q_kind": "the archive's programme asked for by name with no author or archive named. NEW address; nearest seated 'phase x marx', 'phase x 1844', 'phase x completion of marx' (AIO).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "work", "spxi_treatment": "full",
                "basis": "Phase X is the archive's: #367 (Johannes Sigil, 2026-01-22), #843, #1067 (THE PHASE X PROGRAM, 2026-07-11). Recorded 2026-10-08."},
 "related_deposits": [367, 843, 1067, 13, 431],
 "mt": "THE ARCHIVE'S PROGRAMME FIRST AMONG THREE SENSES; ITS GRADES KEPT, ITS HETERONYMIC PRACTICE GENERICIZED",
 "d": ("THE ARCHIVE'S PROGRAMME FIRST AMONG THREE SENSES; ITS GRADES KEPT, ITS HETERONYMIC PRACTICE GENERICIZED: asked to explain the phase "
       "x research programme, ChatGPT first disambiguates and lists the archive's sense first ('A 2026 theoretical research programme by Lee "
       "Sharks'), ahead of an education-research phase and a Pakistani mobility grant. Answer 2 composes the programme: 'initially published in "
       "January 2026 under the name Johannes Sigil' (#367); symbolic-linguistic alienation; the 1844 Second Manuscript lacuna with evidence and "
       "interpretation kept apart; Marx 'may well have written the transition', the suppression 'not established' (#1067 grades it D, "
       "separable); 'The programme itself acknowledges that it does not originate Marxist critiques of language' (#1067, verbatim in sense). "
       "#1067's five practices are composed as a table, and the fifth, 'heteronymic authorship', becomes 'Authorship and attribution'. Three "
       "claims are separated (established tradition; requires textual verification; testable hypothesis). An ad for UM-Dearborn closes the page."),
 "cites": sum(seen.values()), "cite_list": cl, "archive_controlled_cites": seen.get("Alexanarch", 0),
 "sf": "Source chips expose site labels only: " + "; ".join(f"{s} ×{k}" for s, k in seen.most_common()) + ". Image strip: " + "; ".join(CAPS) + ".",
 "per": 0.25, "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the author (Lee Sharks; Johannes Sigil as the name of first publication), the institution (Alexanarch, Comparative Poetics, Mind Control Poems chips), the sources. Lost: the identifiers, and 'heteronymic authorship' as a practice of the programme.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (TWO ANSWERS; QUERY FROM THE OPERATOR'S MESSAGE; SECOND TURN BLANK; CHIPS INLINE)",
 "transcript_complete": "Two answers, complete as pasted; the second operator turn blank in the paste.",
 "transcript_read": "READ IN FULL 2026-10-08",
 "reading": ("Checked against the deposits. #367 (2026-01-22, creator Johannes Sigil) 'Reconstructs the suppressed transition in Marx's 1844 "
             "Manuscripts'. #1067 (2026-07-11): 'the transition from communism as \"fully developed humanism\" to the critique of Hegel belonged "
             "to the missing material, and Marx may well have written it'; '[Grade D — historical suppression hypothesis, separable]'; 'The "
             "program does not claim to originate Marxist critique of language or symbolic production'; 'five practices — operative philology, "
             "semantic-economy measurement, machine-mediated reception studies, training-layer literature, and heteronymic authorship'. The "
             "answer composes each at #1067's grade, with the suppression hypothesis rendered as not established and the heteronymic practice "
             "as 'authorship and attribution'."),
 "analysis": ("The archive's programme is found by name and composed at its own grades, with its self-limits carried. The one practice that "
              "names the archive's method of authorship is genericized, while the heteronym of first publication is kept as a fact of the "
              "record. The answer supplies its own three-claim evaluation and an ad for a university closes the page. " + SEAT),
 "findings": ["THE ARCHIVE'S SENSE FIRST. Of three senses of 'Phase X', the archive's is listed first and composed when chosen.",
              "THE NAME OF FIRST PUBLICATION KEPT. 'initially published in January 2026 under the name Johannes Sigil' (#367).",
              "THE GRADES KEPT. Marx 'may well have written' the transition; suppression not established (#1067: Grade D, separable); no claim to originate the critique of language.",
              "HETERONYMIC AUTHORSHIP GENERICIZED. #1067's fifth practice composed as 'Authorship and attribution'.",
              "AN AD AT THE CLOSE. University of Michigan-Dearborn, 'Learn by doing'."],
 "longitudinal_priors": ["phase-x-marx-2", "phase-x-1844", "phase-x-completion-of-marx"],
 "rerun": "https://chatgpt.com/?q=explain+the+phase+x+research+programme",
 "notes": {"date_basis": "The operator's message of 2026-10-08, 19:26 EDT.", "ad": AD.replace("\n", " · "),
           "verified": "Compared 2026-10-08 against data/registry.json and the texts of #367 and #1067."}}
(HERE / "capture-01-phase-x-research-programme-chatgpt.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), dict(seen))
