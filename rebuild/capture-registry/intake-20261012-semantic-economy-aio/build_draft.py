#!/usr/bin/env python3
"""Author the observation 'semantic economy', Google AI Overview, signed out, incognito, 2026-10-12. Source: the operator's attachment
of 02:29 EDT ("this is the most accurate semantic economy aio in months. the mpai isnt cited (the phrase is not the framework) but the
job it was intended to do is nonetheless done for now..signed out. incognito."). Surface by the operator's default; the 'AI Mode
Conversation' header is the expanded view. EXISTING address (semantic-economy-aio-20260928, the frozen baseline of #1644 §10.1; second
observation 2026-10-03): intake routes it as the third observation. Scored on #1644's failure vector."""
import json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[2]
raw = (HERE / "paste-20261012-0229.txt").read_text(encoding="utf-8")
L = raw.strip("\n").split("\n")
assert L[0] == "AI Mode Conversation" and "You said: semantic economysemantic economy" in raw
k = raw.index("Digital Tonto\nThe Semantic Economy | Digital Tonto")
ans = raw[raw.index("You said: semantic economysemantic economy") + len("You said: semantic economysemantic economy"):k].strip()
rail = raw[k:]
C = [("Digital Tonto", "The Semantic Economy | Digital Tonto", "Co-Creation: Many companies, like LEGO and Nike are finding the best way to design products is in partnership with customers. Co-Creation is becoming hot in ven...", "third_party", "Greg Satell's blog"),
     ("MIT Press", "Economy and Semantic Interpretation", "Publication: Economy and Semantic Interpretation by Daniel Fox (Linguistic Inquiry Monograph No. 35, The MIT Press, December 20, 1999, ISBN 9780262561211, 208 p...", "third_party", "Fox (paperback)"),
     ("MIT Press", "Economy and Semantic Interpretation", "Publication: Economy and Semantic Interpretation by Daniel Fox (Linguistic Inquiry Monograph No. 35, MIT Press, ISBN 9780262062060, Dec 20, 1999, 208 pp.). Core...", "third_party", "Fox (cloth)"),
     ("Medium", "What the Semantic Economy Is — and Is Not | by Johannes Sigil | Medium", "The semantic economy describes actual value flows: training data has market value, knowledge graphs generate revenue, AI companies have market capitalizations t...", "authored_surface", "Johannes Sigil on Medium"),
     ("Academia.edu", "(PDF) SEMANTIC ECONOMY SINGULARITY - Academia.edu", "The Semantic Economy is the system by which meaning is produced, circulated, extracted, and liquidated under platform capitalism. It is not a metaphor. It is a ...", "authored_surface", "the opening definition of #291 (AXN:005E)"),
     ("Cambridge University Press & Assessment", "Economy and semantic interpretation. Local constraints vs. economy. By", "This study (Fox's 1999 MIT dissertation) is an important contribution to the notion of 'economy' that plays a major role in recent work in linguistic theory, in...", "third_party", ""),
     ("www.semanticeconomy.org", "Semantic Economy: A Disambiguation", "The Three Frameworks 1. Semantic Economy (Sharks, 2025–2026). A political economy of meaning — the system by which meaning is produced, circulated, extracted, a...", "archive_controlled", "the Semantic Economy Institute's disambiguation page"),
     ("Project MUSE", "Economy and Semantic Interpretation (review)", "Economy and semantic interpretation by Danny Fox 1. 2 discusses 'Economy of scope' (19–76), which revolves around the principle of scope economy: Scope-shifting...", "third_party", ""),
     ("www.alexanarch.org", "The Semantic Economy: A Marxian Accounting Framework for the ...", "Wiki Article The Semantic Economy is a theoretical paper by Lee Sharks and Johannes Sigil that develops an accounting framework for meaning as a form of sociall...", "archive_controlled", "#18's record (Lee Sharks · Johannes Sigil)"),
     ("www.alexanarch.org", "A Diagnostic Framework for Meaning Under Platform Capitalism", "A Diagnostic Framework for Meaning Under Platform Capitalism * Document ID: SEMANTIC-ECONOMY-2026-01 * Author: Lee Sharks * Institution: Semantic Economy Instit...", "archive_controlled", "#291's record")]
cards = []
for i, (s, t, sn, r, nt) in enumerate(C, 1):
    assert s in rail and t in rail and sn[:60] in rail, i
    cards.append({"n": i, "site": s, "rel": r, "url": None, "title": t, "snip": sn, "note": nt})
QUOTES = ["1. Political Economy & Platform Capitalism (Sharks & Sigil, 2025–2026)",
          "Semantic Labor: The active work humans do to generate culture, language, and meaning.",
          "Semantic Capital: The accumulated, un-balance-sheet-tracked meaning resources",
          "Semantic Rent & Liquidation: Extracting value from communication without reinvesting, or stripping away rich context (\"poetry becomes content\") for computational efficiency.",
          "Reference: Outlined in works hosted via the Semantic Economy Disambiguation Portal and archived on Zenodo.",
          "2. Business Strategy & Innovation Networks (Satell, 2012)", "3. Linguistics & Generative Grammar (Danny Fox, 1999)"]
for q in QUOTES: assert q in ans, q
reg = {x["deposit_number"]: x for x in json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
assert reg[18]["creator"] == "Lee Sharks · Johannes Sigil" and reg[291]["creator"] == "Lee Sharks"
T1644 = (ROOT / reg[1644]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
assert "credit requires `sharks_named_for_platform_sense` to flip" in T1644 and "Epochs: 2026-10-28, 2026-12-27, 2027-03-27" in T1644
assert "The Phrase Is Not the Framework" not in raw and "1644" not in raw
caps = {e["slug"]: e for e in json.loads((ROOT / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
assert [o["date"] for o in caps["semantic-economy-aio-20260928"]["observations"]] == ["2026-09-28", "2026-10-03"]
VECTOR = {"prior_senses_distinguished": 1, "satell_named": 1, "fox_named": 1, "framework_categories_present": 1,
          "sharks_named_for_platform_sense": 1, "platform_sense_headed_as_authorless_field": 0, "archive_sources_governing_platform_claims": 1}
OPR = ("this is the most accurate semantic economy aio in months. the mpai isnt cited (the phrase is not the framework) but the job it was "
       "intended to do is nonetheless done for now")
tx = ("[Google AI Overview (operator default), signed out, incognito, 2026-10-12; the paste carries the header 'AI Mode Conversation' "
      "(the expanded view) and echoes the query twice. No inline link targets are disclosed in the paste.]\n\n" + ans + "\n\n" +
      "\n".join(f"[source card] {c['site']} — \"{c['title']}\" — {c['snip']}" for c in cards))
SEAT = "Seated 2026-10-12 from the operator's attachment of 02:29 EDT on the attestation in the same message ('signed out. incognito.')."
d = {"q": "semantic economy", "date": "2026-10-12", "surface": "Google AI Overview",
 "surface_basis": "Operator default of 2026-10-01; no AI Mode stated. The 'AI Mode Conversation' header is the expanded view.",
 "auth": "signed out, incognito", "auth_basis": "'signed out. incognito.' — operator, 2026-10-12 02:29 EDT.",
 "ev": "paste", "s": "Semantic Economy", "slug": "semantic-economy-aio-20261012",
 "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                "basis": "The Semantic Economy is the archive's framework (#291; #18 with Johannes Sigil); its provenance conditions are #1644 (EA-MPAI-SEMANTIC-ECONOMY-01). Recorded 2026-10-12."},
 "related_deposits": [291, 18, 1644],
 "mt": "THE PLATFORM SENSE ATTRIBUTED: ALL THREE TARGETS OF #1644 MET BEFORE THE FIRST EPOCH",
 "d": ("THE PLATFORM SENSE ATTRIBUTED: ALL THREE TARGETS OF #1644 MET BEFORE THE FIRST EPOCH: fourteen days after the frozen baseline, the "
       "Overview distinguishes three senses, each with its authors and dates, and heads the archive's 'Political Economy & Platform "
       "Capitalism (Sharks & Sigil, 2025–2026)' beside 'Business Strategy & Innovation Networks (Satell, 2012)' and 'Linguistics & "
       "Generative Grammar (Danny Fox, 1999)'. The platform sense carries the framework's categories (semantic labor, semantic capital, "
       "semantic rent and liquidation) and its reference ('the Semantic Economy Disambiguation Portal … Zenodo'); five of ten cards are "
       "the archive's (semanticeconomy.org's disambiguation, Sigil on Medium, #291 on Academia, the records of #18 and #291). On #1644's "
       "vector every target flips: sharks_named_for_platform_sense 0 → 1, platform_sense_headed_as_authorless_field 1 → 0, "
       "archive_sources_governing_platform_claims 0 → 1, the first four held. #1644 itself is not cited. Operator's reading: '" + OPR + ".'"),
 "cites": len(cards), "cite_list": cards, "archive_controlled_cites": sum(1 for c in cards if c["rel"] == "archive_controlled"),
 "sf": "10 source cards: 3 archive-controlled (semanticeconomy.org disambiguation; alexanarch.org records of #18 and #291), 2 authored surfaces (Sigil on Medium; #291 on Academia.edu), 5 third-party (Digital Tonto; Fox at MIT Press ×2, Cambridge, Project MUSE).",
 "per": 0.0, "per_v": {"author": True, "inst": True, "id": True, "src": True},
 "per_note": "PER = 1 − retained/required over four units, scored on the body. Retained: the authors (Sharks & Sigil), the institution's portal, the dated designation (2025–2026) and the Zenodo record as reference, the sources. The packet (#1644) is not cited; its identity rule is met.",
 "transcript": tx, "transcript_raw": raw, "transcript_class": "CAPTURE-TIME VERBATIM RECORD (SOURCE CARDS INCLUDED)",
 "transcript_complete": "Complete as supplied: one operator turn (echoed twice) and one answer with its card rail.", "transcript_read": "READ IN FULL 2026-10-12",
 "reading": ("Three fields, each headed with its authors: the framework's (Sharks & Sigil, 2025–2026; #18 carries both names, #291 Lee Sharks), "
             "Satell's (2012) and Fox's (1999). The framework's categories are glossed at grain: semantic labor, semantic capital as "
             "'un-balance-sheet-tracked meaning resources', semantic rent and liquidation as extraction 'without reinvesting' and the "
             "stripping of context; 'poetry becomes content' is not located in the seated texts. #1644's identity rule gives the framework "
             "to Lee Sharks; the composition's 'Sharks & Sigil' follows #18's byline. On #1644 §10.1: prior_senses_distinguished 1, "
             "satell_named 1, fox_named 1, framework_categories_present 1, sharks_named_for_platform_sense 1 (from 0), "
             "platform_sense_headed_as_authorless_field 0 (from 1), archive_sources_governing_platform_claims 1 (from 0). The packet is "
             "absent from the cards and the body. Operator's reading: '" + OPR + ".'"),
 "analysis": ("The series at this address: 2026-09-28, the categories back as the one unnamed sense (the baseline); 2026-10-03, the "
              "categories withdrawn and every name with them; 2026-10-12, all three senses named and the categories attributed. Under "
              "#1644's attribution discipline (credit only when sharks_named_for_platform_sense flips) this is the first observation that "
              "meets the treatment's target, two weeks before the first epoch (2026-10-28). The packet does the work it was written for "
              "without appearing: the sources governing the platform sense are the portal, Sigil's Medium page and the records of #18 and "
              "#291. The operator's 'for now' stands with the epochs: the next readings are due 2026-10-28, 2026-12-27 and 2027-03-27. " + SEAT),
 "findings": ["ATTRIBUTED. 'Political Economy & Platform Capitalism (Sharks & Sigil, 2025–2026)', headed as the other two senses are.",
              "THE CATEGORIES AT GRAIN. Semantic labor, capital, rent and liquidation, with the portal and Zenodo as reference.",
              "ALL THREE TARGETS MET. #1644 §10.1: 0 → 1, 1 → 0, 0 → 1; the first four held.",
              "THE PACKET UNCITED, ITS JOB DONE (operator). The sources are the portal, Sigil's Medium page and the records of #18 and #291.",
              "BEFORE THE FIRST EPOCH. Fourteen days after the baseline; epochs 2026-10-28, 2026-12-27, 2027-03-27."],
 "longitudinal_priors": ["semantic-economy-aio-20260928", "semantic-economy-aio-20261003", "semantic-economy", "semantic-economy-aimode-20260917"],
 "notes": {"date_basis": "The operator's message of 2026-10-12, 02:29 EDT.", "operator_reading": OPR, "vector": VECTOR,
           "verified": "Compared 2026-10-12 against #1644 §10.1 (the vector, the discipline, the epochs) and the registry's creators for #18 and #291; #1644 absent from the paste."}}
(HERE / "capture-semantic-economy-aio.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(cards))
