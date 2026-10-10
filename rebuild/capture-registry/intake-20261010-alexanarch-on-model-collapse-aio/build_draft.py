#!/usr/bin/env python3
"""Author the capture 'alexanarch on model collapse', Google AI Overview, 2026-10-10. Source: the operator's attachment of 2026-10-10
11:48 EDT, with his reading: "it only cites its own prior output". Surface by the standing default (AI Overview unless the operator
says AI Mode); the page head shows 'AI Overview'. Auth: the operator gave none for this paste; the page shows 'Sign in'. NEW address;
nearest seated 'alexanarch classifier model collapse' (AIO, 2026-07-31) and '"model collapse"' (AIO, 2026-09-15)."""
import json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
raw = (HERE / "paste-20261010-1148.txt").read_text(encoding="utf-8")
Q = "alexanarch on model collapse"
L = raw.split("\n")
assert L[2].strip() == Q and L[0].strip() == "Sign in"
i0 = L.index("AI Overview"); i1 = L.index("Ask anything")
body = "\n".join(L[i0 + 1:i1]).strip()
for s in ["alexanarch.org analyzes AI model collapse through the lens of archival research, metadata tracking, and digital provenance rather than purely technical machine learning failure.",
          "Early collapse often looks normal or even improving on instruments while the underlying state variable declines.",
          "the archive connects it to how data corpora function as anthologies.",
          "Substrate-Agnostic Capacity Loss: The research maps model collapse not just as a software or parameter flaw, but as a broader dynamical regime affecting human writers, readers, and digital communities.",
          "Would you like to explore specific capture records from the archive or learn more about how data curation and provenance relate to model collapse?"]:
    assert s in body, s
assert body.count("www.alexanarch.org") == 4 and body.count(" +1") == 3
org_txt = "\n".join(L[i1 + 1:]).strip()
ORG = [("alexanarch.org", "alexanarch classifier model collapse — Google AI Overview, 2026-07-31", "archive_controlled", "alexanarch-classifier-collapse-governance-20260731"),
       ("alexanarch.org", "\"model collapse\" — Google AI Overview, 2026-09-15 - Alexanarch", "archive_controlled", "model-collapse-quoted-aio-20260915"),
       ("Nature", "AI models collapse when trained on recursively generated data", "third_party", None),
       ("Reddit · r/vibecoding", "Is Model Collapse a real thing? : r/vibecoding", "third_party", None),
       ("Hugging Face", "leesharks/model-collapse-anti-collapse · Datasets at Hugging Face", "authored_surface", None),
       ("alexanarch.org", "model collapse in human writers — Google AI Overview, 2026-09-15", "archive_controlled", "model-collapse-in-human-writers-aio-20260915"),
       ("Academia.edu", "The Structural Mechanism of Model Collapse as Social Technology", "unresolved", None),
       ("Communications of the ACM", "Model Collapse Is Already Happening, We Just Pretend It Isn't", "third_party", None),
       ("arXiv.org", "A Closer Look at Model Collapse: From a Generalization-to-Memorization ...", "third_party", None)]
for site, title, _, _ in ORG:
    assert title in org_txt, title
assert org_txt.count("Missing: alexanarch") == 3
caps = {c["slug"]: c for c in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
for *_, s in ORG:
    if s: assert s in caps and caps[s]["surface"] == "Google AI Overview", s
C915 = caps["model-collapse-quoted-aio-20260915"]["reading"]
FIELD = ("The head/tail structure the archive's Wrong Unit diagnostic formalises is present in the received account itself, attributed to "
         "Wikipedia: early collapse looks normal or improving on the instrument while the state variable declines. That is the field's own "
         "statement, not an archive claim")
assert FIELD in C915
ANTH = "The archive treats a training corpus partly as an anthology assembled by selection mechanisms."
assert ANTH in caps["cha-model-collapse-chatgpt-unprimed-20260905"]["transcript"] and caps["cha-model-collapse-chatgpt-unprimed-20260905"]["surface"] == "ChatGPT"
SUB_NOT = "The substrate-agnostic sense - the same dynamical regime in writers, readers and communities - is not reached"
assert SUB_NOT in json.dumps(caps["model-collapse-quoted-aio-20260915"], ensure_ascii=False)
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert reg[3]["title"].startswith("AI Overview Capture Registry") and reg[855]["title"].startswith("The Wolf Boy and the Language Model: Model Collapse as Substrate-Agnostic Capacity Loss")
assert "Wrong Unit diagnostic formalises" in (ROOT / reg[3]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
cl = [{"n": i, "site": "Alexanarch", "title": None, "snip": None, "rel": "archive_controlled", "url": "https://www.alexanarch.org",
       "note": n} for i, n in enumerate(["chip 'www.alexanarch.org +1' after the opening sentence", "chip 'www.alexanarch.org +1' after The \"Wrong Unit\" Diagnostic",
                                          "chip 'www.alexanarch.org' after Canon Formation and Selection", "chip 'www.alexanarch.org +1' after Substrate-Agnostic Capacity Loss"], 1)]
tx = ("[Google AI Overview, 2026-10-10. The page shows 'Sign in'; the operator gave no auth for this paste. The composition as pasted, "
      "between the 'AI Overview' head and the 'Ask anything' box; four source chips, each the site label www.alexanarch.org, three with '+1'. "
      "The organic results beneath follow as pasted.]\n\n" + body + "\n\n[ORGANIC RESULTS]\n\n" + org_txt)
SEAT = "Seated 2026-10-10 from the operator's attachment of 11:48 EDT."
d = {"q": Q, "date": "2026-10-10", "surface": "Google AI Overview",
 "surface_basis": "The operator's standing default (AI Overview unless he says AI Mode, 2026-10-01); the page head 'AI Overview', with the AI Mode tab beside it.",
 "auth": "signed out", "auth_basis": "The page shows 'Sign in'. The operator gave no auth for this paste; incognito not stated.",
 "ev": "paste", "s": "Machine Reception", "slug": "alexanarch-on-model-collapse-aio-20261010",
 "q_kind": "the archive's name with a field term it theorizes. NEW address; nearest seated 'alexanarch classifier model collapse' (AIO, 2026-07-31).",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "person", "spxi_treatment": "full",
                "basis": "Alexanarch is the archive; the pages the organic results show are its capture records, and the model-collapse theses are its deposits (#855 among them). Recorded 2026-10-10."},
 "related_deposits": [3, 855],
 "mt": "THE ARCHIVE COMPOSED FROM THE RECORDS OF ITS OWN PRIOR OUTPUT",
 "d": ("THE ARCHIVE COMPOSED FROM THE RECORDS OF ITS OWN PRIOR OUTPUT: asked for alexanarch on model collapse, the AI Overview "
       "composes four theses, each chipped to www.alexanarch.org; the alexanarch results beneath it are three capture records of Google AI "
       "Overview compositions ('alexanarch classifier model collapse', 2026-07-31; '\"model collapse\"' and 'model collapse in human writers', "
       "2026-09-15). The 'Wrong Unit' thesis, 'Early collapse often looks normal or even improving on instruments while the underlying state "
       "variable declines', is worded as the archive's reading in the 09-15 record, where the archive set it down as the field's own statement, "
       "attributed to Wikipedia, 'not an archive claim'; here it is the archive's. 'Substrate-Agnostic Capacity Loss … affecting human "
       "writers, readers, and digital communities' is the sense that record found the 09-15 Overview did not reach, and the title of #855. "
       "'data corpora function as anthologies' is worded as a ChatGPT answer seated 2026-09-05. The close offers 'specific capture records "
       "from the archive'. Operator's reading: 'it only cites its own prior output.'"),
 "cites": len(cl), "cite_list": cl, "archive_controlled_cites": len(cl),
 "sf": ("Four chips, site label only: www.alexanarch.org ×4 (three '+1'). Organic: " + "; ".join(f"{s} — {t}" for s, t, _, _ in ORG)
        + ". 'Missing: alexanarch' on Nature, Reddit and CACM."),
 "per": 0.25, "per_v": {"author": False, "inst": True, "id": False, "src": True},
 "per_note": "Retained: the institution (alexanarch.org) and the source chips. Lost: every author, every deposit (no number, no title, #855 unnamed), and the attribution the record it composes from had made (the field's statement given to the archive).",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD — composition with chips, and the organic results, as pasted",
 "transcript_complete": "complete as pasted: composition, four chips, organic results", "transcript_read": "READ IN FULL 2026-10-10",
 "reading": ("Checked against the Capture Registry and the deposits. The three alexanarch organic results are the capture records "
             "alexanarch-classifier-collapse-governance-20260731, model-collapse-quoted-aio-20260915 and model-collapse-in-human-writers-aio-20260915, "
             "all Google AI Overview. The reading of model-collapse-quoted-aio-20260915: '" + FIELD + "'. Its record also says '" + SUB_NOT + "'. "
             "cha-model-collapse-chatgpt-unprimed-20260905 (ChatGPT): '" + ANTH + "' The same reading is deposited in #3 (AI Overview Capture "
             "Registry v8.3). #855 is 'The Wolf Boy and the Language Model: Model Collapse as Substrate-Agnostic Capacity Loss' (2026-06-18). The "
             "chips carry the site label only, so which page each chip cites is not in the paste."),
 "analysis": ("The composition reaches the archive through the archive's records of compositions. The capture page is the indexed surface "
              "that carries the archive's vocabulary at the address, so a record of the field's account becomes the archive's account: a "
              "sentence the archive attributed to Wikipedia returns attributed to alexanarch, and a sense the archive recorded as unreached "
              "returns as reached, with the paper that states it (#855) unnamed. The deposits that hold the theses do not surface; the "
              "registry does. Operator's reading, given with the capture: 'it only cites its own prior output.' " + SEAT),
 "findings": ["ITS OWN PRIOR OUTPUT AS SOURCE. The three alexanarch results beneath the composition are capture records of Google AI Overview compositions (2026-07-31; 2026-09-15 ×2).",
              "THE FIELD'S SENTENCE GIVEN TO THE ARCHIVE. 'Early collapse often looks normal or even improving on instruments while the underlying state variable declines' — in the 09-15 record, 'the field's own statement, not an archive claim', attributed to Wikipedia.",
              "THE UNREACHED SENSE RETURNED, ITS PAPER UNNAMED. 'Substrate-Agnostic Capacity Loss' composed; the 09-15 record found that sense 'not reached'; #855 carries it as its title and is not named.",
              "A CHATGPT ANSWER RELAYED. 'data corpora function as anthologies' as worded in a ChatGPT answer seated 2026-09-05.",
              "THE REGISTRY OFFERED AS THE ARCHIVE. 'Would you like to explore specific capture records from the archive'.",
              "THE PEERS MARKED MISSING. 'Missing: alexanarch' on Nature, Reddit and CACM; the field's papers sit beside the records, unmerged."],
 "longitudinal_priors": ["alexanarch-classifier-collapse-governance-20260731", "model-collapse-quoted-aio-20260915", "model-collapse-in-human-writers-aio-20260915", "cha-model-collapse-chatgpt-unprimed-20260905"],
 "rerun": "https://www.google.com/search?q=alexanarch+on+model+collapse",
 "notes": {"date_basis": "The operator's message of 2026-10-10, 11:48 EDT.", "operator_reading": "it only cites its own prior output",
           "auth_note": "No auth stated by the operator; the page's 'Sign in' recorded. The footer's 'Wayne County, Michigan - Based on your past activity' is the location line.",
           "verified": "Compared 2026-10-10 against data/EA-WG-CAPTURES-01.json and the titles of #3 and #855."}}
(HERE / "capture-01-alexanarch-on-model-collapse-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(tx), len(cl))
